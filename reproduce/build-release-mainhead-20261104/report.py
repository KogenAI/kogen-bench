import json
from pathlib import Path
rows = json.loads((Path(__file__).parent / 'data/results.json').read_text())
for r in rows:
    print(r['task'], r['arm'], r['outcome'], 'intent=', r['valid_intent'], 'landed=', r['landed'], 'hidden_all_pass=', r['hidden_all_pass'], 'wall_s=', r['wall_s'], 'input=', r['input_tokens'], 'output=', r['output_tokens'])
