#!/usr/bin/env python3
"""Recompute the published cache-replay tables from the sanitized CSVs."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "rounds/cache-replay-mechanism/data"
FILES = {
    "OpenAI Responses": DATA / "attempts-openai.csv",
    "ChatGPT backend": DATA / "attempts-chatgpt-eu.csv",
}
FIELDS = [
    "panel",
    "phase",
    "prefix_tokens",
    "affinity",
    "cache_condition",
    "scope",
    "dispatched",
    "usage_valid",
    "input_tokens",
    "cached_input_tokens",
    "uncached_input_tokens",
]


def read_attempts(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != FIELDS:
            raise ValueError(f"Unexpected columns in {path.name}")
        rows = list(reader)

    for row_number, row in enumerate(rows, start=2):
        for field in ("prefix_tokens",):
            row[field] = int(row[field])
        for field in ("dispatched", "usage_valid"):
            if row[field] == "":
                row[field] = None
            elif row[field] in {"true", "false"}:
                row[field] = row[field] == "true"
            else:
                raise ValueError(f"Invalid {field} in {path.name}:{row_number}")
        for field in ("input_tokens", "cached_input_tokens", "uncached_input_tokens"):
            row[field] = int(row[field]) if row[field] else None

        counters = [row[field] for field in ("input_tokens", "cached_input_tokens", "uncached_input_tokens")]
        if row["dispatched"]:
            if row["usage_valid"] is not True or any(value is None for value in counters):
                raise ValueError(f"Dispatched row lacks valid counters in {path.name}:{row_number}")
            input_tokens, cached_tokens, uncached_tokens = counters
            if min(counters) < 0 or cached_tokens > input_tokens or cached_tokens + uncached_tokens != input_tokens:
                raise ValueError(f"Inconsistent counters in {path.name}:{row_number}")
        elif row["usage_valid"] is True or any(value is not None for value in counters):
            raise ValueError(f"Undispatched row has usage counters in {path.name}:{row_number}")
    return rows


def summarize(rows: list[dict[str, Any]]) -> tuple[int, int, int, int, float | None]:
    """Return assigned, dispatched, valid, total input, cached share percentage."""
    dispatched = [row for row in rows if row["dispatched"]]
    valid = [row for row in dispatched if row["usage_valid"]]
    total_input = sum(row["input_tokens"] for row in valid)
    cached = sum(row["cached_input_tokens"] for row in valid)
    share = 100 * cached / total_input if total_input else None
    return len(rows), len(dispatched), len(valid), cached, share


def share_cell(rows: list[dict[str, Any]]) -> str:
    assigned, dispatched, valid, cached, share = summarize(rows)
    if share is None:
        return f"— ({valid}/{assigned})"
    total_input = sum(row["input_tokens"] for row in rows if row["dispatched"] and row["usage_valid"])
    return f"{share:.1f}% ({valid}/{assigned}; {cached:,}/{total_input:,})"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    output.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(output)


def core_table(datasets: dict[str, list[dict[str, Any]]]) -> str:
    result = []
    for prefix in (11008, 2048, 512):
        for affinity in ("all_on", "all_off"):
            for condition in ("warm", "cold"):
                result.append(
                    [
                        str(prefix),
                        affinity,
                        condition,
                        *[
                            share_cell(
                                [
                                    attempt
                                    for attempt in attempts
                                    if attempt["phase"] == "probe"
                                    and attempt["panel"] == "core"
                                    and attempt["prefix_tokens"] == prefix
                                    and attempt["affinity"] == affinity
                                    and attempt["cache_condition"] == condition
                                ]
                            )
                            for attempts in datasets.values()
                        ],
                    ]
                )
    return markdown_table(["Prefix tokens", "HTTP affinity", "Condition", *datasets.keys()], result)


def coordinator_summary_table(datasets: dict[str, list[dict[str, Any]]]) -> str:
    definitions = [
        ("11,008", "all on", "warm", "long_warm"),
        ("11,008", "all on", "cold", "core"),
        ("11,008", "all off", "warm", "core"),
        ("11,008", "all off", "cold", "core"),
        ("2,048", "all on", "warm", "medium_warm"),
        ("2,048", "all on", "cold", "core"),
        ("2,048", "all off", "warm", "core"),
        ("2,048", "all off", "cold", "core"),
        ("512", "any", "any", "short_any"),
    ]
    result = []
    for prefix, affinity_label, condition_label, selection in definitions:
        cells = []
        for attempts in datasets.values():
            probes = [row for row in attempts if row["phase"] == "probe"]
            if selection == "long_warm":
                selected = [
                    row for row in probes
                    if row["prefix_tokens"] == 11008
                    and row["affinity"] == "all_on"
                    and row["cache_condition"] == "warm"
                    and row["panel"] in {"core", "conversation_scope"}
                ]
            elif selection == "medium_warm":
                selected = [
                    row for row in probes
                    if row["prefix_tokens"] == 2048
                    and row["affinity"] == "all_on"
                    and row["cache_condition"] == "warm"
                    and row["panel"] in {"core", "individual_header"}
                ]
            elif selection == "short_any":
                selected = [row for row in probes if row["prefix_tokens"] == 512 and row["panel"] == "core"]
            else:
                selected = [
                    row for row in probes
                    if row["panel"] == "core"
                    and row["prefix_tokens"] == int(prefix.replace(",", ""))
                    and row["affinity"] == affinity_label.replace(" ", "_")
                    and row["cache_condition"] == condition_label
                ]
            cells.append(share_cell(selected))
        result.append([prefix, affinity_label, condition_label, *cells])
    return markdown_table(["Prefix tokens", "HTTP affinity", "Condition", *datasets.keys()], result)


def leave_one_out_table(datasets: dict[str, list[dict[str, Any]]]) -> str:
    headers = sorted(
        {
            row["affinity"]
            for attempts in datasets.values()
            for row in attempts
            if row["panel"] == "individual_header" and row["affinity"].startswith("omit:")
        }
    )
    result = []
    for affinity in headers:
        result.append(
            [
                affinity.removeprefix("omit:"),
                *[
                    share_cell(
                        [
                            row for row in attempts
                            if row["panel"] == "individual_header"
                            and row["phase"] == "probe"
                            and row["prefix_tokens"] == 2048
                            and row["cache_condition"] == "warm"
                            and row["affinity"] == affinity
                        ]
                    )
                    for attempts in datasets.values()
                ],
            ]
        )
    result.append(
        [
            "all_on comparator",
            *[
                share_cell(
                    [
                        row for row in attempts
                        if row["panel"] == "individual_header"
                        and row["phase"] == "probe"
                        and row["prefix_tokens"] == 2048
                        and row["cache_condition"] == "warm"
                        and row["affinity"] == "all_on"
                    ]
                )
                for attempts in datasets.values()
            ],
        ]
    )
    return markdown_table(["Omitted HTTP control", *datasets.keys()], result)


def scope_table(datasets: dict[str, list[dict[str, Any]]]) -> str:
    scopes = sorted(
        {
            row["scope"]
            for attempts in datasets.values()
            for row in attempts
            if row["panel"] == "conversation_scope"
        }
    )
    result = []
    for scope in scopes:
        result.append(
            [
                scope,
                *[
                    share_cell(
                        [
                            row for row in attempts
                            if row["panel"] == "conversation_scope"
                            and row["phase"] == "probe"
                            and row["scope"] == scope
                        ]
                    )
                    for attempts in datasets.values()
                ],
            ]
        )
    return markdown_table(["Scope treatment", *datasets.keys()], result)


def main() -> None:
    datasets = {label: read_attempts(path) for label, path in FILES.items()}
    expected_rows = {"OpenAI Responses": 180, "ChatGPT backend": 180}
    for label, attempts in datasets.items():
        if len(attempts) != expected_rows[label]:
            raise SystemExit(f"Unexpected attempt count for {label}: {len(attempts)}")

    tables = [
        ("Core panel", core_table(datasets)),
        ("Coordinator summary roll-up", coordinator_summary_table(datasets)),
        ("Individual-header diagnostics", leave_one_out_table(datasets)),
        ("Conversation-scope diagnostics", scope_table(datasets)),
    ]
    for title, table in tables:
        print(f"## {title}\n\n{table}\n")


if __name__ == "__main__":
    main()
