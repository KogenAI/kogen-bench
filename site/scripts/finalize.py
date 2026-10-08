#!/usr/bin/env python3
"""Copy source data into the static output after Astro renders the pages."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


SITE = Path(__file__).resolve().parents[1]
ROOT = SITE.parent
DIST = SITE / "dist"
DATA = SITE / ".generated" / "site-data.json"


def copy_file(source_rel: str, dest_rel: str) -> None:
    source = ROOT / source_rel
    destination = DIST / dest_rel
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    for rel in data["meta"]["jsonl_files"]:
        copy_file(rel, f"downloads/{rel}")
    for rel in data["meta"].get("index_files", []):
        copy_file(rel, f"downloads/{rel}")
    for rel in data["meta"].get("json_files", []):
        copy_file(rel, f"downloads/{rel}")
    copy_file("rounds/index.json", "downloads/rounds/index.json")

    expected_markdown = {"/index.md" if page["route"] == "/" else f"{page['route'].rstrip('/')}.md" for page in data["pages"]}
    missing = [path for path in sorted(expected_markdown) if not (DIST / path.lstrip("/")).is_file()]
    if missing:
        raise SystemExit("Missing Markdown alternates from Astro output: " + ", ".join(missing[:20]))

    # Only page routes invoke negotiation; downloads and assets retain their responses.
    (DIST / "_routes.json").write_text(json.dumps({"version": 1, "include": ["/*"], "exclude": ["/downloads/*", "/fonts/*", "/js/*", "/_astro/*", "/*.md", "/*.json", "/*.txt", "/*.xml", "/favicon*", "/apple-touch-icon.png", "/og.png"]}) + "\n", encoding="utf-8")

    copied_indexes = len(data["meta"].get("index_files", [])) + 1
    copied_json = len(data["meta"].get("json_files", []))
    print(f"Copied {len(data['meta']['jsonl_files'])} JSONL files, {copied_indexes} indexes, and {copied_json} JSON files into site/dist/downloads/.")

    max_output_bytes = 25 * 1024 * 1024
    oversized = [
        (path, path.stat().st_size)
        for path in DIST.rglob("*")
        if path.is_file() and path.stat().st_size > max_output_bytes
    ]
    if oversized:
        details = ", ".join(f"{path.relative_to(DIST)} ({size} bytes)" for path, size in oversized[:10])
        raise SystemExit(f"Site output exceeds the 25 MiB per-file limit: {details}")


if __name__ == "__main__":
    main()
