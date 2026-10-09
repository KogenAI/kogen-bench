#!/usr/bin/env python3
"""rz1 analysis per the FROZEN DECISION-RULE (levers/rz1/prereg/DECISION-RULE.md, PRE-LAUNCH-SHA256 66d56f8e + AMENDMENT-1).

Usage:  python3 rz1_analyze.py interim   # after pairs 1..12 (PLAN order) are all officially graded
        python3 rz1_analyze.py final     # after all 21 pairs (or an early stop)
Reads PLAN.json (pair order, cell ids) and the official r70 grade rows (levers/r70/grades.jsonl) through safe_rows.
Prints aggregate numbers only (no test names/output). Y = 1 only for official outcome 'pass'.
"""
import json, sys
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEV = HERE.parent
sys.path.insert(0, str(LEV / "lib"))
from safe_rows import load_rows, sanitize  # noqa: E402

MARGIN = 0.15
ALPHA = 0.025  # per direction, at the interim and at the final (alpha split)


def p_tail(k, n):
    return 1.0 if n == 0 else sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "interim"
    plan = json.loads((HERE / "PLAN.json").read_text())
    cells = sorted(plan["cells"], key=lambda c: c["index"])
    upto = 12 if mode == "interim" else plan["pair_count"]
    rows = [sanitize(r) for r in load_rows(str(LEV / "r70" / "grades.jsonl"))]
    # latest official grade per cell_id (grade rows carry cell_id; regrades append)
    grade = {}
    for r in rows:
        cid = r.get("cell_id") or ""
        if cid.startswith("codex__gpt-6-luna__max__default__r70-") and r.get("experiment", "").startswith("rz1-"):
            grade[cid] = r
    pairs = {}
    for c in cells:
        if c["pair_order"] < upto:
            pairs.setdefault(c["pair_order"], {})[c["stack"]] = c
    missing = [c["cell_id"] for p in pairs.values() for c in p.values() if c["cell_id"] not in grade]
    if missing:
        print(json.dumps({"mode": mode, "error": "ungraded cells", "missing": missing}, indent=1))
        return 2
    R = L = 0
    per_task = {}
    for po, p in sorted(pairs.items()):
        yr = 1 if grade[p["rust"]["cell_id"]].get("outcome") == "pass" else 0
        yz = 1 if grade[p["zig"]["cell_id"]].get("outcome") == "pass" else 0
        R += (yr == 0 and yz == 1); L += (yr == 1 and yz == 0)
        per_task.setdefault(p["rust"]["task"], []).append((yr, yz))
    D = sum(sum(z - r for r, z in v) / len(v) for v in per_task.values()) / len(per_task)
    pp, pm = p_tail(R, R + L), p_tail(L, R + L)
    out = {"mode": mode, "pairs_analysed": len(pairs), "R_rescues_zig": R, "L_losses_zig": L, "D": round(D, 6),
           "p_plus": pp, "p_minus": pm,
           "per_task": {t: {"rust_pass": sum(r for r, _ in v), "zig_pass": sum(z for _, z in v), "pairs": len(v)} for t, v in sorted(per_task.items())}}
    if mode == "interim":
        # futility: even if every remaining planned pair is a rescue, can the FINAL superiority criterion be met?
        rem = [c for c in cells if c["pair_order"] >= upto and c["stack"] == "rust"]
        best = {t: list(v) for t, v in per_task.items()}
        for c in rem:
            best.setdefault(c["task"], []).append((0, 1))
        Rb = R + len(rem)
        Db = sum(sum(z - r for r, z in v) / len(v) for v in best.values()) / len(best)
        ppb = p_tail(Rb, Rb + L)
        zig_worse = D <= -MARGIN and pm < ALPHA
        futile = not (Db >= MARGIN and ppb < ALPHA)
        out.update(best_case_final={"R": Rb, "L": L, "D": round(Db, 6), "p_plus": ppb},
                   stop_zig_worse=zig_worse, stop_futility=futile,
                   decision=("STOP: ZIG WORSE (conclusive, Rust stays)" if zig_worse else
                             "STOP: FUTILITY (INCONCLUSIVE, Rust stays)" if futile else
                             "CONTINUE: run --launch --from-pair 13"))
    else:
        if D >= MARGIN and pp < ALPHA:
            dec = "ZIG REPLACES RUST"
        elif D <= -MARGIN and pm < ALPHA:
            dec = "ZIG WORSE (conclusive, Rust stays)"
        else:
            dec = "INCONCLUSIVE (Rust stays)"
        out["decision"] = dec + " -- subject to the INVALID/INCOMPLETE checks in DECISION-RULE.md"
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
