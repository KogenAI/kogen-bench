# Rust vs Elixir evidence synthesis

**Draft synthesis, not published; Almir decides on publishing. Descriptive evidence review; not a pre-registered analysis.**

Repo source: this repository, commit `f762ce6` (`git log -1 --format=%h`). This review counts official full passes as reported in the round documents, except the rve3 post hoc row, which counts official `pass_` fields read through a whitelist-only grade reader.

## Round-by-round evidence

| Round | Design (pairing, tasks, model/effort, hosts, registration) | n | Rust passes | Elixir passes | Split pairs (Rust-only / Elixir-only) | Failure stages and validity status; reason/source |
|---|---|---:|---:|---:|---:|---|
| `r70` / `r70-rve` (same cohort) | Unpaired retrospective comparison; tasks 1, 3, 4, 6; direct model use, `gpt-6-luna` max; both languages on kogen-bench-eu; not preregistered. `r70-rve` is the audit/recomputation page for the original 40-cell R70 cohort. | 10 cells/arm | 8/10 in both records | 2/10 in both records | n/a (unpaired) | Recorded shortfalls: Rust hidden tests, 16/18 (2 cells); Elixir hidden tests, 24/25 (3 cells), 27/28 (1 cell), 15/18 (2 cells), 17/18 (1 cell), 22/24 (1 cell). Further stage attribution: **not recorded**. `r70`: **INCOMPLETE** (2/7 tasks admitted; 0 scored core rows); tasks 1 and 4 are confounded. `r70-rve`: **INVALID; descriptive analysis** due to unmatched conditions, no preregistration evidence, and no single matched registered protocol. Source: `rounds/r70/README.md`; `rounds/r70-rve/README.md`, `MEASURED.md`. |
| `r70-rve-ext` | Unpaired descriptive extension; tasks 2, 5, 7; direct model use, `gpt-6-luna` max; both languages on kogen-bench-eu; reps 31–32 registered as descriptive, rep 33 separately post hoc. | 6 cells/arm registered; 7 Rust and 8 Elixir including post hoc rep 33 | 5/6 (6/7 incl. post hoc) | 4/6 (5/8 incl. post hoc) | n/a (unpaired) | Failure stages: **not recorded**. **Valid, descriptive** for reps 31–32; small samples, one model, and author-selected templates; rep 33 is post hoc. Source: `rounds/r70-rve-ext/README.md`, `DECISION-RULE.md`, `RESULTS.md`. |
| `r70-rve-rerun` | Unpaired FE2 sensitivity rerun, task 4 Rust vs Elixir (plus task-1 Elixir-only sensitivity cells); direct model use, `gpt-6-luna` max; Rust and Elixir on kogen-bench-eu; registered descriptive sensitivity check. | 3 cells/arm on task 4 | 3/3 | 0/3 | n/a (unpaired) | Elixir task-4 hidden tests: original 15/18 (2 cells), 17/18 (1 cell); FE2 rerun 17/18 (3 cells). Further stage attribution: **not recorded**. **Descriptive / confounded**; task-4 fixed-front-end admission controls failed for Rust and Elixir, so outcomes do not isolate a front-end effect. Source: `rounds/r70-rve-rerun/README.md`, `DECISION-RULE.md`, `RESULTS.md`, `RERUN-RESULTS.md`. |
| `rve2` | Paired on tasks 1, 5, 7; registered same-day comparison, `gpt-6-luna` max, CLI 0.161.0; both arms within each pair on same host (EU/US). Counts below are only the documented interim peek. | 6 completed pairs in peek | 1/6 | 0/6 | 1 / 0 | Failure stages: **not recorded**. **INVALID** after a task-definition prompt mismatch on tasks 5 and 7; stopped. The peek is not a final-round tally. Source: rounds/rve2/DECISION-RULE.md, STATUS-INVALID.md, PEEKS.log (records pending). |
| `rve3` registered interim | Paired on tasks 1, 5, 7; registered fresh comparison, `gpt-6-luna` max, CLI 0.161.0; same host within each pair across EU/US. Registered interim scores set flagged cells to zero. | 9 pairs | 7/9 | 0/9 | 7 / 0 | These zeroed scores are not official pass rates or a stage tally. They are an artefact of the invalid registered audit rule, which counted github.com text in command output; seven flagged cells exceeded the limit of two. **INVALID** under the registered rule. Source: rounds/rve3/DECISION-RULE.md, INTERIM-RESULT.json, STATUS-INVALID.md (records pending). |
| `rve3` official `pass_`, post hoc | Same 9 pairs and design as above; post hoc recount of official `pass_` only, without the interim rule's flagged-cell zeroing. | 9 pairs | 8/9 | 3/9 | 5 / 0 (both pass 3; both fail 1, p06) | Rust failures: p06 hidden tests, 2/24. Elixir failures: p01 (t5) hidden, 1/24; p02 (t7) public gate; p03 (t1) hidden, 1/25; p04 (t7) public gate; p06 (t5) public gate; p09 (t1) hidden, 1/25. **Descriptive, post hoc; rve3 remains INVALID as registered.** Official `tests_ran=false` denotes a public-gate failure (setup/build/check); `tests_ran=true` with `pass_=false` denotes hidden-test failure. Source: maintainer-verified grade-key and command review (see Sources); rve3 round records (records pending). |
| `rve3` after the stop, descriptive | Pairs 10–11, tasks 7 and 1; same rve3 setup; not part of the registered interim. | 2 pairs | 1/2 | 1/2 | 0 / 0 (both pass 1; both fail 1, p10) | p10 (t7): Rust hidden tests, 1/24; Elixir public gate. p11 (t1): both pass. **Descriptive only; rve3 remains INVALID as registered.** Source: maintainer-verified grade-key and command review (see Sources); rve3 records pending. |
| `spot1`, descriptive spot check | Tasks r70-5 (EU) and r70-7 (US), one cell per language; gpt-6-luna max; kit `b4f0eb6`; 1200 s limit; corrected audit with 0 flags; not registered. | 2 cells/arm | 2/2 | 1/2 | 1 / 0 | Elixir r70-5: hidden tests, 23/24, after passing every public gate. Rust had no failures; Elixir r70-7 passed 24/24. **Descriptive, not registered.** Source: maintainer-provided spot1 results (records pending). |

Go and TS/Bun were also run in spot1; this synthesis reports only Rust and Elixir.

`r70` and `r70-rve` refer to the same original cohort and are shown in one row so they cannot be double-counted. `r70-rve-rerun` reports only task 4 as the direct Rust–Elixir comparison; task 1 reruns Elixir alone. `r70-rve-ext` registered the reps 31–32 counts; the separate rep-33 totals are shown only to disclose the added observations. R70 task-8 v2 is not included: its arms were Rust and Go only, and it had no scored cells.

## Direction

The official rve3 `pass_` counts were Rust 8/9 vs Elixir 3/9. The registered interim showed 7/9 vs 0/9 as zeroed scores, an artefact of the invalid audit rule, which counted github.com text in command output. Rust had more observed official full passes in every comparable row with a tally except the after-stop rve3 row, where both passed one of two cells. Rve2's documented peek favored Rust; its full stopped cohort is not tallied here. The registered rve3 analysis remains INVALID.

## Limitations

- The comparisons use small samples: typically 2–10 cells per arm, and the paired registered rounds had at most nine pairs in the analyzed data. A one-cell change can materially alter the rates.
- The public R70 cohorts largely use direct model calls with `gpt-6-luna` at max. They do not establish results across models or effort settings. Supplemental R70 records lack complete per-cell effective model/effort receipts; the R70 original summary states only one model for its comparison.
- Task overlap is partial and deliberate: original R70/RvE uses tasks 1, 3, 4, 6; the extension uses 2, 5, 7; registered rounds use 1, 5, 7. The combined R70/RvE row represents the same cohort, and the FE2 rerun is a separate sensitivity cohort. Do not pool them as independent samples.
- The original cohort has task 1 and task 4 front-end/skeleton confounds; task 6's output-order question remains unresolved. The FE2 task-4 fixed-front-end admission controls failed for Rust and Elixir, limiting causal interpretation of the rerun.
- The registered lane had an open-agent-network defect. A host egress firewall mitigated access to public code hosts, but its IP-level rules have limits. The lane's `patch.diff` omits untracked files even though grading uses the full tree. These are integrity and reproducibility limitations, not evidence that a particular language benefited.
- Under the corrected audit, which counts agent-originated network attempts only, all 18 rve3 interim cells are 0 flagged; under the registered audit they had 7 flagged cells. This corrected audit context does not change rve3's **INVALID as registered** status.
- Elixir's public gates include format, Credo, and Dialyzer checks; Rust's include fmt and Clippy. The four Elixir public-gate failures in rve3 pairs 1–11 are exactly the four Elixir cells whose agents never ran `make check` (they ran only `make build`). Across rve3 and spot1, every Elixir agent that ran `make check` (last exit 0) passed the official gates; Rust agents skipped `make check` twice (p06 and p10) and still passed the gates. This different gate strictness and check behavior is a same-chance caveat. A public rerun probe could not reproduce the grader's Elixir environment, so no tool-level attribution is made.
- Earlier-round failure-stage attribution beyond the recorded hidden-test shortfalls is **not recorded**. r70-rve-rerun's Elixir task-4 failures are also not stage-attributed in those records.
- The spot1 cell limit was 1200 s, not the 3600 s used in registered rounds; this matters for the one spot1 Go timeout (outside this synthesis's scope).
- `r70-rve` is INVALID as a comparative registered study; `rve2` is INVALID due to prompt mismatch; `rve3` is INVALID under its registered audit rule. Keep these statuses visible. The extension is marked VALID for its limited registered descriptive cohort, not as a general language ranking.

## Decision

Decision (recorded by the maintainers, 2026-10-09): **Rust**.

The official rve3 `pass_` counts were Rust 8/9 vs Elixir 3/9. The registered interim showed 7/9 vs 0/9 as zeroed scores, an artefact of the invalid audit rule, which counted github.com text in command output. Elixir is dropped from further rounds. Rust vs Go vs TS/Bun is being tested in a separate registered round (rtg1) on new core-like tasks.

The evidence supports that Rust had more observed official full passes in every tallied comparison except the 2-pair rve3 after-stop row, which was tied, and in the descriptive rve2 peek (not a registered analysis).

The evidence does not establish a general causal Rust-over-Elixir advantage across tasks, models, effort levels, or future rounds.

## Sources

All repo paths below are relative to this repository at commit `f762ce6`.

- `rounds/r70/README.md`
- `rounds/r70-rve/README.md`; `rounds/r70-rve/MEASURED.md`
- `rounds/r70-rve-ext/README.md`; `rounds/r70-rve-ext/DECISION-RULE.md`; `rounds/r70-rve-ext/RESULTS.md`
- `rounds/r70-rve-rerun/README.md`; `rounds/r70-rve-rerun/DECISION-RULE.md`; `rounds/r70-rve-rerun/RESULTS.md`; `rounds/r70-rve-rerun/RERUN-RESULTS.md`
- `rounds/r70-rve-task8v2/README.md` (scope check: no Elixir arm and no scored cells)
- rve2 round records (records pending).
- rve3 round records (records pending).
- rve3 official `pass_` and `tests_ran` fields, read through a whitelist-only grade reader; maintainer-verified evidence also includes test, failure, and error fields and command text/exit codes in the run record (2026-10-09 ~11:00–11:35Z).
- Maintainer-provided descriptive facts for rve3 pairs 10–11 and spot1 (2026-10-09); spot1 corrected-audit result and run configuration (records pending).
- Decision recorded by the maintainers on 2026-10-09. This supersedes the four-arm successor planned in rounds/rve3/STATUS-INVALID.md (records pending), which was cancelled.

The rve3 grade fields cited above were read through a whitelist-only grade reader; no grade, `grades.jsonl`, window, or manifest file was opened directly. No files under `tasks/*/hidden/` or `tasks/*/grader/` were read.
