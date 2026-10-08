#!/usr/bin/env python3
"""Mine privacy-filtered benchmark records staged from the Mac Studio.

This importer reads only a local, allow-listed scratch copy. It reuses
``mine_probe`` sanitization, record fields, patch filtering, archive format, and
manifest writer. Source paths, transcripts, rollouts, and request logs are not
written to Kogen Bench.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import mine_probe as mp


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STUDIO = Path("/tmp/kogen-bench-mstudio-scratch-20261008/studio")
TARGET_ROUNDS = {
    "harness-compare-1", "confirm-combined-1", "claim-b-rerun-1",
    "claim-b-screen-1", "hard1-calibrate-1", "kh-compare-2026-09-29",
    "harness-pick-2026-09-29", "kh-climb", "e06-context", "e09-tidewave",
    "night-2026-10-01", "x-compaction", "x-context", "x-continuation",
    "x-ladder", "x-minikogen", "x-mining", "x-models", "x-parallel",
    "x-race", "x-recovery", "x-review", "x-roles", "x-surface",
    "unmapped", "l1-task-grader-trust",
}
RESULTS_SOURCES = {
    "harness-compare-1.tar.zst": ("harness-compare-1", "harness-compare-1"),
    "harness-compare-1-prelim.tar.zst": ("harness-compare-1", "harness-compare-1-prelim"),
    "confirm-combined-1.tar.zst": ("confirm-combined-1", "confirm-combined-1"),
    "claim-b-rerun-1.tar.zst": ("claim-b-rerun-1", "claim-b-rerun-1"),
    "claim-b-screen-1": ("claim-b-screen-1", "claim-b-screen-1"),
    "claim-b-screen-1-retained-infra-grade": ("claim-b-screen-1", "claim-b-screen-1-retained-infra-grade"),
    "hard1-calibrate-1.tar.zst": ("hard1-calibrate-1", "hard1-calibrate-1"),
    "kh-compare-2026-09-29": ("kh-compare-2026-09-29", "kh-compare-2026-09-29"),
    "hp-grok.tar.zst": ("harness-pick-2026-09-29", "harness-pick-2026-09-29-hp-grok"),
}
OBJECT_ROUNDS = {
    "results/chatgpt-smoke": ("unmapped", "chatgpt-smoke-object"),
    "results/claim-b-screen-1": ("claim-b-screen-1", "claim-b-screen-1-object"),
    "results/claim-b-rerun-1": ("claim-b-rerun-1", "claim-b-rerun-1-object"),
    "hc/results/robust-control-retry1/20260930T124335.109354Z-94428-3d2bf25d": (
        "x-recovery", "robust-control-retry1-object",
    ),
    "hc/results/tokens-control-retry1/20260930T124214.686564Z-91504-02f8c2d1": (
        "x-mining", "tokens-control-retry1-object",
    ),
    "hc/results/cache-base-03/20260930T133406.177020Z-25929-479caf0b": (
        "x-mining", "cache-base-03-object",
    ),
    "hc/results/robust-recovery/20260930T140619.624705Z-52725-065ea9a1": (
        "x-recovery", "robust-recovery-object",
    ),
    "hc/results/x-ladder-m01-luna-max/20260930T131835.247034Z-16992-ccc8c533": (
        "x-ladder", "x-ladder-m01-luna-max-object",
    ),
    "hc/results/x-models-m01-s01-candidate/20260930T140353.928603Z-49288-c6013009": (
        "x-models", "x-models-m01-s01-candidate-object",
    ),
}


def _object_round_mapping(experiment: str) -> tuple[str, str] | None:
    mapped = OBJECT_ROUNDS.get(experiment)
    if mapped:
        return mapped
    parts = Path(experiment).parts
    # The damaged-host snapshot identifies this worker copy by its relative
    # directory suffix; its host address is deliberately not retained here.
    if len(parts) >= 6 and parts[0] == "worker" and parts[-5:] == (
        "srv", "bh", "bench", "results", "claim-b-rerun-1",
    ):
        return "claim-b-rerun-1", "claim-b-rerun-1-worker-object"
    return None


def _digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _safe_round(label: str, round_ids: set[str]) -> str:
    if label in round_ids:
        return label
    raise ValueError(f"unregistered Studio source round: {label}")


def _source_round_from_hc_label(label: str) -> str | None:
    match = re.match(r"^(x-[a-z]+)(?:-|$)", label)
    return match.group(1) if match else None


def _source_path_candidates(studio: Path, value: Any) -> list[Path]:
    if not isinstance(value, str) or not value.startswith("/"):
        return []
    candidates: list[Path] = []
    marker = "/bench/"
    if marker in value:
        relative = value.split(marker, 1)[1]
        direct = studio / "bench" / relative
        candidates.append(direct)
        parts = Path(relative).parts
        if len(parts) >= 4 and parts[0:2] == ("hc", "results"):
            label = parts[2]
            candidates.append(studio / "bench" / "hc" / "results" / f"{label}.tar.zst" / label / Path(*parts[3:]))
        elif len(parts) >= 3 and parts[0] == "results":
            label = parts[1]
            candidates.append(studio / "bench" / "results" / f"{label}.tar.zst" / label / Path(*parts[2:]))
    return candidates


def _resolve_source_path(studio: Path, value: Any) -> Path | None:
    """Resolve an original Studio manifest path to its staged local copy."""
    candidates = _source_path_candidates(studio, value)
    for candidate in candidates:
        if candidate.is_file() and candidate.name == "manifest.json":
            return candidate
    return None


def _resolve_source_cell_dir(studio: Path, value: Any) -> Path | None:
    for candidate in _source_path_candidates(studio, value):
        if candidate.parent.is_dir():
            return candidate.parent
    return None


def _classification(value: Any) -> str | None:
    if isinstance(value, bool):
        return "pass" if value else "fail"
    if not isinstance(value, str):
        return None
    normalized = value.strip().lower()
    mapping = {
        "correct": "pass", "pass": "pass", "passed": "pass",
        "incorrect": "fail", "fail": "fail", "failed": "fail",
        "infra": "infra", "infrastructure": "infra", "infra_error": "infra",
        "grader_error": "grader_error", "timeout": "timeout",
        "interrupted": "interrupted", "pending": "pending",
        "restore_failed": "restore_failed", "invalid": "invalid",
        "unknown": "unknown",
    }
    return mapping.get(normalized)


def _grade_from_ledger(ledger: dict[str, Any] | None) -> dict[str, Any] | None:
    if not ledger:
        return None
    raw = ledger.get("grade_outcome") or ledger.get("outcome") or ledger.get("result")
    classification = _classification(raw)
    if classification is None and isinstance(ledger.get("pass_"), bool):
        classification = _classification(ledger["pass_"])
    if classification is None and isinstance(ledger.get("pass"), bool):
        classification = _classification(ledger["pass"])
    if classification is None:
        return None
    return {"outcome": classification, "tests_ran": ledger.get("tests_ran")}


def _ledger_usage(ledger: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(ledger, dict):
        return None
    raw = ledger.get("usage") if isinstance(ledger.get("usage"), dict) else ledger
    names = {
        "input": ("uncached_input_tokens", "input"),
        "cached_input": ("cached_tokens", "cached_input_tokens", "cached_input"),
        "output": ("output_tokens", "output"),
        "reasoning": ("reasoning_tokens", "reasoning"),
    }
    result: dict[str, Any] = {}
    for target, keys in names.items():
        for key in keys:
            value = raw.get(key)
            if isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0:
                result[target] = value
                break
    return result if result else None


def _row_identity(ledger: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(ledger.get("task") or ""), str(ledger.get("rep") or ""),
        str(ledger.get("model") or ledger.get("requested_model") or ""),
        str(ledger.get("harness") or ""),
    )


def _manifest_label(path: Path, studio: Path) -> str:
    relative = path.relative_to(studio / "bench")
    if relative.parts[:2] == ("hc", "results"):
        return relative.parts[2].removesuffix(".tar.zst")
    return relative.parts[0]


def mine(studio: Path, output: Path, *, zstd: str) -> dict[str, Any]:
    studio = studio.resolve()
    bench = studio / "bench"
    if not bench.is_dir():
        raise FileNotFoundError(f"staged Studio tree is missing: {bench}")
    round_ids = set(json.loads((ROOT / "rounds/index.json").read_text(encoding="utf-8")))
    if not TARGET_ROUNDS.issubset(round_ids):
        raise ValueError("one or more expected Studio rounds are not registered")

    # Parse the verified object list before importing any object members.
    object_report_path = studio / "source-object-verification.json"
    object_rows = json.loads(object_report_path.read_text(encoding="utf-8"))["objects"] if object_report_path.is_file() else []
    object_map = {row["experiment"]: row for row in object_rows if row.get("valid") is True}

    candidates: list[dict[str, Any]] = []
    unresolved_refs = 0
    ledger_only_count = 0
    source_counts: Counter[str] = Counter()

    def add_manifest(path: Path, round_id: str, source_label: str, ledger: dict[str, Any] | None = None) -> None:
        nonlocal unresolved_refs
        try:
            manifest = mp.read_json(path)
        except (OSError, json.JSONDecodeError):
            return
        if not isinstance(manifest, dict) or not isinstance(manifest.get("cell_id"), str):
            return
        requested = manifest.get("requested")
        if not isinstance(requested, dict):
            return
        raw_sha = _digest(path)
        patch_hashes = tuple(_digest(patch) for patch, _attempt in mp._patch_paths(path.parent))
        source_key = hashlib.sha256(
            (round_id + "\0" + raw_sha + "\0" + "\0".join(patch_hashes)).encode("utf-8")
        ).hexdigest()
        ledger = ledger or {}
        adjusted = dict(manifest)
        adjusted["experiment"] = round_id
        ledger_grade = _grade_from_ledger(ledger)
        manifest_grade = manifest.get("grade") if isinstance(manifest.get("grade"), dict) else None
        grade = ledger_grade or manifest_grade
        record, patch_sources = mp._record_for_cell(
            path.parent, adjusted, None, grade, {}, set(), round_ids,
        )
        record["source_cell_key"] = source_key
        record["source_cell_id"] = record.get("cell_id")
        record["cell_id"] = record.get("cell_id") or source_key
        record["source_experiment"] = mp.safe_label(source_label) or "studio-source"
        record["source_manifest_sha256"] = raw_sha
        record["source_copy_count"] = 1
        record["published_export"] = False
        record.pop("public_cell_id", None)

        if ledger_grade and manifest_grade:
            from_manifest = mp._grade_fields(manifest_grade)
            from_ledger = mp._grade_fields(ledger_grade)
            if from_manifest and from_ledger and from_manifest["classification"] != from_ledger["classification"]:
                record["source_grade_mismatch"] = {
                    "manifest": from_manifest["classification"],
                    "ledger": from_ledger["classification"],
                }
        if ledger:
            record["source_record_type"] = "manifest+ledger"
            if isinstance(ledger.get("status"), str):
                record["status"] = mp.safe_label(ledger.get("status"), identifier=True)
            wall = mp.nonnegative_number(ledger.get("wall_s"))
            if wall is not None:
                record["wall_s"] = wall
            usage = _ledger_usage(ledger)
            if usage:
                normalized = mp._usage_fields({"usage": usage})
                for key, value in normalized.items():
                    if value is not None:
                        record["usage"][key] = value
            task = mp.safe_label(ledger.get("task"))
            if task:
                record["task"] = task
            rep = ledger.get("rep")
            if rep is not None:
                record["rep"] = mp.safe_label(str(rep)) or record.get("rep")
            model = mp.safe_label(ledger.get("model") or ledger.get("requested_model"))
            if model:
                record["model"] = model
            effort = mp.safe_label(ledger.get("effort") or ledger.get("requested_effort"))
            if effort:
                record["effort"] = effort
            harness = mp.safe_label(ledger.get("harness"))
            if harness:
                record["harness"] = harness
            arm = mp.safe_label(ledger.get("arm"))
            if arm:
                record["arm"] = arm
        if not record.get("arm"):
            record["arm"] = mp.safe_label(source_label)

        new_patch_sources = []
        for patch_path, old_member in patch_sources:
            attempt_match = re.search(r"attempt-(\d+)", old_member)
            attempt = int(attempt_match.group(1)) if attempt_match else 1
            new_patch_sources.append((patch_path, f"cells/{source_key}/attempt-{attempt}/patch.diff"))
        patch_records = []
        for patch in record["patches"]:
            item = dict(patch)
            reasons = item.get("archive_exclusion_reasons") or []
            # Keep useful audit metadata without copying scan-marker strings
            # into the public output itself.
            item["archive_exclusion_reasons"] = [
                "over_50mb" if reason == "over_50mb" else "credential_marker"
                for reason in reasons
            ]
            if item.get("archive_exclusion_reasons"):
                item["archive_member"] = None
            else:
                item["archive_member"] = f"cells/{source_key}/attempt-{item.get('attempt', 1)}/patch.diff"
            patch_records.append(item)
        record["patches"] = patch_records
        source_counts[source_label] += 1
        candidates.append({
            "round": round_id,
            "source_label": source_label,
            "manifest_path": path,
            "manifest_sha256": raw_sha,
            "patch_hashes": patch_hashes,
            "record": record,
            "patch_sources": new_patch_sources,
            "ledger": ledger,
            "rank": (1 if ledger_grade else 0, 1 if patch_hashes else 0, 1 if record.get("usage", {}).get("input_tokens") is not None else 0),
        })

    def add_summary_row(round_id: str, source_label: str, row: dict[str, Any], *, cell_id: str | None = None) -> None:
        """Retain safe per-cell summary rows where no raw manifest joins."""
        raw_id = cell_id or row.get("cell") or row.get("id")
        normalized_id = mp.safe_label(raw_id, identifier=True)
        if not normalized_id and isinstance(raw_id, str):
            normalized_id = re.sub(r"[^A-Za-z0-9_.:+-]+", "-", raw_id).strip("-")[:480]
        key_source = normalized_id or json.dumps(
            {k: row.get(k) for k in ("task", "rep", "model", "harness", "arm", "status")},
            sort_keys=True, separators=(",", ":"),
        )
        summary_signature = {
            key: row.get(key) for key in (
                "task", "rep", "model", "effort", "harness", "arm", "status",
                "outcome", "result", "grade", "pass_", "wall_s", "wall",
                "input", "cached", "cached_input", "output", "reasoning", "o", "r",
            )
        }
        signature_text = json.dumps(summary_signature, sort_keys=True, separators=(",", ":"), default=str)
        source_key = hashlib.sha256((round_id + "\0" + source_label + "\0" + str(key_source) + "\0" + signature_text).encode("utf-8")).hexdigest()
        outcome = _classification(row.get("outcome"))
        if outcome is None:
            outcome = _classification(row.get("grade"))
        if outcome is None:
            outcome = _classification(row.get("pass_"))
        grade = {"outcome": outcome} if outcome else None
        usage: dict[str, Any] = {key: None for key in mp.TOKEN_FIELDS}
        aliases = {
            "input_tokens": ("input", "input_tokens"),
            "cached_input_tokens": ("cached", "cached_input", "cached_input_tokens"),
            "output_tokens": ("output", "output_tokens", "o"),
            "reasoning_tokens": ("reasoning", "reasoning_tokens", "r"),
        }
        for target, fields in aliases.items():
            for field in fields:
                value = row.get(field)
                numeric = mp.nonnegative_number(value)
                if numeric is not None:
                    usage[target] = numeric
                    break
        summary_record = {
            "schema_version": 1,
            "source_cell_key": source_key,
            "cell_id": normalized_id or source_key,
            "source_cell_id": normalized_id or source_key,
            "round": round_id,
            "source_experiment": source_label,
            "source_experiments": [source_label],
            "source_record_type": "per_cell_summary",
            "source_manifest_sha256": None,
            "source_copy_count": 1,
            "arm": mp.safe_label(row.get("arm") or row.get("harness")) or source_label,
            "task": mp.safe_label(row.get("task")),
            "rep": mp.safe_label(str(row.get("rep"))) if row.get("rep") is not None else None,
            "model": mp.safe_label(row.get("model")),
            "effort": mp.safe_label(row.get("effort")),
            "harness": mp.safe_label(row.get("harness")),
            "status": mp.safe_label(row.get("status"), identifier=True),
            "wall_s": mp.nonnegative_number(row.get("wall_s", row.get("wall"))),
            "usage": usage,
            "official_grade": mp._grade_fields(grade),
            "grade_join": "source_summary",
            "published_export": False,
            "raw_cell_present": False,
            "manifest_present": False,
            "prompt_sha256": None,
            "base_sha": {},
            "versions": {},
            "patches": [],
        }
        candidates.append({
            "round": round_id,
            "source_label": source_label,
            "manifest_path": None,
            "manifest_sha256": None,
            "patch_hashes": (),
            "record": summary_record,
            "patch_sources": [],
            "ledger": row,
            "rank": (0, 0, 0),
        })

    def add_ledger_only(round_id: str, source_label: str, row: dict[str, Any], original_path: Any) -> None:
        """Retain safe cell-ledger fields when the referenced manifest is absent."""
        nonlocal ledger_only_count
        cell_dir = _resolve_source_cell_dir(studio, original_path)
        raw_id = Path(str(original_path)).parent.name if isinstance(original_path, str) else ""
        cell_id = mp.safe_label(raw_id, identifier=True)
        if not cell_id:
            cell_id = hashlib.sha256(str(original_path).encode("utf-8", errors="replace")).hexdigest()
        ledger_signature = {
            key: row.get(key) for key in (
                "task", "rep", "arm", "status", "grade_outcome", "outcome", "result",
                "pass", "pass_", "wall_s", "uncached_input_tokens", "cached_tokens",
                "output_tokens", "reasoning_tokens",
            )
        }
        signature_text = json.dumps(ledger_signature, sort_keys=True, separators=(",", ":"), default=str)
        source_key = hashlib.sha256(
            (round_id + "\0" + source_label + "\0" + cell_id + "\0" + signature_text).encode("utf-8")
        ).hexdigest()
        if cell_dir is None:
            cell_dir = studio / "bench" / ".missing-studio-cell"
        synthetic_manifest = {
            "cell_id": cell_id,
            "experiment": round_id,
            "requested": {"task": row.get("task"), "rep": row.get("rep")},
            "status": row.get("status"),
            "wall_s": row.get("wall_s"),
        }
        grade = _grade_from_ledger(row)
        record, old_patch_sources = mp._record_for_cell(
            cell_dir, synthetic_manifest, None, grade, {}, set(), round_ids,
        )
        record["source_cell_key"] = source_key
        record["source_cell_id"] = cell_id
        record["cell_id"] = cell_id
        record["source_experiment"] = mp.safe_label(source_label) or "studio-source"
        record["source_experiments"] = [record["source_experiment"]]
        record["source_record_type"] = "cells_ledger_only"
        record["source_manifest_sha256"] = None
        record["source_copy_count"] = 1
        record["manifest_present"] = False
        record["raw_cell_present"] = cell_dir.is_dir() and cell_dir.name != ".missing-studio-cell"
        record["grade_join"] = "cells_ledger_only"
        record["published_export"] = False
        record.pop("public_cell_id", None)
        if isinstance(row.get("status"), str):
            record["status"] = mp.safe_label(row.get("status"), identifier=True)
        wall = mp.nonnegative_number(row.get("wall_s"))
        if wall is not None:
            record["wall_s"] = wall
        usage = _ledger_usage(row)
        if usage:
            normalized = mp._usage_fields({"usage": usage})
            for key, value in normalized.items():
                if value is not None:
                    record["usage"][key] = value
        task = mp.safe_label(row.get("task"))
        if task:
            record["task"] = task
        rep = row.get("rep")
        if rep is not None:
            record["rep"] = mp.safe_label(str(rep))
        arm = mp.safe_label(row.get("arm"))
        if arm:
            record["arm"] = arm
        new_patch_sources = []
        for patch_path, old_member in old_patch_sources:
            match = re.search(r"attempt-(\d+)", old_member)
            attempt = int(match.group(1)) if match else 1
            new_patch_sources.append((patch_path, f"cells/{source_key}/attempt-{attempt}/patch.diff"))
        for patch in record.get("patches", []):
            reasons = patch.get("archive_exclusion_reasons") or []
            patch["archive_exclusion_reasons"] = [
                "over_50mb" if reason == "over_50mb" else "credential_marker"
                for reason in reasons
            ]
            patch["archive_member"] = None if patch["archive_exclusion_reasons"] else (
                f"cells/{source_key}/attempt-{patch.get('attempt', 1)}/patch.diff"
            )
        ledger_only_count += 1
        candidates.append({
            "round": round_id,
            "source_label": source_label,
            "manifest_path": None,
            "manifest_sha256": None,
            "patch_hashes": tuple(patch.get("sha256") for patch in record.get("patches", [])),
            "record": record,
            "patch_sources": new_patch_sources,
            "ledger": row,
            "rank": (1 if grade else 0, 1 if record.get("patches") else 0, 1 if record.get("usage", {}).get("input_tokens") is not None else 0),
        })

    # Grade/usage ledgers for the exact Studio HC result directories.
    hc_root = bench / "hc" / "results"
    ledgers_by_path: dict[Path, list[dict[str, Any]]] = defaultdict(list)
    if hc_root.is_dir():
        for ledger_path in hc_root.rglob("cells.json"):
            try:
                data = mp.read_json(ledger_path)
            except (OSError, json.JSONDecodeError):
                continue
            rows = data if isinstance(data, list) else data.get("cells", []) if isinstance(data, dict) else []
            for row in rows:
                if not isinstance(row, dict):
                    continue
                resolved = _resolve_source_path(studio, row.get("manifest"))
                if resolved:
                    ledgers_by_path[resolved].append(row)
                else:
                    unresolved_refs += 1
                    label = ledger_path.relative_to(hc_root).parts[0].removesuffix(".tar.zst")
                    round_id = _source_round_from_hc_label(label)
                    if label.startswith("e06-context-"):
                        round_id = "e06-context"
                    if round_id in TARGET_ROUNDS:
                        add_ledger_only(round_id, label, row, row.get("manifest"))

    # Sept 29-30 ~/bench/results snapshots.
    results_root = bench / "results"
    for dirname, (round_id, source_label) in RESULTS_SOURCES.items():
        if dirname == "kh-compare-2026-09-29":
            continue
        source_root = results_root / dirname
        if not source_root.is_dir():
            continue
        for path in source_root.rglob("manifest.json"):
            add_manifest(path, _safe_round(round_id, round_ids), source_label)

    hp_regrade_rows: list[dict[str, Any]] = []
    # Per-cell summaries for the harness pick can join their explicit cell IDs
    # to retained Grok manifests. Other rows remain clearly marked as summaries.
    hp_summary = results_root / "hp-summary.json"
    if hp_summary.is_file():
        hp_manifests = []
        hp_root = results_root / "hp-grok.tar.zst"
        if hp_root.is_dir():
            hp_manifests = [p for p in hp_root.rglob("manifest.json")]
        hp_by_id: dict[str, list[Path]] = defaultdict(list)
        for path in hp_manifests:
            try:
                data = mp.read_json(path)
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(data, dict) and isinstance(data.get("cell_id"), str):
                hp_by_id[data["cell_id"]].append(path)
        for row in mp.read_json(hp_summary):
            if not isinstance(row, dict):
                continue
            cell = row.get("cell")
            matching = hp_by_id.get(str(cell), []) if isinstance(cell, str) else []
            ledger = {
                "pass_": row.get("pass_"), "status": row.get("status"),
                "wall_s": row.get("wall_s"), "usage": {
                    "input": row.get("input"), "cached_input": row.get("cached"),
                    "output": row.get("output"), "reasoning": row.get("reasoning"),
                },
                "task": row.get("task"), "rep": row.get("rep"),
                "model": row.get("model"), "effort": row.get("effort"),
                "harness": row.get("harness"),
            }
            if len(matching) == 1:
                add_manifest(matching[0], "harness-pick-2026-09-29", "harness-pick-summary", ledger)
            else:
                add_summary_row("harness-pick-2026-09-29", "harness-pick-summary", row)
        regrade_path = results_root / "hp-regrade-syn40.json"
        if regrade_path.is_file():
            for row in mp.read_json(regrade_path):
                if not isinstance(row, dict):
                    continue
                cell = row.get("cell")
                source_id = str(cell).split("/", 1)[-1] if isinstance(cell, str) else ""
                original = row.get("original") if isinstance(row.get("original"), dict) else {}
                original_grade = original.get("grade")
                if isinstance(original_grade, dict):
                    original_grade = original_grade.get("outcome", original_grade.get("pass_", original_grade.get("pass")))
                regraded = row.get("regrade") if isinstance(row.get("regrade"), dict) else {}
                hp_regrade_rows.append({
                    "cell_id": mp.safe_label(source_id, identifier=True),
                    "original_outcome": _classification(original_grade),
                    "regraded_outcome": _classification(regraded.get("pass")),
                })

    # Keep the underlying kh-compare manifests alongside its unlinked summary
    # rows so the page can show both evidence sources without pooling them.
    kh_raw_root = results_root / "kh-compare-2026-09-29"
    if kh_raw_root.is_dir():
        for path in kh_raw_root.rglob("manifest.json"):
            add_manifest(path, "kh-compare-2026-09-29", "kh-compare-raw")

    # kh-compare summaries have 18 per-cell rows but do not carry the same cell
    # identifiers as the 17 raw manifest IDs. Keep the source-summary rows
    # separate rather than guessing a join to a particular repetition.
    kh_summary = studio.parent / "macbook" / "bench-review" / "studio" / "summary.json"
    if kh_summary.is_file():
        for row in mp.read_json(kh_summary):
            if not isinstance(row, dict):
                continue
            cell_parts = str(row.get("cell") or "").split()
            models = row.get("models") if isinstance(row.get("models"), list) else []
            task = cell_parts[-1] if cell_parts else None
            if task and not task.startswith("hp-"):
                task = "hp-" + task
            normalized = {
                "cell": "-".join(cell_parts), "task": task,
                "model": models[0] if models else None,
                "harness": cell_parts[0] if cell_parts else None,
                "status": row.get("status"), "grade": row.get("grade"),
                "wall": row.get("wall"), "cached": row.get("c"),
                "output": row.get("o"), "reasoning": row.get("r"),
            }
            add_summary_row("kh-compare-2026-09-29", "kh-compare-summary", normalized)
        # The Studio and MacBook copies were byte-identical at extraction.

    # All source-backed HC x-* ledgers and raw manifests. Repeated references
    # are deduplicated below by exact manifest and patch hashes.
    if hc_root.is_dir():
        for path in hc_root.rglob("manifest.json"):
            label = _manifest_label(path, studio)
            round_id = _source_round_from_hc_label(label)
            if label.startswith("e06-context-"):
                round_id = "e06-context"
            if round_id not in TARGET_ROUNDS:
                continue
            rows = ledgers_by_path.get(path, [])
            selected = max(rows, key=lambda row: bool(_grade_from_ledger(row)), default=None)
            add_manifest(path, round_id, label, selected)

    # The iCloud B028 packet points to this one retained e06 model cell.
    if hc_root.is_dir():
        for path in hc_root.glob("e06-context-*/**/manifest.json"):
            if isinstance(mp.read_json(path), dict):
                label = _manifest_label(path, studio)
                add_manifest(path, "e06-context", label, max(ledgers_by_path.get(path, []), key=lambda row: bool(_grade_from_ledger(row)), default=None))

    # Ten damaged host snapshots were confirmed intact by content-addressed
    # SHA-256. Mine their allow-listed members and preserve the verification.
    object_by_sha = {row.get("sha256"): row for row in object_rows if row.get("valid") is True}
    for row in object_rows:
        experiment = row.get("experiment")
        mapping = _object_round_mapping(experiment) if isinstance(experiment, str) else None
        if mapping is None:
            continue
        round_id, source_label = mapping
        meta = object_map.get(experiment)
        if not meta:
            continue
        object_root = studio / "bench-evidence" / f"{meta['sha256']}.tar.zst"
        if not object_root.is_dir():
            continue
        for path in object_root.rglob("manifest.json"):
            add_manifest(path, _safe_round(round_id, round_ids), source_label)

    # The codex-jobs x-ladder rung ledger contains separate ladder-stage
    # outcomes not represented by the HC result directories.
    x_ladder_jobs = bench / "codex-jobs" / "x-ladder"
    if x_ladder_jobs.is_dir():
        for path in x_ladder_jobs.rglob("manifest.json"):
            add_manifest(path, "x-ladder", "x-ladder-rung-ledger")

    # e09-tidewave's structured result ledger is the row-level grade source.
    e09_path = bench / "codex-jobs" / "e09-tidewave" / "results.json"
    if e09_path.is_file():
        for row in mp.read_json(e09_path):
            if not isinstance(row, dict):
                continue
            path = _resolve_source_path(studio, row.get("manifest"))
            if path is None:
                unresolved_refs += 1
                continue
            outcome = _classification(row.get("outcome"))
            ledger = {
                "outcome": outcome,
                "status": row.get("status"),
                "wall_s": row.get("wall_s"),
                "usage": row.get("usage"),
                "task": row.get("task"),
                "rep": row.get("rep"),
                "arm": row.get("arm"),
            }
            add_manifest(path, "e09-tidewave", f"e09-tidewave-{row.get('arm') or 'unknown-arm'}", ledger)

    # Night grades join only when the exact patch SHA-256 matches a retained
    # Studio output patch. Unmatched grade logs are not copied or guessed.
    night_root = bench / "night-2026-10-01"
    grades_by_patch: dict[str, list[dict[str, Any]]] = defaultdict(list)
    if (night_root / "grading").is_dir():
        for path in (night_root / "grading").glob("*results.jsonl"):
            for row in mp.read_jsonl(path):
                digest = row.get("patch_sha256")
                if isinstance(digest, str) and mp.HEX_SHA256.fullmatch(digest):
                    grades_by_patch[digest.lower()].append(row)
    night_patch_grade_conflicts: dict[str, dict[str, Any]] = {}
    for digest, matches in grades_by_patch.items():
        outcomes_for_patch = sorted({
            outcome for outcome in (_classification(row.get("outcome")) for row in matches)
            if outcome is not None
        })
        if len(outcomes_for_patch) > 1:
            grade_ids = sorted({
                label for label in (mp.safe_label(row.get("id"), identifier=True) for row in matches)
                if label
            })
            tasks = sorted({
                label for label in (mp.safe_label(row.get("task")) for row in matches)
                if label
            })
            night_patch_grade_conflicts[digest] = {
                "patch_sha256": digest,
                "grade_record_ids": grade_ids,
                "tasks": tasks,
                "outcomes": outcomes_for_patch,
                "grade_rows": len(matches),
                "retained_result_patch_match": False,
            }
    night_patch_join_count = 0
    if (night_root / "results").is_dir():
        for path in (night_root / "results").rglob("manifest.json"):
            patch_grades: list[dict[str, Any]] = []
            patch_hashes = {_digest(patch) for patch, _attempt in mp._patch_paths(path.parent)}
            for patch_hash in patch_hashes:
                patch_grades.extend(grades_by_patch.get(patch_hash, []))
                if patch_hash in night_patch_grade_conflicts:
                    night_patch_grade_conflicts[patch_hash]["retained_result_patch_match"] = True
            outcomes = {_classification(row.get("outcome")) for row in patch_grades}
            outcomes.discard(None)
            selected = None
            if len(outcomes) == 1:
                selected = {
                    "outcome": next(iter(outcomes)),
                    "status": "graded",
                    "task": (patch_grades[0].get("task") if patch_grades else None),
                }
                night_patch_join_count += 1
            add_manifest(path, "night-2026-10-01", _manifest_label(path, studio), selected)

    # Studio reference rows are grader controls, not model executions. Keep
    # them separately typed in the existing L1 control round.
    l1_reference_rows: list[dict[str, Any]] = []
    for result_path in sorted((night_root / "grading").glob("probe-stu-reference-*-results.jsonl")):
        for row in mp.read_jsonl(result_path):
            outcome = _classification(row.get("outcome")) or _classification(row.get("pass_"))
            raw_id = mp.safe_label(row.get("id"), identifier=True)
            if not raw_id or not outcome:
                continue
            source_label = "night-stu-reference-controls"
            source_key = hashlib.sha256(
                ("l1-task-grader-trust\0" + source_label + "\0" + raw_id + "\0" + outcome).encode("utf-8")
            ).hexdigest()
            l1_reference_rows.append({
                "schema_version": 1,
                "source_cell_key": source_key,
                "cell_id": raw_id,
                "source_cell_id": raw_id,
                "round": "l1-task-grader-trust",
                "source_experiment": source_label,
                "source_experiments": [source_label],
                "source_record_type": "grader_control_result",
                "source_manifest_sha256": None,
                "source_payload_sha256": _digest(result_path),
                "source_copy_count": 1,
                "arm": mp.safe_label(row.get("control")) or "reference-control",
                "task": mp.safe_label(row.get("task")),
                "rep": None,
                "model": None,
                "effort": None,
                "harness": None,
                "status": None,
                "wall_s": None,
                "usage": {key: None for key in mp.TOKEN_FIELDS},
                "official_grade": mp._grade_fields({"outcome": outcome, "tests_ran": row.get("tests_ran")}),
                "grade_join": "grader_control_result",
                "published_export": False,
                "raw_cell_present": False,
                "manifest_present": False,
                "prompt_sha256": None,
                "base_sha": {},
                "versions": {},
                "patches": [],
            })
    candidates.extend({
        "round": "l1-task-grader-trust",
        "source_label": "night-stu-reference-controls",
        "manifest_path": None,
        "manifest_sha256": None,
        "patch_hashes": (),
        "record": row,
        "patch_sources": [],
        "ledger": {},
        "rank": (1, 0, 0),
    } for row in l1_reference_rows)

    # The e06 packet's grade settlement cross-checks the one retained HC
    # manifest. Grader wall time is deliberately never treated as model wall.
    packet_root = studio.parent / "icloud" / "B028-v1" / "evidence" / "e06"
    e06_checks: dict[str, Any] = {}
    if packet_root.is_dir():
        grade_settlement = mp.read_json(packet_root / "grade-settlement.json") if (packet_root / "grade-settlement.json").is_file() else {}
        final_settlement = mp.read_json(packet_root / "FINAL-SETTLEMENT.json") if (packet_root / "FINAL-SETTLEMENT.json").is_file() else {}
        packet_rows = mp.read_json(packet_root / "graded-results.json") if (packet_root / "graded-results.json").is_file() else []
        packet_hashes = {
            row.get("manifest_sha256") for row in packet_rows
            if isinstance(row, dict) and mp.HEX_SHA256.fullmatch(str(row.get("manifest_sha256") or ""))
        }
        studio_e06_hashes = {
            item.get("manifest_sha256") for item in candidates
            if item.get("round") == "e06-context" and item.get("manifest_sha256")
        }
        e06_checks = {
            "settlement_cell_id": mp.safe_label(grade_settlement.get("id"), identifier=True),
            "grade_settlement_pass": grade_settlement.get("pass_"),
            "grader_wall_s": mp.nonnegative_number(grade_settlement.get("grade_wall_s")),
            "effective_compactions": final_settlement.get("effective_compactions"),
            "complete_adjacent_pairs": final_settlement.get("complete_adjacent_pairs"),
            "packet_manifest_sha256_matches_studio": bool(packet_hashes & studio_e06_hashes),
        }

    # The archived x-race summary is retained as a safe aggregate check. Only
    # explicit scalar totals are emitted; nested receipts and paths are ignored.
    x_race_summary: dict[str, Any] = {}
    x_race_results_path = bench / "codex-jobs" / "x-race" / "results.json"
    if x_race_results_path.is_file():
        x_race_doc = mp.read_json(x_race_results_path)
        rows = x_race_doc.get("rows", []) if isinstance(x_race_doc, dict) else []
        result_counts = Counter(str(row.get("result")) for row in rows if isinstance(row, dict))
        per_arm: dict[str, Counter[str]] = defaultdict(Counter)
        task_rep_arm = set()
        for row in rows:
            if not isinstance(row, dict):
                continue
            arm = str(row.get("arm") or "(unlabeled)")
            per_arm[arm][str(row.get("result") or "unknown")] += 1
            task_rep_arm.add((arm, str(row.get("task")), str(row.get("rep"))))
        summary = x_race_doc.get("summary", {}) if isinstance(x_race_doc, dict) else {}
        aggregate_summary: dict[str, Any] = {}
        if isinstance(summary, dict):
            for condition in ("equal", "time"):
                condition_data = summary.get(condition)
                if not isinstance(condition_data, dict):
                    continue
                arms = condition_data.get("arms") if isinstance(condition_data.get("arms"), dict) else {}
                aggregate_summary[condition] = {
                    "status": condition_data.get("status"),
                    "completed_pairs": condition_data.get("paired_cells"),
                    "paired_tasks": condition_data.get("paired_tasks"),
                    "arms": {
                        str(arm): {
                            key: arm_data.get(key)
                            for key in ("completed", "scored", "tasks", "accepted", "infra")
                            if isinstance(arm_data, dict) and isinstance(arm_data.get(key), (int, float, bool, str))
                        }
                        for arm, arm_data in arms.items()
                    },
                }
        x_race_summary = {
            "result_ledger_rows": len(rows),
            "unique_arm_task_rep_keys": len(task_rep_arm),
            "row_outcomes": dict(sorted(result_counts.items())),
            "outcomes_by_arm": {arm: dict(sorted(counts.items())) for arm, counts in sorted(per_arm.items())},
            "aggregate_summary": aggregate_summary,
        }

    kh_summary_studio = results_root / "kh-compare-2026-09-29" / "summary.json"
    kh_summary_macbook = studio.parent / "macbook" / "bench-review" / "studio" / "summary.json"
    kh_summary_copies_match = (
        kh_summary_studio.is_file() and kh_summary_macbook.is_file()
        and _digest(kh_summary_studio) == _digest(kh_summary_macbook)
    )

    # No safe per-cell records exist for the kh-climb, x-compaction, or
    # x-continuation sources: those folders contain summary state, patches, or
    # logs only. The source README update records this limitation explicitly.

    # Merge exact duplicate manifests while preserving all observed source
    # labels. A differing manifest or patch hash stays as a separate row.
    deduped: dict[tuple[str, str | None, tuple[str, ...]], dict[str, Any]] = {}
    for item in candidates:
        if item["manifest_sha256"] is None:
            key = (item["round"], None, (item["record"]["source_cell_key"],))
        else:
            key = (item["round"], item["manifest_sha256"], item["patch_hashes"])
        prior = deduped.get(key)
        if prior is None:
            item["source_labels"] = [item["source_label"]]
            deduped[key] = item
            continue
        if item["source_label"] not in prior["source_labels"]:
            prior["source_labels"].append(item["source_label"])
        prior["record"]["source_copy_count"] += 1
        if item["rank"] > prior["rank"]:
            merged_labels = prior["source_labels"]
            copy_count = prior["record"]["source_copy_count"]
            deduped[key] = item
            item["source_labels"] = merged_labels
            item["record"]["source_copy_count"] = copy_count

    by_round: dict[str, list[dict[str, Any]]] = defaultdict(list)
    patch_sources_by_round: dict[str, list[tuple[Path, str]]] = defaultdict(list)
    for item in deduped.values():
        record = item["record"]
        labels = sorted(set(item.get("source_labels", [item["source_label"]])))
        record["source_experiments"] = [mp.safe_label(label) for label in labels]
        record["source_experiments"] = [label for label in record["source_experiments"] if label]
        record["source_experiment"] = record["source_experiments"][0] if record["source_experiments"] else "studio-source"
        by_round[item["round"]].append(record)
        if item["patch_sources"]:
            patch_sources_by_round[item["round"]].extend(item["patch_sources"])

    hp_regrade_mismatches = []
    if hp_regrade_rows:
        hp_rows = by_round.get("harness-pick-2026-09-29", [])
        for regrade in hp_regrade_rows:
            if not regrade.get("cell_id"):
                continue
            matches = [row for row in hp_rows if row.get("source_cell_id") == regrade["cell_id"]]
            for row in matches:
                row["source_regrade"] = {
                    "original_outcome": regrade.get("original_outcome"),
                    "regraded_outcome": regrade.get("regraded_outcome"),
                }
                official = (row.get("official_grade") or {}).get("classification") if isinstance(row.get("official_grade"), dict) else None
                original = regrade.get("original_outcome")
                regraded = regrade.get("regraded_outcome")
                if regraded and (
                    (official and regraded != official)
                    or (original and regraded != original)
                ):
                    row["source_regrade_mismatch"] = {
                        "summary_outcome": official,
                        "original_outcome": original,
                        "regraded_outcome": regraded,
                    }
                    hp_regrade_mismatches.append({
                        "cell_id": regrade["cell_id"],
                        "summary_outcome": official,
                        "original_outcome": original,
                        "regraded_outcome": regraded,
                    })

    # Keep duplicate source cell IDs distinct in the row file while retaining
    # the original ID for explicit cohort cross-checks.
    for round_id, rows in by_round.items():
        counts = Counter(str(row.get("source_cell_id") or row.get("cell_id")) for row in rows)
        for row in rows:
            original_id = str(row.get("source_cell_id") or row.get("cell_id"))
            if counts[original_id] > 1:
                synthetic = f"{original_id}--studio-{row['source_cell_key'][:8]}"
                row["cell_id"] = synthetic[:512]

    source_grade_mismatches = []
    for round_id, rows in sorted(by_round.items()):
        for row in rows:
            mismatch = row.get("source_grade_mismatch")
            if isinstance(mismatch, dict):
                source_grade_mismatches.append({
                    "round": round_id,
                    "source_cell_id": row.get("source_cell_id"),
                    "source_experiment": row.get("source_experiment"),
                    **mismatch,
                })

    # These source pairs have a documented identity relationship. Other
    # repeated IDs belong to separately named experiments and are not joined.
    comparison_pairs = {
        "harness-compare-1": (
            ("harness-compare-1", "harness-compare-1-prelim"),
        ),
        "claim-b-screen-1": (
            ("claim-b-screen-1", "claim-b-screen-1-object"),
        ),
        "claim-b-rerun-1": (
            ("claim-b-rerun-1", "claim-b-rerun-1-worker-object"),
        ),
    }
    source_variant_mismatches = []
    for round_id, source_pairs in comparison_pairs.items():
        rows_by_id: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
        for row in by_round.get(round_id, []):
            source_id = str(row.get("source_cell_id") or "")
            source = str(row.get("source_experiment") or "")
            if source_id and source in {label for pair in source_pairs for label in pair}:
                rows_by_id[source_id][source] = row
        for source_id, source_rows in sorted(rows_by_id.items()):
            for left_label, right_label in source_pairs:
                left = source_rows.get(left_label)
                right = source_rows.get(right_label)
                if not left or not right:
                    continue
                left_outcome = (left.get("official_grade") or {}).get("classification") if isinstance(left.get("official_grade"), dict) else None
                right_outcome = (right.get("official_grade") or {}).get("classification") if isinstance(right.get("official_grade"), dict) else None
                if left_outcome != right_outcome:
                    source_variant_mismatches.append({
                        "round": round_id,
                        "source_cell_id": source_id,
                        "left_source": left_label,
                        "left_outcome": left_outcome or "ungraded",
                        "right_source": right_label,
                        "right_outcome": right_outcome or "ungraded",
                    })

    output.mkdir(parents=True, exist_ok=True)
    round_summary: dict[str, Any] = {}
    for round_id, rows in sorted(by_round.items()):
        rows.sort(key=lambda row: (str(row.get("source_experiment")), str(row.get("source_cell_id")), str(row.get("source_cell_key"))))
        mp._write_jsonl_gz(output / f"{round_id}.jsonl.gz", rows)
        outcomes = Counter(
            ((row.get("official_grade") or {}).get("classification") if isinstance(row.get("official_grade"), dict) else "ungraded")
            or "unknown" for row in rows
        )
        sources: dict[str, Counter[str]] = defaultdict(Counter)
        for row in rows:
            label = str(row.get("source_experiment") or "studio-source")
            grade = row.get("official_grade") if isinstance(row.get("official_grade"), dict) else {}
            sources[label][str(grade.get("classification") or "ungraded")] += 1
        round_summary[round_id] = {
            "records": len(rows),
            "outcomes": dict(sorted(outcomes.items())),
            "source_experiments": {label: dict(sorted(counts.items())) for label, counts in sorted(sources.items())},
            "patch_records": sum(len(row.get("patches", [])) for row in rows),
            "credential_excluded_patch_records": sum(
                1 for row in rows for patch in row.get("patches", [])
                if "credential_marker" in (patch.get("archive_exclusion_reasons") or [])
            ),
        }

    archive_summary = []
    patches_dir = output / "patches"
    for round_id, sources in sorted(patch_sources_by_round.items()):
        unique_sources = {}
        for path, member in sources:
            unique_sources[member] = (path, member)
        staged_archive = output / f"{round_id}.tar.zst"
        compressed_bytes = mp._write_patch_archive(zstd, staged_archive, list(unique_sources.values()))
        if compressed_bytes > mp.MAX_PATCH_ARCHIVE_BYTES:
            staged_archive.unlink()
            for row in by_round[round_id]:
                for patch in row.get("patches", []):
                    if patch.get("archive_member"):
                        patch["archive_member"] = None
                        patch["archive_exclusion_reasons"] = ["archive_over_300mb"]
            # Rewrite records after removing the unshipped archive members.
            mp._write_jsonl_gz(output / f"{round_id}.jsonl.gz", by_round[round_id])
            archive_summary.append({"round": round_id, "files": len(unique_sources), "compressed_bytes": compressed_bytes, "written": False})
            continue
        patches_dir.mkdir(parents=True, exist_ok=True)
        destination = patches_dir / f"{round_id}.tar.zst"
        staged_archive.replace(destination)
        archive_summary.append({"round": round_id, "files": len(unique_sources), "compressed_bytes": compressed_bytes, "written": True})

    object_provenance = []
    for row in object_rows:
        source_label = "damaged-host snapshot"
        experiment = row.get("experiment")
        mapping = _object_round_mapping(experiment) if isinstance(experiment, str) else None
        if mapping is not None:
            _round_id, source_label = mapping
        object_provenance.append({
            "source": source_label,
            "sha256": row.get("sha256"),
            "bytes": row.get("bytes"),
            "verified_against_content_address": row.get("valid") is True,
        })
    provenance_path = output / "STUDIO-SOURCES.json"
    provenance_path.write_text(json.dumps({
        "source": "read-only Mac Studio and iCloud staged records",
        "source_files_filtered": ["manifest.json", "cells.json", "cells.jsonl", "patch.diff", "grade result rows", "selected settlement metadata"],
        "excluded_source_classes": ["transcripts", "rollouts", "request logs", "grader tails", "build worktrees"],
        "verified_content_addressed_objects": object_provenance,
        "e06_packet_cross_check": e06_checks,
        "unresolved_manifest_references": unresolved_refs,
        "cells_ledger_only_rows": ledger_only_count,
        "night_exact_patch_grade_joins": night_patch_join_count,
        "night_patch_grade_conflicts": [
            night_patch_grade_conflicts[key] for key in sorted(night_patch_grade_conflicts)
        ],
        "l1_studio_reference_control_rows": len(l1_reference_rows),
        "l1_studio_reference_control_outcomes": dict(sorted(Counter(
            (row.get("official_grade") or {}).get("classification", "unknown")
            for row in l1_reference_rows
        ).items())),
        "hp_syn40_regrade_rows": len(hp_regrade_rows),
        "hp_syn40_regrade_mismatches": hp_regrade_mismatches,
        "source_grade_mismatches": source_grade_mismatches,
        "source_variant_mismatches": source_variant_mismatches,
        "x_race_codex_job_aggregate": x_race_summary,
        "kh_compare_studio_macbook_summary_copies_match": kh_summary_copies_match,
        "rounds": round_summary,
        "patch_archives": archive_summary,
        "unmined_target_sources": {
            "kh-climb": "Only state-current.json and log rows were staged; log data are excluded and no per-cell manifests were found.",
            "x-compaction": "Only source patches were staged; no per-cell model records were found.",
            "x-continuation": "Only source patches were staged; the source reports no real model attempts.",
            "ctx-store": "The Studio Codex job is an offline query/store analysis with query and retrieval records, not model-cell execution records; request-level content was excluded from this per-cell model import.",
        },
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_entries = mp._write_manifest(output)
    return {
        "rounds": round_summary,
        "source_candidate_records": len(candidates),
        "deduplicated_records": sum(len(rows) for rows in by_round.values()),
        "verified_objects": len(object_provenance),
        "unresolved_manifest_references": unresolved_refs,
        "night_exact_patch_grade_joins": night_patch_join_count,
        "patch_archives": archive_summary,
        "manifest_entries": len(manifest_entries),
        "output_bytes": sum(path.stat().st_size for path in output.rglob("*") if path.is_file()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--studio", type=Path, default=DEFAULT_STUDIO, help="local filtered Studio scratch root")
    parser.add_argument("--output", type=Path, required=True, help="new staging output directory")
    parser.add_argument("--zstd", default="zstd")
    args = parser.parse_args()
    print(json.dumps(mine(args.studio, args.output, zstd=args.zstd), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
