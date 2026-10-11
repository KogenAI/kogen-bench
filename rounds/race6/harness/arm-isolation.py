#!/usr/bin/env python3
"""macOS read/write denies for every other arm, including future siblings."""
import json,sys
from pathlib import Path
from condition import ARMS
def profile(root,arm):
    root=Path(root).resolve()
    paths={str(root/a) for a in ARMS if a!=arm}
    paths.add(str(root/'snapshots'))
    logs={str(root/'out')}
    # Covers same-host sibling language wave directories if provisioned externally.
    for wave in root.parent.glob('race6-*'):
        if wave!=root:
            paths.update(str(wave/a) for a in ARMS)
            paths.add(str(wave/'snapshots'));logs.add(str(wave/'out'))
    return '(version 1)\n(allow default)\n'+''.join('(deny file-read* file-write* (subpath '+json.dumps(p)+'))\n' for p in sorted(paths))+''.join('(deny file-read* (subpath '+json.dumps(p)+'))\n' for p in sorted(logs))
if __name__=='__main__':print(profile(sys.argv[1],sys.argv[2]),end='')
