# HC01 — environment record (draft)

Lane status is running. This draft records the two completed syn06 smoke cells; both have completion markers, and neither is represented as graded. The 32-cell plan remains the lane scope.

```yaml
schema: benchmark-environment/1
round: hc01
scope:
  status: running
  status_basis: The lane plan has 32 cells; this record documents the two completed syn06 smoke cells only. They have COMPLETE
    receipts and are not graded in this record.
  result_manifest:
    path: levers/env-receipts/hc01-execution-index.json
    sha256: fa4f6d93392398ef75dd1ae9439dc6180a9ee2f49ae0fa0278e8a8b587367b09
  registered_plan:
    path: levers/hc01-lane/PLAN.json
    sha256: 9ba7922a076b5f0f7b5e267bf7fd41a08ef50f8c35ce4bdabd80330f148f3c5b
  documented_smoke_cells: 2
environments:
- id: kogen-bench-us-20261008T055112Z
  captured_at_utc: '2026-10-08T05:51:12Z'
  valid_from_utc: '2026-10-08T05:51:12Z'
  valid_until_utc: '2026-10-08T05:51:12Z'
  host:
    id: kogen-bench-us
    capture_host: kogen-bench-us
    cpu_model: AMD EPYC-Milan
    physical_cores: 1
    logical_cores: 2
    allocation: 1 physical core and 2 logical CPUs visible; root cgroup CPU quota was not established in this capture (G1)
    ram_bytes: 8123707392
    memory_limit_bytes: unlimited for the user slice at capture time
    os_name_version: Ubuntu 24.04.5 LTS
    kernel: '6.8.0-142-generic #142-Ubuntu SMP PREEMPT_DYNAMIC Wed Sep 2 14:24:27 UTC 2026'
  receipt:
    path: levers/env-receipts/host-us-20261008T0551Z.json
    sha256: 581d2b418a8313314a1d6dbdfbbffac9a61ea53f76942ba10b3b9c8a813c4775
client:
  kind: kogen
  codex_cli_version: codex-cli 0.160.0 as reported by the host receipt
  binary_sha256: ec94cbcf14419a9ae46b3cf6580781b83c9522feaa6a425b130342c9679aa894
  binary_receipt:
    path: levers/hc01-lane/READY.md
    sha256: af4aeb4638119e951797544a687820a055c586ef9024f75f2a7485f2a178d262
  source_commit: 1bc242254bd9c0d793795e956b27ca0926c9875b
  version: kogen 1bc24225 (2026-10-08)
  launcher_wrapper_sha256: 3535a629e78cc926c257b0968834db4147b19e065d5f8e63f55c3f230fefda6f
  launcher_receipt:
    path: levers/hc01-lane/SHA256SUMS
    sha256: 51a79ea04b46ef1e3cb3ace26f32984aa42db7cd79a4cdc0cc2c55f05642120e
recipe:
  id: ladder-luna
  config:
    path: levers/hc01-lane/RECIPE.json
    sha256: 6b3982e49633024715eb83ffc5d7726fd6e1b53e52167308d07bb2c24b6cff18
  roles:
  - role: shaper
    configured_model: gpt-6.1-sol
    configured_effort: high
  - role: fallback_shaper
    configured_model: gpt-6.1-sol
    configured_effort: high
  - role: planner
    configured_model: gpt-6.1-sol
    configured_effort: high
  - role: auditor
    configured_model: gpt-6.1-sol
    configured_effort: high
  - role: reviewer
    configured_model: gpt-6.1-sol
    configured_effort: high
  - role: context
    configured_model: gpt-6.1-sol
    configured_effort: high
  - role: builder
    configured_model: gpt-6-luna
    configured_effort: max
  - role: rung2
    configured_model: gpt-6-luna
    configured_effort: max
  - role: rung3
    configured_model: gpt-6-luna
    configured_effort: max
  fallback_and_retry_policy: Recipe no_fallback is true; lane plan retries are zero.
sandbox:
  kind_version: bubblewrap 0.9.0 at the host capture; attempt configs identify R74 bench.py/bwrap isolation
  attempt_isolation: read-only auth bind; chatgpt.com-only egress; per-arm harness names are recorded in attempt configs
grader:
  version: night_grade v2 / mac-private-v2 route
  code_sha256: 52563c104e42de3076d0f95a6461fe32d9acb79836cde0db023cb8d41be48efe
  code_scope: route wrapper, not the immutable grader engine
  route_host: grading-mac
  receipt:
    path: probe-luna-low-20261002/grades/grade_cell.sh
    sha256: 52563c104e42de3076d0f95a6461fe32d9acb79836cde0db023cb8d41be48efe
  smoke_grade_status: No official HC01 grade receipt is included in this environment record.
tasks:
- id: syn-06-migration-ticket-numbers
  version: HC01 SMALL32 syn06 r1
  base_kind: git-commit
  base_revision: f8b30351614c1b4ad22b28c6bd21b13598fe8a5e
  prompt_sha256: 1b0906a68da1c191e6397557eda0a2d66ef4e2b7cc059b21ac4b89a6230d725d
  arms:
  - name: 'OFF'
    context_packet: false
    spec:
      path: levers/hc01-lane/specs/us-syn06-off.json
      sha256: 2b678c8c46ec5e58f263eb9ee395bbc9e6599075e9bcd80882881a130dc937c8
  - name: 'ON'
    context_packet: true
    spec:
      path: levers/hc01-lane/specs/us-syn06-on.json
      sha256: ae734e76fe0c8ec1775dff669294c49e238c78c0dc3a3f421d793486d4685934
execution:
  attempt_manifest:
    path: levers/env-receipts/hc01-execution-index.json
    sha256: fa4f6d93392398ef75dd1ae9439dc6180a9ee2f49ae0fa0278e8a8b587367b09
  cells:
  - cell_id: kogen-rs-hc01-off__gpt-6-luna__max__default__syn-06-migration-ticket-numbers__r1
    host_id: kogen-bench-us
    task_id: syn-06-migration-ticket-numbers
    arm: 'OFF'
    context_packet: false
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 1b0906a68da1c191e6397557eda0a2d66ef4e2b7cc059b21ac4b89a6230d725d
    base_kind: git-commit
    base_revision: f8b30351614c1b4ad22b28c6bd21b13598fe8a5e
    spec:
      path: levers/hc01-lane/specs/us-syn06-off.json
      sha256: 2b678c8c46ec5e58f263eb9ee395bbc9e6599075e9bcd80882881a130dc937c8
    started_at_utc: '2026-10-08T05:33:47.384Z'
    ended_at_utc: '2026-10-08T05:50:26.027Z'
    manifest:
      path: kogen-bench-us:public-source-location-withheld
      sha256: 5a99e73aaeb95c603152fd466656a60e3f080a968c369b3ccf08d7a658087edf
    attempt_config:
      path: kogen-bench-us:public-source-location-withheld
      sha256: 775f6d3df6f88179d694d713032f538d1ecdec4bce97950e537132d1f07ad5d4
    complete:
      path: kogen-bench-us:public-source-location-withheld
      sha256: 0da3bf585f891f9223f32da53a10b0ad88d654f2095fc8dd9b72a23f1e809b6c
  - cell_id: kogen-rs-hc01-on__gpt-6-luna__max__default__syn-06-migration-ticket-numbers__r1
    host_id: kogen-bench-us
    task_id: syn-06-migration-ticket-numbers
    arm: 'ON'
    context_packet: true
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 1b0906a68da1c191e6397557eda0a2d66ef4e2b7cc059b21ac4b89a6230d725d
    base_kind: git-commit
    base_revision: f8b30351614c1b4ad22b28c6bd21b13598fe8a5e
    spec:
      path: levers/hc01-lane/specs/us-syn06-on.json
      sha256: ae734e76fe0c8ec1775dff669294c49e238c78c0dc3a3f421d793486d4685934
    started_at_utc: '2026-10-08T05:50:26.834Z'
    ended_at_utc: '2026-10-08T06:09:14.084Z'
    manifest:
      path: kogen-bench-us:public-source-location-withheld
      sha256: c115f63504cdb1347720af66fac34998348a54e7a7d867b8097fddd11ff75fab
    attempt_config:
      path: kogen-bench-us:public-source-location-withheld
      sha256: af488199357d78c7acdece4ddd5e834ce25ae66706de6545e06b2de53ca52485
    complete:
      path: kogen-bench-us:public-source-location-withheld
      sha256: 9e0e560966cffe79a9add66ae3569823a5dddb86a3e53e1761a387574eb27b13
accounting:
  schema: Kogen R74 recipe request usage parsed and aggregated by the HC01 runner.
  collector:
    path: levers/hc01-lane/run_kogen_rs_cell.py
    sha256: 6af98311e430856861347756d030420b21b3ba2ab07c0e2f5f6747e4dfc321b1
  parser:
    path: levers/hc01-lane/run_r74recipe_r5.py
    sha256: e556ad1c505f0e53b0bfb5dc20ea05bf26d0fdc0a56277ec5a985a5071fd083d
  input_includes_cached: false
  total_formula: uncached input + cached input + output
  reasoning_in_output: The collector emits a separate reasoning counter; total is uncached input + cached input + output.
  cache_write_semantics: Parser accepts separate cache_write aliases; the counter is recorded separately and is not part of
    total.
  aggregation: Per-request rows are summarized, then grouped into stages and summed across token keys; builder and configured
    role pins are included in usage.json.
  interrupted_or_missing_usage: The parser returns 0 when a usage field is absent or not numeric; therefore absent values
    are represented as zero by current code.
  cache_share_formula: cached / (uncached + cached) in the request summary.
  price_basis: not-priced in this environment record
evidence:
  local_files:
  - note: host capture procedure
    path: levers/env-receipts/capture_host_env.sh
    sha256: c22a6778b726c12bcb2402896930369bfb946b5a57a1d52283164e0d820695bc
  - note: host receipt checksum list
    path: levers/env-receipts/SHA256SUMS
    sha256: d57b455ad9d8d1a34f0979f07eda207731118e566b55e9500e4c61216271ee66
  - note: US host point-in-time receipt
    path: levers/env-receipts/host-us-20261008T0551Z.json
    sha256: 581d2b418a8313314a1d6dbdfbbffac9a61ea53f76942ba10b3b9c8a813c4775
  - note: registered HC01 design and task base
    path: levers/hc01/DESIGN.md
    sha256: 2c5415746ac867d68a25cba9c366bf41754f5c834cb05d182a151b9fee3a16d3
  - note: EU to US host amendment
    path: levers/hc01/AMENDMENT-1.md
    sha256: 8c56e2ae12fe7b7b2441c21608055356a5b691db9e3b844d1cd8301e7bdfc2d2
  - note: registered 32-cell plan and smoke order
    path: levers/hc01-lane/PLAN.json
    sha256: 9ba7922a076b5f0f7b5e267bf7fd41a08ef50f8c35ce4bdabd80330f148f3c5b
  - note: Kogen role/model/effort configuration
    path: levers/hc01-lane/RECIPE.json
    sha256: 6b3982e49633024715eb83ffc5d7726fd6e1b53e52167308d07bb2c24b6cff18
  - note: Kogen binary pin and build receipt
    path: levers/hc01-lane/READY.md
    sha256: af4aeb4638119e951797544a687820a055c586ef9024f75f2a7485f2a178d262
  - note: US host preflight and task-base receipt
    path: levers/hc01-lane/PREFLIGHT-US.md
    sha256: 7a442eee537e07447d48d614887f6a41bb83a8073402eea4a2b703105862bebf
  - note: lane source and wrapper checksum list
    path: levers/hc01-lane/SHA256SUMS
    sha256: 51a79ea04b46ef1e3cb3ace26f32984aa42db7cd79a4cdc0cc2c55f05642120e
  - note: OFF smoke run specification
    path: levers/hc01-lane/specs/us-syn06-off.json
    sha256: 2b678c8c46ec5e58f263eb9ee395bbc9e6599075e9bcd80882881a130dc937c8
  - note: ON smoke run specification
    path: levers/hc01-lane/specs/us-syn06-on.json
    sha256: ae734e76fe0c8ec1775dff669294c49e238c78c0dc3a3f421d793486d4685934
  - note: lane launcher
    path: levers/hc01-lane/bench-rs.py
    sha256: d22b68595efb033a976932639734934600366415250a318b31adcecf9d5e72f7
  - note: lane adapter and no-fallback environment
    path: levers/hc01-lane/lane_adapter.py
    sha256: cdbf90d62df7141fef6f625a9b8b05bbb6a92587ecadd01c549be7e58ce8760c
  - note: Kogen request/stage usage aggregation
    path: levers/hc01-lane/run_kogen_rs_cell.py
    sha256: 6af98311e430856861347756d030420b21b3ba2ab07c0e2f5f6747e4dfc321b1
  - note: request usage parser and normalization
    path: levers/hc01-lane/run_r74recipe_r5.py
    sha256: e556ad1c505f0e53b0bfb5dc20ea05bf26d0fdc0a56277ec5a985a5071fd083d
  - note: planned official grade route wrapper
    path: probe-luna-low-20261002/grades/grade_cell.sh
    sha256: 52563c104e42de3076d0f95a6461fe32d9acb79836cde0db023cb8d41be48efe
  - note: joined smoke manifest/config/completion receipts
    path: levers/env-receipts/hc01-execution-index.json
    sha256: fa4f6d93392398ef75dd1ae9439dc6180a9ee2f49ae0fa0278e8a8b587367b09
gaps:
- field: environments[*].host.allocation
  reason: The host receipt shows visible physical/logical cores but does not contain a root CPU quota value.
  recoverability: partial
  evidence: host-us-20261008T0551Z.json SHA-256 listed in evidence.local_files
- field: environments[*].host continuity over complete cell intervals
  reason: The single host receipt was captured after OFF ended and during ON; it does not establish the host state throughout
    either full interval.
  recoverability: partial
  evidence: host receipt plus per-cell manifest hashes in hc01-execution-index.json
- field: recipe.roles[*].effective_model and effective_effort
  reason: The local recipe attests configured pins; the allowed attempt config receipts do not contain per-request role/model/effort
    observations.
  recoverability: partial
  evidence: RECIPE.json SHA-256 and per-cell attempt config hashes in hc01-execution-index.json
- field: client.dirty_patch_sha256
  reason: The lane readiness record pins the Kogen source commit and binary, but no per-run dirty-tree receipt is included
    in the allowed attempt files.
  recoverability: partial
  evidence: READY.md and remote attempt config receipts
- field: sandbox.network_policy_sha256 and mount_tool_inventory_sha256
  reason: Attempt configs state the isolation mode and egress text but do not include independent hashes for network policy
    or mount/tool inventory.
  recoverability: partial
  evidence: per-cell attempt config hashes in hc01-execution-index.json
- field: grader immutable engine hash and task suite manifest hash
  reason: The cited hash identifies the Mac Studio route wrapper; the smoke cells have no official grade receipt and no public
    suite-manifest digest.
  recoverability: unresolved
  evidence: grade_cell.sh SHA-256 and absence of a smoke grade receipt in this record
- field: accounting.reasoning_in_output and exact cache-write semantics
  reason: The code stores reasoning and cache_write separately but these source files do not establish provider-side inclusion
    semantics.
  recoverability: partial
  evidence: run_r74recipe_r5.py and run_kogen_rs_cell.py SHA-256 citations above
- field: accounting.interrupted_or_missing_usage
  reason: Current parser converts absent usage fields to zero; it does not preserve null/unknown for absent counters.
  recoverability: partial
  evidence: run_r74recipe_r5.py lines 83-107 and run_kogen_rs_cell.py lines 445-461, with SHA-256 citations above
- field: accounting.filesystem_cache_policy
  reason: Per-arm harness identity is recorded, but build/dependency cache isolation across arms is not shown by the allowed
    receipts.
  recoverability: partial
  evidence: attempt config hashes in hc01-execution-index.json
```
