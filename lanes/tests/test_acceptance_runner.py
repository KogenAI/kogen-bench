"""Acceptance runner and fixture repairs in grading (hardwhy, 31 Oct 2026): a runner that reports no scenario is
infrastructure, never a set of missing ids; grading supplies KOGEN_CUCUMBER/KOGEN_NODE; qualification fails loudly."""

import os
import stat
import unittest
import unittest.mock

from lanes import grading
from tests.test_grade import GradeCase, edit

ID = "acceptance:L3:Adds two numbers"
ACCEPTANCE = '''
[[command]]
name = "acceptance"
run = "{run}"
adapter = "lab_jsonl"
results = "acceptance.jsonl"
timeout_seconds = 60
'''


class Fresh(GradeCase):
    def setUp(self):
        super().setUp()
        grading._binary.clear()  # the in-process grader cache would point into an earlier test's removed home
        self.addCleanup(grading._binary.clear)


def executable(path, text="#!/bin/sh\nexit 0\n"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)
    return path


class AcceptanceRunner(Fresh):
    def setUp(self):
        super().setUp()
        env = unittest.mock.patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        for name in ("KOGEN_CUCUMBER", "KOGEN_NODE", "KOGEN_BIN"):
            os.environ.pop(name, None)

    def acceptance_task(self, run):
        """task-mini plus an acceptance command (lab_jsonl) and one expected acceptance id."""
        ev = os.path.join(self.task, "evaluator", "evaluate.toml")
        edit(ev, "[expected]", ACCEPTANCE.format(run=run.replace('"', '\\"')).lstrip() + "\n[expected]")
        edit(ev, 'requested = ["mini/TestAddPositive", "mini/TestAddNegative"]',
             f'requested = ["mini/TestAddPositive", "mini/TestAddNegative", "{ID}"]')

    def grade(self):
        c, d = self.cell("good", overlays=["reference"])
        return grading.grade_cell(self.run_dir, c, self.tasks)

    def test_runner_that_reports_no_scenario_is_infrastructure(self):
        # what run_acceptance.py wrote on kogen-loop-tool-cut with no Cucumber reachable: only the end marker, exit 0
        self.acceptance_task("""printf '{"suite":"finished"}\\n' > "$LAB_RESULTS\"""")
        ev = self.grade()
        self.assertFalse(ev["all_passed"])
        self.assertIn("acceptance run reported none of 1 expected scenarios", ev["infrastructure"])
        self.assertIn("KOGEN_CUCUMBER=unset", ev["infrastructure"])
        self.assertEqual(ev["missing"], [ID])

    def test_runner_that_writes_nothing_and_fails_is_infrastructure(self):
        self.acceptance_task("exit 1")
        ev = self.grade()
        self.assertFalse(ev["all_passed"])
        self.assertIn("runner did not execute", ev["infrastructure"])

    def test_a_reported_failing_scenario_stays_a_failure(self):
        self.acceptance_task(f"""printf '{{"id":"{ID}","state":"failed"}}\\n{{"suite":"finished"}}\\n' > "$LAB_RESULTS\"""")
        ev = self.grade()
        self.assertIsNone(ev["infrastructure"])
        self.assertFalse(ev["all_passed"])
        self.assertIn(ID, ev["failed"])

    def test_no_expected_acceptance_ids_no_check(self):
        ev = self.grade()
        self.assertIsNone(ev["infrastructure"])
        self.assertTrue(ev["all_passed"])

    def test_grading_supplies_the_runner_from_the_kogen_release_and_path(self):
        tmp = os.path.realpath(self.tmp)  # runner_vars resolves $KOGEN_BIN; macOS temp dirs sit behind the /var -> /private/var link
        rel = os.path.join(tmp, "kogen-x")
        executable(os.path.join(rel, "install.sh"))
        kogen = executable(os.path.join(rel, "bin", "kogen"))
        executable(os.path.join(rel, "lib", "cucumber", "node_modules", grading.CUCUMBER_JS))
        node = executable(os.path.join(tmp, "nodebin", "node"))
        os.environ.update(KOGEN_BIN=kogen, PATH=os.path.dirname(node) + os.pathsep + os.environ.get("PATH", ""))
        cuc = os.path.join(rel, "lib", "cucumber", "node_modules")
        self.assertEqual(grading.runner_vars(), {"KOGEN_CUCUMBER": cuc, "KOGEN_NODE": node})
        # the command sees them: it reports the scenario passed only when both are the supplied paths
        self.acceptance_task(f"""test "$KOGEN_CUCUMBER" = "{cuc}" && test "$KOGEN_NODE" = "{node}" && """
                             f"""printf '{{"id":"{ID}","state":"passed"}}\\n{{"suite":"finished"}}\\n' > "$LAB_RESULTS\"""")
        ev = self.grade()
        self.assertIsNone(ev["infrastructure"])
        self.assertTrue(ev["all_passed"], ev)

    def test_environment_runner_variables_win(self):
        rel = os.path.join(self.tmp, "kogen-y")
        executable(os.path.join(rel, "install.sh"))
        executable(os.path.join(rel, "lib", "cucumber", "node_modules", grading.CUCUMBER_JS))
        os.environ.update(KOGEN_BIN=executable(os.path.join(rel, "bin", "kogen")), KOGEN_CUCUMBER="/c", KOGEN_NODE="/n")
        self.assertEqual(grading.runner_vars(), {"KOGEN_CUCUMBER": "/c", "KOGEN_NODE": "/n"})

    def test_kogen_bin_outside_a_release_supplies_no_cucumber(self):
        os.environ["KOGEN_BIN"] = executable(os.path.join(self.tmp, "loose", "kogen"))
        self.assertNotIn("KOGEN_CUCUMBER", grading.runner_vars())

    def test_qualify_fails_when_the_runner_is_unavailable(self):
        edit(os.path.join(self.task, "task.toml"), 'run = "go test -count=1 ./features/steps/"',
             'run = "\\"$KOGEN_NODE\\" \\"$KOGEN_CUCUMBER/x.js\\" --format message:$KOGEN_ACCEPTANCE_REPORT"')
        os.environ["PATH"] = os.path.join(self.tmp, "empty")
        ok, detail = grading.qualify_acceptance(grading.load_task(self.task))
        self.assertFalse(ok)
        self.assertIn("acceptance runner unavailable: needs KOGEN_CUCUMBER, KOGEN_NODE", detail)


class FixtureRepairs(Fresh):
    def test_missing_fixture_is_laid_with_its_reason_and_graded(self):
        repairs = {"task-mini": [("fixture/copy.go.txt", "add.go", "test reason")]}
        with unittest.mock.patch.dict(grading.FIXTURE_REPAIRS, repairs):
            ev = grading.grade_cell(self.run_dir, self.cell("good", overlays=["reference"])[0], self.tasks)
        self.assertEqual(ev["fixture_repairs"], ["fixture/copy.go.txt: test reason"])
        self.assertTrue(ev["all_passed"])

    def test_present_fixture_is_left_alone(self):
        repairs = {"task-mini": [("add_test.go", "add.go", "never used")]}
        with unittest.mock.patch.dict(grading.FIXTURE_REPAIRS, repairs):
            ev = grading.grade_cell(self.run_dir, self.cell("good", overlays=["reference"])[0], self.tasks)
        self.assertNotIn("fixture_repairs", ev)
        self.assertTrue(ev["all_passed"])

    def test_revive_case_fixture(self):
        task = {"task": {"name": "revive-baseline-go"}}
        dst, src, _ = grading.FIXTURE_REPAIRS["revive-baseline-go"][0]
        tree = os.path.join(self.tmp, "revive")
        os.makedirs(os.path.dirname(os.path.join(tree, src)))
        with open(os.path.join(tree, src), "w") as f:
            f.write("package api\n")
        case_insensitive = os.path.exists(os.path.join(tree, src.replace("/V1/", "/v1/")))
        done = grading.repair_fixtures(task, tree)
        with open(os.path.join(tree, dst)) as f:
            self.assertEqual(f.read(), "package api\n")
        self.assertEqual(len(done), 0 if case_insensitive else 1)
        self.assertEqual(grading.repair_fixtures(task, tree), [])  # never twice, never over a file
        self.assertEqual(grading.repair_fixtures({"task": {"name": "other"}}, tree), [])


if __name__ == "__main__":
    unittest.main()
