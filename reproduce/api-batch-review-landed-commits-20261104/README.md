# Message Batches review of landed commits versus the seat-run Sonnet review

**Verdict: unresolved.** The Message Batches API reviewed 93 landed Kogen commits in 184 s (first pass) on claude-sonnet-5-5. The first pass was flawed: default adaptive thinking used up the 4,000-token output limit on 37 of 93 requests (33 returned no text). Those 37 were rerun at 16,000 tokens (246 s); 1 of the 93 final reviews is still empty. The comparison with the seat-run review is weak: the seat reviews are free-form prose with few severity markers, and the agreement figures below come from a lexical clean/not-clean test.

## What was measured
Each request carries the same review prompt as the seat-run review of the same commit and the same patch text (`git show --stat --patch <sha>`, cut at 200,000 bytes). Model claude-sonnet-5-5, API version 2023-06-01, default thinking, one batch per pass, no retries beyond the single 16,000-token rerun of the reviews that stopped at the output limit.

| Measure | Value |
|---|---|
| Requests / completed | 93 / 93 (1 final review empty) |
| Input / output tokens (both passes, thinking included) | 3,503,074 / 529,318 |
| Cost at Batches price (50% of list) | USD 6.15 (pass 1 USD 3.68, rerun USD 2.47) |
| Same tokens at synchronous list price | USD 12.30 |
| Clean/not-clean agreement with the seat review | 60/93 (64.5%), lexical test; batch said clean 32, seat text clean 13 |
| File-name overlap (Jaccard) where both flag something (n=54) | 0.32 |
| Wall | 184 s + 246 s rerun, including the flawed first pass |

Cost per pass stayed under the USD 5 cap per batch. Agreement is not a correctness measure: neither review was checked against ground truth.

## Files
- `data/commits.tsv`: the 93 commits (repository, Kogen Build slug, commit sha). 91 are in public KogenAI repositories; the other 2 are from a private repository and appear as `private-1` and `private-2`.
- `data/seat_reviews.json`: for each public commit, what the lexical test found in the seat-run review: clean, P1-P3 marker count, file names mentioned, length.
- `data/rows.json`: the per-commit comparison table for all 93 commits; `data/summary.json`: the figures above.
- `data/first_pass_status.json`, `data/rerun_status.json`: batch counts and wall times.

## Rerun
Clone the public repositories named in `data/commits.tsv` from github.com/KogenAI into one folder, then:

```
python3 -I build_requests.py data/commits.tsv CLONES requests.json
ANTHROPIC_API_KEY=... python3 -I submit_batch.py requests.json results.jsonl status.json
python3 -I build_requests.py data/commits.tsv CLONES rerun_requests.json --rerun-truncated results.jsonl --max-tokens 16000
ANTHROPIC_API_KEY=... python3 -I submit_batch.py rerun_requests.json rerun_results.jsonl rerun_status.json
python3 -I report.py results.jsonl status.json rerun_results.jsonl rerun_status.json data/seat_reviews.json rows.json
```

`submit_batch.py` refuses a batch estimated over USD 4.50. The rerun covers the 91 public commits. The model's review text varies between runs, so the figures will move; the request text is deterministic. We checked that these scripts rebuild our run's request text exactly for the 91 public commits (both passes), and that `report.py` on our raw outputs gives `data/rows.json` and `data/summary.json` exactly. The raw outputs themselves are left out of this pack because they quote review text.
