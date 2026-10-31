"""edit5 driver on EU (lanes): LOOP-GAPS lever 5, a patch-edit tool in the shape the model was trained on, at HIGH.
Arms: loop-default (b8a4046 rebuilt on EU), apply-patch (the same tree plus edit5-apply-patch.diff, built in the same
command: Session offers apply_patch whenever write_file is enabled), Codex CLI 0.165.0 (fixed release dir); same gateway
extension, key, model and effort. One cell including grading at a time; blocks (task, rep) rep-major, the starting arm
rotated by block index. Admission only before a cell (measured estimate, round cap, one-request credit probe); an
admitted cell is never cut.
Exit codes: 0 done/skipped, 2 gate or error (stop), 3 admission stop (budget/credit), 4 host busy (nothing started),
5 pre-registered adoption stop (apply_patch unused in the first three counted apply-patch cells)."""
import argparse,hashlib,json,os,pathlib,re,subprocess,sys,time,traceback,urllib.request,urllib.error
R=pathlib.Path(os.environ['EDIT5_ROOT']).resolve()  # run root: harness, grader, bin/, tasks/, extension, protocol inputs
sys.path[:0]=[str(R/'harness'),str(R)]
os.environ.update(LANES_DIR=str(R/'grader'),PATH=os.environ['PATH'],GOMAXPROCS='2',GOPROXY='off',GOTOOLCHAIN='local')
import lanes_bare as h
import confirmation_ext as e
e.install(h)

ARMS=['loop-default','apply-patch','codex']
REPS=2
CAP_USD=9.50
DRY_TASK='ledger-go'
LOCK=pathlib.Path(os.environ.get('LANES_HOST_LOCK_DIR','/run/kogen-host-lock.d'));LOCK_OWNER='research-edit5'
BIN={'loop-default':R/'bin/loop-edit5-base','apply-patch':R/'bin/loop-edit5-edit'}
CODEX_BIN=pathlib.Path(os.environ['CODEX_BIN']).resolve()  # Codex CLI 0.165.0 (x86_64-unknown-linux-musl)
CODEX_DIR=CODEX_BIN.parent
KOGEN=os.environ['KOGEN_BIN']  # kogen CLI used for the loop arms' stdin login
PROTOCOL_PATH=R/'protocol.json'
PROBES=R/'probes.jsonl'
QUOTA_WORDS=('insufficient_quota','billing','quota','exceeded your current')
LOGINS=[R/'login-codex/auth.json',R/'login-loop/.kogen/credentials/openai-compatible.json']

# Registered edit classifier (also written into protocol.json, which the analysis reads). A call edits files when it
# is write_file or apply_patch, or when it is any other tool call (shell; Codex exec/exec_command/shell_command)
# whose command text matches one of these conservative patterns (cxpatch's detector: redirection of cat/echo/printf,
# tee, sed -i, perl -i, Python file writes, patch tools). gofmt -w and redirected test output are not edits.
FILE_EDIT_TOOLS=['write_file','apply_patch']
SHELL_EDIT_PATTERNS=[
 r"\bcat\b[^\n|;&]*>>?\s*(?!/dev/null)[^\s&|;>]",
 r"\btee\b(\s+-a)?\s+(?!/dev/)[^\s|;&-]",
 r"\bsed\b[^\n|;&]*\s-[a-zA-Z]*i",
 r"\bperl\b[^\n|;&]*\s-[a-zA-Z]*i",
 r"write_text\(|write_bytes\(|open\([^)\n]*,\s*['\"][wa]b?\+?['\"]|\.open\(\s*['\"][wa]b?\+?['\"]",
 r"\bapply_patch\b|\bgit\s+apply\b|\bpatch\s+-p\d",
 r"\b(printf|echo)\b[^\n|;&]*>>?\s*(?!/dev/null)[^\s&|;>]",
]
EDIT_RE=re.compile('|'.join('(?:%s)'%p for p in SHELL_EDIT_PATTERNS))

def call_text(c):
 """The command text of a call: the JSON string values joined (loop shell 'command', Codex 'cmd'/'command'), or the raw input."""
 try:
  v=json.loads(c['arguments'])
 except (ValueError,TypeError):
  return c.get('arguments') or ''
 out=[]
 def walk(x):
  if isinstance(x,str):out.append(x)
  elif isinstance(x,list):[walk(y) for y in x]
  elif isinstance(x,dict):[walk(y) for y in x.values()]
 walk(v);return '\n'.join(out)

def edit_kind(c):
 if c['name'] in FILE_EDIT_TOOLS:return c['name']
 if c['name'] in ('finish','read_file','list_files','search_text','view_image'):return None
 return 'shell_edit' if EDIT_RE.search(call_text(c)) else None

def dump(p,d):e.write(p,d)
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def cell_dir(c):return R/c['stratum']/'cells'/c['task']/('r'+str(c['rep']))/c['arm']

def fingerprints():
 from lanes import common
 return {'tasks':{n:common.sha256_tree(str(R/'tasks'/n)) for n in sorted(p.name for p in (R/'tasks').iterdir())},'cache':common.sha256_tree(str(R/'cache-snapshot')),'grader_source':common.sha256_tree(str(R/'grader'),exclude=('.git','__pycache__')),'loop_source':{k:common.sha256_tree(str(R/'source'/k),exclude=('.git','__pycache__')) for k in ('base','edit')},'diff':common.sha256_file(str(R/'edit5-apply-patch.diff')),'binaries':{str(p):common.sha256_file(str(p)) for p in [*BIN.values(),CODEX_DIR/'codex',CODEX_DIR/'codex-code-mode-host']},'shell_wrapper':common.sha256_file(str(R/'tool-shell.py')),'extension':common.sha256_file(str(R/'confirmation_ext.py')),'harness':common.sha256_file(str(R/'harness/lanes_bare.py')),'driver':common.sha256_file(str(R/'run_edit5.py'))}

def order(i):return ARMS[i%3:]+ARMS[:i%3]

def freeze(max_observed=None,mean_observed=None,basis=None):
 if PROTOCOL_PATH.exists():return json.loads(PROTOCOL_PATH.read_text())
 assert max_observed and mean_observed,'freeze needs the measured ledger figures'
 rows=json.loads((R/'eligibility.json').read_text())
 tasks=[r['task'] for r in rows if r['qualified'] and r['task']!=DRY_TASK]
 assert len(tasks)>=4
 blocks=[(t,r) for r in range(1,REPS+1) for t in tasks]
 cells=[{'task':DRY_TASK,'arm':a,'rep':1,'stratum':'dry'} for a in ARMS]+[{'task':t,'arm':a,'rep':r,'stratum':'counted'} for b,(t,r) in enumerate(blocks) for a in order(b)]
 estimate=round(max_observed*1.5,7);cap=CAP_USD
 assert cap<=10.0,'round cap above the $10 limit'
 setup=json.loads((R/'setup.json').read_text());assert setup['all_equal']
 protocol={'frozen_utc':e.stamp(),'id':'edit5-eu-20261031','host':'Hetzner server (2 cores, GOMAXPROCS=2), lanes user','tasks':tasks,'reps':REPS,'blocks':[list(b) for b in blocks],'dry_task':DRY_TASK,'cells':cells,'arms':ARMS,'model':e.MODEL,'effort':'high',
  'order':'dry first (ledger-go: loop-default, apply-patch, codex), then blocks rep-major (rep 1 of every task in qualification order, then rep 2); inside block b the arms run in ARMS rotated by b mod 3; one cell including grading at a time',
  'binaries':'loop-default = b8a4046 (confirmation-eu-20261029/source/kogen-loop, the attested tree) rebuilt on EU; apply-patch = the same tree plus edit5-apply-patch.diff (c0973933...); both built in one command on EU as lanes (go 1.27.2 linux/amd64, CGO_ENABLED=1, GOFLAGS=-p=1); version and capabilities --json equal to loop-b8a4046 611cbb9d...; Codex CLI 0.165.0 fixed release dir',
  'treatment':'apply_patch function tool (one string argument, input) whose description is the apply_patch section of Codex model instructions (codex-rs/core/gpt_5_1_prompt.md); the patch format, matcher (exact, then trailing whitespace, then both, then Unicode punctuation folded) and context-line handling port Codex apply-patch; all hunks are validated before any file changes; protected paths refused as write_file does. Offered by Session whenever write_file is enabled; write_file and the default instructions are unchanged (no instruction sentence: the tool alone)',
  'setup':setup,
  'edit_classifier':{'file_edit_tools':FILE_EDIT_TOOLS,'shell_edit_patterns':SHELL_EDIT_PATTERNS,'rule':'an edit call is write_file, apply_patch, or any other non-read tool call whose command text (JSON string values joined, or the raw freeform input) matches a shell-edit pattern; an edit turn is a forwarded response with >= 1 edit call (gateway receipt output_calls)'},
  'registration':{'question':'does a patch-edit tool in the shape gpt-6.1-terra was trained on (apply_patch) lower the output tokens loop generates on edit turns, and is it adopted, without raising cost per pass; same model/effort/key, Codex CLI as the reference',
   'primary':['output tokens on edit turns per run: sum of usage.output_tokens (reasoning included) over forwarded responses that make >= 1 edit call (edit_classifier), paired per block, exact two-sided sign test, ties dropped',
              'adoption: share of apply-patch cells with >= 1 apply_patch call, and apply_patch calls / all edit calls in the apply-patch arm (descriptive, with the stop rule below)',
              'cost per pass: per-arm total USD / passes; paired per block: cell USD where a failed cell counts as worse than any passed cell and two failed cells tie; exact two-sided sign test, ties dropped'],
   'primary_comparison':'apply-patch vs loop-default; apply-patch vs codex and loop-default vs codex reported the same way (Codex edit turns use the same classifier on its shell/exec text and its freeform apply_patch; descriptive)',
   'secondary':['agent wall s per cell (sign test)','requests per run (sign test)','pass (discordant pairs)'],
   'also_reported':'total, reasoning and non-reasoning output tokens, edit turns and edit calls by kind (write_file / apply_patch / shell_edit), apply_patch error results, per-task breakdown, per-arm totals; descriptive. Blocks of one task are repeated sessions, not independent tasks: the test is over blocks; per-task direction is also shown',
   'stop_rules':'adoption stop: after the third counted apply-patch cell, if none of the three made an apply_patch call, the round stops (the tool is not taken up, so it cannot change edit generation); otherwise only the spend guard (admission only) and the credit probe; no reruns or replacements; every launched cell is retained',
   'exclusions':'a cell with an infrastructure, identity or tool-definition gate failure is reported and the round stops (no replacement)',
   'power':'replayconf per-task log ratio between two equal loop arms (api-replay/loop-default) of output tokens on write_file turns: sd 0.262 (10 tasks with such turns). Under -30% edit-turn output P(block favours apply-patch)=Phi(0.357/0.262)=0.913; two-sided exact sign test p<0.05 needs 8/8, 9/10, 10/12; power n=8 0.48, n=10 0.79, n=12 0.92. Under -10% (P=0.66) power is 0.03-0.16 at n=8-12. The $10 cap at measured prices affords 5 tasks x 2 reps = 10 blocks (33 runs; expected $4.9, x1.5 = $7.4); 12 blocks of 6 tasks would need ~$10.7 at x1.5. So n=10 is registered: it resolves a large effect only. Cost per pass: the lever expects -3 to -8%, which this round cannot resolve; reported.'},
  'admission_estimate_rule':'largest per-run cost in api-spend-ledger.tsv on the EU clean route, gpt-6.1-terra HIGH, x1.5','admission_estimate_basis':basis,'admission_estimate_usd':estimate,
  'round_cap_rule':'fixed $9.50 (brief: <= $10), includes credit probes; expected spend = runs x measured mean per run of these tasks x 1.5','round_cap_basis':{'runs':len(cells),'mean_usd':mean_observed,'expected_x1_5_usd':round(len(cells)*mean_observed*1.5,6)},'round_cap_usd':cap,
  'budget_policy':'admit only before a cell; an admitted cell is never cut; usage, model and effort gates unchanged; no timeout changes (deadline = default 3600 s, bounded only by the lock lease, which the orchestrator keeps >= 4200 s ahead)',
  'credit_probe':'one minimal Responses request (max_output_tokens 16, effort low) on the same key before each admission; counted in spend; quota/billing errors stop admission',
  'dry_gate':'counted cells start only after all three dry cells finished with requests > 0 and identity/effort gates passed, every apply-patch request offered apply_patch and no loop-default request did, and every forwarded response carries the output_calls receipt (patch-witnesses.json); the tool-definition witness is checked on every counted loop cell',
  'credentials':'the OpenAI API key passed on stdin to both tools\' real stdin login commands into run-local stores; removed at the end',
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
 """Per cell from the gateway receipts: tool definitions offered, output_calls coverage, edit turns and their output."""
 out=cell_dir(c)
 rows=[json.loads(x) for x in (out/'route-receipts.jsonl').read_text().splitlines() if json.loads(x).get('forwarded')]
 offered=[('apply_patch' in (x.get('tool_names') or [])) for x in rows]
 kinds={'write_file':0,'apply_patch':0,'shell_edit':0};edit_turns=0;edit_out=0;out_total=0
 for x in rows:
  assert x['model']==e.MODEL and x['reasoning']['effort']=='high'
  u=x.get('usage') or {};out_total+=u.get('output_tokens',0)
  ks=[k for k in (edit_kind(cl) for cl in x.get('output_calls') or []) if k]
  for k in ks:kinds[k]+=1
  if ks:edit_turns+=1;edit_out+=u.get('output_tokens',0)
 return {'cell':str(out.relative_to(R)),'requests':len(rows),'apply_patch_offered':sum(offered),'output_calls_recorded':sum('output_calls' in x for x in rows),'edit_turns':edit_turns,'edit_turn_output_tokens':edit_out,'output_tokens':out_total,'edit_calls':kinds,'model_effort_verified':True}

def host_check():
 """Returns None when another lanes workload is active (nothing started)."""
 expires=None
 if LOCK.is_dir():  # the original host's lease; a host without one skips this check
  if (LOCK/'owner').read_text().strip()!=LOCK_OWNER:raise RuntimeError('host lock not held by '+LOCK_OWNER)
  expires=float((LOCK/'expires').read_text().strip())
  if time.time()+600>expires:raise RuntimeError('less than ten minutes remain in the lock lease')
 rows=subprocess.check_output(['ps','-u','lanes','-o','pid=,ppid=,pgid=,comm=,args='],text=True)
 own={os.getpid(),os.getppid()};busy=[]
 for line in rows.splitlines():
  x=line.strip().split(None,4)
  if len(x)<5:continue
  pid,ppid,pgid,comm,args=x
  if int(pid) in own or comm in ('ps','bash','sh','sudo','sshd') and int(ppid) in own:continue
  if any(z in comm for z in ('kogen','codex','claude','compile','link')) or comm in ('go','node','npm','npx') or ('python' in comm and 'run_edit5.py' not in args):busy.append(line)
 if busy:return None
 return {'utc':e.stamp(),'load_1m':os.getloadavg()[0],'lock_owner':LOCK_OWNER,'lock_expires':expires,'own_pid':os.getpid(),'own_pgid':os.getpgrp()}

def make_args(c):
 arm='codex' if c['arm']=='codex' else 'loop'
 return argparse.Namespace(tasks=str(R/'tasks'),task=c['task'],arm=arm,run_dir=str(R/c['stratum']),rep=c['rep'],lane=c['arm'],model=e.MODEL,effort='high',provider='openai-compatible',loop_instructions=None,home=str(R/'empty-login'),codex_home=str(R/'empty-codex'),loop_bin=str(BIN.get(c['arm'],BIN['loop-default'])),codex_bin=str(CODEX_BIN),intent_form='gherkin',deadline_s=h.DEADLINE_S,force=False,keep=False,no_grade=False,cpu_profile=True,host='EU',kogen_models=None)

def login():
 key=sys.stdin.readline().strip()
 assert key.startswith('sk-'),'no key on stdin'
 env=dict(os.environ);env['CODEX_HOME']=str(R/'login-codex')
 a=subprocess.run([str(CODEX_BIN),'-c','cli_auth_credentials_store="file"','login','--with-api-key'],input=key+'\n',env=env,text=True,capture_output=True,timeout=30)
 env=dict(os.environ);env['HOME']=str(R/'login-loop')
 b=subprocess.run([KOGEN,'provider','login','openai-compatible'],input=key+'\n',env=env,text=True,capture_output=True,timeout=30)
 assert a.returncode==b.returncode==0,'stdin login failed'
 assert json.loads(LOGINS[0].read_text())['OPENAI_API_KEY']==json.loads(LOGINS[1].read_text())['api_key']==key
 dump(R/'login.json',{'utc':e.stamp(),'uid':os.getuid(),'key':'OpenAI API key, passed on stdin','method':'both actual tools stdin login commands (fixed release paths); key held in memory only','commands_exit':[a.returncode,b.returncode],'keys_equal_in_memory':True,'contents_recorded':False,'kogen_login_binary_sha256':sha(KOGEN)})
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
  ap=[x for x in protocol['cells'][:index] if x['stratum']=='counted' and x['arm']=='apply-patch']
  if len(ap)>=3 and not any(witness(x)['edit_calls']['apply_patch'] for x in ap[:3]):
   dump(R/'status-counted.json',{'utc':e.stamp(),'state':'stopped','index':index,'error':'adoption stop: no apply_patch call in the first three counted apply-patch cells','spend_usd':spend(protocol)})
   print('adoption stop: no apply_patch call in the first three counted apply-patch cells',file=sys.stderr);sys.exit(5)
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
 wit=witness(c) if route and route.get('requests') else None
 with (R/'cell-ledger.jsonl').open('a') as f:f.write(json.dumps({'utc':e.stamp(),'index':index,'cell':c,'result_path':str(out/'result.json'),'outcome':result.get('outcome'),'all_passed':result.get('all_passed'),'route':route,'witness':wit},sort_keys=True)+'\n')
 print(json.dumps({'cell':c,'outcome':result.get('outcome'),'passed':result.get('all_passed'),'agent_wall':result.get('totals',{}).get('wall_s'),'usd':route and route.get('usd_list'),'requests':route and route.get('requests'),'witness':wit}),flush=True)
 if not route or not route['all_usage_present'] or not route['response_models'] or set(route['response_models'])!={e.MODEL}:raise RuntimeError('route, usage or model identity gate failed')
 receipts=[json.loads(x) for x in (out/'route-receipts.jsonl').read_text().splitlines() if json.loads(x).get('forwarded')]
 if any(x.get('model')!=e.MODEL or (x.get('reasoning') or {}).get('effort')!='high' for x in receipts):raise RuntimeError('identity/effort gate failed')
 if result.get('outcome') in ('harness_error','timeout') or route['stop_reason']:raise RuntimeError('infrastructure gate failed; no replacement')
 if c['arm']=='apply-patch' and wit['apply_patch_offered']!=wit['requests']:raise RuntimeError('tool-definition gate failed: apply_patch not offered on every request')
 if c['arm']=='loop-default' and wit['apply_patch_offered']:raise RuntimeError('tool-definition gate failed: loop-default offered apply_patch')
 if c['stratum']=='dry' and index==2:
  w={x['arm']:witness(x) for x in protocol['cells'][:3]}
  ok=all(v['requests']>0 and v['output_calls_recorded']==v['requests'] for v in w.values()) and w['apply-patch']['apply_patch_offered']==w['apply-patch']['requests'] and w['loop-default']['apply_patch_offered']==0
  dump(R/'patch-witnesses.json',{'utc':e.stamp(),'dry':w,'activation':'apply-patch offered apply_patch on every request, loop-default on none; output_calls recorded on every response' if ok else 'witness missing','dry_adoption':w['apply-patch']['edit_calls'],'dry_gate_passed':ok})
  if not ok:raise RuntimeError('dry gate failed: '+json.dumps(w))
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
