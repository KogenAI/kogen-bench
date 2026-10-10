#!/usr/bin/env python3
"""Shared arm regeneration from current Elixir, without authoring fixed laws."""
import json, pathlib, subprocess, sys
root=pathlib.Path.cwd(); arm=json.loads((root/'package.json').read_text())['arm']
for cmd in [['elixir','bridge/frontend/main.exs','app','verification/ir.json'],['python3',f'bridge/{arm}/emit.py','verification/ir.json','laws.json','verification']]:
    p=subprocess.run(cmd)
    if p.returncode: raise SystemExit(p.returncode)
