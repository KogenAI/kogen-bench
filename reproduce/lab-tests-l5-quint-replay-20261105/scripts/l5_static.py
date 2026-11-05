#!/usr/bin/env python3
"""L5 part C (static): every @model: scenario, the model it names, and whether the replay can express it.
usage: l5_static.py <kogen repo> <sha> <out.json>
Rule (fixed in the Lab record): a scenario is `expressible` only if its model is build.qnt (the only model the replay's generator targets)
and every requirement id on the scenario appears in build.qnt's text; `requirement outside the model` if the model is build but some id does not;
`no generator` for scenarios naming another model."""
import json, re, subprocess, sys
repo, sha, out = sys.argv[1:4]
git = lambda *a: subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True).stdout
qnt = {m: git('show', f'{sha}:spec/quint/{m}.qnt') for m in ('build', 'shaping', 'run_control', 'recovery', 'stages')}
def expand(t):
    """Requirement ids in a model's text, expanding its own range notation (REV-3..5, VER-6/7/9)."""
    out = set()
    for m in re.finditer(r'\b([A-Z]{2,5})-(\d+)(?:\.\.(\d+)|((?:/\d+)+))?', t):
        p, a = m[1], int(m[2]); out.add(f'{p}-{a}')
        if m[3]: out.update(f'{p}-{k}' for k in range(a, int(m[3]) + 1))
        if m[4]: out.update(f'{p}-{k}' for k in m[4].split('/') if k)
    return out
ids = {m: expand(t) for m, t in qnt.items()}
rows = []
for f in sorted(git('ls-tree', '--name-only', f'{sha}', 'spec/features/').split()):
    txt = git('show', f'{sha}:{f}').splitlines()
    tags = []
    for i, l in enumerate(txt):
        s = l.strip()
        if s.startswith('@'): tags = s.split(); continue
        m = re.match(r'(Scenario Outline|Scenario):\s*(.*)', s)
        if m:
            mt = [t for t in tags if t.startswith('@model:')]
            if mt:
                model = mt[0][7:]; reqs = [t[1:] for t in tags if re.fullmatch(r'@[A-Z]{2,5}-\d+', t)]
                missing = [r for r in reqs if r not in ids.get(model, set())]
                cls = ('expressible' if not missing else 'requirement outside the model') if model == 'build' else 'no generator'
                rows.append(dict(feature=f.split('/')[-1], line=i + 1, model=model, reqs=reqs, missing_in_model=missing, cls=cls, title=m[2][:90]))
            tags = []
        elif s and not s.startswith('#'): tags = [] if not s.startswith('@') else tags
summary = {c: sum(r['cls'] == c for r in rows) for c in ('expressible', 'requirement outside the model', 'no generator')}
byModel = {m: sum(r['model'] == m for r in rows) for m in ('build', 'shaping', 'run_control', 'recovery', 'stages')}
json.dump(dict(sha=sha, total=len(rows), by_model=byModel, summary=summary, rows=rows), open(out, 'w'), indent=1)
print(len(rows), byModel, summary)
for r in rows: print(r['feature'][:14], r['line'], r['model'], r['cls'], r['missing_in_model'], '|', r['title'][:60])
