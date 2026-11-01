#!/usr/bin/env python3
"""report.py <pairs.tsv>: counters and attribution table for the shape example-check screen (standard library only)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
T = lambda v: v == "True"
n = len(rows)
c0 = sum(T(r["g0_contradiction"]) for r in rows); c1 = sum(T(r["g1_contradiction"]) for r in rows)
h0 = sum(T(r["g0_hidden_pass"]) for r in rows); h1 = sum(T(r["g1_hidden_pass"]) for r in rows)
w = sum(r["hidden_change"] == "win" for r in rows); l = sum(r["hidden_change"] == "loss" for r in rows)
print(f"pairs {n} in {len({r['run'] for r in rows})} runs, {len({r['task'] for r in rows})} tasks")
print(f"contradiction cells: base {c0}, lever {c1}")
print(f"hidden pass: base {h0}/{n}, lever {h1}/{n}; wins {w} losses {l} net {w-l}")
def refused(r): return r["g1_outcome"] in ("refused", "questions_pending")
print(f"lever shaping ended refused/questions: {sum(refused(r) for r in rows)} of {n}; base: {sum(r['g0_outcome'] in ('refused','questions_pending') for r in rows)}")
print("lever outcomes:", dict(sorted(collections.Counter(r["g1_outcome"] for r in rows).items())))
print("base outcomes:", dict(sorted(collections.Counter(r["g0_outcome"] for r in rows).items())))
print("\nDiscordant pairs by class (a = example-check refusal ended shaping; b = other shape-stage cause; e = no stage cause, build/hidden variance or no lever event)")
print("class\tpairs\twins\tlosses\thidden-unchanged")
for c in "abcde":
    rs = [r for r in rows if r["class"] == c]
    if rs: print(f"{c}\t{len(rs)}\t{sum(r['hidden_change']=='win' for r in rs)}\t{sum(r['hidden_change']=='loss' for r in rs)}\t{sum(r['hidden_change']=='same' for r in rs)}")
a = [r for r in rows if r["class"] == "a"]
print(f"\nclass a: {len(a)} pairs, {sum(r['hidden_change']=='loss' for r in a)} hidden losses, 0 wins")
g0c = [r for r in rows if T(r["g0_contradiction"])]
print(f"base contradiction cells {len(g0c)}: lever landed {sum(r['g1_outcome']=='landed' for r in g0c)} (example-check refusals in those cells {sum(int(r['g1_example_check_refusals']) for r in g0c if r['g1_outcome']=='landed')}), refused/questions {sum(refused(r) for r in g0c)}, still contradiction {sum(T(r['g1_contradiction']) for r in g0c)}")
print("\nrun\ttask\tbase hidden\tlever hidden\tclass")
for r in rows:
    if r["class"]: print(f"{r['run']}\t{r['task']}\t{r['g0_hidden_pass']}\t{r['g1_hidden_pass']}\t{r['class']}")
