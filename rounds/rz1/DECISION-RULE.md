# Round rz1: Zig vs Rust on Round-70 Kogen-subsystem tasks (pre-registration)

FROZEN 2026-10-08, after the official admission controls and before any rz1 model cell. Its sha256 is recorded in levers/rz1/prereg/PRE-LAUNCH-SHA256.

Owner question (Almir, via the coordinator, 8 Oct): does Zig beat Rust for Kogen-subsystem work? Contract: careful-rebuild/build/workflows/BENCH-DRIVER.md.

## Hypothesis and decision it changes
- **H1 (Zig better):** with the same model, the same task, the same hidden suite and the same grader, Codex gpt-6-luna at max effort reaches hidden-suite full pass more often in Zig than in Rust.
- **Decision:** Zig replaces Rust as Kogen's implementation language **only if** the superiority criterion below is met. Otherwise Rust stays.
- **Inconclusive is a valid outcome.** No repetitions are added after the first cell.

## Arms and fixed configuration
- **Arms:** the same Codex CLI (0.161.0) runs direct with gpt-6-luna at max effort on each task's Rust variant (r70-N-rust, toolchain rust 1.97.1) and on its Zig variant (r70-N-zig, toolchain zig 0.17.0).
- **What is identical across arms:** the public prompt except for its 3-line stack footer, the hidden suite (hidden test file, byte-identical; its sha256 is recorded per task), grade.py, and the official r70 grade route (grade_window.py, then grade_worker.py on kogen-bench-eu).
- **Limits:** 3,600-second cell limit and 0 model retries.
- **Host:** kogen-bench-eu only, with its own billing@ login. One cell at a time, and nothing else runs during measured cells.
- **Versions:** identical within the round, recorded in ENVIRONMENT.md.

## Harness, grader and credential disclosure
- **Harness.** The standard Codex-direct harness of the r70 rounds:
  - it uses the runner's codex adapter (`codex exec --json … --dangerously-bypass-approvals-and-sandbox`) inside the bench bwrap sandbox;
  - egress is limited to chatgpt.com; auth.openai.com is blocked;
  - it uses EU's own billing@ device login (probe-kgn-eu, status probe passed 13:24Z).
  
  Two things differ from the historical r70 tables: the Codex CLI is 0.161.0 instead of 0.160.0, and EU uses its own login. Comparisons are therefore made only within rz1, never against the r70 tables.
- **Credential readability (owner ruling D, 8 Oct).** The agent's own shell commands can technically read the Codex harness home, including its auth.json. This is identical for both arms and the same as every past Codex-direct round. Mitigations:
  - short-lived access tokens;
  - chatgpt.com-only egress;
  - the tokscan redaction loop over all results on EU (every 20 min);
  - nothing is published unscanned.
  
  This is recorded as a hardening item, not a launch blocker (BENCH-DRIVER.md as updated 8 Oct).
- **Hidden material stays unreadable.** Hidden suites, references and other cells' data are unreadable from the agent sandbox. The rz1 lane isolation probe denied fake hidden-suite, reference, other-result and other-home auth files (levers/rz1/gate/isolation.json).
- **Grader (shared infra, rule J, applied before registration):**
  - grade_worker.py sha256 0e8ae1bf… (the rz1 results glob and the `zig` stack prefix);
  - grade_window.py sha256 4dcf8bc7… (`.zig-cache` and `zig-out` excluded from reference staging);
  - the patch is levers/rz1/PATCH-grader-zig.diff (e8a6e69a…);
  - the self-test inventory was identical before and after.

## Population (frozen at registration)
- **Admitted set A = {1, 2, 3, 4, 5, 6, 7}** (levers/rz1/ADMITTED-TASKS.json).
  - Both arms of every admitted task passed the official r70 admission controls on EU:
    - each reference passes all N hidden tests with setup, build and `make check` green;
    - each no-op fails with all N tests executed;
    - the suite sha256 is identical across stacks.
  - **Task 8 is dropped:** the r70-8-rust reference fails its own `make check` (cargo fmt/clippy, rc 2) in both controls, and task 8 was never admitted in r70.
  - |A| = 7, so N_pairs = 21 and there are 42 cells.
- **PLAN.json:** plan sha256 56978c2927e9bc0b0cf494483ebc866006a5f684730a6cd127683bc799dc45cc (file sha256 887a85ac31116209a03c9702b2d346e6a5f378df9ba0bc525b46f791d89026c1), seed 1717. The smoke pair is task-4-rep-2.
- **Launcher:** ops-logs/rz1_eu.sh, sha256 recorded in PRE-LAUNCH-SHA256.
  - Smoke runs with `--smoke-only`.
  - The first bulk segment runs with `--launch --through-pair 12`; the second, after the interim, with `--launch --from-pair 13`.
  - A nonzero cell rc is logged and the run continues, under ITT.
- **Tasks:** the admitted set A ⊆ {r70-1 … r70-8}, filled in at freezing. A task is admitted only if both arms pass the launch-gate controls on EU through the official route: reference PASS, no-op FAIL with every hidden test executed, and skeleton parity per levers/r70-zig/PARITY-r70-N.md.
- **Dropped tasks:** listed with their reasons and excluded entirely. This is decided before any model cell.
- **Pairs:** (task, rep) for rep ∈ {1, 2, 3}, so the planned pairs number N_pairs = 3·|A|, with two cells per pair.
- **Order:** the pair order is shuffled with `random.Random(1717)`, and the arm order within each pair is drawn from the same generator. The schedule is frozen in PLAN.json (its sha is recorded).
- **Smoke:** the first pair is the smoke pair. It is officially graded before the remaining pairs are released, and it stays in ITT.
- **Development and held-out:** no tuning happens in this round, so every admitted task is held-out. The Zig variants were authored on 8 Oct, and authors (cx jobs) saw the sealed suites. No contestant cell has seen them.
- **Declared author exposure, task 1.** The task-1 author job (zig-author-1) also read raw historical grade rows (levers/r70/grades.jsonl and r70-rve/official-rve-grades.jsonl: rows of r70-1-rust and lang-sol cells, which can carry failing-test names and output tails) into its model context. This broke the hidden-suite rule, and it is logged in kogen-bench tasks/CONTAMINATION-LOG.md (2026-10-08, "raw grade rows in a Zig task-author job").
  - The reader was a non-contestant author that already had declared access to the task-1 suite, so the held-out status of rz1 contestant cells is unchanged.
  - The other seven author logs contain no raw grade rows (verified).

## Outcome and ITT
- **Outcome:** Y = 1 only for a valid official full pass (build OK and every collected hidden test passing) on the correct task, arm and model receipts. Otherwise Y = 0.
- **ITT:** every assigned cell keeps its arm. No-patch, timeout, build failure and model failure all score 0.
- **Transport replacement (outcome-blind):** a cell whose provider transport failed is re-run in the same slot, appended to the end of the schedule.
  - A transport failure means an HTTP, stream or auth error, or a runner infra error, before any patch was produced, judged from transport receipts alone.
  - At most 2 replacements per arm. Reaching the cap makes the round INVALID.
  - A cell that produced a patch is never replaced.
  - Every attempt is kept and reported. Success is reported both counting every delivered attempt and conditional on a completed run, and retry time and usage count in the costs.

## Primary estimand and tests
- **Effect D:** for each task t, D_t = mean over its completed pairs of (Y_Zig − Y_Rust). D = mean of D_t over tasks, with equal task weights.
- **Discordant pairs:** a rescue is Rust 0 / Zig 1, a loss is Rust 1 / Zig 0. R and L are their counts over the analysed pairs.
- **Superiority:** one-sided exact paired McNemar, p_plus = Pr[Binomial(R+L, ½) ≥ R], and p_plus = 1 if R+L = 0. Inclusive tail, no mid-p, no continuity correction.
- **Harm:** p_minus is the same with L in place of R.
- **Alpha split, per direction:** .025 at the interim and .025 at the final analysis.

## Interim analysis (exactly one)
- **When:** after the first 12 pairs in PLAN order (the smoke pair plus pairs 2–12) are all officially graded. The launcher stops at that boundary (`--through-pair 12`) and resumes only with `--from-pair 13` after the interim.
- **D at the interim:** equal weights over the tasks represented among those 12 pairs.
- **Stop early, "Zig worse" (conclusive):** if D ≤ −0.15 and p_minus < .025.
- **Stop early for futility (INCONCLUSIVE; Rust stays):** if, even when every remaining planned pair is a rescue, the final superiority criterion (D ≥ +0.15 and p_plus < .025) cannot be met.
- **Otherwise:** continue to the full planned schedule.
- **No superiority stop at the interim.** Zig can only win at the final analysis.

## Final decision, in this order
1. **INVALID** if the arm-fixed comparison, the hidden suite, the grader or the registration was compromised, or the transport-replacement cap was reached.
2. **INCOMPLETE** if any assigned cell is unstarted or unfinished, or any delivered candidate lacks its official grade. This doesn't apply after a pre-registered early stop.
3. **ZIG REPLACES RUST** only if D ≥ +0.15 and p_plus < .025.
4. **ZIG WORSE (conclusive, Rust stays)** if D ≤ −0.15 and p_minus < .025. This also covers the interim stop.
5. **INCONCLUSIVE (Rust stays)** in every other case, including the futility stop.

## Power, stated before data
Rust's history on these tasks with the same model is about 83% full pass (r70 tasks 1/3/4/6: 8/10; rve-ext tasks 2/5/7: 5/6). Over the 21 pairs that means about 3.6 expected Rust failures. Superiority at .025 needs, for example, 6 rescues and 0 losses (p = .0156), or 8 rescues and 1 loss (p = .0195). The chance of a "Zig replaces Rust" verdict is therefore small even if Zig is truly better. The informative outcomes are "Zig worse" or "inconclusive". This was disclosed to and accepted by the owner before registration.

## Secondary measurements (descriptive; no decision weight)
- Per task and arm: pass counts, official tests passed/total from the grader's own summary, and build success.
- Per arm: total tokens (uncached input + cached input + output; reasoning is part of output), median and total wall time, and token/pass and wall/pass, including failures and retries.
- Reasoning and cache semantics are reported as the harness records them.
- The analysis runs within task blocks, on one host.

## Budget and stopping
- **Budget:** 42 cells plus up to 4 replacements; about 6–10 minutes and about 0.4–0.6M tokens each; under 30M Luna tokens in total.
- **Stopping:** only the interim rule above, or an operational pause (disk, load, login, egress). An operational pause keeps the schedule and resumes it unchanged.
