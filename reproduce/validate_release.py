#!/usr/bin/env python3
"""Fail closed when release gates or independent review receipts remain open."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_GRADE_PASS_MARKER = "official grade counts verified"


def release_included_with_label(
    round_id: str,
    report: dict,
    declared_label: str | None,
    official_grade_reproducer_passed: bool,
    policy: dict,
) -> bool:
    """Check the explicit exception for descriptive rounds with declared gaps."""
    if policy.get("analysis_status") != "DESCRIPTIVE":
        return False
    if not isinstance(declared_label, str) or declared_label != policy.get("label") or not declared_label.startswith("DESCRIPTIVE"):
        return False
    missing = report.get("missing")
    if report.get("errors") or not isinstance(missing, int) or isinstance(missing, bool) or missing <= 0:
        return False
    deviations = report.get("protocol_deviations")
    if not isinstance(deviations, list) or not deviations or any(not isinstance(item, str) or not item.strip() for item in deviations):
        return False
    return official_grade_reproducer_passed


def read_round_label(round_id: str) -> str | None:
    page = ROOT / "rounds" / round_id / "README.md"
    if not page.is_file():
        return None
    match = re.search(r"^Label:\s*(.*?)\s*$", page.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1) if match else None


def run_official_grade_reproducer(round_id: str, policy: dict) -> tuple[bool, str]:
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

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    output = (result.stdout + "\n" + result.stderr).strip()
    passed = result.returncode == 0 and OFFICIAL_GRADE_PASS_MARKER in result.stdout.lower()
    return passed, output


def main() -> None:
    # Scrutiny runs before the existing publication evidence checks. A newly
    # listed round needs an independent model review receipt bound to its exact
    # evidence bytes and reviewed commit; absent or stale receipts block release.
    from scrutinize import scrutinize, validate_signoffs

    try:
        scrutiny_errors = validate_signoffs(scrutinize())
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"SCRUTINY GATE: BLOCKED — {exc}") from exc
    if scrutiny_errors:
        print("SCRUTINY GATE: BLOCKED")
        for error in scrutiny_errors:
            print("- " + error)
        raise SystemExit(1)

    round_config = json.loads((ROOT / "reproduce/release-rounds.json").read_text(encoding="utf-8"))
    required_rounds = round_config.get("required_strict_rounds")
    if not isinstance(required_rounds, list) or not required_rounds or any(not isinstance(item, str) or not item for item in required_rounds) or len(set(required_rounds)) != len(required_rounds):
        raise SystemExit("RELEASE GATE: invalid required_strict_rounds in reproduce/release-rounds.json")
    labelled_policies = round_config.get("release_included_with_label", {})
    if (
        not isinstance(labelled_policies, dict)
        or any(round_id not in required_rounds for round_id in labelled_policies)
        or any(not isinstance(policy, dict) for policy in labelled_policies.values())
    ):
        raise SystemExit("RELEASE GATE: invalid release_included_with_label in reproduce/release-rounds.json")

    register = json.loads((ROOT / "results/publication-blockers.json").read_text(encoding="utf-8"))
    blockers = register.get("blockers")
    errors = []
    included_labels = []
    if not isinstance(blockers, list) or not blockers:
        errors.append("Publication evidence register is missing its gate rows")
        blockers = []
    ids = [row.get("id") for row in blockers]
    if any(not isinstance(value, str) or not value for value in ids) or len(set(ids)) != len(ids):
        errors.append("Publication evidence gate IDs must be nonempty and unique")
    invalid_statuses = [row.get("id") for row in blockers if row.get("status") not in {"resolved", "open"}]
    if invalid_statuses:
        errors.append("Publication gates have unknown statuses: " + ", ".join(map(str, invalid_statuses)))
    open_gates = [row for row in blockers if row.get("status") != "resolved"]
    expected_status = "blocked" if open_gates else "ready"
    if register.get("publication_status") != expected_status:
        errors.append(f"Publication status must be {expected_status} from the registered gate states")

    try:
        subprocess.run([sys.executable, str(ROOT / "reproduce/validate_repo.py")], cwd=ROOT, check=True)
    except subprocess.CalledProcessError as exc:
        errors.append(f"Repository validator failed with exit code {exc.returncode}")

    from validate_round import records, validate

    rows = records()
    for round_id in required_rounds:
        report = validate(round_id, rows, strict=True)
        if report["errors"]:
            errors.append(f"{round_id} strict record validation failed: " + "; ".join(report["errors"][:5]))
            continue

        policy = labelled_policies.get(round_id)
        if policy is not None:
            reproduced, output = run_official_grade_reproducer(round_id, policy)
            if output:
                print(output)
            label = read_round_label(round_id)
            if release_included_with_label(round_id, report, label, reproduced, policy):
                included_labels.append(
                    f"{round_id} ({report['missing']} declared Standard capture gaps; "
                    f"{len(report['protocol_deviations'])} declared deviations)"
                )
            else:
                errors.append(
                    f"{round_id} is not eligible for release-included-with-label: "
                    f"status/label, declared gaps/deviations, or official-grade reproducer check failed"
                )
            if not reproduced:
                errors.append(f"{round_id} official-grade reproducer failed or did not verify grade counts")
            continue

        if not report["strict_release_eligible"]:
            errors.append(
                f"{round_id} has {report['missing']} declared missing Standard capture slots and "
                f"{len(report['protocol_deviations'])} protocol deviations; it is not release-compliant"
            )

    if open_gates:
        errors.append("Open publication evidence gates: " + ", ".join(str(row.get("id")) for row in open_gates))
    if errors:
        print("RELEASE GATE: BLOCKED")
        for error in errors:
            print("- " + error)
        raise SystemExit(1)
    if included_labels:
        print("RELEASE-INCLUDED WITH LABEL: " + "; ".join(included_labels))
    print("RELEASE GATE: PASS — publication evidence gates resolved; scored-round records strict or explicitly labelled")


if __name__ == "__main__":
    main()
