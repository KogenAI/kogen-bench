#!/usr/bin/env python3
"""Recompute release-round claims from public rows; emit no task or suite details.

This is a deliberately fail-closed audit aid, not a substitute for human sign-off.
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUNDS = ("l3-repair", "l3b-repair-vs-continue", "lang-sol-replication")


def rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def records(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def missing(value) -> bool:
    if value is None or value == "":
        return True
    if isinstance(value, dict):
        if "missing" in value or "withheld" in value:
            return True
        return any(missing(v) for v in value.values())
    return False


def at(value: dict, *keys):
    for key in keys:
        value = value.get(key) if isinstance(value, dict) else None
    return value


def issue(out: dict, code: str, detail: str, location: str):
    out["issues"].append({"code": code, "detail": detail, "location": location})


def assert_claim(out: dict, text: str, pattern: str, expected: tuple[int, ...], location: str):
    match = re.search(pattern, text, flags=re.I | re.S)
    if not match:
        issue(out, "claim_missing", "Expected numerical claim is absent or changed", location)
    elif tuple(map(int, match.groups())) != expected:
        issue(out, "count_mismatch", f"Reported {match.groups()}; recomputed {expected}", location)


def assert_percent_claim(out: dict, text: str, expected: tuple[float, ...], location: str):
    match = re.search(r"(?:equal-task mean is Rust |task-specific pass fractions is )(\d+\.\d+)%, (?:Go )?(\d+\.\d+)%, and (?:TS-Bun )?(\d+\.\d+)%", text)
    if not match or tuple(map(float, match.groups())) != expected:
        issue(out, "rate_mismatch", f"Equal-task percentages differ from recomputed {expected}", location)


def valid_outcome(row: dict, key: str = "outcome") -> bool:
    return row.get(key, "").lower() in {"pass", "fail", "invalid"}


def check_usage(out: dict, data: list[dict], keys: tuple[str, str, str], location: str):
    for row in data:
        try:
            values = [int(row[k]) for k in keys]
            if any(v < 0 for v in values) or sum(values) != int(row["total_tokens"]):
                raise ValueError
        except (KeyError, ValueError):
            issue(out, "usage_mismatch", "A scored row has non-recomputable token total", location)
            return


def check_records(out: dict, round_id: str, scored: list[dict], identifier: str, path: Path):
    rec = records(path)
    ids = [r.get("cell_id") for r in rec]
    csv_ids = [r.get(identifier) for r in scored]
    if len(set(ids)) != len(ids) or len(set(csv_ids)) != len(csv_ids):
        issue(out, "duplicate_id", "Duplicate scored or Standard record ID", str(path.relative_to(ROOT)))
    absent = set(csv_ids) - set(ids)
    extra = set(ids) - set(csv_ids)
    out["standard_records"] = len(rec)
    out["scored_rows"] = len(scored)
    if absent or extra:
        issue(out, "record_coverage", f"{len(absent)} scored rows lack Standard records; {len(extra)} records lack scored rows", str(path.relative_to(ROOT)))
    csv_by_id = {r[identifier]: r for r in scored}
    for r in rec:
        cell = csv_by_id.get(r.get("cell_id"))
        if cell and r.get("outcome") != cell.get("outcome", cell.get("repair_outcome")):
            issue(out, "record_outcome", "Standard outcome differs from scored row", str(path.relative_to(ROOT)))
            break
    fields = {
        "cell_times": ("timestamps", "cell", "start_utc"),
        "grader": ("grade", "grader"),
        "model_effective": ("model", "effective"),
        "effort_effective": ("effort", "effective"),
        "host_class": ("environment", "cpu_model"),
        "sandbox": ("sandbox", "profile"),
        "price_table": ("cost", "price_table_version"),
        "cost_usd": ("cost", "usd"),
    }
    out["missing_fields"] = {name: sum(missing(at(r, *path)) for r in rec) for name, path in fields.items()}
    for name, count in out["missing_fields"].items():
        if count:
            issue(out, "missing_field", f"{name}: {count}/{len(rec)} Standard records missing or withheld", str(path.relative_to(ROOT)))


def compare_conditions(out: dict, data: list[dict], arm_key: str, location: str, fields: tuple[str, ...]):
    arms = {r[arm_key] for r in data}
    for field in fields:
        by_arm = {arm: {r.get(field, "") for r in data if r[arm_key] == arm} for arm in arms}
        if any(not vals or "" in vals for vals in by_arm.values()):
            issue(out, "comparison_missing", f"Comparison field {field} is missing in an arm", location)
        elif len({tuple(sorted(vals)) for vals in by_arm.values()}) > 1:
            issue(out, "comparison_diff", f"Comparison field {field} differs across arms", location)


def git_chronology(out: dict, round_id: str, first_result: str | None):
    rel = f"rounds/{round_id}/DECISION-RULE.md"
    result = subprocess.run(["git", "log", "--diff-filter=A", "--format=%aI", "--", rel], cwd=ROOT, capture_output=True, text=True, check=True)
    dates = [line for line in result.stdout.splitlines() if line]
    out["rule_first_public_commit"] = dates[-1] if dates else None
    out["first_result"] = first_result
    if not dates or not first_result:
        issue(out, "chronology_unproven", "Public git cannot establish rule before first result", rel)
        return
    rule_time = dt.datetime.fromisoformat(dates[-1].replace("Z", "+00:00"))
    result_time = dt.datetime.fromisoformat(first_result.replace("Z", "+00:00"))
    if rule_time >= result_time:
        issue(out, "chronology_unproven", "First public rule commit postdates first recorded result; private pre-registration needs immutable receipt", rel)


def operator_receipt(out: dict, round_id: str, root: Path):
    source = {
        "l3-repair": root / "lanes-2026-10-07/l3/DESIGN.md",
        "l3b-repair-vs-continue": root / "lanes-2026-10-07/l3b/DESIGN.md",
        "lang-sol-replication": root / "lang-sol-replication/DESIGN.md",
    }[round_id]
    if not source.is_file():
        issue(out, "receipt_missing", "Operator design receipt unavailable", "operator design receipt")
        return
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    modified = dt.datetime.fromtimestamp(source.stat().st_mtime, dt.timezone.utc)
    out["operator_design"] = {"sha256": digest, "filesystem_mtime_utc": modified.isoformat()}
    public_path = ROOT / "rounds" / round_id / ("DESIGN.md" if round_id == "lang-sol-replication" else "README.md")
    public = public_path.read_text()
    declared = re.search(r"(?:Design SHA-256:\s*|original design source bytes is `)([a-f0-9]{64})", public)
    if declared and declared.group(1) != digest:
        issue(out, "receipt_hash_mismatch", "Operator design bytes differ from published source SHA-256", str(public_path.relative_to(ROOT)))
    elif not declared:
        issue(out, "receipt_hash_missing", "No published hash binds this operator design", str(public_path.relative_to(ROOT)))
    first = out.get("first_result")
    if first and modified >= dt.datetime.fromisoformat(first.replace("Z", "+00:00")):
        issue(out, "receipt_post_result", "Operator design file modification time follows first result; filesystem time is not immutable proof", "operator design receipt")
    else:
        issue(out, "receipt_not_immutable", "Operator design filesystem time is not independent immutable pre-registration proof", "operator design receipt")


def private_l3b_rule_check(out: dict, root: Path):
    evidence = json.loads((ROOT / "rounds/l3b-repair-vs-continue/data/rule-evidence.json").read_text())
    script = root / "lanes-2026-10-07/l3b/l3b_rule_check.py"
    if not script.is_file() or hashlib.sha256(script.read_bytes()).hexdigest() != evidence["private_check_sha256"]:
        issue(out, "private_check_unavailable", "Private per-test checker unavailable or hash differs", "rounds/l3b-repair-vs-continue/data/rule-evidence.json:4")
        return
    grade_file = root / "lanes-2026-10-07/l3b/grades.jsonl"
    if not grade_file.is_file():
        issue(out, "private_check_unavailable", "Private grade receipt unavailable", "operator private grade receipt")
        return
    grade_hash = hashlib.sha256(grade_file.read_bytes()).hexdigest()
    out["private_grade_sha256"] = grade_hash
    public_env = (ROOT / "rounds/l3b-repair-vs-continue/ENVIRONMENT.md").read_text()
    if grade_hash not in public_env:
        issue(out, "private_grade_hash_mismatch", "Private grade receipt does not match published environment hash", "rounds/l3b-repair-vs-continue/ENVIRONMENT.md:19")
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, check=False)
    line = next((x for x in result.stdout.splitlines() if x.startswith("rule: ")), "")
    match = re.search(r"REPAIR-CONTINUE =\s*(-?\d+).*per-test available:\s*(True|False).*any REPAIR regression:\s*(True|False)", line)
    if result.returncode or not match:
        issue(out, "private_check_failed", "Private per-test checker did not produce a parseable summary", "operator private rule checker")
        return
    difference, available, regression = match.groups()
    out["private_rule_check"] = {"rescue_difference": int(difference), "per_test_available": available == "True", "any_repair_regression": regression == "True"}
    if int(difference) != 2 or available != "True" or regression != "False":
        issue(out, "private_check_failed", "Private rule result differs from published boolean or rescue difference", "rounds/l3b-repair-vs-continue/data/rule-evidence.json")


def environment_check(out: dict, round_id: str, first_start: str | None = None, last_end: str | None = None):
    rel = f"rounds/{round_id}/ENVIRONMENT.md"
    path = ROOT / rel
    if not path.is_file():
        issue(out, "environment_missing", "No round ENVIRONMENT.md", rel)
        return
    text = path.read_text()
    captures = re.findall(r"captured_at_utc:\s*['\"]?([0-9T:\-]+Z)", text)
    out["environment_capture_times"] = captures
    if not captures:
        issue(out, "environment_capture_missing", "Environment has no dated host capture", rel)
    elif first_start:
        first = dt.datetime.fromisoformat(first_start.replace("Z", "+00:00"))
        earliest = min(dt.datetime.fromisoformat(x.replace("Z", "+00:00")) for x in captures)
        if earliest > first:
            issue(out, "environment_late", "All dated host captures follow first contestant start", rel)
        if last_end and earliest > dt.datetime.fromisoformat(last_end.replace("Z", "+00:00")):
            issue(out, "environment_post_run", "All dated host captures follow every contestant execution", rel)


def audit_l3(out: dict, findings: str):
    base = ROOT / "rounds/l3-repair"
    data = [r for r in rows(base / "data/cells.csv") if r["kind"] == "pair"]
    out["counts"] = {"repair": [sum(r["repair_outcome"] == "pass" for r in data), len(data)]}
    assert_claim(out, (base / "README.md").read_text(), r"Headline:.*?(\d+)/(\d+) repairs rescued", tuple(out["counts"]["repair"]), "rounds/l3-repair/README.md:19")
    assert_claim(out, findings, r"L3 descriptive round records (\d+)/(\d+) repairs rescued", tuple(out["counts"]["repair"]), "FINDINGS.md:11")
    assert_claim(out, (base / "RESULTS.md").read_text(), r"Rescues:.*?(\d+)/(\d+)", tuple(out["counts"]["repair"]), "rounds/l3-repair/RESULTS.md:36")
    if len(data) != 6:
        issue(out, "denominator", f"Rule requires six repairs; found {len(data)}", "rounds/l3-repair/DECISION-RULE.md:5")
    frozen = json.loads((base / "INPUTS.json").read_text())["arm_a_failure_pool"]
    if {r["original_cell_id"] for r in data} != {r["cell_id"] for r in frozen}:
        issue(out, "source_join", "Repair source IDs differ from frozen failure pool", "rounds/l3-repair/INPUTS.json")
    for field in ("grader_version", "harness_version", "model_effective", "effort_effective", "sandbox", "date_window"):
        issue(out, "comparison_missing", f"Original-versus-repair comparison lacks paired {field} in public rows", "rounds/l3-repair/data/cells.csv:1")
    check_usage(out, data, ("uncached_input_tokens", "cached_input_tokens", "output_tokens"), "rounds/l3-repair/data/cells.csv")
    published = (base / "RESULTS.md").read_text()
    total = sum(int(r["total_tokens"]) for r in data)
    aggregate = re.search(r"\*\*Total\*\*.*?\*\*([\d,]+)\*\*\s*\|\s*$", published, re.M)
    if not aggregate or int(aggregate.group(1).replace(",", "")) != total:
        issue(out, "count_mismatch", f"Reported total tokens differ from recomputed {total}", "rounds/l3-repair/RESULTS.md:21")
    for r in data:
        if not valid_outcome(r, "repair_outcome"):
            issue(out, "invalid_outcome", "Unrecognized repair outcome", "rounds/l3-repair/data/cells.csv")
            break
    check_records(out, "l3-repair", data, "repair_cell_id", base / "records.jsonl")
    if out["counts"]["repair"][0] < 3:
        issue(out, "rule_failed", "Three-rescue primary threshold was not met", "rounds/l3-repair/DECISION-RULE.md:23")
    issue(out, "rule_unverifiable", "Per-test preservation condition lacks public pass sets", "rounds/l3-repair/DECISION-RULE.md:23")
    git_chronology(out, "l3-repair", None)
    environment_check(out, "l3-repair")


def audit_l3b(out: dict):
    base = ROOT / "rounds/l3b-repair-vs-continue"
    data = rows(base / "data/scored-cells.csv")
    counts = {arm: [sum(r["outcome"] == "pass" for r in data if r["arm"] == arm), sum(r["arm"] == arm for r in data)] for arm in ("REPAIR", "CONTINUE", "RESTART")}
    out["counts"] = counts
    assert_claim(out, (base / "README.md").read_text(), r"Rescues:.*?REPAIR (\d+)/(\d+); CONTINUE (\d+)/(\d+); RESTART (\d+)/(\d+)", tuple(v for arm in counts for v in counts[arm]), "rounds/l3b-repair-vs-continue/README.md:60")
    assert_claim(out, (base / "RESULTS.md").read_text(), r"Rescues:.*?REPAIR (\d+)/(\d+); CONTINUE (\d+)/(\d+); RESTART (\d+)/(\d+)", tuple(v for arm in counts for v in counts[arm]), "rounds/l3b-repair-vs-continue/RESULTS.md:19")
    source = rows(base / "data/original-failures.csv")
    ids = {r["original_failure_cell_id"] for r in source}
    if len(ids) != 8 or len(data) != 24 or any({r["arm"] for r in data if r["original_failure_cell_id"] == ident} != set(counts) for ident in ids):
        issue(out, "denominator", "Expected eight failures paired across all three arms and 24 cells", "rounds/l3b-repair-vs-continue/data/scored-cells.csv")
    if {r["original_failure_cell_id"] for r in data} != ids:
        issue(out, "source_join", "Scored cells do not exactly join frozen original failures", "rounds/l3b-repair-vs-continue/data/original-failures.csv")
    if any(not valid_outcome(r) for r in data):
        issue(out, "invalid_outcome", "Unrecognized outcome", "rounds/l3b-repair-vs-continue/data/scored-cells.csv")
    check_usage(out, data, ("uncached_input_tokens", "cached_input_tokens", "output_tokens"), "rounds/l3b-repair-vs-continue/data/scored-cells.csv")
    measured = (base / "MEASURED.md").read_text()
    summed = sum(int(r["total_tokens"]) for r in data)
    aggregate = re.search(r"Overall scored attempts: \*\*([\d,]+) tokens", measured)
    if not aggregate or int(aggregate.group(1).replace(",", "")) != summed:
        issue(out, "count_mismatch", f"Reported scored tokens differ from recomputed {summed}", "rounds/l3b-repair-vs-continue/MEASURED.md:48")
    check_records(out, "l3b-repair-vs-continue", data, "cell_id", base / "records.jsonl")
    evidence = json.loads((base / "data/rule-evidence.json").read_text())
    if not evidence.get("per_test_no_regression") or evidence.get("repair_cells_checked") != 8:
        issue(out, "rule_failed", "Private no-regression summary is false or incomplete", "rounds/l3b-repair-vs-continue/data/rule-evidence.json")
    else:
        issue(out, "rule_unverifiable", "Per-test no-regression is a private boolean, without public pass sets", "rounds/l3b-repair-vs-continue/data/rule-evidence.json:2")
    if counts["REPAIR"][0] - counts["CONTINUE"][0] < 2:
        issue(out, "rule_failed", "Primary rescue difference below two", "rounds/l3b-repair-vs-continue/DECISION-RULE.md:3")
    starts = [r["started_at"] for r in data if r.get("started_at")]
    git_chronology(out, "l3b-repair-vs-continue", min(starts) if starts else None)
    environment_check(out, "l3b-repair-vs-continue", min(starts) if starts else None,
                      max(r["finished_at"] for r in data if r.get("finished_at")))
    for field in ("model", "effort", "grader", "harness", "runner", "sandbox", "host_class"):
        issue(out, "comparison_missing", f"Scored CSV omits {field} needed for arm comparability", "rounds/l3b-repair-vs-continue/data/scored-cells.csv:1")


def audit_lang(out: dict, findings: str):
    base = ROOT / "rounds/lang-sol-replication"
    data = rows(base / "data/cells.csv")
    stacks = ("rust", "go", "ts-bun")
    counts = {stack: {cohort: [sum(r["outcome"] == "pass" for r in data if r["stack"] == stack and r["cohort"] == cohort), sum(r["stack"] == stack and r["cohort"] == cohort for r in data)] for cohort in ("new", "reused")} for stack in stacks}
    out["counts"] = counts
    text = (base / "README.md").read_text()
    expected = tuple(v for stack in stacks for v in counts[stack]["new"])
    assert_claim(out, text, r"New passes were Rust (\d+)/(\d+), Go (\d+)/(\d+), and TS-Bun (\d+)/(\d+)", expected, "rounds/lang-sol-replication/README.md:30")
    combined = tuple(v for stack in stacks for v in [sum(counts[stack][c][i] for c in ("new", "reused")) for i in (0, 1)])
    assert_claim(out, text, r"Combined raw passes were Rust (\d+)/(\d+), Go (\d+)/(\d+), and TS-Bun (\d+)/(\d+)", combined, "rounds/lang-sol-replication/README.md:30")
    assert_claim(out, findings, r"raw totals are Rust (\d+)/(\d+), Go (\d+)/(\d+), and TS-Bun (\d+)/(\d+)", combined, "FINDINGS.md:95")
    equal = {}
    for stack in stacks:
        # Published task code can contain a stack suffix; the leading task number is the unit.
        task_keys = sorted({re.search(r"r70-(\d+)", r["task"]).group(1) for r in data if r["stack"] == stack})
        if len(task_keys) != 6:
            issue(out, "denominator", f"{stack} has {len(task_keys)} task strata, expected six", "rounds/lang-sol-replication/data/cells.csv")
        rates = []
        for key in task_keys:
            group = [r for r in data if r["stack"] == stack and re.search(r"r70-(\d+)", r["task"]).group(1) == key]
            rates.append(sum(r["outcome"] == "pass" for r in group) / len(group))
        equal[stack] = round(100 * sum(rates) / len(rates), 1) if rates else None
    out["equal_task_percent"] = equal
    assert_percent_claim(out, text, tuple(equal.values()), "rounds/lang-sol-replication/README.md:30")
    assert_percent_claim(out, findings, tuple(equal.values()), "FINDINGS.md:95")
    assert_claim(out, (base / "RESULTS.md").read_text(), r"Combined raw official pass counts are Rust (\d+)/(\d+), Go (\d+)/(\d+), and TS-Bun (\d+)/(\d+)", combined, "rounds/lang-sol-replication/RESULTS.md:94")
    if len(data) != 58 or sum(r["cohort"] == "new" for r in data) != 27:
        issue(out, "denominator", "Expected 27 new plus 31 reused exact IDs", "rounds/lang-sol-replication/data/cells.csv")
    if any(not valid_outcome(r) for r in data):
        issue(out, "invalid_outcome", "Unrecognized outcome", "rounds/lang-sol-replication/data/cells.csv")
    check_usage(out, data, ("uncached", "cached", "output"), "rounds/lang-sol-replication/data/cells.csv")
    check_records(out, "lang-sol-replication", [r for r in data if r["cohort"] == "new"], "cell_id", base / "records.jsonl")
    compare_conditions(out, [r for r in data if r["cohort"] == "new"], "stack", "rounds/lang-sol-replication/data/cells.csv:1", ("host", "cli_version"))
    for field in ("grader", "harness", "runner", "sandbox", "model_effective", "effort_effective"):
        issue(out, "comparison_missing", f"Comparison metadata {field} incomplete in Standard records", "rounds/lang-sol-replication/records.jsonl")
    grade_times = [r["grade_window_at"] for r in data if r["cohort"] == "new" and r.get("grade_window_at")]
    git_chronology(out, "lang-sol-replication", min(grade_times) if grade_times else None)
    environment_check(out, "lang-sol-replication")
    issue(out, "rule_underspecified", "Four-pass equalized-task branch has no registered formula or scale", "rounds/lang-sol-replication/DECISION-RULE.md:24")


def discover_rounds(findings: str) -> dict[str, Path | None]:
    """Union the actual folders and all public indices; keep absent IDs visible."""
    found = {p.name: p for p in (ROOT / "rounds").iterdir() if p.is_dir()}
    indexed = set(json.loads((ROOT / "rounds/index.json").read_text()))
    indexed.update(re.findall(r"rounds/([^/)]+)/(?:README|RESULTS|MEASURED)\.md", findings))
    indexed.update(x["round_id"] for x in json.loads((ROOT / "reproduce/round-inventory.json").read_text())["rounds"])
    records_index = json.loads((ROOT / "results/run-records/index.json").read_text())
    indexed.update(x["round_id"] for x in records_index["files"])
    return {name: found.get(name) for name in sorted(indexed | found.keys())}


def evidence_location(path: Path, line: int = 1) -> str:
    try:
        return f"{path.relative_to(ROOT)}:{line}"
    except ValueError:
        return f"{path}:{line}"


def cited_line(path: Path, pattern: str) -> str:
    if path.is_file():
        for number, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            if re.search(pattern, line, re.I):
                return evidence_location(path, number)
    return evidence_location(path)


def read_inventory_classes() -> dict[str, str]:
    inventory_path = ROOT / "reproduce/round-inventory.json"
    if not inventory_path.is_file():
        return {}
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    return {
        row["round_id"]: ("FULLY RERUNNABLE" if row.get("full_execution_replayable") else "ANALYSIS ONLY")
        for row in inventory.get("rounds", [])
        if isinstance(row, dict) and isinstance(row.get("round_id"), str)
    }


def generic_round(out: dict, name: str, base: Path | None, inventory: dict[str, str]):
    out["audit_depth"] = "mechanical"
    out["reproducibility_class"] = inventory.get(name, "UNCLASSIFIED / local untracked")
    if base is None:
        issue(out, "round_directory_missing", "Indexed round has no available directory", f"rounds/{name}:1")
        out["status"] = "INCOMPLETE"
        return
    readme = base / "README.md"
    if not readme.is_file():
        issue(out, "round_readme_missing", "Round has no README", evidence_location(readme))
        page = ""
    else:
        page = readme.read_text(errors="replace")
    public_status = re.search(r"^STATUS:\s*\*\*([^*]+)\*\*", page, re.M | re.I)
    out["published_status"] = public_status.group(1).upper() if public_status else None
    row_files = sorted((base / "data").glob("*.csv")) if (base / "data").is_dir() else []
    row_files += sorted(base.glob("*.csv"))
    row_files += sorted((base / "raw").glob("*.jsonl")) if (base / "raw").is_dir() else []
    out["row_files"] = {}
    all_times = []
    for path in row_files:
        try:
            if path.suffix == ".csv":
                data = rows(path)
            else:
                data = records(path)
        except (ValueError, UnicodeError, OSError) as exc:
            issue(out, "row_file_unreadable", f"Cannot parse row file: {exc}", evidence_location(path))
            continue
        info = {"rows": len(data)}
        if data and isinstance(data[0], dict):
            for key in ("outcome", "official_grade_outcome", "repair_outcome", "verdict", "status"):
                if key in data[0]:
                    info[key] = dict(collections.Counter(str(r.get(key, "")).lower() for r in data))
            token_sets = (("uncached_input_tokens", "cached_input_tokens", "output_tokens"),
                          ("uncached", "cached", "output"),
                          ("input_uncached_tokens", "input_cached_tokens", "output_tokens"))
            for keys in token_sets:
                if set((*keys, "total_tokens")) <= data[0].keys():
                    errors = []
                    missing_usage = []
                    for number, row in enumerate(data, 2):
                        if all(row.get(k) in (None, "") for k in (*keys, "total_tokens")):
                            missing_usage.append(number)
                            continue
                        try:
                            if sum(int(row[k]) for k in keys) != int(row["total_tokens"]):
                                errors.append(number)
                        except (TypeError, ValueError, KeyError):
                            errors.append(number)
                    info["token_sum_checked"] = len(data) - len(missing_usage)
                    if missing_usage:
                        info["token_usage_missing_lines"] = missing_usage[:30]
                        issue(out, "usage_missing", f"{len(missing_usage)} rows lack token usage; first rows {missing_usage[:10]}", evidence_location(path, missing_usage[0]))
                    if errors:
                        info["token_sum_error_lines"] = errors[:30]
                        issue(out, "usage_mismatch", f"{len(errors)} row token totals do not equal components; first rows {errors[:10]}", evidence_location(path, errors[0]))
                    break
            for key in ("grade_finished_at", "grade_window_at", "started_at", "finished_at", "timestamp_utc"):
                if key in data[0]:
                    all_times.extend(str(r[key]) for r in data if r.get(key))
        out["row_files"][evidence_location(path).rsplit(":", 1)[0]] = info
    # Standard records and the historical captured-delivery export are not
    # interchangeable with official grades; report their coverage separately.
    standard = base / "records.jsonl"
    export = ROOT / "results/run-records" / f"{name}.jsonl"
    for label, path in (("standard_records", standard), ("captured_deliveries", export)):
        if path.is_file():
            try:
                data = records(path)
                out[label] = len(data)
                if label == "standard_records":
                    for key, parts in {"model_effective": ("model", "effective"), "effort_effective": ("effort", "effective"),
                                       "grader": ("grade", "grader"), "host_class": ("environment", "cpu_model"),
                                       "sandbox": ("sandbox", "profile")}.items():
                        count = sum(missing(at(r, *parts)) for r in data)
                        if count:
                            issue(out, "missing_field", f"{key}: {count}/{len(data)} Standard records missing or withheld", evidence_location(path))
                for r in data:
                    for parts in (("grade", "timestamp"), ("timestamps", "cell", "start_utc")):
                        value = at(r, *parts)
                        if isinstance(value, str) and re.match(r"\d{4}-\d\d-\d\dT", value):
                            all_times.append(value)
            except (ValueError, OSError):
                issue(out, "row_file_unreadable", "Records cannot be parsed", evidence_location(path))
    out["first_result_or_capture"] = min(all_times) if all_times else None
    rule = base / "DECISION-RULE.md"
    if not rule.is_file():
        issue(out, "rule_missing", "No exact pre-registered decision rule is retained", cited_line(readme, r"Pre-registered:|Decision rule:"))
    else:
        rel = f"rounds/{name}/DECISION-RULE.md"
        if base.is_relative_to(ROOT):
            dates = subprocess.run(["git", "log", "--diff-filter=A", "--format=%aI", "--", rel], cwd=ROOT,
                                   capture_output=True, text=True).stdout.splitlines()
        else:
            dates = []
        out["rule_first_public_commit"] = dates[-1] if dates else None
        if not dates or not all_times:
            issue(out, "chronology_unproven", "No independently dated pre-result rule and result pair can be proved", evidence_location(rule))
        else:
            try:
                if dt.datetime.fromisoformat(dates[-1]) >= dt.datetime.fromisoformat(min(all_times).replace("Z", "+00:00")):
                    issue(out, "chronology_unproven", "Public rule commit follows first available result/capture", evidence_location(rule))
            except ValueError:
                issue(out, "chronology_unproven", "Chronology timestamp cannot be parsed", evidence_location(rule))
    if re.search(r"^Pre-registered:\s*(?:\*\*)?no\b", page, re.M | re.I):
        issue(out, "rule_not_preregistered", "Page explicitly says pre-registration did not occur", cited_line(readme, r"Pre-registered:"))
    if "Amendment" in (rule.read_text(errors="replace") if rule.is_file() else "") and re.search(r"after .*outcome|after .*result", rule.read_text(errors="replace"), re.I):
        issue(out, "post_result_amendment", "Decision-rule amendment reports known outcomes; registered decision cannot be promoted", cited_line(rule, r"after .*outcome|after .*result"))
    if (base / "MISSING.md").is_file():
        text = (base / "MISSING.md").read_text(errors="replace")
        if re.search(r"missing|unavailable|not recorded|withheld", text, re.I):
            issue(out, "declared_evidence_gap", "Round declares missing inputs or receipts; inspect MISSING.md for exact scope", cited_line(base / "MISSING.md", r"missing|unavailable|not recorded|withheld"))
    if not (base / "ENVIRONMENT.md").is_file():
        issue(out, "environment_missing", "No round environment capture", cited_line(readme, r"Venue:|host|environment"))
    if not row_files:
        issue(out, "headline_unverifiable", "No public per-cell or per-attempt analysis rows in this round directory", cited_line(readme, r"Data completeness:|Result:|Headline:"))
    else:
        issue(out, "headline_not_recomputed", "Generic row inspection checked coverage and token sums; headline formulas need a round-specific reproducer or hand check", cited_line(readme, r"Headline:|Result:|Verdict:"))
    if re.search(r"(?:different hosts?|not interleaved|confounded|different date|different venue|authentication.*depart)", page, re.I):
        issue(out, "condition_mismatch", "Page reports an unmatched comparison condition", cited_line(readme, r"different hosts?|not interleaved|confounded|different date|different venue|authentication.*depart"))
    if not row_files and not standard.is_file() and not export.is_file():
        issue(out, "cell_evidence_missing", "No round-level rows or captured deliveries; exact missing cell IDs cannot be enumerated", cited_line(readme, r"Data completeness:|Raw records:"))
    if out["reproducibility_class"] != "FULLY RERUNNABLE":
        issue(out, "execution_not_rerunnable", f"Inventory class: {out['reproducibility_class']}; exact execution kit has not passed clean-machine proof", "reproduce/round-inventory.json")
    return


def assign_status(out: dict, page: str):
    codes = {x["code"] for x in out["issues"]}
    published = out.get("published_status", "") or ""
    if published == "INVALID" or codes & {"count_mismatch", "rate_mismatch", "usage_mismatch", "record_outcome", "duplicate_id", "denominator", "source_join"}:
        status = "INVALID"
    elif published in {"NOT-RUN", "NOT RUN", "WITHDRAWN", "INCOMPLETE / NOT VALID"} or ("cell_evidence_missing" in codes and re.search(r"not run|withdrawn|no .*cells.*run", page, re.I)):
        status = "INCOMPLETE"
    elif re.search(r"^Label:\s*(?:\*\*)?DESCRIPTIVE", page, re.M | re.I):
        status = "DESCRIPTIVE"
    elif re.search(r"\bpilot\b", page[:2500], re.I):
        status = "PILOT"
    elif not codes:
        status = "VALID"
    else:
        status = "DESCRIPTIVE"
    out["status"] = status
    out["reason_codes"] = sorted(codes) if status != "VALID" else []


def analysis_replayers() -> dict[str, str]:
    return {x["round_id"]: x["script"] for x in json.loads((ROOT / "reproduce/round-inventory.json").read_text())["rounds"]
            if x["replay_type"] == "analysis-only" and x.get("script")}


def run_analysis_replayer(out: dict, command: str, cache: dict[str, dict]):
    if command not in cache:
        argv = shlex.split(command)
        if len(argv) < 2 or argv[0] != "python3" or not (ROOT / argv[1]).is_file():
            cache[command] = {"passed": False, "detail": "unavailable or unsupported analysis script"}
        else:
            try:
                result = subprocess.run([sys.executable, *argv[1:]], cwd=ROOT, capture_output=True, text=True, timeout=120)
                cache[command] = {"passed": result.returncode == 0, "exit_code": result.returncode,
                                  "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
                                  "detail": (result.stderr or result.stdout)[-500:] if result.returncode else ""}
            except subprocess.TimeoutExpired:
                cache[command] = {"passed": False, "detail": "analysis script timed out after 120 seconds"}
    out["analysis_replayer"] = {"command": command, **cache[command]}
    if cache[command]["passed"]:
        out["issues"] = [x for x in out["issues"] if x["code"] != "headline_not_recomputed"]
    else:
        issue(out, "analysis_replayer_failed", cache[command]["detail"], command)


def scrutinize(root: Path = ROOT, operator_root: Path | None = None) -> dict:
    global ROOT
    ROOT = root
    config = json.loads((ROOT / "reproduce/release-rounds.json").read_text())
    listed = list(config.get("scrutiny_rounds", []))
    findings = (ROOT / "FINDINGS.md").read_text()
    output = {"source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "rounds": {}}
    inventory = read_inventory_classes()
    discovered = discover_rounds(findings)
    replayers = analysis_replayers()
    replay_cache = {}
    output["coverage"] = {"round_directories": sum(p is not None for p in discovered.values()),
                          "indexed_ids": len(discovered), "release_ids": listed}
    for name, base in discovered.items():
        result = {"issues": []}
        output["rounds"][name] = result
        generic_round(result, name, base, inventory)
        if name in replayers:
            run_analysis_replayer(result, replayers[name], replay_cache)
        if name == "l3-repair":
            audit_l3(result, findings)
        elif name == "l3b-repair-vs-continue":
            audit_l3b(result)
        elif name == "lang-sol-replication":
            audit_lang(result, findings)
        if name in ROUNDS and operator_root is not None:
            operator_receipt(result, name, operator_root)
            if name == "l3b-repair-vs-continue":
                private_l3b_rule_check(result, operator_root)
        if name in ROUNDS:
            result["audit_depth"] = "hand + mechanical"
            result["issues"] = [x for x in result["issues"] if x["code"] != "headline_not_recomputed"]
        page = (base / "README.md").read_text(errors="replace") if base and (base / "README.md").is_file() else ""
        assign_status(result, page)
    return output


def evidence_digest(round_id: str) -> str:
    """Bind a sign-off to all public round evidence and the checker itself."""
    paths = [ROOT / "FINDINGS.md", ROOT / "reproduce/release-rounds.json",
             ROOT / "reproduce/scrutinize.py", ROOT / "tasks/CONTAMINATION-LOG.md"]
    paths.extend(p for p in (ROOT / "rounds" / round_id).rglob("*") if p.is_file())
    h = hashlib.sha256()
    for path in sorted(paths):
        h.update(str(path.relative_to(ROOT)).encode())
        h.update(b"\0")
        h.update(hashlib.sha256(path.read_bytes()).digest())
    return h.hexdigest()


def is_independent_reviewer(reviewer) -> bool:
    """Accept only an independent model identity, never a round-author sign-off."""
    return (
        isinstance(reviewer, dict)
        and reviewer.get("kind") == "independent_model"
        and re.match(r"^gpt-6-astra$", str(reviewer.get("model", ""))) is not None
        and reviewer.get("effort") in {"high", "xhigh", "max", "ultra"}
        and reviewer.get("round_author") is not True
    )


def validate_signoffs(report: dict) -> list[str]:
    """Require independent model review receipts for the indexed release rounds."""
    errors = []
    for round_id in report["coverage"]["release_ids"]:
        audit = report["rounds"][round_id]
        path = ROOT / "reproduce/scrutiny-signoffs" / f"{round_id}.json"
        if not path.is_file():
            errors.append(f"{round_id}: missing scrutiny sign-off")
            continue
        try:
            signoff = json.loads(path.read_text())
        except (ValueError, OSError):
            errors.append(f"{round_id}: unreadable scrutiny sign-off")
            continue
        codes = {finding["code"] for finding in audit["issues"]}
        hard = {"count_mismatch", "rate_mismatch", "usage_mismatch", "record_outcome", "duplicate_id", "denominator", "source_join"}
        if codes & hard:
            errors.append(f"{round_id}: numerical or denominator discrepancy requires correction")
        if signoff.get("round_id") != round_id or signoff.get("source_commit") != report["source_commit"]:
            errors.append(f"{round_id}: sign-off round or source commit mismatch")
        if signoff.get("evidence_sha256") != evidence_digest(round_id):
            errors.append(f"{round_id}: evidence changed since sign-off")
        if signoff.get("operator_design_sha256") != audit.get("operator_design", {}).get("sha256") or not signoff.get("operator_design_sha256"):
            errors.append(f"{round_id}: operator design receipt changed or unavailable")
        if round_id == "l3b-repair-vs-continue" and (not audit.get("private_grade_sha256") or signoff.get("private_grade_sha256") != audit.get("private_grade_sha256")):
            errors.append(f"{round_id}: private grade receipt changed or unavailable")
        if signoff.get("verdict") not in {"PASS", "DESCRIPTIVE"}:
            errors.append(f"{round_id}: sign-off verdict must be PASS or DESCRIPTIVE")
        if signoff.get("verdict") == "PASS" and codes:
            errors.append(f"{round_id}: PASS has open scrutiny issues")
        if signoff.get("verdict") == "DESCRIPTIVE" and set(signoff.get("accepted_issue_codes", [])) != codes:
            errors.append(f"{round_id}: descriptive sign-off must account for every issue code")
        reviewer = signoff.get("reviewer")
        if not is_independent_reviewer(reviewer):
            errors.append(f"{round_id}: independent model reviewer, separate from the round author, is required")
        if not isinstance(signoff.get("signed_at_utc"), str):
            errors.append(f"{round_id}: review date required")
        receipt_name = signoff.get("review_receipt_path")
        receipt_path = ROOT / receipt_name if isinstance(receipt_name, str) else None
        if not receipt_path or not receipt_path.is_file() or not receipt_path.resolve().is_relative_to((ROOT / "reproduce/scrutiny-reviews").resolve()):
            errors.append(f"{round_id}: independent model review receipt missing")
        else:
            receipt_bytes = receipt_path.read_bytes()
            if hashlib.sha256(receipt_bytes).hexdigest() != signoff.get("review_receipt_sha256"):
                errors.append(f"{round_id}: model review receipt hash mismatch")
            try:
                receipt = json.loads(receipt_bytes)
            except ValueError:
                receipt = {}
            if receipt.get("round_id") != round_id or receipt.get("reviewed_commit") != report["source_commit"] or receipt.get("evidence_sha256") != evidence_digest(round_id) or receipt.get("reviewer") != reviewer or not receipt.get("review_text"):
                errors.append(f"{round_id}: model review did not bind commit, evidence, reviewer and findings")
        if signoff.get("verdict") == "DESCRIPTIVE" and not signoff.get("claim_disposition"):
            errors.append(f"{round_id}: descriptive sign-off needs claim disposition")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="machine-readable aggregate report")
    parser.add_argument("--operator-root", type=Path, default=None, help="optional private receipt root; defaults to no private inputs")
    args = parser.parse_args()
    report = scrutinize(operator_root=args.operator_root)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for name, row in report["rounds"].items():
            print(f"{name}: counts={row['counts']} issues={len(row['issues'])}")
            for finding in row["issues"]:
                print(f"  {finding['code']}: {finding['detail']} ({finding['location']})")
    raise SystemExit(1 if any(r["issues"] for r in report["rounds"].values()) else 0)


if __name__ == "__main__":
    main()
