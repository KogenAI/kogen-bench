#!/usr/bin/env python3
"""Print cumulative input/cached/output/reasoning/total tokens at a UTC instant.

Usage: tokens-at.py RACE_DIR ARM UTC_ISO_TIME
Self-contained for use with both race 3 and race 4 directories. Missing receipts
print n/a in each unavailable field; no cumulative usage is invented.
"""
import argparse
import datetime
import json
from pathlib import Path
import re

TOKEN_FIELDS = ('input_tokens', 'cached_input_tokens', 'output_tokens',
                'reasoning_output_tokens', 'total_tokens')
UTC = datetime.timezone.utc


def parse_time(value):
    when = datetime.datetime.fromisoformat(value.strip().replace('Z', '+00:00'))
    if when.tzinfo is None:
        when = when.replace(tzinfo=UTC)
    return when.astimezone(UTC)


def thread_id(root, arm):
    directory = Path(root) / 'out' / arm
    try:
        value = (directory / 'thread').read_text().strip()
    except OSError:
        value = ''
    if not value:
        try:
            with (directory / 'turn-0.jsonl').open(errors='replace') as stream:
                for line in stream:
                    try:
                        row = json.loads(line)
                    except (ValueError, TypeError):
                        continue
                    if isinstance(row, dict) and isinstance(row.get('thread_id'), str) and row['thread_id']:
                        value = row['thread_id']
                        break
        except OSError:
            pass
    # Thread IDs must not expand a glob beyond the requested session.
    return value if re.fullmatch(r'[A-Za-z0-9_-]+', value) else ''


def usage_at(root, arm, utc_time=None):
    """Latest valid cumulative receipt; optionally restrict to timestamp <= cutoff."""
    root = Path(root)
    usage = dict.fromkeys(TOKEN_FIELDS)
    cutoff = parse_time(utc_time) if utc_time is not None else None
    tid = thread_id(root, arm)
    if not tid:
        return usage
    try:
        home = Path((root / 'CODEX_HOME').read_text().strip()).expanduser()
        if not str(home) or str(home) == '.':
            return usage
    except OSError:
        return usage
    if not home.is_absolute():
        home = root / home
    # Only the identified thread's rollouts; never auth/config or other sessions.
    for path in sorted((home / 'sessions').glob(f'*/*/*/rollout-*{tid}*.jsonl')):
        try:
            with path.open(errors='replace') as stream:
                for line in stream:
                    try:
                        row = json.loads(line)
                    except (ValueError, TypeError):
                        continue  # a live rollout can end with an unfinished JSON line
                    if not isinstance(row, dict) or row.get('type') != 'event_msg':
                        continue
                    payload = row.get('payload')
                    if not isinstance(payload, dict) or payload.get('type') != 'token_count':
                        continue
                    info = payload.get('info')
                    total = info.get('total_token_usage') if isinstance(info, dict) else None
                    if not isinstance(total, dict):
                        continue
                    if cutoff is not None:
                        try:
                            timestamp = parse_time(row['timestamp'])
                        except (KeyError, ValueError, TypeError, AttributeError):
                            continue
                        if timestamp > cutoff:
                            continue
                    usage = {key: total[key] if type(total.get(key)) is int and total[key] >= 0 else None
                             for key in TOKEN_FIELDS}
        except OSError:
            continue
    return usage


def snapshot_time(root, label):
    """Full ISO TAKEN_AT; fall back to TAKEN_EPOCH for older time-only snapshots."""
    directory = Path(root) / 'snapshots' / label
    try:
        taken = (directory / 'TAKEN_AT').read_text().strip()
        if 'T' in taken or ' ' in taken:
            return parse_time(taken).isoformat().replace('+00:00', 'Z')
    except (OSError, ValueError, TypeError):
        pass
    try:
        epoch = float((directory / 'TAKEN_EPOCH').read_text())
        return datetime.datetime.fromtimestamp(epoch, UTC).isoformat().replace('+00:00', 'Z')
    except (OSError, ValueError, OverflowError):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('race_dir', type=Path)
    parser.add_argument('arm')
    parser.add_argument('utc_iso_time')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.arm):
        parser.error('invalid arm name')
    try:
        usage = usage_at(args.race_dir, args.arm, args.utc_iso_time)
    except (ValueError, TypeError):
        parser.error('UTC_ISO_TIME must be an ISO timestamp')
    print(' '.join(str(usage[key]) if usage[key] is not None else 'n/a' for key in TOKEN_FIELDS))


if __name__ == '__main__':
    main()
