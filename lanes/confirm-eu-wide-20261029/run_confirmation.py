import argparse,datetime,hashlib,json,os,pathlib,random,shutil,subprocess,sys,time,traceback
R=pathlib.Path(os.environ.get('LANES_CONFIRM_DIR') or os.path.expanduser('~/lanes-work/confirmation-eu-wide-20261029'))
CODEX_DIR=os.environ.get('CODEX_BIN_DIR') or os.path.expanduser('~/.codex/packages/standalone/releases/0.165.0-x86_64-unknown-linux-musl/bin')
GO_ROOT=os.environ.get('LANES_GOROOT') or os.path.expanduser('~/.local/share/mise/installs/go/1.27.2')
NODE_ROOT=os.environ.get('LANES_NODEROOT') or os.path.expanduser('~/.local/share/mise/installs/node/24.21.0')
LEDGER=os.environ.get('LANES_SPEND_LEDGER') or os.path.expanduser('~/lanes-work/api-spend-ledger.tsv')
os.chdir(R)
os.environ.update(LANES_DIR=str(R/'grader'),PATH=GO_ROOT+'/bin:'+NODE_ROOT+'/bin:'+os.path.expanduser('~/.local/bin')+':/usr/bin:/bin',GOMAXPROCS='2',GOPROXY='off',GOTOOLCHAIN='local')
sys.path[:0]=[str(R/'harness'),str(R)]
import lanes_bare as h
import confirmation_ext as e
e.install(h)
PROTOCOL_PATH=R/'protocol.json'
SEED=2026102908

def dump(p,d):e.write(p,d)
def fingerprints():
 from lanes import common
 codex=pathlib.Path(CODEX_DIR)
 return {'tasks':{n:common.sha256_tree(str(R/'tasks'/n)) for n in sorted(p.name for p in (R/'tasks').iterdir())},'cache':common.sha256_tree(str(R/'cache-snapshot')),'grader_source':common.sha256_tree(str(R/'grader'),exclude=('.git','__pycache__')),'loop_source':common.sha256_tree(str(R/'source/kogen-loop'),exclude=('.git','__pycache__')),'binaries':{str(p):common.sha256_file(str(p)) for p in [R/'bin/loop-b8a4046',codex/'codex',codex/'codex-code-mode-host']},'shell_wrapper':common.sha256_file(str(R/'tool-shell.py')),'extension':common.sha256_file(str(R/'confirmation_ext.py')),'harness':common.sha256_file(str(R/'harness/lanes_bare.py')),'driver':common.sha256_file(str(R/'run_confirmation.py'))}

def freeze():
 path=R/'protocol.json'
 if path.exists():return json.loads(path.read_text())
 rng=random.Random(SEED)
 admitted=[x['task'] for x in json.loads((R/'eligibility.json').read_text()) if x['qualified']]
 assert admitted,'no task qualified'
 rng.shuffle(admitted)
 labels=['loop-medium','codex-medium','loop-high','codex-high'];rng.shuffle(labels)
 # Four Williams rows, twice each at eight tasks, balance positions and ordered adjacencies.
 williams=[[0,1,3,2],[1,2,0,3],[2,3,1,0],[3,0,2,1]]
 rows=[williams[i%4] for i in range(len(admitted))];rng.shuffle(rows)
 cells=[{'task':t,'rep':1,'arm':labels[j],'client':labels[j].split('-')[0],'effort':labels[j].split('-')[1],'stratum':'counted'} for t,row in zip(admitted,rows) for j in row]
 inherited=json.loads((R.parent/'confirmation-eu-20261029/protocol.json').read_text())
 protocol={k:v for k,v in inherited.items() if k not in ('cells','dry','effort','attestation','files_sha256','infrastructure_pilots','exposure_limit','max_request_bytes')}
 protocol['request_size_policy']='No local request-size refusal; forward measured request sizes to the provider and preserve its response. Record received and forwarded request bytes per request.'
 protocol.update(frozen_utc=e.stamp(),seed=SEED,tasks_randomized=admitted,cells=cells,dry=[],arms=['loop-medium','codex-medium','loop-high','codex-high'],efforts=['medium','high'],cap_usd=7,per_cell_estimate_usd=e.CELL_ESTIMATE,budget_policy='Admit only when round spend plus conservative cell estimate fits cap; once admitted, never stop for budget. Estimates are not hard bounds. No timeout changes.',order='seeded shuffled task blocks and Williams four-arm rows; at eight tasks every arm occupies each position twice and every directed adjacency twice; one cell including grading at a time',analysis='One repetition. All counted attempts retained. Median and nearest-rank p90 over graded launched cells, failure included. U/C/O tokens and USD per pass use all counted attempts in numerators. Pair loop versus Codex within task and effort; exact two-sided sign test on nonzero wall/cost differences and discordant grades, ties removed. Descriptive selected Go task sample; no general equivalence or non-inferiority claim.',qualification='Fresh reference and all wrong trees with inherited evaluator; reference must pass exact expected ids, each wrong must fail requested tests without infrastructure errors; drop failing tasks.',exposure_limit='Eight user-selected inherited kits, not claimed fresh or randomly sampled. One rep cannot establish within-task variance. Efforts interleaved; provider cache remains observable.',reuse='Original confirmation extension, harness, binaries, source, cache and grader; run root, effort gate and budget parameterized; medium-run process ownership recorder reused; each scheduled cell is invoked separately so local ledger synchronization precedes the next cell; logins restored using each tool real stdin login if absent.',attestation=fingerprints())
 dump(path,protocol)
 return protocol

def make_args(c,run):
 return argparse.Namespace(tasks=str(R/'tasks'),task=c['task'],arm=c['client'],run_dir=str(run),rep=c['rep'],lane=c['arm'],model=e.MODEL,effort=c['effort'],provider='openai-compatible',loop_instructions=None,home=str(R/'empty-login'),codex_home=str(R/'empty-codex'),loop_bin=str(R/'bin/loop-b8a4046'),codex_bin=CODEX_DIR+'/codex',intent_form='gherkin',deadline_s=h.DEADLINE_S,force=False,keep=False,no_grade=False,cpu_profile=True,host='EU',kogen_models=None)

def host_check():
 lease=pathlib.Path('/run/kogen-host-lock.d')  # the original host's lease; a host without one skips this check
 if lease.is_dir():
  assert (lease/'owner').read_text().strip()=='research-confirm'
  expires=float((lease/'expires').read_text().strip())
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
 spent=launched();admission=e.admit_cell(spent)
 e.STATE['effort']=c['effort']
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

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['preflight','counted','cell']);p.add_argument('--index',type=int);a=p.parse_args();protocol=freeze()
 try:
  if a.mode=='preflight':
   for client in ('loop','codex'):
    c={'task':protocol['tasks_randomized'][0],'arm':client}
    preflight_only(c)
  elif a.mode=='cell':
   assert a.index is not None and 0<=a.index<len(protocol['cells'])
   for earlier in protocol['cells'][:a.index]:
    assert (R/earlier['stratum']/'cells'/earlier['task']/('r'+str(earlier['rep']))/earlier['arm']/'result.json').is_file(),'previous scheduled cell missing'
   c=protocol['cells'][a.index]
   print(json.dumps({'starting':c,'index':a.index,'utc':e.stamp()}),flush=True)
   cell(c)
   if a.index==len(protocol['cells'])-1:dump(R/'status-counted.json',{'utc':e.stamp(),'state':'complete','mode':'counted','spend_upper_bound_usd':launched()})
  else:
   for c in protocol['cells']:
    print(json.dumps({'starting':c,'utc':e.stamp()}),flush=True)
    cell(c)
  dump(R/('status-'+a.mode+('-'+str(a.index) if a.mode=='cell' else '')+'.json'),{'utc':e.stamp(),'state':'complete','mode':a.mode,'spend_upper_bound_usd':launched()})
 except Exception as ex:
  dump(R/('status-'+a.mode+('-'+str(a.index) if a.mode=='cell' else '')+'.json'),{'utc':e.stamp(),'state':'stopped','mode':a.mode,'error':str(ex),'traceback':traceback.format_exc(),'spend_upper_bound_usd':launched()})
  print(type(ex).__name__+': '+str(ex),file=sys.stderr);sys.exit(2)
