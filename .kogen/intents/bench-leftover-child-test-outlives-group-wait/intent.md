# Fix leftover child test to outlive the group wait

Slug: bench-leftover-child-test-outlives-group-wait
Model: not applicable — the change edits one test method and has no persistent or interacting state
Acceptance:
- .kogen/intents/bench-leftover-child-test-outlives-group-wait/acceptance.feature
- features/steps/bench-leftover-child-test-outlives-group-wait__steps.js
- features/steps/bench-leftover-child-test-outlives-group-wait__driver/observe.py

The hourly bench-fresh qualification is red because the test method `test_leftover_child_is_unknown_without_post_reap_signal` in class `Run` of `lanes/tests/test_common.py` fails with "CustodyUnknown not raised" (run 20261118T122036Z on 743daf18: 839 passed, 1 failed, 10 skipped; reproduced 3 of 3 by an external reviewer). The test starts a child that spawns an independent grandchild sleeping one second while the child exits at once. Since 743daf18, `_require_group_gone` in `lanes/lanes/common.py` waits without signalling for up to `GROUP_GONE_TIMEOUT_S` (5 seconds, polled every 0.05 seconds) for the process group to disappear, so the one second grandchild now exits inside the wait and nothing is raised. That production behaviour is correct and does not change: a group that is gone within the bound is not lost custody. Only the test's leftover process no longer outlives the bound.

The change edits only that one test method in `lanes/tests/test_common.py`. For the duration of the test it patches the module constant `common.GROUP_GONE_TIMEOUT_S` to 0.3 seconds with `unittest.mock.patch.object`, and the grandchild sleeps for 3 seconds so that it outlives the shortened bound. Every other assertion stays: `common.CustodyUnknown` is raised by `common.run`, the recorded grandchild pid is still alive immediately after the raise (nothing signalled it), and the grandchild exits on its own afterwards; the polling loop is extended to wait up to 6 seconds for that exit. `lanes/lanes/common.py`, `lanes/tests/test_memcap.py` and every other file are not edited. The test is not skipped, relaxed or deleted, and the constant is not raised. Nothing is replaced or removed beyond the old one second sleep and the old 3 second polling loop of that method.

## Decisions
- The patch of `GROUP_GONE_TIMEOUT_S` is 0.3 seconds, applied with `unittest.mock.patch.object(common, "GROUP_GONE_TIMEOUT_S", 0.3)` around the `common.run` call, imported inside the test method so no other part of the file changes; it is a fixed constant in the test, not a setting. (decision: D1, round 1) (evidence: lanes/lanes/common.py; lanes/tests/test_common.py) (source: request)
- The grandchild sleeps 3 seconds and the polling loop for its natural exit allows up to 6 seconds (60 polls of 0.1 seconds), keeping the existing assertions that the pid is alive right after the raise and gone at the end. (decision: D2, round 1) (evidence: lanes/tests/test_common.py) (source: request)
- Production code and `lanes/tests/test_memcap.py` stay byte-identical; acceptance compares their SHA-256 values from the base tree (`lanes/lanes/common.py` 158b6b58fd960f8cdc4d02ed7bc74fcab000eeac026b9bc0be2e62d29678b39e, `lanes/tests/test_memcap.py` 80dd33f33ebef34548b662e7957ab9e2da3d628c14e436fdf1c65fb30b1f2e38) and, when the checkout is a Git work tree, that no file other than test_common.py changed outside the Intent's own files. (decision: D3, round 1) (evidence: lanes/lanes/common.py) (source: request)
- Acceptance has exactly three scenarios and each of them runs the single test method at most once: the first runs `python3 -m unittest` from the `lanes` directory on that one test id, the second runs the same test once in an in-process observer that records non-zero signals and how long the leftover process group lives after the raise, the third reads file bytes and the Git change list. No whole-suite or validate run is inside a scenario; those belong to the build gates. (decision: D4, round 1) (evidence: lanes/tests/test_common.py) (source: request)
- The observer in `observe.py` wraps `common._require_group_gone` only to record, never to change, its behaviour, and wraps `os.kill` and `os.killpg` only to record non-zero signals. (decision: D5, round 1) (assumption: the acceptance environment has a Git work tree or tolerates its absence, and its Python 3 can run the lanes tests; observed only in this checkout's scratch copy) (source: request)

## Source comparison
- Failing test `test_leftover_child_is_unknown_without_post_reap_signal` with "CustodyUnknown not raised": addressed by scenario 1, which fails on the unchanged tree and passes alone with a plain OK line, one test and no skip.
- Grandchild alive right after the raise and exiting by itself within 6 seconds, never signalled, with the bound patched to 0.3 seconds: addressed by scenario 2 through the observer; on the unchanged tree nothing is raised.
- Production code unchanged, test_memcap.py unchanged, only test_common.py changed: addressed by scenario 3, which also holds on the unchanged tree.
- Not skipping, relaxing, deleting the test or raising the constant: carried by scenarios 1 and 2 (raise, bound 0.3, no skip) and by scenario 3.
- Whole lanes suite and validate-repo: existing build gates, not changed and not run inside scenarios.

## Tests
- A leftover grandchild that outlives a shortened group wait bound leaves custody unknown, stays alive after the raise and exits on its own without a signal: update the existing test_leftover_child_is_unknown_without_post_reap_signal in lanes/tests/test_common.py (regression)

## Feasibility
- none
