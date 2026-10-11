"""Frozen race 5 counts and exact scored IDs, owned by the suite runner."""
from pathlib import Path
import os
import subprocess
import sys


def exclusions(root):
    return {line.split()[0] for line in (Path(root) / 'SPEC-BUG-CASES.txt').read_text().splitlines()
            if line.strip() and not line.lstrip().startswith('#')}


def counts(root=None):
    root = Path(root or Path(__file__).resolve().parent)
    values = dict(line.split('=', 1) for line in (root / 'COUNTS.txt').read_text().splitlines()
                  if line.strip() and not line.lstrip().startswith('#'))
    values = {key: int(value) for key, value in values.items()}
    bugs = exclusions(root)
    assert values['N_scored'] > 0, 'N_scored must be positive'
    assert values['N_scored'] == values['N_total'] - len(bugs), 'exclusion count mismatch'
    target = values['N_scored']
    assert values.get('target', target) == target, 'target must equal N_scored (100%)'
    assert values.get('excluded', len(bugs)) == len(bugs), 'excluded count mismatch'
    values.update(target=target, excluded=len(bugs))
    return values, bugs


def inventory(root=None):
    root = Path(root or Path(__file__).resolve().parent)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    output = subprocess.check_output([sys.executable, str(root / 'inputs/conformance/bin/kogen-conformance'),
                                      'list'], cwd=root, env=env, text=True)
    ids = [line.split('\t', 1)[0] for line in output.splitlines() if line.strip()]
    if any(any(char in cid for char in ',*?[]') or any(char.isspace() for char in cid) for cid in ids):
        raise ValueError('case IDs must be exact comma-separated runner selectors')
    if not ids or len(ids) != len(set(ids)):
        raise ValueError('runner list must contain unique case IDs')
    return ids


def scored_ids(root=None):
    values, bugs = counts(root)
    ids = inventory(root)
    if len(ids) != values['N_total'] or not bugs <= set(ids):
        raise ValueError('COUNTS/exclusions differ from runner list')
    return [cid for cid in ids if cid not in bugs]


if __name__ == '__main__':
    if '--cases' in sys.argv:
        print(','.join(scored_ids()))
    else:
        for key, value in counts()[0].items():
            print(f'{key}={value}')
