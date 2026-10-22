"""Grading tests; `GradeCase` is the shared fixture (a copy of task-mini and fake cells)."""

import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import unittest
import unittest.mock

from lanes import common, grading

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "task-mini")
BIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin")


def tar_tree(src, dest):
    with tarfile.open(dest, "w") as t:
        for name in sorted(os.listdir(src)):
            t.add(os.path.join(src, name), arcname=name)


def edit(path, old, new):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.replace(old, new))


class GradeCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        env = unittest.mock.patch.dict(os.environ, {"KOGEN_LANES_HOME": os.path.join(self.tmp, "home")})
        env.start()
        self.addCleanup(env.stop)
        self.tasks = os.path.join(self.tmp, "tasks")
        self.task = os.path.join(self.tasks, "task-mini")
        shutil.copytree(FIX, self.task)
        self.run_dir = os.path.join(self.tmp, "run")

    def cell(self, name, phase="build", overlays=(), cell_id=None, pass_trees=()):
        """A finished cell whose final tree is `start/` with the overlays laid over it."""
        cell_id = cell_id or f"task-mini/r1/{name}"
        d = common.cell_dir(self.run_dir, cell_id)
        os.makedirs(d)
        with grading.scratch(self.task, *overlays) as tree:
            tar_tree(tree, os.path.join(d, "final-tree.tar"))
        common.write_json(os.path.join(d, "result.json"), {
            "cell": cell_id, "lane": name, "phase": phase, "pass_trees": list(pass_trees)})
        return cell_id, d

    def cli(self, script, *args):
        r = subprocess.run([sys.executable, os.path.join(BIN, script), *args], capture_output=True, text=True,
                           env=dict(os.environ, KOGEN_LANES_TASKS=self.tasks))
        return r.returncode, r.stdout, r.stderr

    def evaluation(self, d):
        return common.read_json(os.path.join(d, "evaluation.json"))


class GradeBuild(GradeCase):
    def test_correct_tree_passes_and_wrong_fails(self):
        good, gd = self.cell("good", overlays=["reference"])
        bad, bd = self.cell("bad", overlays=["wrong/negatives-clamped"])
        code, out, err = self.cli("lanes-grade", self.run_dir)
        self.assertEqual(code, 0, err)
        self.assertIn(f"{good}: pass", out)
        self.assertIn(f"{bad}: fail", out)
        ev = self.evaluation(gd)
        self.assertTrue(ev["all_passed"])
        self.assertEqual(ev["ids"], {"mini/TestAddNegative": "passed", "mini/TestAddPositive": "passed",
                                     "mini/TestAddZero": "passed"})
        self.assertIsNone(ev["infrastructure"])
        self.assertEqual(ev["totals"], {"expected": 3, "passed": 3})
        ev = self.evaluation(bd)
        self.assertFalse(ev["all_passed"])
        self.assertEqual(ev["failed"], ["mini/TestAddNegative"])

    def test_named_cells_only(self):
        a, ad = self.cell("a", overlays=["reference"])
        b, bd = self.cell("b", overlays=["reference"])
        self.assertEqual(self.cli("lanes-grade", self.run_dir, a)[0], 0)
        self.assertTrue(os.path.exists(os.path.join(ad, "evaluation.json")))
        self.assertFalse(os.path.exists(os.path.join(bd, "evaluation.json")))

    def test_setup_failure_is_infrastructure(self):
        edit(os.path.join(self.task, "task.toml"), "setup = []", 'setup = ["exit 3"]')
        c, d = self.cell("good", overlays=["reference"])
        code, out, _ = self.cli("lanes-grade", self.run_dir)
        self.assertEqual(code, 0)
        self.assertIn("infrastructure: setup failed: exit 3", out)
        ev = self.evaluation(d)
        self.assertFalse(ev["all_passed"])
        self.assertEqual(ev["infrastructure"], "setup failed: exit 3")
        self.assertEqual(ev["setup"][0]["status"], 3)

    def test_deadline_kills_the_process_group(self):
        marker = os.path.join(self.tmp, "started")
        edit(os.path.join(self.task, "evaluator", "evaluate.toml"), 'run = "go test -json -count=1 -run \'^(TestAddPositive',
             f'run = "touch {marker}; sleep 3173 & sleep 3173; go test -json -count=1 -run \'^(TestAddPositive')
        c, d = self.cell("good", overlays=["reference"])
        t0 = time.monotonic()
        code, _, err = self.cli("lanes-grade", self.run_dir, "--deadline", "1")
        self.assertEqual(code, 0, err)
        self.assertLess(time.monotonic() - t0, 25)
        self.assertTrue(os.path.exists(marker))
        ev = self.evaluation(d)
        self.assertFalse(ev["all_passed"])
        self.assertLessEqual({"mini/TestAddNegative", "mini/TestAddPositive"}, set(ev["timed_out"]))
        self.assertTrue(ev["commands"][0]["timed_out"])
        for _ in range(50):
            left = subprocess.run(["pgrep", "-f", "sleep 3173"], capture_output=True, text=True).stdout.split()
            if not left:
                break
            time.sleep(0.1)
        self.assertEqual(left, [])

    def test_evaluator_gets_a_small_environment(self):
        # setup fails (infrastructure) if the harness's secret leaks or TMPDIR is not private
        edit(os.path.join(self.task, "task.toml"), "setup = []",
             'setup = ["test -z \\"$LANES_TEST_SECRET\\"", "case \\"$TMPDIR\\" in */grade-*/tmp) ;; *) exit 1;; esac"]')
        c, d = self.cell("good", overlays=["reference"])
        with unittest.mock.patch.dict(os.environ, {"LANES_TEST_SECRET": "token"}):
            self.assertEqual(self.cli("lanes-grade", self.run_dir)[0], 0)
        ev = self.evaluation(d)
        self.assertIsNone(ev["infrastructure"], ev["setup"])
        self.assertTrue(ev["all_passed"])

    def test_results_path_must_stay_in_the_results_folder(self):
        edit(os.path.join(self.task, "evaluator", "evaluate.toml"), 'results = "go-test.jsonl"',
             'results = "../escape.jsonl"')
        c, d = self.cell("good", overlays=["reference"])
        self.cli("lanes-grade", self.run_dir)
        ev = self.evaluation(d)
        self.assertIn("results path is outside", ev["infrastructure"])
        self.assertFalse(ev["all_passed"])

    def test_pass_trees(self):
        c, d = self.cell("good", overlays=["reference"], pass_trees=["aaa", "bbb"])
        os.makedirs(os.path.join(d, "pass-trees"))
        with grading.scratch(self.task, "wrong/negatives-clamped") as tree:
            tar_tree(tree, os.path.join(d, "pass-trees", "aaa.tar"))
        self.assertEqual(self.cli("lanes-grade", self.run_dir)[0], 0)
        first, second = self.evaluation(d)["pass_trees"]
        self.assertEqual((first["tree"], first["all_passed"]), ("aaa", False))
        self.assertEqual(second, {"tree": "bbb", "ungraded": "tree not available"})

    def test_missing_tasks_flag_and_unfinished_cell(self):
        os.makedirs(os.path.join(self.run_dir, "cells", "task-mini", "r1", "x"))
        code, out, _ = self.cli("lanes-grade", self.run_dir)
        self.assertEqual((code, out), (0, ""))
        r = subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "..", "bin", "lanes-grade"),
                            self.run_dir], capture_output=True, text=True, env={"PATH": os.environ["PATH"]})
        self.assertEqual(r.returncode, 2)


FAKE_CUCUMBER = r'''
import json, subprocess, sys
report, feature = sys.argv[1], sys.argv[2]
text = open(feature).read().splitlines()
scen = [(i + 1, l.split(":", 1)[1].strip()) for i, l in enumerate(text) if l.strip().startswith("Scenario:")]
p = subprocess.run(["go", "test", "-json", "-count=1", "./features/steps/"], capture_output=True, text=True)
order, res = [], {}
for line in p.stdout.splitlines():
    try:
        e = json.loads(line)
    except ValueError:
        continue
    if e.get("Test"):
        if e["Test"] not in order:
            order.append(e["Test"])
        if e["Action"] in ("pass", "fail"):
            res[e["Test"]] = e["Action"]
msgs = [{"gherkinDocument": {"feature": {"children": [
    {"scenario": {"id": "s%d" % n, "location": {"line": ln}}} for n, (ln, _) in enumerate(scen)]}}}]
failed = False
for n, (ln, name) in enumerate(scen):
    status = {"pass": "PASSED", "fail": "FAILED"}.get(res.get(order[n]) if n < len(order) else None, "UNDEFINED")
    failed |= status != "PASSED"
    msgs += [{"pickle": {"id": "p%d" % n, "uri": feature, "name": name, "astNodeIds": ["s%d" % n]}},
             {"testCase": {"id": "c%d" % n, "pickleId": "p%d" % n, "testSteps": [{"id": "t%d" % n}]}},
             {"testCaseStarted": {"id": "st%d" % n, "testCaseId": "c%d" % n}},
             {"testStepFinished": {"testCaseStartedId": "st%d" % n, "testStepId": "t%d" % n,
                                   "testStepResult": {"status": status}}},
             {"testCaseFinished": {"testCaseStartedId": "st%d" % n, "willBeRetried": False}}]
open(report, "w").write("".join(json.dumps(m) + "\n" for m in msgs))
sys.exit(1 if failed else 0)
'''
RUN = 'python3 features/run_acceptance.py "$KOGEN_ACCEPTANCE_REPORT" "$KOGEN_ACCEPTANCE_FEATURES"'


class GradeShape(GradeCase):
    """The task's acceptance runner is a stand-in for cucumber-js: it reads the two KOGEN_ACCEPTANCE_*
    paths, so a harness that sets neither, or does not lay the Intent's feature in the tree, fails."""

    def setUp(self):
        super().setUp()
        with open(os.path.join(self.task, "start", "features", "run_acceptance.py"), "w") as f:
            f.write(FAKE_CUCUMBER)
        edit(os.path.join(self.task, "task.toml"), 'run = "go test -count=1 ./features/steps/"', "run = '%s'" % RUN)

    def shape_cell(self):
        c, d = self.cell("shaped", phase="shape")
        os.remove(os.path.join(d, "final-tree.tar"))
        shutil.copytree(os.path.join(self.task, "supplied/gherkin"), os.path.join(d, "intent"))
        return c, d

    def counts(self, d):
        ev = self.evaluation(d)
        return {k: ev[k] for k in ("scenarios", "pass_on_reference", "fail_on_start", "wrong_caught", "wrong_total")}

    def test_matrix_and_counts_per_scenario(self):
        c, d = self.shape_cell()
        code, out, err = self.cli("lanes-grade", self.run_dir)
        self.assertEqual(code, 0, err)
        self.assertEqual(self.counts(d), {"scenarios": 2, "pass_on_reference": 2, "fail_on_start": 2,
                                          "wrong_caught": 1, "wrong_total": 1})
        ev = self.evaluation(d)
        self.assertIsNone(ev["infrastructure"])
        self.assertEqual(ev["matrix"], {"reference": {"3": "passed", "7": "passed"},
                                        "start": {"3": "failed", "7": "failed"},
                                        "wrong/negatives-clamped": {"3": "passed", "7": "failed"}})
        self.assertIn("scenarios=2 pass_on_reference=2 fail_on_start=2 wrong_caught=1/1", out)

    def test_weak_steps_do_not_fail_the_start_tree(self):
        c, d = self.shape_cell()
        steps = os.path.join(d, "intent", "features", "steps", "acceptance_test.go")
        edit(steps, "got != 5", "got == 99")
        edit(steps, "got != 1", "got == 99")
        code, out, _ = self.cli("lanes-grade", self.run_dir)
        self.assertEqual(self.counts(d), {"scenarios": 2, "pass_on_reference": 2, "fail_on_start": 0,
                                          "wrong_caught": 0, "wrong_total": 1})
        self.assertIn("fail_on_start=0", out)
        self.assertNotIn(": pass", out)

    def test_runner_without_report_is_infrastructure_not_a_failure(self):
        c, d = self.shape_cell()
        edit(os.path.join(self.task, "task.toml"), "run = '%s'" % RUN, "run = 'exit 1'")
        code, out, _ = self.cli("lanes-grade", self.run_dir)
        ev = self.evaluation(d)
        self.assertIn("wrote no usable report", ev["infrastructure"])
        self.assertNotIn("fail_on_start", ev)
        self.assertIn("infrastructure:", out)

    def test_setup_failure_is_infrastructure(self):
        c, d = self.shape_cell()
        edit(os.path.join(self.task, "task.toml"), "setup = []", 'setup = ["exit 3"]')
        self.cli("lanes-grade", self.run_dir)
        self.assertIn("setup failed: exit 3", self.evaluation(d)["infrastructure"])

    def test_missing_step_files_are_infrastructure(self):
        c, d = self.shape_cell()
        shutil.rmtree(os.path.join(d, "intent", "features"))
        self.cli("lanes-grade", self.run_dir)
        self.assertIn("step files not available", self.evaluation(d)["infrastructure"])


if __name__ == "__main__":
    unittest.main()
