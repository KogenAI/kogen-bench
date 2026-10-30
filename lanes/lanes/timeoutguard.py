"""Stop relaunching a task that keeps hitting the cell deadline (cap8: one task timed out 10 times, each in a new experiment).

Timeouts are counted per (study, task, tool, Kogen sha) in a ledger shared by every experiment on the host
(`LANES_TIMEOUT_LEDGER`; unset: the guard is off). At LIMIT timeouts dispatch starts no further cell of that task: it is
deferred, never dropped. The cells stay in plan.jsonl, PLAN.json records `timeout_deferrals`, and the report shows an
infrastructure gap "deferred: 2 timeouts". The deadline is never changed. A file `<ledger>/override/<key name>` clears
the key: only timeouts after its mtime count again.
"""

import datetime
import fcntl
import json
import os
import re

from . import common

LIMIT = 2
REASON = f"deferred: {LIMIT} timeouts"
SUFFIX = re.compile(r"-[a-z]{1,2}\d*$")  # host/replicate suffix: long-fix-sol-u2, -e3, -s3, -l1, -mb


def ledger():
    return os.environ.get("LANES_TIMEOUT_LEDGER") or None


def study_of(exp):
    return exp.get("study") or SUFFIX.sub("", exp["id"])


def tool_of(lane):
    models = sorted(set((lane.get("settings") or {}).get("models", {}).values()))
    return "+".join(models) or "default"


def key(exp, lane, task):
    return (study_of(exp), task, tool_of(lane), lane["sha"])


def key_name(k):
    return "__".join([re.sub(r"[^A-Za-z0-9._+-]", "_", k[0]), re.sub(r"[^A-Za-z0-9._+-]", "_", k[1]),
                      re.sub(r"[^A-Za-z0-9._+-]", "_", k[2]), k[3][:12]])


def _rows(root):
    return common.read_jsonl(os.path.join(root, "timeouts.jsonl")) if os.path.isfile(os.path.join(root, "timeouts.jsonl")) else []


def _cleared(root, k):
    p = os.path.join(root, "override", key_name(k))
    return os.path.getmtime(p) if os.path.isfile(p) else 0.0


def _utc(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def count(k, root=None):
    root = root or ledger()
    if not root:
        return 0
    since = _cleared(root, k)
    seen = {(r["experiment"], r["cell"]) for r in _rows(root)
            if (r["study"], r["task"], r["tool"], r["sha"]) == k and _utc(r["utc"]) > since}
    return len(seen)


def record(exp, lane, cell, run_dir):
    """Add one timed-out cell to the ledger (idempotent per experiment and cell)."""
    root = ledger()
    if not root:
        return
    task = cell.split("/")[0]
    k = key(exp, lane, task)
    os.makedirs(root, exist_ok=True)
    with open(os.path.join(root, ".lock"), "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if any(r["experiment"] == exp["id"] and r["cell"] == cell for r in _rows(root)):
            return
        row = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "experiment": exp["id"], "cell": cell,
               "study": k[0], "task": k[1], "tool": k[2], "sha": k[3], "run_dir": os.path.abspath(run_dir)}
        with open(os.path.join(root, "timeouts.jsonl"), "a") as f:
            f.write(json.dumps(row) + "\n")
        _publish(root)


def ingest(exp, run_dir, cells):
    """Count the timeouts already in this run's results (a resumed run, or a cell whose process was killed)."""
    for c in cells:
        p = os.path.join(common.cell_dir(run_dir, c["cell"]), "result.json")
        try:
            outcome = common.read_json(p).get("outcome") if os.path.isfile(p) else None
        except (OSError, ValueError):
            continue
        if isinstance(outcome, str) and outcome.startswith("timeout"):
            lane = next(l for l in exp["lanes"] if l["name"] == c["lane"])
            record(exp, lane, c["cell"], run_dir)


def deferred(exp, run_dir, cells):
    """{task: info} of the tasks with an unfinished cell whose key has LIMIT timeouts."""
    root = ledger()
    out = {}
    if not root:
        return out
    lanes = {l["name"]: l for l in exp["lanes"]}
    for c in cells:
        if c["task"] in out:
            continue
        k = key(exp, lanes[c["lane"]], c["task"])
        n = count(k, root)
        if n >= LIMIT:
            out[c["task"]] = {"reason": REASON, "timeouts": n, "study": k[0], "tool": k[2], "sha": k[3],
                              "override": os.path.join(root, "override", key_name(k))}
    return out


def note(run_dir, found):
    """Keep the deferrals in PLAN.json (report and alarms read them there)."""
    path = os.path.join(run_dir, "PLAN.json")
    plan = common.read_json(path) if os.path.isfile(path) else {}
    cur = plan.setdefault("timeout_deferrals", {})
    for t, info in found.items():
        if t not in cur:
            cur[t] = dict(info, utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    for t in [t for t in cur if t not in found]:
        del cur[t]  # cleared by an override
    common.write_json(path, plan)
    root = ledger()
    if root:
        _publish(root)


def gaps(run_dir):
    path = os.path.join(run_dir, "PLAN.json")
    d = common.read_json(path).get("timeout_deferrals", {}) if os.path.isfile(path) else {}
    return [{"task": t, "reason": r["reason"], "state": "deferred", "timeouts": r["timeouts"], "study": r["study"],
             "tool": r["tool"], "sha": r["sha"], "override": r["override"]} for t, r in sorted(d.items())]


def _publish(root):
    """DEFERRED.tsv: one line per deferred key, for fleet alarms (rewritten from the ledger each time)."""
    keys = {}
    for r in _rows(root):
        keys.setdefault((r["study"], r["task"], r["tool"], r["sha"]), 0)
    lines = []
    for k in sorted(keys):
        n = count(k, root)
        if n >= LIMIT:
            lines.append("\t".join([k[0], k[1], k[2], k[3], str(n), REASON]))
    os.makedirs(root, exist_ok=True)
    p = os.path.join(root, "DEFERRED.tsv")
    with open(p + ".tmp", "w") as f:
        f.write("".join(l + "\n" for l in lines))
    os.replace(p + ".tmp", p)
