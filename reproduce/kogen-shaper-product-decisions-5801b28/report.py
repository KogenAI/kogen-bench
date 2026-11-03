#!/usr/bin/env python3
"""report.py <cells.tsv> <questions.tsv>: recompute the per-arm summary behind the finding (standard library only)."""
import csv, sys
cells = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
qs = list(csv.DictReader(open(sys.argv[2]), delimiter="\t"))
for arm in ("base", "candidate"):
    c = [r for r in cells if r["arm"] == arm]
    q = [r for r in qs if r["arm"] == arm]
    saved = sum(r["intent_saved"] == "yes" for r in c)
    print(f"{arm}: cells {len(c)}, Intents saved {saved}, ended with a question {sum(r['outcome'] == 'questions_pending' for r in c)}, "
          f"model requests {sum(int(r['model_requests']) for r in c)}, input tokens {sum(int(r['input_tokens']) for r in c)}, "
          f"output tokens {sum(int(r['output_tokens']) for r in c)}, distinct topics {len({r['topic'] for r in q})}")
b = sum(r["intent_saved"] == "yes" for r in cells if r["arm"] == "base")
k = sum(r["intent_saved"] == "yes" for r in cells if r["arm"] == "candidate")
same_topic = {r["topic"] for r in qs if r["arm"] == "base"} == {r["topic"] for r in qs if r["arm"] == "candidate"}
print(f"question topic identical across arms: {same_topic}")
print("verdict: SAME (0 Intents in both arms)" if b == k == 0 else f"verdict: CHECK (base {b}, candidate {k})")
