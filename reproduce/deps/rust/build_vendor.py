#!/usr/bin/env python3
"""Rebuild the offline Cargo vendor directory from vendor.tsv (dir, crate, version, crates.io SHA-256).

Each .crate is downloaded from crates.io, verified against its pinned SHA-256, unpacked into
<dest>/<dir>, and given the .cargo-checksum.json that Cargo's directory source requires.
Usage: build_vendor.py DEST CACHE_DIR
"""
import hashlib
import json
import shutil
import sys
import tarfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Written verbatim by `cargo vendor`, so rebuilt trees match the original byte for byte.
# `cargo vendor` drops these names wherever they occur in a package.
SKIPPED = {".cargo-ok", ".git", ".gitattributes", ".gitignore"}
COMMENT = ("This file only protects against accidental modifications. It is not a security mechanism "
           "and does not protect against malicious changes.")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(name: str, version: str, expected: str, cache: Path) -> Path:
    path = cache / f"{name}-{version}.crate"
    if not path.is_file() or sha256(path.read_bytes()) != expected:
        url = f"https://static.crates.io/crates/{name}/{name}-{version}.crate"
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
        if sha256(data) != expected:
            raise SystemExit(f"SHA-256 mismatch for {name} {version}")
        path.write_bytes(data)
    return path


def main() -> int:
    dest, cache = Path(sys.argv[1]), Path(sys.argv[2])
    cache.mkdir(parents=True, exist_ok=True)
    staging = dest.with_name(dest.name + ".partial")
    shutil.rmtree(staging, ignore_errors=True)
    staging.mkdir(parents=True)
    rows = [line.split("\t") for line in (HERE / "vendor.tsv").read_text().splitlines() if line.strip()]
    for directory, name, version, expected in rows:
        crate = fetch(name, version, expected, cache)
        target = staging / directory
        prefix = f"{name}-{version}/"
        with tarfile.open(crate, "r:gz") as archive:
            members = [m for m in archive.getmembers() if m.isfile() and m.name.startswith(prefix)]
            files = {}
            for member in members:
                rel = member.name[len(prefix):]
                relative = Path(rel)
                if relative.is_absolute() or ".." in relative.parts:
                    raise SystemExit(f"unsafe archive path: {member.name}")
                if not rel or SKIPPED & set(rel.split("/")):
                    continue
                out = target / relative
                if not out.resolve().is_relative_to(target.resolve()):
                    raise SystemExit(f"unsafe archive path: {member.name}")
                data = archive.extractfile(member).read()
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(data)
                out.chmod(0o755 if member.mode & 0o111 else 0o644)
                files[rel] = sha256(data)
        checksum = {"$comment": COMMENT, "files": dict(sorted(files.items())), "package": expected}
        (target / ".cargo-checksum.json").write_text(json.dumps(checksum, separators=(",", ":")))
    old = dest.with_name(dest.name + ".old")
    shutil.rmtree(old, ignore_errors=True)
    if dest.exists():
        dest.rename(old)
    staging.rename(dest)
    shutil.rmtree(old, ignore_errors=True)
    print(f"vendored {len(rows)} crates into {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
