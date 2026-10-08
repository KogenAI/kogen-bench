"""Check that per-round source-evidence partitions preserve their prior rows."""

from __future__ import annotations

import json
import subprocess
import unittest
from collections import defaultdict
from pathlib import Path

from missing_reasons import expand_value, load_legend
from partitioned_jsonl import read_partitions


ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_COMMIT = "e8c4196"


def baseline_rows(path: str) -> list[dict]:
    raw = subprocess.check_output(["git", "show", f"{PREVIOUS_COMMIT}:{path}"], cwd=ROOT)
    return [json.loads(line) for line in raw.splitlines() if line.strip()]


@unittest.skipUnless(subprocess.run(["git", "cat-file", "-e", PREVIOUS_COMMIT + "^{commit}"], cwd=ROOT, capture_output=True).returncode == 0, "historical migration baseline commit is not in this clone")
class EvidencePartitionTests(unittest.TestCase):
    def test_all_evidence_partitions_expand_to_prior_rows(self) -> None:
        prior_run_rows = baseline_rows("reproduce/inputs/run-evidence.jsonl")
        round_by_cell = {row["cell_id"]: row.get("round_id") for row in prior_run_rows}
        codes = load_legend(ROOT / "results" / "missing-reasons.json")
        families = [
            ("reproduce/inputs/run-evidence", "reproduce/inputs/run-evidence.jsonl", lambda row: row.get("round_id")),
            (
                "reproduce/inputs/context-evidence",
                "reproduce/inputs/context-evidence.jsonl",
                lambda row: round_by_cell.get(row.get("cell_id")),
            ),
            (
                "reproduce/inputs/ungraded-evidence",
                "reproduce/inputs/ungraded-evidence.jsonl",
                lambda row: row.get("round_id"),
            ),
            ("results/source-crosswalk", "results/source-crosswalk.jsonl", lambda row: row.get("round_id")),
        ]

        for directory, previous_path, round_for in families:
            expected: dict[str, list[dict]] = defaultdict(list)
            source_rows = baseline_rows(previous_path)
            for row in source_rows:
                round_id = round_for(row)
                key = round_id if isinstance(round_id, str) and round_id not in ("", "unmapped") else "unassigned"
                if previous_path.endswith("run-evidence.jsonl"):
                    provenance = row.get("provenance")
                    if isinstance(provenance, dict):
                        provenance["source_ref"] = "reproduce/inputs/run-evidence/index.json"
                elif previous_path.endswith("ungraded-evidence.jsonl"):
                    row["schema_version"] = "1.2"
                    provenance = row.get("provenance")
                    if isinstance(provenance, dict):
                        provenance["source_ref"] = "reproduce/inputs/ungraded-evidence/index.json"
                expected[key].append(row)

            index, _rows = read_partitions(ROOT / directory)
            self.assertLess((ROOT / directory / "index.json").stat().st_size, 100_000, directory)
            total = 0
            for entry in index["files"]:
                actual = [
                    json.loads(line)
                    for line in (ROOT / directory / entry["file"]).read_text(encoding="utf-8").splitlines()
                    if line.strip()
                ]
                expanded = [expand_value(row, codes) for row in actual]
                # round_status is relabelled after scrutiny; compare everything else to the baseline.
                strip = lambda rows: [{k: v for k, v in row.items() if k != "round_status"} if isinstance(row, dict) else row for row in rows]
                self.assertEqual(strip(expanded), strip(expected[entry["round_id"]]), f"{directory}/{entry['file']}")
                total += len(actual)
            self.assertEqual(total, len(source_rows), directory)


if __name__ == "__main__":
    unittest.main()
