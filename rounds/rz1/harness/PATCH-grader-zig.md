# Proposed Zig grader inventory patch

This is a proposal only; no shared grader file was changed.

`grade_worker.py` has one result inventory glob: `rec-lever-r70-*/*/*/COMPLETE.json`.
Add `rec-lever-rz1-eu-*/*/*/COMPLETE.json` so the MacBook window inventory sees
RZ1 cells, and recognize `zig` as a stack prefix when a task has a lane suffix.
The worker then reads the standard manifest and patch artifact and runs its
existing `setup.sh`, `make build`, `make check`, and registered hidden-test
route; it does not filter project files by language extension.

`grade_window.py` has no separate result inventory glob: its `inventory()`
calls the host `grade_worker.py inventory`. Its public-reference `rsync` staging
does need cache exclusions for `.zig-cache` and `zig-out`. `build.zig`,
`*.zig`, and `build.zig.zon` remain copied by the normal recursive staging and
are retained in contestant patch artifacts. The patch does not add an extension
include glob, which would risk dropping valid Zig inputs.

This proposal assumes the task `setup.sh` and Makefile provide the offline Zig
build/check commands with the pinned toolchain on `PATH`. It makes no change to
the protected runner, sandbox, dispatch or grade-window files on any host.
