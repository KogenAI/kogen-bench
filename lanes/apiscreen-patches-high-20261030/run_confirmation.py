import argparse,datetime,hashlib,json,os,pathlib,random,subprocess,sys,time,traceback
R=pathlib.Path(os.environ.get('LANES_CONFIRM_DIR') or os.path.expanduser('~/lanes-work/apiscreen-patches-high'))
CODEX_DIR=os.environ.get('CODEX_BIN_DIR') or os.path.expanduser('~/.codex/packages/standalone/releases/0.165.0-x86_64-unknown-linux-musl/bin')
GO_ROOT=os.environ.get('LANES_GOROOT') or os.path.expanduser('~/.local/share/mise/installs/go/1.27.2')
NODE_ROOT=os.environ.get('LANES_NODEROOT') or os.path.expanduser('~/.local/share/mise/installs/node/24.21.0')
LEDGER=os.environ.get('LANES_SPEND_LEDGER') or os.path.expanduser('~/lanes-work/api-spend-ledger.tsv')
os.chdir(R)
os.environ.update(LANES_DIR=str(R/'grader'),PATH=GO_ROOT+'/bin:'+NODE_ROOT+'/bin:'+os.path.expanduser('~/.local/bin')+':/usr/bin:/bin',GOMAXPROCS='2',GOPROXY='off',GOTOOLCHAIN='local')
sys.path[:0]=[str(R/'harness'),str(R/'grader'),str(R)]
import lanes_bare as h
import confirmation_ext as e
e.install(h)
SEED=20261030
CONTROL='speed2'
CANDIDATES=['api-replay','api-batch','api-answer-end']
ARMS=[CONTROL]+CANDIDATES
TASKS=['cron-go','readtime-go','artifact-go','vm-go']
PATCHED_BIN_DIR=pathlib.Path(os.environ.get('LANES_PATCHED_BIN_DIR') or os.path.expanduser('~/lanes-work/apiscreen-bins'))
BINARIES={'speed2':R/'bin/scr-speed2-kogen-loop','api-replay':PATCHED_BIN_DIR/'scr-api-replay-kogen-loop','api-batch':PATCHED_BIN_DIR/'scr-api-batch-kogen-loop','api-answer-end':PATCHED_BIN_DIR/'scr-api-answer-end-kogen-loop'}

def dump(p,d):e.write(p,d)
def stamp():return e.stamp()
def binary(lane):return BINARIES[lane]
def fingerprints():
 from lanes import common
 return {'tasks':{n:common.sha256_tree(str(R/'tasks'/n)) for n in TASKS},'cache':common.sha256_tree(str(R/'cache-snapshot')),'grader_source':common.sha256_tree(str(R/'grader'),exclude=('.git','__pycache__')),'binaries':{n:common.sha256_file(str(binary(n))) for n in ARMS},'extension':common.sha256_file(str(R/'confirmation_ext.py')),'harness':{n:common.sha256_file(str(R/'harness'/n)) for n in ('lanes_bare.py','lanes-bare.sh','pubagg.py','paired.py','pubmetrics.py')},'driver':common.sha256_file(str(R/'run_confirmation.py'))}
def freeze():
 path=R/'protocol-frozen.json'
 if path.exists():return json.loads(path.read_text())
 rng=random.Random(SEED);cells=[];tasks=list(TASKS);rng.shuffle(tasks);orders=[]
 for task in tasks:
  order=list(ARMS);rng.shuffle(order);orders.append({'task':task,'arms':order})
  cells.extend({'task':task,'rep':1,'arm':'loop','lane':lane,'stratum':'patches-high'} for lane in order)
 d={'frozen_utc':stamp(),'seed':SEED,'tasks_randomized':orders,'arms':{n:{'binary':str(binary(n)),'instructions':'shipped default'} for n in ARMS},'model':e.MODEL,'effort':'high','route':'external gateway to OpenAI Responses; default service tier; zero upstream retries','cells':cells,'cell_order':'one cell at a time; arms interleaved and randomized within each task; one rep','cap_usd':3.0,'request_reservation_policy':'before every upstream request, reserve its conservative maximum against cumulative patch-pass spend and the $3 cap','instructions':'shipped default for all four binaries','cache':'EU standard-library Go cache snapshot, restored before each cell','containment':'frozen API screen bubblewrap boundary and negative probe before every cell','host':'Linux laptop, unprivileged benchmark user','host_lock':'the host lease was held by its owner; this driver neither acquired nor released it','grading':'copied unchanged EU lanes grader; final-tree archive graded outside agent namespace','attestation':fingerprints()}
 dump(path,d);return d

def host_check():
 lease=pathlib.Path('/run/kogen-host-lock.d')  # the original host's lease; a host without one skips this check
 if lease.is_dir():
  owner=(lease/'owner').read_text().strip()
  assert owner=='research-apiscreen',f'unexpected held lease owner {owner}'
  expires=float((lease/'expires').read_text().strip())
  if time.time()+600>expires:raise RuntimeError('less than ten minutes remain in the existing owner lease')
 rows=subprocess.check_output(['ps','-u',os.environ.get('LANES_USER') or os.environ['USER'],'-o','pid=,ppid=,pgid=,comm=,args='],text=True)
 own={os.getpid(),os.getppid()};busy=[]
 for line in rows.splitlines():
  x=line.strip().split(None,4)
  if len(x)<5:continue
  pid,ppid,pgid,comm,args=x;pid=int(pid);ppid=int(ppid)
  if pid in own or (comm in ('ps','bash','sh','sudo') and ppid in own):continue
  if any(z in comm for z in ('kogen','codex','compile','link')) or comm in ('go','node','npm','npx') or ('python' in comm and 'run_confirmation.py' not in args):busy.append(line)
 if busy:raise RuntimeError('other lanes/model/build process active: '+repr(busy))
 return {'utc':stamp(),'load_1m':os.getloadavg()[0],'processes':rows,'lock_owner':owner,'lock_expires':expires,'own_pid':os.getpid(),'own_pgid':os.getpgrp()}

def launched():
 total=0.0
 for p in (R/'cells').glob('*/r*/*/route-summary.json'):
  d=json.loads(p.read_text());total+=d.get('usd_list') or d.get('charge_upper_bound_usd') or 0
 return total

def ledger_row(c,out,route):
 receipts=[];p=out/'route-receipts.jsonl'
 if p.exists():
  for line in p.read_text().splitlines():
   try:receipts.append(json.loads(line))
   except ValueError:pass
 rows=[x for x in receipts if x.get('forwarded')]
 usage=[x.get('usage') or {} for x in rows]
 inp=sum((u.get('input_tokens') or 0) for u in usage);cached=sum(((u.get('input_tokens_details') or {}).get('cached_tokens') or 0) for u in usage);output=sum((u.get('output_tokens') or 0) for u in usage)
 cost=sum(e.cost(u) for u in usage if u)
 return {'utc':stamp(),'experiment':f"apiscreen-lm/{c['stratum']+'-v2' if c['stratum']=='counted' else c['stratum']}/cells/{c['task']}/r{c['rep']}/{c['lane']}",'provider':'openai','model':e.MODEL,'requests':len(rows),'input_tokens':inp,'cached_tokens':cached,'output_tokens':output,'usd_list':cost,'note':f"common Responses endpoint; high; experiment-wide $3 request reservation including prior charges; cache_write="+str(sum((((u.get('input_tokens_details') or {}).get('cache_creation_tokens')) or 0) for u in usage))}

def make_args(c,run):
 return argparse.Namespace(tasks=str(R/'tasks'),task=c['task'],arm='loop',run_dir=str(run),rep=c['rep'],lane=c['lane'],model=e.MODEL,effort='high',provider='openai-compatible',loop_instructions=None,home=str(R/'empty-login'),codex_home=None,loop_bin=str(binary(c['lane'])),intent_form='gherkin',deadline_s=h.DEADLINE_S,force=False,keep=False,no_grade=False,cpu_profile=True,host='Linux laptop',kogen_models=None)

def cell(c):
 run=R;out=run/'cells'/c['task']/('r'+str(c['rep']))/c['lane']
 if (out/'result.json').exists():raise RuntimeError('cell already exists; never auto-replace')
 spent=launched()
 if spent>=e.CAP:raise RuntimeError('no remaining screen spend under the $4 cap')
 receipt=host_check();frozen=json.loads((R/'protocol-frozen.json').read_text())
 if fingerprints()!=frozen['attestation']:raise RuntimeError('frozen source, binary, task or cache changed')
 dump(R/('next-cell-'+c['stratum']+'.json'),{'cell':c,'host_preflight':receipt,'prior_screen_spend_usd':spent,'remaining_experiment_cap_usd':e.CAP-spent})
 e.STATE['prior_spend']=spent
 result=h.run_cell(make_args(c,run));dump(out/'host-preflight.json',receipt)
 after=fingerprints()==frozen['attestation'];dump(out/'provenance.json',{'protocol_sha256':hashlib.sha256((R/'protocol-frozen.json').read_bytes()).hexdigest(),'before_verified':True,'after_verified':after})
 if not after:raise RuntimeError('post-cell provenance changed')
 route=json.loads((out/'route-summary.json').read_text()) if (out/'route-summary.json').exists() else None
 row=ledger_row(c,out,route or {});dump(out/'ledger-row.json',row)
 with (R/'cell-ledger.jsonl').open('a') as f:f.write(json.dumps({'utc':stamp(),'cell':c,'result_path':str(out/'result.json'),'outcome':result.get('outcome'),'all_passed':result.get('all_passed'),'route':route,'ledger_row':row})+'\n')
 with open(LEDGER,'a') as ledger:
  ledger.write('\t'.join(str(row[k]) for k in ('utc','experiment','provider','model','requests','input_tokens','cached_tokens','output_tokens','usd_list','note'))+'\n')
 print(json.dumps({'cell':c,'outcome':result.get('outcome'),'passed':result.get('all_passed'),'agent_wall':result.get('totals',{}).get('wall_s'),'route':route,'ledger_row':row}),flush=True)
 if not route or route['stop_reason'] or not route['all_usage_present'] or set(route['response_models'])!={e.MODEL}:raise RuntimeError('cell failed infrastructure/route/usage gate; no replacement')
 if c['lane']!='speed2':
  receipts=[json.loads(x) for x in (out/'route-receipts.jsonl').read_text().splitlines() if x.strip()]
  if c['lane']=='api-replay': witness=any(x.get('client_path','').endswith('/responses') and 'reasoning.encrypted_content' in (x.get('include') or []) for x in receipts)
  elif c['lane']=='api-batch': witness=any(x.get('batch_instruction_present') for x in receipts)
  else: witness=any(x.get('tool_names') and 'finish' not in x.get('tool_names',[]) for x in receipts)
  if not witness:raise RuntimeError('candidate first-cell patch witness missing: '+c['lane'])
  dump(out/'patch-witness.json',{'arm':c['lane'],'verified':True,'receipts':len(receipts),'witness':'native Responses encrypted reasoning include' if c['lane']=='api-replay' else ('batched independent I/O instruction' if c['lane']=='api-batch' else 'finish tool omitted from default terminal definitions')})
 
 return result

p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','dry','counted']);p.add_argument('index',nargs='?',type=int);a=p.parse_args();protocol=freeze()
try:
 if a.mode=='prepare':print(json.dumps({'protocol_sha256':hashlib.sha256((R/'protocol-frozen.json').read_bytes()).hexdigest(),'seed':protocol['seed'],'counted_cells':len(protocol['cells']),'experiment_cap_usd':e.CAP,'arms':ARMS}),flush=True)
 elif a.mode=='dry':raise RuntimeError('no dry cell in this pre-screened patch protocol')
 else:
  if a.index is None or not 0<=a.index<len(protocol['cells']):raise RuntimeError('counted cell index must identify one frozen cell')
  cell(protocol['cells'][a.index])
except Exception as ex:
 dump(R/('status-patches-high-'+a.mode+'.json'),{'utc':stamp(),'state':'stopped','mode':a.mode,'index':a.index,'error':str(ex),'traceback':traceback.format_exc(),'spend_upper_bound_usd':launched()})
 print(type(ex).__name__+': '+str(ex),file=sys.stderr);sys.exit(2)
