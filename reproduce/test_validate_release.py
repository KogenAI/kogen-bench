"""Focused tests for historical labels and the new-round strict cutoff."""

import json
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_release import read_field, round_date, validate_historical_inventory


class ReleasePolicyTest(unittest.TestCase):
    def test_every_historical_round_has_publication_metadata(self):
        errors, historical = validate_historical_inventory()
        self.assertEqual(errors, [])
        self.assertEqual(len(historical), 177)

    def test_l3b_keeps_valid_status_and_declares_narrow_limits(self):
        self.assertIn("VALID", read_field("l3b-repair-vs-continue", "Publication badge"))
        self.assertIn("NARROW / HISTORICAL", read_field("l3b-repair-vs-continue", "Publication badge"))
        self.assertIn("193 missing Standard capture fields", read_field("l3b-repair-vs-continue", "Publication limits"))
        self.assertIn("STATUS: **VALID**", (Path(__file__).resolve().parents[1] / "rounds/l3b-repair-vs-continue/README.md").read_text())

    def test_new_round_cutoff_is_october_ninth_2026(self):
        root = Path(__file__).resolve().parents[1]
        config = json.loads((root / "reproduce/release-rounds.json").read_text())
        cutoff = date.fromisoformat(config["strict_from_date"])
        self.assertEqual(cutoff, date(2026, 10, 9))
        self.assertLess(round_date("l3b-repair-vs-continue"), cutoff)

    def test_non_valid_rounds_declare_reason(self):
        self.assertTrue(read_field("l3-repair", "Why not VALID"))
        self.assertTrue(read_field("l3-repair", "Recomputation status"))


if __name__ == "__main__":
    unittest.main()
