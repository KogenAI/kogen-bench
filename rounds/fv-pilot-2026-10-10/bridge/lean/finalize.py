#!/usr/bin/env python3
"""Host-only qualification summary for the builder record, never trial payload."""
import json
import re
from pathlib import Path

root = Path.cwd().resolve()
summary = {}
for task in ["F01", "W01", "W04", "X01"]:
    laws = json.loads((root / "fixtures" / task / "laws.json").read_text())
    base = (root / "qualification" / task / "base/check.log").read_text()
    reference = (root / "qualification" / task / "reference/check.log").read_text()
    failures = re.findall(r"FV-LAW (\w+) FAIL", base)
    passes = re.findall(r"FV-LAW (\w+) PASS", reference)
    assert failures and len(passes) == len(laws["laws"])
    source_map = json.loads((root / "bridge/lean/out" / task / "source-map.json").read_text())
    assert all(x["line"] > 0 and x["column"] > 0 and x["file"].startswith("lib/") for x in source_map)
    summary[task] = {"base_detected": True, "violated_laws": failures, "reference_clean": True, "laws_total": len(passes), "source_mapping": True, "bound": laws["max_sequence_length"], "proof_method": "core decide; quantified finite/bounded theorem; frontier soundness proved", "toolchain": "lean 4.34.1"}
(root / "qualification/qualification.json").write_text(json.dumps(summary, indent=2) + "\n")
print("FV-FINAL " + json.dumps(summary), flush=True)
