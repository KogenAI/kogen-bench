"""Small policy helpers for separating disclosed blockers from bad records."""
import re
from pathlib import Path
from run_records import is_run_record_file


UNRESOLVED_DELIVERY_STATUS = "unresolved_no_shared_exact_cell_id"


def undocumented_unmatched_graded_ids(cell_ids, crosswalk_rows):
    """Return graded run-record IDs missing an explicit unresolved disposition."""
    documented = {
        row.get("source_record_id")
        for row in crosswalk_rows
        if row.get("record_role") == "captured_delivery"
        and is_run_record_file(row.get("source_file"))
        and row.get("linkage_status") == UNRESOLVED_DELIVERY_STATUS
        and isinstance(row.get("source_record_id"), str)
        and row.get("source_record_id")
    }
    return sorted(set(cell_ids) - documented)


def spec_source_disclosed_unvendored(evidence_map_text):
    """Whether the map explicitly states why source clauses cannot be re-read."""
    return bool(re.search(
        r"the specification source is not vendored in this benchmark worktree",
        evidence_map_text,
        re.IGNORECASE,
    ))


def has_standard_run_records(round_id, run_records):
    """Standard-schema validation applies only when that schema has round rows."""
    return any(
        row.get("audit_round") == round_id or row.get("round_id") == round_id
        for row in run_records
    )


def is_preparation_only_registration(round_id, register_text):
    """Whether the public register explicitly records a pre-scored lane."""
    for line in register_text.splitlines():
        match = re.match(
            r"\s*-\s+\[([^]]+)\]\([^)]*/README\.md\)\s+—\s+\*\*(INTERIM|NOT-RUN)\*\*(.*)$",
            line,
        )
        if not match or match.group(1) != round_id:
            continue
        summary = match.group(3)
        return bool(
            re.search(r"preparation only", summary, re.IGNORECASE)
            and re.search(r"no scored .*cell has run", summary, re.IGNORECASE)
        )
    return False
