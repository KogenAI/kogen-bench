"""Recompute L3b's per-test no-regression condition from public evidence."""

from __future__ import annotations

import json
import csv
from pathlib import Path


ROUND = Path(__file__).resolve().parents[1]
EVIDENCE = ROUND / "data" / "per-test-results.json"


def load_per_test_results(path: Path = EVIDENCE) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("unsupported per-test evidence schema")
    cells = data.get("cells")
    if not isinstance(cells, list) or len(cells) != 32:
        raise ValueError("expected eight originals and 24 scored cells")
    by_id = {}
    for row in cells:
        cell_id = row.get("cell_id")
        passed, failed = row.get("passed_tests"), row.get("failed_tests")
        if not isinstance(cell_id, str) or cell_id in by_id:
            raise ValueError("cell IDs must be present and unique")
        if not isinstance(passed, list) or not isinstance(failed, list):
            raise ValueError(f"missing pass/fail sets for {cell_id}")
        if len(passed) != len(set(passed)) or len(failed) != len(set(failed)):
            raise ValueError(f"duplicate test names for {cell_id}")
        if set(passed) & set(failed):
            raise ValueError(f"overlapping pass/fail sets for {cell_id}")
        if len(passed) != row.get("tests_passed") or len(passed) + len(failed) != row.get("tests_total"):
            raise ValueError(f"per-test set sizes disagree with aggregate counts for {cell_id}")
        by_id[cell_id] = row
    with (ROUND / "data" / "original-failures.csv").open(newline="", encoding="utf-8") as stream:
        original_rows = list(csv.DictReader(stream))
    with (ROUND / "data" / "scored-cells.csv").open(newline="", encoding="utf-8") as stream:
        scored_rows = list(csv.DictReader(stream))
    expected = {r["original_failure_cell_id"]: ("ORIGINAL", r) for r in original_rows}
    expected.update({r["cell_id"]: (r["arm"], r) for r in scored_rows})
    if set(expected) != set(by_id):
        raise ValueError("per-test evidence IDs differ from the public selected-cell ledgers")
    for cell_id, (arm, source) in expected.items():
        row = by_id[cell_id]
        if row["arm"] != arm:
            raise ValueError(f"arm differs from selected-cell ledger for {cell_id}")
        if row["tests_passed"] != int(source["tests_passed"]) or row["tests_total"] != int(source["tests_total"]):
            raise ValueError(f"aggregate counts differ from selected-cell ledger for {cell_id}")
        original_id = source.get("original_failure_cell_id", cell_id)
        if row["original_failure_cell_id"] != original_id:
            raise ValueError(f"paired original differs from selected-cell ledger for {cell_id}")
    originals = [r for r in cells if r.get("arm") == "ORIGINAL"]
    repairs = [r for r in cells if r.get("arm") == "REPAIR"]
    if len(originals) != 8 or len(repairs) != 8:
        raise ValueError("expected one original and one REPAIR cell for each of eight pairs")
    original_by_id = {r["cell_id"]: r for r in originals}
    if len(original_by_id) != 8:
        raise ValueError("original failure IDs must be unique")
    if {r.get("arm") for r in cells} != {"ORIGINAL", "REPAIR", "CONTINUE", "RESTART"}:
        raise ValueError("unexpected arm in per-test evidence")
    for row in cells:
        if row.get("arm") == "ORIGINAL":
            if row.get("original_failure_cell_id") != row["cell_id"]:
                raise ValueError("original cell must refer to itself")
        elif row.get("original_failure_cell_id") not in original_by_id:
            raise ValueError(f"unknown original pair for {row['cell_id']}")
    return cells


def per_test_no_regression(cells: list[dict]) -> tuple[bool, list[dict]]:
    originals = {r["cell_id"]: r for r in cells if r["arm"] == "ORIGINAL"}
    repairs = [r for r in cells if r["arm"] == "REPAIR"]
    comparisons = []
    for repair in repairs:
        original_id = repair["original_failure_cell_id"]
        original_failed = set(originals[original_id]["failed_tests"])
        repair_failed = set(repair["failed_tests"])
        regressions = sorted(repair_failed - original_failed)
        comparisons.append({
            "original_failure_cell_id": original_id,
            "repair_cell_id": repair["cell_id"],
            "regressions": regressions,
            "no_regression": not regressions,
        })
    return all(row["no_regression"] for row in comparisons), comparisons
