# Add the retained cells.json to the h23 round

Slug: h23-round-cells-json-data
Model: not applicable — the change adds one static data file and edits one list in a static JSON index, so there is no state to model
Acceptance:
- .kogen/intents/h23-round-cells-json-data/acceptance.feature
- features/steps/h23-round-cells-json-data__steps.js

The h23 DESCRIPTIVE round (original verdict rejected, no adoption, full rerun unavailable) is already registered with its page, index entry, inventory entry and register line, but the inventory entry lists only the page. This change adds the retained raw data file that the page names and completes the inventory entry.

Scope: create exactly one file, `rounds/h23-release-bbf56fdc-vs-891c91b3/cells.json`, containing the SOURCE FILE bytes (immutable input data; the copy retained in the Intent directory as `fixtures/source-cells.json` is the reference; a final newline is optional). Change exactly one existing file, `reproduce/round-inventory.json`: in the last entry, round_id `h23-release-bbf56fdc-vs-891c91b3`, the `inputs` list becomes exactly `rounds/h23-release-bbf56fdc-vs-891c91b3/cells.json` then `rounds/h23-release-bbf56fdc-vs-891c91b3/README.md`; every other field and entry stays as is. Nothing else changes: not `rounds/index.json`, not `rounds/README.md`, not the round page, no validator, no doc, no `recompute.py`. Nothing is replaced or removed.

The data file parses as JSON with 18 unique (arm, task, rep) slots, 12 with numeric score and total, 6 with null for both, and `candidate_adopted` null. The only paths in the round directory are README.md, cells.json and, if later rows landed, manifest.json and recompute.py. Existing tests and the validator keep passing. The checks read only the working tree, are model-free and fast, run neither tests nor the validator, and hold no private path or host.

## Decisions
- Create exactly one file, rounds/h23-release-bbf56fdc-vs-891c91b3/cells.json, holding the SOURCE FILE bytes (final newline optional), and change exactly one existing file, reproduce/round-inventory.json, whose last entry (round_id h23-release-bbf56fdc-vs-891c91b3) gets inputs rounds/h23-release-bbf56fdc-vs-891c91b3/cells.json then rounds/h23-release-bbf56fdc-vs-891c91b3/README.md; every other field and entry stays unchanged (decision: D1, round 1) (constraint: No change to rounds/index.json, rounds/README.md, the round page, any validator, any doc or recompute.py) (constraint: Every other tracked file under results and rounds stays untouched) (evidence: reproduce/round-inventory.json; rounds/h23-release-bbf56fdc-vs-891c91b3/README.md) (assumption: The inventory file ran as a read-only JSON parse in this session; the validator was not run.) (source: request)
- The acceptance holds the source data as a fixture in the Intent directory (fixtures/source-cells.json) and the earlier inventory entries as a count plus a hash of their key-sorted serialization with the unchanged last entry (fixtures/expected.json); checks read only the working tree and run neither tests nor the validator (decision: D2, round 1) (evidence: features/steps/h23-round-page-and-register-index__steps.js; reproduce/round-inventory.json) (assumption: The hash was computed from the unchanged inventory in this session's read-only copy; it was not rechecked by Kogen.) (source: request)
- The round directory may hold only README.md, cells.json and, if later rows landed, manifest.json and recompute.py; any other file or subdirectory fails the check (decision: D3, round 1) (constraint: The earlier h23 page Intent's check already allows README.md plus cells.json, so it keeps passing) (evidence: rounds/h23-release-bbf56fdc-vs-891c91b3/README.md) (source: request)

## Source comparison
- Request scope (one new file cells.json with the SOURCE FILE bytes; one inventory entry's inputs list): addressed by both scenarios of acceptance.feature and by the fixtures in this Intent directory.
- Request acceptance 1 (the data) is the first scenario; acceptance 2 (the inventory entry) is the second scenario.
- Non-secret literals preserved: the round id h23-release-bbf56fdc-vs-891c91b3, the two inventory input paths in order, the counts 18, 12 and 6, and `candidate_adopted` null.
- Omitted by request: rounds/index.json, rounds/README.md, the page, validators, docs, recompute.py and any recompute.

## Tests
- The retained cells.json is byte-identical to the source, has 18 unique slots (12 numeric, 6 null), candidate_adopted null, and the round directory holds only the allowed files: scenario "The round directory holds the retained data file" reading the working tree (scenario)
- The inventory keeps its earlier entries in order and ends with exactly one h23 entry whose inputs are cells.json then README.md and whose other fields are unchanged: scenario "The inventory entry lists the data file before the page" reading the working tree (scenario)

## Feasibility
- none
