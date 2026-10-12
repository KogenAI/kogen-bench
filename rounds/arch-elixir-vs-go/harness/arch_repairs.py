#!/usr/bin/env python3
"""Count continuation turns after the first affirmative self-reported pass claim."""
from pathlib import Path
import argparse
import json
import re
from arch_config import dump

CLAIM = re.compile(r'\ball\s+(?:(?:\d+|my|our|own|local|visible)\s+)*tests\s+(?:now\s+)?(?:pass(?:ed|ing)?|(?:are|have)\s+(?:(?:all|now)\s+)?pass(?:ed|ing)?)\b', re.I)
NEGATION = re.compile(r"\b(?:not|never|don't|cannot|can't|haven't|if|when|until|before|would|should|will|except|however)\b", re.I)

def affirmative(text):
    for sentence in re.split(r'[.!?\n]', text):
        if CLAIM.search(sentence) and not NEGATION.search(sentence):
            return True
    return False

def count(turns):
    first, launched = None, []
    for path in turns:
        path = Path(path)
        started, claimed = False, False
        for line in path.read_text().splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if event.get('type') in ('thread.started', 'turn.started'):
                started = True
            item = event.get('item') or {}
            if item.get('type') == 'agent_message' and affirmative(item.get('text', '')):
                claimed = True
        if not started:
            continue
        launched.append(path.name)
        if first is None and claimed:
            first = len(launched) - 1
    return dict(first_claim_turn=launched[first] if first is not None else None,
                repair_turns=len(launched) - first - 1 if first is not None else 0,
                no_pass_claim=first is None, launched_turns=len(launched),
                method='assistant agent_message claims only; later started continuation invocations in this phase')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('phase_dir', type=Path)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    turns = sorted(args.phase_dir.glob('turn-*.jsonl'), key=lambda p: int(p.stem.split('-')[-1]))
    dump(args.out, count(turns))

if __name__ == '__main__':
    main()
