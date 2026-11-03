import json
from pathlib import Path
d=json.loads(Path(__file__).with_name('data.json').read_text());m=d['metadata']
print('verdict',m['verdict'],'cells',m['cells'],'instrument_voids',m['instrument_voids'],'finished_at',m['finished_at'])
for r in d['rows']:print(r['tuple'],r['task'],'Intent',int(r['valid']),'landed',int(r['landed']),'hidden',r['hidden'],'outcome',r['outcome'],'wall_s',r['wall_s'])
print('tokens',json.dumps(m['tokens'],sort_keys=True));print('cell_wall_s',m['cell_wall_s']);print('cost_usd',m['cost_usd']);print('disposition',m['disposition'])
