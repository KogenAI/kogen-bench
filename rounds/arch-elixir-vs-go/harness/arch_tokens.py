#!/usr/bin/env python3
"""Race 6 extraction: last cumulative rollout token event at phase kill (inclusive)."""
from datetime import datetime
from pathlib import Path
import argparse
import json
import re
from arch_config import TOKEN_KEYS, dump

STARTED = re.compile(r'^\s*\{\s*"type"\s*:\s*"thread.started"\s*[,}]')
METADATA = re.compile(r'(?<!\\)"type"\s*:\s*"session_meta"')
TOKEN = re.compile(r'(?<!\\)"type"\s*:\s*"token_count"')

def timestamp(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Token timestamp must have a timezone')
    return parsed

def ids_from_turns(turns):
    ids = set()
    for path in turns:
        with Path(path).open() as stream:
            for line in stream:
                if STARTED.match(line):
                    ids.add(json.loads(line)['thread_id'])
    if not ids:
        raise ValueError('Missing thread.started IDs')
    return ids

def thread_usage(thread_id, sessions, cwd, cutoff):
    paths = list(Path(sessions).rglob('*' + thread_id + '*.jsonl'))
    if len(paths) != 1:
        raise ValueError('Expected exactly one rollout for ' + thread_id)
    meta, selected, previous = None, None, None
    eligible, later = 0, 0
    with paths[0].open() as stream:
        for line in stream:
            # Do not decode or retain transcript text or tool output.
            if METADATA.search(line):
                event = json.loads(line)
                if event.get('type') != 'session_meta':
                    continue
                payload = event['payload']
                meta = {key: payload.get(key) for key in ('id', 'cwd')}
            elif TOKEN.search(line):
                event = json.loads(line)
                payload = event.get('payload') or {}
                if event.get('type') != 'event_msg' or payload.get('type') != 'token_count':
                    continue
                usage = (payload.get('info') or {}).get('total_token_usage')
                if usage is None:
                    continue
                at = timestamp(event['timestamp'])
                if previous is not None and at < previous:
                    raise ValueError('Non-monotonic token timestamps')
                previous = at
                if at > cutoff:
                    later += 1
                    continue
                eligible += 1
                selected = {'last_token_event_ts': event['timestamp'],
                            'usage': {key: usage[key] for key in TOKEN_KEYS}}
    if meta != {'id': thread_id, 'cwd': str(Path(cwd).resolve())}:
        raise ValueError('Rollout metadata id/cwd mismatch')
    if selected is None:
        raise ValueError('No eligible cumulative token event')
    usage = selected['usage']
    if not all(type(value) is int and value >= 0 for value in usage.values()):
        raise ValueError('Invalid token count')
    if (usage['total_tokens'] != usage['input_tokens'] + usage['output_tokens'] or
            usage['cached_input_tokens'] > usage['input_tokens'] or
            usage['reasoning_output_tokens'] > usage['output_tokens']):
        raise ValueError('Token accounting identities fail')
    return dict(thread_id=thread_id, cwd=meta['cwd'], eligible_token_events=eligible,
                later_token_events=later, **selected)

def collect_phase(turns, sessions, cwd, kill_utc):
    cutoff = timestamp(kill_utc)
    threads = [thread_usage(thread_id, sessions, cwd, cutoff)
               for thread_id in sorted(ids_from_turns(turns))]
    return dict(kill_utc=kill_utc, n_threads=len(threads), threads=threads,
                usage={key: sum(row['usage'][key] for row in threads) for key in TOKEN_KEYS},
                method='last cumulative total_token_usage per deduplicated thread at/before phase kill; no tail estimate')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run', type=Path, required=True)
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    rows = []
    for path in sorted((args.run / 'out').glob('arch-*/phase-*/PHASE.json')):
        phase = json.loads(path.read_text())
        tokens = collect_phase(sorted(path.parent.glob('turn-*.jsonl')), phase['sessions'],
                               phase['cwd'], phase['kill_utc'])
        rows.append(dict(arm=phase['arm'], phase=phase['phase'], **tokens))
    if not rows:
        raise ValueError('No completed phases')
    # Maintenance must be a fresh thread; summing a resumed build would double-count.
    seen = set()
    for row in rows:
        current = {t['thread_id'] for t in row['threads']}
        if seen & current:
            raise ValueError('A thread was reused across arms or phases')
        seen |= current
    result = dict(schema=1, phases=rows)
    dump(args.out or args.run / 'out/tokens.json', result)
    print('Collected cumulative usage for ' + str(len(rows)) + ' phases')

if __name__ == '__main__':
    main()
