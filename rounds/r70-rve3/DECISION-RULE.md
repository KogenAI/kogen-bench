# Round rve3: Rust vs Elixir on Round-70 tasks (pre-registration)

Registered 2026-10-09 before any rve3 model cell. This is the fresh re-registration after rve2 was stopped and recorded INVALID.

## Hypothesis and decision
- **Question:** with the same model, task, hidden suite and grader, does the agent gpt-6-luna at max effort reach a hidden-suite full pass more often in Rust or in Elixir on Round-70 tasks 1, 5 and 7?
- The decision is **Rust better**, **Elixir better** or **INCONCLUSIVE**. Inconclusive is a valid outcome.

## Arms and fixed configuration
- Arms are `r70-N-rust` and `r70-N-elixir` for N ∈ {1, 5, 7}.
- Agent command line 0.161.0, as pinned and installed by kit `2ac8194d9ef1d8a8bde9ae50593f6bc6f1dcc43f`; model gpt-6-luna at max effort.
- The published lane is `task-runner TASK RUN_ID gpt-6-luna max`. It officially grades each cell as soon as it ends with the kit's shipped grader.
- One cell at a time per host; the lane enforces this. The launcher enforces a 3,600-second cell limit by stopping unit `bench-<run_id>` at 3,600 seconds because the lane itself has no limit. There are 0 model retries.
- Before every cell, the launcher resolves the active kit root, hashes `$KIT/tasks/$TASK/prompt.md`, and compares it to `prompt_sha256_original` in that task's `task.json`. A mismatch or preflight read error is logged as `PREFLIGHT-FAIL` and exits that host's queue without starting the cell.

## Hosts and integrity disclosures
- Hosts are Europe host and US host. Each host used its own agent device login. Both cells of each pair ran on the same host, back to back, so host and account were identical within every pair; the accounts differed between hosts.
- Kit is public kogen-bench main commit `2ac8194d9ef1d8a8bde9ae50593f6bc6f1dcc43f`; it restores the original task prompts. Each registered task prompt's SHA-256 equals that task's `prompt_sha256_original`.
- **rve2 was stopped and recorded INVALID** because the published prompts for tasks 5 and 7 differed from their recorded originals, a task-definition confound. rve3 is a fresh registration with the restored prompts and the per-cell prompt-hash preflight above.
- **Lane network defect:** the published lane's agent sandbox does not restrict network, while the r70 hidden suites are public on GitHub. This is a known kit defect to be fixed after the round.
- **Host mitigations in force:** a provider-only egress firewall for the bench uid; a static `/etc/resolv.conf` (the lane uses `/run` tmpfs); and root's git `safe.directory=*` to address the lane ownership defect. Before the first cell, a no-model probe as bench in the lane sandbox must show `github.com`, `raw.githubusercontent.com` and `codeload.github.com` blocked and `chatgpt.com` reachable. Because the firewall is IP-level, another site served from the same provider-edge IPs may not be blocked.
- **Audit:** post hoc, count (counts only) `github.com`, `githubusercontent` and `kogen-bench` strings and `web_search` calls in every cell's interaction log. A flagged cell scores Y=0 and is reported. More than 2 flagged cells makes the round INVALID.
- Known lane defects: the agent sandbox has open network access; `patch.diff` omits untracked files although grading uses the full tree; and the manifest can contain a stale `agent_version`.
- The owner requested and received a descriptive peek in rve2 before its stop; it is recorded in rve2's `STATUS-INVALID.md` and `PEEKS.log`. The rve2 work trees remain on the hosts.
- This is an urgent same-day registration ordered by the owner. The firewall mitigation and post-hoc audit are disclosed above, as are the lane defects.

## Preconditions (hard gate before the first cell)
Every precondition below must hold on **both** hosts before either host starts its first cell. Record host-specific verification and evidence in the round's operational record. If any condition fails, no scored cell may start until it is corrected and re-verified.
- The installed kit is commit `2ac8194d9ef1d8a8bde9ae50593f6bc6f1dcc43f`, and the installation check reports 0 FAIL.
- Root's git `safe.directory` includes `*`.
- `/etc/resolv.conf` is a regular file.
- The nftables table `inet rve2_egress` is present.
- An egress probe as the execution account in the lane sandbox shows `github.com`, `raw.githubusercontent.com` and `codeload.github.com` BLOCKED and `chatgpt.com` reachable.
- The prompt preflight passes for all six task/arm kits (tasks 1, 5 and 7, both arms).
- One unscored end-to-end dry cell per host has a complete record.

## Population and frozen plan
- Tasks 1, 5 and 7 × 6 pairs each = 18 pairs and 36 cells; seed 20261010.
- Pairs are ordered in two blocks: block 1 is pairs 1–9 (3 per task), block 2 is pairs 10–18 (3 per task); order is shuffled within each block. Each task's six pairs are split 3 EU / 3 US, and block 1 is as balanced across hosts as possible (5/4). Arm order within each pair is random from the same generator. Each host runs its pairs in global plan order.
- The schedule is frozen in `PLAN.json`; its `plan_sha256` is over canonical JSON for the `pairs` list.

## Outcome and intention to treat
- **Outcome:** Y=1 only for an official lane grade with `pass_` true. Timeout, no patch, build failure, model failure and flagged audit all score 0.
- Every assigned cell keeps its assigned arm (ITT). A missing or ungraded assigned cell makes the analysis INCOMPLETE unless a pre-registered stop applies.
- **Transport replacement (outcome-blind):** use rz1's rule: at most 2 replacements per arm, judged from transport receipts before any patch. A transport failure is an HTTP, stream or auth error, or runner infrastructure error, before any patch was produced. A cell that produced a patch is never replaced. Replacements go at the end of that host's queue. Reaching the cap makes the round INVALID. Keep and report every attempt.

## Primary estimand and exact tests
- R = pairs with Rust 1 / Elixir 0; L = pairs with Rust 0 / Elixir 1; D = (R − L) / pairs analysed.
- p_rust = P[Binom(R+L, ½) ≥ R] and p_elixir = P[Binom(R+L, ½) ≥ L]. If R+L=0, both p values are 1. These are inclusive exact tails, with no correction.
- Thresholds are D ≥ +0.15 and p_rust < .025 for **Rust better**, or D ≤ −0.15 and p_elixir < .025 for **Elixir better**.

## Interim analysis (exactly one)
- **When:** after pairs 1–9 are all officially graded.
- Stop with **Rust better** if D ≥ +0.15 and p_rust < .025, or **Elixir better** if D ≤ −0.15 and p_elixir < .025.
- Stop for futility (**INCONCLUSIVE**) if neither direction could meet its final criterion even if all 9 remaining pairs were discordant in its favour.
- Otherwise continue. The launcher does not pause at the interim. Cells beyond pair 9 that finish before the interim decision are kept and reported descriptively if the round stops there.

## Final decision, in this order
1. **INVALID** if the arm-fixed comparison, hidden suite, grader or registration was compromised, or the transport-replacement cap was reached; more than 2 flagged audit cells also makes it INVALID.
2. **INCOMPLETE** if an assigned cell is unstarted or unfinished, or a delivered candidate lacks its official grade, unless a pre-registered early stop applies.
3. **Rust better** if D ≥ +0.15 and p_rust < .025.
4. **Elixir better** if D ≤ −0.15 and p_elixir < .025.
5. **INCONCLUSIVE** in every other case, including the futility stop.

## Power, stated before data
Eighteen pairs give modest power. **INCONCLUSIVE is a valid outcome.** No repetitions are added except transport replacements under the rule above.

## Secondary measurements (descriptive only)
- Per arm: tokens, wall time, tests passed/total.
