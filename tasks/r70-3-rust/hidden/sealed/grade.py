#!/usr/bin/env python3
"""Run this task's sealed black-box acceptance suite against the current build."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    sealed = Path(__file__).resolve().parent
    env = os.environ.copy()
    env["KOGEN_TASK_BIN"] = str(Path.cwd() / "run")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(sealed / "test_hidden.py")],
        env=env,
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
