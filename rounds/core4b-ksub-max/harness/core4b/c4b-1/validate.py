#!/usr/bin/env python3
"""Private eu-only validation. Stores raw logs locally; emits counts and rc only."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path('<ROOT>')
PROFILE = '/benchmark-root/kits/current/reproduce/sandbox-profile.sh'
ENV = {**os.environ, 'HOME': '/tmp/bench-home', 'PYTHONDONTWRITEBYTECODE': '1',
       'PATH': '/benchmark-root/toolchains/go-1.27.1/bin:'
               '/benchmark-root/toolchains/rust-1.97.1/bin:'
               '/benchmark-root/toolchains/bun-1.4.2/bin:'
               '/benchmark-root/toolchains/gleam-1.18.1/bin:'
               '/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:'
               '/opt/bench/mise/installs/erlang/29.0.3/bin:'
               '/opt/bench/mise/installs/node/24.20.0/bin:'
               '/opt/bench/mise/installs/ruby/3.4.8/bin:'
               '/benchmark-root/toolchains/python-3.14.7/bin:/usr/bin:/bin',
       'PYTHONPATH': '/benchmark-root/toolchains/python-3.14.7/lib/python3.14/site-packages',
       'RUSTUP_HOME': '/opt/bench/rustup', 'CARGO_NET_OFFLINE': 'true',
       'GOTOOLCHAIN': 'local', 'GOPROXY': 'off', 'SUITE_DIAGNOSTICS': '1'}


def run(lang, variant, tag, reuse=None):
    source = ROOT / ('bases' if variant == 'base' else 'reference') / lang
    first = None
    work = ROOT / 'validation-work' / f'{lang}-{variant}-{reuse or tag}'
    if reuse is None:
        if work.exists():
            raise RuntimeError('attempt exists; choose a new tag')
        shutil.copytree(source, work, ignore=shutil.ignore_patterns('.git', 'target', '.cache', 'bin', 'node_modules'))
    else:
        first = json.loads((ROOT / 'validation-logs' / f'{lang}-{variant}-{reuse}.json').read_text())
        if not first['verdict']['pass_'] or first['checks'] != {'build_rc': 0, 'check_rc': 0}:
            raise RuntimeError('reuse requires passing build/check/suite')
        if hashlib.sha256((work / 'bin/app').read_bytes()).hexdigest() != first['binary_sha256']:
            raise RuntimeError('validated binary changed')
    task = ROOT / f'taskdir-{lang}'
    task.mkdir(parents=True, exist_ok=True)
    if (task / 'hidden').exists():
        history = ROOT / 'validation-mount-history' / f'{lang}-{variant}-{tag}'
        history.mkdir(parents=True, exist_ok=False)
        (task / 'hidden').rename(history / 'hidden')
    shutil.copytree(ROOT / 'hidden', task / 'hidden')
    logs = ROOT / 'validation-logs'
    logs.mkdir(exist_ok=True, mode=0o700)
    start = time.monotonic()
    suite_files = {str(p.relative_to(task / 'hidden')): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in sorted((task / 'hidden').rglob('*')) if p.is_file()}
    hidden_digest = hashlib.sha256(json.dumps(suite_files, sort_keys=True).encode()).hexdigest()
    if first is not None and hidden_digest != first['hidden_sha256']:
        raise RuntimeError('validated suite changed')
    command = (['/bin/bash', '/task/grader-entrypoint', '/work'] if reuse is None else
               ['python3', '/task/hidden/suite/suite.py', '/work/bin/app'])
    p = subprocess.run([PROFILE, 'grade', str(work), str(task), '--', *command],
                       capture_output=True, env=ENV, timeout=1200)
    stem = f'{lang}-{variant}-{tag}'
    (logs / (stem + '.log')).write_bytes(p.stdout + b'\n--- stderr ---\n' + p.stderr)
    records = []
    for line in p.stdout.splitlines():
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                records.append(obj)
        except ValueError:
            pass
    verdict = next((x for x in reversed(records) if 'pass_' in x), None)
    validation = next((x['validation'] for x in reversed(records) if 'validation' in x), None)
    cleanup = next((x['cleanup'] for x in reversed(records) if 'cleanup' in x), None)
    runtime = next((x['runtime_ms'] for x in reversed(records) if 'runtime_ms' in x), None)
    if first is not None:
        validation = first['checks']
    result = {'lang': lang, 'variant': variant, 'tag': tag, 'sandbox_rc': p.returncode,
              'checks': validation, 'verdict': verdict, 'cleanup': cleanup,
              'suite_runtime_ms': runtime,
              'total_runtime_ms': round((time.monotonic() - start) * 1000),
              'reused_build': reuse, 'hidden_sha256': hidden_digest,
              'hidden_files': suite_files,
              'binary_sha256': hashlib.sha256((work / 'bin/app').read_bytes()).hexdigest()
                               if (work / 'bin/app').is_file() else None}
    (logs / (stem + '.json')).write_text(json.dumps(result, sort_keys=True) + '\n')
    print(json.dumps(result), flush=True)
    expected = verdict is not None and verdict['stage'] == 'suite' and validation == {'build_rc': 0, 'check_rc': 0}
    if expected:
        expected = verdict['pass_'] if variant == 'reference' else not verdict['pass_']
    return p.returncode or (0 if expected else 1)


if __name__ == '__main__':
    raise SystemExit(run(*sys.argv[1:]))
