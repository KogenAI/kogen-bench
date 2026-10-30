"""replayconf driver (lanes): confirmation of reasoning replay at HIGH.
Arms: loop-default (loop-b8a4046), api-replay (scr-api-replay-kogen-loop, replay13's binary), Codex CLI
0.165.0 (fixed release dir); same gateway extension, key, model and effort. One cell including grading at
a time; arms interleaved per task with the starting arm rotated by task index. Admission only before a cell
(measured estimate, round cap, one-request credit probe); an admitted cell is never cut.
Exit codes: 0 done/skipped, 2 gate or error (stop), 3 admission stop (budget/credit), 4 host busy (nothing started)."""
import argparse,hashlib,json,os,pathlib,subprocess,sys,time,traceback,urllib.request,urllib.error
R=pathlib.Path(os.environ['REPLAYCONF_ROOT']).resolve()  # run root: harness, grader, bin/, tasks/, protocol inputs
sys.path[:0]=[str(R/'harness'),str(R)]
os.environ.update(LANES_DIR=str(R/'grader'),PATH=os.environ['PATH'],GOMAXPROCS='2',GOPROXY='off',GOTOOLCHAIN='local')
import lanes_bare as h
import confirmation_ext as e
e.install(h)

ARMS=['loop-default','api-replay','codex']
N=14
DRY_TASK='ledger-go'
LOCK=pathlib.Path('/run/kogen-host-lock.d');LOCK_OWNER='research-replayconf'
BIN={'loop-default':R/'bin/loop-b8a4046','api-replay':R/'bin/scr-api-replay-kogen-loop'}
CODEX_BIN=pathlib.Path(os.environ['CODEX_BIN']).resolve()  # Codex CLI 0.165.0 (x86_64-unknown-linux-musl)
CODEX_DIR=CODEX_BIN.parent
KOGEN=os.environ['KOGEN_BIN']  # kogen 16102c97, linux-x86_64
PROTOCOL_PATH=R/'protocol.json'
PROBES=R/'probes.jsonl'
QUOTA_WORDS=('insufficient_quota','billing','quota','exceeded your current')
LOGINS=[R/'login-codex/auth.json',R/'login-loop/.kogen/credentials/openai-compatible.json']

def dump(p,d):e.write(p,d)
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def cell_dir(c):return R/c['stratum']/'cells'/c['task']/'r1'/c['arm']

def fingerprints():
 from lanes import common
 return {'tasks':{n:common.sha256_tree(str(R/'tasks'/n)) for n in sorted(p.name for p in (R/'tasks').iterdir())},'cache':common.sha256_tree(str(R/'cache-snapshot')),'grader_source':common.sha256_tree(str(R/'grader'),exclude=('.git','__pycache__')),'loop_source':common.sha256_tree(str(R/'source/kogen-loop'),exclude=('.git','__pycache__')),'binaries':{str(p):common.sha256_file(str(p)) for p in [*BIN.values(),CODEX_DIR/'codex',CODEX_DIR/'codex-code-mode-host']},'shell_wrapper':common.sha256_file(str(R/'tool-shell.py')),'extension':common.sha256_file(str(R/'confirmation_ext.py')),'harness':common.sha256_file(str(R/'harness/lanes_bare.py')),'driver':common.sha256_file(str(R/'run_replayconf.py'))}

def order(i):return ARMS[i%3:]+ARMS[:i%3]

def freeze(max_observed=None,mean_observed=None,basis=None):
 if PROTOCOL_PATH.exists():return json.loads(PROTOCOL_PATH.read_text())
 assert max_observed and mean_observed,'freeze needs the measured ledger figures'
 rows=json.loads((R/'eligibility.json').read_text())
 tasks=[r['task'] for r in rows if r['qualified'] and r['task']!=DRY_TASK][:N]
 assert len(tasks)>=8
 cells=[{'task':DRY_TASK,'arm':a,'rep':1,'stratum':'dry'} for a in ARMS]+[{'task':t,'arm':a,'rep':1,'stratum':'counted'} for i,t in enumerate(tasks) for a in order(i)]
 estimate=round(max_observed*1.5,7);cap=round(len(cells)*mean_observed*1.5,6)
 assert cap<=15.0,'round cap above the $15 limit'
 setup=json.loads((R/'setup.json').read_text());assert setup['all_equal']
 protocol={'frozen_utc':e.stamp(),'id':'replayconf-14task-high','host':'Linux host, 4 cores, GOMAXPROCS=2','tasks':tasks,'dry_task':DRY_TASK,'cells':cells,'arms':ARMS,'model':e.MODEL,'effort':'high',
  'order':'dry first (ledger-go: loop-default, api-replay, codex), then tasks in qualification order; inside task i the arms run in ARMS rotated by i mod 3 (loop-default/api-replay/codex, api-replay/codex/loop-default, codex/loop-default/api-replay); one cell including grading at a time',
  'binaries':'loop-default = EU bin/loop-b8a4046 (611cbb9d...), api-replay = EU bin/scr-api-replay-kogen-loop (586f0314...), both the exact files replay13 ran, copied byte for byte; Codex CLI 0.165.0 fixed release dir (same sha256 as EU)',
  'setup':setup,
  'registration':{'question':'does native Responses encrypted reasoning replay (api-replay) lower cost per pass and requests per run vs the shipped loop default, same model/effort/key, on fresh tasks',
   'primary':['cost per pass: per-arm total USD / passes; paired per task: cell USD where a failed cell counts as worse than any passed cell and two failed cells tie; exact two-sided sign test, ties dropped',
              'requests per run: route requests per cell, paired per task, exact two-sided sign test, ties dropped'],
   'primary_comparison':'api-replay vs loop-default; api-replay vs codex and loop-default vs codex reported the same way',
   'secondary':['agent wall s per cell (sign test)','reasoning tokens per cell (sign test)'],
   'also_reported':'pass (discordant pairs), output tokens, per-arm medians and totals; descriptive only',
   'stop_rules':'none beyond the spend guard (admission only) and the credit probe; no reruns or replacements; every launched cell is retained',
   'exclusions':'a pair with an infrastructure gate failure is reported and the round stops (no replacement)',
   'power':'replay13 per-task log(replay/loop USD): sd 0.320 (mean -0.061). Under a -20% effect with that spread P(task favours replay)=Phi(0.223/0.320)=0.757. Two-sided exact sign test p<0.05 needs 8/8, 9/10, 10/12, 12/14, 13/16-17, 15/20; expected wins reach the critical count first at n=20 (15.1>=15); power: n=8 0.11, n=14 0.30, n=20 0.65. The $15 cap at measured prices affords n=14 with the dry (45 runs x $0.2121 x 1.5 = $14.32), so n=14 is registered: underpowered for -20%, adequate only for a larger effect (8/8 at n=8 needs P~0.92).'},
  'admission_estimate_rule':'largest per-run cost in api-spend-ledger.tsv on the EU clean route, gpt-6.1-terra HIGH, x1.5','admission_estimate_basis':basis,'admission_estimate_usd':estimate,
  'round_cap_rule':'registered runs (dry + counted) x replay13 measured mean per-run cost x 1.5; includes credit probes; <= $15','round_cap_basis':{'runs':len(cells),'mean_usd':mean_observed},'round_cap_usd':cap,
  'budget_policy':'admit only before a cell; an admitted cell is never cut; usage, model and effort gates unchanged; no timeout changes (deadline = default 3600 s, bounded only by the lock lease, which the orchestrator keeps >= 4200 s ahead)',
  'credit_probe':'one minimal Responses request (max_output_tokens 16, effort low) on the same key before each admission; counted in spend; quota/billing errors stop admission',
  'dry_gate':'counted cells start only after all three dry cells finished with requests > 0, identity/effort gates passed and the api-replay dry cell showed encrypted reasoning replay (patch-witnesses.json)',
  'credentials':'one OpenAI API key passed on stdin to both tools\' real stdin login commands into run-local stores; removed at the end',
  'attestation':fingerprints()}
 dump(PROTOCOL_PATH,protocol);return protocol

def summary(c):
 p=cell_dir(c)/'route-summary.json'
 if not p.exists():return 0.
 d=json.loads(p.read_text());return d['usd_list'] if d.get('all_usage_present') else d['charge_upper_bound_usd']
def probe_spend():
 return sum(json.loads(x).get('usd',0.) for x in PROBES.read_text().splitlines()) if PROBES.exists() else 0.
def spend(protocol):return sum(summary(c) for c in protocol['cells'])+probe_spend()

def witness(c):
 out=cell_dir(c)
 rows=[json.loads(x) for x in (out/'route-receipts.jsonl').read_text().splitlines() if json.loads(x).get('forwarded')]
 produced=set();replayed=set()
 for x in rows:
  assert x['client_path']=='/v1/responses' and x['encrypted_include_requested']
  assert x['model']==e.MODEL and x['reasoning']['effort']=='high'
  replayed.update(produced.intersection(x['input_encrypted_sha256']));produced.update(x['output_encrypted_sha256'])
 return {'cell':str(out.relative_to(R)),'encrypted_items_produced':len(produced),'encrypted_items_replayed':len(replayed),'native_responses':True,'model_effort_verified':True}

def host_check():
 """Returns None when another lanes workload is active (nothing started)."""
 if (LOCK/'owner').read_text().strip()!=LOCK_OWNER:raise RuntimeError('host lock not held by '+LOCK_OWNER)
 expires=float((LOCK/'expires').read_text().strip())
 if time.time()+600>expires:raise RuntimeError('less than ten minutes remain in the lock lease')
 rows=subprocess.check_output(['ps','-u',str(os.getuid()),'-o','pid=,ppid=,pgid=,comm=,args='],text=True)
 own={os.getpid(),os.getppid()};busy=[]
 for line in rows.splitlines():
  x=line.strip().split(None,4)
  if len(x)<5:continue
  pid,ppid,pgid,comm,args=x
  if int(pid) in own or comm in ('ps','bash','sh','sudo','sshd') and int(ppid) in own:continue
  if any(z in comm for z in ('kogen','codex','claude','compile','link')) or comm in ('go','node','npm','npx') or ('python' in comm and 'run_replayconf.py' not in args):busy.append(line)
 if busy:return None
 return {'utc':e.stamp(),'load_1m':os.getloadavg()[0],'lock_owner':LOCK_OWNER,'lock_expires':expires,'own_pid':os.getpid(),'own_pgid':os.getpgrp()}

def make_args(c):
 arm='codex' if c['arm']=='codex' else 'loop'
 return argparse.Namespace(tasks=str(R/'tasks'),task=c['task'],arm=arm,run_dir=str(R/c['stratum']),rep=1,lane=c['arm'],model=e.MODEL,effort='high',provider='openai-compatible',loop_instructions=None,home=str(R/'empty-login'),codex_home=str(R/'empty-codex'),loop_bin=str(BIN.get(c['arm'],BIN['loop-default'])),codex_bin=str(CODEX_BIN),intent_form='gherkin',deadline_s=h.DEADLINE_S,force=False,keep=False,no_grade=False,cpu_profile=True,host='EU',kogen_models=None)

def login():
 key=sys.stdin.readline().strip()
 assert key.startswith('sk-'),'no key on stdin'
 env=dict(os.environ);env['CODEX_HOME']=str(R/'login-codex')
 a=subprocess.run([str(CODEX_BIN),'-c','cli_auth_credentials_store="file"','login','--with-api-key'],input=key+'\n',env=env,text=True,capture_output=True,timeout=30)
 env=dict(os.environ);env['HOME']=str(R/'login-loop')
 b=subprocess.run([KOGEN,'provider','login','openai-compatible'],input=key+'\n',env=env,text=True,capture_output=True,timeout=30)
 assert a.returncode==b.returncode==0,'stdin login failed'
 assert json.loads(LOGINS[0].read_text())['OPENAI_API_KEY']==json.loads(LOGINS[1].read_text())['api_key']==key
 dump(R/'login.json',{'utc':e.stamp(),'uid':os.getuid(),'key':'one OpenAI API key, passed on stdin','method':'both actual tools stdin login commands (fixed release paths); key held in memory only','commands_exit':[a.returncode,b.returncode],'keys_equal_in_memory':True,'contents_recorded':False,'kogen_login_binary_sha256':sha(KOGEN)})
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
  if not (cell_dir(prev)/'result.json').exists():raise RuntimeError('previous cell not finished')
 if (out/'result.json').exists():print(json.dumps({'skip_done':c}),flush=True);return
 if c['stratum']=='counted':
  w=R/'patch-witnesses.json'
  if not w.exists() or not json.loads(w.read_text()).get('dry_gate_passed'):raise RuntimeError('dry gate not passed')
 if fingerprints()!=protocol['attestation']:raise RuntimeError('frozen source, binary, task or cache changed')
 receipt=host_check()
 if receipt is None:print('host busy: another lanes workload is active; nothing started',file=sys.stderr);sys.exit(4)
 spent=spend(protocol)
 if spent+protocol['admission_estimate_usd']>protocol['round_cap_usd']:stop(protocol,index,'round budget cannot admit next cell: spend + measured estimate exceeds cap')
 p=probe(index)
 if not p['ok'] and p.get('quota'):stop(protocol,index,'stopped at admission: key out of credit ('+e.stamp()+')')
 if not p['ok']:
  time.sleep(60);p=probe(index)
  if not p['ok']:stop(protocol,index,'stopped at admission: key out of credit ('+e.stamp()+')' if p.get('quota') else 'stopped at admission: credit probe failed twice ('+str(p.get('http_status') or p.get('error'))+')')
 e.STATE['effort']='high'
 dump(R/('next-cell-'+str(index)+'.json'),{'cell':c,'host_preflight':receipt,'spend_before_usd':spend(protocol),'estimate_usd':protocol['admission_estimate_usd'],'cap_usd':protocol['round_cap_usd'],'probe_usd':p['usd'],'policy':'admit before cell; never censor an admitted cell for budget'})
 print(json.dumps({'starting':c,'index':index,'utc':e.stamp(),'spend_usd':spend(protocol)}),flush=True)
 result=h.run_cell(make_args(c))
 dump(out/'host-preflight.json',receipt)
 after=fingerprints()==protocol['attestation']
 dump(out/'provenance.json',{'protocol_sha256':sha(PROTOCOL_PATH),'before_verified':True,'after_verified':after})
 if not after:raise RuntimeError('post-cell provenance changed')
 route=json.loads((out/'route-summary.json').read_text()) if (out/'route-summary.json').exists() else None
 wit=witness(c) if c['arm']=='api-replay' and route and route.get('requests') else None
 with (R/'cell-ledger.jsonl').open('a') as f:f.write(json.dumps({'utc':e.stamp(),'index':index,'cell':c,'result_path':str(out/'result.json'),'outcome':result.get('outcome'),'all_passed':result.get('all_passed'),'route':route,'replay_witness':wit},sort_keys=True)+'\n')
 print(json.dumps({'cell':c,'outcome':result.get('outcome'),'passed':result.get('all_passed'),'agent_wall':result.get('totals',{}).get('wall_s'),'usd':route and route.get('usd_list'),'requests':route and route.get('requests'),'replay_witness':wit}),flush=True)
 if not route or not route['all_usage_present'] or not route['response_models'] or set(route['response_models'])!={e.MODEL}:raise RuntimeError('route, usage or model identity gate failed')
 receipts=[json.loads(x) for x in (out/'route-receipts.jsonl').read_text().splitlines() if json.loads(x).get('forwarded')]
 if any(x.get('model')!=e.MODEL or (x.get('reasoning') or {}).get('effort')!='high' for x in receipts):raise RuntimeError('identity/effort gate failed')
 if result.get('outcome') in ('harness_error','timeout') or route['stop_reason']:raise RuntimeError('infrastructure gate failed; no replacement')
 if c['stratum']=='dry' and index==2:
  dry=[cell_dir(x) for x in protocol['cells'][:3]]
  reqs={x.name:json.loads((x/'route-summary.json').read_text())['requests'] for x in dry}
  w=witness(protocol['cells'][[x['arm'] for x in protocol['cells'][:3]].index('api-replay')])
  ok=all(v>0 for v in reqs.values()) and w['encrypted_items_replayed']>0
  dump(R/'patch-witnesses.json',{'utc':e.stamp(),'dry_requests':reqs,'replay':w,'activation':'verified native Responses encrypted reasoning replay' if w['encrypted_items_replayed'] else 'NO replay witness','dry_gate_passed':ok})
  if not ok:raise RuntimeError('dry gate failed: '+json.dumps({'requests':reqs,'replayed':w['encrypted_items_replayed']}))
 if index==len(protocol['cells'])-1:dump(R/'status-counted.json',{'utc':e.stamp(),'state':'complete','spend_usd':spend(protocol)})

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['freeze','login','cell','cleanup','spend','count']);p.add_argument('--index',type=int)
 p.add_argument('--max-observed',type=float);p.add_argument('--mean-observed',type=float);p.add_argument('--basis');a=p.parse_args()
 if a.mode=='freeze':print(json.dumps({k:v for k,v in freeze(a.max_observed,a.mean_observed,a.basis).items() if k not in ('attestation','setup')},indent=1))
 elif a.mode=='login':login()
 elif a.mode=='cleanup':cleanup()
 elif a.mode=='count':print(len(freeze()['cells']))
 elif a.mode=='spend':pr=freeze();print(json.dumps({'spend_usd':spend(pr),'probe_usd':probe_spend(),'cap_usd':pr['round_cap_usd'],'estimate_usd':pr['admission_estimate_usd']}))
 else:
  try:run(a.index)
  except SystemExit:raise
  except Exception as ex:
   dump(R/'status-counted.json',{'utc':e.stamp(),'state':'stopped','index':a.index,'error':str(ex),'traceback':traceback.format_exc()})
   print(type(ex).__name__+': '+str(ex),file=sys.stderr);sys.exit(2)
