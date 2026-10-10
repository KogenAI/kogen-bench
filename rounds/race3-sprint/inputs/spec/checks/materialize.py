#!/usr/bin/env python3
"""Materialize authored fixture data from the integrated Quint export (no replay)."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def decode(x):
 if isinstance(x,list):return [decode(v) for v in x]
 if not isinstance(x,dict):return x
 if '#bigint' in x:return int(x['#bigint'])
 if '#set' in x:return [decode(v) for v in x['#set']]
 if '#map' in x:return {decode(k):decode(v) for k,v in x['#map']}
 if '#tup' in x:return [decode(v) for v in x['#tup']]
 if 'tag' in x:
  tag=x['tag'];value=decode(x['value'])
  if tag in ('Missing','JNull'):return None
  if tag in ('Present','JString','JInt','JBool','JDecimal','JSymbol'):return value
  if tag=='Utf8':return {'utf8':value}
  if tag=='Octets':return {'octets':value}
  return {'tag':tag,'value':value}
 return {k:decode(v) for k,v in x.items()}
def bytes_value(x):
 return x['utf8'].encode() if 'utf8' in x else bytes(x['octets'])
def row_native(row):
 nodes={p:{} for p in row['objects']}
 nodes.update({p:[None]*n for p,n in row['arrays'].items()});nodes.update(row['atoms'])
 for pointer in sorted(nodes,key=lambda p:p.count('/'),reverse=True):
  if not pointer:continue
  parent,key=pointer.rsplit('/',1);key=key.replace('~1','/').replace('~0','~')
  container=nodes[parent]
  if isinstance(container,list):container[int(key)]=nodes[pointer]
  else:container[key]=nodes[pointer]
 return nodes['']
canonical=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
if __name__=='__main__':
 trace=json.loads((ROOT/'quint/traces/life-artifacts-0.itf.json').read_text());state=decode(trace['states'][0]);scripts=state['scripts']
 for script in scripts.values():
  for turn in script['turns']:
   req=turn['request'];req['equals'].update({p:bytes_value(v).decode() for p,v in req.pop('byteEquals').items()})
   req['equals'].update({p:row_native(v) for p,v in req.pop('exact').items()})
  script['digest']=hashlib.sha256(canonical(script)).hexdigest()
 (ROOT/'quint/life-fixtures.json').write_text(json.dumps(scripts,indent=2,ensure_ascii=False)+'\n')
 children={k:{'bytes':v,'digest':hashlib.sha256(bytes_value(v)).hexdigest()} for k,v in state['children'].items()}
 (ROOT/'quint/life-children.json').write_text(json.dumps(children,indent=2)+'\n')
 print('materialized',len(scripts),'scripts and',len(children),'child executables from current model')
