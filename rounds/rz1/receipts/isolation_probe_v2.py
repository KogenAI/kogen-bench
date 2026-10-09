#!/usr/bin/env python3
"""v2 (8 Oct, AMENDMENT-1 follow-up): fixes the inner-script syntax bug of v1 (defread), runs in the REAL cell mode (auto -> bench), binds the vendor dir as cells do.
No-model RZ1 isolation probe using the deployed Linux sandbox wrapper.

Only synthetic files are opened. The real EU auth.json and all real task,
grader, result, and sealed files are left untouched.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path("public-source-location-withheld")
LANE = ROOT / "levers" / "rz1"
RUNNER = ROOT / "probe-kgn" / "runner"
TOOLS = LANE / "tools"
CONF = LANE / "bench-codex.conf"
CODEX_BINARY = Path("public-source-location-withheld")
TASKS = ("rust", "zig")

sys.path.insert(0, str(RUNNER))
import egress  # noqa: E402
import sandbox_linux as SL  # noqa: E402


def can_read(path: str) -> bool:
    try:
        with open(path, "rb") as stream:
            stream.read(1)
        return True
    except OSError:
        return False


def main() -> int:
    gate = LANE / "gate"
    gate.mkdir(parents=True, exist_ok=True)
    work_root = Path(tempfile.mkdtemp(prefix="rz1-isolation-v2-", dir="public-source-location-withheld")); shutil.chown(work_root, group="bench"); work_root.chmod(0o2775)
    rows = []
    try:
        for stack in TASKS:
            shape = work_root / stack
            task_id = f"r70-1-{stack}"
            attempt = shape / "results" / "current-cell" / "attempt-1"
            work = attempt / "work"
            homes = shape / "homes"
            codex_home = homes / "codex"
            other_home = homes / "other"
            task_root = shape / "tasks" / task_id
            other_results = shape / "results" / "other-cell" / "attempt-1"
            for directory in (work, codex_home, other_home, task_root / "sealed" / "tests", other_results):
                directory.mkdir(parents=True, exist_ok=True)
            (codex_home / "auth.json").write_text("DUMMY-HARNESS-CREDENTIAL\n", encoding="utf-8")
            (other_home / "auth.json").write_text("DUMMY-OTHER-CREDENTIAL\n", encoding="utf-8")
            (task_root / "sealed" / "tests" / "fake-suite.py").write_text("DUMMY-SEALED-FIXTURE\n", encoding="utf-8")
            (task_root / "sealed" / "reference.patch").write_text("DUMMY-REFERENCE-FIXTURE\n", encoding="utf-8")
            (other_results / "transcript.txt").write_text("DUMMY-OTHER-CELL-RESULT\n", encoding="utf-8")
            if stack == "rust":
                (work / "build.rs").write_text("fn main() {}\n", encoding="utf-8")
                tool_path = "public-source-location-withheld"
            else:
                (work / "build.zig").write_text("pub fn build(_: anytype) void {}\n", encoding="utf-8")
                (work / "build.zig.zon").write_text(".{}\n", encoding="utf-8")
                tool_path = "public-source-location-withheld"
            (shape / "dummy-cell.json").write_text(json.dumps({"task": task_id, "stack": stack, "model": "none"}) + "\n")

            proxy = egress.Proxy(attempt / "egress.jsonl", f"rz1-isolation-{stack}", [])
            proxy.__enter__()
            env = dict(os.environ)
            env.update({
                "HOME": str(shape / "home"),
                "CODEX_HOME": str(codex_home),
                "BENCH_ROOT": "public-source-location-withheld",
                "BENCH_TASKS": str(shape / "tasks"),
                "BENCH_HOMES": str(homes),
                "BENCH_TOOLS_BIN": str(TOOLS / "bin"),
                "BENCH_CODEX_CONF": str(CONF),
                "BENCH_CODEX_PIN": "0.161.0",
                "BENCH_LINUX_RO": f"{CONF}:{CODEX_BINARY.parent.parent}",
                "PATH": f"{tool_path}:/opt/bench/mise/installs/node/24.20.0/bin:/usr/bin:/bin",
                "TMPDIR": "/tmp",
            })
            env.update(proxy.env())
            code = (
                "import json,os; from pathlib import Path; "
                "canread=lambda p: os.access(p, os.R_OK) and os.path.isfile(p); "
                "paths={'fake_hidden_suite':os.environ['RZ1_FAKE_HIDDEN'],"
                "'fake_reference':os.environ['RZ1_FAKE_REFERENCE'],"
                "'other_result':os.environ['RZ1_FAKE_OTHER_RESULT'],"
                "'other_harness_auth':os.environ['RZ1_FAKE_OTHER_AUTH'],"
                "'own_codex_auth':os.environ['RZ1_FAKE_OWN_AUTH']}; "
                "out={k:bool(canread(v)) for k,v in paths.items()}; "
                "print(json.dumps(out,sort_keys=True))"
            )
            env.update({
                "RZ1_FAKE_HIDDEN": str(task_root / "sealed" / "tests" / "fake-suite.py"),
                "RZ1_FAKE_REFERENCE": str(task_root / "sealed" / "reference.patch"),
                "RZ1_FAKE_OTHER_RESULT": str(other_results / "transcript.txt"),
                "RZ1_FAKE_OTHER_AUTH": str(other_home / "auth.json"),
                "RZ1_FAKE_OWN_AUTH": str(codex_home / "auth.json"),
            })
            os.environ.update({k: v for k, v in env.items() if k.startswith("BENCH_")}); os.environ.pop("BENCH_LINUX_MODE", None)
            for d in (shape, attempt, work, homes, codex_home, other_home):
                shutil.chown(d, group="bench"); d.chmod(0o2775)
            (attempt / "contamination.json").write_text("{}\n")
            argv, record = SL.wrap(["/usr/bin/python3", "-c", code], "codex", attempt, homes, TOOLS,
                                  egress_port=proxy.port, env=env, max_runtime=30)
            try:
                proc = subprocess.run(argv, cwd=work, env=env, stdin=subprocess.DEVNULL,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=45)
                result = json.loads(proc.stdout.strip().splitlines()[-1]) if proc.returncode == 0 else {}
                teardown = SL.teardown(record)
            finally:
                proxy.__exit__(None, None, None)

            expected_hidden = ["fake_hidden_suite", "fake_reference", "other_result", "other_harness_auth"]
            rows.append({
                "shape": stack,
                "task_id": task_id,
                "sandbox_returncode": proc.returncode,
                "isolated_targets_readable": {name: result.get(name) for name in expected_hidden},
                "own_codex_home_dummy_auth_readable_by_command": result.get("own_codex_auth"),
                "own_codex_home_mount": "read-write whole directory in current sandbox_linux.agent_args",
                "sandbox_record_sha256": hashlib.sha256(Path(record).read_bytes()).hexdigest(),
                "teardown_remaining": teardown.get("remaining"),
                "dummy_cell_config_path": str(shape / "dummy-cell.json"),
            })
        denied = all(not any((row["isolated_targets_readable"] or {}).values()) for row in rows)
        auth_isolated = all(row["own_codex_home_dummy_auth_readable_by_command"] is False for row in rows)
        receipt = {
            "schema": "rz1-isolation-receipt/1",
            "captured_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "runner_sandbox_sha256": hashlib.sha256((RUNNER / "sandbox_linux.py").read_bytes()).hexdigest(),
            "method": "deployed sandbox_linux.wrap + bubblewrap; empty egress allowlist; dummy rust and zig cells",
            "real_auth_read": False,
            "real_sealed_or_result_file_read": False,
            "fake_sealed_reference_results_and_auth_tests_denied": denied,
            "own_auth_isolated_from_command": auth_isolated,
            "launch_gate_pass": denied and auth_isolated,
            "results": rows,
        }
        output = gate / "isolation-v2.json"
        output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"receipt": str(output), "launch_gate_pass": receipt["launch_gate_pass"],
                          "dummy_hidden_and_other_data_denied": denied,
                          "dummy_own_auth_denied": auth_isolated,
                          "shapes": [row["shape"] for row in rows]}, sort_keys=True))
        return 0 if receipt["launch_gate_pass"] else 1
    finally:
        shutil.rmtree(work_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
