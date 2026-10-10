> Publication copy: private locations and the operator answer column are removed.
> Historical future-tense wording is retained; the results describe the completed run.

# Lean versus Quint for source connected feedback

Question: given equivalent connections to actual application code, which backend gives an agent more useful information for finding and repairing a defect?

This is a small pilot proposal prepared on 10 October 2026. It compares Lean and Quint. No trials have run. Fixtures and a limited code translation still need implementation. It measures practical performance, not the amount of training data a model saw.

## Scope

Use the same four small Elixir fixtures in both arms. Translate their actual implementation into Lean and Quint and preserve equivalent source locations. Avoid comparing Lynx translation with a manually written Quint Connect driver: that would confound the backend with its integration.

Build only the translation needed for these fixtures: named helper calls, boolean conditions, explicit record transitions and equality over finite enum tokens. Use one common frontend/lowering and two emitters. Unsupported constructs must fail explicitly. This is not a general Elixir translator or a cross-language platform. The limited translator must regenerate from each original-code patch; editing a separate formal copy alone does not repair the application.

Dafny and Why3 are other plausible backends. Keep them outside this first pilot. Verus is relevant if we later study Rust. Their official references are [Dafny](https://dafny.org/), [Why3](https://why3.org/) and [Verus](https://verus-lang.github.io/verus/guide/).

## Four tasks

| Task | Fixed accepted behavior |
| --- | --- |
| Tenant access | Access requires both an allowed role and matching tenant |
| Exact approval | A Build requires approval for its current revision |
| Preservation | Failed preservation retains the sole work copy |
| Cache identity | Cache reuse requires matching tree and context |

The private operator catalog owns fixture details and bounded domains. The operator catalog contains answers and is excluded from agent access. Scheduling, storage and revision changes are explicit events; this panel does not verify real disk durability or all process interleavings.

## Fair inputs

Each arm receives the same application, public API, fixed contract, starter tests, documentation access and source mapping. Supply checked initial proof/verification packages so this pilot measures diagnosis and repair rather than initial authoring. Allow proof annotations to be maintained after a repair; accepted laws and assumptions remain fixed.

Use the same finite domains and maximum sequence length in both arms. Lean may prove a stronger claim, but report that separately. Do not count sampled replay as equivalent to exhaustive checking or a completed proof. A failed proof means unresolved verification until evidence shows an implementation defect.

Before scored runs, check both emitted representations against an independent finite oracle, check source mappings, and ensure both detect each planted violation. The correct reference and alternate valid repairs must pass; faulty bases and plausible wrong repairs must fail. Keep the oracle independent of both emitters. These checks qualify this restricted translation, not all Elixir semantics.

## Run the pilot

Starting location: `<record>`. Keep code, dependencies and raw output there. Create a root README when implementation begins and link this protocol.

Accepted model setting for all work in this benchmark: **GPT-6.1 Sol (`gpt-6.1-sol`), High (`high`)**. This covers building and validating fixtures and bridges, and every repair trial in both arms. Keep the trial setting fixed; individual failures do not trigger escalation. Almir, 10 October 2026, in this chat: “Let's use Sol 6.1 high instead for everything.” This replaces the assistant's proposed Astra Medium construction and Sol Medium trial settings; it does not change unrelated projects or this chat's active model.

1. Implement the four fixtures, independent grader and limited frontend with Lean and Quint emitters. Include correct variants in qualification to detect unnecessary repairs.
2. Pin the fixtures, contracts, mappings, tools and docs by hash. Admit both arms using the checks above. If either cannot qualify, record that limitation rather than silently changing the task.
3. Pin the harness version and use `gpt-6.1-sol` with `high` effort. Run each task three times per arm in fresh sessions, randomizing order. This is 4 tasks × 2 arms × 3 repeats = 24 trials.
4. Use equal caps: 15 minutes, 60,000 total model tokens and ten complete verification/test cycles per trial. The harness must enforce the first reached cap. Record installation/translation engineering separately from per-trial runtime and billed cost.
   Token accounting follows the operator's [2026-10-10 amendment: uncached input plus output](AMENDMENTS.md).
5. Require a diagnosis before the first patch: violated property, suspected causal function and evidence. Let the agent repair original Elixir code, regenerate representations and recheck.
6. Grade the final application independently with sealed tests/oracle. Preserve diagnostics, diagnosis, patch, hashes, time and usage for every trial. Never let a weakened contract or changed assumptions count as a successful repair.
7. Report correct repairs out of 12 trials per arm, causal diagnosis, regressions, time and total cost per successful repair. Show each task separately. This pilot selects what to investigate; it cannot establish a broad winner from four tasks.

The schedule helper is ready and launches nothing:

The scheduling helper used four tasks, two arms and three repeats.

Replace the harness version placeholder before launch. The fixtures, verification commands and isolated execution harness must be implemented and admitted first. Run agents without access to this catalog, hidden tests or alternate answers; prompt-only hiding is insufficient.

Common prompt:

> Identify the violated property and causal function, explaining your evidence before patching. Repair the application to satisfy the fixed contract and preserve its API. Keep accepted laws and assumptions unchanged. Regenerate formal representations from the changed application and run the supplied checks. If verification fails because of a proof or tooling limitation, distinguish that from an implementation defect. Submit the patch and verification results within the budget.

## Resume and finish

Keep an append-only ledger keyed by task, arm, repeat and snapshot. After interruption, inspect process ownership and saved outputs before relaunching. Preserve valid completed results; mark interrupted trials and retain their consumed budget. Do not retry wrong answers until they pass. A translator or grader defect invalidates affected comparisons and requires a new qualified snapshot.

Finish when all 24 trials are accounted for and their independent grades, artifacts and costs are retained. If results justify more work, the next experiment can remove source mappings or use fresh tasks. No additional experiments are part of this pilot.

Technical basis: [Lynx translation](https://github.com/josevalim/lynx/blob/main/lib/lynx/translation.ex), [Lean](https://lean-lang.org/theorem_proving_in_lean4/Introduction/), [Quint property checking](https://quint.sh/docs/checking-properties). The previous expanded design is retained as private superseded proposal history.
