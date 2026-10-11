#!/usr/bin/env python3
"""Alert only: never stop an arm for a writable-root symlink."""
import os,sys,time
from pathlib import Path
def escapes(root,roots):
    root=Path(root).resolve();found=[]
    for top in roots:
        top=Path(top)
        for p in [top,*top.rglob('*')]:
            if p.is_symlink():
                target=p.resolve(strict=False)
                if target!=root and root not in target.parents:found.append((str(p),str(target)))
    return sorted(set(found))
if __name__=='__main__':
    r=Path(sys.argv[1]);a=sys.argv[2];w=r/a
    found=escapes(w,[w,w/'.kitcache',os.environ.get('TMPDIR',str(w/'.kitcache/tmp'))])
    if found:
        with (r/'out/symlink-alerts.log').open('a') as f:
            for p,target in found:f.write(f'{int(time.time())}\t{a}\t{p}\t{target}\n')
