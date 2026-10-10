#!/usr/bin/env python3
"""Print the first 16 SHA-256 hex digits for spec/ and conformance/.

Files are sorted by repository-relative POSIX path. Each hash record contains
the UTF-8 path length (unsigned 8-byte big-endian), path bytes, content length
(unsigned 8-byte big-endian), and exact file bytes. Ignore __pycache__ directories.
The hash includes this script and the deduplication report; do not embed the
result in those files, because doing so would change the result.
"""

import argparse
import hashlib
from pathlib import Path


def suite_sha(root):
    files = []
    for name in ("spec", "conformance"):
        directory = root / name
        if not directory.is_dir():
            raise ValueError(f"missing suite directory: {directory}")
        files.extend(path for path in directory.rglob("*")
                     if path.is_file() and "__pycache__" not in path.relative_to(root).parts)
    digest = hashlib.sha256()
    for path in sorted(files, key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()[:16]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2],
                        help="repository root (defaults to this script's repository)")
    args = parser.parse_args()
    print(suite_sha(args.root.resolve()))


if __name__ == "__main__":
    main()
