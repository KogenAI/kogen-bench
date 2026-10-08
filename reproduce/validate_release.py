#!/usr/bin/env python3
"""Validate historical publication labels and strict gates for new rounds."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRICT_FROM = date(2026, 10, 9)
STATUS_RE = re.compile(r"^\s*([^|]+?)\s*\|\s*(VALID|DESCRIPTIVE|INCOMPLETE|INVALID|PILOT)\s*\|\s*(.*)$")
BADGE_BY_STATUS = {
    "VALID": "VALID",
    "DESCRIPTIVE": "DESCRIPTIVE",
    "INCOMPLETE": "INCOMPLETE",
    "INVALID": "INVALID",
    "PILOT": "DESCRIPTIVE / INCOMPLETE (PILOT)",
}
RECOMPUTATION_STATES = {
    "FULLY RECOMPUTABLE",
    "OBSERVED SOURCE ONLY",
    "NOT RECOMPUTABLE",
}


def status_rows() -> dict[str, tuple[str, str]]:
    rows = {}
    for line in (ROOT / "rounds/STATUS.md").read_text(encoding="utf-8").splitlines():
        match = STATUS_RE.match(line)
        if match:
            round_id, status, reason = (part.strip() for part in match.groups())
            rows[round_id] = (status, reason)
    return rows


def read_field(round_id: str, field: str) -> str | None:
    page = ROOT / "rounds" / round_id / "README.md"
    if not page.is_file():
        return None
    match = re.search(rf"^{re.escape(field)}:\s*(.*?)\s*$", page.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1) if match else None


def read_round_label(round_id: str) -> str | None:
    """Return the round's analytical label for repository cross-checks."""
    return read_field(round_id, "Label")


def round_date(round_id: str) -> date | None:
    value = read_field(round_id, "Round date")
    if not value:
        return None
    match = re.match(r"^(\d{4}-\d{2}-\d{2})$", value)
    if match:
        try:
            return date.fromisoformat(match.group(1))
        except ValueError:
            return None
    if value == "HISTORICAL (before 2026-10-09)":
        return date(2026, 10, 8)
    return None


def validate_historical_inventory() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    historical: list[str] = []
    statuses = status_rows()
    round_dirs = {path.name for path in (ROOT / "rounds").iterdir() if path.is_dir() and (path / "README.md").is_file()}
    for missing in sorted(round_dirs - statuses.keys()):
        errors.append(f"{missing} has a round page but no rounds/STATUS.md classification")
    for missing in sorted(statuses.keys() - round_dirs):
        errors.append(f"{missing} is listed in rounds/STATUS.md but has no round page")

    for round_id in sorted(round_dirs & statuses.keys()):
        status, reasons = statuses[round_id]
        badge = read_field(round_id, "Publication badge")
        recomputation = read_field(round_id, "Recomputation status")
        declared_date = round_date(round_id)
        if not badge:
            errors.append(f"{round_id} has no Publication badge")
        else:
            expected = BADGE_BY_STATUS[status]
            if expected not in badge.split("; "):
                errors.append(f"{round_id} publication badge does not include {expected}")
            if "KEPT FOR AUDIT" not in badge.split("; "):
                errors.append(f"{round_id} publication badge must include KEPT FOR AUDIT")
            if round_id == "l3b-repair-vs-continue" and "NARROW / HISTORICAL" not in badge.split("; "):
                errors.append("l3b-repair-vs-continue must retain its NARROW / HISTORICAL badge")
        if status != "VALID":
            why = read_field(round_id, "Why not VALID")
            if not why or not why.strip():
                errors.append(f"{round_id} is {status} but has no Why not VALID explanation")
            elif reasons != "NONE" and not any(reason in why for reason in reasons.split(", ")):
                errors.append(f"{round_id} Why not VALID does not identify its registered reason codes")
        if round_id == "l3b-repair-vs-continue":
            limits = read_field(round_id, "Publication limits")
            if not limits or "193 missing Standard capture fields" not in limits:
                errors.append("l3b-repair-vs-continue must keep its 193 missing Standard capture fields visible as a publication limit")
        if recomputation not in RECOMPUTATION_STATES:
            errors.append(f"{round_id} has no recognized recomputation status")
        if declared_date is None:
            errors.append(f"{round_id} has no valid Round date")
        elif declared_date < STRICT_FROM:
            historical.append(round_id)
        else:
            # New rounds are checked against complete Standard records below.
            pass
    return errors, historical


def run_official_grade_reproducer(round_id: str, policy: dict) -> tuple[bool, str]:
    """Compatibility helper retained for repository checks and old receipts."""
    script_value = policy.get("reproducer")
    if not isinstance(script_value, str) or not script_value:
        return False, f"{round_id} has no registered official-grade reproducer"
    script = (ROOT / script_value).resolve()
    try:
        script.relative_to(ROOT)
    except ValueError:
        return False, f"{round_id} reproducer escapes the repository"
    if not script.is_file():
        return False, f"{round_id} reproducer is missing: {script_value}"
    result = subprocess.run([sys.executable, str(script)], cwd=ROOT, capture_output=True, text=True, check=False)
    output = (result.stdout + "\n" + result.stderr).strip()
    return result.returncode == 0, output


def main() -> None:
    config = json.loads((ROOT / "reproduce/release-rounds.json").read_text(encoding="utf-8"))
    try:
        strict_from = date.fromisoformat(config["strict_from_date"])
    except (KeyError, TypeError, ValueError):
        raise SystemExit("RELEASE GATE: invalid strict_from_date in reproduce/release-rounds.json")
    if strict_from != STRICT_FROM:
        raise SystemExit("RELEASE GATE: strict_from_date must remain 2026-10-09")

    errors, historical = validate_historical_inventory()
    from validate_round import records, validate

    rows = records()
    status_ids = set(status_rows())
    strict_rounds = []
    # Date is an explicit page field, so new rounds cannot evade the strict gate
    # by omitting their Standard records or by leaving themselves off a list.
    for round_id in sorted(status_ids):
        declared_date = round_date(round_id)
        if declared_date is not None and declared_date >= strict_from:
            strict_rounds.append(round_id)
    for round_id in strict_rounds:
        report = validate(round_id, rows, strict=True)
        if report["errors"]:
            errors.append(f"{round_id} strict record validation failed: " + "; ".join(report["errors"][:5]))
        elif not report["strict_release_eligible"]:
            errors.append(
                f"{round_id} has {report['missing']} missing Standard capture fields and "
                f"{len(report['protocol_deviations'])} protocol deviations"
            )

    register = json.loads((ROOT / "results/publication-blockers.json").read_text(encoding="utf-8"))
    blockers = register.get("blockers")
    if not isinstance(blockers, list) or not blockers:
        errors.append("Publication evidence register is missing its gate rows")
        blockers = []
    ids = [row.get("id") for row in blockers if isinstance(row, dict)]
    if len(ids) != len(blockers) or any(not isinstance(value, str) or not value for value in ids) or len(set(ids)) != len(ids):
        errors.append("Publication evidence gate IDs must be nonempty and unique")
    invalid = [row.get("id") for row in blockers if not isinstance(row, dict) or row.get("status") not in {"resolved", "open"}]
    if invalid:
        errors.append("Publication gates have unknown statuses: " + ", ".join(map(str, invalid)))
    open_gates = [row for row in blockers if isinstance(row, dict) and row.get("status") != "resolved"]
    expected_status = "blocked" if open_gates else "ready"
    if register.get("publication_status") != expected_status:
        errors.append(f"Publication status must be {expected_status} from the registered gate states")
    if open_gates:
        errors.append("Open publication evidence gates: " + ", ".join(str(row.get("id")) for row in open_gates))

    try:
        subprocess.run([sys.executable, str(ROOT / "reproduce/validate_repo.py")], cwd=ROOT, check=True)
    except subprocess.CalledProcessError as exc:
        errors.append(f"Repository validator failed with exit code {exc.returncode}")

    if errors:
        print("RELEASE GATE: BLOCKED")
        for error in errors:
            print("- " + error)
        raise SystemExit(1)
    print(f"HISTORICAL ROUNDS: {len(historical)} labelled; recomputation status and limits declared")
    print(f"NEW STRICT ROUNDS: {len(strict_rounds)} (dated from {strict_from.isoformat()}); complete Standard capture and no deviations required")
    print("RELEASE GATE: PASS — historical record labelled; new-round strict gate and publication evidence gates resolved")


if __name__ == "__main__":
    main()
