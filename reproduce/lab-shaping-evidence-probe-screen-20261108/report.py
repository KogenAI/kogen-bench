import json
from pathlib import Path
d=json.loads((Path(__file__).parent/'data.json').read_text())
for r in (1,2): print('rep',r,'control',sum(x['control_ready'] for x in d if x['rep']==r),'candidate',sum(x['ready'] for x in d if x['rep']==r))
print('gains',sum(not x['control_ready'] and x['ready'] for x in d),'losses',sum(x['control_ready'] and not x['ready'] for x in d))
