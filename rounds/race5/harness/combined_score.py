#!/usr/bin/env python3
"""Publish the per-snapshot, per-arm intersection of the required raw scorings."""
import json
from pathlib import Path
import sys
from scoring_config import counts, inventory, scored_ids


def cases(path):
    result = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict) or not row.get('id'):
            continue
        if row['id'] in result or row.get('status') not in ('pass', 'fail', 'error', 'blocked'):
            raise ValueError(f'invalid duplicate/status in {path}')
        result[row['id']] = row['status']
    return result


def combine(root, label, arm):
    root = Path(root); out = root / 'out'
    values, bugs = counts(root)
    expected = set(inventory(root) if label == 'FINAL' else scored_ids(root))
    first = cases(out / f'results/{label}-{arm}-official.jsonl')
    if set(first) != expected:
        raise ValueError('first scorer inventory differs from frozen selection')
    first_passes = {cid for cid, status in first.items() if status == 'pass'}
    first_count = len(first_passes - bugs)
    near = values['target'] - 3 <= first_count <= values['target'] + 3
    second = None
    if near:
        second = cases(out / f'results/{label}-{arm}-repeat.jsonl')
        if set(second) != expected:
            raise ValueError('second scorer inventory differs from frozen selection')
        passed = first_passes & {cid for cid, status in second.items() if status == 'pass'}
    else:
        passed = first_passes
    combined = len(passed - bugs)
    rows = []
    for cid in sorted(expected):
        row = {'id': cid, 'status': ('pass' if cid in passed else 'fail') if near else first[cid],
               'first_status': first[cid]}
        if near:
            row['second_status'] = second[cid]
        rows.append(row)
    path = out / f'results/{label}-{arm}-combined.jsonl'
    temporary = path.with_suffix('.tmp')
    temporary.write_text(''.join(json.dumps(row) + '\n' for row in rows))
    temporary.replace(path)
    raw = [line.split('\t') for line in (out / 'scores-official.tsv').read_text().splitlines()
           if line.split('\t')[:2] == [label, arm]]
    if not raw:
        raise ValueError('missing raw first score row')
    fields = raw[-1]
    if int(fields[3].split()[1].split('/')[0]) != first_count:
        raise ValueError('raw first score count differs from its per-case results')
    fields[2] = f'{len(passed)}/{values["N_total"]}' if label == 'FINAL' else f'n/a/{values["N_total"]}'
    fields[3] = f'excl {combined}/{values["N_scored"]}'
    fields[5] = 'combined'
    line = '\t'.join(fields)
    destination = out / 'scores-combined.tsv'
    old = [row for row in destination.read_text().splitlines() if row.split('\t')[:2] == [label, arm]] if destination.exists() else []
    if not old or old[-1] != line:
        with destination.open('a') as stream:
            stream.write(line + '\n')
    receipt = {'snapshot': label, 'arm': arm, 'target': values['target'],
               'first_scored': first_count,
               'second_scored': len({cid for cid, status in second.items() if status == 'pass'} - bugs) if near else None,
               'combined_scored': combined, 'N_scored': values['N_scored'], 'double_scored': near,
               'combined_total': len(passed) if label == 'FINAL' else None}
    (out / f'results/{label}-{arm}-score.json').write_text(json.dumps(receipt, indent=2) + '\n')
    return combined


if __name__ == '__main__':
    print(combine(Path(sys.argv[1]), sys.argv[2], sys.argv[3]))
