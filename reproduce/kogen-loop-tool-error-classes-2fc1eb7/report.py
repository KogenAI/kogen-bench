#!/usr/bin/env python3
"""report.py <sessions.tsv>: recompute the session and request counts behind the finding (standard library only)."""
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
print(f"scripted sessions: {len(rows)}")
print(f"recorded provider request bodies per version: {sum(int(r['requests_recorded']) for r in rows)}")
print(f"distinct tool calls scripted: {sum(int(r['tool_calls']) for r in rows if r['mode'] == 'batched')} (each session run batched and split)")
same = sum(r["byte_identical_across_pins"] == "yes" for r in rows)
print(f"sessions whose request bytes are identical across the three versions: {same} of {len(rows)}")
print("verdict: SAME on the scripted sessions" if same == len(rows) else "verdict: CHECK")
