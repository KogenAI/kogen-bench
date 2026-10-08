#!/usr/bin/env python3
"""Recompute and validate the public L4b US result from its sanitized cell CSV."""

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROUND = Path(__file__).resolve().parents[1]
EXPECTED = {
    "cells_sha256": "a990121b1bd84239f78eea995188dccefe20f1999a125f92dc21729c71a949e1",
    "order_sha256": "7bf90b6784c9f48b84fc073d3ac8b34361d28c6b67c0baf76c69cd380577d720",
    "design_sha256": "7b6bd259e4dcf0229f1d4840daaed75fbee27722f916cec3fcc5ac9743f8dc7f",
    "decision_rule_sha256": "280688cd9ba3b7383b5d0bf634bb33ae53cbe28dc29cb2ca27bb86bb6e30810a",
    "variants": ("r70-4-go-fe2", "r70-4-ts-bun-fe2", "r70-5-go"),
    "arm_passes": {"packet": 6, "control": 6},
    "paired_rescues": (("r70-4-ts-bun-fe2", 2), ("r70-5-go", 2)),
    "paired_losses": (("r70-4-ts-bun-fe2", 3), ("r70-5-go", 3)),
    "arm_token_sums": {
        "packet": (425169, 3750400, 189854, 4365423),
        "control": (383221, 3966464, 184884, 4534569),
    },
}
FIELDS = (
    "order", "cell_id", "variant", "task_id", "arm", "seed", "rep",
    "cell_status", "outcome", "tests_passed", "tests_total",
    "uncached_input_tokens", "cached_input_tokens", "output_tokens",
    "total_tokens", "host", "grade_route",
)
TOKEN_FIELDS = (
    "uncached_input_tokens", "cached_input_tokens", "output_tokens", "total_tokens",
)


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_data():
    require(sha256(ROUND / "DESIGN.md") == EXPECTED["design_sha256"], "frozen design changed")
    require(
        sha256(ROUND / "DECISION-RULE.md") == EXPECTED["decision_rule_sha256"],
        "pre-registered decision rule changed",
    )
    order_path = ROUND / "reproduce" / "ORDER.json"
    require(sha256(order_path) == EXPECTED["order_sha256"], "frozen order changed")
    cells_path = ROUND / "data" / "cells.csv"
    require(sha256(cells_path) == EXPECTED["cells_sha256"], "sanitized cell data changed")

    order_doc = json.loads(order_path.read_text())
    expected_cells = order_doc["cells"]
    require(len(expected_cells) == 18, "frozen order must contain 18 cells")
    require(order_doc["n"] == 18 and order_doc["host"] == "us", "unexpected frozen order scope")

    with cells_path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        require(tuple(reader.fieldnames or ()) == FIELDS, "unexpected CSV schema")
        rows = list(reader)
    require(len(rows) == 18, "expected 18 public cell records")
    require([row["cell_id"] for row in rows] == order_doc["cell_ids"], "CSV order differs from frozen order")

    by_id = {cell["cell_id"]: cell for cell in expected_cells}
    require(len(by_id) == 18, "frozen order has duplicate cell IDs")
    int_fields = (
        "order", "seed", "rep", "tests_passed", "tests_total",
        "uncached_input_tokens", "cached_input_tokens", "output_tokens", "total_tokens",
    )
    for row in rows:
        for key in int_fields:
            row[key] = int(row[key])
        frozen = by_id[row["cell_id"]]
        for csv_key, order_key in (
            ("order", "order"), ("variant", "variant"), ("task_id", "task"),
            ("arm", "arm"), ("seed", "seed"), ("rep", "rep"),
        ):
            require(row[csv_key] == frozen[order_key], f"{csv_key} mismatch for {row['cell_id']}")
        require(row["cell_status"] == "VALID", f"non-VALID cell {row['cell_id']}")
        require(row["outcome"] in ("pass", "fail"), f"invalid outcome for {row['cell_id']}")
        require(row["host"] == "kogen-bench-us", f"wrong host for {row['cell_id']}")
        require(row["grade_route"] == "r70-macbook-window-v1", f"wrong grade route for {row['cell_id']}")
        require(row["rep"] == 60 + row["seed"], f"seed/rep mismatch for {row['cell_id']}")
        require(
            row["total_tokens"] == sum(row[key] for key in TOKEN_FIELDS[:3]),
            f"token total mismatch for {row['cell_id']}",
        )
    return rows


def summarize(rows):
    variants = EXPECTED["variants"]
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["variant"], row["arm"])].append(row)
    stats = {}
    for variant in variants:
        for arm in ("packet", "control"):
            cells = grouped[(variant, arm)]
            require(len(cells) == 3, f"expected n=3 for {variant} {arm}")
            stats[(variant, arm)] = {
                "passes": sum(row["outcome"] == "pass" for row in cells),
                "mean_tests": sum(row["tests_passed"] for row in cells) / 3,
                "tests_sum": sum(row["tests_passed"] for row in cells),
            }
    arm_rows = {arm: [row for row in rows if row["arm"] == arm] for arm in ("packet", "control")}
    arm_passes = {arm: sum(row["outcome"] == "pass" for row in cells) for arm, cells in arm_rows.items()}
    require(arm_passes == EXPECTED["arm_passes"], "overall arm pass counts differ from verified result")
    token_sums = {
        arm: tuple(sum(row[key] for row in cells) for key in TOKEN_FIELDS)
        for arm, cells in arm_rows.items()
    }
    require(token_sums == EXPECTED["arm_token_sums"], "arm token totals differ from verified result")

    pairs = defaultdict(dict)
    for row in rows:
        pairs[(row["variant"], row["seed"])][row["arm"]] = row
    require(len(pairs) == 9 and all(set(pair) == {"packet", "control"} for pair in pairs.values()), "paired coverage mismatch")
    rescues, losses = [], []
    for (variant, seed), pair in sorted(pairs.items(), key=lambda item: (variants.index(item[0][0]), item[0][1])):
        p = pair["packet"]["outcome"] == "pass"
        c = pair["control"]["outcome"] == "pass"
        if p and not c:
            rescues.append((variant, seed))
        elif c and not p:
            losses.append((variant, seed))
    require(tuple(rescues) == EXPECTED["paired_rescues"], "paired rescue set mismatch")
    require(tuple(losses) == EXPECTED["paired_losses"], "paired loss set mismatch")

    delta = sum(stats[(variant, "packet")]["passes"] - stats[(variant, "control")]["passes"] for variant in variants)
    no_test_regression = all(
        stats[(variant, "packet")]["mean_tests"] >= stats[(variant, "control")]["mean_tests"] - 1
        for variant in variants
    )
    decision = "CONFIRM" if delta >= 2 and no_test_regression else "NOT CONFIRMED"
    require(delta == 0 and decision == "NOT CONFIRMED", "pre-registered decision mismatch")
    require(
        all(stats[(variant, "packet")]["mean_tests"] == stats[(variant, "control")]["mean_tests"] for variant in variants),
        "per-variant mean tests_passed are not equal",
    )
    return {
        "stats": stats, "pairs": pairs, "rescues": rescues, "losses": losses,
        "delta": delta, "decision": decision, "arm_rows": arm_rows,
        "arm_passes": arm_passes, "token_sums": token_sums,
    }


def render_results(rows, result):
    lines = [
        "## Per-variant outcomes",
        "",
        "| Variant | Packet full passes | Control full passes | Packet mean tests_passed | Control mean tests_passed | P−C |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for variant in EXPECTED["variants"]:
        p = result["stats"][(variant, "packet")]
        c = result["stats"][(variant, "control")]
        lines.append(f"| `{variant}` | {p['passes']}/3 | {c['passes']}/3 | {p['mean_tests']:.2f} | {c['mean_tests']:.2f} | {p['passes']-c['passes']} |")
    lines.extend([
        f"| **Total** | **{result['arm_passes']['packet']}/9** | **{result['arm_passes']['control']}/9** | — | — | **{result['delta']}** |",
        "",
        f"**Decision: {result['decision']}** under the pre-registered rule (required Σ(P−C) ≥ +2; observed Σ(P−C) = {result['delta']}).",
        f"Paired outcomes: **{len(result['rescues'])} rescues** and **{len(result['losses'])} losses**.",
        "",
        "## Paired outcomes by variant and seed",
        "",
        "| Variant | Seed (rep) | Packet outcome (`tests_passed`) | Control outcome (`tests_passed`) | Pair result |",
        "| --- | ---: | --- | --- | --- |",
    ])
    for variant in EXPECTED["variants"]:
        for seed in (1, 2, 3):
            pair = result["pairs"][(variant, seed)]
            p, c = pair["packet"], pair["control"]
            if p["outcome"] == c["outcome"]:
                pair_result = "same"
            elif p["outcome"] == "pass":
                pair_result = "rescue"
            else:
                pair_result = "loss"
            lines.append(
                f"| `{variant}` | {seed} (r{60+seed}) | {p['outcome'].upper()} ({p['tests_passed']}/{p['tests_total']}) | "
                f"{c['outcome'].upper()} ({c['tests_passed']}/{c['tests_total']}) | {pair_result} |"
            )
    lines.extend([
        "",
        "## Token use per official full pass",
        "",
        "Numerator is total usage across all nine cells in that arm, including failed cells; denominator is official full passes. One token definition applies: uncached input + cached input + output = total.",
        "",
        "| Arm | Full passes | Uncached input / pass | Cached input / pass | Output / pass | Total / pass |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    for arm in ("packet", "control"):
        denom = result["arm_passes"][arm]
        per_pass = [value / denom for value in result["token_sums"][arm]]
        lines.append(
            f"| {arm} | {denom}/9 | {per_pass[0]:,.1f} | {per_pass[1]:,.1f} | {per_pass[2]:,.1f} | {per_pass[3]:,.1f} |"
        )
    for arm in ("packet", "control"):
        totals = result["token_sums"][arm]
        lines.append(
            f"\nAll-cell token sums ({arm}): uncached {totals[0]:,}; cached {totals[1]:,}; output {totals[2]:,}; total {totals[3]:,}."
        )
    lines.extend([
        "",
        "## Frozen seeded interleaved order and official outcomes",
        "",
        "| Order | Cell ID | Variant | Arm | Seed | Rep | Outcome | tests_passed |",
        "| ---: | --- | --- | --- | ---: | ---: | --- | ---: |",
    ])
    for row in rows:
        lines.append(
            f"| {row['order']} | `{row['cell_id']}` | `{row['variant']}` | {row['arm']} | {row['seed']} | {row['rep']} | "
            f"{row['outcome'].upper()} | {row['tests_passed']}/{row['tests_total']} |"
        )
    return "\n".join(lines)


def headline(result):
    return (
        f"NOT CONFIRMED: packet {result['arm_passes']['packet']}/9 vs control {result['arm_passes']['control']}/9; "
        f"Σ(P−C)={result['delta']} (pre-registered threshold: +2); "
        f"{len(result['rescues'])} paired rescues and {len(result['losses'])} paired losses."
    )


def update_or_validate(rows, result, write):
    results_path = ROUND / "RESULTS.md"
    results_text = results_path.read_text()
    begin = "<!-- R70-L4B-US:BEGIN -->"
    end = "<!-- R70-L4B-US:END -->"
    require(results_text.count(begin) == 1 and results_text.count(end) == 1, "RESULTS.md markers missing or duplicated")
    generated = begin + "\n\n" + render_results(rows, result) + "\n\n" + end
    start = results_text.index(begin)
    stop = results_text.index(end, start) + len(end)
    if write:
        results_path.write_text(results_text[:start] + generated + results_text[stop:])
    else:
        require(results_text[start:stop] == generated, "published RESULTS.md numbers differ; rerun with --write after review")

    readme = (ROUND / "README.md").read_text()
    require("STATUS: **VALID**" in readme, "README.md must label the US part VALID")
    require("Headline: " + headline(result) in readme, "README.md headline differs from recomputed result")
    for population in (
        "Planned scored cells", "Started scored cells", "Finished cells",
        "Officially graded cells", "ITT denominator",
    ):
        require(f"| {population} | {len(rows)} |" in readme, f"README.md {population} count differs from the cell data")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="replace only the marked numeric block in RESULTS.md")
    args = parser.parse_args()
    rows = load_data()
    result = summarize(rows)
    update_or_validate(rows, result, args.write)
    print(f"PASS: {len(rows)} VALID official US cells; {result['decision']}; Σ(P−C)={result['delta']}.")
    print(f"PASS: {len(result['rescues'])} paired rescues, {len(result['losses'])} paired losses; token totals reconcile.")
    print("PASS: published RESULTS.md tables and README headline match the recomputation.")


if __name__ == "__main__":
    main()
