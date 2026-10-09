#!/usr/bin/env python3
"""Recompute the preregistered rz1 interim and final decision from public records."""
from __future__ import annotations

import gzip
import json
import math
from collections import defaultdict
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ALPHA = 0.025
MARGIN = 0.15


def tail(k: int, n: int) -> float:
    if n == 0:
        return 1.0
    return sum(math.comb(n, i) for i in range(k, n + 1)) / (2**n)


def load_rows() -> dict[str, dict]:
    path = ROOT / "data/mined/rz1.jsonl.gz"
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        rows = [json.loads(line) for line in stream if line.strip()]
    if len(rows) != 42:
        raise AssertionError(f"expected 42 mined records, got {len(rows)}")
    out = {row.get("cell_id"): row for row in rows}
    if len(out) != 42 or None in out:
        raise AssertionError("mined cell IDs are missing or duplicated")
    return out


def analyze(plan: dict, rows: dict[str, dict], upto: int | None) -> dict:
    cells = sorted(plan["cells"], key=lambda cell: cell["index"])
    pair_limit = plan["pair_count"] if upto is None else upto
    pairs: dict[int, dict[str, dict]] = defaultdict(dict)
    for cell in cells:
        if cell["pair_order"] < pair_limit:
            pairs[cell["pair_order"]][cell["stack"]] = cell
    if len(pairs) != pair_limit or any(set(pair) != {"rust", "zig"} for pair in pairs.values()):
        raise AssertionError("plan does not contain complete pairs for requested analysis")
    per_task: dict[str, list[tuple[int, int]]] = defaultdict(list)
    rescues = losses = 0
    for _, pair in sorted(pairs.items()):
        rust_cell, zig_cell = pair["rust"], pair["zig"]
        rust_row = rows.get(rust_cell["cell_id"])
        zig_row = rows.get(zig_cell["cell_id"])
        if rust_row is None or zig_row is None:
            raise AssertionError("planned cell is missing from mined records")
        yr = int(rust_row.get("official_grade", {}).get("outcome") == "pass")
        yz = int(zig_row.get("official_grade", {}).get("outcome") == "pass")
        rescues += int(yr == 0 and yz == 1)
        losses += int(yr == 1 and yz == 0)
        per_task[str(rust_cell["task"])].append((yr, yz))
    d = sum(sum(z - r for r, z in vals) / len(vals) for vals in per_task.values()) / len(per_task)
    result = {
        "mode": "interim" if upto is not None else "final",
        "pairs_analysed": len(pairs),
        "R_rescues_zig": rescues,
        "L_losses_zig": losses,
        "D": round(d, 6),
        "p_plus": tail(rescues, rescues + losses),
        "p_minus": tail(losses, rescues + losses),
        "per_task": {
            task: {
                "rust_pass": sum(r for r, _ in vals),
                "zig_pass": sum(z for _, z in vals),
                "pairs": len(vals),
            }
            for task, vals in sorted(per_task.items())
        },
    }
    if upto is not None:
        remaining = [cell for cell in cells if cell["pair_order"] >= upto and cell["stack"] == "rust"]
        best = {task: list(vals) for task, vals in per_task.items()}
        for cell in remaining:
            best.setdefault(str(cell["task"]), []).append((0, 1))
        rb = rescues + len(remaining)
        db = sum(sum(z - r for r, z in vals) / len(vals) for vals in best.values()) / len(best)
        ppb = tail(rb, rb + losses)
        worse = d <= -MARGIN and result["p_minus"] < ALPHA
        futile = not (db >= MARGIN and ppb < ALPHA)
        result.update({
            "best_case_final": {"R": rb, "L": losses, "D": round(db, 6), "p_plus": ppb},
            "stop_zig_worse": worse,
            "stop_futility": futile,
            "decision": (
                "STOP: ZIG WORSE (conclusive, Rust stays)" if worse else
                "STOP: FUTILITY (INCONCLUSIVE, Rust stays)" if futile else
                "CONTINUE: run --launch --from-pair 13"
            ),
        })
    else:
        if d >= MARGIN and result["p_plus"] < ALPHA:
            decision = "ZIG REPLACES RUST"
        elif d <= -MARGIN and result["p_minus"] < ALPHA:
            decision = "ZIG WORSE (conclusive, Rust stays)"
        else:
            decision = "INCONCLUSIVE (Rust stays)"
        result["decision"] = decision + " -- subject to the INVALID/INCOMPLETE checks in DECISION-RULE.md"
    return result


def main() -> None:
    plan = json.loads((HERE / "receipts/PLAN.json").read_text(encoding="utf-8"))
    rows = load_rows()
    checks = [
        ("interim", analyze(plan, rows, 12)),
        ("final", analyze(plan, rows, None)),
    ]
    for name, actual in checks:
        expected = json.loads((HERE / "receipts" / f"{name}-output.json").read_text(encoding="utf-8"))
        if actual != expected:
            raise AssertionError(f"{name} output does not match sanitized gate receipt")
        print(f"{name.upper()} PASS pairs={actual['pairs_analysed']} D={actual['D']} R={actual['R_rescues_zig']} L={actual['L_losses_zig']} p_plus={actual['p_plus']} p_minus={actual['p_minus']}")
    print("DECISION PASS INCONCLUSIVE (Rust stays)")


if __name__ == "__main__":
    main()
