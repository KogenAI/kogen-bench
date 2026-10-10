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
sys.path.insert(0, str(ROOT / "reproduce"))
from missing_reasons import load_legend

STRICT_FROM = date(2026, 10, 9)
MISSING_CODES = load_legend(ROOT / "results/missing-reasons.json")
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
DECLARED_MISSING_STATUSES = {"DESCRIPTIVE", "INVALID", "INCOMPLETE", "PILOT"}


def declared_missing_errors(round_id: str, status: str, report: dict, root: Path = ROOT) -> tuple[list[str], int]:
    """Check status-based Standard-field exceptions and their public explanation."""
    errors: list[str] = []
    missing = report["missing"]
    declaration_path = root / "rounds" / round_id / "MISSING-DECLARED.json"
    page_path = root / "rounds" / round_id / "README.md"
    if not missing:
        if declaration_path.exists():
            errors.append(f"{round_id} has a stale MISSING-DECLARED.json with no missing fields")
        return errors, 0
    if status == "VALID":
        errors.append(f"{round_id} is VALID but has {missing} missing Standard capture fields")
        return errors, 0
    if status not in DECLARED_MISSING_STATUSES:
        errors.append(f"{round_id} has missing Standard fields under unsupported status {status}")
        return errors, 0
    if not declaration_path.is_file():
        errors.append(f"{round_id} has missing Standard fields but no MISSING-DECLARED.json")
        return errors, 0
    try:
        declaration = json.loads(declaration_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        errors.append(f"{round_id} has invalid MISSING-DECLARED.json")
        return errors, 0
    fields = declaration.get("fields") if isinstance(declaration, dict) else None
    if not isinstance(fields, dict):
        errors.append(f"{round_id} MISSING-DECLARED.json needs a fields object")
        return errors, 0

    actual_fields = report["missing_fields"]
    for field, count in actual_fields.items():
        item = fields.get(field)
        if not isinstance(item, dict):
            errors.append(f"{round_id} has undeclared missing field {field}")
            continue
        code, note = item.get("reason_code"), item.get("note")
        if not isinstance(code, str) or code not in MISSING_CODES:
            errors.append(f"{round_id} has unknown reason code for missing field {field}")
        if not isinstance(note, str) or not note.strip():
            errors.append(f"{round_id} has no plain-language note for missing field {field}")
    for field in fields.keys() - actual_fields.keys():
        errors.append(f"{round_id} declares non-missing field {field}")
    if not page_path.is_file():
        errors.append(f"{round_id} has no README for its missing-field declaration")
    else:
        page = page_path.read_text(encoding="utf-8")
        expected = render_missing_section(fields, actual_fields)
        match = re.search(r"^## What's missing and why\n(.*?)(?=^## |\Z)", page, re.MULTILINE | re.DOTALL)
        if not match or match.group(1).strip() != expected.strip():
            errors.append(f"{round_id} README What's missing and why section differs from MISSING-DECLARED.json")
    return errors, missing


def render_missing_section(fields: dict, counts: dict[str, int]) -> str:
    lines = []
    for field in sorted(counts):
        item = fields.get(field, {})
        code = item.get("reason_code", "unknown") if isinstance(item, dict) else "unknown"
        note = item.get("note", "") if isinstance(item, dict) else ""
        reason = MISSING_CODES.get(code, {}).get("reason", "unknown reason code")
        lines.append(f"- `{field}` ({counts[field]} missing): {note} Reason: {reason} (`{code}`).")
    return "\n".join(lines)


def status_rows(root: Path = ROOT, errors: list[str] | None = None) -> dict[str, tuple[str, str]]:
    rows = {}
    for line in (root / "rounds/STATUS.md").read_text(encoding="utf-8").splitlines():
        match = STATUS_RE.match(line)
        if match:
            round_id, status, reason = (part.strip() for part in match.groups())
            if round_id not in rows:
                rows[round_id] = (status, reason)
            elif rows[round_id][0] != status:
                if errors is not None:
                    errors.append(f"{round_id} has conflicting rounds/STATUS.md rows")
                previous = rows[round_id][0]
                rows[round_id] = ("VALID" if "VALID" in {previous, status} else "AMBIGUOUS", reason)
    return rows


def read_field(round_id: str, field: str, root: Path = ROOT) -> str | None:
    page = root / "rounds" / round_id / "README.md"
    if not page.is_file():
        return None
    match = re.search(rf"^{re.escape(field)}:\s*(.*?)\s*$", page.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1) if match else None


def read_fields(round_id: str, field: str, root: Path = ROOT) -> list[str]:
    page = root / "rounds" / round_id / "README.md"
    if not page.is_file():
        return []
    return re.findall(rf"^{re.escape(field)}:\s*(.*?)\s*$", page.read_text(encoding="utf-8"), re.MULTILINE)


def read_round_label(round_id: str, root: Path = ROOT) -> str | None:
    """Return the round's analytical label for repository cross-checks."""
    return read_field(round_id, "Label", root)


def round_date(round_id: str, root: Path = ROOT) -> date | None:
    value = read_field(round_id, "Round date", root)
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


def readme_status(round_id: str, root: Path = ROOT) -> tuple[list[str], str | None]:
    page = root / "rounds" / round_id / "README.md"
    if not page.is_file():
        return [f"{round_id} has no README status"], None
    content = page.read_text(encoding="utf-8")
    matches = re.findall(r"^STATUS:\s*\*\*(VALID|DESCRIPTIVE|INCOMPLETE|INVALID|PILOT)\*\*", content, re.MULTILINE)
    matches.extend(re.findall(r"^\*\*(VALID|DESCRIPTIVE|INCOMPLETE|INVALID|PILOT)\*\*\s*$", content, re.MULTILINE))
    statuses = set(matches)
    if not statuses:
        return [f"{round_id} README has no recognized status line"], None
    if len(statuses) != 1:
        strict_claim = "VALID" if "VALID" in statuses else None
        return [f"{round_id} README has conflicting status lines: {', '.join(sorted(statuses))}"], strict_claim or sorted(statuses)[0]
    return [], next(iter(statuses))


def publication_badge_status(round_id: str, root: Path = ROOT) -> tuple[list[str], str | None]:
    badges = read_fields(round_id, "Publication badge", root)
    if not badges:
        return [f"{round_id} has no Publication badge"], None
    errors = []
    if len(set(badges)) != 1:
        errors.append(f"{round_id} has conflicting Publication badge lines")
    statuses = []
    for badge in badges:
        tokens = badge.split("; ")
        matches = [status for status, expected in BADGE_BY_STATUS.items() if expected in tokens]
        if len(matches) != 1:
            errors.append(f"{round_id} publication badge must identify exactly one status")
        statuses.extend(matches)
    unique_statuses = set(statuses)
    if len(unique_statuses) != 1:
        errors.append(f"{round_id} Publication badge lines identify different statuses")
    if "VALID" in unique_statuses:
        return errors, "VALID"
    return errors, next(iter(unique_statuses)) if unique_statuses else None


def resolve_status(round_id: str, inventory_status: str, root: Path = ROOT) -> tuple[list[str], str]:
    """Require agreement across the inventory, README status line, and badge."""
    errors: list[str] = []
    readme_errors, readme_value = readme_status(round_id, root)
    badge_errors, badge_value = publication_badge_status(round_id, root)
    errors.extend(readme_errors)
    errors.extend(badge_errors)
    evidence = [inventory_status]
    if readme_value:
        evidence.append(readme_value)
    if badge_value:
        evidence.append(badge_value)
    if len(set(evidence)) != 1:
        errors.append(
            f"{round_id} status sources disagree: STATUS.md={inventory_status}, "
            f"README={readme_value or 'missing'}, badge={badge_value or 'missing'}"
        )
    # Any claim of VALID uses the strict route even while disagreement blocks release.
    effective = "VALID" if "VALID" in evidence else (readme_value or badge_value or inventory_status)
    return errors, effective


def validate_historical_inventory(root: Path = ROOT) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    historical: list[str] = []
    statuses = status_rows(root, errors)
    round_dirs = {path.name for path in (root / "rounds").iterdir() if path.is_dir() and (path / "README.md").is_file()}
    for missing in sorted(round_dirs - statuses.keys()):
        errors.append(f"{missing} has a round page but no rounds/STATUS.md classification")
    for missing in sorted(statuses.keys() - round_dirs):
        errors.append(f"{missing} is listed in rounds/STATUS.md but has no round page")

    for round_id in sorted(round_dirs & statuses.keys()):
        status, reasons = statuses[round_id]
        status_errors, _effective_status = resolve_status(round_id, status, root)
        errors.extend(status_errors)
        badge = read_field(round_id, "Publication badge", root)
        recomputation = read_field(round_id, "Recomputation status", root)
        declared_date = round_date(round_id, root)
        if badge and "KEPT FOR AUDIT" not in badge.split("; "):
            errors.append(f"{round_id} publication badge must include KEPT FOR AUDIT")
        if round_id == "l3b-repair-vs-continue" and (not badge or "NARROW / HISTORICAL" not in badge.split("; ")):
            errors.append("l3b-repair-vs-continue must retain its NARROW / HISTORICAL badge")
        if status != "VALID":
            why = read_field(round_id, "Why not VALID", root)
            if not why or not why.strip():
                errors.append(f"{round_id} is {status} but has no Why not VALID explanation")
            elif reasons != "NONE" and not any(reason in why for reason in reasons.split(", ")):
                errors.append(f"{round_id} Why not VALID does not identify its registered reason codes")
        if round_id == "l3b-repair-vs-continue":
            limits = read_field(round_id, "Publication limits", root)
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


def main(root: Path = ROOT, records_override=None, validate_override=None) -> None:
    config = json.loads((root / "reproduce/release-rounds.json").read_text(encoding="utf-8"))
    try:
        strict_from = date.fromisoformat(config["strict_from_date"])
    except (KeyError, TypeError, ValueError):
        raise SystemExit("RELEASE GATE: invalid strict_from_date in reproduce/release-rounds.json")
    if strict_from != STRICT_FROM:
        raise SystemExit("RELEASE GATE: strict_from_date must remain 2026-10-09")

    errors, historical = validate_historical_inventory(root)
    from validate_round import records, validate

    rows = records_override if records_override is not None else records()
    validate_round = validate_override or validate
    statuses = status_rows(root)
    status_ids = set(statuses)
    strict_rounds = []
    declared_missing_total = 0
    declared_missing_by_status: dict[str, int] = {}
    # Date is an explicit page field, so new rounds cannot evade the strict gate
    # by omitting their Standard records or by leaving themselves off a list.
    for round_id in sorted(status_ids):
        declared_date = round_date(round_id, root)
        if declared_date is not None and declared_date >= strict_from:
            strict_rounds.append(round_id)
    for round_id in strict_rounds:
        report = validate_round(round_id, rows, strict=True)
        if report["errors"]:
            errors.append(f"{round_id} strict record validation failed: " + "; ".join(report["errors"][:5]))
        status_errors, status = resolve_status(round_id, statuses[round_id][0], root)
        errors.extend(status_errors)
        declaration_errors, declared_count = declared_missing_errors(round_id, status, report, root)
        errors.extend(declaration_errors)
        if not report["missing"] and not report["strict_release_eligible"]:
            errors.append(
                f"{round_id} has {len(report['protocol_deviations'])} protocol deviations; "
                "complete Standard capture with no deviations is required"
            )
        if declared_count:
            declared_missing_total += declared_count
            declared_missing_by_status[status] = declared_missing_by_status.get(status, 0) + declared_count

    register = json.loads((root / "results/publication-blockers.json").read_text(encoding="utf-8"))
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
        subprocess.run([sys.executable, str(root / "reproduce/validate_repo.py")], cwd=root, check=True)
    except subprocess.CalledProcessError as exc:
        errors.append(f"Repository validator failed with exit code {exc.returncode}")

    if errors:
        print("RELEASE GATE: BLOCKED")
        for error in errors:
            print("- " + error)
        raise SystemExit(1)
    print(f"HISTORICAL ROUNDS: {len(historical)} labelled; recomputation status and limits declared")
    print(f"NEW ROUNDS: {len(strict_rounds)} (dated from {strict_from.isoformat()}); VALID requires complete Standard capture")
    print(f"DECLARED MISSING STANDARD FIELDS: {declared_missing_total} ({', '.join(f'{status}={count}' for status, count in sorted(declared_missing_by_status.items())) or 'none'})")
    print("RELEASE GATE: PASS — historical record labelled; new-round strict gate and publication evidence gates resolved")


if __name__ == "__main__":
    main()
