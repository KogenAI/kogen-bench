import gzip
import json
import tempfile
import unittest
from pathlib import Path

from mine_probe import _grade_fields, _patch_archive_exclusion_reasons, mine, read_json, read_jsonl, round_for_cell, sanitize


class MineProbeTests(unittest.TestCase):
    def test_grade_and_manifest_receipts_are_loaded_through_safe_rows(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            grades = root / 'grades.jsonl'
            grades.write_text(json.dumps({
                'cell_id': 'synthetic', 'outcome': 'pass', 'test_names': ['hidden-name'],
            }) + '\n', encoding='utf-8')
            manifest = root / 'manifest.json'
            manifest.write_text(json.dumps({
                'cell_id': 'synthetic', 'grade': {'pass': True, 'stderr': 'hidden text'},
            }), encoding='utf-8')
            grade_rows = read_jsonl(grades)
            manifest_row = read_json(manifest)
            self.assertEqual(grade_rows[0]['cell_id'], 'synthetic')
            self.assertNotEqual(grade_rows[0]['test_names'], ['hidden-name'])
            self.assertEqual(manifest_row['cell_id'], 'synthetic')
            self.assertNotEqual(manifest_row['grade']['stderr'], 'hidden text')

    def test_sanitize_removes_hidden_suite_fields_recursively(self):
        row = sanitize({
            "result": "fail",
            "failing": ["secret-test-name"],
            "nested": {"tests_passed": 2, "tail": "hidden grader text"},
        })
        self.assertEqual(row["result"], "fail")
        self.assertNotEqual(row["failing"], ["secret-test-name"])
        self.assertNotEqual(row["nested"]["tail"], "hidden grader text")
        self.assertEqual(row["nested"]["tests_passed"], 2)

    def test_round_aliases(self):
        self.assertEqual(round_for_cell("hc-ladder__model__max", "hc2-v2-task-arm-r1", {"hc-2"}), "hc-2")
        self.assertEqual(round_for_cell("codex__model__high__task", "r58x-studio-task-arm-r1", set()), "r58x-studio")
        self.assertEqual(round_for_cell("kh__model__low__task__r1-arm-r56-studio", "", {"r56"}), "r56")
        registered = {"r1", "r16", "r70", "r70-rve-ext", "claim-b-rerun-1"}
        self.assertEqual(round_for_cell("rec-lever-r16-us-task-r1", "", registered), "r16")
        self.assertEqual(round_for_cell("r70-rve-ext-cell-r1", "", registered), "r70-rve-ext")
        self.assertEqual(round_for_cell("claim-b-rerun-1-cell", "", registered), "claim-b-rerun-1")

    def test_official_grade_uses_outcome_precedence_and_keeps_raw_result(self):
        grade = _grade_fields({"outcome": "fail", "result": "invalid", "tests_ran": True})
        self.assertEqual(grade["classification"], "fail")
        self.assertEqual(grade["pass_fail"], "fail")
        self.assertEqual(grade["result"], "invalid")

    def test_patch_archive_filter_excludes_credential_markers_and_values(self):
        self.assertIn("bearer_marker", _patch_archive_exclusion_reasons(b"Authorization: Bearer " + b"$TOKEN"))
        self.assertIn("jwt_marker", _patch_archive_exclusion_reasons(b"eyJ" + b"header.payload.signature"))
        self.assertIn("refresh_token_marker", _patch_archive_exclusion_reasons(b"refresh_token" + b"=value"))
        self.assertIn("credential_value_field", _patch_archive_exclusion_reasons(b"password: \"not-a-real-value\""))
        self.assertEqual(_patch_archive_exclusion_reasons(b"ordinary patch content"), [])

    def test_mine_writes_curated_record_and_hash_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            results = root / "results"
            cell = results / "r1-us-task-arm-r1"
            (cell / "attempt-1").mkdir(parents=True)
            (cell / "attempt-1/patch.diff").write_text("diff --git a/a b/a\n", encoding="utf-8")
            manifest = {
                "cell_id": "codex__gpt-6-luna__low__default__task__r1",
                "experiment": "r1-us-task-arm-r1",
                "harness": "codex",
                "requested": {"model": "gpt-6-luna", "effort": "low", "task": "task", "rep": 1},
                "status": "ok",
                "wall_s": 12.5,
                "usage": {"input": 100, "cached_input": 20, "output": 5, "reasoning": 2},
                "extra": {"response_ids": ["response-one", "response-two"]},
                "prompt_sha256": "a" * 64,
                "cli_version": "codex-cli 0.160.0",
                "private_text": "Bearer should never be exported",
            }
            (cell / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            grade_id = manifest["cell_id"] + "-arm-r1-studio"
            grades = root / "grades.final.jsonl"
            grades.write_text(json.dumps({
                "cell_id": grade_id,
                "arm": "arm",
                "task": "task",
                "rep": "1",
                "result": "pass",
                "tests_ran": True,
                "tests_total": 4,
                "failing": ["must-not-appear"],
            }) + "\n", encoding="utf-8")
            metadata = root / "cell-metadata.json"
            metadata.write_text(json.dumps({grade_id: {"experiment": manifest["experiment"]}}), encoding="utf-8")
            public_grades = root / "public-grades.jsonl"
            public_grades.write_text(json.dumps({"cell_id": grade_id}) + "\n", encoding="utf-8")
            round_index = root / "rounds.json"
            round_index.write_text(json.dumps(["r1"]), encoding="utf-8")
            output = root / "data/mined"

            summary = mine(
                results,
                grades,
                metadata,
                public_grades,
                round_index,
                output,
                include_patches=False,
            )

            with gzip.open(output / "r1.jsonl.gz", "rt", encoding="utf-8") as handle:
                record = json.loads(handle.readline())
            self.assertEqual(record["official_grade"]["pass_fail"], "pass")
            self.assertEqual(record["official_grade"]["test_counts"], {"tests_total": 4})
            self.assertEqual(record["usage"]["cached_input_tokens"], 20)
            self.assertEqual(record["provider_response_count"], 2)
            self.assertEqual(record["wall_s"], 12.5)
            self.assertTrue(record["published_export"])
            self.assertNotIn("private_text", record)
            self.assertNotIn("failing", record["official_grade"])
            self.assertNotIn("response_ids", record)
            self.assertNotIn("response-one", json.dumps(record))
            self.assertNotIn("Bearer ", json.dumps(record))
            self.assertEqual(summary["source_cell_directories"], 1)
            self.assertTrue((output / "MANIFEST.sha256").is_file())
            self.assertTrue((output / "MANIFEST.sha256").is_file())

    def test_mine_retains_manifest_grade_and_oversized_patch_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            results = root / "results"
            cell = results / "host-cell"
            cell.mkdir(parents=True)
            patch_sha = "b" * 64
            manifest = {
                "cell_id": "codex__gpt-6-luna__low__default__task__r1",
                "experiment": "r1-host-task-r1",
                "requested": {"task": "task", "rep": 1},
                "status": "ok",
                "grade": {"pass": True, "tests_passed": 3},
                "_source_host": "kogen-bench-us",
                "_source_round_override": "r1",
                "_source_patch_metadata": [{
                    "attempt": 1,
                    "sha256": patch_sha,
                    "size_bytes": 50_000_001,
                    "archive_exclusion_reasons": ["over_50mb"],
                }],
            }
            (cell / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            grades = root / "grades.jsonl"
            grades.write_text("", encoding="utf-8")
            metadata = root / "metadata.json"
            metadata.write_text("{}\n", encoding="utf-8")
            public = root / "public.jsonl"
            public.write_text("", encoding="utf-8")
            round_index = root / "rounds.json"
            round_index.write_text('["r1"]\n', encoding="utf-8")
            output = root / "data/mined"

            mine(results, grades, metadata, public, round_index, output, include_patches=False)

            with gzip.open(output / "r1.jsonl.gz", "rt", encoding="utf-8") as handle:
                record = json.loads(handle.readline())
            self.assertEqual(record["official_grade"]["pass_fail"], "pass")
            self.assertEqual(record["grade_join"], "manifest")
            self.assertEqual(record["manifest_grade"]["pass_fail"], "pass")
            self.assertEqual(record["source_host"], "kogen-bench-us")
            self.assertEqual(record["patches"], [{
                "attempt": 1,
                "sha256": patch_sha,
                "size_bytes": 50_000_001,
                "archive_member": None,
                "archive_exclusion_reasons": ["over_50mb"],
            }])

    def test_mine_joins_a_unique_grade_by_host_experiment_label(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            results = root / "results"
            cell = results / "host-cell"
            cell.mkdir(parents=True)
            (cell / "manifest.json").write_text(json.dumps({
                "cell_id": "host-cell-id",
                "experiment": "retained-experiment-label",
                "requested": {"task": "task-a", "rep": 2},
                "status": "ok",
                "_source_round_override": "r1",
            }), encoding="utf-8")
            grades = root / "grades.jsonl"
            grades.write_text("\n".join(json.dumps(row) for row in [
                {
                    "cell_id": "mac-grade-id-a",
                    "experiment": "retained-experiment-label",
                    "task": "task-a",
                    "rep": "2",
                    "outcome": "pass",
                },
                {
                    "cell_id": "mac-grade-id-b",
                    "experiment": "retained-experiment-label",
                    "task": "task-b",
                    "rep": "2",
                    "outcome": "fail",
                },
            ]) + "\n", encoding="utf-8")
            metadata = root / "metadata.json"
            metadata.write_text("{}\n", encoding="utf-8")
            public = root / "public.jsonl"
            public.write_text("", encoding="utf-8")
            round_index = root / "rounds.json"
            round_index.write_text('["r1"]\n', encoding="utf-8")
            output = root / "data/mined"

            mine(results, grades, metadata, public, round_index, output, include_patches=False)

            with gzip.open(output / "r1.jsonl.gz", "rt", encoding="utf-8") as handle:
                record = json.loads(handle.readline())
            self.assertEqual(record["official_grade"]["pass_fail"], "pass")
            self.assertEqual(record["grade_join_method"], "experiment_label")
            self.assertEqual(record["grade_source_id"], "mac-grade-id-a")
            self.assertEqual(record["manifest_cell_id"], "host-cell-id")


if __name__ == "__main__":
    unittest.main()
