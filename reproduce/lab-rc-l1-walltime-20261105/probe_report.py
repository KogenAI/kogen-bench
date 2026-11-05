#!/usr/bin/env python3
"""probe_report.py <out-probe dir> [--write DIR]: per-run time Verify spent before setup-1's command started ("prework_ms" lines in go test -json output)."""
import json, re, sys, os
out = sys.argv[1]
rows = []
for ln in open(os.path.join(out, "chunks.tsv")):
    cond, r, arm, t0, l5, l1, rc = ln.rstrip("\n").split("\t")
    idx = 0
    for l in open(os.path.join(out, f"{cond}-r{r}-{arm}.json")):
        e = json.loads(l)
        if e.get("Test") and e.get("Action") == "output":
            m = re.search(r"prework_ms=(\d+)", e["Output"])
            if m:
                idx += 1
                rows.append((r, arm, idx, t0, l5, l1, int(m.group(1))))
v = sorted(x[-1] for x in rows)
q = lambda p: v[min(len(v) - 1, int(p * len(v)))]
s = f"runs {len(v)}; prework_ms min {v[0]} p50 {q(.5)} p90 {q(.9)} p99 {q(.99)} max {v[-1]}; over 200 ms: {sum(x > 200 for x in v)}; over 300 ms: {sum(x > 300 for x in v)}; load5 {min(float(x[4]) for x in rows)}-{max(float(x[4]) for x in rows)}"
print(s)
if "--write" in sys.argv:
    d = sys.argv[sys.argv.index("--write") + 1]
    open(os.path.join(d, "probe-prework.tsv"), "w").write("round\tchunk\tidx\tchunk_start\tload5\tload1\tprework_ms\n" + "".join("\t".join(map(str, x)) + "\n" for x in rows))
    open(os.path.join(d, "probe-summary.txt"), "w").write(s + "\n")
