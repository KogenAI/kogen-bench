#!/usr/bin/env python3
"""Format an isolated host copy with the pinned official sandbox toolchain."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path('<ROOT>')
spec = importlib.util.spec_from_file_location('validation', ROOT / '<SERVER_ID>.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
lang = sys.argv[1]
revision = sys.argv[2] if len(sys.argv) > 2 else 'fix1'
work = ROOT / f'format-{lang}-{revision}'
if work.exists():
    raise RuntimeError('format attempt already exists; use a new revision')
shutil.copytree(ROOT / 'reference' / lang, work,
                ignore=shutil.ignore_patterns('.git', 'target', 'bin', '.cache', 'node_modules'))
if lang == 'ts-bun':
    shutil.copytree('/benchmark-root/toolchains/bun-1.4.2/node-template/node_modules', work / 'node_modules', symlinks=True)
commands = {'go': ['gofmt', '-w', '.'], 'rust': ['cargo', 'fmt'],
            'ts-bun': ['bun', './node_modules/@biomejs/biome/bin/biome', 'check', '--write', '.']}
proc = subprocess.run([module.PROFILE, 'grade', str(work), str(ROOT / f'taskdir-{lang}'), '--',
                       *commands[lang]], env=module.ENV, capture_output=True, text=True, timeout=60)
(ROOT / 'validation-logs' / f'format-{lang}-{revision}.log').write_text(proc.stdout + proc.stderr)
print(json.dumps({'lang': lang, 'format_rc': proc.returncode}))
