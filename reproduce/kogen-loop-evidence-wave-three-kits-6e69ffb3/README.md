# Three-task Loop evidence wave

Three request-only tasks examined on the current release; no new Loop fault demonstrated. Two stopped for questions. No valid matched behavior comparison; tool feedback coverage is incomplete.

This is a descriptive evidence wave, not a patch efficacy screen. One attempt
per task; gpt-6.1-terra medium in every role; one candidate arm and two worker
slots. No answerer, new control, retry or Claude route. Failed attempts count.

| task | valid Intent | separating acceptance | outcome | hidden all-pass |
| --- | --- | --- | --- | --- |
| rails-ft-i18n-support | False | unknown | questions_pending | False |
| rails-ft-mysql-fulltext-search-foundation | True | unknown | build_blocked | False |
| rails-ft-notification-bundle-window-overlap | False | unknown | questions_pending | False |

The stored adopted-release cells for two tasks stopped before model requests
on environment errors. The third has no retained baseline in the inspected
stores. No matched rescue, regression, statistical or no-fault generality claim
is supported. The inaccessible additional store is a coverage gap.

See data/results.json for per-task provider calls, event counts, phase timing,
known token usage and outcome. Provider intervals measure network/model service,
not model compute alone. The remaining wall includes tools and orchestration;
it is not an exact tool-wall estimate. Partial usage is a lower bound. Dollar
cost and helper/orchestration cost are unknown. Reasoning is a subset of output.

No reported provider errors were observed. Shell tool argument/result hashes
prove calls occurred but do not establish successful execution or feedback
quality. Absence of retry/condensation events does not prove absence in
unretained payloads. UI/policy questions are shaping outcomes, not Loop faults.
MySQL stopped on a builder-reported contradiction: a protected acceptance
request lacked the account scope required by the application's tenant routing.
Static source inspection supports the concern, but the direct tool evidence is
hash-only and the builder report is not independently proven. This falls under
an already-filed fixture-validity mechanism, so no duplicate request was made.

Disposition: drop further paid work from this wave; a distinct event-backed
mechanism on current source is required to restart the Loop shelf.

## Rerun

No source patch was used. Public release source:
[Kogen release commit](https://github.com/KogenAI/kogen/commit/6e69ffb3243603cd5cd9253efd418a0c24130583).
Archive SHA256: 2779df93030406504f013c72304dfc7370094cd02c624edf7998e83a9749630c.
Binary SHA256: ceedfa2237027cce2c3d7b2fa2ac6aee1969337f9995959140547571b323e477.

Reproduce the derived report with `python3 report.py`. Fresh model execution
requires the three qualified AoR kits, a preauthenticated ChatGPT execution
home, the release above, and the normal lanes admission/setup checks. Use
one g1 arm, reps=1, request-only e2e, all role models
`openai/gpt-6.1-terra medium`, slots=2, deadline_s=3600, cost_cap_usd=30.
Task kits and authentication are not distributed by this pack. After build/plan/preflight and normal admission, the execution command is
`lanes-run RUN_DIR --tasks QUALIFIED_TASKS --hosts RUN_DIR/hosts.json`.
New execution
is nondeterministic and cannot reproduce the exact recorded completions.

## Recorded timing and grades

| task | graded checks passed | total wall s | shaping provider wall s | build provider wall s |
| --- | --- | --- | --- | --- |
| rails-ft-i18n-support | 4/15 | 30.168 | 26.490 | 0.000 |
| rails-ft-mysql-fulltext-search-foundation | 3/16 | 326.02 | 85.009 | 97.171 |
| rails-ft-notification-bundle-window-overlap | 3/10 | 20.24 | 19.066 | 0.000 |

Grade counts include regression checks; they are not hidden-only success counts.
All three grading receipts are complete, with no overall infrastructure error.
The separate acceptance-separation matrix is unavailable: shaping did not finish
for the two question stops, and the approved run copy has no reference tree.
It is therefore unknown, not a successful separation measurement.

Known whole-wave contestant usage is 808,128 input tokens (706,944 cached),
6,314 output tokens, including 1,212 reasoning tokens. Failed attempts are
included. No additional paid helper model run was started by this wave.
The orchestrating agent's usage is unavailable and dollar cost remains unknown.
