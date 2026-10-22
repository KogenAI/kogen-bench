import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from lanes import common, dispatch

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
        exp = {"id": "exp-mini", "phase": phase, "intent_form": "gherkin", "reps": 1, "deadline_s": 60,
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
