#!/usr/bin/env python3
"""SELF-TEST ONLY: simulate ps rows from the trivial fake's process registry."""
import json
import os
from pathlib import Path

registry = Path(os.environ["ARCH_SELFTEST_REGISTRY"])
if registry.exists():
    for path in registry.glob("*.json"):
        try:
            row = json.loads(path.read_text())
            os.kill(row["pid"], 0)
        except (ValueError, KeyError, FileNotFoundError, ProcessLookupError):
            continue
        print(f"{row['pid']} {row['ppid']} S {row['command']}")
