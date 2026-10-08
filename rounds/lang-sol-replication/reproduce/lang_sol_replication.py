#!/usr/bin/env python3
"""Recompute and validate the public Sol-medium replication results."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = ROUND_DIR / "data" / "cells.csv"
RESULTS_PATH = ROUND_DIR / "RESULTS.md"
README_PATH = ROUND_DIR / "README.md"
DECISION_PATH = ROUND_DIR / "DECISION-RULE.md"
DESIGN_PATH = ROUND_DIR / "DESIGN.md"
SOURCE_SHA256 = "c9394487c2a139ff57e98fe8c9d5c44d6f6b5e7b33d1a33abba87479fb575892"
PREFIX = "codex__gpt-6.1-sol__medium__default__"
STACKS = ("rust", "go", "ts-bun")
STACK_LABELS = {"rust": "Rust", "go": "Go", "ts-bun": "TS-Bun"}
NEW_TASKS = (
    "r70-1-rust", "r70-2-rust", "r70-4-rust-fe2",
    "r70-1-go", "r70-2-go", "r70-4-go-fe2",
    "r70-1-ts-bun", "r70-2-ts-bun", "r70-4-ts-bun-fe2",
)
NEW_TASKS_BY_STACK = {
    "rust": ("r70-1-rust", "r70-2-rust", "r70-4-rust-fe2"),
    "go": ("r70-1-go", "r70-2-go", "r70-4-go-fe2"),
    "ts-bun": ("r70-1-ts-bun", "r70-2-ts-bun", "r70-4-ts-bun-fe2"),
}
EXPECTED_FIELDS = (
    "cell_id", "cohort", "task", "stack", "rep", "host", "outcome",
    "tests_passed", "tests_total", "uncached", "cached", "output",
    "total_tokens", "wall_s", "grade_window_at", "base_sha", "cli_version",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL: " + message)


def int_field(row: dict[str, str], name: str) -> int | None:
    value = row.get(name, "")
    return None if value == "" else int(value)


def read_cells() -> list[dict[str, str]]:
    with CSV_PATH.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        require(tuple(reader.fieldnames or ()) == EXPECTED_FIELDS, "cells.csv columns changed")
        rows = list(reader)

    require(len(rows) == 58, f"expected 58 exact scoped rows, found {len(rows)}")
    ids = [row["cell_id"] for row in rows]
    require(len(ids) == len(set(ids)), "cell IDs must be unique")

    expected_new = {
        f"{PREFIX}{task}__r{rep}"
        for task in NEW_TASKS for rep in (1, 2, 3)
    }
    expected_reused = set()
    for task_num in (5, 6, 7):
        for stack in STACKS:
            task = f"r70-{task_num}-{stack}"
            max_rep = 4 if task_num in (5, 6) and stack in ("rust", "go") else 3
            expected_reused.update(f"{PREFIX}{task}__r{rep}" for rep in range(1, max_rep + 1))
    expected_ids = expected_new | expected_reused
    require(set(ids) == expected_ids, "cells.csv is not exactly the 27 new and 31 reused IDs")

    for row in rows:
        cid = row["cell_id"]
        require(cid == f'{PREFIX}{row["task"]}__r{row["rep"]}', f"cell identity fields mismatch: {cid}")
        require(row["cohort"] == ("new" if cid in expected_new else "reused"), f"cohort mismatch: {cid}")
        require(row["stack"] in STACKS, f"unknown stack: {cid}")
        require(row["outcome"] in ("pass", "fail", "invalid"), f"unknown outcome: {cid}")
        require(row["host"] in ("kogen-bench-eu", "kogen-bench-us"), f"unknown host: {cid}")
        require(len(row["base_sha"]) == 40 and re.fullmatch(r"[0-9a-f]{40}", row["base_sha"]) is not None,
                f"missing exact Kogen task commit: {cid}")
        require(row["cli_version"] == "codex-cli 0.160.0", f"CLI version mismatch: {cid}")
        datetime.fromisoformat(row["grade_window_at"].replace("Z", "+00:00"))
        passed = int_field(row, "tests_passed")
        total = int_field(row, "tests_total")
        require(passed is not None and total is not None and 0 <= passed <= total,
                f"invalid test counts: {cid}")
        if row["outcome"] != "invalid":
            expected_outcome = "pass" if passed == total else "fail"
            require(row["outcome"] == expected_outcome,
                    f"official grade outcome differs from its full-pass test counts: {cid}")
        numeric_usage = [int_field(row, key) for key in ("uncached", "cached", "output")]
        total_tokens = int_field(row, "total_tokens")
        if any(value is None for value in numeric_usage):
            require(all(value is None for value in numeric_usage) and total_tokens is None,
                    f"partial token values: {cid}")
        else:
            require(total_tokens == sum(value for value in numeric_usage if value is not None),
                    f"token total must equal uncached + cached + output: {cid}")
        if row["cohort"] == "new":
            expected_host = "kogen-bench-eu" if row["stack"] == "rust" else "kogen-bench-us"
            require(row["host"] == expected_host, f"new-cell host split mismatch: {cid}")
            require(all(value is not None for value in numeric_usage) and total_tokens is not None,
                    f"new cell is missing token values: {cid}")
            require(row["wall_s"] != "", f"new cell is missing wall time: {cid}")

    require(sum(row["cohort"] == "new" for row in rows) == 27, "new cohort must contain 27 rows")
    require(sum(row["cohort"] == "reused" for row in rows) == 31, "reused cohort must contain 31 rows")
    return rows


def summary(rows: list[dict[str, str]]) -> dict[str, dict[str, object]]:
    result = {}
    for stack in STACKS:
        new_rows = [row for row in rows if row["cohort"] == "new" and row["stack"] == stack]
        reused_rows = [row for row in rows if row["cohort"] == "reused" and row["stack"] == stack]
        combined_rows = new_rows + reused_rows
        result[stack] = {
            "new": new_rows,
            "reused": reused_rows,
            "combined": combined_rows,
            "new_passes": sum(row["outcome"] == "pass" for row in new_rows),
            "reused_passes": sum(row["outcome"] == "pass" for row in reused_rows),
            "combined_passes": sum(row["outcome"] == "pass" for row in combined_rows),
            "equal_task_rate": equal_task_rate(combined_rows),
            "median_tokens": int(statistics.median(int(row["total_tokens"]) for row in new_rows)),
            "median_wall": statistics.median(float(row["wall_s"]) for row in new_rows),
        }
    return result


def equal_task_rate(rows: list[dict[str, str]]) -> float:
    """Post-hoc mean of per-task pass fractions; each task has equal weight."""
    by_task: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_task[row["task"]].append(row)
    rates = [
        sum(row["outcome"] == "pass" for row in task_rows) / len(task_rows)
        for task_rows in by_task.values()
    ]
    return statistics.mean(rates) if rates else 0.0


def comma_int(value: int) -> str:
    return f"{value:,}"


def render_results(rows: list[dict[str, str]]) -> str:
    stats = summary(rows)
    new_rows = [row for row in rows if row["cohort"] == "new"]
    reused_rows = [row for row in rows if row["cohort"] == "reused"]
    new_order = {task: i for i, task in enumerate(NEW_TASKS)}
    old_order = {5: 0, 6: 1, 7: 2}
    stack_order = {stack: i for i, stack in enumerate(STACKS)}

    def new_key(row: dict[str, str]) -> tuple[int, int, int]:
        return (stack_order[row["stack"]], new_order[row["task"]] % 3, int(row["rep"]))

    def old_key(row: dict[str, str]) -> tuple[int, int, int]:
        task_num = int(row["task"].split("-")[1])
        return (stack_order[row["stack"]], old_order[task_num], int(row["rep"]))

    lines = [
        "# Sol-medium language replication results",
        "",
        "STATUS: **DESCRIPTIVE** — raw rates are reported; the combined registered decision is UNRESOLVED.",
        "",
        "Release label: DESCRIPTIVE — raw captures not retained; results verified against official grades",
        "",
        "The primary outcome is the latest official hidden-suite full-pass grade per exact cell ID. The public data contains 27 new cells and 31 reused t5–t7 cells; no reused cell was rerun. The frozen design text states 36 existing t5–t7 cells, while the exact eligible official IDs resolve to 31 (Rust 11, Go 11, TS-Bun 9). The results below use the exact-ID ledger rows.",
        "",
        "Token accounting: uncached = usage.input; total tokens = uncached + cached + output. The grade-window timestamp is UTC. Wall times are comparable only within a host.",
        "",
        "The two host smoke-gate receipts show all nine rep-1 task-by-stack cells were officially graded before bulk reps. Both host gates passed; the TS-Bun t4-fe2 rep-1 scored 17/18 and remains a FAIL outcome. The lane receipt says its full Standard-record strict check was deferred until analysis under an emitter-gap exception; the exception receipt itself is not in this public bundle.",
        "",
        "<!-- R70-LANG-SOL-REPLICATION:BEGIN -->",
        "## New cells",
        "",
        "| Exact cell ID | Task | Stack | Rep | Host | Outcome | Hidden tests passed/total | Uncached | Cached | Output | Total tokens | wall_s | Grade window (UTC) |",
        "| --- | --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in sorted(new_rows, key=new_key):
        tests = f'{int_field(row, "tests_passed")}/{int_field(row, "tests_total")}'
        lines.append(
            f'| {row["cell_id"]} | {task_label(row["task"])} | {STACK_LABELS[row["stack"]]} | '
            f'{row["rep"]} | {row["host"]} | {row["outcome"].upper()} | {tests} | '
            f'{comma_int(int_field(row, "uncached") or 0)} | {comma_int(int_field(row, "cached") or 0)} | '
            f'{comma_int(int_field(row, "output") or 0)} | {comma_int(int_field(row, "total_tokens") or 0)} | '
            f'{row["wall_s"]} | {row["grade_window_at"]} |'
        )

    lines.extend([
        "",
        "## Reused t5–t7 cells",
        "",
        "These are the latest official Sol-medium rows for the named stacks. INVALID is retained in the denominator as a non-pass; no outcome has been inferred from test names or grader content.",
        "",
        "| Exact cell ID | Task | Stack | Rep | Outcome |",
        "| --- | --- | --- | ---: | --- |",
    ])
    for row in sorted(reused_rows, key=old_key):
        lines.append(
            f'| {row["cell_id"]} | {task_label(row["task"])} | {STACK_LABELS[row["stack"]]} | '
            f'{row["rep"]} | {row["outcome"].upper()} |'
        )

    lines.extend([
        "",
        "## Per-stack summary",
        "",
        "| Stack | New passes | Reused passes | Combined raw passes | Equal-task combined pass rate (post-hoc) | Median total tokens/cell (new) | Median wall_s (new) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for stack in STACKS:
        item = stats[stack]
        lines.append(
            f'| {STACK_LABELS[stack]} | {item["new_passes"]}/{len(item["new"])} | '
            f'{item["reused_passes"]}/{len(item["reused"])} | '
            f'{item["combined_passes"]}/{len(item["combined"])} | '
            f'{float(item["equal_task_rate"])*100:.1f}% | '
            f'{comma_int(int(item["median_tokens"]))} | {float(item["median_wall"]):.1f} |'
        )

    rust = stats["rust"]
    best_new = max(stats["go"]["new_passes"], stats["ts-bun"]["new_passes"])
    new_trigger = best_new - rust["new_passes"] >= 3
    rule_triggered = new_trigger
    lines.extend([
        "",
        "## Verdict",
        "",
        f'Rust records {rust["new_passes"]}/{len(rust["new"])} new passes; the best of Go and TS-Bun records {best_new}/{len(stats["go"]["new"])}. '
        f'Combined raw official pass counts are Rust {rust["combined_passes"]}/{len(rust["combined"])}, '
        f'Go {stats["go"]["combined_passes"]}/{len(stats["go"]["combined"])}, and '
        f'TS-Bun {stats["ts-bun"]["combined_passes"]}/{len(stats["ts-bun"]["combined"])}. '
        f'The equal-task means are Rust {float(rust["equal_task_rate"])*100:.1f}%, '
        f'Go {float(stats["go"]["equal_task_rate"])*100:.1f}%, and '
        f'TS-Bun {float(stats["ts-bun"]["equal_task_rate"])*100:.1f}%.',
        "",
        "The new-cell threshold is not triggered: Rust is 8/9 and the best of Go and TS-Bun is 7/9, fewer than three passes apart. The combined branch says ‘equalized per task’ but records no formula or scale for its four-pass threshold, so it cannot be applied. The equal-task mean above is a post-hoc sensitivity summary. **COMBINED DECISION: UNRESOLVED.**",
        "",
        "Limit: small n, one model per arm, and a decision rule designed to detect only large reversals.",
        "",
        "<!-- R70-LANG-SOL-REPLICATION:END -->",
    ])
    require(not rule_triggered, "the recorded outcome would trigger the stated threshold")
    return "\n".join(lines)


def task_label(task: str) -> str:
    parts = task.split("-")
    task_num = parts[1]
    return "t4-fe2" if task_num == "4" else f"t{task_num}"


def verify_design_copy() -> None:
    data = DESIGN_PATH.read_bytes()
    require(b"Sanitized public presentation" in data, "DESIGN.md must identify the sanitized presentation")
    require(SOURCE_SHA256.encode() in data, "original source SHA-256 provenance missing")
    require(b"does not hash this sanitized presentation" in data,
            "DESIGN.md must distinguish original-source hash provenance from this edited presentation")
    require(b"36 Sol-medium cells" in data, "frozen design source count not preserved")


def verify_readme(rows: list[dict[str, str]]) -> None:
    text = README_PATH.read_text(encoding="utf-8")
    require("27 new cells" in text and "31 reused" in text, "README sample counts do not match CSV")
    require("58 exact cell IDs" in text, "README total cell count does not match CSV")
    for label in ("Planned new cells", "Started new cells", "Finished new cells", "Officially graded new cells", "ITT denominator for new cells"):
        require(f"| {label} | 27 |" in text, f"README integer accounting mismatch: {label}")
    require("36" in text, "README must disclose the frozen-design reuse estimate")
    require("Rust 8/9" in text and "Go 7/9" in text and "TS-Bun 6/9" in text,
            "README new-cell headline does not match CSV")
    require("Rust 18/20" in text and "Go 18/20" in text and "TS-Bun 15/18" in text,
            "README combined headline does not match CSV")
    require("90.3%" in text and "88.9%" in text and "83.3%" in text,
            "README is missing the equal-task sensitivity rates")
    require("post-hoc" in text and "formula" in text,
            "README must label the unregistered equal-task formula as post-hoc")
    for row in rows:
        link = "https://github.com/KogenAI/kogen-ex/commit/" + row["base_sha"]
        require(link in text, f"README missing exact task commit for {row['task']}")
        require(row["task"] in text, f"README missing task ID {row['task']}")
    require("github.com/KogenAI/kogen/" not in text, "README contains a disallowed Kogen repository link")
    for value in (text, RESULTS_PATH.read_text(encoding="utf-8"), DECISION_PATH.read_text(encoding="utf-8")):
        require("/Users/" not in value and "/home/" not in value, "public page contains a local path")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the CSV-derived RESULTS.md")
    args = parser.parse_args()

    rows = read_cells()
    verify_design_copy()
    expected = render_results(rows)
    if args.write:
        RESULTS_PATH.write_text(expected, encoding="utf-8")
    else:
        require(RESULTS_PATH.exists(), "RESULTS.md is missing")
        require(RESULTS_PATH.read_text(encoding="utf-8") == expected,
                "RESULTS.md differs from the CSV-derived result page")
        verify_readme(rows)

    print("OK: 58 exact cell rows; 27 new, 31 reused; official grade counts verified and result tables match cells.csv.")


if __name__ == "__main__":
    main()
