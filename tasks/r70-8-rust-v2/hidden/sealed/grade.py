from __future__ import annotations
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent
candidate = Path(sys.argv[1]).resolve()
suite = root / "test_hidden.py"
env = os.environ.copy()
env["KOGEN_TASK_BIN"] = str(candidate / "run")
env["PYTHONDONTWRITEBYTECODE"] = "1"
env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
with tempfile.TemporaryDirectory(prefix="r70-task8-grade-") as temp:
    report = Path(temp) / "junit.xml"
    command = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--junitxml", str(report), str(suite)]
    completed = subprocess.run(command, cwd=candidate, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    try:
        root_xml = ET.parse(report).getroot()
        suites = [root_xml] if root_xml.tag == "testsuite" else root_xml.findall("testsuite")
        result = {name: sum(int(suite.attrib.get(name, "0")) for suite in suites) for name in ("tests", "failures", "errors", "skipped")}
    except Exception:
        result = {"tests": 0, "failures": 0, "errors": 1, "skipped": 0}
    result["passed"] = completed.returncode == 0 and result["tests"] == 25 and not result["failures"] and not result["errors"] and not result["skipped"]
    print(json.dumps(result, separators=(",", ":")))
    raise SystemExit(0 if result["passed"] else 1)
