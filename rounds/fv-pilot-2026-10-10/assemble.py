#!/usr/bin/env python3
"""Assemble public inputs for a standalone feedback check on a fresh Linux host."""
import argparse
import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('task', choices=['F01', 'W01', 'W04', 'X01'])
    parser.add_argument('arm', choices=['lean', 'quint'])
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error('output must be a new directory')
    fixture = ROOT / 'fixtures' / args.task
    package = ROOT / 'packages' / f'{args.task}-{args.arm}'
    output.mkdir(parents=True)
    shutil.copytree(fixture / 'app', output / 'app')
    shutil.copytree(fixture / 'starter', output / 'app/test')
    for name in ['contract.md', 'laws.json', 'brief.md']:
        shutil.copy2(fixture / name, output / name)
    for name in ['verification', 'docs']:
        shutil.copytree(package / name, output / name)
    for folder in ['frontend', 'shared', args.arm]:
        shutil.copytree(ROOT / 'bridge' / folder, output / 'bridge' / folder)
    for name in ['package.json', 'public-api.json', 'fixed.sha256']:
        shutil.copy2(package / name, output / name)
    (output / 'fv').write_text(
        '#!/bin/sh\nexec python3 "$(dirname "$0")/bridge/' + args.arm + '/fv.py" "$@"\n'
    )
    (output / 'fv').chmod(0o755)
    files = sorted(p for p in output.rglob('*') if p.is_file())
    (output / 'PACKAGE.sha256').write_text(''.join(
        hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + str(p.relative_to(output)) + '\n'
        for p in files
    ))
    print('Assembled public app, starter tests, fixed laws and feedback source.')
    print('On a Linux host with the pinned tools, enter the output directory and run ./fv check.')
    print('This standalone check does not reproduce metered trial execution or final evaluation.')


if __name__ == '__main__':
    main()
