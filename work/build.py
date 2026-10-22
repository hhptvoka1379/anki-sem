import json, sys, re
sys.path.insert(0, '.')
mods = ['answers_part1','answers_part2','answers_part3','answers_part4','answers_part5','answers_part6']
ALL = {}
for m in mods:
    ALL.update(__import__(m).A)

SRC = '/tmp/subset2/answer_key_request/NEEDED.jsonl'
rows = [json.loads(l) for l in open(SRC)]
out, errs = [], []
for r in rows:
    a = ALL[r['id']]
    o = {'id': r['id']}
    if r['type'] == 'mcq':
        if a['kind'] != 'mcq': errs.append((r['id'],'kind'))
        opts = r['options']
        if a['letter'] not in opts: errs.append((r['id'],'letter missing'))
        o['letter'] = a['letter']
        from answer_text_fixes import FIX
        o['answer_text'] = FIX.get(r['id'], opts[a['letter']])
    else:
        if a['kind'] != 'cloze': errs.append((r['id'],'kind'))
        n = r['blanks']
        if len(a['answers']) != n: errs.append((r['id'],f'blanks {len(a["answers"])} vs {n}'))
        o['answers'] = a['answers']
    o['reason'] = a['reason']
    o['confidence'] = a['conf']
    flags = [f for f in a['flags'] if f != 'needs_figure']
    if 'figure' in r:
        flags = ['needs_figure'] + flags
    o['flags'] = flags
    out.append(o)

with open('/home/user/anki-sem/answer_key_output.jsonl','w') as f:
    for o in out:
        f.write(json.dumps(o, ensure_ascii=False) + '\n')
print('rows', len(out), 'errors', errs)
