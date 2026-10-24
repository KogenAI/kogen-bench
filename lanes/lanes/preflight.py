"""Lint-approve every supplied Intent with every lane's Kogen before any cell starts (`lanes-preflight`).

For phase `build`, each task x lane gets a scratch workspace set up as `lanes-cell` does, the supplied
Intent installed, and `kogen intent approve <slug>` run, then again with the printed hash. Approve is
local: no provider is involved. Nothing is written to the run dir.
"""

import argparse
import os
import shutil
import sys
import tempfile
import tomllib

from . import cell, common, experiment, leakage, probe

DEADLINE_S = 120


def _lines(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def check_one(exp, run_dir, tasks, task_id, lane, artifact=None):
    """`(ok, message)` for one task x lane."""
    task = os.path.join(tasks, task_id)
    try:
        with open(os.path.join(task, "task.toml"), "rb") as f:
            task_toml = tomllib.load(f)
        slug = task_toml.get("name")
        if not isinstance(slug, str) or not cell.SLUG.match(slug) or not 3 <= len(slug) <= 48:
            raise cell.CellError(f"task.toml name {slug!r} is not a Kogen slug")
        supplied = os.path.join(task, "supplied", exp["intent_form"])
        cell.check_supplied(supplied, slug)
        kogen = cell.resolve_kogen(run_dir, lane["name"], artifact)
        config = cell.project_yaml(task_toml, lane["settings"].get("models"))
        root = cell.release_root(kogen)  # as a cell does: the Go Kogen's readiness needs <root>/node-path
        if root:
            cell.ensure_node_path(root)
    except (OSError, ValueError, cell.CellError) as e:
        return False, str(e)
    tmp = tempfile.mkdtemp(prefix="lanes-preflight-")
    try:
        ws, out = os.path.join(tmp, "ws"), os.path.join(tmp, "out")
        os.makedirs(out)
        cell.make_workspace(ws, tmp, os.path.join(task, "start"), config)
        cell.install_supplied(ws, supplied, slug)
        c = cell.Cell(ws, kogen, out, DEADLINE_S)
        card = c.invoke(["intent", "approve", slug])
        m = cell.CARD_HASH.search(card[2])
        calls = [card]
        if card[0] == 5 and m and not card[1]:
            calls.append(c.invoke(["intent", "approve", slug, m.group(1)]))
        last = calls[-1]
        if len(calls) == 2 and last[0] == 0 and not last[1]:
            return True, f"approved {m.group(1)[:8]}"
        why = "timed out" if last[1] else f"exit {last[0]}"
        stdout = _lines(last[2])
        with open(os.path.join(out, "stderr.txt"), encoding="utf-8", errors="replace") as f:
            stderr = _lines(f.read())
        detail = [l for l in stdout + stderr if not l.startswith("== kogen")] or ["no output"]
        return False, f"approve refused ({why}):\n    " + "\n    ".join(detail[-12:])
    except cell.CellError as e:
        return False, str(e)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def preflight(run_dir, tasks, artifact=None, out=print):
    """Check every task x lane of the run; returns the number of refusals and leaks (Intent checks: build only)."""
    exp_path = os.path.join(run_dir, "experiment.json")
    exp = experiment.load(exp_path)
    if exp["phase"] == "probe":  # `tasks` is the corpus folder
        return probe.preflight(run_dir, tasks, out=out)
    leaks = 0
    if exp.get("kind") == "climb":  # a climb patch must not carry task content
        home = common.runs_dir()
        earlier = [os.path.join(home, d) for d in sorted(os.listdir(home)) if d != exp["id"]
                   and os.path.isdir(os.path.join(home, d, "cells"))] if os.path.isdir(home) else []
        notes = []
        try:
            hits = leakage.check(exp_path, tasks, earlier, notes=notes)
        except (OSError, ValueError) as e:
            hits = [("leakcheck", "error", str(e), "run dir")]
        for note in notes:
            out(f"leakcheck: note: {note}")
        for hit in hits:
            out("LEAK: " + leakage.format_hit(hit))
        leaks = len(hits)
    if exp["phase"] != "build":
        out(f"preflight: phase {exp['phase']} supplies no Intent; nothing to check")
        return leaks
    bad = leaks
    for task_id in exp["tasks"]:
        for lane in exp["lanes"]:
            ok, message = check_one(exp, run_dir, tasks, task_id, lane, artifact)
            bad += not ok
            out(f"{task_id} x {lane['name']}: {'ok' if ok else 'REFUSED'}: {message}")
    return bad


def main(argv=None):
    p = argparse.ArgumentParser(description="Lint-approve every supplied Intent with every lane's Kogen.")
    p.add_argument("run_dir")
    p.add_argument("--tasks", default=os.environ.get("KOGEN_LANES_TASKS"), help="private tasks folder")
    p.add_argument("--corpus", default=os.environ.get("KOGEN_LANES_CORPUS"), help="probe corpus folder")
    p.add_argument("--artifact", help="kogen executable, folder or .tar.gz for every lane (default: lanes.lock.json)")
    a = p.parse_args(argv)
    try:
        data = probe.corpus_path(a.run_dir, a.corpus) if probe.is_probe(a.run_dir) else a.tasks
    except probe.ProbeError as e:
        p.error(str(e))
    if not data:
        p.error("--tasks or KOGEN_LANES_TASKS is required")
    try:
        bad = preflight(a.run_dir, data, a.artifact)
    except (experiment.ExperimentError, OSError, ValueError) as e:
        print(f"preflight: {e}", file=sys.stderr)
        return 2
    if bad:
        print(f"preflight: {bad} refusal(s); no cell may start", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
