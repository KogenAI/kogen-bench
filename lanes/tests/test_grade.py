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
from lanes import report as reportlib

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
        os.environ.pop("KOGEN_BIN", None)  # restored by `env.stop`: lanes-qualify must not find a Kogen unasked
        self.tasks = os.path.join(self.tmp, "tasks")
        self.task = os.path.join(self.tasks, "task-mini")
        shutil.copytree(FIX, self.task)
        self.run_dir = os.path.join(self.tmp, "run")

    def cell(self, name, phase="build", overlays=(), cell_id=None, pass_trees=(), first_green=None):
        """A finished cell whose final tree is `start/` with the overlays laid over it."""
        cell_id = cell_id or f"task-mini/r1/{name}"
        d = common.cell_dir(self.run_dir, cell_id)
        os.makedirs(d)
        with grading.scratch(self.task, *overlays) as tree:
            tar_tree(tree, os.path.join(d, "final-tree.tar"))
        common.write_json(os.path.join(d, "result.json"), {
            "cell": cell_id, "lane": name, "phase": phase, "pass_trees": list(pass_trees),
            **({"first_green_tree": first_green} if first_green else {})})
        return cell_id, d

    def cli(self, script, *args):
        r = subprocess.run([sys.executable, os.path.join(BIN, script), *args], capture_output=True, text=True,
                           env=dict(os.environ, KOGEN_LANES_TASKS=self.tasks))
        return r.returncode, r.stdout, r.stderr

    def evaluation(self, d):
        return common.read_json(os.path.join(d, "evaluation.json"))


class GradeBuild(GradeCase):
    def test_env_drops_other_variables_that_start_with_go(self):  # L9: GOOGLE_* are credentials
        env = {"GOPATH": "/g", "GOFLAGS": "-mod=mod", "GOOGLE_API_KEY": "secret", "GOOGLE_APPLICATION_CREDENTIALS": "/c",
               "GOTOKEN": "x", "MIX_ENV": "test", "OPENAI_API_KEY": "k"}
        with unittest.mock.patch.dict(os.environ, env):
            got = grading.task_env(grading.load_task(self.task), os.path.join(self.tmp, "t", "tree"))
        self.assertEqual((got["GOPATH"], got["GOFLAGS"], got["MIX_ENV"]), ("/g", "-mod=mod", "test"))
        for name in ("GOOGLE_API_KEY", "GOOGLE_APPLICATION_CREDENTIALS", "GOTOKEN", "OPENAI_API_KEY"):
            self.assertNotIn(name, got)

    def test_env_keeps_the_acceptance_runner_variables_only(self):
        env = {"KOGEN_CUCUMBER": "/c/cucumber.js", "KOGEN_NODE": "/n/node", "KOGEN_FOO": "x",
               "KOGEN_NODE_EXTRA": "y", "KOGEN_CUCUMBERS": "z", "OPENAI_API_KEY": "k"}
        with unittest.mock.patch.dict(os.environ, env):
            got = grading.task_env(grading.load_task(self.task), os.path.join(self.tmp, "t", "tree"))
        self.assertEqual((got["KOGEN_CUCUMBER"], got["KOGEN_NODE"]), ("/c/cucumber.js", "/n/node"))
        for name in ("KOGEN_FOO", "KOGEN_NODE_EXTRA", "KOGEN_CUCUMBERS", "OPENAI_API_KEY"):
            self.assertNotIn(name, got)

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

    def test_first_green_tree_is_marked_and_graded_like_the_others(self):
        c, d = self.cell("good", overlays=["reference"], pass_trees=["aaa", "bbb", "ccc"], first_green="aaa")
        os.makedirs(os.path.join(d, "pass-trees"))
        with grading.scratch(self.task, "reference") as tree:
            tar_tree(tree, os.path.join(d, "pass-trees", "aaa.tar"))
        with grading.scratch(self.task, "wrong/negatives-clamped") as tree:
            tar_tree(tree, os.path.join(d, "pass-trees", "bbb.tar"))
        self.assertEqual(self.cli("lanes-grade", self.run_dir)[0], 0)
        first, second, third = self.evaluation(d)["pass_trees"]
        self.assertEqual((first["tree"], first["all_passed"], first["first_green"]), ("aaa", True, True))
        self.assertEqual((second["tree"], second["all_passed"]), ("bbb", False))
        self.assertEqual(third, {"tree": "ccc", "ungraded": "tree not available"})
        self.assertNotIn("first_green", second)
        self.assertNotIn("first_green", third)

    def test_an_ungraded_first_green_tree_is_still_marked(self):
        c, d = self.cell("good", overlays=["reference"], pass_trees=["aaa"], first_green="aaa")
        self.assertEqual(self.cli("lanes-grade", self.run_dir)[0], 0)
        self.assertEqual(self.evaluation(d)["pass_trees"],
                         [{"tree": "aaa", "ungraded": "tree not available", "first_green": True}])

    def test_a_result_without_a_first_green_tree_marks_nothing(self):
        c, d = self.cell("good", overlays=["reference"], pass_trees=["aaa"])
        self.assertEqual(self.cli("lanes-grade", self.run_dir)[0], 0)
        self.assertNotIn("first_green", self.evaluation(d)["pass_trees"][0])

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


class ShapeFixture(GradeCase):
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

    def counts(self, d, ev=None):
        ev = ev or self.evaluation(d)
        return {k: ev[k] for k in ("scenarios", "pass_on_reference", "fail_on_start", "wrong_caught", "wrong_total")}


class GradeShape(ShapeFixture):
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

    def test_scenarios_counted_from_the_intent_feature_not_the_run(self):  # L9
        c, d = self.shape_cell()
        edit(os.path.join(self.task, "start", "features", "run_acceptance.py"),
             "p = subprocess.run", "scen = scen[:1]\np = subprocess.run")  # the runner stops after one scenario
        self.cli("lanes-grade", self.run_dir)
        self.assertEqual(self.counts(d), {"scenarios": 2, "pass_on_reference": 1, "fail_on_start": 2,
                                          "wrong_caught": 1, "wrong_total": 1})

    def test_feature_lines_cover_outline_rows_and_skip_doc_strings(self):  # L9
        path = os.path.join(self.tmp, "x.feature")
        with open(path, "w") as f:
            f.write('Feature: x\n  Background:\n    Given a table\n      | k | v |\n      | 1 | 2 |\n'
                    '  Scenario: a\n    Given text\n    """\n    Scenario: not one\n    """\n'
                    '  Scenario Outline: b\n    Given a step table\n      | a | b |\n      | 1 | 2 |\n'
                    '    Examples:\n      | n |\n      | 1 |\n      | 2 |\n'
                    '  Rule: r\n    Background:\n      Given rows\n        | x |\n        | y |\n'
                    '    Example: c\n')
        self.assertEqual(grading.feature_lines(path), ["6", "17", "18", "24"])

    def test_unresolved_report_ids_are_no_usable_report(self):  # L9
        c, d = self.shape_cell()
        edit(os.path.join(self.task, "start", "features", "run_acceptance.py"),
             '"astNodeIds": ["s%d" % n]', '"astNodeIds": ["gone%d" % n]')
        self.cli("lanes-grade", self.run_dir)
        self.assertIn("wrote no usable report", self.evaluation(d)["infrastructure"])

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


class GradeE2eShape(ShapeFixture):
    """An e2e cell is graded like a build, and also like a shape cell on the Intent it shaped."""

    BUILD_KEYS = ("all_passed", "commands", "expected", "ids", "infrastructure", "totals", "pass_trees")

    def e2e_cell(self, stages=None, intent=True):
        c, d = self.cell("e2e", phase="e2e", overlays=("reference",))
        if stages is not None:
            result = common.read_json(os.path.join(d, "result.json"))
            common.write_json(os.path.join(d, "result.json"), dict(result, stages=stages))
        if intent:
            shutil.copytree(os.path.join(self.task, "supplied/gherkin"), os.path.join(d, "intent"))
        return c, d

    def test_shape_matrix_is_added_to_the_build_grade(self):
        c, d = self.e2e_cell(stages=[{"stage": "shape", "exit_code": 0}, {"stage": "build", "exit_code": 0}])
        code, out, err = self.cli("lanes-grade", self.run_dir)
        self.assertEqual(code, 0, err)
        ev = self.evaluation(d)
        self.assertEqual(self.counts(d, ev["shape"]), {"scenarios": 2, "pass_on_reference": 2, "fail_on_start": 2,
                                                      "wrong_caught": 1, "wrong_total": 1})
        self.assertIsNone(ev["shape"]["infrastructure"])
        self.assertEqual(ev["shape"]["matrix"]["wrong/negatives-clamped"], {"3": "passed", "7": "failed"})
        self.assertNotIn("scenarios", ev)  # the counts live under `shape`, not at the top level
        self.assertIn("shape scenarios=2 pass_on_reference=2 fail_on_start=2 wrong_caught=1/1", out)

    def test_build_keys_match_a_build_cell(self):
        c, d = self.e2e_cell()
        self.cli("lanes-grade", self.run_dir)
        e2e = self.evaluation(d)
        b, bd = self.cell("build", phase="build", overlays=("reference",))
        self.cli("lanes-grade", self.run_dir)
        build = self.evaluation(bd)
        self.assertNotIn("shape", build)
        self.assertEqual({k: v for k, v in e2e.items() if k != "shape"}, build)
        self.assertTrue(e2e["all_passed"])

    def test_refused_shape_stage_is_infrastructure_with_no_counts(self):
        c, d = self.e2e_cell(stages=[{"stage": "shape", "exit_code": 2}])
        self.cli("lanes-grade", self.run_dir)
        ev = self.evaluation(d)
        self.assertEqual(ev["shape"], {"phase": "shape", "infrastructure": "shape stage did not finish: exit 2"})
        self.assertIn("all_passed", ev)  # the build grade is still there, and its own infrastructure stays unset
        self.assertIsNone(ev["infrastructure"])

    def test_pending_questions_are_named(self):
        c, d = self.e2e_cell(stages=[{"stage": "shape", "exit_code": 5, "detail": "questions_pending"}])
        self.cli("lanes-grade", self.run_dir)
        self.assertEqual(self.evaluation(d)["shape"]["infrastructure"], "shape stage did not finish: questions_pending")

    def test_no_intent_folder_is_the_shape_cell_convention(self):
        c, d = self.e2e_cell(intent=False)
        self.cli("lanes-grade", self.run_dir)
        self.assertEqual(self.evaluation(d)["shape"],
                         {"phase": "shape", "infrastructure": "task has no [acceptance] or the cell has no Intent"})

    def test_report_shows_the_shape_class_next_to_the_build_result(self):
        c, d = self.e2e_cell()
        self.cli("lanes-grade", self.run_dir)
        report = reportlib._lane({"name": "e2e", "sha": None, "patch": None}, [
            {"plan": {"cell": c, "task": "task-mini", "lane": "e2e"}, "result": {"outcome": "landed"},
             "evaluation": self.evaluation(d), "log": [], "class": "correct"},
            {"plan": {"cell": "x", "task": "task-mini", "lane": "e2e"}, "result": {"outcome": "landed"},
             "evaluation": {"all_passed": True, "shape": {"phase": "shape", "infrastructure": "no Intent"}}, "log": [],
             "class": "correct"}], "e2e")
        self.assertEqual(report["classes"], {"correct": 2})
        self.assertEqual(report["shape_classes"], {"correct": 1, "infrastructure": 1})
        self.assertEqual(report["shape"]["scenarios"], 2)
        build = reportlib._lane({"name": "b", "sha": None, "patch": None}, [
            {"plan": {"cell": c, "task": "task-mini", "lane": "b"}, "result": {"outcome": "landed"},
             "evaluation": {"all_passed": True}, "log": [], "class": "correct"}], "build")
        self.assertNotIn("shape_classes", build)
        self.assertIsNone(build["shape"])


if __name__ == "__main__":
    unittest.main()
