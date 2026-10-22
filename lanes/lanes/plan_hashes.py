"""Hashes of every input of a round, and the `PLAN.json` written before any cell runs."""

import argparse
import hashlib
import json
import os
import sys

from . import common, experiment


def sha256_json(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class PlanError(ValueError):
    pass


def task_hashes(task_dir, phase="build", intent_form=None):
    """sha256 of a task: the whole folder, its start tree, hidden tests, brief, each supplied Intent.

    `start/` and `evaluator/` must exist; `request.md` only for the phases that shape (shape, e2e,
    else null if absent); `supplied/<intent_form>/` when a build or e2e experiment names a form.
    """
    name = os.path.basename(os.path.normpath(task_dir))
    for sub in ("", "start", "evaluator"):
        if not os.path.isdir(os.path.join(task_dir, sub)):
            raise PlanError(f"task {name}: missing folder {sub or task_dir}")
    supplied = os.path.join(task_dir, "supplied")
    forms = sorted(os.listdir(supplied)) if os.path.isdir(supplied) else []
    if phase in ("build", "e2e") and intent_form and intent_form not in forms:
        raise PlanError(f"task {name}: no supplied/{intent_form}/ for intent_form {intent_form}")
    request = os.path.join(task_dir, "request.md")
    if phase in ("shape", "e2e") and not os.path.isfile(request):
        raise PlanError(f"task {name}: missing request.md (phase {phase})")
    task_toml = os.path.join(task_dir, "task.toml")
    return {"task": common.sha256_tree(task_dir),
            "tree": common.sha256_tree(os.path.join(task_dir, "start")),
            "hidden_tests": common.sha256_tree(os.path.join(task_dir, "evaluator")),
            "task_toml": common.sha256_file(task_toml) if os.path.isfile(task_toml) else None,
            "request": common.sha256_file(request) if os.path.isfile(request) else None,
            "intents": {f: common.sha256_tree(os.path.join(supplied, f)) for f in forms}}


def lane_hashes(exp, exp_path):
    out = {}
    for lane in exp["lanes"]:
        patch = experiment.patch_path(exp_path, lane)
        out[lane["name"]] = {"patch": common.sha256_file(patch) if patch else None,
                             "settings": sha256_json(lane["settings"])}
    return out


def read_lock(lock_path, exp):
    """`{lane: artifact_sha256}` from lanes.lock.json; PlanError names the bad field."""
    lock = common.read_json(lock_path)
    if not isinstance(lock, list):
        raise PlanError("lock: must be a list of entries")
    artifacts = {}
    for i, entry in enumerate(lock):
        for field in ("name", "artifact_sha256"):
            if not isinstance(entry, dict) or not isinstance(entry.get(field), str) or not entry[field]:
                raise PlanError(f"lock[{i}].{field}: must be a non-empty string")
        artifacts[entry["name"]] = entry["artifact_sha256"]
    for lane in exp["lanes"]:
        if lane["name"] not in artifacts:
            raise PlanError(f"lock: no entry for lane {lane['name']}")
    return artifacts


def build_plan(exp_path, tasks_dir, lock_path):
    """The `PLAN.json` content: the experiment (without `hosts`), the hashes, the lock's artifacts."""
    exp = experiment.load(exp_path)
    artifacts = read_lock(lock_path, exp)
    public = {k: v for k, v in exp.items() if k != "hosts"}  # host names stay out of the public repo
    form = exp.get("intent_form")
    return {"experiment": public,
            "hashes": {"tasks": {t: task_hashes(os.path.join(tasks_dir, t), exp["phase"], form)
                                 for t in exp["tasks"]},
                       "lanes": lane_hashes(exp, exp_path)},
            "lock": {"sha256": common.sha256_file(lock_path), "artifacts": artifacts}}


def main(argv=None):
    p = argparse.ArgumentParser(description="Write PLAN.json before any cell runs.")
    p.add_argument("experiment")
    p.add_argument("--tasks", default=os.environ.get("KOGEN_LANES_TASKS"), help="private tasks folder")
    p.add_argument("--lock", required=True, help="lanes.lock.json")
    p.add_argument("--out", required=True, help="PLAN.json to write")
    a = p.parse_args(argv)
    if not a.tasks:
        p.error("--tasks or KOGEN_LANES_TASKS is required")
    try:
        plan = build_plan(a.experiment, a.tasks, a.lock)
    except (experiment.ExperimentError, PlanError, OSError, ValueError) as e:
        print(f"plan: {e}", file=sys.stderr)
        return 2
    common.write_json(a.out, plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
