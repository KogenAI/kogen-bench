import datetime, json, os, pathlib, shutil, sys, time
P = pathlib.Path(os.environ.get('LANES_PRIVATE') or os.path.expanduser('~/lanes-work'))
S = pathlib.Path(os.environ.get('LANES_HIGH_ROUND_DIR') or os.path.expanduser('~/lanes-work/confirmation-eu-20261029'))
R = pathlib.Path(os.environ.get('LANES_CONFIRM_DIR') or os.path.expanduser('~/lanes-work/confirmation-eu-wide-20261029'))
assert not pathlib.Path('/run/kogen-host-lock.d').is_dir() or pathlib.Path('/run/kogen-host-lock.d/owner').read_text().strip() == 'research-confirm'  # original host's lease only
R.mkdir(exist_ok=False)
for name in ['harness', 'grader', 'source', 'bin', 'cache-snapshot']:
    (R/name).symlink_to(S/name, target_is_directory=True)
for name in ['tool-shell.py', 'cache-manifest.json', 'versions-final.json', 'build-receipt.json']:
    shutil.copy2(S/name, R/name)
for name in ['empty-login', 'empty-codex', 'login-loop', 'login-codex', 'tasks', 'qualification']:
    (R/name).mkdir()
(R/'outside-canary').write_text('private wider confirmation boundary canary\n')
specs = ['c3-tasks/inventory-go','c3-tasks/ledger-go','c5-tasks/logq-go','lvcc-tasks-e2/expr-match-go','lvcc-tasks-e2/goldmark-callouts-go','lvcc-tasks-e2/sh-globopts-go','nt-tasks/heatcal-go','rv-tasks/sync3-go']
for path in specs:
    src=P/path
    shutil.copytree(src,R/'tasks'/src.name,symlinks=True)
ext=(S/'confirmation_ext.py').read_text().replace(str(S),str(R))
ext=ext.replace('CAP=15.0','CAP=7.0')
ext=ext.replace("(body.get('reasoning') or {}).get('effort')!='high'", "(body.get('reasoning') or {}).get('effort')!=STATE['effort']")
ext=ext.replace("effort_requested='high'", "effort_requested=STATE['effort']")
needle="if row.get('model')!=MODEL or any(x['model']!=MODEL for x in row.get('response_models',[])):g.stop_reason='returned model identity mismatch'"
assert needle in ext
ext=ext.replace(needle,needle+"\n   if (row.get('reasoning') or {}).get('effort')!=STATE['effort'] or any((x.get('reasoning') or {}).get('effort')!=STATE['effort'] for x in row.get('response_models',[])):g.stop_reason='returned effort identity mismatch'")
(R/'confirmation_ext.py').write_text(ext)
os.environ.update(LANES_DIR=str(R/'grader'),PATH=GO_ROOT+'/bin:'+NODE_ROOT+'/bin:'+os.path.expanduser('~/.local/bin')+':/usr/bin:/bin',GOMAXPROCS='2',GOPROXY='off',GOTOOLCHAIN='local')
sys.path.insert(0,str(R/'grader'))
from lanes import common, grading
def save(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
rows=[]
for path in specs:
    name=path.split('/')[-1];td=R/'tasks'/name;task=grading.load_task(str(td))
    expected=set(task['eval'].get('expected',{}).get('requested',[])+task['eval'].get('expected',{}).get('regression',[]))
    requested=task['eval'].get('expected',{}).get('requested',[])
    entry={'task':name,'source':str(P/path),'tree_sha256':common.sha256_tree(str(td)),'runs':{},'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    overlays=['reference']+['wrong/'+p.name for p in sorted((td/'wrong').iterdir()) if p.is_dir()]
    for overlay in overlays:
        t=time.monotonic()
        with grading.scratch(str(td),overlay,export=True) as tree:
            result=grading.evaluate_tree(task,tree)
        save(R/'qualification'/(name+'--'+overlay.replace('/','-')+'.json'),result)
        passed=(bool(expected) and result['all_passed'] and not result['infrastructure'] and set(result['observed_ids'])==expected) if overlay=='reference' else (not result['infrastructure'] and any(result['ids'].get(i)=='failed' for i in requested))
        entry['runs'][overlay]={'qualifies':bool(passed),'all_passed':result['all_passed'],'infrastructure':result['infrastructure'],'wall_s':time.monotonic()-t,'observed_ids':len(result.get('observed_ids',[]))}
        print(json.dumps({'qualification':name,'overlay':overlay,**entry['runs'][overlay]}),flush=True)
        if overlay=='reference' and not passed:break
    entry['qualified']=len(overlays)>1 and len(entry['runs'])==len(overlays) and all(x['qualifies'] for x in entry['runs'].values())
    entry['drop_reason']=None if entry['qualified'] else 'Reference failed qualification or a wrong implementation did not fail requested tests; see runs and full grader receipts.'
    rows.append(entry);save(R/'eligibility.json',rows)
save(R/'preparation.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'uid':os.getuid(),'source':str(S),'source_protocol_sha256':common.sha256_file(str(S/'protocol.json')),'qualified':[r['task'] for r in rows if r['qualified']],'dropped':[r['task'] for r in rows if not r['qualified']],'qualification_rule':'fresh export reference passes all exact expected ids; every wrong tree fails at least one requested id without infrastructure error; inherited grader and default evaluator timeouts'})
print('Qualification complete',flush=True)
