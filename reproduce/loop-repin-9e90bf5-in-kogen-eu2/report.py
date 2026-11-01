#!/usr/bin/env python3
"""report.py <pairs.tsv>: counters and attribution table for the kogen-loop re-pin screen (standard library only)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
I = lambda r, k: int(r[k])
n = len(rows)
print(f"pairs {n} in {len({r['run'] for r in rows})} runs, {len({r['task'] for r in rows})} tasks")
h0 = sum(I(r, "g0_hidden_pass") for r in rows); h1 = sum(I(r, "g1_hidden_pass") for r in rows)
w = sum(r["hidden_change"] == "win" for r in rows); l = sum(r["hidden_change"] == "loss" for r in rows)
print(f"hidden pass: base {h0}/{n}, lever {h1}/{n}; wins {w} losses {l} net {w-l}; discordant {w+l} ({100*(w+l)/n:.0f}% of pairs)")
print("base outcomes:", dict(sorted(collections.Counter(r["g0_outcome"] for r in rows).items())))
print("lever outcomes:", dict(sorted(collections.Counter(r["g1_outcome"] for r in rows).items())))
for a in ("g0", "g1"):
    L = [r for r in rows if I(r, a + "_has_log")]
    ref = sum(I(r, a + "_empty_handle_refusals") for r in L); cells = sum(1 for r in L if I(r, a + "_empty_handle_refusals"))
    print(f"{'base' if a=='g0' else 'lever'}: cells with a build log {len(L)}; empty-handle refusals {ref} in {cells} cells; polls {sum(I(r, a+'_polls') for r in L)}; build requests {sum(I(r, a+'_build_requests') for r in L)}; stage ends from network outages {sum(I(r, a+'_net_end') for r in rows)}")
print(f"requests over all stages: base {sum(I(r,'g0_total_requests') for r in rows)}, lever {sum(I(r,'g1_total_requests') for r in rows)}; wall s (descriptive, runs overlapped other work): base {sum(I(r,'g0_wall_s') for r in rows)}, lever {sum(I(r,'g1_wall_s') for r in rows)}")
print("\nDiscordant pairs by class (a = a loop-side event in the patched stage caused the flip; b = shape/approve cause; e = no stage cause shown, build or hidden-test variance)")
print("class\tpairs\twins\tlosses")
for c in "abcde":
    rs = [r for r in rows if r["class"] == c]
    if rs: print(f"{c}\t{len(rs)}\t{sum(r['hidden_change']=='win' for r in rs)}\t{sum(r['hidden_change']=='loss' for r in rs)}")
print("class a proven: 0 pairs")
e = [r for r in rows if r["class"] == "e"]
ew = [r for r in e if r["hidden_change"] == "win" and I(r, "g0_empty_handle_refusals") > 0]
print(f"class e pairs {len(e)}: {len(ew)} wins where the base cell had an empty-handle refusal in its build (possible class a, not provable: tool arguments are hashed); losses {sum(r['hidden_change']=='loss' for r in e)} with no loop event")
print("\nrun\ttask\tbase hidden\tlever hidden\tclass")
for r in rows:
    if r["class"]: print(f"{r['run']}\t{r['task']}\t{r['g0_hidden_pass']}\t{r['g1_hidden_pass']}\t{r['class']}")
