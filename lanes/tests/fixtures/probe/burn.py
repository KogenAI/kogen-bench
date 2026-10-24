"""Fake probe that uses about half a second of CPU and 80 MB of memory."""
import json
import sys
import time

json.load(sys.stdin)
blob = bytearray(80 * 1024 * 1024)
for i in range(0, len(blob), 4096):
    blob[i] = 1
end = time.process_time() + 0.5
while time.process_time() < end:
    sum(range(1000))
print(json.dumps({"output": {"ranked": []}}))
