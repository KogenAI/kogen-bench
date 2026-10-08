#!/usr/bin/env python3
"""Read-only checks for the locally sanitized Kogen v1.2 clause snapshot."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_REVISION = "1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0"
SANITIZED_REVISION = "30d9b25e4eefa7117121de44298fed504b429f4e"
SOURCE_REPOSITORY = "https://github.com/KogenAI/kogen-spec"
SOURCE_VERSION = "v1.2"
MANIFEST_NAMES = {"SOURCE.json", "SHA256SUMS"}
BT = chr(96)
EVIDENCE_REFERENCE = re.compile(
    r"\bspec/([^#\s" + re.escape(BT) + r"<>();\]]+\.md)#([A-Za-z0-9_.%-]+)"
)
LINK = re.compile(r"\]\(([^)]+)\)")
FENCE = re.compile(r"^\s*(" + re.escape(BT) + r"{3,}|~{3,})")


def markdown_lines(text: str):
    fence_char = None
    fence_len = 0
    for line in text.splitlines():
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            if fence_char is None:
                fence_char, fence_len = marker[0], len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_len:
                fence_char, fence_len = None, 0
            continue
        if fence_char is None:
            yield line


def markdown_slug(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(re.escape(BT) + r"([^" + re.escape(BT) + r"]*)" + re.escape(BT), r"\1", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\s*\{#[^}]+\}\s*$", "", value)
    value = value.lower().strip()
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    return re.sub(r"\s+", "-", value)


def markdown_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in markdown_lines(text):
        anchors.update(re.findall(r"<a\s+(?:[^>]*\s)?(?:id|name)=['\"]([^'\"]+)['\"]", line, re.I))
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        heading = re.sub(r"\s*\{#[^}]+\}\s*$", "", match.group(1))
        explicit = re.search(r"\{#([^}]+)\}\s*$", match.group(1))
        if explicit:
            anchors.add(explicit.group(1))
        base = markdown_slug(heading)
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def evidence_fragments(evidence_map: str) -> set[tuple[str, str]]:
    visible = "\n".join(markdown_lines(evidence_map))
    return {
        (unquote(filename), unquote(fragment).rstrip(".,"))
        for filename, fragment in EVIDENCE_REFERENCE.findall(visible)
    }


def check_evidence_fragments(snapshot: Path, evidence_map_path: Path | None = None) -> tuple[list[str], int]:
    evidence_map_path = evidence_map_path or ROOT / "EVIDENCE-MAP.md"
    try:
        visible = "\n".join(markdown_lines(evidence_map_path.read_text(encoding="utf-8")))
    except OSError as exc:
        return [f"Cannot read EVIDENCE-MAP.md: {exc}"], 0
    references = {
        (unquote(filename), unquote(fragment).rstrip(".,"))
        for filename, fragment in EVIDENCE_REFERENCE.findall(visible)
    }
    if not references:
        return ["EVIDENCE-MAP.md contains no spec Markdown fragments to verify"], 0

    anchors_by_file: dict[str, set[str]] = {}
    errors: list[str] = []
    for path in snapshot.rglob("*.md"):
        relative = path.relative_to(snapshot).as_posix()
        try:
            anchors_by_file[relative] = markdown_anchors(path.read_text(encoding="utf-8"))
        except OSError as exc:
            errors.append(f"Cannot read spec snapshot file {relative}: {exc}")

    missing = sorted(
        f"spec/{filename}#{fragment}"
        for filename, fragment in references
        if filename not in anchors_by_file or fragment not in anchors_by_file[filename]
    )
    if missing:
        errors.append("EVIDENCE-MAP fragments missing from the vendored spec snapshot: " + ", ".join(missing))

    linked: set[tuple[str, str]] = set()
    for target in LINK.findall(visible):
        parsed = urlsplit(target.strip().strip("<>"))
        match = re.fullmatch(r"spec/(.+\.md)#(.+)", parsed.path + ("#" + parsed.fragment if parsed.fragment else ""))
        if match:
            linked.add((unquote(match.group(1)), unquote(match.group(2)).rstrip(".,")))
    unlinked = sorted(f"spec/{filename}#{fragment}" for filename, fragment in references - linked)
    if unlinked:
        errors.append("EVIDENCE-MAP fragments are not linked to their sources: " + ", ".join(unlinked))
    return errors, len(references)


def check_local_markdown_links(snapshot: Path) -> list[str]:
    errors: list[str] = []
    for page in snapshot.rglob("*.md"):
        try:
            text = page.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"Cannot read Markdown snapshot page {page.relative_to(snapshot)}: {exc}")
            continue
        for target in LINK.findall(text):
            parsed = urlsplit(target.strip().strip("<>"))
            if parsed.scheme or target.startswith("//"):
                continue
            destination = unquote(parsed.path)
            target_page = (page.parent / destination) if destination else page
            relative = page.relative_to(snapshot).as_posix()
            if not target_page.exists():
                errors.append(f"Broken local spec link in {relative}: {destination or target}")
                continue
            if parsed.fragment and target_page.is_file() and target_page.suffix.lower() == ".md":
                try:
                    anchors = markdown_anchors(target_page.read_text(encoding="utf-8"))
                except OSError as exc:
                    errors.append(f"Cannot read linked spec page {target_page.relative_to(snapshot)}: {exc}")
                    continue
                fragment = unquote(parsed.fragment)
                if fragment not in anchors:
                    errors.append(f"Broken local spec fragment in {relative}: {destination}#{fragment}")
    return errors


def safe_relative(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def check_manifests(snapshot: Path) -> list[str]:
    errors: list[str] = []
    try:
        source = json.loads((snapshot / "SOURCE.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot read spec snapshot SOURCE.json: {exc}"]
    try:
        sums_text = (snapshot / "SHA256SUMS").read_text(encoding="utf-8")
    except OSError as exc:
        return [f"Cannot read spec snapshot SHA256SUMS: {exc}"]

    expected_top_level = {
        "repository": SOURCE_REPOSITORY,
        "content_version": SOURCE_VERSION,
        "original_cited_revision": ORIGINAL_REVISION,
        "sanitized_published_revision": SANITIZED_REVISION,
        "snapshot_kind": "locally sanitized v1.2 clause-reference excerpt",
    }
    for key, value in expected_top_level.items():
        if source.get(key) != value:
            errors.append(f"Spec snapshot SOURCE.json has the wrong {key}")

    content_entries = source.get("published_content_hashes")
    if not isinstance(content_entries, list) or not content_entries:
        return errors + ["Spec snapshot SOURCE.json has no published-content hashes"]
    published: dict[str, str] = {}
    for row in content_entries:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str) or not isinstance(row.get("sha256"), str):
            errors.append("Spec snapshot SOURCE.json contains a malformed published-content hash")
            continue
        path, digest = row["path"], row["sha256"]
        if not safe_relative(path) or path in published or not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append("Spec snapshot SOURCE.json has an unsafe, duplicate, or malformed published path: " + path)
            continue
        published[path] = digest

    source_entries = source.get("original_source_hashes")
    if not isinstance(source_entries, list) or not source_entries:
        errors.append("Spec snapshot SOURCE.json omits original source hashes")
        source_entries = []
    original: dict[str, dict] = {}
    for row in source_entries:
        required = ("path", "source_path", "source_revision", "source_sha256")
        if not isinstance(row, dict) or not all(isinstance(row.get(key), str) for key in required):
            errors.append("Spec snapshot SOURCE.json contains a malformed original-source hash")
            continue
        path = row["path"]
        if not safe_relative(path) or path in original or row["source_revision"] != ORIGINAL_REVISION:
            errors.append("Spec snapshot SOURCE.json has an unsafe, duplicate, or mis-pinned original source path: " + path)
            continue
        if not re.fullmatch(r"[0-9a-f]{64}", row["source_sha256"]):
            errors.append("Spec snapshot SOURCE.json has a malformed original source hash: " + path)
            continue
        expected_source = "CLI-RULE.txt" if path == "CLI-RULE.txt" else (
            "quint/CLASSIFICATION.md" if path == "quint/CLASSIFICATION.md" else f"spec/{path}"
        )
        if row["source_path"] != expected_source:
            errors.append("Unexpected original spec source path for " + path)
        original[path] = row

    if set(original) != set(published):
        errors.append("Original-source and published-content inventories differ")

    actual_content = {
        path.relative_to(snapshot).as_posix()
        for path in snapshot.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    }
    if actual_content != set(published) | {"SOURCE.json"}:
        errors.append("Vendored spec snapshot inventory differs from SOURCE.json")

    required_files = {
        "01-cli.md", "02-formats.md", "03-build.md", "04-provider.md",
        "05-sandbox-custody.md", "06-non-goals.md", "CONFORMANCE.md",
        "CONFORMANCE-v1.2-CASES.md", "CLI-RULE.txt", "quint/CLASSIFICATION.md",
        "README.md", "data/constants.json", "data/lint.json",
        "data/moved.json", "data/yaml-errors.json",
    }
    if not required_files.issubset(published):
        errors.append("Spec snapshot omits required v1.2 clauses, normative data, or its landing page")

    for relative, digest in published.items():
        path = snapshot / relative
        if not path.is_file() or path.is_symlink():
            errors.append("Missing or non-regular vendored spec file: " + relative)
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            errors.append("Published spec byte hash mismatch: " + relative)

    checksums: dict[str, str] = {}
    for line_no, line in enumerate(sums_text.splitlines(), 1):
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            errors.append(f"Malformed SHA256SUMS row {line_no}")
            continue
        digest, path = match.groups()
        if not safe_relative(path) or path in checksums:
            errors.append("SHA256SUMS has an unsafe or duplicate path: " + path)
            continue
        checksums[path] = digest
    expected_sum_paths = set(published) | {"SOURCE.json"}
    if set(checksums) != expected_sum_paths:
        errors.append("SHA256SUMS inventory differs from the published snapshot inventory")
    for relative, digest in checksums.items():
        path = snapshot / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            errors.append("SHA256SUMS hash mismatch: " + relative)

    landing = snapshot / "README.md"
    if landing.is_file():
        text = landing.read_text(encoding="utf-8")
        for required in ("Included inventory", "Omitted upstream material", "Sources and precedence", ORIGINAL_REVISION, SANITIZED_REVISION, "decision ledger"):
            if required.lower() not in text.lower():
                errors.append("Spec snapshot landing page omits required provenance or navigation detail: " + required)
    return errors


def audit_snapshot(snapshot: Path, evidence_map_path: Path | None = None, *, fragments_only: bool = False) -> tuple[list[str], int]:
    errors, count = check_evidence_fragments(snapshot, evidence_map_path)
    errors.extend(check_local_markdown_links(snapshot))
    if not fragments_only:
        errors.extend(check_manifests(snapshot))
    return errors, count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, default=ROOT / "spec")
    parser.add_argument("--evidence-map", type=Path, default=ROOT / "EVIDENCE-MAP.md")
    parser.add_argument("--fragments-only", action="store_true", help="check fragments and navigation before manifests are written")
    args = parser.parse_args()
    errors, count = audit_snapshot(args.snapshot, args.evidence_map, fragments_only=args.fragments_only)
    if errors:
        for error in errors:
            print("SPEC SNAPSHOT: FAIL: " + error, file=sys.stderr)
        return 1
    if args.fragments_only:
        print(f"SPEC SNAPSHOT: PASS — {count} linked EVIDENCE-MAP fragments resolve.")
    else:
        print(f"SPEC SNAPSHOT: PASS — {count} linked v1.2 fragments resolve; provenance, local navigation, and published-byte hashes verify.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
