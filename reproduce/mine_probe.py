#!/usr/bin/env python3
"""Extract privacy-filtered cell metadata and patches from the recovered probe store.

The extractor uses only the Python standard library. Grade rows are sanitized
before any fields are selected, following the safe_rows policy used by the
source workspace. It never copies transcripts, rollouts, prompts, request logs,
grader output, or source paths. A count of provider response IDs is retained
when present so aggregate metadata can be distinguished from one manifest's
usage counters; the IDs themselves are never copied.
"""

from __future__ import annotations

import argparse
import bisect
import gzip
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROBE = Path.home() / "Areas/Kogen/benchmark-recovery-2026-10-02/probe-luna-low-20261002"
DEFAULT_RESULTS = DEFAULT_PROBE / "results"
DEFAULT_GRADES = DEFAULT_PROBE / "grades/grades.final.jsonl"
DEFAULT_METADATA = ROOT / "reproduce/inputs/cell-metadata.json"
DEFAULT_PUBLIC_GRADES = ROOT / "reproduce/inputs/grades.final.jsonl"
DEFAULT_ROUND_INDEX = ROOT / "rounds/index.json"
DEFAULT_FINDINGS = ROOT / "FINDINGS.md"
DEFAULT_OUTPUT = ROOT / "data/mined"
SAFE_ROWS_HOST = Path("/root/Areas/Kogen/bench-manager/rz1-pack/rz1-export/levers/lib/safe_rows.py")
SAFE_ROWS_USER = Path.home() / "Areas/Kogen/bench-manager/rz1-pack/rz1-export/levers/lib/safe_rows.py"
SAFE_ROWS_LOCAL = ROOT / "reproduce/safe_rows.py"

HIDDEN_KEY = re.compile(
    r"(test_names|failing|^tail$|_tail$|failure_summary|stdout|stderr|"
    r"hidden_output|test_output|failed_tests|passed_tests)",
    re.IGNORECASE,
)
REDACTED = "<hidden-suite field removed>"
SAFE_LABEL = re.compile(r"^[A-Za-z0-9_. +:/()≥−-]{1,256}$")
SAFE_ID = re.compile(r"^[A-Za-z0-9_.:+-]{1,512}$")
HEX_SHA = re.compile(r"^[0-9a-fA-F]{7,64}$")
HEX_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")
VERSION = re.compile(
    r"^(?:[A-Za-z][A-Za-z0-9_.+-]*(?:\s+[A-Za-z][A-Za-z0-9_.+-]*)*\s+)?"
    r"(?:v?\d+\.\d+(?:\.\d+)?(?:[-+][A-Za-z0-9_.-]+)?|"
    r"[0-9a-fA-F]{8,64}(?:/[0-9a-fA-F]{8,64}){0,16})$"
)
ATTEMPT_DIR = re.compile(r"(?:^|/)attempt-(\d+)(?:/|$)")
TOKEN_FIELDS = {
    "input_tokens": ("input", "input_tokens", "uncached_input", "uncached_input_tokens"),
    "cached_input_tokens": ("cached_input", "cached_input_tokens"),
    "output_tokens": ("output", "output_tokens"),
    "reasoning_tokens": ("reasoning", "reasoning_tokens"),
}
TEST_COUNT_KEYS = {
    "test_count",
    "tests_total",
    "tests_passed",
    "tests_failed",
    "total_tests",
    "passed_count",
    "failed_count",
}
BASE_HASH_KEYS = {"base_sha", "base_sha256", "base_commit", "base_revision", "base_hash"}
VERSION_KEYS = {
    "cli_version",
    "harness_version",
    "adapter_version",
    "runner_version",
    "kogen_version",
    "tool_version",
}
MAX_PATCH_FILE_BYTES = 50_000_000
MAX_PATCH_ARCHIVE_BYTES = 300_000_000
SOURCE_REPORTED_ROUNDS = {"hc-1", "hc-2", "hc-3", "hc-4", "r58x-studio"}
PATCH_CREDENTIAL_VALUE = re.compile(
    rb"(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token|refresh[_-]?token)"
    rb"\b\s*[:=]\s*(?:[\"'][^\"'\r\n]{4,}[\"']|[A-Za-z0-9_./+=-]{12,})"
)


def _patch_archive_exclusion_reasons(content: bytes) -> list[str]:
    """Keep credential-bearing or credential-shaped patches out of public bundles."""
    lowered = content.lower()
    reasons = []
    if b"bearer " in lowered:
        reasons.append("bearer_marker")
    if b"eyj" in lowered:
        reasons.append("jwt_marker")
    if b"refresh_token" in lowered:
        reasons.append("refresh_token_marker")
    if PATCH_CREDENTIAL_VALUE.search(content):
        reasons.append("credential_value_field")
    return reasons


def sanitize(obj: Any) -> Any:
    """Copy an object while removing known hidden-suite fields recursively."""
    if isinstance(obj, dict):
        return {
            key: REDACTED if HIDDEN_KEY.search(str(key)) else sanitize(value)
            for key, value in obj.items()
        }
    if isinstance(obj, list):
        return [sanitize(value) for value in obj]
    return obj


def read_json(path: Path) -> Any:
    rows = read_safe_rows(path)
    return rows[0] if rows else None


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [row for row in read_safe_rows(path) if isinstance(row, dict)]


def read_safe_rows(path: Path) -> list[Any]:
    """Read protected receipts only through the approved sanitizer CLI."""
    helper = next((candidate for candidate in (SAFE_ROWS_HOST, SAFE_ROWS_USER, SAFE_ROWS_LOCAL)
                   if candidate.is_file() and not candidate.is_symlink()), None)
    if helper is None:
        raise FileNotFoundError("the approved safe_rows.py helper is unavailable")
    result = subprocess.run(
        [sys.executable, str(helper), str(path)],
        check=True, capture_output=True, text=True, timeout=30,
    )
    rows = []
    for line in result.stdout.splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def safe_label(value: Any, *, identifier: bool = False) -> str | None:
    if not isinstance(value, str) or len(value) > (512 if identifier else 256):
        return None
    pattern = SAFE_ID if identifier else SAFE_LABEL
    if not pattern.fullmatch(value):
        return None
    lowered = value.lower()
    if any(marker in lowered for marker in ("bearer ", "eyj", "refresh_token")):
        return None
    if "@" in value or "\\" in value or re.search(r"/(?:Users|home)/", value):
        return None
    return value


def nonnegative_number(value: Any) -> int | float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if not math.isfinite(value) or value < 0:
        return None
    return value


def normalized_round_tag(cell_id: str, experiment: str = "") -> str:
    """Mirror the public round-tag rules, with aliases for the recovered pilots."""
    # These labels are round names, not model/rep suffixes.
    for text in (experiment, cell_id):
        if not isinstance(text, str):
            continue
        for round_id in ("r57-t90-studio", "r57-studio", "r58x-studio"):
            if text == round_id or text.startswith(round_id + "-"):
                return round_id
        match = re.match(r"^hc([1-4])(?:-|$)", text, re.IGNORECASE)
        if match:
            return "hc-" + match.group(1)

    if experiment in {"r70-rve-rerun", "r70-rve-ext"}:
        return experiment

    def canonical(number: str, suffix: str = "") -> str:
        suffix = suffix.lower()
        return "r" + str(int(number)) + (suffix if len(suffix) == 1 or suffix == "p2" else "")

    for text in (cell_id, experiment):
        if not text:
            continue
        match = re.match(r"^(?:rec-lever-)?(?:lr|r)(\d{1,2})([a-z]*[0-9]*)(?=[^a-zA-Z0-9]|$)", text)
        if match:
            prefix = "lr" if text.startswith("lr") or text.startswith("rec-lever-lr") else "r"
            return prefix + str(int(match.group(1))) + (
                match.group(2).lower()
                if len(match.group(2)) == 1 or match.group(2).lower() == "p2"
                else ""
            )
        match = re.search(r"-(?:lr|r)(\d{1,2})([a-z]*[0-9]*)(?=-)", text, re.IGNORECASE)
        if match:
            prefix = "lr" if match.group(0).lower().startswith("-lr") else "r"
            return prefix + str(int(match.group(1))) + (
                match.group(2).lower()
                if len(match.group(2)) == 1 or match.group(2).lower() == "p2"
                else ""
            )
    return "unmapped"


def round_for_cell(cell_id: str, experiment: str, round_ids: set[str]) -> str:
    # Preserve exact registered round names for source families whose IDs do
    # not use the numbered rN convention (for example x-ladder or e09-tidewave).
    if experiment in round_ids:
        return experiment
    # Recovered host runs may use a published round name directly. Match full
    # tokens, preferring longer names so r1 cannot capture r16 or r70-rve-ext.
    for text in (experiment, cell_id):
        if not isinstance(text, str) or not text:
            continue
        for round_id in sorted(round_ids, key=lambda value: (-len(value), value)):
            if re.search(rf"(?<![A-Za-z0-9]){re.escape(round_id)}(?![A-Za-z0-9])", text, re.IGNORECASE):
                return round_id
    result = normalized_round_tag(cell_id, experiment)
    if result in {"lr1", "lr2"}:
        result = "r" + result[-1]
    if result == "r58x":
        result = "r58x-studio"
    if result == "unmapped":
        for text in (experiment, cell_id):
            if not text:
                continue
            match = re.match(r"^(?:rec-lever-)?lr([12])(?:-|$)", text, re.IGNORECASE)
            if match:
                return "lr" + match.group(1)
            match = re.match(r"^(pilot73)(?:-|$)", text, re.IGNORECASE)
            if match:
                return "pilot73"
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", result):
        return "unmapped"
    return result


def source_round_alias(cell_id: str, experiment: str) -> str | None:
    """Retain old launcher labels while assigning their rows to the public round."""
    for text in (experiment, cell_id):
        if not text:
            continue
        if re.match(r"^(?:rec-lever-)?lr[12](?:-|$)", text, re.IGNORECASE):
            match = re.search(r"(?:^|-)lr([12])(?:-|$)", text, re.IGNORECASE)
            if match:
                return "lr" + match.group(1)
        match = re.search(r"(?:^|-)lr([12])(?:-|$)", text, re.IGNORECASE)
        if match:
            return "lr" + match.group(1)
    return None


def grade_round(row: dict[str, Any], metadata: dict[str, Any], round_ids: set[str]) -> str:
    cell_id = row.get("cell_id") or ""
    meta = metadata.get(cell_id, {}) if isinstance(metadata, dict) else {}
    experiment = meta.get("experiment", "") if isinstance(meta, dict) else ""
    return round_for_cell(str(cell_id), str(experiment or ""), round_ids)


def _ids_from_manifest(manifest: dict[str, Any], meta: dict[str, Any] | None = None) -> dict[str, Any]:
    requested = manifest.get("requested") if isinstance(manifest.get("requested"), dict) else {}
    normalized_id = manifest.get("cell_id") if isinstance(manifest.get("cell_id"), str) else ""
    parts = normalized_id.split("__")
    model = requested.get("model")
    effort = requested.get("effort")
    task = requested.get("task")
    rep = requested.get("rep")
    harness = manifest.get("harness")
    if len(parts) >= 5:
        harness = harness or parts[0]
        model = model or parts[1]
        effort = effort or parts[2]
        task = task or parts[4]
    if len(parts) >= 6:
        match = re.match(r"r(\d+)", parts[5], re.IGNORECASE)
        rep = rep if rep is not None else (match.group(1) if match else None)
    if isinstance(meta, dict):
        model = model or meta.get("model")
        harness = harness or meta.get("harness")
        if effort is None:
            # Metadata effort can be a compound display string; keep it only if it is a simple label.
            effort = meta.get("effort")
    return {
        "arm": safe_label(manifest.get("arm")),
        "task": safe_label(task),
        "rep": safe_label(str(rep)) if rep is not None else None,
        "model": safe_label(model),
        "effort": safe_label(effort),
        "harness": safe_label(harness),
    }


def _grade_fields(grade: dict[str, Any] | None) -> dict[str, Any] | None:
    if not grade:
        return None
    raw_outcome = grade.get("outcome") or grade.get("classification")
    raw_result = grade.get("result")
    if raw_outcome is None and isinstance(grade.get("pass"), bool):
        raw_outcome = "pass" if grade["pass"] else "fail"
    outcome = safe_label(raw_outcome)
    result = safe_label(raw_result)
    allowed = {
        "pass", "fail", "invalid", "grader_error", "timeout", "unknown",
        "infra", "interrupted", "pending", "restore_failed",
    }
    if outcome not in allowed:
        outcome = None
    if result not in allowed:
        result = None
    classification = outcome or result or "unknown"
    pass_fail = classification if classification in {"pass", "fail"} else None
    tests_ran = grade.get("tests_ran")
    if not isinstance(tests_ran, bool):
        tests_ran = None
    test_counts = {
        key: grade[key]
        for key in sorted(TEST_COUNT_KEYS)
        if key in grade
        and isinstance(grade[key], int)
        and not isinstance(grade[key], bool)
        and grade[key] >= 0
    }
    return {
        "outcome": outcome,
        "result": result,
        "classification": classification,
        "pass_fail": pass_fail,
        "tests_ran": tests_ran,
        "test_counts": test_counts,
    }


def _usage_fields(manifest: dict[str, Any]) -> dict[str, int | float | None]:
    usage = manifest.get("usage") if isinstance(manifest.get("usage"), dict) else {}
    result: dict[str, int | float | None] = {}
    for output_key, input_keys in TOKEN_FIELDS.items():
        value = None
        for input_key in input_keys:
            if input_key in usage:
                value = nonnegative_number(usage.get(input_key))
                break
        result[output_key] = value
    return result


def _provider_response_count(manifest: dict[str, Any]) -> int | None:
    """Keep only the number of provider responses, never their identifiers."""
    extra = manifest.get("extra") if isinstance(manifest.get("extra"), dict) else {}
    response_ids = extra.get("response_ids")
    if not isinstance(response_ids, list):
        return None
    return len(response_ids)


def _named_sha(obj: Any) -> dict[str, str]:
    found: dict[str, str] = {}

    def visit(value: Any, parent: str = "") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                key_lower = str(key).lower()
                if key_lower in BASE_HASH_KEYS:
                    candidates = [child]
                    if isinstance(child, dict):
                        candidates = [child.get(k) for k in ("sha", "hash", "commit", "revision")]
                    for candidate in candidates:
                        if isinstance(candidate, str) and HEX_SHA.fullmatch(candidate):
                            found["base_sha"] = candidate.lower()
                            break
                if isinstance(child, (dict, list)):
                    visit(child, key_lower)
        elif isinstance(value, list):
            for child in value:
                visit(child, parent)

    visit(obj)
    return found


def _versions(manifest: dict[str, Any], config: Any = None) -> dict[str, str]:
    output: dict[str, str] = {}

    def visit(obj: Any) -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                key_lower = str(key).lower()
                if key_lower in VERSION_KEYS and isinstance(value, str) and VERSION.fullmatch(value.strip()):
                    normalized = value.strip()
                    name = key_lower.removesuffix("_version")
                    output[name] = normalized
                elif key_lower.endswith("_sha256") and isinstance(value, str) and HEX_SHA256.fullmatch(value):
                    output[key_lower] = value.lower()
                elif isinstance(value, (dict, list)):
                    visit(value)
        elif isinstance(obj, list):
            for value in obj:
                visit(value)

    visit(manifest)
    if config is not None:
        visit(config)
    return dict(sorted(output.items()))


def _patch_paths(cell_dir: Path) -> list[tuple[Path, int]]:
    found: list[tuple[Path, int]] = []
    for path in cell_dir.rglob("patch.diff"):
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(cell_dir).as_posix()
        match = ATTEMPT_DIR.search(relative)
        attempt = int(match.group(1)) if match else 1
        found.append((path, attempt))
    return sorted(found, key=lambda item: (item[1], item[0].relative_to(cell_dir).as_posix()))


def _cell_key(round_id: str, experiment: str, manifest_id: str, cell_dir_name: str) -> str:
    identity = "\0".join((round_id, experiment, manifest_id, cell_dir_name))
    return hashlib.sha256(identity.encode("utf-8", errors="replace")).hexdigest()


def _find_grade_id(
    cell_dir: Path,
    manifest: dict[str, Any] | None,
    experiment: str,
    grades: dict[str, dict[str, Any]],
    metadata_ids_by_experiment: dict[str, list[str]],
    sorted_grade_ids: list[str],
    round_ids: set[str],
    grade_ids_by_experiment: dict[str, list[str]] | None = None,
) -> tuple[str | None, str | None]:
    candidates = metadata_ids_by_experiment.get(experiment, [])
    if len(candidates) == 1 and candidates[0] in grades:
        return candidates[0], "metadata_experiment"
    if experiment in grades:
        return experiment, "experiment_id"
    if cell_dir.name in grades:
        return cell_dir.name, "directory_id"
    if not manifest:
        return None, None

    # Some retained lever ledgers use the host experiment label as the join
    # key. Require a unique grade row after matching the manifest's task and
    # repetition fields; ambiguous labels remain unjoined.
    label_ids = (grade_ids_by_experiment or {}).get(experiment, [])
    if label_ids:
        requested = manifest.get("requested") if isinstance(manifest.get("requested"), dict) else {}
        manifest_ids = _ids_from_manifest(manifest)
        candidates = list(label_ids)
        for key in ("task", "rep", "model", "effort"):
            value = requested.get(key)
            if value is None:
                value = manifest_ids.get(key)
            if value is None:
                continue
            candidates = [
                candidate_id for candidate_id in candidates
                if grades[candidate_id].get(key) is None
                or str(grades[candidate_id].get(key)) == str(value)
            ]
        if len(candidates) == 1:
            return candidates[0], "experiment_label"

    normalized_id = manifest.get("cell_id")
    requested = manifest.get("requested") if isinstance(manifest.get("requested"), dict) else {}
    if not isinstance(normalized_id, str) or not normalized_id:
        return None, None
    prefix = normalized_id + "-"
    start = bisect.bisect_left(sorted_grade_ids, prefix)
    matches: list[str] = []
    for candidate_id in sorted_grade_ids[start:]:
        if not candidate_id.startswith(prefix):
            break
        candidate = grades[candidate_id]
        if candidate.get("task") != requested.get("task"):
            continue
        if requested.get("rep") is not None and str(candidate.get("rep")) != str(requested.get("rep")):
            continue
        matches.append(candidate_id)
    if len(matches) == 1:
        return matches[0], "manifest_cell_id_prefix"
    if len(matches) > 1:
        experiment_round = round_for_cell(normalized_id, experiment, round_ids)
        same_round = [
            candidate_id
            for candidate_id in matches
            if round_for_cell(candidate_id, "", round_ids) == experiment_round
        ]
        if len(same_round) == 1:
            return same_round[0], "manifest_prefix_and_round"
    return None, None


def _record_for_cell(
    cell_dir: Path,
    manifest: dict[str, Any] | None,
    grade_id: str | None,
    grade: dict[str, Any] | None,
    metadata: dict[str, Any],
    public_ids: set[str],
    round_ids: set[str],
    grade_join_method: str | None = None,
) -> tuple[dict[str, Any], list[tuple[Path, str]]]:
    experiment = ""
    if manifest and isinstance(manifest.get("experiment"), str):
        experiment = manifest["experiment"]
    meta = metadata.get(grade_id, {}) if grade_id else {}
    if not experiment and isinstance(meta, dict) and isinstance(meta.get("experiment"), str):
        experiment = meta["experiment"]
    effective_id = grade_id or (manifest.get("cell_id") if manifest else None) or cell_dir.name
    source_round_override = (manifest or {}).get("_source_round_override")
    if isinstance(source_round_override, str) and source_round_override in round_ids:
        round_id = source_round_override
    else:
        round_id = round_for_cell(str(effective_id), experiment, round_ids)
    if round_id == "unmapped" and grade_id:
        # The public export has separate names for HC iterations and the Studio R58x lane.
        round_id = round_for_cell(grade_id, experiment, round_ids)
    round_id = safe_label(round_id, identifier=True) or "unmapped"
    source_alias = source_round_alias(str(effective_id), experiment)

    ids = _ids_from_manifest(manifest or {}, meta if isinstance(meta, dict) else None)
    if grade:
        ids["arm"] = safe_label(grade.get("arm")) or ids["arm"]
        ids["task"] = safe_label(grade.get("task")) or ids["task"]
        if grade.get("rep") is not None:
            ids["rep"] = safe_label(str(grade.get("rep"))) or ids["rep"]
    if not ids["task"] and isinstance(meta, dict):
        ids["task"] = safe_label(meta.get("task"))

    manifest_id = manifest.get("cell_id") if manifest else None
    safe_manifest_id = safe_label(manifest_id, identifier=True)
    safe_grade_id = safe_label(grade_id, identifier=True)
    source_key = _cell_key(round_id, experiment, safe_manifest_id or "", cell_dir.name)
    patches: list[dict[str, Any]] = []
    patch_sources: list[tuple[Path, str]] = []
    for path, attempt in _patch_paths(cell_dir):
        content = path.read_bytes()
        size = len(content)
        digest = hashlib.sha256()
        digest.update(content)
        member = f"cells/{source_key}/attempt-{attempt}/patch.diff"
        exclusion_reasons = _patch_archive_exclusion_reasons(content)
        if size > MAX_PATCH_FILE_BYTES:
            exclusion_reasons.append("over_50mb")
        patch_record = {"attempt": attempt, "sha256": digest.hexdigest(), "size_bytes": size}
        if exclusion_reasons:
            patch_record["archive_member"] = None
            patch_record["archive_exclusion_reasons"] = exclusion_reasons
        else:
            patch_record["archive_member"] = member
            patch_sources.append((path, member))
        patches.append(patch_record)

    # A filtered source may carry only the hash and size for an oversized
    # patch. Keep that evidence without staging or publishing its body.
    source_patch_metadata = (manifest or {}).get("_source_patch_metadata")
    if isinstance(source_patch_metadata, list):
        seen_patch_identities = {
            (patch["attempt"], patch["sha256"]) for patch in patches
        }
        for item in source_patch_metadata:
            if not isinstance(item, dict):
                continue
            attempt = item.get("attempt")
            digest = item.get("sha256")
            size = item.get("size_bytes")
            reasons = item.get("archive_exclusion_reasons")
            if (
                not isinstance(attempt, int)
                or isinstance(attempt, bool)
                or attempt < 1
                or not isinstance(digest, str)
                or not HEX_SHA256.fullmatch(digest)
                or not isinstance(size, int)
                or isinstance(size, bool)
                or size < 0
                or not isinstance(reasons, list)
            ):
                continue
            identity = (attempt, digest.lower())
            if identity in seen_patch_identities:
                continue
            safe_reasons = [
                reason for reason in reasons
                if reason in {
                    "over_50mb", "bearer_marker", "jwt_marker", "refresh_token_marker",
                    "credential_value_field", "source_conflict", "gitleaks_detected",
                }
            ]
            if not safe_reasons:
                continue
            patches.append({
                "attempt": attempt,
                "sha256": digest.lower(),
                "size_bytes": size,
                "archive_member": None,
                "archive_exclusion_reasons": safe_reasons,
            })
            seen_patch_identities.add(identity)

    config = None
    if manifest:
        config_path = cell_dir / "config.json"
        if config_path.is_file() and not config_path.is_symlink():
            try:
                config = read_json(config_path)
            except (OSError, json.JSONDecodeError):
                config = None
    version_values = _versions(manifest or {}, config)
    prompt_sha = (manifest or {}).get("prompt_sha256")
    if not isinstance(prompt_sha, str) or not HEX_SHA256.fullmatch(prompt_sha):
        prompt_sha = None

    cell_id = safe_grade_id or safe_manifest_id or source_key
    record = {
        "schema_version": 1,
        "source_cell_key": source_key,
        "cell_id": cell_id,
        **({"manifest_cell_id": safe_manifest_id} if safe_manifest_id else {}),
        **({"grade_source_id": safe_grade_id} if safe_grade_id else {}),
        "round": round_id,
        **({"source_round": source_alias} if source_alias else {}),
        **ids,
        "status": safe_label((manifest or {}).get("status"), identifier=True),
        "wall_s": nonnegative_number((manifest or {}).get("wall_s")),
        "usage": _usage_fields(manifest or {}),
        "provider_response_count": _provider_response_count(manifest or {}),
        "official_grade": _grade_fields(grade),
        "manifest_grade": _grade_fields((manifest or {}).get("grade"))
        if isinstance((manifest or {}).get("grade"), dict) else None,
        "grade_join": (
            "matched" if grade is not None and grade_id is not None
            else "manifest" if grade is not None
            else "unmatched"
        ),
        **({"grade_join_method": grade_join_method} if grade_join_method else {}),
        "published_export": bool(grade_id and grade_id in public_ids),
        "raw_cell_present": cell_dir.is_dir(),
        "manifest_present": manifest is not None,
        "prompt_sha256": prompt_sha.lower() if prompt_sha else None,
        "base_sha": _named_sha(config if config is not None else {}) or _named_sha(manifest or {}),
        "versions": version_values,
        "patches": patches,
    }
    source_host = (manifest or {}).get("_source_host")
    if source_host in {"kogen-bench-us", "kogen-bench-eu"}:
        record["source_host"] = source_host
    source_kind = (manifest or {}).get("_source_kind")
    if source_kind in {
        "early-results", "snapshot-archive", "lever-label-archive", "lever-loose-results"
    }:
        record["source_kind"] = source_kind
    round_assignment = (manifest or {}).get("_source_round_assignment")
    if round_assignment in {
        "early-source-map", "snapshot-index-label", "unregistered-snapshot-label",
        "verified-label-archive", "loose-result-path",
    }:
        record["round_assignment_source"] = round_assignment
    source_archive_sha256 = (manifest or {}).get("_source_archive_sha256")
    if isinstance(source_archive_sha256, str) and HEX_SHA256.fullmatch(source_archive_sha256):
        record["source_archive_sha256"] = source_archive_sha256.lower()
    if grade_id and grade_id in public_ids:
        record["public_cell_id"] = safe_grade_id
    return record, patch_sources


def _record_for_grade_only(
    grade_id: str,
    grade: dict[str, Any],
    metadata: dict[str, Any],
    public_ids: set[str],
    round_ids: set[str],
) -> dict[str, Any]:
    meta = metadata.get(grade_id, {})
    experiment = meta.get("experiment", "") if isinstance(meta, dict) else ""
    round_id = round_for_cell(grade_id, str(experiment or ""), round_ids)
    if round_id == "r58x":
        round_id = "r58x-studio"
    if round_id == "unmapped" and isinstance(experiment, str):
        round_id = round_for_cell(grade_id, experiment, round_ids)
    round_id = safe_label(round_id, identifier=True) or "unmapped"
    source_alias = source_round_alias(grade_id, str(experiment or ""))
    parts = grade_id.split("__")
    harness = safe_label(parts[0]) if len(parts) >= 6 else None
    model = safe_label(parts[1]) if len(parts) >= 6 else None
    effort = safe_label(parts[2]) if len(parts) >= 6 else None
    task = safe_label(grade.get("task"))
    rep = safe_label(str(grade.get("rep"))) if grade.get("rep") is not None else None
    if len(parts) >= 5:
        harness = harness or safe_label(parts[0])
        model = model or safe_label(parts[1])
        effort = effort or safe_label(parts[2])
    key = hashlib.sha256((round_id + "\0" + grade_id).encode("utf-8")).hexdigest()
    return {
        "schema_version": 1,
        "source_cell_key": key,
        "cell_id": safe_label(grade_id, identifier=True) or key,
        "round": round_id,
        **({"source_round": source_alias} if source_alias else {}),
        "arm": safe_label(grade.get("arm")),
        "task": task,
        "rep": rep,
        "model": model,
        "effort": effort,
        "harness": harness,
        "status": None,
        "wall_s": None,
        "usage": {field: None for field in TOKEN_FIELDS},
        "provider_response_count": None,
        "official_grade": _grade_fields(grade),
        "grade_join": "grade_only",
        "published_export": grade_id in public_ids,
        "raw_cell_present": False,
        "manifest_present": False,
        "prompt_sha256": None,
        "base_sha": {},
        "versions": {},
        "patches": [],
        **({"public_cell_id": safe_label(grade_id, identifier=True)} if grade_id in public_ids else {}),
    }


def _write_jsonl_gz(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0, compresslevel=9) as compressed:
            for row in rows:
                compressed.write((json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8"))
    os.replace(temporary, path)


def _write_patch_archive(zstd: str, archive: Path, sources: list[tuple[Path, str]]) -> int:
    archive.parent.mkdir(parents=True, exist_ok=True)
    temporary = archive.with_name(archive.name + ".tmp")
    with temporary.open("wb") as output:
        process = subprocess.Popen(
            [zstd, "-q", "-19", "--threads=1", "-c"],
            stdin=subprocess.PIPE,
            stdout=output,
        )
        assert process.stdin is not None
        try:
            with tarfile.open(fileobj=process.stdin, mode="w|", format=tarfile.PAX_FORMAT) as tar:
                for source, member in sorted(sources, key=lambda item: item[1]):
                    info = tarfile.TarInfo(member)
                    info.size = source.stat().st_size
                    info.mtime = 0
                    info.mode = 0o644
                    info.uid = info.gid = 0
                    info.uname = info.gname = ""
                    with source.open("rb") as handle:
                        tar.addfile(info, handle)
        finally:
            process.stdin.close()
        status = process.wait()
    if status != 0:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"zstd failed while writing {archive.name} (exit {status})")
    os.replace(temporary, archive)
    return archive.stat().st_size


def _priority_rounds(findings: Path, available: set[str]) -> set[str]:
    if not findings.is_file():
        return set()
    text = findings.read_text(encoding="utf-8", errors="replace")
    referenced = set(re.findall(r"rounds/([A-Za-z0-9][A-Za-z0-9._-]*)", text))
    return referenced & available


def _write_manifest(output: Path) -> list[dict[str, Any]]:
    entries = []
    for path in sorted(output.rglob("*")):
        if not path.is_file() or path.name == "MANIFEST.sha256" or path.name.endswith(".tmp"):
            continue
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        entries.append({"sha256": digest.hexdigest(), "path": path.relative_to(output).as_posix()})
    manifest = output / "MANIFEST.sha256"
    temporary = manifest.with_name(manifest.name + ".tmp")
    temporary.write_text("".join(f"{row['sha256']}  {row['path']}\n" for row in entries), encoding="utf-8")
    os.replace(temporary, manifest)
    return entries


def mine(
    results: Path,
    grades_path: Path,
    metadata_path: Path,
    public_grades_path: Path,
    round_index_path: Path,
    output: Path,
    *,
    include_patches: bool = True,
    archive_rounds: set[str] | None = None,
    zstd: str = "zstd",
    findings_path: Path = DEFAULT_FINDINGS,
) -> dict[str, Any]:
    if not results.is_dir():
        raise FileNotFoundError(f"results directory is missing: {results}")
    source_grades = read_jsonl(grades_path)
    grades = {str(row["cell_id"]): row for row in source_grades if isinstance(row.get("cell_id"), str)}
    if len(grades) != len(source_grades):
        raise ValueError("source grade cell_id values are missing or duplicated")
    metadata = read_json(metadata_path) if metadata_path.is_file() else {}
    if not isinstance(metadata, dict):
        raise ValueError("cell metadata must be a JSON object")
    public_grades = read_jsonl(public_grades_path) if public_grades_path.is_file() else []
    public_ids = {str(row["cell_id"]) for row in public_grades if isinstance(row.get("cell_id"), str)}
    round_ids = set(json.loads(round_index_path.read_text(encoding="utf-8"))) if round_index_path.is_file() else set()
    archive_rounds = set(archive_rounds or ())
    invalid_archive_rounds = archive_rounds - round_ids
    if invalid_archive_rounds:
        raise ValueError("patch archive rounds must be registered round IDs")
    metadata_ids_by_experiment: dict[str, list[str]] = defaultdict(list)
    for cell_id, row in metadata.items():
        if isinstance(row, dict) and isinstance(row.get("experiment"), str) and row["experiment"]:
            metadata_ids_by_experiment[row["experiment"]].append(cell_id)

    grade_ids_by_experiment: dict[str, list[str]] = defaultdict(list)
    for cell_id, row in grades.items():
        label = row.get("experiment")
        if isinstance(label, str) and label:
            grade_ids_by_experiment[label].append(cell_id)

    sorted_grade_ids = sorted(grades)
    mined_by_round: dict[str, list[dict[str, Any]]] = defaultdict(list)
    patch_sources_by_round: dict[str, list[tuple[Path, str]]] = defaultdict(list)
    attached_grade_ids: set[str] = set()
    metrics = Counter()
    all_patch_bytes = 0
    all_patch_files = 0
    published_patch_bytes = 0
    published_patch_files = 0
    largest_patch_file = 0
    archive_eligible_patch_bytes = 0
    archive_eligible_patch_files = 0
    excluded_patch_bytes = 0
    excluded_patch_files = 0
    patch_exclusion_reasons = Counter()

    for cell_dir in sorted(results.iterdir(), key=lambda item: item.name):
        if not cell_dir.is_dir() or cell_dir.is_symlink():
            continue
        metrics["cell_directories"] += 1
        manifest_path = cell_dir / "manifest.json"
        manifest = None
        if manifest_path.is_file() and not manifest_path.is_symlink():
            try:
                manifest = read_json(manifest_path)
                if not isinstance(manifest, dict):
                    manifest = None
            except (OSError, json.JSONDecodeError):
                manifest = None
        if manifest is not None:
            metrics["manifests"] += 1
        experiment = manifest.get("experiment", "") if manifest else cell_dir.name
        if not isinstance(experiment, str):
            experiment = cell_dir.name
        grade_id, join_method = _find_grade_id(
            cell_dir,
            manifest,
            experiment,
            grades,
            metadata_ids_by_experiment,
            sorted_grade_ids,
            round_ids,
            grade_ids_by_experiment,
        )
        grade = grades.get(grade_id) if grade_id else None
        if grade is None and isinstance((manifest or {}).get("grade"), dict):
            grade = manifest["grade"]
            metrics["manifest_grade_rows"] += 1
        if grade_id:
            if grade_id in attached_grade_ids:
                raise ValueError(f"official grade row matched more than once: {safe_label(grade_id, identifier=True)}")
            attached_grade_ids.add(grade_id)
            metrics["cell_directories_with_grade"] += 1
            if grade_id in public_ids:
                metrics["source_public_export_matches"] += 1
            metrics["grade_join_" + str(join_method)] += 1
        else:
            metrics["cell_directories_without_grade"] += 1
        record, patches = _record_for_cell(
            cell_dir,
            manifest,
            grade_id,
            grade,
            metadata,
            public_ids,
            round_ids,
            join_method,
        )
        if not record["manifest_present"]:
            metrics["directories_without_manifest"] += 1
        if record["usage"]["input_tokens"] is not None and record["wall_s"] is not None:
            metrics["manifest_usage_and_wall"] += 1
        if record["provider_response_count"] is not None:
            metrics["provider_response_count_known"] += 1
            if record["provider_response_count"] > 1:
                metrics["multi_response_rows"] += 1
        patch_records = {patch.get("sha256"): patch for patch in record["patches"]}
        for patch_path, _member in _patch_paths(cell_dir):
            size = patch_path.stat().st_size
            all_patch_files += 1
            all_patch_bytes += size
            largest_patch_file = max(largest_patch_file, size)
            archive_patches = (
                record["published_export"]
                or record["round"] in SOURCE_REPORTED_ROUNDS
                or record["round"] in archive_rounds
            )
            if archive_patches:
                published_patch_files += 1
                published_patch_bytes += size
                digest = hashlib.sha256(patch_path.read_bytes()).hexdigest()
                patch_record = patch_records[digest]
                if patch_record.get("archive_exclusion_reasons"):
                    excluded_patch_files += 1
                    excluded_patch_bytes += size
                    patch_exclusion_reasons.update(patch_record["archive_exclusion_reasons"])
                else:
                    archive_eligible_patch_files += 1
                    archive_eligible_patch_bytes += size
        archive_candidate = (
            record["published_export"]
            or record["round"] in SOURCE_REPORTED_ROUNDS
            or record["round"] in archive_rounds
        )
        if archive_candidate and patches:
            metrics["archive_patch_cell_count"] += 1
        mined_by_round[record["round"]].append(record)
        record["archive_patches"] = bool(archive_candidate and patches)
        if record["archive_patches"]:
            patch_sources_by_round[record["round"]].extend(patches)

    for grade_id, grade in grades.items():
        if grade_id in attached_grade_ids:
            continue
        record = _record_for_grade_only(grade_id, grade, metadata, public_ids, round_ids)
        mined_by_round[record["round"]].append(record)
        metrics["grade_only_rows"] += 1
        if grade_id in public_ids:
            metrics["source_public_export_matches"] += 1
            metrics["public_grade_rows_without_cell_directory"] += 1

    output.mkdir(parents=True, exist_ok=True)
    record_files = []
    for round_id, rows in sorted(mined_by_round.items()):
        safe_round = safe_label(round_id, identifier=True)
        if not safe_round:
            raise ValueError("round label is unsafe")
        rows.sort(key=lambda row: (str(row.get("cell_id")), str(row.get("source_cell_key"))))
        destination = output / f"{safe_round}.jsonl.gz"
        _write_jsonl_gz(destination, rows)
        record_files.append(destination)

    alias_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for rows in mined_by_round.values():
        for row in rows:
            if row.get("source_round") in {"lr1", "lr2"}:
                alias_rows[row["source_round"]].append(row)
    for source_round, rows in sorted(alias_rows.items()):
        rows.sort(key=lambda row: (str(row.get("cell_id")), str(row.get("source_cell_key"))))
        destination = output / f"{source_round}.jsonl.gz"
        _write_jsonl_gz(destination, rows)
        record_files.append(destination)

    patch_summary: dict[str, Any] = {
        "archives_written": [],
        "all_source_patch_files": all_patch_files,
        "all_source_patch_bytes": all_patch_bytes,
        "published_patch_files": published_patch_files,
        "published_patch_bytes": published_patch_bytes,
        "archive_eligible_patch_files": archive_eligible_patch_files,
        "archive_eligible_patch_bytes": archive_eligible_patch_bytes,
        "excluded_patch_files": excluded_patch_files,
        "excluded_patch_bytes": excluded_patch_bytes,
        "exclusion_reason_counts": dict(sorted(patch_exclusion_reasons.items())),
        "largest_patch_file_bytes": largest_patch_file,
        "max_individual_patch_bytes": MAX_PATCH_FILE_BYTES,
        "compressed_limit_bytes": MAX_PATCH_ARCHIVE_BYTES,
        "compressed_bytes": 0,
        "unarchived_published_patch_files": 0,
        "unarchived_published_patch_bytes": 0,
        "priority_rounds_used": [],
    }
    if include_patches and patch_sources_by_round:
        if shutil.which(zstd) is None:
            raise FileNotFoundError(f"zstd executable not found: {zstd}")
        with tempfile.TemporaryDirectory(prefix="kogen-mine-patches-") as temp_name:
            staged = Path(temp_name)
            staged_archives: dict[str, Path] = {}
            total_compressed = 0
            for round_id, sources in sorted(patch_sources_by_round.items()):
                archive = staged / f"{round_id}.tar.zst"
                compressed_size = _write_patch_archive(zstd, archive, sources)
                staged_archives[round_id] = archive
                total_compressed += compressed_size
            full_copy_fits = largest_patch_file <= MAX_PATCH_FILE_BYTES and total_compressed <= MAX_PATCH_ARCHIVE_BYTES
            available = set(staged_archives)
            to_copy = available if full_copy_fits else _priority_rounds(findings_path, available)
            patches_output = output / "patches"
            patches_output.mkdir(parents=True, exist_ok=True)
            for round_id in sorted(to_copy):
                destination = patches_output / f"{round_id}.tar.zst"
                temporary = destination.with_name(destination.name + ".tmp")
                shutil.copyfile(staged_archives[round_id], temporary)
                os.replace(temporary, destination)
                compressed_size = destination.stat().st_size
                patch_summary["archives_written"].append(
                    {"round": round_id, "files": len(patch_sources_by_round[round_id]), "compressed_bytes": compressed_size}
                )
                patch_summary["compressed_bytes"] += compressed_size
            skipped = available - to_copy
            patch_summary["unarchived_published_patch_files"] = sum(
                len(patch_sources_by_round[round_id]) for round_id in skipped
            )
            patch_summary["unarchived_published_patch_bytes"] = sum(
                Path(source).stat().st_size
                for round_id in skipped
                for source, _member in patch_sources_by_round[round_id]
            )
            patch_summary["priority_rounds_used"] = sorted(to_copy) if not full_copy_fits else []

    summary = {
        "schema_version": 1,
        "source": "read-only probe results and grades.final.jsonl",
        "source_cell_directories": metrics["cell_directories"],
        "source_grade_rows": len(grades),
        "source_public_grade_ids": len(public_ids),
        "public_export_grade_ids": len(public_ids),
        "source_public_export_id_matches": metrics["source_public_export_matches"],
        "public_export_ids_not_in_source_grades": len(public_ids - set(grades)),
        "source_manifests": metrics["manifests"],
        "manifest_usage_and_wall_rows": metrics["manifest_usage_and_wall"],
        "provider_response_count_known_rows": metrics["provider_response_count_known"],
        "multi_response_rows": metrics["multi_response_rows"],
        "cell_directories_with_grade": metrics["cell_directories_with_grade"],
        "cell_directories_without_grade": metrics["cell_directories_without_grade"],
        "directories_without_manifest": metrics["directories_without_manifest"],
        "grade_only_rows": metrics["grade_only_rows"],
        "public_grade_rows_without_cell_directory": metrics["public_grade_rows_without_cell_directory"],
        "grade_join_methods": {
            key.removeprefix("grade_join_"): value
            for key, value in sorted(metrics.items())
            if key.startswith("grade_join_")
        },
        "round_files": [path.name for path in record_files],
        "round_record_counts": {round_id: len(rows) for round_id, rows in sorted(mined_by_round.items())},
        "source_round_alias_counts": {round_id: len(rows) for round_id, rows in sorted(alias_rows.items())},
        "archive_patch_cells": metrics["archive_patch_cell_count"],
        "patches": patch_summary,
    }
    summary_path = output / "SUMMARY.json"
    temporary_summary = summary_path.with_name(summary_path.name + ".tmp")
    temporary_summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary_summary, summary_path)
    _write_manifest(output)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--grades", type=Path, default=DEFAULT_GRADES)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--public-grades", type=Path, default=DEFAULT_PUBLIC_GRADES)
    parser.add_argument("--round-index", type=Path, default=DEFAULT_ROUND_INDEX)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--findings", type=Path, default=DEFAULT_FINDINGS)
    parser.add_argument(
        "--archive-round",
        action="append",
        default=[],
        help="also include safe patches from this registered round in patches/<round>.tar.zst",
    )
    parser.add_argument("--zstd", default="zstd", help="zstd executable used for .tar.zst patch bundles")
    parser.add_argument("--skip-patches", action="store_true", help="write cell records without patch archives")
    args = parser.parse_args()
    summary = mine(
        args.results,
        args.grades,
        args.metadata,
        args.public_grades,
        args.round_index,
        args.output,
        include_patches=not args.skip_patches,
        archive_rounds=set(args.archive_round),
        zstd=args.zstd,
        findings_path=args.findings,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
