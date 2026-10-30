import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from lanes import cell, common, dispatch, preflight

HERE = os.path.dirname(os.path.abspath(__file__))
FAKE = os.path.join(HERE, "fake-kogen")
TASK = os.path.join(HERE, "fixtures", "task-mini")
ENTRY = os.path.join(HERE, "..", "bin", "lanes-preflight")
RUN = os.path.join(HERE, "..", "bin", "lanes-run")
SHA = "0123456789abcdef0123456789abcdef01234567"


class PreflightTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = self._tmp.name
        self.tasks = os.path.join(self.tmp, "tasks")
        shutil.copytree(TASK, os.path.join(self.tasks, "task-mini"))
        self.intent_md = os.path.join(self.tasks, "task-mini", "supplied", "gherkin", "intent.md")
        with open(self.intent_md) as f:
            text = f.read()
        with open(self.intent_md, "w") as f:
            f.write(text.replace("add-numbers", "task-mini"))
        self.home = os.path.join(self.tmp, "home")
        self.run_dir = os.path.join(self.tmp, "run")
        self.make_run("build")

    def make_run(self, phase, lanes=("base", "patched")):
        exp = {"id": "exp-mini", "phase": phase, "intent_form": "gherkin", "reps": 1, "deadline_s": 60, "cost_cap_usd": 100,
               "kogen": {"repo": "https://example.invalid/kogen.git"}, "tasks": ["task-mini"], "hosts": ["local"],
               "decision_rule": {"kind": "paired-pass-rate"},
               "lanes": [{"name": n, "sha": SHA, "patch": None, "settings": {}} for n in lanes]}
        if phase != "build":
            del exp["intent_form"]
        common.write_json(os.path.join(self.run_dir, "experiment.json"), exp)

    def preflight(self, **env):
        e = {**os.environ, "KOGEN_LANES_HOME": self.home, "FAKE_KOGEN_TASK": TASK, **env}
        return subprocess.run([sys.executable, ENTRY, self.run_dir, "--tasks", self.tasks, "--artifact", FAKE],
                              env=e, capture_output=True, text=True, timeout=60)

    def test_one_line_per_task_and_lane(self):
        p = self.preflight()
        self.assertEqual(p.returncode, 0, p.stderr)
        lines = p.stdout.splitlines()
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith("task-mini x base: ok"))
        self.assertTrue(lines[1].startswith("task-mini x patched: ok"))

    def test_lint_refusal_names_kogens_lines(self):
        p = self.preflight(FAKE_KOGEN_LINT="refuse")
        self.assertEqual(p.returncode, 1)
        self.assertEqual(p.stdout.count("REFUSED"), 2)
        self.assertIn("intent/lint: task-mini: scenario 'As requested' has no Then step", p.stdout)
        self.assertIn("no cell may start", p.stderr)

    def test_wrong_slug_is_refused_before_kogen_runs(self):
        with open(self.intent_md) as f:
            text = f.read()
        with open(self.intent_md, "w") as f:
            f.write(text.replace("Slug: task-mini", "Slug: other-name"))
        p = self.preflight()
        self.assertEqual(p.returncode, 1)
        self.assertIn("other-name", p.stdout)

    def test_no_intent_phase_checks_nothing(self):
        self.make_run("shape")
        p = self.preflight(FAKE_KOGEN_LINT="refuse")
        self.assertEqual(p.returncode, 0)
        self.assertIn("nothing to check", p.stdout)

    def set_task_toml(self, line):
        path = os.path.join(self.tasks, "task-mini", "task.toml")
        with open(path) as f:
            text = f.read()
        with open(path, "w") as f:
            f.write(line + "\n" + text)  # before the first table, so it is a top-level key

    def preflight_here(self, deadline_s=1, **env):
        """In-process, with the default approval deadline cut to `deadline_s`; returns `(refusals, lines)`."""
        lines = []
        e = {"KOGEN_LANES_HOME": self.home, "FAKE_KOGEN_TASK": TASK, **env}
        with mock.patch.dict(os.environ, e), mock.patch.object(preflight, "DEADLINE_S", deadline_s):
            bad = preflight.preflight(self.run_dir, self.tasks, artifact=FAKE, out=lines.append)
        return bad, lines

    def test_default_approval_deadline_is_120_seconds(self):
        self.assertEqual(preflight.DEADLINE_S, 120)

    def test_default_deadline_applies_without_the_key(self):
        bad, lines = self.preflight_here(FAKE_KOGEN_APPROVE_DELAY_S="2")
        self.assertEqual(bad, 0)
        self.assertEqual(sum("DEFERRED: approve refused (timed out)" in line for line in lines), 2)
        self.assertIn("task-mini", common.read_json(os.path.join(self.run_dir, "PLAN.json"))["approval_deferrals"])

    def test_approve_timeout_s_replaces_the_deadline(self):
        self.set_task_toml("approve_timeout_s = 20")
        bad, lines = self.preflight_here(FAKE_KOGEN_APPROVE_DELAY_S="2")  # 2 s per call > the 1 s default
        self.assertEqual((bad, len(lines)), (0, 2), lines)
        self.assertTrue(all(": ok: approved " in line for line in lines))

    def test_approve_timeout_s_is_still_a_deadline(self):
        self.set_task_toml("approve_timeout_s = 1")
        bad, lines = self.preflight_here(deadline_s=60, FAKE_KOGEN_APPROVE_DELAY_S="3")
        self.assertEqual(bad, 0)
        self.assertIn("approve refused (timed out)", lines[0])

    def test_invalid_approve_timeout_s_is_refused_before_kogen_runs(self):
        for value in ("0", "-5", "1.5", '"60"', "true", "3601", "[]"):
            with self.subTest(value=value):
                self.make_run("build", lanes=("base",))
                self.restore_task_toml()
                self.set_task_toml(f"approve_timeout_s = {value}")
                bad, lines = self.preflight_here()
                self.assertEqual(bad, 1)
                self.assertIn("REFUSED: task.toml approve_timeout_s", lines[0])
                self.assertIn("1 to 3600", lines[0])

    def restore_task_toml(self):
        shutil.copy(os.path.join(TASK, "task.toml"), os.path.join(self.tasks, "task-mini", "task.toml"))

    def test_cap_is_accepted(self):
        self.set_task_toml(f"approve_timeout_s = {cell.APPROVE_TIMEOUT_MAX_S}")
        bad, lines = self.preflight_here()
        self.assertEqual(bad, 0, lines)

    def test_lanes_run_refuses_to_start_any_cell(self):
        art = "ab" * 32
        os.makedirs(os.path.join(self.home, "artifacts", art))
        shutil.copy(FAKE, os.path.join(self.home, "artifacts", art, "kogen"))
        common.write_json(os.path.join(self.run_dir, "lanes.lock.json"),
                          [{"name": n, "sha": SHA, "patch_sha256": None, "artifact_sha256": art,
                            "kogen_version": "v"} for n in ("base", "patched")])
        hosts = os.path.join(self.tmp, "hosts.json")
        common.write_json(hosts, {"local": {"target": "local", "slots": 1}})
        env = {**os.environ, "KOGEN_LANES_HOME": self.home, "FAKE_KOGEN_TASK": TASK, "FAKE_KOGEN_LINT": "refuse"}
        with mock.patch.dict(os.environ, env), mock.patch.object(dispatch, "verify_inputs"):
            logged = []
            with self.assertRaises(dispatch.DispatchError):
                dispatch.run_all(self.run_dir, self.tasks, hosts, log=logged.append)
        self.assertTrue(any("intent/lint" in m for m in logged))
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "cells")))

    def test_lanes_run_help_says_skip_is_for_tests(self):
        p = subprocess.run([sys.executable, RUN, "--help"], capture_output=True, text=True)
        self.assertIn("--skip-preflight", p.stdout)
        self.assertIn("never in a real run", " ".join(p.stdout.split()))


if __name__ == "__main__":
    unittest.main()
