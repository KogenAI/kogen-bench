# python3 -I report.py .   prints the per-cell table and the counts of README.md from data/cells.json
import json, sys, os
rows = json.load(open(os.path.join(sys.argv[1] if len(sys.argv) > 1 else ".", "data", "cells.json")))
print("| task | arm | outcome | attempts | refusals (gate: problem lines) | assumption / evidence markers in the final Intent | wall s | cost USD |")
print("|---|---|---|---|---|---|---|---|")
for r in rows:
    ref = ", ".join(f"{x['attempt']}: {x['gate']} {x['problem_lines']}" for x in r["refusals"]) or "none"
    fi = r["final_intent"]
    print(f"| {r['task']} | {r['arm']} | {r['outcome']} | {r['attempts_used']} | {ref} | {fi['assumption_markers']} / {fi['evidence_markers']} | {r['wall_s']} | {r['cost_usd_list_equivalent']:.2f} |")
for arm in ("A", "B"):
    c = [r for r in rows if r["arm"] == arm]
    print(f"\narm {arm}: cells {len(c)}, reached readiness {sum(r['outcome'] == 'reached readiness' for r in c)}, "
          f"first-attempt pass {sum(r['first_attempt_pass'] for r in c)}, problem lines {sum(x['problem_lines'] for r in c for x in r['refusals'])}, "
          f"cost USD {sum(r['cost_usd_list_equivalent'] for r in c):.2f}")
