#!/usr/bin/env python3
import json,subprocess,time,sys
from pathlib import Path
r=Path(__file__).resolve().parent;i=int(sys.argv[1]);starts=json.loads((r/'LANGUAGE-EPOCHS.json').read_text())
queue=sorted((s+m*60,a,m) for a,s in starts.items() for m in range(i,60,i))
for epoch,a,m in queue:
    while time.time()<epoch:
        if (r/'STOP').exists():sys.exit(0)
        time.sleep(.5)
    if (r/('STOP-'+a)).exists():continue
    subprocess.run([str(r/'snap.sh'),f'T+{m:03d}m',a],check=True)
