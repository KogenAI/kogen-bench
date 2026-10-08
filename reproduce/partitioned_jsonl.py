"""Read and write small, checksummed JSONL partitions keyed by round."""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Iterable


INDEX_SCHEMA_VERSION = "1.0"
MAX_PARTITION_BYTES = 9_000_000
ROUND_ID = re.compile(r"[a-z0-9][a-z0-9-]*\Z")


def _encode(rows: Iterable[dict], *, ensure_ascii: bool) -> bytes:
    return "".join(
        json.dumps(row, sort_keys=True, ensure_ascii=ensure_ascii) + "\n" for row in rows
    ).encode("utf-8")


def write_partitions(
    rows: Iterable[dict],
    directory: Path,
    *,
    round_for: Callable[[dict], str | None],
    schema_field: str | None = None,
    ensure_ascii: bool = True,
    transform: Callable[[dict], dict] | None = None,
) -> dict:
    """Write rows into deterministic per-round files and return the small index."""
    groups: dict[str, list[dict]] = defaultdict(list)
    for source_row in rows:
        row = transform(source_row) if transform else source_row
        round_id = round_for(row)
        key = round_id if isinstance(round_id, str) and round_id not in ("", "unmapped") else "unassigned"
        if not ROUND_ID.fullmatch(key):
            raise ValueError(f"Unsafe round ID for partition: {key!r}")
        groups[key].append(row)

    ordered_round_ids = sorted(key for key in groups if key != "unassigned")
    if "unassigned" in groups:
        ordered_round_ids.append("unassigned")
    directory.mkdir(parents=True, exist_ok=True)
    entries = []
    for round_id in ordered_round_ids:
        rows_for_round = groups[round_id]
        data = _encode(rows_for_round, ensure_ascii=ensure_ascii)
        if len(data) > MAX_PARTITION_BYTES:
            raise ValueError(f"{round_id}.jsonl exceeds {MAX_PARTITION_BYTES} bytes: {len(data)}")
        entry: dict[str, Any] = {
            "file": f"{round_id}.jsonl",
            "round_id": round_id,
            "record_count": len(rows_for_round),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        if schema_field:
            versions = {row.get(schema_field) for row in rows_for_round}
            if len(versions) != 1 or not all(isinstance(version, str) and version for version in versions):
                raise ValueError(f"{round_id}.jsonl has inconsistent {schema_field}: {versions}")
            entry[schema_field] = next(iter(versions))
        path = directory / entry["file"]
        temporary = path.with_name(path.name + ".tmp")
        temporary.write_bytes(data)
        temporary.replace(path)
        entries.append(entry)

    keep = {entry["file"] for entry in entries}
    for path in directory.glob("*.jsonl"):
        if path.name not in keep:
            path.unlink()
    index = {"index_schema_version": INDEX_SCHEMA_VERSION, "files": entries}
    (directory / "index.json").write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return index


def read_partitions(
    directory: Path,
    *,
    verify: bool = True,
    round_field: str | None = None,
) -> tuple[dict, list[dict]]:
    """Read a partition index, validating every file's count, size and digest."""
    index_path = directory / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    entries = index.get("files")
    if index.get("index_schema_version") != INDEX_SCHEMA_VERSION or not isinstance(entries, list):
        raise ValueError(f"Malformed partition index: {index_path}")
    rows: list[dict] = []
    seen_rounds: set[str] = set()
    for entry in entries:
        round_id = entry.get("round_id") if isinstance(entry, dict) else None
        name = entry.get("file") if isinstance(entry, dict) else None
        if (
            not isinstance(round_id, str)
            or not ROUND_ID.fullmatch(round_id)
            or name != f"{round_id}.jsonl"
            or round_id in seen_rounds
            or not isinstance(entry.get("record_count"), int)
            or isinstance(entry.get("record_count"), bool)
            or entry["record_count"] < 0
            or not isinstance(entry.get("bytes"), int)
            or isinstance(entry.get("bytes"), bool)
            or not 0 <= entry["bytes"] <= MAX_PARTITION_BYTES
            or not re.fullmatch(r"[a-f0-9]{64}", str(entry.get("sha256", "")))
        ):
            raise ValueError(f"Malformed partition entry in {index_path}: {entry!r}")
        seen_rounds.add(round_id)
        path = directory / name
        raw = path.read_bytes()
        if verify and (
            len(raw) != entry["bytes"]
            or hashlib.sha256(raw).hexdigest() != entry["sha256"]
            or len(raw) > MAX_PARTITION_BYTES
        ):
            raise ValueError(f"Partition fingerprint mismatch: {path}")
        lines = raw.splitlines(keepends=True)
        if len(lines) != entry["record_count"]:
            raise ValueError(f"Partition record count mismatch: {path}")
        for number, line in enumerate(lines, 1):
            if not line.strip():
                raise ValueError(f"Blank record in {path}:{number}")
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON in {path}:{number}: {exc}") from exc
            if round_field:
                value = row.get(round_field)
                row_round = value if isinstance(value, str) else "unassigned"
                if row_round != round_id and not (round_id == "unassigned" and row_round in ("", "unmapped", "unassigned")):
                    raise ValueError(f"Record is in the wrong partition: {path}:{number}")
            rows.append(row)
    return index, rows
