#!/usr/bin/env python3
"""Recompute the published descriptive tables. Standard library only."""
import csv,sys,collections,statistics
from pathlib import Path
path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'data/scores.tsv'
rows=list(csv.DictReader(path.open(),delimiter='\t'))
assert len(rows)==36, 'expected all 36 assigned reviews'
assert len({(r['case'],r['arm'],r['rep']) for r in rows})==36, 'duplicate paired result'
for c in {r['case'] for r in rows}:
 assert {(r['arm'],r['rep']) for r in rows if r['case']==c}=={(a,str(n)) for a in ['A','B'] for n in [1,2]}, 'missing arm or repetition'
print('| split | case | arm | n | detected targets | missed targets | requests | wall seconds | guarded cost USD |')
print('|---|---|---|---:|---:|---:|---:|---:|---:|')
for key in sorted({(r['split'],r['case'],r['arm']) for r in rows}):
 rs=[r for r in rows if tuple(r[k] for k in ['split','case','arm'])==key]
 vals=[len(rs),sum(int(r['target_caught']) for r in rs),sum(int(r['target_misses']) for r in rs),sum(int(r['requests']) for r in rs),sum(float(r['review_wall_s']) for r in rs),sum(float(r['guard_estimate_usd']) for r in rs)]
 print('| '+' | '.join(key)+f' | {vals[0]} | {vals[1]} | {vals[2]} | {vals[3]} | {vals[4]:.3f} | {vals[5]:.6f} |')
print('\n| split | arm | n | detected targets | missed targets | requests | wall seconds | guarded cost USD |')
print('|---|---|---:|---:|---:|---:|---:|---:|')
for split in ['DEV','HELD-OUT','ALL']:
 for arm in ['A','B']:
  rs=[r for r in rows if r['arm']==arm and (split=='ALL' or r['split']==split)]
  print(f"| {split} | {arm} | {len(rs)} | {sum(int(r['target_caught']) for r in rs)} | {sum(int(r['target_misses']) for r in rs)} | {sum(int(r['requests']) for r in rs)} | {sum(float(r['review_wall_s']) for r in rs):.3f} | {sum(float(r['guard_estimate_usd']) for r in rs):.6f} |")
print('\nAll attempted repairs remain unverified. Guard estimates are not subscription bills.')
