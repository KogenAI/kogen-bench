#!/usr/bin/env python3
"""report.py <pairs.tsv>: counters and attribution table for the Kogen release check (standard library only)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
n = len(rows)
h0 = sum(int(r["base_hidden_pass"]) for r in rows); h1 = sum(int(r["release_hidden_pass"]) for r in rows)
w = sum(r["change"] == "win" for r in rows); l = sum(r["change"] == "loss" for r in rows)
print(f"pairs {n} in {len({r['run'] for r in rows})} runs, {len({r['task'] for r in rows})} tasks")
print(f"hidden pass: base {h0}/{n}, release {h1}/{n}; wins {w} losses {l} net {w-l}; discordant {w+l}")
print("base outcomes:", dict(sorted(collections.Counter(r["base_outcome"] for r in rows).items())))
print("release outcomes:", dict(sorted(collections.Counter(r["release_outcome"] for r in rows).items())))
print("\nAttribution of discordant pairs (class a = base ended at the example check removed by 093ff1f; a-partial = it consumed shaping attempts; unattributed = no listed fix maps)")
print("fix\tclass\twins\tlosses")
for k in sorted({(r["fix"], r["class"]) for r in rows if r["class"]}):
    rs = [r for r in rows if (r["fix"], r["class"]) == k]
    print(f"{k[0]}\t{k[1]}\t{sum(r['change']=='win' for r in rs)}\t{sum(r['change']=='loss' for r in rs)}")
print("08ae506, e6f69a1, 7e1b082, 3ea2e23, e7d7d73, 24a5a17: 0 pairs")
print("\nrun\ttask\tbase\trelease\tchange\tfix\tclass")
for r in rows:
    if r["change"]: print(f"{r['run']}\t{r['task']}\t{r['base_hidden_pass']}\t{r['release_hidden_pass']}\t{r['change']}\t{r['fix']}\t{r['class']}")
