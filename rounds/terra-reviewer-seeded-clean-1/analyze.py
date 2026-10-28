#!/usr/bin/env python3
"""Recompute every number on the terra-reviewer-seeded-clean-1 page from its published bundles.

Usage, from the repository root:  python3 -I rounds/terra-reviewer-seeded-clean-1/analyze.py [--write]

It reads only this round's files (each cell's attempt.json and evaluation.json in bundles/). Standard library only, no
model call, no private data. Without --write it prints the tables; with --write it also writes results.txt next to it.

A seeded cell "escapes" when the committed tree fails the hidden tests. A clean control "false-blocks" when review
stops the build, or the build ends any way other than landed, or the committed tree fails the hidden tests. A cell is
"invalid" when its outcome is a review that returned nothing usable or that timed out; no cell of this round is. Review
stage figures come from the review stage of attempt.json: wall time, requests, input tokens (cached input included) and
output tokens as logged, and list-price cost where the model has a price. Task ids starting "seed" are seeded cases,
ids starting "clean" are clean controls.
"""
import glob
import json
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
ARMS = [("Sol high", "sol-high"), ("Terra medium", "terra-medium"), ("Opus medium", "opus-medium")]
GRID = [("Terra low", "terra-low-grid"), ("Terra medium", "terra-medium-grid"), ("Terra high", "terra-high-grid")]


def say(text=""):
    OUT.append(text)
    print(text)


def median(xs):
    xs = sorted(x for x in xs if isinstance(x, (int, float)))
    m = len(xs) // 2
    return None if not xs else xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def cp_upper(k, n, conf=0.95):
    """One-sided exact (Clopper-Pearson) upper bound; 0 of 78 gives 3.8%."""
    if k >= n:
        return 1.0
    lo, hi = k / n, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        cdf = sum(math.comb(n, i) * mid ** i * (1 - mid) ** (n - i) for i in range(k + 1))
        lo, hi = (mid, hi) if cdf > 1 - conf else (lo, mid)
    return (lo + hi) / 2


def wilson_upper(k, n, z=1.96):
    p = k / n
    return (p + z * z / (2 * n) + z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / (1 + z * z / n)


def sign_p(wins, losses):
    n = wins + losses
    return 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, i) for i in range(min(wins, losses) + 1)) / 2 ** n)


def load():
    cells = []
    for f in sorted(glob.glob(os.path.join(HERE, "bundles", "*", "attempts", "*", "r*", "*", "a1", "attempt.json"))):
        a = json.load(open(f))
        e = json.load(open(os.path.join(os.path.dirname(f), "evaluation.json")))
        task = f.split(os.sep + "attempts" + os.sep)[1].split(os.sep)[0]
        rv = next((s for s in a["stages"] if s["stage"] == "review"), {})
        cells.append({"task": task, "kind": task.split("-")[0], "lane": a["lane"], "rep": a["cell"].split("/")[1],
                      "outcome": a["outcome"], "passed": e.get("all_passed"), "wall": rv.get("wall_s"),
                      "requests": rv.get("requests"), "input": rv.get("input_tokens"), "output": rv.get("output_tokens"),
                      "cost": rv.get("cost_usd")})
    return cells


def pick(cells, lane, kind=None):
    return [c for c in cells if c["lane"] == lane and (kind is None or c["kind"] == kind)]


def stage_row(name, v):
    cost = [c["cost"] for c in v if isinstance(c["cost"], (int, float)) and c["cost"] > 0]
    cs = f"${median(cost):.3f} (total ${sum(cost):.2f})" if cost else "unpriced"
    return (f"| {name} | {len(v)} | {median([c['wall'] for c in v]):,.0f} | {median([c['requests'] for c in v]):g} | "
            f"{median([c['input'] for c in v]):,.0f} ({sum(c['input'] for c in v) / 1e6:.1f}M) | {median([c['output'] for c in v]):,.0f} | {cs} |")


def main():
    cells = load()
    say("# terra-reviewer-seeded-clean-1: recomputed from the published bundles")
    say()
    say(f"Cells in the bundles: {len(cells)}; lanes: {len({c['lane'] for c in cells})}.")
    say()
    say("## Seeded cases (26 cases x 3 repetitions = 78 cells per arm)")
    say()
    say("| Review setting | Cells | Landed | Committed wrong (escapes) | Upper bound, exact (one-sided 95%) | Upper bound, Wilson (two-sided 95%) | Cases with an escape |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    seeded = {}
    for name, lane in ARMS:
        v = seeded[name] = pick(cells, lane, "seed")
        esc = [c for c in v if c["passed"] is not True]
        say(f"| {name} | {len(v)} | {sum(c['outcome'] == 'landed' for c in v)} | {len(esc)} | {100 * cp_upper(len(esc), len(v)):.1f}% | "
            f"{100 * wilson_upper(len(esc), len(v)):.1f}% | {len({c['task'] for c in esc})} of {len({c['task'] for c in v})} |")
    say()
    say("## Clean controls (15 cases x 2 repetitions = 30 cells per arm)")
    say()
    say("| Review setting | Cells | Landed | False blocks | Committed wrong | Upper bound on the false-block rate, exact (one-sided 95%) |")
    say("| --- | ---: | ---: | ---: | ---: | ---: |")
    clean = {}
    for name, lane in ARMS:
        v = clean[name] = pick(cells, lane, "clean")
        blocks = [c for c in v if c["outcome"] != "landed" or c["passed"] is not True]
        say(f"| {name} | {len(v)} | {sum(c['outcome'] == 'landed' for c in v)} | {len(blocks)} | {sum(c['passed'] is not True for c in v)} | "
            f"{100 * cp_upper(len(blocks), len(v)):.1f}% |")
    say()
    say("## Review stage per cell, seeded cases (median; input sum in brackets)")
    say()
    hdr = "| Review setting | Cells | Wall seconds | Requests | Input tokens (cached included) | Output tokens | List-price cost per cell |"
    say(hdr)
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, _ in ARMS:
        say(stage_row(name, seeded[name]))
    say()
    say("## Review stage per cell, clean controls (median; input sum in brackets)")
    say()
    say(hdr)
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, _ in ARMS:
        say(stage_row(name, clean[name]))
    say()
    say("## Against Sol high, seeded and clean cells together")
    say()
    say("| Review setting | Wall time, Sol high / this (seeded) | Wall time, Sol high / this (clean) | Input tokens per task vs Sol high (median per task) | Tasks lower / higher | Sign test p |")
    say("| --- | ---: | ---: | ---: | ---: | ---: |")
    sol = defaultdict(list)
    for c in pick(cells, "sol-high"):
        sol[c["task"]].append(c["input"])
    sw, sc = median([c["wall"] for c in seeded["Sol high"]]), median([c["wall"] for c in clean["Sol high"]])
    for name, lane in ARMS[1:]:
        per = defaultdict(list)
        for c in pick(cells, lane):
            per[c["task"]].append(c["input"])
        diffs = [median(per[t]) / median(sol[t]) - 1 for t in per]
        lo, hi = sum(d < 0 for d in diffs), sum(d > 0 for d in diffs)
        say(f"| {name} | {sw / median([c['wall'] for c in seeded[name]]):.1f}x | {sc / median([c['wall'] for c in clean[name]]):.1f}x | "
            f"{100 * median(diffs):+.0f}% | {lo} / {hi} | {sign_p(lo, hi):.4f} |")
    say()
    say("## Registered rule for Terra as a reviewer candidate")
    say()
    t, s = seeded["Terra medium"], seeded["Sol high"]
    te, se = sum(c["passed"] is not True for c in t), sum(c["passed"] is not True for c in s)
    tb = sum(c["outcome"] != "landed" or c["passed"] is not True for c in clean["Terra medium"])
    inv = lambda v: sum(c["outcome"] not in ("landed", "fail") for c in v)
    ti, si = inv(pick(cells, "terra-medium")), inv(pick(cells, "sol-high"))
    r1 = te <= 1 and 100 * (wilson_upper(te, len(t)) - wilson_upper(se, len(s))) <= 5
    r2, r3 = tb == 0, ti <= si
    say("| Condition | Terra medium | Sol high | Met |")
    say("| --- | ---: | ---: | --- |")
    say(f"| 1. Escapes on the seeded cases: at most 1 in 78, and the Wilson upper bound within 5 points of Sol high's | {te} of {len(t)} (bound {100 * wilson_upper(te, len(t)):.1f}%) | {se} of {len(s)} (bound {100 * wilson_upper(se, len(s)):.1f}%) | {'yes' if r1 else 'no'} |")
    say(f"| 2. No false block on the clean controls | {tb} of {len(clean['Terra medium'])} | {sum(c['outcome'] != 'landed' or c['passed'] is not True for c in clean['Sol high'])} of {len(clean['Sol high'])} | {'yes' if r2 else 'no'} |")
    say(f"| 3. Validity equal: invalid reviews plus timeouts not above Sol high's | {ti} | {si} | {'yes' if r3 else 'no'} |")
    say()
    say(f"Verdict: **{'Terra medium meets the registered rule and is a reviewer candidate' if r1 and r2 and r3 else 'Terra medium does not meet the registered rule'}**.")
    say()
    say("## Effort grid on a 20-case subset (12 seeded, 8 clean; one repetition each)")
    say()
    say("| Terra review effort | Seeded cells | Escapes | Clean cells | False blocks | Review wall median s | Review input median (cached included) |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, lane in GRID:
        sv, cv = pick(cells, lane, "seed"), pick(cells, lane, "clean")
        say(f"| {name} | {len(sv)} | {sum(c['passed'] is not True for c in sv)} | {len(cv)} | "
            f"{sum(c['outcome'] != 'landed' or c['passed'] is not True for c in cv)} | {median([c['wall'] for c in sv + cv]):,.0f} | "
            f"{median([c['input'] for c in sv + cv]):,.0f} |")
    if "--write" in sys.argv:
        open(os.path.join(HERE, "results.txt"), "w").write("\n".join(OUT) + "\n")


main()
