"""Compare the batch reviews with the seat-run reviews and print the summary table.
Usage: python3 -I report.py results.jsonl status.json rerun_results.jsonl rerun_status.json data/seat_reviews.json rows.json
data/seat_reviews.json holds, per commit slug, what the same lexical test found in the seat-run review text:
clean (no-findings wording and no P1-P3 marker), p (count of P1-P3 markers), files (file names mentioned), chars."""
import json, re, sys, statistics as st
res, stat, res2, stat2, seat_path, rows_path = sys.argv[1:7]
FILE = re.compile(r"[\w./-]+\.(?:go|ex|exs|js|ts|rb|py|rs|md|sh|json|tsv|yml)\b")
def info(t):
    clean = bool(re.search(r"no findings|no (real |correctness )?bugs|looks correct|checks out|no issues", t[:700], re.I)) and not re.search(r"\bP[123]\b", t)
    return clean, len(re.findall(r"\bP[123]\b", t)), {f.split("/")[-1] for f in FILE.findall(t)}
SEAT = json.load(open(seat_path))
A2 = {r["custom_id"]: r for r in map(json.loads, open(res2))}
rows = []; inp = out = err = 0
for r in map(json.loads, open(res)):
    r2 = A2.get(r["custom_id"]); slug = re.sub(r"-[0-9a-f]{7}$", "", r["custom_id"])
    if r["result"]["type"] != "succeeded":
        err += 1; rows.append(dict(slug=slug, error=r["result"]["type"])); continue
    m = r["result"]["message"]; u = m["usage"]; inp += u["input_tokens"]; out += u["output_tokens"]
    if r2:
        u2 = r2["result"]["message"]["usage"]; inp += u2["input_tokens"]; out += u2["output_tokens"]; m = r2["result"]["message"]
    t = "".join(b.get("text", "") for b in m["content"] if b["type"] == "text")
    s = SEAT.get(slug, dict(clean=False, p=0, files=[], chars=0))
    bc, bn, bf = info(t); sc, sn, sf = s["clean"], s["p"], set(s["files"])
    rows.append(dict(slug=slug, batch_clean=bc, seat_clean=sc, batch_p=bn, seat_p=sn,
                     file_jaccard=(len(bf & sf) / len(bf | sf)) if (bf | sf) else None, batch_chars=len(t), seat_chars=s["chars"]))
ok = [r for r in rows if "error" not in r]
agree = sum(r["batch_clean"] == r["seat_clean"] for r in ok)
both_f = [r for r in ok if not r["batch_clean"] and not r["seat_clean"]]
S = json.load(open(stat)); S2 = json.load(open(stat2))
print(json.dumps(dict(n=len(rows), errors=err, verdict_agree=agree, verdict_agree_rate=round(agree / len(ok), 3),
    batch_clean=sum(r["batch_clean"] for r in ok), seat_clean=sum(r["seat_clean"] for r in ok), both_findings=len(both_f),
    mean_file_jaccard_both_findings=round(st.mean(r["file_jaccard"] for r in both_f if r["file_jaccard"] is not None), 3) if both_f else None,
    mean_batch_p=round(st.mean(r["batch_p"] for r in ok), 2), mean_seat_p=round(st.mean(r["seat_p"] for r in ok), 2),
    input_tokens=inp, output_tokens=out, usd_batch=round(inp * 1.0 / 1e6 + out * 5.0 / 1e6, 4),
    usd_sync_equiv=round(inp * 2.0 / 1e6 + out * 10.0 / 1e6, 4), wall_s=S.get("wall_s"), rerun_wall_s=S2.get("wall_s"),
    truncated_first_pass=len(A2), final_truncated=sum(1 for r in ok if r["batch_chars"] == 0), counts=S.get("request_counts")), indent=1))
json.dump(rows, open(rows_path, "w"), indent=1)
