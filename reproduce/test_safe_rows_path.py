"""Tests for resolving the approved sanitizer in constrained environments."""

import tempfile
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from safe_rows_path import resolve_safe_rows_path


class InaccessibleCandidate:
    def is_file(self):
        raise PermissionError("candidate parent is not readable")

    def is_symlink(self):
        raise AssertionError("is_symlink should not run after is_file fails")


class InaccessibleSymlinkCheck:
    def is_file(self):
        return True

    def is_symlink(self):
        raise PermissionError("candidate parent is not readable")


class SafeRowsPathTests(unittest.TestCase):
    def test_permission_errors_skip_candidates(self):
        with tempfile.TemporaryDirectory() as directory:
            available = Path(directory) / "safe_rows.py"
            available.write_text("# test helper\n", encoding="utf-8")
            selected = resolve_safe_rows_path(
                [InaccessibleCandidate(), InaccessibleSymlinkCheck(), available]
            )

        self.assertEqual(selected, available)

    def test_repository_helper_precedes_machine_candidates(self):
        from safe_rows_path import default_candidates

        candidates = default_candidates()
        self.assertEqual(candidates[0], Path(__file__).resolve().with_name("safe_rows.py"))


if __name__ == "__main__":
    unittest.main()
