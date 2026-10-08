#!/usr/bin/env python3
"""Grade only fresh reference and no-op worktrees; print aggregate verdicts."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run(argv, **kwargs):
    return subprocess.run(argv, check=True, **kwargs)


def sandbox(task_dir: Path, work: Path, log_path=None):
    profile = Path(__file__).with_name("sandbox-profile.sh")
    env = {**os.environ, "HOME": "/tmp/home", "PYTHONDONTWRITEBYTECODE": "1",
           "PATH": "/srv/bh/bench/toolchains/go-1.27.1/bin:"
                   "/srv/bh/bench/toolchains/rust-1.97.1/bin:"
                   "/srv/bh/bench/toolchains/bun-1.4.2/bin:"
                   "/srv/bh/bench/toolchains/gleam-1.18.1/bin:"
                   "/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:"
                   "/opt/bench/mise/installs/erlang/29.0.3/bin:"
                   "/opt/bench/mise/installs/node/24.20.0/bin:"
                   "/opt/bench/mise/installs/ruby/3.4.8/bin:"
                   "/srv/bh/bench/toolchains/python-3.14.7/bin:/usr/bin:/bin",
           "PYTHONPATH": "/srv/bh/bench/toolchains/python-3.14.7/lib/python3.14/site-packages",
           "RUSTUP_HOME": "/opt/bench/rustup", "CARGO_NET_OFFLINE": "true",
           "GOTOOLCHAIN": "local", "GOPROXY": "off"}
    proc = subprocess.run([str(profile), "grade", str(work), str(task_dir), "--",
                           "/bin/bash", "/task/hidden/grade.sh", "/work"],
                          env=env, capture_output=True, text=True, timeout=1200)
    if log_path is not None:
        log_path.write_text(proc.stdout + "\n--- stderr ---\n" + proc.stderr)
    verdict = None
    for line in reversed(proc.stdout.splitlines()):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict) and ("pass_" in record or "pass" in record):
            verdict = bool(record.get("pass_", record.get("pass")))
            break
    if verdict is None or proc.returncode not in (0, 1):
        raise RuntimeError(f"grader infrastructure failure (rc={proc.returncode})")
    return verdict


def control(kit: Path, task_id: str):
    task = kit / "tasks" / task_id
    if not task.is_dir() or not (task / "task.json").is_file():
        raise RuntimeError("task kit unavailable")
    meta = json.loads((task / "task.json").read_text())
    bundle_name = meta.get("base_bundle")
    if not bundle_name or meta.get("base_missing"):
        raise RuntimeError("task base is not bundled")
    bundle = kit / "tasks" / bundle_name
    digest = hashlib.sha256(bundle.read_bytes()).hexdigest()
    if digest != meta["base_bundle_sha256"]:
        raise RuntimeError("task base digest mismatch")
    grader = task / "hidden" / "grade.sh"
    if not grader.is_file():
        raise RuntimeError("official hidden grader unavailable")
    reference = task / "hidden" / "sealed" / "reference"
    patch = task / "hidden" / "sealed" / "reference.patch"
    if not reference.is_dir() and not patch.is_file():
        raise RuntimeError("reference is not published")
    with tempfile.TemporaryDirectory(prefix="kogen-controls-", dir="/srv/bh/bench/work") as tmp:
        tmp = Path(tmp)
        outcomes = {}
        for variant in ("noop", "reference"):
            run(["/usr/local/bin/bench-disk-floor", "/srv/bh/bench"])
            work = tmp / variant
            run(["git", "clone", "-q", str(bundle), str(work)])
            run(["git", "-C", str(work), "checkout", "-q", meta["base_sha"]])
            if variant == "reference":
                if patch.is_file():
                    run(["git", "-C", str(work), "apply", "--whitespace=nowarn", str(patch)])
                else:
                    source = reference
                    if not (source / "Makefile").exists():
                        for candidate in (source / meta.get("stack", ""), source / task_id):
                            if candidate.is_dir():
                                source = candidate
                                break
                    shutil.copytree(source, work, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git"))
            outcomes[variant] = sandbox(task, work)
        return outcomes


def main():
    kit = Path(sys.argv[1]).resolve()
    if sys.argv[2] == "grade-candidate":
        task_id = sys.argv[3]
        task = kit / "tasks" / task_id
        result = Path(sys.argv[5]).resolve()
        with tempfile.TemporaryDirectory(prefix="kogen-grade-", dir="/srv/bh/bench/work") as tmp:
            work = Path(tmp) / "candidate"
            shutil.copytree(sys.argv[4], work, ignore=shutil.ignore_patterns(".git"))
            passed = sandbox(task, work, result / "grader.log")
        counts = {}
        for line in (result / "grader.log").read_text().splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict) and ("pass_" in record or "pass" in record):
                counts = {k: record[k] for k in ("tests", "failures", "errors", "skipped", "tests_ran") if k in record}
        (result / "grade.json").write_text(json.dumps({"task": task_id, "pass_": passed, **counts}) + "\n")
        print(json.dumps({"task": task_id, "grade_pass": passed}))
        return 0 if passed else 1
    failed = False
    for task_id in sys.argv[2:]:
        try:
            result = control(kit, task_id)
            admitted = result["reference"] and not result["noop"]
            print(json.dumps({"task": task_id, "reference_pass": result["reference"],
                              "noop_fail": not result["noop"], "admitted": admitted}), flush=True)
            failed |= not admitted
        except (OSError, KeyError, ValueError, RuntimeError, subprocess.CalledProcessError,
                subprocess.TimeoutExpired) as exc:
            print(json.dumps({"task": task_id, "admitted": False,
                              "error": str(exc)[:180]}), flush=True)
            failed = True
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
