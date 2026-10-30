"""Carry approval debt to a later queued unit, always resuming the original experiment."""

import argparse
import fcntl
import os
import subprocess

from . import approval, common


def enqueue(root, run_dir, tasks, kind, slots, estimate):
    exp_id = common.read_json(os.path.join(run_dir, "experiment.json"))["id"]
    common.write_json(os.path.join(root, exp_id + ".json"),
                      {"experiment": exp_id, "run_dir": os.path.abspath(run_dir), "tasks": os.path.abspath(tasks),
                       "kind": kind, "slots": slots, "estimate": estimate})


def drain(root, entry, exclude, out=print):
    os.makedirs(root, exist_ok=True)
    with open(os.path.join(root, ".lock"), "a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return
        # Snapshot once: a still-timed-out task can only be retried in another unit.
        for name in sorted(os.listdir(root)):
            if not name.endswith(".json"):
                continue
            path = os.path.join(root, name)
            row = common.read_json(path)
            if row["experiment"] == exclude:
                continue
            if not approval.gaps(row["run_dir"]):
                os.unlink(path)
                continue
            if not approval.pending(row["run_dir"]):
                out(f"carry: {row['experiment']} has a real refusal; retained for repair", flush=True)
                continue
            out(f"carry: resume {row['experiment']} with its original plan", flush=True)
            subprocess.run(["/bin/bash", entry, row["kind"], row["experiment"], row["tasks"],
                            str(row["slots"]), str(row["estimate"])],
                           env={**os.environ, "LANES_CARRY_ACTIVE": "1"}, check=False)
            if not approval.gaps(row["run_dir"]):
                os.unlink(path)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    e = sub.add_parser("enqueue")
    e.add_argument("root")
    e.add_argument("run_dir")
    e.add_argument("tasks")
    e.add_argument("kind", choices=("cgr", "ccr"))
    e.add_argument("slots", type=int)
    e.add_argument("estimate")
    d = sub.add_parser("drain")
    d.add_argument("root")
    d.add_argument("entry")
    d.add_argument("exclude")
    pending = sub.add_parser("pending")
    pending.add_argument("run_dir")
    a = vars(p.parse_args(argv))
    command = a.pop("command")
    if command == "pending":
        return 0 if approval.pending(a["run_dir"]) else 1
    (enqueue if command == "enqueue" else drain)(**a)
    return 0
