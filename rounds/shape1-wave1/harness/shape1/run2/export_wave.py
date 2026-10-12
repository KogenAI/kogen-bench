#!/usr/bin/env python3
import pathlib,tarfile,sys,subprocess,io
root=pathlib.Path('<ROOT>');safe=pathlib.Path.home()/'Areas/Kogen/bench-manager/rz1-pack/rz1-export/levers/lib/safe_rows.py'
with tarfile.open(fileobj=sys.stdout.buffer,mode='w|') as out:
 for parent in ('run2','results','attempts'):
  for p in sorted((root/parent).rglob('*')):
   if not p.is_file() or p.is_symlink() or '__pycache__' in p.parts:continue
   if p.name in ('lane.stdout','lane.stderr','controller.log'):continue
   if parent=='results' and not p.relative_to(root/parent).parts[0].startswith('s1-'):continue
   name=str(p.relative_to(root))
   if p.suffix.lower() in ('.json','.jsonl') and any(x in p.name.lower() for x in ('grade','manifest','window')):
    data=subprocess.check_output(['/usr/bin/python3',str(safe),str(p)])
    info=tarfile.TarInfo(name);info.size=len(data);info.mode=0o600;out.addfile(info,io.BytesIO(data))
   else:out.add(p,arcname=name,recursive=False)
 data=subprocess.check_output(['/usr/bin/python3',str(safe),str(root/'LINUX-GATES.json')]);info=tarfile.TarInfo('LINUX-GATES.json');info.size=len(data);info.mode=0o600;out.addfile(info,io.BytesIO(data))
