"""Run a batch of DeepSeek requests through OpenRouter: the Batch API (default) or live chat calls.

Usage: deepseek_batch.py <jobs.jsonl> <results.jsonl> [--mode batch|live] [--provider deepinfra/fp8]
                         [--model deepseek/deepseek-v4.1-flash] [--workers 6]
Batch mode submits one job to POST /api/v1/batches, saves the batch id next to results.jsonl
(<results>.batch.json) so a rerun resumes polling instead of resubmitting, and saves the raw final
status JSON (<results>.raw.json) for inspection.
jobs.jsonl lines: {"id": str, "prompt": str, "images": [png paths], "max_tokens": int (optional)}
results.jsonl lines: {"id", "status": "ok"|"error", "content", "usage", "error"}
Resumable: ids already in results.jsonl with status ok are skipped. Each result is appended
as soon as it arrives, so an interrupted run loses nothing.
The key is read from OPENROUTER_API_KEY or opus_attempt/.env (git-ignored); it is never printed.
"""
import argparse, base64, json, mimetypes, os, sys, threading, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = "https://openrouter.ai/api/v1/chat/completions"
BATCH_URL = "https://openrouter.ai/api/v1/batches"
TERMINAL = {"completed", "failed", "expired", "cancelled"}


def api_key():
    if os.environ.get("OPENROUTER_API_KEY"):
        return os.environ["OPENROUTER_API_KEY"]
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"')
    sys.exit("OPENROUTER_API_KEY not set and not in .env")


def provider_block(provider):
    # Pinned so every request runs on the same weights/quantization; no silent fallback elsewhere.
    return {"only": [provider], "allow_fallbacks": False}


def build_messages(job):
    content = [{"type": "text", "text": job["prompt"]}]
    for img in job.get("images", []):
        mime = mimetypes.guess_type(img)[0] or "image/png"
        b64 = base64.b64encode(Path(img).read_bytes()).decode()
        content.append({"type": "image_url", "image_url": {"url": "data:%s;base64,%s" % (mime, b64)}})
    return [{"role": "user", "content": content}]


def build_body(job, model, provider):
    return {"model": model, "provider": provider_block(provider), "messages": build_messages(job),
            "max_tokens": job.get("max_tokens", 8000), "temperature": 0,
            "usage": {"include": True}}


def call(job, model, provider, key, retries=3):
    body = json.dumps(build_body(job, model, provider)).encode()
    last = ""
    for attempt in range(retries):
        req = urllib.request.Request(URL, data=body, headers={
            "Authorization": "Bearer " + key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.load(r)
            if "choices" not in d:
                raise ValueError("no choices: %s" % json.dumps(d)[:300])
            return {"id": job["id"], "status": "ok", "content": d["choices"][0]["message"]["content"],
                    "finish_reason": d["choices"][0].get("finish_reason"), "usage": d.get("usage")}
        except (urllib.error.URLError, ValueError, TimeoutError) as e:
            detail = e.read().decode()[:300] if isinstance(e, urllib.error.HTTPError) else ""
            last = "%s %s" % (e, detail)
            # 4xx other than rate limits will not get better on retry.
            if isinstance(e, urllib.error.HTTPError) and e.code < 500 and e.code != 429:
                break
            time.sleep(5 * (attempt + 1))
    return {"id": job["id"], "status": "error", "error": last}


def http_json(method, url, key, payload=None):
    data = json.dumps(payload, ensure_ascii=False).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit("%s %s -> HTTP %s: %s" % (method, url, e.code, e.read().decode()[:500]))


def result_from_batch_item(item):
    """Map one batch result item to the live-mode result shape. The item layout is not documented
    in what we verified, so accept the two common shapes and fail loudly on anything else."""
    rid = item.get("custom_id") or item.get("id")
    resp = item.get("response") or {}
    body = resp.get("body") if isinstance(resp.get("body"), dict) else resp
    if body.get("choices"):
        ch = body["choices"][0]
        return {"id": rid, "status": "ok", "content": ch["message"]["content"],
                "finish_reason": ch.get("finish_reason"), "usage": body.get("usage")}
    return {"id": rid, "status": "error", "error": "unrecognised result item: %s" % json.dumps(item)[:300]}


def run_batch(jobs, a, key):
    state = Path(a.results + ".batch.json")
    if state.exists():
        batch_id = json.load(open(state))["id"]
        print("resuming batch", batch_id, flush=True)
    else:
        # OpenRouter parses this body as a stream: endpoint, model and provider must precede requests.
        payload = {"endpoint": "/v1/chat/completions", "model": a.model,
                   "provider": provider_block(a.provider),
                   "requests": [{"custom_id": j["id"], "body": {
                       "messages": build_messages(j), "max_tokens": j.get("max_tokens", 8000),
                       "temperature": 0}} for j in jobs]}
        d = http_json("POST", BATCH_URL, key, payload)
        batch_id = d["id"]
        json.dump({"id": batch_id, "submitted": time.strftime("%Y-%m-%dT%H:%M:%S"), "n": len(jobs)}, open(state, "w"))
        print("submitted batch %s (%d requests)" % (batch_id, len(jobs)), flush=True)
    while True:
        d = http_json("GET", "%s/%s" % (BATCH_URL, batch_id), key)
        print("status=%s counts=%s" % (d.get("status"), d.get("request_counts")), flush=True)
        if d.get("status") in TERMINAL:
            break
        time.sleep(a.poll)
    json.dump(d, open(a.results + ".raw.json", "w"), ensure_ascii=False, indent=1)
    items = d.get("results") or []
    if not items:
        sys.exit("batch ended with status %s and no inline results; see %s.raw.json" % (d.get("status"), a.results))
    with open(a.results, "a", encoding="utf-8") as out:
        res = [result_from_batch_item(it) for it in items]
        for r in res:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    errors = sum(r["status"] != "ok" for r in res)
    usage = [r.get("usage") or {} for r in res]
    print("done: results=%d errors=%d prompt_tokens=%d completion_tokens=%d cost_usd=%.4f" % (
        len(res), errors, sum(u.get("prompt_tokens") or 0 for u in usage),
        sum(u.get("completion_tokens") or 0 for u in usage), sum(u.get("cost") or 0 for u in usage)))
    # The batch is finished either way; drop the state so the next run submits only what is missing.
    state.unlink()
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jobs")
    ap.add_argument("results")
    ap.add_argument("--model", default="deepseek/deepseek-v4.1-flash")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--mode", choices=["batch", "live"], default="batch")
    ap.add_argument("--provider", default="deepinfra/fp8")
    ap.add_argument("--poll", type=int, default=30, help="seconds between batch status checks")
    a = ap.parse_args()

    key = api_key()
    jobs = [json.loads(l) for l in open(a.jobs) if l.strip()]
    done = set()
    if Path(a.results).exists():
        done = {r["id"] for r in map(json.loads, open(a.results)) if r.get("status") == "ok"}
    todo = [j for j in jobs if j["id"] not in done]
    print("jobs=%d already_ok=%d to_run=%d model=%s provider=%s mode=%s" % (
        len(jobs), len(done), len(todo), a.model, a.provider, a.mode), flush=True)
    if not todo and not Path(a.results + ".batch.json").exists():
        return
    if a.mode == "batch":
        sys.exit(1 if run_batch(todo, a, key) else 0)

    lock = threading.Lock()
    totals = {"cost": 0.0, "prompt": 0, "completion": 0, "errors": 0}
    with open(a.results, "a", encoding="utf-8") as out:
        def run(job):
            res = call(job, a.model, a.provider, key)
            with lock:
                out.write(json.dumps(res, ensure_ascii=False) + "\n")
                out.flush()
                u = res.get("usage") or {}
                totals["cost"] += u.get("cost") or 0
                totals["prompt"] += u.get("prompt_tokens") or 0
                totals["completion"] += u.get("completion_tokens") or 0
                totals["errors"] += res["status"] != "ok"
                print("%s %s" % (res["id"], res["status"] if res["status"] == "ok" else res["error"][:200]), flush=True)
        with ThreadPoolExecutor(a.workers) as ex:
            list(ex.map(run, todo))
    print("done: errors=%d prompt_tokens=%d completion_tokens=%d cost_usd=%.4f" % (
        totals["errors"], totals["prompt"], totals["completion"], totals["cost"]))
    sys.exit(1 if totals["errors"] else 0)


if __name__ == "__main__":
    main()
