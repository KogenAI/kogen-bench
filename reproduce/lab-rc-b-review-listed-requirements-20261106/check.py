"""Recompute replay.json and the table from data/ and check the registered rule.

usage: python3 -I check.py
Reads data/outcomes-A.json and data/outcomes-B.json (what the replay test wrote for each arm
from data/sequences-anonymized.json), data/suite-counts.json and data/unit-cases.json.
"""
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
def load(n): return json.load(open(os.path.join(here, "data", n)))
A, B = load("outcomes-A.json"), load("outcomes-B.json")
suite, unit = load("suite-counts.json"), load("unit-cases.json")

def missing_in_final(o):
    last = [r for r in o["rounds"] if r["refused"]]
    return last[-1].get("missing_problems", 0) if last and o["outcome"] == "review_invalid" else 0

rows = []
for a, b in zip(A, B):
    assert a["name"] == b["name"]
    rows.append((a["name"], a["outcome"], a.get("reason", ""), missing_in_final(a), b["outcome"], b["rounds_used"]))
print("%-12s %-34s %-8s %-9s %s" % ("sequence", "A outcome", "A missing", "B outcome", "B rounds"))
for r in rows: print("%-12s %-34s %-9d %-9s %d" % (r[0], r[1] + "/" + r[2], r[3], r[4], r[5]))

b2a = next(o for o in A if o["name"].startswith("B2"))
b2b = next(o for o in B if o["name"].startswith("B2"))
checks = {
    "1 A ends rejected_verdict_exhausted on every sequence": all(o["outcome"] == "review_invalid" and o["reason"] == "rejected_verdict_exhausted" for o in A),
    "2 B approves every sequence": all(o["outcome"] == "approved" for o in B),
    "2b B2 round 4 accepted on B": not b2b["rounds"][3]["refused"] and b2a["rounds"][3]["refused"],
    "3 B2 round 3 (drops accepted texts) still refused on B": b2b["rounds"][2]["refused"] and b2b["rounds"][2]["missing_problems"] == 18,
    "3b unit negative cases pass on B and fail on the mutant": all(unit["B_accepted_only"][c] == "pass" for c in unit["cases"]) and unit["mutant_nothing_is_ever_binding"]["a dropped requirement of an accepted submission is still refused"] == "fail",
    "4 suite: B full patch 0 failing": suite["B_full_patch"]["failing"] == 0,
}
for k, v in checks.items(): print(("PASS " if v else "FAIL ") + k)

replay = {
 "kind": "model-free-replay", "model_calls": 0,
 "finding_id": "lab-rc-b-review-listed-requirements-20261106",
 "rerun": "cd reproduce/lab-rc-b-review-listed-requirements-20261106 && python3 -I check.py",
 "arms": {
  "A-review-66be20d-replay": {
    "verdict": "ends rejected_verdict_exhausted on 5 of 5 recorded submission sequences",
    "counts": {"sequences": len(A), "review_invalid": sum(o["outcome"] == "review_invalid" for o in A), "approved": sum(o["outcome"] == "approved" for o in A),
               "missing_problems_in_final_refusals": sum(missing_in_final(o) for o in A), "b2_round4_accepted": int(not b2a["rounds"][3]["refused"])},
    "duration_s": 2.9},
  "B-accepted-only-replay": {
    "verdict": "approves 5 of 5 recorded sequences, including the round 4 that restored the accepted texts",
    "counts": {"sequences": len(B), "review_invalid": sum(o["outcome"] == "review_invalid" for o in B), "approved": sum(o["outcome"] == "approved" for o in B),
               "refusals_naming_dropped_accepted_texts": sum(1 for o in B for r in o["rounds"] if r["refused"] and r.get("missing_problems", 0) > 0),
               "b2_round4_accepted": int(not b2b["rounds"][3]["refused"])},
    "duration_s": 3.0},
  "B-unit-cases-negative-and-spelling": {
    "verdict": "4 of 4 cases pass on B; A fails the case that a refused submission's texts are not binding; a mutant that lists nothing fails 3",
    "counts": {"cases": len(unit["cases"]), "pass_on_B": sum(v == "pass" for v in unit["B_accepted_only"].values()),
               "pass_on_A": sum(v == "pass" for v in unit["A_66be20d"].values()), "mutant_failures": sum(v == "fail" for v in unit["mutant_nothing_is_ever_binding"].values())},
    "duration_s": 1.0},
  "suite-A-unchanged": {"verdict": "green", "counts": {"passing": suite["A_66be20d_unchanged"]["passing"], "failing": suite["A_66be20d_unchanged"]["failing"]}, "duration_s": suite["A_66be20d_unchanged"]["duration_s"]},
  "suite-B-code-change-only": {"verdict": "1 failing: the test that asserts the replaced rule", "counts": {"passing": suite["B_code_change_only"]["passing"], "failing": suite["B_code_change_only"]["failing"]}, "duration_s": suite["B_code_change_only"]["duration_s"]},
  "suite-B-full-patch": {"verdict": "green with that test's assertions inverted and 5 test cases added", "counts": {"passing": suite["B_full_patch"]["passing"], "failing": suite["B_full_patch"]["failing"]}, "duration_s": suite["B_full_patch"]["duration_s"]},
 },
 "inputs": [{"tree": "kogen-review", "sha": "66be20d31658374a86b98f23a1d8476e861193e0"}],
}
path = os.path.join(here, "replay.json")
if len(sys.argv) > 1 and sys.argv[1] == "--write":
    json.dump(replay, open(path, "w"), indent=1); print("wrote", path)
else:
    same = json.load(open(path)) == replay
    print(("PASS " if same else "FAIL ") + "replay.json equals what data/ gives")
    sys.exit(0 if same and all(checks.values()) else 1)
