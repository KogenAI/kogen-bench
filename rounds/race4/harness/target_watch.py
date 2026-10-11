#!/usr/bin/env python3
"""Stop an arm only on a complete, valid result inventory at the target."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
from scoring_config import counts, scored_ids
from tokens_at import TOKEN_FIELDS, usage_at


def result_path(root, arm):
    text = (root / f'BRIEF-{arm}.md').read_text()
    paths = re.findall(r'--out\s+([^\s`]+)', text)
    if len(paths) != 1:
        raise ValueError('brief must give exactly one conformance --out path')
    return Path(paths[0])


def poll(root, arm, expected, values):
    path = result_path(root, arm)
    try:
        if path.stat().st_mtime < float((root / 'START').read_text()):
            return False
        data = path.read_bytes()
        rows = [json.loads(line) for line in data.splitlines() if line.strip()]
        rows = [row for row in rows if isinstance(row, dict) and row.get('id')]
        ids = [row['id'] for row in rows]
        if len(ids) != len(set(ids)) or not expected <= set(ids):
            return False
        if any(row.get('status') not in ('pass', 'fail', 'error', 'blocked') for row in rows):
            return False
        passes = sum(row['id'] in expected and row['status'] == 'pass' for row in rows)
    except (OSError, ValueError, TypeError, KeyError):
        return False
    if passes < values['target']:
        return False
    epoch = int(time.time())
    (root / f'out/target-results-{arm}.jsonl').write_bytes(data)
    subprocess.run([str(root / 'snap.sh'), f'TARGET-{arm}', arm], check=True)
    (root / f'STOP-{arm}').touch()
    token_usage = usage_at(root, arm)
    token_fields = '\t'.join(str(token_usage[key]) if token_usage[key] is not None else 'n/a' for key in TOKEN_FIELDS)
    utc = datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    with (root / 'out/target-stops.tsv').open('a') as stream:
        stream.write(f"{arm}\t{epoch}\t{utc}\t{passes}/{values['N_scored']}\t{hashlib.sha256(data).hexdigest()}\t{token_fields}\n")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('arm')
    parser.add_argument('--once', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.arm not in (root / 'ARMS').read_text().split():
        parser.error('unknown arm')
    values, _ = counts(root)
    expected = set(scored_ids(root))
    (root / 'out').mkdir(exist_ok=True)
    while not any((root / name).exists() for name in ('STOP', 'DONE', f'STOP-{args.arm}')):
        if time.time() >= float((root / 'DEADLINE').read_text()):
            break
        if poll(root, args.arm, expected, values) or args.once:
            break
        time.sleep(10)


if __name__ == '__main__':
    main()
