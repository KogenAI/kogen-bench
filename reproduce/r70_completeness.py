#!/usr/bin/env python3
"""Rebuild and audit the public Round 70 completeness tables from public ledgers."""
import argparse
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_ORDER = ("r70-1", "r70-3", "r70-4", "r70-6")
STACK_ORDER = ("rust", "go", "ts-bun", "elixir", "gleam")
LANGUAGE_ORDER = ("rust", "ts-bun", "go", "elixir")
LABEL = {"rust": "Rust", "go": "Go", "ts-bun": "TypeScript/Bun", "elixir": "Elixir", "gleam": "Gleam"}
REGION = {"kogen-bench-eu": "Europe", "kogen-bench-us": "US"}
HOST = {"rust": "Europe", "elixir": "Europe", "go": "US", "ts-bun": "US"}
COST_FIELDS = (
    "cell_id", "cohort", "task", "stack", "rep", "host",
    "requested_model", "effective_model", "requested_effort", "effective_effort",
    "harness", "harness_version", "harness_fingerprint",
    "uncached_input_tokens", "cached_input_tokens", "cache_write_tokens",
    "output_tokens", "reasoning_tokens", "total_tokens", "wall_s", "cost_usd",
    "price_table_version", "calculator_version", "cost_accounting",
)
MARKERS = {
    "original": ("R70-RVE-ORIGINAL", "rounds/r70/README.md"),
    "rerun": ("R70-RVE-RERUN-FRACTIONS", "rounds/r70-rve-rerun/RESULTS.md"),
    "mixed": ("R70-RVE-MIXED-COHORT", "rounds/r70-rve-ext/RESULTS.md"),
    "native": ("R70-NATIVE-CHECK-DIAGNOSTIC", "rounds/r70-compile/RESULTS.md"),
    "compilehost": ("R70-COMPILE-HOST", "rounds/r70-compile/RESULTS.md"),
    "transcript": ("R70-AGENT-WALL-DIAGNOSTIC", "rounds/r70/README.md"),
    "cost": ("R70-ORIGINAL-COST-SUMMARY", "rounds/r70/README.md"),
}


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def dump_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows))


def fraction(rows):
    return f"{sum(row.get('outcome') == 'pass' for row in rows)}/{len(rows)}"


def md_num(value, digits=3):
    return f"{value:.{digits}f}"


def frac_tests(row):
    return f"{row['tests_passed']}/{row['tests_total']}"


def ordered(rows):
    stack_idx = {stack: i for i, stack in enumerate(STACK_ORDER)}
    return sorted(rows, key=lambda r: (
        int(r.get("task", "r70-999").split("-")[1]),
        stack_idx.get(r.get("stack"), 99), int(r.get("rep", 0)),
    ))


def replace_block(text, label, body):
    begin = f"<!-- {label}:BEGIN -->"
    end = f"<!-- {label}:END -->"
    if text.count(begin) != 1 or text.count(end) != 1:
        raise ValueError(f"Expected exactly one generated block for {label}")
    start = text.index(begin) + len(begin)
    finish = text.index(end)
    if finish < start:
        raise ValueError(f"Malformed generated block for {label}")
    return text[:start] + "\n\n" + body.rstrip() + "\n\n" + text[finish:]


def original_rows(root):
    tests = [r for r in read_jsonl(root / "results/test-counts.jsonl")
             if r.get("cohort") == "r70-original-rve" and r.get("scored") is True]
    checks = {r["cell_id"]: r["make_check"] for r in read_jsonl(root / "reproduce/inputs/r70-original-own-checks.jsonl")}
    if len(tests) != 40 or len(checks) != 40:
        raise ValueError("The original RvE table requires 40 official rows and 40 own-check receipts")
    if {r["cell_id"] for r in tests} != set(checks):
        raise ValueError("Original own-check identities do not match the official test-count ledger")
    for row in tests:
        row["make_check"] = checks[row["cell_id"]]
    return ordered(tests)


def render_original(rows):
    by_stack = {s: [r for r in rows if r["stack"] == s] for s in ("rust", "go", "ts-bun", "elixir")}
    summary = [
        "| Stack | Official full passes | n | Per-task n (1 / 3 / 4 / 6) | Own checks passing | Region |",
        "| --- | ---: | ---: | --- | ---: | --- |",
    ]
    for stack in ("rust", "go", "ts-bun", "elixir"):
        selected = by_stack[stack]
        ns = [sum(r["task"] == f"r70-{task}-{stack}" for r in selected) for task in (1, 3, 4, 6)]
        checks = sum(r["make_check"] == "pass" for r in selected)
        summary.append(
            f"| {LABEL[stack]} | {fraction(selected)} | {len(selected)} | "
            f"{' / '.join(map(str, ns))} | {checks}/{len(selected)} | {HOST[stack]} |"
        )
    detail = [
        "| Task | Stack | Rep | Region | Hidden tests passed/total | Official result | Own check (secondary) |",
        "| --- | --- | ---: | --- | ---: | --- | --- |",
    ]
    for row in rows:
        task_no = row["task"].split("-")[1]
        detail.append(
            f"| {task_no} | {LABEL[row['stack']]} | {row['rep']} | {REGION[row['host']]} | "
            f"{frac_tests(row)} | {row['outcome']} | {row['make_check']} |"
        )
    return "\n".join(summary + ["", "Per-cell as-graded observations:", ""] + detail)


def mixed_cohorts(tests):
    original = [r for r in tests if r.get("cohort") == "r70-original-rve" and r.get("scored") is True]
    rerun = [r for r in tests if r.get("cohort") == "r70-rve-rerun" and r.get("scored") is True]
    ext = [r for r in tests if r.get("cohort") == "r70-rve-ext" and r.get("scored") is True]
    observed = {}
    for stack in ("rust", "go", "ts-bun", "elixir"):
        mix = [r for r in original if r["stack"] == stack and r["task"] != f"r70-4-{stack}"]
        if stack == "elixir":
            mix = [r for r in mix if r["task"] != "r70-1-elixir"]
        mix.extend(r for r in rerun if r["stack"] == stack)
        pre = [r for r in ext if r["stack"] == stack and r["rep"] in (31, 32)]
        all_ext = [r for r in ext if r["stack"] == stack]
        observed[stack] = (mix + pre, mix + all_ext)
    return observed


def render_mixed(tests):
    values = mixed_cohorts(tests)
    lines = [
        "| Stack | Mixed cohort + extension reps 31–32 | Same mix + reps 31–33 (rep 33 post-hoc) |",
        "| --- | ---: | ---: |",
    ]
    for stack in LANGUAGE_ORDER:
        pre, post = values[stack]
        lines.append(f"| {LABEL[stack]} | {fraction(pre)} | {fraction(post)} |")
    return "\n".join(lines)


def render_rerun(tests):
    originals = [r for r in tests if r.get("cohort") == "r70-original-rve"
                 and r.get("scored") is True and (r.get("task") == "r70-1-elixir" or r.get("task", "").startswith("r70-4-"))]
    reruns = [r for r in tests if r.get("cohort") == "r70-rve-rerun" and r.get("scored") is True]
    rows = [(row, "original") for row in originals] + [(row, "FE2 rerun") for row in reruns]
    stack_order = {s: i for i, s in enumerate(("rust", "elixir", "go", "ts-bun"))}
    rows.sort(key=lambda pair: (
        int(pair[0]["task"].split("-")[1]),
        stack_order[pair[0]["stack"]], 0 if pair[1] == "original" else 1, int(pair[0]["rep"]),
    ))
    lines = [
        "| Task | Stack | Cohort | Rep | Hidden tests passed/total | Official result |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for row, cohort in rows:
        lines.append(
            f"| {row['task'].split('-')[1]} | {LABEL[row['stack']]} | {cohort} | {row['rep']} | "
            f"{frac_tests(row)} | {row['outcome']} |"
        )
    original_by = {(r["task"], r["stack"]): [] for r, cohort in rows if cohort == "original"}
    rerun_by = {}
    for row, cohort in rows:
        key = (row["task"].removesuffix("-fe2"), row["stack"])
        (original_by if cohort == "original" else rerun_by).setdefault(key, []).append(row)
    lines += [
        "",
        "Task-level hidden-test totals (these are sums across three cells, not independent samples):",
        "",
        "| Task | Stack | Original hidden-test counts | FE2 hidden-test counts |",
        "| --- | --- | ---: | ---: |",
    ]
    for task, stack in (
        ("r70-1-elixir", "elixir"),
        ("r70-4-rust", "rust"),
        ("r70-4-go", "go"),
        ("r70-4-ts-bun", "ts-bun"),
        ("r70-4-elixir", "elixir"),
    ):
        old = original_by.get((task, stack), [])
        new = rerun_by.get((task, stack), [])
        if task == "r70-1-elixir":
            old_fraction = "each " + frac_tests(old[0])
            new_fraction = "each " + frac_tests(new[0])
        else:
            old_fraction = f"{sum(r['tests_passed'] for r in old)}/{sum(r['tests_total'] for r in old)}"
            new_fraction = f"{sum(r['tests_passed'] for r in new)}/{sum(r['tests_total'] for r in new)}"
        task_label = "1" if task == "r70-1-elixir" else "4"
        lines.append(f"| {task_label} | {LABEL[stack]} | {old_fraction} | {new_fraction} |")
    return "\n".join(lines)


def render_native(root):
    rows = read_jsonl(root / "reproduce/inputs/r70-native-diagnostic-samples.jsonl")
    lines = [
        "| Task | Stack | n | Full make check, median [min–max] s | Hidden wrapper + pytest, median [min–max] s |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for task in (1, 4, 6):
        for stack in STACK_ORDER:
            selected = [r for r in rows if r["task"] == f"r70-{task}-{stack}"]
            if len(selected) != 3:
                raise ValueError(f"Expected n=3 native diagnostic samples for task {task} {stack}")
            checks = [r["full_make_check_s"] for r in selected]
            hidden = [r["hidden_wrapper_pytest_s"] for r in selected]
            lines.append(
                f"| {task} | {LABEL[stack]} | 3 | "
                f"{md_num(statistics.median(checks))} [{md_num(min(checks))}–{md_num(max(checks))}] | "
                f"{md_num(statistics.median(hidden))} [{md_num(min(hidden))}–{md_num(max(hidden))}] |"
            )
    return "\n".join(lines)


def render_compile_host(root):
    source = json.loads((root / "reproduce/inputs/r70-compile-host.json").read_text())
    loads = source["pre_cold_load_1m"]
    if len(loads) != 75:
        raise ValueError(f"Expected 75 pre-cold load samples, got {len(loads)}")
    ram_gib = source["ram_bytes"] / (1024 ** 3)
    model = source["cpu_model"].removesuffix(" Processor")
    vcpu = source["vcpu"]
    median_load = statistics.median(loads)
    return (
        f"Reported host snapshot: {model}, {vcpu} vCPU, {ram_gib:.1f} GiB, "
        f"kernel {source['kernel']}. Median pre-cold 1-minute load was "
        f"{median_load:.1f} on {vcpu} vCPUs, mostly from preceding builds; "
        "stacks were interleaved per rep so the drift was shared."
    )


def quartiles(values):
    if len(values) < 2:
        return values[0], values[0], values[0]
    q1, _, q3 = statistics.quantiles(values, n=4, method="inclusive")
    return statistics.median(values), q1, q3


def render_transcript(root):
    rows = read_jsonl(root / "reproduce/inputs/r70-transcript-share-samples.jsonl")
    lines = [
        "| Stack | Timed cells n | Build/check/test wall share, median [Q1–Q3] | Residual share, median [Q1–Q3] |",
        "| --- | ---: | ---: | ---: |",
    ]
    for stack in ("rust", "go", "ts-bun", "elixir", "gleam"):
        selected = [r for r in rows if r["stack"] == stack]
        build = [r["build_check_test_s"] / r["wall_s"] for r in selected]
        residual = [1 - r["all_commands_s"] / r["wall_s"] for r in selected]
        if not selected:
            raise ValueError(f"No transcript samples for {stack}")
        med, q1, q3 = quartiles(build)
        rmed, rq1, rq3 = quartiles(residual)
        pct = lambda x: f"{x * 100:.1f}%"
        lines.append(
            f"| {LABEL[stack]} | {len(selected)} | {pct(med)} [{pct(q1)}–{pct(q3)}] | "
            f"{pct(rmed)} [{pct(rq1)}–{pct(rq3)}] |"
        )
    if len(rows) != 108:
        raise ValueError(f"Expected 108 timed transcript samples, got {len(rows)}")
    return "\n".join(lines)


def resource_rows(root, tests):
    current = read_jsonl(root / "results/cost-time.jsonl")
    if len(current) == 44 and all("cohort" not in r for r in current):
        rows44 = current
    else:
        rows44 = [r for r in current if r.get("cohort") in {"r70-rve-ext", "r70-rve-rerun"}]
    existing_ids = {r["cell_id"] for r in rows44}
    if len(rows44) != 44:
        raise ValueError("Expected 44 existing rerun/extension resource rows")
    tests_by_id = {r["cell_id"]: r for r in tests}
    extended = []
    for row in rows44:
        grade = tests_by_id.get(row["cell_id"])
        if not grade or grade.get("cohort") not in {"r70-rve-ext", "r70-rve-rerun"}:
            raise ValueError("Existing cost/time ID did not join to its official test-count row")
        parts = row["cell_id"].split("__")
        if len(parts) != 6:
            raise ValueError("Unexpected public Round 70 cell ID shape")
        extended.append({
            "cell_id": row["cell_id"], "cohort": grade["cohort"], "task": grade["task"],
            "stack": grade["stack"], "rep": grade["rep"], "host": grade["host"],
            "requested_model": parts[1], "effective_model": None,
            "requested_effort": parts[2], "effective_effort": None,
            "harness": "codex", "harness_version": None, "harness_fingerprint": None,
            "uncached_input_tokens": row["uncached_input_tokens"],
            "cached_input_tokens": row["cached_input_tokens"], "cache_write_tokens": None,
            "output_tokens": row["output_tokens"], "reasoning_tokens": None,
            "total_tokens": row["total_tokens"], "wall_s": row["wall_s"],
            "cost_usd": None, "price_table_version": None, "calculator_version": None,
            "cost_accounting": None,
        })
    original = read_jsonl(root / "reproduce/inputs/r70-original-resource-receipts.jsonl")
    if len(original) != 20 or {r["cell_id"] for r in original} & existing_ids:
        raise ValueError("Original RvE resource receipts must contain 20 new, unique rows")
    for row in original:
        total = sum(row[k] for k in (
            "uncached_input_tokens", "cached_input_tokens", "output_tokens"
        ))
        extended.append({
            **row,
            "harness_version": row.get("codex_cli_version"),
            "total_tokens": total,
        })
        extended[-1].pop("codex_cli_version", None)
    if len(extended) != 64 or len({r["cell_id"] for r in extended}) != 64:
        raise ValueError("The expanded cost/time ledger must contain 64 unique cells")
    return sorted(extended, key=lambda r: (r["cohort"], r["cell_id"]))


def render_cost(root, ledger_rows):
    original = [r for r in ledger_rows if r["cohort"] == "r70-original-rve" and r["cost_usd"] is not None]
    excluded = read_jsonl(root / "reproduce/inputs/r70-original-excluded-resource.jsonl")
    lines = [
        "The 20 scored records do not preserve a cache-write token counter; cache_write_tokens is null, not zero. The displayed token medians and totals sum the recorded uncached-input, cached-input, and output components. Reasoning is included within output and is not added a second time.",
        "",
        "Scored original RvE resource receipts:",
        "",
        "| Stack | n | Cost USD median [min–max] | Median uncached / cached / output / reasoning tokens |",
        "| --- | ---: | ---: | --- |",
    ]
    for stack in ("rust", "elixir"):
        selected = [r for r in original if r["stack"] == stack]
        if len(selected) != 10:
            raise ValueError(f"Expected ten scored cost receipts for {stack}")
        cost = [r["cost_usd"] for r in selected]
        counters = [
            f"{int(statistics.median([r[k] for r in selected])):,}"
            for k in ("uncached_input_tokens", "cached_input_tokens", "output_tokens", "reasoning_tokens")
        ]
        lines.append(
            f"| {LABEL[stack]} | {len(selected)} | "
            f"{statistics.median(cost):.4f} [{min(cost):.4f}–{max(cost):.4f}] | "
            f"{' / '.join(counters)} |"
        )
    lines += [
        "",
        "Five ungraded deliveries excluded before scoring (individual resource spend only):",
        "",
        "| Delivery | Stack | Cost USD | Wall s | Uncached / cached / cache-write / output / reasoning tokens |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for row in excluded:
        counters = [row[k] for k in ("uncached_input_tokens", "cached_input_tokens", "cache_write_tokens", "output_tokens", "reasoning_tokens")]
        lines.append(
            f"| {row['delivery']} | {LABEL[row['stack']]} | {row['cost_usd']:.6f} | "
            f"{row['wall_s']:.3f} | {' / '.join(f'{v:,}' for v in counters)} |"
        )
    lines += [
        "",
        "Scored plus excluded all-attempt totals by stack:",
        "",
        "| Stack | Scored cost USD total | Excluded deliveries | Excluded cost USD total | All-attempt cost USD total | All-attempt tokens |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for stack in ("rust", "elixir"):
        scored = [r for r in original if r["stack"] == stack]
        attempts = [r for r in excluded if r["stack"] == stack]
        scored_cost = sum(r["cost_usd"] for r in scored)
        excluded_cost = sum(r["cost_usd"] for r in attempts)
        scored_tokens = sum(r["total_tokens"] for r in scored)
        excluded_tokens = sum(sum(r[k] for k in (
            "uncached_input_tokens", "cached_input_tokens", "output_tokens"
        )) for r in attempts)
        lines.append(
            f"| {LABEL[stack]} | {scored_cost:.6f} | {len(attempts)} | "
            f"{excluded_cost:.6f} | {scored_cost + excluded_cost:.6f} | "
            f"{scored_tokens + excluded_tokens:,} |"
        )
    return "\n".join(lines)


def write_metadata(root):
    rows = read_jsonl(root / "reproduce/inputs/r70-original-resource-receipts.jsonl")
    versions = {(r["price_table_version"], r["calculator_version"]) for r in rows}
    if len(versions) != 1:
        raise ValueError("Original RvE resource receipts do not share one pricing/calculator version")
    price, calc = next(iter(versions))
    metadata = {
        "schema_version": 1,
        "official_cell_rows": 64,
        "rows_with_versioned_cost_receipts": 20,
        "rows_without_verified_cost_or_reasoning_receipts": 44,
        "original_rve_price_table_version": price,
        "original_rve_calculator_version": calc,
        "original_rve_cost_definition": "Source-reported Standard API equivalent, not invoice spend. The source accounting prices uncached input, cached input, cache writes and output once; the per-cell original records do not preserve a cache-write token counter, so that counter remains null. Reasoning is a subset of output and is not added twice.",
        "accounting_caveat": "Cumulative Codex receipts do not establish per-request context; long-context reconciliation is false and any surcharge is unresolved.",
        "coverage_note": "The 44 rerun and extension rows have official outcomes, test fractions, uncached/cached/output token values and wall seconds. Cost, reasoning counters, effective model/effort receipts and per-cell harness version are unavailable in the permitted records and remain null, not zero. The 20 original per-cell records do not preserve cache-write token counts; total_tokens sums only recorded uncached-input, cached-input, and output counters.",
        "excluded_attempts_note": "Five ungraded deliveries are shown separately and excluded from scored medians. Their cost values are source-reported; the permitted excluded-delivery summary contains no price-table or calculator version.",
    }
    (root / "results/cost-time-metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")


def generated_blocks(root, tests, ledger_rows):
    original = original_rows(root)
    return {
        "original": render_original(original),
        "rerun": render_rerun(tests),
        "mixed": render_mixed(tests),
        "native": render_native(root),
        "compilehost": render_compile_host(root),
        "transcript": render_transcript(root),
        "cost": render_cost(root, ledger_rows),
    }


def write_blocks(root, blocks):
    for key, (label, rel) in MARKERS.items():
        path = root / rel
        text = path.read_text()
        path.write_text(replace_block(text, label, blocks[key]))


def audit_generated_blocks(root, blocks):
    errors = []
    for key, (label, rel) in MARKERS.items():
        path = root / rel
        try:
            text = path.read_text()
        except OSError:
            errors.append(f"Missing generated Round 70 page: {rel}")
            continue
        begin, end = f"<!-- {label}:BEGIN -->", f"<!-- {label}:END -->"
        if text.count(begin) != 1 or text.count(end) != 1:
            errors.append(f"Generated block markers missing or duplicated: {rel} {label}")
            continue
        actual = text[text.index(begin) + len(begin):text.index(end)].strip()
        if actual != blocks[key].strip():
            errors.append(f"Generated Round 70 table differs from public source data: {rel} {label}")
    return errors


def self_test():
    label = "SELFTEST"
    expected = "| Rust | 5/6 |"
    fixture = f"before\n<!-- {label}:BEGIN -->\n{expected}\n<!-- {label}:END -->\nafter\n"

    def matches(value):
        begin, end = f"<!-- {label}:BEGIN -->", f"<!-- {label}:END -->"
        actual = value[value.index(begin) + len(begin):value.index(end)].strip()
        return actual == expected

    if not matches(fixture):
        raise RuntimeError("Completeness audit self-test rejected a matching table")
    if matches(fixture.replace("5/6", "4/6")):
        raise RuntimeError("Completeness audit self-test accepted a mutated fraction")


def audit(root=ROOT):
    errors = []
    try:
        tests = read_jsonl(root / "results/test-counts.jsonl")
        cost_rows = read_jsonl(root / "results/cost-time.jsonl")
        original = original_rows(root)
        by_stack = {stack: [r for r in original if r["stack"] == stack] for stack in ("rust", "go", "ts-bun", "elixir")}
        expected = {"rust": "8/10", "elixir": "2/10", "go": "7/10", "ts-bun": "7/10"}
        for stack, value in expected.items():
            if fraction(by_stack[stack]) != value:
                errors.append(f"Original RvE pass count differs for {stack}")
        resources = [r for r in cost_rows if r.get("cohort") == "r70-original-rve"]
        supplements = [r for r in cost_rows if r.get("cohort") in {"r70-rve-ext", "r70-rve-rerun"}]
        if len(resources) != 20 or len(supplements) != 44 or len(cost_rows) != 64:
            errors.append("Cost/time coverage must be 20 original RvE plus 44 rerun/extension cells")
        if len({r.get("cell_id") for r in cost_rows}) != len(cost_rows):
            errors.append("Cost/time ledger contains duplicate exact cell IDs")
        for row in cost_rows:
            if set(row) != set(COST_FIELDS):
                errors.append(f"Cost/time row field set mismatch: {row.get('cell_id')}")
            if row.get("cohort") in {"r70-rve-ext", "r70-rve-rerun"}:
                for field in ("cost_usd", "reasoning_tokens", "effective_model", "effective_effort", "harness_version"):
                    if row.get(field) is not None:
                        errors.append(f"Unverified supplemental field {field} is not null: {row.get('cell_id')}")
            elif row.get("cohort") == "r70-original-rve":
                for field in ("cost_usd", "reasoning_tokens", "price_table_version", "calculator_version", "harness_version"):
                    if row.get(field) is None:
                        errors.append(f"Missing verified original RvE field {field}: {row.get('cell_id')}")
                if row.get("cache_write_tokens") is not None:
                    errors.append(f"Original cache-write counter should remain null: {row.get('cell_id')}")
                total = sum(row[k] for k in ("uncached_input_tokens", "cached_input_tokens", "output_tokens"))
                if total != row["total_tokens"]:
                    errors.append(f"Original token total mismatch: {row.get('cell_id')}")
            else:
                errors.append(f"Unknown cost/time cohort: {row.get('cohort')}")
        blocks = generated_blocks(root, tests, cost_rows)
        errors.extend(audit_generated_blocks(root, blocks))
        checks = {
            "rounds/r70/README.md": (
                "one model, direct Codex with gpt-6-luna at max",
                "Tasks 1 and 4 are confounded by skeleton front-end traps; repetition selection was partly strategic.",
                "no general language ranking follows",
                "108 timed original r70 cells",
                "it is not model latency",
            ),
            "rounds/r70-rve-rerun/RESULTS.md": (
                "grader SHA-256 `616b1d53",
                "Go used front end v1",
                "Rust, Elixir, and TypeScript/Bun used front end v2",
                "do not establish a causal front-end effect",
            ),
            "rounds/r70-rve-ext/RESULTS.md": (
                "illustrative mixed cohort, not a corrected estimate",
                "rep 33 is post-hoc",
            ),
            "rounds/r70-rve-ext/README.md": (
                "pre-registered reps 31–32 and post-hoc rep 33",
                "Wall comparisons are within-host only",
            ),
            "rounds/r70-compile/RESULTS.md": (
                "Host specification and load context:",
                "separate diagnostic, not a compile-only ranking",
            ),
            "rounds/r70-task8/RESULTS.md": (
                "planned n=8; scored n=0",
                "kogen-bench-us",
                "gpt-6-luna at max",
                "3600-second cap",
                "zero retries",
                "13/25",
                "No task-8 smoke was launched for Elixir or TypeScript/Bun",
                "Per-smoke usage and cost are unverified in the permitted public receipts; they are not zero",
            ),
            "results/cost-time-metadata.json": (
                "not invoice spend",
                "long-context reconciliation is false",
                "remain null, not zero",
            ),
        }
        for rel, fragments in checks.items():
            text = (root / rel).read_text()
            for fragment in fragments:
                if fragment not in text:
                    errors.append(f"Required Round 70 qualification missing from {rel}: {fragment}")
        if "not timing or token comparisons" in (root / "rounds/r70-rve-ext/README.md").read_text():
            errors.append("Extension README retains stale no-timing/no-token wording")
        return sorted(set(errors))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [f"Round 70 completeness audit could not finish: {exc}"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write expanded ledger, metadata and generated tables")
    args = parser.parse_args()
    self_test()
    if args.write:
        tests = read_jsonl(ROOT / "results/test-counts.jsonl")
        rows = resource_rows(ROOT, tests)
        dump_jsonl(ROOT / "results/cost-time.jsonl", rows)
        write_metadata(ROOT)
        write_blocks(ROOT, generated_blocks(ROOT, tests, rows))
    errors = audit()
    if errors:
        raise SystemExit("\n".join(errors))
    print("Round 70 completeness tables and resource coverage validated; mutation self-test passed.")


if __name__ == "__main__":
    main()
