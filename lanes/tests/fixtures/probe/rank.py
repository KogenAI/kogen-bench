"""Fake probe: answers with the ranking the item names under args.key; records what it was given."""
import json
import os
import sys

req = json.load(sys.stdin)
out = {"ranked": req["input"][req["args"]["key"]],
       "seen": {"stdin_keys": sorted(req), "item_dir": os.path.basename(os.environ["LANES_PROBE_ITEM_DIR"]),
                "corpus": os.environ["LANES_CORPUS"], "cwd": os.getcwd()}}
if req["args"].get("marker"):
    open(req["args"]["marker"], "a").write("ran\n")
print(json.dumps({"output": out}))
