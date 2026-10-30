# Provenance copy of the fault test as run on 30 October 2026. Paths are parameters: set the environment variables named below to a scratch
# directory, your lanes release and your task-kit directory. It needs pinned Kogen artifacts; it is not runnable standalone.
from pathlib import Path
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import time

ROOT = Path(os.environ['FAULT_ROOT'])  # scratch dir holding repo/lanes (patched) and proof/
L = ROOT / 'repo/lanes'
P = Path(os.environ['LANES_PRIVATE'])  # holds runs/ and lc-tasks/
proof = ROOT / 'proof'
proof.mkdir(exist_ok=True)
sys.path.insert(0, str(L))
from lanes import approval, cell, common, dispatch, experiment, preflight, report

os.environ['LANES_NPM_CACHE'] = os.environ['NPM_STAGE_CACHE']
tasks = proof / 'tasks'
for task in ('bytefmt-go', 'task-tags-go'):
    dest = tasks / task
    if not dest.exists():
        tasks.mkdir(exist_ok=True)
        subprocess.run(['/bin/cp', '-cR', str(P / 'lc-tasks' / task), str(dest)], check=True)

fault = proof / 'fault-enabled'
fault.write_text('fault affects task-tags-go, low-effort lane only\n')
shim = proof / 'setup-shim.py'
shim.write_text('''from pathlib import Path
import json, os, sys, time
root = Path(__file__).parent
config = Path('.kogen/project.yaml').read_text()
sleeping = sys.argv[1] == 'task-tags-go' and 'effort: low' in config and (root/'fault-enabled').exists()
with open(root/'setup-calls.jsonl', 'a') as f:
    f.write(json.dumps(dict(task=sys.argv[1], sleeping=sleeping, pid=os.getpid(), pgid=os.getpgrp(), utc=time.time()))+'\\n')
if sleeping:
    print('injected setup delay: sleep 125 > unchanged deadline 120', file=sys.stderr, flush=True)
    os.execv('/bin/sleep', ['sleep', '125'])
''')
for task in ('bytefmt-go', 'task-tags-go'):
    path = tasks / task / 'task.toml'
    text = path.read_text()
    command = shlex.join([sys.executable, str(shim), task])
    if 'setup-shim.py' not in text:
        text = text.replace('setup = [', 'setup = [' + json.dumps(command) + ', ', 1)
    path.write_text(text)

source_run = P / 'runs/q-prefix-st'
lock = common.read_json(source_run / 'lanes.lock.json')
exp = common.read_json(L / 'tests/fixtures/experiment-good.json')
exp.update(id='preflight3-real-fault', tasks=['bytefmt-go', 'task-tags-go'], reps=1,
           decision_rule={'kind': 'descriptive'})
exp['lanes'] = [dict(name=row['name'], sha=row['sha'], patch=None,
                     settings={'models': {'build': 'openai/gpt-5.1 ' + effort}})
                for row, effort in zip(lock, ('low', 'high'))]
source = proof / 'experiment.json'
run = proof / 'run'
common.write_json(str(source), exp)
common.write_json(str(run / 'lanes.lock.json'), lock)
assert dispatch.plan_main([str(source), '--run-dir', str(run), '--tasks', str(tasks)]) == 0
original_plan = (run / 'plan.jsonl').read_bytes()
hosts = proof / 'hosts.json'
common.write_json(str(hosts), {'local': {'target': 'local', 'slots': 1}})
events = proof / 'cell-events.txt'
os.environ['FAKE_EVENTS'] = str(events)
artifacts = [cell.resolve_kogen(str(source_run), row['name'], None) for row in lock]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
pinned = {p: sha(p) for p in artifacts}
original_check = preflight.check_one
checks = []
def observed(exp, run_dir, tasks_dir, task, lane, artifact=None):
    started = time.monotonic()
    ok, message = original_check(exp, run_dir, tasks_dir, task, lane, artifact)
    row = dict(task=task, lane=lane['name'], ok=ok, timeout=isinstance(message, preflight.ApprovalTimeout),
               message=str(message), elapsed_s=round(time.monotonic()-started, 3), deadline_s=preflight.DEADLINE_S,
               cell_events=events.read_text().splitlines() if events.exists() else [])
    checks.append(row)
    common.write_json(str(proof / 'approval-checks.json'), checks)
    print(json.dumps(row), flush=True)
    return ok, message
preflight.check_one = observed

def dispatch_once():
    return dispatch.run_all(str(run), str(tasks), str(hosts), lanes_dir=str(L / 'tests/fixtures/fake-lanes'),
                            log=lambda m: print(m, flush=True))

start = time.monotonic()
code = dispatch_once()
assert code == 5, code
assert approval.pending(run) == {'task-tags-go'}
assert (run / 'plan.jsonl').read_bytes() == original_plan
first_events = events.read_text().splitlines()
assert len([x for x in first_events if x.startswith('cell ')]) == 2, first_events
assert all('bytefmt-go/' in x for x in first_events), first_events
timeouts = [r for r in checks if r['timeout']]
assert len(timeouts) == 2 and all(r['task'] == 'task-tags-go' and r['lane'] == 'a0' for r in timeouts), checks
rep = report.write(str(run))
assert rep['infrastructure_gaps'][0]['task'] == 'task-tags-go'
shutil.copyfile(run / 'report.json', proof / 'gap-report.json')
shutil.copyfile(run / 'report.md', proof / 'gap-report.md')
shutil.copyfile(run / 'PLAN.json', proof / 'gap-PLAN.json')

# This is a later invocation of the same experiment and exact original plan.
fault.unlink()
code2 = dispatch_once()
assert code2 == 0, code2
assert approval.pending(run) == set()
assert (run / 'plan.jsonl').read_bytes() == original_plan
final_events = events.read_text().splitlines()
assert len([x for x in final_events if x.startswith('cell ')]) == 4, final_events
assert len([x for x in final_events if x.startswith('cell ') and 'bytefmt-go/' in x]) == 2
report.write(str(run))
assert all(sha(p) == h for p, h in pinned.items())
pgids = sorted({r['pgid'] for r in common.read_jsonl(proof / 'setup-calls.jsonl')})
remaining = []
for pgid in pgids:
    p = subprocess.run(['ps', '-o', 'pid,args', '-g', str(pgid)], capture_output=True, text=True)
    if len(p.stdout.strip().splitlines()) > 1:
        remaining.append(dict(pgid=pgid, output=p.stdout))
assert not remaining, remaining
common.write_json(str(proof / 'result.json'), dict(first_exit=code, later_exit=code2, elapsed_s=round(time.monotonic()-start, 3),
                  timeouts=len(timeouts), all_planned_cells=4, ordinary_cells_before_retry=2, final_cell_starts=4,
                  deadline_s=preflight.DEADLINE_S, shim_sleep_s=125, pinned_kogen=pinned,
                  recorded_pgids=pgids, remaining_groups=remaining, model_calls=0,
                  cell_executor='model-free fake-lanes fixture; all approvals use real pinned Kogen'))
print('FAULT PROOF PASSED', flush=True)
