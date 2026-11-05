#!/usr/bin/env python3
"""L8 (static) step 1-2: step files that spawn `go test`, their test names, and whether each name exists at the snapshot.
usage: l8_inventory.py <delivery dir> <out dir>"""
import json, os, re, subprocess, sys, collections
dl, out = sys.argv[1:3]
SNAP = {'kogen': '24136fc', 'kogen-build': '956b151', 'kogen-shaping': '42424ca', 'kogen-verification': '6ffb2d1', 'kogen-review': '2fd0a09',
        'kogen-loop': '268327e', 'kogen-coordinator': 'f16789b', 'kogen-setup': '8958731', 'kogen-executor': '0b2d756'}
def git(repo, *a): return subprocess.run(['git', '-C', os.path.join(dl, repo)] + list(a), capture_output=True, text=True).stdout
GOTEST_A = re.compile(r"""['"`]go['"`]\s*,\s*\[[^\]]*?['"`]test['"`]""", re.S)
GOTEST_B = re.compile(r"\bgo test\b")
GOTEST_C = re.compile(r"-run\b")
def wraps_go_test(t): return bool(GOTEST_A.search(t) or GOTEST_B.search(t) or (GOTEST_C.search(t) and re.search(r"['\"`]go['\"`]", t)))
TESTNAME = re.compile(r'\bTest[A-Za-z0-9_]*[A-Za-z0-9]\b')
rows = []; tests_by_repo = {}; ALLDEFS = {}; PENDING = []
for repo, sha in SNAP.items():
    files = git(repo, 'ls-tree', '-r', '--name-only', sha).split('\n')
    defs = {}
    for f in [x for x in files if x.endswith('_test.go')]:
        body = git(repo, 'show', f'{sha}:{f}')
        tag = re.search(r'^//go:build (.+)$', body, re.M)
        for m in re.finditer(r'^func (Test[A-Za-z0-9_]+)\(', body, re.M): defs[m[1]] = dict(file=f, build_tag=tag[1] if tag else None)
    tests_by_repo[repo] = defs
    for n, v in defs.items(): ALLDEFS.setdefault(n, []).append(dict(repo=repo, **v))
    steps = [x for x in files if re.fullmatch(r'features/steps/[^/]+\.js', x)]
    for f in steps:
        txt = git(repo, 'show', f'{sha}:{f}')
        PENDING.append((repo, f, txt))
for repo, f, txt in PENDING:
    spawns = wraps_go_test(txt)
    run_names = sorted({n for m in re.finditer(r"-run\b", txt) for n in TESTNAME.findall(txt[m.end(): m.end() + 300])})
    all_names = sorted(set(TESTNAME.findall(txt)))
    names, basis = (run_names, 'run-argument') if run_names else (all_names, 'any-token')
    names = names if spawns else []
    own = tests_by_repo[repo]
    # `go test -run` takes an unanchored regexp: a token that is a prefix or part of a name matches it.
    in_own = lambda n: any(n in d for d in own)
    anywhere = lambda n: any(n in d for d in ALLDEFS)
    generated = lambda n: bool(re.search(r'func\s+' + re.escape(n), txt))
    rows.append(dict(repo=repo, file=f, spawns_go_test=spawns, name_basis=basis if spawns else None, names=names,
                     exists_own=[n for n in names if in_own(n)], exists_elsewhere=[n for n in names if not in_own(n) and anywhere(n)],
                     generated_by_step=[n for n in names if not anywhere(n) and generated(n)],
                     missing=[n for n in names if not anywhere(n) and not generated(n)],
                     tagged_out=[n for n in names if anywhere(n) and all(d['build_tag'] for k, v in ALLDEFS.items() if n in k for d in v)],
                     modfile=('-modfile' in txt)))
# A name that is not a test of the repo may be a driver the step file copies in at run time: look for it in any other tracked file (not _test.go).
for r in rows:
    r['driver_in_repo'] = []
    for n in list(r['missing']):
        hit = [x for x in git(r['repo'], 'grep', '-E', '-l', 'func[[:space:]]+' + n, SNAP[r['repo']]).split('\n') if x and not x.endswith('_test.go') and not x.endswith(':' + r['file'])]
        if hit: r['driver_in_repo'].append(n); r['missing'].remove(n)
os.makedirs(out, exist_ok=True)
json.dump(dict(snapshots=SNAP, rows=rows), open(os.path.join(out, 'step_files.json'), 'w'), indent=0)
tot = collections.Counter(); sp = collections.Counter(); noname = collections.Counter(); stale = collections.Counter()
for r in rows:
    tot[r['repo']] += 1
    if r['spawns_go_test']:
        sp[r['repo']] += 1
        if not r['names']: noname[r['repo']] += 1
        if r['missing']: stale[r['repo']] += 1
print('repo | step files | spawn go test | without a test name | with a name missing at the snapshot')
for repo in SNAP: print(repo, tot[repo], sp[repo], noname[repo], stale[repo])
print('total', sum(tot.values()), sum(sp.values()), sum(noname.values()), sum(stale.values()))
