#!/usr/bin/env python3
"""Generate deterministic RZ1 pair/arm order from an admitted task list."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from lane_dispatch import LANE_LOCAL, build_plan, write_launch_guard


def read_tasks(value: str | None, file_value: str | None) -> list[int]:
    if bool(value) == bool(file_value):
        raise SystemExit("provide exactly one of --tasks or --tasks-file")
    if value:
        raw = [part.strip() for part in value.split(",") if part.strip()]
    else:
        path = Path(file_value)
        if not path.is_absolute():
            path = LANE_LOCAL / path
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("admitted_tasks")
        if not isinstance(data, list):
            raise SystemExit("tasks file must be a JSON array or contain admitted_tasks")
        raw = data
    try:
        tasks = [int(x) for x in raw]
    except (TypeError, ValueError):
        raise SystemExit("task IDs must be integers from 1 through 8") from None
    if not tasks or len(tasks) != len(set(tasks)) or any(t < 1 or t > 8 for t in tasks):
        raise SystemExit("task IDs must be a non-empty unique subset of 1..8")
    return sorted(tasks)


def main() -> int:
    ap = argparse.ArgumentParser()
    tasks_group = ap.add_mutually_exclusive_group(required=True)
    tasks_group.add_argument("--tasks", help="comma-separated admitted task numbers")
    tasks_group.add_argument("--tasks-file", help="JSON array or {admitted_tasks: [...]} file")
    ap.add_argument("--output", default="PLAN.json", help="output path, relative to levers/rz1 by default")
    ap.add_argument("--provisional", action="store_true", help="mark this plan ineligible for launch")
    args = ap.parse_args()

    tasks = read_tasks(args.tasks, args.tasks_file)
    plan = build_plan(tasks, provisional=args.provisional)
    write_launch_guard(plan)
    output = Path(args.output)
    if not output.is_absolute():
        output = LANE_LOCAL / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "sha256": plan["sha256"], "tasks": tasks,
                      "pairs": plan["pair_count"], "cells": plan["cell_count"],
                      "smoke_pair_id": plan["smoke_pair_id"], "provisional": plan["provisional"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
