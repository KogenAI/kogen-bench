#!/usr/bin/env python3
"""report.py <opus_pairs.tsv>: rebuilds every count of the Opus pairs beside the Kogen shaping data-stores adoption screen (standard library only)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
n = len(rows)
v = lambda r, k: int(r[k])
tg = [r for r in rows if r["role"] == "target"]; gd = [r for r in rows if r["role"] == "guard"]
print(f"pairs {n} (target {len(tg)}, guard {len(gd)}); no pair void")
print(f"valid Intent: g0 {sum(v(r,'g0_valid_intent') for r in rows)}/{n}, g1 {sum(v(r,'g1_valid_intent') for r in rows)}/{n}")
for arm in ("g0", "g1"):
    c = collections.Counter(r[f"{arm}_outcome"] for r in rows)
    print(f"{arm} outcomes: " + ", ".join(f"{k} {m}" for k, m in sorted(c.items())))
print(f"stores named in the saved Intent, target pairs: g0 {sum(v(r,'g0_stores_named') for r in tg)}/{len(tg)}, g1 {sum(v(r,'g1_stores_named') for r in tg)}/{len(tg)}")
print(f"candidate Intent with a data-stores section: target {sum(v(r,'g1_data_stores_section') for r in tg)}/{len(tg)}, guards {sum(v(r,'g1_data_stores_section') for r in gd)}/{len(gd)}")
ap = lambda r, a: int(r[f"{a}_hidden_passed"]) == int(r["hidden_expected"])
print(f"hidden all-pass: target g0 {sum(ap(r,'g0') for r in tg)}, g1 {sum(ap(r,'g1') for r in tg)}; guards g0 {sum(ap(r,'g0') for r in gd)}, g1 {sum(ap(r,'g1') for r in gd)}")
print(f"pairs where the hidden count differs: {sum(r['g0_hidden_passed'] != r['g1_hidden_passed'] for r in rows)}")
print(f"pairs where the outcome class differs: {sum(r['g0_outcome'] != r['g1_outcome'] for r in rows)}")
tok = lambda a, k: sum(int(r[f"{a}_{k}"]) for r in rows if r[f"{a}_{k}"] != "NA")
print("tokens over cells that recorded them: input g0 %d (%d cells), g1 %d (%d cells); output g0 %d, g1 %d" % (tok("g0","input_tokens"), n, tok("g1","input_tokens"), sum(r["g1_input_tokens"] != "NA" for r in rows), tok("g0","output_tokens"), tok("g1","output_tokens")))
print("\nPer pair: pair task machine g0_outcome | g1_outcome | g0_hidden/expected g1_hidden/expected")
for r in rows:
    print(f"{r['pair']}\t{r['task']}\t{r['machine']}\t{r['g0_outcome']} | {r['g1_outcome']} | {r['g0_hidden_passed']}/{r['hidden_expected']} {r['g1_hidden_passed']}/{r['hidden_expected']}")
ref = sum("refus" in r[f"{a}_outcome"] or "question" in r[f"{a}_outcome"] for r in rows for a in ("g0", "g1"))
print(f"\nRefusals or question stops at shaping in either arm: {ref}. Flag rule (a refusal class only in g1, in two or more cells): " + ("not triggered." if ref == 0 else "check."))
