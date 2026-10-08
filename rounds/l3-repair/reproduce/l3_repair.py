#!/usr/bin/env python3
"""Recompute the public L3 repair result block from the aggregate cell CSV."""
import csv
import re
import sys
from decimal import Decimal
from pathlib import Path

ROUND = Path(__file__).resolve().parents[1]
CSV_PATH = ROUND / "data" / "cells.csv"
RESULTS_PATH = ROUND / "RESULTS.md"
README_PATH = ROUND / "README.md"
DECISION_PATH = ROUND / "DECISION-RULE.md"
BEGIN = "<!-- BEGIN L3 GENERATED RESULTS -->"
END = "<!-- END L3 GENERATED RESULTS -->"
EXPECTED_REPAIRS = [
    "codex__gpt-6-luna__max__default__r70-2-elixir-l3r31__r1",
    "codex__gpt-6-luna__max__default__r70-2-elixir-l3r33__r1",
    "codex__gpt-6-luna__max__default__r70-2-go-l3r32__r1",
    "codex__gpt-6-luna__max__default__r70-5-go-l3r1__r1",
    "codex__gpt-6-luna__max__default__r70-5-go-l3r32__r1",
    "codex__gpt-6-luna__max__default__r70-7-rust-l3r31__r1",
]
EXPECTED_PROCESS = [
    "controls_attempt_1",
    "control_deployment_fix",
    "controls_attempt_2",
    "first_repair_attempt_1",
    "task_record_deployment_fix",
    "official_release_sequence",
]
TITLES = {
    "controls_attempt_1": "Admission controls, initial attempt",
    "control_deployment_fix": "Control deployment correction",
    "controls_attempt_2": "Admission controls, retry",
    "first_repair_attempt_1": "Initial scored-cell launch attempt",
    "task_record_deployment_fix": "Task-record deployment correction",
    "official_release_sequence": "Official release and grading sequence",
}


def stop(message):
    print("L3 repair reproduction: FAIL: " + message, file=sys.stderr)
    raise SystemExit(1)


def read_csv():
    try:
        with CSV_PATH.open(newline="", encoding="utf-8") as source:
            records = list(csv.DictReader(source))
    except (OSError, csv.Error) as exc:
        stop(f"cannot read {CSV_PATH.name}: {exc}")
    pairs = [row for row in records if row["kind"] == "pair"]
    process = [row for row in records if row["kind"] == "process"]
    if len(pairs) != 6:
        stop(f"expected six matched pairs, found {len(pairs)}")
    if [row["repair_cell_id"] for row in pairs] != EXPECTED_REPAIRS:
        stop("pair rows are missing, duplicated, or out of the preregistered order")
    if [row["process_step"] for row in process] != EXPECTED_PROCESS:
        stop("process log rows are missing, duplicated, or out of order")
    if len(records) != len(pairs) + len(process):
        stop("unknown record kind in cells.csv")
    for row in pairs:
        try:
            original_passed = int(row["original_passed"])
            original_total = int(row["original_total"])
            repair_passed = int(row["repair_passed"])
            repair_total = int(row["repair_total"])
            uncached = int(row["uncached_input_tokens"])
            cached = int(row["cached_input_tokens"])
            output = int(row["output_tokens"])
            total = int(row["total_tokens"])
            base_passes = int(row["other_base_passes"])
            base_n = int(row["other_base_n"])
            Decimal(row["wall_s"])
        except (TypeError, ValueError, ArithmeticError) as exc:
            stop(f"invalid numeric value for {row.get('repair_cell_id', 'pair')}: {exc}")
        if original_total <= 0 or repair_total <= 0 or base_n <= 0:
            stop(f"non-positive denominator for {row['repair_cell_id']}")
        if not (0 <= original_passed <= original_total and 0 <= repair_passed <= repair_total):
            stop(f"invalid test count for {row['repair_cell_id']}")
        if not (0 <= base_passes <= base_n):
            stop(f"invalid comparator rate for {row['repair_cell_id']}")
        if min(uncached, cached, output, total) < 0 or uncached + cached + output != total:
            stop(f"token sum mismatch for {row['repair_cell_id']}")
        if Decimal(row["wall_s"]) < 0:
            stop(f"negative wall time for {row['repair_cell_id']}")
        expected_outcome = "pass" if repair_passed == repair_total else "fail"
        if row["repair_outcome"] != expected_outcome:
            stop(f"outcome does not match full-pass rule for {row['repair_cell_id']}")
        if original_passed == original_total:
            stop(f"original cell is not a failure: {row['original_cell_id']}")
        for field in ("original_base_commit_sha", "variant_base_commit_sha"):
            if not re.fullmatch(r"[0-9a-f]{40}", row[field]):
                stop(f"invalid {field} for {row['repair_cell_id']}")
    return pairs, process


def comma(value):
    return f"{value:,}"


def render(pairs, process):
    n = len(pairs)
    rescues = sum(row["repair_outcome"] == "pass" for row in pairs)
    # The registered requirement is set preservation. Aggregate pass counts
    # cannot establish it, so leave the condition unknown without per-test data.
    no_regression = None
    uncached_sum = sum(int(row["uncached_input_tokens"]) for row in pairs)
    cached_sum = sum(int(row["cached_input_tokens"]) for row in pairs)
    output_sum = sum(int(row["output_tokens"]) for row in pairs)
    total_sum = sum(int(row["total_tokens"]) for row in pairs)
    wall_sum = sum((Decimal(row["wall_s"]) for row in pairs), Decimal(0))
    decision = "repair-with-verification remains budget-limited" if rescues < 3 or no_regression is not True else "repair-with-verification may be retained"

    lines = [
        "## Matched pair results",
        "",
        "| Task ID | Exact arm | Original cell ID | Original tests | Repair cell ID | Outcome | Repair tests | wall_s | Uncached | Cached | Output | Total tokens |",
        "| --- | --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in pairs:
        lines.append(
            f"| `{row['task_id']}` | Arm A → Arm B | `{row['original_cell_id']}` | "
            f"{row['original_passed']}/{row['original_total']} | `{row['repair_cell_id']}` | "
            f"{row['repair_outcome'].upper()} | "
            f"{row['repair_passed']}/{row['repair_total']} | {Decimal(row['wall_s']):.3f} | "
            f"{comma(int(row['uncached_input_tokens']))} | {comma(int(row['cached_input_tokens']))} | "
            f"{comma(int(row['output_tokens']))} | {comma(int(row['total_tokens']))} |"
        )
    lines.extend([
        f"| **Total** | — | — | — | — | **{rescues}/{n} rescues** | — | **{wall_sum:.3f}** | "
        f"**{comma(uncached_sum)}** | **{comma(cached_sum)}** | **{comma(output_sum)}** | **{comma(total_sum)}** |",
        "",
        "## Independent base pass rates",
        "",
        "Each rate uses the same task and stack's other official reps, excluding that pair's original cell; invalidated rows and reps at or above 700 are excluded.",
        "",
    ])
    for row in pairs:
        lines.append(
            f"- `{row['task_id']}` / original `{row['original_cell_id']}`: "
            f"**{row['other_base_passes']}/{row['other_base_n']}** across "
            f"{row['other_base_n']} other official reps."
        )
    lines.extend([
        "",
        "## Decision",
        "",
        f"Rescues: **{rescues}/{n}**. The preregistered threshold is **at least 3/6**; it was not met, so {decision}.",
        "Per-test no-regression requirement: **UNVERIFIABLE**; per-test grade results are not present in this public bundle. Aggregate pass counts are a separate diagnostic and cannot establish that every previously passed check was preserved.",
        f"Aggregate count diagnostic: **{'PASS' if all(int(row['repair_passed']) >= int(row['original_passed']) for row in pairs) else 'FAIL'}**; these counts do not determine the no-regression condition.",
        "Token definition: uncached input + cached input + output; total is their sum.",
        "",
        "## Process log",
        "",
    ])
    for row in process:
        lines.append(f"- **{TITLES[row['process_step']]}:** {row['details']}")
    return "\n".join(lines)


def validate_pages(pairs, generated, write=False):
    try:
        results = RESULTS_PATH.read_text(encoding="utf-8")
        readme = README_PATH.read_text(encoding="utf-8")
        decision = DECISION_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        stop(f"cannot read round page: {exc}")
    expected_block = f"{BEGIN}\n\n{generated}\n\n{END}"
    matches = list(re.finditer(re.escape(BEGIN) + r".*?" + re.escape(END), results, re.S))
    if len(matches) != 1:
        stop("RESULTS.md must contain exactly one generated-results block")
    if write:
        RESULTS_PATH.write_text(results[:matches[0].start()] + expected_block + results[matches[0].end():], encoding="utf-8")
    elif matches[0].group(0) != expected_block:
        stop("RESULTS.md generated block differs from data/cells.csv")
    n = len(pairs)
    rescues = sum(row["repair_outcome"] == "pass" for row in pairs)
    expected_n = f"n: **{n} matched failures**"
    expected_headline = f"Headline: **{rescues}/{n} repairs rescued; the ≥3/6 threshold was not met, so repair-with-verification remains budget-limited.**"
    if expected_n not in readme or expected_headline not in readme:
        stop("README.md pair count or headline differs from data/cells.csv")
    if any("STATUS: **DESCRIPTIVE**" not in page for page in (readme, results, decision)):
        stop("all round pages must carry STATUS: DESCRIPTIVE")
    if "at least 3 of 6 repairs rescue" not in decision:
        stop("DECISION-RULE.md no longer states the preregistered threshold")
    runner_versions = {row["runner_version"] for row in pairs}
    cli_versions = {row["codex_cli_version"] for row in pairs}
    if len(runner_versions) != 1 or f"Python `{next(iter(runner_versions))}`" not in readme:
        stop("README.md runner version differs from data/cells.csv")
    if len(cli_versions) != 1 or next(iter(cli_versions)) not in readme:
        stop("README.md Codex CLI version differs from data/cells.csv")
    for row in pairs:
        for sha in (row["original_base_commit_sha"], row["variant_base_commit_sha"]):
            link = f"https://github.com/KogenAI/kogen-ex/commit/{sha}"
            if link not in readme:
                stop(f"README.md is missing commit link for {sha}")
        if row["task_id"] not in readme:
            stop(f"README.md is missing task ID {row['task_id']}")
    if "rounds/l3-repair/data/cells.csv" not in readme or "rounds/l3-repair/reproduce/l3_repair.py" not in readme:
        stop("README.md must identify the aggregate data and reproducer files")
    if "python3 rounds/l3-repair/reproduce/l3_repair.py" not in readme:
        stop("README.md is missing the exact reproduction command")


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the CSV-derived RESULTS.md block")
    args = parser.parse_args()
    pairs, process = read_csv()
    generated = render(pairs, process)
    validate_pages(pairs, generated, write=args.write)
    print(f"L3 repair reproduction: PASS ({len(pairs)} matched pairs; {sum(row['repair_outcome'] == 'pass' for row in pairs)} rescues; official grade counts verified)")


if __name__ == "__main__":
    main()
