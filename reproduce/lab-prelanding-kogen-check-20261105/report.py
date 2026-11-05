#!/usr/bin/env python3
"""Recount the Lab from the published per-commit rows (offline, no model, no kogen checkout). python3 -I report.py [data-dir]
Reads data/summary.json (one row per sample commit: the strict / adjusted verdict, cause class, new and old failing tests,
wall and phase seconds of the B run) and data/sample.tsv (what arm A decided), recomputes every count in replay.json and the
pass-rule outcome, and prints them. Exit 1 if replay.json disagrees."""
import csv, json, os, statistics, sys
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
S = json.load(open(D + "/summary.json")); rows = S["rows"]
A = list(csv.DictReader(open(D + "/sample.tsv"), delimiter="\t"))
ran = [r for r in rows if r["wall_s"] is not None]
ref = lambda r, k: str(r[k]).startswith("REFUSE")
br = [r for r in ran if r["role"] == "breaker"]; gd = [r for r in ran if r["role"] == "good"]
c = dict(
    sample=len(rows), breakers=sum(r["role"] == "breaker" for r in rows), good_sample=sum(r["role"] == "good" for r in rows),
    A_breakers_refused=sum(a["role"] == "breaker" and a["A_decision"] != "GREEN landing" for a in A), A_good_refused=sum(a["role"] == "good" and a["A_decision"] != "GREEN landing" for a in A),
    B_breakers_run=len(br), B_good_run=len(gd),
    B_breakers_refused_strict=sum(ref(r, "verdict") for r in br), B_good_refused_strict=sum(ref(r, "verdict") for r in gd),
    B_breakers_refused_adjusted=sum(ref(r, "adjusted") for r in br), B_good_refused_adjusted=sum(ref(r, "adjusted") for r in gd),
    B_breakers_refused_behaviour=sum(r["cause"] == "behaviour" for r in br), B_good_refused_behaviour=sum(r["cause"] == "behaviour" for r in gd))
add = [(r["wall_s"] - (r["times"] or {}).get("lockwait", 0)) / 60 for r in ran]
c["median_minutes_added_x10"] = int(round(statistics.median(add) * 10)) if add else 0
print(json.dumps(c, indent=1))
rp = os.path.join(D, "..", "replay.json")
if os.path.exists(rp):
    R = json.load(open(rp)); ok = True
    for arm, keys in (("A", ["breakers_refused", "good_refused"]), ("B", ["breakers_run", "good_run", "breakers_refused_strict", "good_refused_strict", "breakers_refused_adjusted", "good_refused_adjusted", "breakers_refused_behaviour", "good_refused_behaviour"])):
        for k in keys:
            have = R["arms"][arm]["counts"].get(k); want = c[("A_" if arm == "A" else "B_") + k]
            if have != want: ok = False; print("MISMATCH", arm, k, have, want)
    print("replay.json counts match" if ok else "replay.json counts DIFFER"); sys.exit(0 if ok else 1)
