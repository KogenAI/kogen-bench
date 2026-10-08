# kogen-bench

Benchmarks for [Kogen](https://github.com/KogenAI), a coding-agent harness. The repository records comparisons with Codex and Grok Build, model and effort settings, harness designs, implementation languages, correctness, and reported usage costs. See the [public glossary](rounds/GLOSSARY.md) for arm, model, and analysis terms.

> **Open source, closed contribution.** Source code is available under the Apache License 2.0. This repository does not accept issues or pull requests and is not a public support channel. You may study and adapt it under the license.

## Start here

- [FINDINGS.md](FINDINGS.md) is the family-by-family summary of what the public evidence does and does not establish.
- [Hypothesis register](hypotheses/README.md) lists H01–H153 and links each proposition to its family page.
- [Round register](rounds/README.md) lists experiment pages and their status; each round page is the authority for that run's history and limits.
- [Publication validation](results/publication-validation.md) records the final validator output, current blockers, and bounded claims safe to publish.
- [Public glossary](rounds/GLOSSARY.md) defines arm, model, and analysis terms.
- [Verification guide](reproduce/VERIFY.md) gives the commands and limits for recomputing published records and numbers.
- [Rerun guide](reproduce/RERUN.md) explains task grading and the current state of the execution kit.
- [Round status](rounds/STATUS.md) summarizes current round states.
- [Credits](CREDITS.md) records acknowledgements.

### Find an experiment

Start with the topic in [FINDINGS.md](FINDINGS.md), then follow its H IDs to the linked [family page](hypotheses/README.md). The family page points to relevant round receipts. To look up a known round or study ID directly, use the [round register](rounds/README.md) or the machine-readable [round index](rounds/index.json). Task definitions are in [tasks/](tasks/README.md); official outcomes and captured deliveries are indexed separately in [results/](results/README.md).

### For agents and maintainers

Use the hypothesis register for family ownership and evidence status, the family page for hypothesis-level synthesis, and each round page for run history. [cells.jsonl](results/cells.jsonl) contains official outcome rows; the [run-record index](results/run-records/index.json) lists one captured-delivery JSONL per round, including deliveries without an official grade, plus an `unassigned.jsonl` partition for records without an unambiguous round tag. Other large evidence families are also indexed per round. Schema 1.2 uses compact missing-reason codes listed in the [legend](results/missing-reasons.json). These exports answer different questions and must not be treated as interchangeable. Study design, execution, grading, and interpretation are documented in [METHOD.md](METHOD.md); required cell fields and their [schema](schema/run-record.schema.json) are in [STANDARD.md](STANDARD.md).

### Reproduce

From the repository root, use the standard-library-only scripts in [reproduce/README.md](reproduce/README.md). The primary commands are:

```sh
python3 reproduce/export_results.py
python3 reproduce/build_records.py
python3 reproduce/build_grade_join.py
python3 reproduce/validate_repo.py
```

The historical audit command can rewrite round audit documents and the validation summary; read the reproduction notes before running it.

## Repository map

- [METHOD.md](METHOD.md): study design, execution, grading, and interpretation
- [STANDARD.md](STANDARD.md): required cell records and the [schema](schema/run-record.schema.json)
- [Vendored Kogen specification](spec/README.md): pinned to v1.2 at commit `1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0`. Upstream v1.3-draft exists, but it is not the version cited in EVIDENCE-MAP.md.
- [rounds/](rounds/README.md): round records, outcomes, and status labels
- [decisions/](decisions/README.md): analysis rulings
- [categories/](categories/README.md): results grouped by topic
- [tasks/](tasks/README.md): task records and public-prompt coverage
- [results/](results/README.md): official outcome export and separately captured standard records

For scored studies, VALID, CONFOUNDED, INVALID, and INTERIM describe outcome validity. WITHDRAWN and NOT-RUN describe lifecycle; PRE-REGISTERED identifies a design with no scored cells. DESCRIPTIVE, EXPLORATORY, and CONFIRMATORY describe the analysis. Round pages identify whether the design was registered before execution; historical records may be retrospective. Early rounds are exploratory, some samples are small, and task mixes and venues differ.

Results are counted on task hidden suites; stack lint and typecheck results are separate diagnostics. Task grading materials ship under `tasks/<id>/hidden/` and `tasks/<id>/grader/` and remain outside the agent-visible workspace during a run ([PRIVATE.md](PRIVATE.md), [rerun guide](reproduce/RERUN.md)).

## Local setup

For record verification, requirements are Python 3 (standard library only); no model access, credentials, or benchmark hosts are needed. Rerunning tasks has additional Linux, Bubblewrap, and operator-owned Codex access requirements described in [RERUN.md](reproduce/RERUN.md).

```sh
git clone https://github.com/KogenAI/kogen-bench.git
cd kogen-bench
python3 reproduce/export_results.py
python3 reproduce/build_records.py
python3 reproduce/build_grade_join.py
```

`export_results.py` rebuilds `cells.csv`, `cells.jsonl`, `unmapped.json`, and `export-report.json`. `build_records.py` rebuilds the indexed per-round Standard records from committed indexed evidence. The historical audit command also rewrites round audit documents and the [validation summary](results/validation-summary.md); see [reproduction notes](reproduce/README.md) before using it.

## Website

The research website is built from [site/](site/README.md) for https://bench.kogen.dev. See its README for build inputs, private preview mode, and deployment settings. The source records above remain the evidence authority.

## Checks

```sh
python3 reproduce/validate_repo.py
```

The validator checks round and task indexes, result exports, required record fields, privacy rules, and authored relative links. It excludes archival source excerpts under `sources/` except for the source index. It does not inspect remote configuration. See [VERIFY.md](reproduce/VERIFY.md) for the full recomputation commands and limits.

## License and product identity

The source is licensed under the [Apache License 2.0](LICENSE). Product identity is described in [BRANDING.md](BRANDING.md).

### Publication rules

Upstream code is unmodified; its contents are the upstream authors'. Source files identified as upstream copies remain as published, including their hostnames, deployment paths, public addresses, and test-fixture values such as DNS test IPs. This applies to 37signals LLC's Fizzy, Fizzy SaaS, and Writebook, and to Agents on Rails, commissioned by the Rails Foundation and built by Evil Martians. Their attributions and licence terms are listed in [CREDITS.md](CREDITS.md), [NOTICE](NOTICE), and [LICENSES/](LICENSES/).

Publication edits to Kogen-produced artifacts are recorded in [PUBLICATION-MANIFEST.json](PUBLICATION-MANIFEST.json), with separate as-run and published hashes and the reason for each change. See [SECURITY-NOTES.md](SECURITY-NOTES.md) for the retained public commit identity and the upstream-content exception.

Forks and public deployments must use their own name, logo, visual identity, domain, content, credentials, and data. Kogen brand assets are not licensed under Apache-2.0. You may refer to Kogen only as reasonably necessary to describe the origin of the software.
