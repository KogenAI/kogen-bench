#!/usr/bin/env python3
"""Live driver: ONE Claude Code process for the whole cell (stream-json in/out), so hooks and MCP servers are
loaded once, as in a long interactive session. Sends each prompt of <plan.json> ([[kind, prompt], ...]) after the
previous turn's result; writes turns/NN-kind.json (the result event) and appends events.jsonl like run-cell.sh.
usage: live.py <cell dir> <plan.json> <per-turn timeout s> -- <cc2.py argv...>"""
import json, os, select, subprocess, sys, time

d, plan, tmo = sys.argv[1], json.load(open(sys.argv[2])), float(sys.argv[3])
cmd = sys.argv[sys.argv.index("--") + 1:]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(d + "/live.err", "w"), cwd=d)
raw = open(d + "/live.stream.jsonl", "w")
buf = b""
for n, (kind, prompt) in enumerate(plan, 1):
    t0 = time.time()
    p.stdin.write((json.dumps({"type": "user", "message": {"role": "user", "content": prompt}}) + "\n").encode())
    p.stdin.flush()
    res, rc = None, 0
    while res is None:
        left = tmo - (time.time() - t0)
        if left <= 0:
            rc = 124
            break
        r, _, _ = select.select([p.stdout], [], [], left)
        if not r:
            continue
        chunk = os.read(p.stdout.fileno(), 65536)
        if not chunk:
            rc = 1
            break
        buf += chunk
        while b"\n" in buf:
            line, buf = buf.split(b"\n", 1)
            raw.write(line.decode(errors="replace") + "\n")
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") == "result":
                res = ev
    raw.flush()
    f = "%02d-%s.json" % (n, kind)
    json.dump(res or {}, open(os.path.join(d, "turns", f), "w"))
    if res is not None and res.get("is_error"):
        rc = 1
    with open(d + "/events.jsonl", "a") as e:
        e.write(json.dumps({"n": n, "kind": kind, "t0": t0, "t1": time.time(), "rc": rc, "file": f}) + "\n")
    if rc in (1, 124) and res is None:
        break
p.stdin.close()
try:
    p.wait(30)
except subprocess.TimeoutExpired:
    p.terminate()
