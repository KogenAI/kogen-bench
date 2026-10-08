# Public glossary

Definitions here describe the public record. A historical arm label identifies a recorded variant; it does not establish an exact recipe unless its round page or a linked protocol provides one.

## Models and harnesses

| Term | Meaning |
|---|---|
| Codex | OpenAI coding-agent product used as a benchmark harness or model client, as named by the study. |
| Grok Build | xAI coding-agent product named in the benchmark scope. |
| Kogen (`kh`) | Coding-agent harness evaluated in this repository. `kh` is a historical shorthand. The stages used are round-specific. |
| direct Codex | A single Codex run without Kogen stages, where a round defines that contrast. |
| Luna | Model alias for `gpt-6-luna`. |
| Sol | Model alias for `gpt-6.1-sol`. |
| Astra | Model alias for `gpt-6-astra`. |
| Model and effort labels | Names such as `low`, `medium`, `high`, `max`, and `xhigh` are recorded settings. A label alone does not establish the provider setting actually sent. |
| RvE | Rust-versus-Elixir comparison label used in the R70 stack study. |
| FE2 | Fixed-front-end variant used in the separate pre-registered Round 70 rerun cohort. |
| Rule L | Smoke admission threshold: at least half the reference pass fraction, rounded up to a whole test. |
| X-control | Reference solution submitted through the contestant path as a control; it is not a scored cell. |

## Historical arm and workload labels

| Term | Meaning |
|---|---|
| `P` | Historical prefix for Kogen pipeline arms. The remaining label and round record identify the comparison; the exact stages and settings are round-specific. |
| `P-full` | Historical full-pipeline arm label in the R56 ablation family. The label alone does not identify the full recipe or revision. |
| `P-noctx`, `P-noplan`, `P-nocontract`, `P-noreview` | R56 ablation labels for variants omitting the named context, planning, contract, or review stage. Exact recipes and revisions remain round-specific. |
| `P-*`, `P*`, `B-ctx-*` | Exported historical arm labels. A suffix is not a shared codebook across rounds; use the associated round record for any supported expansion. |
| `plan-shell` | A Kogen arm label associated with a planning shell. Its implementation and revision are round-specific. |
| `ladder` | A multi-stage Kogen builder configuration whose exact stages are round-specific. |
| `best-of-N` | Selection among N candidate outputs. Candidate generation and the selection rule are round-specific; if unpublished, the exact procedure is not derivable from this record. |
| `W1`, `W2`, `W5`, `B2`, `B3`, `p12`, `p17`, `p21`, `agentic30` | Historical arm or stage labels retained to identify exported rows. Their full codebook is not established across rounds. |
| Jev (r47) | Name used for the tested router tool or arm in the surviving r47 record. Its exact implementation and version are not established by the public record. |

## Analysis terms

| Term | Meaning |
|---|---|
| Intention-to-treat (ITT) | Count assigned cells unless a documented environment or adapter fault proves an exclusion under the applicable analysis rule. Model, provider, runner, and timeout failures remain outcomes. Ungraded, cancelled, and missing deliveries remain explicit in the planned denominator; smoke and control cells are outside the scored denominator. |
| Percentage point (pp) | Arithmetic difference between percentages; it is not a relative percent change. |
| Fisher exact test | Exact test of association for a 2-by-2 contingency table. State whether it is one-sided or two-sided. |
| Holm correction | Holm–Bonferroni step-down adjustment for a declared family of comparisons. A p-value without the test and family is not reproducible. |
| CMH-style | A comparison stratified across groups using a Cochran–Mantel–Haenszel-style method. The study must specify its test and strata. |
| Pass, fail, unresolved, not scored | Distinct exported intention-to-treat outcome labels. `Unresolved` and `not_scored` are not failures. |
| DESCRIPTIVE, EXPLORATORY, CONFIRMATORY | Analysis labels for summaries of observed data, hypothesis generation, or analysis governed by a predeclared protocol. |

## Round status labels

| Term | Meaning |
|---|---|
| VALID, CONFOUNDED, INVALID, INTERIM | Outcome-validity labels used in the round register. |
| WITHDRAWN, NOT-RUN, PRE-REGISTERED | Lifecycle labels for a withdrawn study, a study without scored runs, or a registered design with no scored cells. |
