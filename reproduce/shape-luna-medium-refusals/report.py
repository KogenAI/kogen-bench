#!/usr/bin/env python3
"""Aggregate data/cells.jsonl (one row per shaping attempt) into the cause table. Standard library only.
usage: python3 -I report.py <data dir>"""
import json, sys, collections
rows = [json.loads(l) for l in open(sys.argv[1] + "/cells.jsonl")]
ANCHOR = ("tests line ends with a period", "decision line has trailing punctuation")
for r in rows:
    r["anchor"] = int(any(k.startswith(ANCHOR) for att in r["attempt_kinds"] for k in att))
ARMS = ["baseline", "unstated-pass", "coverage-ledger"]
CAUSES = ["ACCEPTED", "FORMAT", "STRICTNESS", "REASONING", "PROVIDER"]
print("1. Outcome of the final attempt per shape (26 shapes per arm)")
print("%-16s" % "arm" + "".join("%11s" % c for c in CAUSES) + "%8s" % "total")
tot = collections.Counter()
for a in ARMS:
    c = collections.Counter(r["cause"] for r in rows if r["arm"] == a)
    print("%-16s" % a + "".join("%11d" % c[k] for k in CAUSES) + "%8d" % sum(c.values()))
    tot.update(c)
print("%-16s" % "all" + "".join("%11d" % tot[k] for k in CAUSES) + "%8d" % sum(tot.values()))
print()
print("2. Failed shapes by cause detail")
for a in ARMS:
    f = [r for r in rows if r["arm"] == a and r["cause"] != "ACCEPTED"]
    print("%s: %d failed of 26" % (a, len(f)))
    c = collections.Counter((r["cause"], r["detail"]) for r in f)
    for (k, d), v in sorted(c.items(), key=lambda x: (x[0][0], -x[1], x[0][1])):
        print("  %2d  %-10s %s" % (v, k, d))
print()
print("3. Shapes where at least one refused attempt (of 3) hit an end-of-line anchor check")
print("   (trailing punctuation after a test layer tag or after a decision source tag; fixing the punctuation alone clears that problem)")
for a in ARMS:
    f = [r for r in rows if r["arm"] == a and r["cause"] != "ACCEPTED"]
    print("%-16s %2d of %2d failed shapes; %2d of 26 shapes overall" % (a, sum(r["anchor"] for r in f), len(f), sum(r["anchor"] for r in f)))
print()
print("4. Refused attempts by kind (a shape can show several kinds)")
c = collections.Counter()
na = collections.Counter()
for r in rows:
    for att in r["attempt_kinds"]:
        na[r["arm"]] += 1
        for k in att: c[(r["arm"], k)] += 1
kinds = sorted({k for _, k in c})
print("%-72s" % "kind" + "".join("%17s" % a for a in ARMS))
for k in sorted(kinds, key=lambda k: -sum(c[(a, k)] for a in ARMS)):
    print("%-72s" % k[:72] + "".join("%17d" % c[(a, k)] for a in ARMS))
print("%-72s" % "refused attempts in total" + "".join("%17d" % na[a] for a in ARMS))
