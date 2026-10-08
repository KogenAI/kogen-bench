"""Read and validate the indexed per-round standard-record export."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from missing_reasons import load_legend
from partitioned_jsonl import MAX_PARTITION_BYTES


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = Path("results/run-records/index.json")
MAX_FILE_BYTES = MAX_PARTITION_BYTES
INDEX_SCHEMA_VERSION = "1.0"


def load_index(root: Path = ROOT) -> dict:
    path = root / INDEX_PATH
    index = json.loads(path.read_text(encoding="utf-8"))
    if index.get("index_schema_version") != INDEX_SCHEMA_VERSION:
        raise ValueError(f"Unsupported run-record index schema in {INDEX_PATH}")
    entries = index.get("files")
    if not isinstance(entries, list):
        raise ValueError("Run-record index must contain a files array")
    names = set()
    round_ids = set()
    for entry in entries:
        name = entry.get("file")
        round_id = entry.get("round_id")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.jsonl", name):
            raise ValueError(f"Invalid run-record file name: {name!r}")
        if name in names:
            raise ValueError(f"Duplicate run-record file in index: {name}")
        if not isinstance(round_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", round_id):
            raise ValueError(f"Invalid run-record round ID: {round_id!r}")
        if round_id in round_ids:
            raise ValueError(f"Duplicate run-record round ID in index: {round_id}")
        if name != f"{round_id}.jsonl":
            raise ValueError(f"Run-record filename does not match round ID: {name}")
        names.add(name)
        round_ids.add(round_id)
        for field in ("record_count", "bytes"):
            if not isinstance(entry.get(field), int) or isinstance(entry[field], bool) or entry[field] < 0:
                raise ValueError(f"Invalid {field} for {name}")
        if entry["bytes"] > MAX_FILE_BYTES:
            raise ValueError(f"Run-record file exceeds {MAX_FILE_BYTES} bytes: {name}")
        if not re.fullmatch(r"[a-f0-9]{64}", str(entry.get("sha256", ""))):
            raise ValueError(f"Invalid sha256 for {name}")
        if not isinstance(entry.get("schema_version"), str) or not entry["schema_version"]:
            raise ValueError(f"Missing record schema version for {name}")
    if not entries or "unassigned" not in round_ids:
        raise ValueError("Run-record index must include an unassigned file")
    return index


def indexed_records(root: Path = ROOT, *, verify: bool = True) -> list[dict]:
    """Load files in index order and optionally verify every recorded checksum."""
    index = load_index(root)
    records = []
    codes = load_legend(root / "results" / "missing-reasons.json")
    unassigned_code = next(
        code for code, entry in codes.items()
        if entry["reason"] == "No unambiguous owning round tag"
        and entry["reconstructable_from"] == "none"
    )
    for entry in index["files"]:
        name = entry["file"]
        path = root / "results" / "run-records" / name
        raw = path.read_bytes()
        if verify:
            if len(raw) != entry["bytes"]:
                raise ValueError(f"Byte count mismatch for {name}")
            if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
                raise ValueError(f"SHA-256 mismatch for {name}")
            if len(raw) > MAX_FILE_BYTES:
                raise ValueError(f"Run-record file exceeds {MAX_FILE_BYTES} bytes: {name}")
        lines = raw.splitlines(keepends=True)
        if len(lines) != entry["record_count"]:
            raise ValueError(f"Record count mismatch for {name}")
        for number, line in enumerate(lines, 1):
            if not line.strip():
                raise ValueError(f"Blank JSONL record in {name}:{number}")
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Malformed JSONL in {name}:{number}: {exc}") from exc
            if row.get("schema_version") != entry["schema_version"]:
                raise ValueError(f"Schema version mismatch in {name}:{number}")
            if entry["round_id"] == "unassigned":
                reason = row.get("round_id")
                if (
                    row.get("audit_round") != "unmapped"
                    or not isinstance(reason, dict)
                    or reason.get("missing") != unassigned_code
                ):
                    raise ValueError(f"Unassigned record lost its round-tag reason in {name}:{number}")
            elif row.get("audit_round") != entry["round_id"] or row.get("round_id") != entry["round_id"]:
                raise ValueError(f"Record is in the wrong round file: {name}:{number}")
            records.append(row)
    return records


def is_run_record_file(value: object) -> bool:
    """Whether a crosswalk source path names a file listed under the run-record directory."""
    return isinstance(value, str) and re.fullmatch(r"results/run-records/[a-z0-9][a-z0-9-]*\.jsonl", value) is not None
