"""Tables for hk2-hard-set-grading-correction. Standard library only.
Usage: python3 -I analyze.py data
"""
import csv, sys, collections

d = sys.argv[1]
rd = lambda n: list(csv.DictReader(open(f"{d}/{n}")))

print("1. Codex-high records published in hk2-hard-set for the three scenario tasks (passes / attempts, by venue)")
rec = rd("hk2-records-affected-tasks.csv")
by = collections.defaultdict(lambda: collections.Counter())
for r in rec:
    k = (r["task"], r["venue"])
    by[k]["n"] += 1
    by[k]["p"] += r["passed"] == "True"
tasks = sorted({r["task"] for r in rec})
for t in tasks:
    tot = sum(by[(t, v)]["n"] for v in ("mb", "st"))
    ps = sum(by[(t, v)]["p"] for v in ("mb", "st"))
    print(f"   {t}: {ps}/{tot} (Mac laptop {by[(t,'mb')]['p']}/{by[(t,'mb')]['n']}, desktop Mac {by[(t,'st')]['p']}/{by[(t,'st')]['n']})")

print("2. Desktop Mac round h2h-22, stored grades read from the run folders: cells whose acceptance ids were all missing")
cells = rd("missing-acceptance-cells.csv")
agg = collections.defaultdict(lambda: collections.Counter())
for c in cells:
    a = agg[c["task"]]
    a["cells"] += 1
    exp = int(c["acceptance_expected"]); miss = int(c["acceptance_missing"])
    a["all_missing"] += exp > 0 and miss == exp
    a["acc_ids"] += exp
    a["acc_missing"] += miss
    a["other_exp"] += int(c["other_expected"])
    a["other_pass"] += int(c["other_passed"])
    a["passed"] += int(c["all_passed"])
for t in sorted(agg):
    a = agg[t]
    print(f"   {t}: {a['cells']} cells, {a['all_missing']} with every acceptance id missing "
          f"({a['acc_missing']} of {a['acc_ids']} ids), other ids passed {a['other_pass']}/{a['other_exp']}, graded pass {a['passed']}")
tot_cells = sum(1 for c in cells if int(c["acceptance_expected"]) and c["acceptance_missing"] == c["acceptance_expected"])
print(f"   total: {tot_cells} of {len(cells)} cells with every acceptance id missing (arms: codex, two kogen-loop variants)")
codex_cells = [c for c in cells if c["arm"].startswith("codex") and int(c["acceptance_expected"]) and c["acceptance_missing"] == c["acceptance_expected"]]
print(f"   of those, Codex cells: {len(codex_cells)}")

print("3. Codex alone, same tasks, graded again with the repaired grader (hk3-lm, hk3-mb)")
for r in rd("regrade-codex-alone.csv"):
    print(f"   {r['cohort']} {r['task']}: pass {r['old_passed']} -> {r['new_passed']}, tests {r['old_tests']} -> {r['new_tests']}, acceptance missing after {r['acceptance_missing_after']}")
