#!/usr/bin/env python3
"""Time build/test tools without storing command text or changing arguments."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid

def emit(path, value):
    fd = os.open(str(path), os.O_CREAT | os.O_APPEND | os.O_WRONLY, 0o600)
    try:
        os.write(fd, (json.dumps(value) + '\n').encode())
    finally:
        os.close(fd)

def main():
    tool, real, *arguments = sys.argv[1:]
    category = 'test' if arguments and arguments[0] == 'test' else (
        'build' if arguments and arguments[0] in ('build', 'compile') else None)
    log = Path(__file__).resolve().parent.parent / '.kitcache/build-test-times.jsonl'
    identity, started = uuid.uuid4().hex, time.monotonic()
    if category:
        emit(log, dict(id=identity, phase=os.environ.get('ARCH_PHASE'), category=category,
                       event='start', at=started, tool=tool))
    # The wrapper runs inside the arm workspace; make that inherited cwd
    # explicit so the mise shim loads the arm's pinned mise.toml.
    code = subprocess.call([real, *arguments], cwd=os.getcwd())
    if category:
        emit(log, dict(id=identity, phase=os.environ.get('ARCH_PHASE'), category=category,
                       event='end', at=time.monotonic(), exit_code=code, tool=tool))
    return code

def collect(path, phase, deadline):
    starts, ends = {}, {}
    if Path(path).is_file():
        for line in Path(path).read_text().splitlines():
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if row.get('phase') == phase and row.get('at', deadline + 1) <= deadline:
                (starts if row.get('event') == 'start' else ends)[row['id']] = row
    by_category = {'build': 0., 'test': 0.}
    for identity, row in starts.items():
        end = ends.get(identity, {}).get('at', deadline)
        by_category[row['category']] += max(0, end - row['at'])
    return dict(by_category=by_category, total_seconds=sum(by_category.values()),
                observed_invocations=len(starts), incomplete_at_kill=sum(k not in ends for k in starts),
                method='sum of wrapped go build/test and mix compile/test wall times; overlapping commands count separately; unfinished commands stop at phase cutoff')

if __name__ == '__main__':
    raise SystemExit(main())
