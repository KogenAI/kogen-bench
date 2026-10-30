"""Short-test driver for highwall-write-check (sanitized copy of the original driver).

Runs one run per invocation, in the frozen order: per task loop-default, write-check, Codex CLI.
Usage: WCHECK_ROOT=<run root> CODEX_BIN=<codex> python3 run-write-check-short-test.py cell --index N
"""
import argparse,datetime,hashlib,importlib.util,json,os,pathlib,subprocess,sys,time,traceback

# Prepared run root (the lanes/ loop-vs-codex confirmation release: harness/, grader/, tasks/, source/kogen-loop,
# bin/loop-b8a4046, cache-snapshot/, tool-shell.py, confirmation_ext.py, run_confirmation.py, protocol.json)
# and the patched candidate under <root>/write-check-screen-high/bin/write-check-linux-amd64.
ORIGIN=pathlib.Path(os.environ['WCHECK_ROOT']).resolve()
SCREEN=ORIGIN/'write-check-screen-high'
sys.path[:0]=[str(ORIGIN/'harness'),str(ORIGIN)]
os.environ.update(LANES_DIR=str(ORIGIN/'grader'),PATH=os.environ['PATH'],GOMAXPROCS='2',GOPROXY='off',GOTOOLCHAIN='local')
import lanes_bare as h
spec=importlib.util.spec_from_file_location('confirmation_ext_screen',SCREEN/'confirmation_ext_screen.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
e.install(h)

BASE_PROTOCOL=json.loads((ORIGIN/'protocol.json').read_text())
TASKS=BASE_PROTOCOL['tasks_randomized']
ARMS=['loop-default','write-check','codex']
CAP=4.0
ESTIMATE=0.75
ORIGIN_BIN=ORIGIN/'bin/loop-b8a4046'
CODEX_BIN=pathlib.Path(os.environ['CODEX_BIN']).resolve()  # Codex CLI 0.165.0 (x86_64-unknown-linux-musl)
CELLS=[{'task':t,'arm':a,'rep':1,'stratum':'counted'} for t in TASKS for a in ARMS]

def dump(path,data):
 path=pathlib.Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def tree_sha(root):
 root=pathlib.Path(root);hsh=hashlib.sha256()
 for p in sorted(x for x in root.rglob('*') if x.is_file() and '.git' not in x.parts):
  rel=p.relative_to(root).as_posix().encode();hsh.update(len(rel).to_bytes(8,'big'));hsh.update(rel)
  with p.open('rb') as f:
   while b:=f.read(1024*1024):hsh.update(b)
 return hsh.hexdigest()

def fingerprints():
 from lanes import common
 c=CODEX_BIN.parent
 return {'tasks':{n:common.sha256_tree(str(ORIGIN/'tasks'/n)) for n in sorted(p.name for p in (ORIGIN/'tasks').iterdir())},'cache':common.sha256_tree(str(ORIGIN/'cache-snapshot')),'grader_source':common.sha256_tree(str(ORIGIN/'grader'),exclude=('.git','__pycache__')),'loop_source':common.sha256_tree(str(ORIGIN/'source/kogen-loop'),exclude=('.git','__pycache__')),'binaries':{str(p):common.sha256_file(str(p)) for p in [ORIGIN_BIN,ORIGIN/'bin/scr-api-replay-kogen-loop',c/'codex',c/'codex-code-mode-host']},'shell_wrapper':common.sha256_file(str(ORIGIN/'tool-shell.py')),'extension':common.sha256_file(str(ORIGIN/'confirmation_ext.py')),'harness':common.sha256_file(str(ORIGIN/'harness/lanes_bare.py')),'driver':common.sha256_file(str(ORIGIN/'run_confirmation.py'))}

def run_spend():
 rows=[]
 for p in (SCREEN/'counted/cells').glob('*/r*/*/route-summary.json'):
  d=json.loads(p.read_text());rows.append(d)
 return sum(x['usd_list'] if x.get('all_usage_present') else x['charge_upper_bound_usd'] for x in rows)

def host_check():
 # The original host also required an exclusive host lease here; keep the host otherwise idle.
 expires=None
 rows=subprocess.check_output(['ps','-u',str(os.getuid()),'-o','pid=,ppid=,pgid=,comm=,args='],text=True)
 own={os.getpid(),os.getppid()};busy=[]
 for line in rows.splitlines():
  x=line.strip().split(None,4)
  if len(x)<5:continue
  pid,ppid,pgid,comm,args=x
  if int(pid) in own or comm in ('ps','bash','sh') and int(ppid) in own:continue
  if any(z in comm for z in ('kogen','codex','compile','link')) or comm in ('go','node','npm','npx') or ('python' in comm and 'run-highwall-screen.py' not in args):busy.append(line)
 if busy:raise RuntimeError('other lanes/build process active')
 return {'utc':e.stamp(),'load_1m':os.getloadavg()[0],'lock_expires':expires}

def make_args(c):
 arm='codex' if c['arm']=='codex' else 'loop'
 loop_bin=SCREEN/'bin/write-check-linux-amd64' if c['arm']=='write-check' else ORIGIN_BIN
 return argparse.Namespace(tasks=str(ORIGIN/'tasks'),task=c['task'],arm=arm,run_dir=str(SCREEN/'counted'),rep=1,lane=c['arm'],model=e.MODEL,effort='high',provider='openai-compatible',loop_instructions=None,home=str(ORIGIN/'empty-login'),codex_home=str(ORIGIN/'empty-codex'),loop_bin=str(loop_bin),codex_bin=str(CODEX_BIN),intent_form='gherkin',deadline_s=h.DEADLINE_S,force=False,keep=False,no_grade=False,cpu_profile=True,host='local',kogen_models=None)

def launch(index):
 assert 0<=index<len(CELLS)
 c=CELLS[index];out=SCREEN/'counted/cells'/c['task']/'r1'/c['arm']
 if (out/'result.json').exists():raise RuntimeError('cell already exists; never auto-replace')
 for prev in CELLS[:index]:
  p=SCREEN/'counted/cells'/prev['task']/'r1'/prev['arm']/'result.json'
  assert p.exists(),'previous screen cell missing'
 before=fingerprints()
 assert before==BASE_PROTOCOL['attestation'],'reused replay source, binaries, task or cache fingerprint changed'
 admission=e.admit_cell(run_spend(),ESTIMATE)
 receipt=host_check()
 e.STATE['effort']='high'
 dump(SCREEN/f'next-cell-{index}.json',{'cell':c,'host_preflight':receipt,**admission})
 result=h.run_cell(make_args(c))
 dump(out/'host-preflight.json',receipt)
 after=fingerprints()==BASE_PROTOCOL['attestation']
 dump(out/'provenance.json',{'before_verified':True,'after_verified':after,'reused_protocol_sha256':hashlib.sha256((ORIGIN/'protocol.json').read_bytes()).hexdigest(),'candidate_binary_sha256':hashlib.sha256((SCREEN/'bin/write-check-linux-amd64').read_bytes()).hexdigest()})
 if not after:raise RuntimeError('post-cell reused-artifact provenance changed')
 route=json.loads((out/'route-summary.json').read_text()) if (out/'route-summary.json').exists() else None
 row={'utc':e.stamp(),'screen':'write-check-screen-high','cell':c,'outcome':result.get('outcome'),'all_passed':result.get('all_passed'),'route':route}
 with (ORIGIN/'cell-ledger.jsonl').open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n')
 print(json.dumps({'cell':c,'outcome':result.get('outcome'),'passed':result.get('all_passed'),'agent_wall':result.get('totals',{}).get('wall_s'),'route':route}),flush=True)
 if not route or not route['all_usage_present'] or not route['response_models'] or set(route['response_models'])!={e.MODEL}:raise RuntimeError('route, usage or model identity gate failed')
 receipts=[json.loads(x) for x in (out/'route-receipts.jsonl').read_text().splitlines() if json.loads(x).get('forwarded')]
 if any(x.get('model')!=e.MODEL or (x.get('reasoning') or {}).get('effort')!='high' for x in receipts):raise RuntimeError('identity/effort gate failed')
 if result.get('outcome') in ('harness_error','timeout') or route['stop_reason']:raise RuntimeError('infrastructure gate failed; no replacement')
 return result

def freeze():
 if (SCREEN/'protocol.json').exists():return json.loads((SCREEN/'protocol.json').read_text())
 proto={'frozen_utc':e.stamp(),'tasks_randomized':TASKS,'cells':CELLS,'arms':ARMS,'model':e.MODEL,'effort':'high','cap_usd':CAP,'per_cell_estimate_usd':ESTIMATE,'order':'Confirm5 frozen task order; within task loop-default, write-check, Codex CLI; one cell at a time including grading','reuse':'replay11 extension, logins, read boundary, grader, protocol, cache and qualified tasks; candidate binary from isolated patched source','budget_policy':'admit only before each cell if spend plus $0.75 estimate <= $4; once admitted, no budget stop; usage/model/effort gates unchanged','base_replay_protocol_sha256':hashlib.sha256((ORIGIN/'protocol.json').read_bytes()).hexdigest(),'base_attestation':BASE_PROTOCOL['attestation'],'candidate_patch_sha256':hashlib.sha256((SCREEN/'highwall-write-check.diff').read_bytes()).hexdigest(),'candidate_source_tree_sha256':tree_sha(SCREEN/'source/kogen-loop'),'candidate_binary_sha256':hashlib.sha256((SCREEN/'bin/write-check-linux-amd64').read_bytes()).hexdigest(),'default_recorded_binary_sha256':BASE_PROTOCOL['attestation']['binaries'][str(ORIGIN_BIN)],'default_same_toolchain_rebuild_sha256':'6a57808cbcfe2d32496f207473ef32a12d53e710a5372c8f04668a641022456e'}
 dump(SCREEN/'protocol.json',proto)
 return proto

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['freeze','cell']);p.add_argument('--index',type=int);a=p.parse_args()
 try:
  freeze()
  if a.mode=='cell':
   if a.index is None:raise ValueError('--index required')
   c=CELLS[a.index]
   print(json.dumps({'starting':c,'utc':e.stamp()}),flush=True)
   launch(a.index)
  dump(SCREEN/('status-counted.json'),{'utc':e.stamp(),'state':'complete','spend_upper_bound_usd':run_spend()})
 except Exception as ex:
  dump(SCREEN/'status-counted.json',{'utc':e.stamp(),'state':'stopped','index':a.index,'error':type(ex).__name__+': '+str(ex),'spend_upper_bound_usd':run_spend()})
  print(type(ex).__name__+': '+str(ex),file=sys.stderr);sys.exit(2)
