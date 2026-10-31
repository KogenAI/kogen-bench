#!/usr/bin/env python3
"""Build the harness snapshot the hard-task packs ran on: the published lanes/ tree plus the alone-arm adapter.

    python3 lanes/hk/apply_overlay.py --study ID --arm codex|claude --out DIR

ID is the `hk_study` value of the experiment file (for example hardplan3-20261030). The script copies lanes/ to
DIR/source/lanes, adds lanes/hk/adapter_<arm>.py as lanes/hk_adapter.py (with the study id filled in) and lanes/hk/gocache.py,
and edits cell.py, costguard.py, grading.py, report.py and approvecache.py in the copy. It also puts bare/lanes_bare.py and
bare/pubmetrics.py in DIR, where the adapter looks for them. Each edit fails loudly if its anchor is not found exactly once.
Run the lanes commands from DIR/source/lanes/bin with HK_STUDY=ID set; the published lanes/ is not changed.
"""
import argparse
import shutil
from pathlib import Path

def once(text: str, before: str, after: str, label: str) -> str:
    count = text.count(before)
    if count == 0 and after in text:
        return text
    if count != 1:
        raise RuntimeError(f"{label}: expected one insertion anchor, found {count}")
    return text.replace(before, after)


def overlay_cell(path: Path) -> None:
    s = path.read_text()
    s = once(s,
        'if not k.startswith("KOGEN_LANES_")',
        'if not k.startswith(("KOGEN_LANES_", "HK_")) and k != "PYTHONPATH"', "cell env")
    s = once(s,
        '    exp = experiment.load(os.path.join(run_dir, "experiment.json"))\n',
        '    exp = experiment.load(os.path.join(run_dir, "experiment.json"))\n'
        '    if exp.get("hk_study") == "@STUDY@" and os.environ.get("HK_STUDY") != exp["hk_study"]:\n'
        '        raise CellError("HK experiment requires its pinned harness adapter")\n', "cell guard")
    s = once(s,
        '    phase = exp["phase"]\n    out = common.cell_dir(run_dir, cell)\n',
        '    if lane.get("driver") == "codex-alone":\n'
        '        from . import hk_adapter\n'
        '        return hk_adapter.run(run_dir, cell, tasks, exp, lane, host, keep, force)\n'
        '    phase = exp["phase"]\n    out = common.cell_dir(run_dir, cell)\n', "cell driver")
    s = once(s,
        '        reason = costguard.note_rate_limit(run_dir, exp, cell)\n',
        '        if exp.get("hk_study") == "@STUDY@":\n'
        '            if os.environ.get("HK_STUDY") != exp["hk_study"]:\n'
        '                raise CellError("HK experiment requires its pinned harness adapter")\n'
        '            result.update(hk_study=exp["hk_study"], arm="kogen", pipeline="shape-build-review",\n'
        '                          repetition_block=exp["hk_repetition_block"])\n'
        '            common.write_json(os.path.join(out, "result.json"), result)\n'
        '        reason = costguard.note_rate_limit(run_dir, exp, cell)\n', "cell receipt")
    path.write_text(s)


def overlay_costguard(path: Path) -> None:
    s = path.read_text()
    s = once(s,
        'def cell_spend(cell_dir):\n    """USD of one cell dir: finished, running (live workspace) or stopped without a result."""\n',
        'def cell_spend(cell_dir):\n    """USD of one cell dir: finished, running (live workspace) or stopped without a result."""\n'
        '    from . import hk_adapter\n'
        '    hk_spend = hk_adapter.codex_spend(cell_dir)\n'
        '    if hk_spend is not None:\n'
        '        return hk_spend\n', "costguard")
    path.write_text(s)


def overlay_grading(path: Path) -> None:
    s = path.read_text()
    marker = '\n\n# --- shape grading -----------------------------------------------------------------------------\n'
    fn = '''\n\ndef hk_public_grade_archive(task, tar_path, deadline_s=None):
    """Grade HK2 against its qualified public oracle in a disposable scratch tree."""
    with scratch() as tree:
        extract(tar_path, tree)
        supplied = os.path.join(task["dir"], "supplied", "gherkin")
        acc = task["task"].get("acceptance") or {}
        steps = os.path.join(tree, acc.get("steps_dir", "features/steps"))
        if os.path.commonpath([os.path.abspath(tree), os.path.abspath(steps)]) != os.path.abspath(tree):
            raise GradeError("public steps path escapes grading workspace")
        shutil.rmtree(steps, ignore_errors=True)
        for dirpath, _, names in os.walk(supplied):
            for name in names:
                src = os.path.join(dirpath, name)
                rel = os.path.relpath(src, supplied)
                if rel == "intent.md" or (os.sep not in rel and rel.startswith("model.")):
                    continue
                if rel == "acceptance.feature":
                    slug = task["task"]["name"]
                    targets = [os.path.join(tree, ".kogen", "intents", slug, "acceptance.feature"),
                               os.path.join(os.path.dirname(steps), "acceptance.feature")]
                else:
                    targets = [os.path.join(tree, rel)]
                for target in targets:
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    shutil.copyfile(src, target)
        rec = evaluate_tree(task, tree, deadline_s=deadline_s)
        rec["hk_public_oracle"] = "restored qualified public scenarios and steps in grading scratch; evaluator unchanged"
        return rec
'''
    if "def hk_public_grade_archive(" not in s:
        if s.count(marker) != 1:
            raise RuntimeError("grading: shape insertion anchor missing")
        s = s.replace(marker, fn + marker)
    s = once(s,
        '    for stage in result.get("stages") or []:\n',
        '    if result.get("hk_study") == "@STUDY@":\n'
        '        return {"not_evaluated": True, "reason": "HK primary uses the independent protected final-tree oracle; shape execution is recorded in stages"}\n'
        '    for stage in result.get("stages") or []:\n', "shaped intent grade")
    s = once(s,
        '        tar = os.path.join(d, "final-tree.tar")\n',
        '        tar = os.path.join(d, "final-tree.tar")\n'
        '        archive_grader = hk_public_grade_archive if result.get("hk_study") == "@STUDY@" else grade_archive\n', "archive grader")
    s = once(s, '            rec = grade_archive(task, tar, deadline_s)\n',
                '            rec = archive_grader(task, tar, deadline_s)\n', "final archive")
    s = once(s,
        '            sub = grade_archive(task, p, deadline_s) if os.path.isfile(p) else {"ungraded": "tree not available"}\n',
        '            sub = archive_grader(task, p, deadline_s) if os.path.isfile(p) else {"ungraded": "tree not available"}\n', "pass tree archive")
    s = once(s,
        'def shape_summary(rec):\n    return "scenarios=%d pass_on_reference=%d fail_on_start=%d wrong_caught=%d/%d" % (\n',
        'def shape_summary(rec):\n'
        '    if rec.get("not_evaluated") is True or not all(k in rec for k in ("scenarios", "pass_on_reference", "fail_on_start", "wrong_caught", "wrong_total")):\n'
        '        return "not evaluated"\n'
        '    return "scenarios=%d pass_on_reference=%d fail_on_start=%d wrong_caught=%d/%d" % (\n', "shape summary")
    path.write_text(s)


def overlay_report(path: Path) -> None:
    s = path.read_text()
    s = once(s,
        '    return {"all_passed": "correct", "failed": "incorrect"}.get(state, "infrastructure")\n',
        '    if shape.get("not_evaluated") is True:\n'
        '        return "not evaluated"\n'
        '    return {"all_passed": "correct", "failed": "incorrect"}.get(state, "infrastructure")\n', "report shape class")
    path.write_text(s)




def overlay_gocache(lane: Path) -> None:
    p = lane / "cell.py"
    s = p.read_text()
    s = once(s, "from . import common, costguard, experiment, live, node_modules, probe, usage",
             "from . import common, costguard, experiment, gocache, live, node_modules, probe, usage", "gocache import")
    s = once(s, "    node_modules.prepare_workspace(start, ws)\n",
             "    node_modules.prepare_workspace(start, ws)\n    return gocache.prepare(start, tmp)\n", "gocache prepare")
    s = once(s, "approval_context=None):\n        self.ws, self.kogen",
             "approval_context=None, go_env=None):\n        self.ws, self.kogen", "cell signature")
    s = once(s, '"GIT_TERMINAL_PROMPT": "0"}', '"GIT_TERMINAL_PROMPT": "0", **(go_env or {})}', "cell go env")
    s = once(s, "    make_workspace(ws, tmp, os.path.join(task, \"start\"), config)\n",
             "    go_env, go_info = make_workspace(ws, tmp, os.path.join(task, \"start\"), config)\n"
             "    common.write_json(os.path.join(out, gocache.INFO), go_info)\n", "go info")
    s = once(s, "approval_context=(run_dir, cell.split(\"/\", 1)[0], lane_name))",
             "approval_context=(run_dir, cell.split(\"/\", 1)[0], lane_name), go_env=go_env)", "cell go_env arg")
    p.write_text(s)
    p = lane / "approvecache.py"
    s = p.read_text()
    s = once(s, '"common.py", "node_modules.py"', '"common.py", "gocache.py", "node_modules.py"', "approvecache code")
    s = once(s, '"LANES_GUARD_LOG"}', '"LANES_GUARD_LOG", "LANES_GO_CACHE"}', "approvecache env")
    p.write_text(s)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--study", required=True)
    ap.add_argument("--arm", choices=("codex", "claude"), required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    here = Path(__file__).resolve().parent
    root = here.parent
    out = Path(a.out)
    if out.exists():
        raise SystemExit(f"{out} exists; give a new directory")
    lane_root = out / "source" / "lanes"
    shutil.copytree(root, lane_root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "hk"))
    lane = lane_root / "lanes"
    for name in ("lanes_bare.py", "pubmetrics.py"):
        shutil.copy2(root / "bare" / name, out / name)
    adapter = (here / f"adapter_{a.arm}.py").read_text().replace("@STUDY@", a.study)
    (lane / "hk_adapter.py").write_text(adapter)
    shutil.copy2(here / "gocache.py", lane / "gocache.py")
    overlay_cell(lane / "cell.py")
    overlay_gocache(lane)
    overlay_costguard(lane / "costguard.py")
    overlay_grading(lane / "grading.py")
    overlay_report(lane / "report.py")
    for name in ("cell.py", "grading.py"):
        p = lane / name
        p.write_text(p.read_text().replace("@STUDY@", a.study))
    if a.arm == "claude":
        p = lane / "cell.py"
        s = p.read_text()
        s = once(s, 'if lane.get("driver") == "codex-alone":', 'if lane.get("driver") in ("codex-alone", "claude-code-alone"):', "driver")
        p.write_text(s)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
