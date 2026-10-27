"""`lanes-ccdry`: run exactly one cell of a Claude Code experiment on a host, then check the executor ran.

The cell is the first unfinished cell of a lane that uses the claude-code executor. After it, Kogen's run log (kept
in the cell's `run-log/`) must show the executor's events; a fall back to a native provider or an executor that never
started fails the check (exit 1). Run it once per host before any measured run.
"""

import argparse
import glob
import os
import sys

from . import ccroute, common, dispatch, experiment


def finished_cells(run_dir):
    cells = os.path.join(run_dir, "cells")
    return {os.path.relpath(os.path.dirname(p), cells).replace(os.sep, "/")
            for p in glob.glob(os.path.join(cells, "*", "r*", "*", "result.json"))}


def main(argv=None):
    p = argparse.ArgumentParser(description="Run one cell of a claude-code experiment on one host; check the executor ran.")
    p.add_argument("run_dir")
    p.add_argument("--tasks", default=os.environ.get("KOGEN_LANES_TASKS"), help="private tasks folder")
    p.add_argument("--hosts", required=True, help="hosts file (JSON)")
    p.add_argument("--host", required=True, help="the host to dry-run on")
    p.add_argument("--lock-cmd")
    p.add_argument("--unlock-cmd")
    p.add_argument("--skip-preflight", action="store_true", help="for tests only")
    p.add_argument("--lanes-dir", default=dispatch.LANES_DIR, help=argparse.SUPPRESS)
    a = p.parse_args(argv)
    if not a.tasks:
        p.error("--tasks or KOGEN_LANES_TASKS is required")
    run_dir = os.path.abspath(a.run_dir)
    try:
        exp = experiment.load(os.path.join(run_dir, "experiment.json"))
        if not ccroute.uses_claude_code(exp):
            print("ccdry: no lane of this experiment uses the claude-code executor", file=sys.stderr)
            return 2
        before = finished_cells(run_dir)
        code = dispatch.run_all(run_dir, a.tasks, a.hosts, a.lock_cmd, a.unlock_cmd, lanes_dir=a.lanes_dir, skip_preflight=a.skip_preflight,
                                only_host=a.host, max_cells=1, claude_code_only=True,
                                log=lambda m: print(m, file=sys.stderr))
    except (experiment.ExperimentError, dispatch.DispatchError, OSError, ValueError) as e:
        print(f"ccdry: {e}", file=sys.stderr)
        return 2
    new = sorted(finished_cells(run_dir) - before)
    if len(new) != 1:
        print(f"ccdry: FAILED: the cell did not finish (run exit {code})", file=sys.stderr)
        return 1
    ok, message = ccroute.check_run_log(common.cell_dir(run_dir, new[0]))
    print(f"ccdry: {'ok' if ok else 'FAILED'}: {new[0]} on {a.host}: {message}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
