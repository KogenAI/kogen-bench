#!/usr/bin/env python3
"""report.py <pairs.tsv>: rebuilds every count of the Kogen shaping data-stores adoption screen (standard library only)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
clean = [r for r in rows if r["pair_status"] == "clean"]
void = [r for r in rows if r["pair_status"] != "clean"]
v = lambda r, k: int(r[k])
print(f"pair rows {len(rows)} (clean {len(clean)}, void {len(void)}: gate timeout, one rerun also void)")
print(f"valid Intent over clean pairs: g0 {sum(v(r,'g0_valid_intent') for r in clean)}/{len(clean)}, g1 {sum(v(r,'g1_valid_intent') for r in clean)}/{len(clean)}")
for arm in ("g0", "g1"):
    c = collections.Counter(r[f"{arm}_class"] for r in clean)
    print(f"{arm} classes (clean pairs): " + ", ".join(f"{k} {n}" for k, n in sorted(c.items())))
tg = [r for r in clean if r["role"] == "target"]; gd = [r for r in clean if r["role"] == "guard"]
print(f"target clean pairs {len(tg)}: valid Intent g0 {sum(v(r,'g0_valid_intent') for r in tg)}, g1 {sum(v(r,'g1_valid_intent') for r in tg)}")
print(f"guard clean pairs {len(gd)}: valid Intent g0 {sum(v(r,'g0_valid_intent') for r in gd)}, g1 {sum(v(r,'g1_valid_intent') for r in gd)}")
ap = lambda r, a: r[f"{a}_hidden_passed"].isdigit() and r["hidden_expected"].isdigit() and int(r[f"{a}_hidden_passed"]) == int(r["hidden_expected"])
print(f"hidden all-pass, target clean pairs: g0 {sum(ap(r,'g0') for r in tg)}, g1 {sum(ap(r,'g1') for r in tg)}; guards: g0 {sum(ap(r,'g0') for r in gd)}, g1 {sum(ap(r,'g1') for r in gd)}")
sn = lambda r, a: r[f"{a}_stores_named"] not in ("NA", "0")
print(f"stores named in a saved Intent (all pair rows): g0 {sum(sn(r,'g0') for r in rows)}, g1 {sum(sn(r,'g1') for r in rows)} (g1 only in the void pair's saved Intents)")
print("input tokens (all pair rows): g0 %d, g1 %d; output: g0 %d, g1 %d" % tuple(sum(int(r[k]) for r in rows) for k in ("g0_input_tokens", "g1_input_tokens", "g0_output_tokens", "g1_output_tokens")))
print("\nPer pair: pair task status g0_outcome g1_outcome g0_hidden/expected g1_hidden/expected")
for r in rows:
    print(f"{r['pair']}\t{r['task']}\t{r['pair_status']}\t{r['g0_outcome']}\t{r['g1_outcome']}\t{r['g0_hidden_passed']}/{r['hidden_expected']}\t{r['g1_hidden_passed']}/{r['hidden_expected']}")
gap = sum(v(r, "g0_valid_intent") for r in clean) - sum(v(r, "g1_valid_intent") for r in clean)
g1only = collections.Counter(r["g1_class"] for r in clean) - collections.Counter(r["g0_class"] for r in clean)
g0cls = {r["g0_class"] for r in clean}
only = {k: n for k, n in collections.Counter(r["g1_class"] for r in clean).items() if k not in g0cls and n >= 2}
print(f"\nRegistered rule: WORSE if g0 valid Intents exceed g1 by >= 2 pairs (gap {gap}) or a refusal class seen only in g1 in >= 2 clean cells ({only or 'none'}).")
print("Rule outcome: " + ("WORSE" if gap >= 2 or only else "not worse by the rule"))
