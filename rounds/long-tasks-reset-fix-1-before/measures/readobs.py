"""Context-reset and repeated-read measures from Kogen run logs (run logs are private; this script is published so the method can be read).
Usage: readobs.py <tasks dir> <run dir> [<run dir> ...]

Per cell: context resets by role; reads after a reset whose result is byte-identical (same sha256) to a read made before it (count, bytes)
and their estimated share of the resetting role's input (result tokens estimated as bytes / 3.0, times the later requests of that role,
over that role's total input); review source-part reads (review read_file calls of at least 4 KB after the review_source_evidence event);
read bytes per thousand lines of the task's start tree.
"""
import glob, json, os, sys, collections

READ = ("read_file", "shell", "search_text", "list_files")
SRC = (".ex", ".exs", ".go", ".js", ".ts", ".py", ".md", ".feature", ".qnt", ".json", ".yaml", ".yml", ".sh", ".toml")

def kloc(task_dir):
    n = 0
    for root, dirs, files in os.walk(os.path.join(task_dir, "start")):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "deps", "_build", "vendor", "dist")]
        for f in files:
            if f.endswith(SRC):
                try: n += sum(1 for _ in open(os.path.join(root, f), errors="ignore"))
                except OSError: pass
    return n / 1000.0

tasks, runs = sys.argv[1], sys.argv[2:]
per_task = collections.defaultdict(list)
for run in runs:
    for res in glob.glob(run + "/cells/*/*/*/result.json"):
        d = os.path.dirname(res); task = d.split("/cells/")[1].split("/")[0]
        r = json.load(open(res)); ev = []
        for l in open(d + "/run-log/log.jsonl"):
            try: ev.append(json.loads(l))
            except ValueError: pass
        inp = collections.Counter(); reqidx = collections.defaultdict(list)
        for i, e in enumerate(ev):
            if e.get("event") == "request":
                inp[e.get("role")] += (e.get("usage") or {}).get("input") or 0; reqidx[e.get("role")].append(i)
        resets = [(i, e.get("role")) for i, e in enumerate(ev) if e.get("event") == "window_reset"]
        def later(role, j):  # requests of this role after event j and before the next reset of the role (carry ends at a reset)
            nxt = min([i for i, r2 in resets if r2 == role and i > j] or [len(ev)])
            return max(1, sum(1 for q in reqidx[role] if j < q < nxt))
        reread = collections.Counter(); reread_tok = collections.Counter()
        for i, role in resets:
            name = "tool_call" if role == "build" else "review_tool_call"
            before = {(e.get("result") or {}).get("sha256") for j, e in enumerate(ev[:i]) if e.get("event") == name and e.get("name") in READ and isinstance(e.get("result"), dict)}
            for j, e in enumerate(ev[i + 1:], start=i + 1):
                if e.get("event") == name and e.get("name") in READ and isinstance(e.get("result"), dict) and e["result"].get("sha256") in before:
                    reread[role] += 1; reread_tok[role] += e["result"].get("bytes", 0) / 3.0 * later(role, j)
        rse = [i for i, e in enumerate(ev) if e.get("event") == "review_source_evidence"]
        parts = [(j, (e.get("result") or {}).get("bytes", 0)) for j, e in enumerate(ev) if rse and j > rse[0] and e.get("event") == "review_tool_call"
                 and e.get("name") == "read_file" and isinstance(e.get("result"), dict) and e["result"].get("bytes", 0) >= 4000]
        part_tok = sum(b / 3.0 * later("review", j) for j, b in parts)
        parts = [b for _, b in parts]
        rbytes = sum((e.get("result") or {}).get("bytes", 0) for e in ev if e.get("event") in ("tool_call", "review_tool_call") and e.get("name") in READ and isinstance(e.get("result"), dict))
        t = r.get("totals") or {}
        per_task[task].append({
            "cell": d.split("/cells/")[1], "outcome": r.get("outcome"), "wall_s": r.get("wall_s"), "cost": t.get("cost_usd"),
            "requests": dict(collections.Counter(ev[i].get("role") for v in reqidx.values() for i in v)),
            "resets": dict(collections.Counter(role for _, role in resets)),
            "post_reset_rereads": dict(reread),
            "reread_share_of_role_input": {k: round(reread_tok[k] / inp[k], 3) for k in reread_tok if inp[k]},
            "review_part_reads": len(parts), "review_part_bytes": sum(parts),
            "review_part_share_of_review_input": round(part_tok / inp["review"], 3) if inp["review"] else None,
            "read_bytes": rbytes})
out = {}
for task, cells in sorted(per_task.items()):
    k = kloc(os.path.join(tasks, task))
    rb = [c["read_bytes"] for c in cells]
    out[task] = {"kloc": round(k, 1), "read_bytes_per_kloc_median": round(sorted(rb)[len(rb) // 2] / k) if k else None, "cells": cells}
    big = [c for c in cells if any(v > 0.10 for v in c["reread_share_of_role_input"].values())]
    out[task]["cells_with_reread_share_over_10pct"] = len(big)
print(json.dumps(out, indent=1))
tasks_over = sum(1 for v in out.values() if v["cells_with_reread_share_over_10pct"] > 0)
print(f"# tasks with post-reset re-reads >10% of a resetting session's input: {tasks_over} (ledger arm needs >= 2)")
