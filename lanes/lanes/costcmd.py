"""`lanes-cost recompute <run-dir>`: reprice a run's finished cells from their stored logs.

Rewrites only the cost fields of each `result.json` (`cost_usd`, `cost_reason`, `models`, `model_sources` of
its stages and totals) with the current usage parser and price table; the old values go to
`cost-backup.json` in the cell dir (kept from the first recompute). Finished cells are never rerun or removed.
"""

import argparse
import glob
import json
import os
import sys
import time

from . import common, costguard, experiment, usage

FIELDS = ("cost_usd", "cost_reason", "models", "model_sources")
BACKUP = "cost-backup.json"


def _logs(cell_dir):
    events = usage.read_log(os.path.join(cell_dir, "run-log", "log.jsonl"))
    shaping = usage.read_log(os.path.join(cell_dir, "shaping-events.ndjson"))
    return events, shaping


def recompute_cell(cell_dir):
    """Reprice one finished cell dir. Returns `(old_usd, new_usd)`, or None when it has no stored log."""
    path = os.path.join(cell_dir, "result.json")
    result = common.read_json(path)
    events, shaping = _logs(cell_dir)
    if events is None and shaping is None:
        return None
    commands = [{"stage": s["stage"], "started": s.get("started"), "ended": s.get("ended"), "wall_s": s.get("wall_s"),
                 "exit_code": s.get("exit_code"), "timed_out": s.get("outcome") == "timeout"}
                for s in result.get("stages", []) if s["stage"] in usage.STAGES]
    new = usage.parse_run_log(events, commands, shape_events=shaping)
    fresh = {s["stage"]: s for s in new["stages"]}
    backup = os.path.join(cell_dir, BACKUP)
    if not os.path.exists(backup):
        common.write_json(backup, {"recomputed": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                   "stages": {s["stage"]: {k: s.get(k) for k in FIELDS} for s in result["stages"]},
                                   "totals": {k: result["totals"].get(k) for k in FIELDS}})
    for s in result["stages"]:
        if s["stage"] in fresh:
            s.update({k: fresh[s["stage"]][k] for k in FIELDS})
    result["totals"].update({k: new["totals"][k] for k in FIELDS})
    common.write_json(path, result)
    return (json.load(open(backup))["totals"]["cost_usd"], result["totals"]["cost_usd"])


def recompute(run_dir, out=print):
    """Recompute the run dir; returns a summary dict. Raises ValueError when a cell is running."""
    run_dir = os.path.abspath(run_dir)
    exp = experiment.load(os.path.join(run_dir, "experiment.json"))
    if glob.glob(os.path.join(run_dir, "cells", "*", "r*", "*", costguard.LIVE)):
        raise ValueError("a cell is running (live.json in its cell dir); stop the run first")
    before = costguard.provider_spend(run_dir, exp)
    done, no_log = 0, []
    with costguard.locked(run_dir):  # the spend readers wait while the cost fields change
        for path in sorted(glob.glob(os.path.join(run_dir, "cells", "*", "r*", "*", "result.json"))):
            cell_dir = os.path.dirname(path)
            if recompute_cell(cell_dir) is None:
                no_log.append(os.path.relpath(cell_dir, os.path.join(run_dir, "cells")))
            else:
                done += 1
    ledger = os.path.join(run_dir, costguard.LEDGER)
    kept = len(common.read_jsonl(ledger)) if os.path.isfile(ledger) else 0  # a retired attempt keeps no logs
    spent_only = sorted(os.path.relpath(os.path.dirname(p), os.path.join(run_dir, "cells")) for p in
                        glob.glob(os.path.join(run_dir, "cells", "*", "r*", "*", costguard.SPENT)))
    after = costguard.provider_spend(run_dir, exp)
    stop = os.path.join(run_dir, costguard.STOP)
    removed = False
    if os.path.isfile(stop) and not any(after.get(p, 0.0) >= soft for p, (soft, _) in costguard.usd_caps(exp).items()):
        os.remove(stop)
        removed = True
    summary = {"cells_recomputed": done, "cells_without_stored_log": no_log, "ledger_kept_recorded": kept, "cells_kept_spent_json": spent_only, "spend_before_usd": before, "spend_after_usd": after,
               "stop_marker_removed": removed}
    out(json.dumps(summary, indent=2, sort_keys=True))
    if no_log:
        out(f"kept the recorded cost of {len(no_log)} cell(s) with no stored log")
    if kept:
        out(f"kept the recorded value of {kept} ledger line(s): a retired attempt's logs are not stored")
    if spent_only:
        out(f"kept the recorded spend (spent.json) of {len(spent_only)} cell(s) that stopped without a result.json")
    return summary


def main(argv=None):
    p = argparse.ArgumentParser(prog="lanes-cost", description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    r = sub.add_parser("recompute", help="reprice finished cells from their stored logs")
    r.add_argument("run_dir")
    a = p.parse_args(argv)
    try:
        recompute(a.run_dir)
    except (ValueError, OSError, experiment.ExperimentError) as e:
        print(f"lanes-cost: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
