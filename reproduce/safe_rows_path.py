"""Resolve the approved sanitizer, tolerating inaccessible machine paths."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


HOST_SAFE_ROWS = Path("/root/Areas/Kogen/bench-manager/rz1-pack/rz1-export/levers/lib/safe_rows.py")


def default_candidates() -> tuple[Path, ...]:
    """Return the repository copy first, followed by supported host copies."""
    local = Path(__file__).resolve().with_name("safe_rows.py")
    candidates = [local, HOST_SAFE_ROWS]
    try:
        candidates.append(
            Path.home() / "Areas/Kogen/bench-manager/rz1-pack/rz1-export/levers/lib/safe_rows.py"
        )
    except (OSError, RuntimeError):
        pass
    return tuple(candidates)


def resolve_safe_rows_path(candidates: Iterable[Path] | None = None) -> Path | None:
    """Choose the first regular, non-symlink helper; inaccessible paths are absent."""
    for candidate in default_candidates() if candidates is None else candidates:
        try:
            if candidate.is_file() and not candidate.is_symlink():
                return candidate
        except OSError:
            continue
    return None
