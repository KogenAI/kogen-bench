import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from lanes import common

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.join(HERE, "fixtures", "task-mini")
ENTRY = os.path.join(HERE, "..", "bin", "lanes-leakcheck")
PREFLIGHT = os.path.join(HERE, "..", "bin", "lanes-preflight")
FAKE = os.path.join(HERE, "fake-kogen")
SHA = "0123456789abcdef0123456789abcdef01234567"
CLEAN = """--- a/lib/review.ex
+++ b/lib/review.ex
@@ -1,2 +1,3 @@
 defmodule Review do
+  # Run the checks again after every repair before declaring success.
 end
"""
FAILURE = ("expected the sum of the two operands to equal the stored total after rounding "
           "but the accumulator kept a stale intermediate value from the previous call")


class LeakTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = self._tmp.name
        self.tasks = os.path.join(self.tmp, "tasks")
        shutil.copytree(TASK, os.path.join(self.tasks, "task-mini"))
        self.hidden = os.path.join(self.tasks, "task-mini", "evaluator", "files", "add_hidden_test.go")
        self.exp_dir = os.path.join(self.tmp, "exp")
        os.makedirs(os.path.join(self.exp_dir, "patches"))
        self.write_patch(CLEAN)

    def write_patch(self, text):
        with open(os.path.join(self.exp_dir, "patches", "p.patch"), "w") as f:
            f.write(text)

    def experiment(self, **extra):
        exp = {"id": "climb-r1", "kind": "climb", "phase": "build", "intent_form": "gherkin",
               "kogen": {"repo": "x"}, "reps": 1, "deadline_s": 60, "hosts": ["local"],
               "tasks": ["task-mini", "task-two"], "split": {"train": ["task-mini"], "test": ["task-two"]},
               "min_effect": 0.1, "noise_ref": "noise.json", "round": 1, "parent": None,
               "decision_rule": {"kind": "keep_revert"},
               "lanes": [{"name": "baseline", "sha": SHA, "patch": None, "settings": {}},
                         {"name": "candidate", "sha": SHA, "patch": "patches/p.patch", "settings": {}}]}
        exp.update(extra)
        path = os.path.join(self.exp_dir, "experiment.json")
        common.write_json(path, exp)
        return path

    def two_tasks(self):
        if os.path.isdir(os.path.join(self.tasks, "task-two")):
            return
        shutil.copytree(TASK, os.path.join(self.tasks, "task-two"))
        with open(os.path.join(self.tasks, "task-two", "task.toml")) as f:
            text = f.read()
        with open(os.path.join(self.tasks, "task-two", "task.toml"), "w") as f:
            f.write(text.replace("task-mini", "task-two"))

    def leak(self, *args, tasks=None, env=None):
        self.two_tasks()
        return subprocess.run([sys.executable, ENTRY, self.experiment(), "--tasks", tasks or self.tasks, *args],
                              capture_output=True, text=True, timeout=60, env=env)

    def put(self, rel, text):
        path = os.path.join(self.tasks, "task-mini", rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def kogen_dir(self, text):
        d = os.path.join(self.tmp, "kogen-src")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "build.ex"), "w") as f:
            f.write(text)
        return d

    def diff_adding(self, line, context=" defmodule Review do"):
        return ("--- a/lib/review.ex\n+++ b/lib/review.ex\n@@ -1,2 +1,3 @@\n" + context + "\n+" + line + "\n end\n")

    def test_clean_patch_passes(self):
        p = self.leak()
        self.assertEqual((p.returncode, p.stdout), (0, ""), p.stderr)

    def test_patch_naming_a_task(self):
        self.write_patch(CLEAN + "+  # handle the task-two case first\n")
        p = self.leak()
        self.assertEqual(p.returncode, 1)
        self.assertIn("candidate patch: task name 'task-two' (from task id task-two)", p.stdout)

    def test_patch_quoting_a_hidden_assertion(self):
        with open(self.hidden) as f:
            lines = [l.strip() for l in f if len(l.strip()) >= 24]
        self.assertTrue(lines, "fixture hidden test has no long line")
        self.write_patch(CLEAN + f"+  // {lines[0]}\n")
        p = self.leak()
        self.assertEqual(p.returncode, 1)
        self.assertIn("hidden-test line", p.stdout)
        self.assertIn("hidden tests: files/add_hidden_test.go", p.stdout)

    def test_patch_copying_failure_output(self):
        run = os.path.join(self.tmp, "runs", "old")
        cell = os.path.join(run, "cells", "task-mini", "r1", "baseline")
        os.makedirs(cell)
        with open(os.path.join(cell, "stdout.txt"), "w") as f:
            f.write("--- FAIL: TestAdd\n    " + FAILURE + "\nFAIL\n")
        self.write_patch(CLEAN + f"+  # Known failure: {FAILURE}\n")
        self.assertEqual(self.leak().returncode, 0, "without --runs nothing is compared")
        p = self.leak("--runs", run)
        self.assertEqual(p.returncode, 1)
        self.assertIn("run output", p.stdout)
        self.assertIn("run old: task-mini/r1/baseline/stdout.txt", p.stdout)

    def test_clean_patch_passes_with_runs(self):
        run = os.path.join(self.tmp, "runs", "old")
        os.makedirs(os.path.join(run, "cells", "t", "r1", "b"))
        with open(os.path.join(run, "cells", "t", "r1", "b", "stdout.txt"), "w") as f:
            f.write(FAILURE)
        self.assertEqual(self.leak("--runs", run).returncode, 0)

    def test_settings_are_checked(self):
        self.two_tasks()
        path = self.experiment(lanes=[
            {"name": "baseline", "sha": SHA, "patch": None, "settings": {"models": {"build": "openai/m high"}}},
            {"name": "candidate", "sha": SHA, "patch": None, "settings": {"models": {"build": "openai/task-two high"}}}])
        p = subprocess.run([sys.executable, ENTRY, path, "--tasks", self.tasks], capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertIn("candidate settings: task name", p.stdout)

    def test_hidden_tests_are_not_copied(self):
        self.two_tasks()
        before = common.sha256_tree(self.tasks)
        self.write_patch(CLEAN + "+  # task-two\n")
        self.leak()
        self.assertEqual(common.sha256_tree(self.tasks), before)
        listing = [os.path.join(d, n) for d, _, fs in os.walk(self.exp_dir) for n in fs]
        self.assertEqual(sorted(os.path.basename(x) for x in listing), ["experiment.json", "p.patch"])

    def test_bad_inputs_exit_2(self):
        p = subprocess.run([sys.executable, ENTRY, os.path.join(self.tmp, "none.json"), "--tasks", self.tasks],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)

    def test_preflight_refuses_a_leaking_climb(self):
        self.two_tasks()
        self.write_patch(CLEAN + "+  # task-two\n")
        run_dir = os.path.join(self.tmp, "run")
        self.experiment()
        shutil.copytree(self.exp_dir, run_dir)
        env = {**os.environ, "KOGEN_LANES_HOME": os.path.join(self.tmp, "home"), "FAKE_KOGEN_TASK": TASK}
        p = subprocess.run([sys.executable, PREFLIGHT, run_dir, "--tasks", self.tasks, "--artifact", FAKE],
                           env=env, capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        self.assertIn("LEAK: candidate patch: task name 'task-two'", p.stdout)

    # --- Kogen's own words are not task content ------------------------------------------------

    def elixir_task(self):
        self.put("reference/lib/core.ex", "defmodule Core do\n  def run(n), do: n |> Integer.to_string() |> "
                 "Enum.with_index()\n  def compute_rounded_total(x), do: x\n  @cap 1_048_576\nend\n")

    def test_language_words_from_kogen_are_not_leaks(self):
        self.elixir_task()
        self.write_patch(self.diff_adding("  defp pad(n), do: n |> Integer.to_string() |> Enum.with_index()"))
        self.assertEqual(self.leak().returncode, 1, "without a Kogen source the words are flagged")
        kogen = self.kogen_dir("defp x(n), do: n |> Integer.to_string() |> Enum.with_index()\n")
        p = self.leak("--kogen", kogen)
        self.assertEqual((p.returncode, p.stdout), (0, ""), p.stderr)

    def test_task_only_identifier_still_leaks_with_kogen(self):
        self.elixir_task()
        self.write_patch(self.diff_adding("  defp pad(n), do: Core.compute_rounded_total(n)"))
        p = self.leak("--kogen", self.kogen_dir("defp x(n), do: n |> Integer.to_string()\n"))
        self.assertEqual(p.returncode, 1)
        self.assertIn("identifier 'compute_rounded_total' (from task task-mini reference: lib/core.ex)", p.stdout)

    def test_words_in_the_patchs_own_context_are_not_leaks(self):
        self.elixir_task()
        self.write_patch(self.diff_adding("  # n |> Integer.to_string() stays", context="   def run(n), do: Integer.to_string(n)"))
        self.assertEqual(self.leak().returncode, 0)

    PHRASE = "verify every boundary value before you report success"

    def base_prompt_task(self):
        """The task holds PHRASE in a literal; the base prompt (`--kogen`) holds it inside a longer one."""
        self.put("reference/lib/phrase.ex", 'def note, do: "%s"\n' % self.PHRASE)
        return self.kogen_dir('@prompt "Be careful: %s, then stop."\n@other "second line of the prompt"\n' % self.PHRASE)

    def test_base_phrase_kept_in_a_rewritten_line_is_not_a_hit(self):
        kogen = self.base_prompt_task()
        self.write_patch(
            '--- a/prompt.ex\n+++ b/prompt.ex\n@@ -1,2 +1,2 @@\n'
            '-@prompt "Be careful: %s, then stop."\n'
            '+@prompt "Always, %s, and then rest."\n @other "second line of the prompt"\n' % (self.PHRASE, self.PHRASE))
        p = self.leak("--kogen", kogen)
        self.assertEqual((p.returncode, p.stdout), (0, ""), p.stderr)

    def test_new_phrase_copied_from_a_task_is_a_hit(self):
        kogen = self.base_prompt_task()
        self.put("reference/lib/fresh.ex", 'def fresh, do: "rerun the migration twice and compare checksums"\n')
        self.write_patch(CLEAN + '+  # Always rerun the migration twice and compare checksums.\n')
        p = self.leak("--kogen", kogen)
        self.assertEqual(p.returncode, 1)
        self.assertIn("string literal 'rerun the migration twice and compare checksums'", p.stdout)

    def test_moved_base_phrase_is_not_a_hit(self):
        kogen = self.base_prompt_task()
        self.write_patch(
            '--- a/prompt.ex\n+++ b/prompt.ex\n@@ -1,2 +1,2 @@\n'
            '-@prompt "Be careful: %s, then stop."\n @other "second line of the prompt"\n'
            '+@prompt "Be careful: %s, then stop."\n' % (self.PHRASE, self.PHRASE))
        p = self.leak("--kogen", kogen)
        self.assertEqual((p.returncode, p.stdout), (0, ""), p.stderr)

    def kogen_file(self, rel, text):
        d = os.path.join(self.tmp, "kogen-src")
        os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
        with open(os.path.join(d, rel), "w") as f:
            f.write(text)
        return d

    def test_phrase_in_a_base_prompt_file_is_not_a_hit(self):
        """A phrase the base prompt files already hold is not task content, even outside the patch context."""
        self.put("reference/lib/phrase.ex", 'def note, do: "%s"\n' % self.PHRASE)
        kogen = self.kogen_file("cli/agent/prompts/builder.md", "Rules: %s, then stop.\n" % self.PHRASE)
        self.write_patch(CLEAN + "+  # Always %s.\n" % self.PHRASE)
        p = self.leak("--kogen", kogen)
        self.assertEqual((p.returncode, p.stdout), (0, ""), p.stderr)

    def test_solution_phrase_only_in_kogen_source_is_still_a_hit(self):
        """The substring rule covers the prompt surface only: a task made from a reverted Kogen feature
        can have its solution phrasing elsewhere in the source at the lane's sha."""
        self.put("reference/lib/phrase.ex", 'def note, do: "%s"\n' % self.PHRASE)
        kogen = self.kogen_file("lib/kogen/solution.ex", '@doc "Then %s, as the old code did."\n' % self.PHRASE)
        self.kogen_file("cli/agent/prompts/builder.md", "Rules: read the request first.\n")
        self.write_patch(CLEAN + "+  # Always %s.\n" % self.PHRASE)
        p = self.leak("--kogen", kogen)
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        self.assertIn("string literal '%s'" % self.PHRASE, p.stdout)

    def test_numbers_are_not_identifiers(self):
        self.elixir_task()
        self.write_patch(self.diff_adding("  @max_output 1_048_576"))
        self.assertEqual(self.leak().returncode, 0)

    def test_default_kogen_source_is_the_harness_clone(self):
        self.elixir_task()
        src, home = os.path.join(self.tmp, "src"), os.path.join(self.tmp, "home")
        os.makedirs(src)
        with open(os.path.join(src, "b.ex"), "w") as f:
            f.write("x |> Enum.with_index()\n")
        git = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e", "GIT_COMMITTER_NAME": "t",
               "GIT_COMMITTER_EMAIL": "t@e", "GIT_CONFIG_GLOBAL": os.devnull}
        for cmd in (["init", "-q"], ["add", "."], ["commit", "-q", "-m", "x"]):
            subprocess.run(["git", "-C", src, *cmd], env=git, check=True, capture_output=True)
        sha = subprocess.run(["git", "-C", src, "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
        os.makedirs(home)
        subprocess.run(["git", "clone", "-q", "--bare", src, os.path.join(home, "kogen.git")], env=git, check=True)
        self.write_patch(self.diff_adding("  y |> Enum.with_index()"))
        self.two_tasks()
        path = self.experiment()
        exp = common.read_json(path)
        for lane in exp["lanes"]:
            lane["sha"] = sha
        common.write_json(path, exp)
        env = {**os.environ, "KOGEN_LANES_HOME": home}
        p = subprocess.run([sys.executable, ENTRY, path, "--tasks", self.tasks], capture_output=True, text=True, env=env)
        self.assertEqual((p.returncode, p.stdout), (0, ""), p.stderr)
        p = subprocess.run([sys.executable, ENTRY, path, "--tasks", self.tasks], capture_output=True, text=True,
                           env={**env, "KOGEN_LANES_HOME": os.path.join(self.tmp, "none")})
        self.assertEqual(p.returncode, 1)
        self.assertIn("no Kogen source", p.stderr)

    # --- an unreadable reference is an error, not a clean result ---------------------------------

    def test_missing_tasks_folder_exits_2(self):
        p = self.leak(tasks=os.path.join(self.tmp, "nowhere"))
        self.assertEqual(p.returncode, 2)
        self.assertIn("not found", p.stderr)

    def test_incomplete_task_folder_exits_2(self):
        for part in ("task.toml", "start", "evaluator"):
            with self.subTest(part=part):
                shutil.rmtree(self.tasks)
                shutil.copytree(TASK, os.path.join(self.tasks, "task-mini"))
                self.two_tasks()
                path = os.path.join(self.tasks, "task-mini", part)
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
                p = self.leak()
                self.assertEqual(p.returncode, 2)
                self.assertIn(part, p.stderr)

    def test_runs_folder_without_cells_exits_2(self):
        empty = os.path.join(self.tmp, "runs", "empty")
        os.makedirs(empty)
        for runs in ([empty], [os.path.join(self.tmp, "runs", "typo")]):
            p = self.leak("--runs", *runs)
            self.assertEqual(p.returncode, 2)
            self.assertIn("no cells/", p.stderr)

    def test_preflight_refuses_when_the_tasks_folder_is_missing(self):
        p = self.preflight(tasks=os.path.join(self.tmp, "nowhere"))
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        self.assertIn("LEAK: leakcheck: error", p.stdout)

    # --- notes ------------------------------------------------------------------------------------

    def test_skipped_files_are_named(self):
        self.put("evaluator/files/big_test.go", "// " + "x" * (1 << 20) + "\n")
        self.put("evaluator/files/binary.bin", "")
        with open(os.path.join(self.tasks, "task-mini", "evaluator", "files", "binary.bin"), "wb") as f:
            f.write(b"\xff\xfe\x00")
        p = self.leak()
        self.assertEqual(p.returncode, 0)
        self.assertIn("big_test.go", p.stderr)
        self.assertIn("binary.bin", p.stderr)

    # --- only failing cells ------------------------------------------------------------------------

    def test_passing_cells_are_not_compared(self):
        run = os.path.join(self.tmp, "runs", "old")
        for rep, passed in (("r1", True), ("r2", False)):
            cell = os.path.join(run, "cells", "task-mini", rep, "baseline")
            os.makedirs(cell)
            common.write_json(os.path.join(cell, "result.json"), {})
            common.write_json(os.path.join(cell, "evaluation.json"), {"all_passed": passed})
            with open(os.path.join(cell, "stdout.txt"), "w") as f:
                f.write(FAILURE if rep == "r1" else "nothing of interest here at all, just a short note")
        self.write_patch(CLEAN + f"+  # {FAILURE}\n")
        self.assertEqual(self.leak("--runs", run).returncode, 0)
        with open(os.path.join(run, "cells", "task-mini", "r1", "baseline", "evaluation.json"), "w") as f:
            f.write('{"all_passed": false}')
        self.assertEqual(self.leak("--runs", run).returncode, 1)

    # --- spellings, paths, other trees ----------------------------------------------------------------

    def test_task_name_in_other_spellings(self):
        for spelling in ("task_two", "TaskTwo", "task two", "taskTwo", "TASK-TWO"):
            with self.subTest(spelling=spelling):
                self.write_patch(CLEAN + f"+  # special case for {spelling}\n")
                p = self.leak()
                self.assertEqual(p.returncode, 1)
                self.assertIn("task name", p.stdout)

    def test_added_file_paths_are_checked(self):
        self.write_patch("--- /dev/null\n+++ b/priv/prompts/task-two.md\n@@ -0,0 +1 @@\n+Keep checks green.\n")
        p = self.leak()
        self.assertEqual(p.returncode, 1)
        self.assertIn("task name 'task-two'", p.stdout)

    def test_identifiers_and_literals_from_every_tree(self):
        trees = {"start": "start/lib/start_only.ex", "reference": "reference/lib/ref_only.ex",
                 "wrong": "wrong/off-by-one/lib/wrong_only.ex"}
        for tree, rel in trees.items():
            with self.subTest(tree=tree):
                self.put(rel, 'def compute_%s_value, do: "unique message of the %s tree"\n' % (tree, tree))
                self.write_patch(CLEAN + f"+  # uses compute_{tree}_value\n")
                p = self.leak()
                self.assertEqual(p.returncode, 1)
                self.assertIn(f"identifier 'compute_{tree}_value' (from task task-mini {tree}", p.stdout)
                self.write_patch(CLEAN + f'+  log("unique message of the {tree} tree")\n')
                p = self.leak()
                self.assertEqual(p.returncode, 1)
                self.assertIn("string literal", p.stdout)

    def preflight(self, tasks):
        run_dir = os.path.join(self.tmp, "run")
        shutil.rmtree(run_dir, ignore_errors=True)
        self.experiment()
        shutil.copytree(self.exp_dir, run_dir)
        env = {**os.environ, "KOGEN_LANES_HOME": os.path.join(self.tmp, "home"), "FAKE_KOGEN_TASK": TASK}
        return subprocess.run([sys.executable, PREFLIGHT, run_dir, "--tasks", tasks, "--artifact", FAKE],
                              env=env, capture_output=True, text=True, timeout=60)


if __name__ == "__main__":
    unittest.main()
