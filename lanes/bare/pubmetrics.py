"""Read-only publication accounting and plan validation; standard library only."""
import collections
import hashlib
import json
import math
import os
from pathlib import Path
import shlex
import shutil

TOKENS = ('input_tokens', 'cached_input_tokens', 'output_tokens', 'reasoning_tokens')

def number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and x >= 0

def read(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return default

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def object_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def evaluation(result, ev):
    commands = ev.get('commands')
    # A grade Boolean is not an execution receipt. Preserve unknown for old receipts.
    tests_ran = (any(isinstance(c, dict) and (number(c.get('status')) or
                 isinstance(c.get('status'), int) or c.get('timed_out') is True) for c in commands)
                 if isinstance(commands, list) else None)
    infra = ('evaluator-setup' if str(ev.get('infrastructure') or '').startswith('setup failed')
             else 'evaluator-infrastructure' if ev.get('infrastructure')
             else 'harness-infrastructure' if result.get('outcome') == 'harness_error' or result.get('publication_infrastructure') else None)
    observed = ev.get('all_passed') if isinstance(ev.get('all_passed'), bool) else None
    scored = observed if not infra and tests_ran is True else None
    return dict(tests_ran=tests_ran, infrastructure_class=infra, reported_pass=observed,
                score_pass=scored, clean_agent_completion=result.get('outcome') == 'finished',
                agent_outcome=result.get('outcome'), evaluation_complete=ev.get('complete'))

def parse_usage(path, arm):
    rec = dict.fromkeys(TOKENS)
    rec.update(requests=0, tool_calls=0, models=[], errors=[], usage_complete={},
               usage_lower_bounds={k: 0 for k in TOKENS}, usage_observations={k: 0 for k in TOKENS})
    missing = {k: False for k in TOKENS}
    responses = started = 0
    broken = False
    mapping = (dict(zip(TOKENS, ('input', 'cached', 'output', 'reasoning'))) if arm == 'loop'
               else dict(zip(TOKENS, ('input_tokens', 'cached_input_tokens', 'output_tokens', 'reasoning_output_tokens'))))
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            for line in f:
                try:
                    e = json.loads(line)
                except ValueError:
                    broken = True
                    continue
                kind = e.get('type')
                if kind == 'session.started' and (e.get('role') or {}).get('model'):
                    rec['models'] = [e['role']['model']]
                if kind == ('request.started' if arm == 'loop' else 'turn.started'):
                    started += 1
                if kind == ('response' if arm == 'loop' else 'turn.completed'):
                    responses += 1
                    u = e.get('usage') or {}
                    for k, source in mapping.items():
                        v = u.get(source)
                        if number(v):
                            rec['usage_lower_bounds'][k] += v
                            rec['usage_observations'][k] += 1
                        else:
                            missing[k] = True
                if kind == 'tool.call' or (kind == 'item.completed' and (e.get('item') or {}).get('type') in
                                           ('command_execution', 'file_change', 'mcp_tool_call')):
                    rec['tool_calls'] += 1
                if kind in ('error', 'turn.failed'):
                    if not str(e.get('message', '')).startswith('Reconnecting'):
                        rec['errors'].append(str(e.get('detail') or e.get('reason') or e.get('message') or e.get('error') or 'agent error')[:300])
        rec['request_unit'] = 'logical-model-requests' if arm == 'loop' else 'completed-CLI-turns'
        rec['requests'] = started if arm == 'loop' else responses
        # Unfinished calls may have unreported consumption, even after earlier completed responses.
        sequence_complete = responses > 0 and started == responses and not broken and not rec['errors']
        for k in TOKENS:
            rec['usage_complete'][k] = sequence_complete and not missing[k]
            if rec['usage_complete'][k]:
                rec[k] = rec['usage_lower_bounds'][k]
    except OSError:
        rec['usage_complete'] = {k: False for k in TOKENS}
    return rec

def usage_record(result, directory):
    """Reconstruct legacy usage from complete streams without changing saved evidence."""
    t = dict(result.get('totals') or {})
    arm = result.get('arm')
    directory = Path(directory)
    if result.get('outcome') == 'harness_error' and 'setup failed' in str(result.get('detail', '')) and not t:
        t.update({k: 0 for k in TOKENS}, usage_complete={k: True for k in TOKENS},
                 usage_lower_bounds={k: 0 for k in TOKENS}, usage_status='known-zero-before-agent')
    elif arm in ('loop', 'codex'):
        side = directory/'usage-events.jsonl'
        path = side if result.get('usage_stream_complete') and side.exists() else directory/'events.jsonl'
        parsed = parse_usage(path, arm)
        if result.get('events_capped') and not result.get('usage_stream_complete'):
            # An old bounded sidecar cannot establish a total. It supplies a lower bound only.
            if side.exists():
                parsed = parse_usage(side, arm)
            parsed['usage_complete'] = {k: False for k in TOKENS}
        if result.get('outcome') != 'finished':
            parsed['usage_complete'] = {k: False for k in TOKENS}
        for k in TOKENS:
            t[k] = parsed[k] if parsed['usage_complete'].get(k) else None
        for k in ('usage_complete', 'usage_lower_bounds', 'usage_observations', 'requests', 'request_unit'):
            if k in parsed:
                t[k] = parsed[k]
    else:
        t.setdefault('usage_complete', {k: False for k in TOKENS})
        t.setdefault('usage_lower_bounds', {k: t.get(k) if number(t.get(k)) else 0 for k in TOKENS})
        for k in TOKENS:
            if not t['usage_complete'].get(k):
                t[k] = None
    complete = t.get('usage_complete') or {}
    t['usage_status'] = t.get('usage_status') or ('complete' if all(complete.get(k) for k in TOKENS[:3]) else
                                                'partial' if any((t.get('usage_lower_bounds') or {}).values()) else 'unknown')
    if t['usage_status'] not in ('complete', 'known-zero-before-agent'):
        t['cost_usd'] = None
    return t

def expected_keys(spec):
    return {f"{task}/r{rep}/{arm['name']}" for task in spec['tasks']
            for rep in range(1, spec.get('reps', 1) + 1) for arm in spec['arms']}

def tree_hash(directory):
    root = Path(directory)
    h = hashlib.sha256()
    for p in sorted(root.rglob('*')):
        if '.git' in p.relative_to(root).parts:
            continue
        if p.is_symlink():
            h.update(str(p.relative_to(root)).encode() + b'\0symlink\0' + os.readlink(p).encode())
        elif p.is_file():
            h.update(str(p.relative_to(root)).encode() + b'\0' + digest(p).encode())
    return h.hexdigest()

def provenance(spec, tasks, code_dir):
    code_dir = Path(code_dir)
    binaries = {}
    keys = {'loop':'loop_bin', 'codex':'codex_bin', 'claude':'claude_bin', 'kogen':'kogen', 'pi':'pi_bin', 'opencode':'opencode_bin'}
    for arm in spec['arms']:
        key = keys[arm['arm']]
        raw = arm.get(key) or spec.get(key) or shutil.which({'loop':'kogen-loop'}.get(arm['arm'], arm['arm']))
        path = Path(os.path.expanduser(raw)) if raw else None
        if not path or not path.is_file():
            raise ValueError('Cannot pin executable for ' + arm['name'])
        binaries[arm['name']] = digest(path)
    from lanes import common, grading, usage, cell
    paths = [code_dir/n for n in ('lanes_bare.py', 'pubmetrics.py', 'pubagg.py', 'paired.py')]
    paths += [Path(m.__file__) for m in (common, grading, usage, cell)]
    grader = Path(os.environ.get('LANES_GRADE_BIN') or Path(common.cache_dir())/'bin/lanes-grade-verdict')
    if not grader.is_file():
        raise ValueError('Prebuilt evaluator binary is required for a pinned batch')
    paths.append(grader)
    return dict(tasks={t:tree_hash(Path(tasks)/t) for t in spec['tasks']},
                binaries=binaries, evaluator_binary=str(grader),
                evaluator_source_sha256=tree_hash(grading.GRADE_DIR), code={p.name:digest(p) for p in paths})

def round_validation(run_dir, specs=None):
    p = Path(run_dir)
    frozen = read(p/'manifest.json')
    batch = read(p/'batch.json', {})
    sources = [frozen['spec']] if frozen else specs or ([batch] if batch else [])
    expected = set().union(*(expected_keys(s) for s in sources)) if sources else set()
    actual = set()
    unfinished = []; exclusions = []; invalid = []; mismatched = []
    for rp in sorted((p/'cells').glob('*/r*/*/result.json')):
        key = str(rp.parent.relative_to(p/'cells')); r = read(rp, {})
        if r.get('cell') != key:
            continue  # archived attempts are disclosed separately
        actual.add(key)
        ev = read(rp.parent/'evaluation.json', {})
        v = evaluation(r, ev)
        status = read(rp.parent/'status.json', {})
        if frozen and r.get('manifest_sha256') != frozen.get('sha256'):
            mismatched.append(key)
        if v['infrastructure_class']:
            exclusions.append(key)
        elif v['score_pass'] is None:
            unfinished.append(key)
        if frozen and status.get('state') != 'terminal':
            invalid.append(key)
    missing = sorted(expected-actual)
    unexpected = sorted(actual-expected)
    immutable = bool(frozen and frozen.get('sha256') == object_hash({k:v for k,v in frozen.items() if k != 'sha256'}))
    batch_matches = bool(frozen and batch == frozen.get('spec'))
    coverage_complete = bool(expected) and not (missing or unexpected or unfinished)
    return dict(immutable_manifest=immutable, batch_matches_manifest=batch_matches,
                provenance_verified=bool(immutable and batch_matches and not mismatched),
                expected=len(expected), observed=len(actual), missing=missing, unexpected=unexpected,
                unfinished=unfinished, classified_exclusions=exclusions, invalid_terminal=invalid,
                provenance_mismatches=mismatched, coverage_complete=coverage_complete,
                complete=bool(immutable and batch_matches and coverage_complete and not invalid and not mismatched),
                manifest_status='pinned' if immutable else 'legacy-unattested',
                plan_basis='immutable' if frozen else 'current-source-specs' if specs else 'latest-batch-only')

def process_active(lines, name, folder, base):
    """Observe actual manifest argv or explicit run directory, including shared-directory companions."""
    if lines is None:
        return None
    uncertain = False
    for line in lines:
        if 'lanes_bare.py' not in line or 'batch' not in line:
            continue
        try:
            argv = shlex.split(line)
        except ValueError:
            uncertain = True
            continue
        for i, token in enumerate(argv[:-2]):
            if Path(token).name != 'lanes_bare.py' or argv[i+1] != 'batch':
                continue
            manifest = Path(argv[i+2]).name.removesuffix('.json')
            run = next((argv[j+1] for j in range(i+3, len(argv)-1) if argv[j] == '--run-dir'), None)
            run = run or next((v.split('=',1)[1] for v in argv[i+3:] if v.startswith('--run-dir=')), None)
            if run:
                resolved = Path(os.path.expanduser(run))
                if not resolved.is_absolute():
                    resolved = Path(base)/resolved
                if resolved == Path(base)/folder/name:
                    return True
            elif manifest == name or manifest == name+'-cx':
                # A bare manifest does not identify an overridden/default destination reliably.
                uncertain = True
    return None if uncertain else False
