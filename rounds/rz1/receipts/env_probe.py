#!/usr/bin/env python3
"""rz1 AMENDMENT-1 (c): no-model environment probe in the REAL cell sandbox mode.

Runs one command through probe-kgn/runner sandbox_linux.wrap exactly as a cell does (BENCH_LINUX_MODE unset -> auto,
which on the workers is sudo systemd-run --uid=bench), with the real EU homes (probe-kgn-eu/homes) and the lane's
BENCH_LINUX_RO from lane_dispatch.py. Inside, it reports booleans and return codes only:
  - the bound Codex vendor dir exposes bin/codex, bin/codex-code-mode-host, codex-path, codex-resources;
  - bin/codex --version runs; bin/codex-code-mode-host can be exec'd (rc not 126/127);
  - the EU Codex home and its auth.json are visible and readable by the sandbox user (os.access only; never opened);
  - a shell tool command (sh -c) runs in the workspace (the path Codex uses for tool calls).
Prints one JSON line; exits 0 only if every check passes.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path("public-source-location-withheld")
LANE = ROOT / "levers" / "rz1"
RUNNER = ROOT / "probe-kgn" / "runner"
sys.path.insert(0, str(RUNNER))
sys.path.insert(0, str(LANE))
import egress  # noqa: E402
import sandbox_linux as SL  # noqa: E402
import lane_dispatch as LD  # noqa: E402

INNER = r'''
import json, os, subprocess
v = os.environ["RZ1_VENDOR"]; home = os.environ["RZ1_CODEX_HOME"]
out = {k: os.path.exists(os.path.join(v, k)) for k in ("bin/codex", "bin/codex-code-mode-host", "codex-path", "codex-resources")}
r = subprocess.run([os.path.join(v, "bin/codex"), "--version"], capture_output=True, text=True)
out["codex_version_rc"] = r.returncode; out["codex_version_ok"] = r.stdout.strip().startswith("codex-cli 0.161.0")
try:
    h = subprocess.run([os.path.join(v, "bin/codex-code-mode-host"), "--help"], capture_output=True, text=True, timeout=10)
    out["code_mode_host_exec_rc"] = h.returncode
except subprocess.TimeoutExpired:
    out["code_mode_host_exec_rc"] = "timeout-but-started"
out["codex_home_visible"] = os.path.isdir(home)
out["auth_readable_by_sandbox_user"] = os.access(os.path.join(home, "auth.json"), os.R_OK)
out["uid"] = os.getuid()
t = subprocess.run(["sh", "-c", "echo tool-ok > probe.txt && cat probe.txt"], capture_output=True, text=True)
out["shell_tool_call_ok"] = t.returncode == 0 and t.stdout.strip() == "tool-ok"
print(json.dumps(out, sort_keys=True))
'''


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="rz1-envprobe-", dir="public-source-location-withheld"))
    shutil.chown(root, group="bench"); root.chmod(0o2775)
    attempt = root / "probe-cell" / "attempt-1"; work = attempt / "work"; work.mkdir(parents=True)
    for d in (root / "probe-cell", attempt, work):
        shutil.chown(d, group="bench"); d.chmod(0o2775)
    env = LD.env_for(root)  # the exact lane env builder used for cells
    env.pop("BENCH_LINUX_MODE", None)
    os.environ.update({k: v for k, v in env.items() if k.startswith("BENCH_")})  # sandbox_linux reads BENCH_LINUX_* from the process env, as in a real runner
    os.environ.pop("BENCH_LINUX_MODE", None)
    env.update(RZ1_VENDOR=LD.CODEX_VENDOR, RZ1_CODEX_HOME=str(Path(LD.EU_HOMES) / "codex"), TMPDIR=str(work))
    (attempt / "contamination.json").write_text("{}\n")
    proxy = egress.Proxy(attempt / "egress.jsonl", "rz1-envprobe", [])
    proxy.__enter__()
    try:
        env.update(proxy.env())
        argv, record = SL.wrap(["/usr/bin/python3", "-c", INNER], "codex", attempt, LD.EU_HOMES, LD.TOOLS_BIN.parent,
                               egress_port=proxy.port, env=env, max_runtime=60)
        proc = subprocess.run(argv, cwd=work, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=90)
        SL.teardown(record)
    finally:
        proxy.__exit__(None, None, None)
    try:
        res = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception:
        res = {"parse_error": True, "sandbox_rc": proc.returncode, "stderr_tail": proc.stderr[-300:]}
    res["sandbox_rc"] = proc.returncode
    res["mode"] = record.get("mode") if isinstance(record, dict) else None
    ok = (proc.returncode == 0 and all(res.get(k) is True for k in ("bin/codex", "bin/codex-code-mode-host", "codex-path",
          "codex-resources", "codex_version_ok", "codex_home_visible", "auth_readable_by_sandbox_user", "shell_tool_call_ok"))
          and res.get("code_mode_host_exec_rc") not in (126, 127))
    res["all_pass"] = ok
    print(json.dumps(res, sort_keys=True))
    shutil.rmtree(root, ignore_errors=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
