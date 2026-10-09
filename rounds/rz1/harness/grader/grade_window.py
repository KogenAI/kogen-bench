#!/usr/bin/env python3
"""MacBook controller: stop launches, drain, stage own R70 suites, grade, purge, resume."""
import argparse,fcntl,json,os,pathlib,re,shlex,subprocess,sys,time
HERE=pathlib.Path(__file__).resolve().parent;ROOT='public-source-location-withheld';REMOTE=ROOT+'/levers/r70';PY='/opt/bench/mise/installs/python/3.14.7/bin/python3'
def ssh(host,cmd,retry=True,**kw):
 for attempt in range(4 if retry else 1):
  try:return subprocess.run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=15','-o','ServerAliveInterval=15','-o','ServerAliveCountMax=3',host,cmd],check=True,**kw)
  except subprocess.CalledProcessError as e:
   if e.returncode!=255 or not retry or attempt==3:raise
   time.sleep(2)

def output(host,cmd):return ssh(host,cmd,capture_output=True,text=True).stdout

def inventory(host,include_off_cohort=False):return json.loads(output(host,f"{PY} {REMOTE}/grade_worker.py {'inventory-with-off-cohort' if include_off_cohort else 'inventory'}"))
def recorded():
 with (HERE/'grades-append.lock').open('a') as guard:
  fcntl.flock(guard,fcntl.LOCK_SH)
  p=HERE/'grades.jsonl';return {r['cell'] for line in p.read_text().splitlines() if line for r in [json.loads(line)]} if p.exists() else set()
def pending(host):return [x for x in inventory(host) if x['cell'] not in recorded()]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('host',choices=['kogen-bench-eu','kogen-bench-us']);ap.add_argument('--calibrate',action='store_true');ap.add_argument('--count',action='store_true');ap.add_argument('--regrade',action='store_true');ap.add_argument('--admission-controls',action='store_true');ap.add_argument('--skeleton-frontend-controls',action='store_true',help='Add one reference-core control per task/stack while restoring the public skeleton run launcher');ap.add_argument('--fixed-variants',default='',help='Run noop, reference, and reference-core-fixed-frontend controls for these fixed public task IDs');ap.add_argument('--cell-ids',default='',help='Grade only these exact full native cell IDs from the pending inventory');ap.add_argument('--controls-only',action='store_true');ap.add_argument('--smokes-only',action='store_true');ap.add_argument('--tasks',default='1,2,3,4');ap.add_argument('--pairs',default='');ap.add_argument('--include-experiments',default='',help='Also regrade these completed public-patch contexts in this same exclusive window');a=ap.parse_args();host=a.host;short=host.rsplit('-',1)[1]
 if a.skeleton_frontend_controls and not (a.admission_controls and a.controls_only):raise SystemExit('--skeleton-frontend-controls requires --admission-controls --controls-only')
 if a.fixed_variants and not (a.admission_controls and a.controls_only):raise SystemExit('--fixed-variants requires --admission-controls --controls-only')
 if a.cell_ids and a.admission_controls:raise SystemExit('--cell-ids cannot be combined with admission controls')
 if a.count:print(len(pending(host)));return
 lock=(HERE/f'grade-{short}.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 stop=f'{REMOTE}/STOP-{short}';window=None;purged=False;was_stopped=False
 try:
  # Take the same flock as launcher before publishing STOP.
  script=f"import fcntl,pathlib; p=pathlib.Path('{REMOTE}'); f=(p/'launch-{short}.lock').open('a'); fcntl.flock(f,fcntl.LOCK_EX); s=p/'STOP-{short}'; print(int(s.exists())); s.touch()"
  was_stopped=output(host,f'{PY} -c {shlex.quote(script)}').strip()=='1'
  while True:
   n=int(output(host,f"{PY} -c {shlex.quote('import sys;sys.path.insert(0,'+repr(REMOTE)+');from dispatch import active;print(len(active()))')}"))
   if n==0:break
   print(f'{host}: draining {n} live cells',flush=True);time.sleep(10)
  jobs=[] if a.controls_only else (inventory(host) if a.regrade else pending(host))
  if short=='eu' and not a.smokes_only and any(j['experiment'].startswith('r70-rve-eu-') for j in jobs) and not a.include_experiments:
   a.include_experiments='r70-eu-6-elixir-gpt-6-luna-r2,r70-eu-6-elixir-gpt-6-luna-r3'
  if a.include_experiments:
   selected=set(a.include_experiments.split(','));extra=[j for j in inventory(host) if j['experiment'] in selected];assert {j['experiment'] for j in extra}==selected, 'Requested context incomplete'
   present={j['cell'] for j in jobs};jobs.extend(j for j in extra if j['cell'] not in present)
  if a.smokes_only:jobs=[j for j in jobs if j['experiment'].endswith('-smoke')]
  if a.admission_controls:
   pairs=[] if a.fixed_variants and not a.pairs else [(task,stack) for task in map(int,a.tasks.split(',')) for stack in ['rust','go','ts-bun','elixir','gleam']]
   if a.pairs:pairs=[(int(p.split(':',1)[0]),p.split(':',1)[1]) for p in a.pairs.split(',')]
   for task,stack in pairs:
    for rep in [1,2]:
     for variant in ['reference','noop']:
      id=f'r70-{task}-{stack}';jobs.append(dict(cell=f'admission-fixed-{short}-{id}-{variant}-r{rep}',cell_id=f'admission-fixed-{id}-{variant}-r{rep}',experiment='admission-fixed',task=id,stack=stack,model='control',rep=rep,variant=variant,patch=None))
    if a.skeleton_frontend_controls:
     id=f'r70-{task}-{stack}';variant='reference-skeleton-frontend';jobs.append(dict(cell=f'admission-fixed-{short}-{id}-{variant}',cell_id=f'admission-fixed-{id}-{variant}',experiment='admission-fixed',task=id,stack=stack,model='control',rep=1,variant=variant,patch=None))
   if a.fixed_variants:
    core_paths={'1:elixir':['lib/core.ex'],'4:rust':['src/core.rs'],'4:elixir':['lib/core.ex'],'4:go':['core.go'],'4:ts-bun':['src/core.ts']}
    for fixed_id in [x.strip() for x in a.fixed_variants.split(',') if x.strip()]:
     match=re.fullmatch(r'r70-(1|4)-(rust|elixir|go|ts-bun)-fe2',fixed_id) or re.fullmatch(r'r70-(8)-(rust|go)-v2',fixed_id)
     if not match:raise SystemExit('invalid fixed task ID: '+fixed_id)
     tasknum,stack=match.group(1),match.group(2);source_task=f'r70-{tasknum}-{stack}'
     # Task-8 v2 (6 Oct 2026) changes only prompt.md; the skeleton is unchanged, so there is no fixed-front-end control.
     for rep in [1]:
      for variant in (['reference','noop'] if fixed_id.endswith('-v2') else ['reference','noop','reference-core-fixed-frontend']):
       job=dict(cell=f'admission-fixed-{short}-{fixed_id}-{variant}-r{rep}',cell_id=f'admission-fixed-{fixed_id}-{variant}-r{rep}',experiment='admission-fixed',task=fixed_id,stack=stack,model='control',rep=rep,variant=variant,patch=None)
       if variant in ['reference','reference-core-fixed-frontend']:job['reference_source_task']=source_task
       if variant=='reference-core-fixed-frontend':job['core_files']=core_paths[f'{tasknum}:{stack}']
       jobs.append(job)
  if a.cell_ids:
   requested=[x.strip() for x in a.cell_ids.split(',') if x.strip()]
   full_id=re.compile(r'[A-Za-z0-9._:-]+(?:__[A-Za-z0-9._:-]+){4}__r[0-9]+')
   if not requested or len(requested)!=len(set(requested)) or any(not full_id.fullmatch(x) for x in requested):raise SystemExit('--cell-ids requires unique full native cell IDs')
   available={j['cell_id']:j for j in jobs}
   missing=[x for x in requested if x not in available]
   if missing:raise SystemExit('requested cell IDs are not all pending on '+host+': '+','.join(missing))
   jobs=[available[x] for x in requested]
  if a.calibrate:
   for variant in ['reference','noop']:
    for task,stack in [(7,'rust'),(6,'go')]:
     id=f'r70-{task}-{stack}';jobs.append(dict(cell=f'calibration-{short}-{id}-{variant}',cell_id=f'calibration-{id}-{variant}',experiment='calibration',task=id,stack=stack,model='control',rep=1,variant=variant,patch=None))
  if not jobs:return
  window=output(host,f'umask 077; mktemp -d public-source-location-withheld').strip()
  ssh(host,f'mkdir -m 700 {window}/suites')
  for task in sorted({x['task'].split('-')[1] for x in jobs}):
   src=pathlib.Path.home()/f'bench-sealed/synthetic/tasks/r70-{task}-rust/sealed/test_hidden.py'
   # Copy via the documented admission route; never inspect suite bytes.
   subprocess.run(['scp','-q','-o','BatchMode=yes','-o','ConnectTimeout=15',str(src),f'{host}:{window}/suites/task-{task}.py'],check=True)
  uploaded={}
  versions=HERE/'fairness-version-changes.json'
  old_bases={r['task_id']:r['before']['base_sha'] for r in json.loads(versions.read_text())['changes']} if versions.exists() else {}
  for j in jobs:
   if j.get('variant') in {'reference','reference-skeleton-frontend','reference-core-fixed-frontend'}:
    source_task=j.get('reference_source_task',j['task'])
    j['reference_source_task']=source_task
    j['reference_base_sha']=old_bases.get(source_task)
    if source_task in uploaded:j.update(uploaded[source_task]);continue
    src=pathlib.Path.home()/f"bench-sealed/synthetic/tasks/{source_task}/sealed/reference.patch"
    if src.is_file():
     target=f"{window}/{source_task}-reference.patch";subprocess.run(['scp','-q','-o','BatchMode=yes','-o','ConnectTimeout=15',str(src),f'{host}:{target}'],check=True);j['patch']=target;uploaded[source_task]={'patch':target}
    else:
     source=src.parent/'reference';assert source.is_dir()
     if not (source/'Makefile').is_file():source=source/j['stack']
     if not (source/'Makefile').is_file():source=source/source_task
     assert (source/'Makefile').is_file(), 'Registered reference project root missing'
     target=f"{window}/{source_task}-reference"
     subprocess.run(['rsync','-a','--exclude=.git','--exclude=target','--exclude=_build','--exclude=deps','--exclude=node_modules','--exclude=build','--exclude=.cache','--exclude=.zig-cache','--exclude=zig-out','--exclude=control-env.json',str(source)+'/',f'{host}:{target}/'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);j['reference_source']=target;uploaded[source_task]={'reference_source':target}
  jobfile=HERE/f'.jobs-{short}.json';jobfile.write_text(json.dumps(jobs));subprocess.run(['scp','-q','-o','BatchMode=yes','-o','ConnectTimeout=15',str(jobfile),f'{host}:{window}/jobs.json'],check=True);jobfile.unlink()
  print(f'{host}: grading {len(jobs)} jobs',flush=True)
  ssh(host,f'flock -x public-source-location-withheld nice -n 10 {PY} {REMOTE}/grade_worker.py {window}',retry=False,stdout=subprocess.DEVNULL)
  # Only aggregate outcomes leave private scratch; test output never does.
  lines=output(host,f'cat {window}/outcomes.jsonl').splitlines();assert len(lines)==len(jobs)
  records=[dict(json.loads(x),host=host,grade_route='r70-macbook-window-v1') for x in lines]
  ssh(host,f'rm -rf -- {window}; test ! -e {window}');purged=True
  with (HERE/'grades-append.lock').open('a') as guard:
   fcntl.flock(guard,fcntl.LOCK_EX)
   with (HERE/'grades.jsonl').open('a') as f:
    for row in records:row['sealed_scratch_purged']=True;f.write(json.dumps(row)+'\n')
  receipt=dict(at=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),host=host,jobs=len(jobs),purged=True,records=[dict(cell=r['cell'],outcome=r['outcome'],tests_total=r['tests_total'],tests_ran=r['tests_ran'],cause=r['cause']) for r in records])
  with (HERE/'windows.jsonl').open('a') as f:f.write(json.dumps(receipt)+'\n')
  (HERE/f'last-window-{short}').write_text(str(time.time()))
  print(json.dumps(receipt),flush=True)
 finally:
  if window and not purged:
   try:ssh(host,f'rm -rf -- {window}; test ! -e {window}');purged=True
   except Exception:print('PURGE FAILED; dispatcher remains stopped',file=sys.stderr)
  if (window is None or purged) and not was_stopped:ssh(host,f'rm -f -- {stop}')
if __name__=='__main__':main()
