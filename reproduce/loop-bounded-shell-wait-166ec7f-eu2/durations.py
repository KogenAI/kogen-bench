#!/usr/bin/env python3
"""Model-free shell command durations from counted cells (bcw B choice).
Per cell: events.jsonl (tool.call / request.started times, 1 s resolution),
tool-items.jsonl (call names, args prefix, output head), shell-timing.jsonl (float t,
shellwait also tool.result). Duration of a command:
 - shellwait: tool.call -> tool.result float t (exact, synchronous loop).
 - sync rounds (l3hard): tool.call -> next request.started (upper bound, +model-free overhead).
 - yield rounds (loopfx3/loopnp): 'exit status' result -> <=1 s; handle chain ->
   request.started after the retrieval that returned completed (upper bound)."""
import json, glob, sys, collections, re, datetime, csv
ROOT = sys.argv[1]
def ts(s): return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").timestamp()
rows = []
for cell in sorted(glob.glob(f"{ROOT}/confirmation-eu2-*/counted/cells/*/*/*")):
    parts = cell.split("/")
    rnd = parts[-6].split("-")[2]; task, rep, arm = parts[-3], parts[-2], parts[-1]
    try:
        ev = [json.loads(l) for l in open(cell + "/events.jsonl")]
        items = [json.loads(l) for l in open(cell + "/tool-items.jsonl")]
    except FileNotFoundError:
        continue
    calls = {}; outs = {}
    for d in items:
        if d.get("kind") == "call": calls[d["call_id"]] = d
        if d.get("kind") == "output": outs[d["call_id"]] = d["head"]
    reqs = sorted(ts(e["time"]) for e in ev if e.get("type") == "request.started")
    ctime = {e["call_id"]: ts(e["time"]) for e in ev if e.get("type") == "tool.call"}
    def next_req(t):
        for r in reqs:
            if r >= t + 0.5 or r > t: return r
        return None
    if rnd == "shellwait":
        st = [json.loads(l) for l in open(cell + "/shell-timing.jsonl")]
        start = {d["id"]: d["t"] for d in st if d["event"] == "tool.call"}
        for d in st:
            if d["event"] == "tool.result" and d["id"] in start:
                rows.append((rnd, task, rep, arm, d["t"] - start[d["id"]], "exact"))
        continue
    handles = {}
    for cid, c in calls.items():
        if c["name"] != "shell" or cid not in ctime: continue
        a = c["arguments"]; head = outs.get(cid, "")
        if '"handle"' in a[:12] or a.startswith('{"handle"'):
            m = re.search(r'"handle"\s*:\s*"([0-9a-f]+)', a)
            if m and '"status":"completed"' in head.replace(" ", "") or (m and head.startswith('{"exit_status"')):
                handles.setdefault(m.group(1), {})["done"] = ctime[cid]
            continue
        if head.startswith("exit status"):
            if rnd == "l3hard":
                n = next_req(ctime[cid]); rows.append((rnd, task, rep, arm, (n - ctime[cid]) if n else None, "upper"))
            else:
                rows.append((rnd, task, rep, arm, 1.0, "le1"))
        else:
            m = re.search(r'"handle"\s*:\s*"([0-9a-f]+)', head)
            if m: handles.setdefault(m.group(1), {})["start"] = ctime[cid]
    for h, v in handles.items():
        if "start" in v and "done" in v:
            n = next_req(v["done"]); rows.append((rnd, task, rep, arm, (n - v["start"]) if n else None, "chain"))
        elif "start" in v:
            rows.append((rnd, task, rep, arm, None, "never-completed"))
w = csv.writer(open(sys.argv[2], "w")); w.writerow(["round", "task", "rep", "arm", "seconds", "kind"]); w.writerows(rows)
def q(xs, p): xs = sorted(xs); return xs[min(len(xs)-1, int(p*len(xs)))]
by = collections.defaultdict(list)
for r in rows:
    if r[4] is not None: by[(r[0], r[1] if r[1].startswith("kogen") else "go-kits")].append(r[4])
print("round task n p50 p75 p90 | share<=5 <=10 <=15 <=20 <=30 <=60")
for k, xs in sorted(by.items()):
    print(k, len(xs), *(round(q(xs, p), 1) for p in (.5, .75, .9)), "|", *(f"{sum(x<=b for x in xs)/len(xs):.0%}" for b in (5, 10, 15, 20, 30, 60)))
print("never-completed handles:", sum(1 for r in rows if r[5] == "never-completed"))
