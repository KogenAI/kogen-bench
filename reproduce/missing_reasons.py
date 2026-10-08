"""Shared compact missing-value encoding for public evidence JSONL files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEGEND_PATH = ROOT / "results" / "missing-reasons.json"


def load_legend(path: Path = LEGEND_PATH) -> dict[str, dict[str, str]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    codes = raw.get("codes")
    if raw.get("legend_schema_version") != "1.0" or not isinstance(codes, dict):
        raise ValueError("Malformed missing-reasons legend")
    pairs: dict[str, dict[str, str]] = {}
    for code, entry in codes.items():
        if (
            not isinstance(code, str)
            or not isinstance(entry, dict)
            or not isinstance(entry.get("reason"), str)
            or not isinstance(entry.get("reconstructable_from"), str)
        ):
            raise ValueError(f"Malformed missing-reason entry: {code!r}")
        pairs[code] = {
            "reason": entry["reason"],
            "reconstructable_from": entry["reconstructable_from"],
        }
    return pairs


def load_marker_to_code(path: Path = LEGEND_PATH) -> dict[tuple[str, str], str]:
    return {
        (entry["reason"], entry["reconstructable_from"]): code
        for code, entry in load_legend(path).items()
    }


def marker_pair(value: Any) -> tuple[str, str] | None:
    """Return the full marker pair from a verbose missing marker, if present."""
    if not isinstance(value, dict) or set(value) not in ({"missing"}, {"missing", "reconstructable_from"}):
        return None
    reason = value.get("missing")
    source = value.get("reconstructable_from", "none")
    if not isinstance(reason, str) or not isinstance(source, str):
        return None
    return reason, source


def compact_value(value: Any, marker_to_code: dict[tuple[str, str], str]) -> Any:
    if isinstance(value, dict) and set(value) == {"missing"} and value.get("missing") in marker_to_code.values():
        return value
    pair = marker_pair(value)
    if pair is not None:
        try:
            return {"missing": marker_to_code[pair]}
        except KeyError as exc:
            raise ValueError(f"Missing reason is absent from results/missing-reasons.json: {pair!r}") from exc
    if isinstance(value, dict):
        return {key: compact_value(item, marker_to_code) for key, item in value.items()}
    if isinstance(value, list):
        return [compact_value(item, marker_to_code) for item in value]
    return value


def expand_value(value: Any, codes: dict[str, dict[str, str]]) -> Any:
    if isinstance(value, dict) and set(value) == {"missing"} and value.get("missing") in codes:
        entry = codes[value["missing"]]
        return {
            "missing": entry["reason"],
            "reconstructable_from": entry["reconstructable_from"],
        }
    if isinstance(value, dict):
        return {key: expand_value(item, codes) for key, item in value.items()}
    if isinstance(value, list):
        return [expand_value(item, codes) for item in value]
    return value


def marker_code(value: Any, codes: dict[str, dict[str, str]]) -> str | None:
    """Return a known compact code, or None for a noncompact value."""
    if isinstance(value, dict) and set(value) == {"missing"}:
        code = value.get("missing")
        return code if isinstance(code, str) and code in codes else None
    return None


def compact_encoding_issues(
    value: Any,
    codes: dict[str, dict[str, str]],
    path: str = "$",
    *,
    allow_legacy_single: bool = False,
) -> list[str]:
    issues: list[str] = []
    if isinstance(value, dict):
        if set(value) == {"missing"}:
            code = value.get("missing")
            if allow_legacy_single and isinstance(code, str) and code not in codes:
                return issues
            if not isinstance(code, str) or code not in codes:
                issues.append(f"{path}: unknown compact missing code {code!r}")
            return issues
        if marker_pair(value) is not None:
            issues.append(f"{path}: verbose missing marker in compact data")
            return issues
        for key, item in value.items():
            issues.extend(compact_encoding_issues(item, codes, f"{path}.{key}", allow_legacy_single=allow_legacy_single))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            issues.extend(compact_encoding_issues(item, codes, f"{path}[{index}]", allow_legacy_single=allow_legacy_single))
    return issues
