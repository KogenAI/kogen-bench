#!/usr/bin/env python3
"""Restore compact schema-1.2 run records to their verbose schema-1.1 form."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from missing_reasons import expand_value, load_legend
from run_records import load_index


ROOT = Path(__file__).resolve().parents[1]
MAX_EXPANDED_FILE_BYTES = 10_000_000


def expand_record(record: dict, codes: dict[str, dict[str, str]]) -> dict:
    expanded = expand_value(record, codes)
    if expanded.get("schema_version") == "1.2":
        expanded["schema_version"] = "1.1"
    provenance = expanded.get("provenance")
    if isinstance(provenance, dict):
        provenance["source_ref"] = {
            "reproduce/inputs/run-evidence/index.json": "reproduce/inputs/run-evidence.jsonl",
            "reproduce/inputs/ungraded-evidence/index.json": "reproduce/inputs/context-evidence.jsonl",
        }.get(provenance.get("source_ref"), provenance.get("source_ref"))
    return expanded


def expand_to_directory(output_dir: Path) -> dict:
    source_dir = ROOT / "results" / "run-records"
    index = load_index(ROOT)
    codes = load_legend(ROOT / "results" / "missing-reasons.json")
    output_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for source_entry in index["files"]:
        source = source_dir / source_entry["file"]
        expanded_lines = []
        for line in source.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = expand_record(json.loads(line), codes)
                expanded_lines.append(json.dumps(row, sort_keys=True) + "\n")
        data = "".join(expanded_lines).encode("utf-8")
        if len(data) > MAX_EXPANDED_FILE_BYTES:
            raise ValueError(f"Expanded {source_entry['file']} exceeds 10 MB: {len(data)} bytes")
        destination = output_dir / source_entry["file"]
        temporary = destination.with_name(destination.name + ".tmp")
        temporary.write_bytes(data)
        temporary.replace(destination)
        entries.append(
            {
                "file": source_entry["file"],
                "round_id": source_entry["round_id"],
                "record_count": len(expanded_lines),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "schema_version": "1.1",
            }
        )
    keep = {entry["file"] for entry in entries}
    for path in output_dir.glob("*.jsonl"):
        if path.name not in keep:
            path.unlink()
    expanded_index = {"index_schema_version": index["index_schema_version"], "files": entries}
    (output_dir / "index.json").write_text(
        json.dumps(expanded_index, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return expanded_index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "run-records-expanded")
    args = parser.parse_args()
    index = expand_to_directory(args.output_dir)
    count = sum(entry["record_count"] for entry in index["files"])
    print(f"Expanded {count} records across {len(index['files'])} files into {args.output_dir}")


if __name__ == "__main__":
    main()
