import unittest

import scrutinize


class ScrutinyTests(unittest.TestCase):
    def test_current_release_counts_are_recomputed(self):
        report = scrutinize.scrutinize(operator_root=None)["rounds"]
        self.assertEqual(report["l3-repair"]["counts"]["repair"], [2, 6])
        self.assertEqual(report["l3b-repair-vs-continue"]["counts"], {
            "REPAIR": [3, 8], "CONTINUE": [1, 8], "RESTART": [2, 8]})
        self.assertEqual(report["lang-sol-replication"]["equal_task_percent"], {
            "rust": 90.3, "go": 88.9, "ts-bun": 83.3})
        self.assertFalse(any(issue["code"] in {"count_mismatch", "rate_mismatch", "usage_mismatch"}
                             for row in report.values() for issue in row["issues"]))

    def test_wrong_headline_is_detected(self):
        result = {"issues": []}
        scrutinize.assert_claim(result, "Headline: 3/6 repairs rescued", r"Headline: (\d+)/(\d+) repairs rescued",
                                (2, 6), "README.md:1")
        self.assertEqual(result["issues"][0]["code"], "count_mismatch")

    def test_usage_arithmetic_is_checked(self):
        result = {"issues": []}
        scrutinize.check_usage(result, [{"a": "2", "b": "3", "c": "4", "total_tokens": "8"}],
                               ("a", "b", "c"), "cells.csv")
        self.assertEqual(result["issues"][0]["code"], "usage_mismatch")

    def test_declared_missing_is_not_complete(self):
        self.assertTrue(scrutinize.missing({"missing": "receipt gap"}))
        self.assertTrue(scrutinize.missing({"host": {"withheld": "public gap"}}))
        self.assertFalse(scrutinize.missing({"model": "pinned"}))

    def test_signoff_reviewer_must_be_independent_model_and_not_round_author(self):
        reviewer = {"kind": "independent_model", "model": "gpt-6-astra", "effort": "high"}
        self.assertTrue(scrutinize.is_independent_reviewer(reviewer))
        self.assertFalse(scrutinize.is_independent_reviewer({**reviewer, "round_author": True}))
        self.assertFalse(scrutinize.is_independent_reviewer({**reviewer, "kind": "round_author"}))

    def test_release_gate_requires_signoffs(self):
        report = scrutinize.scrutinize(operator_root=None)
        errors = scrutinize.validate_signoffs(report)
        self.assertEqual(len(errors), 3)
        self.assertTrue(all("missing scrutiny sign-off" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
