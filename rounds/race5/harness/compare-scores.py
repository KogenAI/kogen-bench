#!/usr/bin/python3
"""Publish per-snapshot flip disclosures and the combined official scores."""
import json
from collections import defaultdict
from pathlib import Path
from combined_score import cases, combine


def compare(root):
    out = root / 'out'; differences = []; flaky = defaultdict(set)
    # Complete/validate combined artifacts even when replaying cached raw runs.
    raw = {}
    for line in (out / 'scores-official.tsv').read_text().splitlines():
        fields = line.split('\t'); raw[tuple(fields[:2])] = fields
    for label, arm in raw:
        combine(root, label, arm)
        receipt = json.loads((out / f'results/{label}-{arm}-score.json').read_text())
        if receipt['double_scored']:
            one = cases(out / f'results/{label}-{arm}-official.jsonl')
            two = cases(out / f'results/{label}-{arm}-repeat.jsonl')
            for cid in sorted(one):
                if one[cid] != two[cid]:
                    flaky[arm].add(cid)
                    differences.append((label, arm, cid, one[cid], two[cid]))
    with (out / 'flaky.tsv').open('w') as stream:
        stream.write('snapshot\tarm\tcase\tfirst\tsecond\n')
        for row in differences:
            stream.write('\t'.join(row) + '\n')
    (out / 'flaky-by-arm.json').write_text(json.dumps({arm: sorted(ids) for arm, ids in flaky.items()}, indent=2) + '\n')
    combined = {}
    for line in (out / 'scores-combined.tsv').read_text().splitlines():
        combined[tuple(line.split('\t')[:2])] = line
    (out / 'scores.tsv').write_text(''.join(line + '\n' for line in combined.values()))


if __name__ == '__main__':
    compare(Path(__file__).resolve().parent)
