"""Small, root-run containment comparison harness. Python 3 standard library only."""
import argparse
import errno
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import secrets
import shutil
import signal
import socket
import statistics
import stat
import subprocess
import sys
import threading
import time
import uuid

ARMS = ("z", "b", "c2", "a"); SELECTABLE_ARMS = ARMS + ("a-bash",); ESCAPES = ("file_read_outside", "file_write_outside", "secret_file_read", "env_secret", "net_loopback")
SURVIVORS = ("survivor_double_fork", "survivor_setsid", "survivor_term_ignore"); RESOURCES = ("mem_cap", "pids_cap")
FIXTURES = ESCAPES + SURVIVORS + RESOURCES + ("allowed_rw",); ALL_FIXTURES = FIXTURES + ("noop",); CAPS = {"memory.max": 256 * 1024 * 1024, "pids.max": 64}
PF_KTHREAD = 0x00200000  # Linux task flag exposed as field 9 in /proc/PID/stat.
ROOT = pathlib.Path(__file__).resolve().parent; BASE = ROOT / "work"; OUT = ROOT / "out"; LEDGER_NAME = "ledger.jsonl"; SECRET_NAME = "CMPSECRET"; BENCH_HOME = str(ROOT)  # the deployment directory is resolved from the script location

def score(fixture, evidence):
    """Pure observer-only scorer. It never consumes fixture stdout or exit claims."""
    if fixture not in ALL_FIXTURES: return 'INVALID(unknown fixture)'
    if not isinstance(evidence, dict): return 'INVALID(missing evidence)'
    if evidence.get('arm_broken') is True: return 'INVALID(arm-broken)'
    for key in ('launch_ok', 'marker_seen'):
        if evidence.get(key) is not True: return 'INVALID(' + key.replace('_', ' ') + ')'
    if fixture == 'noop':
        if evidence.get('observer_ok') is not True: return 'INVALID(observer ok)'
        if evidence.get('launcher_completed') is not True or evidence.get('returncode') != 0 or evidence.get('timed_out') is True or evidence.get('launch_error') not in (None, ''):
            return 'INVALID(noop launcher completion failed)'
        return 'NOT-BLOCKED'
    if fixture == 'allowed_rw':
        if evidence.get('observer_ok') is not True: return 'INVALID(observer ok)'
        return 'NOT-BLOCKED' if evidence.get('allowed_token_seen') is True and evidence.get('allowed_read_token_seen') is True else 'INVALID(arm-broken)'
    if fixture in ESCAPES:
        if evidence.get('observer_ok') is not True: return 'INVALID(observer ok)'
        fields = {'file_read_outside': ('read_token_seen',), 'file_write_outside': ('write_token_seen',), 'secret_file_read': ('secret_file_token_seen',), 'env_secret': ('secret_env_seen',), 'net_loopback': ('listener_accept', 'listener_peer_marked')}[fixture]
        coverage = {'file_read_outside': 'read_scan_complete', 'file_write_outside': 'write_observation_complete', 'secret_file_read': 'secret_file_scan_complete', 'env_secret': 'env_scan_complete', 'net_loopback': 'listener_coverage_complete'}[fixture]
        if any((k not in evidence or not isinstance(evidence[k], bool) for k in fields)):
            return 'INVALID(missing escape evidence)'
        if fixture == 'net_loopback' and evidence.get('listener_healthy') is not True:
            return 'INVALID(listener unhealthy)'
        if fixture == 'net_loopback' and evidence['listener_peer_marked'] and not evidence['listener_accept']:
            return 'INVALID(listener peer inconsistent)'
        if fixture == 'net_loopback' and evidence['listener_accept'] and not evidence['listener_peer_marked']:
            return 'INVALID(listener peer unattributed)'
        leaked = all((evidence[k] for k in fields))
        if leaked: return 'NOT-BLOCKED'
        if evidence.get(coverage) is not True: return 'INVALID(observation coverage incomplete)'
        return 'BLOCKED'
    if fixture in SURVIVORS:
        protocol = evidence.get('survivor_protocol', {})
        if not isinstance(protocol, dict) or protocol.get('stable_pre_kill') is not True or protocol.get('runner_sigkill_delivered') is not True:
            return 'INVALID(survivor protocol incomplete)'
        pre=protocol.get('pre_rows',[]); ident=lambda r:tuple(r.get(k) for k in ('pid','start','ppid','sid'))
        if len(pre)<3 or len({ident(r) for r in pre[-3:]})!=1 or not isinstance(protocol.get('runner_identity'),dict): return 'INVALID(survivor pre-kill identity unstable)'
        for side in ('pre', 'post'):
            rows = protocol.get(side + '_rows')
            if not isinstance(rows, list) or any(any(k not in row for k in ('pid', 'start', 'ppid', 'sid')) for row in rows):
                return 'INVALID(survivor identity evidence missing)'
        if any(k not in protocol['runner_identity'] for k in ('pid','start','ppid','sid')): return 'INVALID(runner identity evidence missing)'
        if 'survivor_present' not in evidence or not isinstance(evidence['survivor_present'], bool):
            return 'INVALID(missing survivor evidence)'
        if fixture == 'survivor_term_ignore' and (protocol.get('term_delivery') is not True or protocol.get('term_survived_live') is not True):
            return 'INVALID(term-ignore control failed)'
        if bool(protocol.get('post_rows')) != evidence['survivor_present']:
            return 'INVALID(survivor evidence inconsistent)'
        if evidence['survivor_present']:
            return 'NOT-BLOCKED'
        if evidence.get('observer_ok') is not True:
            return 'INVALID(observer ok)'
        if protocol.get('post_scan_complete') is not True:
            return 'INVALID(survivor protocol incomplete)'
        return 'BLOCKED'
    if evidence.get('observer_ok') is not True: return 'INVALID(observer ok)'
    if fixture in RESOURCES:
        if evidence.get('resource_mechanism') is not True: return 'UNSUPPORTED(no mechanism)'
        if evidence.get('cgroup_ok') is not True or evidence.get('resource_final_sample') is not True: return 'INVALID(cgroup unreadable or no final sample)'
        if evidence.get('event_counts_zero_origin') is not True or not isinstance(evidence.get('resource_scope_identity'), dict): return 'INVALID(resource scope identity or counter origin missing)'
        limits = evidence.get('effective_limits')
        if not isinstance(limits, dict) or limits.get('memory.max') != CAPS['memory.max'] or limits.get('pids.max') != CAPS['pids.max']: return 'INVALID(effective limits missing/mismatched)'
        if fixture == 'mem_cap':
            if not isinstance(evidence.get('memory_peak'), int) or evidence.get('memory_limit') != CAPS['memory.max'] or not isinstance(evidence.get('memory_events'), dict) or not all((k in evidence['memory_events'] and isinstance(evidence['memory_events'][k], int) for k in ('max', 'oom', 'oom_kill'))): return 'INVALID(memory counters or effective limit missing/mismatched)'
            pressure = evidence.get('memory_peak', 0) >= CAPS['memory.max']; rejected = any(evidence['memory_events'][k] > 0 for k in ('max', 'oom'))
        else:
            if not isinstance(evidence.get('pids_peak'), int) or evidence.get('pids_limit') != CAPS['pids.max'] or not isinstance(evidence.get('pids_events'), dict) or not isinstance(evidence['pids_events'].get('max'), int): return 'INVALID(pids counters or effective limit missing/mismatched)'
            pressure = evidence.get('pids_peak', 0) >= CAPS['pids.max']; rejected = evidence.get('pids_events', {}).get('max', 0) > 0
        if pressure and rejected: return 'ENFORCED'
        if not pressure: return 'INVALID(insufficient above-cap pressure)'
        return 'NOT-ENFORCED'
    return 'INVALID(unhandled fixture)'

def bool_evidence(fixture, leaked):
    """Synthetic evidence for scorer unit and gate tests."""; e = {'launch_ok': True, 'observer_ok': True, 'marker_seen': True}
    if fixture == 'allowed_rw':
        e['allowed_token_seen'] = not leaked; e['allowed_read_token_seen'] = not leaked
    elif fixture in ESCAPES:
        names = {'file_read_outside': ('read_token_seen',), 'file_write_outside': ('write_token_seen',), 'secret_file_read': ('secret_file_token_seen',), 'env_secret': ('secret_env_seen',), 'net_loopback': ('listener_accept', 'listener_peer_marked')}[fixture]; e.update({k: leaked for k in names})
        e[{'file_read_outside': 'read_scan_complete', 'file_write_outside': 'write_observation_complete', 'secret_file_read': 'secret_file_scan_complete', 'env_secret': 'env_scan_complete', 'net_loopback': 'listener_coverage_complete'}[fixture]] = True
        if fixture == 'net_loopback': e['listener_healthy'] = True
    elif fixture in SURVIVORS:
        e['survivor_present'] = leaked; r = {'pid': 1, 'start': 1, 'ppid': 1, 'sid': 1}
        e['survivor_protocol'] = {'stable_pre_kill': True, 'runner_sigkill_delivered': True, 'post_scan_complete': True, 'pre_rows': [r,r,r], 'post_rows': [r] if leaked else [], 'runner_identity': {'pid':2,'start':2,'ppid':1,'sid':2,'argv0':'runner','exe':'/bin/bash'}, 'term_delivery': True, 'term_survived_live': True}
    elif fixture == 'mem_cap':
        e.update(resource_mechanism=True, cgroup_ok=True, cgroup_path='/sys/fs/cgroup/cmp-test', resource_scope_identity={'unit':'cmp-test.scope','control_group':'/cmp-test','cgroup_path':'/sys/fs/cgroup/cmp-test'}, resource_final_sample=True, event_counts_zero_origin=True, effective_limits={'memory.max':CAPS['memory.max'],'pids.max':CAPS['pids.max']}, memory_limit=CAPS['memory.max'], memory_peak=CAPS['memory.max'] if leaked else 1024, memory_events={'max': int(leaked), 'oom': 0, 'oom_kill': 0})
    elif fixture == 'pids_cap':
        e.update(resource_mechanism=True, cgroup_ok=True, cgroup_path='/sys/fs/cgroup/cmp-test', resource_scope_identity={'unit':'cmp-test.scope','control_group':'/cmp-test','cgroup_path':'/sys/fs/cgroup/cmp-test'}, resource_final_sample=True, event_counts_zero_origin=True, effective_limits={'memory.max':CAPS['memory.max'],'pids.max':CAPS['pids.max']}, pids_limit=CAPS['pids.max'], pids_peak=CAPS['pids.max'] if leaked else 1, pids_events={'max': int(leaked)})
    elif fixture == 'noop': e.update(launcher_completed=True, returncode=0, timed_out=False, launch_error=None)
    return e

def scorer_gate():
    for fixture in FIXTURES:
        a = score(fixture, bool_evidence(fixture, False)); b = score(fixture, bool_evidence(fixture, True))
        if fixture == 'allowed_rw':
            assert a == 'NOT-BLOCKED' and b == 'INVALID(arm-broken)', (fixture, a, b)
        elif fixture in RESOURCES:
            assert a.startswith('INVALID(insufficient') and b == 'ENFORCED', (fixture, a, b)
        else:
            assert a == 'BLOCKED' and b == 'NOT-BLOCKED', (fixture, a, b)
        assert score(fixture, {}) == 'INVALID(launch ok)'
    assert score('mem_cap', {**bool_evidence('mem_cap', True), 'resource_mechanism': False}) == 'UNSUPPORTED(no mechanism)'; return True

def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda : f.read(1024 * 1024), b''): h.update(block)
    return h.hexdigest()

def resolve_tools(require_all=True):
    root = pathlib.Path(__file__).resolve().parent; nono_override = os.environ.get('CMP_NONO'); candidates = [pathlib.Path(nono_override)] if nono_override else []; candidates += [root / 'vendor' / 'nono', root / 'nono']; found_nono = next((p for p in candidates if p.is_file() and os.access(p, os.X_OK)), None)
    if found_nono is None:
        p = shutil.which('nono')
        if p: found_nono = pathlib.Path(p)
    paths = {'bwrap': pathlib.Path('/usr/bin/bwrap'), 'systemd-run': pathlib.Path('/usr/bin/systemd-run'), 'nono': found_nono, 'runuser': pathlib.Path('/usr/sbin/runuser') if pathlib.Path('/usr/sbin/runuser').exists() else pathlib.Path('/usr/bin/runuser'), 'shell': pathlib.Path('/usr/bin/bash') if pathlib.Path('/usr/bin/bash').exists() else pathlib.Path(shutil.which('bash') or '/bin/bash'), 'systemctl': pathlib.Path('/usr/bin/systemctl'), 'setsid': pathlib.Path('/usr/bin/setsid'), 'env': pathlib.Path('/usr/bin/env'), 'sleep': pathlib.Path('/usr/bin/sleep'), 'nice': pathlib.Path(shutil.which('nice') or '/usr/bin/nice'), 'cc': pathlib.Path(shutil.which('cc') or '/usr/bin/cc'), 'python': pathlib.Path(sys.executable)}; missing = [name for (name, path) in paths.items() if path is None or not path.is_file()]
    if require_all and missing: raise RuntimeError('missing tools: ' + ','.join(missing))
    found = {k: v for (k, v) in paths.items() if v is not None and v.is_file()}
    optional = {'arm-a-helper': ARM_A_HELPER, 'arm-a-fx': ARM_A_RO / 'fx', 'arm-a-fxa': ARM_A_RO / 'fxa', 'arm-a-adapter': ARM_A_VENDOR / 'adapter.py',
                'arm-a-validate': ARM_A_VENDOR / 'validate.py', 'arm-a-manifest-schema': ARM_A_VENDOR / 'manifest.json'}
    for name, path in optional.items():
        try:
            if path.is_file(): found[name] = path
        except OSError: pass
    return found

def apparatus_hash():
    tools = resolve_tools(); files = {name: sha_file(pathlib.Path(__file__).resolve().parent / name) for name in ('cmp.py', 'fx.c', 'fx', 'fxa.c', 'fxa') if name in ('cmp.py', 'fx.c', 'fx') or (pathlib.Path(__file__).resolve().parent / name).is_file()}; selected = {name: {'path': str(path.resolve()), 'sha256': sha_file(path)} for (name, path) in sorted(tools.items())}; payload = {'files': files, 'tools': selected}; payload['sha256'] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest(); return payload

def hash_matches(expected, current):
    return isinstance(expected, dict) and isinstance(current, dict) and (expected.get('sha256') == current.get('sha256')) and (expected == current)

def load_hash_record(outdir):
    path = pathlib.Path(outdir) / 'apparatus-hash.json'
    if not path.is_file(): return None
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None

def scope_name(marker): return 'cmp-' + hashlib.sha256(marker.encode()).hexdigest()[:32] + '.scope'

def _systemctl_value(systemctl, prop, unit):
    try:
        r = subprocess.run([str(systemctl), 'show', '-p', prop, '--value', unit], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3, check=False)
        return {'returncode': r.returncode, 'stdout': r.stdout.decode('utf-8', 'replace').strip(), 'stderr': r.stderr.decode('utf-8', 'replace')}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'returncode': None, 'stdout': '', 'stderr': repr(exc)}

def scope_lookup(unit, tools, expected=None):
    """Return present, verified absent, or error without conflating lookup failures."""; systemctl = tools.get('systemctl', pathlib.Path('/usr/bin/systemctl')); load, active, control = (_systemctl_value(systemctl, p, unit) for p in ('LoadState', 'ActiveState', 'ControlGroup'))
    result = {'unit':unit,'load_state':load['stdout'],'active_state':active['stdout'],'control_group':control['stdout'],
              'lookup':{'LoadState':load,'ActiveState':active,'ControlGroup':control},'path':None,'cgroup_present':None,'state':'error','errors':[]}
    expected_path = pathlib.Path(expected['cgroup_path']) if isinstance(expected, dict) and expected.get('cgroup_path') else None; props = (('LoadState', load), ('ActiveState', active), ('ControlGroup', control)); failed = [(name, row) for name, row in props if row['returncode'] != 0]
    if failed:
        result['errors'] = [f'{n}:rc={r["returncode"]}:stderr={r["stderr"]}' for n, r in failed]; return result
    if load['stdout'] == 'not-found':
        paths = [expected_path] if expected_path else []
        if control['stdout'].startswith('/'):
            reported = pathlib.Path('/sys/fs/cgroup') / control['stdout'].lstrip('/')
            if expected_path and reported != expected_path:
                result['errors'].append('cgroup identity changed: expected ' + str(expected_path) + ' got ' + str(reported)); return result
            paths.append(reported)
        present = False
        for p in dict.fromkeys(paths):
            try: p.stat(); present = True
            except FileNotFoundError: pass
            except OSError as exc: result['errors'].append('cgroup-stat:' + repr(exc)); return result
        result.update(path=str(expected_path or (paths[-1] if paths else '')) or None, cgroup_present=present,
                      state='present' if present else 'absent'); return result
    if load['stdout'] not in ('loaded', 'masked', 'static', 'transient', 'generated', 'indirect', 'alias', 'linked', 'linked-runtime', 'bad'):
        result['errors'].append('unexpected LoadState: ' + repr(load['stdout'])); return result
    cg = control['stdout']
    if cg and not cg.startswith('/'):
        result['errors'].append('malformed ControlGroup: ' + repr(cg)); return result
    path = pathlib.Path('/sys/fs/cgroup') / cg.lstrip('/') if cg else None
    if expected_path and path and path != expected_path:
        result['errors'].append('cgroup identity changed: expected ' + str(expected_path) + ' got ' + str(path)); return result
    path = expected_path or path; result['path'] = str(path) if path else None
    try:
        present = path is not None and path.stat() is not None
    except FileNotFoundError:
        present = False
    except OSError as exc:
        result['errors'].append('cgroup-stat:' + repr(exc)); return result
    result['cgroup_present'] = present
    if not present and active['stdout'] in ('inactive', 'failed'): result['state'] = 'absent'
    elif path and present: result['state'] = 'present'
    else: result['errors'].append('unit has no verified cgroup path while ' + active['stdout'])
    return result

def cg_path(unit, tools):
    lookup = scope_lookup(unit, tools)
    return pathlib.Path(lookup['path']) if lookup['state'] == 'present' and lookup.get('path') else None

def proc_stat(pid):
    path = pathlib.Path(f'/proc/{pid}/stat')
    try: raw = path.read_bytes()
    except OSError as exc: raise proc_read_error(path, exc) from exc
    opening = raw.find(b' ('); closing = raw.rfind(b')')
    try:
        if opening < 1 or closing <= opening: raise ValueError('missing comm delimiters')
        actual_pid = int(raw[:opening])
        if actual_pid != int(pid): raise ValueError('stat PID does not match proc path')
        tail = raw[closing + 2:].split()
        if len(tail) < 20: raise ValueError('stat tail is truncated before starttime')
        state = tail[0].decode('ascii')
        ppid, sid, flags = int(tail[1]), int(tail[3]), int(tail[6])
        num_threads, start = int(tail[17]), int(tail[19])
        if num_threads < 0 or (state not in ('Z','X') and num_threads == 0) or start < 0:
            raise ValueError('invalid thread count or starttime')
        return {'pid':actual_pid,'ppid':ppid,'sid':sid,'flags':flags,'num_threads':num_threads,
                'start':start,'state':state}
    except (UnicodeDecodeError, ValueError, IndexError) as exc:
        error = ValueError(f'malformed {path}: {exc}')
        error.proc_path = str(path)
        raise error from exc

def proc_read_error(path, exc):
    """Preserve the proc path while keeping errno and OSError semantics."""
    wrapped = OSError(exc.errno, exc.strerror or str(exc), str(path))
    wrapped.proc_path = str(path)
    return wrapped

def proc_error_path(exc):
    path = getattr(exc, 'proc_path', None) or getattr(exc, 'filename', None)
    if isinstance(path, bytes): return os.fsdecode(path)
    return str(path) if path is not None else '<unknown-path>'

def errno_label(number): return errno.errorcode.get(number, str(number))

def proc_read_bytes(path):
    path = pathlib.Path(path)
    try: return path.read_bytes()
    except OSError as exc: raise proc_read_error(path, exc) from exc

def proc_stat_observation(pid):
    started = time.time_ns()
    try:
        value = proc_stat(pid)
        return {'pid':int(pid),'read_started_ns':started,'read_completed_ns':time.time_ns(),
                'stat':value,'error':None,'error_errno':None,'error_path':None}
    except (OSError, ValueError, IndexError, TypeError) as exc:
        return {'pid':int(pid),'read_started_ns':started,'read_completed_ns':time.time_ns(),
                'stat':None,'error':repr(exc),'error_errno':getattr(exc,'errno',None),
                'error_path':proc_error_path(exc),'error_object':exc}

def safe_proc_stat_observation(observation):
    return {key:value for key,value in observation.items() if key != 'error_object'}

def proc_task_census(pid):
    path = pathlib.Path('/proc') / str(pid) / 'task'; started = time.time_ns()
    try:
        entries = list(path.iterdir())
        tids = sorted(int(ent.name) for ent in entries if ent.name.isdigit())
        if not tids or len(tids) != len([ent for ent in entries if ent.name.isdigit()]):
            raise ValueError('empty or malformed task directory census')
        return {'path':str(path),'tids':tids,'read_started_ns':started,
                'read_completed_ns':time.time_ns(),'error':None,'error_errno':None,'error_path':None}
    except OSError as exc:
        wrapped = proc_read_error(path, exc)
        return {'path':str(path),'tids':None,'read_started_ns':started,
                'read_completed_ns':time.time_ns(),'error':repr(wrapped),
                'error_errno':wrapped.errno,'error_path':proc_error_path(wrapped)}
    except ValueError as exc:
        return {'path':str(path),'tids':None,'read_started_ns':started,
                'read_completed_ns':time.time_ns(),'error':repr(exc),
                'error_errno':None,'error_path':str(path)}

def observe_proc_cgroup(pid, expected_start, before_observation=None):
    before = before_observation or proc_stat_observation(pid)
    first = before.get('stat')
    membership = proc_cgroup_info(pid)
    after = proc_stat_observation(pid)
    verified = (expected_start is not None and isinstance(first, dict) and
                first.get('start') == expected_start and isinstance(after.get('stat'), dict) and
                after['stat'].get('start') == expected_start)
    return {'pid':int(pid),'expected_start':expected_start,'before':safe_proc_stat_observation(before),
            'membership':membership,'after':safe_proc_stat_observation(after),'verified_identity':verified,
            'cgroup_path':membership.get('path'),'observed_ns':time.time_ns()}

def verified_process_exit(expected):
    """Confirm /proc no longer contains the observed pid entry."""
    pid = int(expected['pid']); start = expected.get('start')
    observed = proc_stat_observation(pid); current = observed.get('stat')
    if current is None:
        exc = observed.get('error_object')
        if isinstance(exc, OSError) and exc.errno in (errno.ENOENT, errno.ESRCH):
            return (True, {'pid':pid,'expected_start':start,'verification':'proc-entry-gone',
                           'verify_errno':exc.errno,'stat_observation':safe_proc_stat_observation(observed)})
        return (False, {'pid':pid,'expected_start':start,'verification':'proc-stat-error',
                        'verify_error':observed.get('error'),'stat_observation':safe_proc_stat_observation(observed)})
    if start is None:
        verification = 'pid-present-zombie-unidentified' if current['state'] in ('Z','X') else 'pid-present-unidentified'
    elif current['start'] != start:
        verification = 'pid-reused-zombie' if current['state'] in ('Z','X') else 'pid-reused-live'
    elif current['state'] in ('Z','X'):
        verification = 'same-process-zombie'
    else:
        verification = 'same-process-live'
    return (False, {'pid':pid,'expected_start':start,'current_start':current['start'],
                    'state':current['state'],'verification':verification,'current_stat':current,
                    'stat_observation':safe_proc_stat_observation(observed)})

def verify_nonrunnable_group(expected, before_observation, verification, wait_result=None):
    """Prove that a matching Z/X task has no live sibling or unstable parent context."""
    pid = int(expected['pid']); start = expected.get('start'); current = verification.get('current_stat')
    proof = {'ok':False,'pid':pid,'expected_start':start,'state':verification.get('state'),
             'before':before_observation,'recheck':verification.get('stat_observation'),
             'thread_census':None,'parent_context':None,'cgroup_observation':None,
             'final_recheck':None,'harness_wait_result':wait_result,'reason':None}
    if start is None or not isinstance(current, dict) or current.get('start') != start:
        proof['reason'] = 'zombie identity is missing or changed'; return proof
    if current.get('state') not in ('Z','X'):
        proof['reason'] = 'task is not Z/X'; return proof
    parent_pid = current.get('ppid')
    if not isinstance(parent_pid, int) or parent_pid <= 0 or parent_pid == pid:
        proof['reason'] = 'invalid zombie parent PID'; return proof
    parent_before = proc_stat_observation(parent_pid)
    proof['parent_context'] = {'pid':parent_pid,'first':safe_proc_stat_observation(parent_before),'second':None,
                               'wait_result':wait_result if isinstance(wait_result, dict) and wait_result.get('pid') == parent_pid else None}
    proof['thread_census'] = proc_task_census(pid)
    proof['cgroup_observation'] = observe_proc_cgroup(pid,start,verification.get('stat_observation'))
    final = proc_stat_observation(pid); proof['final_recheck'] = safe_proc_stat_observation(final)
    parent_after = proc_stat_observation(parent_pid)
    proof['parent_context']['second'] = safe_proc_stat_observation(parent_after)
    parent_first = parent_before.get('stat'); parent_second = parent_after.get('stat'); final_stat = final.get('stat')
    tids = proof['thread_census'].get('tids')
    if proof['thread_census'].get('error') is not None:
        proof['reason'] = 'task census failed'; return proof
    if current.get('num_threads') not in (0,1) or not isinstance(final_stat, dict) or final_stat.get('num_threads') not in (0,1) or tids != [pid]:
        proof['reason'] = 'zombie thread group has additional or unidentified tasks'; return proof
    if not isinstance(parent_first, dict) or not isinstance(parent_second, dict):
        proof['reason'] = 'parent stat context unavailable'; return proof
    if (parent_first.get('start') != parent_second.get('start') or
            parent_first.get('state') in ('Z','X') or parent_second.get('state') in ('Z','X')):
        proof['reason'] = 'parent identity/stat context changed or is nonrunnable'; return proof
    first_stat = before_observation.get('stat') if isinstance(before_observation, dict) else None
    if (not isinstance(first_stat, dict) or first_stat.get('start') != start or
            first_stat.get('ppid') != current.get('ppid') or
            not isinstance(final_stat, dict) or final_stat.get('start') != start or
            final_stat.get('state') not in ('Z','X') or final_stat.get('ppid') != parent_pid):
        proof['reason'] = 'zombie identity or parent changed during auxiliary proof'; return proof
    proof['ok'] = True; proof['reason'] = 'matching Z/X identity, single-task census, stable parent'
    return proof

def verified_exit_note(exc, expected, source):
    """Return a note only for disappearance-shaped errors on a verified-gone pid."""
    current = exc; seen = set(); error_number = None
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        if isinstance(current, OSError) and current.errno is not None:
            error_number = current.errno; break
        current = current.__cause__ or current.__context__
    if error_number not in (errno.ENOENT, errno.ESRCH): return None
    gone, verification = verified_process_exit(expected)
    if not gone: return None
    return {'kind':'verified-process-exit','source':source,'pid':int(expected['pid']),'expected_start':expected.get('start'),
            'error':repr(exc),'error_errno':error_number,'verification':verification}

def read_proc_identity(pid):
    base = pathlib.Path('/proc') / str(pid); env_raw = proc_read_bytes(base / 'environ').split(b'\x00'); env = {}
    for item in env_raw:
        if b'=' in item:
            (k, v) = item.split(b'=', 1); env[k.decode('utf-8', 'replace')] = v.decode('utf-8', 'replace')
    argv_raw = proc_read_bytes(base / 'cmdline').split(b'\x00'); argv0 = argv_raw[0].decode('utf-8', 'replace') if argv_raw else ''
    stat = proc_stat(pid); partial = {'pid':int(pid),'env':env,'argv0':argv0,'exe':None,**stat}
    try: exe = os.path.realpath(base / 'exe')
    except OSError as exc:
        exc.partial_identity = partial
        if proc_error_path(exc) == '<unknown-path>': exc.proc_path = str(base / 'exe')
        raise
    return {'pid':int(pid),'env':env,'argv0':argv0,'exe':exe,**stat}

def proc_is_kernel_thread(pid, expected_start):
    """Recognize a same-start PF_KTHREAD task with no userspace cmdline or exe."""
    if expected_start is None: return False
    try:
        base = pathlib.Path('/proc') / str(pid)
        status = (base / 'status').read_bytes()
        fields = [line.split(b':', 1)[1].strip(b' \t')
                  for line in status.split(b'\n') if line.startswith(b'Kthread:')]
        if fields != [b'1']: return False
        before = proc_stat(pid)
        if before.get('start') != expected_start or (before.get('flags', 0) & PF_KTHREAD) != PF_KTHREAD: return False
        if (base / 'cmdline').read_bytes() != b'': return False
        try: os.readlink(base / 'exe')
        except OSError as exc:
            if exc.errno not in (errno.ENOENT, errno.ESRCH): return False
        else: return False
        after = proc_stat(pid)
        return after.get('start') == expected_start and (after.get('flags', 0) & PF_KTHREAD) == PF_KTHREAD
    except (OSError, ValueError, IndexError, TypeError):
        return False

def proc_cgroup_info(pid):
    path = pathlib.Path('/proc') / str(pid) / 'cgroup'; started = time.time_ns()
    try: raw = path.read_text()
    except OSError as exc:
        return {'pid':int(pid),'path':None,'read_path':str(path),'read_started_ns':started,
                'read_completed_ns':time.time_ns(),'read_error':repr(exc),
                'error_errno':exc.errno,'error_path':proc_error_path(exc)}
    for line in raw.splitlines():
        fields = line.split(':', 2)
        if len(fields) == 3 and fields[0] == '0' and fields[1] == '':
            return {'pid':int(pid),'path':fields[2],'read_path':str(path),'read_started_ns':started,
                    'read_completed_ns':time.time_ns(),'read_error':None,'error_errno':None,'error_path':None}
    return {'pid':int(pid),'path':None,'read_path':str(path),'read_started_ns':started,
            'read_completed_ns':time.time_ns(),'read_error':'unified cgroup entry missing',
            'error_errno':None,'error_path':str(path)}

def proc_observation_record(event_type, message, pid=None, start_time=None, proc_path=None,
                            error_number=None, cgroup_observation=None, identity_snapshots=None,
                            parent_context=None, cell_scope_identity=None, wait_result=None):
    membership = cgroup_observation.get('membership', {}) if isinstance(cgroup_observation, dict) else {}
    cgroup_path = membership.get('path') if isinstance(membership, dict) else None
    if cgroup_path is None and isinstance(cgroup_observation, dict):
        cgroup_path = cgroup_observation.get('path') or cgroup_observation.get('cgroup_path')
    scope_group = cell_scope_identity.get('control_group') if isinstance(cell_scope_identity, dict) else None
    return {'event_type':event_type,'message':message,'proc_path':proc_path,'errno':error_number,
            'pid':pid,'start_time':start_time,'cgroup':cgroup_path,'cell_cgroup':scope_group,
            'observed_ns':time.time_ns(),'error_observed_ns':None,'cgroup_observation':cgroup_observation,
            'identity_snapshots':identity_snapshots,'parent_context':parent_context,
            'harness_wait_result':wait_result}

def scan_marker(marker, observation_notes=None, resource_scope_identity=None,
                proc_diagnostics=None, harness_wait_result=None):
    (matches, errors) = ([], [])
    notes = observation_notes if observation_notes is not None else []
    note_start = len(notes); diagnostics = []; contexts = {}
    def add_note(note, context=None):
        context = context or {}; pid = note.get('pid')
        before = context.get('before'); after = context.get('after')
        snapshots = {'before':safe_proc_stat_observation(before) if isinstance(before, dict) else None,
                     'after':safe_proc_stat_observation(after) if isinstance(after, dict) else None,
                     'rechecks':context.get('rechecks')}
        cgroup = context.get('cgroup')
        cgroup_path = (cgroup or {}).get('membership',{}).get('path') if isinstance(cgroup,dict) else None
        if cgroup_path is None and isinstance(cgroup,dict): cgroup_path=cgroup.get('path')
        note.setdefault('proc_path', note.get('error_path') or f'/proc/{pid}/stat' if pid is not None else '/proc')
        note.setdefault('errno', note.get('error_errno'))
        note.setdefault('start_time', note.get('expected_start', note.get('current_start')))
        note.setdefault('cgroup',cgroup_path)
        note.setdefault('identity_snapshots', snapshots)
        note.setdefault('cgroup_observation', cgroup)
        note.setdefault('parent_context', context.get('parent_context'))
        note.setdefault('harness_wait_result', harness_wait_result)
        note.setdefault('cell_cgroup', resource_scope_identity.get('control_group') if isinstance(resource_scope_identity, dict) else None)
        note.setdefault('error_observed_ns',context.get('error_observed_ns'))
        notes.append(note)
        record=proc_observation_record('note',note.get('kind'),pid,
            note.get('start_time'),note.get('proc_path'),note.get('errno'),note.get('cgroup_observation'),
            note.get('identity_snapshots'),note.get('parent_context'),resource_scope_identity,harness_wait_result)
        record['error_observed_ns']=note.get('error_observed_ns'); diagnostics.append(record)
    def add_error(message, pid=None, start_time=None, exc=None, context=None, proc_path=None, error_number=None):
        errors.append(message); context = context or {}
        before = context.get('before'); after = context.get('after')
        snapshots = {'before':safe_proc_stat_observation(before) if isinstance(before, dict) else None,
                     'after':safe_proc_stat_observation(after) if isinstance(after, dict) else None,
                     'rechecks':context.get('rechecks')}
        if proc_path is None: proc_path = proc_error_path(exc) if isinstance(exc, OSError) else context.get('proc_path')
        if error_number is None: error_number = getattr(exc,'errno',None)
        cgroup = context.get('cgroup')
        record=proc_observation_record('error',message,pid,start_time,proc_path,error_number,
            cgroup,snapshots,context.get('parent_context'),resource_scope_identity,harness_wait_result)
        record['error_observed_ns']=context.get('error_observed_ns'); diagnostics.append(record)
    try:
        entries = list(pathlib.Path('/proc').iterdir())
    except OSError as exc:
        add_error('/proc:' + repr(exc),exc=exc,pid=None,proc_path=proc_error_path(exc))
        if proc_diagnostics is not None: proc_diagnostics.extend(diagnostics)
        return ([], errors)
    for ent in entries:
        if not ent.name.isdigit(): continue
        pid = int(ent.name); identity_changes = []; completed = False; before_observation = None; membership_before = None
        for attempt in range(3):
            before = None; before_observation = None; membership_before = None
            context = {'before':None,'after':None,'cgroup':None,'parent_context':None}
            try:
                before_observation = proc_stat_observation(pid)
                context['before'] = before_observation
                if before_observation.get('stat') is None: raise before_observation['error_object']
                before = before_observation['stat']
                if resource_scope_identity:
                    membership_before = observe_proc_cgroup(pid,before.get('start'),before_observation)
                    context['cgroup'] = membership_before
                row = read_proc_identity(pid)
                returned_start = row.get('start')
                if before.get('start') != returned_start:
                    identity_changes.append({'before_start':before.get('start'),'returned_start':returned_start})
                    continue
                if identity_changes:
                    context['cgroup']=observe_proc_cgroup(pid,returned_start,before_observation)
                    context['after']=context['cgroup'].get('after')
                    add_note({'kind':'pid-identity-rescanned','source':'marker-scan','pid':pid,
                              'identity_changes':identity_changes,'accepted_start':returned_start,'attempts':attempt + 1},context)
                if row['env'].get('CMPMARK') == marker: matches.append(row)
                completed = True; break
            except PermissionError as exc:
                context['error_observed_ns']=time.time_ns()
                if context.get('cgroup') is None and before is not None:
                    context['cgroup'] = observe_proc_cgroup(pid,before.get('start'),before_observation)
                message=f'{ent.name}:permission:{exc.errno}:{proc_error_path(exc)}'
                add_error(message,pid,before.get('start') if before else None,exc,context); completed = True; break
            except (OSError, ValueError, IndexError) as exc:
                context['error_observed_ns']=time.time_ns()
                expected = {'pid':pid,'start':before.get('start') if before else None}
                context['after'] = None
                partial = getattr(exc,'partial_identity',None)
                if (isinstance(partial,dict) and partial.get('pid') == pid and
                        before is not None and partial.get('start') == before.get('start') and
                        (partial.get('env') or {}).get('CMPMARK') == marker):
                    add_note({'kind':'partial-positive-marker-observation','source':'marker-scan',
                              'pid':pid,'expected_start':expected.get('start'),'argv0':partial.get('argv0'),
                              'cmpmark':marker,'marker_match':True,'exe_identity_complete':False,
                              'error_errno':getattr(exc,'errno',None),'error_path':proc_error_path(exc)},context)
                if isinstance(exc, OSError) and exc.errno in (errno.ENOENT, errno.ESRCH):
                    gone, verification = verified_process_exit(expected)
                    verification_observation = verification.get('stat_observation')
                    context['after'] = verification_observation
                    retry_paths = {f'/proc/{pid}/exe'}
                    if resource_scope_identity is None:
                        retry_paths.add(f'/proc/{pid}/environ')
                    if (not gone and verification.get('verification') == 'same-process-live' and
                            expected.get('start') is not None and proc_error_path(exc) in retry_paths):
                        rechecks = []
                        for _ in range(3):
                            time.sleep(0.001)
                            gone, verification = verified_process_exit(expected)
                            verification_observation = verification.get('stat_observation')
                            rechecks.append({'gone':gone,**{k:v for k,v in verification.items() if k != 'stat_observation'},
                                             'stat_observation':verification_observation})
                            if gone or verification.get('verification') != 'same-process-live': break
                        context['after'] = verification_observation
                        context['rechecks'] = rechecks
                    if gone:
                        if context.get('cgroup') is None:
                            context['cgroup'] = proc_cgroup_info(pid)
                        add_note({'kind':'verified-process-exit','source':'marker-scan','pid':pid,
                                  'expected_start':expected.get('start'),'error':repr(exc),'error_errno':exc.errno,
                                  'error_path':proc_error_path(exc),'verification':verification,
                                  'rechecks':context.get('rechecks',[])},context)
                        completed = True; break
                    if verification.get('verification') == 'same-process-zombie':
                        proof=verify_nonrunnable_group(expected,before_observation,verification,harness_wait_result)
                        context['after']=verification_observation; context['cgroup']=proof.get('cgroup_observation')
                        context['parent_context']=proof.get('parent_context')
                        note={'kind':'verified-nonrunnable-zombie' if proof.get('ok') else 'unverified-zombie-group',
                              'source':'marker-scan','pid':pid,'expected_start':expected.get('start'),
                              'current_start':verification.get('current_start'),'state':verification.get('state'),
                              'error':repr(exc),'error_errno':exc.errno,'error_path':proc_error_path(exc),
                              'verification':verification.get('verification'),'proof':proof}
                        if proof.get('ok'):
                            add_note(note,context)
                        else:
                            message=f'{ent.name}:proc:{exc.errno}:{proc_error_path(exc)}:zombie-proof:{proof.get("reason")}'
                            add_note(note,context); add_error(message,pid,expected.get('start'),exc,context)
                        completed = True; break
                    if verification.get('verification') in ('pid-reused-zombie','pid-present-zombie-unidentified'):
                        if context.get('cgroup') is None: context['cgroup']=proc_cgroup_info(pid)
                        message=f'{ent.name}:proc:{exc.errno}:{proc_error_path(exc)}:{verification.get("verification")}'
                        add_note({'kind':'unverified-zombie-identity','source':'marker-scan','pid':pid,
                                  'expected_start':expected.get('start'),'current_start':verification.get('current_start'),
                                  'state':verification.get('state'),'error':repr(exc),'error_errno':exc.errno,
                                  'error_path':proc_error_path(exc),'verification':verification.get('verification')},context)
                        add_error(message,pid,expected.get('start'),exc,context); completed = True; break
                    if verification.get('verification') == 'same-process-live' and proc_is_kernel_thread(pid, expected.get('start')):
                        if resource_scope_identity:
                            membership_after=observe_proc_cgroup(pid,expected.get('start'),verification_observation)
                            context['cgroup']=membership_after
                        elif context.get('cgroup') is None:
                            context['cgroup']=observe_proc_cgroup(pid,expected.get('start'),verification_observation)
                        context['after']=verification_observation
                        add_note({'kind':'verified-kernel-thread-without-userspace-mm','source':'marker-scan',
                                  'pid':pid,'expected_start':expected.get('start'),'current_start':verification.get('current_start'),
                                  'error':repr(exc),'error_errno':exc.errno,'error_path':proc_error_path(exc)},context)
                        completed = True; break
                    if verification.get('verification') in ('pid-reused-live','pid-present-unidentified'):
                        identity_changes.append({'before_start':expected.get('start'),'returned_start':verification.get('current_start'),
                                                 'read_error_errno':exc.errno})
                        if resource_scope_identity:
                            context['after']=verification_observation
                            message=f'{ent.name}:proc:{exc.errno}:{proc_error_path(exc)}:{verification.get("verification")}'
                            add_note({'kind':'resource-membership-identity-changed','source':'marker-scan','pid':pid,
                                      'expected_start':expected.get('start'),'current_start':verification.get('current_start'),
                                      'state':verification.get('state'),'error':repr(exc),'error_errno':exc.errno,
                                      'error_path':proc_error_path(exc),'membership_before':membership_before},context)
                            add_error(message,pid,expected.get('start'),exc,context)
                            completed=True; break
                        continue
                    error_text = f'{ent.name}:proc:{exc.errno}:{proc_error_path(exc)}:{verification.get("verification")}'
                    if verification.get('verification') == 'same-process-live' and resource_scope_identity:
                        expected_control = resource_scope_identity.get('control_group')
                        if not expected_control and resource_scope_identity.get('cgroup_path', '').startswith('/sys/fs/cgroup/'):
                            expected_control = '/' + resource_scope_identity['cgroup_path'].removeprefix('/sys/fs/cgroup/').lstrip('/')
                        membership_after=observe_proc_cgroup(pid,expected.get('start'),verification_observation)
                        context['after']=verification_observation; context['cgroup']=membership_after
                        pre_membership=membership_before.get('membership',{}) if isinstance(membership_before,dict) else {}
                        post_membership=membership_after.get('membership',{})
                        path = pathlib.Path(proc_error_path(exc))
                        if (exc.errno == errno.ESRCH and proc_error_path(exc) == f'/proc/{pid}/environ' and path.name == 'environ' and expected_control and
                                verification.get('current_start') == expected.get('start') and
                                not identity_changes and
                                membership_before and membership_before.get('verified_identity') is True and
                                membership_after.get('verified_identity') is True and
                                pre_membership.get('path') == expected_control and post_membership.get('path') == expected_control and
                                pre_membership.get('read_error') is None and post_membership.get('read_error') is None):
                            add_note({'kind':'resource-scope-proc-read-candidate','source':'marker-scan','pid':pid,
                                      'expected_start':expected.get('start'),'current_start':verification.get('current_start'),
                                      'state':verification.get('state'),'error':repr(exc),'error_errno':exc.errno,
                                      'error_path':proc_error_path(exc),'observer_error':error_text,
                                      'proc_cgroup':post_membership.get('path'),'scope_control_group':expected_control,
                                      'membership_before':membership_before,'membership_after':membership_after},context)
                        else:
                            add_note({'kind':'unattributed-resource-proc-read-error','source':'marker-scan','pid':pid,
                                      'expected_start':expected.get('start'),'current_start':verification.get('current_start'),
                                      'state':verification.get('state'),'error':repr(exc),'error_errno':exc.errno,
                                      'error_path':proc_error_path(exc),'proc_cgroup':post_membership.get('path'),
                                      'scope_control_group':expected_control,'membership_before':membership_before,
                                      'membership_after':membership_after},context)
                        add_error(error_text,pid,expected.get('start'),exc,context)
                    elif isinstance(exc, OSError):
                        if context.get('cgroup') is None and before is not None:
                            context['cgroup']=observe_proc_cgroup(pid,expected.get('start'),before_observation)
                        add_error(error_text,pid,expected.get('start'),exc,context)
                    else:
                        if context.get('cgroup') is None and before is not None:
                            context['cgroup']=observe_proc_cgroup(pid,expected.get('start'),before_observation)
                        elif context.get('cgroup') is None:
                            context['cgroup']=proc_cgroup_info(pid)
                        add_error(f'{ent.name}:proc:malformed:{exc!r}',pid,expected.get('start'),exc,context,
                                  proc_path=proc_error_path(exc))
                elif isinstance(exc,OSError):
                    if context.get('cgroup') is None and before is not None:
                        context['cgroup']=observe_proc_cgroup(pid,before.get('start'),before_observation)
                    add_error(f'{ent.name}:proc:{exc.errno}:{proc_error_path(exc)}',pid,
                              before.get('start') if before else None,exc,context)
                else:
                    if context.get('cgroup') is None and before is None: context['cgroup']=proc_cgroup_info(pid)
                    add_error(f'{ent.name}:proc:malformed:{exc!r}',pid,
                              before.get('start') if before else None,exc,context,proc_path=proc_error_path(exc))
                completed = True; break
        if not completed:
            add_error(f'{ent.name}:identity-race:retries-exhausted:{identity_changes!r}',pid,
                      before.get('start') if before else None,context={'before':before_observation,
                      'after':None,'cgroup':membership_before,'proc_path':f'/proc/{pid}/stat'})
    for note in notes[note_start:]:
        if not isinstance(note,dict): continue
        pid=note.get('pid'); start=note.get('expected_start',note.get('current_start'))
        if 'proc_path' not in note: note['proc_path']=note.get('error_path') or (f'/proc/{pid}/stat' if pid is not None else '/proc')
        note.setdefault('errno',note.get('error_errno')); note.setdefault('start_time',start)
        note.setdefault('cgroup',note.get('proc_cgroup'))
        note.setdefault('cell_cgroup',resource_scope_identity.get('control_group') if isinstance(resource_scope_identity,dict) else None)
        note.setdefault('harness_wait_result',harness_wait_result)
        if not any(d.get('event_type')=='note' and d.get('message')==note.get('kind') and d.get('pid')==pid for d in diagnostics):
            diagnostics.append(proc_observation_record('note',note.get('kind'),pid,start,note.get('proc_path'),
                note.get('errno'),note.get('cgroup_observation'),note.get('identity_snapshots'),
                note.get('parent_context'),resource_scope_identity,harness_wait_result))
    if proc_diagnostics is not None: proc_diagnostics.extend(diagnostics)
    return (matches, errors)

def find_token_in_mem(expected, token, marker):
    """Scan mapped bytes only while the exact marked process identity stays live."""; identity = dict(expected) if isinstance(expected, dict) else {'pid': int(expected)}; pid = int(identity['pid']); needle = token.encode(); observed = {'pid': pid, 'expected_start': identity.get('start'),
        'relevant_mappings': 0, 'mappings_scanned': 0, 'bytes_scanned': 0, 'coverage_complete': False,
        'identity_before': None, 'identity_after': None, 'error': None, 'observation_note': None, 'seen': None}
    def validate():
        row = read_proc_identity(pid)
        if identity.get('start') is None or row.get('start') != identity.get('start'):
            raise RuntimeError('process start time changed')
        if row.get('state') in ('Z', 'X'):
            raise RuntimeError('process is not live: ' + row.get('state', '?'))
        if marker and (row.get('argv0') != marker or row.get('env', {}).get('CMPMARK') != marker):
            raise RuntimeError('process marker changed')
        return {k: row.get(k) for k in ('pid', 'start', 'ppid', 'sid', 'state', 'argv0', 'exe')}
    fd = None; found = False
    try:
        observed['proc_cgroup_observation']=proc_cgroup_info(pid)
        observed['identity_before_observed_ns']=time.time_ns(); observed['identity_before'] = validate()
        observed['identity_before_completed_ns']=time.time_ns(); maps_path = pathlib.Path(f'/proc/{pid}/maps')
        try: maps_text = maps_path.read_text()
        except OSError as exc: raise RuntimeError(f'maps-read:{errno_label(exc.errno)}:{exc.errno}:{type(exc).__name__}:{maps_path}') from exc
        maps = maps_text.splitlines()
        if not maps:
            raise RuntimeError('empty maps observation')
        try:
            fd = os.open(f'/proc/{pid}/mem', os.O_RDONLY | os.O_CLOEXEC)
        except OSError as exc:
            raise RuntimeError(f'memory-open:{errno_label(exc.errno)}:{exc.errno}:{type(exc).__name__}:/proc/{pid}/mem') from exc
        scanned_all = True
        for line in maps:
            parts = line.split(None, 2)
            if len(parts) < 2:
                raise RuntimeError('malformed maps row')
            if 'r' not in parts[1] or 'w' not in parts[1]: continue
            observed['relevant_mappings'] += 1
            try: lo, hi = (int(x, 16) for x in parts[0].split('-', 1))
            except (ValueError, TypeError) as exc: raise RuntimeError('malformed mapping bounds') from exc
            if hi <= lo: raise RuntimeError('empty relevant mapping')
            pos = lo; overlap = b''
            while pos < hi:
                try: chunk = os.pread(fd, min(65536, hi - pos), pos)
                except OSError as exc: raise RuntimeError(f'incomplete-map:{errno_label(exc.errno)}:{exc.errno}:{type(exc).__name__}:/proc/{pid}/mem') from exc
                if not chunk: raise RuntimeError('incomplete-map:zero-read')
                observed['bytes_scanned'] += len(chunk); data = overlap + chunk
                if needle in data:
                    found = True; observed['seen'] = True; scanned_all = False; break
                overlap = data[-max(0, len(needle) - 1):] if len(needle) > 1 else b''; pos += len(chunk)
            if found: break
            observed['mappings_scanned'] += 1
        if observed['relevant_mappings'] == 0:
            raise RuntimeError('no relevant readable writable mappings')
        observed['identity_after_observed_ns']=time.time_ns(); observed['identity_after'] = validate()
        observed['identity_after_completed_ns']=time.time_ns(); observed['seen'] = found; observed['coverage_complete'] = scanned_all and observed['mappings_scanned'] == observed['relevant_mappings'] and observed['bytes_scanned'] > 0
        if not found and not observed['coverage_complete']:
            raise RuntimeError('incomplete memory coverage')
    except (OSError, PermissionError, RuntimeError, ValueError, IndexError) as exc:
        observed['error_observed_ns']=time.time_ns()
        error_os=exc; seen_errors=set()
        while error_os is not None and id(error_os) not in seen_errors:
            seen_errors.add(id(error_os))
            if isinstance(error_os,OSError):
                observed['error_errno']=error_os.errno; observed['error_path']=proc_error_path(error_os); break
            error_os=error_os.__cause__ or error_os.__context__
        note = verified_exit_note(exc, identity, 'memory-token-scan')
        if note is not None:
            observed['observation_note'] = note
            observed['identity_after_error'] = repr(exc)
            observed['coverage_complete'] = False
        else:
            observed['error'] = repr(exc)
            if observed['identity_after'] is None:
                try: observed['identity_after'] = validate()
                except (OSError, PermissionError, RuntimeError, ValueError, IndexError) as after_exc:
                    observed['identity_after_error'] = repr(after_exc)
    finally:
        if fd is not None: os.close(fd)
    return observed

def scan_peer_pid(server_port, peer_port):
    """Map an accepted TCP peer to a host PID through /proc/net/tcp and socket fds."""
    try:
        lines = pathlib.Path('/proc/net/tcp').read_text().splitlines()[1:]
    except OSError as exc:
        return (None, repr(exc))
    inode = None
    for line in lines:
        p = line.split()
        if len(p) < 10 or p[3] != '01': continue
        try:
            local_port = int(p[1].split(':')[1], 16); remote_port = int(p[2].split(':')[1], 16)
        except (ValueError, IndexError):
            continue
        if local_port == peer_port and remote_port == server_port:
            inode = p[9]; break
    if inode is None: return (None, None)
    wanted = f'socket:[{inode}]'
    for ent in pathlib.Path('/proc').iterdir():
        if not ent.name.isdigit(): continue
        fd_dir = ent / 'fd'
        try:
            for fdp in fd_dir.iterdir():
                try:
                    if os.readlink(fdp) == wanted: return (int(ent.name), None)
                except FileNotFoundError:
                    continue
        except FileNotFoundError:
            continue
        except PermissionError as exc:
            return (None, repr(exc))
    return (None, None)

class Canary:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); self.sock.bind(('127.0' + '.0.1', 0)); self.sock.listen(16); self.sock.settimeout(0.05); self.port = self.sock.getsockname()[1]; (self.rows, self.errors) = ([], []); self.stop_event = threading.Event(); self.started = True; self.shutdown_requested = False; self.worker_exited_at_ns = None; self.closed = False; self.thread = threading.Thread(target=self._serve, daemon=True); self.thread.start()

    def _serve(self):
        try:
            while not self.stop_event.is_set():
                try:
                    (conn, addr) = self.sock.accept()
                except socket.timeout:
                    continue
                except OSError as exc:
                    if not self.stop_event.is_set(): self.errors.append('listener-worker:' + repr(exc))
                    return
                with conn:
                    conn.settimeout(0.2); peer_port = conn.getpeername()[1]; (pid, err) = scan_peer_pid(self.port, peer_port)
                    if err: self.errors.append('listener-peer-scan:' + err)
                    row = {'remote': addr[0], 'peer_port': peer_port, 'peer_pid': pid, 'timestamp_ns': time.time_ns()}
                    if pid:
                        ident = read_proc_identity(pid); row['peer_marker'] = ident['env'].get('CMPMARK'); row['peer_argv0'] = ident['argv0']
                    self.rows.append(row); conn.recv(1024)
        except BaseException as exc:
            self.errors.append('listener-worker-exception:' + repr(exc))
        finally:
            self.worker_exited_at_ns = time.time_ns()

    def close(self):
        self.shutdown_requested = True; self.stop_event.set()
        try:
            self.sock.close()
        except OSError:
            pass
        self.thread.join(timeout=1); self.closed = not self.thread.is_alive()

    @property
    def healthy(self): return self.started and self.closed and self.shutdown_requested and self.worker_exited_at_ns is not None and not self.errors

def append_jsonl(path, row):
    path = pathlib.Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(row, sort_keys=True) + '\n'); f.flush(); os.fsync(f.fileno())

def ledger_state(path):
    events = []
    if not pathlib.Path(path).is_file(): return events
    for line in pathlib.Path(path).read_text().splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            continue
    return events

def cell_key(arm, fixture, rep): return f'{arm}/{fixture}/{rep}'

def completed_cells(path): return {e.get('key') for e in ledger_state(path) if e.get('event') == 'complete'}

def cgroup_snapshot(unit, tools, expected=None):
    if isinstance(expected, dict) and expected.get('unit') == unit and expected.get('cgroup_path'):
        cg = pathlib.Path(expected['cgroup_path'])
        try: cg.stat()
        except FileNotFoundError as exc: return {'ok':False,'path':str(cg),'files':{},'lookup':{'state':'absent','unit':unit,'path':str(cg)},'scope_identity':expected,'errors':[f'acquired cgroup path stat:{exc.errno}:{cg}']}
        except OSError as exc: return {'ok':False,'path':str(cg),'files':{},'lookup':{'state':'error','unit':unit,'path':str(cg)},'scope_identity':expected,'errors':[f'acquired cgroup path stat:{exc.errno}:{type(exc).__name__}:{cg}']}
        lookup = {'state':'present','unit':unit,'control_group':expected.get('control_group'),'path':str(cg),'cgroup_present':True,'verified_from_acquisition':True,'errors':[]}
    else:
        lookup = scope_lookup(unit, tools, expected)
        if lookup.get('state') != 'present' or not lookup.get('path'):
            return {'ok': False, 'path': lookup.get('path'), 'files': {}, 'lookup': lookup,
                    'scope_identity': expected, 'errors': lookup.get('errors') or ['scope/cgroup absent during observation']}
        cg = pathlib.Path(lookup['path'])
    files = {}; errors = []
    for name in ('memory.current', 'memory.peak', 'memory.max', 'memory.events', 'pids.current', 'pids.peak', 'pids.max', 'pids.events', 'cgroup.events'):
        try:
            files[name] = pathlib.Path(cg / name).read_text().strip()
        except OSError as exc:
            errors.append(f'{cg / name}:{exc.errno}:{type(exc).__name__}')
    identity = {'unit': unit, 'control_group': lookup.get('control_group') or (expected or {}).get('control_group'), 'cgroup_path': str(cg)}
    return {'ok': not errors, 'path': str(cg), 'files': files, 'lookup': lookup,
            'scope_identity': identity, 'errors': errors}

def cgroup_tree_snapshot(root):
    """Read all direct memberships below one acquired cgroup identity."""
    root = pathlib.Path(root); members = []; directories = []; errors = []; stack = [root]
    try: root_stat = root.stat()
    except FileNotFoundError: return {'path':str(root),'exists':False,'complete':True,'directories':[],'members':[],'errors':[]}
    except OSError as exc: return {'path':str(root),'exists':None,'complete':False,'directories':[],'members':[],'errors':['root-stat:'+repr(exc)]}
    if not stat.S_ISDIR(root_stat.st_mode): return {'path':str(root),'exists':True,'complete':False,'directories':[],'members':[],'errors':['cgroup root is not a directory']}
    while stack:
        current = stack.pop()
        try: current_stat = current.stat()
        except FileNotFoundError: continue
        except OSError as exc: errors.append('directory-stat:'+str(current)+':'+repr(exc)); continue
        if not stat.S_ISDIR(current_stat.st_mode): errors.append('cgroup child is not a directory:'+str(current)); continue
        directories.append(str(current))
        try: rows = (current / 'cgroup.procs').read_text().split()
        except FileNotFoundError:
            try: current.stat()
            except FileNotFoundError: continue
            except OSError as exc: errors.append('directory-recheck:'+str(current)+':'+repr(exc)); continue
            errors.append('cgroup.procs missing:'+str(current)); rows = []
        except OSError as exc: errors.append('cgroup.procs:'+str(current)+':'+repr(exc)); rows = []
        for value in rows:
            if not value.isdigit(): errors.append('malformed cgroup.procs:'+str(current)+':'+repr(value))
            else: members.append({'pid':int(value),'cgroup_path':str(current)})
        try: children = list(current.iterdir())
        except FileNotFoundError: continue
        except OSError as exc: errors.append('cgroup-children:'+str(current)+':'+repr(exc)); continue
        for child in children:
            try:
                child_stat = child.stat()
                if stat.S_ISDIR(child_stat.st_mode): stack.append(child)
            except FileNotFoundError: continue
            except OSError as exc: errors.append('cgroup-child-stat:'+str(child)+':'+repr(exc))
    try: root.stat(); exists = True
    except FileNotFoundError: exists = False
    except OSError as exc: errors.append('root-final-stat:'+repr(exc)); exists = None
    return {'path':str(root),'exists':exists,'complete':not errors,'directories':directories,
            'members':members,'errors':errors}

def cgroup_evidence(samples):
    good = [s for s in samples if s.get('ok') is True]; paths = {s.get('path') for s in good}
    finals = [s for s in samples if s.get('final') is True]
    if not good or len(paths) != 1: return {'cgroup_ok': False, 'resource_final_sample': False, 'resource_samples': samples, 'resource_scope_identity': None}
    raw = [s['files'] for s in good]
    def nums(key): return [int(f[key]) for f in raw if key in f and f[key].isdigit()]
    final_ok = len(finals) == 1 and finals[0].get('ok') is True and finals[0].get('path') in paths; final_raw = finals[0].get('files', {}) if final_ok else {}; observed_raw = final_raw if final_ok else raw[-1]; source = 'final' if final_ok else 'last_successful_nonfinal'; first = raw[0]; initial_mem = parse_text_kv(first.get('memory.events', '')); initial_pids = parse_text_kv(first.get('pids.events', ''))
    observed_mem = parse_text_kv(observed_raw.get('memory.events', '')); observed_pids = parse_text_kv(observed_raw.get('pids.events', ''))
    mem = {k: observed_mem[k] for k in ('low','high','max','oom','oom_kill') if k in observed_mem}; pids = {k: observed_pids[k] for k in ('max',) if k in observed_pids}; ml = [int(observed_raw['memory.max'])] if observed_raw.get('memory.max', '').isdigit() else []; pl = [int(observed_raw['pids.max'])] if observed_raw.get('pids.max', '').isdigit() else []; identities = {json.dumps(s.get('scope_identity'), sort_keys=True) for s in good if s.get('scope_identity')}; identity = json.loads(next(iter(identities))) if len(identities) == 1 else None
    return {'cgroup_ok': bool(samples) and all(s.get('ok') is True for s in samples) and len(paths) == 1,
            'resource_final_sample': final_ok, 'counter_baseline': 'zero origin: fresh unique systemd scope',
            'counter_origin': {'memory.events': {k: 0 for k in ('low','high','max','oom','oom_kill')}, 'pids.events': {'max': 0}},
            'initial_event_counts': {'memory.events': initial_mem, 'pids.events': initial_pids},
            'observed_event_counts_source': source, 'effective_limits_source': source,
            'event_counts_zero_origin': True, 'resource_scope_identity': identity,
            'cgroup_path': next(iter(paths)), 'memory_peak': max(nums('memory.peak'), default=0),
            'memory_limit': ml[-1] if ml else None, 'effective_limits': {'memory.max': ml[-1] if ml else None, 'pids.max': pl[-1] if pl else None},
            'memory_events': mem, 'pids_peak': max(nums('pids.peak'), default=0), 'pids_limit': pl[-1] if pl else None,
            'pids_events': pids, 'resource_samples': samples, 'raw_cgroup_files': raw,
            'failed_final_samples': [s for s in finals if s.get('ok') is not True]}

def reconcile_resource_oom_observer_errors(fixture, marker, observer_errors, observation_notes, evidence):
    """Excuse only a proved in-scope procfs ESRCH during this cell's recorded OOM kill."""
    if fixture != 'mem_cap' or not isinstance(evidence, dict): return []
    identity = evidence.get('resource_scope_identity')
    events = evidence.get('memory_events')
    limits = evidence.get('effective_limits')
    initial = evidence.get('initial_event_counts', {}).get('memory.events', {})
    finals = [s for s in evidence.get('resource_samples', []) if s.get('final') is True]
    final_raw = finals[0].get('files', {}) if len(finals) == 1 and finals[0].get('ok') is True else {}
    final_events = parse_text_kv(final_raw.get('memory.events', ''))
    zero_origin = (evidence.get('event_counts_zero_origin') is True and isinstance(initial, dict) and
                   all(initial.get(k) == 0 for k in ('low','high','max','oom','oom_kill')))
    oom_proved = (evidence.get('cgroup_ok') is True and evidence.get('resource_final_sample') is True and
                  zero_origin and isinstance(identity, dict) and identity.get('unit') == scope_name(marker) and
                  identity.get('cgroup_path') == evidence.get('cgroup_path') and
                  isinstance(limits, dict) and limits.get('memory.max') == CAPS['memory.max'] and
                  evidence.get('memory_limit') == CAPS['memory.max'] and
                  isinstance(evidence.get('memory_peak'), int) and evidence['memory_peak'] >= CAPS['memory.max'] and
                  isinstance(events, dict) and isinstance(events.get('oom_kill'), int) and events['oom_kill'] > 0 and
                  final_events.get('oom_kill', 0) > 0 and
                  any(final_events.get(k, 0) > 0 for k in ('max','oom')) and
                  any(events.get(k, 0) > 0 for k in ('max','oom')))
    if not oom_proved: return []
    remaining = list(observer_errors); explained = []
    for note in observation_notes:
        if note.get('kind') != 'resource-scope-proc-read-candidate': continue
        expected_path = f"/proc/{note.get('pid')}/environ"
        before = note.get('membership_before'); after = note.get('membership_after')
        before_member = before.get('membership', {}) if isinstance(before, dict) else {}
        after_member = after.get('membership', {}) if isinstance(after, dict) else {}
        error_text = note.get('observer_error')
        if (note.get('error_errno') != errno.ESRCH or note.get('error_path') != expected_path or
                note.get('expected_start') is None or note.get('current_start') != note.get('expected_start') or
                note.get('state') in ('Z','X') or note.get('proc_cgroup') != identity.get('control_group') or
                note.get('scope_control_group') != identity.get('control_group') or error_text not in remaining or
                not isinstance(before,dict) or before.get('verified_identity') is not True or
                not isinstance(after,dict) or after.get('verified_identity') is not True or
                before_member.get('read_error') is not None or after_member.get('read_error') is not None or
                before_member.get('path') != identity.get('control_group') or
                after_member.get('path') != identity.get('control_group')):
            continue
        exit_proof = verify_oom_identity_exit(note)
        if exit_proof.get('ok') is not True: continue
        remaining.remove(error_text)
        explained.append({'kind':'verified-scope-oom-proc-exit','source':'marker-scan','pid':note['pid'],
                          'expected_start':note['expected_start'],'state':note.get('state'),
                          'error_errno':note['error_errno'],'error_path':note['error_path'],
                          'proc_cgroup':note['proc_cgroup'],'scope_control_group':identity['control_group'],
                          'membership_before':before,'membership_after':after,'identity_exit':exit_proof,
                          'proof':{'unit':identity['unit'],'memory.max':evidence['memory_limit'],
                                   'memory.peak':evidence['memory_peak'],'memory.events.oom_kill':final_events['oom_kill'],
                                   'memory.events.max':final_events.get('max',0),'memory.events.oom':final_events.get('oom',0),
                                   'final_sample':True,'zero_origin':True}})
    observer_errors[:] = remaining
    observation_notes.extend(explained)
    return explained

def verify_oom_identity_exit(note):
    """Require same-start disappearance or a separately proved nonrunnable group."""
    expected={'pid':note.get('pid'),'start':note.get('expected_start')}
    before=note.get('membership_before',{}).get('before') if isinstance(note.get('membership_before'),dict) else None
    gone, verification=verified_process_exit(expected)
    result={'ok':False,'pid':expected['pid'],'start_time':expected['start'],
            'observed_ns':time.time_ns(),'verification':verification}
    if gone:
        result['ok']=True; result['kind']='same-identity-proc-entry-gone'; return result
    if verification.get('verification') == 'same-process-zombie':
        proof=verify_nonrunnable_group(expected,before,verification,note.get('harness_wait_result'))
        result['ok']=proof.get('ok') is True; result['kind']='same-identity-nonrunnable-group'
        result['nonrunnable_group']=proof
    return result

def finalize_observation_diagnostics(observer_errors, observation_notes, proc_diagnostics,
                                     memory_observations, cgroup_samples, scope_identity,
                                     harness_wait_result):
    """Keep a structured, timestamped record for every cell observer error and note."""
    diagnostics=list(proc_diagnostics); scope_group=scope_identity.get('control_group') if isinstance(scope_identity,dict) else None
    for note in observation_notes:
        if not isinstance(note,dict): continue
        pid=note.get('pid'); start=note.get('expected_start',note.get('current_start'))
        note.setdefault('proc_path',note.get('error_path'))
        note.setdefault('errno',note.get('error_errno'))
        note.setdefault('start_time',start)
        note.setdefault('cgroup',note.get('proc_cgroup'))
        if note.get('cell_cgroup') is None: note['cell_cgroup']=scope_group
        note.setdefault('identity_snapshots',None)
        note.setdefault('cgroup_observation',None)
        note.setdefault('parent_context',None)
        note.setdefault('harness_wait_result',harness_wait_result)
        note.setdefault('error_observed_ns',None)
        if not any(d.get('event_type')=='note' and d.get('message')==note.get('kind') and d.get('pid')==pid for d in diagnostics):
            diagnostics.append(proc_observation_record('note',note.get('kind'),pid,start,note.get('proc_path'),
                note.get('errno'),note.get('cgroup_observation'),note.get('identity_snapshots'),
                note.get('parent_context'),scope_identity,harness_wait_result))
    for observation in memory_observations:
        error=observation.get('error') or observation.get('observation_note')
        if not error: continue
        path_match=re.search(r'(/proc/\d+/[^\s:]+)',str(error)); pid=observation.get('pid')
        cgroup_observation=observation.get('proc_cgroup_observation')
        identity={'before':observation.get('identity_before'),'after':observation.get('identity_after'),
                  'before_observed_ns':observation.get('identity_before_observed_ns'),
                  'after_observed_ns':observation.get('identity_after_observed_ns')}
        diagnostics.append(proc_observation_record('error' if observation.get('error') else 'note',error,pid,
            observation.get('expected_start'),path_match.group(1) if path_match else None,
            observation.get('error_errno'),cgroup_observation,identity,None,scope_identity,harness_wait_result))
    for sample in cgroup_samples:
        for error in sample.get('errors',[]):
            path_match=re.search(r'(/[^\s:]+)',str(error)); errno_match=re.search(r':(\d+):',str(error))
            diagnostics.append({'event_type':'cgroup-error','message':error,'proc_path':None,
                'errno':int(errno_match.group(1)) if errno_match else None,'pid':None,'start_time':None,
                'cgroup':sample.get('path'),'cell_cgroup':scope_group,'observed_ns':time.time_ns(),
                'cgroup_observation':{'path':sample.get('path'),'error_path':path_match.group(1) if path_match else None,
                                      'sample_observed_ns':sample.get('barrier_observed_ns')},
                'identity_snapshots':None,'parent_context':None,'harness_wait_result':harness_wait_result})
    counts={}
    for item in diagnostics:
        if item.get('event_type')=='error': counts[item.get('message')]=counts.get(item.get('message'),0)+1
    for error in observer_errors:
        if counts.get(error,0):
            counts[error]-=1; continue
        path_match=re.search(r'(/proc/\d+/[^\s:]+)',str(error)); pid_match=re.match(r'(\d+):',str(error))
        errno_match=re.search(r'(?::|errno=)(\d+)(?::|\b)',str(error))
        pid=int(path_match.group(1).split('/')[2]) if path_match else (int(pid_match.group(1)) if pid_match else None)
        matching=next((x for x in memory_observations if x.get('pid')==pid),{})
        diagnostics.append(proc_observation_record('error',error,pid,matching.get('expected_start'),
            path_match.group(1) if path_match else None,int(errno_match.group(1)) if errno_match else None,
            matching.get('proc_cgroup_observation'),None, None,scope_identity,harness_wait_result))
    for item in diagnostics:
        item.setdefault('proc_path',None); item.setdefault('errno',None); item.setdefault('pid',None)
        item.setdefault('start_time',None); item.setdefault('cgroup',None)
        if item.get('cell_cgroup') is None: item['cell_cgroup']=scope_group
        item.setdefault('identity_snapshots',None); item.setdefault('cgroup_observation',None)
        item.setdefault('parent_context',None); item.setdefault('harness_wait_result',harness_wait_result)
        item.setdefault('error_observed_ns',None)
        if item.get('event_type')=='error':
            item['resolved']=item.get('message') not in observer_errors
            if item['resolved']:
                resolution=next((n for n in observation_notes if n.get('kind')=='verified-scope-oom-proc-exit' and
                                 n.get('pid')==item.get('pid') and n.get('error_path')==item.get('proc_path')),None)
                item['resolution_note']=resolution.get('kind') if resolution else 'separately-proved-observer-note'
    return diagnostics

def parse_text_kv(text):
    out = {}
    for line in text.splitlines():
        p = line.split()
        if len(p) == 2:
            try:
                out[p[0]] = int(p[1])
            except ValueError:
                pass
    return out

def signal_identity(expected, sig):
    if not hasattr(os,'pidfd_open') or not hasattr(signal,'pidfd_send_signal'): return False
    try: fd=os.pidfd_open(expected['pid'],0)
    except (OSError,ProcessLookupError): return False
    try:
        current=read_proc_identity(expected['pid'])
        if any(current.get(k)!=expected.get(k) for k in ('pid','start','ppid','sid','argv0','exe')): return False
        if current.get('env',{}).get('CMPMARK')!=expected.get('env',{}).get('CMPMARK'): return False
        signal.pidfd_send_signal(fd,sig); return True
    except (OSError,ProcessLookupError,PermissionError,ValueError,IndexError): return False
    finally: os.close(fd)

def release_resource_holder(marker, timeout=2, proc_diagnostics=None, harness_wait_result=None):
    holder_marker = marker + '-holder'; notes=[]; rows, errors = scan_marker(holder_marker, notes,proc_diagnostics=proc_diagnostics,harness_wait_result=harness_wait_result)
    result = {'marker': holder_marker, 'identity': rows[0] if len(rows) == 1 else None, 'signal': 'SIGKILL', 'released': False, 'errors': list(errors), 'observation_notes':notes}
    if errors or len(rows) != 1:
        result['errors'].append('expected exactly one live resource holder'); return result
    if not signal_identity(rows[0], signal.SIGKILL):
        result['errors'].append('resource holder identity changed or signal failed'); return result
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        left, err = scan_marker(holder_marker, notes,proc_diagnostics=proc_diagnostics,harness_wait_result=harness_wait_result); result['errors'].extend(err)
        if err: return result
        if not left: result['released'] = True; return result
        time.sleep(0.02)
    result['errors'].append('resource holder did not exit after exact signal'); return result

def stop_scope(marker, tools, expected=None, timeout=3):
    if not re.search('-(?:z|b|c2|a|a-bash)-r[^/]+$', marker):
        return {'unit': None, 'cgroup_path': None, 'cgroup_kill': False, 'stop_rc': None, 'cgroup_gone': True, 'scope_absent': True, 'tree_history': [], 'errors': [], 'pass': True}
    unit = scope_name(marker); details = {'unit': unit, 'cgroup_path': expected.get('cgroup_path') if isinstance(expected, dict) else None,
        'scope_identity': expected, 'cgroup_kill': False, 'stop_rc': None, 'stop_stderr': '', 'lookup_history': [],
        'tree_history': [], 'cgroup_gone': False, 'scope_absent': False, 'errors': []}
    if expected and expected.get('unit') not in (None, unit):
        details['errors'].append('scope unit identity mismatch'); details['pass'] = False; return details
    before = scope_lookup(unit, tools, expected); details['lookup_history'].append(before)
    verified = expected or ({'unit':unit,'control_group':before.get('control_group'),'cgroup_path':before.get('path')} if before.get('state') == 'present' and before.get('path') else None)
    if verified:
        details['scope_identity'] = verified; details['cgroup_path'] = verified.get('cgroup_path')
    if before.get('state') == 'error': details['errors'].extend(before.get('errors', ['scope lookup failed']))
    elif before.get('state') == 'present':
        cg = pathlib.Path(before['path']) if before.get('path') else None
        if cg is not None:
            tree = cgroup_tree_snapshot(cg); details['tree_history'].append({'stage':'before-stop',**tree})
            if not tree.get('complete'): details['errors'].extend(tree.get('errors', ['cgroup subtree scan incomplete']))
            try:
                kill_file = cg / 'cgroup.kill'
                try: kill_file.stat()
                except FileNotFoundError: pass
                else: kill_file.write_text('1'); details['cgroup_kill'] = True
            except OSError as exc:
                details['errors'].append('cgroup.kill:' + repr(exc))
    systemctl = tools.get('systemctl', pathlib.Path('/usr/bin/systemctl'))
    try:
        r = subprocess.run([str(systemctl), 'stop', '--no-block', unit], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3, check=False)
        details['stop_rc'] = r.returncode; details['stop_stderr'] = r.stderr.decode('utf-8', 'replace')
        if r.returncode not in (0, 5): details['errors'].append('stop rc=' + str(r.returncode) + ': ' + details['stop_stderr'])
    except (OSError, subprocess.TimeoutExpired) as exc:
        details['stop_stderr'] = repr(exc); details['errors'].append('stop request failed: ' + repr(exc))
    retry_window = min(max(float(timeout), 0.0), 3.0)
    deadline = time.monotonic() + retry_window
    current = before; tree = None
    while time.monotonic() < deadline:
        current = scope_lookup(unit, tools, verified); details['lookup_history'].append(current)
        if current.get('state') == 'error':
            details['errors'].extend(current.get('errors', ['scope lookup failed after stop'])); break
        tree = cgroup_tree_snapshot(verified['cgroup_path']) if verified and verified.get('cgroup_path') else None
        if tree is not None:
            details['tree_history'].append({'stage':'after-stop',**tree})
            if not tree.get('complete'):
                details['errors'].extend(tree.get('errors', ['cgroup subtree scan incomplete after stop'])); break
        tree_absent = tree is None or (tree.get('exists') is False and not tree.get('members'))
        if current.get('state') == 'absent' and tree_absent:
            details['cgroup_gone'] = True; details['scope_absent'] = True; break
        time.sleep(0.03)
    if not details['cgroup_gone'] and not details['errors']:
        members = tree.get('members', []) if isinstance(tree, dict) else []
        if members:
            pids = [str(row.get('pid')) for row in members[:12]]
            suffix = f' (+{len(members) - len(pids)} more)' if len(members) > len(pids) else ''
            details['errors'].append(f'scope/cgroup members remain after bounded stop retries ({retry_window:.2f}s): {", ".join(pids)}{suffix}')
        elif isinstance(tree, dict) and tree.get('exists') is True:
            details['errors'].append(f'empty scope cgroup remains after bounded stop retries ({retry_window:.2f}s): {tree.get("path")}')
        else:
            details['errors'].append(f'scope/cgroup absence not verified before timeout; unit state={current.get("state")!r}, path={current.get("path")!r}')
    details['pass'] = details['cgroup_gone'] and details['scope_absent'] and not details['errors'] and details['stop_rc'] in (0, 5)
    return details

def cleanup_marker(marker, tools, expected_scope=None, proc_diagnostics=None, harness_wait_result=None):
    notes=[]; (rows, errors) = scan_marker(marker, notes,proc_diagnostics=proc_diagnostics,harness_wait_result=harness_wait_result); killed = []
    for row in rows:
        if signal_identity(row, signal.SIGKILL): killed.append(row['pid'])
    deadline = time.monotonic() + 2
    while time.monotonic() < deadline:
        (left, err) = scan_marker(marker, notes,proc_diagnostics=proc_diagnostics,harness_wait_result=harness_wait_result); errors += err
        if not left: break
        for row in left: signal_identity(row, signal.SIGKILL)
        time.sleep(0.03)
    scope = stop_scope(marker, tools, expected_scope); (left, err) = scan_marker(marker, notes,proc_diagnostics=proc_diagnostics,harness_wait_result=harness_wait_result); errors += err; return {'killed_pids': killed, 'remaining': [r['pid'] for r in left], 'errors': errors, 'observation_notes':notes, 'observation_note_count':len(notes), 'scope': scope, 'pass': not errors and (not left) and (scope.get('pass') is True)}

def cleanup_failure_reason(cleanup):
    """Summarize marker and cgroup failures without discarding their causes."""
    parts = []; grouped = {}
    for error in cleanup.get('errors', []):
        if error == 'cleanup verification failed': continue
        match = re.match(r'^\d+:proc:(\d+):(.+)$', str(error))
        if match:
            label = f'proc errno={match.group(1)} {match.group(2)}'
        else:
            label = str(error)
        grouped[label] = grouped.get(label, 0) + 1
    for label, count in list(grouped.items())[:6]:
        parts.append(f'{label} ({count} occurrence' + ('' if count == 1 else 's') + ')')
    remaining = cleanup.get('remaining', [])
    if remaining: parts.append('marked processes remain: ' + ', '.join(map(str, remaining[:12])))
    scope = cleanup.get('scope', {})
    for error in scope.get('errors', []):
        if error not in parts: parts.append('scope: ' + str(error))
    lookup = scope.get('lookup_history', [])
    if lookup and not scope.get('pass'):
        last = lookup[-1]
        parts.append(f'scope lookup ended in {last.get("state")!r} at {last.get("path")!r}')
    trees = scope.get('tree_history', [])
    if trees and not scope.get('pass'):
        last_tree = trees[-1]
        if last_tree.get('members'):
            pids = [str(row.get('pid')) for row in last_tree['members'][:12]]
            parts.append('cgroup members remain: ' + ', '.join(pids))
        elif last_tree.get('exists') is True:
            parts.append('cgroup directory remains: ' + str(last_tree.get('path')))
        if last_tree.get('errors'):
            parts.extend('cgroup: ' + str(error) for error in last_tree['errors'][:3])
    if not parts: return 'cleanup absence verification failed without a recorded detail'
    return '; '.join(parts)

# ---------------------------------------------------------------------------
# Arm a: Kogen's containment helper (kogen-contain, backend linux-cgroupv2), launched
# Helper client used under qualification admission mode. `a-bash` keeps the unchanged
# bash workload on allowed_rw as a separate launch-availability check.
ARM_A_VARIANTS = ('a', 'a-bash')
ARM_A_LABEL = 'helper under qualification (no production admission record yet)'
ARM_A_BASE = pathlib.Path('/var/lib/containment-fixture')
ARM_A_HELPER = ARM_A_BASE / 'bin' / 'kogen-contain-linux-amd64'
# Deployment-specific build history is omitted from this public copy.
ARM_A_HELPER_SHA256 = '5b61d5a713e981f81da11d076bf99aa1a0e7b3e343c5b38428e960569443569b'
ARM_A_RO = ARM_A_BASE / 'ro'
ARM_A_TMPFS = ARM_A_BASE / 'tmpfs'
ARM_A_VENDOR = ROOT / 'vendor' / 'arm-a'
ARM_A_PINS = {'adapter.py': '54fcc737fa2e49d0d9ddc3d7ccf205a4b6459293ddf6481859a2074b51dde332',
              'validate.py': 'd0d2c000c0de473e607b581032d95bafc536d361e707175c742ffbcd7a2678b9',
              'manifest.json': 'f06708d6d4ef4efc1270511ebe63c7181f3b9a9caa2505a74eb542d60ce9a3f2'}
ARM_A_BACKEND = 'linux-cgroupv2'; ARM_A_BACKEND_ID = 'linux-ns-ptrace-v1'; ARM_A_QUAL_BACKEND_ID = 'linux-ns-ptrace-v1-under-qualification'
ARM_A_ACCOUNTING = 'under-qualification-linux-cgroupv2'; ARM_A_SEED_CAPABILITY = 'seeded-workspace-quota'
ARM_A_MANDATORY_CAPABILITIES = ('filesystem-denial', 'network-denial', 'environment-isolation', 'controller-protection',
    'descendant-custody', 'owner-death-cleanup', 'wall-timeout', 'cpu-timeout', 'memory-threshold', 'task-limit',
    'disk-limit', 'file-limit', 'bounded-output', 'reconciliation')
ARM_A_WRITABLE = ('allowed', 'home', 'temp', 'cache')  # allowed is the helper's private `build` dir
ARM_A_PRIVATE_DIRS = {'home': 'home', 'temp': 'temp', 'cache': 'cache', 'build': 'allowed'}
# Mandatory manifest fields with no b counterpart. wall/cpu are chosen so neither binds before the harness
# windows (15/40 s); reaction/grace/cleanup/overrun are the project's separate qualification programme's fixture-manifest values (reaction 1000 ms
# also bounds the helper's guardian-readiness wait, linux_custodian.go:608-630). cpu.max comes out at 100%.
ARM_A_TIMEOUTS = {'wall_ms': 60000, 'cpu_ms': 60000, 'cpu_overrun_ms': 2000, 'reaction_ms': 1000, 'term_grace_ms': 200, 'cleanup_ms': 1600}
ARM_A_STORAGE = {'disk_bytes': 67108864, 'files': 4096, 'stdout_bytes': 262144, 'stderr_bytes': 262144, 'output_total_bytes': 1048576}
ARM_A_SCAFFOLD_BYTES = 4 * 1024 * 1024; ARM_A_INODE_RESERVATION = 8192
ARM_A_REFUSED_RC = 3
ARM_A_CGROUP_FILES = ('memory.current', 'memory.peak', 'memory.max', 'memory.events', 'pids.current', 'pids.peak', 'pids.max', 'pids.events', 'cgroup.events')

def arm_a_load_pinned(name, vendor=None):
    path = pathlib.Path(vendor or ARM_A_VENDOR) / name; digest = sha_file(path)
    if digest != ARM_A_PINS[name]: raise RuntimeError(f'arm-a vendored {name} sha256 {digest} differs from pin')
    spec = importlib.util.spec_from_file_location('cmp_arm_a_' + name.split('.')[0], path); module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module); return module

def arm_a_statx_btime(path):
    """(btime_sec, btime_nsec) via libc statx(AT_SYMLINK_NOFOLLOW, STATX_BASIC_STATS|STATX_BTIME); Linux only."""
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True); buf = ctypes.create_string_buffer(256)
    if libc.statx(ctypes.c_int(-100), os.fsencode(str(path)), ctypes.c_int(0x100), ctypes.c_uint(0x7ff | 0x800), buf) != 0:
        err = ctypes.get_errno(); raise OSError(err, os.strerror(err), str(path))
    raw = buf.raw; mask = int.from_bytes(raw[0:4], 'little')
    if not mask & 0x800: raise RuntimeError('statx did not report a birth time for ' + str(path))
    return int.from_bytes(raw[80:88], 'little', signed=True), int.from_bytes(raw[88:92], 'little')

def arm_a_object_identity(path, btime=None):
    """The helper's birth-pinned root identity."""
    st = os.lstat(path)
    if not stat.S_ISDIR(st.st_mode): raise RuntimeError('arm-a root is not a real directory: ' + str(path))
    sec, nsec = (btime or arm_a_statx_btime)(path)
    if not 0 <= nsec < 1000000000: raise RuntimeError('invalid birth-time nanoseconds for ' + str(path))
    return f'linux-dev.{st.st_dev:x}-ino.{st.st_ino:x}-btime.{sec & 0xffffffffffffffff:x}.{nsec:x}'

def arm_a_bench_ids():
    import pwd
    row = pwd.getpwnam('bench'); return row.pw_uid, row.pw_gid

def arm_a_cell_dirs(attempt, arm, fixture, rep, tmpfs=None, uid=None, gid=None):
    """Per-cell writable roots on the helper's dedicated tmpfs (no other objects may exist there)."""
    tmpfs = pathlib.Path(tmpfs or ARM_A_TMPFS); cell = tmpfs / f'{attempt}-{arm}-{fixture}-r{rep}'
    if cell.exists(): raise RuntimeError('arm-a tmpfs cell dir already exists')
    cell.mkdir(mode=0o755); os.chmod(cell, 0o755); dirs = {}
    for rid in ARM_A_WRITABLE:
        d = cell / rid; d.mkdir(mode=0o700); os.chmod(d, 0o700)
        if uid is not None: os.chown(d, uid, gid, follow_symlinks=False)
        dirs[rid] = d
    return cell, dirs

def arm_a_memory_reservation(tmpfs, statvfs=None):
    """Mirror of the helper's storageBaseline (linux_native.go:733-760, linux_storage.go:17-30,61-72)."""
    tmpfs = pathlib.Path(tmpfs); st = (statvfs or os.statvfs)(str(tmpfs))
    data = (st.f_blocks - st.f_bfree) * st.f_bsize; objects = st.f_files - st.f_ffree
    reservation = ARM_A_SCAFFOLD_BYTES + data + objects * ARM_A_INODE_RESERVATION; entries = 0; stack = [tmpfs]
    while stack:
        current = stack.pop(); entries += 1
        if current.is_dir() and not current.is_symlink():
            stack.extend(sorted(current.iterdir()))
    extra = (entries - objects) * ARM_A_INODE_RESERVATION if entries > objects else 0
    return {'reservation_bytes': reservation + extra, 'data_bytes': data, 'objects': objects, 'entries': entries,
            'extra_entry_bytes': extra, 'block_size': st.f_bsize,
            'formula': '4MiB scaffold + used tmpfs bytes + 8192 per used inode (+8192 per inventoried entry above used inodes)'}

def arm_a_roots(fx_dir, writable, extra_read=()):
    rows = [{'root_id': 'fx-readonly', 'path': str(fx_dir), 'object_identity': arm_a_object_identity(fx_dir), 'mode': 'read'}]
    rows += [{'root_id': rid, 'path': str(path), 'object_identity': arm_a_object_identity(path), 'mode': 'read'} for rid, path in extra_read]
    rows += [{'root_id': rid, 'path': str(writable[rid]), 'object_identity': arm_a_object_identity(writable[rid]), 'mode': 'write'} for rid in ARM_A_WRITABLE]
    return rows

def arm_a_config(*, delegated, tmpfs, roots, profile, implemented_optional, run_id, uid, expires_at, protected, epoch=None):
    """Bootstrap QUALIFICATION config in the project's separate qualification programme's shape (generate_linux_config.py:614-631)."""
    if not isinstance(profile, dict) or profile.get('backend_id') != ARM_A_BACKEND_ID: raise RuntimeError('raw --linux-inspect tuple required')
    capabilities = list(ARM_A_MANDATORY_CAPABILITIES) + ([ARM_A_SEED_CAPABILITY] if ARM_A_SEED_CAPABILITY in (implemented_optional or ()) else [])
    epoch = epoch or {'build_id': str(uuid.uuid4()), 'attempt_id': str(uuid.uuid4()), 'epoch': 1}
    return {'delegated_cgroup': str(delegated), 'private_tmpfs': str(tmpfs), 'protected_roots': [str(p) for p in protected], 'roots': roots,
            'qualification': {'profile': {**profile, 'backend_id': ARM_A_QUAL_BACKEND_ID}, 'capabilities': capabilities,
                              'accounting': ARM_A_ACCOUNTING, 'expires_at': expires_at,
                              'harness': {'run_id': run_id, 'caller_id': 'qualification.' + run_id, 'delegated_uid': int(uid)}},
            'qualification_artifacts': {}, 'epochs': [epoch], 'admission_profile': 'QUALIFICATION'}

def arm_a_manifest(validate, cfg, *, command, argv, marker, reservation, now=None):
    roots = cfg['roots']; writable = {r['root_id']: r for r in roots if r['mode'] == 'write'}; epoch = cfg['epochs'][0]; now = time.time() if now is None else now
    pick = lambda r: {k: r[k] for k in ('root_id', 'path', 'object_identity')}
    m = {'version': '1.0', 'build_id': epoch['build_id'], 'attempt_id': epoch['attempt_id'], 'epoch': epoch['epoch'],
         'command_id': str(uuid.uuid4()), 'owner_id': str(uuid.uuid4()), 'purpose': 'tool', 'command': str(command), 'argv': [str(x) for x in argv],
         'cwd': writable['allowed']['path'], 'env_allowlist': {'PATH': '/usr/bin:/bin', 'HOME': writable['home']['path'], 'CMPMARK': marker},
         'readable_roots': [pick(r) for r in roots if r['mode'] == 'read'], 'writable_roots': [pick(r) for r in roots if r['mode'] == 'write'],
         'private_dirs': dict(ARM_A_PRIVATE_DIRS), 'network': {'mode': 'deny', 'endpoints': []},
         'resource_limits': {'memory_bytes': CAPS['memory.max'] + int(reservation), 'tasks': CAPS['pids.max'], **ARM_A_STORAGE},
         'timeouts': dict(ARM_A_TIMEOUTS), 'deadline': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now + 120)),
         'profile': {**cfg['qualification']['profile'], 'qualification_digest': validate.digest(cfg['qualification'])}}
    m['identity_hash'] = validate.manifest_digest(m); validate.validate_document('manifest', validate.canonical(m)); return m

def arm_a_payload(arm, marker, mode, args, fx_path, done_path):
    """Return (command, argv) for the helper. a: static fxa twin; a-bash: b's bash wrapper unchanged."""
    delay = str(done_path) if mode in RESOURCES and done_path else '30' if mode in SURVIVORS else '2' if mode in RESOURCES else 'run'
    if arm == 'a': return str(ARM_A_RO / 'fxa'), [marker, delay, fx_path, mode, *args]
    if arm == 'a-bash':
        payload = launcher_payload(marker, mode, args, mode in SURVIVORS or mode in RESOURCES, fx_path, done_path); return payload[0], payload[1:]
    raise ValueError('not an arm-a variant: ' + str(arm))

def arm_a_frame(validate, op, payload, manifest=None):
    frame = {'protocol_major': 1, 'protocol_minor': 0, 'request_id': str(uuid.uuid4()), 'operation': op, 'payload': payload, 'payload_digest': validate.digest(payload)}
    if manifest is not None:
        frame.update(build_id=manifest['build_id'], attempt_id=manifest['attempt_id'], epoch=manifest['epoch'], capability_digest=manifest['identity_hash'], deadline=manifest['deadline'])
    return frame

def arm_a_refusal(response):
    if not isinstance(response, dict): return {'code': 'no-response', 'message': 'no helper response'}
    if response.get('status') == 'rejected':
        err = (response.get('payload') or {}).get('error') or {}
        return {'code': response.get('code') or err.get('code'), 'message': err.get('message') or err.get('detail') or json.dumps(err, sort_keys=True)[:300]}
    return None

def arm_a_exit_code(result):
    term = (result or {}).get('termination') if isinstance(result, dict) else None
    if isinstance(term, dict) and isinstance(term.get('exit_code'), int) and not isinstance(term.get('exit_code'), bool): return term['exit_code'] & 0xff
    if isinstance(term, dict) and term.get('signal'):
        sig = getattr(signal, 'SIG' + str(term['signal']).upper().removeprefix('SIG'), None); return 128 + int(sig) if sig is not None else 70
    return 70

def arm_a_status(arm, scored, helper):
    """Arm-a status: a helper refusal is a recorded result; a-bash is never BLOCKED."""
    refusal = (helper or {}).get('refusal')
    if refusal: return f"REFUSED({refusal.get('code')}: {refusal.get('message')})"
    if arm == 'a-bash':
        if scored == 'BLOCKED': return 'INVALID(a-bash is evidence-only and is never scored BLOCKED)'
        result = (helper or {}).get('result') if isinstance((helper or {}).get('result'), dict) else {}
        start_failed = isinstance(result.get('termination'), dict) and result['termination'].get('cause') == 'start-failed'
        if scored != 'NOT-BLOCKED' and (helper or {}).get('marker_seen') is not True and start_failed:
            detail = {'result_status': result.get('status'), 'termination': result.get('termination'), 'error': (result.get('error') or {}).get('code') if isinstance(result.get('error'), dict) else result.get('error'), 'client_rc': (helper or {}).get('client_returncode')}
            return 'LAUNCH-FAILED(' + json.dumps(detail, sort_keys=True, separators=(',', ':')) + ')'
    return scored

class ArmAClient:
    def __init__(self, cmd, env, stderr, cwd):
        self.p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr, env=env, cwd=cwd); self.transcript = []
    def request(self, validate, op, payload, manifest=None, timeout=10):
        import selectors
        frame = arm_a_frame(validate, op, payload, manifest); self.p.stdin.write(validate.canonical(frame) + b'\n'); self.p.stdin.flush()
        sel = selectors.DefaultSelector(); sel.register(self.p.stdout, selectors.EVENT_READ)
        try: ready = sel.select(timeout)
        finally: sel.close()
        if not ready: raise RuntimeError('helper response timeout: ' + op)
        line = self.p.stdout.readline(validate.MAX_FRAME + 2)
        if not line.endswith(b'\n'): raise RuntimeError('control transport failed: ' + op)
        response = validate.strict_load(line[:-1]); self.transcript.append({'request': frame, 'response': response}); return response
    def close(self):
        try:
            if self.p.stdin and not self.p.stdin.closed: self.p.stdin.close()
        except OSError: pass
        try: self.p.wait(timeout=5)
        except subprocess.TimeoutExpired: self.p.kill(); self.p.wait()

def arm_a_client(spec_path):
    """Runs as bench inside the custody scope's runner leaf; owns one helper session."""
    spec = json.loads(pathlib.Path(spec_path).read_text()); out_path = pathlib.Path(spec['result_path']); record = {'label': ARM_A_LABEL, 'started_ns': time.time_ns()}
    def save():
        tmp = out_path.with_name(out_path.name + '.tmp'); tmp.write_text(json.dumps(record, sort_keys=True, indent=1) + '\n'); os.replace(tmp, out_path)
    client = None; rc = 70
    try:
        adapter = arm_a_load_pinned('adapter.py'); validate = arm_a_load_pinned('validate.py')
        os.environ['CORE04_QUALIFICATION_RUN_ID'] = spec['run_id']; os.environ['CORE04_QUALIFICATION_CALLER_ID'] = spec['caller_id']
        adapter.verify_backend_host(ARM_A_BACKEND)
        cmd = adapter.backend_command(spec['helper'], ARM_A_BACKEND, state_dir=spec['state_dir'], caller_id=spec['caller_id'], linux_config=spec['config'])
        record['helper_argv'] = cmd; child_env = {k: v for k, v in os.environ.items() if not k.startswith('CORE04_')}
        with open(spec['helper_stderr'], 'wb') as err:
            client = ArmAClient(cmd, child_env, err, spec['session_dir'])
            hello = client.request(validate, 'hello', {'supported_major': [1], 'supported_minor': [0]}); record['hello'] = hello
            if hello.get('status') != 'ok':
                record.update(refusal=arm_a_refusal(hello) or {'code': hello.get('code'), 'message': 'hello not ok'}, refusal_stage='hello'); return ARM_A_REFUSED_RC
            cfg = json.loads(pathlib.Path(spec['config']).read_text()); reservation = arm_a_memory_reservation(spec['tmpfs']); record['reservation'] = reservation
            manifest = arm_a_manifest(validate, cfg, command=spec['command'], argv=spec['argv'], marker=spec['marker'], reservation=reservation['reservation_bytes'])
            record['manifest'] = manifest; submit = client.request(validate, 'submit', {'manifest': manifest}, manifest); record['submit'] = submit; save()
            refusal = arm_a_refusal(submit)
            if refusal: record.update(refusal=refusal, refusal_stage='submit'); return ARM_A_REFUSED_RC
            handle = submit['payload']['handle']; query = None; transient = 0
            while True:
                query = client.request(validate, 'query', {'handle': handle}); payload = query.get('payload') or {}
                if query.get('status') == 'rejected' and query.get('code') == 'events-unavailable' and transient < 500:
                    transient += 1; record['transient_query_rejections'] = transient; time.sleep(0.02); continue
                if query.get('status') != 'ok' or payload.get('result') is not None or payload.get('state') == 'uncertain': break
                time.sleep(0.02)
            record['final_query'] = query; record['result'] = (query.get('payload') or {}).get('result'); rc = arm_a_exit_code(record['result']); return rc
    except BaseException as exc:
        record['client_error'] = repr(exc); return 71
    finally:
        if client is not None:
            client.close(); record['transcript_frames'] = len(client.transcript)
            try: pathlib.Path(spec['transcript_path']).write_text(json.dumps(client.transcript, sort_keys=True) + '\n')
            except OSError as exc: record['transcript_error'] = repr(exc)
        record['finished_ns'] = time.time_ns()
        try: save()
        except OSError: pass

def arm_a_delegate(cgroup_path, uid):
    """the project's separate qualification programme delegation shape inside the custody scope: root-owned runner leaf; delegated dir with cpu/memory/pids."""
    cg = pathlib.Path(cgroup_path); runner = cg / 'runner'; runner.mkdir(mode=0o755); moved = []
    for _ in range(5):
        pids = (cg / 'cgroup.procs').read_text().split()
        if not pids: break
        for pid in pids: (runner / 'cgroup.procs').write_text(pid); moved.append(int(pid))
    if (cg / 'cgroup.procs').read_text().split(): raise RuntimeError('custody scope still has internal processes')
    (cg / 'cgroup.subtree_control').write_text('+cpu +memory +pids'); enabled = sorted((cg / 'cgroup.subtree_control').read_text().split())
    if not {'cpu', 'memory', 'pids'} <= set(enabled): raise RuntimeError('cpu/memory/pids not enabled for delegated children')
    os.chown(cg, uid, -1, follow_symlinks=False)
    for name in ('cgroup.procs', 'cgroup.subtree_control'): os.chown(cg / name, uid, -1, follow_symlinks=False)
    return {'delegated_cgroup': str(cg), 'runner_leaf': str(runner), 'moved_pids': moved, 'subtree_control': enabled, 'owner_uid': uid}

def arm_a_inspect(tools, helper=None):
    outputs = {}
    for flag in ('--linux-inspect', '--linux-inspect-capabilities'):
        r = subprocess.run([str(tools['runuser']), '-u', 'bench', '--', str(helper or ARM_A_HELPER), flag], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, check=False, env={'PATH': '/usr/bin:/bin'}, cwd='/')
        if r.returncode: raise RuntimeError(f'helper {flag} failed rc={r.returncode}: ' + r.stderr.decode('utf-8', 'replace')[:300])
        outputs[flag] = json.loads(r.stdout)
    profile = outputs['--linux-inspect']; caps = outputs['--linux-inspect-capabilities']
    if not isinstance(caps, dict) or caps.get('profile') != profile: raise RuntimeError('capability inspection does not match --linux-inspect')
    return profile, list(caps.get('implemented_optional_capabilities') or [])

def arm_a_write_private(path, payload, uid, gid):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as f: f.write(payload)
    os.chown(path, uid, gid, follow_symlinks=False); os.chmod(path, 0o600)

def arm_a_setup_cell(state, cgroup_path, tools):
    """Root side, after custody acquisition and before the gate opens: delegation, inspect, per-cell config, client spec."""
    uid, gid = arm_a_bench_ids(); delegation = arm_a_delegate(cgroup_path, uid); profile, optional = arm_a_inspect(tools)
    extra = (('usr', pathlib.Path('/usr')),) if state['arm'] == 'a-bash' else ()
    roots = arm_a_roots(ARM_A_RO, state['writable'], extra)
    cfg = arm_a_config(delegated=cgroup_path, tmpfs=ARM_A_TMPFS, roots=roots, profile=profile, implemented_optional=optional, run_id=state['run_id'], uid=uid,
                       expires_at=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() + 7200)), protected=[ROOT])
    session = pathlib.Path(state['session_dir']); raw = json.dumps(cfg, sort_keys=True, separators=(',', ':')) + '\n'
    arm_a_write_private(session / 'config.json', raw, uid, gid)
    spec = {'helper': str(ARM_A_HELPER), 'state_dir': str(session / 'state'), 'config': str(session / 'config.json'), 'session_dir': str(session),
            'run_id': state['run_id'], 'caller_id': 'qualification.' + state['run_id'], 'tmpfs': str(ARM_A_TMPFS), 'marker': state['marker'],
            'command': state['command'], 'argv': state['argv'], 'result_path': str(session / 'client-result.json'),
            'transcript_path': str(session / 'transcript.json'), 'helper_stderr': str(session / 'helper.stderr')}
    arm_a_write_private(session / 'spec.json', json.dumps(spec, sort_keys=True) + '\n', uid, gid)
    return {'delegation': delegation, 'profile': profile, 'implemented_optional_capabilities': optional, 'config_sha256': hashlib.sha256(raw.encode()).hexdigest(),
            'config': cfg, 'spec': spec, 'helper_sha256': sha_file(ARM_A_HELPER)}

def arm_a_cgroup_snapshot(unit, custody, fx_row, expected, state):
    """R4 sampler: the helper-created candidate cgroup, located from a marked fx PID's verified /proc membership."""
    errors = []; locate = None
    if isinstance(expected, dict) and expected.get('cgroup_path'):
        cg = pathlib.Path(expected['cgroup_path']); identity = expected
    else:
        if not isinstance(fx_row, dict): return {'ok': False, 'path': None, 'files': {}, 'scope_identity': None, 'errors': ['no marked fx process to locate the candidate cgroup']}
        locate = observe_proc_cgroup(fx_row['pid'], fx_row.get('start')); rel = locate.get('cgroup_path')
        custody_path = pathlib.Path((custody or {}).get('cgroup_path') or '/nonexistent')
        if locate.get('verified_identity') is not True or not rel: errors.append('candidate cgroup membership not verified for the marked fx PID')
        cg = pathlib.Path('/sys/fs/cgroup' + rel) if rel else None
        scope_id = ((state or {}).get('submit_scope_id'))
        if cg is not None and cg.parent != custody_path: errors.append(f'candidate cgroup {cg} is not a child of the custody scope {custody_path}')
        if cg is not None and cg.name == 'runner': errors.append('marked fx PID is in the runner leaf, not a helper-created scope')
        if cg is not None and scope_id and cg.name != scope_id: errors.append(f'candidate cgroup {cg.name} differs from the helper-reported process_scope_id {scope_id}')
        if errors: return {'ok': False, 'path': str(cg) if cg else None, 'files': {}, 'scope_identity': None, 'locate': locate, 'errors': errors}
        identity = {'unit': unit, 'control_group': rel, 'cgroup_path': str(cg), 'scope_kind': 'helper-candidate-cgroup',
                    'custody_unit': (custody or {}).get('unit'), 'helper_process_scope_id': scope_id,
                    'located_from': {'pid': fx_row['pid'], 'start': fx_row.get('start'), 'verified_identity': True}}
    try: cg.stat()
    except OSError as exc: return {'ok': False, 'path': str(cg), 'files': {}, 'scope_identity': identity, 'locate': locate, 'errors': [f'candidate cgroup stat:{exc.errno}:{cg}']}
    files = {}
    for name in ARM_A_CGROUP_FILES:
        try: files[name] = pathlib.Path(cg / name).read_text().strip()
        except OSError as exc: errors.append(f'{cg / name}:{exc.errno}:{type(exc).__name__}')
    return {'ok': not errors, 'path': str(cg), 'files': files, 'scope_identity': identity, 'locate': locate, 'errors': errors}

def arm_a_peek_scope_id(state):
    try: client = json.loads((pathlib.Path(state['session_dir']) / 'client-result.json').read_text())
    except (OSError, ValueError, KeyError, TypeError): return None
    return ((client.get('submit') or {}).get('payload') or {}).get('process_scope_id')

def arm_a_observed_fx_path(state):
    """Host-visible path of the granted fx copy: the helper bootstrap chroots into <state>/scopes/<handle>/namespace-root
    and bind-mounts each root at its own path, so /proc/PID/exe reads <namespace-root>/var/lib/containment-fixture/ro/fx."""
    try: client = json.loads((pathlib.Path(state['session_dir']) / 'client-result.json').read_text())
    except (OSError, ValueError, KeyError, TypeError): return None
    handle = ((client.get('submit') or {}).get('payload') or {}).get('handle')
    if not isinstance(handle, str) or not re.fullmatch(r'[A-Za-z0-9._:-]{1,128}', handle): return None
    return str(pathlib.Path(state['session_dir']) / 'state' / 'scopes' / handle / 'namespace-root') + str(ARM_A_RO / 'fx')

def arm_a_launcher_argv(marker, session_dir, tools):
    """Unmetered custody scope (as z) with Delegate=yes so the helper can be given a qualification-style delegated subtree."""
    unit = scope_name(marker); gate_script = 'IFS= read -r gate && [ "$gate" = release ] || exit 125; exec "$@"'
    scope = [str(tools['systemd-run']), '--scope', '--expand-environment=no', '--unit=' + unit, '-p', 'Delegate=yes']
    client = [str(tools['runuser']), '-u', 'bench', '--', str(tools['python']), '-B', '-I', str(ROOT / 'cmp.py'), '_arm_a_client', str(pathlib.Path(session_dir) / 'spec.json')]
    return (scope + [str(tools['shell']), '-c', gate_script, 'cmp-gate', *client], unit)

class ArmAResourceWatcher(threading.Thread):
    """R4 sampler for arm-a resource cells. The helper terminates the whole candidate scope at its memory/task
    limit (result cause resource-limit), often before a full /proc marker scan can see it. This watcher polls only
    the custody scope's children: it locates the helper-created candidate cgroup through a member PID whose
    /proc identity carries this cell's CMPMARK/argv0 and whose /proc/PID/cgroup names that cgroup (verified
    before/after by start time), then reads the same cgroup files as b's sampler every few ms.
    Final sample: after a cgroup.events read shows populated 0, the counters are read and cgroup.events is read
    again in the same snapshot; both must show populated 0 and the cgroup directory identity must be unchanged.
    If the cgroup vanishes first, the failed final attempt is recorded and the cell is INVALID.
    Fail-closed observation:  every failed read is a retained observer error unless it is
    ENOENT/ESRCH and the shared scanner's disappearance policy proves it benign: verified_process_exit() finds the
    /proc entry gone, or a matching Z/X task passes verify_nonrunnable_group(); a vanished candidate cgroup must be
    confirmed absent by a directory stat. Unreadable custody listings and malformed cgroup.procs are always errors."""
    BENIGN_ERRNOS = (errno.ENOENT, errno.ESRCH)
    def __init__(self, unit, custody, marker, state, interval=0.002):
        super().__init__(daemon=True); self.unit = unit; self.custody = custody; self.marker = marker; self.state = state; self.interval = interval
        self.stop_event = threading.Event(); self.samples = []; self.identity = None; self.cg_object = None; self.final_captured = False
        self.fx_rows = []; self.locate_notes = []; self.errors = []; self.final_failures = []; self.cgroup_root = '/sys/fs/cgroup'
    def _error(self, text):
        if text not in self.errors and len(self.errors) < 200: self.errors.append(text)
    def _note(self, text):
        if text not in self.locate_notes and len(self.locate_notes) < 200: self.locate_notes.append(text)
    def _members(self, cgroup_dir):
        """Return member PIDs, or None when the cgroup is gone (directory stat confirms); other failures are errors."""
        try: raw = (pathlib.Path(cgroup_dir) / 'cgroup.procs').read_text()
        except OSError as exc:
            if exc.errno in self.BENIGN_ERRNOS:
                try: pathlib.Path(cgroup_dir).stat()
                except FileNotFoundError: self._note(f'membership-gone-verified:{cgroup_dir}'); return None
                except OSError as again: self._error(f'membership-recheck:{cgroup_dir}:{again.errno}'); return None
                self._error(f'membership-read:{cgroup_dir}:{exc.errno}:cgroup still present'); return None
            self._error(f'membership-read:{cgroup_dir}:{exc.errno}:{type(exc).__name__}'); return None
        pids = []
        for token in raw.split():
            if not token.isdigit(): self._error(f'malformed cgroup.procs:{cgroup_dir}:{token!r}'); continue
            pids.append(int(token))
        return pids
    def _disappeared(self, pid, start, error_errno, before, source, path):
        """Shared disappearance policy: benign only if verified gone or a proven nonrunnable Z/X; else retained."""
        if error_errno in self.BENIGN_ERRNOS:
            gone, verification = verified_process_exit({'pid':pid, 'start':start})
            if gone: self._note(f'{source}-verified-exit:{pid}:{error_errno}'); return True
            if verification.get('verification') == 'same-process-zombie' and isinstance(before, dict):
                proof = verify_nonrunnable_group({'pid':pid, 'start':start}, before, verification)
                if proof.get('ok'): self._note(f'{source}-proven-nonrunnable:{pid}'); return True
                self._error(f'{source}:{pid}:{path}:{error_errno}:zombie-proof:{proof.get("reason")}'); return False
            self._error(f'{source}:{pid}:{path}:{error_errno}:unverified:{verification.get("verification")}'); return False
        self._error(f'{source}:{pid}:{path}:{error_errno}'); return False
    def _identity_row(self, pid):
        before = proc_stat_observation(pid); first = before.get('stat')
        if first is None:
            if before.get('error_errno') in self.BENIGN_ERRNOS: self._note(f'process-stat-gone:{pid}:{before.get("error_errno")}'); return None
            self._error(f'process-stat:{pid}:{before.get("error_path")}:{before.get("error_errno")}:{before.get("error")}'); return None
        try: row = read_proc_identity(pid)
        except OSError as exc:
            self._disappeared(pid, first.get('start'), exc.errno, before, 'process-read', getattr(exc, 'proc_path', None) or proc_error_path(exc)); return None
        except (ValueError, IndexError) as exc:
            self._error(f'malformed-identity:{pid}:{type(exc).__name__}:{exc}'); return None
        if row.get('start') != first.get('start'): self._note(f'identity-changed:{pid}'); return None
        row['_before'] = before; return row
    def _locate(self):
        custody = pathlib.Path(self.custody['cgroup_path']); fx_path = arm_a_observed_fx_path(self.state)
        try: children = [entry for entry in os.scandir(custody) if entry.is_dir(follow_symlinks=False) and entry.name != 'runner']
        except OSError as exc: self._error(f'custody-children:{custody}:{exc.errno}:{type(exc).__name__}'); return
        for entry in children:
            child = pathlib.Path(entry.path); pids = self._members(child)
            for pid in pids or ():
                row = self._identity_row(pid)
                if row is None or row['env'].get('CMPMARK') != self.marker or row['argv0'] != self.marker: continue
                seen = observe_proc_cgroup(row['pid'], row.get('start')); rel = seen.get('cgroup_path'); membership = seen.get('membership') or {}
                failed = False
                for label, obs in (('identity-before', seen.get('before') or {}), ('identity-after', seen.get('after') or {})):
                    if obs.get('stat') is None:
                        failed = True; self._disappeared(pid, row.get('start'), obs.get('error_errno'), row.get('_before'), label, obs.get('error_path'))
                if membership.get('read_error'):
                    failed = True; self._disappeared(pid, row.get('start'), membership.get('error_errno'), row.get('_before'), 'cgroup-membership', membership.get('error_path'))
                if failed: continue
                if seen.get('verified_identity') is not True or not rel or pathlib.Path(self.cgroup_root + rel) != child:
                    self._note(f'locate-unverified:{pid}'); continue
                try: st = child.stat(); self.cg_object = (st.st_dev, st.st_ino)
                except OSError as exc: self._error(f'candidate-cgroup-stat:{child}:{exc.errno}'); return
                self.identity = {'unit': self.unit, 'control_group': rel, 'cgroup_path': str(child), 'scope_kind': 'helper-candidate-cgroup',
                                 'custody_unit': self.custody.get('unit'), 'cgroup_object': f'dev.{st.st_dev:x}-ino.{st.st_ino:x}',
                                 'located_from': {'pid': row['pid'], 'start': row.get('start'), 'exe': row['exe'], 'verified_identity': True, 'via': 'custody-child-cgroup.procs'}}
                if fx_path and row['exe'] == fx_path: self.fx_rows.append({k: row.get(k) for k in ('pid', 'start', 'ppid', 'sid', 'exe', 'argv0')})
                return
    def _fail_final(self, why):
        self.samples.append({'ok': False, 'final': True, 'final_attempt': True, 'path': (self.identity or {}).get('cgroup_path'), 'files': {}, 'errors': [why]})
        self.final_failures.append(why); return True
    def _same_object(self):
        try: st = pathlib.Path(self.identity['cgroup_path']).stat()
        except OSError: return False
        return (st.st_dev, st.st_ino) == self.cg_object
    def _sample(self):
        cg = pathlib.Path(self.identity['cgroup_path']); fx_path = arm_a_observed_fx_path(self.state)
        if fx_path and not self.fx_rows:
            for pid in self._members(cg) or ():
                row = self._identity_row(pid)
                if row is not None and row['exe'] == fx_path and row['env'].get('CMPMARK') == self.marker and row['argv0'] == self.marker:
                    self.fx_rows.append({k: row.get(k) for k in ('pid', 'start', 'ppid', 'sid', 'exe', 'argv0')}); break
        try: first = parse_text_kv((cg / 'cgroup.events').read_text())
        except OSError as exc: return self._fail_final(f'candidate cgroup unreadable before a populated=0 final read: {exc.errno}')
        snap = arm_a_cgroup_snapshot(self.unit, self.custody, None, self.identity, self.state)
        if not snap.get('ok'): return self._fail_final('candidate cgroup became unreadable before a complete populated=0 final read')
        if first.get('populated') == 0:
            again = parse_text_kv(snap['files'].get('cgroup.events', ''))
            if again.get('populated') != 0: self.samples.append(snap); return False
            if not self._same_object(): return self._fail_final('candidate cgroup object changed before the final read')
            snap['final'] = True; snap['final_reason'] = 'counters read between two cgroup.events populated 0 reads; same cgroup object'
            snap['barrier_observed_ns'] = time.time_ns(); self.samples.append(snap); self.final_captured = True; return True
        self.samples.append(snap); return False
    def run(self):
        try:
            while not self.stop_event.is_set():
                if self.identity is None: self._locate()
                elif self._sample(): return
                time.sleep(self.interval)
        except BaseException as exc: self._error('watcher:' + repr(exc))
    def stop(self): self.stop_event.set(); self.join(timeout=5)

def arm_a_watcher_observer_errors(watcher):
    """Every retained watcher error becomes a cell observer error (observer_ok false, so the cell scores INVALID)."""
    return ['arm-a-watcher:' + x for x in (watcher.errors if watcher is not None else [])]

def arm_a_read_session(state):
    """Root reads the client's record and the helper's recorded reservation (state/.../linux.json)."""
    out = {'label': ARM_A_LABEL, 'run_id': state.get('run_id'), 'session_dir': state.get('session_dir')}
    session = pathlib.Path(state['session_dir']) if state.get('session_dir') else None
    if session is None: return out
    try: out['client'] = json.loads((session / 'client-result.json').read_text())
    except (OSError, ValueError) as exc: out['client_read_error'] = repr(exc)
    recorded = []
    try:
        for p in sorted((session / 'state').rglob('linux.json')):
            try:
                doc = json.loads(p.read_text()); recorded.append({'path': str(p), 'memory_reservation_bytes': doc.get('memory_reservation_bytes'), 'cgroup_path': doc.get('cgroup_path')})
            except (OSError, ValueError) as exc: recorded.append({'path': str(p), 'error': repr(exc)})
    except OSError as exc: out['state_read_error'] = repr(exc)
    out['helper_recorded'] = recorded; client = out.get('client') or {}
    retained = {}; budget = 1 << 20
    try:
        for f in sorted(p for p in session.rglob('*') if p.is_file() and not p.is_symlink() and p.name != 'config.json'):
            if budget <= 0: retained[str(f)] = 'omitted: evidence budget exhausted'; continue
            raw = f.read_bytes()[:131072]; budget -= len(raw); retained[str(f)] = raw.decode('utf-8', 'replace')
    except OSError as exc: retained['error'] = repr(exc)
    out['session_files'] = retained
    out['refusal'] = client.get('refusal'); out['result'] = client.get('result'); out['reservation'] = client.get('reservation')
    sub = (client.get('submit') or {}).get('payload') or {}; out['submit_scope_id'] = sub.get('process_scope_id'); out['handle'] = sub.get('handle')
    computed = (client.get('reservation') or {}).get('reservation_bytes'); helper_values = [r.get('memory_reservation_bytes') for r in recorded if 'memory_reservation_bytes' in r]
    out['reservation_matches_helper'] = bool(helper_values) and all(v == computed for v in helper_values)
    return out

def arm_a_install_binaries(root=None, ro=None):
    """Copy the shared fx and the static fxa into the read-only grant; byte-identity is checked and recorded."""
    root = pathlib.Path(root or ROOT); ro = pathlib.Path(ro or ARM_A_RO); rec = {}
    st = ro.lstat()
    if not stat.S_ISDIR(st.st_mode) or st.st_uid != 0 or stat.S_IMODE(st.st_mode) & 0o022: raise RuntimeError('arm-a read-only grant dir must be a root-owned non-writable directory')
    for name in ('fx', 'fxa'):
        src = root / name; dst = ro / name; tmp = ro / ('.' + name + '.new')
        shutil.copyfile(src, tmp); os.chmod(tmp, 0o755); os.replace(tmp, dst)
        rec[name] = {'source': str(src), 'path': str(dst), 'source_sha256': sha_file(src), 'sha256': sha_file(dst)}
        if rec[name]['source_sha256'] != rec[name]['sha256']: raise RuntimeError('arm-a copy is not byte-identical: ' + name)
    rec['fx_identical_to_shared_fx'] = rec['fx']['sha256'] == sha_file(root / 'fx'); return rec

def arm_a_preflight():
    """Host prerequisites set up as the project's separate qualification programme does; refuse to run arm a without them."""
    errors = []; rec = {}
    try:
        rec['helper_sha256'] = sha_file(ARM_A_HELPER)
        if rec['helper_sha256'] != ARM_A_HELPER_SHA256: errors.append('helper sha256 differs from the pinned impl/bin .sha256')
        st = ARM_A_HELPER.stat(); rec['helper_mode'] = f'{st.st_uid}:{st.st_gid}:{stat.S_IMODE(st.st_mode):04o}'
    except OSError as exc: errors.append('helper:' + repr(exc))
    for name in ARM_A_PINS:
        try:
            if sha_file(ARM_A_VENDOR / name) != ARM_A_PINS[name]: errors.append('vendored pin mismatch: ' + name)
        except OSError as exc: errors.append('vendor:' + name + ':' + repr(exc))
    try:
        mounts = [line.split() for line in pathlib.Path('/proc/self/mountinfo').read_text().splitlines()]
        tm = [m for m in mounts if len(m) > 4 and m[4] == str(ARM_A_TMPFS)]; rec['tmpfs_mount'] = [' '.join(m) for m in tm]
        if len(tm) != 1 or ' - tmpfs ' not in ' '.join(tm[0]): errors.append('dedicated tmpfs is not mounted exactly once at ' + str(ARM_A_TMPFS))
        leftovers = sorted(p.name for p in ARM_A_TMPFS.iterdir()); rec['tmpfs_entries'] = leftovers
        if leftovers: errors.append('dedicated tmpfs is not empty: ' + ','.join(leftovers[:5]))
    except OSError as exc: errors.append('tmpfs:' + repr(exc))
    try: rec['apparmor_userns_sysctl'] = pathlib.Path('/proc/sys/kernel/apparmor_restrict_unprivileged_userns').read_text().strip()
    except OSError as exc: rec['apparmor_userns_sysctl'] = repr(exc)
    rec['apparmor_profile'] = '/etc/apparmor.d/cmp-arm-a-contain'; rec['apparmor_profile_present'] = pathlib.Path(rec['apparmor_profile']).is_file()
    if not rec['apparmor_profile_present']: errors.append('AppArmor userns profile for the helper path is absent')
    rec['errors'] = errors; rec['pass'] = not errors; return rec

def prepare_dirs(runid, arm, fixture, rep, attempt):
    if not BASE.resolve().is_relative_to(ROOT):
        raise RuntimeError('CMP_BASE must remain inside the fresh deployment directory')
    root = BASE / runid / attempt / f'{arm}-{fixture}-r{rep}';
    if root.exists(): raise RuntimeError('attempt work tree already exists; refusing O_EXCL reuse')
    allowed = root / 'allowed'; allowed.mkdir(parents=True); os.chmod(BASE, 493); os.chmod(BASE / runid, 493); os.chmod(BASE / runid / attempt, 493); os.chmod(root, 493); os.chmod(allowed, 511); return (root, allowed)

def launcher_payload(marker, mode, args, hold, fx_path, done_path=None):
    shell='/usr/bin/bash'; script='if [ "$3" = mem_cap ] || [ "$3" = pids_cap ]; then (CMPMARK="$0-holder" exec -a "$0-holder" /usr/bin/sleep 120) & holder=$!; (exec -a "$0" "$2" "$3" "${@:4}") & worker=$!; wait "$worker"; rc=$?; : > "$1"; wait "$holder"; exit "$rc"; elif [ "$1" != run ]; then (exec -a "$0" "$2" "$3" "${@:4}"); rc=$?; sleep "$1"; exit "$rc"; else exec -a "$0" "$2" "$3" "${@:4}"; fi'; bridge='exec -a "$1" /usr/bin/bash -c "$2" "$1" "${@:3}"'; delay=str(done_path) if mode in RESOURCES and done_path else '30' if mode in SURVIVORS else '2' if mode in RESOURCES else 'run'; return [shell,'-c',bridge,'cmp-bridge',marker,script,delay,fx_path,mode,*args]

def launcher_argv(arm, marker, mode, args, allowed, tools, scope_gate=False):
    hold = mode in SURVIVORS or mode in RESOURCES; build = str(ROOT / 'fx'); fx_path = build; done_path = str(pathlib.Path(allowed) / 'pressure.done') if mode in RESOURCES else None; payload = launcher_payload(marker, mode, args, hold, fx_path, done_path); runuser = str(tools['runuser'])
    if arm == 'z':
        unit = scope_name(marker); gated = payload
        if scope_gate:
            gate_script='IFS= read -r gate && [ "$gate" = release ] || exit 125; exec "$@"'
            gated=[str(tools['shell']),'-c',gate_script,'cmp-gate',*payload]
        scope=[str(tools['systemd-run']),'--scope','--expand-environment=no','--unit='+unit]
        return (scope + [str(tools['setsid']),runuser,'--preserve-environment','-u','bench','--',*gated], unit)
    unit = scope_name(marker); scope = [str(tools['systemd-run']), '--scope', '--expand-environment=no', '--unit=' + unit, '-p', 'Delegate=yes', '-p', 'MemoryMax=256M', '-p', 'TasksMax=64', '-p', 'CPUQuota=100%']
    if arm == 'b':
        bwrap = [str(tools['bwrap']), '--unshare-pid', '--unshare-net', '--die-with-parent', '--clearenv']
        for d in dict.fromkeys(path_parents(allowed)): bwrap += ['--dir', d]
        bwrap += ['--symlink', 'usr/bin', '/bin', '--ro-bind', '/usr', '/usr', '--ro-bind', '/lib', '/lib', '--ro-bind', '/lib64', '/lib64', '--ro-bind', build, build, '--bind', str(allowed), str(allowed), '--proc', '/proc', '--dev', '/dev', '--chdir', str(allowed), '--setenv', 'PATH', '/usr/bin:/bin', '--setenv', 'HOME', BENCH_HOME, '--setenv', 'CMPMARK', marker, '--', *payload]; return (scope + [runuser, '-u', 'bench', '--', *bwrap], unit)
    if arm == 'c2':
        nono = str(tools['nono']); env = ['/usr/bin/env', '-i', 'PATH=/usr/bin:/bin', 'HOME=' + BENCH_HOME, 'CMPMARK=' + marker]; cmd = [runuser, '-u', 'bench', '--', *env, nono, 'run', '--read', '/usr', '--read', '/lib', '--read', '/lib64', '--read-file', build, '--allow', str(allowed), '--workdir', str(allowed), '--allow-cwd', '--block-net', '--', *payload]; return (scope + cmd, unit)
    if arm == 'a': return (None, None)
    raise ValueError('unknown arm ' + arm)

def path_parents(path):
    parts = pathlib.Path(path).parts; (accum, result) = ('', [])
    for part in parts[:-1]:
        accum = str(pathlib.Path(accum) / part)
        if accum not in ('/', '.'): result.append(accum)
    return result

def runner_row(arm, marker, rows, scope, tools):
    if arm in ARM_A_VARIANTS:
        # The arm-a runner is the helper-session client in the custody scope's runner leaf (unmarked apparatus).
        wanted = os.path.realpath(tools['python']); cg = cg_path(scope, tools) if scope else None; candidates = []
        if cg is not None:
            try: members = (cg / 'runner' / 'cgroup.procs').read_text().split()
            except OSError: members = []
            for pid_text in members:
                try:
                    row = read_proc_identity(int(pid_text))
                    if row['exe'] == wanted: candidates.append(row)
                except (OSError, ValueError, IndexError):
                    continue
        return candidates[0] if len(candidates) == 1 else None
    if arm == 'z':
        candidates = [r for r in rows if r['exe'].endswith('/bash') and r['env'].get('CMPMARK') == marker and r['argv0'] == marker]; return candidates[0] if candidates else None
    if arm == 'b':
        wanted = os.path.realpath(tools['bwrap'])
    else:
        wanted = os.path.realpath(tools['nono'])
    cg = cg_path(scope, tools) if scope else None
    if cg and cg.exists():
        try:
            for pid_text in (cg / 'cgroup.procs').read_text().split():
                try:
                    row = read_proc_identity(int(pid_text))
                    if row['exe'] == wanted: return row
                except (OSError, ValueError, IndexError):
                    continue
        except OSError:
            pass
    return None

def collect_outputs(tokens, allowed_path, write_path, canary):
    errors = []; marker = tokens.get('marker')
    if not isinstance(marker, str) or not marker:
        errors.append('listener-observe:missing marker')
    try:
        write_seen = pathlib.Path(write_path).read_text() == tokens['write']
    except FileNotFoundError:
        write_seen = False
    except OSError as exc:
        write_seen = False; errors.append('write-observe:' + repr(exc))
    try:
        allowed_seen = pathlib.Path(allowed_path).read_text() == tokens['allowed']
    except FileNotFoundError:
        allowed_seen = False
    except OSError as exc:
        allowed_seen = False; errors.append('allowed-observe:' + repr(exc))
    accepts = list(canary.rows); peer = bool(marker) and any((r.get('peer_marker') == marker and r.get('peer_argv0') == marker for r in accepts)); return {'errors': errors, 'write_token_seen': write_seen, 'allowed_token_seen': allowed_seen, 'write_observation_complete': not any(x.startswith('write-observe:') for x in errors), 'allowed_observation_complete': not any(x.startswith('allowed-observe:') for x in errors), 'listener_accept': bool(accepts), 'listener_peer_marked': peer, 'listener_rows': accepts, 'listener_healthy': canary.healthy, 'listener_coverage_complete': canary.healthy}

def captured_output(path, limit=32768):
    try:
        with pathlib.Path(path).open('rb') as stream:
            data = stream.read(limit + 1)
    except OSError as exc:
        return {'text': '', 'truncated': False, 'error': repr(exc)}
    return {'text': data[:limit].decode('utf-8', 'replace'), 'truncated': len(data) > limit}

def saved_cell(outdir, arm, fixture, rep):
    key = cell_key(arm, fixture, rep); path = outdir / 'evidence' / arm / fixture / f'rep-{rep}.json'; events = [x for x in ledger_state(outdir / LEDGER_NAME) if x.get('event') == 'complete' and x.get('key') == key]
    if not events: return None
    event = events[-1]
    if not path.is_file() or event.get('evidence') != str(path) or event.get('evidence_sha256') != sha_file(path): raise RuntimeError('completed cell evidence missing or changed: ' + key)
    try: e = json.loads(path.read_text())
    except (OSError, ValueError) as exc: raise RuntimeError('completed cell evidence unreadable: ' + key) from exc
    if e.get('arm') != arm or e.get('fixture') != fixture or str(e.get('rep')) != str(rep) or e.get('status') != event.get('status') or expected_cell_status(arm, fixture, e) != e.get('status'):
        raise RuntimeError('completed cell evidence does not validate: ' + key)
    return e

def expected_cell_status(arm, fixture, evidence):
    """Re-derive a stored status from stored evidence: score() for every arm; for arm-a variants the raw score must
    also equal the stored scored_status and the helper refusal / a-bash mapping is re-applied ."""
    scored = score(fixture, evidence)
    if arm not in ARM_A_VARIANTS or evidence.get('arm_broken') is True: return scored
    if evidence.get('scored_status') != scored: return 'INVALID(stored scored_status differs from score)'
    return arm_a_status(arm, scored, evidence.get('arm_a'))

def ensure_free_space():
    free = shutil.disk_usage(ROOT).free
    if free <= 15 * 1024 ** 3: raise RuntimeError(f'free space gate failed: {free} bytes (need > 15 GiB)')
    return free

def host_stat_check():
    root_home = pathlib.Path.home()
    bench_home = pathlib.Path(BENCH_HOME).parent
    system_home = bench_home.parent
    paths = ['/', str(root_home), str(system_home), str(bench_home)]
    cmd = ['stat', '-c', '%U:%G %a %n', *paths]
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    expected = ['root:root 755 /', f'root:root 700 {root_home}', f'root:root 755 {system_home}', f'bench:bench 750 {bench_home}']
    return {'pass': r.returncode == 0 and r.stdout.splitlines() == expected, 'lines': r.stdout.splitlines(), 'stderr': r.stderr.strip(), 'expected': expected}

def run_cell(arm, fixture, rep, run_id):
    """Shared, fail-closed executor for qualification, dry runs, and measurement."""
    if arm not in ARMS + ('a-bash',) or fixture not in ALL_FIXTURES: raise ValueError('unsupported arm or fixture')
    if arm == 'a-bash' and fixture != 'allowed_rw': raise ValueError('a-bash is evidence-only on allowed_rw')
    outdir = OUT / run_id; outdir.mkdir(parents=True, exist_ok=True); os.chmod(outdir,0o755); ledger = outdir / LEDGER_NAME; key = cell_key(arm, fixture, rep); evidence_path = outdir / 'evidence' / arm / fixture / f'rep-{rep}.json'
    positive=saved_cell(outdir,arm,'allowed_rw',rep) if fixture not in ('allowed_rw','noop') else None
    if fixture not in ('allowed_rw','noop') and positive is None: raise RuntimeError('same-arm/repetition allowed_rw control is required before '+key)
    old=saved_cell(outdir,arm,fixture,rep)
    if old is not None:
        if positive is not None and positive.get('status')!='NOT-BLOCKED' and old.get('arm_broken'): return old
        if positive is not None and positive.get('status')!='NOT-BLOCKED': raise RuntimeError('completed cell lacks successful positive control: '+key)
        return old
    if positive is not None:
        if positive.get('status') != 'NOT-BLOCKED':
            e = {'arm':arm,'fixture':fixture,'rep':rep,'marker':f'{run_id}-{fixture}-{arm}-r{rep}-arm-broken','arm_broken':True,'status':'INVALID(arm-broken)','reason':'allowed_rw failed'}
            evidence_path.parent.mkdir(parents=True, exist_ok=True); evidence_path.write_text(json.dumps(e, sort_keys=True, indent=2)+'\n'); append_jsonl(ledger, {'event':'complete','key':key,'status':e['status'],'evidence':str(evidence_path),'evidence_sha256':sha_file(evidence_path)}); return e
    free_before = ensure_free_space(); attempt = uuid.uuid4().hex[:10]; marker = f'{run_id}-{fixture}-{arm}-r{rep}-a{attempt}'; unit = scope_name(marker) if arm in ('z','b','c2')+ARM_A_VARIANTS and not (fixture in RESOURCES and arm == 'z') else None
    root, allowed = prepare_dirs(run_id, arm, fixture, rep, attempt); arm_a_state = {}
    if arm in ARM_A_VARIANTS:
        a_uid, a_gid = arm_a_bench_ids(); a_cell, a_dirs = arm_a_cell_dirs(attempt, arm, fixture, rep, uid=a_uid, gid=a_gid); allowed = a_dirs['allowed']; a_session = root / 'a-helper'; a_session.mkdir(mode=0o700); os.chown(a_session, a_uid, a_gid)
        arm_a_state = {'arm': arm, 'run_id': 'cmp-' + run_id, 'marker': marker, 'tmpfs_cell': str(a_cell), 'writable': a_dirs, 'session_dir': str(a_session)}
    outside_read=root/'outside-read'; outside_target=root/'outside-write'; secret_file=root/'secret-file'; allowed_path=allowed/'allowed-rw'; allowed_input=allowed/'allowed-input'
    scope_gate=(arm == 'z' and fixture not in RESOURCES) or arm in ARM_A_VARIANTS
    tokens={'read':'READ_'+secrets.token_hex(24),'write':'WRITE_'+secrets.token_hex(24),'secret_file':'FILESECRET_'+secrets.token_hex(24),'secret_env':'ENVSECRET_'+secrets.token_hex(24),'allowed':'ALLOW_'+secrets.token_hex(24),'net':'NET_'+secrets.token_hex(24)}
    try:
        outside_read.write_text(tokens['read']); secret_file.write_text(tokens['secret_file']); allowed_input.write_text(tokens['allowed']); os.chmod(allowed_input,0o444); os.chmod(outside_read,0o644); os.chmod(secret_file,0o644); os.chmod(root,0o777)
    except BaseException:
        shutil.rmtree(root,ignore_errors=True); raise
    begin={'event':'begin','key':key,'attempt':attempt,'marker':marker,'unit':unit,'workdir':str(allowed),'rootdir':str(root),'free_bytes_before':free_before,'wall_time_ns':time.time_ns()}
    if arm in ARM_A_VARIANTS: begin['arm_a_tmpfs_dir']=arm_a_state['tmpfs_cell']
    append_jsonl(ledger, begin)
    tools=resolve_tools(); canary=None; popen=None; stdout_file=stderr_file=None; stdout_fd=stderr_fd=None; cgs=[]; observer_errors=[]; observer_notes=[]; proc_diagnostics=[]; memory_observations=[]; survivor_rows=[]; protocol={'stable_pre_kill':False,'runner_sigkill_delivered':False,'post_scan_complete':False,'pre_rows':[],'post_rows':[]}; term_delivery=False; term_live=False; fixture_seen=False; read_seen=secret_seen=env_seen=allowed_read_seen=False; read_cov=secret_cov=env_cov=fixture not in ('file_read_outside','secret_file_read','env_secret','allowed_rw'); read_incomplete=secret_incomplete=False; timed_out=False; launch_error=None; returncode=None; completion_ns=None; useful_start=None; teardown_start=None; output_data={}; cleanup={}; cmd=[]; resource=(fixture in RESOURCES and arm in ('b','c2','a')); a_resource_identity=None; a_watcher=None; resource_evidence={}; scope_identity=None; custody_gate_released=not scope_gate; resource_final_captured=False; holder_release={}; wait_context=None; pressure_done=allowed/'pressure.done' if resource else None; stdout_path=evidence_path.with_name(evidence_path.stem+'.stdout.log'); stderr_path=evidence_path.with_name(evidence_path.stem+'.stderr.log')
    try:
        canary=Canary(); args=[]
        if fixture=='file_read_outside': args=[str(outside_read)]
        elif fixture=='file_write_outside': args=[str(outside_target),tokens['write']]
        elif fixture=='secret_file_read': args=[str(secret_file)]
        elif fixture=='net_loopback': args=[str(canary.port),tokens['net']]
        elif fixture=='allowed_rw': args=[str(allowed_path),str(allowed_input)]
        if fixture in RESOURCES and arm=='z': launch_error='UNSUPPORTED(no mechanism)'
        else:
            if arm in ARM_A_VARIANTS:
                arm_a_state['command'],arm_a_state['argv']=arm_a_payload(arm,marker,fixture,args,str(ARM_A_RO/'fx'),str(allowed/'pressure.done') if fixture in RESOURCES else None)
                cmd,unit=arm_a_launcher_argv(marker,arm_a_state['session_dir'],tools)
            else: cmd,unit=launcher_argv(arm,marker,fixture,args,allowed,tools,scope_gate)
            evidence_path.parent.mkdir(parents=True,exist_ok=True)
            stdout_fd=os.open(stdout_path,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600); stdout_file=os.fdopen(stdout_fd,'wb'); stdout_fd=None; stderr_fd=os.open(stderr_path,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600); stderr_file=os.fdopen(stderr_fd,'wb'); stderr_fd=None
            env={'PATH':'/usr/bin:/bin','HOME':BENCH_HOME,'CMPMARK':marker,'CMPSECRET':tokens['secret_env']}
            if arm in ARM_A_VARIANTS: env.pop('CMPMARK')  # the helper apparatus stays unmarked; the candidate gets CMPMARK only through its manifest env
            useful_start=time.monotonic_ns(); popen=subprocess.Popen(cmd,cwd=str(allowed),env=env,stdin=subprocess.PIPE if scope_gate else None,stdout=stdout_file,stderr=stderr_file,start_new_session=False)
            popen_pid=getattr(popen,'pid',None)
            wait_identity=proc_stat_observation(popen_pid) if isinstance(popen_pid,int) else None
            wait_context={'pid':popen_pid,'start_time':(wait_identity.get('stat') or {}).get('start') if wait_identity else None,
                'identity_snapshot':safe_proc_stat_observation(wait_identity) if wait_identity else None,'spawned_ns':time.time_ns(),
                'returncode':None,'wait_observed_monotonic_ns':None}
            done=threading.Event(); waited={}
            def waiter():
                try: waited['rc']=popen.wait()
                finally:
                    waited['at']=time.monotonic_ns(); wait_context.update({'returncode':waited.get('rc'),
                        'wait_observed_monotonic_ns':waited['at']}); done.set()
            threading.Thread(target=waiter,daemon=True).start(); fxpath=None if arm in ARM_A_VARIANTS else os.path.realpath(pathlib.Path(__file__).with_name('fx')); stable=0; last_identity=None; stable_samples=[]
            if arm == 'z':
                custody_deadline=time.monotonic()+5
                while time.monotonic()<custody_deadline:
                    lookup=scope_lookup(unit,tools)
                    if lookup.get('state') == 'present' and lookup.get('path'):
                        scope_identity={'unit':unit,'control_group':lookup.get('control_group'),'cgroup_path':lookup['path'],
                                        'scope_kind':'bookkeeping','resource_limits':False}
                        append_jsonl(ledger,{'event':'scope_acquired','key':key,'marker':marker,'unit':unit,'scope_identity':scope_identity,
                                             'wall_time_ns':time.time_ns(),'before_payload':True})
                        try:
                            if popen.stdin is None: raise RuntimeError('scope gate pipe unavailable')
                            popen.stdin.write(b'release\n'); popen.stdin.flush(); popen.stdin.close(); custody_gate_released=True
                        except (OSError,ValueError,RuntimeError) as exc:
                            observer_errors.append('custody-gate-release:'+repr(exc)); launch_error='z scope gate release failed'
                        break
                    if lookup.get('state') == 'error':
                        observer_errors.extend('custody-scope:'+x for x in lookup.get('errors',['scope lookup failed'])); break
                    if done.is_set(): break
                    time.sleep(0.01)
                if not custody_gate_released and launch_error is None:
                    launch_error='z bookkeeping scope identity was not acquired before payload gate'; observer_errors.append(launch_error)
            if arm in ARM_A_VARIANTS:
                custody_deadline=time.monotonic()+5
                while time.monotonic()<custody_deadline:
                    lookup=scope_lookup(unit,tools)
                    if lookup.get('state') == 'present' and lookup.get('path'):
                        scope_identity={'unit':unit,'control_group':lookup.get('control_group'),'cgroup_path':lookup['path'],
                                        'scope_kind':'bookkeeping','resource_limits':False}
                        append_jsonl(ledger,{'event':'scope_acquired','key':key,'marker':marker,'unit':unit,'scope_identity':scope_identity,
                                             'wall_time_ns':time.time_ns(),'before_payload':True})
                        try:
                            arm_a_state['setup']=arm_a_setup_cell(arm_a_state,lookup['path'],tools)
                            append_jsonl(ledger,{'event':'arm_a_setup','key':key,'marker':marker,'delegation':arm_a_state['setup']['delegation'],
                                                 'config_sha256':arm_a_state['setup']['config_sha256'],'helper_sha256':arm_a_state['setup']['helper_sha256'],'wall_time_ns':time.time_ns()})
                            if popen.stdin is None: raise RuntimeError('scope gate pipe unavailable')
                            popen.stdin.write(b'release\n'); popen.stdin.flush(); popen.stdin.close(); custody_gate_released=True
                            if resource and arm=='a': a_watcher=ArmAResourceWatcher(unit,scope_identity,marker,arm_a_state); a_watcher.start()
                        except (OSError,ValueError,RuntimeError,subprocess.SubprocessError) as exc:
                            observer_errors.append('arm-a-setup:'+repr(exc)); launch_error='arm-a custody/admission setup failed: '+repr(exc)
                        break
                    if lookup.get('state') == 'error':
                        observer_errors.extend('custody-scope:'+x for x in lookup.get('errors',['scope lookup failed'])); break
                    if done.is_set(): break
                    time.sleep(0.01)
                if not custody_gate_released and launch_error is None:
                    launch_error='arm-a custody scope identity was not acquired before payload gate'; observer_errors.append(launch_error)
            deadline=time.monotonic()+(40 if resource else 15)
            while time.monotonic()<deadline:
                if arm in ('z',)+ARM_A_VARIANTS and not custody_gate_released: break
                defer_positive_scope_sample = arm == 'c2' and fixture == 'allowed_rw'
                if (not defer_positive_scope_sample and unit and arm in ('b','c2') and
                        not (resource and resource_final_captured)):
                    snap=cgroup_snapshot(unit,tools,scope_identity)
                    if snap.get('ok') and scope_identity is None:
                        scope_identity=snap.get('scope_identity'); append_jsonl(ledger,{'event':'scope_acquired','key':key,'marker':marker,'unit':unit,'scope_identity':scope_identity,'wall_time_ns':time.time_ns()})
                    cgs.append(snap)
                if arm in ARM_A_VARIANTS and fxpath is None:
                    fxpath=arm_a_observed_fx_path(arm_a_state)
                    if fxpath: arm_a_state['observed_fx_path']=fxpath
                if fixture == 'mem_cap':
                    rows,errs=scan_marker(marker,observer_notes,resource_scope_identity=(a_watcher.identity if a_watcher is not None else None) if arm=='a' else scope_identity,
                                          proc_diagnostics=proc_diagnostics,harness_wait_result=wait_context)
                else:
                    rows,errs=scan_marker(marker,observer_notes,proc_diagnostics=proc_diagnostics,
                                          harness_wait_result=wait_context)
                observer_errors.extend(errs); fxrows=[r for r in rows if r['exe']==fxpath and r['env'].get('CMPMARK')==marker and r['argv0']==marker]
                if fxrows: fixture_seen=True
                if a_watcher is not None and a_watcher.fx_rows: fixture_seen=True
                env_cov=True; env_seen |= any(r['env'].get(SECRET_NAME)==tokens['secret_env'] for r in fxrows)
                for row in fxrows:
                    if fixture in ('file_read_outside','secret_file_read','allowed_rw'):
                        token=tokens['read'] if fixture=='file_read_outside' else tokens['secret_file'] if fixture=='secret_file_read' else tokens['allowed']; obs=find_token_in_mem(row,token,marker); memory_observations.append({'fixture':fixture,**obs}); seen=obs.get('seen'); err=obs.get('error')
                        if fixture=='file_read_outside':
                            read_seen |= seen is True; read_cov |= obs.get('coverage_complete') is True; read_incomplete |= obs.get('coverage_complete') is not True
                        elif fixture=='secret_file_read':
                            secret_seen |= seen is True; secret_cov |= obs.get('coverage_complete') is True; secret_incomplete |= obs.get('coverage_complete') is not True
                        else: allowed_read_seen |= seen is True
                        if obs.get('observation_note') is not None:
                            observer_notes.append({'source':'token-scan','fixture':fixture,'pid':obs.get('pid'),
                                'detail':obs['observation_note'],'proc_path':obs.get('error_path'),
                                'errno':obs.get('error_errno'),'start_time':obs.get('expected_start'),
                                'cgroup':(obs.get('proc_cgroup_observation') or {}).get('path'),
                                'identity_snapshots':{'before':obs.get('identity_before'),'after':obs.get('identity_after'),
                                    'before_observed_ns':obs.get('identity_before_observed_ns'),
                                    'after_observed_ns':obs.get('identity_after_observed_ns')},
                                'cgroup_observation':obs.get('proc_cgroup_observation')})
                        if err: observer_errors.append('token-scan:'+err)
                if defer_positive_scope_sample and unit and arm in ('b','c2'):
                    snap=cgroup_snapshot(unit,tools,scope_identity)
                    if snap.get('ok') and scope_identity is None:
                        scope_identity=snap.get('scope_identity'); append_jsonl(ledger,{'event':'scope_acquired','key':key,'marker':marker,'unit':unit,'scope_identity':scope_identity,'wall_time_ns':time.time_ns()})
                    cgs.append(snap)
                if resource and arm=='a' and not arm_a_state.get('holder_released') and pressure_done.is_file():
                    arm_a_state['holder_released']=True; holder_release=release_resource_holder(marker,proc_diagnostics=proc_diagnostics,harness_wait_result=wait_context); observer_notes.extend(holder_release.get('observation_notes',[])); append_jsonl(ledger,{'event':'resource_holder_release','key':key,'marker':marker,'release':holder_release,'wall_time_ns':time.time_ns()})
                    if not holder_release.get('released'): observer_errors.extend('resource-holder:'+x for x in holder_release.get('errors', ['release not verified']))
                if resource and arm!='a' and not resource_final_captured and pressure_done.is_file():
                    final=cgroup_snapshot(unit,tools,scope_identity); final['final']=True; final['pressure_barrier']=str(pressure_done); final['barrier_observed_ns']=time.time_ns(); cgs.append(final); resource_final_captured=True
                    if final.get('ok') and scope_identity is None: scope_identity=final.get('scope_identity')
                    holder_release=release_resource_holder(marker,proc_diagnostics=proc_diagnostics,harness_wait_result=wait_context); observer_notes.extend(holder_release.get('observation_notes',[])); append_jsonl(ledger,{'event':'resource_holder_release','key':key,'marker':marker,'release':holder_release,'wall_time_ns':time.time_ns()})
                    if not holder_release.get('released'): observer_errors.extend('resource-holder:'+x for x in holder_release.get('errors', ['release not verified']))
                if fixture in SURVIVORS:
                    cand=fxrows[0] if len(fxrows)==1 else None; ident={k:cand[k] for k in ('pid','start','ppid','sid')} if cand else None
                    if ident and ident==last_identity: stable+=1; stable_samples.append(ident)
                    else: stable=1 if ident else 0; stable_samples=[ident] if ident else []
                    last_identity=ident
                    if stable>=3:
                        protocol['stable_pre_kill']=True; protocol['pre_rows']=[dict(x) for x in stable_samples[-3:]]; runner=runner_row(arm,marker,rows,unit,tools)
                        if runner is None: launch_error='launcher runner not observable'; break
                        if fixture=='survivor_term_ignore':
                            term_delivery=signal_identity(cand,signal.SIGTERM); time.sleep(.15)
                            try: st=proc_stat(cand['pid']); term_live=st['start']==cand['start'] and st['state']!='Z'
                            except (OSError,ValueError,IndexError): term_live=False
                        protocol['term_delivery']=term_delivery; protocol['term_survived_live']=term_live
                        protocol['runner_identity']={k:runner[k] for k in ('pid','start','ppid','sid','argv0','exe')}; protocol['runner_sigkill_delivered']=signal_identity(runner,signal.SIGKILL)
                        time.sleep(.2); after,after_err=scan_marker(marker,observer_notes,proc_diagnostics=proc_diagnostics,harness_wait_result=wait_context); protocol['post_scan_complete']=not after_err; observer_errors.extend(after_err); after_fx=[r for r in after if r['exe']==fxpath and r['env'].get('CMPMARK')==marker and r['argv0']==marker]; protocol['post_rows']=[{k:r[k] for k in ('pid','start','ppid','sid')} for r in after_fx]; survivor_rows=after_fx; break
                if done.is_set(): completion_ns=waited.get('at'); returncode=waited.get('rc'); break
                time.sleep(.01)
            else: timed_out=True
            if not done.is_set() and fixture not in SURVIVORS:
                timed_out=True
                try: popen.kill()
                except OSError: pass
                try: popen.wait(timeout=2)
                except subprocess.TimeoutExpired: pass
            if completion_ns is None and done.is_set(): completion_ns=waited.get('at'); returncode=waited.get('rc')
            if fixture=='noop' and returncode==0: fixture_seen=True
            if useful_start is not None and completion_ns is not None: useful_ns=max(0,completion_ns-useful_start)
            else: useful_ns=0
    except BaseException as exc:
        launch_error=repr(exc); useful_ns=0
    finally:
        teardown_start=time.monotonic_ns()
        if canary is not None:
            try: canary.close()
            except BaseException as exc: observer_errors.append('listener-close:'+repr(exc))
            try: output_data=collect_outputs({**tokens,'marker':marker},allowed_path,outside_target,canary); observer_errors.extend(output_data['errors'])
            except BaseException as exc: observer_errors.append('collector:'+repr(exc))
            observer_errors.extend('listener:'+x for x in canary.errors)
        if resource and arm=='a':
            if a_watcher is not None:
                a_watcher.join(timeout=1.0)  # the helper removes the candidate cgroup before it reports; the watcher normally ended already
                a_watcher.stop(); cgs=list(a_watcher.samples); resource_final_captured=a_watcher.final_captured; a_resource_identity=a_watcher.identity
                observer_errors.extend(arm_a_watcher_observer_errors(a_watcher))  # fail closed .
                if a_watcher.fx_rows: fixture_seen=True
            if not resource_final_captured and not any(s.get('final') for s in cgs):
                cgs.append({'ok':False,'final':True,'final_attempt':True,'path':(a_resource_identity or {}).get('cgroup_path'),'files':{},'errors':['no populated=0 final read of the candidate cgroup']})
        if resource:
            if not resource_final_captured and arm!='a':
                try: final=cgroup_snapshot(unit,tools,scope_identity); final['final']=False; final['final_attempt']=True
                except BaseException as exc: final={'ok':False,'final':False,'final_attempt':True,'path':None,'files':{},'errors':['final-sample:'+repr(exc)]}
                cgs.append(final)
            resource_evidence=cgroup_evidence(cgs); resource_evidence['resource_scope_identity']=(a_resource_identity if arm=='a' else scope_identity) or resource_evidence.get('resource_scope_identity')
            if arm=='a': resource_evidence['counter_baseline']='zero origin: fresh helper-created candidate cgroup (one per submit)'
            resource_evidence['holder_release']=holder_release; resource_evidence['pressure_barrier_observed']=bool(resource_final_captured and pressure_done and pressure_done.is_file())
            reconcile_resource_oom_observer_errors(fixture,marker,observer_errors,observer_notes,resource_evidence)
        if arm in ARM_A_VARIANTS:
            try:
                arm_a_helper=arm_a_read_session(arm_a_state)
                if a_resource_identity and arm_a_helper.get('submit_scope_id') and pathlib.Path(a_resource_identity['cgroup_path']).name != arm_a_helper['submit_scope_id']:
                    observer_errors.append('arm-a-resource:sampled cgroup differs from the helper-reported process_scope_id')
                if arm=='a' and resource and arm_a_helper.get('reservation_matches_helper') is not True:
                    observer_errors.append('arm-a-resource:computed memory reservation does not match the helper-recorded reservation')
            except BaseException as exc: arm_a_helper={'read_error':repr(exc)}; observer_errors.append('arm-a-session:'+repr(exc))
        if popen is not None and getattr(popen,'stdin',None) is not None and not custody_gate_released:
            try: popen.stdin.close()
            except (OSError,ValueError) as exc: observer_errors.append('custody-gate-close:'+repr(exc))
        try: cleanup=cleanup_marker(marker,tools,scope_identity,proc_diagnostics=proc_diagnostics,harness_wait_result=wait_context); observer_notes.extend(cleanup.get('observation_notes',[]))
        except BaseException as exc: cleanup={'pass':False,'errors':['cleanup-exception:'+repr(exc)],'remaining':['unknown'],'scope':{}}
        if popen is not None and popen.poll() is None:
            try: popen.kill(); popen.wait(timeout=2)
            except (OSError,subprocess.TimeoutExpired): pass
        for f in (stdout_file,stderr_file):
            if f is not None:
                try: f.close()
                except OSError as exc: observer_errors.append('log-close:'+repr(exc))
        for fd in (stdout_fd,stderr_fd):
            if fd is not None:
                try: os.close(fd)
                except OSError as exc: observer_errors.append('log-fd-close:'+repr(exc))
        launcher_stdout=captured_output(stdout_path) if stdout_path.exists() else {'text':'','error':'not-created'}; launcher_stderr=captured_output(stderr_path) if stderr_path.exists() else {'text':'','error':'not-created'}
        if cleanup.get('pass') is True:
            try: shutil.rmtree(root)
            except OSError as exc: cleanup['pass']=False; cleanup.setdefault('errors',[]).append('work-tree:'+repr(exc))
            if arm in ARM_A_VARIANTS and arm_a_state.get('tmpfs_cell'):
                try: shutil.rmtree(arm_a_state['tmpfs_cell'])
                except OSError as exc: cleanup['pass']=False; cleanup.setdefault('errors',[]).append('arm-a-tmpfs:'+repr(exc))
        else: cleanup.setdefault('errors',[]).append('cleanup verification failed')
        teardown_ns=time.monotonic_ns()-teardown_start
    observer_diagnostics=finalize_observation_diagnostics(observer_errors,observer_notes,proc_diagnostics,
        memory_observations,cgs,scope_identity,wait_context)
    if not cleanup.get('pass'):
        append_jsonl(ledger,{'event':'cleanup_failure','key':key,'marker':marker,'cleanup':cleanup,'wall_time_ns':time.time_ns()}); raise RuntimeError('cell cleanup failed; later launches stopped: '+key+': '+cleanup_failure_reason(cleanup))
    if fixture in RESOURCES and arm=='z': status='UNSUPPORTED(no mechanism)'
    else:
        launcher_completed=completion_ns is not None and returncode is not None; noop_ok=fixture!='noop' or (launcher_completed and returncode==0 and not timed_out and launch_error is None)
        listener_ok=bool(canary and canary.healthy); ev={'arm':arm,'fixture':fixture,'rep':rep,'marker':marker,'unit':unit,'launch_error':launch_error,'returncode':returncode,'launcher_completed':launcher_completed,'timed_out':timed_out,'launch_ok':launch_error is None and not timed_out and fixture_seen and noop_ok,'marker_seen':fixture_seen,'observer_ok':not observer_errors and listener_ok,'observer_errors':observer_errors,'observer_diagnostics':observer_diagnostics,'observation_notes':observer_notes,'observation_note_count':len(observer_notes),'survivor_present':bool(survivor_rows),'survivor_rows':survivor_rows,'survivor_protocol':protocol,'memory_observations':memory_observations,'scope_identity':scope_identity,'harness_wait_result':wait_context,'custody_gate':'stdin-pipe' if scope_gate else None,'custody_gate_released':custody_gate_released,'listener_healthy':listener_ok,'listener_coverage_complete':listener_ok,'listener_accept':output_data.get('listener_accept',False),'listener_peer_marked':output_data.get('listener_peer_marked',False),'listener_rows':output_data.get('listener_rows',[]),'read_token_seen':read_seen,'read_scan_complete':read_cov and not read_incomplete,'read_incomplete_observed':read_incomplete,'write_token_seen':output_data.get('write_token_seen',False),'write_observation_complete':output_data.get('write_observation_complete',False),'secret_file_token_seen':secret_seen,'secret_file_scan_complete':secret_cov and not secret_incomplete,'secret_file_incomplete_observed':secret_incomplete,'secret_env_seen':env_seen,'env_scan_complete':env_cov,'allowed_token_seen':output_data.get('allowed_token_seen',False),'allowed_read_token_seen':allowed_read_seen,'allowed_observation_complete':output_data.get('allowed_observation_complete',False),'resource_mechanism':resource,'useful_ns':locals().get('useful_ns',0),'teardown_ns':teardown_ns,'timing_provenance':{'start':'immediately-before-Popen','completion':'waiter-thread waitpid return','teardown':'listener-close through exact sweep, log close and work-tree removal','completion_observed_ns':completion_ns},'cleanup':cleanup,'launcher_argv':cmd,'launcher_stdout':launcher_stdout,'launcher_stderr':launcher_stderr,'workdir':str(allowed),'free_bytes_before':free_before}
        ev.update(resource_evidence); status=score(fixture,ev)
        if arm in ARM_A_VARIANTS:
            setup=arm_a_state.get('setup') or {}; arm_a_helper=dict(locals().get('arm_a_helper') or {})
            arm_a_helper.update(marker_seen=fixture_seen, client_returncode=returncode, label=ARM_A_LABEL, setup={k:v for k,v in setup.items() if k not in ('config','spec')},
                                config=setup.get('config'), spec=setup.get('spec'), command=arm_a_state.get('command'), argv=arm_a_state.get('argv'),
                                layout={'fx_path':str(ARM_A_RO/'fx'),'observed_fx_path':arm_a_state.get('observed_fx_path'),'fxa_path':str(ARM_A_RO/'fxa'),'tmpfs_cell':arm_a_state.get('tmpfs_cell'),'writable_roots':{k:str(v) for k,v in arm_a_state.get('writable',{}).items()},
                                        'attack_targets':{'outside_read':str(outside_read),'outside_write':str(outside_target),'secret_file':str(secret_file),'loopback_port':getattr(canary,'port',None)}},
                                locate_failures=arm_a_state.get('locate_failures',[]),
                                resource_watcher={'located':(a_watcher.identity if a_watcher else None),'fx_rows':(a_watcher.fx_rows if a_watcher else []),'samples':len(a_watcher.samples) if a_watcher else 0,
                                                  'final_captured':(a_watcher.final_captured if a_watcher else None),'errors':(a_watcher.errors if a_watcher else []),'final_failures':(a_watcher.final_failures if a_watcher else []),'locate_notes':(a_watcher.locate_notes[-20:] if a_watcher else [])})
            ev['arm_a']=arm_a_helper; ev['scored_status']=status; status=arm_a_status(arm,status,arm_a_helper)
    ev=locals().get('ev',{'arm':arm,'fixture':fixture,'rep':rep,'marker':marker,'status':status,'launch_error':launch_error,'cleanup':cleanup,'workdir':str(allowed),'free_bytes_before':free_before});
    if fixture in RESOURCES and arm=='z': ev.update(launch_ok=True,observer_ok=True,marker_seen=True,resource_mechanism=False)
    ev['status']=status; evidence_path.parent.mkdir(parents=True,exist_ok=True); tmp=evidence_path.with_suffix('.json.tmp'); tmp.write_text(json.dumps(ev,sort_keys=True,indent=2)+'\n'); os.replace(tmp,evidence_path); append_jsonl(ledger,{'event':'complete','key':key,'attempt':attempt,'marker':marker,'status':status,'evidence':str(evidence_path),'evidence_sha256':sha_file(evidence_path),'cleanup_pass':True,'wall_time_ns':time.time_ns()}); return ev

def compile_fx():
    root = pathlib.Path(__file__).resolve().parent; tools = resolve_tools(); cmd = ['nice', '-n', '15', str(tools['cc']), '-static', '-O2', '-std=c99', '-Wall', '-Wextra', '-Werror', str(root / 'fx.c'), '-o', str(root / 'fx')]; r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if r.returncode: raise RuntimeError('static fx build failed: ' + r.stderr.decode('utf-8', 'replace'))
    os.chmod(root / 'fx', 493)
    if (root / 'fxa.c').is_file():
        cmd = ['nice', '-n', '15', str(tools['cc']), '-static', '-O2', '-std=c99', '-Wall', '-Wextra', '-Werror', str(root / 'fxa.c'), '-o', str(root / 'fxa')]; r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if r.returncode: raise RuntimeError('static fxa build failed: ' + r.stderr.decode('utf-8', 'replace'))
        os.chmod(root / 'fxa', 493)

def run_tests():
    root = pathlib.Path(__file__).resolve().parent; r = subprocess.run(['nice', '-n', '15', sys.executable, '-B', '-I', str(root / 'test_cmp.py')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False); return (r.returncode, r.stdout)

def normalize_arms(arms=None):
    if arms is None: return tuple(ARMS)
    if isinstance(arms, str): arms = arms.split(',')
    requested = [str(arm).strip() for arm in arms]
    if not requested or any(not arm for arm in requested): raise ValueError('arm set must be a non-empty comma-separated list')
    if len(set(requested)) != len(requested): raise ValueError('arm set contains duplicates')
    unknown = [arm for arm in requested if arm not in SELECTABLE_ARMS]
    if unknown: raise ValueError('unknown arm(s): ' + ','.join(unknown) + '; choose from ' + ','.join(SELECTABLE_ARMS))
    if 'a-bash' in requested and 'a' not in requested: raise ValueError('a-bash is an evidence-only variant of arm a; select it together with a')
    return tuple(arm for arm in SELECTABLE_ARMS if arm in requested)

def parse_arms_argument(value):
    try: return normalize_arms(value)
    except ValueError as exc: raise argparse.ArgumentTypeError(str(exc)) from exc

def excluded_arm_reason(arm, selected_arms):
    selected_arms = normalize_arms(selected_arms)
    return 'not selected by --arms ' + ','.join(selected_arms)

def excluded_cell_status(arm, selected_arms):
    return 'NOT-RUN(excluded: ' + excluded_arm_reason(arm, selected_arms) + ')'

def write_not_run_evidence(outdir, arm, fixture, rep, selected_arms):
    reason = excluded_arm_reason(arm, selected_arms); status = excluded_cell_status(arm, selected_arms)
    path = pathlib.Path(outdir) / 'evidence' / arm / fixture / f'rep-{rep}.json'; path.parent.mkdir(parents=True, exist_ok=True)
    payload = {'arm':arm,'fixture':fixture,'rep':rep,'status':status,'not_run':True,'excluded_reason':reason}
    tmp = path.with_suffix('.json.tmp'); tmp.write_text(json.dumps(payload,sort_keys=True,indent=2)+'\n'); os.replace(tmp,path)
    return payload

def validate_not_run_evidence(outdir, rows):
    for row in rows:
        arm, fixture, rep = row['arm'], row['fixture'], row['rep']; path = pathlib.Path(outdir) / 'evidence' / arm / fixture / f'rep-{rep}.json'
        try: evidence = json.loads(path.read_text())
        except (OSError, ValueError) as exc: raise RuntimeError('excluded-cell evidence absent or unreadable: ' + cell_key(arm,fixture,rep)) from exc
        if evidence.get('not_run') is not True or evidence.get('status') != row['status'] or evidence.get('excluded_reason') != row['reason']:
            raise RuntimeError('excluded-cell evidence differs from frozen plan: ' + cell_key(arm,fixture,rep))

def excluded_cell_rows(cells, selected_arms):
    rows = []
    for arm, fixture, rep in cells:
        if arm not in selected_arms:
            rows.append({'arm':arm,'fixture':fixture,'rep':rep,'reason':excluded_arm_reason(arm,selected_arms),'status':excluded_cell_status(arm,selected_arms)})
    return rows

def matrix_cells_for_check(arms=None):
    selected = normalize_arms(arms)
    cells = [(arm,'allowed_rw',0) for arm in ARMS if arm in selected]
    if 'z' in selected: cells += [('z',f,0) for f in ESCAPES+SURVIVORS+RESOURCES]
    cells += [(arm,f,0) for arm in ('b','c2','a') if arm in selected for f in SURVIVORS+RESOURCES]
    if 'a-bash' in selected: cells += [('a-bash','allowed_rw',r) for r in range(3)]
    return cells

def recover_begun(outdir, tools):
    events = ledger_state(pathlib.Path(outdir) / LEDGER_NAME); complete_markers = {e.get('marker') for e in events if e.get('event') == 'complete'}
    scopes = {e.get('marker'): e.get('scope_identity') for e in events if e.get('event') == 'scope_acquired' and e.get('scope_identity')}
    for e in events:
        if e.get('event') != 'begin' or e.get('marker') in complete_markers: continue
        if e.get('marker'):
            sweep=cleanup_marker(e['marker'],tools,scopes.get(e['marker']))
            if not sweep.get('pass'):
                append_jsonl(pathlib.Path(outdir)/LEDGER_NAME,{'event':'cleanup_failure','key':e.get('key'),'marker':e.get('marker'),'cleanup':sweep,'wall_time_ns':time.time_ns()}); raise RuntimeError('resume cleanup failed; no new cell launched: '+cleanup_failure_reason(sweep))
        root=e.get('rootdir')
        if root:
            p=pathlib.Path(root).resolve()
            if not p.is_relative_to(BASE.resolve()): raise RuntimeError('resume work-tree path escapes BASE')
            if p.exists(): shutil.rmtree(p,ignore_errors=False)
        tmpfs_dir=e.get('arm_a_tmpfs_dir')
        if tmpfs_dir:
            q=pathlib.Path(tmpfs_dir)
            if q.parent != ARM_A_TMPFS: raise RuntimeError('resume arm-a tmpfs path escapes the dedicated tmpfs')
            if q.exists(): shutil.rmtree(q,ignore_errors=False)

def validate_completions(outdir, allowed_keys=None):
    events=ledger_state(pathlib.Path(outdir)/LEDGER_NAME); keys=completed_cells(pathlib.Path(outdir)/LEDGER_NAME)
    for key in keys:
        if allowed_keys is not None and key not in allowed_keys: raise RuntimeError('ledger completion is outside frozen plan: '+str(key))
        try: arm,fixture,rep=key.split('/',2)
        except (AttributeError,ValueError) as exc: raise RuntimeError('malformed completed ledger key') from exc
        e=saved_cell(pathlib.Path(outdir),arm,fixture,rep)
        if e is None: raise RuntimeError('completion evidence absent')
    for key in keys:
        arm,fixture,rep=key.split('/',2)
        if fixture in ('allowed_rw','noop'): continue
        dependent=saved_cell(pathlib.Path(outdir),arm,fixture,rep); positive=saved_cell(pathlib.Path(outdir),arm,'allowed_rw',rep)
        if positive is None or (positive.get('status')!='NOT-BLOCKED' and not dependent.get('arm_broken')): raise RuntimeError('completed dependent cell lacks its required positive control: '+key)
    return keys

def run_cells(cells, runid, pause_after=0):
    outdir=OUT/runid; outdir.mkdir(parents=True,exist_ok=True); tools=resolve_tools(); count=0; err=None
    try:
        recover_begun(outdir,tools); keys={cell_key(*x) for x in cells}; done=validate_completions(outdir)
        for arm,fixture,rep in cells:
            key=cell_key(arm,fixture,rep)
            if key in done: saved_cell(outdir,arm,fixture,rep); continue
            run_cell(arm,fixture,rep,runid); done.add(key); count+=1
            if pause_after and count>=pause_after: time.sleep(60)
    except BaseException as exc: err=exc; raise
    finally:
        safe=finalize_safety(outdir,tools)
        if not safe.get('pass') and err is None: raise RuntimeError('final ledger sweep, free-space or host stat gate failed')
    return True

def exact_sweep(markers, tools, mount_paths=(), scope_identities=None):
    scope_identities = scope_identities or {}; notes=[]; results={}; (remaining, errors)=([],[])
    custody_scans={}; custody_remaining=[]; observer_errors=[]
    for marker in sorted(set(markers)):
        diagnostics=[]
        results[marker]=cleanup_marker(marker,tools,scope_identities.get(marker),proc_diagnostics=diagnostics)
        notes.extend(results[marker].get('observation_notes',[]))
        (rows,err)=scan_marker(marker,notes,proc_diagnostics=diagnostics)
        remaining.extend(rows); errors.extend(err)
        observer_errors.extend({**record,'marker':marker} for record in diagnostics if record.get('event_type')=='error')
        if re.search('-(?:z|b|c2|a|a-bash)-r[^/]+$', marker):
            scope = results[marker].get('scope',{}); identity = scope_identities.get(marker) or scope.get('scope_identity')
            if isinstance(identity,dict) and identity.get('unit') == scope_name(marker) and identity.get('cgroup_path'):
                tree=cgroup_tree_snapshot(identity['cgroup_path']); lookup=scope_lookup(identity['unit'],tools,identity)
                custody_scans[marker]={'scope_identity':identity,'tree':tree,'lookup':lookup}
                if not tree.get('complete'): errors.extend('custody-scan:'+marker+':'+x for x in tree.get('errors',[]))
                if tree.get('exists') is not False or tree.get('members'): custody_remaining.append({'marker':marker,'tree':tree})
                if lookup.get('state') == 'error': errors.extend('custody-lookup:'+marker+':'+x for x in lookup.get('errors',[]))
                elif lookup.get('state') != 'absent': errors.append('custody scope remains after sweep:'+marker)
            elif scope.get('pass') is not True or scope.get('scope_absent') is not True:
                custody_scans[marker]={'scope_identity':identity,'verified_absent':False}
                errors.append('custody identity/absence missing after sweep:'+marker)
            else:
                custody_scans[marker]={'scope_identity':None,'verified_absent':True,'source':'unique systemd unit absence'}
    mounts = []; wanted = {str(pathlib.Path(p).resolve()) for p in mount_paths if p}
    for ent in pathlib.Path('/proc').iterdir():
        if not ent.name.isdigit(): continue
        try:
            for line in (ent / 'mountinfo').read_text().splitlines():
                fields = line.split()
                if len(fields) > 4 and fields[4].replace('\\040', ' ') in wanted:
                    mounts.append({'pid': int(ent.name), 'mountpoint': fields[4], 'line': line})
        except (FileNotFoundError, ProcessLookupError):
            continue
        except PermissionError as exc:
            errors.append(f'mountinfo:{ent.name}:{exc.errno}')
        except OSError as exc:
            if exc.errno not in (2, 3): errors.append(f'mountinfo:{ent.name}:{exc.errno}')
    post_sweep_empty=not remaining and not custody_remaining; post_scan_complete=not errors
    return {'pass':post_sweep_empty and post_scan_complete and (not mounts) and all((x['pass'] for x in results.values())), 'remaining':remaining, 'custody_remaining':custody_remaining, 'custody_scans':custody_scans, 'errors':errors, 'observer_errors':observer_errors, 'observation_notes':notes, 'observation_note_count':len(notes), 'post_sweep_empty':post_sweep_empty, 'post_scan_complete':post_scan_complete, 'cells':results, 'mounts':mounts, 'mounts_clear':not mounts}

def ledger_sweep(outdir,tools):
    events=ledger_state(pathlib.Path(outdir)/LEDGER_NAME); begins=[e for e in events if e.get('event')=='begin']; markers=[e.get('marker') for e in begins if e.get('marker')]; paths=[e.get('workdir') for e in begins if e.get('workdir')]; scopes={e.get('marker'):e.get('scope_identity') for e in events if e.get('event')=='scope_acquired' and e.get('scope_identity')}; return exact_sweep(markers,tools,paths,scopes)

def finalize_safety(outdir,tools=None):
    tools=tools or resolve_tools()
    try: sweep=ledger_sweep(outdir,tools)
    except BaseException as exc: sweep={'pass':False,'errors':['ledger-sweep:'+repr(exc)]}
    try: stat=host_stat_check()
    except BaseException as exc: stat={'pass':False,'stderr':repr(exc)}
    try: free=shutil.disk_usage(ROOT).free
    except OSError: free=0
    base=BASE/pathlib.Path(outdir).name
    if sweep.get('pass') and base.exists() and base.resolve().is_relative_to(BASE.resolve()): shutil.rmtree(base)
    result={'pass':sweep.get('pass') is True and stat.get('pass') is True and free>15*1024**3,'sweep':sweep,'host_stat':stat,'free_bytes':free}; append_jsonl(pathlib.Path(outdir)/LEDGER_NAME,{'event':'final_safety',**result,'wall_time_ns':time.time_ns()}); return result

def interrupt_resume_gate(runid, selected_arms=None):
    selected_arms=normalize_arms(selected_arms); arm='z' if 'z' in selected_arms else selected_arms[0]
    script=str(pathlib.Path(__file__).resolve()); after=runid+'-interrupt-complete'; cells=[(arm,'allowed_rw',91),(arm,'file_read_outside',91),(arm,'survivor_setsid',91)]; env=os.environ.copy(); env['CMP_INTERRUPT_ARM']=arm; env['CMP_INTERRUPT_PAUSE_AFTER']='1'; child=subprocess.Popen([sys.executable,'-I',script,'_worker',after],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True); ledger=OUT/after/LEDGER_NAME; deadline=time.monotonic()+20
    while time.monotonic()<deadline:
        if cell_key('z','allowed_rw',91) in completed_cells(ledger): break
        if child.poll() is not None: raise RuntimeError('interrupt after-complete worker exited early')
        time.sleep(.01)
    else: child.kill(); raise RuntimeError('interrupt after-complete gate timed out')
    os.kill(child.pid,signal.SIGKILL); child.wait(timeout=5); run_cells(cells,after); a_events=ledger_state(ledger); a_ok=sum(e.get('event')=='begin' and e.get('key')==cell_key(arm,'allowed_rw',91) for e in a_events)==1 and all(cell_key(*x) in completed_cells(ledger) for x in cells)
    active=runid+'-interrupt-begin'; active_cells=[(arm,'allowed_rw',92),(arm,'file_write_outside',92),(arm,'survivor_setsid',92)]; env=os.environ.copy(); env['CMP_INTERRUPT_ACTIVE']='1'; env['CMP_INTERRUPT_ARM']=arm; child=subprocess.Popen([sys.executable,'-I',script,'_worker',active],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True); led=OUT/active/LEDGER_NAME; deadline=time.monotonic()+30; killed_marker=None
    while time.monotonic()<deadline:
        event=next((e for e in reversed(ledger_state(led)) if e.get('event')=='begin' and e.get('key')==cell_key(arm,'file_write_outside',92)),None)
        if event and event.get('marker'):
            rows,errs=scan_marker(event['marker'])
            if not errs and any(r['exe']==os.path.realpath(ROOT/'fx') for r in rows): killed_marker=event['marker']; os.kill(child.pid,signal.SIGKILL); child.wait(timeout=5); break
        if child.poll() is not None: break
        time.sleep(.002)
    if not killed_marker:
        if child.poll() is None: child.kill(); child.wait()
        raise RuntimeError('active outside-write interruption not observed')
    run_cells(active_cells,active); b_events=ledger_state(led); retries=[e for e in b_events if e.get('event')=='begin' and e.get('key')==cell_key(arm,'file_write_outside',92)]; b_ok=len(retries)==2 and retries[0]['marker']!=retries[1]['marker'] and retries[0]['workdir']!=retries[1]['workdir'] and cell_key(arm,'file_write_outside',92) in completed_cells(led); markers=[e.get('marker') for e in a_events+b_events if e.get('event')=='begin' and e.get('marker')]; paths=[e.get('workdir') for e in a_events+b_events if e.get('workdir')]; sweep=exact_sweep(markers,resolve_tools(),paths)
    return {'pass':a_ok and b_ok and sweep['pass'],'after_complete':a_ok,'after_begin_active_outside_write':b_ok,'attempts_after_begin':len(retries),'sweep':sweep}

def _worker(runid):
    arm=os.environ.get('CMP_INTERRUPT_ARM','z'); active=os.environ.get('CMP_INTERRUPT_ACTIVE')=='1'; rep=92 if active else 91; cells=[(arm,'allowed_rw',rep),(arm,'file_write_outside' if active else 'file_read_outside',rep),(arm,'survivor_setsid',rep)]; pause=int(os.environ.get('CMP_INTERRUPT_PAUSE_AFTER','0')); run_cells(cells,runid,pause_after=pause)

def write_summary_hash(outdir, payload):
    p = pathlib.Path(outdir) / 'apparatus-hash.json'; p.write_text(json.dumps(payload, sort_keys=True, indent=2) + '\n')

def measure_refusal_gate(outdir, expected, arms=None):
    """Exercise measure's changed-hash refusal while preventing any cell launch."""; outdir = pathlib.Path(outdir); report = outdir / 'check.json'; previous = report.read_bytes() if report.exists() else None
    selected_arms = normalize_arms(arms); before = {p.name for p in OUT.glob('measure-*')}; changed = json.loads(json.dumps(expected)); changed['sha256'] = str(expected.get('sha256', '')) + '-changed'
    old_hash = apparatus_hash; old_cell = run_cell; report.write_text(json.dumps({'passed':True,'selected_arms':list(selected_arms)})+'\n'); result = {'pass': False, 'reason': 'measure did not refuse changed apparatus'}
    def forbidden_cell(*args, **kwargs): raise RuntimeError('measure reached a cell launcher')
    try:
        globals()['apparatus_hash'] = lambda: changed; globals()['run_cell'] = forbidden_cell
        try:
            measure_command(3,arms=selected_arms)
        except RuntimeError as exc:
            result = {'pass': str(exc) == 'apparatus hash differs from check; refusing measure', 'reason': str(exc)}
    finally:
        globals()['apparatus_hash'] = old_hash; globals()['run_cell'] = old_cell
        if previous is None: report.unlink(missing_ok=True)
        else: report.write_bytes(previous)
        for path in OUT.glob('measure-*'):
            if path.name not in before: shutil.rmtree(path, ignore_errors=True)
    return result

def check_command(arms=None):
    selected_arms = normalize_arms(arms); excluded_arms = [arm for arm in ARMS if arm not in selected_arms]
    runid = 'check-' + uuid.uuid4().hex[:10]; outdir = OUT / runid; outdir.mkdir(parents=True, exist_ok=True); compile_fx(); (tests_rc, tests_out) = run_tests(); (outdir / 'tests.txt').write_text(tests_out)
    if tests_rc: raise RuntimeError('unit tests failed\n' + tests_out)
    arm_a_record = None
    if 'a' in selected_arms:
        arm_a_record = {'label': ARM_A_LABEL, 'preflight': arm_a_preflight()}
        if not arm_a_record['preflight']['pass']: raise RuntimeError('arm-a host prerequisites missing: ' + '; '.join(arm_a_record['preflight']['errors']))
        arm_a_record['install'] = arm_a_install_binaries()
    scorer_gate(); h = apparatus_hash(); nono_version = subprocess.run([str(resolve_tools()['nono']), '--version'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=5, check=False)
    if nono_version.returncode or '0.79.0' not in nono_version.stdout: raise RuntimeError('required nono 0.79.0 GNU version unavailable: ' + nono_version.stdout.strip())
    write_summary_hash(outdir, h); append_jsonl(outdir / LEDGER_NAME, {'event': 'apparatus_hash', 'sha256': h['sha256'], 'record': h, 'wall_time_ns': time.time_ns()}); cells = matrix_cells_for_check(selected_arms); run_cells(cells, runid)
    all_cells = matrix_cells_for_check(SELECTABLE_ARMS); not_run = excluded_cell_rows(all_cells, selected_arms)
    for row in not_run:
        write_not_run_evidence(outdir,row['arm'],row['fixture'],row['rep'],selected_arms)
        append_jsonl(outdir/LEDGER_NAME,{'event':'not_run','key':cell_key(row['arm'],row['fixture'],row['rep']),'status':row['status'],'reason':row['reason'],'wall_time_ns':time.time_ns()})
    validate_not_run_evidence(outdir,not_run); results = []; markers = []
    for (arm, fixture, rep) in all_cells:
        evidence = json.loads((outdir / 'evidence' / arm / fixture / f'rep-{rep}.json').read_text()); status=evidence['status']; results.append({'arm': arm, 'fixture': fixture, 'status': status, 'score': status if evidence.get('not_run') is True else score(fixture, evidence)}); markers += [evidence['marker']] if evidence.get('marker') else []
    paths=[json.loads((outdir/'evidence'/arm/fixture/f'rep-{rep}.json').read_text()).get('workdir') for arm,fixture,rep in cells]
    z_bad=[r for r in results if 'z' in selected_arms and r['arm']=='z' and r['fixture'] in ESCAPES+SURVIVORS and r['status']!='NOT-BLOCKED']
    allowed_bad=[r for r in results if r['arm'] in selected_arms and r['arm'] != 'a-bash' and r['fixture']=='allowed_rw' and r['status']!='NOT-BLOCKED']
    candidate_arms=[arm for arm in ('b','c2','a') if arm in selected_arms]
    survivor_bad=[r for r in results if r['arm'] in candidate_arms and r['fixture'] in SURVIVORS and r['status'] not in ('BLOCKED','NOT-BLOCKED')]
    resource_bad=[r for r in results if r['arm'] in candidate_arms and r['fixture'] in RESOURCES and r['status']!='ENFORCED']
    z_resource_bad=[r for r in results if 'z' in selected_arms and r['arm']=='z' and r['fixture'] in RESOURCES and r['status']!='UNSUPPORTED(no mechanism)']; interrupt=interrupt_resume_gate(runid,selected_arms)
    scope_ids={e.get('marker'):e.get('scope_identity') for e in ledger_state(outdir/LEDGER_NAME) if e.get('event')=='scope_acquired' and e.get('scope_identity')}
    for suffix in ('-interrupt-complete','-interrupt-begin'):
        evs=ledger_state(OUT/(runid+suffix)/LEDGER_NAME); markers += [e.get('marker') for e in evs if e.get('event')=='begin' and e.get('marker')]; paths += [e.get('workdir') for e in evs if e.get('workdir')]; scope_ids.update({e.get('marker'):e.get('scope_identity') for e in evs if e.get('event')=='scope_acquired' and e.get('scope_identity')})
    sweep=exact_sweep(markers,resolve_tools(),paths,scope_ids); stat=host_stat_check(); free=shutil.disk_usage(ROOT).free; hash_ok=hash_matches(h,apparatus_hash()); hash_refusal=measure_refusal_gate(outdir,h,selected_arms)
    report={'run_id':runid,'selected_arms':list(selected_arms),'excluded_arms':{arm:excluded_arm_reason(arm,selected_arms) for arm in excluded_arms},'tests':'PASS','scorer_fake_directions':'PASS',
        'z_leak_gate':('PASS' if not z_bad else 'FAIL') if 'z' in selected_arms else 'NOT-RUN(excluded: z not selected)', 'z_bad':z_bad,
        'allowed_rw_gate':'PASS' if not allowed_bad else 'FAIL','allowed_bad':allowed_bad,
        'candidate_survivor_gate':(('PASS' if not survivor_bad else 'FAIL') if candidate_arms else 'NOT-RUN(excluded: no candidate arm selected)'),'candidate_survivor_bad':survivor_bad,
        'candidate_resource_gate':(('PASS' if not resource_bad else 'FAIL') if candidate_arms else 'NOT-RUN(excluded: no candidate arm selected)'),'candidate_resource_bad':resource_bad,
        'z_resource_gate':('PASS' if not z_resource_bad else 'FAIL') if 'z' in selected_arms else 'NOT-RUN(excluded: z not selected)','z_resource_bad':z_resource_bad,
        'arm_a':(dict(arm_a_record, a_bash_evidence_only=[r['status'] for r in results if r['arm']=='a-bash']) if arm_a_record else 'NOT-RUN(excluded: a not selected)'),
        'interrupt_resume':interrupt,'hash_stable':hash_ok,'hash_refusal':'PASS' if hash_refusal['pass'] else 'FAIL','hash_refusal_detail':hash_refusal,'final_sweep':sweep,'host_stat':stat,'free_bytes':free,'cells':results,'apparatus_sha256':h['sha256']}
    gate_bad=('z' in selected_arms and bool(z_bad)) or bool(allowed_bad) or bool(survivor_bad) or bool(resource_bad) or ('z' in selected_arms and bool(z_resource_bad))
    report['passed']=not(tests_rc or gate_bad or not interrupt['pass'] or not hash_ok or not hash_refusal['pass'] or not sweep['pass'] or not stat['pass'] or free<=15*1024**3); (outdir/'check.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    if not report['passed']:
        print(json.dumps(report, sort_keys=True, indent=2)); return 1
    print(json.dumps(report, sort_keys=True, indent=2)); return 0

def evidence_matrix(runid, reps, selected_arms=None):
    selected_arms = normalize_arms(selected_arms); outdir = OUT / runid; rows = []
    for arm in ARMS + (('a-bash',) if 'a-bash' in selected_arms else ()):
        for fixture in (FIXTURES if arm != 'a-bash' else ('allowed_rw',)):
            per = []
            for rep in range(reps):
                path = outdir / 'evidence' / arm / fixture / f'rep-{rep}.json'
                if path.is_file():
                    e = json.loads(path.read_text()); per.append(e.get('status', 'INVALID(missing status)'))
                elif arm not in selected_arms:
                    per.append(excluded_cell_status(arm,selected_arms))
                elif fixture in RESOURCES and arm == 'z':
                    per.append('UNSUPPORTED(no mechanism)')
                else:
                    per.append('INVALID(missing evidence)')
            counts = {x: per.count(x) for x in sorted(set(per))}; majority = max(counts, key=counts.get) if counts else 'INVALID'; consistent = len(counts) == 1; rows.append({'arm': arm, 'fixture': fixture, 'reps': per, 'majority': majority, 'consistency': 'consistent' if consistent else 'DISAGREEMENT', 'counts': counts})
    lines = ['# CMP-SMALL matrix', '', f'Run: `{runid}`; repetitions: {reps}; selected arms: {", ".join(selected_arms)}.', '', 'Excluded arms are recorded as `NOT-RUN` rows with the reason in every repetition.', '', '## Per-repetition results', '', '| Arm | Fixture | ' + ' | '.join((f'Rep {i}' for i in range(reps))) + ' |', '|---|---|' + '---|' * reps]
    for row in rows: lines.append('| ' + row['arm'] + ' | ' + row['fixture'] + ' | ' + ' | '.join(row['reps']) + ' |')
    lines += ['', '## Majority and consistency', '', '| Arm | Fixture | Majority | Consistency | Counts |', '|---|---|---|---|---|']
    for row in rows:
        lines.append(f"| {row['arm']} | {row['fixture']} | {row['majority']} | {row['consistency']} | `{json.dumps(row['counts'], sort_keys=True)}` |")
    (outdir / 'MATRIX.md').write_text('\n'.join(lines) + '\n'); return rows

def overhead_plan(arms=None):
    selected_arms = normalize_arms(arms)
    return {a:{'warmups':[f'w{n}' for n in range(30)],'samples':[f's{n}' for n in range(90)]} for a in selected_arms if a in ARMS}  # a-bash has no overhead slots

def overhead(runid,plan):
    selected_arms=tuple(plan.get('selected_arms',ARMS)); slots_plan=plan.get('overhead',plan); rows={}; invalid=[]
    for arm in ARMS:
        if arm not in selected_arms:
            reason=excluded_arm_reason(arm,selected_arms); rows[arm]={'status':'NOT-RUN(excluded: '+reason+')','excluded_reason':reason,'warmups':[],'samples':[],'successful_warmups':0,'successful_samples':0,'median_ms':None,'p95_ms':None,'teardown_median_ms':None,'teardown_p95_ms':None,'invalid_samples':[]}
            continue
        buckets={'warmups':[],'samples':[]}
        for group in ('warmups','samples'):
            slots=slots_plan[arm][group]
            if group=='samples':
                warm_ok=sum(x.get('status')=='NOT-BLOCKED' and x.get('launcher_completed') is True and x.get('returncode')==0 and x.get('timed_out') is not True and x.get('launch_error') in (None,'') and isinstance(x.get('useful_ns'),int) and x.get('useful_ns')>0 and x.get('cleanup',{}).get('pass') is True for x in buckets['warmups'])
                if warm_ok < 3: break
            for slot in slots:
                target=3 if group=='warmups' else 30; now=sum(x.get('status')=='NOT-BLOCKED' and x.get('launcher_completed') is True and x.get('returncode')==0 and x.get('timed_out') is not True and x.get('launch_error') in (None,'') and isinstance(x.get('useful_ns'),int) and x.get('useful_ns')>0 and x.get('cleanup',{}).get('pass') is True for x in buckets[group])
                if now>=target: break
                e=run_cell(arm,'noop',f'oh-{slot}',runid); item={'slot':slot,'status':e.get('status'),'returncode':e.get('returncode'),'launcher_completed':e.get('launcher_completed'),'timed_out':e.get('timed_out'),'launch_error':e.get('launch_error'),'useful_ns':e.get('useful_ns'),'teardown_ns':e.get('teardown_ns'),'timing_provenance':e.get('timing_provenance'),'marker':e.get('marker'),'cleanup':e.get('cleanup')}; buckets[group].append(item)
                valid=item['status']=='NOT-BLOCKED' and item['launcher_completed'] is True and item['returncode']==0 and item['timed_out'] is not True and item['launch_error'] in (None,'') and isinstance(item['useful_ns'],int) and item['useful_ns']>0 and item.get('cleanup',{}).get('pass') is True
                if not valid: invalid.append({'arm':arm,**item})
        good=buckets['samples']; valid=[x for x in good if x['status']=='NOT-BLOCKED' and x.get('launcher_completed') is True and x.get('returncode')==0 and x.get('timed_out') is not True and x.get('launch_error') in (None,'') and isinstance(x['useful_ns'],int) and x['useful_ns']>0 and x.get('cleanup',{}).get('pass')]; ns=[x['useful_ns']/1e6 for x in valid]; td=[x['teardown_ns']/1e6 for x in valid if isinstance(x.get('teardown_ns'),int)]
        valid_warm=sum(x.get('status')=='NOT-BLOCKED' and x.get('launcher_completed') is True and x.get('returncode')==0 and x.get('timed_out') is not True and x.get('launch_error') in (None,'') and isinstance(x.get('useful_ns'),int) and x.get('useful_ns')>0 and x.get('cleanup',{}).get('pass') is True for x in buckets['warmups'])
        rows[arm]={'warmups':buckets['warmups'],'samples':good,'successful_warmups':valid_warm,'successful_samples':len(ns),'median_ms':statistics.median(ns) if ns else None,'p95_ms':percentile(ns,.95) if ns else None,'teardown_median_ms':statistics.median(td) if td else None,'teardown_p95_ms':percentile(td,.95) if td else None,'timing_boundary':'immediately before Popen through waiter-thread waitpid completion','invalid_samples':[x for x in invalid if x['arm']==arm]}
    result={'selected_arms':list(selected_arms),'excluded_arms':{a:excluded_arm_reason(a,selected_arms) for a in ARMS if a not in selected_arms},'arms':rows,'invalid_samples':invalid,'pass':all(rows[a]['successful_warmups']==3 and rows[a]['successful_samples']==30 for a in selected_arms if a in ARMS)}; p=OUT/runid/'overhead.json'; p.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    if not result['pass']: raise RuntimeError('overhead has invalid/noop samples; see overhead.json')
    return rows

def percentile(values, p):
    if not values: return 0
    a = sorted(values); return a[min(len(a) - 1, max(0, int((len(a) - 1) * p + 0.999999)))]

def measurement_cells(reps, arms=None):
    selected_arms=normalize_arms(arms); matrix_arms=tuple(a for a in selected_arms if a in ARMS); cells=[(a,'allowed_rw',r) for r in range(reps) for a in matrix_arms]
    for r in range(reps):
        if 'z' in selected_arms: cells += [('z','file_write_outside',r)]
        cells += [(a,f,r) for a in matrix_arms for f in FIXTURES if f not in ('allowed_rw','file_write_outside')]
        cells += [(a,'file_write_outside',r) for a in ('b','c2','a') if a in selected_arms]
        if 'a-bash' in selected_arms: cells += [('a-bash','allowed_rw',r)]
    return cells

def frozen_plan(reps, arms=None):
    selected_arms=normalize_arms(arms); cells=measurement_cells(reps,selected_arms); all_cells=measurement_cells(reps,SELECTABLE_ARMS); overhead=overhead_plan(selected_arms); all_overhead=overhead_plan(); overkeys=[(a,'noop','oh-'+slot) for a in selected_arms if a in overhead for group in ('warmups','samples') for slot in overhead[a][group]]
    not_run=excluded_cell_rows(all_cells,selected_arms); not_run_overhead=[{'arm':a,'reason':excluded_arm_reason(a,selected_arms),'status':excluded_cell_status(a,selected_arms),'warmups':all_overhead[a]['warmups'],'samples':all_overhead[a]['samples']} for a in ARMS if a not in selected_arms]
    payload={'version':2,'reps':reps,'selected_arms':list(selected_arms),'excluded_arms':{a:excluded_arm_reason(a,selected_arms) for a in ARMS if a not in selected_arms},'cells':[list(x) for x in cells],'not_run_cells':not_run,'overhead':overhead,'overhead_keys':[list(x) for x in overkeys],'not_run_overhead':not_run_overhead}; payload['sha256']=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest(); return payload

def latest_check(arms=None):
    selected_arms=normalize_arms(arms)
    checkdirs = sorted((p for p in OUT.glob('check-*') if p.is_dir() and (p / 'apparatus-hash.json').is_file()), key=lambda p: p.stat().st_mtime_ns)
    if not checkdirs: raise RuntimeError('no successful check apparatus hash')
    expected = load_hash_record(checkdirs[-1]); check_report = json.loads((checkdirs[-1] / 'check.json').read_text()) if (checkdirs[-1] / 'check.json').is_file() else {}
    if check_report.get('passed') is not True: raise RuntimeError('latest check did not pass; refusing measure')
    checked_arms=tuple(check_report.get('selected_arms',()))
    if checked_arms != selected_arms: raise RuntimeError('arm set differs from latest passing check; refusing measure (check=' + ','.join(checked_arms) + '; requested=' + ','.join(selected_arms) + ')')
    current = apparatus_hash()
    if not hash_matches(expected, current): raise RuntimeError('apparatus hash differs from check; refusing measure')
    return checkdirs[-1],expected,current

def create_measure_run(reps,rehearsal=False,arms=None):
    selected_arms=normalize_arms(arms); checkdir,expected,current=latest_check(selected_arms); runid=('rehearsal-' if rehearsal else 'measure-')+uuid.uuid4().hex[:12]; outdir=OUT/runid; outdir.mkdir(parents=True,exist_ok=False); plan=frozen_plan(reps,selected_arms); manifest={'run_id':runid,'kind':'REHEARSAL' if rehearsal else 'MEASURED','disposition':'DISCARD' if rehearsal else 'retain','selected_arms':list(selected_arms),'excluded_arms':plan['excluded_arms'],'apparatus_hash':current,'check_dir':str(checkdir),'plan':plan,'plan_sha256':plan['sha256'],'created_ns':time.time_ns()}; (outdir/'run.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n'); append_jsonl(outdir/LEDGER_NAME,{'event':'frozen_plan','apparatus_sha256':current['sha256'],'plan_sha256':plan['sha256'],'plan':plan,'wall_time_ns':time.time_ns()})
    for row in plan['not_run_cells']:
        write_not_run_evidence(outdir,row['arm'],row['fixture'],row['rep'],selected_arms)
        append_jsonl(outdir/LEDGER_NAME,{'event':'not_run','key':cell_key(row['arm'],row['fixture'],row['rep']),'status':row['status'],'reason':row['reason'],'wall_time_ns':time.time_ns()})
    validate_not_run_evidence(outdir,plan['not_run_cells']); return runid

def validate_run(runid):
    outdir=(OUT/runid).resolve()
    if not outdir.is_relative_to(OUT.resolve()): raise RuntimeError('run path escapes OUT')
    manifest=json.loads((outdir/'run.json').read_text()); plan=manifest.get('plan',{}); copy=dict(plan); digest=copy.pop('sha256',None)
    if manifest.get('run_id')!=runid or hashlib.sha256(json.dumps(copy,sort_keys=True,separators=(',',':')).encode()).hexdigest()!=digest or manifest.get('plan_sha256')!=digest: raise RuntimeError('frozen plan validation failed')
    selected_arms=normalize_arms(plan.get('selected_arms'))
    if list(selected_arms)!=plan.get('selected_arms') or manifest.get('selected_arms')!=list(selected_arms) or manifest.get('excluded_arms')!=plan.get('excluded_arms'):
        raise RuntimeError('frozen arm-set binding failed')
    validate_not_run_evidence(outdir,plan.get('not_run_cells',[]))
    latest_check(selected_arms)
    current=apparatus_hash()
    if not hash_matches(manifest.get('apparatus_hash'),current): raise RuntimeError('apparatus hash differs from original run; refusing resume')
    checkdir=pathlib.Path(manifest.get('check_dir','')); report=json.loads((checkdir/'check.json').read_text()) if (checkdir/'check.json').is_file() else {}; checked=load_hash_record(checkdir)
    if report.get('passed') is not True or tuple(report.get('selected_arms',()))!=selected_arms or not hash_matches(checked,current): raise RuntimeError('original check/hash/arm set is no longer valid; refusing resume')
    allowed={cell_key(*x) for x in plan['cells']+plan['overhead_keys']}; validate_completions(outdir,allowed); return manifest

def execute_measure_run(runid):
    manifest=validate_run(runid); outdir=OUT/runid; plan=manifest['plan']
    try:
        run_cells([tuple(x) for x in plan['cells']],runid); overhead_rows=overhead(runid,plan); matrix=evidence_matrix(runid,plan['reps'],plan['selected_arms']); safe=finalize_safety(outdir)
        if not safe['pass']: raise RuntimeError('measurement final safety gates failed')
        report={'run_id':runid,'classification':manifest['kind'],'disposition':manifest['disposition'],'selected_arms':plan['selected_arms'],'excluded_arms':plan['excluded_arms'],'plan_sha256':plan['sha256'],'matrix':str(outdir/'MATRIX.md'),'overhead':str(outdir/'overhead.json'),'reps':plan['reps'],'consistency':all(x['consistency']=='consistent' for x in matrix),'status_by_arm':{a:{f:next(r['majority'] for r in matrix if r['arm']==a and r['fixture']==f) for f in FIXTURES} for a in ARMS},'overhead_successful':{a:{'warmups':v['successful_warmups'],'samples':v['successful_samples']} for a,v in overhead_rows.items()},'final_safety':safe}; (outdir/'run-summary.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n'); return report
    except BaseException as exc:
        safe=finalize_safety(outdir); append_jsonl(outdir/LEDGER_NAME,{'event':'measurement_failure','error':repr(exc),'final_safety':safe,'wall_time_ns':time.time_ns()}); raise

def resume_command(runid,arms=None):
    if arms is not None:
        run_dir=(OUT/runid).resolve()
        if not run_dir.is_relative_to(OUT.resolve()): raise RuntimeError('run path escapes OUT')
        manifest=json.loads((run_dir/'run.json').read_text())
        if normalize_arms(arms)!=tuple(manifest.get('selected_arms',())): raise RuntimeError('arm set differs from frozen run; refusing resume')
    report=execute_measure_run(runid); print(json.dumps(report,sort_keys=True,indent=2)); return 0

def rehearsal_command(runid):
    run_manifest=json.loads((OUT/runid/'run.json').read_text()); selected_arms=normalize_arms(run_manifest.get('selected_arms')); arm='z' if 'z' in selected_arms else selected_arms[0]
    script=str(pathlib.Path(__file__).resolve()); child=subprocess.Popen([sys.executable,'-I',script,'_measure_worker',runid],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True); ledger=OUT/runid/LEDGER_NAME; deadline=time.monotonic()+90; interrupted=False
    while time.monotonic()<deadline:
        events=ledger_state(ledger); target=next((e for e in reversed(events) if e.get('event')=='begin' and e.get('key')==cell_key(arm,'file_write_outside',0)),None)
        if target and target.get('marker'):
            rows,errs=scan_marker(target['marker'])
            if not errs and any(r['exe']==os.path.realpath(ROOT/'fx') for r in rows):
                os.kill(child.pid,signal.SIGKILL); child.wait(timeout=10); interrupted=True; break
        if child.poll() is not None: break
        time.sleep(.002)
    if not interrupted:
        if child.poll() is None: child.kill(); child.wait()
        raise RuntimeError('rehearsal failed to SIGKILL active outside-write executor')
    report=execute_measure_run(runid); report['interruption']=f'SIGKILL during active {arm}/file_write_outside; production resume completed'; report['classification']='REHEARSAL'; report['disposition']='DISCARDED'; print(json.dumps(report,sort_keys=True,indent=2)); shutil.rmtree(OUT/runid); base=BASE/runid
    if base.exists(): shutil.rmtree(base)
    return 0

def _measure_worker(runid):
    execute_measure_run(runid)

def measure_command(reps,rehearsal=False,resume=None,arms=None):
    if resume: return resume_command(resume,arms)
    if reps not in ((1,) if rehearsal else (3,)): raise RuntimeError('measured protocol requires --reps 3; rehearsal requires --reps 1 --rehearsal')
    selected_arms=normalize_arms(arms); runid=create_measure_run(reps,rehearsal,selected_arms)
    if rehearsal: return rehearsal_command(runid)
    report=execute_measure_run(runid); print(json.dumps(report,sort_keys=True,indent=2)); return 0

def dry_command(arm, fixture):
    runid='dry-'+uuid.uuid4().hex[:10]
    if fixture not in ('allowed_rw','noop'): run_cell(arm,'allowed_rw',0,runid)
    e=run_cell(arm,fixture,0,runid); safe=finalize_safety(OUT/runid); print(json.dumps({'evidence':e,'final_safety':safe},sort_keys=True,indent=2)); return 0 if not str(e.get('status','')).startswith('INVALID') and safe.get('pass') else 1

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='cmd',required=True); c=sub.add_parser('check'); c.add_argument('--arms',type=parse_arms_argument,default=None,metavar='z,b,c2,a,a-bash'); m=sub.add_parser('measure'); m.add_argument('--reps',type=int,default=3); m.add_argument('--rehearsal',action='store_true'); m.add_argument('--resume'); m.add_argument('--arms',type=parse_arms_argument,default=None,metavar='z,b,c2,a,a-bash'); r=sub.add_parser('resume'); r.add_argument('run_id'); r.add_argument('--arms',type=parse_arms_argument,default=None,metavar='z,b,c2,a,a-bash'); d=sub.add_parser('dry'); d.add_argument('--arm',choices=ARMS+('a-bash',),default='z'); d.add_argument('--fixture',choices=ALL_FIXTURES,default='allowed_rw'); w=sub.add_parser('_worker'); w.add_argument('run_id'); mw=sub.add_parser('_measure_worker'); mw.add_argument('run_id'); ac=sub.add_parser('_arm_a_client'); ac.add_argument('spec'); args=p.parse_args(argv)
    try:
        if args.cmd == 'check': return check_command(args.arms)
        if args.cmd=='measure': return measure_command(args.reps,args.rehearsal,args.resume,args.arms)
        if args.cmd=='resume': return resume_command(args.run_id,args.arms)
        if args.cmd == 'dry': return dry_command(args.arm, args.fixture)
        if args.cmd == '_worker':
            _worker(args.run_id); return 0
        if args.cmd=='_measure_worker': return _measure_worker(args.run_id)
        if args.cmd=='_arm_a_client': return arm_a_client(args.spec)
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr); return 2
    return 2
if __name__ == '__main__': raise SystemExit(main())
