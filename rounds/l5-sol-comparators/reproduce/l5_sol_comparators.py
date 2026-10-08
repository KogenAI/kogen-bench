#!/usr/bin/env python3
"""Recompute and verify every L5 comparison metric from the public CSVs."""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROUND = Path(__file__).resolve().parents[1]
TASKS = (
    "r70-2-elixir",
    "r70-2-go",
    "r70-7-rust",
    "r70-4-elixir-fe2",
    "r70-4-go-fe2",
    "r70-4-ts-bun-fe2",
)
TOKEN_FIELDS = ("uncached", "cached", "output")
EXPECTED_SOL_COMMITS = {
    "r70-2-elixir": "470ba65c1d3c19191a2190a032cd9ebf24e71975",
    "r70-2-go": "13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82",
    "r70-7-rust": "111a0c776ae6d93f6e7fccd3fc694d5f4fa26838",
    "r70-4-elixir-fe2": "5ccd0bf1e816e2b2f5b2694861f8596402409f52",
    "r70-4-go-fe2": "21d21a2f420a387c921f998e5b4d16efc8f80904",
    "r70-4-ts-bun-fe2": "cc3a831a167020538c4ca2ad90185606a2e4ad6a",
}
EXPECTED_LUNA_COMMITS = {
    "r70-2-elixir": ("470ba65c1d3c19191a2190a032cd9ebf24e71975",),
    "r70-2-go": ("13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82",),
    "r70-7-rust": ("111a0c776ae6d93f6e7fccd3fc694d5f4fa26838",),
    "r70-4-elixir-fe2": ("5ccd0bf1e816e2b2f5b2694861f8596402409f52",),
    "r70-4-go-fe2": ("748ebe3a3bc03a112dab83e785159654e0709f9e",),
    "r70-4-ts-bun-fe2": (
        "880afb00474fe33e9cf38a6d70016ddcd4e38e81",
        "cc3a831a167020538c4ca2ad90185606a2e4ad6a",
    ),
}
EXPECTED_LUNA = {
    "r70-2-elixir": (3, 1, (
        "codex__gpt-6-luna__max__default__r70-2-elixir__r31",
        "codex__gpt-6-luna__max__default__r70-2-elixir__r33",
    )),
    "r70-2-go": (3, 2, (
        "codex__gpt-6-luna__max__default__r70-2-go__r32",
    )),
    "r70-7-rust": (6, 5, (
        "codex__gpt-6-luna__max__default__r70-7-rust__r31",
    )),
    "r70-4-elixir-fe2": (3, 0, (
        "codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r10",
        "codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r13",
        "codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9",
    )),
    "r70-4-go-fe2": (2, 1, (
        "codex__gpt-6-luna__max__default__r70-4-go-fe2__r820",
    )),
    "r70-4-ts-bun-fe2": (4, 2, (
        "codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r819",
        "codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r9",
    )),
}


def read_rows(name: str) -> list[dict[str, str]]:
    path = ROUND / "data" / name
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def by_task(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["task"]].append(row)
    return groups


def fmt_number(value: Decimal) -> str:
    rounded = value.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    if rounded == rounded.to_integral_value():
        return f"{int(rounded):,}"
    return f"{rounded:,.1f}"


def fmt_rate(passes: int, n: int) -> str:
    percent = (Decimal(passes) * Decimal(100) / Decimal(n)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP
    )
    value = f"{percent:.1f}".rstrip("0").rstrip(".")
    return f"{passes}/{n} ({value}%)"


def token_per_pass(rows: list[dict[str, str]]) -> str:
    passes = sum(row["outcome"] == "pass" for row in rows)
    if passes == 0:
        return "undefined (0 passes)"
    values = [
        Decimal(sum(int(row[field]) for row in rows)) / Decimal(passes)
        for field in TOKEN_FIELDS
    ]
    total = Decimal(sum(int(row["total_tokens"]) for row in rows)) / Decimal(passes)
    rendered = " / ".join(fmt_number(value) for value in (*values, total))
    return rendered


def validate_rows(
    sol: list[dict[str, str]],
    luna: list[dict[str, str]],
    new: list[dict[str, str]],
) -> tuple[dict[str, list[dict[str, str]]], dict[str, list[dict[str, str]]]]:
    require(len(sol) == 16, f"expected 16 Sol observations, got {len(sol)}")
    require(len(luna) == 21, f"expected 21 POOL-L5 Luna observations, got {len(luna)}")
    require(len(new) == 4, f"expected 4 new Sol observations, got {len(new)}")
    require(len({r["cell_id"] for r in sol}) == len(sol), "duplicate Sol cell_id")
    require(len({r["cell_id"] for r in luna}) == len(luna), "duplicate Luna cell_id")
    require(set(by_task(sol)) == set(TASKS), "Sol task set differs from the frozen task set")
    require(set(by_task(luna)) == set(TASKS), "Luna task set differs from the frozen task set")
    require({r["cohort"] for r in sol} == {"reused", "new"}, "unexpected Sol cohort labels")
    require(sum(r["cohort"] == "reused" for r in sol) == 12, "expected 12 reused Sol observations")
    require(sum(r["cohort"] == "new" for r in sol) == 4, "expected 4 new Sol observations")
    require(all(r["cohort"] == "POOL-L5" for r in luna), "Luna rows must come from POOL-L5")
    require({r["cell_id"] for r in new} == {r["cell_id"] for r in sol if r["cohort"] == "new"},
            "new-cells.csv and Sol cohort IDs differ")

    for label, rows in (("Sol", sol), ("Luna", luna), ("new", new)):
        for row in rows:
            require(row["outcome"] in {"pass", "fail"}, f"unexpected {label} status: {row['cell_id']}")
            components = [int(row[field]) for field in TOKEN_FIELDS]
            require(int(row["total_tokens"]) == sum(components),
                    f"token total is not the component sum: {row['cell_id']}")

    sol_groups, luna_groups = by_task(sol), by_task(luna)
    require({r["model"] for r in sol} == {"gpt-6.1-sol"}, "Sol model metadata mismatch")
    require({r["effort"] for r in sol} == {"medium"}, "Sol effort metadata mismatch")
    require({r["model"] for r in luna} == {"gpt-6-luna"}, "Luna model metadata mismatch")
    require({r["effort"] for r in luna} == {"max"}, "Luna effort metadata mismatch")
    cli_versions = {r["cli_version"] for r in sol + luna}
    require(len(cli_versions) == 1, "CLI version varies across scored rows")
    wrapper_versions = {r["wrapper_sha256"] for r in sol}
    require(wrapper_versions == {"08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300"},
            "Sol wrapper fingerprint differs from the frozen design")

    for task, expected_commit in EXPECTED_SOL_COMMITS.items():
        commits = {row["kogen_commit"] for row in sol_groups[task]}
        require(commits == {expected_commit}, f"Sol Kogen commit mismatch for {task}")
    for task, expected_commits in EXPECTED_LUNA_COMMITS.items():
        commits = tuple(sorted({row["kogen_commit"] for row in luna_groups[task]}))
        require(commits == tuple(sorted(expected_commits)), f"Luna Kogen commit mismatch for {task}")
    for task, (expected_n, expected_passes, expected_failures) in EXPECTED_LUNA.items():
        rows = luna_groups[task]
        failures = tuple(sorted(row["cell_id"] for row in rows if row["outcome"] == "fail"))
        require(len(rows) == expected_n, f"POOL-L5 denominator mismatch for {task}")
        require(sum(row["outcome"] == "pass" for row in rows) == expected_passes,
                f"POOL-L5 pass count mismatch for {task}")
        require(failures == tuple(sorted(expected_failures)), f"POOL-L5 failure IDs mismatch for {task}")

    sol_by_id = {row["cell_id"]: row for row in sol}
    for planned in new:
        observed = sol_by_id[planned["cell_id"]]
        for field in ("task", "stack", "host", "outcome", "kogen_commit", "model", "effort",
                      "uncached", "cached", "output", "total_tokens", "cli_version", "wrapper_sha256"):
            require(planned[field] == observed[field],
                    f"new-cell metadata mismatch for {planned['cell_id']}: {field}")
    require({r["timeout_s"] for r in new} == {"3600"}, "new-cell timeout differs from the frozen design")
    require({r["retries"] for r in new} == {"0"}, "new-cell retry count differs from the frozen design")
    require({r["rep"] for r in new} == {"901", "902"}, "unexpected new rep IDs")
    return sol_groups, luna_groups


def render_registration(
    sol: list[dict[str, str]],
    luna: list[dict[str, str]],
    sol_groups: dict[str, list[dict[str, str]]],
    new: list[dict[str, str]],
) -> str:
    reused = sum(row["cohort"] == "reused" for row in sol)
    new_count = sum(row["cohort"] == "new" for row in sol)
    passful_tasks = sum(any(row["outcome"] == "pass" for row in sol_groups[task]) for task in TASKS)
    cli = sorted({row["cli_version"] for row in sol + luna})[0]
    wrapper = sorted({row["wrapper_sha256"] for row in sol})[0]
    timeout = sorted({int(row["timeout_s"]) for row in new})[0]
    retries = sorted({int(row["retries"]) for row in new})[0]
    sol_model = sol[0]["model"]
    sol_effort = sol[0]["effort"]
    luna_model = luna[0]["model"]
    luna_effort = luna[0]["effort"]
    return "\n".join((
        f"Pre-registered: yes for the {new_count} prospective new cells; design frozen 7 October 2026 before their first scored execution. The {reused} reused official Sol observations are historical and predate the L5 design.",
        "Label: **DESCRIPTIVE (H45)**",
        f"Question: Does direct Codex `{sol_model}` at `{sol_effort}` show passes on selected hard task variants with official `{luna_model}` `{luna_effort}` failures, and at what token cost per pass?",
        f"n: {len(sol)} Sol observations ({reused} reused + {new_count} new); {len(luna)} Luna-max POOL-L5 observations across {len(TASKS)} task variants.",
        f"Headline: Sol recorded at least one pass on {passful_tasks} of {len(TASKS)} variants; task-level rates and Luna failure IDs are in [RESULTS](RESULTS.md).",
        f"Configuration: direct Codex, default prompt, Codex harness; Sol `{sol_model}`/{sol_effort}, Luna `{luna_model}`/{luna_effort}; `{cli}`. New-cell timeout {timeout:,} seconds, retries {retries}; Sol wrapper SHA-256 `{wrapper}`.",
        "Design SHA-256: `f45f183868a242065ee89b74e8e4cb28dfd749b2aea2e93f285801a358e9a75e`.",
    ))


def render_results(sol_groups: dict[str, list[dict[str, str]]],
                   luna_groups: dict[str, list[dict[str, str]]]) -> str:
    reused = sum(row["cohort"] == "reused" for rows in sol_groups.values() for row in rows)
    new_count = sum(row["cohort"] == "new" for rows in sol_groups.values() for row in rows)
    sol_total = sum(map(len, sol_groups.values()))
    luna_total = sum(map(len, luna_groups.values()))
    lines = [
        "Outcomes use the latest official grade row for each exact cell ID.",
        f"Population: {sol_total} Sol observations ({reused} reused + {new_count} new); {luna_total} Luna-max POOL-L5 observations.",
        "",
        "The arm labels below identify direct Codex `gpt-6.1-sol` at medium and direct Codex `gpt-6-luna` at max.",
    ]
    for task in TASKS:
        srows, lrows = sol_groups[task], luna_groups[task]
        sp = sum(row["outcome"] == "pass" for row in srows)
        lp = sum(row["outcome"] == "pass" for row in lrows)
        failures = sorted(row["cell_id"] for row in lrows if row["outcome"] == "fail")
        sol_passes = sorted(row["cell_id"] for row in srows if row["outcome"] == "pass")
        failure_ids = "; ".join(f"`{cell_id}`" for cell_id in failures) or "none"
        sol_ids = "; ".join(f"`{cell_id}`" for cell_id in sol_passes) or "none"
        lines.extend((
            "",
            f"### `{task}`",
            "",
            f"- Sol-medium official full pass: **{fmt_rate(sp, len(srows))}**; tokens per pass (uncached / cached / output / total): {token_per_pass(srows)}.",
            f"- Luna-max official full pass: **{fmt_rate(lp, len(lrows))}**; tokens per pass (uncached / cached / output / total): {token_per_pass(lrows)}.",
            f"- Luna-max failure cell IDs: {failure_ids}.",
            f"- Sol-medium pass cell IDs on this task variant: {sol_ids}.",
        ))
    lines.extend((
        "",
        "Token figures are per task and per official pass. Each cell total is uncached input + cached input + output; per-pass costs sum every attempt, including failures, then divide by passes. Values are rounded to one decimal when needed; separately rounded components can differ slightly from the displayed total. A zero-pass arm has undefined tokens per pass.",
        "",
        "These are task-variant-level observations across separate cells; the Sol pass IDs are not paired to individual Luna failure IDs.",
    ))
    return "\n".join(lines)


def render_reproduction(sol: list[dict[str, str]], luna: list[dict[str, str]]) -> str:
    cli = sorted({row["cli_version"] for row in sol + luna})[0]
    wrapper = sorted({row["wrapper_sha256"] for row in sol})[0]
    sol_commits = {task: sorted({row["kogen_commit"] for row in sol if row["task"] == task}) for task in TASKS}
    luna_commits = {task: sorted({row["kogen_commit"] for row in luna if row["task"] == task}) for task in TASKS}

    def links(commits: list[str]) -> str:
        return "; ".join(
            f"[{sha}](https://github.com/KogenAI/kogen-ex/commit/{sha})"
            for sha in commits
        )

    task_ids = ", ".join(f"`{task}`" for task in TASKS)
    first_sol_commit = sol_commits[TASKS[0]][0]
    lines = [
        f"Kogen commit: exact task and arm commits are linked below; first Sol task commit `{first_sol_commit}`.",
        f"Harness commit: unavailable; no harness Git commit is recorded in the cited source. Sol wrapper SHA-256: `{wrapper}`.",
        f"Model and effort: direct Codex `gpt-6.1-sol`/`medium`; direct Codex `gpt-6-luna`/`max`.",
        f"Task IDs: {task_ids}.",
        f"Command: `python3 rounds/l5-sol-comparators/reproduce/l5_sol_comparators.py`.",
        "Raw records: `rounds/l5-sol-comparators/data/sol-cells.csv`, `rounds/l5-sol-comparators/data/luna-baseline.csv`, and `rounds/l5-sol-comparators/data/new-cells.csv`.",
        f"CLI: `{cli}` on the official Sol and Luna rows.",
        "Task IDs and Kogen commits by arm:",
        "",
        "| Task ID | Sol-medium Kogen commit(s) | Luna-max POOL-L5 Kogen commit(s) |",
        "|---|---|---|",
    ]
    for task in TASKS:
        lines.append(f"| `{task}` | {links(sol_commits[task])} | {links(luna_commits[task])} |")
    lines.extend((
        "",
        "Data files: `rounds/l5-sol-comparators/data/sol-cells.csv`, `rounds/l5-sol-comparators/data/luna-baseline.csv`, and `rounds/l5-sol-comparators/data/new-cells.csv`.",
        "",
        "Run from the SOT repository root:",
        "",
        "```sh",
        "python3 rounds/l5-sol-comparators/reproduce/l5_sol_comparators.py",
        "python3 reproduce/validate_repo.py",
        "```",
    ))
    return "\n".join(lines)


def render_lifecycle(new: list[dict[str, str]]) -> str:
    planned = len(new)
    observed = sum(row["outcome"] in {"pass", "fail"} for row in new)
    return "\n".join((
        "These lifecycle counts cover prospective new L5 cells; the reused Sol observations are historical and predate the L5 lane.",
        "",
        "| Lifecycle measure | n |",
        "|---|---:|",
        f"| Planned cells | {planned} |",
        f"| Identified scored starts | {observed} |",
        f"| Finished cells | {observed} |",
        f"| Officially graded cells | {observed} |",
        f"| ITT denominator | {planned} |",
    ))


def replace_managed(text: str, start: str, end: str, body: str, label: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise SystemExit(f"{label}: expected exactly one managed-block marker pair")
    left = text.index(start) + len(start)
    right = text.index(end)
    if right < left:
        raise SystemExit(f"{label}: managed-block marker order is invalid")
    return text[:left] + "\n" + body + "\n" + text[right:]


def update_or_check(path: Path, start: str, end: str, body: str, label: str, write: bool) -> None:
    text = path.read_text(encoding="utf-8")
    updated = replace_managed(text, start, end, body, label)
    if write:
        path.write_text(updated, encoding="utf-8")
    elif updated != text:
        raise SystemExit(f"{label}: public page block differs from CSV-derived output; rerun with --write")


def main() -> None:
    write = sys.argv[1:] == ["--write"]
    if sys.argv[1:] not in ([], ["--write"]):
        raise SystemExit("usage: l5_sol_comparators.py [--write]")
    sol = read_rows("sol-cells.csv")
    luna = read_rows("luna-baseline.csv")
    new = read_rows("new-cells.csv")
    sol_groups, luna_groups = validate_rows(sol, luna, new)
    readme = ROUND / "README.md"
    results = ROUND / "RESULTS.md"
    for path in (readme, results):
        require("STATUS: **DESCRIPTIVE**" in path.read_text(encoding="utf-8"),
                f"{path.name} must declare STATUS: DESCRIPTIVE")
    update_or_check(
        readme,
        "<!-- L5-REGISTRATION:BEGIN -->",
        "<!-- L5-REGISTRATION:END -->",
        render_registration(sol, luna, sol_groups, new),
        "README registration block",
        write,
    )
    update_or_check(
        readme,
        "<!-- L5-LIFECYCLE:BEGIN -->",
        "<!-- L5-LIFECYCLE:END -->",
        render_lifecycle(new),
        "README lifecycle block",
        write,
    )
    update_or_check(
        readme,
        "<!-- L5-REPRODUCE:BEGIN -->",
        "<!-- L5-REPRODUCE:END -->",
        render_reproduction(sol, luna),
        "README reproduce block",
        write,
    )
    update_or_check(
        results,
        "<!-- L5-RESULTS:BEGIN -->",
        "<!-- L5-RESULTS:END -->",
        render_results(sol_groups, luna_groups),
        "RESULTS metrics block",
        write,
    )
    print("L5 public page matches all 16 Sol and 21 POOL-L5 official cell rows.")
    print("Task rates, failure IDs, per-pass token components, totals, cohort counts, and commits verified.")


if __name__ == "__main__":
    main()
