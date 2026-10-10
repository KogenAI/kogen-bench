#!/usr/bin/python3
"""Compare repeated snapshots; flakiness affects only the arm that exhibited it."""
import json
from collections import defaultdict
from pathlib import Path
from scoring_config import counts


def cases(path):
    result = {}
    for line in path.read_text().splitlines():
        row = json.loads(line)
        if row.get('id'):
            if row['id'] in result:
                raise ValueError(f'duplicate case: {path}: {row["id"]}')
            result[row['id']] = row['status']
    if not result:
        raise ValueError(f'no case results: {path}')
    return result


def compare(root):
    out = root/'out'; arms = (root/'ARMS').read_text().split()
    config, bugs = counts(root); flaky = defaultdict(set); differences = []
    for arm in arms:
        for repeat in sorted((out/'results').glob(f'*-{arm}-repeat.jsonl')):
            label = repeat.name[:-len(f'-{arm}-repeat.jsonl')]
            suffix = '-official' if label == 'FINAL' else ''
            one = cases(out/'results'/f'{label}-{arm}{suffix}.jsonl'); two = cases(repeat)
            for cid in sorted(set(one)|set(two)):
                if one.get(cid,'missing') != two.get(cid,'missing'):
                    flaky[arm].add(cid)
                    differences.append((label,arm,cid,one.get(cid,'missing'),two.get(cid,'missing')))
    with (out/'flaky.tsv').open('w') as f:
        f.write('snapshot\tarm\tcase\tofficial\trepeat\n')
        for row in differences: f.write('\t'.join(row)+'\n')
    with (out/'regrade-diff.tsv').open('w') as f:
        f.write('arm\tcase\tofficial\tregrade\n')
        for arm in arms:
            one=cases(out/'results'/f'FINAL-{arm}-official.jsonl')
            two=cases(out/'results'/f'FINAL-{arm}-regrade.jsonl')
            for cid in sorted(set(one)|set(two)):
                if one.get(cid,'missing') != two.get(cid,'missing'):
                    f.write('\t'.join((arm,cid,one.get(cid,'missing'),two.get(cid,'missing')))+'\n')
    lines=(out/'scores-checkpoints.tsv').read_text().splitlines()+(out/'scores-official.tsv').read_text().splitlines()
    with (out/'scores.tsv').open('w') as f:
        for line in lines:
            fields=line.split('\t'); label,arm=fields[:2]
            suffix='-official' if label=='FINAL' else ''
            result=cases(out/'results'/f'{label}-{arm}{suffix}.jsonl')
            passed={cid for cid,status in result.items() if status=='pass'}-flaky[arm]
            fields[2]=f'{len(passed)}/{config["N_total"]}'
            fields[3]=f'excl {len(passed-bugs)}/{config["N_scored"]}'
            f.write('\t'.join(fields)+'\n')

if __name__ == '__main__':
    compare(Path(__file__).resolve().parent)
