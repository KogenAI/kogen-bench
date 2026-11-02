#!/usr/bin/env python3
"""report.py <cells.tsv>: per-task counts for the Kogen AoR control, Studio block follow-up (standard library only)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
def counted(rs): return [r for r in rs if r["status"] == "counted"]
def s(rs, k): return sum(int(r[k]) for r in rs)
def table(title, rs):
    print(f"\n{title}\ntask\trows\tcounted\tvoid\tvalid_intent\treached_build\tlanded\thidden_all_pass\trequested_all_pass")
    for t in sorted({r["task"] for r in rs} | {"all"}):
        sub = rs if t == "all" else [r for r in rs if r["task"] == t]; c = counted(sub)
        print(f"{t}\t{len(sub)}\t{len(c)}\t{len(sub) - len(c)}\t{s(c,'valid_intent')}\t{s(c,'reached_build')}\t{s(c,'landed')}\t{s(c,'hidden_all_pass')}\t{sum(r['requested_passed'] == r['requested_total'] for r in c)}")
print(f"rows {len(rows)}: counted {len(counted(rows))}, voids {collections.Counter(r['status'] for r in rows if r['status'] != 'counted')}")
table("Follow-up runs only (extra Studio repetitions, reruns included)", [r for r in rows if r["run"] != "first"])
table("Studio block (first run + follow-up)", rows)
print("\noutcomes of counted cells (follow-up):", dict(sorted(collections.Counter(r["outcome"] for r in counted(rows) if r["run"] != "first").items())))
print("outcomes of counted cells (Studio block):", dict(sorted(collections.Counter(r["outcome"] for r in counted(rows)).items())))
fu = [r for r in rows if r["run"] != "first" and r["input_tokens"] != "NA"]
print(f"\ntokens of the follow-up cells that reported them ({len(fu)} of {sum(r['run'] != 'first' for r in rows)} rows): input {sum(int(r['input_tokens']) for r in fu)}, output {sum(int(r['output_tokens']) for r in fu)}")
print("\nPer cell: task run rep status outcome hidden requested wall_s")
for r in rows: print(f"{r['task']}\t{r['run']}\t{r['rep']}\t{r['status']}\t{r['outcome']}\t{r['hidden_passed']}/{r['hidden_expected']}\t{r['requested_passed']}/{r['requested_total']}\t{r['wall_s']}")
