# kogen-executor-phase-api-2f13bd4

The executor component's new head cannot be screened on the adopted Kogen source with its paired component heads: the assembled program does not compile. **Behaviour unresolved; no model runs, no qualification for adoption.** This is a failed assembly check, not evidence that model performance got worse.

## What was checked

Seven commits after the last qualified executor revision were classified by their source diffs. Four add run-event telemetry. Two add and integrate a shared package unused by the adopted consumers. The final commit removes phase-owned prompts, submission tools and shared Build APIs from executor. That last change needs compatible consumers; it cannot be called behaviour-identical merely because the policy is intended to move elsewhere.

The fixed adopted Kogen source is `573d023`. The candidate executor is `2f13bd4`. The exact companion revisions are recorded in `evidence.json`. The previously built assembly used executor `a55cc55` and older shaping; its binary does not test this head and was not reused as evidence.

With adopted shaping, executor's deleted APIs are still referenced. With paired shaping main, Kogen's engine still calls the old shaping setup entry point, which that main has removed. The recorded candidate build reaches that second failure: the two missing symbols are `shape.Init` and `shape.InitInput`, both referenced at the same call site.

## Result

| observation | result |
|---|---|
| Offline candidate compilation | failed, two missing symbols |
| Toolchain | Go 1.27.2, Linux amd64 |
| Assigned model runs started | 0 |
| Model requests and paid screen cost | 0 and $0 |
| Intent validity, acceptance separation, hidden correctness | unmeasured |
| Model and effort | no model called; planned all roles Terra medium, native backend |
| Commit to compiler feedback | 107.57 minutes, including the failed attempt |
| Verdict | unresolved |
| Disposition | drop this incompatible tuple |

The check took the exclusive build lock and used offline source snapshots; its five-minute load reading was 0.02. No control or candidate model arm was launched. There are no discordant task outcomes to attribute and no model-stage mechanism witness. The failure belongs to assembly compatibility.

## Limits and next step

This does not prove a behavioural regression or non-regression. A compatible Kogen consumer, or compatible component consumer revisions retaining the setup entry point, is needed before a fresh candidate-only screen. No compatibility patch or newer Kogen source was substituted. The current executor head remains unqualified.

## Rerun

The screened component sources are not public; `evidence.json` identifies each by commit and records the compiler errors.

To recompute the verdict from recorded evidence without compiling:

```sh
python3 -I reproduce/kogen-executor-phase-api-2f13bd4/report.py reproduce/kogen-executor-phase-api-2f13bd4/evidence.json | diff - reproduce/kogen-executor-phase-api-2f13bd4/expected-output.txt
```

The report checks recorded evidence; it does not rerun the compiler or measure model behaviour.
