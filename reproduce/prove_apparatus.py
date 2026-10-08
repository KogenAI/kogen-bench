#!/usr/bin/env python3
"""Model-free reference/no-op controls for the published task kits.

Only verdicts and hashes are emitted. Grader output is captured and discarded
so hidden test names cannot enter the evidence record.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

TASK_IDS = [
    "elx-port-active-storage-tracking",
    "elx-port-board-publish-unpublish-public-boundary",
    "elx-port-cancelled-account-cleanup",
    "elx-port-erase-account",
    "elx-port-variant-processed-once",
]

def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def tree_sha(path: Path) -> str:
    h = hashlib.sha256()
    if path.is_file():
        return file_sha(path)
    for item in sorted(path.rglob("*"), key=lambda p: p.relative_to(path).as_posix()):
        rel = item.relative_to(path).as_posix().encode("utf-8", "surrogateescape")
        h.update(len(rel).to_bytes(8, "big")); h.update(rel)
        if item.is_symlink():
            h.update(b"L"); h.update(os.readlink(item).encode("utf-8", "surrogateescape"))
        elif item.is_file():
            h.update(b"F"); h.update(bytes.fromhex(file_sha(item)))
        elif item.is_dir():
            h.update(b"D")
    return h.hexdigest()

def find_repo(start: Path) -> Path:
    for p in (start, *start.parents):
        if (p / "tasks/index.json").is_file() and (p / "tasks/_bases/MANIFEST.sha256").is_file():
            return p
    raise RuntimeError("could not locate repository tasks directory")

def run(command: list[str], timeout: int) -> tuple[int, float]:
    started = time.monotonic()
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try: os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError: pass
        try: proc.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            try: os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError: pass
            proc.communicate()
        return 124, time.monotonic() - started
    return int(proc.returncode), time.monotonic() - started

def materialize(bundle: Path, sha: str, workspace: Path) -> None:
    code, _ = run(["git", "clone", "--quiet", "--no-checkout", str(bundle), str(workspace)], 120)
    if code: raise RuntimeError("base bundle clone failed")
    code, _ = run(["git", "-C", str(workspace), "checkout", "--quiet", "--detach", sha], 120)
    if code: raise RuntimeError("recorded base commit is absent from bundle")
    got = subprocess.run(["git", "-C", str(workspace), "rev-parse", "HEAD"], check=True,
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True).stdout.strip()
    if got != sha: raise RuntimeError("materialized base SHA mismatch")

def apply_reference(task_dir: Path, workspace: Path) -> str:
    patch = task_dir / "hidden/sealed/reference.patch"
    tree = task_dir / "hidden/sealed/reference"
    if patch.is_file():
        code, _ = run(["git", "-C", str(workspace), "apply", str(patch)], 120)
        if code: raise RuntimeError("reference patch did not apply cleanly")
        return "patch"
    if tree.is_dir():
        for item in tree.iterdir():
            dst = workspace / item.name
            if item.is_dir() and not item.is_symlink(): shutil.copytree(item, dst, dirs_exist_ok=True, symlinks=True)
            elif item.is_symlink():
                if dst.is_dir() and not dst.is_symlink(): shutil.rmtree(dst)
                elif dst.exists() or dst.is_symlink(): dst.unlink()
                dst.symlink_to(os.readlink(item), target_is_directory=item.is_dir())
            else: shutil.copy2(item, dst)
        return "tree"
    raise RuntimeError("kit has no staged reference solution")

def kit_shas(task_dir: Path, task: dict[str, Any], repo: Path) -> dict[str, str]:
    suite_index = json.loads((repo / "tasks/SUITES-INDEX.json").read_text(encoding="utf-8"))["tasks"][task["id"]]
    return {
        "prompt_sha256": file_sha(task_dir / "prompt.md"),
        "base_bundle_sha256": file_sha(repo / "tasks" / task["base_bundle"]),
        "published_sealed_tree_sha256": suite_index["tree_sha256"],
        "hidden_suite_tree_sha256": tree_sha(task_dir / "hidden/sealed"),
        "grader_tree_sha256": tree_sha(task_dir / "grader"),
        "grader_entry_sha256": file_sha(task_dir / "hidden/grade.sh"),
        "kit_manifest_sha256": file_sha(task_dir / "MANIFEST.sha256"),
        "task_json_sha256": file_sha(task_dir / "task.json"),
    }

def verify_manifest(task_dir: Path) -> int:
    """Verify every listed task-kit file without printing manifest paths."""
    count = 0
    for line in (task_dir / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            expected, rel = line.split("  ", 1)
        except ValueError as exc:
            raise RuntimeError("kit manifest syntax error") from exc
        target = (task_dir / rel).resolve()
        if not target.is_relative_to(task_dir.resolve()) or not target.is_file():
            raise RuntimeError("kit manifest path is missing or escapes task directory")
        if file_sha(target) != expected:
            raise RuntimeError("kit manifest file hash mismatch")
        count += 1
    if not count:
        raise RuntimeError("kit manifest is empty")
    return count

def grade(task_dir: Path, workspace: Path, timeout: int) -> dict[str, Any]:
    # The published grader wrapper is under hidden/: its relative sealed/ path
    # is part of the kit. The duplicate grader/ wrapper is a public stub whose
    # sealed/ payload is intentionally absent.
    grader = task_dir / "hidden/grade.sh"
    if not grader.is_file(): raise RuntimeError("official grader entry point is missing")
    code, elapsed = run(["bash", str(grader), str(workspace)], timeout)
    return {"verdict": "PASS" if code == 0 else "FAIL", "exit_code": code,
            "elapsed_seconds": round(elapsed, 3)}

def one_control(repo: Path, task_id: str, kind: str, rep: int, timeout: int) -> dict[str, Any]:
    task_dir = repo / "tasks" / task_id
    task = json.loads((task_dir / "task.json").read_text(encoding="utf-8"))
    bundle = repo / "tasks" / task["base_bundle"]
    if file_sha(task_dir / "prompt.md") != task["prompt_sha256_original"]:
        raise RuntimeError("prompt SHA does not match task metadata")
    if file_sha(bundle) != task["base_bundle_sha256"]: raise RuntimeError("base bundle SHA mismatch")
    if file_sha(task_dir / "MANIFEST.sha256") != json.loads(
        (repo / "tasks/SUITES-INDEX.json").read_text(encoding="utf-8")
    )["tasks"][task_id]["tree_sha256"]:
        raise RuntimeError("sealed tree index and task manifest disagree")
    verify_manifest(task_dir)
    with tempfile.TemporaryDirectory(prefix="kogen-apparatus-") as temp:
        workspace = Path(temp) / "workspace"
        materialize(bundle, task["base_sha"], workspace)
        form = apply_reference(task_dir, workspace) if kind == "reference" else "none"
        result = grade(task_dir, workspace, timeout)
    result.update({"kind": kind, "replicate": rep, "reference_form": form,
                   "materialized_base_sha": task["base_sha"]})
    return result

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, help="publication worktree containing tasks/ (default: search from this script)")
    ap.add_argument("--task", action="append", choices=TASK_IDS, help="select task(s); default is all 12")
    ap.add_argument("--repetitions", type=int, default=2, help="repetitions of each control (default 2)")
    ap.add_argument("--timeout", type=int, default=1800, help="seconds per official grade (default 1800)")
    ap.add_argument("--output", type=Path, default=Path("control-results.json"))
    args = ap.parse_args()
    if args.repetitions < 1 or args.timeout < 1: ap.error("repetitions and timeout must be positive")
    repo = find_repo(args.repo.expanduser().resolve() if args.repo else Path(__file__).resolve().parent)
    ids = args.task or TASK_IDS
    revision = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True).stdout.strip()
    record: dict[str, Any] = {
        "schema": "kogen-apparatus-controls-v1", "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "repository_revision": revision,
        "runner_sha256": file_sha(Path(__file__).resolve()),
        "host": {"system": platform.system(), "release": platform.release(), "machine": platform.machine(),
                 "python": platform.python_version(),
                 "git": subprocess.run(["git", "--version"], check=True, capture_output=True, text=True).stdout.strip(),
                 "bwrap": shutil.which("bwrap")},
        "grader_mode": "direct official grader invocation; agent sandbox is not exercised",
        "repetitions_per_control": args.repetitions, "tasks": [],
    }
    record["shared_r70_helpers_manifest_sha256"] = file_sha(repo / "tasks/_grader/MANIFEST.sha256")
    all_hold = True
    for task_id in ids:
        task_dir = repo / "tasks" / task_id
        task = json.loads((task_dir / "task.json").read_text(encoding="utf-8"))
        row: dict[str, Any] = {"id": task_id, "base_sha": task["base_sha"],
                               "manifest_entries_verified": verify_manifest(task_dir),
                               "kit_shas": kit_shas(task_dir, task, repo),
                               "controls": {"reference": [], "noop": []}}
        for kind, expected in (("reference", "PASS"), ("noop", "FAIL")):
            for rep in range(1, args.repetitions + 1):
                try: result = one_control(repo, task_id, kind, rep, args.timeout)
                except Exception as exc:
                    result = {"kind": kind, "replicate": rep, "verdict": "ERROR", "error_class": type(exc).__name__}
                result["expected"] = expected; result["holds"] = result.get("verdict") == expected
                row["controls"][kind].append(result); all_hold = all_hold and result["holds"]
        rows = row["controls"]["reference"] + row["controls"]["noop"]
        row["grader_controls_hold"] = all(x["holds"] for x in rows)
        row["grader_self_check"] = {
            "reference_repeats_consistent": len({x["verdict"] for x in row["controls"]["reference"]}) == 1,
            "noop_repeats_consistent": len({x["verdict"] for x in row["controls"]["noop"]}) == 1,
            "holds": row["grader_controls_hold"],
        }
        all_hold = all_hold and row["grader_self_check"]["holds"]
        record["tasks"].append(row)
    record["summary"] = {"task_count": len(record["tasks"]),
                         "all_reference_and_noop_controls_hold": all_hold,
                         "launch_control_gate": "PASS" if all_hold else "FAIL"}
    out = args.output.expanduser().resolve(); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(record["summary"], sort_keys=True)); print(f"evidence: {out}")
    return 0 if all_hold else 1

if __name__ == "__main__":
    raise SystemExit(main())
