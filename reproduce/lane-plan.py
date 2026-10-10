#!/usr/bin/env python3
"""Resolve a frozen cell from a plan and fail closed on launch mismatches."""
import argparse,json,re,sys
from urllib.parse import urlsplit, unquote
from pathlib import Path

EMAIL=re.compile(r'(?i)(?:[a-z0-9.!#$%&\'*+/=?^_`{|}~-]+)@[a-z0-9.-]+\.[a-z]{2,}')
LOCAL_PATH=re.compile(r'(?i)(?:^|[\s=:])(?:~(?:[/\\]|$)|/(?:Users|home)/[^/\\\s]+|/root(?:[/\\]|$)|[a-z]:[/\\](?:Users|home)[/\\])')

def safe_text(value):
 if not isinstance(value,str) or not value.strip(): return None
 value=value.strip()
 if EMAIL.search(value) or LOCAL_PATH.search(value): return None
 return value

def public_ref(value):
 value=safe_text(value)
 if not value: return None
 ssh=re.fullmatch(r'(?:ssh://)?git@([^:/]+)[:/]([^\s]+)',value)
 if ssh: value=ssh.group(1)+'/'+ssh.group(2)
 elif '://' in value:
  try:
   parsed=urlsplit(value)
   if not parsed.hostname or parsed.username or parsed.password: return None
   value=parsed.hostname.lower()+'/'+unquote(parsed.path).lstrip('/')
  except ValueError: return None
 if value.startswith(('/', '~')) or re.match(r'^[a-z]:[/\\]',value,re.I) or '\\' in value:
  return None
 parts=value.split('/')
 if not value or any(part in ('', '.', '..') for part in parts) or any(ch.isspace() for ch in value):
  return None
 return value

def public_label(value):
 """Keep a public source label while rejecting local paths and identities."""
 value=safe_text(value)
 if not value or value.startswith(('/', '~', '\\\\')) or re.match(r'^[a-z]:[/\\\\]',value,re.I):
  return None
 if any(ord(ch)<32 for ch in value): return None
 return ' '.join(value.split())

def safe_or_missing(value):
 value=safe_text(value)
 return value if value else {'missing':'m39'}

def main():
 p=argparse.ArgumentParser(); p.add_argument('--plan',required=True); p.add_argument('--cell',required=True); p.add_argument('--task',required=True); p.add_argument('--model',required=True); p.add_argument('--effort',required=True); a=p.parse_args()
 try: data=json.loads(Path(a.plan).read_text())
 except Exception as e: raise SystemExit(f'cannot read plan: {e}')
 cells=data.get('cells')
 if isinstance(cells,list): rows=cells
 elif isinstance(cells,dict): rows=[dict(v,cell_id=k) if isinstance(v,dict) else {} for k,v in cells.items()]
 else: rows=[data]
 matches=[r for r in rows if isinstance(r,dict) and r.get('cell_id',r.get('id'))==a.cell]
 if len(matches)!=1: raise SystemExit('plan must identify exactly one requested cell')
 c=matches[0]
 aliases={'itt_class':'class','itt_cohort':'cohort','itt_evidence_ref':'evidence_ref'}
 def val(k): return c.get(k,c.get(aliases[k])) if k in aliases else c.get(k)
 required=['round_id','audit_round','cell_id','arm','harness','recipe','class','cohort','evidence_ref','repetition','task','model','effort']
 itt=c.get('itt') if isinstance(c.get('itt'),dict) else {}
 for k in required:
  value=itt.get(k) if k in ('class','cohort','evidence_ref') else val(k)
  if value is None or value=='': raise SystemExit(f'plan cell is missing {k}')
 if itt.get('class') not in ('counted','excluded-env-fault'):
  raise SystemExit('plan ITT class is not in the Standard 1.2 enum')
 if itt.get('cohort') not in ('scored','smoke-control','unresolved'):
  raise SystemExit('plan ITT cohort is not in the Standard 1.2 enum')
 if c.get('task',a.task)!=a.task: raise SystemExit('task does not match plan cell')
 if c.get('model',a.model)!=a.model: raise SystemExit('model does not match plan cell')
 if c.get('effort',a.effort)!=a.effort: raise SystemExit('effort does not match plan cell')
 launcher=c.get('launcher_sha256',c.get('dispatcher_id',data.get('launcher_sha256',data.get('dispatcher_id'))))
 if not isinstance(launcher,str) or not re.fullmatch(r'[0-9a-f]{64}',launcher): raise SystemExit('plan cell requires the launcher script SHA-256 as dispatcher identity')
 base=c.get('base_revision',{})
 base_obj=base if isinstance(base,dict) else None
 if isinstance(base,dict): base=base.get('hash')
 if not base: base=c.get('base_sha')
 if not isinstance(base,str) or not re.fullmatch(r'[0-9a-f]{40}',base): raise SystemExit('plan cell is missing the original base revision')
 if base_obj and base_obj.get('kind') != 'git-commit': raise SystemExit('lane plan base revision must identify a git commit')
 if not isinstance(c.get('harness_version'),str) or not c['harness_version']: raise SystemExit('plan cell is missing the pinned harness version')
 if not isinstance(c.get('adapter_harness_sha'),str) or not re.fullmatch(r'[0-9a-f]{64}',c['adapter_harness_sha']): raise SystemExit('plan cell is missing the adapter/harness fingerprint')
 if c.get('deps_source') not in ('task-derived','shared'): raise SystemExit('plan cell is missing the dependency source')
 ledger=c.get('ledger_sha256')
 if not isinstance(ledger,str) or not re.fullmatch(r'[0-9a-f]{64}',ledger): raise SystemExit('plan cell is missing the source-ledger SHA-256')
 source_ref=public_ref(c.get('source_ref',data.get('source_ref')))
 if not source_ref: raise SystemExit('plan cell is missing a sanitized public input reference')
 if not isinstance(val('repetition'),int) or val('repetition') < 1: raise SystemExit('plan cell repetition must be a positive integer')
 effective_model=public_label(c.get('effective_model',data.get('effective_model')))
 if not effective_model: raise SystemExit('plan cell is missing a public effective_model')
 effective_effort=public_label(c.get('effective_effort',data.get('effective_effort')))
 if not effective_effort: raise SystemExit('plan cell is missing a public effective_effort')
 venue=c.get('venue',data.get('venue'))
 if venue not in ('eu','us'): raise SystemExit('plan cell venue must be eu or us')
 account_class=c.get('account_class',data.get('account_class'))
 if account_class not in ('billing','owner'): raise SystemExit('plan cell account_class must be billing or owner')
 queue_position=c.get('queue_position',data.get('queue_position'))
 if isinstance(queue_position,bool) or not isinstance(queue_position,(int,str)) or not str(queue_position).strip():
  raise SystemExit('plan cell is missing queue_position')
 if isinstance(queue_position,int) and queue_position<0: raise SystemExit('plan cell queue_position cannot be negative')
 queue_position=public_label(str(queue_position))
 if not queue_position: raise SystemExit('plan cell queue_position must be a public identifier')
 kogen_sha=c.get('kogen_sha',data.get('kogen_sha'))
 if not isinstance(kogen_sha,str) or not re.fullmatch(r'[0-9a-f]{40}',kogen_sha):
  raise SystemExit('plan cell is missing the installed Kogen kit revision')
 normalized={k:safe_or_missing(val(k)) for k in ('round_id','audit_round','cell_id','arm','harness','recipe')}
 normalized['repetition']=val('repetition')
 normalized['launcher_sha256']=launcher; normalized['dispatcher_id']=launcher
 normalized['base_revision']={'kind':'git-commit','hash':base}
 normalized['itt']={k:(public_ref(itt.get(k) if k in itt else val('itt_'+k)) if k=='evidence_ref' else safe_or_missing(itt.get(k) if k in itt else val('itt_'+k))) for k in ('class','cohort','evidence_ref')}
 if not normalized['itt']['evidence_ref']: raise SystemExit('plan cell evidence reference must be a public relative identifier')
 normalized['task']=a.task; normalized['model']=safe_or_missing(c.get('model',a.model)); normalized['effort']=safe_or_missing(c.get('effort',a.effort))
 normalized['source_ref']=source_ref
 for k in ('deps_source','adapter_harness_sha','harness_version'):
  value=c.get(k,data.get(k))
  if value is not None:
   if k=='adapter_harness_sha': normalized[k]=value
   else: normalized[k]=safe_or_missing(value)
 normalized['effective_model']=effective_model
 normalized['effective_effort']=effective_effort
 normalized['venue']=venue
 normalized['account_class']=account_class
 normalized['queue_position']=queue_position
 normalized['kogen_sha']=kogen_sha
 base_repo=public_label(c.get('base_repo',data.get('base_repo')))
 if not base_repo: raise SystemExit('plan cell is missing a public task base_repo label')
 normalized['base_repo']=base_repo
 normalized['base_revision']={'kind':'git-commit','hash':base}
 normalized['ledger_sha256']=ledger
 normalized['adapter_harness_sha']=c['adapter_harness_sha']
 normalized['harness_version']=safe_or_missing(c.get('harness_version'))
 if isinstance(normalized['harness_version'],dict): raise SystemExit('plan cell harness version contains a private path or email')
 print(json.dumps(normalized,sort_keys=True))
if __name__=='__main__': main()
