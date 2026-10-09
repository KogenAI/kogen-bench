# RZ1 EU environment record (draft)

```yaml
schema: benchmark-environment/1
round: rz1
scope:
  status: build-only; not release eligible
  host_id: kogen-bench-eu
  host_capture: ubuntu-8gb-nbg1-1
  captured_at_utc: '2026-10-08T13:42:58Z'
  plan: levers/rz1/PLAN.provisional.json
  plan_sha256: 15728e3ca69205060c221757648e52c4f25edad26d34fd53920f8a79bf43f649
  host_receipt:
    path: levers/rz1/gate/host-env.json
    sha256: f5d5884d35b754920ac0a64f1c2b9cda592e94921407107aa61aff564044039f
host:
  cpu_model: AMD EPYC-Milan Processor
  logical_cores: 2
  ram_bytes: 8123707392
  os_name_version: Ubuntu 24.04.5 LTS
  kernel: '6.8.0-142-generic #142-Ubuntu SMP PREEMPT_DYNAMIC Wed Sep 2 14:24:27 UTC 2026'
aliases:
  codex:
    path: public-source-location-withheld
    version: codex-cli 0.161.0
    binary_path: public-source-location-withheld
    binary_sha256: 9a820c17865fa825d04db416818679a9d63bd72e50835c396f496e5684626c9c
    wrapper_sha256: 08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300
  rust:
    path: public-source-location-withheld
    version: 1.97.1
  zig:
    path: public-source-location-withheld
    version: 0.17.0
  python:
    path: /opt/bench/mise/installs/python/3.14.7/bin/python3
    version: Python 3.14.7
  bwrap:
    path: /usr/bin/bwrap
    version: bubblewrap 0.9.0
client:
  model_alias: gpt-6-luna
  effort: max
  version_receipt: levers/rz1/gate/settings.json
  codex_home: public-source-location-withheld
sandbox:
  kind: Linux bubblewrap
  egress: chatgpt.com only; auth.openai.com blocked by design
  isolation_receipt: levers/rz1/gate/isolation.json
grader:
  route: MacBook poll.py / documented R70 grade-window controls
  proposed_patch: levers/rz1/PATCH-grader-zig.diff
  official_smoke_grades: none in this build-only job
gaps:
  - EU Zig task directories 1–8 are staged; parity reports and JSON for tasks 2 and 7 exist only in the local worktree, none are staged on EU, and the admitted set remains an operator decision.
  - Existing shared config.toml is mode 0600 and unreadable to the EU login; it was not copied.
  - Dummy isolation confirms the current profile exposes its own harness home to a command; see isolation receipt.
  - Reference/no-op controls and one officially graded real smoke per arm remain required before bulk release.
```

The host capture script's legacy default Codex pin reports 0.160.0. RZ1 uses
the lane-local wrapper/config and separately verified binary pin 0.161.0 above.
