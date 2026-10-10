# Round rve2: Rust vs Elixir on Round-70 tasks (pre-registration)

Registered 2026-10-09 before any rve2 model cell. This is a pre-registered redo of r70-rve.

## Hypothesis and decision
- **Question:** with the same model, task, hidden suite and grader, does the agent gpt-6-luna at max effort reach a hidden-suite full pass more often in Rust or in Elixir on Round-70 tasks 1, 5 and 7?
- The decision is **Rust better**, **Elixir better** or **INCONCLUSIVE**. Inconclusive is a valid outcome.

## Arms and fixed configuration
- Arms are `r70-N-rust` and `r70-N-elixir` for N ∈ {1, 5, 7}.
- Agent command line 0.161.0, as pinned and installed by the kit; model gpt-6-luna at max effort.
- The published lane is `task-runner TASK RUN_ID gpt-6-luna max`. It officially grades each cell as soon as it ends with the kit's shipped grader.
- One cell at a time per host; the lane enforces this. The launcher enforces a 3,600-second cell limit by stopping unit `bench-<run_id>` at 3,600 seconds because the lane itself has no limit. There are 0 model retries.

## Hosts and integrity disclosures
- Europe host and US host were freshly built 2026-10-09 from the same public kit, with doctor 80/0 and the r70-1 proof controls 6/6.
- Each host used its own agent device login. Both cells of each pair ran on the same host, back to back, so host and account were identical within every pair; the accounts differed between hosts.
- **Lane network defect:** the published lane's agent sandbox does not restrict network, while the r70 hidden suites are public on GitHub. This is a kit defect to be fixed after the round.
- **Mitigation:** during the round, a host egress firewall limits the bench uid to loopback/DNS and provider endpoints (`chatgpt.com`, `ab.chatgpt.com`) at IP level. Before the first cell, a no-model probe as bench must show `github.com`, `raw.githubusercontent.com` and `codeload.github.com` blocked and the provider reachable. Because this is IP-level, another site served from the same provider-edge IPs is not blocked.
- **Audit:** post hoc, count (counts only) `github.com`, `githubusercontent` and `kogen-bench` strings and `web_search` calls in every cell's interaction log. A flagged cell scores Y=0 and is reported. More than 2 flagged cells makes the round INVALID.

## Population and frozen plan
- Tasks 1, 5 and 7 × 6 pairs each = 18 pairs and 36 cells; seed 20261009.
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

## Disclosures
- This is an urgent same-day registration ordered by the owner.
- The hosts use different accounts. The firewall mitigation and post-hoc audit are disclosed above, as is the published lane's network defect.
