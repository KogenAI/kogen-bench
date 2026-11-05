#!/usr/bin/env python3
"""After a phase 2 cell: copy each compaction summary out of the cell's own session transcript
(<cell>/cellhome/.claude/projects/*/<sid>.jsonl) into <cell>/summaries.jsonl with flags: kept_marker (marker/hash/nonce
value), receipts_kept (which issued receipts appear), kept_hook (hook-install text), kept_ticket, kept_tag.
usage: extract2.py <cell dir>"""
import glob, json, os, sys

cell = sys.argv[1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stub2  # noqa: E402
stub2.setup(cell)
cfg = stub2.CFG
sid = open(os.path.join(cell, "session.id")).read().strip()
mk = stub2.marker()
issued = (stub2.state() or {}).get("issued", [])
files = glob.glob(os.path.join(cell, "cellhome", ".claude", "projects", "*", sid + ".jsonl"))
out, after, n = [], False, 0


def text_of(c):
    if isinstance(c, str):
        return c
    return "\n".join(x.get("text", "") for x in c if isinstance(x, dict))


for line in open(files[0]) if files else []:
    try:
        r = json.loads(line)
    except ValueError:
        continue
    if r.get("type") == "system" and r.get("subtype") == "compact_boundary":
        after = True
        continue
    if after and r.get("type") == "user":
        t = text_of(r.get("message", {}).get("content", ""))
        n += 1
        out.append({"compaction": n, "chars": len(t), "kept_marker": bool(mk) and mk in t,
                    "receipts_kept": [i for i, x in enumerate(issued) if x in t], "receipts_issued": len(issued),
                    "kept_hook": "brief --loop" in t, "kept_ticket": cfg["ticket"] in t, "kept_tag": cfg["prefix"] in t,
                    "summary": t})
        after = False
with open(os.path.join(cell, "summaries.jsonl"), "w") as f:
    for o in out:
        f.write(json.dumps(o) + "\n")
print(cell, "summaries:", n, "transcript:", "found" if files else "MISSING")
