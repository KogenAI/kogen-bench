"""Reproduce a published lane round: check inputs against PLAN.json, rebuild, re-grade, optionally re-run."""

import argparse
import glob
import json
import os
import shutil
import sys
import tempfile

from . import common, export, plan_hashes, probe

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
        src = export.published_cell(os.path.join(rnd, "reproduce"), cell)
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


# ---- probe rounds ---------------------------------------------------------------------------

def commands_of(rnd):
    doc = common.read_json(os.path.join(rnd, "commands.json"))
    return {**doc["lanes"], **({"grader": doc["grader"]} if doc.get("grader") else {})}


def check_probe_inputs(rnd, plan, corpus):
    """Names of the published probe inputs whose hash differs from PLAN.json: the corpus and each item, every command
    file (against its own record and the PLAN), each command's sha256."""
    bad = []
    records = os.path.join(rnd, "records.jsonl")
    if os.path.isfile(records):
        want = common.sha256_file(os.path.join(rnd, "PLAN.json"))
        if any(r.get("provenance", {}).get("manifest_sha256") != want for r in common.read_jsonl(records)):
            bad.append("PLAN.json (not the file records.jsonl was written against)")
    try:
        want = plan["hashes"]["corpus"]
        got = probe.corpus_hashes(corpus, probe.load_corpus(corpus, plan["experiment"]))
        bad += [f"corpus/{i}" for i in sorted(set(want["items"]) | set(got["items"])) if got["items"].get(i) != want["items"].get(i)]
        bad += ["corpus files"] * (got["tree"] != want["tree"])
    except (probe.ProbeError, OSError) as e:
        bad.append(f"corpus ({e})")
    hashes = {**{n: plan["hashes"]["lanes"][n]["files"] for n in plan["hashes"]["lanes"]}, "grader": plan["hashes"].get("grader", {}).get("files", {})}
    plan_argv = {l["name"]: l["probe"]["command"] for l in plan["experiment"]["lanes"]}
    plan_argv["grader"] = plan["experiment"]["grader"].get("command", [])
    for name, c in commands_of(rnd).items():
        if plan_hashes.sha256_json(c["argv"]) != c["command_sha256"]:
            bad.append(f"commands.json ({name} command_sha256)")
        for i, f in c["files"].items():
            path = os.path.join(rnd, *f["path"].split("/"))
            if not os.path.exists(path) or export.hash_path(path) != f["sha256"] or f["sha256"] != hashes[name].get(i):
                bad.append(f["path"])
        bad += [f"commands.json ({name}: {why})" for why in argv_differs(c, plan_argv[name], hashes[name])]
    for lane in plan["experiment"]["lanes"]:
        path = os.path.join(rnd, "reproduce", "settings", lane["name"] + ".json")
        if os.path.isfile(path) and plan_hashes.sha256_json(common.read_json(path)) != plan["hashes"]["lanes"][lane["name"]]["settings"]:
            bad.append(os.path.relpath(path, rnd))
    return bad


def argv_differs(c, plan_argv, plan_files):
    """How a published command differs from the argv in PLAN.json: length, a literal element (a flag), an interpreter's
    name, and the argv indices PLAN hashed against the files and interpreters published."""
    if len(c["argv"]) != len(plan_argv):
        return ["argv length differs from PLAN.json"]
    out = [f"element {i} is {pub!r}, PLAN.json has {raw!r}" for i, (pub, raw) in enumerate(zip(c["argv"], plan_argv))
           if str(i) not in c["files"] and str(i) not in c["external"] and pub != raw]
    out += [f"element {i} names {e['name']!r}, PLAN.json has {raw!r}" for i, e in c["external"].items()
            for raw in [plan_argv[int(i)]] if raw != e["name"] and "[redacted]" not in raw and os.path.basename(raw) != e["name"]]
    got = set(c["files"]) | {i for i, e in c["external"].items() if e.get("sha256")}
    if got != set(plan_files):
        out.append("published files and interpreters do not cover the elements PLAN.json hashed")
    return out


def executable(name):
    """An interpreter or tool the command named by an absolute path: the same name on this machine's PATH."""
    return shutil.which(name) or (sys.executable if name.startswith("python") else name)


def local_argv(rnd, c, folder):
    """A published command made runnable: its files copied next to the experiment file, other elements as published."""
    out = []
    for i, a in enumerate(c["argv"]):
        if str(i) in c["files"]:
            src, dest = os.path.join(rnd, *a.split("/")), os.path.join(folder, *a.split("/"))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copytree(src, dest) if os.path.isdir(src) else shutil.copyfile(src, dest)
        out.append(executable(a) if str(i) in c["external"] else a)
    return out


def write_probe_experiment(rnd, plan, work):
    folder, cmds = os.path.join(work, "exp"), commands_of(rnd)
    exp = json.loads(json.dumps(plan["experiment"]))
    for lane in exp["lanes"]:
        lane["probe"]["command"] = local_argv(rnd, cmds[lane["name"]], folder)
    if "grader" in cmds:
        exp["grader"]["command"] = local_argv(rnd, cmds["grader"], folder)
    common.write_json(os.path.join(folder, "experiment.json"), exp)
    return os.path.join(folder, "experiment.json")


def regrade_probe(rnd, cells, corpus, exp_path):
    """Re-grade every published output from `reproduce/cells/<cell>/output.json`; names of cells whose metrics differ."""
    from . import experiment
    exp = experiment.load(exp_path)
    items, lanes, bad = probe.load_corpus(corpus, exp), {l["name"]: l for l in exp["lanes"]}, []
    base = os.path.dirname(exp_path)
    grader = exp["grader"]
    if grader["kind"] == "command":
        grader = {**grader, "command": probe.resolve(grader["command"], base)}
    for cell, (_, want) in sorted(cells.items()):
        item, _, lane = cell.split("/")
        path = os.path.join(export.published_cell(os.path.join(rnd, "reproduce"), cell), "output.json")
        if not os.path.isfile(path):
            bad.append(f"reproduce/cells/{cell} (output not published)")
            continue
        try:
            got = probe.grade(grader, items[item], common.read_json(path), lanes[lane])
        except (probe.ProbeError, KeyError) as e:
            bad.append(f"{cell} (could not be graded: {e})")
            continue
        if got != want["metrics"]:
            bad.append(f"{cell}: re-grade differs in metrics")
    return bad


def probe_lanes_without_usage(cells):
    """Lanes whose every published cell ran no model: `lanes-run` can repeat them exactly."""
    by = {}
    for cell, (attempt, _) in cells.items():
        by.setdefault(attempt["lane"], []).append(not attempt.get("usage"))
    return sorted(l for l, flags in by.items() if all(flags))


def rerun_outcome(run, cell):
    """The rerun cell's outcome from result.json (a cell that failed has no evaluation.json)."""
    try:
        return common.read_json(os.path.join(common.cell_dir(run, cell), "result.json"))["outcome"]
    except (OSError, KeyError):
        return "did not finish"


def rerun_probe(plan, cells, exp_path, corpus, step0, n, work, home):
    """Run the cells of the step-0 lanes (all) and the first `n` of every other lane; step-0 metrics must equal the
    published ones exactly. Returns the cells that differ."""
    run = os.path.join(work, "rerun")
    if tool("lanes-plan", [exp_path, "--run-dir", run, "--corpus", corpus], home):
        return ["lanes-plan failed"]
    seen, chosen = {}, []
    for row in common.read_jsonl(os.path.join(run, "plan.jsonl")):
        seen[row["lane"]] = seen.get(row["lane"], 0) + 1
        if row["cell"] in cells and (row["lane"] in step0 or seen[row["lane"]] <= n):
            chosen.append(row)
    bad = []
    for row in chosen:
        cell = row["cell"]
        tool("lanes-cell", [run, cell, "--corpus", corpus], home)
        state, mine = rerun_outcome(run, cell), load_rerun(run, cell)
        (_, want), exact = cells[cell], row["lane"] in step0
        if state != "ok" or not mine:
            say(f"  {cell}: rerun {state}")
            if exact:
                bad.append(f"{cell} (rerun {state})")
            continue
        same = mine[1].get("metrics") == want["metrics"]
        say(f"  {cell}: metrics {'match' if same else 'DIFFER'}{'' if exact else ' (model lane: not expected to match)'}")
        if exact and not same:
            bad.append(f"{cell}: rerun metrics differ")
    return bad


def say_external(rnd):
    """The interpreters are not hashed or copied: say which version runs here against the published one."""
    for name, c in commands_of(rnd).items():
        for e in c["external"].values():
            if not os.path.isabs(executable(e["name"])):
                say(f"external {name}: {e['name']} is not on this machine's PATH (published {e['version']!r}); a rerun that runs it fails")
                continue
            here = export.tool_version(executable(e["name"]))
            say(f"external {name}: {e['name']} {'version matches the published one' if here == e['version'] else 'version differs'}"
                f" (published {e['version']!r}, here {here!r}); not checked against PLAN.json")


def reproduce_probe(rnd, plan, n, corpus, keep):
    bad = check_probe_inputs(rnd, plan, corpus)
    if bad:
        for b in bad:
            say(f"MISMATCH {b}")
        say("inputs: published files differ from PLAN.json")
        return 1
    say("inputs: every published input matches PLAN.json")
    say_external(rnd)
    work = tempfile.mkdtemp(prefix="lanes-reproduce-")
    home = os.path.join(work, "home")
    try:
        exp_path = write_probe_experiment(rnd, plan, work)
        cells = published_cells(rnd)
        if not cells:
            say("MISMATCH no published cells in bundles/")
            return 1
        bad = regrade_probe(rnd, cells, corpus, exp_path)
        say(f"regrade: {len(cells) - len(bad)} of {len(cells)} cells match the published metrics")
        step0 = probe_lanes_without_usage(cells)
        say(f"rerun: lanes without model usage {', '.join(step0) or 'none'}" + (f"; the first {n} cell(s) of the others" if n else ""))
        bad += rerun_probe(plan, cells, exp_path, corpus, step0, n, work, home)
        for b in bad:
            say(f"MISMATCH {b}")
        say(f"summary: inputs match; {'re-grades and step-0 reruns match' if not bad else 'RESULTS DIFFER'}")
        return 0 if not bad else 1
    finally:
        if keep:
            say(f"kept {work}")
        else:
            shutil.rmtree(work, ignore_errors=True)


def reproduce(rnd, n=0, hosts_file=None, tasks=None, repo=None, keep=False, corpus=None):
    rnd = os.path.abspath(rnd)
    plan0 = common.read_json(os.path.join(rnd, "PLAN.json"))
    if plan0["experiment"]["phase"] == "probe":
        return reproduce_probe(rnd, plan0, n, os.path.abspath(corpus or os.path.join(rnd, "reproduce", "corpus")), keep)
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
    p.add_argument("--corpus", help="probe corpus folder (default: <round>/reproduce/corpus)")
    p.add_argument("--kogen-repo", help="Kogen repository to build from (default: the experiment's)")
    p.add_argument("--keep", action="store_true", help="keep the work folder")
    a = p.parse_args(argv)
    try:
        return reproduce(a.round, a.rerun, a.hosts, a.tasks, a.kogen_repo, a.keep, a.corpus)
    except (OSError, ValueError, KeyError) as e:
        print(f"reproduce: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
