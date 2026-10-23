"""Convert the 2,055 `completamento` notes to a real Cloze note type (typed).

Design
------
* The new note type clones the protobuf config of an existing, unused cloze
  note type (1481924269089, 0 notes), so kind=1 / req / latex settings are
  byte-identical to a model Anki already accepts.
* The 17 field names are kept exactly, so `notes.flds` needs no re-shaping:
  only field 8 (FrontStemHTML) is rewritten, each `<span class="blank-slot">`
  becoming `{{cN::answer}}`, answers taken in order from the
  `<span class="blank-filled">` spans in field 9.
* Cards: the old unreviewed card is reused for c1; extra clozes get fresh ids.
* Every other note stays byte-identical; the input is never opened read-write.
"""
import json
import os
import re
import shutil
import sqlite3
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
import common as C

DONOR_MID = 1481924269089           # Cloze-Brosencephalon, 0 notes; id reused
NEW_NAME = "Semestre Filtro — Completamento (cloze)"
STEM, BACKSTEM = 8, 9

SLOT = re.compile(r'<span class="blank-slot">.*?</span>', re.S)
FILL = re.compile(r'<span class="blank-filled">(.*?)</span>', re.S)

Q_FORMAT = (
    '<div class="sf-card">'
    '<div class="sf-stem">{{cloze:FrontStemHTML}}</div>'
    '<div class="sf-typed">{{type:cloze:FrontStemHTML}}</div>'
    '<div class="sf-image">{{QuestionScanHTML}}</div>'
    '</div>'
)
A_FORMAT = (
    '<div class="sf-card">'
    '<div class="sf-stem">{{cloze:FrontStemHTML}}</div>'
    '<div class="sf-typed">{{type:cloze:FrontStemHTML}}</div>'
    '<div class="sf-image">{{QuestionScanHTML}}</div>'
    '<div class="sf-answer">{{AnswerBannerHTML}}</div>'
    '{{#ExplanationHTML}}<div class="sf-explain">{{ExplanationHTML}}</div>{{/ExplanationHTML}}'
    '</div>'
)

CSS = (
    '.sf-card { font-family: Arial, Helvetica, sans-serif; font-size: 19px;'
    ' line-height: 1.45; color: #1b1b1b; background: #fdfaf6; padding: 18px;'
    ' text-align: left; }\n'
    '.sf-stem { margin-bottom: 14px; }\n'
    '.cloze { font-weight: 700; color: #0b63c5;'
    ' border-bottom: 2px solid #0b63c5; padding: 0 6px; }\n'
    '.sf-typed { margin: 12px 0; font-size: 17px; }\n'
    '.sf-typed code, .sf-typed .type-ok { color: #127a2c; }\n'
    '.sf-typed .type-bad { color: #b3261e; }\n'
    '.sf-explain { margin-top: 16px; padding-top: 10px;'
    ' border-top: 1px solid #d8d2c8; font-size: 16px; }\n'
    '.sf-image img { max-width: 100%; margin-top: 14px; }\n'
    '#answer { border: 0; }\n'
)


def read_varint(buf, i):
    out = shift = 0
    while True:
        b = buf[i]
        i += 1
        out |= (b & 0x7F) << shift
        shift += 7
        if not b & 0x80:
            return out, i


def parse(buf):
    """Decode into [(field, wiretype, value)]; message bodies kept as bytes."""
    i, out = 0, []
    while i < len(buf):
        key, i = read_varint(buf, i)
        field, wt = key >> 3, key & 7
        if wt == 0:
            val, i = read_varint(buf, i)
        elif wt == 2:
            n, i = read_varint(buf, i)
            val = buf[i:i + n]
            i += n
        elif wt == 5:
            val = buf[i:i + 4]
            i += 4
        elif wt == 1:
            val = buf[i:i + 8]
            i += 8
        else:
            raise ValueError(f"bad wire type {wt}")
        out.append((field, wt, val))
    return out


def encode_varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def encode(items):
    out = bytearray()
    for field, wt, val in items:
        out += encode_varint(field << 3 | wt)
        if wt == 0:
            out += encode_varint(val)
        elif wt == 2:
            if isinstance(val, str):
                val = val.encode()
            out += encode_varint(len(val)) + val
        else:
            out += val
    return bytes(out)



def replace_field(items, field, value):
    return [(f, wt, value if f == field else v) for f, wt, v in items]


def main() -> None:
    outdir = f"{C.OUT}/cloze"
    os.makedirs(outdir, exist_ok=True)
    work = f"{outdir}/collection_patched.db"
    src_db = os.environ.get("SF_INPUT_DB", C.LIVE_DB)
    shutil.copy2(src_db, work)

    db = sqlite3.connect(work)
    db.create_collation("unicase",
                        lambda a, b: (a.casefold() > b.casefold())
                        - (a.casefold() < b.casefold()))

    field_names = [r[0] for r in db.execute(
        "select name from fields where ntid=1813027267 order by ord")]
    assert len(field_names) == 17, field_names

    donor_cfg = db.execute("select config from notetypes where id=?",
                           (DONOR_MID,)).fetchone()[0]
    items = parse(donor_cfg)
    kind = dict((f, v) for f, wt, v in items if wt == 0).get(1)
    assert kind == 1, f"donor kind={kind}, expected cloze"
    new_cfg = encode(replace_field(items, 3, CSS))

    now = int(time.time())
    assert db.execute("select count(*) from notes where mid=?",
                      (DONOR_MID,)).fetchone()[0] == 0, "donor is in use"
    assert db.execute("select count(*) from notetypes where name=?",
                      (NEW_NAME,)).fetchone()[0] == 0
    db.execute("update notetypes set name=?, mtime_secs=?, usn=-1, config=? "
               "where id=?", (NEW_NAME, now, new_cfg, DONOR_MID))

    fcfg = db.execute("select config from fields where ntid=? and ord=0",
                      (DONOR_MID,)).fetchone()[0]
    db.execute("delete from fields where ntid=?", (DONOR_MID,))
    db.executemany("insert into fields (ntid,ord,name,config) values (?,?,?,?)",
                   [(DONOR_MID, i, n, fcfg) for i, n in enumerate(field_names)])

    db.execute("delete from templates where ntid=?", (DONOR_MID,))
    tcfg = encode([(1, 2, Q_FORMAT), (2, 2, A_FORMAT)])
    db.execute("insert into templates (ntid,ord,name,mtime_secs,usn,config) "
               "values (?,?,?,?,?,?)", (DONOR_MID, 0, "Cloze", now, -1, tcfg))

    notes = db.execute(
        "select id, flds from notes where mid=1813027267 and flds like ?",
        ("%blank-slot%",)).fetchall()
    converted, card_rows, skipped = [], [], []
    next_card = db.execute("select max(id) from cards").fetchone()[0] + 1
    for nid, flds in notes:
        fl = flds.split("\x1f")
        if len(fl) != 17:
            skipped.append((nid, f"fieldcount={len(fl)}"))
            continue
        if "completamento" not in fl[5].lower():
            continue
        slots = list(SLOT.finditer(fl[STEM]))
        answers = FILL.findall(fl[BACKSTEM])
        if not slots or len(slots) != len(answers):
            skipped.append((nid, f"slots={len(slots)} answers={len(answers)}"))
            continue
        pieces, pos, bad = [], 0, False
        for i, (m, ans) in enumerate(zip(slots, answers), start=1):
            if "::" in ans or "}}" in ans:
                bad = True
                break
            pieces.append(fl[STEM][pos:m.start()])
            pieces.append("{{c%d::%s}}" % (i, ans))
            pos = m.end()
        if bad:
            skipped.append((nid, "answer contains a cloze delimiter"))
            continue
        pieces.append(fl[STEM][pos:])
        fl[STEM] = "".join(pieces)

        old = db.execute("select id, did, due from cards where nid=?",
                         (nid,)).fetchall()
        if len(old) != 1:
            skipped.append((nid, f"cards={len(old)}"))
            continue
        cid, did, due = old[0]
        for k in range(len(slots)):
            use_id = cid if k == 0 else next_card
            if k:
                next_card += 1
            card_rows.append((use_id, nid, did, k, now, -1, 0, 0, due + k,
                              0, 0, 0, 0, 0, 0, 0, 0, ""))
        converted.append((nid, "\x1f".join(fl), len(slots)))

    db.executemany("update notes set mid=?, flds=?, mod=?, usn=-1 where id=?",
                   [(DONOR_MID, flds, now, nid) for nid, flds, _ in converted])
    db.executemany("delete from cards where nid=?", [(n,) for n, _, _ in converted])
    db.executemany(
        "insert into cards (id,nid,did,ord,mod,usn,type,queue,due,ivl,factor,"
        "reps,lapses,left,odue,odid,flags,data) "
        "values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", card_rows)
    db.commit()

    report = {
        "converted_notes": len(converted),
        "cards_created": len(card_rows),
        "multi_cloze_notes": sum(1 for _, _, n in converted if n > 1),
        "skipped": skipped[:50],
        "skipped_count": len(skipped),
        "new_mid": DONOR_MID,
        "new_name": NEW_NAME,
    }
    json.dump(report, open(f"{outdir}/conversion_report.json", "w"), indent=2)
    print(json.dumps(report, indent=2))
    db.close()


if __name__ == "__main__":
    main()

