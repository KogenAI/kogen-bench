#!/usr/bin/env python3
"""Author-only <SERVER_ID>. All builds/checks/tests enter the grade sandbox."""
import json
import ctypes
import os
import re
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path('<ROOT>')
ENV = {**os.environ, 'HOME': '/tmp/bench-home', 'PYTHONDONTWRITEBYTECODE': '1',
       'PATH': '/benchmark-root/toolchains/go-1.27.1/bin:/benchmark-root/toolchains/rust-1.97.1/bin:/benchmark-root/toolchains/bun-1.4.2/bin:/benchmark-root/toolchains/gleam-1.18.1/bin:/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:/opt/bench/mise/installs/erlang/29.0.3/bin:/opt/bench/mise/installs/node/24.20.0/bin:/opt/bench/mise/installs/ruby/3.4.8/bin:/benchmark-root/toolchains/python-3.14.7/bin:/usr/bin:/bin',
       'PYTHONPATH': '/benchmark-root/toolchains/python-3.14.7/lib/python3.14/site-packages',
       'RUSTUP_HOME': '/opt/bench/rustup', 'CARGO_NET_OFFLINE': 'true',
       'GOTOOLCHAIN': 'local', 'GOPROXY': 'off'}
PROFILE = '/benchmark-root/kits/current/reproduce/sandbox-profile.sh'
LOG = ROOT / 'author-logs'
LOG.mkdir(exist_ok=True)
assert ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) == 0
burners = []

def <SERVER_ID>(root):
    found = set()
    pending = [root]
    while pending:
        pid = pending.pop()
        for thread in Path(f'/proc/{pid}/task').glob('*'):
            try:
                for child in map(int, (thread / 'children').read_text().split()):
                    if child not in found:
                        found.add(child)
                        pending.append(child)
            except FileNotFoundError:
                pass
    return found

def process_gate():
    # bwrap also has helper descendants. Adopt, kill and reap them before the
    # final gate, with the same three-second window as the suite runner.
    end = time.monotonic() + 3
    while True:
        pids = <SERVER_ID>(os.getpid()) - {p.pid for p in burners}
        for pid in pids:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        for pid in pids:
            try:
                os.waitpid(pid, os.WNOHANG)
            except ChildProcessError:
                pass
        remaining = <SERVER_ID>(os.getpid()) - {p.pid for p in burners}
        if not remaining:
            return {'leftovers': 0, 'zombies': 0, 'cleanup_rc': 0}
        assert time.monotonic() < end, sorted(remaining)
        time.sleep(.01)

def sandbox(work, task, args, label):
    start = time.monotonic()
    p = subprocess.run([PROFILE, 'grade', str(work), str(task), '--', *args],
                       env=ENV, capture_output=True, text=True, timeout=600)
    elapsed = time.monotonic() - start
    (LOG / (label + '.log')).write_text(p.stdout + '\n--- stderr ---\n' + p.stderr)
    gate = process_gate()
    (LOG / (label + '-cleanup.json')).write_text(json.dumps(gate) + '\n')
    return p, elapsed

def verdict(p):
    lines = [line for line in p.stdout.splitlines() if line.startswith('{')]
    return json.loads(lines[-1]) if lines else {'stage': 'infrastructure'}


def emit(record):
    records.append(record)
    print(json.dumps(record), flush=True)
    (ROOT / 'validation-counts.json').write_text(json.dumps({
        'host': 'eu', 'records': records,
        'total_seconds': round(time.monotonic() - began, 3)}, indent=2) + '\n')


mode = sys.argv[1]
langs = sys.argv[2:] or ['rust', 'go', 'ts-bun']
records = []
began = time.monotonic()
for lang in langs:
    task = ROOT / ('taskdir-' + lang)
    task.mkdir(exist_ok=True)
    if (task / 'hidden').exists():
        shutil.rmtree(task / 'hidden')
    shutil.copytree(ROOT / 'hidden', task / 'hidden')
    shutil.copy2(ROOT / 'author-cleanup-check.py', task / 'author-cleanup-check.py')
    shutil.copy2(ROOT / 'author-contract-check.py', task / 'author-contract-check.py')
    for variant in ['bases', 'reference']:
        work = ROOT / variant / lang
        if mode == 'format':
            cmds = {'rust': 'make setup && cargo fmt', 'go': 'gofmt -w .',
                    'ts-bun': 'make setup && bun ./node_modules/@biomejs/biome/bin/biome check --write .'}
            p, elapsed = sandbox(work, task, ['/bin/sh', '-c', cmds[lang]], f'format-{variant}-{lang}')
            print(json.dumps({'variant': variant, 'lang': lang, 'format_rc': p.returncode}), flush=True)
        elif mode == 'validate':
            p, elapsed = sandbox(work, task, ['/bin/bash', '/task/grader-entrypoint', '/work'], f'grade-{variant}-{lang}')
            record = verdict(p)
            record.update(variant=variant, lang=lang, grader_rc=p.returncode,
                          grade_seconds=round(elapsed, 3), check_rc=0 if record['stage']=='suite' else None,
                          **process_gate())
            assert 'C4_CLEANUP {"leftovers": 0, "zombies": 0}' in p.stderr
            timing = re.search(r'Ran 29 tests in ([0-9.]+)s', p.stderr)
            assert timing is not None, record
            record['suite_seconds'] = float(timing.group(1))
            emit(record)
            assert p.returncode == 0 and record['stage'] == 'suite', record
            assert record['tests'] == 29 and record['errors'] == record['skipped'] == 0, record
            assert record['failures'] == (29 if variant == 'bases' else 0), record

if mode in ['validate', 'regressions']:
    import hashlib
    import signal
    canary = (ROOT / 'hidden/CANARY.txt').read_text().splitlines()[-1]
    files = sorted(p for p in (ROOT / 'hidden').rglob('*') if p.is_file())
    assert len(files) == 4
    assert all(canary in p.read_text() for p in files)
    assert ('# ' + canary) in (ROOT / 'grader-entrypoint').read_text().splitlines()
    emit({'canary_files': len(files), 'grade_canary_rc': 0, 'rc': 0})
    p, elapsed = sandbox(ROOT / 'reference/rust', ROOT / 'taskdir-rust',
                         ['python3', '/task/author-cleanup-check.py'], 'cleanup-check')
    cleanup = verdict(p)
    assert p.returncode == 0 and cleanup['cleanup_tests'] == 21, cleanup
    cleanup.update(process_gate())
    emit(cleanup)
    p, elapsed = sandbox(ROOT / 'reference/rust', ROOT / 'taskdir-rust',
                         ['python3', '/task/author-contract-check.py'], 'contract-check')
    contract = verdict(p)
    assert p.returncode == 0 and contract['contract_tests'] == 38 and contract['internal_alternates_tests'] == 1, contract
    contract.update(process_gate())
    emit(contract)
    if mode == 'regressions':
        sys.exit(0)

    def interrupted(signum, frame):
        raise RuntimeError('validation guard interrupted')

    signal.signal(signal.SIGTERM, interrupted)
    cores = len(os.sched_getaffinity(0))
    burners = []
    try:
        for _ in range(cores):
            burners.append(subprocess.Popen(['yes'], stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL))
        for lang in langs:
            for run in range(1, 6):
                assert all(p.poll() is None for p in burners)
                p, elapsed = sandbox(ROOT / 'reference' / lang, ROOT / ('taskdir-' + lang),
                                     ['python3', '/task/hidden/suite/run.py', '/work/bin/app'],
                                     f'loaded-{lang}-{run}')
                record = verdict(p)
                record.update(variant='reference', lang=lang, run=run, loaded=True,
                              cpu_burners=cores, grader_rc=p.returncode,
                              suite_seconds=round(elapsed, 3), **process_gate())
                assert 'C4_CLEANUP {"leftovers": 0, "zombies": 0}' in p.stderr
                emit(record)
                assert all(p.poll() is None for p in burners)
                assert p.returncode == 0 and record['pass_'] and record['tests'] == 29, record
                assert record['failures'] == record['errors'] == record['skipped'] == 0, record
    finally:
        for burner in burners:
            burner.terminate()
        for burner in burners:
            burner.wait(timeout=3)
    emit({'cpu_burners': cores, 'burners_reaped': len(burners), 'rc': 0, **process_gate()})
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in files + sorted(ROOT.glob('prompt-*.md')) + [ROOT / 'SPEC.md']}
    (ROOT / 'host-hashes.json').write_text(json.dumps(hashes, indent=2, sort_keys=True) + '\n')
