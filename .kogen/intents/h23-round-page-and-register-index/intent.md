# Publish the h23 round page and register it

Slug: h23-round-page-and-register-index
Model: not applicable — the change adds a static report page and appends three registry entries; there is no state or interacting rule to model
Acceptance:
- .kogen/intents/h23-round-page-and-register-index/acceptance.feature
- features/steps/h23-round-page-and-register-index__steps.js

Publish the report page of round h23-release-bbf56fdc-vs-891c91b3 as one DESCRIPTIVE historical audit round (18 planned slots, 12 numeric grades, 6 without; original verdict rejected, no adoption, full rerun unavailable) and register it in the same row everywhere the repository requires, so the round directory never exists unregistered: the round index, the reproduction inventory and the human-readable round register.

The row creates exactly one file, `rounds/h23-release-bbf56fdc-vs-891c91b3/README.md`, whose bytes are those recorded in `.kogen/intents/h23-round-page-and-register-index/fixtures/page.md` (the final newline is optional). It changes exactly three existing files and nothing else: no cells.json, no recompute.py, no validator change, no other doc. The page has no Round date line on purpose. The words score and total that the page shows in code formatting are page content only. The page mentions `python3 recompute.py`; a later row adds that script and cells.json, and this row creates neither.

The three changes, with the retained values in `.kogen/intents/h23-round-page-and-register-index/fixtures/expected.json`:

- `rounds/index.json` (a JSON list of round IDs): append the ID h23-release-bbf56fdc-vs-891c91b3 as the last entry, in the style of the existing entries. Every earlier entry stays unchanged and in order.
- `reproduce/round-inventory.json`: append the retained inventory-entry object (`round_id` h23-release-bbf56fdc-vs-891c91b3, `script` null, `inputs` listing only the round page, `replay_type` unavailable, `full_execution_replayable` false, and the retained `availability_note`) as the last entry of the "rounds" list, in the file's existing style. Every earlier entry stays unchanged and in order. Until the next row lands, the entry lists only the page as input.
- `rounds/README.md`: append one blank line and then the retained rounds-readme-bullet line (the `bullet` value in expected.json) as the last line. The earlier text stays unchanged.

Protected by the existing tests and the validator, not by acceptance: they keep passing; every other tracked file under results and rounds is untouched; the git index records of everything under results and rounds, other than the records under the new round directory, rounds/README.md and rounds/index.json, hash to sha256 71bba8d8344ca2eb38957b0eeabdc347689725cb35ff85ca1870935e29580b5d when taken as `git ls-files -s -z` prints them, each record keeping its NUL byte; the build establishes by reading the repository how to reproduce that digest.

## Decisions
- The round ID is appended as the last entry of rounds/index.json, because the existing list is not in sorted order and the validator only requires that every index ID has exactly one inventory entry, not an order. (constraint: the earlier index entries stay unchanged and in the same order) (evidence: rounds/index.json; reproduce/validate_repo.py) (source: request)
- The index entry, the inventory entry and the round-register line land together with the page, so that the validator's rule of exactly one inventory entry for every ID in rounds/index.json holds. (decision: D2, round 1) (constraint: exactly one inventory entry for the new ID, last in the "rounds" list; earlier entries unchanged and in order) (evidence: reproduce/validate_repo.py; reproduce/round-inventory.json) (source: request)
- The register bullet is appended to rounds/README.md after exactly one blank line, as its last line, and the earlier text is unchanged. (decision: D3, round 1) (constraint: the file equals the earlier text, one blank line and the bullet line) (evidence: rounds/README.md) (source: request)
- The round directory holds only README.md, plus cells.json if the next row has already landed; no recompute.py, no other file, and no Round date line on the page. (decision: D4, round 1) (constraint: no other file is created or changed) (assumption: the request states that cells.json and recompute.py arrive in later rows, so this row creates neither and a later cells.json is tolerated by the page check) (source: request)
- The acceptance checks inspect only the working tree, hold the earlier register text and the earlier list entries as sha256 digests recorded from the unchanged files, and run neither the tests nor the validator. (decision: D5, round 1) (evidence: rounds/README.md; rounds/index.json; reproduce/round-inventory.json) (source: request)
- The round ID is appended as the last entry of rounds/index.json, because the existing list is not in sorted order and the validator only requires that every index ID has exactly one inventory entry, not an order. (decision: D1, round 1) (constraint: the earlier index entries stay unchanged and in the same order) (evidence: rounds/index.json; reproduce/validate_repo.py) (assumption: An ad hoc listing showed the index is not alphabetical; no run confirmed the validator accepts the appended order.) (source: request)

## Source comparison
- Page bytes: addressed, `rounds/h23-release-bbf56fdc-vs-891c91b3/README.md` equals the retained page in fixtures/page.md (final newline optional).
- Register bullet: addressed, the retained bullet line is the last line of rounds/README.md after one blank line.
- Inventory entry: addressed, the retained object is the last entry of the "rounds" list; the entry lists only the page as input.
- Round index: addressed, the round ID is the last entry of rounds/index.json.
- cells.json and recompute.py: omitted on purpose; a later row adds them. A validator change: excluded from this row.
- Digest 71bba8d8344ca2eb38957b0eeabdc347689725cb35ff85ca1870935e29580b5d of the other git index records under results and rounds: a protected constraint reproduced by the build from the repository, not an acceptance scenario.

## Tests
- The round page is the retained page and alone in its directory: scenario "The round page is the retained page and alone in its directory" in acceptance.feature (scenario)
- The round register holds the earlier text, one blank line and the retained bullet line last: scenario "The round register lists the round" in acceptance.feature (scenario)
- The index and the inventory keep their earlier entries in order and gain exactly one new last entry each: scenario "The index and the inventory register the round" in acceptance.feature (scenario)
- The validator and existing tests keep passing unchanged: the configured validate-repo check (existing)

## Feasibility
- none
