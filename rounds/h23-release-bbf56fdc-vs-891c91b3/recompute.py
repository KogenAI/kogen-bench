#!/usr/bin/env python3
"""Recompute descriptive historical fractions; no model calls or third-party packages."""
import json, math
from pathlib import Path
d=json.loads(Path(__file__).with_name("cells.json").read_text())
assert len(d["cells"]) == d["planned_slots"] == 18
assert len({(r["arm"],r["task"],r["rep"]) for r in d["cells"]}) == 18
assert {r["rep"] for r in d["cells"]} == {1,2,3}
means={}
for arm, expected in d["expected_task_means"].items():
 means[arm]={}
 for task, want in expected.items():
  rows=[r for r in d["cells"] if r["arm"]==arm and r["task"]==task]
  assert len(rows)==3, (arm,task,len(rows))
  fractions=[r["score"]/r["total"] if r["score"] is not None and r["total"] else 0 for r in rows]
  got=sum(fractions)/len(fractions)
  assert math.isclose(got,want,rel_tol=1e-12,abs_tol=1e-12),(arm,task,got,want)
  means[arm][task]=got
print(json.dumps({"task_means":means,"original_decision":d["original_decision"],"causal_comparison":False},indent=2,sort_keys=True))
