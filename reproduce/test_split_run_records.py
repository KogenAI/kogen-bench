"""Prove that indexed run-record partitions preserve every original record."""

import json
import subprocess
import unittest
from collections import defaultdict
from pathlib import Path

from expand_records import expand_record
from missing_reasons import load_legend
from run_records import MAX_FILE_BYTES, ROOT, indexed_records, load_index


BASELINE_COMMIT = "7cc9c0d"


@unittest.skipUnless(subprocess.run(["git", "cat-file", "-e", BASELINE_COMMIT + "^{commit}"], cwd=ROOT, capture_output=True).returncode == 0, "historical migration baseline commit is not in this clone")
class SplitRunRecordTests(unittest.TestCase):
    def test_indexed_files_are_a_lossless_partition_of_main(self):
        original = subprocess.check_output(
            ["git", "show", f"{BASELINE_COMMIT}:results/run-records.jsonl"], cwd=ROOT
        )
        original_lines = original.splitlines(keepends=True)
        expected_by_round = defaultdict(list)
        for line in original_lines:
            row = json.loads(line)
            round_id = row.get("round_id")
            key = round_id if isinstance(round_id, str) and round_id not in ("", "unmapped") else "unassigned"
            expected_by_round[key].append(line)

        index = load_index(ROOT)
        concatenated = []
        codes = load_legend(ROOT / "results" / "missing-reasons.json")
        for entry in index["files"]:
            path = ROOT / "results" / "run-records" / entry["file"]
            raw = path.read_bytes()
            self.assertLessEqual(len(raw), MAX_FILE_BYTES, entry["file"])
            actual_lines = raw.splitlines(keepends=True)
            expanded_lines = [
                (json.dumps(expand_record(json.loads(line), codes), sort_keys=True) + "\n").encode()
                for line in actual_lines
            ]
            self.assertEqual(expanded_lines, expected_by_round[entry["round_id"]], entry["file"])
            concatenated.extend(actual_lines)

        self.assertEqual(len(original_lines), 6521)
        self.assertEqual(indexed_records(ROOT), [json.loads(line) for line in concatenated])
        self.assertEqual(next(item["record_count"] for item in index["files"] if item["round_id"] == "unassigned"), 500)


if __name__ == "__main__":
    unittest.main()
