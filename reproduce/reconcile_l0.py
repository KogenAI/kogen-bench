#!/usr/bin/env python3
"""Recompute L0 historical counts and declared intervals from sanitized CSVs."""
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "rounds" / "l0-reconcile" / "data"
PUBLIC_GRADE_EXPORT = ROOT / "reproduce" / "inputs" / "grades.final.jsonl"
PUBLIC_GRADE_EXPORT_SHA256 = "4d639a3848b3661dcb5646630b6a4914e5053ff4b94ab029424d47d040e3c977"
PRE_REFRESH_R69_SNAPSHOT = "58c9ca5ee40fb958c61c61e381191a922886f88f (2026-10-07T16:18:30+03:00)"
PRE_REFRESH_R69_EXPORT_SHA256 = "cbf85effb6334c650fa0204da6e2777ed8a5a699f14ab854529d998b5177703a"
Z95 = 1.959963984540054
Z_ONE_SIDED_95 = 1.644853627


def read_csv(name):
    with (DATA / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_public_grade_export():
    raw = PUBLIC_GRADE_EXPORT.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != PUBLIC_GRADE_EXPORT_SHA256:
        raise AssertionError(
            "Pinned official grade export changed: expected "
            + PUBLIC_GRADE_EXPORT_SHA256 + ", found " + digest
        )
    grades = {}
    for line_no, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        cell_id = row.get("cell_id")
        if not isinstance(cell_id, str) or not cell_id:
            raise AssertionError(f"official grade row {line_no} has no cell_id")
        if cell_id in grades:
            raise AssertionError(f"duplicate official grade cell_id at row {line_no}: {cell_id}")
        grades[cell_id] = row
    return grades


def wilson(k, n, z=Z95):
    if n <= 0:
        raise ValueError("Wilson interval requires n > 0")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def difference_ci(ka, na, kb, nb):
    pa, pb = ka / na, kb / nb
    la, ua = wilson(ka, na)
    lb, ub = wilson(kb, nb)
    delta = pa - pb
    return (delta - math.sqrt((pa - la) ** 2 + (ub - pb) ** 2),
            delta + math.sqrt((ua - pa) ** 2 + (pb - lb) ** 2))


def exact_task_stratified_p(rows, first, second):
    """Upper-tail exact test, conditioning on pairwise successes per task."""
    tasks = sorted({r["task"] for r in rows})
    distribution = [Fraction(1)]
    observed = 0
    for task in tasks:
        a = [r for r in rows if r["task"] == task and r["arm"] == first]
        b = [r for r in rows if r["task"] == task and r["arm"] == second]
        na, nb = len(a), len(b)
        ka = sum(r["outcome"] == "PASS" for r in a)
        kb = sum(r["outcome"] == "PASS" for r in b)
        observed += ka
        successes, total = ka + kb, na + nb
        denominator = math.comb(total, na)
        local = [Fraction(0)] * (na + 1)
        low = max(0, na - (total - successes))
        high = min(na, successes)
        for x in range(low, high + 1):
            local[x] = Fraction(
                math.comb(successes, x) * math.comb(total - successes, na - x),
                denominator,
            )
        updated = [Fraction(0)] * (len(distribution) + len(local) - 1)
        for i, left in enumerate(distribution):
            for j, right in enumerate(local):
                updated[i + j] += left * right
        distribution = updated
    if sum(distribution) != 1:
        raise AssertionError("exact task-stratified distribution does not sum to one")
    p = sum(distribution[observed:])
    return p, observed, len(tasks)


def r72():
    p1 = read_csv("r72-p1.csv")
    p3 = read_csv("r72-p3-partial.csv")
    counts = Counter((r["arm"], r["outcome"]) for r in p1)
    assert len(p1) == 168
    assert counts[("kogen-ladder-luna", "PASS")] == 64
    assert counts[("kogen-ladder-luna", "FAIL")] == 19
    assert counts[("kogen-ladder-luna", "INVALID")] == 1
    assert counts[("codex-luna-max", "PASS")] == 60
    assert counts[("codex-luna-max", "FAIL")] == 24
    p3_counts = Counter((r["arm"], r["outcome"]) for r in p3)
    assert len(p3) == 24
    assert (p3_counts[("kogen-ladder", "PASS")],
            p3_counts[("codex-sol-high", "PASS")]) == (12, 10)
    print("R72 P1: Kogen Luna 64/84 (19 FAIL, 1 INVALID); Codex Luna max 60/84 (24 FAIL).")
    print("R72 P3 partial: Kogen ladder 12/13; Codex Sol high 10/11.")
    print("R72 public scored export matches: 0; P1 claim reproduced exactly; stopped/INTERIM.")


def r74():
    scored = read_csv("r74-graded-subset.csv")
    smokes = read_csv("r74-smoke-attempts.csv")
    coverage = read_csv("r74-coverage.csv")[0]
    counts = Counter((r["arm"], r["outcome"]) for r in scored)
    smoke_counts = Counter(r["smoke_disposition"] for r in smokes)
    assert len(scored) == int(coverage["official_scored_grade_rows"]) == 167
    assert len(smokes) == int(coverage["smoke_attempt_grade_rows"]) == 9
    assert int(coverage["retained_specs_after_amendment_c"]) == 398
    assert int(coverage["retained_specs_without_scored_grade"]) == 231
    assert int(coverage["published_sot_scored_rows"]) == 0
    assert smoke_counts == Counter({"SELECTED_SMOKE": 8, "WITHDRAWN_ENV_FAULT": 1})
    assert sum(counts.values()) == 167
    print("R74 scored internal subset: 167 official grades; 9 smoke attempts (8 selected, 1 withdrawn env fault).")
    for arm in sorted({r["arm"] for r in scored}):
        arm_counts = Counter(r["outcome"] for r in scored if r["arm"] == arm)
        print(f"  {arm}: " + ", ".join(f"{k}={arm_counts[k]}" for k in sorted(arm_counts)))
    print("R74 retained=398; scored=167; no scored grade=231; public scored export=0.")
    print("Public-export claim reproduced; full cohort NOT-RECONSTRUCTABLE; source round WITHDRAWN.")


def r69():
    all_rows = read_csv("r69-itt.csv")
    rows = [r for r in all_rows if r["included_in_itt"] == "yes"]
    grades = read_public_grade_export()
    for row in all_rows:
        official = grades.get(row["cell_id"])
        expected_public_outcome = str(official.get("outcome") or "").lower() if official else ""
        if row["public_export_outcome"] != expected_public_outcome:
            raise AssertionError(
                "r69-itt.csv public_export_outcome is stale for " + row["cell_id"]
            )
    graded = [r for r in rows if r["official_grade_outcome"]]
    public = [r for r in graded if r["cell_id"] in grades]
    expected = {"spec": (63, 99), "approach": (66, 99), "accept": (66, 98), "none": (59, 100)}
    assert len(all_rows) == 400 and len(rows) == 396 and len(graded) == 327 and len(public) == 150
    public_outcomes = Counter(grades[r["cell_id"]].get("outcome") for r in public)
    assert public_outcomes == Counter({"pass": 113, "fail": 37})
    summaries = {}
    for arm, (expected_pass, expected_n) in expected.items():
        arm_rows = [r for r in rows if r["arm"] == arm]
        k = sum(r["outcome"] == "PASS" for r in arm_rows)
        n = len(arm_rows)
        assert (k, n) == (expected_pass, expected_n)
        summaries[arm] = (k, n)
        low, high = wilson(k, n)
        print(f"R69 {arm.upper()}: {k}/{n}; Wilson 95% CI {100*low:.2f}–{100*high:.2f}%.")
    for first in ("approach", "accept"):
        ka, na = summaries[first]
        kb, nb = summaries["spec"]
        lo, hi = difference_ci(ka, na, kb, nb)
        p, observed, n_tasks = exact_task_stratified_p(rows, first, "spec")
        print(f"  {first.upper()}−SPEC: {100*(ka/na-kb/nb):+.2f} pp; Newcombe 95% CI {100*lo:+.2f} to {100*hi:+.2f} pp; exact one-sided task test p={float(p):.12f} ({p}), tasks={n_tasks}.")
    print(f"R69 refreshed official export exact-ID coverage={len(public)}/{len(graded)}; PASS={public_outcomes['pass']}, FAIL={public_outcomes['fail']}; SHA-256={PUBLIC_GRADE_EXPORT_SHA256}.")
    print(f"R69 historical coverage was 95/327 only in snapshot {PRE_REFRESH_R69_SNAPSHOT}, export SHA-256={PRE_REFRESH_R69_EXPORT_SHA256}; this snapshot is superseded.")
    print("R69 retained ITT=396/400 (327 grades plus 69 ITT failures; 4 proven exclusions).")
    print("R69 four-arm counts reproduced exactly.")


def r57():
    all_rows = read_csv("r57-pooled-itt.csv")
    rows = [r for r in all_rows if r["included_in_pooled_itt"] == "yes"]
    assert len(rows) == 311
    outcomes = Counter((r["arm"], r["outcome"]) for r in rows)
    arm_n = Counter(r["arm"] for r in rows)
    shell_pass = outcomes[("shell-only", "PASS")]
    default_pass = outcomes[("default-tools", "PASS")]
    assert (shell_pass, arm_n["shell-only"]) == (114, 155)
    assert (default_pass, arm_n["default-tools"]) == (111, 156)
    assert sum(bool(r["public_export_outcome"]) for r in rows) == 311

    planned_per_arm = {"us": 4, "eu": 8, "studio": 16}
    groups = defaultdict(lambda: defaultdict(list))
    for r in rows:
        groups[(r["task"], r["host"])][r["arm"]].append(r)
    assert len(groups) == 16
    assert sum(planned_per_arm[h] for _, h in groups) == 156
    weighted_delta = 0.0
    variance_term = 0.0
    equal_delta = 0.0
    equal_variance_term = 0.0
    for (task, host), arms in groups.items():
        planned = planned_per_arm[host]
        shell = arms["shell-only"]
        default = arms["default-tools"]
        ks = sum(r["outcome"] == "PASS" for r in shell)
        kd = sum(r["outcome"] == "PASS" for r in default)
        ns, nd = len(shell), len(default)
        if nd != planned or ns not in (planned, planned - 1):
            raise AssertionError(f"unexpected arm n for {task}/{host}")
        if ns != planned - 1 and ns != planned:
            raise AssertionError("unexpected missing count")
        ps, pd = ks / ns, kd / nd
        ls, _ = wilson(ks, ns, Z_ONE_SIDED_95)
        _, ud = wilson(kd, nd, Z_ONE_SIDED_95)
        w = planned / 156
        delta = ps - pd
        weighted_delta += w * delta
        variance_term += w * w * ((ps - ls) ** 2 + (ud - pd) ** 2)
        we = 1 / len(groups)
        equal_delta += we * delta
        equal_variance_term += we * we * ((ps - ls) ** 2 + (ud - pd) ** 2)
    lower = weighted_delta - math.sqrt(variance_term)
    equal_lower = equal_delta - math.sqrt(equal_variance_term)
    print(f"R57 pooled: shell {shell_pass}/{arm_n['shell-only']}; default {default_pass}/{arm_n['default-tools']}; public grade matches=311/311.")
    print(f"  Fixed host×task weights: delta={100*weighted_delta:+.2f} pp; one-sided 95% stratified Newcombe/MOVER lower={100*lower:+.2f} pp (criterion ≥−10 pp: met={lower >= -0.10}).")
    print(f"  Equal-stratum sensitivity: delta={100*equal_delta:+.2f} pp; lower={100*equal_lower:+.2f} pp.")
    print("R57 one planned Studio shell slot lacks a recovered cell ID and grade; excluded from ITT, not scored as failure; source round INTERIM.")


def main():
    r72()
    r74()
    r69()
    r57()


if __name__ == "__main__":
    main()
