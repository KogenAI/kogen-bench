#!/usr/bin/env python3
"""Build the Standard 1.2 records for the two late scored-round additions.

Inputs are the committed, sanitized cell CSVs and receipt extracts in each
round's data directory. Missing historical receipts stay explicit and are
reported in the round's MISSING.md declaration.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from missing_reasons import compact_value, load_marker_to_code


ROOT = Path(__file__).resolve().parents[1]
PHASES = ("setup", "shape", "plan", "develop", "review", "gate", "grade")
TOKEN_FIELDS = ("input", "cached_input", "output", "reasoning")
LANG_STACKS = {"rust": "Rust", "go": "Go", "ts-bun": "TS-Bun"}
L3_STACKS = {"elixir": "Elixir", "go": "Go", "rust": "Rust"}
DEVIATIONS = {
    "lang-sol-replication": [
        "The full Standard-record gate was deferred until analysis under the lane's emitter-gap exception. The referenced strict-exception receipt is not included in the public bundle; this retrospective record validation does not establish pre-run compliance.",
        "The exact pre-run design commitment and first-call-start receipts are not in the public bundle. Registration timing remains operator-reported.",
        "Per-cell runner manifests, sandbox fingerprints, phase counters, cost inputs, host-load samples, effective-setting receipts, and stop-cause receipts were not recovered into the public bundle. Missing fields remain explicit.",
        "The 31 reused t5-t7 cells are already represented in the Round 70 source cohort; this round's Standard file records only its 27 new scored cells to avoid duplicate exact identities.",
    ],
    "l3-repair": [
        "The complete Standard-record gate was not run before analysis. These records were assembled retrospectively from cells.csv and the sanitized lane release-state summary; the pre-registration timing remains operator-reported.",
        "Per-cell contestant manifests, official repair-grade timestamp receipts, sandbox fingerprints, phase counters, cost inputs, host-load samples, and stop-cause receipts were not recovered into the public bundle. Missing fields remain explicit.",
        "Per-test grade outcomes are absent from the public bundle, so the registered per-test pass-set no-regression condition is unverifiable. Aggregate test counts are not substituted for it.",
        "The six paired original failures belong to the existing Round 70 cohort. This Standard file records only the six new repair cells to avoid duplicate exact identities.",
    ],
}


def missing(reason: str) -> dict:
    return {"missing": reason, "reconstructable_from": "none"}


def not_applicable(reason: str) -> dict:
    return {"not_applicable": reason}


def withheld(reason: str) -> dict:
    return {"withheld": reason}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def phase_objects():
    return {phase: {"start_utc": missing("Phase timestamp not present in the public per-cell data"),
                    "end_utc": missing("Phase timestamp not present in the public per-cell data")}
            for phase in PHASES}


def build_record(round_id: str, row: dict[str, str], source_digest: str) -> dict:
    if round_id == "lang-sol-replication":
        cell_id = row["cell_id"]
        task_id = row["task"]
        stack = LANG_STACKS[row["stack"]]
        base_revision = row["base_sha"]
        model = "gpt-6.1-sol"
        effort = "medium"
        host = row["host"]
        outcome = row["outcome"]
        passed = int(row["tests_passed"])
        total = int(row["tests_total"])
        wall_s = float(row["wall_s"])
        token_values = {"input": int(row["uncached"]), "cached_input": int(row["cached"]),
                        "output": int(row["output"]), "reasoning": missing("Reasoning counter not recorded separately")}
        grade_timestamp = row["grade_window_at"]
        cli_version = row["cli_version"]
        runner_version = missing("Per-cell runner version not recorded in the public round data")
        runner_py = missing("Python toolchain version not recorded for the public round data")
        wrapper_sha = missing("Per-cell Codex adapter fingerprint not recorded in the public round data")
        round_ref = "rounds/lang-sol-replication/data/cells.csv"
        arm = f"direct Codex / {stack}"
        task_base = {"kind": "git-commit", "hash": base_revision}
        cap = 3600
        dispatcher = missing("Exact dispatcher revision is not present in the public receipt extract")
    else:
        cell_id = row["repair_cell_id"]
        task_id = row["task_id"]
        stack = L3_STACKS[row["stack"]]
        base_revision = row["variant_base_commit_sha"]
        model = "gpt-6-luna"
        effort = "max"
        host = row["host"]
        outcome = row["repair_outcome"]
        passed = int(row["repair_passed"])
        total = int(row["repair_total"])
        wall_s = float(row["wall_s"])
        token_values = {"input": int(row["uncached_input_tokens"]),
                        "cached_input": int(row["cached_input_tokens"]),
                        "output": int(row["output_tokens"]),
                        "reasoning": missing("Reasoning counter not recorded separately")}
        grade_timestamp = missing("Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt")
        cli_version = f"codex-cli {row['codex_cli_version']}"
        runner_version = f"Python {row['runner_version']}"
        runner_py = runner_version
        wrapper_sha = "08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300"
        round_ref = "rounds/l3-repair/data/cells.csv; rounds/l3-repair/data/lane-release-state.json"
        arm = f"direct Codex repair / {stack}"
        task_base = {"kind": "git-commit", "hash": base_revision}
        cap = 3600
        dispatcher = missing("Per-cell dispatcher revision is not present in the public round data")

    phase_missing = lambda label: missing(f"{label} phase timing was not separately recorded in the public round data")
    phase_durations = {phase: phase_missing(phase) for phase in PHASES}
    # Direct Codex has no Kogen shaping/planning/review/gate stage records.
    for phase in ("shape", "plan", "review", "gate"):
        phase_durations[phase] = not_applicable("Direct Codex cell has no separately executed Kogen phase")
    token_phases = {
        phase: {token: missing(f"{phase} phase token counter was not recorded separately") for token in TOKEN_FIELDS}
        for phase in PHASES
    }
    for phase in ("shape", "plan", "review", "gate", "grade"):
        token_phases[phase] = {token: not_applicable("Direct Codex has no separately attributable model-token stage") for token in TOKEN_FIELDS}
    token_phases["setup"] = {token: not_applicable("Task setup has no model-token usage") for token in TOKEN_FIELDS}

    timestamps = {"cell": {"start_utc": missing("Per-cell contestant start timestamp not recorded in the public round data"),
                            "end_utc": missing("Per-cell contestant end timestamp not recorded in the public round data")},
                  "phases": phase_objects(),
                  "attempts": missing("Attempt-boundary receipts are not in the public round data")}
    if isinstance(grade_timestamp, str):
        timestamps["phases"]["grade"] = {"start_utc": grade_timestamp, "end_utc": grade_timestamp}

    return {
        "schema_version": "1.2",
        "audit_round": round_id,
        "round_id": round_id,
        "cell_id": cell_id,
        "task": {"id": task_id, "base_repo": "KogenAI/kogen-ex",
                 "base_revision": {"kind": "git-commit", "hash": base_revision}},
        "arm": arm,
        "harness": "Codex CLI",
        "model": {"requested": model, "effective": missing("Per-cell effective-model receipt not published")},
        "effort": {"requested": effort, "effective": missing("Per-cell effective-effort receipt not published"),
                   "runner_requested": effort},
        "recipe": "direct Codex",
        "host": {"id": host, "spec_ref": withheld("Host specification references are withheld by the public record policy"),
                 "cpu": withheld("Host CPU model is withheld by the public record policy"),
                 "vcpu": withheld("Host allocation is withheld by the public record policy"),
                 "ram_gib": withheld("Host memory capacity is withheld by the public record policy"),
                 "os": withheld("Host operating-system details are withheld by the public record policy"),
                 "kernel": withheld("Host kernel details are withheld by the public record policy")},
        "tools": {"harness": "Codex CLI", "kogen": not_applicable("Direct Codex does not execute Kogen"),
                  "codex_cli": cli_version, "runner": runner_version, "grader": missing("Per-cell grader software version is not in the public data"),
                  "toolchains": {"python": runner_py, "ruby": missing("Toolchain inventory not recorded"),
                                 "elixir": missing("Toolchain version not recorded"), "erlang": missing("Toolchain version not recorded"),
                                 "rust": missing("Toolchain version not recorded"), "node": missing("Toolchain version not recorded"),
                                 "other_inventory": missing("Full per-cell toolchain inventory not recorded")}},
        "sandbox": {"profile": missing("Per-cell sandbox profile is not present in the public round data"),
                    "profile_sha256": missing("Per-cell sandbox profile fingerprint is not present in the public round data"),
                    "egress_profile": missing("Per-cell egress profile is not present in the public round data"),
                    "egress_allow": missing("Per-cell egress allowlist is not present in the public round data")},
        "timing": {"phases_s": phase_durations, "total_wall_s": wall_s, "timeout_cap_s": cap},
        "tokens": {"phases": token_phases, "total": token_values},
        "cost": {"usd": missing("Per-cell cost and pricing inputs are not present in the public round data"),
                 "price_table_version": missing("Price table version not recorded"),
                 "calculator_version": missing("Cost calculator version not recorded"),
                 "accounting": "Token counters are public; no cost estimate is derived.",
                 "long_context_reconciled": False},
        "outcome": outcome,
        "stop_reason": missing("A scored outcome does not establish the runner stop cause"),
        "graded": True,
        "itt": {"class": "counted", "evidence_ref": f"{round_ref}; STANDARD.md#intention-to-treat", "cohort": "scored"},
        "kogen": {"landed": not_applicable("Direct Codex study; no Kogen candidate is built or landed"),
                   "best_candidate": not_applicable("Direct Codex study has no Kogen candidate")},
        "grade": {"grader": missing("Per-cell grader software version is not in the public data"),
                  "tests_ran": passed + (total - passed) > 0,
                  "timestamp": grade_timestamp},
        "provenance": {"ledger_sha256": source_digest,
                       "manifest_sha256": missing("Per-cell run manifest fingerprint not in the public round data"),
                       "source_ref": round_ref},
        "timestamps": timestamps,
        "circumstances": {"load1_start": missing("Host boundary load was not captured in the public round data"),
                          "load1_end": missing("Host boundary load was not captured in the public round data"),
                          "concurrent_cells_start": missing("Host-wide concurrent cell count was not captured"),
                          "concurrent_cells_end": missing("Host-wide concurrent cell count was not captured"),
                          "cap_start": 3, "cap_end": 3, "queue": missing("Queue receipt was not captured"),
                          "dispatcher_id": dispatcher,
                          "incidents": missing("Per-cell incident receipt was not captured"),
                          "load_samples": missing("Timestamped host-wide load samples were not captured")},
        "environment": {"os": withheld("Operating-system details are withheld by the public record policy"),
                        "kernel": withheld("Kernel details are withheld by the public record policy"),
                        "cpu_model": withheld("CPU model is withheld by the public record policy"),
                        "cores": withheld("Host allocation details are withheld by the public record policy"),
                        "ram_gib": withheld("Memory capacity is withheld by the public record policy"),
                        "toolchains": {"python": runner_py, "ruby": missing("Toolchain inventory not recorded"),
                                       "elixir": missing("Toolchain version not recorded"), "erlang": missing("Toolchain version not recorded"),
                                       "rust": missing("Toolchain version not recorded"), "node": missing("Toolchain version not recorded"),
                                       "other_inventory": missing("Full per-cell toolchain inventory not recorded")},
                        "network": {"profile": missing("Per-cell network profile not present in the public round data"),
                                    "allowlist_hosts": missing("Per-cell network allowlist not present in the public round data")},
                        "account_class": missing("Dated account-class receipt is not present in the public round data")},
        "setup": {"task_base": task_base, "adapter_harness_sha": wrapper_sha,
                  "sandbox_mode": missing("Per-cell sandbox mode is not present in the public round data"),
                  "sandbox_profile_sha256": missing("Per-cell sandbox fingerprint is not present in the public round data"),
                  "deps_source": missing("Per-cell dependency source is not recorded"),
                  "kogen_sha": not_applicable("Direct Codex study has no Kogen executable revision")},
    }


def declaration(records: list[dict], round_id: str) -> dict:
    from validate_round import gap_sources, gaps
    actual = gaps(records)
    return {
        "round": round_id,
        "cells": len(records),
        "fields": {
            path: {
                "count": sum(reasons.values()),
                "reasons": reasons,
                "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in cells.csv.",
            }
            for path, reasons in actual.items()
        },
        "gap_sources": gap_sources(records),
        "protocol_deviations": DEVIATIONS[round_id],
    }


def measured(round_id: str, records: list[dict], declaration_value: dict) -> str:
    missing_count = sum(field["count"] for field in declaration_value["fields"].values())
    if round_id == "lang-sol-replication":
        coverage = "27 new scored cells have Standard 1.2 rows; 31 reused exact IDs remain in the Round 70 cohort and are not duplicated here."
        metrics = "Official full-pass outcome, aggregate hidden-test count, wall seconds, and uncached/cached/output tokens."
    else:
        coverage = "Six new repair cells have Standard 1.2 rows; their six paired originals remain in the Round 70 cohort and are not duplicated here."
        metrics = "Official full-pass outcome, aggregate hidden-test count, wall seconds, and uncached/cached/output tokens. Per-test pass-set preservation is not measured in the public bundle."
    return f"""# Measurements — {round_id}

Question: See [README.md](README.md). The scored unit is an exact cell ID. The result uses only committed, sanitized data and the lane receipts linked by the round page.

Required measures: {metrics}

Coverage: {coverage} Every published scored row has an as-graded outcome. The all-planned denominator beyond the listed cohort is not inferred from these records.

Coverage counts: {len(records)} Standard records; {sum(r['graded'] is True for r in records)} officially graded rows; {missing_count} explicitly missing scalar/array capture slots across the records. Exact paths, reasons, and their impact are in [MISSING.md](MISSING.md).

Verdict impact: Explicit receipt gaps limit protocol compliance and measurement completeness. The recorded as-graded outcomes, aggregate test counts, wall values, and token totals are unchanged. The separate publication release gate remains blocked by any open publication evidence gate and by these historical deviations.
"""


def main() -> None:
    for round_id in ("lang-sol-replication", "l3-repair"):
        round_dir = ROOT / "rounds" / round_id
        csv_path = round_dir / "data" / "cells.csv"
        source_digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
        source_rows = read_csv(csv_path)
        if round_id == "lang-sol-replication":
            rows = [row for row in source_rows if row["cohort"] == "new"]
        else:
            rows = [row for row in source_rows if row["kind"] == "pair"]
        marker_to_code = load_marker_to_code()
        records = [compact_value(build_record(round_id, row, source_digest), marker_to_code) for row in rows]
        out = round_dir / "records.jsonl"
        out.write_text("".join(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n" for record in records), encoding="utf-8")
        declared = declaration(records, round_id)
        (round_dir / "MISSING.md").write_text(
            f"# Declared gaps and protocol deviations — {round_id}\n\n"
            "This declaration describes gaps in the public Standard records. No missing receipt is replaced with a reconstructed or invented value. The exact fields and counts below are generated from `records.jsonl`.\n\n"
            "## Protocol deviations\n\n"
            + "\n".join(f"- {item}" for item in DEVIATIONS[round_id])
            + "\n\n## Exact missing-value declaration\n\n```json\n"
            + json.dumps(declared, indent=2, ensure_ascii=False)
            + "\n```\n",
            encoding="utf-8",
        )
        (round_dir / "MEASURED.md").write_text(measured(round_id, records, declared), encoding="utf-8")
        print(f"{round_id}: wrote {len(records)} Standard 1.2 records; {len(declared['fields'])} missing field paths explicitly declared")


if __name__ == "__main__":
    main()
