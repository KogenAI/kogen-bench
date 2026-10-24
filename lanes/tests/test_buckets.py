import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock

from lanes import buckets, common, grading

BIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin")
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "task-mini")
SHA = "0123456789abcdef0123456789abcdef01234567"
ADD = "mini/TestAddNegative"


def experiment(id_, rnd, parent, train=("t1", "t2"), test=("t3",)):
    lane = {"sha": SHA, "settings": {"models": {"build": "openai/m high"}}}
    return {"id": id_, "kind": "climb", "phase": "build", "intent_form": "gherkin", "kogen": {"repo": "x"},
            "lanes": [dict(lane, name="baseline", patch=None), dict(lane, name="candidate", patch="p.patch")],
            "tasks": [*train, *test], "reps": 1, "deadline_s": 60, "hosts": ["local"],
            "split": {"train": list(train), "test": list(test)}, "min_effect": 0.1, "noise_ref": "n.json",
            "round": rnd, "parent": parent, "decision_rule": {"kind": "keep_revert"}}


class Case(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.tasks = os.path.join(self.tmp, "tasks")

    def round(self, id_, rnd, parent, decision, **kw):
        d = os.path.join(self.tmp, id_)
        common.write_json(os.path.join(d, "experiment.json"), experiment(id_, rnd, parent, **kw))
        if decision:
            common.write_json(os.path.join(d, "report.json"), {"verdict": {"decision": decision, "case": decision}})
        return d

    def cli(self, script, *args, **env):
        r = subprocess.run([sys.executable, os.path.join(BIN, script), *args], capture_output=True, text=True,
                           env=dict(os.environ, **env))
        return r.returncode, r.stdout, r.stderr


class ClimbLog(Case):
    def chain(self, *decisions):
        dirs, parent = [], None
        for i, dec in enumerate(decisions, 1):
            dirs.append(self.round(f"r{i}", i, parent, dec))
            parent = f"r{i}"
        return dirs

    def test_three_flat_rounds_stall_in_any_order_of_arguments(self):
        dirs = self.chain("keep", "within_noise", "revert", "within_noise")
        code, out, _ = self.cli("lanes-climb-log", *reversed(dirs))
        self.assertEqual(code, 0)
        self.assertIn("STALL: the last 3 rounds", out)
        self.assertLess(out.index("round 1"), out.index("round 4"))

    def test_a_keep_ends_the_stall(self):
        out = self.cli("lanes-climb-log", *self.chain("revert", "within_noise", "keep"))[1]
        self.assertIn("no stall: 0 flat", out)

    def test_two_rounds_stall_with_window_two(self):
        dirs = self.chain("keep", "within_noise", "revert")
        self.assertIn("no stall", self.cli("lanes-climb-log", *dirs)[1])
        self.assertIn("STALL", self.cli("lanes-climb-log", *dirs, "--window", "2")[1])

    def test_missing_report_is_not_flat(self):
        out = self.cli("lanes-climb-log", *self.chain("within_noise", None, "within_noise"))[1]
        self.assertIn("no report", out)
        self.assertIn("no stall", out)

    def test_broken_lineage_exits_2(self):
        a, c = self.round("r1", 1, None, "keep"), self.round("r3", 3, "r2", "keep")
        code, _, err = self.cli("lanes-climb-log", a, c)
        self.assertEqual(code, 2)
        self.assertIn("one chain of parent rounds", err)
        self.assertEqual(self.cli("lanes-climb-log", self.tmp + "/nowhere")[0], 2)


FAILING = {"ids": {ADD: "failed", "mini/TestAddPositive": "passed"}, "failed": [ADD], "all_passed": False,
           "infrastructure": None, "expected": {"requested": [ADD, "mini/TestAddPositive"], "regression": []}}


class Buckets(Case):
    def setUp(self):
        super().setUp()
        for t in ("t1", "t2", "t3"):
            d = os.path.join(self.tmp, "tasks", t)
            os.makedirs(os.path.join(d, "supplied", "gherkin"))
            with open(os.path.join(d, "request.md"), "w") as f:
                f.write("Make Add return the sum, including negative numbers.")
            with open(os.path.join(d, "supplied", "gherkin", "intent.md"), "w") as f:
                f.write("Add returns the sum of a and b.")
        self.rows = []
        self.evals = {}

    def failed(self, task, ev, plumbing=None, cls="incorrect", outcome="landed"):
        """A row shaped like `report.climb_report`'s: `plumbing` rows come from its `plumbing`, others from `train_failures`."""
        cell = f"{task}/r1/candidate"
        if plumbing:
            self.rows.append({"cell": cell, "lane": "candidate", "split": "train", "category": plumbing,
                              "outcome": outcome if plumbing != "harness" else "landed"})
        else:
            self.rows.append({"cell": cell, "lane": "candidate", "class": cls, "outcome": outcome})
        if ev is not None:
            common.write_json(os.path.join(common.cell_dir(self.rd, cell), "evaluation.json"), ev)

    def finish(self, extra=()):
        train = [r for r in self.rows if "class" in r]
        plumbing = [r for r in self.rows if "category" in r] + list(extra)
        common.write_json(os.path.join(self.rd, "report.json"), {
            "verdict": {"decision": "within_noise", "case": "within_noise"},
            "climb": {"train_failures": train, "plumbing": plumbing}})

    def table(self, ref=None):
        self.finish()
        with unittest.mock.patch("sys.stdout") as so:
            code = buckets.buckets_main([self.rd, "--tasks", self.tasks, "--json", self.tmp + "/o.json"],
                                        reference=lambda task_dir: ref or {"ids": {ADD: "passed"}})
        self.assertEqual(code, 0)
        return common.read_json(self.tmp + "/o.json"), "".join(c.args[0] for c in so.write.call_args_list)

    def test_every_bucket(self):
        self.rd = self.round("r1", 1, None, "within_noise")
        self.failed("t1", dict(FAILING))  # model failure: the reference passes it, the task text names it
        self.failed("t2", dict(FAILING, infrastructure="setup failed: go mod download"), plumbing="harness")
        self.failed("t2", None, plumbing="timeout", outcome="timeout")
        data, text = self.table()
        by = {r["cell"] + r["bucket"]: r for r in data["rows"]}
        self.assertEqual(sorted(r["bucket"] for r in data["rows"]), ["grader_bug", "harness_error", "model_failure"])
        self.assertEqual({r["bucket"] for r in data["rows"] if "timeout" in r["evidence"]}, {"harness_error"})
        self.assertEqual(data["counts"], {"grader_bug": 1, "harness_error": 1, "model_failure": 1})
        self.assertIn("setup failed", by["t2/r1/candidategrader_bug"]["evidence"])
        self.assertIn("counts: grader_bug 1, ambiguous_task 0, harness_error 1, model_failure 1", text)

    def test_reference_also_fails_is_grader_bug(self):
        self.rd = self.round("r1", 1, None, "within_noise")
        self.failed("t1", dict(FAILING))
        data, _ = self.table({"ids": {ADD: "failed"}})
        self.assertEqual(data["rows"][0]["bucket"], "grader_bug")
        self.assertIn(ADD, data["rows"][0]["evidence"])

    def test_untold_test_is_ambiguous(self):
        self.rd = self.round("r1", 1, None, "within_noise")
        odd = "mini/TestFrobnicateWidgetsQuickly"
        self.failed("t1", {"ids": {odd: "failed"}, "failed": [odd], "infrastructure": None,
                         "expected": {"requested": [odd], "regression": []}})
        data, _ = self.table()
        self.assertEqual(data["rows"][0]["bucket"], "ambiguous_task")
        self.assertIn(odd, data["rows"][0]["evidence"])

    def test_missing_evaluation_and_missing_final_tree_are_harness(self):
        self.rd = self.round("r1", 1, None, "within_noise")
        self.failed("t1", None)
        self.failed("t2", {"all_passed": False, "infrastructure": "final-tree.tar missing"}, plumbing="harness")
        data, _ = self.table()
        self.assertEqual({r["bucket"] for r in data["rows"]}, {"harness_error"})

    def test_test_split_is_never_read(self):
        self.rd = self.round("r1", 1, None, "within_noise")
        self.failed("t3", dict(FAILING))  # a stale or tampered report names a test task
        self.finish(extra=[{"cell": "t3/r1/baseline", "lane": "baseline", "split": "test", "category": "timeout",
                            "outcome": None}])
        real = common.read_json
        seen = []
        with unittest.mock.patch("sys.stdout"), unittest.mock.patch(
                "lanes.common.read_json", side_effect=lambda p: seen.append(p) or real(p)):
            code = buckets.buckets_main([self.rd, "--tasks", self.tasks, "--json", self.tmp + "/o.json"],
                                        reference=self.fail_if_called)
        self.assertEqual(code, 0)
        self.assertEqual(real(self.tmp + "/o.json")["rows"], [])
        self.assertFalse([p for p in seen if "t3" in p])

    def fail_if_called(self, task_dir):
        self.fail("the reference was graded for " + task_dir)

    def test_plumbing_harness_without_grader_infrastructure_is_harness(self):
        self.rd = self.round("r1", 1, None, "within_noise")
        self.failed("t1", None, plumbing="harness")
        self.failed("t2", {"infrastructure": None, "ids": {}}, plumbing="harness")
        data, _ = self.table()
        self.assertEqual([r["bucket"] for r in data["rows"]], ["harness_error"] * 2)

    def test_nothing_landed_is_model_failure_and_skips_the_test_name_check(self):
        self.rd = self.round("r1", 1, None, "within_noise")
        odd = "mini/TestFrobnicateWidgetsQuickly"
        self.failed("t1", {"ids": {odd: "failed"}, "failed": [odd], "infrastructure": None,
                           "expected": {"requested": [odd], "regression": []}},
                    cls="workflow_failure", outcome="build_blocked")
        self.finish()
        with unittest.mock.patch("sys.stdout"):
            code = buckets.buckets_main([self.rd, "--tasks", self.tasks, "--json", self.tmp + "/o.json"],
                                        reference=self.fail_if_called)
        self.assertEqual(code, 0)
        row = common.read_json(self.tmp + "/o.json")["rows"][0]
        self.assertEqual(row["bucket"], "model_failure")
        self.assertIn("no build landed", row["evidence"])
        self.assertIn("build_blocked", row["evidence"])

    def test_shape_round_does_not_grade_the_reference(self):
        self.rd = self.round("r1", 1, None, "within_noise")
        exp = common.read_json(self.rd + "/experiment.json")
        exp["phase"] = "shape"
        common.write_json(self.rd + "/experiment.json", exp)
        self.failed("t1", {"infrastructure": None, "scenarios": 3, "pass_on_reference": 3, "fail_on_start": 3,
                           "wrong_caught": 1, "wrong_total": 2})
        self.failed("t2", {"infrastructure": None, "scenarios": 3, "pass_on_reference": 2, "fail_on_start": 3,
                           "wrong_caught": 2, "wrong_total": 2})
        self.finish()
        with unittest.mock.patch("sys.stdout"):
            code = buckets.buckets_main([self.rd, "--tasks", self.tasks, "--json", self.tmp + "/o.json"],
                                        reference=self.fail_if_called)
        self.assertEqual(code, 0)
        self.assertEqual([r["bucket"] for r in common.read_json(self.tmp + "/o.json")["rows"]],
                         ["model_failure", "grader_bug"])

    def test_report_without_climb_section_names_it(self):
        self.rd = self.round("r1", 1, None, "within_noise")
        code, _, err = self.cli("lanes-buckets", self.rd, "--tasks", self.tasks)
        self.assertEqual(code, 2)
        self.assertIn("no 'climb' section", err)

    def test_report_required(self):
        self.rd = self.round("r1", 1, None, None)
        code, _, err = self.cli("lanes-buckets", self.rd, "--tasks", self.tasks)
        self.assertEqual(code, 2)
        self.assertIn("report.json missing", err)
        self.assertEqual(self.cli("lanes-buckets", self.rd)[0], 2)

    @unittest.skipUnless(shutil.which("go"), "go not installed")
    def test_real_grader_on_the_mini_task(self):
        """A wrong tree fails a hidden test the reference passes; a broken grader file fails both."""
        env = {"KOGEN_LANES_HOME": os.path.join(self.tmp, "home")}
        task = os.path.join(self.tasks, "t1")
        shutil.copytree(FIX, task, dirs_exist_ok=True)
        self.rd = self.round("r1", 1, None, "within_noise")
        with unittest.mock.patch.dict(os.environ, env):
            with grading.scratch(task, "wrong/negatives-clamped") as tree:
                ev = grading.evaluate_tree(grading.load_task(task), tree)
        self.assertFalse(ev["all_passed"])
        self.failed("t1", ev)
        self.finish()
        code, out, err = self.cli("lanes-buckets", self.rd, "--tasks", self.tasks, **env)
        self.assertEqual(code, 0, err)
        self.assertIn("| model_failure |", out)
        self.assertIn("TestAddNegative", out)
