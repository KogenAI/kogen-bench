#!/usr/bin/env python3
"""Private host-only validation. Every build/check is inside the official profile."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path('<ROOT>')
ENV = {**os.environ, 'HOME': '/tmp/bench-home', 'PYTHONDONTWRITEBYTECODE': '1',
       'PATH': '/benchmark-root/toolchains/go-1.27.1/bin:/benchmark-root/toolchains/rust-1.97.1/bin:/benchmark-root/toolchains/bun-1.4.2/bin:/benchmark-root/toolchains/gleam-1.18.1/bin:/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:/opt/bench/mise/installs/erlang/29.0.3/bin:/opt/bench/mise/installs/node/24.20.0/bin:/opt/bench/mise/installs/ruby/3.4.8/bin:/benchmark-root/toolchains/python-3.14.7/bin:/usr/bin:/bin',
       'PYTHONPATH': '/benchmark-root/toolchains/python-3.14.7/lib/python3.14/site-packages',
       'RUSTUP_HOME': '/opt/bench/rustup', 'CARGO_NET_OFFLINE': 'true',
       'GOTOOLCHAIN': 'local', 'GOPROXY': 'off'}
PROFILE = '/benchmark-root/kits/current/reproduce/sandbox-profile.sh'


def run(lang, variant, iteration):
    task = ROOT / f'taskdir-{lang}'
    task.mkdir(exist_ok=True)
    shutil.copytree(ROOT / 'hidden', task / 'hidden', dirs_exist_ok=True)
    work = ROOT / f'work-{variant}-{lang}-{iteration}'
    if work.exists() or (ROOT / 'validation-logs' / f'{variant}-{lang}-{iteration}.log').exists():
        raise RuntimeError('attempt already exists; choose unused iteration IDs')
    shutil.copytree(ROOT / ('bases' if variant == 'base' else 'reference') / lang, work,
                    ignore=shutil.ignore_patterns('.git', 'target', 'bin', '.cache', 'node_modules'))
    # The template's offline setup is preparatory copying only, not a build/check.
    if lang == 'ts-bun':
        template = Path('/benchmark-root/toolchains/bun-1.4.2/node-template')
        shutil.copytree(template / 'node_modules', work / 'node_modules', symlinks=True)
        if (template / 'bun.lock').exists():
            shutil.copyfile(template / 'bun.lock', work / 'bun.lock')
    start = time.monotonic()
    proc = subprocess.run([PROFILE, 'grade', str(work), str(task), '--',
                           '/bin/sh', '/task/grader-entrypoint', '/work'],
                          env=ENV, capture_output=True, text=True, timeout=1200)
    duration = round(time.monotonic() - start, 3)
    logs = ROOT / 'validation-logs'
    logs.mkdir(exist_ok=True)
    (logs / f'{variant}-{lang}-{iteration}.log').write_text(proc.stdout + '\n' + proc.stderr)
    records = []
    for line in (proc.stdout + '\n' + proc.stderr).splitlines():
        try:
            records.append(json.loads(line))
        except ValueError:
            pass
    summary = next((r for r in reversed(records) if 'pass_' in r), None)
    stages = [r for r in records if 'stage_rc' in r]
    clean = [r for r in records if 'leftovers' in r]
    suite_seconds = next((r['suite_seconds'] for r in records if 'suite_seconds' in r), None)
    result = {'lang': lang, 'variant': variant, 'iteration': iteration,
              'sandbox_rc': proc.returncode, 'seconds': duration, 'suite_seconds': suite_seconds, 'summary': summary,
              'stage_rcs': [r['stage_rc'] for r in stages],
              'leftovers': max((r['leftovers'] for r in clean), default=-1),
              'zombies': max((r['zombies'] for r in clean), default=-1),
              'before_leftovers': max((r.get('before_leftovers', 0) for r in records), default=-1),
              'before_zombies': max((r.get('before_zombies', 0) for r in records), default=-1),
              'app_survivors': max((r.get('app_survivors', 0) for r in records), default=-1)}
    print(json.dumps(result), flush=True)
    with (ROOT / 'validation-counts.jsonl').open('a') as stream:
        stream.write(json.dumps(result) + '\n')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', choices=('rust', 'go', 'ts-bun'), required=True)
    parser.add_argument('--variant', choices=('base', 'reference'), required=True)
    parser.add_argument('--runs', type=int, default=1)
    parser.add_argument('--start', type=int, default=1)
    args = parser.parse_args()
    for i in range(args.start, args.start + args.runs):
        run(args.lang, args.variant, i)


if __name__ == '__main__':
    main()
