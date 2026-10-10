#!/usr/bin/env python3
from pathlib import Path
import sys,json,importlib.util,re
R=Path(__file__).resolve().parent.parent;sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'conformance'))
spec=importlib.util.spec_from_file_location('t2',R/'conformance/bin/t2_dedupe.py');t2=importlib.util.module_from_spec(spec);spec.loader.exec_module(t2)
from kogen_conformance.runner import load_cases
cases={c['id']:c for c in load_cases()};ex=dict(l.split('\t',1) for l in (R/'harness/EXCLUDED-V2.txt').read_text().splitlines());total,groups=t2.duplicate_groups(R/'conformance/cases')
# Rebuild duplicate reasons so repeated runs are idempotent.
ex={cid: '; '.join(part for part in reason.split('; ') if not part.startswith('duplicate of ')) for cid,reason in ex.items()}
ex={cid:reason for cid,reason in ex.items() if reason}
def metadata(cid):
 c=cases[cid]
 if '_manifest' not in c:return {k:v for k,v in c.items() if k not in {'id','seed','steps','_file'}}
 m=json.loads(json.dumps(c['_manifest']));seed=str(m.pop('seed'));m.pop('id',None)
 # These provenance fields encode the case identity/seed. Normalize only the
 # numeric seed token, preserving the entire rest of each field. Runtime data
 # (fixtures, scripts/digests, requires/tools/seams and limits) stays byte exact.
 def identity(v):
  if isinstance(v,str):return re.sub(r'(?<!\d)'+re.escape(seed)+r'(?!\d)','<seed>',v)
  if isinstance(v,list):return [identity(x) for x in v]
  return v
 for key in ['itf_file','command_line','witnesses']:
  if key in m:m[key]=identity(m[key])
 return m
lines=['# Assembly manifest-aware deduplication','', 'Reran t2_dedupe.py after T1. Ignore id/seed, including the seed tokens in itf_file, command_line and witnesses. Preserve every other manifest field, notably all fixtures, tools/seams, fake scripts/digests and limits.',''];accepted=0;rejected=0
for group in groups:
 kept=group[0]
 for dropped in group[1:]:
  one,two=metadata(kept),metadata(dropped)
  if one==two:
   assert metadata(kept)==metadata(dropped)
   if dropped not in ex:ex[dropped]='duplicate of '+kept
   else:ex[dropped]+='; duplicate of '+kept
   accepted+=1;lines.append(f'- Drop {dropped}: duplicate of {kept}; manifests equal apart from id/seed.')
  else:
   keys=sorted(k for k in set(one)|set(two) if one.get(k)!=two.get(k));lines.append(f'- Keep {dropped} and {kept}: manifest differs: '+', '.join(keys));rejected+=1
lines+=['',f'Accepted duplicate exclusions: {accepted}; retained pairs with differing manifests: {rejected}.','']
(R/'conformance/T2-MANIFEST-AUDIT.md').write_text('\n'.join(lines));(R/'harness/EXCLUDED-V2.txt').write_text(''.join(f'{cid}\t{reason}\n' for cid,reason in sorted(ex.items())));(R/'harness/SPEC-BUG-CASES.txt').write_text('\n'.join(sorted(ex))+'\n');print('excluded',len(ex),'accepted duplicates',accepted,'rejected',rejected)
