import json
from pathlib import Path
d=json.loads((Path(__file__).parent/'data.json').read_text())
b={(x['task'],x['rep'],x['arm']):x for x in d}
for arm in ('historical','current'):
 print(arm, [sum(b[(f'c{i:02d}',r,arm)]['ready'] for i in range(1,11)) for r in (1,2)])
print('gains',sum(not b[(f'c{i:02d}',r,'historical')]['ready'] and b[(f'c{i:02d}',r,'current')]['ready'] for i in range(1,11) for r in (1,2)))
print('losses',sum(b[(f'c{i:02d}',r,'historical')]['ready'] and not b[(f'c{i:02d}',r,'current')]['ready'] for i in range(1,11) for r in (1,2)))
