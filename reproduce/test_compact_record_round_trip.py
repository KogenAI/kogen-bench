"""Prove compact records expand byte-for-byte to the preceding verbose files."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from expand_records import ROOT, expand_to_directory
from run_records import load_index


VERBOSE_COMMIT = "e8c4196"


@unittest.skipUnless(subprocess.run(["git", "cat-file", "-e", VERBOSE_COMMIT + "^{commit}"], cwd=ROOT, capture_output=True).returncode == 0, "historical migration baseline commit is not in this clone")
class CompactRecordRoundTripTests(unittest.TestCase):
    def test_every_record_and_index_restore_byte_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "expanded"
            expanded_index = expand_to_directory(output_dir)
            self.assertEqual(
                (output_dir / "index.json").read_bytes(),
                subprocess.check_output(
                    ["git", "show", f"{VERBOSE_COMMIT}:results/run-records/index.json"], cwd=ROOT
                ),
            )
            compact_index = load_index(ROOT)
            self.assertEqual(len(expanded_index["files"]), len(compact_index["files"]))
            record_count = 0
            for entry in compact_index["files"]:
                name = entry["file"]
                verbose = subprocess.check_output(
                    ["git", "show", f"{VERBOSE_COMMIT}:results/run-records/{name}"], cwd=ROOT
                )
                self.assertEqual((output_dir / name).read_bytes(), verbose, name)
                record_count += entry["record_count"]
            self.assertEqual(record_count, 6521)


if __name__ == "__main__":
    unittest.main()
