"""Hidden-test grading, shape grading and task qualification (the Lab's evaluate and qualify)."""

import contextlib
import json
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import time
import tomllib

from . import common

GRADE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "grade")
SETUP_DEADLINE_S = 600
# Host variables the toolchains need; nothing else (no tokens) reaches agent-written code.
ENV_PREFIXES = ("GO", "MIX_", "HEX_", "NODE_", "NPM_CONFIG_", "npm_config_")
STATUS_ORDER = ["UNKNOWN", "PASSED", "SKIPPED", "PENDING", "UNDEFINED", "AMBIGUOUS", "FAILED"]
_binary = []


class GradeError(ValueError):
    pass


def grader_binary():
    """The Go verdict binary: `LANES_GRADE_BIN`, else built once per process into the cache."""
    if os.environ.get("LANES_GRADE_BIN"):
        return os.environ["LANES_GRADE_BIN"]
    if not _binary:
        out = os.path.join(common.cache_dir(), "bin", "lanes-grade-verdict")
        tmp = f"{out}.{os.getpid()}"  # build aside, then rename: concurrent processes cannot race
        os.makedirs(os.path.dirname(out), exist_ok=True)
        try:
            r = subprocess.run(["go", "build", "-o", tmp, "."], cwd=GRADE_DIR, capture_output=True,
                               text=True, timeout=300)
        except subprocess.TimeoutExpired:
            raise GradeError("go build of the grader timed out")
        if r.returncode:
            raise GradeError("cannot build the grader: " + r.stderr.strip())
        os.replace(tmp, out)
        _binary.append(out)
    return _binary[0]


def read_toml(path):
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_task(task_dir):
    task = read_toml(os.path.join(task_dir, "task.toml"))
    ev = read_toml(os.path.join(task_dir, "evaluator", "evaluate.toml"))
    if not ev.get("overlay") or not ev.get("command"):
        raise GradeError("evaluate.toml needs overlay and at least one [[command]]")
    return {"dir": task_dir, "task": task, "eval": ev}


def extract(tar_path, dest):
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(tar_path) as t:
        t.extractall(dest, filter="data")


def lay(src, dest):
    shutil.copytree(src, dest, dirs_exist_ok=True, symlinks=True)


@contextlib.contextmanager
def scratch(task_dir=None, *overlays):
    """A fresh grading dir under `$KOGEN_LANES_HOME/tmp`; yields its `tree/` (`start/` with the
    overlay folders, e.g. `reference`, laid over it when `task_dir` is given). Removed on exit."""
    base = os.path.join(common.lanes_home(), "tmp")
    os.makedirs(base, exist_ok=True)
    root = tempfile.mkdtemp(prefix="grade-", dir=base)
    tree = os.path.join(root, "tree")
    try:
        os.makedirs(tree)
        if task_dir:
            for sub in ("start",) + overlays:
                lay(os.path.join(task_dir, sub), tree)
        yield tree
    finally:
        shutil.rmtree(root, ignore_errors=True)


def sh(cmd, cwd, env, deadline_s):
    """Run a shell line in its own group; return `{status, timed_out, wall_ms}`."""
    t0 = time.monotonic()
    with open(os.devnull, "wb") as null:
        code, timed_out = common.run(["sh", "-c", cmd], cwd=cwd, env=env, deadline_s=deadline_s,
                                     stdout=null, stderr=null, stdin=subprocess.DEVNULL)
    return {"status": code, "timed_out": timed_out, "wall_ms": int((time.monotonic() - t0) * 1000)}


def task_env(task, tree, extra=None):
    """The Lab's `commandEnv`: toolchain variables, HOME, PATH, LANG, the task `env`, and a private
    TMPDIR next to the tree."""
    env = {k: v for k, v in os.environ.items() if k.startswith(ENV_PREFIXES)}
    env.update(HOME=os.environ.get("HOME", "/"), PATH=os.environ.get("PATH", "/usr/bin:/bin"),
               LANG=os.environ.get("LANG", "C.UTF-8"))
    env.update({k: str(v) for k, v in task["task"].get("env", {}).items()})
    tmp = os.path.join(os.path.dirname(tree), "tmp")
    os.makedirs(tmp, exist_ok=True)
    env["TMPDIR"] = tmp
    env.update(extra or {})
    return env


def run_setup(task, tree, lines):
    """Run setup lines in order; return (rows, infrastructure reason or None)."""
    rows = []
    for line in lines:
        row = dict(sh(line, tree, task_env(task, tree), SETUP_DEADLINE_S), name=line)
        rows.append(row)
        if row["status"] or row["timed_out"]:
            return rows, "setup failed: " + line
    return rows, None


def evaluate_tree(task, tree, hidden=True, deadline_s=None):
    """Grade the work tree `tree` in place: overlay hidden tests, setup, evaluator commands.

    Returns the evaluation record (Lab key names); a setup failure or an unusable results path is
    `infrastructure`, never a test failure. Not ported from the Lab: inferring `[expected]` when
    the task has none (such a task is not qualified), folder verification after staging, and
    killing a signalled evaluator.
    """
    ev = task["eval"]
    results_dir = os.path.join(os.path.dirname(tree), "results")
    if hidden:
        lay(os.path.join(task["dir"], "evaluator", ev["overlay"]), tree)
    rec = {"infrastructure": None}
    rec["setup"], rec["infrastructure"] = run_setup(task, tree, task["task"].get("setup", []) + ev.get("setup", []))
    commands = []
    for c in ev["command"] if not rec["infrastructure"] else []:
        path = os.path.normpath(os.path.join(results_dir, c["results"]))
        if os.path.commonpath([results_dir, path]) != results_dir:
            rec["infrastructure"] = "results path is outside the results folder: " + c["results"]
            break
        os.makedirs(os.path.dirname(path), exist_ok=True)
        row = sh(c["run"], tree, task_env(task, tree, {"LAB_RESULTS": path}), deadline_s or c["timeout_seconds"])
        commands.append({"name": c["name"], "adapter": c["adapter"], "results_path": path,
                         "status": row["status"], "timed_out": row["timed_out"]})
    try:
        r = subprocess.run([grader_binary()], capture_output=True, text=True, timeout=120,
                           input=json.dumps({"commands": commands, "expected": ev.get("expected", {})}))
    except subprocess.TimeoutExpired:
        raise GradeError("grader timed out")
    if r.returncode:
        raise GradeError("grader failed: " + r.stderr.strip())
    rec.update(json.loads(r.stdout))
    if rec["infrastructure"]:
        rec["all_passed"] = False
    rec["totals"] = {"expected": len(rec["ids"]), "passed": sum(s == "passed" for s in rec["ids"].values())}
    return rec


def grade_archive(task, tar_path, deadline_s=None):
    with scratch() as tree:
        extract(tar_path, tree)
        return evaluate_tree(task, tree, deadline_s=deadline_s)


# --- shape grading -----------------------------------------------------------------------------

def intent_slug(intent_md):
    with open(intent_md, encoding="utf-8") as f:
        m = re.search(r"^Slug:\s*(\S+)", f.read(), re.M)
    if not m:
        raise GradeError("intent.md has no Slug:")
    return m.group(1)


def intent_steps(intent_md):
    """Step files in the Intent's `Acceptance:` list (the feature file and `.kogen/` paths excluded)."""
    with open(intent_md, encoding="utf-8") as f:
        lines = f.read().splitlines()
    files = []
    if "Acceptance:" in lines:
        for line in lines[lines.index("Acceptance:") + 1:]:
            if not line.startswith("- "):
                break
            files.append(line[2:].strip())
    for p in files:
        if os.path.isabs(p) or ".." in p.split("/"):
            raise GradeError("unsafe step path in Intent: " + p)
    return [p for p in files if not p.startswith(".kogen/") and not p.endswith(".feature")]


def read_report(path):
    """Scenario line -> lower-case status from a Cucumber Messages NDJSON report (as Kogen's
    `Checks.read_report`: retried cases ignored, worst step status, unfinished cases `report_invalid`,
    a line seen twice `duplicate`). None when the file is missing, not NDJSON or has no test case."""
    try:
        with open(path, encoding="utf-8") as f:
            msgs = [json.loads(line) for line in f if line.strip()]
        if not all(isinstance(m, dict) for m in msgs):
            return None
    except (OSError, ValueError):
        return None
    lines = {}

    def walk(children):
        for ch in children or []:
            walk((ch.get("rule") or {}).get("children"))
            node = ch.get("scenario")
            if node:
                lines[node["id"]] = node["location"]["line"]
                for ex in node.get("examples") or []:
                    for row in ex.get("tableBody") or []:
                        lines[row["id"]] = row["location"]["line"]

    for m in msgs:
        if "gherkinDocument" in m:
            walk((m["gherkinDocument"].get("feature") or {}).get("children"))
    pickles = {m["pickle"]["id"]: m["pickle"] for m in msgs if "pickle" in m}
    cases = {m["testCase"]["id"]: m["testCase"] for m in msgs if "testCase" in m}
    started = {m["testCaseStarted"]["id"]: m["testCaseStarted"]["testCaseId"] for m in msgs if "testCaseStarted" in m}
    retried = {m["testCaseFinished"]["testCaseStartedId"] for m in msgs
               if "testCaseFinished" in m and m["testCaseFinished"].get("willBeRetried")}
    finished = {m["testCaseFinished"]["testCaseStartedId"] for m in msgs
                if "testCaseFinished" in m and not m["testCaseFinished"].get("willBeRetried")}
    steps = {}
    for m in msgs:
        f = m.get("testStepFinished")
        if f:
            steps.setdefault(f["testCaseStartedId"], {})[f["testStepId"]] = f["testStepResult"]["status"]
    out = {}
    for sid, cid in started.items():
        if sid in retried:
            continue
        tc, got = cases[cid], steps.get(sid, {})
        if sid in finished and all(s["id"] in got for s in tc["testSteps"]):
            worst = max(got.values(), key=STATUS_ORDER.index, default="UNKNOWN").lower()
        else:
            worst = "report_invalid"
        line = str(lines[pickles[tc["pickleId"]]["astNodeIds"][-1]])
        out[line] = "duplicate" if line in out else worst
    return out or None


def shape_tree(task, overlays, intent, slug, step_files, deadline_s):
    """Run the task's acceptance runner on one tree with the shaped Intent's scenarios and steps.

    Returns `{line: status}` or `{"infrastructure": reason}` (setup failed, or the runner wrote no
    usable report: a runner error is not a failed scenario).
    """
    acc = task["task"]["acceptance"]
    with scratch(task["dir"], *overlays) as tree:
        shutil.rmtree(os.path.join(tree, acc.get("steps_dir", "features/steps")), ignore_errors=True)
        folder = os.path.join(tree, ".kogen", "intents", slug)
        os.makedirs(folder)
        for name in os.listdir(intent):
            if os.path.isfile(os.path.join(intent, name)):
                shutil.copy(os.path.join(intent, name), folder)
        for rel, src in step_files.items():
            os.makedirs(os.path.dirname(os.path.join(tree, rel)), exist_ok=True)
            shutil.copy(src, os.path.join(tree, rel))
        _, bad = run_setup(task, tree, task["task"].get("setup", []))
        if bad:
            return {"infrastructure": bad}
        report = os.path.join(os.path.dirname(tree), "acceptance-report.ndjson")
        env = task_env(task, tree, {"KOGEN_ACCEPTANCE_FEATURES": f".kogen/intents/{slug}/acceptance.feature",
                                    "KOGEN_ACCEPTANCE_REPORT": report})
        row = sh(acc["run"], tree, env, deadline_s)
        scenarios = read_report(report)
        if scenarios is None:
            why = "timed out" if row["timed_out"] else f"exit {row['status']}"
            return {"infrastructure": f"acceptance run wrote no usable report ({why})"}
        return scenarios


def grade_shape(task, cell, deadline_s=600):
    """Run the shaped Intent's scenarios against the reference, start and each wrong tree.

    `matrix[tree][scenario line]` is the scenario's status. Counts are over scenarios: `scenarios`
    (those the reference run reports), `pass_on_reference`, `fail_on_start` (scenarios not passing
    on start); `wrong_caught` counts wrong trees where some scenario does not pass, of `wrong_total`.
    A tree whose run gave no report is `infrastructure` and no counts are written.
    """
    rec = {"phase": "shape", "infrastructure": None}
    intent = os.path.join(cell, "intent")
    if not task["task"].get("acceptance") or not os.path.isfile(os.path.join(intent, "intent.md")):
        rec["infrastructure"] = "task has no [acceptance] or the cell has no Intent"
        return rec
    slug = intent_slug(os.path.join(intent, "intent.md"))
    with scratch() as final:  # step files may be in the Intent folder or the cell's final tree
        if os.path.isfile(os.path.join(cell, "final-tree.tar")):
            extract(os.path.join(cell, "final-tree.tar"), final)
        listed, found = intent_steps(os.path.join(intent, "intent.md")), {}
        for p in listed:
            hit = [os.path.join(s, p) for s in (intent, final) if os.path.isfile(os.path.join(s, p))]
            if hit:
                found[p] = hit[0]
        if not listed or len(found) < len(listed):
            rec["infrastructure"] = "step files not available: " + ", ".join(
                [p for p in listed if p not in found] or ["none listed"])
            return rec
        wrong = sorted(os.listdir(os.path.join(task["dir"], "wrong"))) if os.path.isdir(
            os.path.join(task["dir"], "wrong")) else []
        trees = {"reference": ["reference"], "start": [], **{"wrong/" + w: ["wrong/" + w] for w in wrong}}
        rec["matrix"] = {name: shape_tree(task, o, intent, slug, found, deadline_s) for name, o in trees.items()}
    bad = [f"{n}: {m['infrastructure']}" for n, m in rec["matrix"].items() if "infrastructure" in m]
    if bad:
        rec["infrastructure"] = "; ".join(bad)
        return rec
    ref, start = rec["matrix"]["reference"], rec["matrix"]["start"]
    rec.update(scenarios=len(ref), pass_on_reference=sum(s == "passed" for s in ref.values()),
               fail_on_start=sum(start.get(line) != "passed" for line in ref),
               wrong_caught=sum(any(rec["matrix"]["wrong/" + w].get(line) != "passed" for line in ref) for w in wrong),
               wrong_total=len(wrong))
    return rec


def shape_summary(rec):
    return "scenarios=%d pass_on_reference=%d fail_on_start=%d wrong_caught=%d/%d" % (
        rec["scenarios"], rec["pass_on_reference"], rec["fail_on_start"], rec["wrong_caught"], rec["wrong_total"])


# --- cells -------------------------------------------------------------------------------------

def grade_cell(run_dir, cell, tasks_dir, deadline_s=None):
    """Grade one finished cell and write its `evaluation.json`; return the record."""
    d = common.cell_dir(run_dir, cell)
    result = common.read_json(os.path.join(d, "result.json"))
    task = load_task(os.path.join(tasks_dir, cell.split("/")[0]))
    if result.get("phase") == "shape":
        rec = grade_shape(task, d, deadline_s or 600)
    else:
        tar = os.path.join(d, "final-tree.tar")
        if os.path.isfile(tar):
            rec = grade_archive(task, tar, deadline_s)
        else:
            rec = {"all_passed": False, "infrastructure": "final-tree.tar missing"}
        # FORMATS names pass trees only by id; the run dir holds no tree content for them yet (see
        # ISSUES.md, L4 -> L1/L3). A tree archive at `pass-trees/<id>.tar` is graded when present.
        rec["pass_trees"] = []
        for tree in result.get("pass_trees") or []:
            p = os.path.join(d, "pass-trees", str(tree) + ".tar")
            sub = grade_archive(task, p, deadline_s) if os.path.isfile(p) else {"ungraded": "tree not available"}
            rec["pass_trees"].append(dict(sub, tree=tree))
    common.write_json(os.path.join(d, "evaluation.json"), rec)
    return rec


def finished_cells(run_dir):
    base = os.path.join(run_dir, "cells")
    return sorted(os.path.relpath(r, base) for r, _, f in os.walk(base) if "result.json" in f)


# --- qualification -----------------------------------------------------------------------------

def qualify(task_dir):
    """The Lab's qualification rules (`steps.go`); returns a list of `(check, ok, detail)`.

    Not ported: repeating start and reference three times (determinism compares two reference
    runs), second implementations, the killed-evaluator check and `[expected]` inference.
    """
    task, out = load_task(task_dir), []
    exp = task["eval"].get("expected", {})
    requested, regression = exp.get("requested", []), exp.get("regression", [])

    def run(overlays, hidden=True):
        with scratch(task_dir, *overlays) as tree:
            return evaluate_tree(task, tree, hidden=hidden)

    def note(check, ok, detail):
        out.append((check, bool(ok), detail))

    ref = run(["reference"])
    every = sorted(set(requested + regression))
    ref_ok = ref["all_passed"] and not ref["infrastructure"] and sorted(ref["observed_ids"]) == every
    note("reference", ref_ok, ref["infrastructure"] or (
        "passes and reproduces every expected id" if ref_ok else "did not reproduce the expected passing ids"))
    start = run([])
    bad = [f"regression id {i} did not pass on the start" for i in regression if start["ids"].get(i) != "passed"]
    bad += [f"requested id {i} passed on the start" for i in requested if start["ids"].get(i) == "passed"]
    note("start", not start["infrastructure"] and requested and not bad,
         start["infrastructure"] or "; ".join(bad) or ("no requested ids in [expected]" if not requested else
                                                       "passes regression ids and fails every requested id"))
    wrongs = sorted(os.listdir(os.path.join(task_dir, "wrong"))) if os.path.isdir(os.path.join(task_dir, "wrong")) else []
    if not wrongs:
        note("wrong", False, "task has no wrong implementation")
    for w in wrongs:
        r = run(["wrong/" + w])
        failed = [i for i in requested if r["ids"].get(i) == "failed"]
        note("wrong/" + w, failed and not r["infrastructure"], r["infrastructure"] or (
            "failed requested ids: " + ", ".join(failed) if failed else "no requested id failed"))
    bare = run(["reference"], hidden=False)
    note("emptied overlay", not bare["infrastructure"] and not bare["all_passed"],
         bare["infrastructure"] or ("passes without the hidden tests" if bare["all_passed"]
                                    else "does not pass without the hidden tests"))
    again = run(["reference"])
    note("determinism", again["ids"] == ref["ids"], "same result twice" if again["ids"] == ref["ids"]
         else "reference results differ between runs")
    return out


def qualify_main(argv):
    code = 0
    for task_dir in argv:
        name = os.path.basename(os.path.normpath(task_dir))
        try:
            rows = qualify(task_dir)
        except (GradeError, OSError, KeyError, tomllib.TOMLDecodeError) as e:
            rows = [("task", False, str(e))]
        for check, ok, detail in rows:
            print(f"{'ok  ' if ok else 'FAIL'} {name} {check}: {detail}")
            code = code or (0 if ok else 1)
    return code
