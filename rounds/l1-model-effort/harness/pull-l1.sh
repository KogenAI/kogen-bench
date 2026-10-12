#!/bin/bash
set -euo pipefail
L1_RECORD_ROOT=$(cd "$(dirname "$0")/.." && pwd)
exec /usr/bin/python3 - "$L1_RECORD_ROOT" <<'PY'
import io, json, os, subprocess, sys, tarfile
from pathlib import Path
record=Path(sys.argv[1]); dest=record/'raw/scored'; dest.mkdir(parents=True,exist_ok=True)
wrapper=Path('[path omitted]')
remote=r'''
import io,json,sys,tarfile
from pathlib import Path
host='kogen-operator-'+sys.argv[1]
ledger=Path('/root/l1')/('ledger-'+host+'.jsonl')
paths=[ledger,Path('/root/l1')/('template-'+host+'.json'),Path('/root/l1')/('current-'+host+'.json')]
runs=set()
if ledger.exists():
 for line in ledger.read_text().splitlines():
  try: row=json.loads(line)
  except ValueError: continue
  if row.get('run_dir'): runs.add(row['run_dir'])
for name in sorted(runs):
 root=Path(name)
 if root.parent!=Path('[path omitted]') or not root.name.startswith(host+'-'): raise RuntimeError('invalid ledger path')
 for pattern in ('l1-summary.json','receipts.tsv','receipts-check.txt','tokens-final-*.txt','scores*.tsv','final-*.txt','t030-*.txt','offline-*.json','process-stop.json','supervisor-stop.json','snap-times.log','final-snap.txt','arms.log','target-stops.tsv','disk-admission.json','l1-score-*.stderr','results/*-score.json','results/FINAL-*.jsonl','results/T+030m-*.jsonl'):
  paths.extend((root/'out').glob(pattern))
with tarfile.open(fileobj=sys.stdout.buffer,mode='w|gz') as tar:
 for path in sorted(set(paths)):
  if not path.is_file() or path.is_symlink(): continue
  if path.parent==Path('/root/l1'): arcname=host+'/'+path.name
  else: arcname=host+'/'+str(path.relative_to('[path omitted]'))
  # Explicit allowlist above excludes prompts, session files and turn transcripts.
  tar.add(path,arcname=arcname,recursive=False)
'''
import base64
encoded=base64.b64encode(remote.encode()).decode()
for h in ('eu','us'):
 command="python3 -c \"import base64;exec(base64.b64decode('"+encoded+"'))\" "+h
 result=subprocess.run([str(wrapper),h,command],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if result.returncode: raise SystemExit(result.stderr.decode(errors='replace'))
 archive=dest/('kogen-operator-'+h+'.tgz'); archive.write_bytes(result.stdout)
 with tarfile.open(fileobj=io.BytesIO(result.stdout)) as tar:
  for member in tar.getmembers():
   p=Path(member.name)
   if p.is_absolute() or '..' in p.parts or not member.isfile(): raise RuntimeError('unsafe archive member')
   target=dest/p; target.parent.mkdir(parents=True,exist_ok=True)
   target.write_bytes(tar.extractfile(member).read())
 print('Pulled',h,'ledger, summaries and scores to',dest/('kogen-operator-'+h))
PY
