#!/usr/bin/python3
# receipts.py — evidence from session turn_context, never from requested CLI flags.
import datetime
import json
import sys
from pathlib import Path
from validity import codex_home, events


def settings(row):
    p = row.get('payload') or row
    model = p.get('model')
    effort = p.get('effort') or p.get('reasoning_effort') or p.get('model_reasoning_effort')
    reasoning = p.get('reasoning')
    if isinstance(reasoning, dict):
        effort = effort or reasoning.get('effort')
    return model, effort


def contexts(paths):
    result = []; seen = {}
    for path in sorted(paths):
        active_id = None
        for row in events(path):
            payload = row.get('payload') or {}
            if row.get('type') == 'event_msg' and payload.get('type') == 'task_started':
                active_id = payload.get('turn_id')
            if row.get('type') != 'turn_context':
                continue
            p = row.get('payload') or {}; model, effort = settings(row)
            if not model and not effort:
                continue
            # A session can repeat context for one turn. Keep distinct settings
            # within that turn so a later context cannot conceal a mismatch.
            turn_id = p.get('turn_id') or active_id
            key = turn_id or row.get('timestamp') or ('row', len(result))
            if key in seen:
                result[seen[key]][1].add((model, effort))
            else:
                seen[key] = len(result); result.append((row.get('timestamp'), {(model, effort)}, turn_id))
    return result


def epoch(value):
    try:
        return datetime.datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()
    except (ValueError, AttributeError):
        return None


def collect(root):
    out = root / 'out'; out.mkdir(exist_ok=True); rows = []; flags = []
    for arm in (root / 'ARMS').read_text().split():
        d = out / arm
        turns = sorted(d.glob('turn-*.jsonl'), key=lambda p: int(p.stem.split('-')[-1]))
        thread = (d / 'thread').read_text().strip() if (d / 'thread').exists() else ''
        if not thread and turns:
            thread = next((e.get('thread_id', '') for e in events(turns[0]) if e.get('thread_id')), '')
        ctx = contexts((codex_home(root) / 'sessions').rglob('*%s*.jsonl' % thread)) if thread else []
        if not turns:
            flags.append('FLAG %s receipts no turn logs' % arm)
        for i, turn in enumerate(turns):
            used = set(); turn_events = list(events(turn))
            ids = {e.get('turn_id') for e in turn_events if e.get('turn_id')}
            ts = turn.with_suffix('.ts')
            times = [float(l.split('\t')[0]) for l in ts.read_text().splitlines() if l.strip()] if ts.exists() else []
            for timestamp, values, tid in ctx:
                when = epoch(timestamp)
                if ((ids and tid in ids) or (not ids and times and when is not None and
                                            min(times) <= when <= max(times))):
                    used.update(values)
            if not used and not ids and len(ctx) == len(turns):
                used = ctx[i][1]
            if not used:
                # Only explicit model/effort fields in JSON events are receipts.
                def walk(value):
                    if isinstance(value, dict):
                        model, effort = settings(value)
                        if model or effort:
                            used.add((model, effort))
                        if model and effort:
                            return
                        for child in value.values():
                            walk(child)
                    elif isinstance(value, list):
                        for child in value:
                            walk(child)
                for event in turn_events:
                    walk(event)
            models = ','.join(sorted({str(m or 'n/a (missing model receipt)') for m, _ in used})) or 'n/a (missing receipt)'
            efforts = ','.join(sorted({str(e or 'n/a (missing effort receipt)') for _, e in used})) or 'n/a (missing receipt)'
            n = turn.stem.split('-')[-1]; rows.append((arm, n, models, efforts))
            if used != {('gpt-6.1-sol', 'high')}:
                flags.append('FLAG %s turn-%s receipt model=%s effort=%s' % (arm, n, models, efforts))
    with (out / 'receipts.tsv').open('w') as f:
        f.write('arm\tturn\tmodel\teffort\n')
        for row in rows:
            f.write('\t'.join(row) + '\n')
    return flags


def main():
    root = Path(__file__).resolve().parent
    flags = collect(root)
    for flag in flags:
        print(flag)
    print('receipts done')
    return bool(flags)


if __name__ == '__main__':
    sys.exit(main())
