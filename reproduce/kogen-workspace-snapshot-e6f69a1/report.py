#!/usr/bin/env python3
"""report.py <pairs.tsv>: counters, per-task paired outcomes, build requests, orientation before the first edit, tokens, wall and attribution for the Kogen workspace-snapshot check (standard library only)."""
import csv, sys, collections, math, statistics
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
n = len(rows)
S = lambda k, rs=None: sum(float(r[k]) for r in (rows if rs is None else rs))
def sign(w, l):
    m = w + l
    if m == 0: return 1.0
    return min(1.0, 2 * sum(math.comb(m, i) for i in range(min(w, l) + 1)) / 2 ** m)
w = sum(r["change"] == "win" for r in rows); l = sum(r["change"] == "loss" for r in rows)
print(f"pairs {n} in {len({r['run'] for r in rows})} runs, {len({r['task'] for r in rows})} tasks")
print(f"hidden pass: g0 {int(S('g0_hidden'))}/{n}, g1 {int(S('g1_hidden'))}/{n}; wins {w} losses {l} net {w-l}; discordant {w+l}; exact two-sided sign p {sign(w,l):.2f}")
print("g0 outcomes:", dict(sorted(collections.Counter(r["g0_outcome"] for r in rows).items())))
print("g1 outcomes:", dict(sorted(collections.Counter(r["g1_outcome"] for r in rows).items())))
print("valid Intent: g0", int(S("g0_intent_valid")), "g1", int(S("g1_intent_valid")))
print("acceptance separating correct from incorrect: g0", int(S("g0_acc_sep")), "g1", int(S("g1_acc_sep")))
print("acceptance contradicted by the builder: g0", int(S("g0_contradiction")), "g1", int(S("g1_contradiction")))
print(f"requests per cell (all stages): g0 {S('g0_requests')/n:.2f} g1 {S('g1_requests')/n:.2f}")
lo = sum(int(r["g1_build_req"]) < int(r["g0_build_req"]) for r in rows); hi = sum(int(r["g1_build_req"]) > int(r["g0_build_req"]) for r in rows)
print(f"build requests per cell: g0 {S('g0_build_req')/n:.2f} g1 {S('g1_build_req')/n:.2f} (total {int(S('g0_build_req'))} vs {int(S('g1_build_req'))}); g1 lower in {lo} pairs, higher in {hi}, equal in {n-lo-hi}; sign p {sign(lo,hi):.4f}")
bl = [r for r in rows if r["g0_outcome"] == "landed" and r["g1_outcome"] == "landed"]
print(f"build requests per cell, {len(bl)} pairs landed on both sides: g0 {S('g0_build_req',bl)/len(bl):.2f} g1 {S('g1_build_req',bl)/len(bl):.2f}")
for t in (300, 500, 1000):
    a, b = int(S(f"g0_orient{t}")), int(S(f"g1_orient{t}"))
    print(f"orientation requests before the first edit (edit = write_file or a shell call with arguments >= {t} bytes): g0 {a} g1 {b} (fall {100*(1-b/a):.1f}%)")
print(f"request-1 input tokens: g0 {S('g0_req1_input')/n:.0f} g1 {S('g1_req1_input')/n:.0f}; g1 larger in {sum(int(r['g1_req1_input'])>int(r['g0_req1_input']) for r in rows)} of {n} pairs")
t0, t1 = S("g0_tokens"), S("g1_tokens")
print(f"tokens per cell (input + output, all stages): g0 {t0/n:.0f} g1 {t1/n:.0f} ({100*(t1/t0-1):+.2f}%); pairs landed on both sides {len(bl)}: {100*(S('g1_tokens',bl)/S('g0_tokens',bl)-1):+.2f}%")
print(f"pooled agent wall per cell (all stages, failed attempts included): g0 {S('g0_wall_s')/n:.1f} s g1 {S('g1_wall_s')/n:.1f} s; median g0 {statistics.median(float(r['g0_wall_s']) for r in rows):.1f} g1 {statistics.median(float(r['g1_wall_s']) for r in rows):.1f}; landed on both sides: g0 {S('g0_wall_s',bl)/len(bl):.1f} g1 {S('g1_wall_s',bl)/len(bl):.1f}")
print("\nPer task (6 pairs each): valid Intent g0/g1, acceptance separating g0/g1, hidden pass g0/g1, wins, losses, build requests per cell g0/g1")
for t in sorted({r["task"] for r in rows}):
    rs = [r for r in rows if r["task"] == t]
    s = lambda k: sum(int(r[k]) for r in rs)
    print(f"{t}\t{s('g0_intent_valid')}/{s('g1_intent_valid')}\t{s('g0_acc_sep')}/{s('g1_acc_sep')}\t{s('g0_hidden')}/{s('g1_hidden')}\t{sum(r['change']=='win' for r in rs)}\t{sum(r['change']=='loss' for r in rs)}\t{s('g0_build_req')/len(rs):.2f}/{s('g1_build_req')/len(rs):.2f}")
print("\nAttribution of discordant pairs (a = builder stage, the patched stage: both cells landed and the cell that failed a hidden test had the failing behaviour in its own Intent; b = shape-time acceptance defect, a different Intent, builder blocked in one arm; c = review; d = infrastructure; e = unclear)")
print("class\twins\tlosses")
for c in "abcde":
    rs = [r for r in rows if r["class"] == c]
    print(f"{c}\t{sum(r['change']=='win' for r in rs)}\t{sum(r['change']=='loss' for r in rs)}")
print("\nrun\ttask\tg0\tg1\tchange\tclass")
for r in rows:
    if r["change"]: print(f"{r['run']}\t{r['task']}\t{r['g0_hidden']}\t{r['g1_hidden']}\t{r['change']}\t{r['class']}")
