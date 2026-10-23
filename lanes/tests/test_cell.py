import glob
import io
import json
import os
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import time
import unittest

from lanes import cell, common

HERE = os.path.dirname(os.path.abspath(__file__))
FAKE = os.path.join(HERE, "fake-kogen")
TASK = os.path.join(HERE, "fixtures", "task-mini")
ENTRY = os.path.join(HERE, "..", "bin", "lanes-cell")
SHA = "0123456789abcdef0123456789abcdef01234567"


def read(path, mode="r"):
    with open(path, mode) as f:
        return f.read()


def alive(pid):
    for _ in range(100):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        time.sleep(0.02)
    return True


# Workspace setup counts against the cell deadline, so under load a short deadline can pass before the fake
# Kogen has written its pid file. Use a deadline that setup cannot plausibly use up, and wait (bounded) for the file.
HANG_DEADLINE_S = 10
KILL_MARGIN_S = 15  # the cell must be over this long after its deadline


def wait_pids(path, count, limit=30):
    end = time.monotonic() + limit
    while time.monotonic() < end:
        try:
            pids = read(path).split()
        except FileNotFoundError:
            pids = []
        if len(pids) >= count:
            return [int(p) for p in pids]
        time.sleep(0.05)
    raise AssertionError(f"{path} not written with {count} pids within {limit}s")


class CellTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = self._tmp.name
        self.tasks = os.path.join(self.tmp, "tasks")
        shutil.copytree(TASK, os.path.join(self.tasks, "task-mini"))
        self.home = os.path.join(self.tmp, "home")
        # the fixture's supplied Intent says `Slug: add-numbers`; a cell's slug is the task's name
        self.intent_md = os.path.join(self.tasks, "task-mini", "supplied", "gherkin", "intent.md")
        with open(self.intent_md) as f:
            text = f.read()
        with open(self.intent_md, "w") as f:
            f.write(text.replace("add-numbers", "task-mini"))

    def wrapper(self, body, name="kogen"):
        """A `kogen` that runs `body` (shell) first, then the fake."""
        path = os.path.join(self.tmp, name)
        with open(path, "w") as f:
            f.write(f'#!/bin/sh\n{body}\nexec {sys.executable} {FAKE} "$@"\n')
        os.chmod(path, 0o755)
        return path

    def make_run(self, phase, deadline_s=60, models=None, lanes=("base",)):
        run = os.path.join(self.tmp, "run-" + phase)
        exp = {"id": "exp-mini", "phase": phase, "intent_form": "gherkin", "reps": 1, "deadline_s": deadline_s, "cost_cap_usd": 100,
               "kogen": {"repo": "https://example.invalid/kogen.git"}, "tasks": ["task-mini"], "hosts": ["local"],
               "decision_rule": {"kind": "paired-pass-rate"},
               "lanes": [{"name": n, "sha": SHA, "patch": None, "settings": {"models": models or {}}} for n in lanes]}
        common.write_json(os.path.join(run, "experiment.json"), exp)
        return run

    def cell(self, run, lane="base", *extra, mode="correct", artifact=FAKE, **env):
        e = {**os.environ, "FAKE_KOGEN_MODE": mode, "FAKE_KOGEN_TASK": TASK, "KOGEN_LANES_HOME": self.home, **env}
        cmd = [sys.executable, ENTRY, run, f"task-mini/r1/{lane}", "--tasks", self.tasks, *extra]
        if artifact:
            cmd += ["--artifact", artifact]
        return subprocess.run(cmd, capture_output=True, text=True, env=e)

    def done(self, run, lane="base"):
        path = common.cell_dir(run, f"task-mini/r1/{lane}")
        return path, common.read_json(os.path.join(path, "result.json"))

    def tar_names(self, path):
        with tarfile.open(os.path.join(path, "final-tree.tar")) as t:
            return t.getnames()

    def test_shape_phase(self):
        run = self.make_run("shape")
        r = self.cell(run)
        self.assertEqual(r.returncode, 0, r.stderr)
        path, res = self.done(run)
        self.assertEqual((res["phase"], res["outcome"], res["exit_code"]), ("shape", "ok", 0))
        self.assertEqual(res["cell"], "task-mini/r1/base")
        self.assertEqual(res["kogen_version"], "kogen fake0000 (2026-01-01)")
        self.assertEqual((res["host"], res["pass_trees"], res["intent_hash"]), ("local", [], None))
        self.assertTrue(os.path.isfile(os.path.join(path, "intent", "intent.md")))
        self.assertTrue(os.path.isfile(os.path.join(path, "shaping-events.ndjson")))
        self.assertFalse(os.path.exists(os.path.join(path, "run-log")))
        self.assertEqual([s["stage"] for s in res["stages"]], ["shape"])
        self.assertEqual(res["stages"][0]["input_tokens"], 2000)
        self.assertEqual(res["totals"]["requests"], 1)
        self.assertIn("== kogen intent shape", read(os.path.join(path, "stdout.txt")))

    def test_build_correct_and_wrong(self):
        run = self.make_run("build")
        self.assertEqual(self.cell(run).returncode, 0)
        path, res = self.done(run)
        self.assertEqual((res["outcome"], res["exit_code"]), ("landed", 0))
        self.assertRegex(res["intent_hash"], r"^[0-9a-f]{64}$")
        self.assertEqual(len(res["pass_trees"]), 1)
        self.assertEqual(res["pass_trees"][0], res["final_tree"])
        self.assertEqual([s["stage"] for s in res["stages"]], ["approve", "build", "review"])
        self.assertTrue(os.path.isfile(os.path.join(path, "run-log", "log.jsonl")))
        self.assertFalse(os.path.exists(os.path.join(path, "intent")))
        with tarfile.open(os.path.join(path, "final-tree.tar")) as t:
            good = t.extractfile("add.go").read()
        self.assertEqual(good, read(os.path.join(TASK, "reference", "add.go"), "rb"))
        self.assertEqual(self.cell(run, "base", "--force", mode="wrong").returncode, 0)
        path, res = self.done(run)
        self.assertEqual(res["outcome"], "landed")  # Kogen cannot tell; the grader does
        with tarfile.open(os.path.join(path, "final-tree.tar")) as t:
            self.assertNotEqual(t.extractfile("add.go").read(), good)

    def test_build_fail(self):
        run = self.make_run("build")
        self.assertEqual(self.cell(run, mode="fail").returncode, 0)
        path, res = self.done(run)
        self.assertEqual((res["outcome"], res["exit_code"]), ("build_blocked", 1))
        self.assertEqual(res["pass_trees"], [])
        self.assertEqual(res["stages"][1]["outcome"], "build_blocked")

    def test_e2e(self):
        run = self.make_run("e2e")
        self.assertEqual(self.cell(run).returncode, 0)
        path, res = self.done(run)
        self.assertEqual(res["outcome"], "landed")
        self.assertEqual([s["stage"] for s in res["stages"]][:3], ["shape", "approve", "build"])
        self.assertTrue(os.path.isfile(os.path.join(path, "intent", "acceptance.feature")))
        self.assertEqual(res["totals"]["requests"], 3)

    def test_e2e_shape_failure_stops(self):
        run = self.make_run("e2e")
        os.remove(os.path.join(self.tasks, "task-mini", "request.md"))
        self.assertEqual(self.cell(run).returncode, 2)  # refused before anything runs
        self.assertFalse(os.path.exists(common.cell_dir(run, "task-mini/r1/base")))
        with open(os.path.join(self.tasks, "task-mini", "request.md"), "w"):
            pass  # Kogen refuses an empty request
        self.assertEqual(self.cell(run).returncode, 0)
        path, res = self.done(run)
        self.assertEqual((res["outcome"], res["exit_code"]), ("usage", 2))
        self.assertEqual([s["stage"] for s in res["stages"]], ["shape"])

    def test_hang_times_out_without_orphans(self):
        run = self.make_run("build", deadline_s=HANG_DEADLINE_S)
        pids = os.path.join(self.tmp, "pids")
        wrapper = os.path.join(self.tmp, "kogen")
        with open(wrapper, "w") as f:
            f.write(f'#!/bin/sh\nif [ "$2" = build ]; then sleep 300 &\necho $$ $! > {pids}; fi\n'
                    f'exec {sys.executable} {FAKE} "$@"\n')
        os.chmod(wrapper, 0o755)
        t0 = time.monotonic()
        self.assertEqual(self.cell(run, mode="hang", artifact=wrapper).returncode, 0)
        self.assertLess(time.monotonic() - t0, HANG_DEADLINE_S + KILL_MARGIN_S)
        path, res = self.done(run)
        self.assertEqual(res["outcome"], "timeout")
        self.assertEqual(res["stages"][1]["outcome"], "timeout")
        for pid in wait_pids(pids, 2):
            self.assertFalse(alive(pid), f"process {pid} outlived the cell")

    def test_settings_and_commands_in_project_yaml(self):
        run = self.make_run("shape", models={"build": "openai/gpt-x high", "review": "acme/model-y low"})
        r = self.cell(run, "base", "--keep")
        self.assertEqual(r.returncode, 0, r.stderr)
        ws = r.stderr.split("kept workspace: ")[1].strip()
        self.addCleanup(shutil.rmtree, os.path.dirname(ws), True)
        yaml = subprocess.run(["git", "-C", ws, "show", "HEAD:.kogen/project.yaml"], capture_output=True,
                              text=True).stdout
        self.assertIn("version: 1\n", yaml)
        self.assertIn("  build: {model: gpt-x, effort: high}\n", yaml)
        self.assertIn("  review: {model: model-y, effort: low}\n", yaml)
        self.assertIn("    - name: test\n      run: 'go test ./...'\n", yaml)
        self.assertIn("    - 'gofmt -w .'\n", yaml)
        self.assertIn("    steps_dir: 'features/steps'\n", yaml)
        self.assertEqual(read(os.path.join(ws, ".gitignore")), ".kogen/local/\n")
        self.assertEqual(subprocess.run(["git", "-C", ws, "status", "--porcelain", "--", ".kogen/project.yaml"],
                                        capture_output=True, text=True).stdout, "")
        run = self.make_run("build", models={"build": "openai/gpt-x high"})
        self.assertEqual(self.cell(run).returncode, 0)
        path, _ = self.done(run)
        log = common.read_jsonl(os.path.join(path, "run-log", "log.jsonl"))
        self.assertEqual({e["model"] for e in log if e.get("event") == "request" and e["role"] == "build"},
                         {"gpt-x"})

    def test_project_yaml_bare_model_ids(self):
        one = cell.project_yaml({}, {"build": "openai/gpt-6-luna low"})
        self.assertIn("models:\n  build: {model: gpt-6-luna, effort: low}\n", one)
        self.assertNotIn("openai", one)
        self.assertNotIn("review:", one)
        two = cell.project_yaml({}, {"build": "openai/gpt-6-luna low", "review": "openai/gpt-6 high"})
        self.assertIn("  build: {model: gpt-6-luna, effort: low}\n  review: {model: gpt-6, effort: high}\n", two)
        self.assertNotIn("models:", cell.project_yaml({}, {}))

    def test_same_start_tree_for_every_cell(self):
        run = self.make_run("shape", lanes=("a", "b"))
        trees = set()
        for lane in ("a", "b"):
            self.assertEqual(self.cell(run, lane).returncode, 0)
            trees.add(self.done(run, lane)[1]["final_tree"])
        self.assertEqual(len(trees), 1)

    def test_hidden_tests_never_in_workspace(self):
        run = self.make_run("e2e")
        r = self.cell(run, "base", "--keep")
        self.assertEqual(r.returncode, 0, r.stderr)
        ws = r.stderr.split("kept workspace: ")[1].strip()
        self.addCleanup(shutil.rmtree, os.path.dirname(ws), True)
        for dirpath, _, files in os.walk(ws):
            self.assertNotIn("add_hidden_test.go", files)
            self.assertNotIn("evaluate.toml", files)
        path, _ = self.done(run)
        self.assertFalse([n for n in self.tar_names(path) if "hidden" in n or "evaluator" in n])

    def answers(self):
        with open(os.path.join(self.tasks, "task-mini", "answers.txt"), "w") as f:
            f.write("1: a\n")

    def test_questions_answered_from_answers_file(self):
        self.answers()
        run = self.make_run("e2e")
        r = self.cell(run, FAKE_KOGEN_QUESTIONS="once")
        self.assertEqual(r.returncode, 0, r.stderr)
        path, res = self.done(run)
        self.assertEqual((res["outcome"], res["exit_code"]), ("landed", 0))
        self.assertEqual([s["stage"] for s in res["stages"]][:3], ["shape", "approve", "build"])
        self.assertEqual(res["stages"][0]["outcome"], "ok")
        self.assertIn("== kogen intent shape task-mini -", read(os.path.join(path, "stdout.txt")))

    def test_questions_without_answers_is_pending(self):
        run = self.make_run("e2e")
        self.assertEqual(self.cell(run, FAKE_KOGEN_QUESTIONS="once").returncode, 0)
        path, res = self.done(run)
        self.assertEqual(res["outcome"], "questions_pending")
        self.assertEqual([s["stage"] for s in res["stages"]], ["shape"])
        self.assertEqual(res["stages"][0]["outcome"], "questions_pending")
        self.assertNotIn("shape task-mini -", read(os.path.join(path, "stdout.txt")))

    def test_one_answer_round_then_pending(self):  # L9: capped at one round
        self.answers()
        run = self.make_run("shape")
        self.assertEqual(self.cell(run, FAKE_KOGEN_QUESTIONS="always").returncode, 0)
        path, res = self.done(run)
        self.assertEqual(res["outcome"], "questions_pending")
        self.assertEqual(read(os.path.join(path, "stdout.txt")).count("== kogen intent shape"), 2)

    def test_shape_exit_5_without_questions_is_not_ok(self):  # L9: exit 5 is ok only for approve with a card
        wrapper = self.wrapper('if [ "$2" = shape ]; then echo "something else"; exit 5; fi')
        run = self.make_run("shape")
        self.assertEqual(self.cell(run, artifact=wrapper).returncode, 0)
        res = self.done(run)[1]
        self.assertEqual((res["outcome"], res["stages"][0]["outcome"]), ("exit_5", "exit_5"))

    def test_pass_trees_are_stored_as_tars(self):  # L9
        run = self.make_run("build")
        self.assertEqual(self.cell(run).returncode, 0)
        path, res = self.done(run)
        self.assertTrue(res["pass_trees"])
        for tree in res["pass_trees"]:
            tar = os.path.join(path, "pass-trees", tree + ".tar")
            with tarfile.open(tar) as t:
                self.assertTrue(any(n.endswith(".go") for n in t.getnames()))

    def test_approve_exit_5_without_card_is_not_ok(self):
        wrapper = self.wrapper('if [ "$2" = approve ]; then echo "intent/questions_pending: 1 unanswered"; exit 5; fi')
        run = self.make_run("build")
        self.assertEqual(self.cell(run, artifact=wrapper).returncode, 0)
        path, res = self.done(run)
        self.assertEqual(res["outcome"], "intent/questions_pending")
        self.assertEqual(res["exit_code"], 5)
        self.assertIsNone(res["intent_hash"])
        self.assertEqual([(s["stage"], s["outcome"]) for s in res["stages"]],
                         [("approve", "intent/questions_pending")])

    def test_supplied_intent_laid_out_like_the_shaper(self):
        steps = os.path.join(self.tasks, "task-mini", "supplied", "gherkin", "features", "steps", "add_steps.js")
        with open(steps, "w") as f:
            f.write("// supplied step\n")
        run = self.make_run("build")
        r = self.cell(run, "base", "--keep")
        self.assertEqual(r.returncode, 0, r.stderr)
        ws = r.stderr.split("kept workspace: ")[1].strip()
        self.addCleanup(shutil.rmtree, os.path.dirname(ws), True)
        self.assertEqual(read(os.path.join(ws, "features", "steps", "add_steps.js")), "// supplied step\n")
        intent = os.path.join(ws, ".kogen", "intents", "task-mini")
        self.assertEqual(sorted(os.listdir(intent)), ["acceptance.feature", "intent.md"])
        self.assertEqual(self.done(run)[1]["outcome"], "landed")

    def test_supplied_slug_must_match_task_name(self):
        with open(self.intent_md, "w") as f:
            f.write("# T\n\nSlug: add-numbers\nModel: none\n")
        run = self.make_run("build")
        r = self.cell(run)
        self.assertEqual(r.returncode, 2)
        self.assertIn("Slug", r.stderr)
        self.assertFalse(os.path.exists(common.cell_dir(run, "task-mini/r1/base")))

    def test_shaped_intent_saved_with_its_step_files(self):
        wrapper = self.wrapper(
            'if [ "$2" = shape ]; then "$0.real" "$@"; c=$?; i=.kogen/intents/$3/intent.md\n'
            'printf "Acceptance:\\n- .kogen/intents/$3/acceptance.feature\\n- features/steps/new_steps.js\\n" >> $i\n'
            'mkdir -p features/steps; echo step > features/steps/new_steps.js; exit $c; fi')
        os.symlink(FAKE, wrapper + ".real")
        run = self.make_run("shape")
        self.assertEqual(self.cell(run, artifact=wrapper).returncode, 0)
        path, res = self.done(run)
        self.assertEqual(res["outcome"], "ok")
        self.assertEqual(read(os.path.join(path, "intent", "features", "steps", "new_steps.js")), "step\n")
        self.assertTrue(os.path.isfile(os.path.join(path, "intent", "intent.md")))
        self.assertTrue(os.path.isfile(os.path.join(path, "intent", "acceptance.feature")))

    def test_kogen_does_not_see_the_private_task_folder(self):
        wrapper = self.wrapper('env > "$0.env"; echo "$@" > "$0.args"')
        run = self.make_run("shape")
        self.assertEqual(self.cell(run, artifact=wrapper, KOGEN_LANES_TASKS=self.tasks).returncode, 0)
        self.assertNotIn("KOGEN_LANES", read(wrapper + ".env"))
        self.assertNotIn(self.tasks, read(wrapper + ".env"))
        self.assertNotIn(self.tasks, read(wrapper + ".args"))

    def test_hung_version_times_out_without_orphans(self):
        pids = os.path.join(self.tmp, "pids")
        wrapper = self.wrapper(f'if [ "$1" = version ]; then sleep 300 & echo $$ $! > {pids}; wait; fi')
        run = self.make_run("shape", deadline_s=HANG_DEADLINE_S)
        t0 = time.monotonic()
        self.assertEqual(self.cell(run, artifact=wrapper).returncode, 0)
        self.assertLess(time.monotonic() - t0, HANG_DEADLINE_S + KILL_MARGIN_S)
        path, res = self.done(run)
        self.assertEqual(res["outcome"], "timeout")
        self.assertIsNone(res["kogen_version"])
        for pid in wait_pids(pids, 2):
            self.assertFalse(alive(pid), f"process {pid} outlived the cell")

    def test_e2e_deadline_is_shared_across_commands(self):
        run = self.make_run("e2e", deadline_s=3)
        self.assertEqual(self.cell(run, mode="hang").returncode, 0)
        path, res = self.done(run)
        self.assertEqual(res["outcome"], "timeout")
        self.assertEqual([(s["stage"], s["outcome"]) for s in res["stages"][:3]],
                         [("shape", "ok"), ("approve", "ok"), ("build", "timeout")])
        self.assertLess(res["wall_s"], 15)

    def test_shape_fail_and_hang(self):
        run = self.make_run("shape")
        wrapper = self.wrapper('if [ "$2" = shape ]; then echo "intent/refused: no"; exit 1; fi')
        self.assertEqual(self.cell(run, artifact=wrapper).returncode, 0)
        res = self.done(run)[1]
        self.assertEqual((res["outcome"], res["exit_code"]), ("refused", 1))
        pid = os.path.join(self.tmp, "shape-pid")
        wrapper = self.wrapper(f'if [ "$2" = shape ]; then echo $$ > {pid}; exec sleep 300; fi', "kogen2")
        run = self.make_run("shape", deadline_s=HANG_DEADLINE_S)
        self.assertEqual(self.cell(run, "base", "--force", artifact=wrapper).returncode, 0)
        self.assertEqual(self.done(run)[1]["outcome"], "timeout")
        self.assertFalse(alive(wait_pids(pid, 1)[0]))

    def test_failed_build_without_outcome_event_has_one_outcome(self):
        wrapper = self.wrapper('if [ "$2" = build ]; then exit 1; fi')
        run = self.make_run("build")
        self.assertEqual(self.cell(run, artifact=wrapper).returncode, 0)
        res = self.done(run)[1]
        self.assertEqual(res["outcome"], "no_outcome")
        self.assertEqual(res["stages"][1]["outcome"], "no_outcome")

    def interrupt(self, sig):
        run = self.make_run("build", deadline_s=120)
        pids = os.path.join(self.tmp, "pids")
        wrapper = self.wrapper(f'if [ "$2" = build ]; then sleep 300 & echo $$ $! > {pids}; fi')
        tmpdir = tempfile.mkdtemp(dir=self.tmp)
        env = {**os.environ, "FAKE_KOGEN_MODE": "hang", "FAKE_KOGEN_TASK": TASK, "KOGEN_LANES_HOME": self.home,
               "TMPDIR": tmpdir}
        proc = subprocess.Popen([sys.executable, ENTRY, run, "task-mini/r1/base", "--tasks", self.tasks,
                                 "--artifact", wrapper], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_DFL))
        for _ in range(500):
            if os.path.exists(pids) and read(pids).strip():
                break
            time.sleep(0.02)
        time.sleep(0.3)
        proc.send_signal(sig)
        _, err = proc.communicate(timeout=30)
        for pid in read(pids).split():
            self.assertFalse(alive(int(pid)), f"process {pid} outlived the cell")
        self.assertEqual(os.listdir(tmpdir), [])
        self.assertFalse(os.path.exists(os.path.join(common.cell_dir(run, "task-mini/r1/base"), "result.json")))
        return proc.returncode, err

    def test_sigterm_and_sighup_clean_up(self):
        self.assertEqual(self.interrupt(signal.SIGTERM)[0], 143)
        self.assertEqual(self.interrupt(signal.SIGHUP)[0], 129)

    def test_sigint_is_one_line(self):
        code, err = self.interrupt(signal.SIGINT)
        self.assertEqual(code, 130)
        self.assertIn("cell: interrupted", err)
        self.assertNotIn("Traceback", err)

    def test_rerun_refused_unless_force(self):
        run = self.make_run("shape")
        self.assertEqual(self.cell(run).returncode, 0)
        path, first = self.done(run)
        r = self.cell(run)
        self.assertEqual(r.returncode, 2)
        self.assertIn("already done", r.stderr)
        self.assertEqual(self.done(run)[1], first)
        self.assertEqual(self.cell(run, "base", "--force").returncode, 0)
        self.assertNotEqual(self.done(run)[1]["started"], first["started"])

    def test_partial_cell_is_rerun(self):
        run = self.make_run("shape")
        path = common.cell_dir(run, "task-mini/r1/base")
        os.makedirs(path)
        with open(os.path.join(path, "stdout.txt"), "w") as f:
            f.write("stale\n")
        self.assertEqual(self.cell(run).returncode, 0)
        self.assertNotIn("stale", read(os.path.join(path, "stdout.txt")))

    def test_artifact_from_lock_and_archive_unpacked_once(self):
        run = self.make_run("shape", lanes=("a", "b"))
        sha = "ab" * 32
        folder = os.path.join(self.home, "artifacts", sha)
        os.makedirs(folder)
        buf = os.path.join(folder, "kogen-fake-test.tar.gz")
        with tarfile.open(buf, "w:gz") as t:
            t.add(FAKE, "kogen-fake-test/bin/kogen")
        common.write_json(os.path.join(run, "lanes.lock.json"),
                          [{"name": n, "sha": SHA, "patch_sha256": None, "artifact_sha256": sha,
                            "kogen_version": "x"} for n in ("a", "b")])
        for lane in ("a", "b"):
            r = self.cell(run, lane, artifact=None)
            self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(len(os.listdir(os.path.join(self.home, "unpacked"))), 1)
        self.assertEqual(self.done(run, "b")[1]["kogen_version"], "kogen fake0000 (2026-01-01)")

    def release(self, with_install=True):
        """A release archive with install.sh's layout (`kogen-x/{install.sh,bin/kogen}`) in a lock-less artifact folder."""
        folder = os.path.join(self.tmp, "artifact")
        os.makedirs(folder, exist_ok=True)
        with tarfile.open(os.path.join(folder, "kogen-fake-test.tar.gz"), "w:gz") as t:
            t.add(FAKE, "kogen-fake-test/bin/kogen")
            if with_install:
                marker = os.path.join(self.tmp, "install.sh")
                with open(marker, "w") as f:
                    f.write("#!/bin/sh\n")
                t.add(marker, "kogen-fake-test/install.sh")
        return folder

    def fake_node(self, version, name="node-bin"):
        """A `node` on its own PATH folder that answers the execPath-and-version probe; returns (folder, execPath)."""
        folder = os.path.join(self.tmp, name)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, "node")
        with open(path, "w") as f:
            f.write(f'#!/bin/sh\nprintf "%s\\n%s\\n" "{path}" "{version}"\n')
        os.chmod(path, 0o755)
        return folder, path

    def node_path_file(self):
        (root,) = glob.glob(os.path.join(self.home, "unpacked", "*", "kogen-fake-test"))
        return os.path.join(root, "node-path")

    def test_unpacked_release_gets_node_path(self):
        run = self.make_run("shape")
        folder, node = self.fake_node("24.1.0")
        r = self.cell(run, artifact=self.release(), PATH=folder + os.pathsep + os.environ["PATH"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(read(self.node_path_file()), node + "\n")
        self.assertEqual(self.done(run)[1]["node"], {"path": node, "version": "24.1.0"})

    def test_stale_node_path_is_rewritten(self):
        run = self.make_run("shape")
        folder, node = self.fake_node("22.0.0")
        env = {"PATH": folder + os.pathsep + os.environ["PATH"]}
        artifact = self.release()
        self.assertEqual(self.cell(run, artifact=artifact, **env).returncode, 0)
        with open(self.node_path_file(), "w") as f:
            f.write("/gone/bin/node\n")
        self.assertEqual(self.cell(run, "base", "--force", artifact=artifact, **env).returncode, 0)
        self.assertEqual(read(self.node_path_file()), node + "\n")

    def test_old_or_missing_node_refused(self):
        run = self.make_run("shape")
        folder, _ = self.fake_node("20.11.0")
        for path in (folder + os.pathsep + "/usr/bin:/bin", "/usr/bin:/bin"):
            r = self.cell(run, artifact=self.release(), PATH=path)
            self.assertEqual(r.returncode, 2)
            self.assertIn("Node 22 or newer", r.stderr)
            self.assertFalse(os.path.exists(os.path.join(common.cell_dir(run, "task-mini/r1/base"), "result.json")))

    def test_plain_artifact_needs_no_node(self):
        run = self.make_run("shape")
        r = self.cell(run, artifact=self.release(with_install=False), PATH="/usr/bin:/bin")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIsNone(self.done(run)[1]["node"])

    def test_missing_artifact_refused(self):
        run = self.make_run("shape")
        r = self.cell(run, artifact=None)
        self.assertEqual(r.returncode, 2)
        self.assertIn("lanes.lock.json", r.stderr)


if __name__ == "__main__":
    unittest.main()
