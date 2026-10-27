#!/usr/bin/env python3
"""Recompute every number on the reviewer-models-seeded-1 and reviewer-models-clean-1 pages from published files.

Usage, from the repository root:  python3 -I rounds/reviewer-models-seeded-1/analyze.py [--write]

It reads rounds/reviewer-models-seeded-1/, rounds/reviewer-models-clean-1/ and, for the Sol high comparison arm and
the Sonnet context row, the already published rounds review-value-2-openai and review-value-2 (records.jsonl and each
bundle's attempt.json and evaluation.json). It uses the Python standard library, makes no model call and needs no
private data. Without --write it prints the tables; with --write it also writes results.txt next to itself.

A seeded cell "escapes" when the committed tree fails the hidden tests (the record's outcome is "fail"). A clean
control "false-blocks" when review stops the build or the committed tree fails (anything but a landed, passing cell).
Review stage figures are the review stage of attempt.json: wall time, requests, input and output tokens as logged,
and list-price cost where the model has a price.
"""
import glob
import json
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROUNDS = os.path.dirname(HERE)
OUT = []


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


def sign_p(wins, losses):
    n = wins + losses
    return 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, i) for i in range(min(wins, losses) + 1)) / 2 ** n)


def load(round_id):
    base = os.path.join(ROUNDS, round_id)
    cells = []
    for f in sorted(glob.glob(os.path.join(base, "bundles", "*", "attempts", "*", "r*", "*", "a1", "attempt.json"))):
        a = json.load(open(f))
        e = json.load(open(os.path.join(os.path.dirname(f), "evaluation.json")))
        task = f.split(os.sep + "attempts" + os.sep)[1].split(os.sep)[0]
        rv = next((s for s in a["stages"] if s["stage"] == "review"), {})
        cells.append({"task": task, "lane": a["lane"], "rep": a["cell"].split("/")[1], "outcome": a["outcome"],
                      "passed": e.get("all_passed"), "wall": rv.get("wall_s"), "requests": rv.get("requests"),
                      "input": rv.get("input_tokens"), "output": rv.get("output_tokens"), "cost": rv.get("cost_usd")})
    return cells


def main():
    say("# reviewer-models-seeded-1 and reviewer-models-clean-1: recomputed from the published files")
    say()
    seeded = {"Sol high": [c for c in load("review-value-2-openai")],
              "Terra medium": [c for c in load("reviewer-models-seeded-1") if c["lane"] == "r-terra-medium"],
              "Opus medium": [c for c in load("reviewer-models-seeded-1") if c["lane"] == "r-opus-medium"]}
    order = ["Sol high", "Terra medium", "Opus medium"]
    say("## Seeded defects (26 cases x 3 repetitions = 78 cells per arm)")
    say()
    say("| Review setting | Cells | Landed | Committed wrong (escapes) | Upper bound (one-sided 95%) | Cases with an escape |")
    say("| --- | ---: | ---: | ---: | ---: | ---: |")
    for arm in order:
        v = seeded[arm]
        esc = [c for c in v if c["passed"] is not True]
        say(f"| {arm} | {len(v)} | {sum(c['outcome'] == 'landed' for c in v)} | {len(esc)} | "
            f"{100 * cp_upper(len(esc), len(v)):.1f}% | {len({c['task'] for c in esc})} of {len({c['task'] for c in v})} |")
    say()
    say("## Review stage per cell (median; sums in brackets)")
    say()
    say("| Review setting | Wall seconds | Requests | Input tokens | Output tokens | List-price cost per cell |")
    say("| --- | ---: | ---: | ---: | ---: | ---: |")
    for arm in order:
        v = seeded[arm]
        cost = [c["cost"] for c in v if isinstance(c["cost"], (int, float))]
        cs = f"${median(cost):.3f} (total ${sum(cost):.2f})" if cost else "unpriced"
        say(f"| {arm} | {median([c['wall'] for c in v]):,.0f} (sum {sum(c['wall'] for c in v) / 3600:.1f} h) | "
            f"{median([c['requests'] for c in v]):g} | {median([c['input'] for c in v]):,.0f} ({sum(c['input'] for c in v) / 1e6:.1f}M) | "
            f"{median([c['output'] for c in v]):,.0f} | {cs} |")
    say()
    sol_wall = median([c["wall"] for c in seeded["Sol high"]])
    sol_in = defaultdict(list)
    for c in seeded["Sol high"]:
        sol_in[c["task"]].append(c["input"])
    say("## Against Sol high")
    say()
    say("| Review setting | Wall time, Sol high / this | Input tokens per task vs Sol high (median per task) | Tasks lower / higher | Sign test p |")
    say("| --- | ---: | ---: | ---: | ---: |")
    for arm in ["Terra medium", "Opus medium"]:
        wall = median([c["wall"] for c in seeded[arm]])
        per = defaultdict(list)
        for c in seeded[arm]:
            per[c["task"]].append(c["input"])
        diffs = {t: median(per[t]) / median(sol_in[t]) - 1 for t in per}
        lo = sum(d < 0 for d in diffs.values())
        hi = sum(d > 0 for d in diffs.values())
        say(f"| {arm} | {sol_wall / wall:.1f}x | {100 * median(list(diffs.values())):+.0f}% | {lo} / {hi} | {sign_p(lo, hi):.4f} |")
    say()
    sonnet = [r for r in map(json.loads, open(os.path.join(ROUNDS, "review-value-2", "records.jsonl"))) if r["arm"] == "r-now"]
    esc = sum(r["outcome"] == "fail" for r in sonnet)
    say(f"Context, from the published earlier round: Claude Sonnet 5.5 at medium effort as reviewer committed a wrong tree in {esc} cells "
        f"({len(sonnet)} records; that page counts 77 valid cells because one cell was invalid).")
    say()
    say("## Clean controls (correct code; 15 cases x 2 repetitions planned per arm)")
    say()
    clean = load("reviewer-models-clean-1")
    say("| Review setting | Cells graded | Cells planned | False blocks | Committed wrong | Review wall median s | Review requests median |")
    say("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    planned = {"r-opus-medium": 30, "r-now-sol": 30, "r-terra-medium": 30}
    names = {"r-now-sol": "Sol high", "r-terra-medium": "Terra medium", "r-opus-medium": "Opus medium"}
    for lane in ["r-now-sol", "r-terra-medium", "r-opus-medium"]:
        v = [c for c in clean if c["lane"] == lane]
        blocks = [c for c in v if c["outcome"] != "landed"]
        wrong = [c for c in v if c["passed"] is not True]
        say(f"| {names[lane]} | {len(v)} | {planned[lane]} | {len(blocks)} | {len(wrong)} | "
            f"{median([c['wall'] for c in v]):,.0f} | {median([c['requests'] for c in v]):g} |")
    say()
    if "--write" in sys.argv:
        open(os.path.join(HERE, "results.txt"), "w").write("\n".join(OUT) + "\n")


main()
