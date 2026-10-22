import glob
import os
import shutil
import subprocess
import tempfile
import unittest

from lanes import common

from .test_end_to_end import Pipeline, edit

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reproduce.sh")


class Reproduce(unittest.TestCase):
    """One published round (the fake Kogen, lanes-export with publication on), copied for each test."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.pipe = Pipeline(cls.tmp)
        run, _ = cls.pipe.run("rp-build", "build")
        cls.published, _ = cls.pipe.export(run, "lane-rp-build")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def setUp(self):
        self.round = os.path.join(tempfile.mkdtemp(), "lane-rp-build")
        self.addCleanup(shutil.rmtree, os.path.dirname(self.round))
        shutil.copytree(self.published, self.round)

    def reproduce(self, *args):
        return subprocess.run([SCRIPT, self.round, "--kogen-repo", self.pipe.repo, *args], capture_output=True,
                              text=True, env=self.pipe.env)

    def test_matching_round_exits_zero(self):
        r = self.reproduce()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("artifacts: 0 differ", r.stdout)
        self.assertIn("regrade: 4 of 4 cells match", r.stdout)

    def test_second_publish_private_keeps_the_trees_and_reproduces(self):
        out = os.path.join(self.pipe.bench, "rounds", "lane-rp-build")
        before = sorted(glob.glob(os.path.join(self.round, "reproduce", "cells", "**", "*.tar"), recursive=True))
        self.assertTrue(before)
        run = os.path.join(self.pipe.tmp, "runs", "rp-build")
        self.pipe.cli("lanes-export", run, "--round-id", "lane-rp-build", "--out", out, "--check", "round", "--publish-private")
        shutil.rmtree(self.round)
        shutil.copytree(out, self.round)
        self.assertEqual(sorted(glob.glob(os.path.join(self.round, "reproduce", "cells", "**", "*.tar"), recursive=True)), before)
        r = self.reproduce()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_changed_hidden_test_exits_one_and_names_the_file(self):
        edit(os.path.join(self.round, "reproduce", "tasks", "task-mini", "evaluator", "files", "add_hidden_test.go"), "Add(", "Add (")
        r = self.reproduce()
        self.assertEqual(r.returncode, 1)
        self.assertIn("MISMATCH tasks/task-mini/evaluator", r.stdout)
        self.assertNotIn("regrade:", r.stdout)

    def test_changed_patch_and_settings_are_named(self):
        with open(os.path.join(self.round, "patches", "wrong", "wrong.patch"), "a") as f:
            f.write("\n")
        edit(os.path.join(self.round, "reproduce", "settings", "base.json"), "gpt-6-luna", "gpt-6-sol")
        r = self.reproduce()
        self.assertEqual(r.returncode, 1)
        self.assertIn("MISMATCH patches/wrong/wrong.patch", r.stdout)
        self.assertIn("MISMATCH reproduce/settings/base.json", r.stdout)

    def test_changed_published_grade_exits_one(self):
        path = glob.glob(os.path.join(self.round, "bundles", "*", "attempts", "task-mini", "r1", "wrong", "a1", "evaluation.json"))[0]
        edit(path, '"all_passed": false', '"all_passed": true')
        r = self.reproduce()
        self.assertEqual(r.returncode, 1)
        self.assertIn("MISMATCH task-mini/r1/wrong: re-grade differs in all_passed", r.stdout)

    def test_unpublished_final_tree_exits_one(self):
        shutil.rmtree(os.path.join(self.round, "reproduce", "cells", "task-mini", "r2", "base"))
        r = self.reproduce()
        self.assertEqual(r.returncode, 1)
        self.assertIn("MISMATCH reproduce/cells/task-mini/r2/base", r.stdout)

    def test_different_artifact_is_reported_not_failed(self):
        os.remove(os.path.join(self.round, "records.jsonl"))
        edit(os.path.join(self.round, "PLAN.json"), self.plan_artifact("base"), "ab" * 32)
        r = self.reproduce()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("artifact base: DIFFERS", r.stdout)

    def plan_artifact(self, lane):
        return common.read_json(os.path.join(self.round, "PLAN.json"))["lock"]["artifacts"][lane]

    def test_rerun_prints_rerun_next_to_published(self):
        r = self.reproduce("--rerun", "1")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("results differ from run to run", r.stdout)
        lines = [l for l in r.stdout.splitlines() if l.startswith("  task-mini/")]
        self.assertEqual(len(lines), 2)  # one cell per lane
        for line in lines:
            self.assertIn("published", line)
            self.assertIn("| rerun", line)
            self.assertNotIn("rerun -", line)
        self.assertEqual(sum("rerun pass" in l for l in lines), 1)  # the base lane builds the right tree, the wrong lane not


if __name__ == "__main__":
    unittest.main()
