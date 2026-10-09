# rz1: Zig vs Rust on Round-70 Kogen-subsystem tasks

Round date: 2026-10-08
Publication badge: VALID; KEPT FOR AUDIT
Recomputation status: FULLY RECOMPUTABLE

## Status

**VALID**

### Limits
- **RELEASE_EVIDENCE_PARTIAL:** the round publishes mined per-cell records, patches, egress and contamination receipts, launcher logs, and official grade counts. It does not publish Standard 1.2 run records, so strict checklist compliance is not established. See [MISSING.md](MISSING.md).
- **OPERATIONAL_PAUSE:** a 5 h 37 m 47 s disk pause split pair 20. The schedule resumed unchanged under the registered operational-pause clause (disclosures 2–6 below).
- **CHRONOLOGY_UNPROVEN (scrutiny):** the rule's freeze time (2026-10-08T15:28:24Z, before any model cell) is operator-recorded with hashes. It was not published before results, so no independently dated rule/result pair exists.
- **EXECUTION_NOT_RERUNNABLE (scrutiny):** the published kits and harness have not yet passed a clean-machine rerun proof. The decision and every count recompute from the committed records (`python3 rounds/rz1/reproduce_decision.py`; per-cell rows in [data/cells.csv](data/cells.csv), built by `build_cells_csv.py`).
- **PUBLIC_SUITES:** both arms' hidden suites were publicly downloadable during the round, but no cell could reach them (disclosure 1). The suites are now published in full, so the r70-N-zig tasks can no longer serve as held-out tasks (see "Held-out status after publication").

STATUS: **VALID** — pre-registered decision rule executed as registered; final decision **INCONCLUSIVE (Rust stays)**

Pre-registered: yes. [DECISION-RULE.md](DECISION-RULE.md) (SHA-256 `e96b3c16ea8c0bedef77e2ff87b6fc56d981378130301854c4d3cf038a1d6260`) was frozen 2026-10-08T15:28:24Z, before any rz1 model cell. [AMENDMENT-1.md](AMENDMENT-1.md) was appended 2026-10-08T15:42:43Z, before any scored cell. It covers smoke-gate environment faults only, and nothing in it depends on outcomes. Frozen hashes: [PRE-LAUNCH-SHA256](PRE-LAUNCH-SHA256). The published DECISION-RULE.md is a sanitized copy: one hidden-suite file name is replaced by "hidden test file". The as-run SHA-256 above verifies against the original, and the published bytes are hashed in [MANIFEST.sha256](MANIFEST.sha256).
Label: CONFIRMATORY design, executed as registered; the decision is INCONCLUSIVE.
Question: With the same model, task, hidden suite and grader, does Codex `gpt-6-luna` at `max` reach a hidden-suite full pass more often in Zig than in Rust on Round-70 Kogen-subsystem tasks?
n: 21 pairs, 42 scored cells (tasks r70-1 … r70-7 × 3 reps × 2 arms). All 42 were officially graded. Task 8 was dropped before any model cell, because its Rust reference fails its own `make check`.
Headline: INCONCLUSIVE (Rust stays). D = −0.190476, R = 2 rescues, L = 6 losses, p_plus = 0.96484375, p_minus = 0.14453125.
Configuration:
- Codex CLI `0.161.0`, direct, `gpt-6-luna` at `max`.
- 3,600-second cell limit, 0 model retries.
- One cell at a time on `kogen-bench-eu`, in the bench Bubblewrap sandbox with network unshared and provider-only egress.
- Official grade route `r70-macbook-window-v1`: grade_window.py `4dcf8bc7…`, then grade_worker.py `0e8ae1bf…` on `kogen-bench-eu`.
- Toolchains: Rust 1.97.1 and Zig 0.17.0. PLAN.json plan SHA-256 `56978c29…`, seed 1717.

Token total is uncached input + cached input + output.
Raw records: [mined cell records](../../data/mined/rz1.jsonl.gz), [patches](patches/), [egress receipts](egress/), [contamination receipts](contamination/), [receipts](receipts/) and [harness](harness/).

## Result

**Zig was descriptively worse:** D −0.19, with 14/21 full passes for Zig against 18/21 for Rust. **But it missed the pre-registered Zig-worse bar:** p_minus = 0.145, which is not below .025. **The result is therefore INCONCLUSIVE, and Rust stays.** Inconclusive is a valid, pre-registered outcome. The power statement in the decision rule, made before any data, said the design was unlikely to yield a superiority verdict even if Zig were better.

Full passes per task, Rust / Zig, 3 pairs each:
- r70-1: 3 / 3
- r70-2: 3 / 2
- r70-3: 3 / 1
- r70-4: 2 / 0
- r70-5: 2 / 3
- r70-6: 2 / 2
- r70-7: 3 / 3
- **Total: 18 / 14 over 21 pairs**

rz1's official grade rows are published as [mined cell records](../../data/mined/rz1.jsonl.gz). They are not yet in the cross-round outcome export (`results/cells.jsonl`), so this page states its counts in text rather than in a validator-checked pass table. `rounds/rz1/reproduce_decision.py` verifies every count and statistic against the committed records.

The rule applies these thresholds:
- Superiority (Zig replaces Rust) needs D ≥ +0.15 and p_plus < .025. Observed: D −0.19, p_plus 0.965. Not met.
- Zig worse (conclusive) needs D ≤ −0.15 and p_minus < .025. Observed: D −0.19 meets the first part, but p_minus 0.145 does not meet the second. Not met.
- Everything else is INCONCLUSIVE, and Rust stays.

Frozen analyzer output: [receipts/final-output.json](receipts/final-output.json) (as-run SHA-256 `0cbf88ee8f33eb45dd3cf458f19268ee3338cfb06e9f63770c6d8855396623d8`, analyzer `rz1_analyze.py` `3080b281…`).
Public recomputation: `python3 rounds/rz1/reproduce_decision.py` recomputes the interim and final analyses from the committed PLAN and mined records and asserts equality with both frozen outputs.

### Interim (exactly one, as registered)
After pairs 1–12 were officially graded, the interim gave D −0.027778, R 2, L 2 and p_plus = p_minus = 0.6875, so the round continued with no stop. The rule allowed no superiority stop at the interim. Output: [receipts/interim-output.json](receipts/interim-output.json).

### INVALID and INCOMPLETE checks (DECISION-RULE, final steps 1–2)
None was triggered:
- 42/42 cells have exactly one official grade row.
- Every row has tests_ran, build OK, and setup and `make check` rc 0.
- Grader SHA `0e8ae1bf…` is on all 42 rows, and the pre-launch hashes verify.
- runner_status is `ok` on 42/42 with no runner error class, so 0 transport replacements were needed (the cap is 2 per arm).
- The hidden-suite SHA-256 is identical across arms for every task.
- Model, CLI, effort and host are uniform.
- The launcher logs show START and END exactly once for plan indices 2–41. Indices 0–1 repeat only because of the Amendment-1 smoke attempts, which are not scored.

## Timeline (UTC)
- **2026-10-08:**
  - 15:28:24Z: pre-registration frozen.
  - 15:34Z and 15:38Z: smoke launch-gate attempts that failed on proven environment faults (Amendment 1). They are kept and are not scored.
  - 15:42:54Z–15:55:14Z: valid smoke pair (task-4-rep-2).
  - 16:01:07Z: segment A starts (plan indices 2–23).
  - 18:28:31Z: segment A graded (22/22). The interim follows and gives CONTINUE.
  - Segment B (indices 24–38) runs.
  - 20:11:17Z: disk pause starts (disclosure 2).
  - 20:37:51Z: indices 24–38 graded during the pause (15/15).
- **2026-10-09:**
  - 01:49:04Z: resume.
  - 01:49:05Z–01:58:19Z: index 39.
  - 01:58:20Z–02:11:10Z: indices 40–41.
  - 02:17:30Z: indices 39–41 graded (3/3).
  - About 02:19Z: final analysis.
  - 02:20:48Z: round gate released.

## Disclosures
1. **Hidden suites were publicly downloadable; cells could not reach them.**
   - **Exposure.** The Rust r70-1…7 hidden suites are public in this repository (`tasks/r70-N-rust/`, reachable from every public main since `b56a272`). Each Zig kit's hidden test file is byte-identical to the public r70-N-elixir hidden test, plus a few shared helpers. Both arms' hidden tests were therefore publicly downloadable throughout rz1.
   - **Isolation.** Cells ran in the runner sandbox with the network unshared (loopback only). The only route out was the egress allowlist proxy to the provider hosts, and no web-search tool was configured.
   - **Egress evidence over all 42 scored cells:**
     - allowed traffic went only to chatgpt.com (1,584 records) and ab.chatgpt.com (42);
     - 210 denials, all `*.oaiusercontent.com`, not in the allowlist;
     - 0 records to GitHub or this repository;
     - `contamination.json` flag false with 0 strong hits in 42/42 cells;
     - 0 web-search calls in 42/42 transcripts.
   - The only GitHub string in any transcript is one Zig standard-library doc-comment issue URL (ziglang/zig issue 24510), read from the local toolchain, in 3 Zig cells.
   - The 3 smoke-attempt records show the same egress pattern.
   - The integrity verdict was made outcome-blind, before segment-B grading: CLEARED. The suites were public but not reachable.
2. **Operational disk pause, 2026-10-08T20:11:17Z to 2026-10-09T01:49:04Z (5 h 37 m 47 s).**
   - During plan index 38, the Studio disk backstop read free space on `kogen-bench-eu` below 10 GiB + 200 MB and touched the registered lane STOP.
   - The launcher checks STOP only between cells, so index 38 ran to completion. It is kept unchanged.
   - Indices 39–41 had not started.
   - Space was restored by cleanup that deleted only data already verified as preserved elsewhere (free space 9.92 → 12.24 GiB).
   - The schedule then resumed unchanged, under the decision rule's operational-pause clause.
   - Both notes were written outcome-blind, before any segment-B grading and before the resume: [OPERATIONAL-NOTE-2026-10-08-disk-pause.md](OPERATIONAL-NOTE-2026-10-08-disk-pause.md) (`b6421bfe…`) and its [addendum](OPERATIONAL-NOTE-2026-10-09-resume-addendum.md) (`07c60f35…`).
3. **Index 39 ran through `lane_dispatch.py launch-one`.**
   - The pause split pair 20: index 38 (Rust) was done and index 39 (Zig) had not started.
   - Index 39 ran alone, through the same frozen dispatcher the launcher calls (`launch-one --plan PLAN.json --index 39 --scope bulk`), after a manual replica of the launcher preflight (12/12 checks passed).
   - Indices 40–41 then ran with `rz1_eu.sh --launch --from-pair 21`.
   - `--from-pair 20` would have re-run the already measured index 38, which the rule forbids.
4. **Round gate holder.**
   - On 2026-10-09 the host's setup owner installed a client updater that takes an exclusive lock on the host maintenance lock.
   - So that no update could run mid-round, one long-lived holder kept the shared side of that lock from just before index 39 (about 01:49Z) until after the final analysis. It was released at 02:20:48Z.
   - rz1's own Codex binary (0.161.0) and tools were verified unchanged after the operator-client update. The updated operator clients are not used by rz1 cells.
5. **Guard false STOP, 01:49:20Z → 01:50:00Z, with no schedule effect.**
   - The Studio pair-boundary disk guard touched the lane STOP at 01:49:20Z. It was working from a stale baseline: the 8 Oct pre-pause plateau, from before the cleanup.
   - The correct single-dip projection was CONTINUE (12.24 − 0.95 = 11.29 GiB, against a required 10.195 GiB).
   - The operator removed the STOP at 01:50:00Z, while index 39 was running, and fixed the guard.
   - The launcher's next STOP check came at about 01:58Z, after index 39 ended, so no cell and no part of the schedule was affected.
6. **6 vs 10 GiB floor.**
   - The frozen launcher's own preflight refuses a cell below 6 GiB free.
   - The maintained host rule is 10 GiB. It was enforced from the Studio as a 10 GiB + 200 MB backstop, plus a pair-boundary projection.
   - The frozen launcher was left untouched.
   - Every launcher preflight recorded at least 11,373,895,680 B (10.59 GiB) free. Index 39 started at 13,143,158,784 B, per its manual preflight.
7. **Interim.** One pre-registered interim ran after pairs 1–12: D −0.028, R 2, L 2, p 0.6875, so the round continued (see above).
8. **Credential readability (owner ruling D, 2026-10-08).**
   - The agent's own shell commands could technically read the Codex harness home, including its auth file. This was identical in both arms and is the same as in every past Codex-direct round.
   - Mitigations: short-lived tokens, provider-only egress, a periodic token-scan redaction loop over results, and no unscanned publication. Transcripts and rollouts are not published (see [MISSING.md](MISSING.md)).
   - This is recorded as a hardening item, not a launch blocker.
9. **Author contamination, task 1.**
   - The Zig task-1 author job read raw historical grade rows, which can carry failing-test names and output tails, into its model context.
   - This is logged in [tasks/CONTAMINATION-LOG.md](../../tasks/CONTAMINATION-LOG.md) ("2026-10-08: raw grade rows in a Zig task-author job").
   - The reader was a non-contestant author that already had declared suite access. No contestant cell saw it, so held-out status during the round is unchanged.
10. **Budget estimate exceeded.**
    - The decision rule estimated under 30M tokens in total. The 42 scored cells used 38,631,007 tokens (uncached input + cached input + output), most of it cached input.
    - The budget is not a stopping rule. The only stopping rules are the interim rule and operational pauses, so the decision is unaffected.

11. **Billing and operator workers.** Every rz1 cell used the evaluation host's own dedicated Codex device login. The workers that packaged and reviewed this round ran under separate accounts, as recorded in the operator job ledger. No contestant cell used them, and they have no effect on any outcome.

## Held-out status after publication
This release publishes the Zig kits in full under `tasks/r70-{1..8}-zig/`, including their sealed hidden suites and references, so a fresh machine can rerun the round. That makes the r70-N-zig tasks unusable as held-out tasks from now on, exactly as their Elixir twins (and the Rust variants) already are. Future rounds that need held-out tasks must use different tasks.

## Secondary measurements (descriptive; no decision weight)

| Arm | Cells | Official tests passed / total | Build OK | Tokens (uncached + cached + output) | Reasoning tokens (part of output) | Median wall | Total wall |
|---|---:|---:|---:|---:|---:|---:|---:|
| Rust | 21 | 499 / 504 | 21/21 | 16,123,967 (1,267,478 + 14,319,872 + 536,617) | 366,603 | 267.2 s | 6,020.3 s |
| Zig | 21 | 448 / 504 | 21/21 | 22,507,040 (1,522,187 + 20,376,320 + 608,533) | 401,402 | 310.2 s | 6,825.4 s |

Per full pass, including failed cells: Rust 895,776 tokens and 334.5 s of wall over its 18 full passes; Zig 1,607,646 tokens and 487.5 s over its 14.

Wall is the runner's per-cell wall time. Per-pass ratios include failed cells. There were no retries or replacements. Values come from [the mined records](../../data/mined/rz1.jsonl.gz); [recomputed.json](recomputed.json) has the generic recomputation.

## Required reproduction metadata

- Kogen commit: not applicable. The tasks are self-contained Round-70 fixtures.
- Task bases as run: each rz1 cell's base commit is recorded in its mined record and in the `base_sha` column of [data/cells.csv](data/cells.csv). Each base is the HEAD of the task's published bundle in `tasks/_bases/`.
  - Exception: the shared task.json for r70-1-rust and r70-6-rust names an older base, the one used by earlier Round-70 cohorts. rz1 ran r70-1-rust at `76b4f1fdc3bfb10f6a145de9c912fb0056239c16` and r70-6-rust at `2e15e5332f42c34957417a8ca69d747fb01bf488`, which are the bundle HEADs, not task.json's `ff6960b7…` and `5a1aefaa…`. To rerun rz1 exactly, check out those commits.
  - All other rz1 tasks ran at their task.json `base_sha`.
- Harness commit: unavailable. The rz1 harness is not a Git commit. The as-run files and their hashes are in [harness/](harness/) and [PRE-LAUNCH-SHA256](PRE-LAUNCH-SHA256): lane_dispatch.py `47ef532b…`, rz1_eu.sh `d08c0e4b…`, the bench-codex wrapper and configuration, the grader patch `e8a6e69a…`, and the as-run graders in [harness/grader/](harness/grader/).
- Model and effort: `gpt-6-luna` at `max` for every cell (Codex CLI 0.161.0).
- Task IDs: r70-1-rust … r70-7-rust and r70-1-zig … r70-7-zig. The r70-8-zig kit is published but was never run.
- Historical execution command: `ops-logs/rz1_eu.sh --smoke-only`, then `--launch --through-pair 12`, then `--launch --from-pair 13` (stopped by the pause after index 38), then `lane_dispatch.py launch-one --plan PLAN.json --index 39 --scope bulk`, then `rz1_eu.sh --launch --from-pair 21`, then `rz1_analyze.py interim` and `final`. Launcher logs are in [receipts/](receipts/).
- Raw records: [mined cell records](../../data/mined/rz1.jsonl.gz) and this directory. Declared gaps: [MISSING.md](MISSING.md).

Terminology: [public round glossary](../GLOSSARY.md).
