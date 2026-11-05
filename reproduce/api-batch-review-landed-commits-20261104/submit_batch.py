"""Submit requests to the Message Batches API, poll until it ends, write the results and status.
Usage: ANTHROPIC_API_KEY=... python3 -I submit_batch.py requests.json results.jsonl status.json
Refuses when the estimate is over USD 4.50 (90% of the USD 5 per-batch cap)."""
import json, os, sys, time, urllib.request, urllib.error
req_path, res_path, st_path = sys.argv[1:4]
H = {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01", "content-type": "application/json"}
def call(path, body=None):
    r = urllib.request.Request("https://api.anthropic.com" + path, json.dumps(body).encode() if body is not None else None, H)
    try:
        return urllib.request.urlopen(r, timeout=120).read()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read()[:300].decode(errors='replace')}")
reqs = json.load(open(req_path))
est = sum(len(r["params"]["messages"][0]["content"]) / 4 for r in reqs) / 1e6 * 1.0 + len(reqs) * 1500 / 1e6 * 5.0   # batch: $1/MTok in, $5/MTok out
print("estimate usd", round(est, 3))
if est > 5 * 0.9:
    raise SystemExit("estimate over cap")
bid = json.loads(call("/v1/messages/batches", {"requests": reqs}))["id"]; t0 = time.time()
while True:
    s = json.loads(call("/v1/messages/batches/" + bid))
    if s["processing_status"] == "ended":
        break
    if time.time() - t0 > 6 * 3600:
        raise SystemExit("still processing after 6h; batch " + bid)
    time.sleep(60)
open(res_path, "wb").write(call("/v1/messages/batches/" + bid + "/results"))
open(st_path, "w").write(json.dumps(dict(s, wall_s=round(time.time() - t0))))
print("ended", s["request_counts"], round(time.time() - t0))
