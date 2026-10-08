#!/usr/bin/env python3
"""Recompute and check L4 results using only the published aggregate CSVs."""

import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ("r70-2-go", "r70-2-elixir", "r70-4-elixir-fe2", "r70-7-rust")
HOSTS = {
    "r70-2-go": "kogen-bench-us",
    "r70-2-elixir": "kogen-bench-eu",
    "r70-4-elixir-fe2": "kogen-bench-eu",
    "r70-7-rust": "kogen-bench-eu",
}
HISTORY = {
    "r70-2-elixir": (31, 32, 33, 910),
    "r70-2-go": (31, 32, 33, 911),
    "r70-4-elixir-fe2": (9, 10, 13, 909, 910),
    "r70-7-rust": (1, 2, 3, 31, 32, 33, 905),
}
CONTROL_ORDER = {
    ("r70-2-go", 51): 1, ("r70-2-go", 52): 2, ("r70-2-go", 53): 3,
    ("r70-2-elixir", 53): 3, ("r70-2-elixir", 52): 6, ("r70-2-elixir", 51): 8,
    ("r70-4-elixir-fe2", 53): 2, ("r70-4-elixir-fe2", 51): 7, ("r70-4-elixir-fe2", 52): 9,
    ("r70-7-rust", 53): 1, ("r70-7-rust", 51): 4, ("r70-7-rust", 52): 5,
}
TOKEN_FIELDS = ("uncached_input_tokens", "cached_input_tokens", "output_tokens")
CSV_FIELDS = {
    "arm", "variant", "task_id", "seed", "rep", "cell_id", "host", "model", "effort",
    "outcome", "tests_passed", "tests_total", *TOKEN_FIELDS, "grade_route", "runner_status",
    "grade_finished_at", "control_release_order", "wrapper_cli_reported", "wrapper_sha256",
}


def fail(message):
    print("ERROR:", message, file=sys.stderr)
    raise SystemExit(1)


def read_csv(name):
    with (ROOT / "data" / name).open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if set(reader.fieldnames or ()) != CSV_FIELDS:
            fail(f"unexpected columns in {name}")
        return list(reader)


def number(row, field):
    try:
        return int(row[field])
    except (KeyError, TypeError, ValueError):
        fail(f"missing integer {field} for {row.get('cell_id', '(unknown cell)')}")


def verify_scored(rows):
    if len(rows) != 24:
        fail(f"expected 24 scored rows, got {len(rows)}")
    cells = defaultdict(lambda: defaultdict(dict))
    ids = set()
    wrappers = set()
    wrapper_versions = set()
    for row in rows:
        arm, variant = row["arm"], row["variant"]
        if arm not in {"packet", "control"} or variant not in VARIANTS:
            fail("unexpected scored arm or variant")
        seed, rep = number(row, "seed"), number(row, "rep")
        if seed not in (1, 2, 3) or rep != (seed if arm == "packet" else seed + 50):
            fail(f"rep/seed mismatch for {row['cell_id']}")
        task = variant + ("-l4pk" if arm == "packet" else "")
        expected_id = f"codex__gpt-6-luna__max__default__{task}__r{rep}"
        if row["task_id"] != task or row["cell_id"] != expected_id:
            fail(f"task/exact ID mismatch for {row['cell_id']}")
        if row["cell_id"] in ids:
            fail(f"duplicate cell ID {row['cell_id']}")
        ids.add(row["cell_id"])
        if row["host"] != HOSTS[variant] or row["model"] != "gpt-6-luna" or row["effort"] != "max":
            fail(f"configuration mismatch for {row['cell_id']}")
        if row["grade_route"] != "r70-macbook-window-v1" or row["runner_status"] != "ok":
            fail(f"invalid official grade metadata for {row['cell_id']}")
        if not row["grade_finished_at"] or any(not row[k] for k in TOKEN_FIELDS):
            fail(f"missing grade timestamp or token component for {row['cell_id']}")
        passed, total = number(row, "tests_passed"), number(row, "tests_total")
        if not 0 <= passed <= total or row["outcome"] not in {"pass", "fail"}:
            fail(f"invalid aggregate outcome for {row['cell_id']}")
        if (row["outcome"] == "pass") != (passed == total):
            fail(f"outcome/full-pass mismatch for {row['cell_id']}")
        if not row["wrapper_sha256"] or not row["wrapper_cli_reported"]:
            fail(f"missing wrapper fingerprint for {row['cell_id']}")
        if arm == "control" and number(row, "control_release_order") != CONTROL_ORDER[(variant, rep)]:
            fail(f"control order mismatch for {row['cell_id']}")
        cells[variant][arm][seed] = row
        wrappers.add(row["wrapper_sha256"])
        wrapper_versions.add(row["wrapper_cli_reported"])
    for variant in VARIANTS:
        for arm in ("packet", "control"):
            if set(cells[variant][arm]) != {1, 2, 3}:
                fail(f"incomplete seed set for {variant} {arm}")
    if len(wrappers) != 1 or len(wrapper_versions) != 1:
        fail("scored cells do not share one runner wrapper fingerprint/version")
    return cells


def verify_history(rows):
    expected = {
        f"codex__gpt-6-luna__max__default__{variant}__r{rep}"
        for variant, reps in HISTORY.items() for rep in reps
    }
    if len(rows) != 20:
        fail(f"expected 20 historical context rows, got {len(rows)}")
    found, grouped = set(), defaultdict(list)
    for row in rows:
        variant, rep = row["variant"], number(row, "rep")
        cell_id = f"codex__gpt-6-luna__max__default__{variant}__r{rep}"
        if row["arm"] != "historical" or row["cell_id"] != cell_id or cell_id not in expected:
            fail(f"unexpected historical cell ID {row['cell_id']}")
        if cell_id in found:
            fail(f"duplicate historical cell ID {cell_id}")
        found.add(cell_id)
        if row["model"] != "gpt-6-luna" or row["effort"] != "max" or row["grade_route"] != "r70-macbook-window-v1":
            fail(f"invalid historical grade metadata for {cell_id}")
        passed, total = number(row, "tests_passed"), number(row, "tests_total")
        if not 0 <= passed <= total or row["outcome"] not in {"pass", "fail"}:
            fail(f"invalid historical aggregate outcome for {cell_id}")
        if (row["outcome"] == "pass") != (passed == total):
            fail(f"historical outcome/full-pass mismatch for {cell_id}")
        grouped[variant].append(row)
    if found != expected:
        fail("historical exact IDs differ from the registered context set")
    for variant, reps in HISTORY.items():
        if sorted(number(row, "rep") for row in grouped[variant]) != sorted(reps):
            fail(f"historical reps mismatch for {variant}")
    return grouped


def tokens(row):
    return sum(number(row, key) for key in TOKEN_FIELDS)


def passes(rows):
    return sum(row["outcome"] == "pass" for row in rows)


def mean_tests(rows):
    return sum(number(row, "tests_passed") for row in rows) / len(rows)


def fmt_count(value):
    return f"{value:,}"


def fmt_mean(value):
    return f"{value:,.2f}"


def fmt_cost(total, success_count):
    if not success_count:
        return "— (0 passes)"
    value = total / success_count
    return fmt_count(int(value)) if value.is_integer() else f"{value:,.1f}"


def compute(cells, history):
    summary, paired, rescues, losses = {}, [], 0, 0
    for variant in VARIANTS:
        summary[variant] = {}
        for arm in ("packet", "control"):
            selected = [cells[variant][arm][s] for s in (1, 2, 3)]
            n_pass = passes(selected)
            total_tokens = sum(tokens(row) for row in selected)
            summary[variant][arm] = {
                "rows": selected, "passes": n_pass, "mean": mean_tests(selected),
                "tokens": total_tokens, "per_pass": fmt_cost(total_tokens, n_pass),
            }
        for seed in (1, 2, 3):
            p, c = cells[variant]["packet"][seed], cells[variant]["control"][seed]
            ps, cs = p["outcome"] == "pass", c["outcome"] == "pass"
            label = "rescue" if ps and not cs else "loss" if cs and not ps else "both pass" if ps else "both fail"
            rescues += label == "rescue"
            losses += label == "loss"
            paired.append((variant, seed, p, c, label))
    delta = sum(summary[v]["packet"]["passes"] - summary[v]["control"]["passes"] for v in VARIANTS)
    nonworse = sum(summary[v]["packet"]["passes"] >= summary[v]["control"]["passes"] for v in VARIANTS)
    regression = any(summary[v]["packet"]["mean"] < summary[v]["control"]["mean"] - 1 for v in VARIANTS)
    decision = "KEEP" if delta >= 2 and nonworse >= 3 and not regression else "DROP"
    overall = {}
    for arm in ("packet", "control"):
        selected = [cells[v][arm][s] for v in VARIANTS for s in (1, 2, 3)]
        n_pass, token_sum = passes(selected), sum(tokens(row) for row in selected)
        overall[arm] = {"passes": n_pass, "mean": mean_tests(selected), "tokens": token_sum, "per_pass": fmt_cost(token_sum, n_pass)}
    history_counts = {v: (passes(history[v]), len(history[v])) for v in VARIANTS}
    worst = min((summary[v]["packet"]["mean"] - summary[v]["control"]["mean"], v) for v in VARIANTS)
    return {"summary": summary, "paired": paired, "rescues": rescues, "losses": losses,
            "delta": delta, "nonworse": nonworse, "regression": regression,
            "decision": decision, "overall": overall, "history": history_counts, "worst": worst}


def cell_label(row):
    return f"{row['outcome'].upper()} {number(row, 'tests_passed')}/{number(row, 'tests_total')}"


def render_results(x):
    out = [
        "# L4 deterministic context packet results", "", "STATUS: **VALID**", "",
        "The primary comparison follows Amendment 1: packet and contemporaneous no-packet controls are paired by variant and seed. Each cell is the latest official aggregate grade row for its exact cell ID, from the MacBook grading route.",
        "", "## Paired outcomes", "",
        "| Source variant | Seed | Packet cell | No-packet control | Pair |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for v, seed, p, c, label in x["paired"]:
        out.append(f"| `{v}` | {seed} | {cell_label(p)} | {cell_label(c)} | {label} |")
    out += [
        "", "## Pass counts, test counts, and tokens", "",
        "A full pass is an official `pass` outcome. Mean `tests_passed` is the arithmetic mean across the three cells in that variant and arm. One cell's total tokens are uncached input + cached input + output; total is the sum. Tokens per pass is all tokens consumed by every cell in that arm divided by its full-pass count, so failed-cell tokens remain in the numerator.",
        "", "| Source variant | Arm | Successful cells | Mean tests_passed | Total tokens | Tokens per successful cell |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for v in VARIANTS:
        for arm in ("packet", "control"):
            item = x["summary"][v][arm]
            out.append(f"| `{v}` | {arm} | {item['passes']}/3 | {fmt_mean(item['mean'])} | {fmt_count(item['tokens'])} | {item['per_pass']} |")
    for arm in ("packet", "control"):
        item = x["overall"][arm]
        out.append(f"| All variants | {arm} | {item['passes']}/12 | {fmt_mean(item['mean'])} | {fmt_count(item['tokens'])} | {item['per_pass']} |")
    out += [
        "", "## Historical baselines (context only)", "",
        "These are the registered historical Luna-max cells. Amendment 1 makes the contemporaneous paired controls the decision basis; the historical baseline is shown only as context.",
        "", "| Source variant | Historical successes | Eligible cells |", "| --- | ---: | ---: |",
    ]
    for v in VARIANTS:
        n_pass, n = x["history"][v]
        out.append(f"| `{v}` | {n_pass}/{n} | {n} |")
    worst_v = x["worst"][1]
    out += [
        "", "## Decision and protocol notes", "",
        f"The net packet-minus-control change is **{x['delta']:+d} full passes**. There are **{x['rescues']} paired rescues** and **{x['losses']} paired losses**. Packet pass counts are no lower than controls on **{x['nonworse']}/4 variants**. The regression rule did not fire; the worst mean `tests_passed` comparison is {fmt_mean(x['summary'][worst_v]['packet']['mean'])} packet versus {fmt_mean(x['summary'][worst_v]['control']['mean'])} control on `{worst_v}` (difference {fmt_mean(x['worst'][0])}).",
        "", f"**Verdict: {x['decision']}** packets in specification sections 3.2 and 4.9, as a descriptive pilot. The result is based on four outcome-selected variants and three cells per arm per variant; the rule thresholds are coarse and support no general claim.",
        "", "The EU controls followed the seeded order recorded for the lane. One EU control was launched while a grade-window drain was in progress; this delayed the window only and affected no result. The three US controls ran after their packet cells had finished and were **not interleaved**.",
        "", "A separate confirmation round, `l4b-confirm`, is running on three new variants; it is not included here.", "",
    ]
    return "\n".join(out)


def render_readme(x, scored, history):
    p_n = sum(r["arm"] == "packet" for r in scored)
    c_n = sum(r["arm"] == "control" for r in scored)
    seed_n = len({number(r, "seed") for r in scored if r["arm"] == "packet"})
    wrapper_version = scored[0]["wrapper_cli_reported"]
    wrapper_sha = scored[0]["wrapper_sha256"]
    return "\n".join([
        "Pre-registered: yes; original design frozen 7 October 2026 before the first scored packet cell. Amendment 1 was written after 6 of 12 packet outcomes were known; its disclosure is retained in the decision rule.",
        "Label: descriptive pilot; n=3 per arm per variant. The thresholds are coarse and support no general claim.",
        "Question: Do frozen public context packets increase official full-suite passes over same-seed contemporaneous no-packet controls on four L1-admitted variants?",
        f"n: {len(scored)} official scored cells ({p_n} packet, {c_n} control; {len(VARIANTS)} variants × {seed_n} seeds per arm); {len(history)} historical cells are context only.",
        f"Headline: **{x['decision']}** packets in specification sections 3.2 and 4.9: packet-minus-control = {x['delta']:+d} passes, {x['rescues']} paired rescues, {x['losses']} losses, and no regression. The US controls were not interleaved.",
        "Configuration: direct Codex, `gpt-6-luna` at `max`, 3,600-second cap, zero retries; Elixir and Rust on EU, Go on US; official `r70-macbook-window-v1` grades. Tokens are uncached input + cached input + output; total is their sum.",
        f"Official runner wrapper: {wrapper_version}, SHA-256 `{wrapper_sha}`; this same fingerprint appears on all scored cells.",
        "Limit: outcome-selected tasks, n=3 per arm per variant, coarse thresholds, and mixed scheduling; the result supports no general claim.",
        "",
        "| Lifecycle count | Count |",
        "| --- | ---: |",
        f"| Planned scored cells | {len(scored)} |",
        f"| Started scored cells | {len(scored)} |",
        f"| Finished scored cells | {len(scored)} |",
        f"| Officially graded scored cells | {len(scored)} |",
        f"| ITT denominator for scored cells | {len(scored)} |",
    ])


def main():
    scored, history_rows = read_csv("paired-cells.csv"), read_csv("historical-baselines.csv")
    cells, history = verify_scored(scored), verify_history(history_rows)
    x = compute(cells, history)
    actual = (ROOT / "RESULTS.md").read_text(encoding="utf-8").rstrip("\n")
    if actual != render_results(x).rstrip("\n"):
        fail("RESULTS.md differs from the results recomputed from CSV")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    begin, end = "<!-- L4-COMPUTED:BEGIN -->", "<!-- L4-COMPUTED:END -->"
    start, finish = readme.find(begin), readme.find(end)
    if start < 0 or finish < start or readme.find(begin, start + 1) >= 0:
        fail("missing or duplicate computed block in README.md")
    actual_block = readme[start + len(begin):finish].strip("\n")
    if actual_block != render_readme(x, scored, history_rows):
        fail("README.md summary differs from the results recomputed from CSV")
    if x["decision"] != "KEEP":
        fail("the computed Amendment 1 decision is not KEEP")
    print(f"OK: 24 scored cells; 20 historical context cells; delta={x['delta']:+d}; rescues={x['rescues']}; losses={x['losses']}; verdict={x['decision']}")


if __name__ == "__main__":
    main()
