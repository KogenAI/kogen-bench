"""Focused tests for the release-included-with-label policy."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_release import release_included_with_label


class ReleaseIncludedWithLabelTest(unittest.TestCase):
    def setUp(self):
        self.policy = {
            "analysis_status": "DESCRIPTIVE",
            "label": "DESCRIPTIVE — raw captures not retained; results verified against official grades",
        }
        self.label = self.policy["label"]
        self.report = {"errors": [], "missing": 1782, "protocol_deviations": ["declared gap"] * 4}

    def test_accepts_declared_descriptive_round_with_official_grade_reproducer(self):
        self.assertTrue(release_included_with_label(
            "lang-sol-replication", self.report, self.label, True, self.policy
        ))

    def test_rejects_wrong_analysis_status(self):
        policy = {**self.policy, "analysis_status": "CONFIRMATORY"}
        self.assertFalse(release_included_with_label(
            "lang-sol-replication", self.report, self.label, True, policy
        ))

    def test_rejects_missing_label(self):
        self.assertFalse(release_included_with_label(
            "lang-sol-replication", self.report, "DESCRIPTIVE", True, self.policy
        ))

    def test_rejects_undeclared_or_invalid_gaps(self):
        report = {**self.report, "errors": ["Undeclared gap"]}
        self.assertFalse(release_included_with_label(
            "lang-sol-replication", report, self.label, True, self.policy
        ))

    def test_rejects_round_without_gaps_or_deviations(self):
        report = {"errors": [], "missing": 0, "protocol_deviations": []}
        self.assertFalse(release_included_with_label(
            "lang-sol-replication", report, self.label, True, self.policy
        ))

    def test_rejects_round_without_official_grade_reproduction(self):
        self.assertFalse(release_included_with_label(
            "lang-sol-replication", self.report, self.label, False, self.policy
        ))


if __name__ == "__main__":
    unittest.main()
