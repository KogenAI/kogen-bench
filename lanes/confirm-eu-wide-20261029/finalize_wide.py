import datetime, hashlib, json, os, pathlib
R=pathlib.Path(os.environ.get('LANES_CONFIRM_DIR') or os.path.expanduser('~/lanes-work/confirmation-eu-wide-20261029'))
CODEX_DIR=os.environ.get('CODEX_BIN_DIR') or os.path.expanduser('~/.codex/packages/standalone/releases/0.165.0-x86_64-unknown-linux-musl/bin')
GO_ROOT=os.environ.get('LANES_GOROOT') or os.path.expanduser('~/.local/share/mise/installs/go/1.27.2')
NODE_ROOT=os.environ.get('LANES_NODEROOT') or os.path.expanduser('~/.local/share/mise/installs/node/24.21.0')
LEDGER=os.environ.get('LANES_SPEND_LEDGER') or os.path.expanduser('~/lanes-work/api-spend-ledger.tsv')
assert json.loads((R/'validation.json').read_text())['counted']==len(json.loads((R/'protocol.json').read_text())['cells'])
assert json.loads((R/'status-counted.json').read_text())['state']=='complete'
paths=[R/'login-codex/auth.json',R/'login-loop/.kogen/credentials/openai-compatible.json']
for p in paths:
    if p.exists(): p.unlink()
cleanup={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'removed only the two temporary tool-owned login files created for this run','uid':os.getuid(),'credential_paths_absent':all(not p.exists() for p in paths),'original_local_key_untouched':True}
assert cleanup['credential_paths_absent']
if not (R/'credential-cleanup.json').exists():
    (R/'credential-cleanup.json').write_text(json.dumps(cleanup,indent=2)+'\n')
files={}
for d in ['qualification','counted','preflight','preflight-all','infrastructure-prelaunch']:
    for p in sorted((R/d).rglob('*')):
        if p.is_file() and not p.is_symlink(): files[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['confirmation_ext.py','run_confirmation.py','analyze_wide.py','validate_wide.py','finalize_wide.py','prepare_wide.py','amend_positive_probe.py','positive-probe-incident.json','budget-censoring-policy.json','protocol.before-positive-probe-fix.json','confirmation_ext.before-positive-probe-fix.py','protocol.json','preparation.json','build-receipt.json','cache-manifest.json','versions-final.json','eligibility.json','login-receipt.json','validation.json','credential-cleanup.json','cell-ledger.jsonl','process-groups.jsonl']:
    p=R/n;files[n]=hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['analysis.json','all-attempts.tsv','ledger-validation.json','ledger-rows.tsv','CONFIRMATION-RESULT.md']:
    p=R/n
    if p.is_file():files[n]=hashlib.sha256(p.read_bytes()).hexdigest()
attestation={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'uid':os.getuid(),'canonical_run':str(R),'files_sha256':files,'reused_asset_attestation':json.loads((R/'protocol.json').read_text())['attestation'],'validation':json.loads((R/'validation.json').read_text()),'logins_cleared':True,'host_lease_neither_acquired_nor_released':True}
(R/'attestation-final.json').write_text(json.dumps(attestation,indent=2)+'\n')
print(json.dumps({'credential_paths_absent':True,'attested_files':len(files)}))
