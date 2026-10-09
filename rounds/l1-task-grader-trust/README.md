# L1 — Task and grader trust

Round date: HISTORICAL (before 2026-10-09)
Publication badge: VALID; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**VALID**

### Why not VALID
- None: the README documents a pre-result registration, execution under its rule, reconciled denominators, recomputable results, matched conditions, and retained evidence.


STATUS: **VALID**

## Required reproduction metadata

- Kogen commit: not applicable as a single round-level value; the eight task variant commits are listed below.
- Harness commit: not recorded as a Git commit; available wrapper fingerprints are SHA-256 values, not Git commits.
- Model and effort: selected pool configuration is Codex `gpt-6-luna` at max; no scored model cell was launched.
- Task IDs: see the exact task variant IDs and task commits below.
- Official replacement grading: operator grade windows are recorded in the L1 source ledger; exact control commands are listed below.
- Raw records: `grades.jsonl`, `windows.jsonl`, `POOLS.json`, the prep snapshot in `CONTROL-MANIFEST.md`, and the sanitized `data/controls.csv` receipt.

Pre-registered: yes; design dated 7 October 2026, before any scored cell.
Label: VALID model-free grader-control audit; no scored model cells were launched.
Question: Do the official task/grader controls reject prompt-violating reference mutants and accept an allowed alternative implementation across selected r70 variants?
n: 8 original task variants; 24 original staged / 21 graded / 3 withdrawn; 2 replacement mutants graded; 7 admitted variants / 21 original graded controls. The original 37-row ledger has 34 graded control rows and 3 withdrawal audit rows, including 11 admission grades. The separate L1-EU cohort adds 10 grades; the combined CSV has 47 rows.
Headline: 14 behavioral mutant detections across the 7 admitted variants (two per variant) + 7 passing alternatives.
Configuration: Pool selection uses Codex gpt-6-luna at max, default. Control authoring is model-free; Rust and Elixir variants use kogen-bench-eu, and Go and TypeScript/Bun variants use kogen-bench-us. Control manifests identify these as NOT a model cell.
Limit: The original 24 controls retain their recorded disposition: 21 officially graded and 3 withdrawn. Original r711/r714 remain labelled as build rejections; replacements r720/r719 are officially graded behavioral failures and supersede those build rejections for the two-mutant criterion. The controls support only these seeded examples and do not establish general grader fairness or build success. No scored model cells were launched.

## Reproduction

Kogen task commits:

| Task ID | Kogen commit |
| --- | --- |
| r70-2-elixir | [470ba65c1d3c19191a2190a032cd9ebf24e71975](https://github.com/KogenAI/kogen-ex/commit/470ba65c1d3c19191a2190a032cd9ebf24e71975) |
| r70-2-go | [13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82](https://github.com/KogenAI/kogen-ex/commit/13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82) |
| r70-4-rust | [4211fe638592cc4266d25e630417c6920a544188](https://github.com/KogenAI/kogen-ex/commit/4211fe638592cc4266d25e630417c6920a544188) |
| r70-4-elixir-fe2 | [5ccd0bf1e816e2b2f5b2694861f8596402409f52](https://github.com/KogenAI/kogen-ex/commit/5ccd0bf1e816e2b2f5b2694861f8596402409f52) |
| r70-4-go-fe2 | [21d21a2f420a387c921f998e5b4d16efc8f80904](https://github.com/KogenAI/kogen-ex/commit/21d21a2f420a387c921f998e5b4d16efc8f80904) (public control base; reference source [748ebe3a3bc03a112dab83e785159654e0709f9e](https://github.com/KogenAI/kogen-ex/commit/748ebe3a3bc03a112dab83e785159654e0709f9)) |
| r70-4-ts-bun-fe2 | [cc3a831a167020538c4ca2ad90185606a2e4ad6a](https://github.com/KogenAI/kogen-ex/commit/cc3a831a167020538c4ca2ad90185606a2e4ad6a) |
| r70-5-go | [e0b4a2478a17a924fcecb965b2941ca3396f49d6](https://github.com/KogenAI/kogen-ex/commit/e0b4a2478a17a924fcecb965b2941ca3396f49d6) |
| r70-7-rust | [111a0c776ae6d93f6e7fccd3fc694d5f4fa26838](https://github.com/KogenAI/kogen-ex/commit/111a0c776ae6d93f6e7fccd3fc694d5f4fa26838) |

Harness and CLI: contestant ledger rows record Codex CLI 0.160.0. The bench-codex wrapper SHA-256 is 08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300. An official harness version label is not recorded; the selected baseline rows record grader SHA-256 616b1d53fe6ee56376134f0cf6a9350e94b5ecb7ec5b84f46a93e3c677356416, with 5fe9ea3fa0cb748e3a60d4e9153e41c61ec735bd3b5d6590dc7708e7343ae91f on the selected r70-4-rust row. The lane controller and inventory helper fingerprints are recorded below.

Data files: grades.jsonl (SHA-256 39bdd350fe6fca7c5c941b415f3ef91f6b6c9d444c40d96d1426018f3702d69a); windows.jsonl (SHA-256 7de4ad159d388c4b084f8c6a3c8599f71b3dde22c60aa39865fdba4e06163428); POOLS.json (SHA-256 662a097ede933ba115464f238f060de0be5ad46134b9631d6bdef2a848cae020); controls.csv (SHA-256 1d799c14750878dbce58dee45b979e3de0cb4e1beb03606c0fd9279bab8e3482); reproduction checker reproduce/l1_controls.py. The selection uses the latest grade row per exact cell ID, removes invalidated IDs, excludes contestant x-controls from Luna-max rates, and excludes task 8.

Public control-ledger reproduction command: `python3 reproduce/l1_controls.py`. It reads only `data/controls.csv` and verifies the public control-count claims and the staged/replacement IDs against CONTROL-MANIFEST.md.

Run these commands from the lane workspace root. They are recorded operator commands; this page-update job did not run any grades:

    python3 levers/lanes-2026-10-07/l1/grade_window.py kogen-bench-us --admission-controls --controls-only --pairs 2:go,5:go
    python3 levers/lanes-2026-10-07/l1/grade_window.py kogen-bench-us --admission-controls --controls-only --fixed-variants r70-4-go-fe2
    python3 levers/lanes-2026-10-07/l1/grade_window.py kogen-bench-eu --cell-ids codex__gpt-6-luna__max__default__r70-2-elixir__r701,codex__gpt-6-luna__max__default__r70-2-elixir__r702,codex__gpt-6-luna__max__default__r70-2-elixir__r703,codex__gpt-6-luna__max__default__r70-4-rust__r707,codex__gpt-6-luna__max__default__r70-4-rust__r708,codex__gpt-6-luna__max__default__r70-4-rust__r709,codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r710,codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r711,codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r712,codex__gpt-6-luna__max__default__r70-7-rust__r722,codex__gpt-6-luna__max__default__r70-7-rust__r723,codex__gpt-6-luna__max__default__r70-7-rust__r724
    python3 levers/lanes-2026-10-07/l1/grade_window.py kogen-bench-us --cell-ids codex__gpt-6-luna__max__default__r70-2-go__r704,codex__gpt-6-luna__max__default__r70-2-go__r705,codex__gpt-6-luna__max__default__r70-2-go__r706,codex__gpt-6-luna__max__default__r70-4-go-fe2__r713,codex__gpt-6-luna__max__default__r70-4-go-fe2__r714,codex__gpt-6-luna__max__default__r70-4-go-fe2__r715,codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r716,codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r717,codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r718,codex__gpt-6-luna__max__default__r70-5-go__r719,codex__gpt-6-luna__max__default__r70-5-go__r720,codex__gpt-6-luna__max__default__r70-5-go__r721

The lane-local grade_window.py SHA-256 is ad286b1059b23967c9bd034108acf9e2095699665e3606aeaa10418f5e558930; inventory_l1.py SHA-256 is 689babb23b3d8d467cb9915f2600e2ebdff7b3049144dd9083d2209173553618.

Sources: [decision rule](DECISION-RULE.md); [results](RESULTS.md); [control manifest prep snapshot](CONTROL-MANIFEST.md); [exact sanitized control ledger](data/controls.csv); [pool-selection context](POOL-SELECTION.md); pool and staging records are POOLS.json and the lane staging records.

## Replacement-mutant amendment — 7 October 2026

Status: **VALID**. The original 35 ledger rows are unchanged: 21 of 24 original staged controls were graded and 3 were withdrawn. Replacements r719/r720 have official grades; both failed behaviorally with 16/18 tests passing and make_check true. They complete two behavioral mutants for each of the seven admitted variants. Original r711/r714 remain labelled as build rejections and are superseded by r720/r719, respectively, for the two-mutant criterion.

Behavior class for both replacements: **rebase-success outcome misclassification**. The public mutant amendment records each patch SHA-256 and behavior class; it does not publish patch contents or hidden/reference material.

| Host | Task | Cell ID | Patch SHA-256 | Behavior class | Official grade | Grade window |
| --- | --- | --- | --- | --- | --- | --- |
| kogen-bench-us | r70-4-go-fe2 | codex__gpt-6-luna__max__default__r70-4-go-fe2__r719 | `71ad31d37bdf1745dbf6a39efa8c1dbf6ab138f7432ef4c017c03c51a25fd1fc` | rebase-success outcome misclassification | fail, 16/18; make_check true | 2026-10-07T14:55:34Z |
| kogen-bench-eu | r70-4-elixir-fe2 | codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r720 | `f95c4624becd7edd205d1b62b801dd7ac1207255bcd7afd0c012b98e19321fc7` | rebase-success outcome misclassification | fail, 16/18; make_check true | 2026-10-07T16:40:48Z |

The official grades were recorded in the operator windows on the assigned hosts. Exact task commits, harness/CLI versions, commands, and public data files are recorded in the reproduction block above. No scored model cells were launched.


## Addendum: L1-EU (7 Oct 2026)

STATUS: **VALID**. This model-free extension records 10 official grades: four task-6 admission controls and six mutant/alternative X-controls across two EU Elixir task variants. It changes no part of the original seven-variant headline above. No scored model cells were launched.

Pre-registered: yes; the L1-EU selection and control design were recorded on 7 October before these control grades. See the sanitized [dated registration receipt](reproduce/L1-EU-REGISTRATION.md), which records the source hashes and pre-grade chronology.
Label: VALID control audit; `r70-6-elixir` is **NOT ADMITTED** and `r70-7-elixir` is **ADMITTED**.
Question: Do the official controls establish admission and detect the seeded prompt violations for the two selected EU Elixir variants?
n: 2 task variants; 4 task-6 admission grades; 6 X-control grades; 10 appended rows in `data/controls.csv`.
Headline: Task 6 reference/no-op admission passed, but both prompt-length mutants passed, so task 6 is not admitted. Task 7's two mutants failed and its alternative passed, so task 7 is admitted.
Configuration: Elixir on kogen-bench-eu. The task-6 baseline was 3/6; the task-7 baseline was 5/6. Task 7 already had two reference PASS and two no-op FAIL admission controls in the R70 ledger.
Limit: These seeded controls support only the reported behavior classes. The task-6 suite did not detect the two prompt-length violations. The planned `l4b-confirm-eu` is **NOT-RUN** for insufficient power: only one variant was admitted, its baseline was 5/6, and no cells were spent.

Task 6 admission controls: references r1/r2 passed 24/24; no-ops r1/r2 failed 0/24. X-control outcomes and public patch metadata:

| Task | Kind | Cell ID | Patch SHA-256 | Behavior class | Official grade | Grade window |
| --- | --- | --- | --- | --- | --- | --- |
| r70-6-elixir | mutant | codex__gpt-6-luna__max__default__r70-6-elixir__r730 | `a7098c0191e08eedc35e062bd7122c9e3c0b157856e7590cd6c9dc301ecf4981` | Event IDs longer than the specified limit are accepted. | pass, 24/24 | 2026-10-07T20:42:58Z |
| r70-6-elixir | mutant | codex__gpt-6-luna__max__default__r70-6-elixir__r731 | `f0aadd52c1dc42f068476927d2201912fa7aaa2f260ef917f81f92848313e218` | Job slugs longer than the specified limit are accepted. | pass, 24/24 | 2026-10-07T20:44:13Z |
| r70-6-elixir | alternative | codex__gpt-6-luna__max__default__r70-6-elixir__r732 | `cba3ae7bca030c3741416ba022b2a20dac88a607ec576d7c2f3d4c11c687a4e3` | Behavior-equivalent alternative implementation. | pass, 24/24 | 2026-10-07T20:45:28Z |
| r70-7-elixir | mutant | codex__gpt-6-luna__max__default__r70-7-elixir__r733 | `b0f3e4fd6d189c556a521a5e730dc77d95e3c8c8234af6c1efa652caa127c818` | Scale parsing accepts values above the specified ceiling. | fail, 23/24 | 2026-10-07T20:46:43Z |
| r70-7-elixir | mutant | codex__gpt-6-luna__max__default__r70-7-elixir__r734 | `a72692f3eb6686acd0ce1b87bba70d894de6f6b9fe024e320f5bd59ea08f021b` | Status IDs may begin with uppercase letters. | fail, 23/24 | 2026-10-07T20:48:11Z |
| r70-7-elixir | alternative | codex__gpt-6-luna__max__default__r70-7-elixir__r735 | `0cc7c063795b669918bb4579231c6ae7421609166a81dcf3bec926f91aacc40d` | Behavior-equivalent alternative implementation. | pass, 24/24 | 2026-10-07T20:49:39Z |

Only each staged patch's SHA-256 and behavior class are published; patch contents are omitted.
All six staged patches passed `git apply --check`, public setup/build, and public `make check` in a temporary task copy before grading; author verification did not run hidden tests.

### L1-EU reproduction

Kogen task commits: [`r70-6-elixir`](https://github.com/KogenAI/kogen-ex/commit/133e688d87f0392a00c164d34455cde04def28ad); [`r70-7-elixir`](https://github.com/KogenAI/kogen-ex/commit/c1899948806e61033520431b9e4d8749c72074d1).
Harness/CLI and toolchain: `bench-codex` wrapper SHA-256 `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`; `codex-cli 0.160.0`; Elixir `1.20.2`; Erlang/OTP `29.0.3`; official L1-EU grades use grader SHA-256 `0e6f8aa06dce3b42813e326a85c2248115bf95bc127449f8fb99e3929bec0843`.
Task IDs: `r70-6-elixir`, `r70-7-elixir`.

Recorded public patch checks in a temporary task copy: `git apply --check patch.diff`; `./setup.sh && make build && make check`.

Recorded official commands:

```sh
python3 levers/lanes-2026-10-07/l1/grade_window.py kogen-bench-eu --admission-controls --controls-only --pairs 6:elixir
python3 levers/lanes-2026-10-07/l1/grade_window.py kogen-bench-eu --cell-ids codex__gpt-6-luna__max__default__r70-6-elixir__r730,codex__gpt-6-luna__max__default__r70-6-elixir__r731,codex__gpt-6-luna__max__default__r70-6-elixir__r732,codex__gpt-6-luna__max__default__r70-7-elixir__r733,codex__gpt-6-luna__max__default__r70-7-elixir__r734,codex__gpt-6-luna__max__default__r70-7-elixir__r735
python3 reproduce/l1_controls.py
```

L1-EU source data files: `levers/lanes-2026-10-07/l1/grades.jsonl`, `levers/lanes-2026-10-07/l1-eu/SELECTION.md`, and `levers/lanes-2026-10-07/l1-eu/STAGED.md`. The public receipt is `data/controls.csv`; it records cohort, kind, official outcome, aggregate tests, cause class, task commit, grader fingerprint, grade-window timestamp, and only the patch SHA-256 and behavior class for X-controls.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/l1-task-grader-trust.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 15 rows (fail 9, pass 6); overall pass rate is 40.0% (6/15) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 15 missing published metadata). Missing counters remain unknown, not zero.
This round also has 15 raw-only or non-public rows; they are kept separate from the published-export denominator.
