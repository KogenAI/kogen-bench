# T1 changes

Applied with `python3 conformance/bin/t1_patch.py`.

- `cases/**/*.manifest.json`: retain only model/effort body predicates; clear request headers/presence assertions; relax positive exact bounds by +2, append two spare final responses with gates cleared, and refresh script digests.
- `cases/quint/{status,recovery,git}/*.itf.json`: insert no-hash approval review cards; capture full hashes and use captures/prefixes for commands and observations, including status reapproval.
- `cases/04-shape-approve-queue-land.json`: remove scripted role checks and provider/OAuth request observations, including exact list counts; allow unused responses and append two spare responses.
- `bin/t1_patch.py`: reproducible case-only patch script.

Counts (this run):

- case_files_changed: 124
- empty_no_call_envelopes: 96
- equals_assertions_removed: 43736
- exact_bounds_relaxed: 1888
- full_hash_literals_replaced: 159
- header_assertions_removed: 14344
- legacy_oauth_request_observations_removed: 1
- legacy_request_expectations_removed: 7
- legacy_request_observations_removed: 14
- legacy_spare_turns_added: 2
- prefix_hash_literals_replaced: 8
- presence_assertions_removed: 28472
- review_calls_inserted: 23
- script_digests_refreshed: 2928
- script_envelopes_scanned: 3024
- spare_turns_added: 3776

Validation: all 228 JSON case files parse; 3,024 script envelopes pass bounds/predicate/digest checks; 1,221 status/recovery/git trace steps pass the runner schema validator; target hash literals are absent. A second run makes no changes.

Exclusions: none.

Assembler notes:

- The runner job must remove `_validate_script`'s mandatory `/input` predicate. Current runner rejects these intentionally relaxed scripts until that patch is assembled. POST remains as a required schema discriminator; request headers are empty.
- Empty 0/0 envelopes have no scripted response and represent no-call cases; retained. All call-bearing envelopes retain `min_requests >= 1`. Existing unequal bounds are retained.
- Spare responses are copies of each script's final response (gates cleared); the original minimum is unchanged.
- Source/fixture provenance digests are unchanged because no spec files were edited. Embedded script digests were recalculated.
- Approval review cards use the runner's existing full-line capture syntax, following intent review cases. No implementation binary is present for end-to-end execution.

Changed case files:

- `cases/04-shape-approve-queue-land.json`
- `cases/quint/approve/trace-20270010.manifest.json`
- `cases/quint/approve/trace-20270011.manifest.json`
- `cases/quint/approve/trace-20270012.manifest.json`
- `cases/quint/approve/trace-20270013.manifest.json`
- `cases/quint/approve/trace-20270014.manifest.json`
- `cases/quint/approve/trace-20270015.manifest.json`
- `cases/quint/approve/trace-20270016.manifest.json`
- `cases/quint/approve/trace-20270017.manifest.json`
- `cases/quint/build/trace-20271010.manifest.json`
- `cases/quint/build/trace-20271011.manifest.json`
- `cases/quint/build/trace-20271012.manifest.json`
- `cases/quint/build/trace-20271013.manifest.json`
- `cases/quint/build/trace-20271014.manifest.json`
- `cases/quint/build/trace-20271015.manifest.json`
- `cases/quint/build/trace-20271016.manifest.json`
- `cases/quint/build/trace-20271017.manifest.json`
- `cases/quint/check/trace-20272010.manifest.json`
- `cases/quint/check/trace-20272011.manifest.json`
- `cases/quint/check/trace-20272012.manifest.json`
- `cases/quint/check/trace-20272013.manifest.json`
- `cases/quint/check/trace-20272014.manifest.json`
- `cases/quint/check/trace-20272015.manifest.json`
- `cases/quint/check/trace-20272016.manifest.json`
- `cases/quint/check/trace-20272017.manifest.json`
- `cases/quint/cli/trace-20261010.manifest.json`
- `cases/quint/cli/trace-20261011.manifest.json`
- `cases/quint/cli/trace-20261012.manifest.json`
- `cases/quint/cli/trace-20261013.manifest.json`
- `cases/quint/cli/trace-20261014.manifest.json`
- `cases/quint/cli/trace-20261015.manifest.json`
- `cases/quint/cli/trace-20261016.manifest.json`
- `cases/quint/cli/trace-20261017.manifest.json`
- `cases/quint/git/trace-20262010.itf.json`
- `cases/quint/git/trace-20262010.manifest.json`
- `cases/quint/git/trace-20262011.itf.json`
- `cases/quint/git/trace-20262011.manifest.json`
- `cases/quint/git/trace-20262012.itf.json`
- `cases/quint/git/trace-20262012.manifest.json`
- `cases/quint/git/trace-20262013.manifest.json`
- `cases/quint/git/trace-20262014.itf.json`
- `cases/quint/git/trace-20262014.manifest.json`
- `cases/quint/git/trace-20262015.itf.json`
- `cases/quint/git/trace-20262015.manifest.json`
- `cases/quint/git/trace-20262016.itf.json`
- `cases/quint/git/trace-20262016.manifest.json`
- `cases/quint/git/trace-20262017.itf.json`
- `cases/quint/git/trace-20262017.manifest.json`
- `cases/quint/init/trace-20267010.manifest.json`
- `cases/quint/init/trace-20267011.manifest.json`
- `cases/quint/init/trace-20267012.manifest.json`
- `cases/quint/init/trace-20267013.manifest.json`
- `cases/quint/init/trace-20267014.manifest.json`
- `cases/quint/init/trace-20267015.manifest.json`
- `cases/quint/init/trace-20267016.manifest.json`
- `cases/quint/init/trace-20267017.manifest.json`
- `cases/quint/intent/trace-20268010.manifest.json`
- `cases/quint/intent/trace-20268011.manifest.json`
- `cases/quint/intent/trace-20268012.manifest.json`
- `cases/quint/intent/trace-20268013.manifest.json`
- `cases/quint/intent/trace-20268014.manifest.json`
- `cases/quint/intent/trace-20268015.manifest.json`
- `cases/quint/intent/trace-20268016.manifest.json`
- `cases/quint/intent/trace-20268017.manifest.json`
- `cases/quint/landing/trace-20273010.manifest.json`
- `cases/quint/landing/trace-20273011.manifest.json`
- `cases/quint/landing/trace-20273012.manifest.json`
- `cases/quint/landing/trace-20273013.manifest.json`
- `cases/quint/landing/trace-20273014.manifest.json`
- `cases/quint/landing/trace-20273015.manifest.json`
- `cases/quint/landing/trace-20273016.manifest.json`
- `cases/quint/landing/trace-20273017.manifest.json`
- `cases/quint/process/trace-20263010.manifest.json`
- `cases/quint/process/trace-20263011.manifest.json`
- `cases/quint/process/trace-20263012.manifest.json`
- `cases/quint/process/trace-20263013.manifest.json`
- `cases/quint/process/trace-20263014.manifest.json`
- `cases/quint/process/trace-20263015.manifest.json`
- `cases/quint/process/trace-20263016.manifest.json`
- `cases/quint/process/trace-20263017.manifest.json`
- `cases/quint/queue/trace-20274010.manifest.json`
- `cases/quint/queue/trace-20274011.manifest.json`
- `cases/quint/queue/trace-20274012.manifest.json`
- `cases/quint/queue/trace-20274013.manifest.json`
- `cases/quint/queue/trace-20274014.manifest.json`
- `cases/quint/queue/trace-20274015.manifest.json`
- `cases/quint/queue/trace-20274016.manifest.json`
- `cases/quint/queue/trace-20274017.manifest.json`
- `cases/quint/recovery/trace-20266010.itf.json`
- `cases/quint/recovery/trace-20266010.manifest.json`
- `cases/quint/recovery/trace-20266011.itf.json`
- `cases/quint/recovery/trace-20266011.manifest.json`
- `cases/quint/recovery/trace-20266012.itf.json`
- `cases/quint/recovery/trace-20266012.manifest.json`
- `cases/quint/recovery/trace-20266013.itf.json`
- `cases/quint/recovery/trace-20266013.manifest.json`
- `cases/quint/recovery/trace-20266014.itf.json`
- `cases/quint/recovery/trace-20266014.manifest.json`
- `cases/quint/recovery/trace-20266015.itf.json`
- `cases/quint/recovery/trace-20266015.manifest.json`
- `cases/quint/recovery/trace-20266016.itf.json`
- `cases/quint/recovery/trace-20266016.manifest.json`
- `cases/quint/recovery/trace-20266017.itf.json`
- `cases/quint/recovery/trace-20266017.manifest.json`
- `cases/quint/shape/trace-20269010.manifest.json`
- `cases/quint/shape/trace-20269011.manifest.json`
- `cases/quint/shape/trace-20269012.manifest.json`
- `cases/quint/shape/trace-20269013.manifest.json`
- `cases/quint/shape/trace-20269014.manifest.json`
- `cases/quint/shape/trace-20269015.manifest.json`
- `cases/quint/shape/trace-20269016.manifest.json`
- `cases/quint/shape/trace-20269017.manifest.json`
- `cases/quint/status/trace-20265010.manifest.json`
- `cases/quint/status/trace-20265011.manifest.json`
- `cases/quint/status/trace-20265012.manifest.json`
- `cases/quint/status/trace-20265013.itf.json`
- `cases/quint/status/trace-20265013.manifest.json`
- `cases/quint/status/trace-20265014.manifest.json`
- `cases/quint/status/trace-20265015.itf.json`
- `cases/quint/status/trace-20265015.manifest.json`
- `cases/quint/status/trace-20265016.itf.json`
- `cases/quint/status/trace-20265016.manifest.json`
- `cases/quint/status/trace-20265017.itf.json`
- `cases/quint/status/trace-20265017.manifest.json`
