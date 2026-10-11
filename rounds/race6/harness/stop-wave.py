#!/usr/bin/env python3
"""All arm processes gone -> FINAL complete -> unlock -> audit -> DONE."""
import os,subprocess,time
from pathlib import Path
from processes import stop,arm_processes
from importlib.machinery import SourceFileLoader
host_idle=SourceFileLoader("score_admission",str(Path(__file__).resolve().parent/"score-admission.py")).load_module().host_idle
ROOT=Path(__file__).resolve().parent
def main():
    import json
    starts=json.loads((ROOT/'LANGUAGE-EPOCHS.json').read_text()) if (ROOT/'LANGUAGE-EPOCHS.json').exists() else {a:int((ROOT/'START').read_text()) for a in (ROOT/'ARMS').read_text().split()}
    for deadline in sorted({t+3600 for t in starts.values()}):
        while time.time()<deadline and not (ROOT/'STOP').exists():time.sleep(.5)
        selected=[a for a,t in starts.items() if t+3600==deadline]
        if (ROOT/'STOP').exists():selected=[a for a in starts if not (ROOT/'snapshots/FINAL'/a).exists()]
        stop(ROOT,selected)
        assert not arm_processes(ROOT,selected=selected),'refusing FINAL with live arm processes'
        for a in selected:subprocess.run([str(ROOT/'snap.sh'),'FINAL',a],check=True)
        if (ROOT/'STOP').exists():break
    stop(ROOT)
    assert not arm_processes(ROOT),'refusing unlock with live arm processes'
    assert all((ROOT/'snapshots/FINAL'/a).exists() for a in starts),'incomplete FINAL'
    while not host_idle():time.sleep(5)
    subprocess.run([str(ROOT/'unlock.sh')],check=True)
    if os.uname().sysname=='Linux':
        # Only this fixed-purpose sudo helper may expose the benchadmin suite.
        subprocess.run(['sudo','-n','/usr/local/sbin/race6-suite-release',str(ROOT)],check=True)
    with (ROOT/'out/audit.txt').open('w') as f:
        audit=subprocess.run(['python3',str(ROOT/'audit.py')],stdout=f,stderr=subprocess.STDOUT)
    (ROOT/'out/audit-status').write_text(str(audit.returncode)+'\n')
    (ROOT/'DONE').touch()
    subprocess.run(['python3',str(ROOT/'detach.py'),str(ROOT/'out/score-wave.log'),str(ROOT/'score-wave.sh')],check=True)
    print('DONE; scoring detached asynchronously',flush=True)
if __name__=='__main__':main()
