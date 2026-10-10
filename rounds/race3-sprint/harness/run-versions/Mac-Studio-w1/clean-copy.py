#!/usr/bin/python3
# Clean source copy: keep offline dependencies, omit generated build output.
import shutil
import sys
from pathlib import Path


def copy(source, dest):
    excluded = {'target', '_build', 'build', 'dist', 'bin', '.kitcache', '.cache', '.git'}
    dest.mkdir(parents=True, exist_ok=False)
    for entry in source.iterdir():
        if entry.name in excluded:
            continue
        if entry.is_dir() and not entry.is_symlink():
            shutil.copytree(entry, dest / entry.name, symlinks=True)
        else:
            shutil.copy2(entry, dest / entry.name, follow_symlinks=False)
    # Gleam's downloaded dependencies live beside generated build output.
    if (source / 'build/packages').is_dir():
        shutil.copytree(source / 'build/packages', dest / 'build/packages', symlinks=True)
    for entry in dest.rglob('*'):
        if entry.is_file() and not entry.is_symlink():
            try:
                text = entry.read_text()
                if '\0' not in text and str(source) in text:
                    entry.write_text(text.replace(str(source), str(dest)))
            except (UnicodeError, OSError):
                pass


if __name__ == '__main__':
    copy(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
