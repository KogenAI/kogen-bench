import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

from lanes import common

HERE = os.path.dirname(os.path.abspath(__file__))
FAKE = os.path.join(HERE, "fake-kogen")
TASK = os.path.join(HERE, "fixtures", "task-mini")
EVENTS_NEEDED = {"start", "request", "pass", "review", "commit", "outcome"}
GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@" + "example.invalid", "-c", "commit.gpgsign=false",
       "-c", "core.hooksPath=/dev/null"]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def sh(*cmd, cwd=None, env=None, input=None):
    return subprocess.run(cmd, cwd=cwd, env=env, input=input, capture_output=True, text=True)


class FakeKogen(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tree = os.path.join(self._tmp.name, "work")
        shutil.copytree(os.path.join(TASK, "start"), self.tree)
        for args in (["init", "-q"], ["add", "-A"], ["commit", "-qm", "start"]):
            subprocess.run([*GIT[:1], "-C", self.tree, *GIT[1:], *args], check=True, capture_output=True)

    def kogen(self, *args, mode="correct", **extra):
        env = {**os.environ, "FAKE_KOGEN_MODE": mode, **extra}
        return sh(sys.executable, FAKE, *args, cwd=self.tree, env=env)

    def head(self):
        return sh("git", "-C", self.tree, "rev-parse", "HEAD").stdout

    def request_file(self):
        path = os.path.join(self._tmp.name, "request.md")
        write(path, read(os.path.join(TASK, "request.md")))
        return path

    def approve(self, *extra):
        self.assertEqual(self.kogen("init").returncode, 0)
        self.assertEqual(self.kogen("intent", "shape", "add-numbers", self.request_file(), *extra).returncode, 0)
        card = self.kogen("intent", "approve", "add-numbers", *extra)
        self.assertEqual(card.returncode, 5)
        sha = [l.split()[1] for l in card.stdout.splitlines() if l.startswith("SHA-256:")][0]
        self.assertEqual(self.kogen("intent", "approve", "add-numbers", sha[:8], *extra).returncode, 0)

    def pipeline(self, mode):
        self.approve()
        return self.kogen("intent", "build", "add-numbers", mode=mode)

    def test_version(self):
        r = self.kogen("version", FAKE_KOGEN_VERSION="kogen abc12345 (2026-02-02)")
        self.assertEqual(r.stdout.strip(), "kogen abc12345 (2026-02-02)")

    def test_unknown_mode_exits_2(self):
        r = self.kogen("version", mode="wrng")
        self.assertEqual(r.returncode, 2)
        self.assertIn("FAKE_KOGEN_MODE", r.stdout)

    def test_init_writes_config_and_gitignore(self):
        r = self.kogen("init")
        self.assertEqual(r.returncode, 0)
        text = read(os.path.join(self.tree, ".kogen", "project.yaml"))
        self.assertIn("version: 1", text)
        self.assertIn("build:", text)
        self.assertIn(".kogen/local/", read(os.path.join(self.tree, ".gitignore")).splitlines())
        self.assertEqual(sh("git", "-C", self.tree, "log", "-1", "--format=%s").stdout.strip(),
                         "Add Kogen configuration")
        head = self.head()
        again = self.kogen("init")  # already initialized: no-op
        self.assertEqual(again.returncode, 0)
        self.assertIn("already initialized", again.stdout)
        self.assertEqual(self.head(), head)

    def test_init_takes_no_options(self):
        for args in (["init", "--project", self.tree], ["init", "--by", "x"], ["init", "extra"]):
            with self.subTest(args=args):
                r = self.kogen(*args)
                self.assertEqual(r.returncode, 2)
                self.assertFalse(os.path.exists(os.path.join(self.tree, ".kogen")))
        self.assertIn("unknown option '--project'", self.kogen("init", "--project", "x").stdout)

    def test_project_option_where_kogen_has_it(self):
        elsewhere = tempfile.mkdtemp(dir=self._tmp.name)
        self.assertEqual(self.kogen("init").returncode, 0)
        r = sh(sys.executable, FAKE, "intent", "shape", "add-numbers", self.request_file(),
               "--project", self.tree, cwd=elsewhere)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertTrue(os.path.exists(os.path.join(self.tree, ".kogen/intents/add-numbers/intent.md")))
        self.assertEqual(sh(sys.executable, FAKE, "version", "--project", self.tree, cwd=elsewhere).returncode, 2)
        self.assertEqual(self.kogen("intent", "build", "add-numbers", "--bogus", "1").returncode, 2)

    def test_shape_reads_stdin_and_writes_intent(self):
        self.kogen("init")
        r = sh(sys.executable, FAKE, "intent", "shape", "add-numbers", "-", cwd=self.tree, input="# Add\nbody\n")
        self.assertEqual(r.returncode, 0)
        for f in ("intent.md", "acceptance.feature"):
            self.assertTrue(os.path.exists(os.path.join(self.tree, ".kogen/intents/add-numbers", f)))

    def shaping_events(self):
        path = os.path.join(self.tree, ".kogen/local/shaping/add-numbers/events.ndjson")
        return [json.loads(l) for l in read(path).splitlines()]

    def test_shaping_events_use_kogens_names(self):  # shape.ex l.374, shape_evidence.ex l.276
        self.kogen("init")
        self.assertEqual(self.kogen("intent", "shape", "add-numbers", self.request_file()).returncode, 0)
        call, end = self.shaping_events()
        self.assertEqual(call["role"], "shape")
        self.assertEqual(end, {"event": "session_end", "elapsed_ms": 420})

    def test_questions_mode(self):
        self.kogen("init")
        first = self.kogen("intent", "shape", "add-numbers", self.request_file(), FAKE_KOGEN_QUESTIONS="once")
        self.assertEqual((first.returncode, first.stdout.splitlines()[0]), (5, "Questions for add-numbers:"))
        self.assertFalse(os.path.exists(os.path.join(self.tree, ".kogen/intents/add-numbers/intent.md")))
        env = {**os.environ, "FAKE_KOGEN_QUESTIONS": "once"}
        done = sh(sys.executable, FAKE, "intent", "shape", "add-numbers", "-", cwd=self.tree, env=env, input="1: a\n")
        self.assertEqual(done.returncode, 0)
        env["FAKE_KOGEN_QUESTIONS"] = "always"
        again = sh(sys.executable, FAKE, "intent", "shape", "add-numbers", "-", cwd=self.tree, env=env, input="1: a\n")
        self.assertEqual(again.returncode, 5)

    def test_init_commits_a_leftover_project_yaml_as_it_is(self):
        os.makedirs(os.path.join(self.tree, ".kogen"))
        write(os.path.join(self.tree, ".kogen", "project.yaml"), "version: 1\nmodels:\n  build: {model: mine, effort: low}\n")
        self.assertEqual(self.kogen("init").returncode, 0)
        self.assertIn("model: mine", sh("git", "-C", self.tree, "show", "HEAD:.kogen/project.yaml").stdout)

    def test_bad_slug_exits_2(self):
        self.assertEqual(self.kogen("intent", "build", "A").returncode, 2)

    def test_approve_rejects_malformed_hash(self):
        self.approve()
        for bad in ("ABCDEF12", "abc", "xyzxyz", "a" * 65):
            with self.subTest(bad=bad):
                self.assertEqual(self.kogen("intent", "approve", "add-numbers", bad).returncode, 2)

    def test_build_requires_approval(self):
        self.kogen("init")
        self.assertEqual(self.kogen("intent", "build", "add-numbers").returncode, 1)

    def run_logs(self):
        base = os.path.join(self.tree, ".kogen/local/runs")
        return [os.path.join(base, d) for d in sorted(os.listdir(base))]

    def test_correct_mode_commits_reference_and_logs(self):
        r = self.pipeline("correct")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(read(os.path.join(self.tree, "add.go")), read(os.path.join(TASK, "reference", "add.go")))
        self.assertEqual(sh("git", "-C", self.tree, "status", "--porcelain").stdout.strip(), "")
        self.assertFalse(os.path.exists(os.path.join(self.tree, ".kogen/local/approvals/add-numbers.json")))
        runs = self.run_logs()
        self.assertEqual(len(runs), 1)
        events = common.read_jsonl(os.path.join(runs[0], "log.jsonl"))
        self.assertTrue(EVENTS_NEEDED <= {e["event"] for e in events})
        self.assertTrue(all("at" in e for e in events))
        req = [e for e in events if e["event"] == "request"][0]
        self.assertEqual(set(req["usage"]), {"input", "cached", "output", "reasoning"})
        self.assertEqual(events[-1]["outcome"], "landed")
        self.assertTrue(os.path.exists(os.path.join(runs[0], "result.json")))

    def test_wrong_mode_copies_wrong_variant_and_logs(self):
        r = self.pipeline("wrong")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(read(os.path.join(self.tree, "add.go")),
                         read(os.path.join(TASK, "wrong", "negatives-clamped", "add.go")))
        events = common.read_jsonl(os.path.join(self.run_logs()[0], "log.jsonl"))
        self.assertEqual(events[-1]["outcome"], "landed")

    def test_fail_mode_prints_kogens_lines_and_does_not_commit(self):
        self.approve()
        before = self.head()
        r = self.kogen("intent", "build", "add-numbers", mode="fail")
        self.assertEqual(r.returncode, 1)
        first, second = r.stdout.splitlines()[:2]
        self.assertRegex(first, r"^failed add-numbers: build_blocked \(Build [0-9a-f]{8}\)$")
        self.assertRegex(second, r"^candidate/build_blocked: ")
        self.assertEqual(self.head(), before)

    def test_hang_mode_is_killed_by_deadline(self):
        self.approve()
        env = {**os.environ, "FAKE_KOGEN_MODE": "hang"}
        t0 = time.monotonic()
        code, timed_out = common.run([sys.executable, FAKE, "intent", "build", "add-numbers"],
                                     cwd=self.tree, env=env, deadline_s=1.5)
        self.assertTrue(timed_out)
        self.assertLess(time.monotonic() - t0, 20)


class FixtureTask(unittest.TestCase):
    """task-mini follows the Lab task layout (task.json, evaluate.json required keys)."""

    def test_required_keys(self):
        try:
            import tomllib
        except ImportError:
            self.skipTest("tomllib needs Python 3.11")
        with open(os.path.join(TASK, "task.toml"), "rb") as f:
            task = tomllib.load(f)
        for key in ("name", "split", "language", "requires", "test_globs", "regression_tests"):
            self.assertIn(key, task)
        self.assertIn(task["split"], ("development", "confirmation"))
        self.assertTrue(all({"name", "run"} <= set(c) for c in task["check"]))
        self.assertIn("run", task["acceptance"])
        with open(os.path.join(TASK, "evaluator", "evaluate.toml"), "rb") as f:
            ev = tomllib.load(f)
        self.assertIn("overlay", ev)
        self.assertTrue(os.path.isdir(os.path.join(TASK, "evaluator", ev["overlay"])))
        for cmd in ev["command"]:
            self.assertTrue({"name", "run", "adapter", "results", "timeout_seconds"} <= set(cmd))
            self.assertIn(cmd["adapter"], ("go_test_json", "exunit_lab", "lab_jsonl"))
        for f in ("intent.md", "acceptance.feature"):
            self.assertTrue(os.path.exists(os.path.join(TASK, "supplied", "gherkin", f)))

    @unittest.skipUnless(shutil.which("go"), "go not installed")
    def test_reference_passes_and_wrong_fails_hidden_tests(self):
        for variant, ok in (("reference", True), ("wrong/negatives-clamped", False)):
            with tempfile.TemporaryDirectory() as d:
                shutil.copytree(os.path.join(TASK, "start"), d, dirs_exist_ok=True)
                shutil.copytree(os.path.join(TASK, variant), d, dirs_exist_ok=True)
                shutil.copytree(os.path.join(TASK, "evaluator", "files"), d, dirs_exist_ok=True)
                env = {**os.environ, "GOFLAGS": "-mod=mod", "GOTOOLCHAIN": "local"}
                r = sh("go", "test", "./...", cwd=d, env=env)
                self.assertEqual(r.returncode == 0, ok, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
