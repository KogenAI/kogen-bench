"""Fake probe like rank.py, with two switches: it fails on the item whose repo is args.fail_repo, and every run
fails while the environment variable PROBE_BREAK is set (to show how a failed rerun is reported)."""
import json
import os
import sys

req = json.load(sys.stdin)
if os.environ.get("PROBE_BREAK") or req["input"].get("repo") == req["args"].get("fail_repo"):
    sys.exit(2)
print(json.dumps({"output": {"ranked": req["input"][req["args"]["key"]]}}))
