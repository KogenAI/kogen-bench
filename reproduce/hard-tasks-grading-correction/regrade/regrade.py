"""regrade.py <out dir> <runs dir> <cohort>=<tasks dir> ...: regrade the kept final trees of hard-task cohorts with the
preflight8 grader (PYTHONPATH=<preflight8>/repo/lanes). No model calls; never writes into a run dir.

A tree is kept when the cell has `final-tree.tar`, or (bare agent arms) `final.diff` with `start_commit`/`final_tree`
in result.json: the start workspace is rebuilt as lanes_bare.make_bare_workspace builds it, its commit must equal
`start_commit`, final.diff is applied and the tree must equal `final_tree`; otherwise the cell is `tree_mismatch`, not
graded. Grading is the HK public oracle every cohort used (supplied scenarios and steps laid in the scratch, as the
supports' `hk_public_grade_archive`) over preflight8's `evaluate_tree`. KOGEN_CUCUMBER and KOGEN_NODE come from the
environment (the cohort's Kogen release, recorded). One cell at a time; before each cell, waits while delivery heavy
commands (`work.noindex/heavy-cmds/`) exist on the host. Writes <out>/<cohort>/<task>/<rep>/<arm>.json and summary.jsonl.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

from lanes import cell as lcell, grading

IDENTITY, START_DATE = lcell.IDENTITY, lcell.START_DATE


def git(ws, *args, env, check=True):
    r = subprocess.run(["git", "-C", ws, *args], capture_output=True, text=True, env=env)
    if check and r.returncode:
        raise RuntimeError(f"git {args[0]}: {r.stderr.strip()[:300]}")
    return r.stdout.strip()


def rebuild(task_dir, tt, diff, start_commit, final_tree, work):
    """start/ + supplied gherkin (lanes_bare.make_bare_workspace), committed as Start; apply final.diff; archive."""
    ws = os.path.join(work, "ws")
    shutil.copytree(os.path.join(task_dir, "start"), ws, symlinks=True)
    supplied = os.path.join(task_dir, "supplied", "gherkin")
    steps = (tt.get("acceptance") or {}).get("steps_dir") or "features/steps"
    feature = os.path.join(os.path.dirname(steps) or "features", "acceptance.feature")
    for dirpath, _, names in os.walk(supplied):
        for name in names:
            src = os.path.join(dirpath, name)
            rel = os.path.relpath(src, supplied)
            if rel == "intent.md" or (os.sep not in rel and rel.startswith("model.")):
                continue
            dst = os.path.join(ws, feature if rel == "acceptance.feature" else rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
    env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
           "XDG_CONFIG_HOME": os.path.join(work, "xdg"),
           "GIT_AUTHOR_NAME": IDENTITY["name"], "GIT_AUTHOR_EMAIL": IDENTITY["email"],
           "GIT_COMMITTER_NAME": IDENTITY["name"], "GIT_COMMITTER_EMAIL": IDENTITY["email"],
           "GIT_AUTHOR_DATE": START_DATE, "GIT_COMMITTER_DATE": START_DATE}
    git(ws, "init", "-q", "--initial-branch=main", env=env)
    with open(os.path.join(ws, ".git", "config"), "a") as config:
        config.write("\n[user]\n\tname = " + IDENTITY["name"] + "\n\temail = " + IDENTITY["email"] +
                     "\n[commit]\n\tgpgsign = false\n[core]\n\thooksPath = " + os.devnull + "\n")
    with open(os.path.join(ws, ".git", "info", "exclude"), "a") as f:
        f.write("/.claude/\n/.codex/\n/.agents/\n/AGENTS.md" + ".local\n")  # as lanes_bare writes it
    git(ws, "add", "-A", env=env)
    git(ws, "commit", "-q", "-m", "Start", env=env)
    got_start = git(ws, "rev-parse", "HEAD", env=env)
    if got_start != start_commit:
        return None, f"start commit {got_start[:12]} != recorded {start_commit[:12]}"
    if os.path.getsize(diff) > 1:
        git(ws, "apply", "--binary", "--whitespace=nowarn", os.path.abspath(diff), env=env)
    git(ws, "add", "-A", env=env)
    git(ws, "commit", "-q", "-m", "Agent work", "--allow-empty", env=env)
    got_tree = git(ws, "rev-parse", "HEAD^{tree}", env=env)
    if got_tree != final_tree:
        return None, f"rebuilt tree {got_tree[:12]} != recorded final_tree {final_tree[:12]}"
    tar = os.path.join(work, "final-tree.tar")
    git(ws, "archive", "--format=tar", "-o", tar, "HEAD", env=env)
    return tar, None


def hk_public_grade(task, tar):
    """The supports' hk_public_grade_archive, over this release's evaluate_tree."""
    with grading.scratch() as tree:
        grading.extract(tar, tree)
        supplied = os.path.join(task["dir"], "supplied", "gherkin")
        acc = task["task"].get("acceptance") or {}
        steps = os.path.join(tree, acc.get("steps_dir", "features/steps"))
        shutil.rmtree(steps, ignore_errors=True)
        for dirpath, _, names in os.walk(supplied):
            for name in names:
                src = os.path.join(dirpath, name)
                rel = os.path.relpath(src, supplied)
                if rel == "intent.md" or (os.sep not in rel and rel.startswith("model.")):
                    continue
                if rel == "acceptance.feature":
                    targets = [os.path.join(tree, ".kogen", "intents", task["task"]["name"], "acceptance.feature"),
                               os.path.join(os.path.dirname(steps), "acceptance.feature")]
                else:
                    targets = [os.path.join(tree, rel)]
                for target in targets:
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    shutil.copyfile(src, target)
        rec = grading.evaluate_tree(task, tree)
        rec["hk_public_oracle"] = "restored qualified public scenarios and steps in grading scratch; evaluator unchanged"
        return rec


def must_wait():
    """`$REGRADE_GATE` (a shell line; exit 0 = go) when set, else: delivery heavy commands exist on this host."""
    if os.environ.get("REGRADE_GATE"):
        return subprocess.run(["sh", "-c", os.environ["REGRADE_GATE"]]).returncode != 0
    r = subprocess.run(["pgrep", "-f", "work.noindex/heavy-cmds/"], capture_output=True, text=True)
    return bool(r.stdout.split())


WAITED = [0.0]


def wait_gate(out):
    """Wait for the gate; past `$REGRADE_MAX_WAIT_S` (default 8 h) of total waiting, stop visibly (GAVE-UP file)."""
    limit = float(os.environ.get("REGRADE_MAX_WAIT_S", 8 * 3600))
    while must_wait():
        if WAITED[0] >= limit:
            with open(os.path.join(out, "GAVE-UP"), "w") as f:
                f.write(f"gate still closed after {WAITED[0]:.0f} s of waiting; rerun the same command to resume\n")
            print("GAVE-UP: gate closed too long", flush=True)
            sys.exit(3)
        time.sleep(30)
        WAITED[0] += 30


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    out, runs = sys.argv[1], sys.argv[2]
    only = os.environ.get("REGRADE_ONLY", "")  # optional comma list of <cohort>/<task>/<rep>/<arm> prefixes
    runner = grading.runner_vars()
    for spec in sys.argv[3:]:
        cohort, tasks_dir = spec.split("=", 1)
        base = os.path.join(runs, cohort, "cells")
        for t in sorted(os.listdir(base)):
            for rep in sorted(os.listdir(os.path.join(base, t))):
                for arm in sorted(os.listdir(os.path.join(base, t, rep))):
                    key = f"{cohort}/{t}/{rep}/{arm}"
                    d = os.path.join(base, t, rep, arm)
                    dest = os.path.join(out, key + ".json")
                    if not os.path.isfile(os.path.join(d, "result.json")) or os.path.exists(dest):
                        continue
                    if only and not any(key.startswith(p) for p in only.split(",")):
                        continue
                    res = json.load(open(os.path.join(d, "result.json")))
                    old = json.load(open(os.path.join(d, "evaluation.json"))) if os.path.isfile(
                        os.path.join(d, "evaluation.json")) else {}
                    row = dict(cell=key, outcome=res.get("outcome"), old_all_passed=old.get("all_passed"),
                               old_passed=sum(v == "passed" for v in (old.get("ids") or {}).values()),
                               old_expected=len(old.get("ids") or {}), old_infrastructure=old.get("infrastructure"))
                    task = grading.load_task(os.path.join(tasks_dir, t))
                    work = os.path.join(out, "work", key.replace("/", "_"))
                    shutil.rmtree(work, ignore_errors=True)  # left by a stopped run
                    os.makedirs(work)
                    tar = os.path.join(d, "final-tree.tar")
                    try:
                        if os.path.isfile(tar):
                            row["tree_source"] = "final-tree.tar"
                        elif os.path.isfile(os.path.join(d, "final.diff")) and res.get("start_commit") and res.get("final_tree"):
                            tar, why = rebuild(os.path.join(tasks_dir, t), task["task"], os.path.join(d, "final.diff"),
                                               res["start_commit"], res["final_tree"], work)
                            row["tree_source"] = "final.diff rebuilt, start_commit and final_tree verified"
                            if why:
                                row.update(tree_source="final.diff", status="tree_mismatch", detail=why)
                        else:
                            row.update(status="not_kept", detail="no final-tree.tar, pass-tree tar or final.diff")
                        if os.environ.get("REGRADE_REBUILD_ONLY"):  # check trees only: print, write nothing
                            print(key, row.get("status", "tree ok"), row.get("tree_source"), row.get("detail", ""), flush=True)
                            continue
                        if "status" not in row:
                            row["tree_sha256"] = sha256(tar)
                            wait_gate(out)
                            t0 = time.monotonic()
                            rec = hk_public_grade(task, tar)
                            row.update(status="graded", wall_s=round(time.monotonic() - t0, 1),
                                       all_passed=rec.get("all_passed"), infrastructure=rec.get("infrastructure"),
                                       passed=sum(v == "passed" for v in rec["ids"].values()), expected=len(rec["ids"]),
                                       not_passed=sorted(k for k, v in rec["ids"].items() if v != "passed"),
                                       fixture_repairs=rec.get("fixture_repairs"),
                                       changed_ids=sorted(k for k in set(rec["ids"]) | set(old.get("ids") or {})
                                                          if rec["ids"].get(k) != (old.get("ids") or {}).get(k)))
                            os.makedirs(os.path.dirname(dest), exist_ok=True)
                            with open(dest + ".evaluation.json", "w") as f:
                                json.dump(rec, f, indent=1, sort_keys=True)
                    except Exception as e:  # recorded, never silent
                        row.update(status="error", detail=f"{type(e).__name__}: {e}"[:500])
                    finally:
                        shutil.rmtree(work, ignore_errors=True)
                    row["runner"] = runner
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    with open(dest, "w") as f:
                        json.dump(row, f, indent=1, sort_keys=True)
                    with open(os.path.join(out, "summary.jsonl"), "a") as f:
                        f.write(json.dumps(row, sort_keys=True) + "\n")
                    print(key, row.get("status"), row.get("old_all_passed"), "->", row.get("all_passed"),
                          f"{row.get('old_passed')}/{row.get('old_expected')} -> {row.get('passed')}/{row.get('expected')}",
                          row.get("infrastructure") or row.get("detail") or "", flush=True)


if __name__ == "__main__":
    main()
