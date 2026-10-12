#!/usr/bin/env python3
"""Execute the validated subset without changing registered source."""
import sys,os,json,time,hashlib,fcntl,subprocess,datetime
from pathlib import Path
ROOT=Path('<ROOT>');sys.path.insert(0,str(ROOT))
from shape_common import digest,write_json,reserve_json
from run_shaper import safe_json,audit_events,check_task_validation,check_gates,record_labels
from linux_support import require_linux_gap
W=ROOT/'run2';BASE=Path('<ROOT>');STOP=BASE/'logs/ROUND-STOP'
def utc():return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def log(phase,host,**values):
 line=f'{phase} utc={utc()} host={host} '+' '.join(f'{k}={v}' for k,v in values.items())
 for path in (BASE/'logs/launcher.log',ROOT/'logs/launcher.log',ROOT/'core4b/SLOTS.log',W/'SLOTS-APPEND.log'):
  path.parent.mkdir(parents=True,exist_ok=True)
  with path.open('a') as f:f.write(line+'\n');f.flush();os.fsync(f.fileno())
def hold(host):
 receipt=W/'hold.json'
 if receipt.exists():raise RuntimeError('wave hold already exists')
 with (BASE/'queue.txt').open('r+b') as q:
  fcntl.flock(q,fcntl.LOCK_EX);sha=hashlib.sha256(q.read()).hexdigest()
  if STOP.exists():
   previous=json.loads((ROOT/'prep/hold.json').read_text())
   if previous.get('held') is not True or STOP.read_text()!=previous['stop_payload']:raise RuntimeError('foreign STOP')
   reused=True;payload=previous['stop_payload']
  else:
   reused=False
   while True:
    slot=subprocess.run(['pgrep','-f',r'^bash ./rep[ce]\.sh '],stdout=subprocess.DEVNULL)
    units=subprocess.check_output(['systemctl','list-units','--all','--state=active','--no-legend','bench-*'],text=True)
    if slot.returncode==1 and not units.strip():break
    if slot.returncode not in (0,1):raise RuntimeError('slot inspection failed')
    if (ROOT/'STOP').exists():raise RuntimeError('shape STOP before hold')
    time.sleep(2)
   q.seek(0)
   if hashlib.sha256(q.read()).hexdigest()!=sha:raise RuntimeError('queue modified under lock')
   payload=f'shape1-run2 host={host} held={utc()} queue_sha256={sha}\n'
   with STOP.open('x') as f:f.write(payload);f.flush();os.fsync(f.fileno())
   os.chmod(STOP,0o600)
  reserve_json(receipt,dict(host=host,utc=utc(),queue_sha256=sha,stop_payload=payload,held=True,reused_hold=reused))
  log('HOLD-FOR-SHAPE1',host,queue_sha256=sha,reused=reused)
def release(host):
 row=json.loads((W/'hold.json').read_text())
 with (BASE/'queue.txt').open('rb') as q:
  fcntl.flock(q,fcntl.LOCK_EX);sha=hashlib.sha256(q.read()).hexdigest()
  if sha!=row['queue_sha256']:raise RuntimeError('queue changed after current hold; retain hold')
  if STOP.read_text()!=row['stop_payload']:raise RuntimeError('foreign hold; retain')
  STOP.unlink();q.seek(0)
  if hashlib.sha256(q.read()).hexdigest()!=sha:
   STOP.write_text(row['stop_payload']);raise RuntimeError('queue changed during release')
  row.update(held=False,released_utc=utc(),released_queue_sha256=sha,queue_unchanged=True)
  write_json(W/'hold.json',row);log('RELEASE-FOR-SHAPE1',host,queue_unchanged=True,queue_sha256=sha)
 gates=json.loads((ROOT/'LINUX-GATES.json').read_text());gates[host]['quiet_window']=False;write_json(ROOT/'LINUX-GATES.json',gates)
def admission(host,add):
 require_linux_gap();reg=ROOT/'REGISTRATION-FIX-4.json';frozen=safe_json(reg)
 if digest(reg)!=add['registration_sha256'] or any(digest(ROOT/k)!=v for k,v in frozen['files'].items()):raise RuntimeError('frozen files changed')
 if 'Supervisor-verified (code read + all self-tests OK). ACCEPTED.' not in (ROOT/'REVIEW-LOG.md').read_text():raise RuntimeError('FIX-4 acceptance missing')
 gates=json.loads((ROOT/'LINUX-GATES.json').read_text());gate=gates[host]
 for c in add['cells']:
  if c['host']!=host:continue
  task=c['task'];registered=next(t for t in json.loads((ROOT/'plan.json').read_text())['tasks'] if t['id']==task)
  check_task_validation(gate,task,digest(ROOT/'overlays'/f'overlay-shape-{task}.tar'),registered,digest(reg))
 excluded='c4b-2' if host=='eu' else 'c4b-5'
 if excluded in gate.get('tasks',{}):raise RuntimeError('excluded task unexpectedly passed; require reconciliation')
 for lang in ('rust','go','ts-bun'):
  reserve_json(ROOT/'attempts'/f'{excluded}-{lang}.json',dict(task=excluded,language=lang,host=host,launched=False,model_attempt=False,disposition='not-launched-mutant-validation-failed',failing_mutants=add['excluded_tasks'][excluded][lang],addendum='run2/ADDENDUM.json',**record_labels('old-descriptive')))
 disk=os.statvfs('/benchmark-root')
 if disk.f_bavail*disk.f_frsize<20*1024**3:raise RuntimeError('disk admission failed')
 gate.update(quiet_window=True,disk_admission=True,targeted_recheck_accepted=True,review_acceptance_evidence='REVIEW-LOG.md:2026-10-09T18:06:40Z',wave_addendum='run2/ADDENDUM.json',hold_evidence='run2/hold.json')
 write_json(ROOT/'LINUX-GATES.json',gates)
def main(host):
 status={'host':host,'cells':[],'complete':False,'state':'waiting-slot-boundary'};write_json(W/'status.json',status)
 add=json.loads((W/'ADDENDUM.json').read_text());held=False
 try:
  hold(host);held=True;admission(host,add)
  for c in add['cells']:
   if c['host']!=host:continue
   if (ROOT/'STOP').exists():break
   task,lang=c['task'],c['language'];rid=f's1-{host}-{task}-{lang}'
   check_gates(host,task,lang,'old-descriptive')
   status.update(state='shaping',current=rid);write_json(W/'status.json',status)
   log('SHAPE-START',host,run_id=rid,lane='old-descriptive',strict_eligible=False)
   with (W/(rid+'.stdout')).open('wb') as out,(W/(rid+'.stderr')).open('wb') as err:
    child=subprocess.Popen(['/usr/bin/python3',str(ROOT/'run_shaper.py'),host,task,lang,'--launch','--lane','old-descriptive'],stdout=out,stderr=err)
    transcript=Path('/benchmark-root/results')/rid/'codex.jsonl'
    while child.poll() is None:
     if transcript.exists() and audit_events(transcript)['flag_count']:
      (ROOT/'STOP').write_text('live transcript audit flag\n')
     time.sleep(2)
    rc=child.returncode
   control=json.loads((ROOT/'results'/rid/'old-lane-control.json').read_text())
   try:
    from collect_intent import collect
    receipt=collect(task,lang,rid,Path('/benchmark-root/results')/rid,Path('/benchmark-root/work')/rid/'repo',ROOT/'results'/rid/'intent')
    row=dict(run_id=rid,wall_seconds=control['wall_seconds'],stop_reason=control['stop_reason'],collected=True,intent_present=(ROOT/'results'/rid/'intent/repo/INTENT.md').is_file(),audit_flags=receipt['audit_flags'],launch_status=receipt['launch_status'],launcher_rc=rc,**record_labels('old-descriptive'))
   except Exception as exc:
    (ROOT/'STOP').write_text('collection failure\n')
    row=dict(run_id=rid,wall_seconds=control.get('wall_seconds'),stop_reason=control['stop_reason'],collected=False,audit_flags=control.get('audit_flags'),collection_error=type(exc).__name__,**record_labels('old-descriptive'))
   status['cells'].append(row);write_json(W/'status.json',status)
   log('SHAPE-END',host,run_id=rid,seconds=row['wall_seconds'],stop_reason=row['stop_reason'],collected=row['collected'],audit_flags=row['audit_flags'])
   if row['audit_flags'] or (ROOT/'STOP').exists():break
  status.update(complete=True,state='finished')
 except Exception as exc:
  status.update(complete=True,state='failed',error_type=type(exc).__name__)
  (W/'error.txt').write_text(str(exc)+'\n')
 finally:
  if held:
   try:release(host);status['released']=True
   except Exception as exc:status.update(released=False,release_error=type(exc).__name__)
  write_json(W/'status.json',status)
  print(json.dumps(status),flush=True)
if __name__=='__main__':main(sys.argv[1])
