"""Run one cell: one task, one repetition, one lane, one phase (`lanes-cell`).

A cell gets a fresh git workspace holding the task's `start/` and a fixed `.kogen/project.yaml`
(no `kogen init`, which would call the shaping model), runs the phase's Kogen commands, each in its
own process group under the cell's shared deadline, and writes its cell dir (FORMATS.md). The hidden
tests (`evaluator/`) are never copied anywhere the run can see. `result.json` is written last.
"""

import argparse
import datetime
import glob
import os
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import time
import tomllib

from . import common, experiment, usage

IDENTITY = {"name": "Kogen Lanes", "email": "lanes@" + "example.invalid"}
START_DATE = "2026-01-01T00:00:00+0000"
CARD_HASH = re.compile(r"^SHA-256:\s*([0-9a-f]{64})\s*$", re.M)
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ERROR_LINE = re.compile(r"^([a-z_]+/[a-z_]+):", re.M)
INTENT_FILES = ("intent.md", "acceptance.feature")  # and model.*: these live in the Intent folder
# Exit code -> outcome (FORMATS Kogen exit codes); a build's last `outcome` event wins over these.
OUTCOMES = {0: "ok", 1: "refused", 2: "usage", 3: "environment", 70: "internal",
            129: "signal", 130: "signal", 143: "signal"}


class CellError(Exception):
    """The harness cannot run or record this cell (nothing is written)."""


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def yq(s):
    """A YAML single-quoted scalar, as Kogen writes them."""
    if "\n" in s:
        raise CellError(f"a command with a newline cannot go in project.yaml: {s!r}")
    return "'" + s.replace("'", "''") + "'"


def project_yaml(task_toml, models):
    """`.kogen/project.yaml` from the task's commands and the lane's `"provider/model effort"` lines."""
    def items(key, item=yq):
        vals = task_toml.get(key) or []
        return [f"  {key}: []"] if not vals else [f"  {key}:"] + [f"    - {item(v)}" for v in vals]

    lines = ["version: 1", "commands:", *items("setup"), *items("fix")]
    checks = task_toml.get("check") or []
    lines += ["  checks: []"] if not checks else ["  checks:"] + [
        line for c in checks for line in (f"    - name: {c['name']}", f"      run: {yq(c['run'])}")]
    acc = task_toml.get("acceptance")
    lines += ["  acceptance:", f"    run: {yq(acc['run'])}", f"    steps_dir: {yq(acc['steps_dir'])}"] if acc \
        else ["  acceptance:", "    run: null", "    steps_dir: null"]
    protect = task_toml.get("protect") or []
    lines += ["protect: []"] if not protect else ["protect:"] + [f"  - {yq(p)}" for p in protect]
    if models:
        lines.append("models:")
        for role, value in sorted(models.items()):
            model, _, effort = value.rpartition(" ")
            lines.append(f"  {role}: {{model: {model}, effort: {effort}}}")
    return "\n".join(lines) + "\n"


def _find_kogen(root):
    for rel in ("bin/kogen", "kogen", "*/bin/kogen"):
        for path in sorted(glob.glob(os.path.join(root, rel))):
            if os.path.isfile(path) and os.access(path, os.X_OK):
                return path
    return None


def _unpack(archive):
    """Unpack a release archive once per content hash under `$KOGEN_LANES_HOME/unpacked/`."""
    base = os.path.join(common.lanes_home(), "unpacked")
    dest = os.path.join(base, common.sha256_file(archive))
    if not os.path.isdir(dest):
        os.makedirs(base, exist_ok=True)
        tmp = tempfile.mkdtemp(dir=base, prefix=".unpack-")
        with tarfile.open(archive) as t:
            t.extractall(tmp, filter="data")
        try:
            os.rename(tmp, dest)
        except OSError:  # another cell unpacked it first
            shutil.rmtree(tmp, ignore_errors=True)
    return dest


def resolve_kogen(run_dir, lane, artifact=None):
    """Path of the lane's `kogen` executable: from `--artifact`, else the lock's artifact folder.

    The artifact is an executable, a folder holding one (`bin/kogen`), or a `.tar.gz` release.
    """
    if artifact is None:
        lock = os.path.join(run_dir, "lanes.lock.json")
        try:
            entry = next(e for e in common.read_json(lock) if e["name"] == lane)
        except (OSError, ValueError, StopIteration, KeyError, TypeError):
            raise CellError(f"no --artifact and no entry for lane {lane} in {lock}") from None
        artifact = os.path.join(common.lanes_home(), "artifacts", entry["artifact_sha256"])
    if os.path.isfile(artifact) and artifact.endswith((".tar.gz", ".tgz")):
        found = _find_kogen(_unpack(artifact))
    elif os.path.isfile(artifact):
        found = artifact if os.access(artifact, os.X_OK) else None
    else:
        found = _find_kogen(artifact)
        for archive in sorted(glob.glob(os.path.join(artifact, "*.tar.gz"))) if not found else []:
            found = _find_kogen(_unpack(archive))
    if not found:
        raise CellError(f"no kogen executable in artifact {artifact}")
    return os.path.abspath(found)


def _git(ws, *args, env=None, check=True):
    r = subprocess.run(["git", "-C", ws, *args], capture_output=True, text=True, env=env)
    if check and r.returncode:
        raise CellError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def make_workspace(ws, tmp, start, config):
    """Copy `start/`, add the fixed configuration and commit it, with stable author, date and config."""
    shutil.copytree(start, ws, symlinks=True)
    os.makedirs(os.path.join(ws, ".kogen"), exist_ok=True)
    with open(os.path.join(ws, ".kogen", "project.yaml"), "w", encoding="utf-8") as f:
        f.write(config)
    gi = os.path.join(ws, ".gitignore")
    old = open(gi, encoding="utf-8").read() if os.path.exists(gi) else ""
    if ".kogen/local/" not in old.splitlines():
        with open(gi, "w", encoding="utf-8") as f:
            f.write(old + ("" if old.endswith("\n") or not old else "\n") + ".kogen/local/\n")
    env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
           "XDG_CONFIG_HOME": os.path.join(tmp, "xdg"),  # no global excludes while staging the start tree
           "GIT_AUTHOR_NAME": IDENTITY["name"], "GIT_AUTHOR_EMAIL": IDENTITY["email"],
           "GIT_COMMITTER_NAME": IDENTITY["name"], "GIT_COMMITTER_EMAIL": IDENTITY["email"],
           "GIT_AUTHOR_DATE": START_DATE, "GIT_COMMITTER_DATE": START_DATE}
    _git(ws, "init", "-q", "--initial-branch=main", env=env)
    for key, value in (("user.name", IDENTITY["name"]), ("user.email", IDENTITY["email"]),
                       ("commit.gpgsign", "false"), ("core.hooksPath", os.devnull)):
        _git(ws, "config", key, value)
    _git(ws, "add", "-A", env=env)
    _git(ws, "commit", "-q", "-m", "Start", env=env)


class Cell:
    def __init__(self, ws, kogen, out, deadline_s):
        self.ws, self.kogen, self.out = ws, kogen, out
        self.deadline = time.monotonic() + deadline_s
        self.commands = []
        # Kogen's shaper can run shell commands: keep the paths of private data out of its environment.
        self.env = {**{k: v for k, v in os.environ.items() if not k.startswith("KOGEN_LANES_")},
                    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
                    "GIT_TERMINAL_PROMPT": "0"}

    def invoke(self, args, stdin_path=None):
        """One Kogen command in its own process group; `(code, timed_out, stdout, started, ended)`."""
        started, t0 = now(), time.monotonic()
        o, e = os.path.join(self.out, "o.tmp"), os.path.join(self.out, "e.tmp")
        with open(o, "w") as fo, open(e, "w") as fe, open(stdin_path or os.devnull) as fi:
            code, timed_out = common.run([self.kogen, *args], cwd=self.ws, env=self.env,
                                         deadline_s=max(self.deadline - t0, 0.01),
                                         stdout=fo, stderr=fe, stdin=fi)
        text = open(o, encoding="utf-8", errors="replace").read()
        for tmp, name in ((o, "stdout.txt"), (e, "stderr.txt")):
            with open(tmp, encoding="utf-8", errors="replace") as src, \
                    open(os.path.join(self.out, name), "a", encoding="utf-8") as dst:
                dst.write(f"== kogen {' '.join(args)}\n{src.read()}")
            os.remove(tmp)
        return code, timed_out, text, started, now(), time.monotonic() - t0

    def version(self, tmp):
        """`kogen version` in its own group under the cell deadline; None when it fails."""
        path = os.path.join(tmp, "version.txt")
        with open(path, "w") as fo, open(os.devnull) as fi:
            code, timed_out = common.run([self.kogen, "version"], cwd=self.ws, env=self.env, stdin=fi,
                                         deadline_s=max(self.deadline - time.monotonic(), 0.01), stdout=fo)
        with open(path, encoding="utf-8", errors="replace") as f:
            return None if code or timed_out else f.read().strip() or None

    def record(self, stage, calls, detail=None):
        """One command-level record from one or more invocations (`shape` and `approve` may be several).

        `detail` names a failure that the exit code alone does not (it becomes the outcome).
        """
        code, timed_out = calls[-1][0], calls[-1][1]
        self.commands.append({"stage": stage, "started": calls[0][3], "ended": calls[-1][4],
                              "wall_s": round(sum(c[5] for c in calls), 3), "exit_code": code,
                              **({"timed_out": True} if timed_out else {}),
                              **({"detail": detail} if detail else {})})
        return code == 0 and not timed_out and not detail

    def shape(self, slug, request, answers):
        """Shape; when Kogen asks questions, answer them once from `answers` (stdin of `shape <slug> -`)."""
        calls = [self.invoke(["intent", "shape", slug, request])]
        if self._asks(calls[-1]) and answers and not calls[-1][1]:
            calls.append(self.invoke(["intent", "shape", slug, "-"], answers))
        return self.record("shape", calls, "questions_pending" if self._asks(calls[-1]) else None)

    @staticmethod
    def _failure(call):
        """Why an approve that printed no card failed: Kogen's `<class>/<reason>`, else None."""
        if call[0] == 5 and not call[1]:
            m = ERROR_LINE.search(call[2])
            return m.group(1) if m else "exit_5"
        return None

    @staticmethod
    def _asks(call):
        return call[0] == 5 and not call[1] and "Questions for " in call[2]

    def approve(self, slug):
        card = self.invoke(["intent", "approve", slug])
        m = CARD_HASH.search(card[2])
        if card[0] != 5 or not m or card[1]:
            self.record("approve", [card], self._failure(card) or ("no_card" if card[0] == 0 else None))
            return None
        done = self.invoke(["intent", "approve", slug, m.group(1)])
        return m.group(1) if self.record("approve", [card, done]) else None


def command_outcome(cmd, events):
    """One rule for a command's outcome, used for its stage record and for the cell."""
    if cmd.get("timed_out"):
        return "timeout"
    if cmd.get("detail"):
        return cmd["detail"]
    if cmd["stage"] == "build":
        logged = [e.get("outcome") for e in events or [] if e.get("event") == "outcome"]
        return logged[-1] if logged else ("ok" if cmd["exit_code"] == 0 else "no_outcome")
    return OUTCOMES.get(cmd["exit_code"], f"exit_{cmd['exit_code']}")


def run_cell(run_dir, cell, tasks, artifact=None, host="local", keep=False, force=False):
    """Run the cell and write its cell dir; returns `result.json` as a dict."""
    task_id, rep, lane_name = cell.split("/")
    exp = experiment.load(os.path.join(run_dir, "experiment.json"))
    lane = next((l for l in exp["lanes"] if l["name"] == lane_name), None)
    task = os.path.join(tasks, task_id)
    if lane is None or not re.fullmatch(r"r\d+", rep) or not os.path.isdir(os.path.join(task, "start")):
        raise CellError(f"unknown cell {cell}: lane, rep or task folder not found")
    phase = exp["phase"]
    out = common.cell_dir(run_dir, cell)
    if os.path.exists(os.path.join(out, "result.json")) and not force:
        raise CellError(f"{cell} is already done (result.json exists); use --force to rerun")
    kogen = resolve_kogen(run_dir, lane_name, artifact)
    with open(os.path.join(task, "task.toml"), "rb") as f:
        task_toml = tomllib.load(f)
    slug = task_toml.get("name")
    if not isinstance(slug, str) or not SLUG.match(slug) or not 3 <= len(slug) <= 48:
        raise CellError(f"{task_id}: task.toml name {slug!r} is not a Kogen slug (3-48 of a-z, 0-9, -)")
    config = project_yaml(task_toml, lane["settings"].get("models"))
    request = os.path.join(task, "request.md")
    supplied = os.path.join(task, "supplied", exp.get("intent_form") or "")
    if phase != "build" and not os.path.isfile(request):
        raise CellError(f"{task_id} has no request.md")
    if phase == "build":
        check_supplied(supplied, slug)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    tmp = tempfile.mkdtemp(prefix="lanes-cell-")
    try:
        return _run(exp, cell, lane_name, task, slug, kogen, config, out, tmp, host)
    finally:
        if keep:
            print(f"kept workspace: {os.path.join(tmp, 'ws')}", file=sys.stderr)
        else:
            shutil.rmtree(tmp, ignore_errors=True)


def check_supplied(supplied, slug):
    """Refuse a supplied Intent that is missing or whose `Slug:` line is not the task's slug."""
    try:
        with open(os.path.join(supplied, "intent.md"), encoding="utf-8") as f:
            text = f.read()
    except OSError:
        raise CellError(f"{supplied} has no intent.md") from None
    m = re.search(r"^Slug:\s*(\S+)", text, re.M)
    if not m or m.group(1) != slug:
        raise CellError(f"supplied Intent says Slug: {m.group(1) if m else None}, but the task's slug "
                        f"(task.toml name) is {slug}; Kogen refuses an Intent in a folder of another name")


def install_supplied(ws, supplied, slug):
    """Lay a supplied Intent out as Kogen's shaper does (the Lab does the same, with the task name as slug):
    `intent.md`, `acceptance.feature` and `model.*` in `.kogen/intents/<slug>/`, every other file (the
    step files its `Acceptance:` list names) at its relative path in the work tree."""
    for dirpath, _, names in os.walk(supplied):
        for name in names:
            src = os.path.join(dirpath, name)
            rel = os.path.relpath(src, supplied)
            home = rel in INTENT_FILES or (os.sep not in rel and rel.startswith("model."))
            dst = os.path.join(ws, ".kogen", "intents", slug, rel) if home else os.path.join(ws, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)


def acceptance_list(intent_md):
    """The paths of an intent.md `Acceptance:` list."""
    paths, on = [], False
    for line in intent_md.splitlines():
        if on and line.startswith("- "):
            paths.append(line[2:].strip())
        elif on:
            break
        on = on or line.strip() == "Acceptance:"
    return paths


def save_intent(ws, slug, dest):
    """Copy the shaped Intent to `dest` in the supplied layout: the Intent folder's files, plus every
    other file its `Acceptance:` list names at its relative path (Kogen writes those at the repo root)."""
    src = os.path.join(ws, ".kogen", "intents", slug)
    if not os.path.isfile(os.path.join(src, "intent.md")):
        return
    shutil.copytree(src, dest)
    with open(os.path.join(src, "intent.md"), encoding="utf-8", errors="replace") as f:
        listed = acceptance_list(f.read())
    for rel in listed:
        path = os.path.join(ws, rel)
        if not rel.startswith((".kogen/", "/", "..")) and ".." not in rel.split("/") and os.path.isfile(path):
            os.makedirs(os.path.dirname(os.path.join(dest, rel)), exist_ok=True)
            shutil.copyfile(path, os.path.join(dest, rel))


def _run(exp, cell, lane_name, task, slug, kogen, config, out, tmp, host):
    phase = exp["phase"]
    ws = os.path.join(tmp, "ws")
    make_workspace(ws, tmp, os.path.join(task, "start"), config)
    inputs = os.path.join(tmp, "inputs")  # the brief and answers, outside the work tree and the task folder
    os.makedirs(inputs)
    request, answers = os.path.join(inputs, "request.md"), os.path.join(inputs, "answers.txt")
    for name, dst in (("request.md", request), ("answers.txt", answers)):
        if os.path.isfile(os.path.join(task, name)):
            shutil.copyfile(os.path.join(task, name), dst)
    c = Cell(ws, kogen, out, exp["deadline_s"])
    started, t0 = now(), time.monotonic()
    version = c.version(tmp)
    intent_hash, ok = None, True
    if phase in ("shape", "e2e"):
        ok = c.shape(slug, request, answers if os.path.isfile(answers) else None)
        save_intent(ws, slug, os.path.join(out, "intent"))
    if phase == "build":
        install_supplied(ws, os.path.join(task, "supplied", exp["intent_form"]), slug)
    if ok and phase != "shape":
        intent_hash = c.approve(slug)
        ok = intent_hash is not None
    if ok and phase != "shape":
        c.record("build", [c.invoke(["intent", "build", slug])])
    return _collect(exp, cell, lane_name, ws, slug, c, out, started, t0, version, intent_hash, host)


def _collect(exp, cell, lane_name, ws, slug, c, out, started, t0, version, intent_hash, host):
    runs = sorted(glob.glob(os.path.join(ws, ".kogen", "local", "runs", "*")))
    if len(runs) > 1:
        raise CellError(f"{cell}: {len(runs)} build runs in one cell; a cell runs one build")
    events = None
    if runs:
        shutil.copytree(runs[0], os.path.join(out, "run-log"))
        events = usage.read_log(os.path.join(runs[0], "log.jsonl"))
    shape_path = os.path.join(ws, ".kogen", "local", "shaping", slug, "events.ndjson")
    shape_events = usage.read_log(shape_path)
    if shape_events is not None:
        shutil.copyfile(shape_path, os.path.join(out, "shaping-events.ndjson"))
    final_tree = _git(ws, "rev-parse", "HEAD^{tree}")
    _git(ws, "archive", "--format=tar", "-o", os.path.join(out, "final-tree.tar"), "HEAD")
    trees = [e["tree"] for e in events or [] if e.get("event") in ("review", "commit") and e.get("tree")]
    for tree in dict.fromkeys(trees):  # keep the trees the workspace still has, for lanes-grade
        if _git(ws, "cat-file", "-t", tree, check=False) == "tree":
            os.makedirs(os.path.join(out, "pass-trees"), exist_ok=True)
            _git(ws, "archive", "--format=tar", "-o", os.path.join(out, "pass-trees", tree + ".tar"), tree)
    stages = usage.parse_run_log(events, c.commands, shape_events=shape_events)
    outcomes = {cmd["stage"]: command_outcome(cmd, events) for cmd in c.commands}
    for rec in stages["stages"]:  # one rule for the stage records and the cell
        if rec["stage"] in outcomes:
            rec["outcome"] = outcomes[rec["stage"]]
    result = {"cell": cell, "lane": lane_name, "phase": exp["phase"], "exit_code": c.commands[-1]["exit_code"],
              "outcome": command_outcome(c.commands[-1], events), "started": started, "ended": now(),
              "wall_s": round(time.monotonic() - t0, 3), "kogen_version": version,
              "final_tree": final_tree, "pass_trees": list(dict.fromkeys(trees)),
              "intent_hash": intent_hash, "host": host, **stages}
    common.write_json(os.path.join(out, "result.json"), result)
    return result


class Terminated(BaseException):
    """SIGTERM or SIGHUP, raised in the main thread so `finally` blocks and `common.run` clean up."""


def _terminate(signum, frame):
    raise Terminated(signum)


def main(argv=None):
    p = argparse.ArgumentParser(description="Run one lane cell and write its cell dir.")
    p.add_argument("run_dir")
    p.add_argument("cell", help="<task>/r<rep>/<lane>")
    p.add_argument("--tasks", default=os.environ.get("KOGEN_LANES_TASKS"), help="private tasks folder")
    p.add_argument("--artifact", help="kogen executable, folder or .tar.gz (default: lanes.lock.json)")
    p.add_argument("--host", default="local")
    p.add_argument("--keep", action="store_true", help="keep the temp workspace")
    p.add_argument("--force", action="store_true", help="rerun a finished cell")
    a = p.parse_args(argv)
    if not a.tasks:
        p.error("--tasks or KOGEN_LANES_TASKS is required")
    for sig in (signal.SIGTERM, signal.SIGHUP):  # stop like Ctrl-C: kill our groups, remove the workspace
        signal.signal(sig, _terminate)
    try:
        result = run_cell(a.run_dir, a.cell, a.tasks, a.artifact, a.host, a.keep, a.force)
    except (CellError, experiment.ExperimentError) as e:
        print(f"cell: {e}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("cell: interrupted", file=sys.stderr)
        return 130
    except Terminated as e:
        print(f"cell: terminated by signal {e.args[0]}", file=sys.stderr)
        return 128 + e.args[0]
    print(f"{a.cell}: {result['outcome']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
