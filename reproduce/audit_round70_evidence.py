#!/usr/bin/env python3
"""Reconcile Round 70 language outcomes from the sanitized public receipt ledgers."""
import json
import math
import re
from datetime import datetime, timezone
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
STACKS = ("rust", "elixir", "go", "ts-bun")
STACK_LABELS = {
    "rust": "Rust",
    "elixir": "Elixir",
    "go": "Go",
    "ts-bun": "TypeScript/Bun",
}
TASKS_EXT = {f"r70-{task}-{stack}" for task in (2, 5, 7) for stack in STACKS}
TASKS_ORIGINAL = {f"r70-{task}-{stack}" for task in (1, 3, 4, 6) for stack in STACKS}
TASKS_RERUN = {"r70-1-elixir-fe2"} | {f"r70-4-{stack}-fe2" for stack in STACKS}
CAUSES = {
    None,
    "hidden_test_failure",
    "timeout",
    "patch_application_failure",
    "build_failure",
    "setup_failure",
    "infrastructure_failure",
}


def read_jsonl(path):
    rows = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.name}:{number}: invalid JSON: {exc}") from exc
    return rows


def fraction(rows):
    return f"{sum(row.get('outcome') == 'pass' for row in rows)}/{len(rows)}"


def tests_fraction(row):
    return f"{row['tests_passed']}/{row['tests_total']}"


def has_fragment(text, fragment):
    return fragment in text


def parsed_time(value):
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def export_join_errors(test_rows, export_rows, cohort):
    """Match supplemental official grades to their sanitized outcome-export rows."""
    expected_round = cohort
    expected = {}
    errors = []
    for row in test_rows:
        cell_id = row.get("cell_id", "")
        parts = cell_id.split("__")
        if len(parts) != 6:
            errors.append(f"{cell_id}: malformed full cell identity")
            continue
        task = row.get("task")
        if parts[4] != task or parts[5] != "r" + str(row.get("rep")):
            errors.append(f"{cell_id}: test-count task or repetition differs from exact cell identity")
            continue
        export_task = task[:-4] if cohort == "r70-rve-rerun" and task.endswith("-fe2") else task
        key = (expected_round, export_task, row.get("stack"), str(row.get("rep")))
        if key in expected:
            errors.append(f"{cell_id}: duplicate supplemental task/arm/repetition identity")
        expected[key] = (row, parts)

    relevant = [row for row in export_rows if row.get("round") == expected_round]
    actual = defaultdict(list)
    for row in relevant:
        key = (row.get("round"), row.get("task"), row.get("arm"), str(row.get("rep")))
        actual[key].append(row)

    for key in sorted(set(expected) - set(actual)):
        errors.append(f"{cohort}: missing exported row for task/arm/rep {key[1:]}")
    for key in sorted(set(actual) - set(expected)):
        errors.append(f"{cohort}: extra exported row without a test-count identity {key[1:]}")
    for key in sorted(set(expected) & set(actual)):
        test, parts = expected[key]
        rows = actual[key]
        if len(rows) != 1:
            errors.append(f"{test['cell_id']}: {len(rows)} exported rows match the full task/arm/rep identity")
            continue
        exported = rows[0]
        checks = {
            "outcome": test.get("outcome"),
            "arm": test.get("stack"),
            "task": key[1],
            "rep": str(test.get("rep")),
            "harness": parts[0],
            "model": parts[1],
            "effort": parts[2],
        }
        for field, value in checks.items():
            if exported.get(field) != value:
                errors.append(f"{test['cell_id']}: exported {field} {exported.get(field)!r} differs from {value!r}")
        export_scored = exported.get("ITT outcome") != "not_scored"
        if export_scored is not test.get("scored"):
            errors.append(f"{test['cell_id']}: exported scored status differs from test-count ledger")
    return errors


def self_test():
    """Check claim matching and detect missing or mutated exported cell rows."""
    expected = "| Rust | 5/6 |"
    fixture = "| Stack | Reps |\n| --- | ---: |\n| Rust | 5/6 |\n"
    if not has_fragment(fixture, expected):
        raise RuntimeError("Round 70 evidence self-test rejected a matching fixture")
    mutated = fixture.replace("5/6", "4/6", 1)
    if has_fragment(mutated, expected):
        raise RuntimeError("Round 70 evidence self-test accepted a mutated count")
    sample_tests = [
        {"cell_id": "rust-31", "stack": "rust", "host": "kogen-bench-eu", "rep": 31},
        {"cell_id": "rust-32", "stack": "rust", "host": "kogen-bench-eu", "rep": 32},
        {"cell_id": "rust-33", "stack": "rust", "host": "kogen-bench-eu", "rep": 33},
    ]
    sample_costs = {
        "rust-31": {"total_tokens": 20, "wall_s": 2},
        "rust-32": {"total_tokens": 40, "wall_s": 4},
        "rust-33": {"total_tokens": 50, "wall_s": 8},
    }
    sample_summary = summarize_extension_costs(sample_tests, sample_costs)
    cost_line = render_cost_time_line("rust", sample_summary["rust"])
    cost_fixture = f"| Stack | Host | Headline | Headline wall | Post-hoc | Post-hoc wall |\n{cost_line}\n"
    if cost_line != "| Rust | kogen-bench-eu | 30 | 3 | 40 | 4 |" or cost_line not in cost_fixture:
        raise RuntimeError("Round 70 evidence self-test rejected matching cost-time medians")
    mutated_cost_fixture = cost_fixture.replace("| 40 | 4 |", "| 41 | 4 |", 1)
    if cost_line in mutated_cost_fixture:
        raise RuntimeError("Round 70 evidence self-test accepted mutated cost-time medians")
    test_row = {
        "cell_id": "codex__gpt-6-luna__max__default__r70-2-rust__r31",
        "cohort": "r70-rve-ext", "task": "r70-2-rust", "stack": "rust", "rep": 31,
        "outcome": "pass", "scored": True,
    }
    export_row = {
        "round": "r70-rve-ext", "task": "r70-2-rust", "arm": "rust", "rep": "31",
        "outcome": "pass", "ITT outcome": "pass", "harness": "codex", "model": "gpt-6-luna", "effort": "max",
    }
    if export_join_errors([test_row], [export_row], "r70-rve-ext"):
        raise RuntimeError("Round 70 evidence self-test rejected a matching export row")
    mutations = (
        [],
        [{**export_row, "outcome": "fail"}],
        [{**export_row, "arm": "go"}],
        [{**export_row, "task": "r70-5-rust"}],
        [{**export_row, "rep": "32"}],
        [{**export_row, "ITT outcome": "not_scored"}],
    )
    if any(not export_join_errors([test_row], case, "r70-rve-ext") for case in mutations):
        raise RuntimeError("Round 70 evidence self-test accepted a missing or mutated export row")
    rerun_test = {
        "cell_id": "codex__gpt-6-luna__max__default__r70-4-rust-fe2__r9",
        "cohort": "r70-rve-rerun", "task": "r70-4-rust-fe2", "stack": "rust", "rep": 9,
        "outcome": "pass", "scored": True,
    }
    rerun_export = {
        "round": "r70-rve-rerun", "task": "r70-4-rust", "arm": "rust", "rep": "9",
        "outcome": "pass", "ITT outcome": "pass", "harness": "codex", "model": "gpt-6-luna", "effort": "max",
    }
    if export_join_errors([rerun_test], [rerun_export], "r70-rve-rerun"):
        raise RuntimeError("Round 70 evidence self-test rejected a matching FE2 export row")
    if not export_join_errors([rerun_test], [{**rerun_export, "outcome": "fail"}], "r70-rve-rerun"):
        raise RuntimeError("Round 70 evidence self-test accepted a mutated FE2 export row")


def load_ledgers(root, errors):
    try:
        tests = read_jsonl(root / "results/test-counts.jsonl")
        controls = read_jsonl(root / "results/controls.jsonl")
    except (OSError, ValueError) as exc:
        errors.append(f"Round 70 evidence ledger cannot be read: {exc}")
        return [], []
    return tests, controls


def control_summary(rows, control_type, variant):
    matches = [row for row in rows if row["control_type"] == control_type and row["variant"] == variant]
    if not matches:
        return "not run"
    counts = Counter((row["outcome"], row["tests_passed"], row["tests_total"]) for row in matches)
    if len(counts) == 1:
        (outcome, passed, total), n = next(iter(counts.items()))
        if n == 1:
            return f"1 {outcome}, {passed}/{total}"
        return f"{n} {outcome}, each {passed}/{total}"
    parts = []
    for (outcome, passed, total), n in sorted(counts.items()):
        parts.append(f"{n} {outcome} at {passed}/{total}")
    return "; ".join(parts)


def validate_rows(tests, controls, errors):
    test_ids = [row.get("cell_id") for row in tests]
    control_ids = [row.get("cell_id") for row in controls]
    if len(test_ids) != len(set(test_ids)):
        errors.append("Duplicate exact cell ID in results/test-counts.jsonl")
    if len(control_ids) != len(set(control_ids)):
        errors.append("Duplicate exact cell ID in results/controls.jsonl")

    for row in tests:
        if row.get("outcome") not in {"pass", "fail", "invalid"}:
            errors.append("Invalid official outcome in test-count ledger")
        if row.get("failure_cause_class") not in CAUSES:
            errors.append("Unmapped failure class in test-count ledger")
        if not isinstance(row.get("scored"), bool) or not isinstance(row.get("cohort"), str):
            errors.append("Malformed scored flag in test-count ledger")
        if row.get("tests_ran") not in {True, False}:
            errors.append("Missing tests_ran flag in test-count ledger")
        if not isinstance(row.get("runner_status"), str) or not row["runner_status"]:
            errors.append("Missing runner status in test-count ledger")
        time_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)"
        for field in ("grade_started_at", "grade_finished_at", "window_snapshot_at"):
            if not re.fullmatch(time_pattern, str(row.get(field) or "")):
                errors.append(f"Test-count row has no valid {field}")
        started = parsed_time(row.get("grade_started_at"))
        finished = parsed_time(row.get("grade_finished_at"))
        snapshot = parsed_time(row.get("window_snapshot_at"))
        if started and finished and started > finished:
            errors.append("Test-count grade start is after its grade finish")
        if finished and snapshot and finished > snapshot:
            errors.append("Test-count grade finish is after its matching window snapshot")
        for field in ("tests_passed", "tests_total"):
            if not isinstance(row.get(field), int) or row[field] < 0:
                errors.append("Missing or invalid hidden-test count in test-count ledger")
        if row.get("tests_ran") is True and row.get("tests_passed", 0) > row.get("tests_total", 0):
            errors.append("Passed-test count exceeds total in test-count ledger")
        if row.get("tests_ran") is False and (row.get("tests_passed"), row.get("tests_total")) != (0, 0):
            errors.append("A non-run grade must retain its official 0/0 count")
        if row.get("host") not in {"kogen-bench-us", "kogen-bench-eu"}:
            errors.append("Unapproved public host label in test-count ledger")
        if row.get("window_snapshot_at") == "not_recorded":
            errors.append("Test-count row has no matching grade-window snapshot")
        if row.get("grade_selection") != "latest official row per exact cell_id":
            errors.append("Test-count row does not declare latest-row selection")

    for row in controls:
        if row.get("outcome") not in {"pass", "fail", "invalid"}:
            errors.append("Invalid official outcome in controls ledger")
        if row.get("failure_cause_class") not in CAUSES:
            errors.append("Unmapped failure class in controls ledger")
        if row.get("scored") is not False:
            errors.append("A control row is marked scored")
        if row.get("tests_ran") not in {True, False}:
            errors.append("Missing tests_ran flag in controls ledger")
        if not isinstance(row.get("source"), str) or not row["source"]:
            errors.append("Missing public source label in controls ledger")
        for field in ("tests_passed", "tests_total"):
            if not isinstance(row.get(field), int) or row[field] < 0:
                errors.append("Missing or invalid hidden-test count in controls ledger")
        if row.get("host") not in {"kogen-bench-us", "kogen-bench-eu"}:
            errors.append("Unapproved public host label in controls ledger")
        time_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)"
        if not re.fullmatch(time_pattern, str(row.get("window_time") or "")):
            errors.append("Control row has no official grade-window time")
        if not re.fullmatch(time_pattern, str(row.get("window_snapshot_at") or "")):
            errors.append("Control row has no matching public window-capture time")
        window_time = parsed_time(row.get("window_time"))
        snapshot_time = parsed_time(row.get("window_snapshot_at"))
        if window_time and snapshot_time and window_time > snapshot_time:
            errors.append("Control grade-window start is after its matching window snapshot")
        expected_window_id = f"{row.get('host')}@{row.get('window_snapshot_at')}"
        if row.get("window_id") != expected_window_id:
            errors.append("Control window ID does not identify its public host and snapshot timestamp")
        if row.get("window_snapshot_at") == "not_recorded":
            errors.append("Control row has no matching grade-window snapshot")
        digest = row.get("patch_sha256")
        if digest not in {"no_patch", "not_published"} and not re.fullmatch(r"[a-f0-9]{64}", str(digest or "")):
            errors.append("Invalid patch SHA-256 representation in controls ledger")
        if row.get("grade_selection") != "latest official row per exact cell_id":
            errors.append("Control row does not declare latest-row selection")

    expected_test_counts = {
        "r70-original-rve": 40,
        "r70-rve-rerun": 15,
        "r70-rve-ext": 29,
        "r70-task8-v1-smoke": 2,
        "r70-task8-v2-smoke": 2,
    }
    for cohort, expected in expected_test_counts.items():
        actual = sum(row.get("cohort") == cohort for row in tests)
        if actual != expected:
            errors.append(f"{cohort} test-count rows {actual}, expected {expected}")

    expected_controls = {
        ("r70-rve-rerun", "admission"): 30,
        ("r70-rve-rerun", "x-control"): 6,
        ("r70-rve-ext", "admission"): 48,
        ("r70-rve-ext", "x-control"): 12,
        ("r70-task8-v1", "admission"): 20,
        ("r70-task8-v1", "x-control"): 2,
        ("r70-task8-v2", "admission"): 4,
    }
    for (cohort, kind), expected in expected_controls.items():
        actual = sum(row.get("cohort") == cohort and row.get("control_type") == kind for row in controls)
        if actual != expected:
            errors.append(f"{cohort} {kind} control rows {actual}, expected {expected}")

    if len(tests) != sum(expected_test_counts.values()):
        errors.append("Unexpected test-count ledger row outside the registered cohorts")
    if len(controls) != sum(expected_controls.values()):
        errors.append("Unexpected controls ledger row outside the registered cohorts")


def validate_public_identities(root, tests, errors):
    def read_plan(rel):
        try:
            plan = json.loads((root / rel).read_text())
            ids = plan.get("cell_ids")
            if not isinstance(ids, list) or not all(isinstance(cid, str) for cid in ids):
                raise ValueError("cell_ids must be a list of exact IDs")
            if len(ids) != len(set(ids)) or len(ids) != plan.get("expected_count"):
                raise ValueError("cell_ids do not match the unique declared count")
            return set(ids)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"Round 70 public plan {rel} cannot be reconciled: {exc}")
            return set()

    rerun_plan = read_plan("rounds/r70-rve-rerun/PLAN.json")
    rerun_rows = aggregate(tests, "r70-rve-rerun")
    rerun_ids = {row.get("cell_id") for row in rerun_rows}
    if rerun_plan - rerun_ids:
        errors.append(f"FE2 rerun plan IDs missing from test-count ledger: {sorted(rerun_plan - rerun_ids)}")
    if rerun_ids - rerun_plan:
        errors.append(f"FE2 rerun test-count IDs extra to public plan: {sorted(rerun_ids - rerun_plan)}")

    task8_plan = read_plan("rounds/r70-task8/PLAN.json")
    task8_scored = [row for row in tests if row.get("cohort", "").startswith("r70-task8") and row.get("scored") is True]
    task8_scored_ids = {row.get("cell_id") for row in task8_scored}
    task8_missing = sorted(task8_plan - task8_scored_ids)
    task8_extra = sorted(task8_scored_ids - task8_plan)
    if task8_extra:
        errors.append(f"Task-8 scored IDs extra to the exact public plan: {task8_extra}")
    if task8_scored:
        errors.append("Task-8 scored rows appear although the public round is NOT-RUN")

    try:
        exported = read_jsonl(root / "results/cells.jsonl")
    except (OSError, ValueError) as exc:
        exported = []
        errors.append(f"Official result export cannot be read for Round 70 identity joins: {exc}")
    join_counts = {}
    for cohort in ("r70-rve-ext", "r70-rve-rerun"):
        cohort_rows = aggregate(tests, cohort)
        errors.extend(export_join_errors(cohort_rows, exported, cohort))
        join_counts[cohort] = len(cohort_rows)

    return {
        "extension_export_join_rows": join_counts.get("r70-rve-ext", 0),
        "rerun_export_join_rows": join_counts.get("r70-rve-rerun", 0),
        "rerun_plan_cells": len(rerun_plan),
        "task8_plan_cells": len(task8_plan),
        "task8_scored_cells": len(task8_scored_ids),
        "task8_planned_ids_not_run": task8_missing,
        "task8_scored_ids_extra_to_plan": task8_extra,
    }


def aggregate(rows, cohort, *, task=None, stack=None, reps=None):
    selected = [row for row in rows if row.get("cohort") == cohort]
    if task is not None:
        selected = [row for row in selected if row.get("task") == task]
    if stack is not None:
        selected = [row for row in selected if row.get("stack") == stack]
    if reps is not None:
        selected = [row for row in selected if row.get("rep") in reps]
    return selected


def rounded_median(values):
    """Round a nonnegative median to the nearest integer, with halves upward."""
    return int(math.floor(median(values) + 0.5))


def summarize_extension_costs(extension_rows, cost_by_id):
    summary = {}
    for stack in STACKS:
        rows = [row for row in extension_rows if row.get("stack") == stack]

        def metrics(selected):
            matched = [
                cost_by_id[row["cell_id"]]
                for row in selected
                if row.get("cell_id") in cost_by_id
            ]
            if not matched:
                return None
            return {
                "total_tokens": rounded_median([row["total_tokens"] for row in matched]),
                "wall_s": rounded_median([row["wall_s"] for row in matched]),
            }

        hosts = {row.get("host") for row in rows}
        summary[stack] = {
            "host": next(iter(hosts)) if len(hosts) == 1 else "unmapped",
            "headline": metrics([row for row in rows if row.get("rep") in {31, 32}]),
            "posthoc": metrics(rows),
        }
    return summary


def render_cost_time_line(stack, summary):
    headline = summary["headline"]
    posthoc = summary["posthoc"]
    return (
        f"| {STACK_LABELS[stack]} | {summary['host']} | "
        f"{headline['total_tokens']:,} | {headline['wall_s']:,} | "
        f"{posthoc['total_tokens']:,} | {posthoc['wall_s']:,} |"
    )


def validate_cost_time(tests, cost_rows, errors):
    target_tests = [
        row for row in tests
        if row.get("cohort") in {"r70-rve-ext", "r70-rve-rerun"}
    ]
    if len(target_tests) != 44:
        errors.append(f"Cost/time target test-count rows {len(target_tests)}, expected 44")
    if len(cost_rows) != 44:
        errors.append(f"Cost/time ledger rows {len(cost_rows)}, expected 44")

    expected_fields = {
        "cell_id", "uncached_input_tokens", "cached_input_tokens", "output_tokens",
        "total_tokens", "wall_s",
    }
    cost_by_id = {}
    for row in cost_rows:
        cell_id = row.get("cell_id")
        if not isinstance(cell_id, str) or not cell_id:
            errors.append("Cost/time row has no exact cell_id")
            continue
        if cell_id in cost_by_id:
            errors.append("Duplicate exact cell ID in results/cost-time.jsonl")
            continue
        if set(row) != expected_fields:
            errors.append("Cost/time row has unexpected or missing fields")
        token_fields = (
            "uncached_input_tokens", "cached_input_tokens", "output_tokens", "total_tokens",
        )
        valid = True
        for field in token_fields:
            value = row.get(field)
            if type(value) is not int or value < 0:
                errors.append(f"Cost/time row has invalid {field}")
                valid = False
        wall = row.get("wall_s")
        if isinstance(wall, bool) or not isinstance(wall, (int, float)) or not math.isfinite(wall) or wall <= 0:
            errors.append("Cost/time row has invalid wall_s")
            valid = False
        if valid and row["total_tokens"] != sum(row[field] for field in token_fields[:3]):
            errors.append("Cost/time total_tokens does not equal uncached input plus cached input plus output")
            valid = False
        if valid:
            cost_by_id[cell_id] = row

    expected_ids = {row.get("cell_id") for row in target_tests}
    observed_ids = {row.get("cell_id") for row in cost_rows}
    if expected_ids - observed_ids:
        errors.append("Cost/time ledger is missing target cell IDs")
    if observed_ids - expected_ids:
        errors.append("Cost/time ledger has cell IDs outside the extension and FE2 rerun cohorts")

    extension_rows = [row for row in target_tests if row.get("cohort") == "r70-rve-ext"]
    expected_hosts = {
        "rust": "kogen-bench-eu",
        "elixir": "kogen-bench-eu",
        "go": "kogen-bench-us",
        "ts-bun": "kogen-bench-us",
    }
    for stack, host in expected_hosts.items():
        rows = [row for row in extension_rows if row.get("stack") == stack]
        if any(row.get("host") != host for row in rows):
            errors.append(f"Extension host mapping mismatch for {stack}")

    summary = summarize_extension_costs(extension_rows, cost_by_id)
    for stack in STACKS:
        if not summary[stack]["headline"] or not summary[stack]["posthoc"]:
            errors.append(f"Cost/time medians cannot be computed for {stack}")
        elif summary[stack]["host"] != expected_hosts[stack]:
            errors.append(f"Cost/time summary host mismatch for {stack}")
    return summary


def check_fragment(path, text, fragment, errors, label):
    if fragment not in text:
        errors.append(f"Round 70 evidence claim mismatch in {path}: {label}")


def validate_claims(root, tests, controls, cost_summary, errors):
    def read(rel):
        path = root / rel
        try:
            return path, path.read_text()
        except OSError as exc:
            errors.append(f"Missing Round 70 claim page {rel}: {exc}")
            return path, ""

    ext_path, ext_text = read("rounds/r70-rve-ext/RESULTS.md")
    rerun_path, rerun_text = read("rounds/r70-rve-rerun/RESULTS.md")
    task8_path, task8_text = read("rounds/r70-task8/RESULTS.md")
    ext_readme_path, ext_readme = read("rounds/r70-rve-ext/README.md")
    ext_measured_path, ext_measured = read("rounds/r70-rve-ext/MEASURED.md")
    ext_rule_path, ext_rule = read("rounds/r70-rve-ext/DECISION-RULE.md")
    rerun_readme_path, rerun_readme = read("rounds/r70-rve-rerun/README.md")
    rerun_measured_path, rerun_measured = read("rounds/r70-rve-rerun/MEASURED.md")
    rerun_rule_path, rerun_rule = read("rounds/r70-rve-rerun/DECISION-RULE.md")
    rerun_record_path, rerun_record = read("rounds/r70-rve-rerun/RERUN-RESULTS.md")
    task8_readme_path, task8_readme = read("rounds/r70-task8/README.md")
    task8_measured_path, task8_measured = read("rounds/r70-task8/MEASURED.md")
    task8_rule_path, task8_rule = read("rounds/r70-task8/DECISION-RULE.md")
    register_path, register = read("rounds/README.md")
    stacks_path, stacks_page = read("categories/stacks.md")
    models_path, models_page = read("categories/models-and-effort.md")
    results_readme_path, results_readme = read("results/README.md")
    r70_path, r70_page = read("rounds/r70/README.md")
    parity_path, parity_page = read("rounds/r70-rve-rerun/SKELETON-PARITY.md")
    rule8_path, rule8_page = read("rounds/r70-task8/DECISION-RULE.md")

    original = aggregate(tests, "r70-original-rve")
    rerun = aggregate(tests, "r70-rve-rerun")
    extension = aggregate(tests, "r70-rve-ext")
    ext_pre = [row for row in extension if row.get("rep") in {31, 32}]
    ext_all = extension
    ext_admission = aggregate(controls, "r70-rve-ext", task=None)
    ext_admission = [row for row in ext_admission if row.get("control_type") == "admission"]
    ext_xcontrols = [row for row in controls if row.get("cohort") == "r70-rve-ext" and row.get("control_type") == "x-control"]
    rep31 = [row for row in extension if row.get("rep") == 31]

    if len(ext_pre) == 24 and len(ext_all) == 29:
        check_fragment(ext_path, ext_text, "STATUS: **VALID** — DESCRIPTIVE", errors, "extension results status")
        headline_values = [
            f"{STACK_LABELS[stack]} {fraction([row for row in ext_pre if row['stack'] == stack])}"
            for stack in STACKS
        ]
        headline = "Pre-registered reps 31–32 per stack: " + ", ".join(headline_values[:-1]) + ", and " + headline_values[-1] + ". Rep 33 is a separate post-hoc addition."
        check_fragment(ext_path, ext_text, headline, errors, "extension headline")
        short_headline = "Headline: Reps 31–32 per stack: " + ", ".join(headline_values[:-1]) + ", and " + headline_values[-1] + "."
        check_fragment(ext_readme_path, ext_readme, short_headline, errors, "extension README headline")
        check_fragment(ext_readme_path, ext_readme, "n: 24 pre-registered cells at reps 31–32; 5 post-hoc rep-33 cells; 29 official grades total.", errors, "extension README denominator")
        check_fragment(ext_readme_path, ext_readme, "Supplemental evidence: 29 official grades; 60 control receipts.", errors, "extension supplemental completeness")
        check_fragment(ext_measured_path, ext_measured, "Coverage and verdict below apply only to the Standard run-record capture.", errors, "extension measurement scope")
        check_fragment(ext_measured_path, ext_measured, "Separate supplemental ledgers publish 29 official grades and 60 control receipts", errors, "extension supplemental measurement coverage")
        check_fragment(ext_readme_path, ext_readme, "All smokes met Rule L; admission controls and X-controls had their expected outcomes.", errors, "extension README gate summary")
        category_headline = "reps 31–32 produced " + ", ".join(headline_values[:-1]) + ", and " + headline_values[-1] + "; rep 33 is post-hoc."
        check_fragment(stacks_path, stacks_page, category_headline, errors, "stack category extension counts")
        for stack in STACKS:
            pre = [row for row in ext_pre if row["stack"] == stack]
            all_rows = [row for row in ext_all if row["stack"] == stack]
            line = f"| {STACK_LABELS[stack]} | {fraction(pre)} | {fraction(all_rows)} |"
            check_fragment(ext_path, ext_text, line, errors, f"extension stack count {stack}")
        cost_header = (
            "| Stack | Host | Reps 31–32 median total tokens (headline) | "
            "Reps 31–32 median wall s (headline) | Reps 31–33 median total tokens (post-hoc) | "
            "Reps 31–33 median wall s (post-hoc) |"
        )
        check_fragment(ext_path, ext_text, cost_header, errors, "extension cost-time table header")
        check_fragment(ext_path, ext_text, "Wall time is comparable only within a host.", errors, "extension wall-time comparability note")
        if "Wall-time and token medians are not included" in ext_text:
            errors.append("Extension results page still omits the cost-time medians")
        for stack in STACKS:
            if cost_summary[stack]["headline"] and cost_summary[stack]["posthoc"]:
                check_fragment(
                    ext_path,
                    ext_text,
                    render_cost_time_line(stack, cost_summary[stack]),
                    errors,
                    f"extension cost-time median {stack}",
                )
        for task in sorted(TASKS_EXT):
            task_rows = [row for row in ext_all if row["task"] == task]
            stack = next((candidate for candidate in STACKS if task.endswith("-" + candidate)), "unmapped")
            line = f"| {task} | {stack} | {fraction(task_rows)} |"
            check_fragment(ext_path, ext_text, line, errors, f"extension task count {task}")
    else:
        errors.append("Extension cohort cannot be fully reconciled to the registered 24+5 cells")

    if len(ext_admission) == 48 and len(ext_xcontrols) == 12 and len(rep31) == 12:
        check_fragment(
            ext_path,
            ext_text,
            "The 48 reference/no-op admission controls had their expected outcomes: every reference passed and every no-op failed.",
            errors,
            "extension admission controls",
        )
        check_fragment(ext_path, ext_text, "All 12 contestant-path X-controls passed.", errors, "extension X-controls")
        check_fragment(ext_path, ext_text, "The 12 rep-31 smoke cells met Rule L.", errors, "extension smoke gate")
        if any(row["outcome"] != "pass" for row in ext_xcontrols):
            errors.append("Extension X-control ledger contains a non-pass outcome")
        if any(row["variant"] == "reference" and row["outcome"] != "pass" for row in ext_admission):
            errors.append("Extension reference admission outcome mismatch")
        if any(row["variant"] == "noop" and row["outcome"] != "fail" for row in ext_admission):
            errors.append("Extension no-op admission outcome mismatch")
        if any(row["tests_passed"] * 2 < row["tests_total"] for row in rep31):
            errors.append("An extension rep-31 smoke does not meet Rule L")
        check_fragment(ext_rule_path, ext_rule, "48 reference/no-op admission controls across the 12 task-by-stack pairs", errors, "extension decision-rule admission count")
        check_fragment(ext_rule_path, ext_rule, "All 12 contestant-path X-controls passed", errors, "extension decision-rule X-control count")
        if sum(row["variant"] == "reference" and row["outcome"] == "pass" for row in ext_admission) != 24:
            errors.append("Extension reference admission control totals do not equal 24 passes")
        if sum(row["variant"] == "noop" and row["outcome"] == "fail" for row in ext_admission) != 24:
            errors.append("Extension no-op admission control totals do not equal 24 failures")
    else:
        errors.append("Extension admission, X-control, or smoke receipt count mismatch")

    for stack in STACKS:
        source = [row for row in original if row["stack"] == stack]
        rerun_stack = [row for row in rerun if row["stack"] == stack]
        if len(source) != 10:
            errors.append(f"Original RvE denominator mismatch for {stack}")
        ext_12 = [row for row in ext_pre if row["stack"] == stack]
        ext_all_stack = [row for row in ext_all if row["stack"] == stack]
        table_line = (
            f"| {STACK_LABELS[stack]} | {fraction(source)} | {fraction(rerun_stack)} | "
            f"{fraction(source + ext_12)} | {fraction(source + ext_all_stack)} |"
        )
        check_fragment(ext_path, ext_text, table_line, errors, f"combined cohort count {stack}")
    check_fragment(
        ext_path,
        ext_text,
        "Task-4 admission controls failed for Rust, Elixir, and TypeScript/Bun. "
        "The pre-registered fixed-front-end rerun cells are shown in a separate column; original as-graded outcomes are kept. "
        "These totals do not establish a corrected stack comparison.",
        errors,
        "FE2 presentation and interpretation limit",
    )
    check_fragment(ext_path, ext_text, "The pre-registered fixed-front-end rerun cells are shown in a separate column; original as-graded outcomes are kept.", errors, "FE2 table label")
    as_graded_values = [
        f"{STACK_LABELS[stack]} {fraction([row for row in original if row['stack'] == stack] + [row for row in ext_pre if row['stack'] == stack])}"
        for stack in ("rust", "ts-bun", "go", "elixir")
    ]
    as_graded_line = "Original as-graded outcomes plus extension reps 31–32, excluding the separate FE2 rerun cells: " + ", ".join(as_graded_values[:-1]) + ", and " + as_graded_values[-1] + "."
    check_fragment(ext_path, ext_text, as_graded_line, errors, "original plus extension count")

    rerun_expected = (
        ("Task 1", "elixir", "r70-1-elixir", "r70-1-elixir-fe2"),
        ("Task 4", "rust", "r70-4-rust", "r70-4-rust-fe2"),
        ("Task 4", "elixir", "r70-4-elixir", "r70-4-elixir-fe2"),
        ("Task 4", "go", "r70-4-go", "r70-4-go-fe2"),
        ("Task 4", "ts-bun", "r70-4-ts-bun", "r70-4-ts-bun-fe2"),
    )
    for task_label, stack, old_task, new_task in rerun_expected:
        old_rows = [row for row in original if row["task"] == old_task]
        new_rows = [row for row in rerun if row["task"] == new_task]
        line = f"| {task_label} | {STACK_LABELS[stack]} | {fraction(old_rows)} | {fraction(new_rows)} |"
        check_fragment(rerun_path, rerun_text, line, errors, f"rerun comparison {old_task}")
    if len(rerun) == 15:
        total_line = f"| **All rerun cells** | — | — | **{fraction(rerun)}** |"
        check_fragment(rerun_path, rerun_text, total_line, errors, "rerun total")
        check_fragment(rerun_readme_path, rerun_readme, f"n: 15 official rerun grades", errors, "rerun planned sample count")
        check_fragment(rerun_readme_path, rerun_readme, f"Headline: The FE2 rerun recorded {fraction(rerun)} full passes", errors, "rerun headline")
        check_fragment(rerun_readme_path, rerun_readme, "Supplemental evidence: 15 official grades; 36 control receipts.", errors, "rerun supplemental completeness")
        check_fragment(rerun_measured_path, rerun_measured, "Coverage and verdict below apply only to the Standard run-record capture.", errors, "rerun measurement scope")
        check_fragment(rerun_measured_path, rerun_measured, "Separate supplemental ledgers publish 15 official grades and 36 control receipts", errors, "rerun supplemental measurement coverage")
        check_fragment(rerun_readme_path, rerun_readme, "Design: 40 original RvE cells and 15 pre-registered FE2 rerun cells (task 1 Elixir; task 4 all four stacks); the outcomes are reported as separate cohorts.", errors, "rerun design")
        check_fragment(rerun_readme_path, rerun_readme, "Limit: Task-4 admission controls failed for Rust, Elixir, and TypeScript/Bun, preventing causal front-end or stack conclusions.", errors, "rerun interpretation limit")
        check_fragment(rerun_record_path, rerun_record, f"The rerun cohort recorded {fraction(rerun)} full passes.", errors, "rerun outcome record count")
        check_fragment(register_path, register, f"across {len(rerun)} official grades", errors, "round register rerun denominator")
        check_fragment(register_path, register, f"ledger records {fraction(rerun)} full passes", errors, "round register rerun pass count")
        check_fragment(stacks_page, stacks_page, f"ledger records {fraction(rerun)} full passes across 15 official grades", errors, "stack category rerun count and denominator")
        check_fragment(models_path, models_page, f"ledger records {fraction(rerun)} full passes across 15 official grades", errors, "models category rerun count and denominator")
        task4_frontend = [row for row in controls if row["cohort"] == "r70-rve-rerun" and row["control_type"] == "admission" and row["task"] in {f"r70-4-{stack}-fe2" for stack in STACKS} and row["variant"] == "skeleton-frontend" and row["outcome"] != "invalid"]
        frontend_by_stack = {row["stack"]: row for row in task4_frontend}
        if set(frontend_by_stack) != set(STACKS):
            errors.append("Rerun fixed-front-end admission control rows do not cover all four task-4 stacks")
        else:
            expected_failed = {"rust", "elixir", "ts-bun"}
            observed_failed = {stack for stack, row in frontend_by_stack.items() if row["outcome"] == "fail"}
            observed_passed = {stack for stack, row in frontend_by_stack.items() if row["outcome"] == "pass"}
            if observed_failed != expected_failed or observed_passed != {"go"}:
                errors.append("Rerun fixed-front-end admission control outcomes mismatch")
            check_fragment(rerun_rule_path, rerun_rule, "build failure for Rust, a hidden-test failure for Elixir, and a hidden-test failure for TypeScript/Bun", errors, "rerun decision-rule control causes")

    task8_v1 = aggregate(tests, "r70-task8-v1-smoke")
    task8_v2 = aggregate(tests, "r70-task8-v2-smoke")
    if len(task8_v1) != 2 or len(task8_v2) != 2:
        errors.append("Task-8 v1/v2 smoke row count mismatch")
    for row in task8_v1 + task8_v2:
        line = f"| {'v2' if row['cohort'].endswith('v2-smoke') else 'v1'} | {STACK_LABELS[row['stack']]} | {row['cell_id']} | {row['outcome']} | {tests_fraction(row)} | no |"
        check_fragment(task8_path, task8_text, line, errors, f"task-8 smoke {row['cell_id']}")
        if row.get("scored") is not False or row.get("outcome") != "fail":
            errors.append("Task-8 smoke must be an unscored official failure")

    expected_task8_control_lines = []
    task8_specs = (
        ("v1", "rust", "r70-task8-v1", True),
        ("v1", "elixir", "r70-task8-v1", True),
        ("v1", "go", "r70-task8-v1", True),
        ("v1", "ts-bun", "r70-task8-v1", True),
        ("v2", "rust", "r70-task8-v2", False),
        ("v2", "go", "r70-task8-v2", False),
    )
    for version, stack, cohort, has_x in task8_specs:
        subset = [row for row in controls if row["cohort"] == cohort and row["task"] in {f"r70-8-{stack}", f"r70-8-{stack}-v2"}]
        reference = control_summary(subset, "admission", "reference")
        noop = control_summary(subset, "admission", "noop")
        skeleton = control_summary(subset, "admission", "skeleton-frontend")
        xcontrol = control_summary(subset, "x-control", "contestant-path") if has_x else "not run"
        line = f"| {version} {STACK_LABELS[stack]} | {reference} | {noop} | {skeleton} | {xcontrol} |"
        check_fragment(task8_path, task8_text, line, errors, f"task-8 controls {version} {stack}")

    task8_plan = root / "rounds/r70-task8/PLAN.json"
    try:
        plan = json.loads(task8_plan.read_text())
        planned_task8 = len(plan.get("cell_ids", []))
    except (OSError, json.JSONDecodeError):
        planned_task8 = -1
        errors.append("Task-8 public plan cannot be read")
    scored_task8 = sum(row.get("scored") is True and row.get("cohort", "").startswith("r70-task8") for row in tests)
    check_fragment(task8_readme_path, task8_readme, f"n: Planned {planned_task8} scored cells; scored n = {scored_task8}.", errors, "task-8 planned and scored denominators")
    check_fragment(task8_readme_path, task8_readme, "Supplemental evidence: 4 unscored smokes; 26 control receipts.", errors, "task-8 supplemental completeness")
    check_fragment(task8_measured_path, task8_measured, "Coverage and verdict below apply only to the Standard run-record capture.", errors, "task-8 measurement scope")
    check_fragment(task8_measured_path, task8_measured, "Separate supplemental ledgers publish 4 unscored smokes and 26 control receipts", errors, "task-8 supplemental measurement coverage")
    check_fragment(task8_rule_path, task8_rule, "two scored repetitions per stack and eight planned scored cells", errors, "task-8 decision-rule denominator")
    check_fragment(task8_rule_path, task8_rule, "the smoke threshold is 13/25", errors, "task-8 decision-rule threshold")
    check_fragment(task8_readme_path, task8_readme, "The four Rust/Go v1 and v2 smoke grades are not scored", errors, "task-8 smoke scoring note")
    check_fragment(task8_readme_path, task8_readme, "Limit: Official smoke and control receipts are public", errors, "task-8 public evidence limit")
    check_fragment(task8_readme_path, task8_readme, "Elixir and TypeScript/Bun reference controls failed; those stacks had no task-8 smoke or scored cells.", errors, "task-8 unrun stacks")
    check_fragment(register_path, register, "Rust and Go v1/v2 smokes failed Rule L, so no scored cells were released", errors, "task-8 round register lifecycle")
    check_fragment(task8_text, task8_text, "The Elixir and TypeScript/Bun reference controls each failed all three recorded checks at 24/25.", errors, "task-8 reference control failures")
    references = [row for row in controls if row["cohort"] == "r70-task8-v2" and row["variant"] == "reference"]
    if references and all(row["tests_passed"] == row["tests_total"] == 25 for row in references):
        threshold = math.ceil(min(row["tests_passed"] / row["tests_total"] for row in references) * 25 / 2)
        check_fragment(task8_path, task8_text, f"which is {threshold}/25 when the reference passes 25/25", errors, "task-8 Rule L threshold")
    else:
        errors.append("Task-8 reference receipts do not establish the stated Rule L threshold")
    failed_refs = [row for row in controls if row["cohort"] == "r70-task8-v1" and row["control_type"] == "admission" and row["variant"] == "reference" and row["stack"] in {"elixir", "ts-bun"}]
    if len(failed_refs) != 4 or any(row["outcome"] != "fail" or (row["tests_passed"], row["tests_total"]) != (24, 25) for row in failed_refs):
        errors.append("Task-8 Elixir/TypeScript-Bun reference failure receipts do not reconcile to four failures at 24/25")
    check_fragment(task8_rule_path, task8_rule, "Rust and Go smokes failed Rule L in both prompt versions", errors, "task-8 decision-rule smoke outcomes")

    if len(original) == 40:
        check_fragment(r70_path, r70_page, "the three original Elixir cells returned 24/25 and the three FE2 rerun cells returned 25/25", errors, "Round 70 task-1 counts")
        check_fragment(r70_path, r70_page, "This is consistent with an encoding confound", errors, "Round 70 task-1 interpretation")
        check_fragment(parity_path, parity_page, "The three original cells returned 24/25 each. The three FE2 rerun cells returned 25/25 each.", errors, "skeleton parity task-1 counts")
    check_fragment(stacks_path, stacks_page, f"ledger records {fraction(rerun)} full passes", errors, "stack category rerun count")
    check_fragment(results_readme_path, results_readme, "publishes 88 latest official hidden-test count rows", errors, "results README test-count row total")
    check_fragment(results_readme_path, results_readme, "publishes 122 admission and X-control rows", errors, "results README control row total")
    check_fragment(results_readme_path, results_readme, "Controls come from operator grade windows whose window captures are internal and not published.", errors, "results README window chronology definition")
    check_fragment(results_readme_path, results_readme, "`window_id` is `<host>@<window_snapshot_at>`, a host and time label only", errors, "results README window identity definition")
    check_fragment(register_path, register, "24 pre-registered rep-31/32 cells and five post-hoc rep-33 cells", errors, "round register extension denominators")
    check_fragment(register_path, register, "across 15 official grades", errors, "round register rerun denominator")
    if len(tests) == 88 and len(controls) == 122:
        check_fragment(results_readme_path, results_readme, "Each row includes runner status, exact cell ID, hidden tests passed/total, and grade timestamps.", errors, "results README evidence fields")
        check_fragment(results_readme_path, results_readme, "Earlier invalidated grade rows are excluded.", errors, "results README invalidated-grade note")
    else:
        errors.append("Documented Round 70 evidence row totals do not match the public ledgers")
    wording_pages = (ext_text, ext_rule, rerun_text, rerun_rule, rerun_record, task8_text, rule8_page, r70_page)
    ranking_terms = re.compile(r"\b(?:clearly|lead|leads|leader|behind|supports?|winner)\b", re.IGNORECASE)
    if any(ranking_terms.search(text) for text in wording_pages):
        errors.append("Ranking or causal wording remains in a Round 70 results page")
    if re.search(r"\breplacements?\b", ext_text, re.IGNORECASE):
        errors.append("FE2 rerun outcomes are still described as replacements on the VALID extension page")
    for rel, page_text in (("categories/stacks.md", stacks_page), ("categories/models-and-effort.md", models_page), ("rounds/README.md", register)):
        for line in page_text.splitlines():
            if "r70" in line.lower() and ranking_terms.search(line):
                errors.append(f"Ranking wording remains in the Round 70 summary in {rel}")
    for rel, text in (
        ("rounds/r70-rve-ext/RESULTS.md", ext_text),
        ("rounds/r70-rve-rerun/RESULTS.md", rerun_text),
        ("rounds/r70-task8/RESULTS.md", task8_text),
        ("rounds/r70-task8/DECISION-RULE.md", rule8_page),
        ("categories/models-and-effort.md", models_page),
    ):
        if re.search(r"\btest_[a-z0-9_]+\b|/Users/|/home/|~/|\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text):
            errors.append(f"Disallowed test name, path, or identity in {rel}")

    summary = {
        "original_rve_cells": len(original),
        "rerun_cells": len(rerun),
        "extension_cells": len(extension),
        "extension_pre_registered_cells": len(ext_pre),
        "extension_posthoc_cells": sum(row.get("posthoc") is True for row in extension),
        "task8_v1_smokes": len(task8_v1),
        "task8_v2_smokes": len(task8_v2),
        "controls": len(controls),
        "rerun_passes": fraction(rerun),
        "extension_rep31_32": {stack: fraction([row for row in ext_pre if row["stack"] == stack]) for stack in STACKS},
    }
    return summary


def audit(root=ROOT):
    errors = []
    tests, controls = load_ledgers(root, errors)
    try:
        cost_rows = read_jsonl(root / "results/cost-time.jsonl")
    except (OSError, ValueError) as exc:
        cost_rows = []
        errors.append(f"Round 70 cost/time ledger cannot be read: {exc}")
    validate_rows(tests, controls, errors)
    # This legacy Round 70 audit validates the 44 rerun/extension rows. The
    # completeness audit separately validates the expanded 64-row ledger,
    # including 20 original RvE resource receipts and the added nullable fields.
    target_cost_rows = [
        {key: row.get(key) for key in (
            "cell_id", "uncached_input_tokens", "cached_input_tokens",
            "output_tokens", "total_tokens", "wall_s",
        )}
        for row in cost_rows
        if row.get("cohort") in {"r70-rve-ext", "r70-rve-rerun"}
    ]
    cost_summary = validate_cost_time(tests, target_cost_rows, errors)
    identity_summary = validate_public_identities(root, tests, errors)
    summary = validate_claims(root, tests, controls, cost_summary, errors)
    summary.update(identity_summary)
    return sorted(set(errors)), summary


def main():
    self_test()
    errors, summary = audit()
    print(json.dumps({"summary": summary, "failures": errors, "mutation_self_test": "passed"}, indent=2, sort_keys=True))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
