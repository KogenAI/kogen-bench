"""Hidden-test grading, shape grading and task qualification (the Lab's evaluate and qualify)."""

import contextlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import tomllib

from . import cell, common, experiment, preflight

GRADE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "grade")
ADAPTERS_DIR = os.path.join(GRADE_DIR, "adapters")  # `$KOGEN_LAB_ADAPTERS`: files evaluate.toml commands load
SETUP_DEADLINE_S = 600
# Host variables the toolchains need; nothing else (no tokens) reaches agent-written code.
GO_VARS = frozenset(("GOPATH", "GOCACHE", "GOFLAGS", "GOMODCACHE", "GOPROXY", "GOROOT", "GOTOOLCHAIN",
                     "GOOS", "GOARCH", "GOMAXPROCS", "GOENV", "GONOPROXY", "GONOSUMDB", "GONOSUMCHECK",
                     "GOPRIVATE", "GOSUMDB", "GOINSECURE", "GOVCS", "GOWORK", "GOAMD64", "GOARM",
                     "GOEXPERIMENT", "GODEBUG", "GOTMPDIR", "GOTELEMETRY", "GOTELEMETRYDIR", "GOFIPS140",
                     "GOCACHEPROG", "GOEXE", "GOHOSTOS", "GOHOSTARCH", "GOTOOLDIR", "GOMEMLIMIT", "GOGC",
                     "CGO_ENABLED", "CGO_CFLAGS", "CGO_CPPFLAGS", "CGO_CXXFLAGS", "CGO_LDFLAGS"))
ENV_PREFIXES = ("MIX_", "HEX_", "NODE_", "NPM_CONFIG_", "npm_config_")
# The acceptance runner's own variables (a task's `[acceptance] run` line uses them), by exact name: no `KOGEN_` prefix.
RUNNER_VARS = frozenset(("KOGEN_CUCUMBER", "KOGEN_NODE"))
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


def fresh_export(tree):
    """Make `tree` a fresh export: delete every file the tree's own `.gitignore` files ignore.

    Task trees are laid by copying folders, so a build output that a `.gitignore` hides (the `./run` of a
    Go task) can sit in the tree and mask a missing build step; Kogen's own verification starts from the
    tracked files only. Git decides what is ignored, with the user's and the system's git config left out
    so the answer is the same on every host. Returns the removed paths, relative to `tree`.
    """
    git_dir = tempfile.mkdtemp(prefix="export-", dir=os.path.dirname(tree))
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    try:
        for cmd in (["init", "-q", "--bare", git_dir],
                    ["--git-dir", git_dir, "--work-tree", tree, "ls-files", "-z", "--others", "--ignored",
                     "--exclude-standard"]):
            try:
                r = subprocess.run(["git", *cmd], capture_output=True, env=env, timeout=120)
            except (OSError, subprocess.TimeoutExpired) as e:
                raise GradeError(f"cannot export a fresh tree: {e}")
            if r.returncode:
                raise GradeError("cannot export a fresh tree: " + r.stderr.decode(errors="replace").strip())
        removed = [p for p in r.stdout.decode("utf-8", "surrogateescape").split("\0") if p]
    finally:
        shutil.rmtree(git_dir, ignore_errors=True)
    for rel in removed:
        path = os.path.join(tree, rel)
        os.remove(path)
        parent = os.path.dirname(path)
        while parent != tree and not os.listdir(parent):  # drop the folders that held only ignored files
            os.rmdir(parent)
            parent = os.path.dirname(parent)
    return removed


@contextlib.contextmanager
def scratch(task_dir=None, *overlays, export=False):
    """A fresh grading dir under `$KOGEN_LANES_HOME/tmp`; yields its `tree/` (`start/` with the
    overlay folders, e.g. `reference`, laid over it when `task_dir` is given; with `export` the
    ignored files are then removed, see `fresh_export`). Removed on exit."""
    base = os.path.join(common.lanes_home(), "tmp")
    os.makedirs(base, exist_ok=True)
    root = tempfile.mkdtemp(prefix="grade-", dir=base)
    tree = os.path.join(root, "tree")
    try:
        os.makedirs(tree)
        if task_dir:
            for sub in ("start",) + overlays:
                lay(os.path.join(task_dir, sub), tree)
            if export:
                fresh_export(tree)
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
    """The Lab's `commandEnv`: toolchain variables, the acceptance runner variables, HOME, PATH, LANG, `KOGEN_LAB_ADAPTERS`, the task `env`, and a private
    TMPDIR next to the tree."""
    env = {k: v for k, v in os.environ.items() if k in GO_VARS or k in RUNNER_VARS or k.startswith(ENV_PREFIXES)}
    env.update(HOME=os.environ.get("HOME", "/"), PATH=os.environ.get("PATH", "/usr/bin:/bin"),
               LANG=os.environ.get("LANG", "C.UTF-8"))
    env.update({k: str(v) for k, v in task["task"].get("env", {}).items()})
    tmp = os.path.join(os.path.dirname(tree), "tmp")
    os.makedirs(tmp, exist_ok=True)
    env["TMPDIR"] = tmp
    env["KOGEN_LAB_ADAPTERS"] = ADAPTERS_DIR
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
    try:
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
    except (KeyError, IndexError, TypeError, ValueError):  # an id the report does not resolve: report_invalid
        return None
    return out or None


def feature_lines(path):
    """Line numbers of the scenarios in a feature file, as `read_report` keys them: each `Scenario:`
    and each data row of an `Examples:` block (not its header row). Rows of a step data table or of a
    Background are not scenarios: a block ends at any line that is not a table row."""
    lines, rows, header, doc = [], False, False, False
    with open(path, encoding="utf-8") as f:
        for n, raw in enumerate(f, 1):
            line = raw.strip()
            if line.startswith(('"""', "```")):
                doc, rows = not doc, False
            elif doc or not line or line.startswith("#"):
                continue
            elif line.startswith("|"):
                if rows and header:
                    header = False
                elif rows:
                    lines.append(str(n))
            elif re.match(r"(Examples|Scenarios)\s*:", line):
                rows, header = True, True
            else:
                rows = False
                if re.match(r"(Scenario|Example)\s*:", line):
                    lines.append(str(n))
    return lines


def shape_tree(task, overlays, intent, slug, step_files, deadline_s, export=False):
    """Run the task's acceptance runner on one tree with the shaped Intent's scenarios and steps.

    Returns `{line: status}` or `{"infrastructure": reason}` (setup failed, or the runner wrote no
    usable report: a runner error is not a failed scenario). `export` starts from a fresh export (see `fresh_export`).
    """
    acc = task["task"]["acceptance"]
    with scratch(task["dir"], *overlays, export=export) as tree:
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
    (those in the Intent's feature), `pass_on_reference`, `fail_on_start` (scenarios not passing
    on start); `wrong_caught` counts wrong trees where some scenario does not pass, of `wrong_total`.
    A tree whose run gave no report is `infrastructure` and no counts are written.
    """
    rec = {"phase": "shape", "infrastructure": None}
    intent = os.path.join(cell, "intent")
    if not task["task"].get("acceptance") or not all(
            os.path.isfile(os.path.join(intent, n)) for n in ("intent.md", "acceptance.feature")):
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
    wanted = feature_lines(os.path.join(intent, "acceptance.feature"))  # the Intent's scenarios, not the run's
    rec.update(scenarios=len(wanted), pass_on_reference=sum(ref.get(line) == "passed" for line in wanted),
               fail_on_start=sum(start.get(line) != "passed" for line in wanted),
               wrong_caught=sum(any(rec["matrix"]["wrong/" + w].get(line) != "passed" for line in wanted)
                                for w in wrong),
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
        # The entry for `first_green_tree` (the first green `pass` tree, before any review edit) says so.
        rec["pass_trees"] = []
        first = result.get("first_green_tree")
        for tree in result.get("pass_trees") or []:
            p = os.path.join(d, "pass-trees", str(tree) + ".tar")
            sub = grade_archive(task, p, deadline_s) if os.path.isfile(p) else {"ungraded": "tree not available"}
            rec["pass_trees"].append(dict(sub, tree=tree, **({"first_green": True} if first and tree == first else {})))
    common.write_json(os.path.join(d, "evaluation.json"), rec)
    return rec


def finished_cells(run_dir):
    base = os.path.join(run_dir, "cells")
    return sorted(os.path.relpath(r, base) for r, _, f in os.walk(base) if "result.json" in f)


# --- qualification -----------------------------------------------------------------------------

def qualify(task_dir, kogen=None):
    """The Lab's qualification rules (`steps.go`); returns a list of `(check, ok, detail)`.

    Every tree runs from a fresh export (ignored files removed), and the `acceptance` check runs the supplied
    Intent's scenarios on the reference with the task's own setup only, so a missing build step cannot hide.

    Not ported: repeating start and reference three times (determinism compares two reference
    runs), second implementations, the killed-evaluator check and `[expected]` inference.

    The `intent` check lint-approves the supplied Intent with Kogen (`kogen`, else `$KOGEN_BIN`); it is
    skipped, as ok, when neither names a Kogen.
    """
    task, out = load_task(task_dir), []
    exp = task["eval"].get("expected", {})
    requested, regression = exp.get("requested", []), exp.get("regression", [])

    def run(overlays, hidden=True):
        with scratch(task_dir, *overlays, export=True) as tree:  # a fresh export: ignored build outputs cannot mask a step
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
    note("acceptance", *qualify_acceptance(task))
    for check, ok, detail in qualify_intent(task, kogen):
        note(check, ok, detail)
    again = run(["reference"])
    note("determinism", again["ids"] == ref["ids"], "same result twice" if again["ids"] == ref["ids"]
         else "reference results differ between runs")
    return out


def qualify_acceptance(task):
    """Run the supplied Intent's scenarios on the reference as Kogen's verification does: a fresh export, the
    task `setup`, then the task's acceptance command (the evaluator's own setup does not run, so a build
    that only the evaluator performs is caught). Returns `(ok, detail)`; skipped, as ok, when the task has no
    report-writing `[acceptance]`, no supplied Gherkin Intent, or needs a `$KOGEN_*` runner variable the host lacks.
    """
    acc, form = task["task"].get("acceptance"), os.path.join(task["dir"], "supplied", "gherkin")
    if not acc or "KOGEN_ACCEPTANCE_REPORT" not in acc.get("run", "") or not os.path.isfile(
            os.path.join(form, "intent.md")) or not os.path.isfile(os.path.join(form, "acceptance.feature")):
        return True, "skipped: no acceptance command that writes a report, or no supplied Gherkin Intent"
    absent = sorted(v for v in set(re.findall(r"\$\{?(KOGEN_[A-Z_]+)", acc["run"]))
                    if not v.startswith("KOGEN_ACCEPTANCE_") and v not in os.environ)
    if absent:
        return True, "skipped: needs " + ", ".join(absent) + " in the environment"
    intent = os.path.join(form, "intent.md")
    try:
        listed = intent_steps(intent)
        found = {p: os.path.join(form, p) for p in listed if os.path.isfile(os.path.join(form, p))}
        if not listed or len(found) < len(listed):
            return False, "step files not available: " + ", ".join(
                [p for p in listed if p not in found] or ["none listed"])
        got = shape_tree(task, ["reference"], form, intent_slug(intent), found, 600, export=True)
    except GradeError as e:
        return False, str(e)
    if "infrastructure" in got:
        return False, got["infrastructure"]
    wanted = feature_lines(os.path.join(form, "acceptance.feature"))
    bad = [line for line in wanted if got.get(line) != "passed"]
    if not wanted or bad:
        return False, ("no scenarios in the supplied feature" if not wanted else
                       "reference does not pass supplied scenarios at line " + ", ".join(bad))
    return True, f"reference passes all {len(wanted)} supplied scenarios from a fresh export"


def qualify_intent(task, kogen=None):
    """Ask Kogen whether each supplied Intent is acceptable, as `lanes-preflight` will: install it in a scratch
    workspace and run `kogen intent approve <slug>` (twice, the second time with the printed hash), within the
    task's `approve_timeout_s`. Runs `gherkin` (always) and every other form the task supplies. Returns
    `(check, ok, detail)` rows: `intent`, then `intent/<form>`; one skipped row, as ok, when `kogen` (a Kogen
    executable, a folder or a release archive) and `$KOGEN_BIN` are both missing.
    """
    kogen = kogen or os.environ.get("KOGEN_BIN")
    if not kogen:
        return [("intent", True, "skipped: needs --kogen or KOGEN_BIN in the environment")]
    forms = ["gherkin"] + [f for f in experiment.INTENT_FORMS[1:]
                           if os.path.isfile(os.path.join(task["dir"], "supplied", f, "intent.md"))]
    rows = []
    for form in forms:
        check = "intent" if form == "gherkin" else "intent/" + form
        try:
            slug = task["task"].get("name")
            if not isinstance(slug, str) or not cell.SLUG.match(slug) or not 3 <= len(slug) <= 48:
                raise cell.CellError(f"task.toml name {slug!r} is not a Kogen slug")
            supplied = os.path.join(task["dir"], "supplied", form)
            cell.check_supplied(supplied, slug)
            deadline_s = cell.approve_timeout(task["task"], preflight.DEADLINE_S)
            binary = cell.resolve_kogen(None, "qualify", kogen)
            config = cell.project_yaml(task["task"], None)
            root = cell.release_root(binary)  # as a cell does: the Go Kogen's readiness needs <root>/node-path
            if root:
                cell.ensure_node_path(root)
            rows.append((check, *preflight.approve_supplied(task["dir"], slug, supplied, binary, config, deadline_s)))
        except (OSError, ValueError, cell.CellError) as e:
            rows.append((check, False, str(e)))
    return rows


def qualify_main(argv):
    kogen, tasks, i = None, [], 0
    while i < len(argv):
        if argv[i] == "--kogen":
            if i + 1 == len(argv):
                print("lanes-qualify: --kogen needs a path", file=sys.stderr)
                return 2
            kogen, i = argv[i + 1], i + 2
        elif argv[i].startswith("--kogen=") and len(argv[i]) > 8:
            kogen, i = argv[i][8:], i + 1
        else:
            tasks.append(argv[i])
            i += 1
    code = 0
    for task_dir in tasks:
        name = os.path.basename(os.path.normpath(task_dir))
        try:
            rows = qualify(task_dir, kogen)
        except (GradeError, OSError, KeyError, tomllib.TOMLDecodeError) as e:
            rows = [("task", False, str(e))]
        for check, ok, detail in rows:
            print(f"{'ok  ' if ok else 'FAIL'} {name} {check}: {detail}")
            code = code or (0 if ok else 1)
    return code
