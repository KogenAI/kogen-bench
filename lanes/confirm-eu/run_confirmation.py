import argparse,datetime,hashlib,json,os,pathlib,random,shutil,subprocess,sys,time,traceback
R=pathlib.Path(os.environ.get('LANES_CONFIRM_DIR') or os.path.expanduser('~/lanes-work/confirmation-eu-replay-20261030'))
CODEX_DIR=os.environ.get('CODEX_BIN_DIR') or os.path.expanduser('~/.codex/packages/standalone/releases/0.165.0-x86_64-unknown-linux-musl/bin')
GO_ROOT=os.environ.get('LANES_GOROOT') or os.path.expanduser('~/.local/share/mise/installs/go/1.27.2')
NODE_ROOT=os.environ.get('LANES_NODEROOT') or os.path.expanduser('~/.local/share/mise/installs/node/24.21.0')
os.chdir(R)
os.environ.update(LANES_DIR=str(R/'grader'),PATH=GO_ROOT+'/bin:'+NODE_ROOT+'/bin:'+os.path.expanduser('~/.local/bin')+':/usr/bin:/bin',GOMAXPROCS='2',GOPROXY='off',GOTOOLCHAIN='local')
sys.path[:0]=[str(R/'harness'),str(R)]
import lanes_bare as h
import confirmation_ext as e
e.install(h)
PROTOCOL_PATH=R/'protocol.json'
SEED=2026102908
ARMS=['loop-default','api-replay','codex']
BIN={a:R/'bin'/('scr-api-replay-kogen-loop' if a=='api-replay' else 'loop-b8a4046') for a in ARMS}
def dump(p,d):e.write(p,d)
def fingerprints():
 from lanes import common
 codex=pathlib.Path(CODEX_DIR)
 return {'tasks':{n:common.sha256_tree(str(R/'tasks'/n)) for n in sorted(p.name for p in (R/'tasks').iterdir())},'cache':common.sha256_tree(str(R/'cache-snapshot')),'grader_source':common.sha256_tree(str(R/'grader'),exclude=('.git','__pycache__')),'loop_source':common.sha256_tree(str(R/'source/kogen-loop'),exclude=('.git','__pycache__')),'binaries':{str(p):common.sha256_file(str(p)) for p in [R/'bin/loop-b8a4046',R/'bin/scr-api-replay-kogen-loop',codex/'codex',codex/'codex-code-mode-host']},'shell_wrapper':common.sha256_file(str(R/'tool-shell.py')),'extension':common.sha256_file(str(R/'confirmation_ext.py')),'harness':common.sha256_file(str(R/'harness/lanes_bare.py')),'driver':common.sha256_file(str(R/'run_confirmation.py'))}
def freeze():
 path=R/'protocol.json'
 if path.exists():return json.loads(path.read_text())
 inherited=json.loads((R.parent/'confirmation-eu-wide-20261029/protocol.json').read_text())
 qualified={x['task'] for x in json.loads((R/'eligibility.json').read_text()) if x['qualified']}
 tasks=[t for t in inherited['tasks_randomized'] if t in qualified]
 assert tasks and set(tasks)==qualified
 protocol={k:v for k,v in inherited.items() if k not in ('amendments','attestation','cells','efforts','arms','dry')}
 protocol.update(frozen_utc=e.stamp(),tasks_randomized=tasks,cells=[{'task':t,'arm':a,'rep':1,'stratum':'counted'} for t in tasks for a in ARMS],arms=ARMS,dry=[],model=e.MODEL,effort='high',cap_usd=4,per_cell_estimate_usd=e.CELL_ESTIMATE,order='Confirm5 frozen task order; inside each task loop-default, api-replay, codex; one cell including grading at a time',reuse='Confirm5 qualified tasks, harness, source, cache, grader and read boundary; api-screen native Responses replay binary and witness; run-local real tool stdin logins',route='loop-default shipped Chat adapter; api-replay native Responses plus encrypted reasoning replay; Codex CLI native Responses; same external gateway/upstream',instructions='loop arms shipped default instructions; Codex shipped defaults, user config and rules ignored',analysis='One rep per task; every attempt retained, no replacement. Median and nearest-rank p90 over graded launched attempts. Cost/pass includes every launched attempt. Pair by task, exact two-sided sign tests excluding ties for wall, requests, reasoning, output, cost and discordant grades. Drift check against confirm5 loop-high on same tasks. Fixed within-task order may confound cache/order effects.',witness_gate='Verify first api-replay counted cell before continuing: native Responses, encrypted include requested, hashes of encrypted output reasoning replayed in subsequent input, exact model and HIGH effort.',budget_policy='Before launch require total spend plus conservative cell estimate <= $4. Once admitted, finish the cell without a budget stop; actual spend can exceed an estimate. Complete usage, model and effort gates unchanged; no timeout changes.',attestation=fingerprints())
 dump(path,protocol);return protocol
def make_args(c,run):
 return argparse.Namespace(tasks=str(R/'tasks'),task=c['task'],arm=c.get('client','codex' if c['arm']=='codex' else 'loop'),run_dir=str(run),rep=c['rep'],lane=c['arm'],model=e.MODEL,effort=c.get('effort','high'),provider='openai-compatible',loop_instructions=None,home=str(R/'empty-login'),codex_home=str(R/'empty-codex'),loop_bin=str(BIN.get(c['arm'],R/'bin/loop-b8a4046')),codex_bin=CODEX_DIR+'/codex',intent_form='gherkin',deadline_s=h.DEADLINE_S,force=False,keep=False,no_grade=False,cpu_profile=True,host='EU',kogen_models=None)
def witness(c):
 out=R/c['stratum']/'cells'/c['task']/('r'+str(c['rep']))/c['arm']
 rows=[json.loads(x) for x in (out/'route-receipts.jsonl').read_text().splitlines() if json.loads(x).get('forwarded')]
 produced=set();replayed=set()
 for x in rows:
  assert x['client_path']=='/v1/responses' and x['encrypted_include_requested']
  assert x['model']==e.MODEL and x['reasoning']['effort']=='high'
  replayed.update(produced.intersection(x['input_encrypted_sha256']));produced.update(x['output_encrypted_sha256'])
 assert replayed,'no encrypted reasoning replay witness'
 dump(R/'patch-witnesses.json',{'utc':e.stamp(),'cell':str(out.relative_to(R)),'activation':'verified native Responses encrypted reasoning replay','model_effort_verified':True,'encrypted_items_produced':len(produced),'encrypted_items_replayed':len(replayed)})

def host_check():
 assert pathlib.Path('/run/kogen-host-lock.d/owner').read_text().strip()=='research-confirm'
 expires=float(pathlib.Path('/run/kogen-host-lock.d/expires').read_text().strip())
 if time.time()+600>expires:raise RuntimeError('less than ten minutes remain in existing owner lease')
 rows=subprocess.check_output(['ps','-u','lanes','-o','pid=,ppid=,pgid=,comm=,args='],text=True)
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
 spent=launched();admission=e.admit_cell(spent)
 e.STATE['effort']=c.get('effort','high')
 receipt=host_check()
 frozen=json.loads(PROTOCOL_PATH.read_text())
 if fingerprints()!=frozen['attestation']:raise RuntimeError('frozen source, binary, task or cache changed')
 dump(R/('next-cell-'+c['stratum']+'.json'),{'cell':c,'host_preflight':receipt,**admission})
 result=h.run_cell(make_args(c,run))
 dump(out/'host-preflight.json',receipt)
 after_verified=fingerprints()==frozen['attestation']
 dump(out/'provenance.json',{'protocol_sha256':hashlib.sha256(PROTOCOL_PATH.read_bytes()).hexdigest(),'before_verified':True,'after_verified':after_verified})
 if not after_verified:raise RuntimeError('post-cell provenance changed')
 route=json.loads((out/'route-summary.json').read_text()) if (out/'route-summary.json').exists() else None
 with (R/'cell-ledger.jsonl').open('a') as f:f.write(json.dumps({'utc':e.stamp(),'cell':c,'result_path':str(out/'result.json'),'outcome':result.get('outcome'),'all_passed':result.get('all_passed'),'route':route})+'\n')
 print(json.dumps({'cell':c,'outcome':result.get('outcome'),'passed':result.get('all_passed'),'agent_wall':result.get('totals',{}).get('wall_s'),'route':route}),flush=True)
 if not route or not route['all_usage_present'] or not route['response_models'] or set(route['response_models'])!={e.MODEL}:raise RuntimeError('route, usage or model identity gate failed')
 receipts=[json.loads(x) for x in (out/'route-receipts.jsonl').read_text().splitlines() if json.loads(x).get('forwarded')]
 if any(x.get('model')!=e.MODEL or (x.get('reasoning') or {}).get('effort')!=c.get('effort','high') for x in receipts):raise RuntimeError('identity/effort gate failed')
 if result.get('outcome') in ('harness_error','timeout') or route['stop_reason']:raise RuntimeError('infrastructure gate failed; no replacement')
 if c['arm']=='api-replay' and not (R/'patch-witnesses.json').exists():witness(c)

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

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['freeze','cell']);p.add_argument('--index',type=int);a=p.parse_args();protocol=freeze()
 try:
  if a.mode=='cell':
   assert a.index is not None and 0<=a.index<len(protocol['cells'])
   for previous in protocol['cells'][:a.index]:
    assert (R/previous['stratum']/'cells'/previous['task']/('r'+str(previous['rep']))/previous['arm']/'result.json').exists(),'previous cell missing'
   if a.index>1:assert (R/'patch-witnesses.json').exists(),'first replay witness not verified'
   c=protocol['cells'][a.index];print(json.dumps({'starting':c,'utc':e.stamp()}),flush=True);cell(c)
   if a.index==len(protocol['cells'])-1:dump(R/'status-counted.json',{'utc':e.stamp(),'state':'complete','spend_upper_bound_usd':launched()})
  dump(R/('status-'+a.mode+('-'+str(a.index) if a.mode=='cell' else '')+'.json'),{'utc':e.stamp(),'state':'complete','spend_upper_bound_usd':launched()})
 except Exception as ex:
  dump(R/'status-counted.json',{'utc':e.stamp(),'state':'stopped','index':a.index,'error':str(ex),'traceback':traceback.format_exc(),'spend_upper_bound_usd':launched()})
  print(type(ex).__name__+': '+str(ex),file=sys.stderr);sys.exit(2)
