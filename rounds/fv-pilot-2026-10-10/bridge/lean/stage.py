#!/usr/bin/env python3
"""Optional broker adapter: immutable regenerate/check/starter plans."""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def main():
    backend = Path(__file__).resolve().parent
    root = backend.parent
    if sys.argv[1:] not in (["regenerate"], ["check"], ["starter"]): return 2
    action = sys.argv[1]; statefile = backend / ".fv-stage.json"
    state = {"regenerated": "none", "laws_ok": 0, "laws_total": 0, "translated": False, "status": 2}
    if action != "regenerate" and statefile.exists(): state = json.loads(statefile.read_text())
    env = dict(os.environ)
    env.update({"ELAN_HOME": "/opt/fv-tools/elan", "LANG": "C.UTF-8", "ERL_FLAGS": "+S 1:1 +A 1"})
    env["PATH"] = "/opt/fv-tools/elan/bin:/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:/opt/bench/mise/installs/erlang/29.0.3/bin:/usr/bin:/bin"
    try:
        for line in (root / "fixed.sha256").read_text().splitlines():
            expected, relative = line.split(maxsplit=1); target = (root / relative.lstrip("*")).resolve()
            if not target.is_relative_to(root) or hashlib.sha256(target.read_bytes()).hexdigest() != expected: raise RuntimeError("changed fixed laws: " + relative)
        laws = json.loads((root / "laws.json").read_text()); state["laws_total"] = len(laws["laws"])
        out = root / "verification"
        if action == "regenerate":
            for cmd in [["elixir", str(root / "bridge/frontend/main.exs"), str(root / "app"), str(out / "ir.json")], ["python3", str(root / "bridge/lean/emit.py"), str(out / "ir.json"), str(root / "laws.json"), str(out)]]:
                if subprocess.run(cmd, env=env).returncode: raise RuntimeError("regeneration rejected current source")
            state.update(translated=True, status=0, regenerated=hashlib.sha256((out / "ir.json").read_bytes() + (out / "Implementation.lean").read_bytes()).hexdigest())
            statefile.write_text(json.dumps(state) + "\n"); return 0
        if action == "check":
            if not state["translated"]: raise RuntimeError("regeneration incomplete")
            result = subprocess.run(["python3", str(root / "bridge/lean/check.py"), str(out), str(root / "laws.json")], env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print(result.stdout, end="")
            match = re.search(r"FV-LAWS (\d+)/(\d+)", result.stdout)
            state.update(status=result.returncode, laws_ok=int(match[1]) if match and result.returncode != 2 else 0)
            statefile.write_text(json.dumps(state) + "\n"); return result.returncode
        tests = state["translated"] and subprocess.run(["mix", "test"], cwd=root / "app", env=env).returncode == 0
        status = state["status"] or (0 if tests else 1)
        print(f'FV-SUMMARY arm=lean laws_ok={state["laws_ok"]}/{state["laws_total"]} tests_ok={str(tests).lower()} regenerated={state["regenerated"]}')
        return status
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        print("FV-ERROR " + str(exc)); state["status"] = 2; statefile.write_text(json.dumps(state) + "\n")
        if action == "starter": print(f'FV-SUMMARY arm=lean laws_ok=0/{state["laws_total"]} tests_ok=false regenerated={state["regenerated"]}')
        return 2


if __name__ == "__main__": sys.exit(main())
