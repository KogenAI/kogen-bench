#!/usr/bin/env python3
"""Recompute the descriptive pilot analysis from the public lifecycle ledger."""
import json
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAMES = {'F01': 'Tenant access', 'W01': 'Exact approval',
         'W04': 'Preservation', 'X01': 'Cache identity'}


def distribution(rows, key, digits=0):
    values = [r[key] for r in rows]
    def fmt(v):
        return f'{v:,.{digits}f}' if digits else (f'{v:,.0f}' if v == int(v) else f'{v:,.1f}')
    return f'{fmt(statistics.median(values))} [{fmt(min(values))}–{fmt(max(values))}]'


def generate():
    ledger = [json.loads(line) for line in (ROOT / 'ledger.jsonl').read_text().splitlines()]
    latest = {row['cell_id']: row for row in ledger}
    valid = sorted((r for r in latest.values() if r['status'] == 'completed'),
                   key=lambda r: (r['task'], r['arm'], r['repeat']))
    invalid = [r for r in ledger if r['status'] == 'infra_invalid']
    arms = {a: [r for r in valid if r['arm'] == a] for a in ['lean', 'quint']}
    lines = ['# Lean versus Quint verification pilot: results', '',
             'Both arms reached 12 correct repairs out of 12 valid trials. This is a',
             "ceiling: the protocol's main measure does not separate them. The effort",
             'observations below are secondary and descriptive. There are only three',
             'repeats per task and arm, with 12 trials per arm across four small tasks.',
             'These observations support no broad winner claim.', '',
             'Lean is a proof assistant that checks formal definitions and proofs.',
             'Quint is a specification language with model checking for state transitions.',
             'Both worked from the same Elixir applications, contracts and starter tests.', '',
             '## How and where it ran', '',
             'All valid trials ran on one Hetzner Linux host (2 vCPU) in Europe, with',
             'Codex CLI 0.161.0, requested gpt-6.1-sol and high effort, using the same',
             'account throughout. Each trial used a fresh session. The fixed randomized',
             'schedule specified three repeats for each task and arm. Concurrency was',
             'at most two trials; remaining trials ran sequentially.', '',
             f'Valid trial UTC interval: {min(r["start"] for r in valid)} to {max(r["end"] for r in valid)}.',
             f'Infrastructure-invalid UTC interval: {min(r["start"] for r in invalid)} to {max(r["end"] for r in invalid)}.', '',
             'Equal caps were 900 seconds, 60,000 uncached input plus output tokens,',
             'and ten complete check cycles. A cycle regenerates the representation,',
             'checks the fixed laws and runs starter tests; failed checks consume cycles.',
             'Reported wall time covers the agent trial, not construction or later grading.', '',
             '## Per-task results', '',
             'Each bracket gives the observed minimum–maximum; preceding values are',
             'medians. Diagnosis counts are match / partial / miss, using the fixed',
             'grader rule: both property and function phrases = match, one = partial,',
             'neither = miss. This is a deterministic text score, not a human assessment',
             'of explanation quality. Regression counts are reported final-grade failures',
             'in protected behavior and checks, not a claim about all possible behavior.', '',
             '| Task | Arm | Correct / 3 | Diagnosis M/P/X | Before patch | Cycles median [range] (sum) | Wall seconds median [range] | Capped tokens median [range] | Raw tokens median [range] | Regressions |',
             '| --- | --- | ---: | --- | ---: | --- | --- | --- | --- | ---: |']
    for task, name in NAMES.items():
        for arm, rows in arms.items():
            cell = [r for r in rows if r['task'] == task]
            counts = Counter(r['evaluation']['diagnosis']['score'] for r in cell)
            lines.append(f'| {task}: {name} | {arm.title()} | {sum(r["evaluation"]["passed"] for r in cell)}/3 | '
                         f'{counts["match"]}/{counts["partial"]}/{counts["miss"]} | '
                         f'{sum(r["diagnosis_first"] is True for r in cell)}/3 | '
                         f'{distribution(cell,"cycles")} ({sum(r["cycles"] for r in cell)}) | '
                         f'{distribution(cell,"wall_seconds",1)} | {distribution(cell,"capped_total_tokens")} | '
                         f'{distribution(cell,"raw_total_tokens")} | {sum(len(r["evaluation"]["regressions"]) for r in cell)} |')
    lines += ['', '## Arm summaries and secondary effort differences', '',
              '| Arm | Correct / 12 | Diagnosis M/P/X | Before patch | Cycles median [range] (sum) | Wall seconds median [range] | Capped tokens median [range] | Raw tokens median [range] | Regressions |',
              '| --- | ---: | --- | ---: | --- | --- | --- | --- | ---: |']
    for arm, rows in arms.items():
        counts = Counter(r['evaluation']['diagnosis']['score'] for r in rows)
        lines.append(f'| {arm.title()} | {sum(r["evaluation"]["passed"] for r in rows)}/12 | '
                     f'{counts["match"]}/{counts["partial"]}/{counts["miss"]} | '
                     f'{sum(r["diagnosis_first"] is True for r in rows)}/12 | '
                     f'{distribution(rows,"cycles")} ({sum(r["cycles"] for r in rows)}) | '
                     f'{distribution(rows,"wall_seconds",1)} | {distribution(rows,"capped_total_tokens")} | '
                     f'{distribution(rows,"raw_total_tokens")} | {sum(len(r["evaluation"]["regressions"]) for r in rows)} |')
    lines += ['', 'Both arms had diagnosis before the first patch in 12/12 trials (100%).',
              'Lean had 12 matches; Quint had 11 matches and one partial (W01, repeat 1).',
              'The match-rate difference is 8.3 percentage points, one trial.',
              'No valid trial reached a cap or reported a regression.', '',
              'Descriptive differences below are Quint minus Lean. Ratios are Quint /',
              'Lean; they compare arm medians, not causal treatment effects.', '',
              '| Secondary measure | Median difference | Median ratio |',
              '| --- | ---: | ---: |']
    for key, title, digits in [('cycles', 'Check cycles', 1), ('wall_seconds', 'Wall seconds', 1),
                               ('capped_total_tokens', 'Capped tokens', 1), ('raw_total_tokens', 'Raw tokens', 1)]:
        l = statistics.median(r[key] for r in arms['lean'])
        q = statistics.median(r[key] for r in arms['quint'])
        lines.append(f'| {title} | +{q-l:,.{digits}f} | {q/l:.3f}× |')
    lines += ['', 'Lean used 32 total cycles and Quint 40: eight more cycles for Quint',
              '(25%). Total agent wall time was 1,124.9 seconds for Lean and 1,538.3',
              'seconds for Quint, a difference of 413.4 seconds (36.8%). Backend runtime',
              'is part of the observed effort. Task difficulty, agent choices, cache use,',
              'host sharing and the small sample limit interpretation. No significance',
              'test or general ranking is warranted.', '', '## Total cost per successful repair', '',
              'There is no billed dollar record. Tokens measure usage, not money; cached',
              'input and output have different pricing. No dollar cost is estimated.',
              'For each arm, total cost per successful repair in tokens means the sum of',
              'all valid-trial usage divided by the number of correct repairs. Every valid',
              'trial succeeded here, so this is the arithmetic mean, not the median.',
              'Construction, qualification and smoke usage are outside this trial metric.', '',
              '| Task | Arm | Total capped tokens | Total raw tokens | Capped tokens / correct repair | Raw tokens / correct repair |',
              '| --- | --- | ---: | ---: | ---: | ---: |']
    for task in [*NAMES, 'All tasks']:
        for arm, rows in arms.items():
            cell = rows if task == 'All tasks' else [r for r in rows if r['task'] == task]
            successes = sum(r['evaluation']['passed'] for r in cell)
            capped = sum(r['capped_total_tokens'] for r in cell)
            raw = sum(r['raw_total_tokens'] for r in cell)
            lines.append(f'| {task} | {arm.title()} | {capped:,} | {raw:,} | {capped/successes:,.1f} | {raw/successes:,.1f} |')
    lines += ['', 'Capped tokens = input − cached input + output. Raw tokens = input +',
              'output. Reasoning is already included in output and is not added again.',
              'Cache-write input is retained when reported and is already part of input.',
              'The token cap is observed only when an atomic request usage report arrives;',
              'overshoot is retained rather than truncated. These trials had no overshoot.', '',
              'Infrastructure failures consumed additional usage. Counting those attempts',
              'as operational overhead gives the following totals per successful repair;',
              'they remain excluded from the 12-trial success and effort distributions.', '',
              '| Arm | Invalid attempts | Additional capped / raw tokens | Inclusive capped tokens / success | Inclusive raw tokens / success |',
              '| --- | ---: | ---: | ---: | ---: |']
    for arm, rows in arms.items():
        bad = [r for r in invalid if r['arm'] == arm]
        c = sum(r['capped_total_tokens'] for r in bad)
        t = sum(r['raw_total_tokens'] for r in bad)
        lines.append(f'| {arm.title()} | {len(bad)} | {c:,} / {t:,} | '
                     f'{(sum(r["capped_total_tokens"] for r in rows)+c)/12:,.1f} | '
                     f'{(sum(r["raw_total_tokens"] for r in rows)+t)/12:,.1f} |')
    lines += ['', '## Deviations, amendments and infrastructure history', '',
              '1. Before scored trials, the token cap was interpreted as uncached input',
              '   plus output, excluding cached input. Raw usage remains reported.',
              '2. Before scored trials, both packages removed precomputed checker output.',
              '   Authored bridge replay was restricted to identical source locations only.',
              '   Native backend diagnostics were retained. Checking was mediated by a',
              '   broker, project setup was frozen, and API/completion checks were hardened.',
              '3. The operator waived a second model’s review of the fixes to save time. The supervisor inspected the changes instead, and the full qualification checks were repeated.',
              '4. The four excluded attempts were repeat 2 of tenant access and exact approval, each with Lean and Quint. The command executor was missing from the agent’s execution environment. Correction rows retain the original usage and mark those attempts as infrastructure failures; their artifacts remain archived privately. Replacement attempts used the same scheduled combinations. Valid completed trials were retained. Before restarting, an operational test had to demonstrate command execution, documentation access, a counted check and prevention of bypassing the counted checker. Caps and grading were unchanged. The operational test also',
              '   exposed local socket restrictions and broker-control-file inspection;',
              '   local file transport and cleanup corrected these before scored restart.',
              '5. During the run, the operator moved the second half of the planned',
              '   two-host split to Europe. All 24 valid trials ran on one Hetzner Linux host in Europe, with two virtual CPUs and at most two simultaneous trials, instead of the planned 12 trials in Europe and 12 in the United States. The same harness, readiness approval, Codex binary and account were used for all 24. Schedule rows 13–24 moved to that host and its existing account configuration; the earlier allocation was retained. The United States host ran no trials. Task order, packages, model, effort, caps, checking, isolation and grading were unchanged.',
              '6. After initial admission, harness launch parameters were changed to specify the account configuration directory, expected account and host-specific readiness approval. Launch used Europe’s approval; overall approval remained false because the second host was pending. Recorded harness versions in the schedule were updated without changing trial order, and deployed files were reconciled before launch.',
              '7. Two power losses on the operator’s local workstation had no effect on trials because they ran on the',
              '   European Linux host. Exact power-loss times were not retained here.',
              '8. Two interrupted qualification evaluation attempts were repeated',
              '   sequentially with unchanged sources after an output-redirection fault.',
              '   No completed application failure was rerun to obtain a passing answer.',
              '9. Standard capture is incomplete: no billed cost, phase-level usage,',
              '   host boundary telemetry or provider-effective receipt is supplied.',
              '   The package declares these gaps and remains DESCRIPTIVE.', '',
              'The protocol and amendments are preserved as sanitized publication copies.',
              'The sanitized ledger retains all 59 lifecycle rows, including running',
              'entries, superseded infrastructure completions and four correction rows.',
              'Analysis takes each cell’s latest status, then excludes infra-invalid',
              'attempts; their usage is shown separately. Final grades and diagnosis scores',
              'are source-reported receipts. The private final evaluator is not published,',
              'so this bundle recomputes the analysis but cannot repeat final grading.', '',
              '## Individual valid trials', '',
              '| Task | Arm | Repeat | Correct | Diagnosis | Before patch | Cycles | Wall s | Capped tokens | Raw tokens | Regressions |',
              '| --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |']
    for r in valid:
        e = r['evaluation']
        lines.append(f'| {r["task"]} | {r["arm"].title()} | {r["repeat"]} | '
                     f'{"PASS" if e["passed"] else "FAIL"} | {e["diagnosis"]["score"]} | '
                     f'{"yes" if r["diagnosis_first"] else "no"} | {r["cycles"]} | '
                     f'{r["wall_seconds"]:.1f} | {r["capped_total_tokens"]:,} | '
                     f'{r["raw_total_tokens"]:,} | {len(e["regressions"])} |')
    lines += ['', '## Next steps', '',
              'Both tools achieved 12/12 correct repairs. This small pilot establishes no winner or tool-selection decision; effort differences are descriptive. A separately registered follow-up could use harder tasks or remove source-location feedback, with equal inputs and caps and complete execution and billed-cost records.', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    (ROOT / 'RESULTS.md').write_text(generate())
    print('Recomputed RESULTS.md from the public lifecycle ledger.')
