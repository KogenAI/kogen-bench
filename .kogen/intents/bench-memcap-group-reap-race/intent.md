# Wait for a reaped process group to disappear

Slug: bench-memcap-group-reap-race
Model: not applicable — the change is one bounded polling loop in a helper function with no persistent or interacting state
Acceptance:
- .kogen/intents/bench-memcap-group-reap-race/acceptance.feature
- features/steps/bench-memcap-group-reap-race__steps.js
- features/steps/bench-memcap-group-reap-race__driver/probe.py

The hourly bench-fresh qualification is red because `tests.test_memcap.FaultTest.test_cgroup` fails (assertion `6 != 0`, log "process custody unknown; claim retained"). The cell was killed correctly by the cgroup v2 memory limit, but `_require_group_gone` in `lanes/lanes/common.py` probes the process group once with `os.killpg(pgid, 0)` right after the leader was reaped. With `memory.oom.group` the other members of the cell cgroup are still tearing down for a short time, so the single probe sees a live group and the run is marked custody unknown.

The change: `_require_group_gone(pgid)` keeps probing with signal 0, without ever sending a signal, until the group disappears or a bounded wait ends. The bound is the named module constant `GROUP_GONE_TIMEOUT_S = 5.0` (5 seconds) in `lanes/lanes/common.py`, polled every 50 milliseconds, i.e. the named constant `GROUP_GONE_POLL_S = 0.05` seconds; the function reads `GROUP_GONE_TIMEOUT_S` when it is called, so a test can patch the module attribute small. The group disappearing (ProcessLookupError) returns at once. A group still present when the bound ends raises `CustodyUnknown('process group still exists after leader exit')` exactly as today. A `PermissionError` from the probe raises the same `CustodyUnknown` immediately, without waiting. `_kill_group`, its callers and every other signalling path are unchanged, and a surviving group is never treated as gone.

`lanes/tests/test_memcap.py` is not modified: no skip, no relaxed assertion, no larger cap, both delegated and non-delegated branches kept. Whether `test_cgroup` passes inside a delegated cgroup is checked after landing by the hourly bench-fresh run (reproduction: `systemd-run --user --wait -P -p OOMPolicy=continue python3 -m unittest tests.test_memcap`; `OOMPolicy=continue` is an environment setting of the bench-fresh unit and is not part of this change), not by a scenario here. Focused model-free tests of the helper are added in `lanes/tests/test_group_gone.py`. No published round is updated.

## Decisions
- The bound is the module constant `GROUP_GONE_TIMEOUT_S = 5.0` (5 seconds) and the poll interval, 50 milliseconds, the constant `GROUP_GONE_POLL_S = 0.05` (seconds); neither is a setting, flag or environment variable. (evidence: lanes/lanes/common.py) (source: request)
- The wait uses repeated `os.killpg(pgid, 0)` probes only; no signal is sent during the wait and `_kill_group` is untouched. (evidence: lanes/lanes/common.py; lanes/tests/test_process_custody.py) (source: request)
- PermissionError raises CustodyUnknown immediately, and a group still present at the bound raises CustodyUnknown with the existing message. (evidence: lanes/lanes/common.py) (source: request)
- `lanes/tests/test_memcap.py` stays byte-identical; the acceptance scenario checks its SHA-256 literal from main and the presence of both test branches, because the delegated-cgroup outcome can only be observed by the bench-fresh run. (evidence: lanes/tests/test_memcap.py) (source: request)
- The helper tests go in a new file `lanes/tests/test_group_gone.py` so they run under the existing `sh lanes/test.sh` discovery. (evidence: lanes/test.sh; lanes/tests/test_process_custody.py) (source: request)
- Acceptance drives the real function through `features/steps/bench-memcap-group-reap-race__driver/probe.py`, which starts a real process group whose leader exits 0 and is reaped while a `sleep` member remains, and reports whether `CustodyUnknown` was raised, the elapsed time and the non-zero signals sent. (assumption: the acceptance sandbox lets an orphaned group member be reaped by init or a subreaper, so a short-lived member leaves the group promptly) (source: request)
- Bound is module constant GROUP_GONE_TIMEOUT_S=5.0, poll GROUP_GONE_POLL_S=0.05, read at call time; no setting/flag/env (decision: D1, round 1) (constraint: no signal during wait) (constraint: PermissionError raises immediately) (evidence: lanes/lanes/common.py) (source: request)
- Wait uses signal-0 probes only; _kill_group unchanged (decision: D2, round 1) (evidence: lanes/lanes/common.py; lanes/tests/test_process_custody.py) (source: request)
- PermissionError or surviving group at the bound raises CustodyUnknown as today (decision: D3, round 1) (evidence: lanes/lanes/common.py) (source: request)
- test_memcap.py stays byte-identical, checked by SHA-256 literal in acceptance (decision: D4, round 1) (evidence: lanes/tests/test_memcap.py) (source: request)
- Helper tests in new lanes/tests/test_group_gone.py under existing discovery (decision: D5, round 1) (evidence: lanes/test.sh; lanes/tests/test_process_custody.py) (source: request)
- Acceptance drives real function with a real process group via a Python driver (decision: D6, round 1) (assumption: Acceptance sandbox must reap orphaned group members promptly (init or subreaper); observed working in this checkout's scratch probe only) (source: request)

## Source comparison
- Bound 5 seconds, poll every 50 milliseconds (`GROUP_GONE_POLL_S = 0.05`): carried by the constants in D1.
- Group member exits 0.5 s after the reaped leader: addressed by scenario 1 (must return without CustodyUnknown); the original single probe raises here.
- Member alive after the bound (bound shortened to 0.3 s): addressed by scenario 2 (must raise CustodyUnknown after waiting at least the bound).
- PermissionError from the probe: addressed by scenario 3 (CustodyUnknown, under 1 second with the default 5 s bound).
- No signal while waiting: addressed by scenario 4 (no signal other than the zero probe reaches `os.killpg` or `_killpg`).
- test_memcap.py unchanged: addressed by scenario 5 (SHA-256 `80dd33f33ebef34548b662e7957ab9e2da3d628c14e436fdf1c65fb30b1f2e38` of the file on main, both `test_watchdog` and `test_cgroup` present).
- Whole lanes suite (`sh lanes/test.sh`), `reproduce/validate_repo.py`, the leak check: existing checks that must keep passing; not changed.
- Delegated-cgroup pass of test_cgroup and the 6 != 0 symptom: verified after landing by the hourly bench-fresh run, not by a scenario.

## Tests
- A group whose last member exits shortly after the leader is reaped returns without CustodyUnknown: `GroupGone.test_waits_for_a_member_that_exits_after_the_leader` in lanes/tests/test_group_gone.py (unit)
- A group that outlives the bound raises CustodyUnknown (bound patched small, no signal sent): `GroupGone.test_group_that_outlives_the_bound_is_custody_unknown` in lanes/tests/test_group_gone.py (unit)
- PermissionError raises CustodyUnknown without sleeping: `GroupGone.test_permission_error_does_not_wait` in lanes/tests/test_group_gone.py (unit)
- A group that is already gone returns without sleeping: `GroupGone.test_gone_group_returns_at_once` in lanes/tests/test_group_gone.py (unit)
- The wait, the bound, PermissionError and the no-signal rule on a real process group: all five scenarios in acceptance.feature (scenario)
- Existing custody and memory-cap behavior is unchanged: lanes/tests/test_process_custody.py and lanes/tests/test_memcap.py (existing)

## Feasibility
- none
