#!/usr/bin/env python3
"""Find an arm's first target snapshot using conditional both-pass official scores."""
import json
from pathlib import Path
import re
import subprocess
import sys
from scoring_config import counts

ROOT = Path(__file__).resolve().parent


def search(root, arm):
    values, _ = counts(root); target = values['target']
    start = int((root / 'START').read_text())
    final_time = (int((root / 'DEADLINE').read_text()) - start) / 60
    points = []
    for path in (root / 'snapshots').iterdir():
        if not (path / arm).is_dir():
            continue
        match = re.fullmatch(r'T\+(\d+)m', path.name)
        if match:
            minutes = int(match[1])
        elif path.name == f'TARGET-{arm}':
            minutes = (int((path / 'TAKEN_EPOCH').read_text()) - start) / 60
        elif path.name == 'FINAL':
            minutes = final_time
        else:
            continue
        points.append((minutes, path.name))
    points.sort()
    if not any(label == 'FINAL' for _, label in points):
        raise ValueError('FINAL snapshot missing')
    seen = {}
    def score(label):
        if label not in seen:
            # The helper does every required second run before returning the
            # per-case both-pass count; raw first counts never decide the search.
            output = subprocess.check_output([str(root / 'score-one.sh'), label, arm], text=True)
            seen[label] = int(output.strip())
        return seen[label]
    final = score('FINAL')
    for _, label in points:
        if label.startswith('TARGET-'):
            score(label)
    lo, hi = 0, len(points)
    while lo < hi:
        mid = (lo + hi) // 2
        if score(points[mid][1]) >= target:
            hi = mid
        else:
            lo = mid + 1
    candidates = [i for i, (_, label) in enumerate(points) if seen.get(label, -1) >= target]
    first = min(candidates) if candidates else None
    guards = []
    if first is not None:
        minutes, _ = points[first]
        prior = [label for t, label in points if label.startswith('T+') and t < minutes]
        if prior:
            guards.append(f'{prior[-1]}={score(prior[-1])}')
    # Scores can regress: verify earlier checkpoints using the same official rule.
    first = None
    for i, (_, label) in enumerate(points):
        if score(label) >= target:
            first = i
            break
    if first is not None:
        minutes, _ = points[first]
        prior = [label for t, label in points if label.startswith('T+') and t < minutes]
        if prior:
            guard = f'{prior[-1]}={score(prior[-1])}'
            if guard not in guards:
                guards.append(guard)
    repeats = []
    for _, label in points:
        if label not in seen:
            continue
        receipt = json.loads((root / f'out/results/{label}-{arm}-score.json').read_text())
        if receipt['double_scored']:
            repeats.append(f"{label}:{receipt['first_scored']}/{receipt['second_scored']}=>{receipt['combined_scored']}")
    result = 'not reached' if first is None else points[first][1]
    minutes = '' if first is None else f'{points[first][0]:.4f}'
    with (root / 'out/ttt.tsv').open('a') as out:
        out.write(f'{arm}\t{result}\t{minutes}\tFINAL={final}\ttarget={target}\tguard:{" ".join(guards)}\trepeat:{" ".join(repeats)}\n')
    print(f'{arm}: {result}' + (f' at {minutes} min' if minutes else ''))


if __name__ == '__main__':
    search(ROOT, sys.argv[1])
