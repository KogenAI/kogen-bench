import contextlib
import io
import json
import os
import shlex
import shutil
import subprocess
import tempfile
import unittest

from lanes import common, plan_hashes

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


class PlanHashes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.tasks = os.path.join(self.tmp, "tasks")
        self.task = os.path.join(self.tasks, "task-mini")
        shutil.copytree(os.path.join(FIX, "task-mini"), self.task)
        exp = common.read_json(os.path.join(FIX, "experiment-good.json"))
        exp["tasks"] = ["task-mini"]
        self.exp = os.path.join(self.tmp, "experiment.json")
        common.write_json(self.exp, exp)
        os.makedirs(os.path.join(self.tmp, "patches"))
        with open(os.path.join(self.tmp, "patches", "p1.patch"), "w") as f:
            f.write("--- a\n+++ b\n")
        self.lock = os.path.join(self.tmp, "lanes.lock.json")
        common.write_json(self.lock, [{"name": n, "sha": "0" * 40, "patch_sha256": None,
                                       "artifact_sha256": "ab" * 32, "kogen_version": "v"}
                                      for n in ("base", "patched")])

    def plan(self):
        return plan_hashes.build_plan(self.exp, self.tasks, self.lock)

    def test_stable_and_complete(self):
        a, b = self.plan(), self.plan()
        self.assertEqual(a, b)
        t = a["hashes"]["tasks"]["task-mini"]
        for k in ("task", "tree", "hidden_tests", "task_toml", "request"):
            self.assertRegex(t[k], r"^[0-9a-f]{64}$")
        self.assertEqual(list(t["intents"]), ["gherkin"])
        self.assertIsNone(a["hashes"]["lanes"]["base"]["patch"])
        self.assertRegex(a["hashes"]["lanes"]["patched"]["patch"], r"^[0-9a-f]{64}$")
        self.assertEqual(a["lock"]["artifacts"], {"base": "ab" * 32, "patched": "ab" * 32})
        self.assertEqual(a["experiment"]["id"], "exp-mini")

    def test_hosts_are_not_published(self):
        exp = common.read_json(self.exp)
        exp["hosts"] = ["secret-host"]
        common.write_json(self.exp, exp)
        plan = self.plan()
        self.assertNotIn("hosts", plan["experiment"])
        self.assertNotIn("secret-host", json.dumps(plan))

    def test_whole_task_hash_covers_reference_and_wrong(self):
        before = self.plan()["hashes"]["tasks"]["task-mini"]
        with open(os.path.join(self.task, "reference", "add.go"), "a") as f:
            f.write("// changed\n")
        after = self.plan()["hashes"]["tasks"]["task-mini"]
        self.assertNotEqual(before["task"], after["task"])
        self.assertEqual(before["tree"], after["tree"])

    def fails(self, *args):
        """Run main; assert exit 2, no PLAN written, and return stderr."""
        out = os.path.join(self.tmp, "PLAN-bad.json")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = plan_hashes.main([self.exp, "--out", out] + list(args or ("--tasks", self.tasks, "--lock", self.lock)))
        self.assertEqual(code, 2)
        self.assertFalse(os.path.exists(out))
        return err.getvalue()

    def test_missing_task_start_or_evaluator_exits_2(self):
        self.assertIn("task-mini", self.fails("--tasks", os.path.join(self.tmp, "nope"), "--lock", self.lock))
        shutil.move(os.path.join(self.task, "evaluator"), os.path.join(self.tmp, "ev"))
        self.assertIn("evaluator", self.fails())
        shutil.move(os.path.join(self.tmp, "ev"), os.path.join(self.task, "evaluator"))
        shutil.rmtree(os.path.join(self.task, "start"))
        self.assertIn("start", self.fails())

    def test_missing_intent_form_exits_2(self):
        shutil.rmtree(os.path.join(self.task, "supplied", "gherkin"))
        self.assertIn("supplied/gherkin", self.fails())

    def test_request_needed_only_by_shaping_phases(self):
        os.remove(os.path.join(self.task, "request.md"))
        self.assertIsNone(self.plan()["hashes"]["tasks"]["task-mini"]["request"])  # build phase
        exp = common.read_json(self.exp)
        exp["phase"] = "shape"
        common.write_json(self.exp, exp)
        self.assertIn("request.md", self.fails())

    def test_bad_lock_exits_2(self):
        def lock(data):
            common.write_json(self.lock, data)
            return self.fails()
        self.assertIn("lock: must be a list", lock({}))
        self.assertIn("lock[0].artifact_sha256", lock([{"name": "base"}]))
        self.assertIn("lock[0].name", lock([{"artifact_sha256": "ab"}]))
        self.assertIn("no entry for lane patched", lock([{"name": "base", "artifact_sha256": "ab"}]))

    def test_hidden_test_change_changes_only_its_hash(self):
        before = self.plan()["hashes"]["tasks"]["task-mini"]
        with open(os.path.join(self.task, "evaluator", "files", "add_hidden_test.go"), "a") as f:
            f.write("// changed\n")
        after = self.plan()["hashes"]["tasks"]["task-mini"]
        self.assertNotEqual(before["hidden_tests"], after["hidden_tests"])
        changed = ("hidden_tests", "task")  # the whole-task hash covers the evaluator too
        self.assertNotEqual(before["task"], after["task"])
        self.assertEqual({k: v for k, v in before.items() if k not in changed},
                         {k: v for k, v in after.items() if k not in changed})

    def test_intent_patch_and_settings_changes(self):
        before = self.plan()
        with open(os.path.join(self.task, "supplied", "gherkin", "intent.md"), "a") as f:
            f.write("x\n")
        with open(os.path.join(self.tmp, "patches", "p1.patch"), "a") as f:
            f.write("+more\n")
        exp = common.read_json(self.exp)
        exp["lanes"][0]["settings"]["models"]["build"] = "openai/gpt-x low"
        common.write_json(self.exp, exp)
        after = self.plan()
        self.assertNotEqual(before["hashes"]["tasks"]["task-mini"]["intents"], after["hashes"]["tasks"]["task-mini"]["intents"])
        self.assertNotEqual(before["hashes"]["lanes"]["patched"]["patch"], after["hashes"]["lanes"]["patched"]["patch"])
        self.assertNotEqual(before["hashes"]["lanes"]["base"]["settings"], after["hashes"]["lanes"]["base"]["settings"])
        self.assertEqual(before["hashes"]["lanes"]["patched"]["settings"], after["hashes"]["lanes"]["patched"]["settings"])

    def test_command_line_writes_plan(self):
        out = os.path.join(self.tmp, "PLAN.json")
        code = plan_hashes.main([self.exp, "--tasks", self.tasks, "--lock", self.lock, "--out", out])
        self.assertEqual(code, 0)
        self.assertEqual(common.read_json(out), self.plan())
        self.assertIn("nope.json", self.fails("--tasks", self.tasks, "--lock", os.path.join(self.tmp, "nope.json")))


@unittest.skipUnless(shutil.which("go"), "go not installed")
class TaskMiniAcceptance(unittest.TestCase):
    """task-mini's acceptance run fails on start/ and wrong/, passes on reference/ (L1 review r2-m1)."""

    def accept(self, *overlays):
        try:
            import tomllib
        except ImportError:
            self.skipTest("tomllib needs Python 3.11")
        task = os.path.join(FIX, "task-mini")
        with tempfile.TemporaryDirectory() as tree:
            for src in ("start",) + overlays:
                shutil.copytree(os.path.join(task, src), tree, dirs_exist_ok=True)
            with open(os.path.join(task, "task.toml"), "rb") as f:
                run = tomllib.load(f)["acceptance"]["run"]
            return subprocess.run(shlex.split(run), cwd=tree, capture_output=True).returncode

    def test_acceptance(self):
        self.assertNotEqual(self.accept(), 0)
        self.assertNotEqual(self.accept("wrong/negatives-clamped"), 0)
        self.assertEqual(self.accept("reference"), 0)


if __name__ == "__main__":
    unittest.main()
