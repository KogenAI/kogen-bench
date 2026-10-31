"""edit5 setup on EU (run as lanes): LOOP-GAPS lever 5, a patch-edit tool shaped like the one the model was
trained on (apply_patch) vs loop default vs Codex at HIGH. Run dir with the EU replay round's harness, grader and
GOCACHE snapshot (same symlink targets as confirmation-eu-replay-20261030, attested against its protocol), the two
loop binaries built in one command on EU (b8a4046 source, and the same source plus edit5-apply-patch.diff), the
replay round's gateway extension with its run-dir path changed plus measurement-only receipts (each response's
tool calls; new tool outputs), and the candidate tasks qualified under the unchanged confirm5 rule."""
import datetime,hashlib,json,os,pathlib,shutil,sys,time
P=pathlib.Path(os.environ['TASKS_SRC']).resolve()  # task kits (private): c3-tasks, c5-tasks, rv-tasks, nt-tasks, lvcc-tasks-e2
R=pathlib.Path(os.environ['EDIT5_ROOT']).resolve()  # run root to create
EU_R=os.environ['EU_REPLAY_ROOT']  # run-root path string embedded in confirmation_ext.eu.py
# Pre-registered (31 Oct). Fresh = not used by replayconf, batchconf, batchtool, wcheck12 or eu6 (the brief's
# list); every other Go kit on EU/eu2 is used by those rounds or is an rv-tasks rewording. These are the
# confirm5/wide/replay kits (29-30 Oct; not lever-5 evidence: apidiag used wcheck12's four tasks). Order: the
# four cheapest by the replay round's measured cost, then goldmark-callouts (a longer edit task); the first five
# that qualify run. sh-globopts and expr-match are reserves ($1.1-1.7 per three-arm block; they do not fit the
# $10 cap twice). Sources are the replay round's own (eligibility.json there).
CANDIDATES=['c3-tasks/inventory-go','c5-tasks/logq-go','rv-tasks/sync3-go','nt-tasks/heatcal-go','lvcc-tasks-e2/goldmark-callouts-go','lvcc-tasks-e2/sh-globopts-go','lvcc-tasks-e2/expr-match-go']
WANT=5
EXCLUDED={'cron-go','readtime-go','artifact-go','vm-go',  # wcheck12
 'tengo-switch-go','tally-periodic-go','toml-required-go','expr-seqfuncs-go','moneyledger-go','pool-go',  # batchtool's six
 'bytefmt-go','deps-go','argvsplit-go','semrange-go','r70-5-go','splitter-go','jobq-go','wrapcol-go','r70-7-go','patchapply-go','task-tags-go','csvq-go','decround-go','isocal-go',  # replayconf
 'spans-go','r70-1-go','tokenbucket-go','rate-go','r70-4-go','tengo-power-go','tally-commodities-go','cadence-go','shardpool-go','goose-labels-go',  # batchconf
 'taskorder-go','urlnorm-go','revive-baseline-go'}  # eu6
assert not EXCLUDED.intersection(c.split('/')[-1] for c in CANDIDATES)
DRY_TASK='ledger-go'  # replayconf's and eu6's dry task; dry only, never counted
CODEX_DIR=pathlib.Path(os.environ['CODEX_BIN']).resolve().parent  # Codex CLI 0.165.0 (x86_64-unknown-linux-musl)
KOGEN=pathlib.Path(os.environ['KOGEN_BIN'])  # kogen CLI used for the loop arms' stdin login
ENV=dict(LANES_DIR=str(R/'grader'),PATH=os.environ['PATH'],GOMAXPROCS='2',GOPROXY='off',GOTOOLCHAIN='local')
BINS={'loop-edit5-base':'670055db9d4b72dc6b0554b3861ef0bbaf53a9c5fe0d7794c1bdb86ebc2a5043','loop-edit5-edit':'47b1c01f57ce5f09fb5d654e6d7e3bc5b83d7e0a6447791a9d4c7a27d8ba1180'}
DIFF_SHA='c0973933bb274d08a0ad3dc724052f021904eed469769d44156b567d0904f26e'
def save(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()

RECORD='''
def output_calls(final):
 """Measurement only: the tool calls of one response (name, call id, argument text up to 64 KiB, its bytes)."""
 rows=[]
 for x in final.get('output') or []:
  if x.get('type') in ('function_call','custom_tool_call','local_shell_call'):
   text=x.get('arguments') if x.get('type')=='function_call' else x.get('input') if x.get('type')=='custom_tool_call' else json.dumps(x.get('action'))
   text=text if isinstance(text,str) else json.dumps(text)
   rows.append({'type':x.get('type'),'name':x.get('name') or 'local_shell','call_id':x.get('call_id'),'bytes':len(text.encode()),'arguments':text[:65536]})
 return rows

def record_outputs(g,body):
 """Measurement only (shellwait's record_items, outputs only): the head of each new tool output the client sends."""
 try:
  seen=g.__dict__.setdefault('seen_outputs',set());rows=[]
  items=[]
  for x in body.get('input') or []:
   if isinstance(x,dict) and x.get('type') in ('function_call_output','custom_tool_call_output'):
    o=x.get('output');items.append((x.get('call_id'),o if isinstance(o,str) else json.dumps(o)))
  for m in body.get('messages') or []:
   if m.get('role')=='tool':
    o=m.get('content');items.append((m.get('tool_call_id'),o if isinstance(o,str) else json.dumps(o)))
  for cid,text in items:
   if cid in seen:continue
   seen.add(cid);text=text or ''
   rows.append({'request':len(g.rows)+1,'call_id':cid,'head':text[:300],'bytes':len(text.encode())})
  if rows:
   with (g.out/'tool-outputs.jsonl').open('a') as f:f.write(''.join(json.dumps(r)+'\\n' for r in rows))
 except Exception as e:
  with (g.out/'tool-outputs.jsonl').open('a') as f:f.write(json.dumps({'record_error':type(e).__name__})+'\\n')

def install(h):'''
EDITS=[  # (old, new): each old must occur exactly once
 ("raw=self.rfile.read(n);row['client_request_bytes']=len(raw);body=json.loads(raw)","raw=self.rfile.read(n);row['client_request_bytes']=len(raw);body=json.loads(raw);record_outputs(g,body)"),
 ("    if not client_stream and final is not None:","    if final is not None:row['output_calls']=output_calls(final)\n    if not client_stream and final is not None:"),
 ("\ndef install(h):",RECORD),
]

def setup():
 """R holds harness/grader/cache-snapshot symlinks (replay round targets), bin/ (two loop binaries), source/
 (base and edit trees), the diff, empty-codex, empty-login, outside-canary and the replay extension."""
 os.environ.update(ENV);sys.path.insert(0,str(R/'grader'))
 from lanes import common
 eu=json.loads((R/'eu-protocol.json').read_text())['attestation']
 ext=(R/'confirmation_ext.eu.py').read_text()
 assert sha(R/'confirmation_ext.eu.py')=='19c9755dd572750afd94f39d78b4d29dc8ec933377e77c3c7fc7fa1a79df7249' and ext.count(EU_R)==1
 ext=ext.replace(EU_R,str(R))
 for old,new in EDITS:
  assert ext.count(old)==1,old[:60];ext=ext.replace(old,new)
 (R/'confirmation_ext.py').write_text(ext)
 (R/'tasks').mkdir(exist_ok=True)
 if not (R/'tasks'/DRY_TASK).exists():shutil.copytree(P/'c3-tasks'/DRY_TASK,R/'tasks'/DRY_TASK,symlinks=True)
 here={'cache':common.sha256_tree(str(R/'cache-snapshot')),'grader_source':common.sha256_tree(str(R/'grader'),exclude=('.git','__pycache__')),'harness':common.sha256_file(str(R/'harness/lanes_bare.py')),
  'binaries':{**{k:sha(R/'bin'/k) for k in BINS},'codex':sha(CODEX_DIR/'codex'),'codex-code-mode-host':sha(CODEX_DIR/'codex-code-mode-host')},'diff':sha(R/'edit5-apply-patch.diff'),
  'source':{k:common.sha256_tree(str(R/'source'/k),exclude=('.git','__pycache__')) for k in ('base','edit')},'dry_task_'+DRY_TASK:common.sha256_tree(str(R/'tasks'/DRY_TASK))}
 eub={pathlib.Path(k).name:v for k,v in eu['binaries'].items()}
 checks={'cache':here['cache']==eu['cache'],'grader_source':here['grader_source']==eu['grader_source'],'harness':here['harness']==eu['harness'],
  'base source = attested loop source':here['source']['base']==eu['loop_source'],
  **{'binary '+k:here['binaries'][k]==v for k,v in BINS.items()},'binary codex':here['binaries']['codex']==eub['codex'],'binary codex-code-mode-host':here['binaries']['codex-code-mode-host']==eub['codex-code-mode-host'],
  'diff':here['diff']==DIFF_SHA,'dry task':here['dry_task_'+DRY_TASK]==eu['tasks'][DRY_TASK]}
 toolchains={'go':sha(shutil.which('go')),'node':sha(shutil.which('node')),'bwrap':sha('/usr/bin/bwrap'),'kogen_login_binary':sha(KOGEN)}
 expected_toolchains={'go':'548d3c32f83fa81152f543eb1526be7884cfe0526eb5e9ce29d3eca14786e7e0','node':'7fde7b8afa198da66257f42ee2001d874c7355631e6d1579a5fb5ef1f246df4c','bwrap':'e318903862396f96de3df57264e0158682b952fd3fb53ac23d876413e7b30f71','kogen_login_binary':'de3697827aa4b20987a8b34146519776aecbf246ab7a63beb2e42612b4792d7c'}
 checks.update({'toolchain '+k:toolchains[k]==v for k,v in expected_toolchains.items()})
 save(R/'setup.json',{'utc':now(),'origin':EU_R+' (harness/grader/cache via the wide-round symlinks)','eu_protocol_sha256':sha(R/'eu-protocol.json'),
  'eu_extension_sha256':sha(R/'confirmation_ext.eu.py'),'extension_sha256':sha(R/'confirmation_ext.py'),'extension_change':'run dir path (one occurrence); measurement-only receipts: output_calls per response (tool name, call id, arguments up to 64 KiB) and tool-outputs.jsonl (head of each new tool output)',
  'build':'on the run host, one command for both trees: CGO_ENABLED=1 GOFLAGS=-p=1 go build -o bin/loop-edit5-{base,edit} ./cmd/kogen-loop (go 1.27.2 linux/amd64); base tree = confirmation-eu-20261029/source/kogen-loop (the attested b8a4046 tree); version and capabilities --json of both equal those of loop-b8a4046 (611cbb9d...), the binaries differ only by the diff (the rebuilt base is not byte-identical to 611cbb9d: build path/cgo stamping)',
  'tests':'offline on EU as lanes before setup: gofmt clean, go vet ./tools ./loop ./conformance clean, go test ./tools/ ./loop/ ./conformance/ pass on the edit tree (default timeouts), including 8 new apply_patch tool tests and 2 session tests',
  'here':here,'toolchains':toolchains,'equal_to_expected':checks,'all_equal':all(checks.values())})
 print(json.dumps({'all_equal':all(checks.values()),'checks':checks}),flush=True)
 assert all(checks.values()),'EU copy differs from the replay attestation or the built files'

def qualify():
 os.environ.update(ENV);sys.path.insert(0,str(R/'grader'))
 from lanes import common,grading
 eu=json.loads((R/'eu-protocol.json').read_text())['attestation']
 (R/'qualification').mkdir(exist_ok=True)
 rows=[];n=0
 for path in [str(R/'tasks'/DRY_TASK)]+[str(P/c) for c in CANDIDATES]:
  name=pathlib.Path(path).name;dry=name==DRY_TASK
  if not dry and n>=WANT:break
  td=R/'tasks'/name
  if not dry:shutil.copytree(path,td,symlinks=True)
  task=grading.load_task(str(td))
  entry={'task':name,'source':path,'role':'dry' if dry else 'candidate','tree_sha256':common.sha256_tree(str(td)),'runs':{},'utc':now()}
  entry['tree_equals_replay_round_copy']=entry['tree_sha256']==eu['tasks'].get(name)
  expected=set(task['eval'].get('expected',{}).get('requested',[])+task['eval'].get('expected',{}).get('regression',[]))
  requested=task['eval'].get('expected',{}).get('requested',[])
  overlays=['reference']+['wrong/'+p.name for p in sorted((td/'wrong').iterdir()) if p.is_dir()]
  for overlay in overlays:
   t=time.monotonic()
   with grading.scratch(str(td),overlay,export=True) as tree:
    result=grading.evaluate_tree(task,tree)
   save(R/'qualification'/(name+'--'+overlay.replace('/','-')+'.json'),result)
   # The confirm5 wider-round rule (prepare_wide.py), unchanged.
   passed=(bool(expected) and result['all_passed'] and not result['infrastructure'] and set(result['observed_ids'])==expected) if overlay=='reference' else (not result['infrastructure'] and any(result['ids'].get(i)=='failed' for i in requested))
   entry['runs'][overlay]={'qualifies':bool(passed),'all_passed':result['all_passed'],'infrastructure':result['infrastructure'],'wall_s':round(time.monotonic()-t,3),'observed_ids':len(result.get('observed_ids',[]))}
   print(json.dumps({'qualification':name,'overlay':overlay,**entry['runs'][overlay]}),flush=True)
   if overlay=='reference' and not passed:break
  entry['qualified']=len(overlays)>1 and len(entry['runs'])==len(overlays) and all(x['qualifies'] for x in entry['runs'].values())
  if not entry['qualified'] and not dry:shutil.move(str(td),str(R/'qualification'/(name+'.dropped-tree')))
  if entry['qualified'] and not dry:n+=1
  rows.append(entry)
 save(R/'eligibility.json',rows)
 q=[r['task'] for r in rows if r['qualified'] and r['task']!=DRY_TASK]
 print(json.dumps({'qualified':q,'dry_task_qualified':rows[0]['qualified']}),flush=True)
 assert rows[0]['qualified'],'dry task failed requalification'
 assert len(q)>=4,'fewer than four tasks qualified'

if __name__=='__main__':
 {'setup':setup,'qualify':qualify}[sys.argv[1]]()
