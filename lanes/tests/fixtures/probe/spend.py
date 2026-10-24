"""Fake probe that reports a model call it made: 1M input tokens of a priced model."""
import json
import sys

json.load(sys.stdin)
print(json.dumps({"output": {"ranked": []},
                  "usage": [{"model": "gpt-6-luna", "provider": "openai", "input_tokens": 1000000,
                             "cached_input_tokens": 0, "output_tokens": 0, "reasoning_tokens": 0}]}))
