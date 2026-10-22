import os
import shutil
import unittest

from tests.test_grade import GradeCase, edit


class Qualify(GradeCase):
    def qualify(self):
        code, out, err = self.cli("lanes-qualify", self.task)
        return code, out

    def failing(self, out):
        return [line[5:].split(": ")[0].split(" ", 1)[1] for line in out.splitlines() if line.startswith("FAIL")]

    def test_fixture_qualifies(self):
        code, out = self.qualify()
        self.assertEqual(code, 0, out)
        self.assertEqual(len(out.splitlines()), 5)
        self.assertTrue(all(line.startswith("ok") for line in out.splitlines()))

    def test_reference_must_pass(self):
        shutil.copy(os.path.join(self.task, "start", "add.go"), os.path.join(self.task, "reference", "add.go"))
        code, out = self.qualify()
        self.assertEqual(code, 1)
        self.assertEqual(self.failing(out), ["reference"])

    def test_start_must_fail_requested_tests(self):
        shutil.copy(os.path.join(self.task, "reference", "add.go"), os.path.join(self.task, "start", "add.go"))
        code, out = self.qualify()
        self.assertEqual(code, 1)
        self.assertIn("start", self.failing(out))
        self.assertIn("requested id mini/TestAddPositive passed on the start", out)

    def test_wrong_tree_must_fail(self):
        shutil.copy(os.path.join(self.task, "reference", "add.go"),
                    os.path.join(self.task, "wrong", "negatives-clamped", "add.go"))
        code, out = self.qualify()
        self.assertEqual(self.failing(out), ["wrong/negatives-clamped"])

    def test_wrong_tree_that_does_not_compile_is_not_a_known_wrong_solution(self):
        with open(os.path.join(self.task, "wrong", "negatives-clamped", "add.go"), "w") as f:
            f.write("package mini\n\nfunc Add(a, b int) int { return a +\n")
        code, out = self.qualify()
        self.assertEqual(code, 1)
        self.assertEqual(self.failing(out), ["wrong/negatives-clamped"])
        self.assertIn("no requested id failed", out)

    def test_wrong_tree_detail_names_the_failed_ids(self):
        code, out = self.qualify()
        self.assertIn("failed requested ids: mini/TestAddNegative", out)

    def test_start_must_pass_regression_ids(self):
        with open(os.path.join(self.task, "start", "add.go"), "w") as f:
            f.write("package mini\n\nfunc Add(a, b int) int { return 1 }\n")
        code, out = self.qualify()
        self.assertEqual(code, 1)
        self.assertEqual(self.failing(out)[:1], ["start"])
        self.assertIn("regression id mini/TestAddZero did not pass on the start", out)

    def test_no_requested_ids(self):
        edit(os.path.join(self.task, "evaluator", "evaluate.toml"), 'requested = ["mini/TestAddPositive", "mini/TestAddNegative"]',
             "requested = []")
        code, out = self.qualify()
        self.assertIn("no requested ids in [expected]", out)

    def test_reference_must_reproduce_exactly_the_expected_ids(self):
        with open(os.path.join(self.task, "evaluator", "files", "extra_test.go"), "w") as f:
            f.write('package mini\n\nimport "testing"\n\nfunc TestExtra(t *testing.T) {}\n')
        edit(os.path.join(self.task, "evaluator", "evaluate.toml"), "-run '^(TestAddPositive|TestAddNegative)$'",
             "-run '^(TestAddPositive|TestAddNegative|TestExtra)$'")
        code, out = self.qualify()
        self.assertEqual(self.failing(out), ["reference"])
        self.assertIn("did not reproduce the expected passing ids", out)

    def test_wrong_tree_required(self):
        shutil.rmtree(os.path.join(self.task, "wrong"))
        code, out = self.qualify()
        self.assertEqual(self.failing(out), ["wrong"])

    def test_without_hidden_tests_must_not_pass(self):
        edit(os.path.join(self.task, "evaluator", "evaluate.toml"), 'requested = ["mini/TestAddPositive", "mini/TestAddNegative"]',
             'requested = []')
        code, out = self.qualify()
        self.assertEqual(code, 1)
        self.assertIn("emptied overlay", self.failing(out))

    def test_setup_failure_fails_the_task(self):
        edit(os.path.join(self.task, "task.toml"), "setup = []", 'setup = ["exit 1"]')
        code, out = self.qualify()
        self.assertEqual(code, 1)
        self.assertIn("setup failed: exit 1", out)

    def test_broken_task_folder(self):
        os.remove(os.path.join(self.task, "task.toml"))
        code, out = self.qualify()
        self.assertEqual((code, self.failing(out)), (1, ["task"]))


if __name__ == "__main__":
    unittest.main()
