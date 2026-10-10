# Race 3 results page — pre-declared outline (written before the race; frozen with DECISION-RULE.md)

1. **Verdict.** One sentence, from the decision rule only: "X wins (best median time to TARGET/N (50/56) and best in N of 4 runs)", or "No decisive winner", or "Target not reached; ranked by median score/56".
2. **Primary table.** Per language: time to TARGET/N (50/56) in runs A, B, C and D (stall-adjusted, with raw in brackets), median, runs won, and FINAL score /56 per run.
3. **Score curves.** Score/56 at every 5-minute snapshot: one chart per run with all five languages, plus a combined median curve.
4. **Milestones.** Time to 75 %, 90 % and 100 % of the 56 scored cases, per run and as the median.
5. **Cost.** Per arm and as per-language medians:
   - input, cached, output and reasoning tokens;
   - estimated quota points;
   - turns; CPU-seconds;
   - model-wait vs command time;
   - stalls (count and time).
6. **Engineering.** Per language at FINAL, as medians with ranges:
   - cold and incremental start-to-ready time;
   - own test-suite time;
   - artifact size (with each language's method stated);
   - startup median; median invocation runtime; peak RSS;
   - lint findings; LOC; test definitions.
7. **Maintainability (blind review).** Rubric scores 1–5 (structure, error handling, test quality, readability) with short reasons; reported separately and never combined with the conformance result.
8. **Integrity.**
   - flaky cases per arm (double scoring within TARGET±3 and FINAL) and clean-copy regrade differences;
   - audit flags and model/effort receipts;
   - CPU-cap sampler (peak and p95 per arm), stalls and throttling on the shared account;
   - harness faults, if any, and the invalidation outcome.
9. **Setup and disclosures.** Hosts, toolchains, kit (aids, guides, libraries, sources, checksums), the soft caps and efficiency cores, the network-on sandbox with the audit guard, the `~/.codex` history, warm-up scoring, the frozen suite and SPEC-BUG list, and the decision-rule hash.
10. **Reproduce.** Links to briefs, kit manifest, harness, suite, decision rule, Standard records, per-case results.

Nothing is added, dropped or re-weighted after the data are seen. Any extra analysis appears under a clearly labelled "post-hoc (not pre-declared)" heading.

Frozen inputs sha: `2eeacf689c103dc3`. Registered TARGET/N: 50/56; exclusions: 88 of 144.
