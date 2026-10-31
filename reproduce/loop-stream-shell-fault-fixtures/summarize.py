#!/usr/bin/python3 -I
"""Model-free: print the fixture table and the checks behind the README from the raw rows.
usage: summarize.py results/summary.jsonl"""
import json, sys
rows = {}
for l in open(sys.argv[1]):
    r = json.loads(l); rows[r["scenario"]] = r
def attempts(r): return [a["outcome"] for a in r["attempts"]]
def end(r):
    e = r.get("error")
    return ("error " + e["class"] + "/" + e["reason"]) if e else ("ok (" + str(r.get("round_ended", {}).get("ending")) + ")")
print("%-16s %5s %8s  %-26s %s" % ("scenario", "exit", "wall_s", "attempts", "end"))
for n, r in rows.items():
    print("%-16s %5s %8.2f  %-26s %s" % (n, r["exit"], r["wall_s"], ",".join(attempts(r)), end(r)))
def within(n, lo, hi): return lo <= rows[n]["wall_s"] <= hi
checks = [
 ("productive controls never stopped (fb60, gap120, slow200, sh_slow_stream, sh_silent700)",
  all(rows[n]["exit"] == 0 and "failed" not in attempts(rows[n]) for n in ("fb60", "gap120", "slow200", "sh_slow_stream", "sh_silent700"))),
 ("headers alone are not a first byte: fb_hdr1 retried after 90 s (wall 92 s)", attempts(rows["fb_hdr1"]) == ["failed", "completed"] and within("fb_hdr1", 91.5, 92.5)),
 ("no byte on 3 attempts fails at 280 s", attempts(rows["fb_hang3"]) == ["failed"] * 3 and within("fb_hang3", 279, 281) and rows["fb_hang3"]["error"]["reason"] == "unavailable"),
 ("idle stop at 180 s: gap200, keepalive, trickle all 182 s with one retry",
  all(attempts(rows[n]) == ["failed", "completed"] and within(n, 181.5, 182.5) for n in ("gap200", "keepalive", "trickle"))),
 ("limit is per gap, not total: slow200 (200 s of 10 s gaps) not stopped", rows["slow200"]["exit"] == 0 and attempts(rows["slow200"]) == ["completed"]),
 ("429 Retry-After 30 ignored: retry after the fixed 2 s", attempts(rows["h429_ra"]) == ["failed", "completed"] and within("h429_ra", 1.9, 2.2)),
 ("waits are 2 s then 8 s: h429x3, h503x3, trunc_mid3 end at 10 s", all(within(n, 9.9, 10.2) and rows[n]["exit"] == 1 for n in ("h429x3", "h503x3", "trunc_mid3"))),
 ("unreadable event: one immediate retry (badjson1 ok in 0.01 s; badjson2 invalid_response after 2 attempts)",
  within("badjson1", 0, 0.1) and attempts(rows["badjson1"]) == ["failed", "completed"] and attempts(rows["badjson2"]) == ["failed", "failed"] and rows["badjson2"]["error"]["reason"] == "invalid_response"),
 ("no retry for h400, sse_ctx, incomplete", all(len(rows[n]["attempts"]) == 1 and rows[n]["exit"] == 1 for n in ("h400", "sse_ctx", "incomplete"))),
 ("shell hang: only the task deadline stops it; nothing left behind",
  all(rows[n]["exit"] == 1 and rows[n]["error"]["reason"] == "deadline" and rows[n]["left_in_session"] == "0" for n in ("sh_hang_silent", "sh_hang_trapterm", "sh_infinite"))),
 ("silent 700 s shell not stopped at 600 s", rows["sh_silent700"]["exit"] == 0 and rows["sh_silent700"]["wall_s"] > 699),
]
print()
for t, ok in checks: print(("PASS " if ok else "FAIL ") + t)
sys.exit(0 if all(ok for _, ok in checks) else 1)
