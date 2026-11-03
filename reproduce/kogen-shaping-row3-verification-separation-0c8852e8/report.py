#!/usr/bin/env python3
"""report.py <shaping_row3_pairs.tsv>: rebuilds every count of the Kogen shaping property-acceptance screen (standard library only)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
n = len(rows); v = lambda r, k: int(r[k])
pr = [r for r in rows if r["role"] == "property"]; gd = [r for r in rows if r["role"] == "guard"]
print(f"pairs {n} (property tasks {len(pr)}, guard tasks {len(gd)}), cells {2*n}")
print(f"valid Intent: g0 {sum(v(r,'g0_valid_intent') for r in rows)}/{n}, g1 {sum(v(r,'g1_valid_intent') for r in rows)}/{n}")
print(f"  property tasks: g0 {sum(v(r,'g0_valid_intent') for r in pr)}/{len(pr)}, g1 {sum(v(r,'g1_valid_intent') for r in pr)}/{len(pr)}")
print(f"  guard tasks: g0 {sum(v(r,'g0_valid_intent') for r in gd)}/{len(gd)}, g1 {sum(v(r,'g1_valid_intent') for r in gd)}/{len(gd)}")
for arm in ("g0", "g1"):
    c = collections.Counter(r[f"{arm}_outcome"] for r in rows)
    print(f"{arm} outcomes: " + ", ".join(f"{k} {m}" for k, m in sorted(c.items())))
def allpass(r, a):
    h = r[f"{a}_hidden_passed"]; return h.isdigit() and int(h) == int(r["hidden_expected"])
na = lambda a: sum(r[f"{a}_hidden_passed"] == "NA" for r in rows)
print(f"hidden all-pass: g0 {sum(allpass(r,'g0') for r in rows)}, g1 {sum(allpass(r,'g1') for r in rows)}; hidden not graded (kept tree missing): g0 {na('g0')}, g1 {na('g1')}")
print(f"landed builds: g0 {sum(r['g0_outcome']=='landed build' for r in rows)}, g1 {sum(r['g1_outcome']=='landed build' for r in rows)}")
disc = [r for r in rows if r["g0_valid_intent"] != r["g1_valid_intent"]]
print(f"pairs discordant on valid Intent: {len(disc)} (g0 valid only: {sum(v(r,'g0_valid_intent')>v(r,'g1_valid_intent') for r in disc)}, g1 valid only: {sum(v(r,'g1_valid_intent')>v(r,'g0_valid_intent') for r in disc)})")
print("tokens: input g0 %d, g1 %d; output g0 %d, g1 %d; summed wall s g0 %d, g1 %d" % tuple(sum(int(r[k]) for r in rows) for k in ("g0_input_tokens","g1_input_tokens","g0_output_tokens","g1_output_tokens","g0_wall_s","g1_wall_s")))
print("\nPer pair: pair task rep g0_outcome | g1_outcome | g0_hidden/expected g1_hidden/expected")
for r in rows:
    print(f"{r['pair']}\t{r['task']}\t{r['rep']}\t{r['g0_outcome']} | {r['g1_outcome']} | {r['g0_hidden_passed']}/{r['hidden_expected']} {r['g1_hidden_passed']}/{r['hidden_expected']}")
better = sum(v(r,'g1_valid_intent') for r in pr) > sum(v(r,'g0_valid_intent') for r in pr) and sum(v(r,'g1_valid_intent') for r in gd) >= sum(v(r,'g0_valid_intent') for r in gd)
print("\nRegistered reading: better would need a protected property acceptance saved on property tasks and no guard losing valid Intent. Property valid Intent gain: %s; guard valid Intent change: %+d. Reading: %s" % ("none" if sum(v(r,'g1_valid_intent') for r in pr) <= sum(v(r,'g0_valid_intent') for r in pr) else "yes", sum(v(r,'g1_valid_intent') for r in gd)-sum(v(r,'g0_valid_intent') for r in gd), "better" if better else "not better"))
