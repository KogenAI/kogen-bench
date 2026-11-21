# Add the h23 round strict records and declarations

Slug: h23-round-strict-records
Model: not applicable — the change adds four static record and declaration files to one round directory; there is no state or interacting rule to model
Acceptance:
- .kogen/intents/h23-round-strict-records/acceptance.feature
- features/steps/h23-round-strict-records__steps.js

The round directory `rounds/h23-release-bbf56fdc-vs-891c91b3` holds `README.md` and `cells.json` but no Standard 1.2 records. Its executions are dated 16 November 2026, after the 9 October strict date, so it needs the same record files as `rounds/claude-code-fix-rechecks-1`. Add exactly four files to the round directory and change no other path: `records.jsonl`, `MEASURED.md`, `MISSING.md` and `MISSING-DECLARED.json`. This is part 1 of 2; part 2 adds the README metadata and the status row, so no status row exists yet and the release validator does not check the round as strict yet.

`records.jsonl` has one Standard 1.2 record per new attempt in `cells.json` (the fifteen slots with `reused` false), one JSON object per line, each carrying the slot's `arm`, `task.id` and rep from `cells.json`. The three reused baseline slots (`reused` true) get no record, as in `reproduce/build_scored_round_records.py`, where reused cells already represented elsewhere are left out of the round's records and the omission is stated in the protocol deviations of `MISSING.md`. Every field `cells.json` cannot supply is declared missing with a registered reason code from `results/missing-reasons.json`; no value is invented. Produce the files with the existing tooling under `reproduce/` (`missing_reasons.py`, `validate_round.py` and the record and declaration shape of `build_scored_round_records.py` and the rechecks round); a throwaway script used for this is not committed.

Change no validator, test, policy, README, `cells.json`, `rounds/README.md`, `rounds/index.json` or file under `.kogen/`. The four files hold no home path, host name, IP address, e-mail address, credential, raw transcript or account meter.

## Decisions
- Each record carries its slot's rep in a way the acceptance finds at run time: either a `rep` field, or a standalone token in `cell_id` (`<n>`, `r<n>` or `rep<n>` between non-alphanumeric separators); the Standard record has no dedicated rep field and the rechecks round carries the rep inside `cell_id`. (constraint: arm equals the slot arm and task.id equals the slot task; each of the fifteen new slots is matched by exactly one record) (evidence: rounds/claude-code-fix-rechecks-1/records.jsonl; rounds/h23-release-bbf56fdc-vs-891c91b3/cells.json) (assumption: the exact cell_id spelling is the Build's choice; the acceptance accepts a rep field or a delimited rep token) (source: request)
- The three reused baseline slots get no record; records.jsonl has exactly fifteen lines, and MISSING.md states the omission under its protocol deviations. (constraint: records.jsonl has one line per new attempt and no line for a reused slot) (evidence: reproduce/build_scored_round_records.py; rounds/h23-release-bbf56fdc-vs-891c91b3/cells.json) (source: request)
- MISSING-DECLARED.json follows the rechecks round shape: a `fields` object keyed by Standard field path, each with a registered `reason_code`, a nonblank `note` and counts, and its field set equals the set of fields the records leave missing under the strict validation in validate_round.py. (constraint: every reason_code exists in results/missing-reasons.json; no value is invented) (evidence: rounds/claude-code-fix-rechecks-1/MISSING-DECLARED.json; reproduce/validate_round.py; reproduce/validate_release.py; results/missing-reasons.json) (source: request)
- The acceptance reads only the working tree: it lists the round directory, parses the four files, and runs validate_round.validate on the round's own records.jsonl; it uses no git history, base revision, diff, status or listing of every tracked path. (decision: D4, round 1) (constraint: the round directory holds exactly README.md, cells.json and the four added files, no other file or subdirectory) (evidence: reproduce/validate_round.py; rounds/h23-release-bbf56fdc-vs-891c91b3/cells.json) (source: request)
- The existing suites are protected by the configured validate-repo check, not re-run by acceptance. (decision: D5, round 1) (evidence: .kogen/project.yaml) (assumption: running python3 reproduce/validate_repo.py after the four files land was not run in this shaping, so it is not confirmed that the validator accepts the new files before part 2) (source: request)
- controls.json is deferred because a correct implementation is four generated files of well over 65536 bytes (fifteen full Standard records). (decision: D6, round 1) (evidence: rounds/claude-code-fix-rechecks-1/records.jsonl) (source: request)
- cell_id encodes the rep as <round>-<task>-r<rep>-<arm>; records.jsonl has fifteen lines and none for the three reused baseline slots (decision: D1, round 1) (evidence: rounds/claude-code-fix-rechecks-1/records.jsonl; reproduce/build_scored_round_records.py; rounds/h23-release-bbf56fdc-vs-891c91b3/cells.json) (assumption: The cell_id format is the shaper's reading of the rechecks precedent; no validator mandates it.) (source: request)
- Acceptance reads the working tree only and runs validate_round.validate strictly on the round's own records.jsonl (decision: D2, round 1) (evidence: reproduce/validate_round.py; reproduce/validate_release.py) (assumption: Ran validate_round.validate on the rechecks round in a read-only probe (zero errors, field sets equal); not run on the h23 files, which do not exist yet.) (source: request)
- controls.json deferred (decision: D3, round 1) (assumption: No wrong-implementation controls were run; the step regexes were only checked against the rechecks-1 files as known-good.) (source: request)

## Source comparison
- Four new files in the h23 round directory and nothing else: addressed by the directory-contents scenario and the records scenario.
- Fifteen records, arm, task and rep from cells.json: addressed by the records scenario (rep found at run time, see D1).
- Three reused baseline slots follow the build-script precedent: addressed as omission with a stated deviation (D2); the records scenario fails if the line count is not fifteen or a slot is unmatched.
- Registered reason codes only, no invented value: addressed by the declaration scenario against results/missing-reasons.json and the strict validation of the records.
- No home path, host name, IP address, e-mail address, credential, raw transcript or account meter: addressed by the privacy scenario.
- No change to validators, tests, policy, README, cells.json, rounds/README.md, rounds/index.json or .kogen/: a constraint on the Build, observed only through the round directory contents.
- Part 2 (README metadata, status row): out of scope, not touched.

## Tests
- records.jsonl has one Standard 1.2 line per new attempt, none for reused slots: the records scenario in acceptance.feature (scenario)
- every declared missing field uses a registered reason code and matches the records: the declaration scenario (scenario)
- the four files hold no private text: the privacy scenario (scenario)
- the round directory holds exactly six entries, read from the working tree only: the directory scenario (scenario)
- existing repository checks keep passing: python3 reproduce/validate_repo.py as the configured check (existing)

## Feasibility
- none
