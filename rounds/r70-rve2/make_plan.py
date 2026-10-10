#!/usr/bin/env python3
"""Create the frozen rve2 assignment plan using only the Python standard library."""
import hashlib
import json
import random

SEED = 20261009
TASKS = (1, 5, 7)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def build_plan():
    rng = random.Random(SEED)
    # Choose the block-1 EU allocation: five of nine, while each task gets 1 or 2.
    counts = [1, 1, 1]
    for idx in rng.sample(range(3), 2):
        counts[idx] += 1
    host_by_task = {}
    for task, eu_first in zip(TASKS, counts):
        hosts = ["eu"] * eu_first + ["us"] * (3 - eu_first)
        hosts += ["eu"] * (3 - eu_first) + ["us"] * eu_first
        host_by_task[task] = hosts

    pairs = []
    order = 0
    for block in (1, 2):
        block_items = [(task, rep) for task in TASKS for rep in range(1, 4)]
        rng.shuffle(block_items)
        for task, rep in block_items:
            order += 1
            host = host_by_task[task][(block - 1) * 3 + rep - 1]
            arms = ["rust", "elixir"]
            rng.shuffle(arms)
            cells = [{
                "arm": arm,
                "task_id": f"r70-{task}-{arm}",
                "run_id": f"rve2-{host}-p{order:02d}-{arm}",
            } for arm in arms]
            pairs.append({"pair_order": order, "block": block, "task": task,
                          "rep": rep, "host": host, "cells": cells})
    return pairs


def main():
    pairs = build_plan()
    plan = {"round": "rve2", "seed": SEED, "pairs": pairs,
            "plan_sha256": hashlib.sha256(canonical(pairs)).hexdigest()}
    with open("PLAN.json", "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({"plan_sha256": plan["plan_sha256"], "pairs": len(pairs),
                      "cells": sum(len(p["cells"]) for p in pairs)}, sort_keys=True))


if __name__ == "__main__":
    main()
