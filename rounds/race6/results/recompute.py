#!/usr/bin/env python3
"""Verify public aggregate arithmetic without reading any suite or private files."""
from pathlib import Path
import csv,json,statistics
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent
summary=json.loads((ROOT/'results/summary.json').read_text())
def read(name):return list(csv.DictReader((ROOT/'results'/name).open(),delimiter='\t'))
def timestamp(value):return datetime.fromisoformat(value.replace('Z','+00:00'))
cells=read('cells.tsv');tokens=read('tokens.tsv');assert len(cells)==len(tokens)==16
assert len({(x['host'],x['language'],x['condition']) for x in cells})==16
assert set(x['host'] for x in cells)=={'Mac Studio','MacBook'}
assert summary['denominators']=={'N_total':106,'N_scored':106,'excluded':0}
assert summary['round_status_literal']=='invalid round'
for cell in cells:
 assert sum(int(cell[k]) for k in ['pass','fail','error'])==106
 assert cell['FINAL/106']==f"{cell['pass']}/106"
 assert cell['valid']=='true under accepted deviation'
 assert cell['literal_status']=='non-deciding: invalid round'
 assert cell['audit_class']=='classify-note' and cell['T+030m']=='unavailable'
 assert int(cell['raw_wall_s'])==int(cell['stall_adjusted_wall_s'])==3600
for language in ['Elixir','Go']:
 src=summary['languages'][language]
 assert src['literal_frozen_rule']['status']=='invalid round'
 assert all(v is None for v in src['literal_frozen_rule']['medians'].values())
 out=src['accepted_deviation_descriptive'];groups={c:[int(x['pass']) for x in cells if x['language']==language and x['condition']==c.upper()] for c in 'abcd'}
 med={c:statistics.median(v) for c,v in groups.items()};spread={c:max(v)-min(v) for c,v in groups.items()}
 assert med==out['medians'] and spread==out['spread']
 for c in 'bcd':
  direction=f'{c.upper()} above A' if min(groups[c])>max(groups['a']) else f'{c.upper()} below A' if max(groups[c])<min(groups['a']) else 'no clear direction'
  assert direction==out['directions'][c]
  assert med[c]-med['a']==out['differences'][c+'-A']
  for host,key in [('Mac Studio','studio'),('MacBook','macbook')]:
   count={x['condition']:int(x['pass']) for x in cells if x['host']==host and x['language']==language}
   assert count[c.upper()]-count['A']==out['paired_differences'][key][c+'-A']
 top=sorted(med.values(),reverse=True);ambiguous=top[0]-top[1]<=3 or any(v>10 for v in spread.values())
 assert ambiguous==out['ambiguous_pilot']
 assert all(v==2 for v in out['valid_sample_size'].values())
 print(f"{language}: A/B/C/D medians {('/'.join(str(med[c]) for c in 'abcd'))}/106; B/C/D above A; ambiguous={ambiguous}")
index={(x['host'],x['language'],x['condition']):x for x in tokens}
kill={'Mac Studio':timestamp('2026-10-11T07:28:00Z'),'MacBook':timestamp('2026-10-11T07:26:00Z')}
for cell in cells:
 t=index[cell['host'],cell['language'],cell['condition']]
 assert int(t['total'])==int(t['input'])+int(t['output'])
 assert int(t['cached_input'])<=int(t['input']) and int(t['reasoning'])<=int(t['output'])
 assert cell['tokens_to_kill_point']==t['total']
 assert timestamp(t['last_token_event_ts'])<=kill[t['host']] and int(t['n_threads'])==1
 for k in ['input','cached_input','output','reasoning','last_token_event_ts','n_threads']:assert cell['tokens_'+k]==t[k]
 assert any(x==cell for x in summary['cells'])
# Verify every README token median against independently grouped TSV values.
readme=(ROOT/'README.md').read_text();median_rows=[line for line in readme.splitlines() if line.startswith('| Median (2 hosts) |')]
assert len(median_rows)==8
for line in median_rows:
 fields=[x.strip() for x in line.strip('|').split('|')];language,condition=fields[2:4]
 pair=[x for x in tokens if x['language']==language and x['condition']==condition];assert len(pair)==2
 for field,value in zip(['input','cached_input','output','reasoning','total'],fields[4:9]):
  assert statistics.median(int(x[field]) for x in pair)==float(value.replace(',',''))
print('PASS: 16 per-arm counts; literal/accepted readings; per-language medians, differences, spreads, directions and ambiguity; 16 token totals and 8 token median rows. Missing T+030m remains unavailable.')
