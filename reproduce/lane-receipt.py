#!/usr/bin/env python3
"""Append UTC and monotonic phase boundaries to lane-timing.json."""
import json,sys,time
from datetime import datetime,timezone
from pathlib import Path
path,phase,edge=sys.argv[1:]
p=Path(path); d=json.loads(p.read_text()) if p.exists() else {'phases':{},'attempts':[]}
now={'utc':datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'),'monotonic_ns':time.monotonic_ns()}
d.setdefault('phases',{}).setdefault(phase,{})[edge]=now
p.write_text(json.dumps(d,sort_keys=True)+'\n')
