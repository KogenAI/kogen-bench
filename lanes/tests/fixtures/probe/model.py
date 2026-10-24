"""Fake probe that reports one small model call, so its lane counts as a lane with usage."""
import json
import sys

req = json.load(sys.stdin)
print(json.dumps({"output": {"ranked": req["input"]["rank_a"]},
                  "usage": [{"model": "gpt-6-luna", "provider": "openai", "input_tokens": 10,
                             "cached_input_tokens": 0, "output_tokens": 5, "reasoning_tokens": 0}]}))
