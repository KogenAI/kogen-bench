#!/usr/bin/env python3
"""Read-only checks for the public L1 control ledger and its count claims."""

import csv
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROUND = Path(__file__).resolve().parents[1]
DATA = ROUND / "data" / "controls.csv"


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")


with DATA.open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))

require(rows, "controls.csv is empty")
ids = [row["control_cell_id"] for row in rows]
require(len(ids) == len(set(ids)), "duplicate control cell ID")

allowed_kinds = {"reference", "mutant", "alternative", "noop", "skeleton-frontend"}
allowed_status = {"VALID", "WITHDRAWN"}
allowed_cohorts = {"staged", "admission", "replacement", "l1-eu"}
for row in rows:
    require(row["control_kind"] in allowed_kinds, f"invalid control kind for {row['control_cell_id']}")
    require(row["status"] in allowed_status, f"invalid status for {row['control_cell_id']}")
    require(bool(re.fullmatch(r"[0-9a-f]{40}", row["task_base_commit"])), f"invalid task base SHA for {row['control_cell_id']}")
    if row["status"] == "VALID":
        require(row["outcome"] in {"pass", "fail"}, f"invalid graded outcome for {row['control_cell_id']}")
        require(bool(re.fullmatch(r"[0-9a-f]{64}", row["grader_sha256"])), f"invalid grader SHA for {row['control_cell_id']}")
        require(row["phase"] in {"build", "test"}, f"invalid phase for {row['control_cell_id']}")
        require(row["grade_window_timestamp"].endswith("Z"), f"missing grade-window timestamp for {row['control_cell_id']}")
        datetime.fromisoformat(row["grade_window_timestamp"].replace("Z", "+00:00"))
        require(row["cohort"] in allowed_cohorts, f"invalid cohort for {row['control_cell_id']}")
    else:
        require(row["outcome"] == "not_graded", f"withdrawn control has a grade outcome: {row['control_cell_id']}")
        require(row["cohort"] == "staged", f"withdrawn control is not marked staged: {row['control_cell_id']}")
        require(bool(row["withdrawal_reason"]), f"withdrawal reason missing for {row['control_cell_id']}")

l1_eu = [row for row in rows if row["cohort"] == "l1-eu"]
original_rows = [row for row in rows if row["cohort"] != "l1-eu"]
graded = [row for row in original_rows if row["status"] == "VALID"]
staged = [row for row in original_rows if row["cohort"] == "staged"]
staged_graded = [row for row in staged if row["status"] == "VALID"]
withdrawn = [row for row in staged if row["status"] == "WITHDRAWN"]
replacements = [row for row in original_rows if row["cohort"] == "replacement"]
admission = [row for row in original_rows if row["cohort"] == "admission"]
admitted_variants = sorted({row["variant"] for row in staged_graded})
staged_mutants = [row for row in staged_graded if row["control_kind"] == "mutant"]
mutants = staged_mutants + [row for row in replacements if row["control_kind"] == "mutant"]
alternatives = [row for row in staged_graded if row["control_kind"] == "alternative"]
mutant_causes = Counter(row["cause_class"] for row in mutants)
admission_kinds = Counter(row["control_kind"] for row in admission)

require(len(original_rows) == 37, "original ledger must contain 34 grade rows and 3 withdrawal audit rows")
require(len(rows) == 47, "combined ledger must contain 47 rows including L1-EU")
require(len(graded) == 34, "original L1 grade-row count mismatch")
require(len(staged) == 24, "staged-control count mismatch")
require(len(staged_graded) == 21, "graded staged-control count mismatch")
require(len(withdrawn) == 3, "withdrawn staged-control count mismatch")
require(len(replacements) == 2, "replacement-control count mismatch")
require(all(row["status"] == "VALID" for row in replacements), "replacement controls must be officially graded")
require(all(row["control_kind"] == "mutant" for row in replacements), "replacement controls must be mutants")
require(all(row["phase"] == "test" and row["outcome"] == "fail" for row in replacements), "replacement grades must be behavioral test failures")
require(all(row["tests_passed/total"] == "16/18" and row["cause_class"] == "behavioral_failure" for row in replacements), "replacement grade details mismatch")
require({row["control_cell_id"] for row in replacements} == {
    "codex__gpt-6-luna__max__default__r70-4-go-fe2__r719",
    "codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r720",
}, "replacement mutant IDs mismatch")
require(len(admitted_variants) == 7, "admitted-variant count mismatch")
require(len(staged_mutants) == 14, "original staged mutant count mismatch")
require(sum(row["cause_class"] == "behavioral_failure" for row in staged_mutants) == 12, "original behavioral mutant count mismatch")
require(sum(row["cause_class"] == "behavioral_failure" for row in replacements) == 2, "replacement behavioral mutant count mismatch")
require(mutant_causes == Counter({"behavioral_failure": 14, "build_failure": 2}), "mutant cause counts mismatch")
require(len(alternatives) == 7 and all(row["outcome"] == "pass" for row in alternatives), "each admitted variant must have one passing alternative")
require(len(admission) == 11, "admission-control grade count mismatch")
require(admission_kinds == Counter({"reference": 5, "noop": 5, "skeleton-frontend": 1}), "admission-control kind counts mismatch")
require(
    all(row["outcome"] == "pass" for row in admission if row["control_kind"] in {"reference", "skeleton-frontend"})
    and all(row["outcome"] == "fail" for row in admission if row["control_kind"] == "noop"),
    "admission-control outcomes mismatch",
)

# Keep the L1-EU extension separate from the original seven-variant headline.
require(len(l1_eu) == 10, "L1-EU addendum row count mismatch")
require(Counter(row["control_kind"] for row in l1_eu) == Counter({"reference": 2, "noop": 2, "mutant": 4, "alternative": 2}), "L1-EU kind counts mismatch")
l1_eu_expected = {
    "admission-fixed-r70-6-elixir-reference-r1": ("r70-6-elixir", "reference", "pass", "24/24", "none", "133e688d87f0392a00c164d34455cde04def28ad", "2026-10-07T20:37:00Z", "", ""),
    "admission-fixed-r70-6-elixir-noop-r1": ("r70-6-elixir", "noop", "fail", "0/24", "behavioral_failure", "133e688d87f0392a00c164d34455cde04def28ad", "2026-10-07T20:38:16Z", "", ""),
    "admission-fixed-r70-6-elixir-reference-r2": ("r70-6-elixir", "reference", "pass", "24/24", "none", "133e688d87f0392a00c164d34455cde04def28ad", "2026-10-07T20:39:32Z", "", ""),
    "admission-fixed-r70-6-elixir-noop-r2": ("r70-6-elixir", "noop", "fail", "0/24", "behavioral_failure", "133e688d87f0392a00c164d34455cde04def28ad", "2026-10-07T20:40:48Z", "", ""),
    "codex__gpt-6-luna__max__default__r70-6-elixir__r730": ("r70-6-elixir", "mutant", "pass", "24/24", "none", "133e688d87f0392a00c164d34455cde04def28ad", "2026-10-07T20:42:58Z", "a7098c0191e08eedc35e062bd7122c9e3c0b157856e7590cd6c9dc301ecf4981", "Event IDs longer than the specified limit are accepted."),
    "codex__gpt-6-luna__max__default__r70-6-elixir__r731": ("r70-6-elixir", "mutant", "pass", "24/24", "none", "133e688d87f0392a00c164d34455cde04def28ad", "2026-10-07T20:44:13Z", "f0aadd52c1dc42f068476927d2201912fa7aaa2f260ef917f81f92848313e218", "Job slugs longer than the specified limit are accepted."),
    "codex__gpt-6-luna__max__default__r70-6-elixir__r732": ("r70-6-elixir", "alternative", "pass", "24/24", "none", "133e688d87f0392a00c164d34455cde04def28ad", "2026-10-07T20:45:28Z", "cba3ae7bca030c3741416ba022b2a20dac88a607ec576d7c2f3d4c11c687a4e3", "Behavior-equivalent alternative implementation."),
    "codex__gpt-6-luna__max__default__r70-7-elixir__r733": ("r70-7-elixir", "mutant", "fail", "23/24", "behavioral_failure", "c1899948806e61033520431b9e4d8749c72074d1", "2026-10-07T20:46:43Z", "b0f3e4fd6d189c556a521a5e730dc77d95e3c8c8234af6c1efa652caa127c818", "Scale parsing accepts values above the specified ceiling."),
    "codex__gpt-6-luna__max__default__r70-7-elixir__r734": ("r70-7-elixir", "mutant", "fail", "23/24", "behavioral_failure", "c1899948806e61033520431b9e4d8749c72074d1", "2026-10-07T20:48:11Z", "a72692f3eb6686acd0ce1b87bba70d894de6f6b9fe024e320f5bd59ea08f021b", "Status IDs may begin with uppercase letters."),
    "codex__gpt-6-luna__max__default__r70-7-elixir__r735": ("r70-7-elixir", "alternative", "pass", "24/24", "none", "c1899948806e61033520431b9e4d8749c72074d1", "2026-10-07T20:49:39Z", "0cc7c063795b669918bb4579231c6ae7421609166a81dcf3bec926f91aacc40d", "Behavior-equivalent alternative implementation."),
}
require({row["control_cell_id"] for row in l1_eu} == set(l1_eu_expected), "L1-EU cell IDs mismatch")
for row in l1_eu:
    variant, kind, outcome, tests, cause, commit, window, patch_sha, behavior = l1_eu_expected[row["control_cell_id"]]
    require((row["variant"], row["task"], row["stack"], row["host"]) == (variant, variant, "elixir", "kogen-bench-eu"), f"L1-EU task metadata mismatch for {row['control_cell_id']}")
    require((row["control_kind"], row["phase"], row["outcome"], row["tests_passed/total"], row["cause_class"]) == (kind, "test", outcome, tests, cause), f"L1-EU grade mismatch for {row['control_cell_id']}")
    require((row["task_base_commit"], row["grader_sha256"], row["grade_window_timestamp"], row["status"], row["cohort"]) == (commit, "0e6f8aa06dce3b42813e326a85c2248115bf95bc127449f8fb99e3929bec0843", window, "VALID", "l1-eu"), f"L1-EU provenance mismatch for {row['control_cell_id']}")
    require((row["patch_sha256"], row["behavior_class"]) == (patch_sha, behavior), f"L1-EU public patch metadata mismatch for {row['control_cell_id']}")
    require(not row["withdrawal_reason"], f"L1-EU grade has a withdrawal reason: {row['control_cell_id']}")
require(Counter((row["control_kind"], row["outcome"]) for row in l1_eu if row["variant"] == "r70-6-elixir") == Counter({("reference", "pass"): 2, ("noop", "fail"): 2, ("mutant", "pass"): 2, ("alternative", "pass"): 1}), "task 6 L1-EU outcomes mismatch")
require(Counter((row["control_kind"], row["outcome"]) for row in l1_eu if row["variant"] == "r70-7-elixir") == Counter({("mutant", "fail"): 2, ("alternative", "pass"): 1}), "task 7 L1-EU outcomes mismatch")

staged_by_variant = defaultdict(list)
for row in staged_graded:
    staged_by_variant[row["variant"]].append(row)
all_by_variant = defaultdict(list)
for row in staged_graded + replacements:
    all_by_variant[row["variant"]].append(row)
for variant in admitted_variants:
    entries = staged_by_variant[variant]
    require(Counter(row["control_kind"] for row in entries) == Counter({"mutant": 2, "alternative": 1}), f"staged control mix mismatch for {variant}")
    behavioral = [row for row in all_by_variant[variant] if row["control_kind"] == "mutant" and row["cause_class"] == "behavioral_failure"]
    require(len(behavioral) == 2, f"each admitted variant must have two behavioral mutants: {variant}")
    require(all(row["outcome"] == "fail" for row in behavioral), f"behavioral mutant outcome mismatch for {variant}")
    require(sum(row["outcome"] == "pass" for row in entries if row["control_kind"] == "alternative") == 1, f"alternative outcome mismatch for {variant}")
    if any(row["cause_class"] == "build_failure" for row in entries):
        require(Counter(row["cause_class"] for row in entries if row["control_kind"] == "mutant") == Counter({"behavioral_failure": 1, "build_failure": 1}), f"behavioral-mutant evidence mismatch for {variant}")
        require(sum(row["cohort"] == "replacement" and row["control_kind"] == "mutant" for row in all_by_variant[variant]) == 1, f"build rejection lacks one replacement for {variant}")

build_failure_ids = {
    row["control_cell_id"] for row in mutants if row["cause_class"] == "build_failure"
}
require(build_failure_ids == {
    "codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r711",
    "codex__gpt-6-luna__max__default__r70-4-go-fe2__r714",
}, "task-4 build-failure mutant IDs mismatch")

manifest = (ROUND / "CONTROL-MANIFEST.md").read_text(encoding="utf-8")
manifest_ids = set(re.findall(r"`(codex__[^`]+)`", manifest))
control_ids = {row["control_cell_id"] for row in staged + replacements}
require(manifest_ids == control_ids, "control manifest IDs do not match the staged and replacement ledger records")

readme = (ROUND / "README.md").read_text(encoding="utf-8")
results = (ROUND / "RESULTS.md").read_text(encoding="utf-8")
decision = (ROUND / "DECISION-RULE.md").read_text(encoding="utf-8")
for document, name in ((readme, "README.md"), (results, "RESULTS.md")):
    for phrase in (
        "24 original staged / 21 graded / 3 withdrawn",
        "2 replacement mutants graded",
        "14 behavioral mutant detections across the 7 admitted variants (two per variant) + 7 passing alternatives",
    ):
        require(phrase in document, f"{name} is missing the reproduced claim: {phrase}")
    require("34 graded control rows" in document, f"{name} is missing the 34-row ledger count")
for control_id in sorted(build_failure_ids):
    require(control_id in results, f"RESULTS.md is missing build-failure mutant ID {control_id}")
require("build rejection" in results.lower() and "superseded" in results.lower(), "RESULTS.md must label original build failures as superseded build rejections")
require("NOT-RUN because no L1 control has an official grade" not in decision, "DECISION-RULE.md contains the stale NOT-RUN claim")

expected_rows = {}
for variant, entries in all_by_variant.items():
    mutant_rows = sorted(
        (row for row in entries if row["control_kind"] == "mutant" and row["cause_class"] == "behavioral_failure"),
        key=lambda row: int(row["control_cell_id"].rsplit("r", 1)[1]),
    )
    alternative = next(row for row in entries if row["control_kind"] == "alternative")
    def label(row, variant=variant):
        if row["cohort"] == "replacement":
            rejected = next(
                old for old in staged_by_variant[variant]
                if old["control_kind"] == "mutant" and old["cause_class"] == "build_failure"
            )
            return f"behavioral failure (replacement r{row['control_cell_id'].rsplit('r', 1)[1]}; supersedes build rejection r{rejected['control_cell_id'].rsplit('r', 1)[1]})"
        return "behavioral failure"
    expected_rows[variant] = (
        mutant_rows[0]["host"], label(mutant_rows[0]), label(mutant_rows[1]), alternative["outcome"]
    )

table_rows = {}
for line in results.splitlines():
    if not line.startswith("| ") or "---" in line:
        continue
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    if len(cells) == 5 and cells[0] in expected_rows:
        table_rows[cells[0]] = tuple(cells[1:])
require(table_rows == expected_rows, "per-variant RESULTS.md outcome table does not match controls.csv")
for row in withdrawn:
    require(row["control_cell_id"] in results, f"RESULTS.md is missing withdrawn control {row['control_cell_id']}")
require("5 references and 1 skeleton-frontend control passed; 5 no-ops failed" in results, "RESULTS.md admission-outcome summary does not match controls.csv")

print(
    "PASS: original 37-row L1 ledger; 24 original staged (21 graded, 3 withdrawn) + 2 graded replacements; "
    "7 admitted variants; original headline remains 14 behavioral mutant failures + 7 alternatives pass; "
    "11 original admission grades. Separate L1-EU cohort: 10 grades (4 task-6 admission, 6 X-controls); "
    "47 total CSV rows."
)
