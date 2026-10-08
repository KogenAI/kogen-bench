#!/usr/bin/env python3
"""Recompute the public L2 plan-specificity results from the round CSVs."""

import argparse
import csv
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUND = ROOT / "rounds" / "l2-plan-specificity"
DATA = ROUND / "data"
LEVELS = ("criteria", "approach", "steps")
TOKEN_FIELDS = (
    "uncached_input_tokens",
    "cached_input_tokens",
    "output_tokens",
)


def load_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_int(row, key):
    try:
        value = int(row[key])
    except (KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f"invalid integer in {path_label(row)}: {key}") from exc
    if value < 0:
        raise SystemExit(f"negative token count in {path_label(row)}: {key}")
    return value


def path_label(row):
    return row.get("cell_id") or row.get("variant_id") or "CSV row"


def check(condition, message):
    if not condition:
        raise SystemExit(message)


def components(rows):
    return {key: sum(as_int(row, key) for row in rows) for key in TOKEN_FIELDS}


def sum_components(values):
    return sum(values.values())


def fmt(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            value = value.numerator
        else:
            return f"{float(value):,.1f}"
    if isinstance(value, float) and not value.is_integer():
        return f"{value:,.2f}"
    return f"{int(value):,}"


def pass_rate(rows):
    return sum(row["outcome"] == "PASS" for row in rows), len(rows)


def task_family(row):
    level = row["level"]
    task = row["task_id"]
    if level == "none":
        return task
    suffix = "-l2" + level
    check(task.endswith(suffix), f"task/level mismatch for {task}")
    return task[: -len(suffix)]


def read_and_check_data():
    cells = load_csv(DATA / "official_cells.csv")
    plans = load_csv(DATA / "planner_usage.csv")
    baseline = load_csv(DATA / "historical_no_plan_max.csv")
    check(len(cells) == 78, "expected 78 current official cells")
    check(len({row["cell_id"] for row in cells}) == 78, "duplicate current cell IDs")
    check(all(row["cohort"] == "l2" and row["status"] == "VALID" for row in cells), "unexpected current cohort/status")
    check(all(row["grade_route"] == "r70-macbook-window-v1" for row in cells), "unexpected official grade route")
    check({row["model"] for row in cells} == {"gpt-6-luna"}, "unexpected current model")
    check({row["cli_version"] for row in cells} == {"codex-cli 0.160.0"}, "unexpected builder CLI version")
    check({row["runner_python"] for row in cells} == {"3.14.7"}, "unexpected runner Python version")
    check({row["runner_fingerprint_sha256"] for row in cells} == {"3a6638ea3d6967f03770478039bf1f32e522ab393c32feb5df85d1b923e1ca19"}, "unexpected runner fingerprint")
    check({row["wrapper_sha256"] for row in cells} == {"08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300"}, "unexpected wrapper fingerprint")
    check(all(row["outcome"] in {"PASS", "FAIL"} for row in cells), "unexpected current outcome")
    check(all(row["builder"] in {"low", "max"} for row in cells), "unexpected builder effort")
    check(all(row["level"] in {"none", *LEVELS} for row in cells), "unexpected plan level")
    check(sum(row["stage"] == "gate" for row in cells) == 42, "gate lifecycle count mismatch")
    check(sum(row["stage"] == "bulk" for row in cells) == 36, "bulk lifecycle count mismatch")
    check(sum(row["level"] == "none" for row in cells) == 6, "no-plan low cell count mismatch")
    check(sum(row["level"] != "none" for row in cells) == 72, "factorial cell count mismatch")
    check(all((row["stage"] == "gate" and row["rep"] == "1") or (row["stage"] == "bulk" and row["rep"] == "2") for row in cells), "stage/rep mapping mismatch")
    for row in cells:
        check(as_int(row, "total_tokens") == sum(as_int(row, key) for key in TOKEN_FIELDS), f"builder token sum mismatch: {row['cell_id']}")
        check(len(row["base_commit_sha"]) == 40, f"missing exact base commit: {row['cell_id']}")

    check(len(plans) == 18, "expected 18 plan receipts")
    check(len({row["variant_id"] for row in plans}) == 18, "duplicate planner variant IDs")
    plan_by_variant = {}
    for row in plans:
        check(row["level"] in LEVELS and row["model"] == "gpt-6-luna" and row["effort"] == "max", "unexpected planner configuration")
        check(row["cli_version"] == "codex-cli 0.160.1", "unexpected planner CLI version")
        check(as_int(row, "total_tokens") == sum(as_int(row, key) for key in TOKEN_FIELDS), f"planner token sum mismatch: {row['variant_id']}")
        plan_by_variant[row["variant_id"]] = row
    planned = [row for row in cells if row["level"] != "none"]
    check({row["variant_id"] for row in planned} == set(plan_by_variant), "plan receipt/variant mapping mismatch")
    for row in planned:
        receipt = plan_by_variant[row["variant_id"]]
        check(receipt["plan_sha256"] == row["plan_sha256"], f"plan SHA mismatch: {row['variant_id']}")
        check(receipt["task_id"] == task_family(row) and receipt["level"] == row["level"], f"plan identity mismatch: {row['variant_id']}")

    check(len(baseline) == 32, "expected 32 valid historical no-plan max cells")
    check(len({row["cell_id"] for row in baseline}) == 32, "duplicate historical baseline cell IDs")
    check(all(row["level"] == "none" and row["builder"] == "max" and row["status"] == "VALID" for row in baseline), "unexpected historical baseline row")
    check(all(row["outcome"] in {"PASS", "FAIL"} for row in baseline), "unexpected historical baseline outcome")
    check(sum(row["outcome"] == "PASS" for row in baseline) == 20, "historical no-plan baseline pass count mismatch")
    return cells, plans, baseline, plan_by_variant


def primary_pairs(cells):
    by_pair = defaultdict(dict)
    for row in cells:
        if row["builder"] == "low" and row["level"] in {"steps", "criteria"}:
            by_pair[(task_family(row), row["rep"])][row["level"]] = row["outcome"]
    check(len(by_pair) == 12, "expected 12 Luna-low steps/criteria pairs")
    check(all(set(outcomes) == {"steps", "criteria"} for outcomes in by_pair.values()), "incomplete primary pair")
    pairs = []
    for (task, rep), outcomes in sorted(by_pair.items()):
        if outcomes["steps"] == outcomes["criteria"]:
            result = "tie"
        elif outcomes["steps"] == "PASS":
            result = "steps win"
        else:
            result = "criteria win"
        pairs.append((task, rep, outcomes["steps"], outcomes["criteria"], result))
    wins = sum(pair[4] == "steps win" for pair in pairs)
    losses = sum(pair[4] == "criteria win" for pair in pairs)
    ties = sum(pair[4] == "tie" for pair in pairs)
    net = wins - losses
    check((wins, losses, ties, net) == (3, 1, 8, 2), "primary comparison mismatch")
    discordant = wins + losses
    p_numerator = sum(math.comb(discordant, k) for k in range(wins, discordant + 1))
    p_observed = Fraction(p_numerator, 2**discordant)
    minimal_threshold_p = Fraction(1, 2**3)
    return pairs, wins, losses, ties, net, p_observed, minimal_threshold_p


def rate_summary(cells, baseline):
    summary = {}
    for level in ("none", *LEVELS):
        for builder in ("low", "max"):
            rows = [row for row in cells if row["level"] == level and row["builder"] == builder]
            if rows:
                summary[(level, builder)] = pass_rate(rows)
    summary[("none", "max historical")] = pass_rate(baseline)
    expected = {
        ("none", "low"): (1, 6),
        ("criteria", "low"): (4, 12),
        ("approach", "low"): (4, 12),
        ("steps", "low"): (6, 12),
        ("criteria", "max"): (6, 12),
        ("approach", "max"): (7, 12),
        ("steps", "max"): (6, 12),
        ("none", "max historical"): (20, 32),
    }
    check(summary == expected, "descriptive pass-rate summary mismatch")
    return summary


def token_cost(cells, plans, plan_by_variant):
    result = {}
    for level in LEVELS:
        for builder in ("low", "max"):
            rows = [row for row in cells if row["level"] == level and row["builder"] == builder]
            check(len(rows) == 12, f"expected 12 cells for {level}/{builder}")
            successes = sum(row["outcome"] == "PASS" for row in rows)
            builder_tokens = components(rows)
            plan_amortized = {key: Fraction(0, 1) for key in TOKEN_FIELDS}
            plan_oneoff = {key: 0 for key in TOKEN_FIELDS}
            for cell in rows:
                receipt = plan_by_variant[cell["variant_id"]]
                for key in TOKEN_FIELDS:
                    amount = as_int(receipt, key)
                    plan_amortized[key] += Fraction(amount, 4)
                    plan_oneoff[key] += amount
            for view, plan_charge in (("amortized", plan_amortized), ("one-off", plan_oneoff)):
                charged = {key: Fraction(builder_tokens[key], 1) + plan_charge[key] for key in TOKEN_FIELDS}
                total = sum(charged.values())
                result[(view, level, builder)] = {
                    "cells": len(rows),
                    "successes": successes,
                    "builder": builder_tokens,
                    "plan": plan_charge,
                    "charged": charged,
                    "total": total,
                    "per_success": total / successes if successes else None,
                }
    return result


def commit_map(cells):
    mapped = {}
    for row in cells:
        key = (row["task_id"], row["level"])
        value = (row["base_commit_sha"], row["plan_sha256"])
        if key in mapped:
            check(mapped[key] == value, f"commit/plan mapping changed within cells: {key[0]}")
        mapped[key] = value
    check(len(mapped) == 24, "expected six no-plan and 18 planned task IDs")
    return sorted(mapped.items(), key=lambda item: (item[0][0], item[0][1]))


def render_readme_summary(cells, baseline, wins, losses, ties, net, p_observed, p_minimal):
    current_passes = sum(row["outcome"] == "PASS" for row in cells)
    low_none = pass_rate([row for row in cells if row["level"] == "none" and row["builder"] == "low"])
    low_rates = [pass_rate([row for row in cells if row["level"] == level and row["builder"] == "low"]) for level in LEVELS]
    max_rates = [pass_rate([row for row in cells if row["level"] == level and row["builder"] == "max"]) for level in LEVELS]
    eu_rep2 = [row for row in cells if row["host"] == "kogen-bench-eu" and row["rep"] == "2"]
    worker_counts = defaultdict(int)
    for row in eu_rep2:
        worker_counts[row["grade_worker_sha256"][:8]] += 1
    changed_rows = [row for row in eu_rep2 if row["grade_worker_sha256"].startswith("0e6f8aa0")]
    changed = len(changed_rows)
    changed_tasks = ", ".join(f"`{task}`" for task in sorted(row["task_id"] for row in changed_rows))
    check(changed == 2 and worker_counts.get("73dc09af", 0) == 16, "EU rep-2 grader provenance mismatch")
    return "\n".join([
        "<!-- L2-CSV-SUMMARY:BEGIN -->",
        f"- Lifecycle counts: planned {len(cells)} / started {len(cells)} / finished {len(cells)} / graded {len(cells)} / ITT {len(cells)}.",
        f"- Headline: Luna-low steps vs criteria: {wins} steps-only wins, {losses} criteria-only {'win' if losses == 1 else 'wins'}, {ties} ties; net +{net}/12, below the preregistered +3 adoption threshold. Do not adopt steps for cheap builders; report descriptively.",
        f"- Luna-low descriptive full-pass rates: none {low_none[0]}/{low_none[1]}; criteria {low_rates[0][0]}/{low_rates[0][1]}; approach {low_rates[1][0]}/{low_rates[1][1]}; steps {low_rates[2][0]}/{low_rates[2][1]}.",
        f"- Luna-max descriptive full-pass rates: criteria {max_rates[0][0]}/{max_rates[0][1]}; approach {max_rates[1][0]}/{max_rates[1][1]}; steps {max_rates[2][0]}/{max_rates[2][1]}; historical no-plan baseline {sum(r['outcome']=='PASS' for r in baseline)}/{len(baseline)}.",
        f"- Sign-test caveat: observed one-sided exact p={p_observed.numerator}/{p_observed.denominator}={float(p_observed):.4f} over {wins+losses} discordant pairs; the minimal +3 case (3 wins, 0 losses) gives p={p_minimal.numerator}/{p_minimal.denominator}={float(p_minimal):.3f}.",
        f"- Grading provenance: the final {changed} EU rep-2 cells ({changed_tasks}) used grade_worker SHA 0e6f8aa0 instead of 73dc09af; the change was inventory-glob-only and scoring code was byte-identical.",
        "<!-- L2-CSV-SUMMARY:END -->",
    ])


def render_commit_map(cells, baseline):
    lines = [
        "<!-- L2-COMMIT-MAP:BEGIN -->",
        "| Task ID | Plan level | Kogen commit | Plan SHA-256 |",
        "|---|---|---|---|",
    ]
    for (task, level), (commit, plan_sha) in commit_map(cells):
        commit_link = f"[`{commit}`](https://github.com/KogenAI/kogen-ex/commit/{commit})"
        lines.append(f"| `{task}` | {level} | {commit_link} | {plan_sha or '—'} |")
    historical = defaultdict(list)
    for row in baseline:
        historical[(row["task_id"], row["base_commit_sha"])].append(row["cell_id"])
    lines += [
        "",
        "Historical Luna-max no-plan baseline commits:",
        "",
        "| Task ID | Official cell IDs | Kogen commit |",
        "|---|---|---|",
    ]
    for (task, commit), cell_ids in sorted(historical.items()):
        commit_link = f"[`{commit}`](https://github.com/KogenAI/kogen-ex/commit/{commit})"
        lines.append(f"| `{task}` | {', '.join(f'`{cell_id}`' for cell_id in sorted(cell_ids))} | {commit_link} |")
    lines.append("<!-- L2-COMMIT-MAP:END -->")
    return "\n".join(lines)


def render_cost_bullets(costs, view):
    lines = []
    for level in LEVELS:
        for builder in ("low", "max"):
            item = costs[(view, level, builder)]
            builder_total = sum_components(item["builder"])
            plan_total = sum(item["plan"].values())
            charged_total = item["total"]
            builder_text = "/".join(fmt(item["builder"][key]) for key in TOKEN_FIELDS) + f"/{fmt(builder_total)}"
            plan_text = "/".join(fmt(item["plan"][key]) for key in TOKEN_FIELDS) + f"/{fmt(plan_total)}"
            charged_text = "/".join(fmt(item["charged"][key]) for key in TOKEN_FIELDS) + f"/{fmt(charged_total)}"
            lines.append(
                f"- **{level} / Luna-{builder}:** {item['successes']} of {item['cells']} cells passed; "
                f"builder uncached/cached/output/total = {builder_text}; "
                f"plan charge uncached/cached/output/total = {plan_text}; "
                f"combined charged uncached/cached/output/total = {charged_text}; "
                f"tokens per official full-task pass = {fmt(item['per_success'])}."
            )
    return "\n".join(lines)


def render_results(cells, plans, baseline, pairs, wins, losses, ties, net, p_observed, p_minimal, rates, costs):
    plan_components = components(plans)
    rows = [
        "# Results",
        "",
        "STATUS: **VALID**",
        "",
        "The current cohort has 78/78 officially graded exact cell IDs: 42 gate cells and 36 rep-2 bulk cells. It includes 72 planned factorial cells and six Luna-low no-plan cells. Every included current row is labeled VALID; the historical Luna-max no-plan baseline is a separate descriptive cohort.",
        "",
        "## Per-cell outcomes and builder tokens",
        "",
        "Token rule: uncached input + cached input + output; total = the sum of those three components. Builder tokens below include the provided frozen plan in the builder prompt. No hidden grader details are included.",
        "",
        "| Task / variant | Level | Builder | Rep | Stage | Status | Outcome | Cell ID | Uncached | Cached | Output | Total |",
        "|---|---|---:|---:|---|---|---|---|---:|---:|---:|---:|",
    ]
    for row in cells:
        rows.append(
            f"| `{row['task_id']}` | {row['level']} | Luna-{row['builder']} | {row['rep']} | {row['stage']} | {row['status']} | {row['outcome']} | `{row['cell_id']}` | "
            f"{as_int(row, 'uncached_input_tokens'):,} | {as_int(row, 'cached_input_tokens'):,} | {as_int(row, 'output_tokens'):,} | {as_int(row, 'total_tokens'):,} |"
        )
    rows += [
        "",
        "## Descriptive full-task outcomes",
        "",
        f"- Luna-low no-plan cells: {rates[('none','low')][0]}/{rates[('none','low')][1]}.",
        f"- Luna-low criteria: {rates[('criteria','low')][0]}/{rates[('criteria','low')][1]}; approach: {rates[('approach','low')][0]}/{rates[('approach','low')][1]}; steps: {rates[('steps','low')][0]}/{rates[('steps','low')][1]}.",
        f"- Luna-max criteria: {rates[('criteria','max')][0]}/{rates[('criteria','max')][1]}; approach: {rates[('approach','max')][0]}/{rates[('approach','max')][1]}; steps: {rates[('steps','max')][0]}/{rates[('steps','max')][1]}.",
        f"- Historical Luna-max no-plan baseline: {rates[('none','max historical')][0]}/{rates[('none','max historical')][1]} valid official cells; this is unrandomized historical context.",
        "",
        "## Primary Luna-low paired comparison",
        "",
        "| Measure | Steps vs criteria |",
        "|---|---:|",
        f"| Steps-only wins | {wins} |",
        f"| Criteria-only wins | {losses} |",
        f"| Ties | {ties} |",
        f"| Net (wins − losses) | {net} |",
        "",
        "| Source task | Rep | Steps | Criteria | Pair result |",
        "|---|---:|---|---|---|",
    ]
    for task, rep, steps, criteria, result in pairs:
        rows.append(f"| `{task}` | {rep} | {steps} | {criteria} | {result} |")
    rows += [
        "",
        f"The preregistered adoption screen required net +3 across 12 pairs and lower total tokens per official pass than criteria. The observed net was +{net}; steps do not meet the adoption screen. The observed one-sided exact sign test, excluding ties, is p = {p_observed.numerator}/{p_observed.denominator} = {float(p_observed):.4f} ({wins} wins among {wins+losses} discordant pairs). The minimal +3 screen outcome of three wins and zero losses would still have p = {p_minimal.numerator}/{p_minimal.denominator} = {float(p_minimal):.3f}; treat this as a pilot screen, not confirmatory evidence.",
        "",
        "## Planner receipts",
        "",
        f"The {len(plans)} frozen-plan generations used Luna-max. Receipt components sum to uncached {plan_components['uncached_input_tokens']:,}, cached {plan_components['cached_input_tokens']:,}, output {plan_components['output_tokens']:,}, total {sum_components(plan_components):,} tokens.",
        "",
        "## Tokens per official pass",
        "",
        "Each plan receipt is included in the cost view. Amortized charges allocate one plan receipt over its four planned uses (two builder efforts × two reps). One-off charges assign the full receipt to each task-level scored result. Cost totals keep uncached input, cached input, and output separate; no dollar conversion or wall-time combination is used.",
        "",
        "### Amortized planning cost",
        "",
        render_cost_bullets(costs, "amortized"),
        "",
        "### One-off planning cost",
        "",
        render_cost_bullets(costs, "one-off"),
        "",
        "### No-plan cost context",
        "",
    ]
    no_plan = [row for row in cells if row['level'] == 'none' and row['builder'] == 'low']
    no_plan_tokens = components(no_plan)
    no_plan_total = sum_components(no_plan_tokens)
    no_plan_passes = sum(row['outcome'] == 'PASS' for row in no_plan)
    rows.append(
        f"Current Luna-low no-plan cells: {no_plan_passes}/{len(no_plan)} passed; uncached/cached/output/total = "
        f"{'/'.join(fmt(no_plan_tokens[key]) for key in TOKEN_FIELDS)}/{fmt(no_plan_total)}; "
        f"tokens per official full-task pass = {fmt(Fraction(no_plan_total, no_plan_passes))}. No planner charge applies, so both planning-cost views coincide. The historical Luna-max no-plan baseline is reported for outcome context only and is not mixed into the L2 planning-cost comparison."
    )
    rows += [
        "",
        "## Grading provenance note",
        "",
        "The final two EU rep-2 cells, `r70-4-elixir-fe2-l2criteria` and `r70-4-elixir-fe2-l2steps`, were officially graded with grade_worker SHA prefix `0e6f8aa0` rather than `73dc09af`. The difference was an inventory-glob-only change; scoring code was byte-identical. The result rows above use the latest official row for each exact cell ID.",
        "",
    ]
    return "\n".join(rows)


def verify_readme(cells, baseline, wins, losses, ties, net, p_observed, p_minimal):
    page = (ROUND / "README.md").read_text(encoding="utf-8")
    marker = "<!-- L2-CSV-SUMMARY:BEGIN -->"
    end_marker = "<!-- L2-CSV-SUMMARY:END -->"
    start = page.find(marker)
    end = page.find(end_marker)
    check(start >= 0 and end > start, "README CSV summary markers missing")
    actual = page[start : end + len(end_marker)]
    expected = render_readme_summary(cells, baseline, wins, losses, ties, net, p_observed, p_minimal)
    check(actual == expected, "README summary differs from CSV recomputation")
    commits = "<!-- L2-COMMIT-MAP:BEGIN -->"
    commits_end = "<!-- L2-COMMIT-MAP:END -->"
    cstart = page.find(commits)
    cend = page.find(commits_end)
    check(cstart >= 0 and cend > cstart, "README commit map markers missing")
    check(page[cstart : cend + len(commits_end)] == render_commit_map(cells, baseline), "README Kogen commit map differs from CSV")
    check("STATUS: **VALID**" in page, "README status is not VALID")
    families = sorted({task_family(row) for row in cells})
    planned_rows = [row for row in cells if row["level"] != "none"]
    builders = sorted({row["builder"] for row in planned_rows})
    reps = sorted({row["rep"] for row in planned_rows})
    n_line = (
        f"n: **{len(cells)} assigned cells**: {len(planned_rows)} factorial cells "
        f"({len(families)} variants × {len(LEVELS)} plan levels × {len(builders)} builders × {len(reps)} reps) "
        f"plus {sum(row['level']=='none' for row in cells)} Luna-low no-plan cells."
    )
    headline_line = "Headline: **" + expected.splitlines()[2].removeprefix("- Headline: ") + "**"
    check(n_line in page, "README sample-size line differs from CSV")
    check(headline_line in page, "README headline differs from CSV")
    for row in (
        "| Planned | 78 | All assigned cells |",
        "| Started | 78 | All gate and bulk cells |",
        "| Finished | 78 | All completed runs |",
        "| Officially graded | 78 | Latest official row per exact cell ID |",
        "| ITT denominator | 78 | All assigned cells |",
    ):
        check(row in page, "README lifecycle table differs from CSV: " + row)
    config = next((line for line in page.splitlines() if line.startswith("Configuration: ")), "")
    check("3,600-second cap and zero retries" in config and "builder CLI 0.160.0" in config and "planner CLI 0.160.1" in config, "README configuration/provenance mismatch")
    decision = (ROUND / "DECISION-RULE.md").read_text(encoding="utf-8")
    expected_decision_lines = (
        f"The official outcomes give {wins} steps-only wins, {losses} criteria-only wins, and {ties} ties: net +{net}/12.",
        f"The observed one-sided exact sign-test p-value, excluding ties, is {p_observed.numerator}/{p_observed.denominator} = {float(p_observed):.4f} across {wins+losses} discordant pairs.",
        f"Luna-low pass rates are descriptive: no-plan 1/6, criteria 4/12, approach 4/12, steps 6/12.",
        f"The recorded gate did not meet that stop condition; all {sum(row['stage']=='bulk' for row in cells)} planned rep-2 cells ran and were officially graded.",
    )
    for line in expected_decision_lines:
        check(line in decision, "decision rule differs from CSV: " + line)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the recomputed RESULTS.md instead of verifying it")
    args = parser.parse_args()
    cells, plans, baseline, plan_by_variant = read_and_check_data()
    pairs, wins, losses, ties, net, p_observed, p_minimal = primary_pairs(cells)
    rates = rate_summary(cells, baseline)
    costs = token_cost(cells, plans, plan_by_variant)
    expected = render_results(cells, plans, baseline, pairs, wins, losses, ties, net, p_observed, p_minimal, rates, costs)
    results_path = ROUND / "RESULTS.md"
    if args.write:
        results_path.write_text(expected, encoding="utf-8")
    else:
        actual = results_path.read_text(encoding="utf-8")
        check(actual == expected, "RESULTS.md differs from CSV recomputation")
        verify_readme(cells, baseline, wins, losses, ties, net, p_observed, p_minimal)
    print(
        f"L2 reproduction passed: {len(cells)} current official cells, {len(plans)} planner receipts, "
        f"{len(baseline)} historical baseline cells; primary {wins}-{losses}-{ties}, net +{net}."
    )


if __name__ == "__main__":
    main()
