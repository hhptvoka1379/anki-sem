// Gate 8: runs each saved back-side HTML in jsdom WITH its scripts and reports
// whether "Risposta accettata" is visible, plus what assets/typed_answer.js
// itself computes from Anki's comparison block.
// Usage: node typed_check.js <cases.json>   (writes JSON results to stdout)
// cases: [{name, html, main, accepted}]
const { JSDOM, VirtualConsole } = require("jsdom");
const path = require("path");
const typed = require(path.resolve(__dirname, "../../assets/typed_answer.js"));

function visibleText(win, needle) {
  const doc = win.document;
  const walker = doc.createTreeWalker(doc.body, 4 /* SHOW_TEXT */);
  let n;
  while ((n = walker.nextNode())) {
    if (n.textContent.includes(needle)) {
      let el = n.parentElement, hidden = false;
      while (el) {
        const cs = win.getComputedStyle(el);
        if (cs.display === "none" || cs.visibility === "hidden" || el.hasAttribute("hidden")) { hidden = true; break; }
        el = el.parentElement;
      }
      if (!hidden) return true;
    }
  }
  return false;
}

(async () => {
  const cases = JSON.parse(require("fs").readFileSync(process.argv[2], "utf8"));
  const out = [];
  for (const c of cases) {
    const errors = [];
    const vc = new VirtualConsole();
    vc.on("jsdomError", (e) => errors.push(String(e.message || e)));
    const dom = await require("jsdom").JSDOM.fromFile(c.html, {
      runScripts: "dangerously", pretendToBeVisual: true, virtualConsole: vc,
      url: "file://" + path.resolve(c.html),
    });
    await new Promise((r) => setTimeout(r, 150));
    const w = dom.window;
    const el = w.document.getElementById("typeans");
    const typedText = typed.typedFrom(el);
    out.push({
      name: c.name,
      typeans_found: !!el,
      typed_read: typedText,
      matcher_accepts: typed.accepted(typedText, c.main, c.accepted || ""),
      accepted_shown: visibleText(w, "Risposta accettata"),
      script_errors: errors,
    });
    w.close();
  }
  console.log(JSON.stringify(out));
})();
