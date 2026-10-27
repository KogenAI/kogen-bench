#!/usr/bin/env python3
"""Recompute every number on the shaper-models-1 page from its published bundle.

Usage, from the repository root:  python3 -I rounds/shaper-models-1/analyze.py [--write]

It reads only rounds/shaper-models-1/ (the bundle's attempt.json and evaluation.json of every graded cell, and
PLAN.json), uses the Python standard library, makes no model call and needs no private data. Without --write it
prints the tables; with --write it also writes results.txt next to itself.

A cell "holds" when its Intent's scenarios all pass on the reference solution, all fail on the starting code, and
every known-wrong variant is caught, and the shaper finished. Cells where the shaper did not finish carry an
infrastructure note in evaluation.json and do not hold.
"""
import glob
import json
import math
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []


def say(text=""):
    OUT.append(text)
    print(text)


def wilson(k, n, z=1.959964):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def median(xs):
    xs = sorted(x for x in xs if isinstance(x, (int, float)))
    if not xs:
        return None
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def sign_p(wins, losses):
    n = wins + losses
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(wins, losses) + 1)) / 2 ** n)


def load():
    cells = []
    for f in sorted(glob.glob(os.path.join(HERE, "bundles", "*", "attempts", "*", "r*", "*", "a1", "attempt.json"))):
        a = json.load(open(f))
        e = json.load(open(os.path.join(os.path.dirname(f), "evaluation.json")))
        task = f.split(os.sep + "attempts" + os.sep)[1].split(os.sep)[0]
        stage = next(s for s in a["stages"] if s["stage"] == "shape")
        held = (not e.get("infrastructure") and isinstance(e.get("scenarios"), int) and e["scenarios"] > 0
                and e["pass_on_reference"] == e["scenarios"] == e["fail_on_start"] and e["wrong_caught"] == e["wrong_total"])
        arm, split = a["lane"].rsplit("-", 1)
        cells.append({"task": task, "arm": arm, "split": split, "rep": a["cell"].split("/")[1], "outcome": a["outcome"],
                      "held": bool(held), "wall": stage["wall_s"], "input": stage["input_tokens"], "output": stage["output_tokens"],
                      "requests": stage["requests"], "cost": stage["cost_usd"], "lane": a["lane"]})
    return cells


def main():
    cells = load()
    plan = json.load(open(os.path.join(HERE, "PLAN.json")))
    say("# shaper-models-1: recomputed from the published bundle")
    say()
    say(f"Graded cells: {len(cells)}")
    say()
    say("## Matrices held, by arm and split")
    say()
    say("| Arm | Split | Cells | Held | Shaper outcomes |")
    say("| --- | --- | ---: | ---: | --- |")
    by = defaultdict(list)
    for c in cells:
        by[(c["arm"], c["split"])].append(c)
    order = ["sol-high", "sol-low", "sonnet-medium", "opus-medium", "terra-medium"]
    for arm in order:
        for split in ("train", "test"):
            v = by.get((arm, split))
            if v:
                oc = ", ".join(f"{k} {n}" for k, n in sorted(Counter(c["outcome"] for c in v).items()))
                say(f"| {arm} | {split} | {len(v)} | {sum(c['held'] for c in v)} | {oc} |")
    say()
    say("## All 16 tasks, 2 repetitions (32 cells per arm)")
    say()
    say("| Arm | Cells | Held | Share | 95% Wilson interval |")
    say("| --- | ---: | ---: | ---: | --- |")
    arms = defaultdict(list)
    for c in cells:
        arms[c["arm"]].append(c)
    for arm in order:
        v = arms[arm]
        k, n = sum(c["held"] for c in v), len(v)
        lo, hi = wilson(k, n)
        say(f"| {arm} | {n} | {k} | {100 * k / n:.0f}% | {100 * lo:.0f}% to {100 * hi:.0f}% |")
    say()

    def held_by_task(arm, tasks):
        return {t: sum(c["held"] for c in arms[arm] if c["task"] == t) for t in tasks}

    def compare(a, b, tasks):
        pa, pb = held_by_task(a, tasks), held_by_task(b, tasks)
        w = sum(pa[t] > pb[t] for t in tasks)
        l = sum(pa[t] < pb[t] for t in tasks)
        return w, l, sign_p(w, l)

    all_tasks = sorted({c["task"] for c in arms["sol-high"]} | {c["task"] for c in arms["sol-low"]})
    train = sorted({c["task"] for c in cells if c["split"] == "train"})
    test = sorted({c["task"] for c in cells if c["split"] == "test"})
    say("## Paired comparisons by task (repetitions summed per task; two-sided exact sign test over tasks that differ)")
    say()
    say("| Comparison | Tasks | A better | B better | Tied | p |")
    say("| --- | --- | ---: | ---: | ---: | ---: |")
    rows = [("sol-low", "sol-high", all_tasks, "all 16"), ("sonnet-medium", "sol-high", all_tasks, "all 16"),
            ("sol-low", "sonnet-medium", all_tasks, "all 16"), ("opus-medium", "sol-high", train, "train 8"),
            ("opus-medium", "sol-low", train, "train 8"), ("opus-medium", "sonnet-medium", train, "train 8"),
            ("terra-medium", "sol-high", test, "test 8"), ("terra-medium", "sol-low", test, "test 8"),
            ("terra-medium", "sonnet-medium", test, "test 8")]
    smallest = 1.0
    for a, b, tasks, label in rows:
        w, l, p = compare(a, b, tasks)
        smallest = min(smallest, p)
        say(f"| {a} (A) vs {b} (B) | {label} | {w} | {l} | {len(tasks) - w - l} | {p:.3f} |")
    say()
    say(f"Smallest p among these nine comparisons: {smallest:.3f}. None is below 0.05.")
    say()
    say("## Shape stage per cell (median over cells that logged the value)")
    say()
    say("| Arm | Wall seconds | Requests | Input tokens | Output tokens | List-price cost per cell |")
    say("| --- | ---: | ---: | ---: | ---: | ---: |")
    for arm in order:
        v = arms[arm]
        cost = [c["cost"] for c in v if isinstance(c["cost"], (int, float))]
        cs = f"${median(cost):.2f} ({len(cost)} cells priced)" if cost and arm != "terra-medium" else "unpriced"
        w, r, i, o = (median([c[k] for c in v]) for k in ("wall", "requests", "input", "output"))
        say(f"| {arm} | {w:,.0f} | {r:g} | {i:,.0f} | {o:,.0f} | {cs} |")
    say()
    say("## Graded cells per lane")
    say()
    got = Counter(c["lane"] for c in cells)
    for lane in [l["name"] for l in plan["experiment"]["lanes"]]:
        say(f"- {lane}: {got.get(lane, 0)} graded cells")
    if "--write" in sys.argv:
        open(os.path.join(HERE, "results.txt"), "w").write("\n".join(OUT) + "\n")


main()
