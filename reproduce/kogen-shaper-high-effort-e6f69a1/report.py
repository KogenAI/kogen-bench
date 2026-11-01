#!/usr/bin/env python3
"""report.py <pairs.tsv>: counters, per-task paired outcomes and attribution for the Kogen shaper-effort check (standard library only)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
n = len(rows)
h0 = sum(int(r["medium_hidden_pass"]) for r in rows); h1 = sum(int(r["high_hidden_pass"]) for r in rows)
w = sum(r["change"] == "win" for r in rows); l = sum(r["change"] == "loss" for r in rows)
print(f"pairs {n} in {len({r['run'] for r in rows})} runs, {len({r['task'] for r in rows})} tasks")
print(f"hidden pass: medium {h0}/{n}, high {h1}/{n}; wins {w} losses {l} net {w-l}; discordant {w+l}")
print("medium outcomes:", dict(sorted(collections.Counter(r["medium_outcome"] for r in rows).items())))
print("high outcomes:", dict(sorted(collections.Counter(r["high_outcome"] for r in rows).items())))
print("valid Intent (shape and approval passed): medium", sum(int(r["medium_intent_valid"]) for r in rows), "high", sum(int(r["high_intent_valid"]) for r in rows))
print("acceptance contradicted by the builder: medium", sum(int(r["medium_acceptance_contradicted"]) for r in rows), "high", sum(int(r["high_acceptance_contradicted"]) for r in rows))
print("\nPer task (6 pairs each): valid Intent m/h, acceptance contradicted m/h, hidden pass m/h, wins, losses")
for t in sorted({r["task"] for r in rows}):
    rs = [r for r in rows if r["task"] == t]
    s = lambda k: sum(int(r[k]) for r in rs)
    print(f"{t}\t{s('medium_intent_valid')}/{s('high_intent_valid')}\t{s('medium_acceptance_contradicted')}/{s('high_acceptance_contradicted')}\t{s('medium_hidden_pass')}/{s('high_hidden_pass')}\t{sum(r['change']=='win' for r in rs)}\t{sum(r['change']=='loss' for r in rs)}")
print("\nAttribution of discordant pairs (class a = the shaping stage differed: acceptance written at shaping was contradicted or refused downstream in one arm only; e = both arms shaped and landed, one hidden test flipped, no shaping difference shown; b, c, d = 0)")
print("class\twins\tlosses")
for c in sorted({r["class"] for r in rows if r["class"]}):
    rs = [r for r in rows if r["class"] == c]
    print(f"{c}\t{sum(r['change']=='win' for r in rs)}\t{sum(r['change']=='loss' for r in rs)}")
print("\nrun\ttask\tmedium\thigh\tchange\tclass")
for r in rows:
    if r["change"]: print(f"{r['run']}\t{r['task']}\t{r['medium_hidden_pass']}\t{r['high_hidden_pass']}\t{r['change']}\t{r['class']}")
