import datetime,hashlib,json,os,pathlib,sys
R=pathlib.Path(os.environ.get('LANES_CONFIRM_DIR') or os.path.expanduser('~/lanes-work/confirmation-eu-wide-20261029'))
CODEX_DIR=os.environ.get('CODEX_BIN_DIR') or os.path.expanduser('~/.codex/packages/standalone/releases/0.165.0-x86_64-unknown-linux-musl/bin')
GO_ROOT=os.environ.get('LANES_GOROOT') or os.path.expanduser('~/.local/share/mise/installs/go/1.27.2')
NODE_ROOT=os.environ.get('LANES_NODEROOT') or os.path.expanduser('~/.local/share/mise/installs/node/24.21.0')
LEDGER=os.environ.get('LANES_SPEND_LEDGER') or os.path.expanduser('~/lanes-work/api-spend-ledger.tsv')
assert not pathlib.Path('/run/kogen-host-lock.d').is_dir() or pathlib.Path('/run/kogen-host-lock.d/owner').read_text().strip()=='research-confirm'  # original host's lease only
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
old=json.loads((R/'protocol.json').read_text())
assert len(list((R/'counted').glob('cells/*/r*/*/route-summary.json')))==4
failed=R/'counted/cells/sh-globopts-go/r1/loop-high'
assert not (failed/'route-receipts.jsonl').exists() and not (failed/'route-summary.json').exists()
result=json.loads((failed/'result.json').read_text())
assert result['outcome']=='harness_error' and result['detail']=='RuntimeError: actual tool namespace negative probe failed'
probe=json.loads((failed/'boundary-probe.json').read_text());actual=json.loads(probe['stdout'])
assert not actual['workspace_readable'] and actual['network_denied'] and all(actual['denials'].values())
archive=R/'infrastructure-prelaunch/cells/sh-globopts-go/r1/loop-high'
archive.parent.mkdir(parents=True,exist_ok=True)
failed.rename(archive)
old_protocol=R/'protocol.before-positive-probe-fix.json';old_protocol.write_bytes((R/'protocol.json').read_bytes())
old_ext=R/'confirmation_ext.before-positive-probe-fix.py';old_ext.write_bytes((R/'confirmation_ext.py').read_bytes())
ext=(R/'confirmation_ext.py').read_text();needle="pathlib.Path('Makefile').is_file()"
assert ext.count(needle)==1
ext=ext.replace(needle,"pathlib.Path('go.mod').is_file() and bool(pathlib.Path('go.mod').read_bytes())")
(R/'confirmation_ext.py').write_text(ext)
incident={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'Inherited positive workspace probe required Makefile, absent in sh-globopts. All containment denials passed. No model process or API request started.','zero_inference':True,'usd':0,'archived_directory':str(archive),'original_result_path':str(failed/'result.json'),'archived_files_sha256':{str(p.relative_to(R)):sha(p) for p in archive.rglob('*') if p.is_file()},'original_protocol_sha256':sha(old_protocol),'original_extension_sha256':sha(old_ext),'change':'Positive workspace check reads nonempty go.mod; all read/network denials and actual namespace mounts unchanged. No task, evaluator, cache, prompt, arm, order, timeout, model or spend limit changed.','completed_model_cells_before_amendment':4,'resume_scheduled_index':4,'model_attempts_replaced':0,'cell_ledger_mapping':'The original zero-call harness_error row result_path is relocated to archived_directory/result.json; retain original row and this mapping.'}
save(R/'positive-probe-incident.json',incident)
# Load the frozen driver functions without executing its command-line entry point.
source=(R/'run_confirmation.py').read_text();exec(compile(source[:source.index('p=argparse.ArgumentParser();')],str(R/'run_confirmation.py'),'exec'))
original_probe=e.probe
def every_probe(tmp,out,arm,env):return original_probe(tmp,R/'preflight-all'/e.STATE['task']/arm,arm,env)
e.probe=every_probe
for task in old['tasks_randomized']:
 for arm in ('loop','codex'):preflight_only({'task':task,'arm':arm})
new_fingerprints=fingerprints()
assert all(new_fingerprints[k]==old['attestation'][k] for k in old['attestation'] if k!='extension')
assert new_fingerprints['extension']==sha(R/'confirmation_ext.py')
new=dict(old);new['frozen_utc']=e.stamp();new['attestation']=new_fingerprints
new['amendments']=[{'reason':incident['reason'],'incident':'positive-probe-incident.json','prior_protocol_sha256':sha(old_protocol),'scope':incident['change'],'zero_inference_setup_abort_archived':str(archive),'existing_four_model_cells_retained':True,'all_eight_tasks_both_clients_preflight_passed':True}]
save(R/'protocol.json',new)
incident['new_protocol_sha256']=sha(R/'protocol.json');incident['new_extension_sha256']=sha(R/'confirmation_ext.py');incident['all_16_preflight_probes_passed']=True
save(R/'positive-probe-incident.json',incident)
print('Probe amendment complete; frozen order and prior model results retained',flush=True)
