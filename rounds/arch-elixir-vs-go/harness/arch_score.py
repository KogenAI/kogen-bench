#!/usr/bin/env python3
"""Always score two repetitions, off a writable copy of a frozen phase FINAL."""
from pathlib import Path
import argparse
import importlib.util
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from arch_config import load, dump, treatment
from arch_snapshot import tree_hash, writable_copy

PROFILE = ('(version 1) (allow default) (deny network-outbound) '
           '(allow network-outbound (remote ip "localhost:*")) '
           '(allow process-exec (literal "/bin/ps") (with no-sandbox)) (allow process-info*)')

def _counter_shapes(value, repetition_counters=None):
    if repetition_counters is None:
        repetition_counters = set()
    found = False
    if isinstance(value, dict):
        if 'passed' in value and 'total' in value:
            passed, total = value['passed'], value['total']
            if (not isinstance(passed, int) or isinstance(passed, bool) or passed < 0 or
                    not isinstance(total, int) or isinstance(total, bool) or total < passed):
                raise ValueError('Malformed K-ID counters')
            found = True
            if value.get('repetition') in (1, 2):
                repetition_counters.add(value['repetition'])
        for child in value.values():
            found = _counter_shapes(child, repetition_counters) or found
    elif isinstance(value, list):
        for child in value:
            found = _counter_shapes(child, repetition_counters) or found
    return found

def normalize(result, groups, expected, reps=2, expected_contract=None):
    if result.get('schema_version') != 2:
        raise ValueError('Unsupported scorer schema_version; frozen runner requires schema_version 2')
    if result.get('reps') != reps:
        raise ValueError('Scorer schema/repetition count differs from freeze')
    required = ('spec_sha256', 'suite_sha256', 'spec_sha256_end', 'groups', 'k_ids', 'priority_k_ids')
    if any(key not in result for key in required):
        raise ValueError('Scorer v2 report is missing documented contract or counter fields')
    for key, value in (expected_contract or {}).items():
        if key in result and result[key] != value:
            raise ValueError('Scorer contract hash differs from freeze: ' + key)
    for key in ('k_ids', 'priority_k_ids'):
        repetition_counters = set()
        if (not _counter_shapes(result[key], repetition_counters) or
                repetition_counters != set(range(1, reps + 1))):
            raise ValueError('Scorer v2 K-ID counters lack overall or per-repetition totals: ' + key)
    rows = result.get('cases', [])
    if not isinstance(rows, list):
        raise ValueError('Scorer cases must be an array')
    ids = [row['id'] for row in rows]
    wanted = {case for case, group in expected.items() if group in groups}
    if len(ids) != len(set(ids)) or set(ids) != wanted:
        raise ValueError('Scored case inventory differs from freeze')
    if result.get('spec_changed_during_run') is not False:
        raise ValueError('Scorer spec changed or stability receipt is missing')
    totals = {group: dict(passed=0, total=0) for group in groups}
    for row in rows:
        group = row['group']
        if 'k_ids' in row and (not isinstance(row['k_ids'], list) or
                               any(not isinstance(k_id, str) for k_id in row['k_ids'])):
            raise ValueError('Scorer v2 case k_ids must be a list of strings')
        repetitions = row.get('repetitions', [])
        if group != expected[row['id']] or len(repetitions) != reps:
            raise ValueError('Wrong group or incomplete repetitions')
        if sorted(rep.get('repetition') for rep in repetitions) != list(range(1, reps + 1)):
            raise ValueError('Duplicate or missing repetition')
        if any(type(rep.get('passed')) is not bool for rep in repetitions):
            raise ValueError('Missing boolean repetition outcomes')
        passed = all(rep['passed'] for rep in repetitions)
        if row.get('passed') is not passed:
            raise ValueError('Scorer did not apply every-repetition pass rule')
        totals[group]['total'] += 1
        totals[group]['passed'] += int(passed)
    if totals != result.get('groups'):
        raise ValueError('Group aggregate disagrees with per-case results')
    return dict(groups=totals, cases=[dict(id=row['id'], group=row['group'], passed=row['passed']) for row in rows],
                duration_s=result.get('duration_s'))

def _score(root, arm, phase, snapshot_path=None, result_path=None):
    root = Path(root).resolve()
    config = load(root)
    frozen = json.loads((root / 'ARCH-FREEZE.json').read_text())
    snapshot = Path(snapshot_path) if snapshot_path is not None else root / 'snapshots' / phase / 'FINAL' / arm
    receipt = (json.loads((snapshot.parent / (arm + '.capture.json')).read_text())
               if snapshot_path is None else {'source_hash': tree_hash(snapshot)})
    if tree_hash(snapshot) != receipt['source_hash']:
        raise ValueError('FINAL snapshot hash changed')
    score_label = Path(result_path).stem if result_path is not None else arm
    destination = (root / 'score-work' / 'reference' / phase / score_label
                   if result_path is not None else root / 'score-work' / phase / arm)
    destination.parent.mkdir(parents=True, exist_ok=True)
    writable_copy(snapshot, destination)
    groups = ['B', 'F'] if phase == 'build' else ['M']
    output = (root / 'tests/reference-results' / phase / (score_label + '.json')
              if result_path is not None else root / 'tests/results' / phase / (arm + '.json'))
    output.parent.mkdir(parents=True, exist_ok=True)
    binary = destination / 'kogen'
    started = time.monotonic()
    official_scoring_ran = False
    try:
        if not binary.is_file() or not os.access(binary, os.X_OK):
            # Missing deliverables fail all tests; they are not a harness failure.
            result = dict(groups={g: dict(passed=0, total=sum(x == g for x in frozen['cases'].values())) for g in groups},
                          cases=[dict(id=k, group=g, passed=False) for k, g in frozen['cases'].items() if g in groups],
                          candidate_missing=True, duration_s=0)
        else:
            env = dict(os.environ, NO_COLOR='1', GOTOOLCHAIN='local', GOPROXY='off', GOSUMDB='off',
                       HEX_OFFLINE='1', PYTHONDONTWRITEBYTECODE='1')
            for key in list(env):
                if key.startswith('KOGEN_') or key in ('OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'CODEX_HOME'):
                    env.pop(key)
            stack = config['toolchains']
            toolchains = ('go', 'elixir', 'erlang') if treatment(arm) == 'E' else ('go',)
            env['PATH'] = ':'.join(str(Path(stack[k]) / 'bin') for k in toolchains) + ':/usr/bin:/bin:/usr/sbin:/sbin'
            private = root / 'tests/.score-env' / phase / score_label
            for name in ('home', 'tmp', 'config'):
                (private / name).mkdir(parents=True, exist_ok=True)
            env.update(HOME=str(private / 'home'), TMPDIR=str(private / 'tmp'),
                       XDG_CONFIG_HOME=str(private / 'config'), GIT_CONFIG_GLOBAL='/dev/null',
                       GIT_CONFIG_NOSYSTEM='1')
            # macOS seatbelt allows only loopback traffic needed by this suite.
            sandbox = shutil.which('sandbox-exec')
            if not sandbox:
                raise ValueError('Offline scoring requires macOS sandbox-exec')
            command = [sandbox, '-p', PROFILE, sys.executable, str(root / 'tests/run_hidden.py'),
                       '--kogen', str(binary), '--groups', ','.join(groups), '--out', str(output), '--reps', '2']
            log = (root / 'out/reference-scores' / (score_label + '-' + phase + '.log')
                   if result_path is not None else root / 'out' / arm / ('score-' + phase + '.log'))
            with log.open('w') as stream:
                proc = subprocess.Popen(command, cwd=destination, env=env, stdout=stream,
                                        stderr=subprocess.STDOUT, start_new_session=True)
                try:
                    proc.wait(timeout=config['score_timeout_seconds'])
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    helper_spec = importlib.util.spec_from_file_location('arch_hidden_cleanup', root / 'tests/runner_core.py')
                    helper = importlib.util.module_from_spec(helper_spec)
                    helper_spec.loader.exec_module(helper)
                    helper.cleanup_processes(str(root / 'tests/.tmp'), [proc.pid])
                    proc.wait(timeout=5)
                    raise RuntimeError('Scorer exceeded its separate scoring deadline')
            if proc.returncode not in (0, 1):
                raise RuntimeError('Scorer invocation failed: exit ' + str(proc.returncode))
            raw = json.loads(output.read_text())
            spec = {name: frozen['files']['spec/' + name] for name in ('SPEC.md', 'PROTOCOL.md')}
            from arch_gates import contract_hash
            result = normalize(raw, groups, frozen['cases'], expected_contract={
                'spec_sha256': spec, 'spec_sha256_end': spec,
                'contract_sha256': contract_hash(frozen)})
            official_scoring_ran = True
            if result_path is not None:
                output.unlink(missing_ok=True)
        if tree_hash(snapshot) != receipt['source_hash']:
            raise ValueError('Scoring mutated FINAL')
        result.update(arm=arm, phase=phase, snapshot_sha256=receipt['source_hash'],
                      scoring_wall_seconds=time.monotonic() - started, scoring_error=None,
                      scoring_case_count=len(result.get('cases', [])) if official_scoring_ran else 0)
    except Exception as error:
        result = dict(arm=arm, phase=phase, scoring_error=str(error), groups=None)
        if result_path is not None and 'output' in locals():
            output.unlink(missing_ok=True)
    destination_receipt = Path(result_path) if result_path is not None else root / 'out' / arm / ('score-' + phase + '.json')
    if result_path is not None:
        result = dict(arm_kind=treatment(arm), phase=phase,
                      scoring_error=result.get('scoring_error'),
                      scoring_wall_seconds=result.get('scoring_wall_seconds', 0),
                      scoring_case_count=result.get('scoring_case_count', 0))
    dump(destination_receipt, result)
    return result

def score(root, arm, phase):
    try:
        return _score(root, arm, phase)
    except Exception as error:
        result = dict(arm=arm, phase=phase, scoring_error=str(error), groups=None)
        dump(Path(root) / 'out' / arm / ('score-' + phase + '.json'), result)
        return result

def score_snapshot(root, arm, phase, snapshot_path, result_path):
    try:
        return _score(root, arm, phase, snapshot_path=snapshot_path, result_path=result_path)
    except Exception as error:
        result = dict(arm=arm, phase=phase, scoring_error=str(error), groups=None,
                      scoring_wall_seconds=0, scoring_case_count=0)
        dump(Path(result_path), result)
        return result

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--arm', required=True)
    p.add_argument('--phase', choices=('build', 'maintenance'), required=True)
    args = p.parse_args()
    result = score(args.root, args.arm, args.phase)
    print(json.dumps(result))
    return int(bool(result['scoring_error']))

if __name__ == '__main__':
    raise SystemExit(main())
