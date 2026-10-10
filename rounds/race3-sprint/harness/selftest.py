#!/usr/bin/python3
# Deterministic fixtures under this harness; never launch Codex or a race.
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from validity import tree_hash, file_hash

R = Path(__file__).resolve().parent
FILES = ['scoring_config.py', 'validity.py', 'checks.py', 'checks.sh', 'receipts.py', 'audit.py',
         'snap.sh', 'score-arm.sh', 'score-all.sh', 'clean-copy.py', 'compare-scores.py',
         'validate-results.py', 'kg-wrap.py', 'sweep.sh', 'metrics.py', 'stalls.py',
         'final-metrics.sh', 'lock.sh', 'lock-macbook.sh', 'lock-studio.sh', 'unlock.sh']


def stage(root, frozen=False):
    for name in FILES:
        shutil.copy2(R / name, root / name)
    for name in ['BRIEF.tmpl', 'TARGET.md', 'SPEC-BUG-CASES.txt', 'EXCLUDED-V2.txt', 'COUNTS.txt', 'inputs.sha'] + ['BRIEF-%s.md' % a for a in ('rust', 'go', 'ts', 'gleam', 'ex')]:
        shutil.copy2(R / name, root / name)
    if frozen:
        shutil.copytree(R / 'inputs', root / 'inputs')
    else:
        for name in ('spec', 'conformance'):
            (root / 'inputs' / name).mkdir(parents=True)
            (root / 'inputs' / name / 'frozen.txt').write_text(name + '\n')
        (root / 'inputs/NCASES').write_text(str(__import__('scoring_config').counts(R)[0]['N_total'])+'\n')
    (root / 'out').mkdir(); (root / 'ARMS').write_text('rust go\n')
    (root / 'START').write_text('1000\n'); (root / 'out/arms.log').write_text('')
    (root / 'env.sh').write_text('export PATH=/usr/bin:/bin\n')
    return root


def invoke(root, name, *args, expected=0, env=None):
    cmd = ['/bin/bash' if name.endswith('.sh') else '/usr/bin/python3', str(root / name)] + list(args)
    p = subprocess.run(cmd, cwd=str(R), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', **(env or {})))
    assert p.returncode == expected, '%s rc=%s expected=%s\n%s' % (name, p.returncode, expected, p.stdout)
    return p.stdout


def receipt(root, arm, model='gpt-6.1-sol', effort='high', command=None):
    d = root / 'out' / arm; d.mkdir(exist_ok=True)
    row = {'type': 'turn_context', 'payload': {'model': model, 'effort': effort}}
    text = json.dumps(row) + '\n'
    if command:
        text += json.dumps({'type': 'item.completed', 'item': {'type': 'command_execution', 'command': command}}) + '\n'
    (d / 'turn-0.jsonl').write_text(text)


def snapshot(root, label='FINAL'):
    for arm in (root / 'ARMS').read_text().split():
        d = root / 'snapshots' / label / arm; d.mkdir(parents=True)
        shutil.copy2(root / 'TARGET.md', d / 'TARGET.md')
        for name in ('spec', 'conformance'):
            (d / ('.%s.sha' % name)).write_text(tree_hash(root / 'inputs' / name) + '\n')
        (d / '.target.sha').write_text(file_hash(root / 'TARGET.md') + '\n')
    (root / 'snapshots' / label / 'TAKEN_AT').write_text('00:20:00\n')


def audit_test(root):
    stage(root); receipt(root, 'rust', command='cat ~/.codex/auth.json')
    receipt(root, 'go', command='cat spec/CORE.md; printf ok; cargo test --offline')
    snapshot(root); (root / 'snapshots/FINAL/rust/.spec.sha').write_text('planted\n')
    text = invoke(root, 'audit.py', expected=1)
    flags = [line for line in text.splitlines() if line.startswith('FLAG ')]
    assert len(flags) == 2 and all(line.startswith('FLAG rust ') for line in flags), text
    assert any('.codex/auth.json' in line for line in flags) and any('spec hash' in line for line in flags), text
    # Library aliases and each protected artifact have independent positive tests.
    for command in ('cat ~/Library/a', 'cat "$HOME/Library/a"', 'cat %s/Library/a' % Path.home()):
        receipt(root, 'rust', command=command)
        text = invoke(root, 'audit.py', expected=1)
        assert command[:30] in text, text
    receipt(root, 'rust', command='echo benign')
    (root / 'snapshots/FINAL/rust/.spec.sha').write_text(tree_hash(root / 'inputs/spec') + '\n')
    for name in ('conformance', 'target'):
        marker = root / ('snapshots/FINAL/go/.%s.sha' % name); saved = marker.read_text(); marker.write_text('bad\n')
        text = invoke(root, 'audit.py', expected=1)
        assert len([l for l in text.splitlines() if l.startswith('FLAG ')]) == 1, text
        marker.write_text(saved)
    invoke(root, 'audit.py')
    (root / 'snapshots/FINAL/go/TARGET.md').write_text('changed')
    text = invoke(root, 'audit.py', expected=1)
    assert len([l for l in text.splitlines() if l.startswith('FLAG ')]) == 1 and 'TARGET.md content' in text


def receipts_test(root):
    stage(root); receipt(root, 'rust'); receipt(root, 'go')
    home = root / 'home'; sessions = home / 'sessions/2026/10/10'; sessions.mkdir(parents=True)
    (root / 'CODEX_HOME').write_text(str(home))
    (root / 'out/rust/thread').write_text('test-thread')
    rows = [{'type': 'turn_context', 'payload': {'turn_id': 'a', 'model': 'gpt-6.1-sol', 'effort': 'high'}},
            {'type': 'turn_context', 'payload': {'turn_id': 'a', 'model': 'gpt-6.1-sol', 'effort': 'high'}},
            {'type': 'turn_context', 'payload': {'turn_id': 'b', 'model': 'other', 'effort': 'low'}}]
    (sessions / 'rollout-test-thread.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
    (root / 'out/rust/turn-0.jsonl').write_text('{}\n')
    (root / 'out/rust/turn-1.jsonl').write_text('{}\n')
    text = invoke(root, 'receipts.py', expected=1)
    flags = [l for l in text.splitlines() if l.startswith('FLAG ')]
    assert len(flags) == 1 and 'rust turn-1' in flags[0], text
    rows[-1]['payload'].update(model='gpt-6.1-sol', effort='high')
    (sessions / 'rollout-test-thread.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
    invoke(root, 'receipts.py')
    (root / 'out/go/turn-0.jsonl').write_text('{}\n')
    assert 'FLAG go turn-0' in invoke(root, 'receipts.py', expected=1)
    assert len((root / 'out/receipts.tsv').read_text().splitlines()) == 4


def checks_test(root):
    stage(root, frozen=True)
    kit = root / 'kit'; kit.mkdir(); (kit / 'payload').write_text('kit\n')
    (kit / 'logs').mkdir(); (kit / 'cache/tmp').mkdir(parents=True)
    (root / 'tools').mkdir(); cli = root / 'tools/codex'
    cli.write_text('#!/bin/sh\necho codex-cli selftest\n'); cli.chmod(0o755)
    (root / 'env.sh').write_text('export PATH="%s:/usr/bin:/bin"\nexport GOMAXPROCS=2 CARGO_NET_OFFLINE=true\n' % (root / 'tools'))
    for arm in ('rust', 'go'):
        (root / arm).mkdir(); (root / arm / '.kit-env.sh').write_text('export CARGO_HOME="%s/.kitcache/cargo"\n' % (root / arm))
    (root / 'home').mkdir(); (root / 'home/auth.json').write_text('{}')
    (root / 'CODEX_HOME').write_text(str(root / 'home'))
    env = {'RACE3_KIT_DIR': str(kit)}
    text = invoke(root, 'checks.sh', env=env); assert text.count('PASS ') == 7, text
    (root / 'KIT-SHA256').write_text((root / 'out/kit.sha256').read_text())
    (root / 'CODEX-VERSION').write_text('codex-cli selftest\n')
    (kit / 'logs/run.log').write_text('excluded'); (kit / 'cache/tmp/temp').write_text('excluded')
    invoke(root, 'checks.sh', env=env)
    mutations = [('BRIEF-go.md', 'tamper', 'briefs'), ('kit/payload', 'tamper', 'kit'),
                 ('inputs/NCASES', '145\n', 'frozen-inputs'), ('CODEX-VERSION', 'bad', 'codex-version'),
                 ('go/.kit-env.sh', 'export GOMAXPROCS=3\n', 'arm-environments'),
                 ('TARGET.md', 'bad', 'target-spec-bugs')]
    for filename, value, gate in mutations:
        p = root / filename; saved = p.read_text(); p.write_text(value)
        text = invoke(root, 'checks.sh', expected=1, env=env); assert 'FAIL ' + gate in text, text
        if gate == 'briefs': assert '--- BRIEF.tmpl' in text
        p.write_text(saved)
    (root / 'home/auth.json').unlink()
    assert 'FAIL codex-auth' in invoke(root, 'checks.sh', expected=1, env=env)


def scoring_test(root):
    stage(root); snapshot(root); snapshot(root, 'T+5m')
    for arm in ('rust', 'go'):
        d = root / 'snapshots/FINAL' / arm
        (d / 'target').mkdir(); (d / 'target/generated').write_text('build')
        (d / 'build/packages').mkdir(parents=True); (d / 'build/packages/dependency').write_text('dep')
    # Deterministic stand-in for only the expensive conformance runner. Exercise
    # the real orchestration, copying and per-arm comparison/adjustment.
    (root / 'score-arm.sh').write_text('''#!/bin/bash
R=$(cd "$(dirname "$0")" && pwd)
/usr/bin/python3 "$R/fake-score.py" "$1" "$2"
''')
    (root / 'score-arm.sh').chmod(0o755)
    (root / 'fake-score.py').write_text('''import json,os,sys
from pathlib import Path
r=Path(__file__).resolve().parent; l,a=sys.argv[1:]; tag=os.environ.get('SCORE_TAG',''); f=Path(os.environ.get('SCORE_SOURCE',r/'snapshots'/l/a))
if tag=='regrade':
    assert not (f/'target').exists() and (f/'build/packages/dependency').is_file()
sys.path.insert(0,str(r))
from scoring_config import counts
config,_=counts(r)
rows=[{'id':'one','status':'pass'},{'id':'two','status':'pass'}]
if tag=='repeat' and a=='rust': rows[0]['status']='fail'
if tag=='regrade' and a=='go': rows[1]['status']='fail'
(r/'out/results').mkdir(exist_ok=True)
(r/('out/results/%s-%s%s.jsonl'%(l,a,'-'+tag if tag else ''))).write_text(''.join(json.dumps(x)+'\\n' for x in rows))
with (r/('out/scores%s.tsv'%('-'+tag if tag else ''))).open('a') as w: w.write('%s\\t%s\\t2/%s\\texcl 2/%s\\tsnapshot@00:20:00\\t%s\\n'%(l,a,config['N_total'],config['N_scored'],tag or 'official'))
with (r/'out/calls').open('a') as w: w.write('%s %s %s\\n'%(l,a,tag))
''')
    for script in ('stalls.py', 'metrics.py'):
        (root / script).write_text('print("test stub")\n')
    invoke(root, 'score-all.sh')
    calls = (root / 'out/calls').read_text().splitlines()
    assert len(calls) == 8 and sum(l.startswith('T+5m') for l in calls) == 2, calls
    assert (root / 'out/flaky.tsv').read_text().splitlines()[1:] == ['FINAL\trust\tone\tpass\tfail']
    assert (root / 'out/regrade-diff.tsv').read_text().splitlines()[1:] == ['go\ttwo\tpass\tfail']
    config,_=__import__('scoring_config').counts(root)
    for line in (root/'out/scores.tsv').read_text().splitlines():
        fields=line.split('\t'); passed=1 if fields[1]=='rust' else 2
        assert fields[2]==f'{passed}/{config["N_total"]}' and fields[3]==f'excl {passed}/{config["N_scored"]}',line
    assert all(f'\t2/{config["N_total"]}\t' in l for l in (root / 'out/scores-official.tsv').read_text().splitlines())

    # Also run the real score-arm executable path, with a cheap fake provider of
    # conformance results using the REAL frozen inventory and kg-wrap.
    shutil.copy2(R / 'score-arm.sh', root / 'score-arm.sh')
    shutil.copy2(R / 'validate-results.py', root / 'validate-results.py')
    shutil.rmtree(root / 'inputs'); shutil.copytree(R / 'inputs', root / 'inputs')
    kogen = root / 'snapshots/FINAL/rust/kogen'
    kogen.write_text('#!/bin/sh\ntest "$LANG" = en_US.UTF-8 && test "$LC_ALL" = en_US.UTF-8 || exit 97\necho version-selftest\n'); kogen.chmod(0o755)
    runner = root / 'inputs/conformance/bin/kogen-conformance'
    runner.write_text("""#!/usr/bin/python3
import json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kogen_conformance.runner import load_cases
args=sys.argv[1:]
assert args[args.index('--jobs')+1]=='4' and args[args.index('--timeout')+1]=='60'
subprocess.run([args[args.index('--kogen')+1],'version'],check=True)
with open(args[args.index('--out')+1],'w') as f:
    for row in load_cases(): f.write(json.dumps({'id':row['id'],'status':'pass'})+'\\n')
""")
    runner.chmod(0o755)
    invoke(root, 'score-arm.sh', 'FINAL', 'rust', env={'SCORE_TAG': 'official'})
    assert not (root / 'out/kgstats/rust.tsv').exists()
    result = root / 'out/results/FINAL-rust-official.jsonl'
    invoke(root, 'validate-results.py', str(result))
    runner.write_text('#!/bin/sh\nexit 2\n')
    # A broken runner with no valid output must not silently become zero passes.
    invoke(root, 'score-arm.sh', 'FINAL', 'rust', expected=1, env={'SCORE_TAG': 'broken'})
    assert 'FLAG rust FINAL' in (root / 'out/scoring-errors.txt').read_text()


if __name__ == '__main__':
    functions = {'audit': audit_test, 'checks': checks_test, 'receipts': receipts_test, 'scoring': scoring_test}
    chosen = sys.argv[1:] or list(functions)
    for name in chosen:
        with tempfile.TemporaryDirectory(prefix='.selftest-', dir=str(R)) as tmp:
            functions[name](Path(tmp))
        print('PASS', name)
