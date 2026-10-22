"""ExUnit tasks: qualify and grade `task-mini-ex` (the `exunit_lab` adapter and Lab formatter)."""

import os
import shutil
import unittest

from lanes import grading
from tests.test_grade import BIN, GradeCase, edit

EX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "task-mini-ex")


@unittest.skipUnless(shutil.which("elixir") and shutil.which("mix"), "elixir and mix are not installed")
class ExUnitTask(GradeCase):
    def setUp(self):
        super().setUp()
        self.task = os.path.join(self.tasks, "task-mini-ex")
        shutil.copytree(EX, self.task)

    def test_fixture_qualifies(self):
        code, out, err = self.cli("lanes-qualify", self.task)
        self.assertEqual(code, 0, out + err)
        self.assertEqual(len(out.splitlines()), 5)

    def test_formatter_is_found_through_the_adapters_variable(self):
        env = grading.task_env(grading.load_task(self.task), os.path.join(self.tmp, "t", "tree"))
        self.assertTrue(os.path.isfile(os.path.join(env["KOGEN_LAB_ADAPTERS"], "lab_formatter.exs")))

    def test_wrong_tree_fails_the_requested_id_it_breaks(self):
        code, out, err = self.cli("lanes-qualify", self.task)
        self.assertIn("failed requested ids: LabEval.AddTest:test adds negatives", out)

    def test_grade_passes_reference_and_fails_wrong(self):
        good, gd = self.cell("good", overlays=["reference"], cell_id="task-mini-ex/r1/good")
        bad, bd = self.cell("bad", overlays=["wrong/negatives-clamped"], cell_id="task-mini-ex/r1/bad")
        code, out, err = self.cli("lanes-grade", self.run_dir)
        self.assertEqual(code, 0, err)
        self.assertIn(f"{good}: pass", out)
        self.assertIn(f"{bad}: fail", out)
        rec = self.evaluation(bd)
        self.assertEqual(rec["ids"]["LabEval.AddTest:test adds negatives"], "failed")
        self.assertEqual(rec["ids"]["MiniTest:test adds zero"], "passed")
        self.assertEqual(self.evaluation(gd)["totals"], {"expected": 3, "passed": 3})


if __name__ == "__main__":
    unittest.main()
