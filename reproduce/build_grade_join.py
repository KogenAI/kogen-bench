#!/usr/bin/env python3
"""Build the exact public official-export join for captured grade IDs."""

import csv
import json
from pathlib import Path
from run_records import indexed_records, is_run_record_file
from missing_reasons import compact_value, load_marker_to_code
from partitioned_jsonl import read_partitions, write_partitions


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
INPUT = RESULTS / "grade-join-input.jsonl"
OUTPUT = RESULTS / "grade-join.csv"
CROSSWALK = RESULTS / "source-crosswalk"
PUBLIC_GRADE_SNAPSHOT = ROOT / "reproduce/inputs/grades.final.jsonl"
EXPECTED_DELIVERIES = 5020
EXPECTED_PUBLIC = 5020
EXPECTED_CAPTURE_REPORTED = 0
EXACT_JOIN_STATUS = "exact_official_grade_join"
EXACT_JOIN_RULE = "source_record_id == public_cell_id == grades.final.jsonl cell_id (unique on both sides)"
PUBLIC_SNAPSHOT_CUT = "2026-10-05T11:08:31Z"
FIELDS = [
    "delivery_id",
    "official_grade_id",
    "source",
    "rule",
    "publication_scope",
]


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def build_join() -> list[dict]:
    rows = []
    seen_deliveries = set()
    seen_grades = set()
    for line_number, item in enumerate(read_jsonl(INPUT), 1):
        delivery_id = item.get("delivery_id")
        official_grade_id = item.get("official_grade_id")
        if not delivery_id or not official_grade_id:
            raise ValueError(f"empty required ID on input line {line_number}")
        if delivery_id in seen_deliveries:
            raise ValueError(f"duplicate delivery_id on input line {line_number}")
        if official_grade_id in seen_grades:
            raise ValueError(f"duplicate official_grade_id on input line {line_number}")
        if delivery_id != official_grade_id:
            raise ValueError(f"non-exact grade ID join on input line {line_number}")
        seen_deliveries.add(delivery_id)
        seen_grades.add(official_grade_id)
        rows.append(
            {
                "delivery_id": delivery_id,
                "official_grade_id": official_grade_id,
                "source": item["source"],
                "rule": item["rule"],
            }
        )

    rows.sort(key=lambda row: row["delivery_id"])
    if len(rows) != EXPECTED_DELIVERIES:
        raise ValueError(f"expected {EXPECTED_DELIVERIES} exact grade joins, found {len(rows)}")

    public_ids = {
        row.get("cell_id")
        for row in read_jsonl(PUBLIC_GRADE_SNAPSHOT)
        if isinstance(row.get("cell_id"), str) and row.get("cell_id")
    }
    capture_by_id = {
        row.get("cell_id"): row
        for row in indexed_records()
        if row.get("graded") is True and isinstance(row.get("cell_id"), str)
    }
    input_by_id = {row["delivery_id"]: row for row in read_jsonl(INPUT)}
    for row in rows:
        cid = row["official_grade_id"]
        source = input_by_id[cid].get("source")
        rule = str(input_by_id[cid].get("rule", ""))
        if cid in public_ids:
            if source != "grades.final.jsonl" or "exact equality" not in rule:
                raise ValueError(f"public export row lacks an exact official-ID rule: {cid}")
            row["publication_scope"] = "public_export"
        else:
            capture = capture_by_id.get(cid)
            grade = capture.get("grade", {}) if capture else {}
            timestamp = grade.get("timestamp") if isinstance(grade, dict) else None
            if (
                source != "run-record capture metadata"
                or "capture-reported" not in rule
                or "official export row absent" not in rule
                or capture is None
                or capture.get("outcome") not in {"pass", "fail"}
                or not isinstance(timestamp, str)
                or timestamp <= PUBLIC_SNAPSHOT_CUT
            ):
                raise ValueError(f"post-cut mapping lacks capture-side outcome/timestamp evidence: {cid}")
            row["publication_scope"] = "capture_reported_export_absent"
    public_count = sum(row["publication_scope"] == "public_export" for row in rows)
    capture_reported_count = len(rows) - public_count
    if (public_count, capture_reported_count) != (EXPECTED_PUBLIC, EXPECTED_CAPTURE_REPORTED):
        raise ValueError(
            "unexpected public/internal grade split: "
            f"{public_count} public export matches, {capture_reported_count} capture-reported mappings"
        )

    graded_run_ids = {
        row.get("cell_id")
        for row in indexed_records()
        if row.get("graded") is True and isinstance(row.get("cell_id"), str)
    }
    if graded_run_ids != seen_deliveries:
        raise ValueError(
            "exact grade join does not cover precisely the capture rows marked graded "
            f"({len(graded_run_ids)} graded capture IDs, {len(seen_deliveries)} joined IDs)"
        )
    return rows


def write_crosswalk(rows: list[dict]) -> None:
    by_delivery = {row["delivery_id"]: row for row in rows}
    crosswalk_rows = read_partitions(CROSSWALK)[1]
    records = indexed_records()
    source_by_id = {}
    for row in records:
        cell_id = row.get("cell_id")
        if isinstance(cell_id, str):
            round_id = row.get("round_id")
            round_id = round_id if isinstance(round_id, str) and round_id else "unassigned"
            source_by_id[cell_id] = f"results/run-records/{round_id}.jsonl"
    capture_rows: dict[str, dict] = {}
    for item in crosswalk_rows:
        if (
            item.get("record_role") == "captured_delivery"
            and item.get("source_record_id") in source_by_id
        ):
            source_id = item.get("source_record_id")
            if isinstance(source_id, str) and source_id in capture_rows:
                raise ValueError(f"duplicate captured-delivery crosswalk row: {source_id}")
            if isinstance(source_id, str):
                capture_rows[source_id] = item

    missing = set(by_delivery) - set(capture_rows)
    if missing:
        raise ValueError(f"{len(missing)} joined delivery IDs have no crosswalk row")

    for item in crosswalk_rows:
        source_id = item.get("source_record_id")
        if item.get("record_role") != "captured_delivery":
            continue
        if source_id in source_by_id:
            item["source_file"] = source_by_id[source_id]
        elif item.get("source_file") == "results/run-records.jsonl" or is_run_record_file(item.get("source_file")):
            raise ValueError(f"Captured-delivery crosswalk ID is absent from indexed run records: {source_id}")
        if source_id not in by_delivery:
            continue

        join = by_delivery[source_id]
        capture_reported = join["publication_scope"] == "capture_reported_export_absent"
        item["public_cell_id"] = join["official_grade_id"]
        item["linked_cell_ids"] = [join["official_grade_id"]]
        item["linkage_status"] = "capture_reported_identity_mapping" if capture_reported else EXACT_JOIN_STATUS
        item["identity_status"] = "capture_reported_shared_cell_id" if capture_reported else "exact_shared_cell_id"
        item["grade_status"] = "capture_reported_grade" if capture_reported else "officially_graded"
        item["grade_publication_status"] = join["publication_scope"]
        item["grade_publication_label"] = (
            "capture-reported grade; official export row absent"
            if capture_reported
            else "officially graded; in the public export"
        )
        item["grade_join_source"] = join["source"]
        item["grade_join_rule"] = join["rule"] if capture_reported else EXACT_JOIN_RULE
        if capture_reported:
            item["grade_publication_note"] = (
                "The capture ledger reports the outcome and grade timestamp, but the "
                "authoritative official-export row is absent, so the official side of this "
                f"identity mapping cannot be independently checked. Graded after the public "
                f"snapshot cut ({PUBLIC_SNAPSHOT_CUT}); excluded from canonical outcome counts."
            )
            item["explanation"] = (
                "Capture-reported grade; authoritative official-export row absent. The public "
                "capture reports an outcome and timestamp, but the mapping's official side "
                "cannot be independently checked. Excluded from canonical outcome counts. "
                f"Graded after the public snapshot cut ({PUBLIC_SNAPSHOT_CUT})."
            )
        else:
            item["grade_publication_note"] = (
                "The exact official grade ID is present in the public grade snapshot."
            )
            item["explanation"] = (
                "Officially graded and present in the public export. Exact join: "
                "source_record_id == public_cell_id == grades.final.jsonl cell_id."
            )

    marker_to_code = load_marker_to_code()
    write_partitions(
        crosswalk_rows,
        CROSSWALK,
        round_for=lambda row: row.get("round_id") if isinstance(row.get("round_id"), str) else None,
        ensure_ascii=False,
        transform=lambda row: compact_value(row, marker_to_code),
    )


def main() -> None:
    rows = build_join()
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    write_crosswalk(rows)
    public_count = sum(row["publication_scope"] == "public_export" for row in rows)
    capture_reported_count = len(rows) - public_count
    print(
        f"wrote {public_count} public exact official-export matches and "
        f"{capture_reported_count} capture-reported ID mappings without export rows; "
        "regenerated results/source-crosswalk/index.json and its per-round files"
    )


if __name__ == "__main__":
    main()
