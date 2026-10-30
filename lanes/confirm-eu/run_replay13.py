import argparse,hashlib,json,os,pathlib,shutil,subprocess,sys,time,traceback,urllib.request,urllib.error
# replay13: resume the frozen confirmation-eu-replay-20261030 counted round from cell 6 with a measured
# admission estimate, a rescaled round cap, and a one-request credit probe before every admission.
R=pathlib.Path(__file__).resolve().parent
assert os.getuid()==int(os.environ.get('LANES_UID',os.getuid()))  # the run user's uid when set
sys.path.insert(0,str(R))
import run_confirmation as rc
from run_confirmation import e,h
FIRST=6  # cells 0-5 finished before this resume
BASELINE_USD=1.51963285  # counted spend of cells 0-5 (round-spend-accounting.json)
MAX_OBSERVED_USD=0.5632162  # largest ledger per-run cost, EU clean route, gpt-6.1-terra HIGH: confirmation-eu-wide-20261029/counted/cells/expr-match-go/r1/loop-high
ESTIMATE=round(MAX_OBSERVED_USD*1.5,7)
MEAN_USD=BASELINE_USD/6
CAP=round(18*MEAN_USD*1.5,6)
e.CELL_ESTIMATE=ESTIMATE;e.CAP=CAP
PROBES=R/'replay13-probes.jsonl'
QUOTA_WORDS=('insufficient_quota','billing','quota','exceeded your current')
LOGINS=[R/'login-codex/auth.json',R/'login-loop/.kogen/credentials/openai-compatible.json']

def summary(c):
 p=R/c['stratum']/'cells'/c['task']/('r'+str(c['rep']))/c['arm']/'route-summary.json'
 if not p.exists():return 0.
 d=json.loads(p.read_text());return d['usd_list'] if d.get('all_usage_present') else d['charge_upper_bound_usd']
def probe_spend():
 return sum(json.loads(x).get('usd',0.) for x in PROBES.read_text().splitlines()) if PROBES.exists() else 0.
def resumed_spend():
 protocol=json.loads(rc.PROTOCOL_PATH.read_text())
 return sum(summary(c) for c in protocol['cells'][FIRST:])+probe_spend()
rc.launched=resumed_spend

def amend():
 p=rc.PROTOCOL_PATH;backup=R/'protocol.before-replay13-20261030.json'
 d=json.loads(p.read_text())
 if any(a.get('id')=='replay13' for a in d.get('amendments',[])):print('amendment already present');return
 if not backup.exists():shutil.copy2(p,backup)
 d.setdefault('amendments',[]).append({'id':'replay13','utc':e.stamp(),'effective_from_cell_index':FIRST,'previous_protocol_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),
  'admission_estimate_rule':'largest observed per-run cost in api-spend-ledger.tsv on this EU clean route for gpt-6.1-terra at HIGH effort, times 1.5','admission_estimate_basis':{'usd':MAX_OBSERVED_USD,'row':'confirmation-eu-wide-20261029/counted/cells/expr-match-go/r1/loop-high'},'admission_estimate_usd':ESTIMATE,
  'round_cap_rule':'registered remaining runs x measured mean per-run cost of this round x 1.5; applies to spend from cell index 6 onward plus credit probes','round_cap_basis':{'remaining_runs':18,'measured_mean_usd':MEAN_USD,'measured_runs':6,'measured_total_usd':BASELINE_USD},'round_cap_usd':CAP,
  'reason':'the $4 cap with a frozen $2.50 estimate could not hold the registered 24-cell round at measured prices (six cells cost $1.519633, then admission stopped with 18 unstarted)',
  'credit_probe':'before each admission one minimal Responses request on the same key and upstream (max_output_tokens 16); counted in round spend and the ledger; insufficient_quota, billing or 429 quota errors stop admission',
  'unchanged':'cell list and order, arms, model, HIGH effort, identity/usage gates, timeouts, grader, binaries; an admitted cell is never cut for budget'})
 rc.dump(p,d);print('amended',hashlib.sha256(p.read_bytes()).hexdigest())

def login():
 source=R.parent/'confirmation-eu-overlap-20261030/login-codex/auth.json'
 key=json.loads(source.read_text())['OPENAI_API_KEY']
 codex=rc.CODEX_DIR+'/codex'
 kogen=(os.environ.get('KOGEN_LANES_HOME') or os.path.expanduser('~/.cache/kogen-lanes'))+'/unpacked/319d16843aaec9cecc79a2646f690efa1a857702ed650ac6d9288186e674b8e3/kogen-16102c97-linux-x86_64/bin/kogen'
 env=dict(os.environ);env['CODEX_HOME']=str(R/'login-codex')
 a=subprocess.run([codex,'-c','cli_auth_credentials_store="file"','login','--with-api-key'],input=key+'\n',env=env,text=True,capture_output=True,timeout=30)
 env=dict(os.environ);env['HOME']=str(R/'login-loop')
 b=subprocess.run([kogen,'provider','login','openai-compatible'],input=key+'\n',env=env,text=True,capture_output=True,timeout=30)
 assert a.returncode==b.returncode==0,'stdin login failed'
 assert json.loads(LOGINS[0].read_text())['OPENAI_API_KEY']==json.loads(LOGINS[1].read_text())['api_key']==key
 e.write(R/'replay13-login.json',{'utc':e.stamp(),'uid':os.getuid(),'method':'both actual tools stdin login commands (fixed release paths); key held in memory only','commands_exit':[a.returncode,b.returncode],'keys_equal_in_memory':True,'contents_recorded':False})
 print('Both stdin logins completed',flush=True)

def cleanup():
 for p in LOGINS:p.unlink(missing_ok=True)
 e.write(R/'replay13-credential-cleanup.json',{'utc':e.stamp(),'uid':os.getuid(),'method':'unlink only two run-local tool login files','credential_paths_absent':all(not p.exists() for p in LOGINS)})
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

def stop(index,reason):
 rc.dump(R/'status-counted.json',{'utc':e.stamp(),'state':'stopped','index':index,'error':reason,'spend_upper_bound_usd':BASELINE_USD+resumed_spend(),'resumed_spend_usd':resumed_spend(),'cap_usd':CAP,'estimate_usd':ESTIMATE})
 print(reason,file=sys.stderr);sys.exit(3)

def run(index):
 protocol=rc.freeze()
 assert any(a.get('id')=='replay13' for a in protocol.get('amendments',[])),'replay13 amendment missing'
 assert FIRST<=index<len(protocol['cells'])
 for previous in protocol['cells'][:index]:
  assert (R/previous['stratum']/'cells'/previous['task']/('r'+str(previous['rep']))/previous['arm']/'result.json').exists(),'previous cell missing'
 assert (R/'patch-witnesses.json').exists(),'first replay witness not verified'
 c=protocol['cells'][index]
 if (R/c['stratum']/'cells'/c['task']/('r'+str(c['rep']))/c['arm']/'result.json').exists():print(json.dumps({'skip_finished':c}),flush=True);return
 spent=resumed_spend()
 if spent+ESTIMATE>CAP:stop(index,'round budget cannot admit next cell: resumed spend + measured estimate exceeds cap')
 p=probe(index)
 if not p['ok'] and p.get('quota'):stop(index,'stopped at admission: key out of credit ('+e.stamp()+')')
 if not p['ok']:
  time.sleep(60);p=probe(index)
  if not p['ok']:stop(index,'stopped at admission: key out of credit ('+e.stamp()+')' if p.get('quota') else 'stopped at admission: credit probe failed twice ('+str(p.get('http_status') or p.get('error'))+')')
 print(json.dumps({'starting':c,'index':index,'utc':e.stamp(),'resumed_spend_usd':resumed_spend(),'estimate_usd':ESTIMATE,'cap_usd':CAP,'probe_usd':p['usd']}),flush=True)
 try:
  rc.cell(c)
  rc.dump(R/('status-cell-'+str(index)+'.json'),{'utc':e.stamp(),'state':'complete','spend_upper_bound_usd':BASELINE_USD+resumed_spend(),'resumed_spend_usd':resumed_spend()})
  if index==len(protocol['cells'])-1:rc.dump(R/'status-counted.json',{'utc':e.stamp(),'state':'complete','spend_upper_bound_usd':BASELINE_USD+resumed_spend(),'resumed_spend_usd':resumed_spend(),'cap_usd':CAP})
 except Exception as ex:
  rc.dump(R/'status-counted.json',{'utc':e.stamp(),'state':'stopped','index':index,'error':str(ex),'traceback':traceback.format_exc(),'spend_upper_bound_usd':BASELINE_USD+resumed_spend()})
  print(type(ex).__name__+': '+str(ex),file=sys.stderr);sys.exit(2)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['amend','login','cell','cleanup','spend']);p.add_argument('--index',type=int);a=p.parse_args()
 if a.mode=='amend':amend()
 elif a.mode=='login':login()
 elif a.mode=='cleanup':cleanup()
 elif a.mode=='spend':print(json.dumps({'resumed_spend_usd':resumed_spend(),'probe_usd':probe_spend(),'cap_usd':CAP,'estimate_usd':ESTIMATE}))
 else:run(a.index)
