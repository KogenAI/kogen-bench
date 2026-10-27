#!/usr/bin/env python3
"""Recompute every number on the terra-builder-1 and terra-builder-effort-1 pages from their published files.

Usage, from the repository root:  python3 -I rounds/terra-builder-1/analyze.py [--write]

It reads only rounds/terra-builder-1/ and rounds/terra-builder-effort-1/ (each bundle's attempt.json and
evaluation.json, and fair-tests.json), uses the Python standard library, makes no model call and needs no private
data. Without --write it prints the tables; with --write it also writes results.txt next to itself.

Definitions. A cell "passed" when every hidden test of its task passed. A cell "passed the fair tests" when it
landed and every hidden test that does not depend on a name the request never states passed (fair-tests.json
holds the counts). The two tasks whose Intents contained clashing rules (task-05, task-06) are void in the
re-score, and cells that stopped for a harness reason (cost_cap) are left out of it.
"""
import glob
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROUNDS = os.path.dirname(HERE)
OUT = []
VOID_TASKS = {"task-05", "task-06"}
PLUMBING = {"cost_cap"}


def say(text=""):
    OUT.append(text)
    print(text)


def median(xs):
    xs = sorted(x for x in xs if isinstance(x, (int, float)))
    m = len(xs) // 2
    return None if not xs else xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def load(round_id):
    base = os.path.join(ROUNDS, round_id)
    fair = json.load(open(os.path.join(base, "fair-tests.json")))["cells"]
    cells = []
    for f in sorted(glob.glob(os.path.join(base, "bundles", "*", "attempts", "*", "r*", "*", "a1", "attempt.json"))):
        a = json.load(open(f))
        e = json.load(open(os.path.join(os.path.dirname(f), "evaluation.json")))
        task = f.split(os.sep + "attempts" + os.sep)[1].split(os.sep)[0]
        build = next((s for s in a["stages"] if s["stage"] == "build"), {})
        ids = e["ids"]
        fr = fair[a["cell"]]
        arm = "-".join(a["lane"].split("-")[:2])
        cells.append({"task": task, "arm": arm, "lane": a["lane"], "outcome": build.get("outcome") or a["outcome"],
                      "passed": ids["passed_count"], "total": sum(ids.values()), "all": bool(e["all_passed"]),
                      "wall": a["wall_s"], "input": a["totals"]["input_tokens"], "output": a["totals"]["output_tokens"],
                      "fair_total": fr["hidden"] - fr["unfair"], "fair_passed": fr["fair_passed"], "unfair": fr["unfair"],
                      "fair_pass": a["outcome"] == "landed" and fr["fair_failed"] == 0})
    return cells


def tables(round_id, order):
    cells = load(round_id)
    say(f"## {round_id}")
    say()
    tasks = sorted({c["task"] for c in cells})
    say("### Per task: outcome and hidden tests passed")
    say()
    say("| Task | Hidden tests (not passing the request-stated filter: unfair) | " + " | ".join(order) + " |")
    say("| --- | --- | " + " | ".join("---" for _ in order) + " |")
    for t in tasks:
        row = {c["arm"]: c for c in cells if c["task"] == t}
        first = next(iter(row.values()))
        cols = []
        for arm in order:
            c = row[arm]
            cols.append(f"{c['outcome']}, {c['passed']}/{c['total']}" + (" (all)" if c["all"] else ""))
        say(f"| {t} | {first['total']} ({first['unfair']} unfair) | " + " | ".join(cols) + " |")
    say()
    say("### Per arm, as run (all tasks)")
    say()
    say("| Arm | Cells | Passed all hidden tests | Hidden tests passed | Median wall s | Input tokens (sum) | Output tokens (sum) |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for arm in order:
        v = [c for c in cells if c["arm"] == arm]
        say(f"| {arm} | {len(v)} | {sum(c['all'] for c in v)} | {sum(c['passed'] for c in v)}/{sum(c['total'] for c in v)} | "
            f"{median([c['wall'] for c in v]):,.0f} | {sum(c['input'] for c in v) / 1e6:.2f}M | {sum(c['output'] for c in v) / 1e3:.0f}k |")
    say()
    say("### Re-score: fair tests, void tasks and harness stops removed")
    say()
    say("Counts over the cells that remain (task-05 and task-06 are void for every arm; cost_cap cells are excluded).")
    say()
    say("| Arm | Cells kept | Passed the fair tests | Fair hidden tests passed (kept cells) | Cells kept out | Passed the fair tests, all cells as run |")
    say("| --- | ---: | ---: | ---: | --- | ---: |")
    for arm in order:
        v = [c for c in cells if c["arm"] == arm]
        kept = [c for c in v if c["task"] not in VOID_TASKS and c["outcome"] not in PLUMBING]
        out = [c for c in v if c not in kept]
        why = ", ".join(sorted({f"{c['task']} ({'void task' if c['task'] in VOID_TASKS else c['outcome']})" for c in out})) or "none"
        say(f"| {arm} | {len(kept)} | {sum(c['fair_pass'] for c in kept)} | "
            f"{sum(c['fair_passed'] for c in kept)}/{sum(c['fair_total'] for c in kept)} | {why} | "
            f"{sum(c['fair_pass'] for c in v)} of {len(v)} |")
    say()
    return cells


def main():
    say("# terra-builder-1 and terra-builder-effort-1: recomputed from the published files")
    say()
    tables("terra-builder-1", ["sol-medium", "terra-medium", "terra-max"])
    tables("terra-builder-effort-1", ["sol-medium", "terra-low", "terra-medium", "terra-high"])
    if "--write" in sys.argv:
        open(os.path.join(HERE, "results.txt"), "w").write("\n".join(OUT) + "\n")


main()
