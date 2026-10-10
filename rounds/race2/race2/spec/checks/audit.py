#!/usr/bin/env python3
"""Static integrity checks and current source/trace inventory; no executable replay."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PARENT=ROOT.parent.parent
canonical=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
source_inventory={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'quint').glob('*.qnt'))}
def closure(p,seen=None):
 seen=set() if seen is None else seen
 p=p.resolve()
 if p in seen:return seen
 seen.add(p)
 for name in re.findall(r'from "([^\"]+)"',p.read_text()):
  assert name.startswith('./'),(p,name)
  child=(p.parent/name).with_suffix('.qnt');assert child.exists(),child;closure(child,seen)
 return seen
closures={}
for p in sorted((ROOT/'quint').glob('*.qnt')):
 files=sorted(closure(p),key=lambda x:str(x.relative_to(ROOT)));digest=hashlib.sha256()
 for child in files:
  rel='spec/'+str(child.relative_to(ROOT));digest.update(rel.encode()+b'\0'+child.read_bytes()+b'\0')
 closures[p.stem]={'source_digest':digest.hexdigest(),'sources':[{'path':'spec/'+str(c.relative_to(ROOT)),'sha256':hashlib.sha256(c.read_bytes()).hexdigest()} for c in files]}
# Keep the owner's old metadata separate, refresh current CLI manifest.
p=ROOT/'quint/cli-fixtures/manifest.json';d=json.loads(p.read_text());d.update(closures['cli']);p.write_text(json.dumps(d,indent=2)+'\n')
original=(PARENT/'core-now/spec/CORE.md').read_bytes();current=(ROOT/'CORE.md').read_bytes()
m0=(PARENT/'m0/spec/CORE.md').read_bytes();seam=re.search(rb'^### Test seam.*?(?=^## |\Z)',m0,re.M|re.S)[0]
assert current.count(seam)==1 and current.replace(seam,b'')==original
for name in ['provider_login.qnt','version.qnt']:assert (ROOT/'quint'/name).read_bytes()==(PARENT/'core-now/spec/quint'/name).read_bytes()
assert (ROOT/'quint/kogen_io.qnt').read_bytes()==(PARENT/'m0/spec/quint/kogen_io.qnt').read_bytes()
actual={}
for p in (ROOT/'quint').glob('*.qnt'):
 for m in re.finditer(r'^module (\w+) \{(.*?)(?=^module |\Z)',p.read_text(),re.M|re.S):
  actual[m[1]]=set(re.findall(r'^  (?:pure )?(?:type|def|val|action|run|var) (\w+)',m[2],re.M))
for p in (ROOT/'features').glob('*.feature'):
 for tag in re.findall(r'@quint:([^\s]+)',p.read_text()):
  mod,name=tag.split('.',1);assert name in actual[mod],tag
coverage=json.loads((ROOT/'checks/coverage-inventory.json').read_text())
for r in coverage:
 for element in r['elements']:
  mod,name=element.split('.');assert name in actual[mod],element
assert 'not claimed' not in (ROOT/'COVERAGE.md').read_text().lower()
# Parse support JSON and validate available fixture digests, without invoking their effects.
for filename in ['life-fixtures.json','git-fixtures.json','process-fixtures.json','statusrec-fixtures.json']:
 scripts=json.loads((ROOT/'quint'/filename).read_text())
 for name,script in scripts.items():
  if 'digest' in script:assert hashlib.sha256(canonical({k:v for k,v in script.items() if k!='digest'})).hexdigest()==script['digest'],(filename,name)
trace_metadata=[]
for p in sorted((ROOT/'quint/traces').glob('*.itf.json')):
 trace=json.loads(p.read_text());steps=[step for state in trace['states'] for step in state.get('lastStep',[])]
 for effect in steps:
  tag=effect.get('tag');value=effect.get('value',{})
  if tag=='Cli':operands=value['cmd']
  elif tag=='Setup' and value['op'].get('tag')=='GitCommand':operands=value['op']['value']
  else:continue
  assert '${capture:' not in json.dumps(operands),(p.name,'capture in command operands')
 module='intent' if p.name.startswith('life-artifacts-') else p.stem.split('-')[0]
 meta={'trace':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'states':len(trace['states']),'actions':len(steps),'executable_witness':bool(steps),'replayed':False,'not_a_replay_manifest':True}
 if module in closures:meta.update(closures[module])
 trace_metadata.append(meta);p.with_suffix('.metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
summary={'core_preserved_except_verbatim_seam':True,'newer_modules_preserved':True,'io_preserved':True,'all_imports_local':True,'all_quint_tags_resolve':True,'all_coverage_elements_resolve':True,'fixture_digests_valid':True,'command_capture_audit':'pass for retained traces','source_sha256':source_inventory,'closures':closures,'traces':trace_metadata}
(ROOT/'checks/integrity.json').write_text(json.dumps(summary,indent=2)+'\n')
print('integrity PASS:',len(source_inventory),'files;',len(coverage),'clause rows;',len(trace_metadata),'traces')
