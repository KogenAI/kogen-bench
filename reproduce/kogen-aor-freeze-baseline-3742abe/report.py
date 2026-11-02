#!/usr/bin/env python3
"""report.py <freeze.tsv> <control.tsv> <control_st2.tsv>: per-task table for the frozen-tree Kogen AoR baseline,
and the descriptive pool with the published 514dab4 control (standard library only)."""
import csv, sys, collections
def load(p): return list(csv.DictReader(open(p), delimiter="\t"))
frz = load(sys.argv[1]); ctl = load(sys.argv[2])
st2 = [r for r in load(sys.argv[3]) if r["status"] == "counted" and r["run"] != "first"]
def s(rs, k): return sum(int(r[k]) for r in rs)
def line(label, rs):
    return f"{label}\t{len(rs)}\t{s(rs,'valid_intent')}\t{s(rs,'reached_build')}\t{s(rs,'landed')}\t{s(rs,'hidden_all_pass')}\t{sum(r['requested_passed']==r['requested_total'] for r in rs)}"
HEAD = "task\tcells\tvalid_intent\treached_build\tlanded\thidden_all_pass\trequested_all_pass"
def table(title, rs):
    print(f"\n{title}\n{HEAD}")
    for t in sorted({r["task"] for r in rs}): print(line(t, [r for r in rs if r["task"] == t]))
    print(line("all", rs))
print(f"frozen-tree cells {len(frz)}: " + ", ".join(f"{h} {sum(r['host']==h for r in frz)}" for h in ("server1", "laptop", "server2")))
table("Frozen tree (3742abe), one run per task per host", frz)
table("Control 514dab4 first pack (Studio, eu2, laptop)", ctl)
table("Control 514dab4 follow-up (extra Studio runs, counted only)", st2)
pool = frz + ctl + st2
table("Pool: frozen tree + control + control follow-up (descriptive)", pool)
print("\nBlocks (cells, valid Intent, landed, hidden all-pass):")
for label, rs in (("frozen server1", [r for r in frz if r["host"]=="server1"]), ("frozen laptop", [r for r in frz if r["host"]=="laptop"]), ("frozen server2", [r for r in frz if r["host"]=="server2"]),
                  ("control server1", [r for r in ctl if r["host"]=="eu2"]), ("control laptop", [r for r in ctl if r["host"]=="laptop"]),
                  ("control Mac (first + follow-up)", [r for r in ctl if r["host"]=="Studio"] + st2)):
    print(f"{label}\t{len(rs)}\t{s(rs,'valid_intent')}\t{s(rs,'landed')}\t{s(rs,'hidden_all_pass')}")
print("\noutcomes (frozen tree):", dict(sorted(collections.Counter(r["outcome"] for r in frz).items())))
print(f"tokens (frozen tree): input {s(frz,'input_tokens')} (cached {s(frz,'cached_tokens')}), output {s(frz,'output_tokens')}")
print("\nFirst mistake per cell (frozen tree): task host first_mistake")
for r in frz: print(f"{r['task']}\t{r['host']}\t{r['first_mistake']}")
print("\nPer cell (frozen tree): task host hidden requested input output wall_s")
for r in frz: print(f"{r['task']}\t{r['host']}\t{r['hidden_passed']}/{r['hidden_expected']}\t{r['requested_passed']}/{r['requested_total']}\t{r['input_tokens']}\t{r['output_tokens']}\t{r['wall_s']}")
