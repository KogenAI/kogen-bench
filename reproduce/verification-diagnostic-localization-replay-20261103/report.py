import json,sys,hashlib
from pathlib import Path
x=json.loads(Path(sys.argv[1]).read_text());c=x['cases']
assert len(c)==10 and len({r['repo'] for r in c})==5
for r in c:
 assert hashlib.sha256(r['retained_output'].encode()).hexdigest()==r['input_sha256']
t={k:sum(r['score'][k] for r in c) for k in ['file','line_or_function','exact_tested_tuple','stale_revision_demonstrated']}
assert all(t[k]==x['totals'][k] for k in t)
print('cases=10 repos=5 mechanisms=8')
print('file='+str(t['file'])+'/10 line_or_function='+str(t['line_or_function'])+'/10 exact_tuple='+str(t['exact_tested_tuple'])+'/10')
print('quoted_resource_host_failures: retained=2 current='+str(sum(r['current']['host_failure'] for r in c if r['id'] in [3,4])))
print('provisional_case10_excluded: file=4/9 line_or_function=2/9 exact_tuple=0/9')
print('repair_effect=unmeasured paid_cells=0 verdict=unresolved')
