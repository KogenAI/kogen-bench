# python3 -I report.py .   prints the tables of README.md from data/cells.json and data/stage1-comparators.json
import json, os, sys
d = sys.argv[1] if len(sys.argv) > 1 else "."
cells = json.load(open(os.path.join(d, "data", "cells.json")))
s1 = json.load(open(os.path.join(d, "data", "stage1-comparators.json")))
print("| task | arm | rep | outcome | submissions | refusals (attempt: gate lines, class) | first shaper round s (share of 1800 s) | gate checks s | tool calls | wall s | cost USD |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for c in cells:
    ref = ", ".join(f"{r['attempt']}: {r['gate']} {r['problem_lines']} ({r['cause']})" for r in c["refusals"]) or "none"
    cost = "not recorded" if c["cost_usd_list_equivalent"] is None else f"{c['cost_usd_list_equivalent']:.2f}"
    print(f"| {c['task']} | {c['arm']} | {c['rep']} | {c['outcome']} | {c['submissions']} | {ref} | {c['first_shaper_round_s']} ({c['first_round_share_of_deadline']:.0%}) | {c['gate_checks_ms']/1000:.0f} | {c['shaper_tool_calls']} | {c['wall_s']} | {cost} |")
print()
for arm in ("B2", "B2b"):
    r = [c for c in cells if c["arm"] == arm]
    print(f"arm {arm}: cells {len(r)}, reached readiness {sum(c['reached_readiness'] for c in r)}, ended at the deadline {sum(c['outcome'] == 'deadline' for c in r)}, "
          f"refusals {sum(len(c['refusals']) for c in r)}, cost USD {sum(c['cost_usd_list_equivalent'] or 0 for c in r):.2f} (cells with a record)")
print("\nStage 1, arm B (patches B1-B3 and P) and the release, same tasks, same deadline:")
print("| task | arm | outcome | first shaper round s | tool calls | wall s |")
print("|---|---|---|---|---|---|")
for c in sorted(s1, key=lambda x: (x["task"], x["arm"])):
    print(f"| {c['task']} | {c['arm']} | {c['outcome']} | {c['first_shaper_round_s']} | {c['shaper_tool_calls']} | {c['wall_s']} |")
