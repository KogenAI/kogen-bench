#!/usr/bin/env python3
"""Check generated implementation and fixed bounded laws without network."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'shared'))
from replay import report


def decode_record(text):
    fields = {}
    for name, value in re.findall(r"v_(\w+)\s*:=\s*(FV\.Atom\.a_\w+|true|false|-?\d+)", text):
        fields[name] = value.removeprefix("FV.Atom.a_") if value.startswith("FV.Atom") else ({"true": True, "false": False}.get(value, value))
        if isinstance(fields[name], str) and re.fullmatch(r"-?\d+", fields[name]): fields[name] = int(fields[name])
    return {k: v for k, v in fields.items() if not k.endswith("_present") and fields.get(k + "_present", True)}


def trace_sources(output, ir, laws):
    reports = []
    if laws["task"] == "F01":
        for m in re.finditer(r"FV-COUNTEREXAMPLE (\w+) actor=(\{.*?\}) resource=(\{.*?\}) actual=(true|false)", output, re.S):
            report(ir,laws,m[1],[decode_record(m[2]),decode_record(m[3])],m[4]=='true')
            reports.append(m[1])
    else:
        for m in re.finditer(r"FV-COUNTEREXAMPLE (\w+) before=(\{.*?\}) sequence=\[(.*?)\]", output, re.S):
            sequence = re.findall(r"FV\.Atom\.a_(\w+)", m[3])
            if not sequence: raise ValueError("missing event in Lean counterexample")
            report(ir,laws,m[1],[decode_record(m[2]),sequence[-1]])
            reports.append(m[1])
    return set(reports)


def print_backend_output(output):
    # The emitted #eval witness is private replay transport, not a native
    # Lean diagnostic. Keep all native text verbatim and expose only locations
    # derived from that witness through the common reporter.
    witness = (r"^FV-COUNTEREXAMPLE \w+ (?:"
               r"actor=\{.*?\} resource=\{.*?\} actual=(?:true|false) expected=(?:true|false)|"
               r"before=\{.*?\} sequence=\[.*?\]|"
               r"init=\{.*?\} expected=\{.*?\})\r?\n?")
    print(re.sub(witness, "", output, flags=re.M | re.S), end="")


def main():
    p = argparse.ArgumentParser(); p.add_argument("out", type=Path); p.add_argument("laws", type=Path)
    args = p.parse_args(); out = args.out.resolve(); laws = json.loads(args.laws.read_text())
    digest = hashlib.sha256((out / "Laws.lean").read_bytes()).hexdigest()
    if digest != (out / "laws.sha256").read_text().strip():
        print("FV-INFRA fixed Laws.lean hash changed"); return 2
    env = dict(os.environ); env["LEAN_PATH"] = str(out)
    tool = "/opt/fv-tools/elan/bin/lean"
    try:
        compile_result = subprocess.run([tool, "+fv-4.34.1", "-o", "Implementation.olean", "Implementation.lean"], cwd=out, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        print(compile_result.stdout, end="")
        if compile_result.returncode:
            print("FV-INFRA generated implementation did not typecheck"); return 2
        result = subprocess.run([tool, "+fv-4.34.1", "Laws.lean"], cwd=out, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=420)
        print_backend_output(result.stdout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("FV-INFRA checker failed: " + str(exc)); return 2
    statuses = dict(re.findall(r"FV-LAW (\w+) (PASS|FAIL)", result.stdout))
    try:
        traced = trace_sources(result.stdout, json.loads((out / "ir.json").read_text()), laws)
        failed = {law for law, status in statuses.items() if status == "FAIL"}
        if not failed.issubset(traced) and "init=" not in result.stdout:
            print("FV-INFRA incomplete source replay"); return 2
    except (ValueError, KeyError, IndexError) as exc:
        print("FV-INFRA counterexample replay failed: " + str(exc)); return 2
    ok = sum(statuses.get(law["id"]) == "PASS" for law in laws["laws"])
    print(f"FV-LAWS {ok}/{len(laws['laws'])}")
    if len(statuses) != len(laws["laws"]):
        print("FV-INFRA incomplete law diagnostics"); return 2
    if result.returncode and all(x == "PASS" for x in statuses.values()):
        print("FV-INFRA laws evaluated true but proof checking failed"); return 2
    return 0 if result.returncode == 0 and ok == len(laws["laws"]) else 1


if __name__ == "__main__": sys.exit(main())
