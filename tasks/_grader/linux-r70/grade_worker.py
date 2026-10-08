#!/usr/bin/env python3
"""Private worker executor for MacBook-controlled R70 grade windows.
No bench grader or restore. Emit aggregate outcomes only; purge scratch in caller.
"""
import hashlib,re,json,os,pathlib,shutil,subprocess,sys,tempfile,time,xml.etree.ElementTree as ET
ROOT=pathlib.Path('/srv/bh/bench/recovery-2026-10-02'); R=ROOT/'levers/r70'
GRADER_SHA256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
sys.path.insert(0,str(ROOT/'probe-kgn/runner'))
from sandbox_linux import base_args
from dispatch import active

def now():return time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
def inventory(include_off_cohort=False):
 rows=[]
 # 7 Oct 2026 (operator, rule J): also inventory the r70 lane roots (Sol replication, L2/L3/L4); exact --cell-ids still select what is graded.
 for complete in [c for pattern in ('rec-lever-r70-*/*/*/COMPLETE.json','rec-lever-lang-sol-*/*/*/COMPLETE.json','rec-lever-l2-*/*/*/COMPLETE.json','rec-lever-l3-*/*/*/COMPLETE.json','rec-lever-l4-*/*/*/COMPLETE.json','rec-lever-l5-*/*/*/COMPLETE.json','rec-lever-l4b-*/*/*/COMPLETE.json','rec-lever-l3b/*/*/COMPLETE.json') for c in pathlib.Path('/srv/bh/bench/results').glob(pattern)]:
  cell=complete.parent;m=json.loads((cell/'manifest.json').read_text());req=m['requested']
  selected=re.fullmatch(r'r70-rve-eu-[1346]-(?:rust|elixir)-gpt-6-luna-r(\d+)',m['experiment'])
  off_cohort=bool(selected and req['rep']!=int(selected[1]))
  if off_cohort and not include_off_cohort:continue  # diagnostic only, never scored

  stack=req['task'].split('-',2)[2]
  if stack.endswith('-fe2'):stack=stack[:-4]
  stack=next((k for k in ('ts-bun','elixir','rust','gleam','go') if stack==k or stack.startswith(k+'-')),stack)  # lane variant suffixes (-l3r31, -fe2-l2steps, ...)
  rows.append(dict(off_cohort=off_cohort,round_id='r70-rve' if m['experiment'].startswith('r70-rve-') else 'r70',cell=str(cell),cell_id=m['cell_id'],experiment=m['experiment'],task=req['task'],stack=stack,model=req['model'],rep=req['rep'],effort=req['effort'],patch=str(cell/m['artifacts']['patch']),started_at=m['started_at'],finished_at=m['ended_at'],runner_status=m['status'],runner_error_class=m.get('error_class'),sandbox=m.get('sandbox'),wall_s=m.get('wall_s'),usage=m.get('usage'),observed=m.get('observed'),prompt_sha256=m.get('prompt_sha256'),wrapper=m.get('wrapper'),runner=m.get('runner'),manifest_sha256=hashlib.sha256((cell/'manifest.json').read_bytes()).hexdigest(),base_sha=m.get('workdir',{}).get('base_sha'),host_metadata=m.get('host'),cli_version=m.get('cli_version')))
 return rows

def grade(job,window):
 start=time.monotonic();row={k:v for k,v in job.items() if k not in ['patch','sandbox','reference_source']};row.update(grader_sha256=GRADER_SHA256,grade_started_at=now(),outcome='invalid',cause=None,tests_passed=0,tests_total=0,tests_ran=False,make_check=None,build_ok=False)
 scratch=pathlib.Path(tempfile.mkdtemp(prefix='cell-',dir=window));scratch.chmod(0o700)
 (scratch/'home').mkdir()
 project=scratch/'project';td=ROOT/'new-tasks'/job['task'];meta=json.loads((td/'task.json').read_text())
 env={**os.environ,'RUSTUP_HOME':'/opt/bench/rustup','CARGO_NET_OFFLINE':'true','GOTOOLCHAIN':'local','GOCACHE':str(scratch/'go-cache'),'HOME':str(scratch/'home'),**meta['env'],'GIT_CONFIG_GLOBAL':'/dev/null','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_COUNT':'1','GIT_CONFIG_KEY_0':'safe.directory','GIT_CONFIG_VALUE_0':'*'}
 def run(argv,label,hidden=False):
  args=base_args()+['--ro-bind','/srv/bh/bench/toolchains','/srv/bh/bench/toolchains','--bind',str(scratch),str(scratch)]
  if hidden:args+=['--ro-bind',str(window/'suites'),str(window/'suites')]
  args+=['--remount-ro','/','--chdir',str(project)]
  with (scratch/(label+'.log')).open('wb') as f:
   try:p=subprocess.run(args+argv,env=env,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,timeout=900);return p.returncode
   except subprocess.TimeoutExpired:return 124
 try:
  if active():raise RuntimeError('cell started inside grade window')
  variant=job.get('variant')
  source_task=job.get('reference_source_task',job['task'])
  source_td=ROOT/'new-tasks'/source_task
  source_meta=json.loads((source_td/'task.json').read_text())
  reference_variant=variant in {'reference','reference-skeleton-frontend','reference-core-fixed-frontend'}
  reference_base=job.get('reference_base_sha') or source_meta.get('base_sha')
  patch=pathlib.Path(job['patch']) if job.get('patch') else None
  if patch and not patch.is_file():row['cause']='patch_missing';return row
  def archive(source_root,revision,destination):
   destination.mkdir()
   result=subprocess.run(['git','-C',str(source_root),'archive',revision],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,env=env)
   if result.returncode:raise RuntimeError('public archive failed')
   subprocess.run(['tar','-x','-C',str(destination)],input=result.stdout,check=True,stderr=subprocess.DEVNULL)
  def install_reference(destination):
   if job.get('reference_source'):
    if not reference_variant:raise RuntimeError('reference source on a non-reference control')
    shutil.copytree(job['reference_source'],destination,dirs_exist_ok=True)
   if patch and patch.stat().st_size:
    # The documented MacBook route stages this patch; application stays in private scratch.
    result=subprocess.run(['git','apply','--whitespace=nowarn',str(patch)],cwd=destination,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    if result.returncode:raise RuntimeError('reference patch did not apply to its registered base')
  if variant=='reference-core-fixed-frontend':
   archive(td/'skeleton',meta['base_sha'],project)
   reference_project=scratch/'reference-project'
   archive(source_td/'skeleton',reference_base,reference_project)
   install_reference(reference_project)
   core_files=job.get('core_files') or []
   if not core_files:raise RuntimeError('fixed-frontend control has no registered core files')
   for name in core_files:
    relative=pathlib.Path(name)
    if relative.is_absolute() or '..' in relative.parts:raise RuntimeError('unsafe core path in fixed-frontend control')
    source_file=reference_project/relative;target_file=project/relative
    if source_file.is_symlink() or not source_file.is_file():raise RuntimeError('registered reference core file missing')
    target_file.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source_file,target_file)
   row['reference_core_files']=core_files
   row['frontend_source']='unmodified-fixed-public-skeleton-entrypoint'
  elif variant in {'reference','reference-skeleton-frontend'}:
   archive(source_td/'skeleton',reference_base,project)
   install_reference(project)
  else:
   archive(td/'skeleton',meta['base_sha'],project)
   # Contestant cells: apply the delivered patch to the public base (restored 6 Oct 2026; it was dropped in a refactor).
   if patch and patch.stat().st_size:
    result=subprocess.run(['git','apply','--whitespace=nowarn',str(patch)],cwd=project,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    if result.returncode:row['cause']='patch_apply';return row
    row['contestant_patch_applied']=True
  # Registered private reference files were hardened after patch generation.
  # Go's calibration patch consequently carries non-executable private modes.
  # Restore only the admitted reference launch/setup permissions, never a cell's.
  if reference_variant:
   if job['stack']=='ts-bun':
    # Re-control the original solution under the repaired strict typing contract.
    for name in ['package.json','tsconfig.json','setup.sh']:
     shutil.copy2(td/'skeleton'/name,project/name)
    (project/'src/runtime.d.ts').unlink(missing_ok=True)
    row['reference_typing_contract']='repaired-public-bun-types'
   row['reference_base_sha']=reference_base
   row['public_base_sha']=meta['base_sha']
   if variant=='reference-skeleton-frontend':
    base_run=td/'skeleton'/'run';project_run=project/'run'
    if base_run.is_symlink() or not base_run.is_file() or project_run.is_symlink():raise RuntimeError('public skeleton launcher is not a regular file')
    shutil.copy2(base_run,project_run)
    row['frontend_source']='unmodified-public-skeleton-run'
   restored=[]
   for name in ['setup.sh','run','run-hidden']:
    path=project/name
    if path.is_symlink():raise RuntimeError('reference executable is a symlink')
    if not path.stat().st_mode & 0o111:path.chmod(path.stat().st_mode | 0o700);restored.append(name)
   row['calibration_exec_modes_restored']=restored
  row['setup_rc']=run(['./setup.sh'],'setup')
  row['build_rc']=run(['make','build'],'build');row['build_ok']=row['build_rc']==0
  row['make_check_rc']=run(['make','check'],'check');row['make_check']=row['make_check_rc']==0
  # Hidden harness is public but trusted; use its frozen base version.
  wrapper=project/'run-hidden'
  if wrapper.is_symlink():wrapper.unlink()  # never follow a contestant link outside scratch
  elif wrapper.exists() and not wrapper.is_file():shutil.rmtree(wrapper)
  shutil.copy2(td/'skeleton/run-hidden',wrapper)
  report=scratch/'junit.xml';tasknum=job['task'].split('-')[1]
  # Suite mounted only for this offline test invocation, after build/check.
  suite_path=window/'suites'/f'task-{tasknum}.py'
  row['collection_rc']=run(['./run-hidden','--collect-only',str(suite_path)],'collection',True)
  counts=re.findall(r'(\d+) tests? collected', (scratch/'collection.log').read_text(errors='replace'))
  expected=int(counts[-1]) if counts and row['collection_rc']==0 else 0
  suite_hash=hashlib.sha256(suite_path.read_bytes()).hexdigest()
  row.update(tests_expected=expected,expected_count_source='sealed-suite-pytest-collection',suite_sha256=suite_hash)
  registration=ROOT/'levers/r70-rve/rerun/suite-registration.json'
  if registration.is_file() and job['task'] in json.loads(registration.read_text()).get('variants',{}):
   registered=json.loads(registration.read_text())['variants'][job['task']]
   if suite_hash!=registered.get('suite_sha256'):
    row['cause']='suite_hash_mismatch';return row
   if expected!=registered.get('tests'):
    row['cause']='registered_suite_count_mismatch';return row
  if expected<=0:row['cause']='hidden_collection_invalid';return row
  row['hidden_rc']=run(['./run-hidden','--junitxml',str(report),str(window/'suites'/f'task-{tasknum}.py')],'hidden',True)
  if not report.exists():row['cause']='hidden_report_missing';return row
  suites=ET.parse(report).getroot().findall('testsuite')
  # Sanitized diagnostic export: names only, never failure message/body.
  row['failed_test_names']=sorted({t.attrib.get('name','unknown') for suite in suites for t in suite.findall('testcase') if t.find('failure') is not None or t.find('error') is not None})
  total=sum(int(s.attrib['tests']) for s in suites);fails=sum(int(s.attrib['failures']) for s in suites);errors=sum(int(s.attrib['errors']) for s in suites);skips=sum(int(s.attrib['skipped']) for s in suites)
  row.update(tests_total=total,tests_passed=total-fails-errors-skips,tests_errors=errors,tests_skipped=skips,tests_ran=total==expected and errors==0 and skips==0)
  if not row['tests_ran'] or row['hidden_rc'] not in [0,1]:row['cause']='hidden_execution_invalid'
  else:row.update(outcome='pass' if fails==0 and row['hidden_rc']==0 else 'fail',cause=None if fails==0 else 'hidden_tests_failed')
  if not row['build_ok']:row.update(outcome='fail',cause='build_failed')
  elif row['setup_rc']:row.update(outcome='fail',cause='setup_failed')
  # ITT retains runner timeouts/errors as failures even if a partial patch passes.
  if job.get('runner_status') not in [None,'ok'] and row['outcome']=='pass':row.update(outcome='fail',cause='runner_'+job['runner_status'])
 except Exception as e:row['cause']='infra_'+type(e).__name__
 finally:
  categories={'rustup_toolchain':'no default toolchain','missing_home':'could not find cargo home','permission':'Permission denied','readonly':'Read-only file system','toolchain_fetch':'toolchain','executable':'not executable','module_missing':'no required module','command_missing':'not found','path_missing':'No such file or directory','cwd_mismatch':'go.mod file not found'}
  row['diagnostics']={label:[name for name,pattern in categories.items() if pattern.lower() in (scratch/(label+'.log')).read_text(errors='replace').lower()] for label in ['setup','build','check'] if (scratch/(label+'.log')).exists()}
  # Operator diagnostics contain categories/counts only, never source excerpts,
  # filenames from a reference, compiler messages, or hidden-suite diagnostics.
  if (scratch/'check.log').exists():
   check=(scratch/'check.log').read_text(errors='replace')
   row['check_failure_summary']={'typescript_error_codes':{code:len(re.findall(r'error '+code+r'\b',check)) for code in sorted(set(re.findall(r'error (TS\d+)\b',check)))},'formatter_failure':'Formatter would have printed' in check,'biome_invoked':'biome check' in check,'bun_test_invoked':'bun test' in check}
  row.update(grade_wall_s=round(time.monotonic()-start,3),grade_finished_at=now());shutil.rmtree(scratch)
 return row

if __name__=='__main__':
 if sys.argv[1] in ['inventory','inventory-with-off-cohort']:print(json.dumps(inventory(sys.argv[1]=='inventory-with-off-cohort')))
 else:
  window=pathlib.Path(sys.argv[1]);assert window.name.startswith('r70-window-') and window.stat().st_mode & 0o777==0o700
  assert not active();jobs=json.loads((window/'jobs.json').read_text())
  for job in jobs:
   row=grade(job,window)
   with (window/'outcomes.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
   print(json.dumps(row),flush=True)
