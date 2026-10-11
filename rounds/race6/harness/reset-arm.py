#!/usr/bin/env python3
"""Reset only a validated condition's generated copy; never follow symlinks."""
import os,shutil,sys
from pathlib import Path
from condition import language
ROOT=Path(__file__).resolve().parent
arm=sys.argv[1];language(arm)
for path in (ROOT/arm,ROOT/'out'/arm):
    if path.is_symlink():path.unlink();continue
    if not path.exists():continue
    for base,dirs,files in os.walk(path,followlinks=False):
        Path(base).chmod(Path(base).stat().st_mode|0o700)
        for name in files:
            p=Path(base)/name
            if not p.is_symlink():p.chmod(p.stat().st_mode|0o600)
    shutil.rmtree(path)
