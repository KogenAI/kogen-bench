#!/usr/bin/env python3
"""Freeze control files, full input tree and both kit pins before launching."""
import hashlib,json,os,stat,sys,subprocess
from pathlib import Path
from validity import tree_hash
ROOT=Path(__file__).resolve().parent
DYNAMIC={'HARNESS-SHA256','LANGUAGE-EPOCHS.json','FREEZE.json','ARMS','CODEX_HOME','START','DEADLINE','CAP_MIN','STOP','DONE','locks.tsv','stopper.sh','INCIDENTS.md'}
def kit_hash(path):
    h=hashlib.sha256()
    for p in sorted(Path(path).rglob('*')):
        if 'score-pool' in p.parts:continue
        rel=p.relative_to(path).as_posix()
        if p.is_symlink():value='L '+os.readlink(p)
        elif p.is_file():value='F '+hashlib.sha256(p.read_bytes()).hexdigest()+' '+str(bool(p.stat().st_mode&0o111))
        else:continue
        h.update((rel+'\0'+value+'\n').encode())
    return h.hexdigest()
def manifest(root=ROOT):
    root=Path(root)
    result={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.iterdir())
            if p.is_file() and p.name not in DYNAMIC and not p.name.startswith(('STOP-','.'))}
    for arm in 'abcd':
        if (root/'spec-subsets'/arm).exists():result['spec-subsets/'+arm]=tree_hash(root/'spec-subsets'/arm)
    return result
def validate_inputs(root=ROOT):
    root=Path(root)
    if sys.platform.startswith('linux') and not os.access(root/'inputs/conformance',os.R_OK):
        got=subprocess.check_output(['sudo','-n','/usr/local/sbin/race6-suite-verify',str(root)],text=True).strip()
    else:got=tree_hash(root/'inputs',frozen=True)
    return got==(root/'inputs.sha').read_text().strip()
def check(root=ROOT):
    root=Path(root)
    assert not json.loads((root/'SPEC-SPLIT-DECISIONS.json').read_text())['unresolved'],'unresolved split decisions'
    for name in ('ELIXIR-KIT-SHA256','GO-KIT-SHA256'):
        if (root/name).exists():assert (root/name).read_text()==(root/'KIT-SHA256').read_text(),name+' differs from full race5 kit pin'
    pin=json.loads((root/'FREEZE.json').read_text())
    assert pin==manifest(root),'control files changed after freeze'
    assert validate_inputs(root),'inputs changed'
    kit=Path(os.environ.get('RACE6_KIT_DIR',str(root.parent/'race6-kit')))
    assert kit_hash(kit/'quint')==(root/'QUINT-KIT-SHA256').read_text().strip(),'Quint kit changed'
    (root/'out').mkdir(exist_ok=True)
    output=subprocess.check_output(['bash',str(root/'kitsum.sh')],text=True,env=dict(os.environ,RACE_KIT_MANIFEST=str(root/'out/kit-manifest.sha256')))
    import re
    assert re.search(r'\bhash ([0-9a-f]{64})',output)[1]==(root/'KIT-SHA256').read_text().strip(),'TS kit changed'
    local=root/'out/host-inventory/hidden-inventory.json'
    if local.exists():assert hashlib.sha256(local.read_bytes()).hexdigest()==(local.parent/'INVENTORY-SHA256').read_text().strip(),'host inventory changed after admission'
    print('PASS rule, split, briefs, inputs, both kits and harness freeze')
if __name__=='__main__':
    if '--check' in sys.argv:check()
    elif '--pin-quint' in sys.argv:
        kit=Path(os.environ.get('RACE6_KIT_DIR',str(ROOT.parent/'race6-kit')))
        (ROOT/'QUINT-KIT-SHA256').write_text(kit_hash(kit/'quint')+'\n')
    else:
        assert not (ROOT/'FREEZE.json').exists(),'already frozen; make a fresh reviewed preparation to change it'
        (ROOT/'FREEZE.json').write_text(json.dumps(manifest(),indent=2,sort_keys=True)+'\n')
        check()
