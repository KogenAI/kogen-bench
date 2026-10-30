import argparse,datetime,hashlib,json,os,pathlib,random,shutil,subprocess,sys,time,traceback
R=pathlib.Path(os.environ.get('LANES_CONFIRM_DIR') or os.path.expanduser('~/lanes-work/confirmation-eu-20261029'))
CODEX_DIR=os.environ.get('CODEX_BIN_DIR') or os.path.expanduser('~/.codex/packages/standalone/releases/0.165.0-x86_64-unknown-linux-musl/bin')
GO_ROOT=os.environ.get('LANES_GOROOT') or os.path.expanduser('~/.local/share/mise/installs/go/1.27.2')
NODE_ROOT=os.environ.get('LANES_NODEROOT') or os.path.expanduser('~/.local/share/mise/installs/node/24.21.0')
os.chdir(R)
os.environ.update(LANES_DIR=str(R/'grader'),PATH=GO_ROOT+'/bin:'+NODE_ROOT+'/bin:'+os.path.expanduser('~/.local/bin')+':/usr/bin:/bin',GOMAXPROCS='2',GOPROXY='off',GOTOOLCHAIN='local')
sys.path[:0]=[str(R/'harness'),str(R)]
import lanes_bare as h
import confirmation_ext as e
e.install(h)
SEED=20261029

def dump(p,d):e.write(p,d)
def fingerprints():
 from lanes import common
 codex=pathlib.Path(CODEX_DIR)
 return {'tasks':{n:common.sha256_tree(str(R/'tasks'/n)) for n in ['artifact-go','readtime-go','cron-go','vm-go','r70-1-go']},'cache':common.sha256_tree(str(R/'cache-snapshot')),'grader_source':common.sha256_tree(str(R/'grader'),exclude=('.git','__pycache__')),'loop_source':common.sha256_tree(str(R/'source/kogen-loop'),exclude=('.git','__pycache__')),'binaries':{str(p):common.sha256_file(str(p)) for p in [R/'bin/loop-b8a4046',codex/'codex',codex/'codex-code-mode-host']},'shell_wrapper':common.sha256_file(str(R/'tool-shell.py')),'extension':common.sha256_file(str(R/'confirmation_ext.py')),'harness':common.sha256_file(str(R/'harness/lanes_bare.py')),'driver':common.sha256_file(str(R/'run_confirmation.py'))}

def freeze():
 rng=random.Random(SEED);tasks=['artifact-go','readtime-go','cron-go','vm-go'];rng.shuffle(tasks)
 cells=[]
 for rep in (1,2):
  order=list(tasks)
  if rep==2:rng.shuffle(order)
  for t in order:
   i=tasks.index(t);arms=['loop','codex'] if (i<2)==(rep==1) else ['codex','loop']
   for arm in arms:cells.append({'task':t,'rep':rep,'arm':arm,'stratum':'counted'})
 protocol={'frozen_utc':e.stamp(),'infrastructure_pilots':['dry/cells/r70-1-go/r1/loop: adapter idle and grader staging; receipts retained','dry/cells/r70-1-go/r1/codex: missing code-mode helper and gateway serialization; receipts retained','dry/cells/r70-1-go/r2/loop and codex: pre-final runtime/byte guard; both archives pass, Codex completion guard hit; receipts retained'],'seed':SEED,'tasks_randomized':tasks,'cells':cells,'dry':[{'task':'r70-1-go','rep':3,'arm':a,'stratum':'dry'} for a in ('loop','codex')],'host':'Linux host, 2 cores','host_lock':'research-confirm held externally; never acquire or release','model':e.MODEL,'effort':'high','upstream_endpoint':'https://api.openai.com/v1/responses','route':'frozen external authentication gateway; loop shipped openai-compatible Chat wire translated to Responses; Codex Responses passthrough','instructions':'loop shipped DefaultInstructions (instructions empty); Codex shipped instructions, user config and rules ignored','cap_usd':15,'per_cell_hard_cap_usd':e.CELL_CAP,'max_request_bytes':e.MAX_BYTES,'max_output_tokens':e.MAX_OUTPUT,'max_upstream_retries':0,'cell_deadline':'default 3600s, shortened only to existing lease expiry minus 30s; no cell starts with less than 600s remaining','cache':'identical dedicated prebuilt standard-library GOCACHE snapshot restored before every cell; no hidden-test artifacts','containment':'outer bubblewrap mount/user/PID/IPC/UTS namespaces, only workspace and read-only toolchains; credentials external; generated shell tools enter nested user/PID/network namespace; Codex internal sandbox replaced by identical external boundary','grading':'unchanged Studio lanes grader; final-tree.tar exported and graded outside namespace','analysis':'all attempts retained, no automatic replacement; per-task arithmetic means over two reps; repeat stratum separately; medians and nearest-rank p90 over graded launched attempts; cost/pass and tokens/pass over all launched attempts; unstarted distinct from ungraded; small descriptive confirmation, no non-inferiority claim','exposure_limit':'current specs/results audited on Studio, MacBook, EU and EU2; prior laptop inventory reused because host unreachable; historical overwritten specs not recoverable','attestation':fingerprints(),'files_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'confirmation_ext.py',R/'run_confirmation.py',R/'harness/lanes_bare.py',R/'harness/pubmetrics.py',R/'bin/loop-b8a4046']}}
 path=R/'protocol.json'
 if not path.exists():dump(path,protocol)
 return json.loads(path.read_text())

def make_args(c,run):
 return argparse.Namespace(tasks=str(R/'tasks'),task=c['task'],arm=c['arm'],run_dir=str(run),rep=c['rep'],lane=c['arm'],model=e.MODEL,effort='high',provider='openai-compatible',loop_instructions=None,home=str(R/'empty-login'),codex_home=str(R/'empty-codex'),loop_bin=str(R/'bin/loop-b8a4046'),codex_bin=CODEX_DIR+'/codex',intent_form='gherkin',deadline_s=h.DEADLINE_S,force=False,keep=False,no_grade=False,cpu_profile=True,host='EU',kogen_models=None)

def host_check():
 assert pathlib.Path('/run/kogen-host-lock.d/owner').read_text().strip()=='research-confirm'
 expires=float(pathlib.Path('/run/kogen-host-lock.d/expires').read_text().strip())
 if time.time()+600>expires:raise RuntimeError('less than ten minutes remain in existing owner lease')
 rows=subprocess.check_output(['ps','-u',os.environ.get('LANES_USER') or os.environ['USER'],'-o','pid=,ppid=,pgid=,comm=,args='],text=True)
 own={os.getpid(),os.getppid()};busy=[]
 for line in rows.splitlines():
  x=line.strip().split(None,4)
  if len(x)<5:continue
  pid,ppid,pgid,comm,args=x
  if int(pid) in own or comm in ('ps','bash','sh') and int(ppid) in own:continue
  if any(z in comm for z in ('kogen','codex','compile','link')) or comm in ('go','node','npm','npx') or ('python' in comm and 'run_confirmation.py' not in args):busy.append(line)
 if busy:raise RuntimeError('other lanes/build process active: '+repr(busy))
 return {'utc':e.stamp(),'load_1m':os.getloadavg()[0],'processes':rows,'lock_owner':'research-confirm','lock_expires':expires,'own_pid':os.getpid(),'own_pgid':os.getpgrp()}

def launched():
 rows=[]
 for p in R.glob('*/cells/*/r*/*/route-summary.json'):
  d=json.loads(p.read_text());rows.append(d)
 return sum(x['usd_list'] if x.get('all_usage_present') else x['charge_upper_bound_usd'] for x in rows)

def cell(c):
 run=R/c['stratum'];out=run/'cells'/c['task']/('r'+str(c['rep']))/c['arm']
 if (out/'result.json').exists():raise RuntimeError('cell already exists; never auto-replace')
 spent=launched()
 if spent+e.CELL_CAP+0.000039>15:raise RuntimeError('next cell may exceed total $15 cap')
 receipt=host_check()
 frozen=json.loads((R/'protocol.json').read_text())
 if fingerprints()!=frozen['attestation']:raise RuntimeError('frozen source, binary, task or cache changed')
 dump(R/('next-cell-'+c['stratum']+'.json'),{'cell':c,'host_preflight':receipt,'prior_spend_upper_bound_usd':spent,'reserved_cell_cap_usd':e.CELL_CAP})
 result=h.run_cell(make_args(c,run))
 dump(out/'host-preflight.json',receipt)
 after_verified=fingerprints()==frozen['attestation']
 dump(out/'provenance.json',{'protocol_sha256':hashlib.sha256((R/'protocol.json').read_bytes()).hexdigest(),'before_verified':True,'after_verified':after_verified})
 if not after_verified:raise RuntimeError('post-cell provenance changed')
 route=json.loads((out/'route-summary.json').read_text()) if (out/'route-summary.json').exists() else None
 with (R/'cell-ledger.jsonl').open('a') as f:f.write(json.dumps({'utc':e.stamp(),'cell':c,'result_path':str(out/'result.json'),'outcome':result.get('outcome'),'all_passed':result.get('all_passed'),'route':route})+'\n')
 print(json.dumps({'cell':c,'outcome':result.get('outcome'),'passed':result.get('all_passed'),'agent_wall':result.get('totals',{}).get('wall_s'),'route':route}),flush=True)
 if any(any(z in error for z in ('413','429','confirmation_guard','failed to spawn','permission denied')) for error in result.get('errors',[])):raise RuntimeError('runtime or API guard failure; no replacement')
 if result.get('outcome') in ('harness_error','timeout') or not route or route['stop_reason'] or not route['all_usage_present'] or not route['response_models'] or set(route['response_models'])!={e.MODEL}:raise RuntimeError('cell failed infrastructure/route/usage gate; no replacements')
 if c['stratum']=='dry' and result.get('outcome') not in ('finished','agent_error'):raise RuntimeError('dry cell not ready')
 return result

def preflight_only(c):
 import tempfile
 task=R/'tasks'/c['task'];tt,_,_=h.load_task_inputs(str(task),'gherkin')
 tmp=tempfile.mkdtemp(prefix='confirmation-boundary-');ws=str(pathlib.Path(tmp)/'ws')
 try:
  h.make_bare_workspace(ws,tmp,str(task),'gherkin',tt)
  e.STATE['task']=c['task']
  out=R/'preflight'/c['arm'];out.mkdir(parents=True,exist_ok=True)
  e.probe(tmp,str(out),c['arm'],h.agent_env(tt,tmp,{}))
  print('Boundary passed: '+c['arm'],flush=True)
 finally:shutil.rmtree(tmp)

p=argparse.ArgumentParser();p.add_argument('mode',choices=['preflight','dry-loop','dry-codex','counted']);a=p.parse_args();protocol=freeze()
try:
 if a.mode=='preflight':
  for c in protocol['dry']:preflight_only(c)
 elif a.mode.startswith('dry-'):cell(next(c for c in protocol['dry'] if c['arm']==a.mode[4:]))
 else:
  for c in protocol['cells']:cell(c)
 dump(R/('status-'+a.mode+'.json'),{'utc':e.stamp(),'state':'complete','mode':a.mode,'spend_upper_bound_usd':launched()})
except Exception as ex:
 dump(R/('status-'+a.mode+'.json'),{'utc':e.stamp(),'state':'stopped','mode':a.mode,'error':str(ex),'traceback':traceback.format_exc(),'spend_upper_bound_usd':launched()})
 print(type(ex).__name__+': '+str(ex),file=sys.stderr);sys.exit(2)
