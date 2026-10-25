import os
import shutil
import unittest
import unittest.mock

from lanes import grading
from tests.test_grade import GradeCase, edit

E2E = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "e2e")
ACCEPT = 'run = \'python3 features/run_acceptance.py "$KOGEN_ACCEPTANCE_REPORT" "$KOGEN_ACCEPTANCE_FEATURES"\''


class Qualify(GradeCase):
    def qualify(self):
        code, out, err = self.cli("lanes-qualify", self.task)
        return code, out

    def failing(self, out):
        return [line[5:].split(": ")[0].split(" ", 1)[1] for line in out.splitlines() if line.startswith("FAIL")]

    def test_fixture_qualifies(self):
        code, out = self.qualify()
        self.assertEqual(code, 0, out)
        self.assertEqual(len(out.splitlines()), 6)
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


class FreshExport(GradeCase):
    def qualify(self):
        code, out, err = self.cli("lanes-qualify", self.task)
        return code, out

    def write(self, rel, text=""):
        path = os.path.join(self.task, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def accepting(self, run=ACCEPT):
        """task-mini with a report-writing acceptance command and a supplied Intent that carries the task's slug."""
        shutil.copy(os.path.join(E2E, "run_acceptance.py"), os.path.join(self.task, "start", "features"))
        edit(os.path.join(self.task, "task.toml"), 'run = "go test -count=1 ./features/steps/"', run)
        for name in ("intent.md", "acceptance.feature"):
            edit(os.path.join(self.task, "supplied", "gherkin", name), "add-numbers", "task-mini")

    def test_fresh_export_drops_ignored_files_and_keeps_tracked_ones(self):
        tree = os.path.join(self.tmp, "t", "tree")
        for rel, text in ((".gitignore", "/run\n/node_modules/\n"), ("run", "bin"), ("node_modules/x/f", "dep"),
                          ("pkg/.gitignore", "out\n"), ("pkg/out", "o"), ("pkg/keep", "k"), ("top", "t")):
            path = os.path.join(tree, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(text)
        with unittest.mock.patch.dict(os.environ, {"GIT_DIR": "/nonexistent"}):
            removed = grading.fresh_export(tree)
        self.assertEqual(sorted(removed), ["node_modules/x/f", "pkg/out", "run"])
        self.assertEqual(sorted(os.path.relpath(os.path.join(r, f), tree) for r, _, fs in os.walk(tree) for f in fs),
                         [".gitignore", "pkg/.gitignore", "pkg/keep", "top"])
        self.assertFalse(os.path.exists(os.path.join(tree, "node_modules")))
        self.assertEqual(os.listdir(os.path.dirname(tree)), ["tree"])  # no git dir left behind

    def test_ignored_build_output_cannot_mask_a_missing_build_step(self):
        edit(os.path.join(self.task, "task.toml"), "setup = []", 'setup = ["test -f built.txt"]')
        self.write("start/built.txt", "built by hand")
        self.write("start/.gitignore", "/built.txt\n")
        code, out = self.qualify()
        self.assertEqual(code, 1, out)
        self.assertIn("setup failed: test -f built.txt", out)

    def test_tracked_file_is_kept(self):
        edit(os.path.join(self.task, "task.toml"), "setup = []", 'setup = ["test -f built.txt"]')
        self.write("start/built.txt", "tracked")
        code, out = self.qualify()
        self.assertEqual(code, 0, out)

    def test_acceptance_on_the_reference_runs_from_a_fresh_export(self):
        self.accepting()
        code, out = self.qualify()
        self.assertEqual(code, 0, out)
        self.assertEqual(len(out.splitlines()), 6)
        self.assertIn("ok   task-mini acceptance: reference passes all 2 supplied scenarios from a fresh export", out)

    def test_acceptance_fails_when_only_the_evaluator_builds(self):  # acceptance steps run a binary that only the evaluator builds
        self.accepting('run = \'test -f built.txt && python3 features/run_acceptance.py "$KOGEN_ACCEPTANCE_REPORT" "$KOGEN_ACCEPTANCE_FEATURES"\'')
        edit(os.path.join(self.task, "evaluator", "evaluate.toml"), "setup = []", 'setup = ["touch built.txt"]')
        self.write("start/.gitignore", "/built.txt\n")
        self.write("start/built.txt", "left over from a build")
        code, out = self.qualify()
        self.assertEqual(code, 1, out)
        self.assertEqual([line.split(": ")[0] for line in out.splitlines() if line.startswith("FAIL")], ["FAIL task-mini acceptance"])
        self.assertIn("wrote no usable report", out)

    def test_acceptance_passes_when_the_task_setup_builds(self):
        self.accepting('run = \'test -f built.txt && python3 features/run_acceptance.py "$KOGEN_ACCEPTANCE_REPORT" "$KOGEN_ACCEPTANCE_FEATURES"\'')
        edit(os.path.join(self.task, "task.toml"), "setup = []", 'setup = ["touch built.txt"]')
        self.write("start/.gitignore", "/built.txt\n")
        code, out = self.qualify()
        self.assertEqual(code, 0, out)

    def test_acceptance_fails_when_the_reference_fails_a_scenario(self):
        self.accepting()
        shutil.copy(os.path.join(self.task, "start", "add.go"), os.path.join(self.task, "reference", "add.go"))
        code, out = self.qualify()
        self.assertEqual(code, 1)
        self.assertIn("FAIL task-mini acceptance: reference does not pass supplied scenarios at line", out)

    def test_acceptance_needing_a_missing_runner_variable_is_skipped(self):
        self.accepting('run = \'"$KOGEN_NODE" cucumber.js --format "message:$KOGEN_ACCEPTANCE_REPORT"\'')
        env = {k: v for k, v in os.environ.items() if k != "KOGEN_NODE"}
        with unittest.mock.patch.dict(os.environ, env, clear=True):
            code, out = self.qualify()
        self.assertEqual(code, 0, out)
        self.assertIn("ok   task-mini acceptance: skipped: needs KOGEN_NODE in the environment", out)

    def test_task_without_a_report_writing_acceptance_is_skipped(self):
        code, out = self.qualify()
        self.assertEqual(code, 0, out)
        self.assertIn("ok   task-mini acceptance: skipped", out)


if __name__ == "__main__":
    unittest.main()
