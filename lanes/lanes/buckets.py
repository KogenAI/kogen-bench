"""Stall rule: climb lineage (`lanes-climb-log`) and root-cause buckets of train failures (`lanes-buckets`).

Reads finished climb run directories (experiment.json, report.json, cells); never runs Kogen and never
opens a cell of the test split. The only thing it runs is the task's reference tree through the grader.
"""

import argparse
import collections
import os
import re
import sys

from lanes import common, experiment, grading

BUCKETS = ("grader_bug", "ambiguous_task", "harness_error", "model_failure")
FLAT = ("within_noise", "revert")  # a round that moved nothing worth keeping
TEXT = (".md", ".feature", ".qnt", ".lean")
STOP = {"test", "tests", "should", "the", "and", "for", "with", "case", "spec", "when"}
COVERED = 0.5  # a failing test whose name shares less than this with the task text is flagged
HARNESS_INFRA = ("final-tree.tar missing", "tree not available")


class BucketError(Exception):
    pass


def _load(run_dir):
    exp = experiment.load(os.path.join(run_dir, "experiment.json"))
    if exp.get("kind") != "climb":
        raise BucketError(f"{run_dir}: not a climb experiment")
    path = os.path.join(run_dir, "report.json")
    return exp, common.read_json(path) if os.path.isfile(path) else None


# ---- lineage ----------------------------------------------------------------------------

def lineage(run_dirs):
    """Rounds of one climb, oldest first: `{id, round, decision, case, dir}`; decision is None without report.json."""
    rounds = {}
    for d in run_dirs:
        exp, rep = _load(d)
        if exp["id"] in rounds:
            raise BucketError(f"round {exp['id']} given twice")
        verdict = (rep or {}).get("verdict") or {}
        rounds[exp["id"]] = {"id": exp["id"], "round": exp["round"], "parent": exp["parent"], "dir": d,
                             "decision": verdict.get("decision"), "case": verdict.get("case")}
    heads = [r for r in rounds.values() if not any(o["parent"] == r["id"] for o in rounds.values())]
    if len(heads) != 1:
        raise BucketError("the run directories are not one climb (one chain of parent rounds expected)")
    chain, r = [], heads[0]
    while r:
        chain.append(r)
        r = rounds.get(r["parent"])
    if len(chain) != len(rounds):
        raise BucketError("a given round is not on the parent chain of the latest round")
    return chain[::-1]


def stalled(chain, window):
    """True when the last `window` rounds all ended flat (within noise or revert); needs that many rounds."""
    last = chain[-window:]
    return len(last) == window and all(r["decision"] in FLAT for r in last)


def climb_log_main(argv):
    p = argparse.ArgumentParser(prog="lanes-climb-log", description="List a climb's rounds and say whether it stalled.")
    p.add_argument("run_dirs", nargs="+", metavar="run-dir")
    p.add_argument("--window", type=int, default=3, help="flat rounds in a row that count as a stall (2 or 3)")
    a = p.parse_args(argv)
    if a.window < 2:
        p.error("--window must be at least 2")
    try:
        chain = lineage(a.run_dirs)
    except (BucketError, experiment.ExperimentError, OSError, ValueError) as e:
        print(f"lanes-climb-log: {e}", file=sys.stderr)
        return 2
    for r in chain:
        print(f"round {r['round']}  {r['id']}  {r['decision'] or 'no report'}" + (f" [{r['case']}]" if r["case"] else ""))
    flat = 0
    for r in reversed(chain):
        if r["decision"] not in FLAT:
            break
        flat += 1
    if stalled(chain, a.window):
        print(f"STALL: the last {flat} rounds were flat (within noise or revert); bucket the train failures")
    else:
        print(f"no stall: {flat} flat round(s) at the end, {a.window} needed")
    return 0


# ---- buckets ----------------------------------------------------------------------------

def _words(name):
    name = name.rsplit("/", 1)[-1]
    parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", name)
    return [w for w in (p.lower() for p in parts) if len(w) > 2 and w not in STOP]


def _text(*paths):
    files = []
    for path in paths:
        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path):
            files += [os.path.join(r, f) for r, _, fs in os.walk(path) for f in sorted(fs)]
    out = []
    for f in files:
        if f.endswith(TEXT):
            with open(f, encoding="utf-8", errors="replace") as fh:
                out.append(fh.read())
    return "\n".join(out).lower()


def unstated(ids, text):
    """The ids whose name shares less than half its words with `text` (the task text and Intent)."""
    flagged = []
    for i in ids:
        words = _words(i)
        hit = sum(1 for w in words if w[:max(3, len(w) - 2)] in text)
        if words and hit / len(words) < COVERED:
            flagged.append(i)
    return flagged


def failures(evaluation):
    """Names of what failed in a build evaluation: test ids not passed, and commands that did not finish ok."""
    ids = [i for i, s in sorted((evaluation.get("ids") or {}).items()) if s != "passed"]
    return ids + ["command " + c["name"] for c in evaluation.get("commands") or [] if not c.get("ok", True)]


class Reference:
    """Grades each task's reference tree once (hidden tests, no model); `fn(task_dir)` returns the evaluation."""

    def __init__(self, fn=None):
        self.fn, self.cache = fn or self._grade, {}

    @staticmethod
    def _grade(task_dir):
        with grading.scratch(task_dir, "reference") as tree:
            return grading.evaluate_tree(grading.load_task(task_dir), tree)

    def __call__(self, task_dir):
        if task_dir not in self.cache:
            self.cache[task_dir] = self.fn(task_dir)
        return self.cache[task_dir]


def _intent_text(exp, task_dir, cell_dir):
    paths = [os.path.join(task_dir, "request.md")]
    if exp["phase"] == "build":
        paths.append(os.path.join(task_dir, "supplied", exp["intent_form"]))
    else:
        paths.append(os.path.join(cell_dir, "intent"))
    return _text(*paths)


def classify(exp, run_dir, row, tasks_dir, reference):
    """`(bucket, evidence)` of one train failure (`row`: a `train_failures` or train `plumbing` row)."""
    cell = row["cell"]
    task = cell.split("/")[0]
    cdir = common.cell_dir(run_dir, cell)
    task_dir = os.path.join(tasks_dir, task)
    category = row.get("category")
    if category and category != "harness":
        return "harness_error", f"plumbing {category}" + (f" ({row['outcome']})" if row.get("outcome") else "")
    if not category and row.get("class") != "incorrect":  # nothing landed: the evaluation says nothing
        return "model_failure", f"no build landed: class {row.get('class')}, outcome {row.get('outcome')}"
    path = os.path.join(cdir, "evaluation.json")
    if not os.path.isfile(path):
        return "harness_error", f"no evaluation.json; class {row.get('class')}, outcome {row.get('outcome')}"
    ev = common.read_json(path)
    infra = ev.get("infrastructure")
    if infra:
        if any(m in str(infra) for m in HARNESS_INFRA):
            return "harness_error", f"infrastructure: {infra}"
        return "grader_bug", f"grader infrastructure: {infra}"
    if category:  # plumbing harness without grader infrastructure: the harness itself failed
        return "harness_error", f"plumbing harness ({row.get('outcome')})"
    if exp["phase"] == "shape":
        n = ev.get("scenarios", 0)
        if ev.get("pass_on_reference", 0) < n:
            return "grader_bug", f"the reference holds {ev['pass_on_reference']} of {n} Intent scenarios"
        return "model_failure", (f"scenarios {n}, fail on start {ev.get('fail_on_start')}, "
                                 f"wrong caught {ev.get('wrong_caught')}/{ev.get('wrong_total')}")
    ref = reference(task_dir)
    failed = failures(ev)
    ref_failed = failed if ref.get("infrastructure") else failures(ref)  # an ungradable reference is the grader's fault
    shared = [f for f in failed if f in ref_failed]
    if shared:
        return "grader_bug", "the reference also fails: " + ", ".join(shared)
    asked = (ev.get("expected") or {}).get("requested")
    tests = [f for f in failed if not f.startswith("command ") and (not asked or f in asked)]
    flagged = unstated(tests, _intent_text(exp, task_dir, cdir))
    if flagged:
        return "ambiguous_task", "hidden test names not found in the request or Intent (human to check): " + ", ".join(flagged)
    return "model_failure", "fails " + (", ".join(failed) or "no named test") + "; the reference passes them"


def bucket_run(run_dir, tasks_dir, reference):
    """Rows `{run, cell, lane, bucket, evidence}` for the remaining train failures of one climb round."""
    exp, rep = _load(run_dir)
    if rep is None:
        raise BucketError(f"{run_dir}: report.json missing (run lanes-report first)")
    train = set(exp["split"]["train"])
    if "climb" not in rep:
        raise BucketError(f"{run_dir}: report.json has no 'climb' section (not a climb report)")
    climb = rep["climb"]
    todo = [r for r in climb["train_failures"]] + [
        r for r in climb["plumbing"] if r["split"] == "train"]
    rows = []
    for r in sorted(todo, key=lambda r: (r["cell"], r["lane"])):
        if r["cell"].split("/")[0] not in train:  # a test task never gets looked at
            continue
        bucket, evidence = classify(exp, run_dir, r, tasks_dir, reference)
        rows.append({"run": exp["id"], "cell": r["cell"], "lane": r["lane"], "bucket": bucket, "evidence": evidence})
    return rows


def render(rows):
    cell = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
    out = ["| run | cell | bucket | evidence |", "|---|---|---|---|"]
    out += [f"| {cell(r['run'])} | {cell(r['cell'])} | {r['bucket']} | {cell(r['evidence'])} |" for r in rows]
    n = collections.Counter(r["bucket"] for r in rows)
    return "\n".join(out + ["", "counts: " + ", ".join(f"{b} {n[b]}" for b in BUCKETS)]) + "\n"


def buckets_main(argv, reference=None):
    p = argparse.ArgumentParser(prog="lanes-buckets", description="Bucket the remaining train failures of a climb by root cause.")
    p.add_argument("run_dirs", nargs="+", metavar="run-dir")
    p.add_argument("--tasks", default=os.environ.get("KOGEN_LANES_TASKS"), help="private tasks folder")
    p.add_argument("--json", metavar="FILE", help="also write the rows as JSON")
    a = p.parse_args(argv)
    if not a.tasks:
        p.error("--tasks or KOGEN_LANES_TASKS is required")
    ref = reference or Reference()
    rows = []
    try:
        for d in a.run_dirs:
            rows += bucket_run(d, a.tasks, ref)
    except (BucketError, experiment.ExperimentError, grading.GradeError, OSError, KeyError, ValueError) as e:
        print(f"lanes-buckets: {e}", file=sys.stderr)
        return 2
    sys.stdout.write(render(rows))
    if a.json:
        common.write_json(a.json, {"rows": rows, "counts": dict(collections.Counter(r["bucket"] for r in rows))})
    return 0
