"""Reproduce a published lane round: check inputs against PLAN.json, rebuild, re-grade, optionally re-run."""

import argparse
import glob
import json
import os
import shutil
import sys
import tempfile

from . import common, export, plan_hashes

BIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin")
DEADLINE_S = 7200
SKIP = ("commands", "grader_version")  # command wall times and the grader's version are not results
TASK_FILES = {"task": "", "tree": "/start", "hidden_tests": "/evaluator", "task_toml": "/task.toml", "request": "/request.md"}


def say(text):
    print(text, flush=True)


def tool(name, args, home):
    """Run a lanes entry point in its own process group; its output goes to stderr."""
    code, timed_out = common.run([sys.executable, os.path.join(BIN, name), *args], env=dict(os.environ, KOGEN_LANES_HOME=home),
                                 deadline_s=DEADLINE_S, stdout=sys.stderr, stderr=sys.stderr)
    return 124 if timed_out else code


def patch_copy(rnd, lane):
    return os.path.join(rnd, "patches", lane["name"], os.path.basename(lane["patch"]))


def check_inputs(rnd, plan, tasks):
    """Names of the published files whose hash differs from PLAN.json."""
    bad, exp = [], plan["experiment"]
    records = os.path.join(rnd, "records.jsonl")
    if os.path.isfile(records):
        want = common.sha256_file(os.path.join(rnd, "PLAN.json"))
        if any(r.get("provenance", {}).get("manifest_sha256") != want for r in common.read_jsonl(records)):
            bad.append("PLAN.json (not the file records.jsonl was written against)")
    for task, want in plan["hashes"]["tasks"].items():
        try:
            got = plan_hashes.task_hashes(os.path.join(tasks, task), exp["phase"], exp.get("intent_form"))
        except plan_hashes.PlanError as e:
            bad.append(f"tasks/{task} ({e})")
            continue
        bad += [f"tasks/{task}{rel}" for k, rel in TASK_FILES.items() if got[k] != want[k]]
        bad += [f"tasks/{task}/supplied/{f}" for f in sorted(set(want["intents"]) | set(got["intents"]))
                if got["intents"].get(f) != want["intents"].get(f)]
    for lane in exp["lanes"]:
        want = plan["hashes"]["lanes"][lane["name"]]
        if lane["patch"]:
            path = patch_copy(rnd, lane)
            if not os.path.isfile(path) or common.sha256_file(path) != want["patch"]:
                bad.append(os.path.relpath(path, rnd))
        path = os.path.join(rnd, "reproduce", "settings", lane["name"] + ".json")
        if not os.path.isfile(path) or plan_hashes.sha256_json(common.read_json(path)) != want["settings"]:
            bad.append(os.path.relpath(path, rnd))
    return bad


def write_experiment(rnd, plan, work, hosts, repo):
    exp = dict(plan["experiment"], hosts=hosts)
    if repo:
        exp["kogen"] = {"repo": repo}
    for lane in exp["lanes"]:
        if lane["patch"]:
            dest = os.path.join(work, lane["patch"])
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copyfile(patch_copy(rnd, lane), dest)
    common.write_json(os.path.join(work, "experiment.json"), exp)
    return os.path.join(work, "experiment.json")


def rebuild(plan, exp_path, run, home):
    """Build every lane; returns (built ok, lanes whose artifact hash differs from PLAN.json)."""
    if tool("lanes-build", [exp_path, "--run-dir", run], home):
        say("rebuild: lanes-build failed")
        return False, []
    differs = []
    for entry in common.read_json(os.path.join(run, "lanes.lock.json")):
        want = plan["lock"]["artifacts"][entry["name"]]
        same = entry["artifact_sha256"] == want
        say(f"artifact {entry['name']}: {'matches' if same else 'DIFFERS (built ' + entry['artifact_sha256'][:12] + ', published ' + want[:12] + ')'}")
        if not same:
            differs.append(entry["name"])
    return True, differs


def published_cells(rnd):
    """`{cell: (attempt, evaluation)}` from the round's bundle."""
    out = {}
    for path in sorted(glob.glob(os.path.join(rnd, "bundles", "*", "attempts", "*", "*", "*", "a1", "attempt.json"))):
        attempt = common.read_json(path)
        out[attempt["cell"]] = (attempt, common.read_json(os.path.join(os.path.dirname(path), "evaluation.json")))
    return out


def regrade(rnd, cells, tasks, work, home):
    """Re-grade the published final trees with lanes-grade (no model calls); names of cells that differ."""
    run, bad, missing = os.path.join(work, "grade"), [], set()
    for cell, (attempt, _) in cells.items():
        src = os.path.join(rnd, "reproduce", "cells", *cell.split("/"))
        if not os.path.isdir(src):
            bad.append(f"reproduce/cells/{cell} (final tree not published)")
            missing.add(cell)
            continue
        dest = common.cell_dir(run, cell)
        shutil.copytree(src, dest)
        if os.path.exists(os.path.join(dest, "evaluation.json")):
            os.remove(os.path.join(dest, "evaluation.json"))
        common.write_json(os.path.join(dest, "result.json"), attempt)
    tool("lanes-grade", [run, "--tasks", tasks], home)
    for cell, (_, want) in cells.items():
        path = os.path.join(common.cell_dir(run, cell), "evaluation.json")
        if cell in missing:
            continue
        if not os.path.isfile(path):
            bad.append(f"{cell} (could not be graded)")
            continue
        got = export.scrub(common.read_json(path), [])
        diff = [k for k in export.EVAL_KEYS if k not in SKIP and got.get(k) != want.get(k)]
        if diff:
            bad.append(f"{cell}: re-grade differs in {', '.join(diff)}")
    return bad


def rerun(plan, cells, exp_path, built_run, tasks, hosts_file, n, work, home):
    """Run the first `n` planned cells of each lane with the reader's own login; print them next to the published ones."""
    run = os.path.join(work, "rerun")
    os.makedirs(run)
    shutil.copyfile(os.path.join(built_run, "lanes.lock.json"), os.path.join(run, "lanes.lock.json"))
    if tool("lanes-plan", [exp_path, "--run-dir", run, "--tasks", tasks], home):
        return False
    rows, seen = [], {}
    for row in common.read_jsonl(os.path.join(run, "plan.jsonl")):
        seen[row["lane"]] = seen.get(row["lane"], 0) + 1
        if seen[row["lane"]] <= n:
            rows.append(row)
    with open(os.path.join(run, "plan.jsonl"), "w", encoding="utf-8") as f:
        f.writelines(json.dumps(r, sort_keys=True) + "\n" for r in rows)
    ok = tool("lanes-run", [run, "--tasks", tasks, "--hosts", hosts_file], home) == 0
    ok = tool("lanes-grade", [run, "--tasks", tasks], home) == 0 and ok
    say("rerun (a new model run: results differ from run to run, so these are not expected to match):")
    for row in rows:
        cell, parts = row["cell"], []
        for label, side in (("published", cells.get(cell)), ("rerun", load_rerun(run, cell))):
            att, ev = side or (None, None)
            parts.append(f"{label} {export.outcome_of(ev) if ev else '-'} wall {att.get('wall_s') if att else '-'}s "
                         f"cost {(att.get('totals') or {}).get('cost_usd') if att else '-'}")
        say(f"  {cell}: " + " | ".join(parts))
    return ok


def load_rerun(run, cell):
    d = common.cell_dir(run, cell)
    try:
        return common.read_json(os.path.join(d, "result.json")), common.read_json(os.path.join(d, "evaluation.json"))
    except OSError:
        return None


def reproduce(rnd, n=0, hosts_file=None, tasks=None, repo=None, keep=False):
    rnd = os.path.abspath(rnd)
    tasks = tasks or os.path.join(rnd, "reproduce", "tasks")
    plan = common.read_json(os.path.join(rnd, "PLAN.json"))
    bad = check_inputs(rnd, plan, tasks)
    if bad:
        for b in bad:
            say(f"MISMATCH {b}")
        say("inputs: published files differ from PLAN.json")
        return 1
    say("inputs: every published input matches PLAN.json")
    hosts = ["local"]
    if n and hosts_file:
        hosts = sorted(common.read_json(hosts_file))
    work = tempfile.mkdtemp(prefix="lanes-reproduce-")
    home = os.path.join(work, "home")
    try:
        exp_path = write_experiment(rnd, plan, work, hosts, repo)
        built_run = os.path.join(work, "built")
        built, differs = rebuild(plan, exp_path, built_run, home)
        cells = published_cells(rnd)
        bad = regrade(rnd, cells, tasks, work, home) if cells else ["no published cells in bundles/"]
        for b in bad:
            say(f"MISMATCH {b}")
        say(f"regrade: {len(cells) - len(bad)} of {len(cells)} cells match the published grades")
        ok = built and not bad
        if n and built:
            hf = hosts_file or os.path.join(work, "hosts.json")
            if not hosts_file:
                common.write_json(hf, {"local": {"target": "local", "slots": 1}})
            ok = rerun(plan, cells, exp_path, built_run, tasks, hf, n, work, home) and ok
        say(f"summary: inputs match; {'artifacts: ' + str(len(differs)) + ' differ (a different toolchain can do that)' if built else 'REBUILD FAILED'}; "
            f"{'re-grades match' if not bad else 'RE-GRADES DIFFER'}")
        return 0 if ok else 1
    finally:
        if keep:
            say(f"kept {work}")
        else:
            shutil.rmtree(work, ignore_errors=True)


def main(argv=None):
    p = argparse.ArgumentParser(description="Reproduce a published lane round.")
    p.add_argument("round", help="<kogen-bench>/rounds/<id>")
    p.add_argument("--rerun", type=int, default=0, metavar="N", help="re-run N cells per lane with your own provider login")
    p.add_argument("--hosts", help="hosts file for --rerun (default: this machine, one slot)")
    p.add_argument("--tasks", help="task folders (default: <round>/reproduce/tasks)")
    p.add_argument("--kogen-repo", help="Kogen repository to build from (default: the experiment's)")
    p.add_argument("--keep", action="store_true", help="keep the work folder")
    a = p.parse_args(argv)
    try:
        return reproduce(a.round, a.rerun, a.hosts, a.tasks, a.kogen_repo, a.keep)
    except (OSError, ValueError, KeyError) as e:
        print(f"reproduce: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
