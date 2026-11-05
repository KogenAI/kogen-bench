"""Build Message Batches requests: one review request per commit in data/commits.tsv.
Usage: python3 -I build_requests.py data/commits.tsv CLONES_DIR requests.json
         [--rerun-truncated FIRST_RESULTS.jsonl --max-tokens 16000]
CLONES_DIR holds a clone of each public repository named in commits.tsv (github.com/KogenAI/<repo>).
The patch text is `git show --stat --patch <sha>`, cut at 200,000 bytes; rows whose repo is "private" are skipped."""
import json, subprocess, sys
a = sys.argv[1:]
commits, clones, out_path = a[0], a[1], a[2]
max_tokens = int(a[a.index("--max-tokens") + 1]) if "--max-tokens" in a else 4000
only = None
if "--rerun-truncated" in a:   # second pass: only the first-pass reviews that stopped at the output limit
    only = {r["custom_id"] for r in map(json.loads, open(a[a.index("--rerun-truncated") + 1]))
            if r["result"]["type"] == "succeeded" and r["result"]["message"]["stop_reason"] == "max_tokens"}
out = []
for l in open(commits):
    repo, slug, sha = l.rstrip("\n").split("\t")
    if repo == "repo" or repo == "private":
        continue
    cid = slug[:60] + "-" + sha[:7]
    if only is not None and cid not in only:
        continue
    patch = subprocess.run(["git", "-C", f"{clones}/{repo}", "show", "--stat", "--patch", sha],
                           capture_output=True, check=True).stdout[:200000].decode(errors="replace")
    p = (f"Review this landed commit ({repo} {sha}, Kogen Build {slug}) from stdin for correctness bugs only: wrong behaviour, missed cases, broken error handling, tests that cannot fail. For each finding give file:line, the concrete failure scenario, and severity (P1/P2/P3). If there are none, say 'No findings.' Be brief; no style notes.\n\n" + patch)
    out.append({"custom_id": cid, "params": {"model": "claude-sonnet-5-5", "max_tokens": max_tokens,
                                             "messages": [{"role": "user", "content": p}]}})
json.dump(out, open(out_path, "w"))
print(len(out), "requests", sum(len(r["params"]["messages"][0]["content"]) for r in out) // 4, "approx tokens")
