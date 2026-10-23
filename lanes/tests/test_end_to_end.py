"""The harness's acceptance test: real entry points, fake Kogen, a tiny task, two experiments."""

import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from lanes import common

from .test_export import make_bench

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
E2E = os.path.join(FIX, "e2e")
BIN = os.path.join(HERE, "..", "bin")
FAKE_KOGEN = os.path.join(HERE, "fake-kogen")
GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@" + "example.invalid", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"]
ACCEPT = "run = 'python3 features/run_acceptance.py \"$KOGEN_ACCEPTANCE_REPORT\" \"$KOGEN_ACCEPTANCE_FEATURES\"'"


def edit(path, old, new):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.replace(old, new))


class Pipeline:
    """Everything a test needs to run an experiment end to end inside `tmp`."""

    def __init__(self, tmp):
        self.tmp = tmp
        self.tasks = os.path.join(tmp, "tasks")
        task = os.path.join(self.tasks, "task-mini")
        shutil.copytree(os.path.join(FIX, "task-mini"), task)
        shutil.copy(os.path.join(E2E, "run_acceptance.py"), os.path.join(task, "start", "features"))
        edit(os.path.join(task, "task.toml"), 'run = "go test -count=1 ./features/steps/"', ACCEPT)
        for name in ("intent.md", "acceptance.feature"):  # a supplied Intent must carry the task's slug
            edit(os.path.join(task, "supplied", "gherkin", name), "add-numbers", "task-mini")
        self.repo = os.path.join(tmp, "kogen-src")
        shutil.copytree(os.path.join(E2E, "kogen-src"), self.repo)
        for cmd in (["init", "-q"], ["add", "-A"], ["commit", "-q", "-m", "fixture"]):
            subprocess.run([*GIT, *cmd], cwd=self.repo, check=True)
        self.sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo, check=True, capture_output=True, text=True).stdout.strip()
        self.exp_dir = os.path.join(tmp, "exp")
        os.makedirs(os.path.join(self.exp_dir, "patches"))
        edit(os.path.join(self.repo, "cmd", "kogen", "main.go"), 'const mode = "correct"', 'const mode = "wrong"')
        with open(os.path.join(self.exp_dir, "patches", "wrong.patch"), "w") as f:
            subprocess.run(["git", "diff"], cwd=self.repo, check=True, stdout=f)
        subprocess.run(["git", "checkout", "-q", "."], cwd=self.repo, check=True)
        self.hosts = os.path.join(tmp, "hosts.json")
        common.write_json(self.hosts, {"local": {"target": "local", "slots": 2}})
        self.bench = os.path.join(tmp, "bench")
        make_bench(self.bench)
        self.env = dict(os.environ, KOGEN_LANES_HOME=os.path.join(tmp, "home"), KOGEN_LANES_TASKS=self.tasks,
                        FAKE_KOGEN_SCRIPT=FAKE_KOGEN, FAKE_KOGEN_TASK=task,
                        LANE_SHAPE_INTENT=os.path.join(task, "supplied", "gherkin"))

    def cli(self, name, *args, ok=True):
        r = subprocess.run([sys.executable, os.path.join(BIN, name), *args], capture_output=True, text=True, env=self.env)
        if ok and r.returncode:
            raise AssertionError(f"{name} {' '.join(args)} exited {r.returncode}\n{r.stdout}\n{r.stderr}")
        return r

    def experiment(self, exp_id, phase):
        lanes = [{"name": n, "sha": self.sha, "patch": p, "settings": {"models": dict.fromkeys(("shape", "build", "review"), "openai/gpt-6-luna high")}}
                 for n, p in ((("base", None), ("wrong", "patches/wrong.patch")) if phase == "build" else (("shaper", None),))]
        rule = ({"kind": "paired_sign", "baseline": "wrong", "candidate": "base", "max_p": "0.5"} if phase == "build"
                else {"kind": "descriptive"})
        exp = {"id": exp_id, "phase": phase, "kogen": {"repo": self.repo}, "lanes": lanes, "tasks": ["task-mini"],
               "reps": 2 if phase == "build" else 1, "deadline_s": 120, "cost_cap_usd": 100, "hosts": ["local"], "decision_rule": rule}
        if phase == "build":
            exp["intent_form"] = "gherkin"
        path = os.path.join(self.exp_dir, exp_id + ".json")
        common.write_json(path, exp)
        return path

    def run(self, exp_id, phase):
        """lanes-build, -plan, -run, -grade, -report; returns (run dir, report output)."""
        path, run = self.experiment(exp_id, phase), os.path.join(self.tmp, "runs", exp_id)
        self.cli("lanes-build", path, "--run-dir", run)
        self.cli("lanes-plan", path, "--run-dir", run)
        self.cli("lanes-run", run, "--hosts", self.hosts)
        self.cli("lanes-grade", run)
        return run, self.cli("lanes-report", run).stdout

    def export(self, run, round_id):
        """lanes-export with the strict round check (the whole-checkout release gate takes minutes), then the private inputs and each cell's trees published (--publish-private)."""
        out = os.path.join(self.bench, "rounds", round_id)
        args = [run, "--round-id", round_id, "--out", out, "--date", "2026-10-22", "--check", "round"]
        r = self.cli("lanes-export", *args)
        self.cli("lanes-export", *args, "--publish-private")
        return out, r.stdout


class EndToEnd(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.p = Pipeline(self.tmp)

    def test_build_experiment_picks_the_correct_lane(self):
        run, verdict = self.p.run("e2e-build", "build")
        self.assertIn("base vs wrong", verdict)
        self.assertIn("KEEP", verdict)
        for lane, want in (("base", True), ("wrong", False)):
            for rep in (1, 2):
                ev = common.read_json(os.path.join(common.cell_dir(run, f"task-mini/r{rep}/{lane}"), "evaluation.json"))
                self.assertIs(ev["all_passed"], want, f"{lane} r{rep}")
        rep = common.read_json(os.path.join(run, "report.json"))
        for lane in rep["lanes"]:
            self.assertEqual({s["stage"] for s in lane["stages"]}, {"approve", "build", "review"})
            self.assertGreater(lane["totals"]["cost_usd"], 0)
        lock = {e["name"]: e["artifact_sha256"] for e in common.read_json(os.path.join(run, "lanes.lock.json"))}
        self.assertNotEqual(lock["base"], lock["wrong"])
        out, text = self.p.export(run, "lane-e2e-build")
        self.assertIn("PASS", text)
        r = subprocess.run([os.path.join(HERE, "..", "reproduce.sh"), out, "--kogen-repo", self.p.repo], capture_output=True, text=True, env=self.p.env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("every published input matches PLAN.json", r.stdout)
        self.assertIn("artifacts: 0 differ", r.stdout)
        self.assertIn("re-grades match", r.stdout)

    def test_shape_experiment(self):
        run, verdict = self.p.run("e2e-shape", "shape")
        self.assertIn("no decision", verdict)
        ev = common.read_json(os.path.join(common.cell_dir(run, "task-mini/r1/shaper"), "evaluation.json"))
        self.assertEqual((ev["scenarios"], ev["pass_on_reference"], ev["wrong_caught"], ev["wrong_total"]), (2, 2, 1, 1))
        rep = common.read_json(os.path.join(run, "report.json"))
        self.assertEqual([s["stage"] for s in rep["lanes"][0]["stages"]], ["shape"])
        self.assertGreater(rep["lanes"][0]["totals"]["cost_usd"], 0)
        out, text = self.p.export(run, "lane-e2e-shape")
        self.assertIn("PASS", text)
        r = subprocess.run([os.path.join(HERE, "..", "reproduce.sh"), out, "--kogen-repo", self.p.repo], capture_output=True, text=True, env=self.p.env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("re-grades match", r.stdout)


if __name__ == "__main__":
    unittest.main()
