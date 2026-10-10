"""Focused tests for historical labels and the new-round strict cutoff."""

import json
import contextlib
import io
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_release import (
    BADGE_BY_STATUS,
    declared_missing_errors,
    main as release_main,
    read_field,
    render_missing_section,
    resolve_status,
    round_date,
    validate_historical_inventory,
)


class ReleasePolicyTest(unittest.TestCase):
    def test_every_historical_round_has_publication_metadata(self):
        errors, historical = validate_historical_inventory()
        self.assertEqual(errors, [])
        self.assertEqual(len(historical), 179)

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

    def check_declaration(self, status, fields, counts):
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            root = Path(directory)
            round_dir = root / "rounds" / "sample"
            round_dir.mkdir(parents=True)
            declaration = {"fields": fields}
            (round_dir / "MISSING-DECLARED.json").write_text(json.dumps(declaration))
            (round_dir / "README.md").write_text(
                "## What's missing and why\n\n" + render_missing_section(fields, counts) + "\n"
            )
            return declared_missing_errors(
                "sample", status, {"missing": sum(counts.values()), "missing_fields": counts}, root
            )

    def write_release_root(
        self,
        root,
        *,
        inventory_status,
        readme_status,
        badge_status,
        date="2026-10-10",
        section="",
        extra_badges=(),
    ):
        round_id = "sample"
        round_dir = root / "rounds" / round_id
        (round_dir).mkdir(parents=True, exist_ok=True)
        reason = "NONE" if inventory_status == "VALID" else "TEST_REASON"
        badge = f"{BADGE_BY_STATUS[badge_status]}; KEPT FOR AUDIT"
        readme = [
            f"Round date: {date}",
            f"Publication badge: {badge}",
            f"Why not VALID: {reason}",
            "Recomputation status: FULLY RECOMPUTABLE",
            f"STATUS: **{readme_status}**",
        ]
        readme.extend(f"Publication badge: {extra_badge}" for extra_badge in extra_badges)
        if inventory_status == "PILOT":
            readme.extend(["", "## Status", "", "**PILOT**"])
        if section:
            readme.extend(["", "## What's missing and why", "", section])
        (round_dir / "README.md").write_text("\n".join(readme) + "\n")
        (root / "rounds" / "STATUS.md").write_text(
            f"# Status\n\n## Rounds\n\n{round_id} | {inventory_status} | {reason}\n"
        )
        (root / "reproduce").mkdir(parents=True, exist_ok=True)
        (root / "reproduce" / "release-rounds.json").write_text(
            json.dumps({"strict_from_date": "2026-10-09"})
        )
        (root / "results").mkdir(parents=True, exist_ok=True)
        (root / "results" / "publication-blockers.json").write_text(
            json.dumps({"publication_status": "ready", "blockers": [{"id": "gate", "status": "resolved"}]})
        )
        repo_validator = root / "reproduce" / "validate_repo.py"
        repo_validator.write_text("print('repository privacy and hidden-content gates pass')\n")
        return round_id, round_dir, repo_validator

    def test_valid_round_with_missing_field_fails(self):
        errors, _ = self.check_declaration("VALID", {}, {"usage.tokens": 1})
        self.assertTrue(any("VALID but has 1 missing" in error for error in errors))

    def test_descriptive_round_with_all_fields_declared_passes(self):
        fields = {"usage.tokens": {"reason_code": "m40", "note": "The counter was not retained."}}
        for status in ("DESCRIPTIVE", "INVALID"):
            with self.subTest(status=status):
                errors, count = self.check_declaration(status, fields, {"usage.tokens": 2})
                self.assertEqual(errors, [])
                self.assertEqual(count, 2)

    def test_descriptive_round_with_undeclared_field_fails(self):
        fields = {"usage.tokens": {"reason_code": "m40", "note": "The counter was not retained."}}
        errors, _ = self.check_declaration("DESCRIPTIVE", fields, {"usage.tokens": 1, "usage.wall": 1})
        self.assertTrue(any("undeclared missing field usage.wall" in error for error in errors))

    def test_bad_missing_reason_code_fails(self):
        fields = {"usage.tokens": {"reason_code": "m999", "note": "The counter was not retained."}}
        errors, _ = self.check_declaration("DESCRIPTIVE", fields, {"usage.tokens": 1})
        self.assertTrue(any("unknown reason code" in error for error in errors))

    def test_status_sources_must_agree_and_any_valid_claim_is_strict(self):
        cases = [
            ("VALID", "DESCRIPTIVE", "VALID", "inventory/README mismatch"),
            ("DESCRIPTIVE", "DESCRIPTIVE", "VALID", "inventory/badge mismatch"),
            ("DESCRIPTIVE", "VALID", "DESCRIPTIVE", "README/badge mismatch"),
        ]
        from tempfile import TemporaryDirectory

        for inventory_status, readme_status, badge_status, label in cases:
            with self.subTest(label=label), TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_release_root(
                    root,
                    inventory_status=inventory_status,
                    readme_status=readme_status,
                    badge_status=badge_status,
                )
                errors, effective = resolve_status("sample", inventory_status, root)
                self.assertTrue(errors)
                self.assertEqual(effective, "VALID")

    def test_ambiguous_readme_or_badge_with_valid_claim_still_selects_strict(self):
        from tempfile import TemporaryDirectory

        for conflicting_source in ("README", "badge"):
            with self.subTest(source=conflicting_source), TemporaryDirectory() as directory:
                root = Path(directory)
                _, round_dir, _ = self.write_release_root(
                    root,
                    inventory_status="DESCRIPTIVE",
                    readme_status="DESCRIPTIVE",
                    badge_status="DESCRIPTIVE",
                )
                page = round_dir / "README.md"
                if conflicting_source == "README":
                    page.write_text(page.read_text() + "STATUS: **VALID**\n")
                else:
                    content = page.read_text().replace(
                        "Publication badge: DESCRIPTIVE; KEPT FOR AUDIT",
                        "Publication badge: VALID; DESCRIPTIVE; KEPT FOR AUDIT",
                    )
                    page.write_text(content)
                errors, effective = resolve_status("sample", "DESCRIPTIVE", root)
                self.assertTrue(errors)
                self.assertEqual(effective, "VALID")

    def test_conflicting_publication_badge_lines_fail_release(self):
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_release_root(
                root,
                inventory_status="DESCRIPTIVE",
                readme_status="DESCRIPTIVE",
                badge_status="DESCRIPTIVE",
                extra_badges=("VALID; KEPT FOR AUDIT",),
            )
            report = {
                "errors": [],
                "missing": 0,
                "missing_fields": {},
                "strict_release_eligible": True,
                "protocol_deviations": [],
            }
            output = io.StringIO()
            with contextlib.redirect_stdout(output), self.assertRaises(SystemExit):
                release_main(root, records_override=[{}], validate_override=lambda *_args, **_kwargs: report)
            self.assertIn("RELEASE GATE: BLOCKED", output.getvalue())
            self.assertIn("conflicting Publication badge lines", output.getvalue())

    def test_identical_publication_badge_lines_pass_release(self):
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            root = Path(directory)
            repeated = "DESCRIPTIVE; KEPT FOR AUDIT"
            self.write_release_root(
                root,
                inventory_status="DESCRIPTIVE",
                readme_status="DESCRIPTIVE",
                badge_status="DESCRIPTIVE",
                extra_badges=(repeated,),
            )
            report = {
                "errors": [],
                "missing": 0,
                "missing_fields": {},
                "strict_release_eligible": True,
                "protocol_deviations": [],
            }
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                release_main(root, records_override=[{}], validate_override=lambda *_args, **_kwargs: report)
            self.assertIn("RELEASE GATE: PASS", output.getvalue())

    def test_incomplete_and_pilot_can_use_declared_missing_route(self):
        fields = {"usage.tokens": {"reason_code": "m40", "note": "The counter was not retained."}}
        counts = {"usage.tokens": 2}
        for status in ("INCOMPLETE", "PILOT"):
            with self.subTest(status=status):
                errors, declared = self.check_declaration(status, fields, counts)
                self.assertEqual(errors, [])
                self.assertEqual(declared, 2)

    def test_missing_or_mismatched_readme_explanation_fails(self):
        from tempfile import TemporaryDirectory

        fields = {"usage.tokens": {"reason_code": "m40", "note": "The counter was not retained."}}
        counts = {"usage.tokens": 1}
        for section in ("", "- Wrong field or reason."):
            with self.subTest(section=section), TemporaryDirectory() as directory:
                root = Path(directory)
                _, round_dir, _ = self.write_release_root(
                    root,
                    inventory_status="DESCRIPTIVE",
                    readme_status="DESCRIPTIVE",
                    badge_status="DESCRIPTIVE",
                    section=section,
                )
                (round_dir / "MISSING-DECLARED.json").write_text(json.dumps({"fields": fields}))
                report = {"missing": 1, "missing_fields": counts}
                errors, _ = declared_missing_errors("sample", "DESCRIPTIVE", report, root)
                self.assertTrue(any("What's missing and why section differs" in error for error in errors))

    def test_release_cli_reports_declared_missing_count_from_temp_files(self):
        from tempfile import TemporaryDirectory

        fields = {"usage.tokens": {"reason_code": "m40", "note": "The counter was not retained."}}
        counts = {"usage.tokens": 2}
        section = render_missing_section(fields, counts)
        with TemporaryDirectory() as directory:
            root = Path(directory)
            _, round_dir, _ = self.write_release_root(
                root,
                inventory_status="DESCRIPTIVE",
                readme_status="DESCRIPTIVE",
                badge_status="DESCRIPTIVE",
                section=section,
            )
            (round_dir / "MISSING-DECLARED.json").write_text(json.dumps({"fields": fields}))
            report = {
                "errors": [],
                "missing": 2,
                "missing_fields": counts,
                "strict_release_eligible": False,
                "protocol_deviations": [],
            }
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                release_main(root, records_override=[{}], validate_override=lambda *_args, **_kwargs: report)
            self.assertIn("DECLARED MISSING STANDARD FIELDS: 2 (DESCRIPTIVE=2)", output.getvalue())

    def test_repository_privacy_hidden_content_gate_failure_still_blocks(self):
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_release_root(
                root,
                inventory_status="VALID",
                readme_status="VALID",
                badge_status="VALID",
            )
            (root / "reproduce" / "validate_repo.py").write_text(
                "print('privacy/forbidden-artifact and hidden-content gate failed')\nraise SystemExit(1)\n"
            )
            report = {
                "errors": [],
                "missing": 0,
                "missing_fields": {},
                "strict_release_eligible": True,
                "protocol_deviations": [],
            }
            output = io.StringIO()
            with contextlib.redirect_stdout(output), self.assertRaises(SystemExit):
                release_main(root, records_override=[{}], validate_override=lambda *_args, **_kwargs: report)
            self.assertIn("Repository validator failed with exit code 1", output.getvalue())

    def test_strict_from_cutoff_cannot_be_waived(self):
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_release_root(
                root,
                inventory_status="VALID",
                readme_status="VALID",
                badge_status="VALID",
            )
            config_path = root / "reproduce" / "release-rounds.json"
            config_path.write_text(json.dumps({"strict_from_date": "2026-10-10"}))
            with self.assertRaisesRegex(SystemExit, "strict_from_date must remain 2026-10-09"):
                release_main(root, records_override=[], validate_override=lambda *_args, **_kwargs: {})

    def test_new_valid_round_remains_strict_when_capture_is_missing(self):
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_release_root(
                root,
                inventory_status="VALID",
                readme_status="VALID",
                badge_status="VALID",
            )
            report = {
                "errors": [],
                "missing": 1,
                "missing_fields": {"usage.tokens": 1},
                "strict_release_eligible": False,
                "protocol_deviations": [],
            }
            output = io.StringIO()
            with contextlib.redirect_stdout(output), self.assertRaises(SystemExit):
                release_main(root, records_override=[{}], validate_override=lambda *_args, **_kwargs: report)
            self.assertIn("sample is VALID but has 1 missing Standard capture fields", output.getvalue())


if __name__ == "__main__":
    unittest.main()
