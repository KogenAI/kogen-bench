#!/usr/bin/python3
# Shared hash and receipt helpers; never read authentication contents.
import hashlib
import json
import os
import subprocess
import shutil
from pathlib import Path


def tree_hash(path, frozen=False):
    # Exactly the registered INPUTS-SHA pipeline; snapshots ignore Python bytecode.
    skip = '' if frozen else ' -not -path "*/__pycache__/*"'
    sha='shasum -a 256' if shutil.which('shasum') else 'sha256sum'
    command = ('set -o pipefail; find . -type f' + skip +
               ' -print0 | sort -z | xargs -0 '+sha+' | '+sha+' | cut -c1-16')
    return subprocess.check_output(['/bin/bash', '-c', command], cwd=str(path), text=True).strip()


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def codex_home(root):
    pin = root / 'CODEX_HOME'
    return Path(os.path.expanduser(pin.read_text().strip() if pin.exists() else
                                 os.environ.get('CODEX_HOME', '$HOME/.codex')))


def events(path):
    with open(path, errors='replace') as f:
        for line in f:
            try:
                row = json.loads(line)
                if isinstance(row, dict):
                    yield row
            except ValueError:
                continue
