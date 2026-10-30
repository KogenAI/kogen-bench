"""batchconf confirmation driver (lanes): loop-default, loop + batching sentence (no tool),
loop + batch tool (+ sentence) and Codex CLI at HIGH on fresh qualified tasks, interleaved per task
(arm order rotated by task index), one cell at a time including grading.
Admission only before a cell (measured estimate, cap, one-request credit probe); an admitted cell is
never cut. No activation stop rule. A provider fault inside a cell (missing usage, timeout,
incomplete response) is kept as a failed launched attempt and the round continues; identity or
effort mismatch on a returned response, or a harness error, stops the round."""
import argparse,hashlib,importlib.util,json,os,pathlib,subprocess,sys,time,traceback,urllib.request,urllib.error
R=pathlib.Path(os.environ['BATCHCONF_ROOT']).resolve()  # run root: harness, grader, bin/, tasks/, cache-snapshot, protocol inputs
sys.path[:0]=[str(R/'harness'),str(R)]
os.environ.update(LANES_DIR=str(R/'grader'),PATH=os.environ['PATH'],GOMAXPROCS='2',GOPROXY='off',GOTOOLCHAIN='local')
os.environ.setdefault('LANES_CONFIRM_DIR',str(R));os.environ.setdefault('CODEX_BIN_DIR',str(pathlib.Path(os.environ['CODEX_BIN']).resolve().parent))  # read by confirmation_ext.py at import
import lanes_bare as h
import confirmation_ext as e
e.install(h)

ARMS=['loop-default','sentence','batch','codex']
CANDIDATES={'batch':'batch'}  # arm -> new tool name
BIN={'loop-default':R/'bin/loop-base-linux-amd64','sentence':R/'bin/loop-sentence-linux-amd64','batch':R/'bin/loop-batch-linux-amd64'}
CAP_LIMIT=15.0
CODEX_BIN=pathlib.Path(os.environ['CODEX_BIN']).resolve()  # Codex CLI 0.165.0 (x86_64 musl release)
CODEX_DIR=CODEX_BIN.parent
KOGEN=os.environ['KOGEN_BIN']  # kogen 16102c97, linux-x86_64
# Admission estimate: your own largest per-run cost on this route at high effort x1.5, passed to freeze.
PROTOCOL_PATH=R/'protocol.json'
PROBES=R/'probes.jsonl'
QUOTA_WORDS=('insufficient_quota','billing','quota','exceeded your current')
LOGINS=[R/'login-codex/auth.json',R/'login-loop/.kogen/credentials/openai-compatible.json']

def dump(p,d):e.write(p,d)
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def cell_dir(c):return R/'counted/cells'/c['task']/'r1'/c['arm']

def fingerprints():
 from lanes import common
 return {'tasks':{n:common.sha256_tree(str(R/'tasks'/n)) for n in sorted(p.name for p in (R/'tasks').iterdir())},'cache':common.sha256_tree(str(R/'cache-snapshot')),'grader_source':common.sha256_tree(str(R/'grader'),exclude=('.git','__pycache__')),'binaries':{str(p):common.sha256_file(str(p)) for p in [*BIN.values(),CODEX_DIR/'codex',CODEX_DIR/'codex-code-mode-host']},'shell_wrapper':common.sha256_file(str(R/'tool-shell.py')),'extension':common.sha256_file(str(R/'confirmation_ext.py')),'harness':common.sha256_file(str(R/'harness/lanes_bare.py')),'driver':common.sha256_file(str(R/'run_batchconf.py'))}

def freeze(max_observed=None,mean_observed=None,basis=None,registration=None):
 if PROTOCOL_PATH.exists():return json.loads(PROTOCOL_PATH.read_text())
 assert max_observed and mean_observed and registration,'freeze needs the measured ledger figures and the registration'
 el=json.loads((R/'eligibility.json').read_text())
 tasks=[r['task'] for r in el['rows'] if r['qualified']]
 assert 8<=len(tasks)<=12
 cells=[{'task':t,'arm':ARMS[(i+k)%4],'rep':1,'stratum':'counted'} for i,t in enumerate(tasks) for k in range(4)]
 estimate=round(max_observed*1.5,7);cap=round(len(cells)*mean_observed*1.5,6)
 assert cap<=CAP_LIMIT,'round cap above the $15 limit'
 setup=json.loads((R/'setup.json').read_text())
 protocol={'frozen_utc':e.stamp(),'id':'batchconf-confirmation-20261030','tasks':tasks,'cells':cells,'arms':ARMS,'model':e.MODEL,'effort':'high',
  'order':'qualified task order; inside task i the arms run in [loop-default, sentence, batch, codex] rotated by i mod 4; one cell including grading at a time',
  'binaries':'loop-default, sentence and batch built for linux/amd64 in one directory with the same toolchain (go1.27.2, CGO off, go build ./cmd/kogen-loop) from the short test\'s base tree plus each patch in patches/',
  'setup':setup,'registration':registration,'admission_estimate_rule':'largest per-run cost in your spend ledger on this route, gpt-6.1-terra HIGH (any arm, upper bound where usage was absent), x1.5','admission_estimate_basis':basis,'admission_estimate_usd':estimate,
  'round_cap_rule':'registered runs x measured mean per-run cost x 1.5 (mean of the short test\'s 12 loop-default/batch/Codex runs); includes credit probes; <= $15','round_cap_basis':{'runs':len(cells),'mean_usd':mean_observed},'round_cap_usd':cap,
  'budget_policy':'admit only before a cell; an admitted cell is never cut; usage, model and effort gates unchanged; no timeout changes',
  'credit_probe':'one minimal Responses request (max_output_tokens 16, effort low) on the same key before each admission; counted in spend; quota/billing errors stop admission',
  'fault_policy':'provider fault in a cell (missing usage, incomplete/runaway response, loop provider wait limit, harness deadline) = failed launched attempt, counted at its charge upper bound, kept, no replacement, round continues; returned model/effort identity mismatch or harness_error stops the round',
  'attestation':fingerprints()}
 dump(PROTOCOL_PATH,protocol);return protocol

def summary(c):
 p=cell_dir(c)/'route-summary.json'
 if not p.exists():return 0.
 d=json.loads(p.read_text());return d['usd_list'] if d.get('all_usage_present') else d['charge_upper_bound_usd']
def probe_spend():
 return sum(json.loads(x).get('usd',0.) for x in PROBES.read_text().splitlines()) if PROBES.exists() else 0.
def spend(protocol):return sum(summary(c) for c in protocol['cells'])+probe_spend()

def operations(c):
 """Tool operations and new-tool calls of a finished loop cell, from its events."""
 ops=calls=batched=0;tool=CANDIDATES.get(c['arm']);events=cell_dir(c)/'events.jsonl'
 for line in (events.read_text().splitlines() if events.exists() else []):
  d=json.loads(line)
  if d.get('type')!='tool.result':continue
  if tool and d.get('name')==tool:
   n=d.get('operations') or 0;ops+=n;calls+=1;batched+=n>=2
  else:ops+=1
 return {'operations':ops,'new_tool_calls':calls,'new_tool_calls_with_2plus_ops':batched,'activated':batched>0}

def stopped(protocol,arm):
 """Activation record of a candidate before its next cell: stopped when < 2 of its first 3 can use it."""
 done=[c for c in protocol['cells'] if c['arm']==arm and (cell_dir(c)/'result.json').exists()][:3]
 used=sum(operations(c)['activated'] for c in done)
 return {'arm':arm,'first_cells':len(done),'activated':used,'stopped':used+(3-len(done))<2}

def host_check():
 assert pathlib.Path('/run/kogen-host-lock.d/owner').read_text().strip()=='research-confirm'
 expires=float(pathlib.Path('/run/kogen-host-lock.d/expires').read_text().strip())
 if time.time()+600>expires:raise RuntimeError('less than ten minutes remain in existing owner lease')
 rows=subprocess.check_output(['ps','-u',os.environ.get('LANES_USER','lanes'),'-o','pid=,ppid=,pgid=,comm=,args='],text=True)
 own={os.getpid(),os.getppid()};busy=[]
 for line in rows.splitlines():
  x=line.strip().split(None,4)
  if len(x)<5:continue
  pid,ppid,pgid,comm,args=x
  if int(pid) in own or comm in ('ps','bash','sh') and int(ppid) in own:continue
  if any(z in comm for z in ('kogen','codex','compile','link')) or comm in ('go','node','npm','npx') or ('python' in comm and 'run_batchconf.py' not in args):busy.append(line)
 if busy:raise RuntimeError('other lanes/build process active')
 return {'utc':e.stamp(),'load_1m':os.getloadavg()[0],'lock_owner':'research-confirm','lock_expires':expires,'own_pid':os.getpid(),'own_pgid':os.getpgrp()}

def make_args(c):
 arm='codex' if c['arm']=='codex' else 'loop'
 return argparse.Namespace(tasks=str(R/'tasks'),task=c['task'],arm=arm,run_dir=str(R/'counted'),rep=1,lane=c['arm'],model=e.MODEL,effort='high',provider='openai-compatible',loop_instructions=None,home=str(R/'empty-login'),codex_home=str(R/'empty-codex'),loop_bin=str(BIN.get(c['arm'],BIN['loop-default'])),codex_bin=str(CODEX_BIN),intent_form='gherkin',deadline_s=h.DEADLINE_S,force=False,keep=False,no_grade=False,cpu_profile=True,host='host',kogen_models=None)

def login():
 key=os.environ.get('OPENAI_API_KEY') or sys.stdin.readline().strip()  # your own key, shared by all four arms
 assert key,'no API key'
 env=dict(os.environ);env['CODEX_HOME']=str(R/'login-codex')
 a=subprocess.run([str(CODEX_BIN),'-c','cli_auth_credentials_store="file"','login','--with-api-key'],input=key+'\n',env=env,text=True,capture_output=True,timeout=30)
 env=dict(os.environ);env['HOME']=str(R/'login-loop')
 b=subprocess.run([KOGEN,'provider','login','openai-compatible'],input=key+'\n',env=env,text=True,capture_output=True,timeout=30)
 assert a.returncode==b.returncode==0,'stdin login failed'
 assert json.loads(LOGINS[0].read_text())['OPENAI_API_KEY']==json.loads(LOGINS[1].read_text())['api_key']==key
 dump(R/'login.json',{'utc':e.stamp(),'uid':os.getuid(),'method':'both actual tools stdin login commands (fixed release paths); key held in memory only','commands_exit':[a.returncode,b.returncode],'keys_equal_in_memory':True,'contents_recorded':False})
 print('Both stdin logins completed',flush=True)

def cleanup():
 for p in LOGINS:p.unlink(missing_ok=True)
 dump(R/'credential-cleanup.json',{'utc':e.stamp(),'uid':os.getuid(),'method':'unlink only the two run-local tool login files','credential_paths_absent':all(not p.exists() for p in LOGINS)})
 print('credential_paths_absent',all(not p.exists() for p in LOGINS),flush=True)

def probe(index):
 key=json.loads(LOGINS[0].read_text())['OPENAI_API_KEY']
 body={'model':e.MODEL,'input':'Reply with OK.','max_output_tokens':16,'reasoning':{'effort':'low'},'store':False}
 row={'utc':e.stamp(),'kind':'credit-probe','before_cell_index':index,'upstream':'https://api.openai.com/v1/responses','request':{k:v for k,v in body.items() if k!='input'},'usd':0.}
 req=urllib.request.Request('https://api.openai.com/v1/responses',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(req,timeout=120) as r:
   d=json.loads(r.read());u=d.get('usage') or {}
   row.update(http_status=r.status,request_id=r.headers.get('x-request-id'),model=d.get('model'),status=d.get('status'),usage=u,usd=e.cost(u),ok=True)
 except urllib.error.HTTPError as x:
  text=x.read().decode(errors='replace');err={}
  try:err=json.loads(text).get('error') or {}
  except ValueError:pass
  low=(str(err.get('code'))+' '+str(err.get('type'))+' '+str(err.get('message'))).lower()
  row.update(http_status=x.code,request_id=x.headers.get('x-request-id'),error_code=err.get('code'),error_type=err.get('type'),ok=False,quota=any(w in low for w in QUOTA_WORDS))
 except Exception as x:
  row.update(ok=False,quota=False,error=type(x).__name__+': '+str(x)[:200])
 with PROBES.open('a') as f:f.write(json.dumps(row)+'\n')
 return row

def stop(protocol,index,reason,code=3):
 dump(R/'status-counted.json',{'utc':e.stamp(),'state':'stopped','index':index,'error':reason,'spend_usd':spend(protocol),'cap_usd':protocol['round_cap_usd'],'estimate_usd':protocol['admission_estimate_usd']})
 print(reason,file=sys.stderr);sys.exit(code)

def run(index):
 protocol=freeze()
 assert 0<=index<len(protocol['cells'])
 c=protocol['cells'][index];out=cell_dir(c)
 for prev in protocol['cells'][:index]:
  if not (cell_dir(prev)/'result.json').exists() and not (cell_dir(prev)/'skipped.json').exists():raise RuntimeError('previous cell neither finished nor skipped')
 if (out/'result.json').exists() or (out/'skipped.json').exists():print(json.dumps({'skip_done':c}),flush=True);return
 if fingerprints()!=protocol['attestation']:raise RuntimeError('frozen source, binary, task or cache changed')
 spent=spend(protocol)
 if spent+protocol['admission_estimate_usd']>protocol['round_cap_usd']:stop(protocol,index,'round budget cannot admit next cell: spend + measured estimate exceeds cap')
 p=probe(index)
 if not p['ok'] and p.get('quota'):stop(protocol,index,'stopped at admission: key out of credit ('+e.stamp()+')')
 if not p['ok']:
  time.sleep(60);p=probe(index)
  if not p['ok']:stop(protocol,index,'stopped at admission: key out of credit ('+e.stamp()+')' if p.get('quota') else 'stopped at admission: credit probe failed twice ('+str(p.get('http_status') or p.get('error'))+')')
 receipt=host_check()
 e.STATE['effort']='high'
 dump(R/('next-cell-'+str(index)+'.json'),{'cell':c,'host_preflight':receipt,'spend_before_usd':spend(protocol),'estimate_usd':protocol['admission_estimate_usd'],'cap_usd':protocol['round_cap_usd'],'probe_usd':p['usd'],'policy':'admit before cell; never censor an admitted cell for budget'})
 print(json.dumps({'starting':c,'index':index,'utc':e.stamp(),'spend_usd':spend(protocol)}),flush=True)
 result=h.run_cell(make_args(c))
 dump(out/'host-preflight.json',receipt)
 after=fingerprints()==protocol['attestation']
 dump(out/'provenance.json',{'protocol_sha256':sha(PROTOCOL_PATH),'before_verified':True,'after_verified':after})
 if not after:raise RuntimeError('post-cell provenance changed')
 route=json.loads((out/'route-summary.json').read_text()) if (out/'route-summary.json').exists() else None
 extra=operations(c) if c['arm']!='codex' and (out/'events.jsonl').exists() else {}
 with (R/'cell-ledger.jsonl').open('a') as f:f.write(json.dumps({'utc':e.stamp(),'cell':c,'result_path':str(out/'result.json'),'outcome':result.get('outcome'),'all_passed':result.get('all_passed'),'route':route,**extra},sort_keys=True)+'\n')
 print(json.dumps({'cell':c,'outcome':result.get('outcome'),'passed':result.get('all_passed'),'agent_wall':result.get('totals',{}).get('wall_s'),'usd':route and route.get('usd_list'),'requests':route and route.get('requests'),**extra}),flush=True)
 if not route or not route['requests']:raise RuntimeError('route gate failed: no forwarded request')
 receipts=[json.loads(x) for x in (out/'route-receipts.jsonl').read_text().splitlines() if json.loads(x).get('forwarded')]
 returned=[(x.get('model'),(x.get('reasoning') or {}).get('effort')) for x in receipts]+[(m.get('model'),(m.get('reasoning') or {}).get('effort')) for x in receipts for m in x.get('response_models') or []]
 if any(m is not None and m!=e.MODEL for m,_ in returned) or any(f is not None and f!='high' for _,f in returned):raise RuntimeError('identity/effort gate failed')
 if result.get('outcome')=='harness_error':raise RuntimeError('harness error; no replacement')
 fault=[] if route['all_usage_present'] and not route['stop_reason'] and result.get('outcome')!='timeout' else [route['stop_reason'],result.get('outcome'),'usage absent' if not route['all_usage_present'] else None]
 if fault:dump(out/'provider-fault.json',{'utc':e.stamp(),'cell':c,'fault':[x for x in fault if x],'policy':'failed launched attempt, counted at charge upper bound, kept, no replacement; round continues (registered)'})
 if index==len(protocol['cells'])-1:dump(R/'status-counted.json',{'utc':e.stamp(),'state':'complete','spend_usd':spend(protocol)})

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['freeze','login','cell','cleanup','spend']);p.add_argument('--index',type=int)
 p.add_argument('--max-observed',type=float);p.add_argument('--mean-observed',type=float);p.add_argument('--basis');p.add_argument('--registration');a=p.parse_args()
 if a.mode=='freeze':print(json.dumps({k:v for k,v in freeze(a.max_observed,a.mean_observed,a.basis,json.loads(pathlib.Path(a.registration).read_text()) if a.registration else None).items() if k not in ('attestation','setup')},indent=1))
 elif a.mode=='login':login()
 elif a.mode=='cleanup':cleanup()
 elif a.mode=='spend':pr=freeze();print(json.dumps({'spend_usd':spend(pr),'probe_usd':probe_spend(),'cap_usd':pr['round_cap_usd'],'estimate_usd':pr['admission_estimate_usd']}))
 else:
  try:run(a.index)
  except SystemExit:raise
  except Exception as ex:
   dump(R/'status-counted.json',{'utc':e.stamp(),'state':'stopped','index':a.index,'error':str(ex),'traceback':traceback.format_exc()})
   print(type(ex).__name__+': '+str(ex),file=sys.stderr);sys.exit(2)
