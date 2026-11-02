#!/usr/bin/env python3
"""report.py <pairs.tsv>: counters, per-task paired outcomes, requests, fetch-only requests, wall and attribution for the Kogen bounded-shell-wait check (standard library only)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
n = len(rows)
S = lambda k: sum(float(r[k]) for r in rows)
w = sum(r["change"] == "win" for r in rows); l = sum(r["change"] == "loss" for r in rows)
print(f"pairs {n} in {len({r['run'] for r in rows})} runs, {len({r['task'] for r in rows})} tasks")
print(f"hidden pass: g0 {int(S('g0_hidden_pass'))}/{n}, g1 {int(S('g1_hidden_pass'))}/{n}; wins {w} losses {l} net {w-l}; discordant {w+l}")
print("g0 outcomes:", dict(sorted(collections.Counter(r["g0_outcome"] for r in rows).items())))
print("g1 outcomes:", dict(sorted(collections.Counter(r["g1_outcome"] for r in rows).items())))
print("valid Intent: g0", int(S("g0_intent_valid")), "g1", int(S("g1_intent_valid")))
print("acceptance separating correct from incorrect: g0", int(S("g0_acc_separating")), "g1", int(S("g1_acc_separating")))
print("acceptance contradicted by the builder: g0", int(S("g0_acc_contradicted")), "g1", int(S("g1_acc_contradicted")))
print(f"requests per cell (all stages): g0 {S('g0_requests')/n:.2f} g1 {S('g1_requests')/n:.2f}; build+review: g0 {S('g0_build_review_requests')/n:.2f} g1 {S('g1_build_review_requests')/n:.2f}")
print(f"fetch-only requests: g0 {int(S('g0_fetch_only'))} ({S('g0_fetch_only')/n:.3f} per cell) g1 {int(S('g1_fetch_only'))}")
print(f"pooled agent wall per cell (all stages, failed attempts included): g0 {S('g0_wall_s')/n:.1f} s g1 {S('g1_wall_s')/n:.1f} s")
print("pairs where the lever fired in either cell (a handle fetch, or a command over 2 s that returned in its own response):", sum(int(r["lever_fired"]) for r in rows))
print("\nPer task (6 pairs each): valid Intent g0/g1, acceptance separating g0/g1, hidden pass g0/g1, wins, losses")
for t in sorted({r["task"] for r in rows}):
    rs = [r for r in rows if r["task"] == t]
    s = lambda k: sum(int(r[k]) for r in rs)
    print(f"{t}\t{s('g0_intent_valid')}/{s('g1_intent_valid')}\t{s('g0_acc_separating')}/{s('g1_acc_separating')}\t{s('g0_hidden_pass')}/{s('g1_hidden_pass')}\t{sum(r['change']=='win' for r in rs)}\t{sum(r['change']=='loss' for r in rs)}")
print("\nAttribution of discordant pairs (a = the loop behaviour changed by the patch: a handle fetch or a longer in-response command in the differing cells; b = shape-time acceptance defect, a different Intent drawn, builder blocked in one arm; c = review; d = infrastructure; e = landed in both, one hidden test flipped)")
print("class\twins\tlosses")
for c in "abcde":
    rs = [r for r in rows if r["class"] == c]
    print(f"{c}\t{sum(r['change']=='win' for r in rs)}\t{sum(r['change']=='loss' for r in rs)}")
print("\nrun\ttask\tg0\tg1\tchange\tclass")
for r in rows:
    if r["change"]: print(f"{r['run']}\t{r['task']}\t{r['g0_hidden_pass']}\t{r['g1_hidden_pass']}\t{r['change']}\t{r['class']}")
