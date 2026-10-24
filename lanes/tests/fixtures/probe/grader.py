"""Fake `command` grader: scores how many items the output lists; shows it received `expected`."""
import json
import sys

req = json.load(sys.stdin)
print(json.dumps({"listed": len(req["output"].get("ranked", [])), "has_expected": float("expected" in req["item"])}))
