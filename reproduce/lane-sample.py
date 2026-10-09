#!/usr/bin/env python3
"""Capture a sanitized local boundary sample for a lane cell."""
import json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
out,edge,cap,planfile=sys.argv[1:]
try: load=float(Path('/proc/loadavg').read_text().split()[0])
except Exception: load=None
try:
 mem=next(int(line.split()[1]) for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith('MemAvailable:'))
except Exception: mem=None
try:
 pressure=int(next(value.split('=',1)[1] for line in Path('/proc/pressure/memory').read_text().splitlines() if line.startswith('some ') for value in line.split() if value.startswith('total=')))
except Exception: pressure=None
try:
 units=subprocess.check_output(['systemctl','list-units','--type=service','--state=running','--no-legend','bench-*.service'],text=True,stderr=subprocess.DEVNULL).splitlines()
 count=sum(bool(x.strip()) for x in units)
except Exception: count=None
try: plan=json.loads(Path(planfile).read_text()) if planfile else {}
except Exception: plan={}
try: data=json.loads(Path(out).read_text())
except Exception: data={}
data[edge]={'timestamp_utc':datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'),'load1':load,'memory_available_kib':mem,'pressure':pressure,'running_bench_units':count,'cap':int(cap) if cap.isdigit() else None,'queue_position':plan.get('queue_position'),'dispatcher_id':plan.get('launcher_sha256',plan.get('dispatcher_id'))}
Path(out).write_text(json.dumps(data,sort_keys=True)+'\n')
