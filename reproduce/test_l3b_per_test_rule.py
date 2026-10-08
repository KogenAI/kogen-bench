"""Ensure the public L3b no-regression rule recomputes from per-test sets."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
L3B_REPRO = ROOT / "rounds" / "l3b-repair-vs-continue" / "reproduce"
sys.path.insert(0, str(L3B_REPRO))

from l3b_per_test_rule import load_per_test_results, per_test_no_regression  # noqa: E402


class L3bPerTestRuleTests(unittest.TestCase):
    def test_no_regression_recomputes_from_published_sets(self) -> None:
        cells = load_per_test_results()
        result, comparisons = per_test_no_regression(cells)
        self.assertEqual(len(comparisons), 8)
        self.assertTrue(result)
        self.assertTrue(all(row["no_regression"] for row in comparisons))


if __name__ == "__main__":
    unittest.main()
