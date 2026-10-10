#!/usr/bin/env python3
"""Recompute round summaries and source/export comparisons from mined records."""

from __future__ import annotations

import argparse
import gzip
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from mine_probe import _write_manifest, round_for_cell


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MINED = ROOT / "data/mined"
DEFAULT_METADATA = ROOT / "reproduce/inputs/cell-metadata.json"
DEFAULT_PUBLIC_GRADES = ROOT / "reproduce/inputs/grades.final.jsonl"
DEFAULT_ROUNDS = ROOT / "rounds"
TOKEN_KEYS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_tokens")
SIMPLE_TOKEN_KEYS = TOKEN_KEYS[:3]
ALIAS_FILES = {"lr1.jsonl.gz", "lr2.jsonl.gz"}
TOKEN_MISMATCH_CLASSES = (
    "multi_request_aggregation",
    "cached_input_treatment",
    "cached_input_counted_twice",
    "reasoning_counted_twice",
    "rounding",
    "unexplained_single_response",
)


def read_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = json.loads(line)
                if isinstance(row, dict):
                    rows.append(row)
    return rows


def read_mined(mined_dir: Path) -> dict[str, list[dict[str, Any]]]:
    rounds: dict[str, list[dict[str, Any]]] = {}
    for path in sorted(mined_dir.glob("*.jsonl.gz")):
        if path.name in ALIAS_FILES:
            continue
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            rows = [json.loads(line) for line in handle if line.strip()]
        if not all(isinstance(row, dict) for row in rows):
            raise ValueError(f"mined rows must be objects: {path.name}")
        rounds[path.name.removesuffix(".jsonl.gz")] = rows
    return rounds


def result_of_public(row: dict[str, Any]) -> str:
    result = row.get("outcome") or row.get("result") or "unknown"
    return result if isinstance(result, str) else "unknown"


def numeric(value: Any) -> int | float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if not math.isfinite(value):
        return None
    return value


def _outcome(row: dict[str, Any]) -> str:
    grade = row.get("official_grade")
    if not isinstance(grade, dict):
        return "ungraded"
    result = grade.get("classification") or grade.get("outcome") or grade.get("result")
    if isinstance(result, str) and result:
        return result
    return "unknown"


def _usage(row: dict[str, Any]) -> dict[str, int | float | None]:
    value = row.get("usage")
    value = value if isinstance(value, dict) else {}
    return {key: numeric(value.get(key)) for key in TOKEN_KEYS}


def summarize_rows(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(rows)
    outcomes = Counter(_outcome(row) for row in rows)
    passed = outcomes["pass"]
    failed = outcomes["fail"]
    scored = passed + failed
    components: dict[str, dict[str, Any]] = {}
    for key in TOKEN_KEYS:
        values = [usage[key] for usage in map(_usage, rows) if usage[key] is not None]
        components[key] = {
            "total": sum(values),
            "known_cells": len(values),
            "missing_cells": len(rows) - len(values),
        }
    simple_values = []
    for row in rows:
        usage = _usage(row)
        if all(usage[key] is not None for key in SIMPLE_TOKEN_KEYS):
            simple_values.append(sum(usage[key] for key in SIMPLE_TOKEN_KEYS))
    walls = [numeric(row.get("wall_s")) for row in rows]
    walls = [value for value in walls if value is not None]
    return {
        "cells": len(rows),
        "officially_graded_cells": sum(1 for row in rows if _outcome(row) != "ungraded"),
        "outcomes": dict(sorted(outcomes.items())),
        "pass_count": passed,
        "fail_count": failed,
        "pass_rate": (passed / scored) if scored else None,
        "pass_rate_denominator": scored,
        "usage_tokens": components,
        "input_plus_cached_plus_output": {
            "total": sum(simple_values),
            "complete_cells": len(simple_values),
            "incomplete_cells": len(rows) - len(simple_values),
        },
        "wall_s": {
            "median": statistics.median(walls) if walls else None,
            "known_cells": len(walls),
            "missing_cells": len(rows) - len(walls),
        },
    }


def _arm_name(row: dict[str, Any]) -> str:
    arm = row.get("arm")
    return arm if isinstance(arm, str) and arm else "(unlabeled)"


def summarize_by_arm(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[_arm_name(row)].append(row)
    return {arm: summarize_rows(group) for arm, group in sorted(groups.items())}


def reconcile_harness_compare(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Select one final grade per source cell and describe overlapping captures."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[_arm_name(row)].append(row)

    final_arm = "harness-compare-1"
    preliminary_arm = "harness-compare-1-prelim"
    duplicate_arm = "(unlabeled)"
    selected = groups.get(final_arm, [])
    preliminary = groups.get(preliminary_arm, [])
    duplicates = groups.get(duplicate_arm, [])

    def index_by_source_id(group: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
        indexed: dict[str, dict[str, Any]] = {}
        for row in group:
            source_id = row.get("source_cell_id") or row.get("cell_id")
            if not isinstance(source_id, str) or not source_id:
                raise ValueError(f"{label} row has no normalized source cell ID")
            if source_id in indexed:
                raise ValueError(f"{label} has duplicate source_cell_id {source_id}")
            indexed[source_id] = row
        return indexed

    final_by_id = index_by_source_id(selected, final_arm)
    preliminary_by_id = index_by_source_id(preliminary, preliminary_arm)
    duplicate_by_id = index_by_source_id(duplicates, duplicate_arm)
    if not final_by_id or set(final_by_id) != set(preliminary_by_id) or set(final_by_id) != set(duplicate_by_id):
        raise ValueError("harness-compare-1 source cell identities differ across the three inventories")

    match_fields = {
        "usage": lambda row: row.get("usage"),
        "wall_s": lambda row: row.get("wall_s"),
        "official_grade": lambda row: row.get("official_grade"),
        "prompt_sha256": lambda row: row.get("prompt_sha256"),
        "patch_sha256s": lambda row: [patch.get("sha256") for patch in row.get("patches", []) if isinstance(patch, dict)],
    }
    duplicate_pairs = {
        field: sum(
            getter(final_by_id[cell_id]) == getter(duplicate_by_id[cell_id])
            for cell_id in final_by_id
        )
        for field, getter in match_fields.items()
    }
    if any(count != len(final_by_id) for count in duplicate_pairs.values()):
        raise ValueError("unlabelled harness capture does not match the final capture for every source cell")

    full_inventory = summarize_rows(rows)
    preliminary_summary = summarize_rows(preliminary)
    selected_summary = summarize_rows(selected)
    reconciled = {
        "identity_field": "source_cell_id (falling back to cell_id for unlabelled captures)",
        "raw_inventory_rows": len(rows),
        "distinct_source_cell_ids": len(final_by_id),
        "inventories": {
            final_arm: {"rows": len(selected), "outcomes": selected_summary["outcomes"]},
            preliminary_arm: {"rows": len(preliminary), "outcomes": preliminary_summary["outcomes"]},
            duplicate_arm: {"rows": len(duplicates), "outcomes": summarize_rows(duplicates)["outcomes"]},
        },
        "selected_grade_inventory": final_arm,
        "selection_rule": "one row per source_cell_id from the final official-grade inventory; preliminary grades and the matching unlabelled capture copies are excluded",
        "selected_rows": len(selected),
        "selected_outcomes": selected_summary["outcomes"],
        "selected_pass_rate": selected_summary["pass_rate"],
        "final_unlabelled_duplicate_pairs": {
            "pairs": len(final_by_id),
            "matching_fields": duplicate_pairs,
        },
        "previously_reported_pooled_rate": {
            "pass": full_inventory["pass_count"],
            "fail": full_inventory["fail_count"],
            "grader_error": full_inventory["outcomes"].get("grader_error", 0),
            "pass_fail_denominator": full_inventory["pass_rate_denominator"],
            "pass_rate": full_inventory["pass_rate"],
            "status": "superseded; pools three overlapping source inventories",
        },
    }
    return selected, reconciled


def cohort_category(row: dict[str, Any]) -> str:
    cell_id = row.get("cell_id")
    cell_id = cell_id.lower() if isinstance(cell_id, str) else ""
    if "-smoke" in cell_id:
        return "smoke"
    if "-v1guard" in cell_id:
        return "v1_guard"
    if row.get("arm") == "allin-diverse-edge":
        return "additional_arm"
    return "primary_or_unclassified"


def summarize_cohorts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[cohort_category(row)].append(row)
    return {
        category: {
            "summary": summarize_rows(group),
            "by_arm": summarize_by_arm(group),
            "cell_ids": sorted(str(row.get("cell_id")) for row in group),
        }
        for category, group in sorted(groups.items())
    }


def _pass_pair(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(rows)
    outcomes = Counter(_outcome(row) for row in rows)
    denominator = outcomes["pass"] + outcomes["fail"]
    return {
        "cells": len(rows),
        "pass": outcomes["pass"],
        "fail": outcomes["fail"],
        "pass_fail_denominator": denominator,
        "pass_rate": outcomes["pass"] / denominator if denominator else None,
        "cell_ids": sorted(str(row.get("cell_id")) for row in rows),
    }


def _headline_comparison(round_id: str, rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Check round-page source headlines where the page states a numeric cohort."""
    categories = {category: [row for row in rows if cohort_category(row) == category]
                  for category in ("primary_or_unclassified", "v1_guard", "smoke", "additional_arm")}
    by_arm: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_arm[_arm_name(row)].append(row)

    if round_id == "hc-1":
        primary = categories["primary_or_unclassified"]
        expected = {"hc-ladder-solshape": (19, 20), "hc-ladderso-solshape": (17, 20)}
        actual = {arm: _pass_pair([r for r in primary if _arm_name(r) == arm]) for arm in expected}
        matches = len(primary) == 40 and all(
            actual[arm]["pass"] == pair[0] and actual[arm]["pass_fail_denominator"] == pair[1]
            for arm, pair in expected.items()
        )
        return {
            "published_claims": {
                "officially_graded_scored_cells": 40,
                "arm_passes": {arm: {"pass": pair[0], "denominator": pair[1]} for arm, pair in expected.items()},
            },
            "recomputed_scored_cohort": {
                "cells": len(primary),
                "by_arm": actual,
            },
            "raw_store_rows": len(rows),
            "excluded_smoke_cell_ids": sorted(str(row.get("cell_id")) for row in categories["smoke"]),
            "matches_published_scored_claims": matches,
        }

    if round_id == "hc-2":
        primary = categories["primary_or_unclassified"]
        guards = categories["v1_guard"]
        expected_primary = {"hc2-ladder": (16, 20), "hc2-ladder-diverse": (13, 20), "hc2-floor": (13, 20)}
        expected_guards = {"hc2-ladder": (9, 10), "hc2-ladder-diverse": (10, 10), "hc2-floor": (7, 10)}
        actual_primary = {arm: _pass_pair([r for r in primary if _arm_name(r) == arm]) for arm in expected_primary}
        actual_guards = {arm: _pass_pair([r for r in guards if _arm_name(r) == arm]) for arm in expected_guards}
        matches = len(primary) + len(guards) == 90 and all(
            actual_primary[arm]["pass"] == pair[0] and actual_primary[arm]["pass_fail_denominator"] == pair[1]
            for arm, pair in expected_primary.items()
        ) and all(
            actual_guards[arm]["pass"] == pair[0] and actual_guards[arm]["pass_fail_denominator"] == pair[1]
            for arm, pair in expected_guards.items()
        )
        return {
            "published_claims": {
                "scored_and_guard_cells": 90,
                "v2_arm_passes": {arm: {"pass": pair[0], "denominator": pair[1]} for arm, pair in expected_primary.items()},
                "v1_guard_passes": {arm: {"pass": pair[0], "denominator": pair[1]} for arm, pair in expected_guards.items()},
            },
            "recomputed_scored_and_guard_cohort": {
                "cells": len(primary) + len(guards),
                "v2_by_arm": actual_primary,
                "v1_guard_by_arm": actual_guards,
            },
            "raw_store_rows": len(rows),
            "excluded_smoke_cell_ids": sorted(str(row.get("cell_id")) for row in categories["smoke"]),
            "matches_published_scored_claims": matches,
        }

    if round_id == "hc-3":
        primary = categories["primary_or_unclassified"]
        guards = categories["v1_guard"]
        expected_primary = {"hc3-ladder": (16, 20), "hc3-ladder-edge": (13, 20)}
        expected_guards = {"hc3-ladder": (7, 10), "hc3-ladder-edge": (10, 10)}
        actual_primary = {arm: _pass_pair([r for r in primary if _arm_name(r) == arm]) for arm in expected_primary}
        actual_guards = {arm: _pass_pair([r for r in guards if _arm_name(r) == arm]) for arm in expected_guards}
        reported = len(primary) + len(guards)
        matches = reported == 60 and all(
            actual_primary[arm]["pass"] == pair[0] and actual_primary[arm]["pass_fail_denominator"] == pair[1]
            for arm, pair in expected_primary.items()
        ) and all(
            actual_guards[arm]["pass"] == pair[0] and actual_guards[arm]["pass_fail_denominator"] == pair[1]
            for arm, pair in expected_guards.items()
        )
        return {
            "published_claims": {
                "scored_and_guard_cells": 60,
                "v2_arm_passes": {arm: {"pass": pair[0], "denominator": pair[1]} for arm, pair in expected_primary.items()},
                "v1_guard_passes": {arm: {"pass": pair[0], "denominator": pair[1]} for arm, pair in expected_guards.items()},
            },
            "recomputed_scored_and_guard_cohort": {
                "cells": reported,
                "v2_by_arm": actual_primary,
                "v1_guard_by_arm": actual_guards,
            },
            "raw_store_rows": len(rows),
            "additional_arm": {
                "arm": "allin-diverse-edge",
                **_pass_pair(categories["additional_arm"]),
            },
            "excluded_smoke_cell_ids": sorted(str(row.get("cell_id")) for row in categories["smoke"]),
            "matches_published_scored_claims": matches,
        }

    if round_id == "hc-4":
        graded_ids = sorted(
            str(row.get("cell_id")) for row in rows
            if isinstance(row.get("official_grade"), dict)
            and _outcome(row) != "ungraded"
        )
        return {
            "published_evidence_statement": "No official-grade count or closed scored denominator had been recovered; no efficacy result was claimed.",
            "recomputed_official_grade_cells": len(graded_ids),
            "newly_recovered_grade_cell_ids": graded_ids,
            "raw_store_rows": len(rows),
            "closed_scored_denominator_recovered": False,
        }

    if round_id == "r58x-studio":
        scored = categories["primary_or_unclassified"]
        expected_arms = {"kogen-best-d8f": 18, "codex-sol-high": 18}
        actual = {arm: _pass_pair([r for r in scored if _arm_name(r) == arm]) for arm in expected_arms}
        matches = len(scored) == 36 and len(categories["smoke"]) == 2 and all(
            actual[arm]["cells"] == count for arm, count in expected_arms.items()
        )
        return {
            "published_claims": {
                "scored_cells": 36,
                "scored_cells_per_arm": expected_arms,
                "smoke_cells": 2,
            },
            "recomputed_scored_cohort": {"cells": len(scored), "by_arm": actual},
            "recomputed_smoke_cell_ids": sorted(str(row.get("cell_id")) for row in categories["smoke"]),
            "raw_store_rows": len(rows),
            "matches_published_cohort_claims": matches,
        }

    return None


def _metadata_comparison(
    rows: list[dict[str, Any]], metadata: dict[str, Any]
) -> dict[str, Any]:
    token_compared = 0
    token_equal = 0
    token_mismatches = []
    token_mismatch_classes: Counter[str] = Counter()
    token_format_counts: dict[str, Counter[str]] = defaultdict(Counter)
    token_missing_usage = 0
    token_missing_metadata = 0
    token_missing_usage_examples: list[dict[str, str]] = []
    token_missing_metadata_examples: list[dict[str, str]] = []
    exact_codex_examples: list[dict[str, Any]] = []
    exact_cache_reasoning_examples: list[dict[str, Any]] = []
    wall_compared = 0
    wall_equal = 0
    wall_mismatches = []
    wall_missing_source = 0
    wall_missing_metadata = 0
    seen_ids: set[str] = set()
    for row in rows:
        cell_id = row.get("public_cell_id") or row.get("cell_id")
        if not isinstance(cell_id, str) or cell_id in seen_ids:
            continue
        seen_ids.add(cell_id)
        meta = metadata.get(cell_id)
        if not isinstance(meta, dict):
            token_missing_metadata += 1
            if len(token_missing_metadata_examples) < 5:
                token_missing_metadata_examples.append({
                    "round": str(row.get("round") or "(unknown)"),
                    "cell_id": cell_id,
                })
            wall_missing_metadata += 1
            continue
        meta_tokens = numeric(meta.get("tokens"))
        usage = _usage(row)
        if meta_tokens is None:
            token_missing_metadata += 1
            if len(token_missing_metadata_examples) < 5:
                token_missing_metadata_examples.append({
                    "round": str(row.get("round") or "(unknown)"),
                    "cell_id": cell_id,
                })
        elif any(usage[key] is None for key in SIMPLE_TOKEN_KEYS):
            token_missing_usage += 1
            if len(token_missing_usage_examples) < 5:
                token_missing_usage_examples.append({
                    "round": str(row.get("round") or "(unknown)"),
                    "cell_id": cell_id,
                })
        else:
            raw_total = sum(usage[key] for key in SIMPLE_TOKEN_KEYS)
            token_compared += 1
            harness = row.get("harness") if isinstance(row.get("harness"), str) else "(unknown)"
            token_format_counts[harness]["compared"] += 1
            if raw_total == meta_tokens:
                token_equal += 1
                token_format_counts[harness]["equal"] += 1
                control = {
                    "round": str(row.get("round") or "(unknown)"),
                    "cell_id": cell_id,
                    "harness": harness,
                    "published_metadata_tokens": meta_tokens,
                    "input_tokens": usage["input_tokens"],
                    "cached_input_tokens": usage["cached_input_tokens"],
                    "output_tokens": usage["output_tokens"],
                    "reasoning_tokens": usage["reasoning_tokens"],
                }
                if harness == "codex" and len(exact_codex_examples) < 3:
                    exact_codex_examples.append(control)
                if (
                    usage["cached_input_tokens"] > 0
                    and usage["reasoning_tokens"] is not None
                    and usage["reasoning_tokens"] > 0
                    and len(exact_cache_reasoning_examples) < 3
                ):
                    exact_cache_reasoning_examples.append(control)
            else:
                response_count = row.get("provider_response_count")
                if isinstance(response_count, bool) or not isinstance(response_count, int) or response_count < 0:
                    response_count = None
                reasoning = usage["reasoning_tokens"]
                input_output = usage["input_tokens"] + usage["output_tokens"]
                if reasoning is not None and raw_total + reasoning == meta_tokens:
                    cause = "reasoning_counted_twice"
                elif input_output == meta_tokens:
                    cause = "cached_input_treatment"
                elif usage["input_tokens"] + 2 * usage["cached_input_tokens"] + usage["output_tokens"] == meta_tokens:
                    cause = "cached_input_counted_twice"
                elif not isinstance(raw_total, int) and round(raw_total) == meta_tokens:
                    cause = "rounding"
                elif response_count is not None and response_count > 1:
                    cause = "multi_request_aggregation"
                else:
                    cause = "unexplained_single_response"
                token_mismatch_classes[cause] += 1
                token_format_counts[harness]["different"] += 1
                if cause == "multi_request_aggregation":
                    decision = (
                        "Keep the published metadata total as reported for the full-cell metric; "
                        "retain the manifest usage sum as a separate counter because the sanitized "
                        "bundle has no per-response usage breakdown."
                    )
                elif cause == "reasoning_counted_twice":
                    decision = (
                        "Use uncached input + cached input + output; reasoning is already included "
                        "within output under METHOD.md."
                    )
                elif cause in {"cached_input_treatment", "cached_input_counted_twice"}:
                    decision = (
                        "Count cached input exactly once, after resolving whether the harness input "
                        "counter is uncached or already cache-inclusive."
                    )
                elif cause == "rounding":
                    decision = "Use the integer token counters; no rounding is part of the published definition."
                else:
                    decision = (
                        "Treat the published and manifest values as an unresolved numeric data error; "
                        "preserve both values pending source evidence."
                    )
                token_mismatches.append({
                    "cell_id": cell_id,
                    "harness": harness,
                    "published_metadata_tokens": meta_tokens,
                    "recomputed_input_plus_cached_plus_output": raw_total,
                    "provider_response_count": response_count,
                    "classification": cause,
                    "definition_decision": decision,
                })

        meta_wall = numeric(meta.get("wall_s"))
        source_wall = numeric(row.get("wall_s"))
        if meta_wall is None:
            wall_missing_metadata += 1
        elif source_wall is None:
            wall_missing_source += 1
        else:
            wall_compared += 1
            if math.isclose(source_wall, meta_wall, rel_tol=0, abs_tol=1e-9):
                wall_equal += 1
            else:
                wall_mismatches.append({
                    "cell_id": cell_id,
                    "published_metadata_wall_s": meta_wall,
                    "recomputed_manifest_wall_s": source_wall,
                })
    return {
        "token_formula": "METHOD.md: uncached input + cached input + output; reasoning is a subset of output and is not added again",
        "token_comparison_scope": "The manifest counter is compared with the published cell metadata total. Provider response IDs are reduced to a count only; request logs and per-response records are excluded.",
        "token_cells_compared": token_compared,
        "token_cells_equal": token_equal,
        "token_cells_different": len(token_mismatches),
        "token_mismatch_classes": dict(sorted(token_mismatch_classes.items())),
        "token_format_counts": {
            harness: dict(sorted(counts.items()))
            for harness, counts in sorted(token_format_counts.items())
        },
        "token_genuine_data_errors": sum(
            1 for item in token_mismatches
            if item["classification"] == "unexplained_single_response"
        ),
        "token_missing_usage": token_missing_usage,
        "token_missing_metadata": token_missing_metadata,
        "token_missing_usage_examples": token_missing_usage_examples,
        "token_missing_metadata_examples": token_missing_metadata_examples,
        "token_exact_codex_examples": exact_codex_examples,
        "token_exact_cache_reasoning_examples": exact_cache_reasoning_examples,
        "token_mismatches": token_mismatches,
        "wall_cells_compared": wall_compared,
        "wall_cells_equal": wall_equal,
        "wall_cells_different": len(wall_mismatches),
        "wall_missing_source": wall_missing_source,
        "wall_missing_metadata": wall_missing_metadata,
        "wall_mismatches": wall_mismatches,
    }


def _source_data_conflicts(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    conflicts = []
    cells = set()
    fields = Counter()
    allowed_roots = {
        "round", "status", "wall_s", "arm", "task", "rep", "model", "effort",
        "harness", "experiment", "manifest_cell_id", "prompt_sha256", "base_sha",
    }
    for row in rows:
        raw = row.get("data_conflicts")
        if not isinstance(raw, list):
            continue
        cell_id = row.get("public_cell_id") or row.get("cell_id")
        for item in raw:
            if not isinstance(item, dict) or not isinstance(item.get("field"), str):
                continue
            field = item["field"]
            if not (field in allowed_roots or field.startswith((
                "usage.", "official_grade.", "manifest_grade.", "patch.", "base_sha.", "versions."
            ))):
                continue
            safe = {
                "cell_id": cell_id,
                "field": field,
                "preferred_value": item.get("preferred_value"),
                "recovered_value": item.get("recovered_value"),
                "preferred_source": item.get("preferred_source"),
                "recovered_source": item.get("recovered_source"),
            }
            conflicts.append(safe)
            fields[field] += 1
            if isinstance(cell_id, str):
                cells.add(cell_id)
    conflicts.sort(key=lambda item: (
        str(item.get("cell_id")), str(item.get("field")),
        json.dumps(item.get("preferred_value"), sort_keys=True),
        json.dumps(item.get("recovered_value"), sort_keys=True),
    ))
    return {
        "count": len(conflicts),
        "cells": len(cells),
        "field_counts": dict(sorted(fields.items())),
        "items": conflicts,
    }


def _public_comparison(
    round_id: str,
    rows: list[dict[str, Any]],
    public_grades: dict[str, dict[str, Any]],
    metadata: dict[str, Any],
    round_ids: set[str],
) -> dict[str, Any]:
    paired = []
    per_cell_mismatches = []
    arm_mismatches = []
    rows_by_id = {
        row.get("public_cell_id"): row
        for row in rows
        if isinstance(row.get("public_cell_id"), str)
    }
    public_rows_in_round: list[dict[str, Any]] = []
    for cell_id, public in public_grades.items():
        meta = metadata.get(cell_id, {})
        experiment = meta.get("experiment", "") if isinstance(meta, dict) else ""
        if round_for_cell(cell_id, str(experiment or ""), round_ids) != round_id:
            continue
        public_rows_in_round.append(public)

    for row in rows:
        cell_id = row.get("public_cell_id")
        if not isinstance(cell_id, str) or cell_id not in public_grades:
            continue
        public = public_grades[cell_id]
        public_result = result_of_public(public)
        raw_result = _outcome(row)
        item = {
            "cell_id": cell_id,
            "arm": _arm_name(row),
            "published_arm": public.get("arm"),
            "recomputed_raw_arm": row.get("arm"),
            "published_result": public_result,
            "recomputed_raw_result": raw_result,
        }
        paired.append(item)
        if public_result != raw_result:
            per_cell_mismatches.append(item)
        if public.get("arm") and public.get("arm") != row.get("arm"):
            arm_mismatches.append(item)

    mismatch_by_arm: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in per_cell_mismatches:
        mismatch_by_arm[item["arm"]].append(item)

    published_synthetic = [
        {
            "cell_id": public.get("cell_id"),
            "arm": public.get("arm") or _arm_name(rows_by_id.get(public.get("cell_id"), {})),
            "official_grade": {"classification": result_of_public(public)},
        }
        for public in public_rows_in_round
    ]
    published_counts = summarize_by_arm(published_synthetic)
    raw_paired_rows = [rows_by_id[row["cell_id"]] for row in paired]
    raw_counts = summarize_by_arm(raw_paired_rows)
    public_only = [
        {
            "cell_id": public.get("cell_id"),
            "arm": public.get("arm"),
            "published_result": result_of_public(public),
        }
        for public in public_rows_in_round
        if public.get("cell_id") not in rows_by_id
    ]
    aggregate_mismatches = []
    for arm in sorted(set(published_counts) | set(raw_counts)):
        public_summary = published_counts.get(arm, summarize_rows([]))
        raw_summary = raw_counts.get(arm, summarize_rows([]))
        for key in ("pass_count", "fail_count", "outcomes"):
            if public_summary[key] != raw_summary[key]:
                mismatch_cell_ids = sorted(
                    item["cell_id"]
                    for item in mismatch_by_arm.get(arm, [])
                )
                mismatch_cell_ids.extend(
                    item["cell_id"] for item in public_only
                    if item.get("arm") == arm
                )
                mismatch_cell_ids.extend(
                    item["cell_id"] for item in arm_mismatches
                    if arm in {item.get("published_arm"), item.get("recomputed_raw_arm")}
                )
                aggregate_mismatches.append({
                    "arm": arm,
                    "metric": key,
                    "published": public_summary[key],
                    "recomputed": raw_summary[key],
                    "cell_ids": sorted(set(mismatch_cell_ids)),
                })
    return {
        "public_export_rows_in_round": len(public_rows_in_round),
        "paired_public_cell_ids": len(paired),
        "outcome_matches": len(paired) - len(per_cell_mismatches),
        "outcome_mismatches": per_cell_mismatches,
        "arm_mismatches": arm_mismatches,
        "public_only_rows_missing_from_mined": len(public_only),
        "public_only_cells": sorted(public_only, key=lambda item: str(item.get("cell_id"))),
        "published_export_outcomes_by_arm": published_counts,
        "recomputed_raw_outcomes_for_paired_ids_by_arm": raw_counts,
        "aggregate_mismatches": aggregate_mismatches,
    }


def _page_text(round_id: str, data: dict[str, Any]) -> str:
    raw = data["raw_source"]
    public = data["published_export_comparison"]
    tokens = data["cell_metadata_comparison"]
    raw_outcomes = raw["outcomes"]
    outcome_line = ", ".join(f"{name} {count}" for name, count in sorted(raw_outcomes.items())) or "no official grades"
    pass_rate = raw.get("pass_rate")
    rate_text = "n/a" if pass_rate is None else f"{pass_rate * 100:.1f}% ({raw['pass_count']}/{raw['pass_rate_denominator']})"
    paired = public["paired_public_cell_ids"]
    matches = public["outcome_matches"]
    public_only = public["public_only_rows_missing_from_mined"]
    public_total = public["public_export_rows_in_round"]
    arm_mismatches = public["arm_mismatches"]
    source_conflicts = data.get("source_data_conflicts", {})
    source_description = (
        "selected final official-grade inventory"
        if round_id == "harness-compare-1"
        else "source"
    )
    section = [
        "## Recomputed from raw records",
        "",
        f"[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/{round_id}.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The {source_description} contains {raw['cells']} rows ({outcome_line}); overall pass rate is {rate_text} among pass/fail grades. Per-arm detail and coverage counts are in the JSON.",
        "",
        (f"Published-export outcome cross-check: {matches}/{paired} shared cell IDs match; {public_only}/{public_total} public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`."
         if paired else "No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below."),
    ]
    if round_id == "harness-compare-1":
        reconciliation = data["source_record_reconciliation"]
        previous = reconciliation["previously_reported_pooled_rate"]
        previous_rate = f"{previous['pass_rate'] * 100:.1f}% ({previous['pass']}/{previous['pass_fail_denominator']})"
        section.append(
            f"Cohort reconciliation: the 240 source records contain 80 final official-grade rows, 80 preliminary-grade rows, and 80 unlabelled capture copies. The execution-level rate selects one final row per `{reconciliation['identity_field']}`: **{rate_text}**. The earlier {previous_rate} arithmetic is retained only as a superseded source-inventory calculation; it pooled duplicates and preliminary grades, including {previous['grader_error']} grader errors outside the pass/fail denominator. All {reconciliation['final_unlabelled_duplicate_pairs']['pairs']} final/unlabelled pairs match on usage, wall time, grade, prompt hash, and delivered patch hashes."
        )
    if source_conflicts.get("count"):
        field_summary = ", ".join(
            f"`{field}` {count}"
            for field, count in sorted(source_conflicts.get("field_counts", {}).items())
        )
        section.append(
            f"Recovered-source discrepancies: {source_conflicts['count']} field mismatches across "
            f"{source_conflicts['cells']} cell IDs ({field_summary}). Existing values were preserved; "
            "each cell, field, kept value, and recovered value is listed below."
        )
        for item in source_conflicts.get("items", []):
            section.append(
                f"- `{item['cell_id']}` field `{item['field']}`: kept "
                f"`{json.dumps(item['preferred_value'], sort_keys=True)}`, recovered "
                f"`{json.dumps(item['recovered_value'], sort_keys=True)}`."
            )
    if arm_mismatches:
        section.append(f"Arm-label mismatches between public and raw records: {len(arm_mismatches)}; exact labels and cell IDs are in `recomputed.json`.")
    if not paired and public_total:
        section.append(
            f"The public grade export has {public_only}/{public_total} rows for this round but none join to mined source rows; the exact published values and cell IDs are in `recomputed.json`."
        )
    if public["outcome_mismatches"]:
        section.append("Exact outcome mismatches (published vs recomputed):")
        for item in public["outcome_mismatches"]:
            section.append(
                f"- `{item['cell_id']}`: published `{item['published_result']}`, recomputed `{item['recomputed_raw_result']}`."
            )
    elif paired:
        section.append("No per-cell outcome mismatches were found in the shared IDs.")
    else:
        section.append("No shared public-export cell IDs are available for a paired outcome comparison.")
    token_compared = tokens["token_cells_compared"]
    token_equal = tokens["token_cells_equal"]
    token_different = tokens["token_cells_different"]
    if token_compared:
        classes = tokens.get("token_mismatch_classes", {})
        class_summary = ", ".join(
            f"{name.replace('_', ' ')} {count}"
            for name, count in sorted(classes.items())
        ) or "no mismatches"
        section.append(
            f"Token reconciliation under [METHOD.md](../../METHOD.md): {token_equal}/{token_compared} published metadata totals equal the manifest `input + cached input + output` sum; {token_different} differ ({class_summary}). Reasoning remains a separate reported component and is not added to output."
        )
        section.append(
            f"The recompute keeps both numbers visible. {tokens.get('token_genuine_data_errors', 0)} unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded."
        )
        if tokens["token_mismatches"]:
            section.append("Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):")
            for item in tokens["token_mismatches"]:
                response_count = "unknown" if item.get("provider_response_count") is None else str(item["provider_response_count"])
                section.append(
                    f"- `{item['cell_id']}`: published `{item['published_metadata_tokens']}`, manifest `{item['recomputed_input_plus_cached_plus_output']}`, provider responses `{response_count}`; `{item['classification']}`."
                )
    else:
        section.append(
            f"No complete published metadata/manifest token pairs are available for this round ({tokens.get('token_missing_usage', 0)} missing manifest usage; {tokens.get('token_missing_metadata', 0)} missing published metadata). Missing counters remain unknown, not zero."
        )
    if round_id != "harness-compare-1" and raw["cells"] != raw.get("published_export_cells", raw["cells"]):
        if round_id == "r70":
            section.append(
                "These 108 outcomes are now public in rounds/r70/cells.jsonl but remain separate from the repository-wide outcome export."
            )
        else:
            section.append(
                f"This round also has {raw['cells'] - raw['published_export_cells']} raw-only or non-public rows; they are kept separate from the published-export denominator."
            )
    headline = data.get("published_headline_comparison")
    if headline:
        if round_id == "hc-1":
            actual = headline["recomputed_scored_cohort"]["by_arm"]
            arm_counts = ", ".join(
                f"{arm} {summary['pass']}/{summary['pass_fail_denominator']}"
                for arm, summary in sorted(actual.items())
            )
            status = "match" if headline["matches_published_scored_claims"] else "do not match"
            section.append(
                f"Historical headline check: published 40/40 scored cells and arm counts 19/20 and 17/20; recomputed {headline['recomputed_scored_cohort']['cells']} cells ({arm_counts}). These counts {status} the published claims."
            )
        elif round_id == "hc-2":
            scored = headline["recomputed_scored_and_guard_cohort"]
            v2_counts = ", ".join(
                f"{arm} {summary['pass']}/{summary['pass_fail_denominator']}"
                for arm, summary in sorted(scored["v2_by_arm"].items())
            )
            guard_counts = ", ".join(
                f"{arm} {summary['pass']}/{summary['pass_fail_denominator']}"
                for arm, summary in sorted(scored["v1_guard_by_arm"].items())
            )
            status = "match" if headline["matches_published_scored_claims"] else "do not match"
            section.append(
                f"Historical headline check: published 90 scored/guard cells, v2 counts 16/20, 13/20, 13/20, and guard counts 9/10, 10/10, 7/10; recomputed v2 ({v2_counts}) and guards ({guard_counts}). These counts {status} the published claims."
            )
        elif round_id == "hc-3":
            scored = headline["recomputed_scored_and_guard_cohort"]
            v2_counts = ", ".join(
                f"{arm} {summary['pass']}/{summary['pass_fail_denominator']}"
                for arm, summary in sorted(scored["v2_by_arm"].items())
            )
            guard_counts = ", ".join(
                f"{arm} {summary['pass']}/{summary['pass_fail_denominator']}"
                for arm, summary in sorted(scored["v1_guard_by_arm"].items())
            )
            status = "match" if headline["matches_published_scored_claims"] else "do not match"
            section.append(
                f"Historical headline check: published 60 scored/guard cells, v2 counts 16/20 and 13/20, and guard counts 7/10 and 10/10; recomputed v2 ({v2_counts}) and guards ({guard_counts}). These counts {status} the published claims."
            )
        if "matches_published_scored_claims" in headline:
            extra_ids = headline.get("excluded_smoke_cell_ids", [])
            if round_id == "hc-3":
                extra_ids += headline.get("additional_arm", {}).get("cell_ids", [])
            if extra_ids:
                section.append("Separate cells excluded from that headline cohort:")
                section.extend(f"- `{cell_id}`" for cell_id in extra_ids)
        elif "matches_published_cohort_claims" in headline:
            status = "matches" if headline["matches_published_cohort_claims"] else "does not match"
            scored_counts = ", ".join(
                f"{arm} {summary['pass']}/{summary['pass_fail_denominator']}"
                for arm, summary in sorted(headline["recomputed_scored_cohort"]["by_arm"].items())
            )
            section.append(
                f"Historical cohort check: the mined data contain {headline['recomputed_scored_cohort']['cells']} scored cells and {len(headline['recomputed_smoke_cell_ids'])} smoke cells. This {status} the published 36+2 split; scored arm counts: {scored_counts}."
            )
            section.append("Separate smoke cell IDs:")
            section.extend(f"- `{cell_id}`" for cell_id in headline["recomputed_smoke_cell_ids"])
        else:
            section.append(
                f"Evidence update: raw storage contains {headline['recomputed_official_grade_cells']} officially graded rows, although this page previously said the count was not recovered. Their exact IDs are listed in `recomputed.json`; the closed scored denominator remains unresolved, so this does not establish an efficacy cohort."
            )
    return "\n".join(section) + "\n"


def _update_readme(path: Path, round_id: str, section: str, observed_cells: int | None = None) -> None:
    text = path.read_text(encoding="utf-8")
    update = (
        "**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution."
    )
    if round_id == "unmapped":
        recovered = str(observed_cells) if isinstance(observed_cells, int) else "the recovered"
        update = (
            f"**Recomputation update:** The mined raw records provide partial per-cell outcome, manifest token-counter, and wall-time recomputation for {recovered} observed rows only. The published cohort is larger and its cell-to-round assignments remain unresolved."
        )
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(("**Recomputation limit:**", "**Recomputation update:**")):
            lines[index] = update
    text = "\n".join(lines)
    marker = "## Recomputed from raw records"
    if marker in text:
        text = text[: text.index(marker)].rstrip() + "\n\n"
    path.write_text(text.rstrip() + "\n\n" + section, encoding="utf-8")


def recompute(
    mined_dir: Path,
    metadata_path: Path,
    public_grades_path: Path,
    rounds_dir: Path,
    *,
    update_pages: bool = True,
) -> dict[str, Any]:
    mined = read_mined(mined_dir)
    round_index = rounds_dir / "index.json"
    registered_rounds = (
        set(json.loads(round_index.read_text(encoding="utf-8")))
        if round_index.is_file() else set(mined)
    )
    metadata = read_json(metadata_path, {})
    if not isinstance(metadata, dict):
        raise ValueError("cell metadata must be a JSON object")
    public_list = read_jsonl(public_grades_path) if public_grades_path.is_file() else []
    public_grades = {
        row["cell_id"]: row
        for row in public_list
        if isinstance(row.get("cell_id"), str)
    }
    token_compared = 0
    token_equal = 0
    token_missing_usage = 0
    token_missing_metadata = 0
    token_missing_usage_examples: list[dict[str, str]] = []
    token_missing_metadata_examples: list[dict[str, str]] = []
    exact_codex_examples: list[dict[str, Any]] = []
    exact_cache_reasoning_examples: list[dict[str, Any]] = []
    token_mismatch_classes: Counter[str] = Counter()
    token_format_counts: dict[str, Counter[str]] = defaultdict(Counter)
    token_mismatches: list[dict[str, Any]] = []
    output_summary: dict[str, Any] = {
        "schema_version": 1,
        "source": "data/mined/<round>.jsonl.gz; outcomes cross-checked against reproduce/inputs/grades.final.jsonl",
        "rounds_written": [],
        "global": {
            "mined_rounds": len(mined),
            "mined_cell_records": sum(len(rows) for rows in mined.values()),
            "public_export_grade_rows": len(public_grades),
        },
    }
    for round_id, rows in sorted(mined.items()):
        if round_id not in registered_rounds:
            continue
        by_arm = summarize_by_arm(rows)
        published_rows = [row for row in rows if row.get("published_export") is True]
        selected_rows = rows
        source_record_reconciliation = None
        if round_id == "harness-compare-1":
            selected_rows, source_record_reconciliation = reconcile_harness_compare(rows)
        raw_summary = summarize_rows(selected_rows)
        raw_summary["published_export_cells"] = len(published_rows)
        data = {
            "schema_version": 1,
            "round": round_id,
            "scope": "Observed rows from the recovered probe store. This does not infer unobserved planned cells, an ITT denominator, or missing execution records.",
            "raw_source": raw_summary,
            "raw_source_by_arm": by_arm,
            "raw_source_by_cohort": summarize_cohorts(rows),
            "mined_rows_with_public_export_ids": summarize_rows(published_rows),
            "mined_rows_with_public_export_ids_by_arm": summarize_by_arm(published_rows),
            "published_export_comparison": _public_comparison(round_id, rows, public_grades, metadata, set(mined)),
            "cell_metadata_comparison": _metadata_comparison(rows, metadata),
            "source_data_conflicts": _source_data_conflicts(rows),
            "published_headline_comparison": _headline_comparison(round_id, rows),
        }
        if source_record_reconciliation is not None:
            data["source_record_reconciliation"] = source_record_reconciliation
            data["source_record_inventory"] = summarize_rows(rows)
        token_comparison = data["cell_metadata_comparison"]
        token_compared += token_comparison["token_cells_compared"]
        token_equal += token_comparison["token_cells_equal"]
        token_missing_usage += token_comparison["token_missing_usage"]
        token_missing_metadata += token_comparison["token_missing_metadata"]
        token_missing_usage_examples.extend(token_comparison["token_missing_usage_examples"])
        token_missing_metadata_examples.extend(token_comparison["token_missing_metadata_examples"])
        exact_codex_examples.extend(token_comparison["token_exact_codex_examples"])
        exact_cache_reasoning_examples.extend(token_comparison["token_exact_cache_reasoning_examples"])
        token_mismatch_classes.update(token_comparison["token_mismatch_classes"])
        for harness, counts in token_comparison["token_format_counts"].items():
            token_format_counts[harness].update(counts)
        token_mismatches.extend(
            {"round": round_id, **item}
            for item in token_comparison["token_mismatches"]
        )
        round_dir = rounds_dir / round_id
        round_dir.mkdir(parents=True, exist_ok=True)
        destination = round_dir / "recomputed.json"
        destination.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        readme = round_dir / "README.md"
        if update_pages and readme.is_file():
            _update_readme(readme, round_id, _page_text(round_id, data), len(rows))
        output_summary["rounds_written"].append(round_id)

    classes = {
        name: token_mismatch_classes.get(name, 0)
        for name in TOKEN_MISMATCH_CLASSES
    }
    unexplained = [
        item for item in token_mismatches
        if item["classification"] == "unexplained_single_response"
    ]
    multi_response_counts = [
        item["provider_response_count"]
        for item in token_mismatches
        if item["classification"] == "multi_request_aggregation"
        and isinstance(item.get("provider_response_count"), int)
    ]
    examples: dict[str, list[dict[str, Any]]] = {}
    for name in TOKEN_MISMATCH_CLASSES:
        candidates = [item for item in token_mismatches if item["classification"] == name]
        selected = candidates[:5]
        if name == "multi_request_aggregation":
            by_harness: dict[str, dict[str, Any]] = {}
            for item in candidates:
                by_harness.setdefault(item["harness"], item)
            selected = list(by_harness.values())[:5]
        examples[name] = [
            {key: item.get(key) for key in (
                "round", "cell_id", "harness", "published_metadata_tokens",
                "recomputed_input_plus_cached_plus_output", "provider_response_count",
            )}
            for item in selected
        ]
    token_audit = {
        "schema_version": 1,
        "scope": "Unique cells with numeric published metadata tokens and complete manifest input, cached-input, and output counters.",
        "definition": "METHOD.md: uncached input + cached input + output; reasoning is included within output and is not added again.",
        "privacy": "Contains public cell IDs and numeric counts only. Provider response identifiers, request logs, transcripts, and rollouts are excluded.",
        "recomputed_round_count": len(mined),
        "recomputed_rounds": sorted(mined),
        "compared": token_compared,
        "equal": token_equal,
        "different": len(token_mismatches),
        "missing_manifest_usage": token_missing_usage,
        "missing_published_metadata": token_missing_metadata,
        "missing_value_examples": {
            "published_metadata": token_missing_metadata_examples[:5],
            "manifest_usage": token_missing_usage_examples[:5],
        },
        "exact_match_controls": {
            "codex_usage_format": exact_codex_examples[:3],
            "cached_input_and_reasoning": exact_cache_reasoning_examples[:3],
        },
        "mismatch_classes": classes,
        "class_examples": examples,
        "harness_format_counts": {
            harness: dict(sorted(counts.items()))
            for harness, counts in sorted(token_format_counts.items())
        },
        "multi_response_count_range": {
            "minimum": min(multi_response_counts) if multi_response_counts else None,
            "maximum": max(multi_response_counts) if multi_response_counts else None,
        },
        "genuine_numeric_data_errors": unexplained,
        "mismatches": token_mismatches,
        "earlier_audit_reference": {
            "compared": 2188,
            "equal": 1600,
            "different": 588,
            "cell_membership_available": False,
            "interpretation": "Earlier audit reports fewer comparisons (2,188 vs 4,774), but its cell list is unavailable, so subset membership and overlap cannot be checked.",
        },
    }
    output_summary["global"]["token_metadata_comparison"] = {
        "compared": token_compared,
        "equal": token_equal,
        "different": len(token_mismatches),
        "missing_manifest_usage": token_missing_usage,
        "missing_published_metadata": token_missing_metadata,
        "mismatch_classes": classes,
        "genuine_numeric_data_errors": len(unexplained),
        "multi_response_count_range": token_audit["multi_response_count_range"],
    }
    audit_path = mined_dir / "TOKEN-AUDIT.json"
    audit_path.write_text(json.dumps(token_audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_manifest(mined_dir)
    return output_summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mined", type=Path, default=DEFAULT_MINED)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--public-grades", type=Path, default=DEFAULT_PUBLIC_GRADES)
    parser.add_argument("--rounds", type=Path, default=DEFAULT_ROUNDS)
    parser.add_argument("--no-page-updates", action="store_true")
    args = parser.parse_args()
    summary = recompute(
        args.mined,
        args.metadata,
        args.public_grades,
        args.rounds,
        update_pages=not args.no_page_updates,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
