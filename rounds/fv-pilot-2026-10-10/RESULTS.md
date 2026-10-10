# Lean versus Quint verification pilot: results

Both arms reached 12 correct repairs out of 12 valid trials. This is a
ceiling: the protocol's main measure does not separate them. The effort
observations below are secondary and descriptive. There are only three
repeats per task and arm, with 12 trials per arm across four small tasks.
These observations support no broad winner claim.

Lean is a proof assistant that checks formal definitions and proofs.
Quint is a specification language with model checking for state transitions.
Both worked from the same Elixir applications, contracts and starter tests.

## How and where it ran

All valid trials ran on one Hetzner Linux host (2 vCPU) in Europe, with
Codex CLI 0.161.0, requested gpt-6.1-sol and high effort, using the same
account throughout. Each trial used a fresh session. The fixed randomized
schedule specified three repeats for each task and arm. Concurrency was
at most two trials; remaining trials ran sequentially.

Valid trial UTC interval: 2026-10-10T13:59:16Z to 2026-10-10T14:57:28Z.
Infrastructure-invalid UTC interval: 2026-10-10T13:39:55Z to 2026-10-10T13:47:13Z.

Equal caps were 900 seconds, 60,000 uncached input plus output tokens,
and ten complete check cycles. A cycle regenerates the representation,
checks the fixed laws and runs starter tests; failed checks consume cycles.
Reported wall time covers the agent trial, not construction or later grading.

## Per-task results

Each bracket gives the observed minimum–maximum; preceding values are
medians. Diagnosis counts are match / partial / miss, using the fixed
grader rule: both property and function phrases = match, one = partial,
neither = miss. This is a deterministic text score, not a human assessment
of explanation quality. Regression counts are reported final-grade failures
in protected behavior and checks, not a claim about all possible behavior.

| Task | Arm | Correct / 3 | Diagnosis M/P/X | Before patch | Cycles median [range] (sum) | Wall seconds median [range] | Capped tokens median [range] | Raw tokens median [range] | Regressions |
| --- | --- | ---: | --- | ---: | --- | --- | --- | --- | ---: |
| F01: Tenant access | Lean | 3/3 | 3/0/0 | 3/3 | 2 [2–2] (6) | 78.9 [69.2–80.3] | 21,971 [18,581–39,132] | 220,499 [194,140–222,357] | 0 |
| F01: Tenant access | Quint | 3/3 | 3/0/0 | 3/3 | 4 [3–4] (11) | 119.8 [103.0–135.6] | 31,957 [26,272–32,882] | 227,360 [208,853–319,346] | 0 |
| W01: Exact approval | Lean | 3/3 | 3/0/0 | 3/3 | 2 [2–5] (9) | 88.6 [84.8–120.7] | 29,040 [22,313–30,974] | 194,558 [191,856–277,161] | 0 |
| W01: Exact approval | Quint | 3/3 | 2/1/0 | 3/3 | 3 [2–6] (11) | 119.4 [100.6–178.8] | 35,442 [18,694–50,078] | 274,162 [229,126–479,646] | 0 |
| W04: Preservation | Lean | 3/3 | 3/0/0 | 3/3 | 4 [3–4] (11) | 110.4 [97.3–126.9] | 28,138 [25,030–39,743] | 290,495 [259,910–327,914] | 0 |
| W04: Preservation | Quint | 3/3 | 3/0/0 | 3/3 | 4 [3–4] (11) | 145.5 [114.6–156.6] | 43,767 [37,401–52,675] | 362,999 [320,323–450,201] | 0 |
| X01: Cache identity | Lean | 3/3 | 3/0/0 | 3/3 | 2 [2–2] (6) | 90.1 [85.2–92.5] | 26,860 [22,306–37,728] | 245,100 [217,634–315,232] | 0 |
| X01: Cache identity | Quint | 3/3 | 3/0/0 | 3/3 | 2 [2–3] (7) | 109.2 [108.1–147.2] | 29,167 [21,499–29,528] | 313,967 [201,723–315,480] | 0 |

## Arm summaries and secondary effort differences

| Arm | Correct / 12 | Diagnosis M/P/X | Before patch | Cycles median [range] (sum) | Wall seconds median [range] | Capped tokens median [range] | Raw tokens median [range] | Regressions |
| --- | ---: | --- | ---: | --- | --- | --- | --- | ---: |
| Lean | 12/12 | 12/0/0 | 12/12 | 2 [2–5] (32) | 89.3 [69.2–126.9] | 27,499 [18,581–39,743] | 233,728.5 [191,856–327,914] | 0 |
| Quint | 12/12 | 11/1/0 | 12/12 | 3 [2–6] (40) | 119.6 [100.6–178.8] | 32,419.5 [18,694–52,675] | 314,723.5 [201,723–479,646] | 0 |

Both arms had diagnosis before the first patch in 12/12 trials (100%).
Lean had 12 matches; Quint had 11 matches and one partial (W01, repeat 1).
The match-rate difference is 8.3 percentage points, one trial.
No valid trial reached a cap or reported a regression.

Descriptive differences below are Quint minus Lean. Ratios are Quint /
Lean; they compare arm medians, not causal treatment effects.

| Secondary measure | Median difference | Median ratio |
| --- | ---: | ---: |
| Check cycles | +1.0 | 1.500× |
| Wall seconds | +30.3 | 1.339× |
| Capped tokens | +4,920.5 | 1.179× |
| Raw tokens | +80,995.0 | 1.347× |

Lean used 32 total cycles and Quint 40: eight more cycles for Quint
(25%). Total agent wall time was 1,124.9 seconds for Lean and 1,538.3
seconds for Quint, a difference of 413.4 seconds (36.8%). Backend runtime
is part of the observed effort. Task difficulty, agent choices, cache use,
host sharing and the small sample limit interpretation. No significance
test or general ranking is warranted.

## Total cost per successful repair

There is no billed dollar record. Tokens measure usage, not money; cached
input and output have different pricing. No dollar cost is estimated.
For each arm, total cost per successful repair in tokens means the sum of
all valid-trial usage divided by the number of correct repairs. Every valid
trial succeeded here, so this is the arithmetic mean, not the median.
Construction, qualification and smoke usage are outside this trial metric.

| Task | Arm | Total capped tokens | Total raw tokens | Capped tokens / correct repair | Raw tokens / correct repair |
| --- | --- | ---: | ---: | ---: | ---: |
| F01 | Lean | 79,684 | 636,996 | 26,561.3 | 212,332.0 |
| F01 | Quint | 91,111 | 755,559 | 30,370.3 | 251,853.0 |
| W01 | Lean | 82,327 | 663,575 | 27,442.3 | 221,191.7 |
| W01 | Quint | 104,214 | 982,934 | 34,738.0 | 327,644.7 |
| W04 | Lean | 92,911 | 878,319 | 30,970.3 | 292,773.0 |
| W04 | Quint | 133,843 | 1,133,523 | 44,614.3 | 377,841.0 |
| X01 | Lean | 86,894 | 777,966 | 28,964.7 | 259,322.0 |
| X01 | Quint | 80,194 | 831,170 | 26,731.3 | 277,056.7 |
| All tasks | Lean | 341,816 | 2,956,856 | 28,484.7 | 246,404.7 |
| All tasks | Quint | 409,362 | 3,703,186 | 34,113.5 | 308,598.8 |

Capped tokens = input − cached input + output. Raw tokens = input +
output. Reasoning is already included in output and is not added again.
Cache-write input is retained when reported and is already part of input.
The token cap is observed only when an atomic request usage report arrives;
overshoot is retained rather than truncated. These trials had no overshoot.

Infrastructure failures consumed additional usage. Counting those attempts
as operational overhead gives the following totals per successful repair;
they remain excluded from the 12-trial success and effort distributions.

| Arm | Invalid attempts | Additional capped / raw tokens | Inclusive capped tokens / success | Inclusive raw tokens / success |
| --- | ---: | ---: | ---: | ---: |
| Lean | 2 | 5,748 / 49,396 | 28,963.7 | 250,521.0 |
| Quint | 2 | 6,948 / 74,660 | 34,692.5 | 314,820.5 |

## Deviations, amendments and infrastructure history

1. Before scored trials, the token cap was interpreted as uncached input
   plus output, excluding cached input. Raw usage remains reported.
2. Before scored trials, both packages removed precomputed checker output.
   Authored bridge replay was restricted to identical source locations only.
   Native backend diagnostics were retained. Checking was mediated by a
   broker, project setup was frozen, and API/completion checks were hardened.
3. The operator waived a second model’s review of the fixes to save time. The supervisor inspected the changes instead, and the full qualification checks were repeated.
4. The four excluded attempts were repeat 2 of tenant access and exact approval, each with Lean and Quint. The command executor was missing from the agent’s execution environment. Correction rows retain the original usage and mark those attempts as infrastructure failures; their artifacts remain archived privately. Replacement attempts used the same scheduled combinations. Valid completed trials were retained. Before restarting, an operational test had to demonstrate command execution, documentation access, a counted check and prevention of bypassing the counted checker. Caps and grading were unchanged. The operational test also
   exposed local socket restrictions and broker-control-file inspection;
   local file transport and cleanup corrected these before scored restart.
5. During the run, the operator moved the second half of the planned
   two-host split to Europe. All 24 valid trials ran on one Hetzner Linux host in Europe, with two virtual CPUs and at most two simultaneous trials, instead of the planned 12 trials in Europe and 12 in the United States. The same harness, readiness approval, Codex binary and account were used for all 24. Schedule rows 13–24 moved to that host and its existing account configuration; the earlier allocation was retained. The United States host ran no trials. Task order, packages, model, effort, caps, checking, isolation and grading were unchanged.
6. After initial admission, harness launch parameters were changed to specify the account configuration directory, expected account and host-specific readiness approval. Launch used Europe’s approval; overall approval remained false because the second host was pending. Recorded harness versions in the schedule were updated without changing trial order, and deployed files were reconciled before launch.
7. Two power losses on the operator’s local workstation had no effect on trials because they ran on the
   European Linux host. Exact power-loss times were not retained here.
8. Two interrupted qualification evaluation attempts were repeated
   sequentially with unchanged sources after an output-redirection fault.
   No completed application failure was rerun to obtain a passing answer.
9. Standard capture is incomplete: no billed cost, phase-level usage,
   host boundary telemetry or provider-effective receipt is supplied.
   The package declares these gaps and remains DESCRIPTIVE.

The protocol and amendments are preserved as sanitized publication copies.
The sanitized ledger retains all 59 lifecycle rows, including running
entries, superseded infrastructure completions and four correction rows.
Analysis takes each cell’s latest status, then excludes infra-invalid
attempts; their usage is shown separately. Final grades and diagnosis scores
are source-reported receipts. The private final evaluator is not published,
so this bundle recomputes the analysis but cannot repeat final grading.

## Individual valid trials

| Task | Arm | Repeat | Correct | Diagnosis | Before patch | Cycles | Wall s | Capped tokens | Raw tokens | Regressions |
| --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| F01 | Lean | 1 | PASS | match | yes | 2 | 78.9 | 18,581 | 222,357 | 0 |
| F01 | Lean | 2 | PASS | match | yes | 2 | 69.2 | 39,132 | 194,140 | 0 |
| F01 | Lean | 3 | PASS | match | yes | 2 | 80.3 | 21,971 | 220,499 | 0 |
| F01 | Quint | 1 | PASS | match | yes | 3 | 103.0 | 26,272 | 227,360 | 0 |
| F01 | Quint | 2 | PASS | match | yes | 4 | 135.6 | 32,882 | 319,346 | 0 |
| F01 | Quint | 3 | PASS | match | yes | 4 | 119.8 | 31,957 | 208,853 | 0 |
| W01 | Lean | 1 | PASS | match | yes | 5 | 120.7 | 22,313 | 277,161 | 0 |
| W01 | Lean | 2 | PASS | match | yes | 2 | 84.8 | 29,040 | 191,856 | 0 |
| W01 | Lean | 3 | PASS | match | yes | 2 | 88.6 | 30,974 | 194,558 | 0 |
| W01 | Quint | 1 | PASS | partial | yes | 3 | 119.4 | 35,442 | 274,162 | 0 |
| W01 | Quint | 2 | PASS | match | yes | 6 | 178.8 | 50,078 | 479,646 | 0 |
| W01 | Quint | 3 | PASS | match | yes | 2 | 100.6 | 18,694 | 229,126 | 0 |
| W04 | Lean | 1 | PASS | match | yes | 4 | 126.9 | 39,743 | 290,495 | 0 |
| W04 | Lean | 2 | PASS | match | yes | 4 | 110.4 | 25,030 | 259,910 | 0 |
| W04 | Lean | 3 | PASS | match | yes | 3 | 97.3 | 28,138 | 327,914 | 0 |
| W04 | Quint | 1 | PASS | match | yes | 4 | 156.6 | 43,767 | 362,999 | 0 |
| W04 | Quint | 2 | PASS | match | yes | 3 | 114.6 | 52,675 | 320,323 | 0 |
| W04 | Quint | 3 | PASS | match | yes | 4 | 145.5 | 37,401 | 450,201 | 0 |
| X01 | Lean | 1 | PASS | match | yes | 2 | 92.5 | 22,306 | 217,634 | 0 |
| X01 | Lean | 2 | PASS | match | yes | 2 | 85.2 | 37,728 | 315,232 | 0 |
| X01 | Lean | 3 | PASS | match | yes | 2 | 90.1 | 26,860 | 245,100 | 0 |
| X01 | Quint | 1 | PASS | match | yes | 2 | 109.2 | 29,167 | 313,967 | 0 |
| X01 | Quint | 2 | PASS | match | yes | 3 | 147.2 | 29,528 | 315,480 | 0 |
| X01 | Quint | 3 | PASS | match | yes | 2 | 108.1 | 21,499 | 201,723 | 0 |

## Next steps

Both tools achieved 12/12 correct repairs. This small pilot establishes no winner or tool-selection decision; effort differences are descriptive. A separately registered follow-up could use harder tasks or remove source-location feedback, with equal inputs and caps and complete execution and billed-cost records.
