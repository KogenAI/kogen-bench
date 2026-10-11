#!/usr/bin/env python3
"""Read-only Python kit hash; pin independently from the unchanged main kit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT = Path(__file__).resolve().parent
REQUIRED = ('templates/py', 'env-py.sh', 'probe-py.sh', 'LIBS-py.md', 'toolchains')


def kit_path(root=ROOT):
    return Path(os.environ.get('RACE5_PY_KIT_DIR', str(Path(root).parent / 'race5-py-kit'))).resolve()


def manifest(kit):
    kit = Path(kit).resolve()
    missing = [name for name in REQUIRED if not (kit / name).exists()]
    if missing:
        raise ValueError('Python kit pending: missing ' + ', '.join(missing))
    rows = []
    for base, dirs, files in os.walk(kit, followlinks=False):
        rel = Path(base).relative_to(kit)
        dirs[:] = sorted(d for d in dirs if not (rel == Path('.') and d == 'logs')
                         and not (rel == Path('cache') and d in ('tmp', 'ruff', 'mypy'))
                         and d != '__pycache__')
        for name in sorted(files + [d for d in dirs if (Path(base)/d).is_symlink()]):
            path = Path(base) / name
            if name.endswith('.pyc') or name == '.DS_Store':
                continue
            before = path.lstat()
            if path.is_symlink():
                record = dict(path=str(path.relative_to(kit)), link=os.readlink(path))
            else:
                digest = hashlib.sha256()
                with path.open('rb') as stream:
                    for block in iter(lambda: stream.read(1024 * 1024), b''):
                        digest.update(block)
                record = dict(path=str(path.relative_to(kit)), sha256=digest.hexdigest(),
                              executable=bool(before.st_mode & 0o111))
            after = path.lstat()
            if (before.st_size, before.st_mtime_ns, before.st_mode) != (after.st_size, after.st_mtime_ns, after.st_mode):
                raise ValueError('Python kit changed during hashing; retry after preparation completes')
            rows.append(record)
    payload = json.dumps(sorted(rows, key=lambda row: row['path']), sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(payload).hexdigest(), rows


def check(root=ROOT):
    root = Path(root)
    pin = root / 'PY-KIT-SHA256'
    if not pin.is_file():
        raise ValueError('PY-KIT-SHA256 missing: run py-kit.py --pin after the Python kit lands')
    got, rows = manifest(kit_path(root))
    if (root/'out').is_dir():
        (root/'out/python-kit-manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
        (root/'out/python-kit.sha256').write_text(got+'\n')
    expected = pin.read_text().strip()
    print(f'Python kit files={len(rows)} hash={got}')
    if got != expected:
        raise ValueError('Python kit differs from PY-KIT-SHA256')
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pin', action='store_true')
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    if args.pin:
        digest, rows = manifest(kit_path(args.root))
        (args.root / 'PY-KIT-SHA256').write_text(digest + '\n')
        (args.root / 'evidence').mkdir(exist_ok=True)
        (args.root / 'evidence/python-kit-manifest.json').write_text(json.dumps(rows, indent=2) + '\n')
        print(f'PASS pinned Python kit: files={len(rows)} hash={digest}')
    else:
        check(args.root)

if __name__ == '__main__':
    main()
