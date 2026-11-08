import json
from pathlib import Path
d=json.loads((Path(__file__).parent/'data.json').read_text())
print('baseline',sum(x['baseline_ready'] for x in d),'candidate',sum(x['candidate_ready'] for x in d),'gains',sum(not x['baseline_ready'] and x['candidate_ready'] for x in d),'losses',sum(x['baseline_ready'] and not x['candidate_ready'] for x in d))
