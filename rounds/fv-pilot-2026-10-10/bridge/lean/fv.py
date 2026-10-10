#!/usr/bin/env python3
"""Lean package CLI; shared pipeline defined in bridge/fv-cli.md."""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def main():
    root = Path.cwd().resolve()
    if sys.argv[1:] != ["check"]:
        print("usage: ./fv check"); return 2
    passed, total, tests, digest, status = 0, 0, False, "none", 2
    env = dict(os.environ)
    env.update({"ELAN_HOME": "/opt/fv-tools/elan", "LANG": "C.UTF-8", "ERL_FLAGS": "+S 1:1 +A 1"})
    env["PATH"] = "/opt/fv-tools/elan/bin:/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:/opt/bench/mise/installs/erlang/29.0.3/bin:/usr/bin:/bin"
    try:
        laws = json.loads((root / "laws.json").read_text()); total = len(laws["laws"])
        verified = set()
        for line in (root / "fixed.sha256").read_text().splitlines():
            expected, relative = line.split(maxsplit=1); relative = relative.lstrip("*")
            target = (root / relative).resolve()
            if not target.is_relative_to(root): raise RuntimeError("invalid fixed path")
            if hashlib.sha256(target.read_bytes()).hexdigest() != expected: raise RuntimeError("changed fixed law: " + relative)
            verified.add(relative)
        if not {"laws.json", "verification/Laws.lean", "verification/laws.sha256"}.issubset(verified): raise RuntimeError("incomplete fixed hashes")
        out = root / "verification"; ir = out / "ir.json"
        r = subprocess.run(["elixir", str(root / "bridge/frontend/main.exs"), str(root / "app"), str(ir)], env=env)
        if r.returncode: raise RuntimeError("frontend rejected current source")
        r = subprocess.run(["python3", str(root / "bridge/lean/emit.py"), str(ir), str(root / "laws.json"), str(out)], env=env)
        if r.returncode: raise RuntimeError("emitter rejected current source")
        digest = hashlib.sha256(ir.read_bytes() + (out / "Implementation.lean").read_bytes()).hexdigest()
        r = subprocess.run(["python3", str(root / "bridge/lean/check.py"), str(out), str(root / "laws.json")], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print(r.stdout, end=""); status = r.returncode
        match = re.search(r"FV-LAWS (\d+)/(\d+)", r.stdout)
        if match and status != 2: passed = int(match[1])
        r = subprocess.run(["mix", "test"], cwd=root / "app", env=env)
        tests = r.returncode == 0
        if status == 0 and not tests: status = 1
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        print("FV-ERROR " + str(exc)); status = 2
    print(f"FV-SUMMARY arm=lean laws_ok={passed}/{total} tests_ok={str(tests).lower()} regenerated={digest}")
    return status


if __name__ == "__main__": sys.exit(main())
