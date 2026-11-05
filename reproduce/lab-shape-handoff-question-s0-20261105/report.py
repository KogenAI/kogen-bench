#!/usr/bin/env python3
"""Stage 0 census for the shaping handoff-question Lab. Usage: python3 -I report.py <data dir>. Reads only the TSV files; no model, no network."""
import csv, sys, collections, os
D = sys.argv[1] if len(sys.argv) > 1 else "data"
CLASSIFIER = {"41d70052", "d98cfe01"}  # releases verified to carry the question check (question_check events in their cells)
logs = list(csv.DictReader(open(os.path.join(D, "delivery-shape-logs.tsv")), delimiter="\t"))
cells = list(csv.DictReader(open(os.path.join(D, "research-cells.tsv")), delimiter="\t"))
cases = list(csv.DictReader(open(os.path.join(D, "handoff-cases.tsv")), delimiter="\t"))
for r in logs:
    for k in ("question_blocks","handoff_blocks","blocks_without_options","blocks_without_recommended","blocks_with_deferral_option","blocks_with_deferral_recommended"): r[k] = int(r[k])
def era(r): return "classifier" if r["kogen_release"] in CLASSIFIER else "before"
def summ(rs):
    return dict(shape_logs=len(rs), question_stop_logs=sum(r["question_blocks"] > 0 for r in rs), handoff_ended_logs=sum(r["handoff_blocks"] > 0 for r in rs))
print("delivery shaping logs (Studio + laptop):", summ(logs))
for e in ("before", "classifier"):
    s = summ([r for r in logs if era(r) == e]); n = s["shape_logs"]
    print(f"  {e}: {s}  handoff-ended rate {100*s['handoff_ended_logs']/n:.2f}% per 100 shape logs" + (f"  (rule-of-three 95% upper bound {300/n:.2f}%)" if s["handoff_ended_logs"] == 0 else ""))
from math import comb
b, c = summ([r for r in logs if era(r) == "before"]), summ([r for r in logs if era(r) == "classifier"])
N, K, n2 = b["shape_logs"] + c["shape_logs"], b["handoff_ended_logs"] + c["handoff_ended_logs"], c["shape_logs"]
print(f"  one-sided exact test, chance of {c['handoff_ended_logs']} handoff-ended in the {n2} classifier-era logs if the rate were the same in both eras: {comb(N-K, n2)*comb(K, c['handoff_ended_logs'])/comb(N, n2):.3f}")
allh = summ(logs); print(f"  all releases: handoff-ended {100*allh['handoff_ended_logs']/allh['shape_logs']:.2f}% per 100 shape logs")
blocks = sum(r["question_blocks"] for r in logs)
print("question blocks:", blocks, "handoff blocks:", sum(r["handoff_blocks"] for r in logs),
      "blocks without options:", sum(r["blocks_without_options"] for r in logs), "without recommended:", sum(r["blocks_without_recommended"] for r in logs),
      "with deferral option:", sum(r["blocks_with_deferral_option"] for r in logs), "deferral recommended:", sum(r["blocks_with_deferral_recommended"] for r in logs))
print("handoff-ended logs by release era:", collections.Counter(era(r) for r in logs if r["handoff_blocks"] > 0))
print("handoff cases by reading:", collections.Counter(c["reading"] for c in cases), "rounds>1:", [c["item"] for c in cases if int(c["handoff_rounds"]) > 1])
oc = collections.Counter(c["outcome"] for c in cells); cl = collections.Counter(x for c in cells for x in c["item_classes"].split(",") if x)
print(f"research cells (unique): {len(cells)} outcomes {dict(oc)}")
print("  question-check item classes:", dict(cl), " handoff-class items:", cl.get("handoff", 0))
qp = [c for c in cells if c["outcome"] == "questions_pending"]
print("  questions_pending cells:", len(qp), "last-question class ui_ux:", sum(c["item_classes"].split(",")[-1] == "ui_ux" for c in qp if c["item_classes"]), "no class recorded:", sum(1 for c in qp if not c["item_classes"]))
