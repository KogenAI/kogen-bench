"""Reproduce the hard-tasks-grading-correction numbers from published.csv and regrade.csv (standard library only).

Corrected verdict per cell (rules in README):
  regraded   the kept tree was regraded with the repaired grader and its hidden-test results equal the stored grade's;
             pass = all_passed and a normal ending (landed, ok, finished)
  pending    regraded, but a hidden test gives a different result on the regrade host than on the cohort's own host,
             or a kept Linux tree that only the laptop can regrade (case fixture) and has not been yet
  fail       not regraded, and fails whatever the acceptance runner says: the run did not end normally, or a hidden
             test failed in the stored grade on the cohort's own host (not one caused by the case fixture)
  unknown    not regraded and the tree was not kept; only acceptance ids were missing, so it could pass or fail
  published  the task's grade was not affected by either defect: the published verdict stands
"""
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
COHORTS = ["hk3-lm", "hk3-mb", "cco-mb", "ccs2-mb", "ccs3-lm"]
ACCEPTANCE = {"kogen-loop-tool-cut", "kogen-loop-read-ledger", "kogen-loop-parallel-calls"}
CASE_FIXTURE = "revive-baseline-go"
NORMAL = {"landed", "ok", "finished"}


def non_discriminating(task, host):
    return task in ACCEPTANCE or (task == CASE_FIXTURE and host == "linux")


def sign_p(wins, losses):
    n = wins + losses
    if not n:
        return 1.0
    k = min(wins, losses)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def read(name):
    with open(os.path.join(HERE, name), newline="") as f:
        return list(csv.DictReader(f))


pub = read("published.csv")
reg = {(r["cohort"], r["task"], r["arm"]): r for r in read("regrade.csv")}
cells = {(r["cohort"], r["task"], r["arm"]): r for r in pub}

print("1. Published pairs, and the ones the grader forced")
print("cohort   pairs ties forced | other tasks: n kogen alone kogen-only alone-only sign-p")
tot = [0] * 9
for co in COHORTS:
    tasks = sorted({r["task"] for r in pub if r["cohort"] == co})
    host = cells[(co, tasks[0], "kogen")]["host"]
    ties = forced = n = k = a = kw = aw = 0
    for t in tasks:
        kp, ap = int(cells[(co, t, "kogen")]["passed"]), int(cells[(co, t, "alone")]["passed"])
        ties += kp == ap
        if non_discriminating(t, host):
            forced += 1
        else:
            n, k, a, kw, aw = n + 1, k + kp, a + ap, kw + (kp > ap), aw + (ap > kp)
    row = [len(tasks), ties, forced, n, k, a, kw, aw]
    tot = [x + y for x, y in zip(tot, row + [0])]
    print(f"{co:8} {row[0]:5} {ties:4} {forced:6} | {n:13} {k:5} {a:5} {kw:10} {aw:10} {sign_p(kw, aw):6.2f}")
print(f"{'all':8} {tot[0]:5} {tot[1]:4} {tot[2]:6} | {tot[3]:13} {tot[4]:5} {tot[5]:5} {tot[6]:10} {tot[7]:10} "
      f"{sign_p(tot[6], tot[7]):6.2f}")


def verdict(co, t, arm):
    p, r = cells[(co, t, arm)], reg.get((co, t, arm))
    if not non_discriminating(t, p["host"]):
        return "pass" if p["passed"] == "1" else "fail", "published"
    if r and r["status"] == "graded":
        if r["hidden_ids_differing_from_stored"] not in ("", "0"):
            return "pending", f"hidden results differ on the {r['graded_on']}"
        ok = r["new_passed"] == "1" and p["outcome"] in NORMAL
        return "pass" if ok else "fail", f"regraded on the {r['graded_on']} ({r['new_tests']})"
    if p["outcome"] not in NORMAL:
        return "fail", f"ended {p['outcome']}"
    if t in ACCEPTANCE and int(p["hidden_not_passed"] or 0) > 0:
        return "fail", f"{p['hidden_not_passed']} hidden ids failed in the stored grade"
    if r is None or r["status"] != "not_kept":
        return "pending", "kept tree, laptop regrade not run yet"
    return "unknown", "tree not kept"


print()
print("2. Corrected verdict on the affected tasks")
print("cohort   task                       kogen                                       alone")
summary = {}
for co in COHORTS:
    s = summary.setdefault(co, {"kogen": {}, "alone": {}, "pairs": {}})
    tasks = sorted({r["task"] for r in pub if r["cohort"] == co})
    for t in tasks:
        v = {arm: verdict(co, t, arm) for arm in ("kogen", "alone")}
        for arm in v:
            s[arm][v[arm][0]] = s[arm].get(v[arm][0], 0) + 1
        kv, av = v["kogen"][0], v["alone"][0]
        pair = ("tie" if kv == av else "kogen" if kv == "pass" else "alone") if {kv, av} <= {"pass", "fail"} else "open"
        s["pairs"][pair] = s["pairs"].get(pair, 0) + 1
        if non_discriminating(t, cells[(co, t, "kogen")]["host"]):
            print(f"{co:8} {t:26} {v['kogen'][0] + ': ' + v['kogen'][1]:43} {v['alone'][0]}: {v['alone'][1]}")

print()
print("3. Corrected totals per cohort (all tasks)")
print("cohort   kogen pass/fail/unknown/pending  alone pass/fail/unknown/pending  pairs: kogen-only alone-only tie open  sign-p")
for co in COHORTS:
    s = summary[co]
    fmt = lambda d: "/".join(str(d.get(x, 0)) for x in ("pass", "fail", "unknown", "pending"))
    pr = s["pairs"]
    print(f"{co:8} {fmt(s['kogen']):31}  {fmt(s['alone']):31}  {pr.get('kogen', 0):17} {pr.get('alone', 0):10} "
          f"{pr.get('tie', 0):3} {pr.get('open', 0):4}  {sign_p(pr.get('kogen', 0), pr.get('alone', 0)):.2f}")

print()
graded = [r for r in reg.values() if r["status"] == "graded"]
print(f"4. Regrade: {len(graded)} trees graded, {sum(r['status'] == 'not_kept' for r in reg.values())} cells without a kept tree; "
      f"pass flips {sum(r['old_passed'] != r['new_passed'] for r in graded)}; "
      f"acceptance ids still missing {sum(int(r['acceptance_missing_after'] or 0) for r in graded)}; "
      f"trees whose hidden results differ from the stored grade {sum(r['hidden_ids_differing_from_stored'] not in ('', '0') for r in graded)}")
