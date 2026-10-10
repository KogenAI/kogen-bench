#!/usr/bin/env python3
"""Print the installed Codex version, pinned version, and resolved binary SHA-256."""
import hashlib
import os
import re
import subprocess
import sys

if len(sys.argv) != 3:
    raise SystemExit("usage: lane-codex-info.py CODEX_BINARY PINNED_VERSION")

binary, pinned = sys.argv[1:]
try:
    output = subprocess.check_output(
        [binary, "--version"], text=True, stderr=subprocess.STDOUT
    ).strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?)\b", output)
    binary_version = match.group(1) if match else "unknown"
except (OSError, subprocess.SubprocessError, UnicodeError):
    binary_version = "unknown"

try:
    resolved = os.path.realpath(binary)
    with open(resolved, "rb") as source:
        digest = hashlib.sha256(source.read()).hexdigest()
except OSError:
    digest = "unknown"

mismatch = not pinned or binary_version == "unknown" or pinned != binary_version
print(f"{pinned}\t{binary_version}\t{digest}\t{str(mismatch).lower()}")
