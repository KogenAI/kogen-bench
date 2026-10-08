# L3b repair vs continue — environment record

Round status is complete: the [public results table](RESULTS.md) records official grades for all 24 planned cells, corroborated by the retained receipts. The latest retained grade window is 2026-10-08T06:06:26Z. No outcomes or hidden-suite content are reproduced here; suite digests only are retained. Per-cell score metadata now records host node, platform/kernel, Python, concurrency, grader digest, and task-suite digest. Host captures at 05:51Z remain point-in-time snapshots.

Evidence availability: every `levers/...` path cited below is a private operator record that is not part of this repository. Its SHA-256 is source-reported (see [PRIVATE.md](../../PRIVATE.md)) and can't be verified from public bytes; this covers the design, cell plan, grade windows, execution index and host captures. Host observations (CPU, memory, OS, kernel, sandbox) come from private dated captures taken 2026-10-08T05:51Z and are likewise source-reported. Values that no retained record supports are listed under `gaps` instead. Publicly checkable inputs are the outcome CSVs and records in this round directory.

```yaml
schema: benchmark-environment/1
round: l3b-repair-vs-continue
scope:
  status: complete
  status_basis: 'Complete: RESULTS-24.md records official grade receipts for all 24 planned scored cells; the score ledger
    and RELEASE-STATE corroborate 24 of 24 across four grade windows through 2026-10-08T06:06:26Z.'
  result_manifest:
    path: levers/env-receipts/l3b-execution-index.json
    sha256: c0849cef7d9a28b20ce53d6970315c14a278fca5518cb260e77b3698f57ce9c4
  score_ledger:
    path: levers/lanes-2026-10-07/l3b/grades.jsonl
    sha256: de29adb99ffcd8dde954ab2aba09bbf5a4a984ef9932ecad777f0ee3fc7bef52
  release_state:
    path: levers/lanes-2026-10-07/l3b/RELEASE-STATE.json
    sha256: b6cc877115a567e15caf58834c48f259571ee3c67678e6e53429183ced53d7dd
  scored_cell_count: 24
  planned_scored_cell_count: 24
  results_receipt:
    path: levers/lanes-2026-10-07/l3b/RESULTS-24.md
    sha256: cde087a2cb356c85f4b18073ec13290d3b171fdc1986243ee8a789cf2a349f55
environments:
- id: kogen-bench-us-20261008T055112Z
  captured_at_utc: '2026-10-08T05:51:12Z'
  valid_from_utc: '2026-10-08T05:51:12Z'
  valid_until_utc: '2026-10-08T05:51:12Z'
  host:
    id: kogen-bench-us
    capture_host: kogen-bench-us
    provider_class: 2-vCPU AMD EPYC KVM VM
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
- id: kogen-bench-eu-20261008T055115Z
  captured_at_utc: '2026-10-08T05:51:15Z'
  valid_from_utc: '2026-10-08T05:51:15Z'
  valid_until_utc: '2026-10-08T05:51:15Z'
  host:
    id: kogen-bench-eu
    capture_host: kogen-bench-eu
    provider_class: 2-vCPU AMD EPYC KVM VM
    cpu_model: AMD EPYC-Milan
    physical_cores: 1
    logical_cores: 2
    allocation: 1 physical core and 2 logical CPUs visible; root cgroup CPU quota was not established in this capture (G1)
    ram_bytes: 8123707392
    memory_limit_bytes: unlimited for the user slice at capture time
    os_name_version: Ubuntu 24.04.5 LTS
    kernel: '6.8.0-142-generic #142-Ubuntu SMP PREEMPT_DYNAMIC Wed Sep 2 14:24:27 UTC 2026'
  receipt:
    path: levers/env-receipts/host-eu-20261008T0551Z.json
    sha256: 223bd8e313d918f91ee4525886f6a65b0ea3f6856f9ada394c59f3aebbbb01e1
client:
  kind: codex
  codex_cli_version: codex-cli 0.160.0 as reported by cell records and the point-in-time host capture
  binary_sha256: 12eb3e81114588aca3b7998f4f19e8997b056aca08e57a7ca7c8a3ec8c652aad
  binary_receipt:
    path: levers/env-receipts/host-us-20261008T0551Z.json
    sha256: 581d2b418a8313314a1d6dbdfbbffac9a61ea53f76942ba10b3b9c8a813c4775
  wrapper_sha256: 08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300
  wrapper_receipt:
    path: levers/lanes-2026-10-07/l3b/pilot-run-records.jsonl
    sha256: 92a96ae4227d456fa9da5e67c10f416126aa0d6f04e1721efbad212d59269637
  model_alias: gpt-6-luna
  effort: max
recipe:
  id: direct Codex
  config:
    path: levers/lanes-2026-10-07/l3b/cell-plan.json
    sha256: 0bdb4ff9ea51c1ac2750fa1ad71ea7436936603be76096566c378a57bfa7ef48
  roles:
  - role: direct coding agent
    requested_model: gpt-6-luna
    observed_model: gpt-6-luna in per-cell records
    requested_effort: max
    effective_effort: max in per-cell records
    prompt_hash_source: each execution row
    client_ref: client above
  fallback_and_retry_policy: Zero retries and a 3600-second cap in the public round configuration; direct model alias is fixed
    per scored cell.
sandbox:
  kind_version: bubblewrap 0.9.0 on the 2026-10-08 host captures; pilot records identify bwrap and an allowlist-proxy profile.
  pilot_profile_sha256: b67e7afbad1110342e222e1fd7b58e129500d4dd44c2aa39c57ef7494fcde104
  pilot_network_allowlist:
  - api.openai.com
  - chatgpt.com
grader:
  version: r70-macbook-window-v1 route
  code_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
  receipt:
    path: levers/lanes-2026-10-07/l3b/grades.jsonl
    sha256: de29adb99ffcd8dde954ab2aba09bbf5a4a984ef9932ecad777f0ee3fc7bef52
  window_receipt:
    path: levers/lanes-2026-10-07/l3b/windows.jsonl
    sha256: a80b9264723e6db63c66b16282d27ee0434f8048a4658a7f4e4b6845ba817799
  hash_to_window_joins:
  - at_utc: '2026-10-08T03:45:41Z'
    bench_host: kogen-bench-us
    cell_ids:
    - codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r9018
    - codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l3b9c__r9020
    grader_route: r70-macbook-window-v1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    receipts: windows.jsonl:4; grades.jsonl:49-50
  - at_utc: '2026-10-08T03:46:39Z'
    bench_host: kogen-bench-eu
    cell_ids:
    - codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b13r__r9016
    grader_route: r70-macbook-window-v1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    receipts: windows.jsonl:5; grades.jsonl:51
  - at_utc: '2026-10-08T04:43:42Z'
    bench_host: kogen-bench-us
    cell_ids:
    - codex__gpt-6-luna__max__default__r70-2-go__r9006
    - codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l3b9r__r9019
    - codex__gpt-6-luna__max__default__r70-5-go-l3b32c__r9023
    - codex__gpt-6-luna__max__default__r70-2-go-l3b32c__r9008
    - codex__gpt-6-luna__max__default__r70-5-go__r9021
    - codex__gpt-6-luna__max__default__r70-2-go-l3b32r__r9007
    - codex__gpt-6-luna__max__default__r70-5-go-l3b32r__r9022
    grader_route: r70-macbook-window-v1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    receipts: windows.jsonl:6; grades.jsonl:52-58
  - at_utc: '2026-10-08T06:06:26Z'
    bench_host: kogen-bench-eu
    cell_ids:
    - codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b9r__r9010
    - codex__gpt-6-luna__max__default__r70-2-elixir__r9003
    - codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9009
    - codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b10c__r9014
    - codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b10r__r9013
    - codex__gpt-6-luna__max__default__r70-7-rust__r9024
    - codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b13c__r9017
    - codex__gpt-6-luna__max__default__r70-2-elixir-l3b33r__r9004
    - codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9015
    - codex__gpt-6-luna__max__default__r70-7-rust-l3b31r__r9025
    - codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b9c__r9011
    - codex__gpt-6-luna__max__default__r70-2-elixir-l3b33c__r9005
    - codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9012
    - codex__gpt-6-luna__max__default__r70-7-rust-l3b31c__r9026
    grader_route: r70-macbook-window-v1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    receipts: windows.jsonl:7; grades.jsonl:59-72
execution:
  attempt_manifest:
    path: levers/env-receipts/l3b-execution-index.json
    sha256: c0849cef7d9a28b20ce53d6970315c14a278fca5518cb260e77b3698f57ce9c4
  completed_cell_count: 24
  cells:
  - cell_id: codex__gpt-6-luna__max__default__r70-2-go-l3b32c__r9008
    host_id: kogen-bench-us
    task_id: r70-2-go-l3b32c
    arm: CONTINUE
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: c296c324a89cc03adc56b3d896051d7f9c01ad22954ffe5dc7cfbb8ba1166b90
    base_kind: git-commit
    base_revision: a25ca44fcd42ac0f98b47de2361517171775480a
    started_at_utc: '2026-10-08T04:22:38.838Z'
    ended_at_utc: '2026-10-08T04:25:30.404Z'
    experiment: l3b-r70-2-go-l3b32c-continue-gpt-6-luna-r9008
    result_directory: kogen-bench-us:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-us:public-source-location-withheld
      sha256: c0d2773b1b69b976d957e37e4219d541c2b979147fbf6441ef905c22ba852381
    completion_receipt:
      path: kogen-bench-us:public-source-location-withheld
      sha256: 3fe02dd9550cd05747000da1a4f03ff85030a47339757f8b2a21b6f38b36e942
    variant_tree_sha256: 103cb78fc54ae20a3f4372b85e8d82ea958da36f7698257802fcf13f8bb2e86e
  - cell_id: codex__gpt-6-luna__max__default__r70-2-go-l3b32r__r9007
    host_id: kogen-bench-us
    task_id: r70-2-go-l3b32r
    arm: REPAIR
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: f9f379f1b0e557285ad06942908404d5064d27b40632b1c44926f6ff670ca444
    base_kind: git-commit
    base_revision: a25ca44fcd42ac0f98b47de2361517171775480a
    started_at_utc: '2026-10-08T04:28:02.873Z'
    ended_at_utc: '2026-10-08T04:34:01.673Z'
    experiment: l3b-r70-2-go-l3b32r-repair-gpt-6-luna-r9007
    result_directory: kogen-bench-us:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-us:public-source-location-withheld
      sha256: 34d9d0ad591442f9055cf99f5b798107eec21a9775cdf9d4e70e480883f735fa
    completion_receipt:
      path: kogen-bench-us:public-source-location-withheld
      sha256: b6f111363af44d837601121dd7fef164e1ef1584e37e6ad00adbc41cb5ab292c
    variant_tree_sha256: 103cb78fc54ae20a3f4372b85e8d82ea958da36f7698257802fcf13f8bb2e86e
  - cell_id: codex__gpt-6-luna__max__default__r70-2-go__r9006
    host_id: kogen-bench-us
    task_id: r70-2-go
    arm: RESTART
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: e121b09e202f3efd340d0279f38f7ca17a47d45fabbe384bf1eedb2fdd345c98
    base_kind: git-commit
    base_revision: 13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82
    started_at_utc: '2026-10-08T04:10:38.804Z'
    ended_at_utc: '2026-10-08T04:13:52.872Z'
    experiment: l3b-r70-2-go-restart-gpt-6-luna-r9006
    result_directory: kogen-bench-us:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-us:public-source-location-withheld
      sha256: b6f122c222166db7a64ace548beb1581cc841c2775fd0ab4e382a902f05dc7fc
    completion_receipt:
      path: kogen-bench-us:public-source-location-withheld
      sha256: 8a2fea14a238d9925443644b911b38f81c141408475b05c597d749b220e31f71
    variant_application:
      kind: original_base
      reason: RESTART starts from the original task base; no variant tree is applied
      evidence: levers/lanes-2026-10-07/l3b/RELEASE-STATE.json sha256:b6cc877115a567e15caf58834c48f259571ee3c67678e6e53429183ced53d7dd
  - cell_id: codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l3b9c__r9020
    host_id: kogen-bench-us
    task_id: r70-4-ts-bun-fe2-l3b9c
    arm: CONTINUE
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: a3ddbdbf9dfb81fa7e911f3e404c3225317488885d9bb78caec1e1b6e881170e
    base_kind: git-commit
    base_revision: d7a7c0f26f1871c900f5986653fce91aaaa33736
    started_at_utc: '2026-10-08T03:37:24.495Z'
    ended_at_utc: '2026-10-08T03:41:36.057Z'
    experiment: l3b-r70-4-ts-bun-fe2-l3b9c-continue-gpt-6-luna-r9020
    result_directory: kogen-bench-us:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-us:public-source-location-withheld
      sha256: c9300be8a1783f83e055d671e58bebab499976a6b5ca45b2ae68aa35e6ef3190
    completion_receipt:
      path: kogen-bench-us:public-source-location-withheld
      sha256: f7bffc48c0ec1a158562da3c93ab31bd9e1074d189e1c94b7291612590f0a31b
    variant_tree_sha256: 8deb74eac9b4768930a3390cb4d4cf06c2cd5a652176fc8948fc532c2823340d
  - cell_id: codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l3b9r__r9019
    host_id: kogen-bench-us
    task_id: r70-4-ts-bun-fe2-l3b9r
    arm: REPAIR
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 3ef071cfe43e0c9218049fd546bbd8c185eb957c16df8e841ea3dec300d14d57
    base_kind: git-commit
    base_revision: d7a7c0f26f1871c900f5986653fce91aaaa33736
    started_at_utc: '2026-10-08T04:13:53.820Z'
    ended_at_utc: '2026-10-08T04:20:24.438Z'
    experiment: l3b-r70-4-ts-bun-fe2-l3b9r-repair-gpt-6-luna-r9019
    result_directory: kogen-bench-us:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-us:public-source-location-withheld
      sha256: b5fcbeca62214b08de002a27099c9e3062a1e204966a7228ef552e751dc754c5
    completion_receipt:
      path: kogen-bench-us:public-source-location-withheld
      sha256: 6f5ad922cdcb7537e0851c8563f52820cccf7bb283a1d2094476cc1232356378
    variant_tree_sha256: 8deb74eac9b4768930a3390cb4d4cf06c2cd5a652176fc8948fc532c2823340d
  - cell_id: codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r9018
    host_id: kogen-bench-us
    task_id: r70-4-ts-bun-fe2
    arm: RESTART
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: bfc6c16480b6815adf15c395b25709dc9b8dc0d3a057b4ec2109bab2447af977
    base_kind: git-commit
    base_revision: cc3a831a167020538c4ca2ad90185606a2e4ad6a
    started_at_utc: '2026-10-08T03:32:24.577Z'
    ended_at_utc: '2026-10-08T03:37:23.281Z'
    experiment: l3b-r70-4-ts-bun-fe2-restart-gpt-6-luna-r9018
    result_directory: kogen-bench-us:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-us:public-source-location-withheld
      sha256: ad43b7eef918fba72a14dc91dcbe9c10f8793850c36e97c6bfff4a8a09e6bf3b
    completion_receipt:
      path: kogen-bench-us:public-source-location-withheld
      sha256: 586b7e584c3c0340b27cd4e5672c4d631276c76239b22141461f1c6eda684da3
    variant_application:
      kind: original_base
      reason: RESTART starts from the original task base; no variant tree is applied
      evidence: levers/lanes-2026-10-07/l3b/RELEASE-STATE.json sha256:b6cc877115a567e15caf58834c48f259571ee3c67678e6e53429183ced53d7dd
  - cell_id: codex__gpt-6-luna__max__default__r70-5-go-l3b32c__r9023
    host_id: kogen-bench-us
    task_id: r70-5-go-l3b32c
    arm: CONTINUE
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: f4dabd3e73549637a579b15ecb332e103d37e0f96a8ee00e58ba744d2fb5af35
    base_kind: git-commit
    base_revision: 54091c79f09540e6d773be15dcc54df6232a48d8
    started_at_utc: '2026-10-08T04:20:26.830Z'
    ended_at_utc: '2026-10-08T04:22:38.118Z'
    experiment: l3b-r70-5-go-l3b32c-continue-gpt-6-luna-r9023
    result_directory: kogen-bench-us:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-us:public-source-location-withheld
      sha256: eb6ba79ce20fbbc3ec6ab40730aa129fc1c865b141ec981f741db94dbf69922d
    completion_receipt:
      path: kogen-bench-us:public-source-location-withheld
      sha256: bb7e26cb4f66bb1cccc76882d9693f6d0420ff75ca39599cf32e8b35143e7716
    variant_tree_sha256: 25dc3c646c4de6080492028c1f7f4038c7018b5ea1612540ac6d19c6ea7df566
  - cell_id: codex__gpt-6-luna__max__default__r70-5-go-l3b32r__r9022
    host_id: kogen-bench-us
    task_id: r70-5-go-l3b32r
    arm: REPAIR
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 7226b3b39fa39af6b05f90ea9715927061b53cad93e4d42d27ce1120eef1967e
    base_kind: git-commit
    base_revision: 54091c79f09540e6d773be15dcc54df6232a48d8
    started_at_utc: '2026-10-08T04:34:02.899Z'
    ended_at_utc: '2026-10-08T04:38:25.242Z'
    experiment: l3b-r70-5-go-l3b32r-repair-gpt-6-luna-r9022
    result_directory: kogen-bench-us:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-us:public-source-location-withheld
      sha256: eacf1dfac3858a5c3527a3fc8d19a0e02e42567918f4a1a0ca61a8307062264e
    completion_receipt:
      path: kogen-bench-us:public-source-location-withheld
      sha256: 95d5b0a43715e47fb15288394282f941d94f9c92c16640af74975bdd70deeb73
    variant_tree_sha256: 25dc3c646c4de6080492028c1f7f4038c7018b5ea1612540ac6d19c6ea7df566
  - cell_id: codex__gpt-6-luna__max__default__r70-5-go__r9021
    host_id: kogen-bench-us
    task_id: r70-5-go
    arm: RESTART
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 5eafbf51a3c4c09e949fe03cbd98e8f69507ed6456e3e0d9f5197bf21cc3c89e
    base_kind: git-commit
    base_revision: e0b4a2478a17a924fcecb965b2941ca3396f49d6
    started_at_utc: '2026-10-08T04:25:32.856Z'
    ended_at_utc: '2026-10-08T04:27:59.630Z'
    experiment: l3b-r70-5-go-restart-gpt-6-luna-r9021
    result_directory: kogen-bench-us:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-us:public-source-location-withheld
      sha256: d86337f96336293f154c2db3fb54b05163ef7dc7ae7baca3008141a41f346eed
    completion_receipt:
      path: kogen-bench-us:public-source-location-withheld
      sha256: 08f75b54f07c2fa149cc49d1cd28ef454896a6665d3c96d0de3a4f75eef9cb4a
    variant_application:
      kind: original_base
      reason: RESTART starts from the original task base; no variant tree is applied
      evidence: levers/lanes-2026-10-07/l3b/RELEASE-STATE.json sha256:b6cc877115a567e15caf58834c48f259571ee3c67678e6e53429183ced53d7dd
  - cell_id: codex__gpt-6-luna__max__default__r70-2-elixir-l3b33c__r9005
    host_id: kogen-bench-eu
    task_id: r70-2-elixir-l3b33c
    arm: CONTINUE
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 0922b5849968b703fdea88ab6105e210852263df0dc30e8ba5ef95d020fcb471
    base_kind: git-commit
    base_revision: bcf8ab895355cfe822b08d187373dbc6faccb36c
    started_at_utc: '2026-10-08T05:35:23.092Z'
    ended_at_utc: '2026-10-08T05:41:12.534Z'
    experiment: l3b-r70-2-elixir-l3b33c-continue-gpt-6-luna-r9005
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 5a4cf303356709eb692cc0e5d33247958e6839cca224ef705095d53d1f2bfec3
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 88add08f0c9ffcfc1583ac3bd4ba419aecf6a3beddd90c931196fc4a75c89c68
    variant_tree_sha256: 833d9aaa604593030ca4519c7ff8adbdd2f2941db156239f9817557c6cb96abd
  - cell_id: codex__gpt-6-luna__max__default__r70-2-elixir-l3b33r__r9004
    host_id: kogen-bench-eu
    task_id: r70-2-elixir-l3b33r
    arm: REPAIR
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 27019f56551e3442897e080c908fe2064b694e52bc4f7d2b4f9579cd4cae0063
    base_kind: git-commit
    base_revision: bcf8ab895355cfe822b08d187373dbc6faccb36c
    started_at_utc: '2026-10-08T05:08:28.922Z'
    ended_at_utc: '2026-10-08T05:24:30.762Z'
    experiment: l3b-r70-2-elixir-l3b33r-repair-gpt-6-luna-r9004
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: a182f3570ef80b52159c374740afee9eee72dda4a63309186cb58b93ab05f184
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: faeacfa067d588b374f365c916f60d8b8765fc54d6f3ec33b7748c4155415b0e
    variant_tree_sha256: 833d9aaa604593030ca4519c7ff8adbdd2f2941db156239f9817557c6cb96abd
  - cell_id: codex__gpt-6-luna__max__default__r70-2-elixir__r9003
    host_id: kogen-bench-eu
    task_id: r70-2-elixir
    arm: RESTART
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 98bb12f5e44f7036239f30ec5e82e45d02e273e6a0dee2061a1b6a1234f0521d
    base_kind: git-commit
    base_revision: 470ba65c1d3c19191a2190a032cd9ebf24e71975
    started_at_utc: '2026-10-08T04:16:32.244Z'
    ended_at_utc: '2026-10-08T04:29:27.619Z'
    experiment: l3b-r70-2-elixir-restart-gpt-6-luna-r9003
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 608dff9e308ecf52b0359517798e7f0131d97c37e92b5dd570ec3f089c5ed007
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 8d82d4221aad4907dad5ed7787f83e22f1aeff40b483376f6ccf3dcf0bfc3cca
    variant_application:
      kind: original_base
      reason: RESTART starts from the original task base; no variant tree is applied
      evidence: levers/lanes-2026-10-07/l3b/RELEASE-STATE.json sha256:b6cc877115a567e15caf58834c48f259571ee3c67678e6e53429183ced53d7dd
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b10c__r9014
    host_id: kogen-bench-eu
    task_id: r70-4-elixir-fe2-l3b10c
    arm: CONTINUE
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 8f1147c1c76f4f7b8919f26defd9f736749b776100ff0c2e55a2e79a6375fb59
    base_kind: git-commit
    base_revision: a06ebe6275402f8bc55e7d84f973ecbaf22145c8
    started_at_utc: '2026-10-08T04:40:46.918Z'
    ended_at_utc: '2026-10-08T04:45:26.457Z'
    experiment: l3b-r70-4-elixir-fe2-l3b10c-continue-gpt-6-luna-r9014
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 8f7de4e5c0b358c82e01dfd5bf6b6211b7b906182a1d10439b5e204348f6383e
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 118e42de5322389a93ac6ac96660f0b31bb21284657fff6a794a85ae725b1de4
    variant_tree_sha256: ee73a3af3a59f59df96aec83a65790e0aa96b91b1c90f3fa9c0f7aa3336ea09e
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b10r__r9013
    host_id: kogen-bench-eu
    task_id: r70-4-elixir-fe2-l3b10r
    arm: REPAIR
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 3a63ab1170d7c4384333356f4d220ddc4cb992593d92aab88cc9a0ba9d4a1099
    base_kind: git-commit
    base_revision: a06ebe6275402f8bc55e7d84f973ecbaf22145c8
    started_at_utc: '2026-10-08T04:46:19.011Z'
    ended_at_utc: '2026-10-08T04:52:50.330Z'
    experiment: l3b-r70-4-elixir-fe2-l3b10r-repair-gpt-6-luna-r9013
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: c70b0ea24cbfbdc2b48baa778ee0bc15f22a0b014da4da363a39276c03a2c092
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: ea893bf3550a7ab5d96837bd9bdde042c31a24c227f9d15da5b8cded5e5ed337
    variant_tree_sha256: ee73a3af3a59f59df96aec83a65790e0aa96b91b1c90f3fa9c0f7aa3336ea09e
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b13c__r9017
    host_id: kogen-bench-eu
    task_id: r70-4-elixir-fe2-l3b13c
    arm: CONTINUE
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 8f1147c1c76f4f7b8919f26defd9f736749b776100ff0c2e55a2e79a6375fb59
    base_kind: git-commit
    base_revision: d3c4244af14088776ea541cfca512c928847dda5
    started_at_utc: '2026-10-08T05:05:13.904Z'
    ended_at_utc: '2026-10-08T05:08:27.385Z'
    experiment: l3b-r70-4-elixir-fe2-l3b13c-continue-gpt-6-luna-r9017
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: d30c3d23cbdd0fd960faa7c840c9ca2762ee209a441f208d3bd19310a542a332
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 1d89a7657bbd88516321f242012937ef1292c0752b563be427c0d9057929d5f7
    variant_tree_sha256: 86001055f3fba2c0c920a2f9c31938205f791d38f36635f2bbc510d913d7b2c5
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b13r__r9016
    host_id: kogen-bench-eu
    task_id: r70-4-elixir-fe2-l3b13r
    arm: REPAIR
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 3a63ab1170d7c4384333356f4d220ddc4cb992593d92aab88cc9a0ba9d4a1099
    base_kind: git-commit
    base_revision: d3c4244af14088776ea541cfca512c928847dda5
    started_at_utc: '2026-10-08T03:32:22.354Z'
    ended_at_utc: '2026-10-08T03:38:19.395Z'
    experiment: l3b-r70-4-elixir-fe2-l3b13r-repair-gpt-6-luna-r9016
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 74aefd452f23ecc109adf08f80ba05cc330b834426e38ccc739a39c5625486e5
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 26cbe14e01eb2eeea14d8e528b924e8ea3c896864954f6201fdb095cfe3739a3
    variant_tree_sha256: 86001055f3fba2c0c920a2f9c31938205f791d38f36635f2bbc510d913d7b2c5
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b9c__r9011
    host_id: kogen-bench-eu
    task_id: r70-4-elixir-fe2-l3b9c
    arm: CONTINUE
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 8f1147c1c76f4f7b8919f26defd9f736749b776100ff0c2e55a2e79a6375fb59
    base_kind: git-commit
    base_revision: 123de8a8f281a2c1ae5bdd07c47a5a90383d249e
    started_at_utc: '2026-10-08T05:33:05.065Z'
    ended_at_utc: '2026-10-08T05:35:20.353Z'
    experiment: l3b-r70-4-elixir-fe2-l3b9c-continue-gpt-6-luna-r9011
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 24a805a04d12a7738791949b316c8edb74ba649286d4d087797aa5fe47ea506b
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: d82567ea483ddbcf53a35977e172e205488c01df96c367d2f669126c59db9828
    variant_tree_sha256: 3d36b9a632c759ef9bd281128557571b01f29c0f81b3861d73ebb67f9a5e2c1b
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b9r__r9010
    host_id: kogen-bench-eu
    task_id: r70-4-elixir-fe2-l3b9r
    arm: REPAIR
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 3a63ab1170d7c4384333356f4d220ddc4cb992593d92aab88cc9a0ba9d4a1099
    base_kind: git-commit
    base_revision: 123de8a8f281a2c1ae5bdd07c47a5a90383d249e
    started_at_utc: '2026-10-08T04:10:35.451Z'
    ended_at_utc: '2026-10-08T04:16:29.204Z'
    experiment: l3b-r70-4-elixir-fe2-l3b9r-repair-gpt-6-luna-r9010
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: a3f86394ed10b13f9b189921a89ed493ff886bf035779b2f6db301bc7cafa1b7
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 8e4dc0b5d3a9ef3c56fda83ac42cbd8fc9d41670c63309ae2e24a1564417a31a
    variant_tree_sha256: 3d36b9a632c759ef9bd281128557571b01f29c0f81b3861d73ebb67f9a5e2c1b
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9009
    host_id: kogen-bench-eu
    task_id: r70-4-elixir-fe2
    arm: RESTART
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: e69139b9b22efa380f5ed5bb7b101efa38b7727db3cb3e3db6aba831194cec95
    base_kind: git-commit
    base_revision: 5ccd0bf1e816e2b2f5b2694861f8596402409f52
    started_at_utc: '2026-10-08T04:33:04.574Z'
    ended_at_utc: '2026-10-08T04:37:14.628Z'
    experiment: l3b-r70-4-elixir-fe2-restart-gpt-6-luna-r9009
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 66987807d8831ba74f59aafe08d23690ceb95ae0710db3101c1289e64134ae37
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 6ce3a2075e3bfe837d77734c25c3a0cfd1d403067b857220171da5f0e54d4c14
    variant_application:
      kind: original_base
      reason: RESTART starts from the original task base; no variant tree is applied
      evidence: levers/lanes-2026-10-07/l3b/RELEASE-STATE.json sha256:b6cc877115a567e15caf58834c48f259571ee3c67678e6e53429183ced53d7dd
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9012
    host_id: kogen-bench-eu
    task_id: r70-4-elixir-fe2
    arm: RESTART
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: e69139b9b22efa380f5ed5bb7b101efa38b7727db3cb3e3db6aba831194cec95
    base_kind: git-commit
    base_revision: 5ccd0bf1e816e2b2f5b2694861f8596402409f52
    started_at_utc: '2026-10-08T05:41:14.120Z'
    ended_at_utc: '2026-10-08T05:46:24.775Z'
    experiment: l3b-r70-4-elixir-fe2-restart-gpt-6-luna-r9012
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: d7c96f15c4215b395362495e9c83da05cc813a5528b8078fa245a379eb1d8c16
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 74ad8649656a83a96ff9a029f3d64d0c954a7b4fd77dad58edef187e9c3d6ad1
    variant_application:
      kind: original_base
      reason: RESTART starts from the original task base; no variant tree is applied
      evidence: levers/lanes-2026-10-07/l3b/RELEASE-STATE.json sha256:b6cc877115a567e15caf58834c48f259571ee3c67678e6e53429183ced53d7dd
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9015
    host_id: kogen-bench-eu
    task_id: r70-4-elixir-fe2
    arm: RESTART
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: e69139b9b22efa380f5ed5bb7b101efa38b7727db3cb3e3db6aba831194cec95
    base_kind: git-commit
    base_revision: 5ccd0bf1e816e2b2f5b2694861f8596402409f52
    started_at_utc: '2026-10-08T05:24:31.997Z'
    ended_at_utc: '2026-10-08T05:29:12.139Z'
    experiment: l3b-r70-4-elixir-fe2-restart-gpt-6-luna-r9015
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 27950e3e10af5bdb8a05be779aee68620218537e96de413f8c6f9b9aa46211a0
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 8c732789cb8078feaa9e22d0cf0d0f1afe106bf159127ac32e8a0d0f36ff6f25
    variant_application:
      kind: original_base
      reason: RESTART starts from the original task base; no variant tree is applied
      evidence: levers/lanes-2026-10-07/l3b/RELEASE-STATE.json sha256:b6cc877115a567e15caf58834c48f259571ee3c67678e6e53429183ced53d7dd
  - cell_id: codex__gpt-6-luna__max__default__r70-7-rust-l3b31c__r9026
    host_id: kogen-bench-eu
    task_id: r70-7-rust-l3b31c
    arm: CONTINUE
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: cae2e41f2fe387d688eaa51f850119e5a3d4fc9d461db019fcb1401786526a34
    base_kind: git-commit
    base_revision: ec773802393fe9d7cd19e493a5e749809470cb03
    started_at_utc: '2026-10-08T05:46:26.170Z'
    ended_at_utc: '2026-10-08T05:47:42.188Z'
    experiment: l3b-r70-7-rust-l3b31c-continue-gpt-6-luna-r9026
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: c7a569bda1c7e9d47fb96f79ac47e96865db6774dba6e44ccf0668dfe3057d18
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: e0ac5967efe57c50cee65b3f617630071345fadf2a6d8a4ebe526b85de5c5f1f
    variant_tree_sha256: 73def08cadfc2f6bb0ac4ce2f2a9b0cc784d272545f249579b8188befb9f2c27
  - cell_id: codex__gpt-6-luna__max__default__r70-7-rust-l3b31r__r9025
    host_id: kogen-bench-eu
    task_id: r70-7-rust-l3b31r
    arm: REPAIR
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 88b44d30e889a21d454f716c27716674ff1eb20668c7ab6522f306f21f9c95e3
    base_kind: git-commit
    base_revision: ec773802393fe9d7cd19e493a5e749809470cb03
    started_at_utc: '2026-10-08T05:29:14.085Z'
    ended_at_utc: '2026-10-08T05:33:02.803Z'
    experiment: l3b-r70-7-rust-l3b31r-repair-gpt-6-luna-r9025
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 7886b47e88b518171dfce88785bb30966407f4579263d52a0c024bd84e76b3d3
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: a6dd2d14f5d3f1d9ff49559706e4997c3803dbf299eae9da122c24a12fbcd91d
    variant_tree_sha256: 73def08cadfc2f6bb0ac4ce2f2a9b0cc784d272545f249579b8188befb9f2c27
  - cell_id: codex__gpt-6-luna__max__default__r70-7-rust__r9024
    host_id: kogen-bench-eu
    task_id: r70-7-rust
    arm: RESTART
    model_alias: gpt-6-luna
    effort: max
    prompt_sha256: 27eb953bac3aa7ef6def484742af1b75dccd8c93078edf32240681c58c499d08
    base_kind: git-commit
    base_revision: 111a0c776ae6d93f6e7fccd3fc694d5f4fa26838
    started_at_utc: '2026-10-08T04:56:37.279Z'
    ended_at_utc: '2026-10-08T04:58:26.917Z'
    experiment: l3b-r70-7-rust-restart-gpt-6-luna-r9024
    result_directory: kogen-bench-eu:public-source-location-withheld
    attempt_manifest:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: e88499414f752c52640788fc40430ae5d2441ac06a3f035e333315d21e74f2e4
    completion_receipt:
      path: kogen-bench-eu:public-source-location-withheld
      sha256: 3dcf785180390509d86149e5ef8b705f8d2b60b50323b79bc082e3847cce633b
    variant_application:
      kind: original_base
      reason: RESTART starts from the original task base; no variant tree is applied
      evidence: levers/lanes-2026-10-07/l3b/RELEASE-STATE.json sha256:b6cc877115a567e15caf58834c48f259571ee3c67678e6e53429183ced53d7dd
  cell_environment_evidence:
  - cell_id: codex__gpt-6-luna__max__default__r70-2-elixir-l3b33c__r9005
    task_id: r70-2-elixir-l3b33c
    arm: CONTINUE
    rep: 9005
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 5ca6ad5c8f26f56336224ce83e631a809d0208423a09f58c3e69c8b28bcd2aad
  - cell_id: codex__gpt-6-luna__max__default__r70-2-elixir-l3b33r__r9004
    task_id: r70-2-elixir-l3b33r
    arm: REPAIR
    rep: 9004
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 5ca6ad5c8f26f56336224ce83e631a809d0208423a09f58c3e69c8b28bcd2aad
  - cell_id: codex__gpt-6-luna__max__default__r70-2-elixir__r9003
    task_id: r70-2-elixir
    arm: RESTART
    rep: 9003
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 5ca6ad5c8f26f56336224ce83e631a809d0208423a09f58c3e69c8b28bcd2aad
  - cell_id: codex__gpt-6-luna__max__default__r70-2-go-l3b32c__r9008
    task_id: r70-2-go-l3b32c
    arm: CONTINUE
    rep: 9008
    host_id: kogen-bench-us
    node: kogen-bench-us
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 5ca6ad5c8f26f56336224ce83e631a809d0208423a09f58c3e69c8b28bcd2aad
  - cell_id: codex__gpt-6-luna__max__default__r70-2-go-l3b32r__r9007
    task_id: r70-2-go-l3b32r
    arm: REPAIR
    rep: 9007
    host_id: kogen-bench-us
    node: kogen-bench-us
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 5ca6ad5c8f26f56336224ce83e631a809d0208423a09f58c3e69c8b28bcd2aad
  - cell_id: codex__gpt-6-luna__max__default__r70-2-go__r9006
    task_id: r70-2-go
    arm: RESTART
    rep: 9006
    host_id: kogen-bench-us
    node: kogen-bench-us
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 5ca6ad5c8f26f56336224ce83e631a809d0208423a09f58c3e69c8b28bcd2aad
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b10c__r9014
    task_id: r70-4-elixir-fe2-l3b10c
    arm: CONTINUE
    rep: 9014
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b10r__r9013
    task_id: r70-4-elixir-fe2-l3b10r
    arm: REPAIR
    rep: 9013
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b13c__r9017
    task_id: r70-4-elixir-fe2-l3b13c
    arm: CONTINUE
    rep: 9017
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b13r__r9016
    task_id: r70-4-elixir-fe2-l3b13r
    arm: REPAIR
    rep: 9016
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b9c__r9011
    task_id: r70-4-elixir-fe2-l3b9c
    arm: CONTINUE
    rep: 9011
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2-l3b9r__r9010
    task_id: r70-4-elixir-fe2-l3b9r
    arm: REPAIR
    rep: 9010
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9009
    task_id: r70-4-elixir-fe2
    arm: RESTART
    rep: 9009
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9012
    task_id: r70-4-elixir-fe2
    arm: RESTART
    rep: 9012
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - cell_id: codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9015
    task_id: r70-4-elixir-fe2
    arm: RESTART
    rep: 9015
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - cell_id: codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l3b9c__r9020
    task_id: r70-4-ts-bun-fe2-l3b9c
    arm: CONTINUE
    rep: 9020
    host_id: kogen-bench-us
    node: kogen-bench-us
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - cell_id: codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l3b9r__r9019
    task_id: r70-4-ts-bun-fe2-l3b9r
    arm: REPAIR
    rep: 9019
    host_id: kogen-bench-us
    node: kogen-bench-us
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - cell_id: codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r9018
    task_id: r70-4-ts-bun-fe2
    arm: RESTART
    rep: 9018
    host_id: kogen-bench-us
    node: kogen-bench-us
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - cell_id: codex__gpt-6-luna__max__default__r70-5-go-l3b32c__r9023
    task_id: r70-5-go-l3b32c
    arm: CONTINUE
    rep: 9023
    host_id: kogen-bench-us
    node: kogen-bench-us
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 754d878d4e17209440b1072be9691a5947081c42c40630ca302212f6f053edfc
  - cell_id: codex__gpt-6-luna__max__default__r70-5-go-l3b32r__r9022
    task_id: r70-5-go-l3b32r
    arm: REPAIR
    rep: 9022
    host_id: kogen-bench-us
    node: kogen-bench-us
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 754d878d4e17209440b1072be9691a5947081c42c40630ca302212f6f053edfc
  - cell_id: codex__gpt-6-luna__max__default__r70-5-go__r9021
    task_id: r70-5-go
    arm: RESTART
    rep: 9021
    host_id: kogen-bench-us
    node: kogen-bench-us
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 754d878d4e17209440b1072be9691a5947081c42c40630ca302212f6f053edfc
  - cell_id: codex__gpt-6-luna__max__default__r70-7-rust-l3b31c__r9026
    task_id: r70-7-rust-l3b31c
    arm: CONTINUE
    rep: 9026
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 20f6ee33ae5bbaa003bba6acfb377a71e77680344ea69426a02b08fb0ffbc325
  - cell_id: codex__gpt-6-luna__max__default__r70-7-rust-l3b31r__r9025
    task_id: r70-7-rust-l3b31r
    arm: REPAIR
    rep: 9025
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 20f6ee33ae5bbaa003bba6acfb377a71e77680344ea69426a02b08fb0ffbc325
  - cell_id: codex__gpt-6-luna__max__default__r70-7-rust__r9024
    task_id: r70-7-rust
    arm: RESTART
    rep: 9024
    host_id: kogen-bench-eu
    node: kogen-bench-eu
    platform: Linux-6.8.0-142-generic-x86_64-with-glibc2.39
    kernel: 6.8.0-142-generic
    python: 3.14.7
    concurrency: 1
    grader_sha256: 0c83f2b64678563220f537d4faa73e5869496378041810cc211f0e23589acca3
    suite_sha256: 20f6ee33ae5bbaa003bba6acfb377a71e77680344ea69426a02b08fb0ffbc325
  suite_sha256_by_task:
  - task_id: r70-2-elixir
    suite_sha256: 5ca6ad5c8f26f56336224ce83e631a809d0208423a09f58c3e69c8b28bcd2aad
  - task_id: r70-2-go
    suite_sha256: 5ca6ad5c8f26f56336224ce83e631a809d0208423a09f58c3e69c8b28bcd2aad
  - task_id: r70-4-elixir-fe2
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - task_id: r70-4-ts-bun-fe2
    suite_sha256: 6136eb268b80242b1113d5ca83debeb245be0cb32685fecfd51a304c0fb37148
  - task_id: r70-5-go
    suite_sha256: 754d878d4e17209440b1072be9691a5947081c42c40630ca302212f6f053edfc
  - task_id: r70-7-rust
    suite_sha256: 20f6ee33ae5bbaa003bba6acfb377a71e77680344ea69426a02b08fb0ffbc325
accounting:
  schema: Codex raw/normalized token fields documented in CODEX-ROLLOUTS-2026-10-07.
  collector:
    path: levers/CODEX-ROLLOUTS-2026-10-07.md
    sha256: 019a11ccbccf7384c7574839a11c4d01c517928847c5e0a5aead45f167e1144c
  input_includes_cached: true
  total_formula: uncached input + cached input + output
  reasoning_in_output: Yes, per pilot accounting note; reasoning is included within output.
  cache_write_semantics: The per-cell total formula excludes the separate cache_write counter.
  aggregation: The retained run records report cell-level aggregates.
  interrupted_or_missing_usage: Per-cell manifest receipts define the aggregation boundary; this document does not reconstruct
    per-request totals from cell aggregates.
  cache_share_formula: sum(cached input) / sum(uncached input + cached input), cohort pinned to the recorded run.
  price_basis:
    method: API-equivalent Standard rates; pilot price table dated 2026-10-03.
    calculator:
      path: levers/cost.py
      sha256: bec77e83a8a6def16a4fc85befb53c8751cf443435790108ec83ade400fdf09a
    pilot_receipt:
      path: levers/lanes-2026-10-07/l3b/pilot-run-records.jsonl
      sha256: 92a96ae4227d456fa9da5e67c10f416126aa0d6f04e1721efbad212d59269637
evidence:
  local_files:
  - note: host capture procedure
    path: levers/env-receipts/capture_host_env.sh
    sha256: c22a6778b726c12bcb2402896930369bfb946b5a57a1d52283164e0d820695bc
  - note: host receipt checksum list
    path: levers/env-receipts/SHA256SUMS
    sha256: d57b455ad9d8d1a34f0979f07eda207731118e566b55e9500e4c61216271ee66
  - note: US point-in-time host receipt
    path: levers/env-receipts/host-us-20261008T0551Z.json
    sha256: 581d2b418a8313314a1d6dbdfbbffac9a61ea53f76942ba10b3b9c8a813c4775
  - note: EU point-in-time host receipt
    path: levers/env-receipts/host-eu-20261008T0551Z.json
    sha256: 223bd8e313d918f91ee4525886f6a65b0ea3f6856f9ada394c59f3aebbbb01e1
  - note: frozen round design
    path: levers/lanes-2026-10-07/l3b/DESIGN.md
    sha256: 38acbba12ad264a058592b494cc315b89e3cadd89b65006420a39796dcb5abb3
  - note: round release state and scored-cell count
    path: levers/lanes-2026-10-07/l3b/RELEASE-STATE.json
    sha256: b6cc877115a567e15caf58834c48f259571ee3c67678e6e53429183ced53d7dd
  - note: registered cell/task/arm assignment
    path: levers/lanes-2026-10-07/l3b/cell-plan.json
    sha256: 0bdb4ff9ea51c1ac2750fa1ad71ea7436936603be76096566c378a57bfa7ef48
  - note: pilot model, environment, sandbox, and accounting receipts
    path: levers/lanes-2026-10-07/l3b/pilot-run-records.jsonl
    sha256: 92a96ae4227d456fa9da5e67c10f416126aa0d6f04e1721efbad212d59269637
  - note: official grade-window receipts
    path: levers/lanes-2026-10-07/l3b/windows.jsonl
    sha256: a80b9264723e6db63c66b16282d27ee0434f8048a4658a7f4e4b6845ba817799
  - note: per-cell grader hash and route joins; outcomes omitted
    path: levers/lanes-2026-10-07/l3b/grades.jsonl
    sha256: de29adb99ffcd8dde954ab2aba09bbf5a4a984ef9932ecad777f0ee3fc7bef52
  - note: Codex token-field normalization notes
    path: levers/CODEX-ROLLOUTS-2026-10-07.md
    sha256: 019a11ccbccf7384c7574839a11c4d01c517928847c5e0a5aead45f167e1144c
  - note: pilot API-equivalent cost calculator
    path: levers/cost.py
    sha256: bec77e83a8a6def16a4fc85befb53c8751cf443435790108ec83ade400fdf09a
  - note: public round state and run configuration
    path: ../kogen-bench-sot/rounds/l3b-repair-vs-continue/README.md
    sha256: e97a15b565edef1409e8a45ebeab584f829a3f38103224e5b5edefcc45bbf233
  - note: joined per-cell public execution receipt index
    path: levers/env-receipts/l3b-execution-index.json
    sha256: c0849cef7d9a28b20ce53d6970315c14a278fca5518cb260e77b3698f57ce9c4
gaps:
- field: environments[*].host.allocation
  reason: Capture reports 1 physical and 2 logical CPUs, but cgroup_root_cpu_max was not available, so a quota or scheduler
    allocation cannot be stated.
  recoverability: partial
  evidence: host-us and host-eu receipts listed in evidence.local_files
- field: client.binary_sha256, wrapper_sha256 historical binding, and source_commit
  reason: The native Codex hash is attested by the 05:51Z host capture, after the L3b cells; per-cell records attest version
    0.160.0 but do not bind that native hash or a source commit to each earlier run.
  recoverability: partial
  evidence: host receipt hashes and per-cell remote manifest hashes in l3b-execution-index.json
- field: client.model_revision
  reason: Run receipts identify the gpt-6-luna alias and max effort, not an immutable provider model revision.
  recoverability: unresolved
  evidence: per-cell manifest receipts in l3b-execution-index.json
- field: sandbox per-cell config, network-policy hash, and mount/tool inventory hash
  reason: Pilot records retain a bwrap profile hash, but the allowed per-cell receipts do not establish those hashes for every
    bulk execution.
  recoverability: partial
  evidence: pilot-run-records.jsonl sha256:92a96ae4227d456fa9da5e67c10f416126aa0d6f04e1721efbad212d59269637 and remote per-cell
    manifests
- field: accounting.cache_write, request-level missing usage, and filesystem cache policy
  reason: Retained accounting notes lack per-request long-context counters and do not establish cache-write coverage or a
    per-cell cold/warm filesystem-cache policy.
  recoverability: partial
  evidence: CODEX-ROLLOUTS-2026-10-07.md and pilot-run-records.jsonl SHA-256 citations above
```
