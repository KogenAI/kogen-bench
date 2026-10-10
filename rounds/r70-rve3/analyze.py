#!/usr/bin/env python3
"""Analyze rve3 pair outcomes without emitting non-allowlisted grade/manifest fields."""
import json
import math
import os
import subprocess
import sys

ROW_FILTER = "<private-path>"
GRADE_KEYS = "pass_,tests,failures,errors,skipped,tests_ran"
MANIFEST_KEYS = "runner_rc,graded"


def read_allowed(path, keys):
    result = subprocess.run([sys.executable, ROW_FILTER, path, "--keys", keys],
                            check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def exact_tail(n, k):
    if n == 0:
        return 1.0
    return sum(math.comb(n, i) for i in range(k, n + 1)) / (2 ** n)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("interim", "final"):
        raise SystemExit("usage: analyze.py interim|final")
    stage = sys.argv[1]
    limit = 9 if stage == "interim" else 18
    with open("PLAN.json", encoding="utf-8") as f:
        plan = json.load(f)
    try:
        with open("audit.json", encoding="utf-8") as f:
            audit = json.load(f)
    except FileNotFoundError:
        audit = {}
    try:
        with open("timeouts.json", encoding="utf-8") as f:
            timeouts = set(json.load(f))
    except FileNotFoundError:
        timeouts = set()
    ys, missing, flagged = {}, [], []
    for pair in plan["pairs"][:limit]:
        for cell in pair["cells"]:
            rid = cell["run_id"]
            base = os.path.join("pulled", pair["host"], rid)
            try:
                manifest = read_allowed(os.path.join(base, "manifest.json"), MANIFEST_KEYS)
                grade = read_allowed(os.path.join(base, "grade.json"), GRADE_KEYS)
            except (OSError, subprocess.CalledProcessError, json.JSONDecodeError):
                missing.append(rid)
                continue
            if not manifest.get("graded") or "pass_" not in grade:
                missing.append(rid)
                continue
            flag_count = audit.get(rid, 0)
            if isinstance(flag_count, dict):
                flag_count = flag_count.get("count", 0)
            if flag_count:
                flagged.append(rid)
            ys[rid] = int(bool(grade["pass_"]) and not flag_count and rid not in timeouts)

    pair_results, R, L = [], 0, 0
    for pair in plan["pairs"][:limit]:
        outcomes = {c["arm"]: ys.get(c["run_id"]) for c in pair["cells"]}
        if outcomes.get("rust") is None or outcomes.get("elixir") is None:
            continue
        rust, elixir = outcomes["rust"], outcomes["elixir"]
        R += int(rust == 1 and elixir == 0)
        L += int(rust == 0 and elixir == 1)
        pair_results.append({"pair_order": pair["pair_order"], "task": pair["task"],
                             "rust": rust, "elixir": elixir})
    n = len(pair_results)
    D = (R - L) / n if n else None
    p_rust, p_elixir = exact_tail(R + L, R), exact_tail(R + L, L)
    invalid = len(flagged) > 2
    rust_win = D is not None and D >= 0.15 and p_rust < 0.025
    elixir_win = D is not None and D <= -0.15 and p_elixir < 0.025
    verdict = "INVALID" if invalid else "INCOMPLETE" if missing else (
        "Rust better" if rust_win else "Elixir better" if elixir_win else "continue" if stage == "interim" else "INCONCLUSIVE")
    if stage == "interim" and not invalid and not missing and not (rust_win or elixir_win):
        remaining = 18 - limit
        can_rust = (R + remaining - L) / 18 >= 0.15 and exact_tail(R + remaining + L, R + remaining) < 0.025
        can_elixir = (R - (L + remaining)) / 18 <= -0.15 and exact_tail(R + L + remaining, L + remaining) < 0.025
        if not can_rust and not can_elixir:
            verdict = "INCONCLUSIVE (futility)"
    print(json.dumps({"stage": stage, "pairs_analyzed": n, "R": R, "L": L, "D": D,
                      "p_rust": p_rust, "p_elixir": p_elixir, "verdict": verdict,
                      "missing_or_ungraded": sorted(set(missing)), "flagged": sorted(set(flagged)),
                      "timeouts": sorted(timeouts),
                      "pair_outcomes": pair_results}, sort_keys=True))


if __name__ == "__main__":
    main()
