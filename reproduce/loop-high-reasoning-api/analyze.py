#!/usr/bin/env python3
"""Reproduce the loop-high-reasoning-api numbers from runs.csv (standard library only)."""
import csv, pathlib

ROWS = list(csv.DictReader(open(pathlib.Path(__file__).with_name('runs.csv'), newline='')))
TOOLS = ['loop', 'codex']


def total(effort, tool, col):
    return sum(float(r[col]) for r in ROWS if r['effort'] == effort and r['tool'] == tool)


print('Per tool, gpt-6.1-terra, same OpenAI API key, 4 tasks x 2 reps (totals over all 8 runs)')
print('effort | tool | passed/launched | requests | reasoning tokens | output tokens | USD')
for effort in ('high', 'medium'):
    for t in TOOLS:
        rs = [r for r in ROWS if r['effort'] == effort and r['tool'] == t]
        print(f"{effort} | {t} | {sum(int(r['passed']) for r in rs)}/{len(rs)} | {total(effort, t, 'requests'):.0f} | "
              f"{total(effort, t, 'reasoning_tokens'):,.0f} | {total(effort, t, 'output_tokens'):,.0f} | ${total(effort, t, 'cost_usd'):.3f}")
print()
print('Loop over Codex at high: reasoning tokens x%.2f, requests x%.2f, USD x%.3f' % (
    total('high', 'loop', 'reasoning_tokens') / total('high', 'codex', 'reasoning_tokens'),
    total('high', 'loop', 'requests') / total('high', 'codex', 'requests'),
    total('high', 'loop', 'cost_usd') / total('high', 'codex', 'cost_usd')))
