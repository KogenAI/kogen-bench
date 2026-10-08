# L4 deterministic context packet decision rule

STATUS: **DESCRIPTIVE** (see the round README: post-result amendment, non-interleaved controls)

The original design was frozen on 7 October 2026 before any scored L4 cell. Amendment 1 below is reproduced verbatim, including its disclosure that it was written after 6 of 12 packet outcomes were known; Amendment 1 governs the final comparison and decision. The original historical-baseline rule is retained as design history.

## Original pre-registration

### Question and pool

For the four L1-admitted failure variants `r70-2-elixir`, `r70-2-go`, `r70-4-elixir-fe2`, and `r70-7-rust`, does a frozen deterministic context packet derived only from public task material improve official full-suite pass outcomes for gpt-6-luna at max?

### Arms and inputs

The original baseline arm reused distinct valid official Luna-max cell IDs for each source variant. The packet arm used one public variant per source task, with an unchanged public task tree and a prompt that appended only its frozen context packet. The packet was written once from public prompt, skeleton, and interface material. Packet cells used gpt-6-luna at max, three fixed seeds per variant, a 3,600-second cap, and zero retries. Elixir and Rust were assigned to EU; Go to US.

The original primary outcome was full-suite pass rate by variant. A partial test count was not a pass. The original decision rule compared packet outcomes with historical baseline outcomes and included a failure-class condition; Amendment 1 replaces that primary analysis and removes that condition. The original first-seed futility gate was to stop only if no first-seed packet cell rescued its historical baseline.

### Fairness and accounting

The planned controls held model, effort, runner, sandbox, timeout, retry count, public task tree, host assignment, and official grading route fixed. The packet was the only prompt change. One token definition applies throughout: uncached input, cached input, and output; total is their sum.

The original preparation record required release checks before scored cells. This paragraph records the state at registration; the scored packet and control cells reported here were later run and officially graded.

## Amendment 1 (7 Oct 2026, ~14:40Z, before any control launch): contemporaneous controls and paired analysis

Reason: historical baselines confound the packet with cohort and time changes. A pass on a variant whose baseline is below 100% is not a repair of a failed state. "No new failure class" cannot be measured from aggregate fields. Amendment adopted 7 Oct 2026. Disclosure: this amendment was written after 6 of the 12 packet outcomes were known (all four seed-1 cells and 2-go seeds 2–3); no control outcome was known.

- **Controls:** 12 contemporaneous no-packet cells. Each uses the source task unchanged (`r70-2-go`, `r70-2-elixir`, `r70-4-elixir-fe2`, `r70-7-rust`) with gpt-6-luna at max, seeds 1, 2 and 3 as reps 51, 52 and 53. Harness, sandbox, host, 3,600-second cap, zero retries and grading route are the same as the packet arm. EU runs its 9 controls in the seeded random order `random.Random(20261017).shuffle`: r70-7-rust r53, r70-4-elixir-fe2 r53, r70-2-elixir r53, r70-7-rust r51, r70-7-rust r52, r70-2-elixir r52, r70-4-elixir-fe2 r51, r70-2-elixir r51, r70-4-elixir-fe2 r52. They run alongside the remaining EU packet cells. The US 2-go controls run after the US packet cells had finished and are labelled **not interleaved**.
- **Primary analysis (paired per variant):** P_v = packet passes out of 3, and C_v = control passes out of 3. Keep packets in spec sections 3.2 and 4.9 only if Σ_v (P_v − C_v) ≥ +2 across the 4 variants, P_v ≥ C_v on at least 3 of 4 variants, and the regression rule does not fire. Otherwise drop them.
- **Rescue** is reserved for a seed s where the control failed and the packet passed (paired by seed). A **loss** is the reverse. Both are reported per variant.
- **Regression rule:** on any variant, if the mean official tests_passed of the packet cells is more than 1 test below the mean of the control cells, packets are dropped regardless of pass counts.
- **Removed:** the "no new failure class" condition.
- **Historical baselines** remain descriptive context only. The futility gate already applied stands. Packet cells already run keep their official grades.
- **Label:** descriptive pilot with n = 3 per arm per variant; the thresholds are coarse and support no general claim.
