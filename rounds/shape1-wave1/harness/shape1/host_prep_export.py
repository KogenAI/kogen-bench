#!/usr/bin/env python3
"""Export opaque prep evidence; never include private suites or source trees."""
import sys
import tarfile
from pathlib import Path

ROOT=Path('<ROOT>')


def selected():
    files=set()
    for name in ('LINUX-GATES.json','REGISTRATION-FIX-4.json'):
        p=ROOT/name
        if p.is_file():files.add(p)
    for p in (ROOT/'prep').glob('*'):
        if p.is_file() and p.suffix in ('.json','.log','.stderr'):
            files.add(p)
    files.update((ROOT/'prep/isolation').glob('*.log'))
    files.update((ROOT/'prep').glob('attempt-*/*.json'))
    files.update((ROOT/'prep').glob('attempt-*/*.log'))
    files.update((ROOT/'prep').glob('attempt-*/isolation/*.log'))
    for sub in ('logs/launcher.log','core4b/SLOTS.log'):
        p=ROOT/sub
        if p.is_file():files.add(p)
    for p in (ROOT/'mutants').glob('*/validation-linux-hostprep-*.json'):
        files.add(p)
    # Explicit log-only patterns do not traverse or copy the hidden task tree.
    for work in (ROOT/'private').glob('mutant-*'):
        for name in ('progress.json','validation.json'):
            p=work/name
            if p.is_file():files.add(p)
        files.update(work.glob('*/reference/*.log'))
        files.update(work.glob('*/m*/*.log'))
    return sorted(files)


if __name__=='__main__':
    with tarfile.open(fileobj=sys.stdout.buffer,mode='w|') as archive:
        for path in selected():
            archive.add(path,arcname=str(path.relative_to(ROOT)),recursive=False)
