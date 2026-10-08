import unittest

from validation_policy import (
    has_standard_run_records,
    is_preparation_only_registration,
    spec_source_disclosed_unvendored,
    undocumented_unmatched_graded_ids,
)


class PublicationValidationPolicyTests(unittest.TestCase):
    def test_unresolved_join_is_a_blocker_only_when_every_id_is_disclosed(self):
        unresolved = {
            "record_role": "captured_delivery",
            "source_file": "results/run-records/r1.jsonl",
            "source_record_id": "existing-run-record-id",
            "linkage_status": "unresolved_no_shared_exact_cell_id",
        }
        self.assertEqual(
            undocumented_unmatched_graded_ids(["existing-run-record-id"], [unresolved]),
            [],
        )
        self.assertEqual(
            undocumented_unmatched_graded_ids(
                ["existing-run-record-id", "undocumented-run-record-id"], [unresolved]
            ),
            ["undocumented-run-record-id"],
        )

    def test_unresolved_status_must_belong_to_captured_run_record(self):
        wrong_source = {
            "record_role": "official_outcome_export_row",
            "source_file": "results/cells.jsonl",
            "source_record_id": "existing-run-record-id",
            "linkage_status": "unresolved_no_shared_exact_cell_id",
        }
        self.assertEqual(
            undocumented_unmatched_graded_ids(["existing-run-record-id"], [wrong_source]),
            ["existing-run-record-id"],
        )

    def test_missing_spec_source_needs_explicit_disclosure(self):
        disclosed = "The specification source is not vendored in this benchmark worktree."
        self.assertTrue(spec_source_disclosed_unvendored(disclosed))
        self.assertFalse(spec_source_disclosed_unvendored("Clause coverage is complete."))

    def test_standard_schema_applies_when_round_rows_exist(self):
        rows = [{"audit_round": "r1"}, {"round_id": "r2"}]
        self.assertTrue(has_standard_run_records("r1", rows))
        self.assertTrue(has_standard_run_records("r2", rows))
        self.assertFalse(has_standard_run_records("l3-repair", rows))

    def test_preparation_only_lane_may_be_registered_without_lane_edits(self):
        line = "- [l3-repair](l3-repair/README.md) — **INTERIM** Preparation only; no scored L3 cell has run."
        self.assertTrue(is_preparation_only_registration("l3-repair", line))
        self.assertFalse(is_preparation_only_registration("l3-repair", "- [l3-repair](l3-repair/README.md) — **INTERIM** Counts unavailable."))


if __name__ == "__main__":
    unittest.main()
