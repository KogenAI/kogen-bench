#!/usr/bin/env python3
"""After a cell: copy each compaction summary out of the Claude Code session transcript into <cell>/summaries.jsonl,
with flags for whether the summary kept the marker / ticket / tag. usage: extract.py <cell dir> <claude config dir>"""
import glob, hashlib, json, os, sys

cell, cfgdir = sys.argv[1], sys.argv[2]
cfg = json.load(open(os.path.join(cell, "cell.json")))
sid = open(os.path.join(cell, "session.id")).read().strip()
marker = "SB-" + hashlib.sha256((cfg["brief_rev"] + cfg["nonce"]).encode()).hexdigest()[:8]
files = glob.glob(os.path.join(cfgdir, "projects", "*", sid + ".jsonl"))
out, after_boundary, n = [], False, 0


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
        after_boundary = True
        continue
    if after_boundary and r.get("type") == "user":
        t = text_of(r.get("message", {}).get("content", ""))
        n += 1
        out.append({"compaction": n, "chars": len(t), "kept_marker": marker in t, "kept_ticket": cfg["ticket"] in t,
                    "kept_tag": cfg["prefix"] in t, "summary": t})
        after_boundary = False
with open(os.path.join(cell, "summaries.jsonl"), "w") as f:
    for o in out:
        f.write(json.dumps(o) + "\n")
print(cell, "summaries:", n, "transcript:", "found" if files else "MISSING")
