#!/usr/bin/env python3
"""Retain source checkpoints on Macs; retain three periodic checkpoints on Linux."""
import argparse
import json
import os
from pathlib import Path
import platform
import re
import shutil
import time

BUILD_DIRS = {'target', '_build', 'node_modules', '.venv', 'build', 'dist'}
DEP_BUILD_DIRS = BUILD_DIRS | {'ebin', 'obj'}


def remove(path):
    # Unlink symlinks rather than following them out of the snapshot.
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def prune(root, host=None, now=None):
    root = Path(root).resolve()
    host = host or platform.system()
    now = time.time() if now is None else now
    snapshots = root / 'snapshots'
    if not snapshots.is_dir():
        return []
    points = []
    for path in snapshots.iterdir():
        if path.is_symlink() or not path.is_dir() or not re.fullmatch(r'T\+\d+m', path.name):
            continue
        if not (path / 'SNAPSHOT_COMPLETE').is_file():
            continue
        try:
            epoch = int((path / 'TAKEN_EPOCH').read_text())
        except (OSError, ValueError):
            continue
        if path.name in ('T+030m',): continue  # Preserve executable hourly curves.
        points.append((epoch, path))
    points.sort(key=lambda item: (item[0], item[1].name))
    actions = []
    if host == 'Linux':
        for _, path in points[:-3]:
            remove(path)
            actions.append(dict(snapshot=path.name, action='remove-periodic'))
    else:
        arms = (root / 'ARMS').read_text().split()
        for epoch, path in points:
            if now - epoch <= 30 * 60:  # Exactly 30 minutes is retained too.
                continue
            for arm in arms:
                repo = path / arm
                if repo.is_symlink() or not repo.is_dir() or (repo / 'PRUNED_BUILD_OUTPUT').exists():
                    continue
                # Mark before deleting so a failure cannot leave an apparently
                # executable checkpoint. No scoring runs during the wave.
                (repo / 'PRUNED_BUILD_OUTPUT').write_text('Source-only; build output pruned after 30 minutes.\n')
                removed = []
                for name in sorted(BUILD_DIRS):
                    entry = repo / name
                    if entry.exists() or entry.is_symlink():
                        remove(entry); removed.append(name)
                deps = repo / 'deps'
                if deps.is_dir() and not deps.is_symlink():
                    for base, dirs, files in os.walk(deps, followlinks=False):
                        for name in list(dirs):
                            if name in DEP_BUILD_DIRS:
                                entry = Path(base) / name
                                remove(entry); dirs.remove(name)
                                removed.append(str(entry.relative_to(repo)))
                        for name in files:
                            if name.endswith(('.beam', '.o', '.a', '.so', '.dylib')):
                                entry = Path(base) / name
                                remove(entry); removed.append(str(entry.relative_to(repo)))
                actions.append(dict(snapshot=path.name, arm=arm, action='prune-build-output', removed=removed))
    if actions:
        (root / 'out').mkdir(exist_ok=True)
        with (root / 'out/snapshot-pruning.jsonl').open('a') as stream:
            for action in actions:
                stream.write(json.dumps(dict(epoch=int(now), host=host, **action), sort_keys=True) + '\n')
    return actions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--host', choices=('Darwin', 'Linux'))
    parser.add_argument('--loop', action='store_true')
    args = parser.parse_args()
    while True:
        prune(args.root, args.host)
        if not args.loop or any((args.root / name).exists() for name in ('STOP', 'DONE')):
            break
        time.sleep(15)

if __name__ == '__main__':
    main()
