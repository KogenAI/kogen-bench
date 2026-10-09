#!/usr/bin/env python3
"""RZ1 EU lane plumbing, reusing the frozen R70 runner helpers."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import sys

LANE_LOCAL = Path(__file__).resolve().parent
LEVER_LOCAL = LANE_LOCAL.parent
ROOT = Path(os.environ.get("RZ1_HOST_ROOT", "public-source-location-withheld"))
LANE = ROOT / "levers" / "rz1"
RESULTS = Path("public-source-location-withheld")
R70_SOURCE = LEVER_LOCAL / "r70" / "dispatch.py"
R70_HOST_SOURCE = ROOT / "levers" / "r70" / "dispatch.py"
RUNNER = ROOT / "probe-kgn" / "runner"
PYTHON = "/opt/bench/mise/installs/python/3.14.7/bin/python3"
CODEX_BINARY = "public-source-location-withheld"
CODEX_SHA256 = "9a820c17865fa825d04db416818679a9d63bd72e50835c396f496e5684626c9c"
CODEX_PIN = "0.161.0"
# rz1 AMENDMENT-1 (a): bind the whole versioned vendor dir read-only so codex sees its siblings
# (bin/codex-code-mode-host, codex-path, codex-resources); binding only bin/codex broke tool calls in smoke attempt 2.
CODEX_VENDOR = "public-source-location-withheld"
TASKS_ROOT = ROOT / "new-tasks"
EU_HOMES = ROOT / "probe-kgn-eu" / "homes"
TOOLS_BIN = LANE / "tools" / "bin"
CODEX_CONF = LANE / "bench-codex.conf"
EXPECTED_TASKS = tuple(range(1, 9))
STACKS = ("rust", "zig")
MODEL = "gpt-6-luna"
EFFORT = "max"
PROMPT = "default"
REPS = (1, 2, 3)
PLAN_SEED = 1717

sys.path.insert(0, str(LEVER_LOCAL / "lib"))
from launch_guard import native_cell_id, only_args, plan_sha256 as guard_plan_sha256, write_or_check_plan  # noqa: E402

GUARD_SOURCE = "RZ1 deterministic plan seed 1717; native IDs from lane specs"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def spec_doc(task: int, stack: str) -> dict:
    block = f"rz1-eu-{task}-{stack}"
    return {
        "name": block,
        "label": "RZ1 Zig-vs-Rust EU",
        "tasks": [f"r70-{task}-{stack}"],
        "reps": 3,
        "prompts": [PROMPT],
        "timeout_s": 3600,
        "retries": 0,
        "seed": 1,
        "arms": [{"harness": "codex", "model": MODEL, "effort": EFFORT}],
        "extra_args": {"codex": []},
    }


def block_name(task: int, stack: str) -> str:
    return f"rz1-eu-{task}-{stack}"


def spec_host_path(task: int, stack: str) -> Path:
    block = block_name(task, stack)
    return LANE / block / "cells" / f"{block}.json"


def spec_local_path(task: int, stack: str) -> Path:
    block = block_name(task, stack)
    return LANE_LOCAL / block / "cells" / f"{block}.json"


def result_path(task: int, stack: str) -> Path:
    return RESULTS / f"rec-lever-rz1-eu-{task}-{stack}"


def prepare_specs() -> list[Path]:
    paths: list[Path] = []
    for task in EXPECTED_TASKS:
        for stack in STACKS:
            path = spec_local_path(task, stack)
            path.parent.mkdir(parents=True, exist_ok=True)
            (path.parent.parent / "logs").mkdir(parents=True, exist_ok=True)
            doc = spec_doc(task, stack)
            encoded = json.dumps(doc, indent=2, sort_keys=True) + "\n"
            if path.exists():
                current = json.loads(path.read_text(encoding="utf-8"))
                if current != doc:
                    raise SystemExit(f"refusing frozen spec drift: {path}")
            else:
                path.write_text(encoded, encoding="utf-8")
            paths.append(path)
    return paths


def r70_module():
    source = R70_SOURCE if R70_SOURCE.is_file() else R70_HOST_SOURCE
    spec = importlib.util.spec_from_file_location("rz1_r70_dispatch", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load R70 dispatcher helpers from {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def env_for(result: Path) -> dict[str, str]:
    """Start with R70's runtime env and override only lane-owned values."""
    env = r70_module().env_for(result)
    env.update(
        BENCH_ROOT="public-source-location-withheld",
        BENCH_TASKS=str(TASKS_ROOT),
        BENCH_HOMES=str(EU_HOMES),
        BENCH_TOOLS_BIN=str(TOOLS_BIN),
        BENCH_CODEX_CONF=str(CODEX_CONF),
        BENCH_CODEX_PIN=CODEX_PIN,
        BENCH_RESULTS=str(result),
        BENCH_LINUX_RO=f"{CODEX_CONF}:{CODEX_VENDOR}",
        PATH="/opt/bench/mise/installs/node/24.20.0/bin:/opt/bench/cargo/bin:/usr/bin:/bin:/usr/sbin:/sbin",
    )
    return env


def argv_for(task: int, stack: str, rep: int) -> list[str]:
    spec = spec_doc(task, stack)
    cell_id = native_cell_id(spec, rep)
    return [
        PYTHON,
        "bench.py",
        "run",
        str(spec_host_path(task, stack)),
        *only_args(cell_id),
        "--no-gate",
        "--retries",
        "0",
        "--jobs",
        "1",
        "--no-status-pause",
        "--cleanup",
    ]


def build_plan(tasks: list[int], *, provisional: bool) -> dict:
    if not tasks or len(tasks) != len(set(tasks)) or any(t not in EXPECTED_TASKS for t in tasks):
        raise ValueError("tasks must be a non-empty unique subset of 1..8")
    tasks = sorted(tasks)
    rng = random.Random(PLAN_SEED)
    pair_order = [(task, rep) for task in tasks for rep in REPS]
    rng.shuffle(pair_order)
    pairs: list[dict] = []
    cells: list[dict] = []
    for index, (task, rep) in enumerate(pair_order):
        arm_order = list(STACKS)
        rng.shuffle(arm_order)
        pair_id = f"task-{task}-rep-{rep}"
        pair_cells = []
        for arm_index, stack in enumerate(arm_order):
            spec = spec_doc(task, stack)
            cell_id = native_cell_id(spec, rep)
            local_spec = spec_local_path(task, stack)
            if not local_spec.is_file():
                raise ValueError(f"missing lane spec: {local_spec}; run lane_dispatch.py setup")
            spec_sha = sha256_bytes(local_spec.read_bytes())
            argv = argv_for(task, stack, rep)
            cell = {
                "index": len(cells),
                "pair_id": pair_id,
                "pair_order": index,
                "arm_order": arm_index,
                "task": task,
                "task_id": f"r70-{task}-{stack}",
                "stack": stack,
                "rep": rep,
                "smoke": index == 0,
                "cell_id": cell_id,
                "spec": str(spec_host_path(task, stack)),
                "spec_sha256": spec_sha,
                "result_root": str(result_path(task, stack)),
                "argv": argv,
                "argv_sha256": sha256_bytes(canonical_bytes(argv)),
            }
            cells.append(cell)
            pair_cells.append(cell_id)
        pairs.append({
            "pair_id": pair_id,
            "order": index,
            "task": task,
            "rep": rep,
            "smoke_pair": index == 0,
            "arm_order": arm_order,
            "cell_ids": pair_cells,
        })

    core = {
        "schema": "rz1-plan/1",
        "lane": "rz1-eu",
        "host": "kogen-bench-eu",
        "seed": PLAN_SEED,
        "provisional": bool(provisional),
        "admitted_tasks": tasks,
        "repetitions_per_task_per_arm": 3,
        "arms": {
            "rust": {"harness": "codex", "model": MODEL, "effort": EFFORT, "task_suffix": "rust"},
            "zig": {"harness": "codex", "model": MODEL, "effort": EFFORT, "task_suffix": "zig"},
        },
        "codex_pin": CODEX_PIN,
        "codex_binary_sha256": CODEX_SHA256,
        "pair_count": len(pairs),
        "cell_count": len(cells),
        "smoke_pair_id": pairs[0]["pair_id"],
        "pairs": pairs,
        "cells": cells,
    }
    guard_ids = sorted(cell["cell_id"] for cell in cells)
    guard_key = sha256_bytes(canonical_bytes({"tasks": tasks, "provisional": bool(provisional), "seed": PLAN_SEED}))[:16]
    core["launch_guard"] = {
        "directory": f"launch-guard/{guard_key}",
        "sha256": guard_plan_sha256("rz1-eu", GUARD_SOURCE, guard_ids),
        "cell_ids": guard_ids,
    }
    return dict(core, sha256=sha256_bytes(canonical_bytes(core)))


def write_launch_guard(plan: dict) -> dict:
    guard_dir = LANE_LOCAL / plan["launch_guard"]["directory"]
    plan_doc = write_or_check_plan(guard_dir, "rz1-eu", GUARD_SOURCE,
                                   plan["launch_guard"]["cell_ids"], plan["launch_guard"]["cell_ids"],
                                   dry_run=True)
    if plan_doc["sha256"] != plan["launch_guard"]["sha256"]:
        raise ValueError("launch_guard SHA does not match RZ1 plan")
    return plan_doc


def verify_launch_guard(plan: dict) -> dict:
    guard_dir = LANE_LOCAL / plan["launch_guard"]["directory"]
    plan_doc = write_or_check_plan(guard_dir, "rz1-eu", GUARD_SOURCE,
                                   plan["launch_guard"]["cell_ids"], plan["launch_guard"]["cell_ids"],
                                   dry_run=False)
    if plan_doc["sha256"] != plan["launch_guard"]["sha256"]:
        raise ValueError("launch_guard SHA does not match RZ1 plan")
    return plan_doc


def load_plan(path: str | Path) -> dict:
    path = Path(path)
    if not path.is_absolute():
        path = LANE_LOCAL / path
    plan = json.loads(path.read_text(encoding="utf-8"))
    expected = build_plan(plan.get("admitted_tasks", []), provisional=bool(plan.get("provisional")))
    if plan != expected:
        raise ValueError("plan does not match the deterministic RZ1 generator")
    verify_launch_guard(plan)
    return plan


def plan_path(path: str | Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else LANE_LOCAL / path


def describe_cell(plan: dict, index: int) -> dict:
    try:
        return plan["cells"][index]
    except (IndexError, TypeError):
        raise ValueError(f"cell index out of range: {index}") from None


def require_release(plan: dict, scope: str) -> dict:
    receipt_path = LANE / "gate" / "release-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    key = "allows_smoke_launch" if scope == "smoke" else "allows_scored_launch"
    if receipt.get(key) is not True:
        raise RuntimeError(f"release receipt does not allow {scope} launch")
    if receipt.get("plan_sha256") != plan["sha256"]:
        raise RuntimeError("release receipt is bound to a different plan sha256")
    return receipt


def launch_one(plan_file: str, index: int, scope: str) -> int:
    plan = load_plan(plan_file)
    if plan["provisional"]:
        raise RuntimeError("provisional plan cannot launch")
    require_release(plan, scope)
    if scope == "smoke" and not plan["cells"][index]["smoke"]:
        raise RuntimeError("smoke scope may select only the first planned pair")
    if scope == "bulk" and plan["cells"][index]["smoke"]:
        raise RuntimeError("bulk scope keeps the already-run smoke cells in the ITT plan")
    sys.path.insert(0, str(LEVER_LOCAL / "lib"))
    from count_cells import count_cells
    cell = describe_cell(plan, index)
    task, stack, rep = int(cell["task"]), str(cell["stack"]), int(cell["rep"])
    env = env_for(result_path(task, stack))
    block = LANE / block_name(task, stack)
    log_path = block / "logs" / f"{cell['cell_id']}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    child = None

    def terminate(signum, _frame):
        if child is not None and child.poll() is None:
            try:
                os.killpg(child.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        else:
            raise SystemExit(128 + signum)

    old_term = signal.signal(signal.SIGTERM, terminate)
    old_int = signal.signal(signal.SIGINT, terminate)
    launch_lock = (ROOT / "levers" / "r70" / "launch-eu.lock").open("a")
    locked = False
    try:
        try:
            fcntl.flock(launch_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("R70 EU launch interlock is busy") from None
        locked = True
        if count_cells() != 0:
            raise RuntimeError("another benchmark cell is running on EU")
        disk_rows = subprocess.check_output(["df", "-B1", "--output=avail", "/srv"], text=True).splitlines()
        try:
            free_bytes = int(disk_rows[1].strip())
        except (IndexError, ValueError):
            raise RuntimeError("could not determine EU free disk bytes") from None
        if free_bytes < 6 * 1024 ** 3:
            raise RuntimeError("EU disk free space is below 6 GiB")
        stop_markers = [ROOT / "STOP-eu", ROOT / "levers" / "STOP-eu", ROOT / "levers" / "r70" / "STOP-eu", LANE / "STOP"]
        if any(path.exists() for path in stop_markers):
            raise RuntimeError("an EU STOP marker is present")
        with log_path.open("ab", buffering=0) as output:
            child = subprocess.Popen(cell["argv"], cwd=RUNNER, env=env, stdin=subprocess.DEVNULL,
                                     stdout=output, stderr=subprocess.STDOUT, start_new_session=True)
    finally:
        if locked:
            fcntl.flock(launch_lock, fcntl.LOCK_UN)
        launch_lock.close()
    try:
        return child.wait()
    except KeyboardInterrupt:
        terminate(signal.SIGTERM, None)
        try:
            return child.wait(timeout=15)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            return child.wait()
    finally:
        signal.signal(signal.SIGTERM, old_term)
        signal.signal(signal.SIGINT, old_int)


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("setup")
    verify = sub.add_parser("verify-plan")
    verify.add_argument("--plan", required=True)
    emit = sub.add_parser("describe")
    emit.add_argument("--plan", required=True)
    emit.add_argument("--index", type=int, required=True)
    launch = sub.add_parser("launch-one")
    launch.add_argument("--plan", required=True)
    launch.add_argument("--index", type=int, required=True)
    launch.add_argument("--scope", choices=("smoke", "bulk"), required=True)
    version = sub.add_parser("version-check")
    args = ap.parse_args()

    if args.cmd == "setup":
        paths = prepare_specs()
        print(json.dumps({"spec_count": len(paths), "specs": [str(p) for p in paths]}, indent=2))
        return 0
    if args.cmd == "verify-plan":
        plan = load_plan(args.plan)
        print(json.dumps({"plan_sha256": plan["sha256"], "cells": plan["cell_count"],
                          "pairs": plan["pair_count"], "provisional": plan["provisional"]}, sort_keys=True))
        return 0
    if args.cmd == "describe":
        plan = load_plan(args.plan)
        print(json.dumps(describe_cell(plan, args.index), sort_keys=True))
        return 0
    if args.cmd == "launch-one":
        return launch_one(args.plan, args.index, args.scope)
    if args.cmd == "version-check":
        env = env_for(result_path(1, "rust"))
        env["TMPDIR"] = str(LANE / "gate" / "version-tmp")
        env["MISE_STATE_DIR"] = str(LANE / "gate" / "version-mise-state")
        Path(env["TMPDIR"]).mkdir(parents=True, exist_ok=True)
        Path(env["MISE_STATE_DIR"]).mkdir(parents=True, exist_ok=True)
        wrapper = TOOLS_BIN / "bench-codex"
        result = subprocess.run([str(wrapper), "--version"], cwd=RUNNER, env=env, stdin=subprocess.DEVNULL,
                                capture_output=True, text=True, timeout=15, check=False)
        receipt = {"wrapper": str(wrapper), "codex_home": str(EU_HOMES / "codex"), "version": result.stdout.strip(),
                   "returncode": result.returncode, "pin": CODEX_PIN, "binary": CODEX_BINARY,
                   "binary_sha256_expected": CODEX_SHA256}
        print(json.dumps(receipt, sort_keys=True))
        return result.returncode
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
