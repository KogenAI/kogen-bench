#!/usr/bin/env python3
"""report.py <aor_control_573d023_cells.tsv>: rebuilds every count of the adopted-release control block (standard library only)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
v = lambda r, k: int(r[k])
def line(name, rs):
    c = collections.Counter(r["outcome"] for r in rs)
    print(f"{name}: cells {len(rs)}, valid Intent {sum(v(r,'valid_intent') for r in rs)}, reached build {sum(v(r,'reached_build') for r in rs)}, landed {sum(v(r,'landed') for r in rs)}, hidden all-pass {sum(v(r,'hidden_all_pass') for r in rs)}")
    print("  outcomes: " + ", ".join(f"{k} {n}" for k, n in sorted(c.items())))
    print("  tokens: input %d, output %d, summed wall s %d" % tuple(sum(int(r[k]) for r in rs) for k in ("input_tokens", "output_tokens", "wall_s")))
line("Mac block", [r for r in rows if r["block"] == "Mac"])
line("Linux block", [r for r in rows if r["block"] == "Linux"])
line("both blocks", rows)
print("\nPer task: task block outcome hidden/expected")
for r in sorted(rows, key=lambda r: (r["task"], r["block"])):
    print(f"{r['task']}\t{r['block']}\t{r['outcome']}\t{r['hidden_passed']}/{r['hidden_expected']}")
print("\nFirst mistake (stage) per cell:")
c = collections.Counter(r["first_mistake"].split(":")[0] for r in rows if not r["first_mistake"].startswith("build landed"))
print(", ".join(f"{k} {n}" for k, n in sorted(c.items())) + "; landed with missing requested checks: %d" % sum(r["first_mistake"].startswith("build landed") for r in rows))
