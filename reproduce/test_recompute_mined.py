import unittest

from recompute_mined import _metadata_comparison, _page_text, _public_comparison, summarize_rows


class RecomputeMinedTests(unittest.TestCase):
    def test_summarizes_pass_rate_tokens_and_wall_median(self):
        rows = [
            {
                "official_grade": {"classification": "pass"},
                "usage": {
                    "input_tokens": 100,
                    "cached_input_tokens": 20,
                    "output_tokens": 5,
                    "reasoning_tokens": 2,
                },
                "wall_s": 10,
            },
            {
                "official_grade": {"classification": "fail"},
                "usage": {
                    "input_tokens": 50,
                    "cached_input_tokens": 0,
                    "output_tokens": 7,
                    "reasoning_tokens": 1,
                },
                "wall_s": 20,
            },
        ]
        summary = summarize_rows(rows)
        self.assertEqual(summary["pass_count"], 1)
        self.assertEqual(summary["fail_count"], 1)
        self.assertEqual(summary["pass_rate"], 0.5)
        self.assertEqual(summary["input_plus_cached_plus_output"]["total"], 182)
        self.assertEqual(summary["usage_tokens"]["reasoning_tokens"]["total"], 3)
        self.assertEqual(summary["wall_s"]["median"], 15)

    def test_does_not_turn_missing_usage_into_zero(self):
        summary = summarize_rows([{"official_grade": None, "usage": {}, "wall_s": None}])
        self.assertEqual(summary["input_plus_cached_plus_output"]["complete_cells"], 0)
        self.assertEqual(summary["usage_tokens"]["output_tokens"]["missing_cells"], 1)
        self.assertIsNone(summary["wall_s"]["median"])

    def test_reports_missing_metadata_example_cell_ids(self):
        comparison = _metadata_comparison(
            [{"cell_id": "pilot73-cell", "round": "pilot73", "usage": {}}],
            {},
        )
        self.assertEqual(comparison["token_missing_metadata"], 1)
        self.assertEqual(
            comparison["token_missing_metadata_examples"],
            [{"round": "pilot73", "cell_id": "pilot73-cell"}],
        )

    def test_reports_exact_formula_control_with_cache_and_reasoning(self):
        cell_id = "codex__model__low__task__formula-control"
        comparison = _metadata_comparison(
            [{
                "cell_id": cell_id,
                "round": "r1",
                "harness": "codex",
                "usage": {
                    "input_tokens": 100,
                    "cached_input_tokens": 20,
                    "output_tokens": 5,
                    "reasoning_tokens": 2,
                },
            }],
            {cell_id: {"tokens": 125}},
        )
        self.assertEqual(comparison["token_cells_equal"], 1)
        self.assertEqual(comparison["token_exact_codex_examples"][0]["cell_id"], cell_id)
        self.assertEqual(comparison["token_exact_cache_reasoning_examples"][0]["cell_id"], cell_id)

    def test_classifies_multi_response_scope_without_replacing_either_value(self):
        cell_id = "kh-gpt__model__low__task__r1"
        comparison = _metadata_comparison(
            [{
                "public_cell_id": cell_id,
                "harness": "kh-gpt",
                "provider_response_count": 3,
                "usage": {
                    "input_tokens": 100,
                    "cached_input_tokens": 40,
                    "output_tokens": 10,
                    "reasoning_tokens": 2,
                },
            }],
            {cell_id: {"tokens": 500, "wall_s": 10}},
        )
        self.assertEqual(comparison["token_mismatch_classes"], {"multi_request_aggregation": 1})
        self.assertEqual(comparison["token_genuine_data_errors"], 0)
        self.assertEqual(comparison["token_mismatches"][0]["published_metadata_tokens"], 500)
        self.assertEqual(comparison["token_mismatches"][0]["recomputed_input_plus_cached_plus_output"], 150)
        self.assertEqual(comparison["token_mismatches"][0]["provider_response_count"], 3)

    def test_classifies_reasoning_and_cache_formula_differences(self):
        reasoning_id = "codex__model__low__task__reasoning"
        cached_id = "codex__model__low__task__cached"
        rows = [
            {
                "public_cell_id": reasoning_id,
                "harness": "codex",
                "provider_response_count": 1,
                "usage": {
                    "input_tokens": 10,
                    "cached_input_tokens": 20,
                    "output_tokens": 5,
                    "reasoning_tokens": 2,
                },
            },
            {
                "public_cell_id": cached_id,
                "harness": "codex",
                "provider_response_count": 1,
                "usage": {
                    "input_tokens": 10,
                    "cached_input_tokens": 20,
                    "output_tokens": 5,
                    "reasoning_tokens": 2,
                },
            },
        ]
        comparison = _metadata_comparison(
            rows,
            {
                reasoning_id: {"tokens": 37, "wall_s": 10},
                cached_id: {"tokens": 15, "wall_s": 10},
            },
        )
        self.assertEqual(comparison["token_mismatch_classes"], {
            "cached_input_treatment": 1,
            "reasoning_counted_twice": 1,
        })

    def test_reports_public_rows_missing_from_mined_source(self):
        raw = {
            "public_cell_id": "codex__model__low__task__r1",
            "arm": "control",
            "official_grade": {"classification": "pass"},
        }
        public = {
            raw["public_cell_id"]: {"cell_id": raw["public_cell_id"], "arm": "control", "outcome": "pass"},
            "codex__model__low__task__r2": {"cell_id": "codex__model__low__task__r2", "arm": "control", "outcome": "fail"},
        }
        metadata = {
            raw["public_cell_id"]: {"experiment": "r1-task"},
            "codex__model__low__task__r2": {"experiment": "r1-task"},
        }
        comparison = _public_comparison("r1", [raw], public, metadata, {"r1"})
        self.assertEqual(comparison["public_export_rows_in_round"], 2)
        self.assertEqual(comparison["paired_public_cell_ids"], 1)
        self.assertEqual(comparison["public_only_rows_missing_from_mined"], 1)
        self.assertEqual(comparison["public_only_cells"][0]["cell_id"], "codex__model__low__task__r2")
        self.assertEqual(comparison["aggregate_mismatches"][0]["published"], 1)

    def test_round_section_links_raw_records_and_recomputation(self):
        data = {
            "raw_source": {
                "cells": 1,
                "outcomes": {"pass": 1},
                "pass_count": 1,
                "pass_rate": 1,
                "pass_rate_denominator": 1,
                "published_export_cells": 1,
            },
            "published_export_comparison": {
                "paired_public_cell_ids": 1,
                "outcome_matches": 1,
                "public_only_rows_missing_from_mined": 0,
                "public_export_rows_in_round": 1,
                "arm_mismatches": [],
                "outcome_mismatches": [],
            },
            "cell_metadata_comparison": {
                "token_cells_compared": 0,
                "token_cells_equal": 0,
                "token_cells_different": 0,
            },
            "published_headline_comparison": None,
        }
        section = _page_text("r1", data)
        self.assertIn("[`recomputed.json`](recomputed.json)", section)
        self.assertIn("[mined cell records](../../data/mined/r1.jsonl.gz)", section)

    def test_round_page_lists_published_and_manifest_token_values(self):
        data = {
            "raw_source": {
                "cells": 1,
                "outcomes": {"pass": 1},
                "pass_count": 1,
                "pass_rate": 1,
                "pass_rate_denominator": 1,
                "published_export_cells": 1,
            },
            "published_export_comparison": {
                "paired_public_cell_ids": 1,
                "outcome_matches": 1,
                "public_only_rows_missing_from_mined": 0,
                "public_export_rows_in_round": 1,
                "arm_mismatches": [],
                "outcome_mismatches": [],
            },
            "cell_metadata_comparison": {
                "token_cells_compared": 1,
                "token_cells_equal": 0,
                "token_cells_different": 1,
                "token_genuine_data_errors": 0,
                "token_mismatch_classes": {"multi_request_aggregation": 1},
                "token_mismatches": [{
                    "cell_id": "kh-gpt__model__low__task__r1",
                    "published_metadata_tokens": 500,
                    "recomputed_input_plus_cached_plus_output": 150,
                    "provider_response_count": 3,
                    "classification": "multi_request_aggregation",
                }],
            },
            "published_headline_comparison": None,
        }
        section = _page_text("r1", data)
        self.assertIn("`kh-gpt__model__low__task__r1`", section)
        self.assertIn("published `500`, manifest `150`", section)


if __name__ == "__main__":
    unittest.main()
