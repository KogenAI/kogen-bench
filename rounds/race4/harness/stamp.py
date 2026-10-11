#!/usr/bin/python3
# stamp.py OUT_JSONL OUT_TS — pass Codex JSON events through unchanged to OUT_JSONL; write "epoch<TAB>type<TAB>item_id<TAB>item_type" to OUT_TS for timing
import sys, time, json
out = open(sys.argv[1], 'w', buffering=1); ts = open(sys.argv[2], 'w', buffering=1)
for line in sys.stdin:
    out.write(line)
    try:
        e = json.loads(line); it = e.get('item') or {}
        ts.write(f"{time.time():.3f}\t{e.get('type','')}\t{it.get('id','')}\t{it.get('type','')}\n")
    except Exception:
        pass
