#!/usr/bin/env python3
"""Recompute the public L3b outcome table and preregistered decision."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

from l3b_per_test_rule import load_per_test_results, per_test_no_regression

ROOT = Path(__file__).resolve().parents[3]
ROUND = "l3b-repair-vs-continue"
DATA = ROOT / "rounds" / ROUND / "data"
README = ROOT / "rounds" / ROUND / "README.md"
RESULTS = ROOT / "rounds" / ROUND / "RESULTS.md"
BEGIN = "<!-- L3B-RESULTS:BEGIN -->"
END = "<!-- L3B-RESULTS:END -->"
PRIVATE_CHECK_SHA = "17ebe3ef4a67bd09c83c8a8568505e8c3e42ea31981afc80ae7bcdc5c046d4a2"
ARMS = ("REPAIR", "CONTINUE", "RESTART")


def fail(message: str) -> None:
    raise SystemExit("L3b reproducer: " + message)


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def integer(row: dict[str, str], key: str) -> int:
    try:
        value = int(row[key])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid {key}: {exc}")
    if value < 0:
        fail(f"negative {key}")
    return value


def decimal(row: dict[str, str], key: str) -> Decimal:
    try:
        value = Decimal(row[key])
    except (KeyError, ArithmeticError, TypeError, ValueError) as exc:
        fail(f"invalid {key}: {exc}")
    if not value.is_finite() or value < 0:
        fail(f"invalid nonnegative {key}")
    return value


def load_data():
    originals = read_csv("original-failures.csv")
    scored = read_csv("scored-cells.csv")
    try:
        evidence = json.loads((DATA / "rule-evidence.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read rule evidence: {exc}")
    if len(originals) != 8 or len(scored) != 24:
        fail("expected 8 original failures and 24 scored cells")

    original_by_id = {row.get("original_failure_cell_id"): row for row in originals}
    cell_ids = [row.get("cell_id") for row in scored]
    if len(original_by_id) != 8 or any(not value for value in original_by_id):
        fail("original failure IDs must be unique and present")
    if len(set(cell_ids)) != 24 or any(not value for value in cell_ids):
        fail("scored cell IDs must be unique and present")

    for row in originals:
        passed, total = integer(row, "tests_passed"), integer(row, "tests_total")
        if row.get("outcome") != "fail" or total <= 0 or passed >= total:
            fail("every selected original must be an official aggregate failure")
        if not re.fullmatch(r"[0-9a-f]{64}", row.get("patch_sha256", "")):
            fail("each original needs its public delivered-patch SHA-256")
        for field in ("started_at", "finished_at"):
            if not row.get(field):
                fail(f"missing original {field}")
        parts = [integer(row, name) for name in (
            "uncached_input_tokens", "cached_input_tokens", "output_tokens"
        )]
        if integer(row, "total_tokens") != sum(parts):
            fail("original token components do not sum")
        decimal(row, "wall_s")

    seen = defaultdict(Counter)
    for row in scored:
        original_id, arm = row.get("original_failure_cell_id"), row.get("arm")
        if original_id not in original_by_id:
            fail("scored row refers to an unknown original")
        if arm not in ARMS:
            fail("unknown arm")
        seen[original_id][arm] += 1
        passed, total = integer(row, "tests_passed"), integer(row, "tests_total")
        if total <= 0 or passed > total:
            fail("invalid aggregate test fraction")
        if row.get("outcome") != ("pass" if passed == total else "fail"):
            fail("official outcome disagrees with aggregate counts")
        if total != integer(original_by_id[original_id], "tests_total"):
            fail("scored denominator differs from its matched original")
        expected_patch = original_by_id[original_id]["patch_sha256"] if arm in {"REPAIR", "CONTINUE"} else ""
        if row.get("patch_sha256", "") != expected_patch:
            fail("patch assignment differs from the public design")
        for field in ("started_at", "finished_at"):
            if not row.get(field):
                fail(f"missing scored {field}")
        parts = [integer(row, name) for name in (
            "uncached_input_tokens", "cached_input_tokens", "output_tokens"
        )]
        if integer(row, "total_tokens") != sum(parts):
            fail("scored token components do not sum")
        decimal(row, "wall_s")
    if any(seen[cid] != Counter({arm: 1 for arm in ARMS}) for cid in original_by_id):
        fail("each original must have one cell per arm")

    if evidence.get("schema_version") != 1:
        fail("unknown rule evidence schema")
    per_test_cells = load_per_test_results()
    per_test_digest = hashlib.sha256((DATA / "per-test-results.json").read_bytes()).hexdigest()
    if evidence.get("per_test_evidence_file") != "per-test-results.json":
        fail("rule evidence does not point to the published per-test sets")
    if evidence.get("per_test_evidence_sha256") != per_test_digest:
        fail("per-test evidence SHA-256 differs from the cited data")
    if evidence.get("public_rule_recomputation") != "rounds/l3b-repair-vs-continue/reproduce/l3b_per_test_rule.py":
        fail("rule evidence does not cite the public recomputation")
    no_regression, comparisons = per_test_no_regression(per_test_cells)
    if evidence.get("per_test_no_regression_available") is not True:
        fail("public per-test evidence is not marked available")
    if evidence.get("per_test_no_regression") is not no_regression:
        fail("stored per-test summary differs from the recomputed pass/fail sets")
    if evidence.get("repair_cells_checked") != len(comparisons):
        fail("per-test evidence must cover every REPAIR cell")
    evidence["per_test_comparisons"] = comparisons
    if evidence.get("private_check_sha256") != PRIVATE_CHECK_SHA:
        fail("private check SHA-256 differs from the cited source")
    return originals, scored, evidence


def render(originals, scored, evidence) -> str:
    rescue = Counter(
        row["arm"] for row in scored
        if row["outcome"] == "pass" and integer(row, "tests_passed") == integer(row, "tests_total")
    )
    counts = Counter(row["arm"] for row in scored)
    totals = {}
    for arm in ARMS:
        rows = [row for row in scored if row["arm"] == arm]
        totals[arm] = {
            "uncached": sum(integer(row, "uncached_input_tokens") for row in rows),
            "cached": sum(integer(row, "cached_input_tokens") for row in rows),
            "output": sum(integer(row, "output_tokens") for row in rows),
            "wall": sum((decimal(row, "wall_s") for row in rows), Decimal(0)),
        }
    delta = rescue["REPAIR"] - rescue["CONTINUE"]
    keep = delta >= 2 and evidence["per_test_no_regression"]
    tick = chr(96)

    lines = [
        "### Arm totals",
        "",
        "| Arm | Cells | Full-suite rescues | Uncached input | Cached input | Output | Total tokens | Wall seconds |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for arm in ARMS:
        part = totals[arm]
        token_total = part["uncached"] + part["cached"] + part["output"]
        lines.append(
            f"| {arm} | {counts[arm]} | {rescue[arm]} | {part['uncached']:,} | "
            f"{part['cached']:,} | {part['output']:,} | {token_total:,} | {part['wall']:.3f} |"
        )
    lines.extend([
        "",
        f"Rescues: **REPAIR {rescue['REPAIR']}/8; CONTINUE {rescue['CONTINUE']}/8; "
        f"RESTART {rescue['RESTART']}/8**.",
        f"Rule: REPAIR − CONTINUE = **{delta}** (threshold ≥2); per-test no-regression recomputed "
        f"**{str(evidence['per_test_no_regression']).lower()}**. Result: "
        f"**{'observed KEEP for these eight selected failures' if keep else 'do not keep repair-with-verification'}**.",
        "The no-regression comparison is recomputed from [per-test-results.json](data/per-test-results.json); "
        "the public sets include names because the selected suites are exposed.",
        "",
        "### Scored cells",
        "",
        "| Cell ID | Original failure | Arm | Outcome | Test fraction | Patch SHA-256 | Started at (UTC) | Finished at (UTC) | Uncached input | Cached input | Output | Total tokens | Wall seconds |",
        "| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    arm_order = {arm: index for index, arm in enumerate(ARMS)}
    for row in sorted(scored, key=lambda item: (item["original_failure_cell_id"], arm_order[item["arm"]])):
        patch = row["patch_sha256"] or "—"
        lines.append(
            f"| {tick}{row['cell_id']}{tick} | {tick}{row['original_failure_cell_id']}{tick} | "
            f"{row['arm']} | {row['outcome']} | {row['tests_passed']}/{row['tests_total']} | "
            f"{tick}{patch}{tick} | {row['started_at']} | {row['finished_at']} | "
            f"{integer(row, 'uncached_input_tokens'):,} | {integer(row, 'cached_input_tokens'):,} | "
            f"{integer(row, 'output_tokens'):,} | {integer(row, 'total_tokens'):,} | "
            f"{decimal(row, 'wall_s'):.3f} |"
        )
    scored_tokens = sum(
        integer(row, field) for row in scored
        for field in ("uncached_input_tokens", "cached_input_tokens", "output_tokens")
    )
    source_tokens = sum(
        integer(row, field) for row in originals
        for field in ("uncached_input_tokens", "cached_input_tokens", "output_tokens")
    )
    scored_wall = sum((decimal(row, "wall_s") for row in scored), Decimal(0))
    source_wall = sum((decimal(row, "wall_s") for row in originals), Decimal(0))
    lines.extend([
        "",
        f"Scored attempts total: **{scored_tokens:,} tokens; {scored_wall:.3f} seconds**. "
        f"Including the eight original attempts once: **{scored_tokens + source_tokens:,} tokens; "
        f"{scored_wall + source_wall:.3f} seconds**.",
        "",
        "Patch hashes identify the delivered public patch for each matched failure; RESTART has no patch.",
    ])
    return "\n".join(lines)


def check_pages(generated: str, write: bool) -> None:
    text = RESULTS.read_text(encoding="utf-8")
    matches = list(re.finditer(re.escape(BEGIN) + r".*?" + re.escape(END), text, re.S))
    if len(matches) != 1:
        fail("RESULTS.md must contain exactly one generated block")
    block = f"{BEGIN}\n\n{generated}\n\n{END}"
    if write:
        RESULTS.write_text(text[:matches[0].start()] + block + text[matches[0].end():], encoding="utf-8")
    elif matches[0].group(0) != block:
        fail("RESULTS.md generated block differs from public data")

    readme = README.read_text(encoding="utf-8")
    required = (
        "STATUS: **VALID** — registered rule met (difference 2, threshold ≥2); KEEP applies to these eight selected failures only, with per-test evidence published.",
        "## Deviation DEV-1",
        "Label: VALID for the registered rule — raw captures not retained; results verified against official grades",
        "Rescues: **REPAIR 3/8; CONTINUE 1/8; RESTART 2/8**.",
        "Per-test no-regression is recomputed from the public pass/fail sets",
        PRIVATE_CHECK_SHA,
        "python3 rounds/l3b-repair-vs-continue/reproduce/l3b_repair_vs_continue.py",
    )
    if any(fragment not in readme for fragment in required):
        fail("README.md omits a required status, result, private-check citation, or command")
    if "STATUS: **VALID**" not in RESULTS.read_text(encoding="utf-8"):
        fail("RESULTS.md does not carry VALID status")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the data-derived RESULTS.md block")
    args = parser.parse_args()
    originals, scored, evidence = load_data()
    check_pages(render(originals, scored, evidence), write=args.write)
    rescue = Counter(row["arm"] for row in scored if row["outcome"] == "pass")
    print(
        f"L3b reproduction: PASS ({len(scored)} scored cells; "
        f"{rescue['REPAIR']} REPAIR, {rescue['CONTINUE']} CONTINUE, "
        f"{rescue['RESTART']} RESTART rescues; official grade counts verified)"
    )


if __name__ == "__main__":
    main()
