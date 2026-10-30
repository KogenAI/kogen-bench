import glob
import os
import shutil
import tempfile
import time
import unittest
from unittest import mock

from lanes import approval, approvecache, common, dispatch, preflight

HERE = os.path.dirname(os.path.abspath(__file__))
FAKE = os.path.join(HERE, "fake-kogen")
TASK = os.path.join(HERE, "fixtures", "task-mini")
SHA = "0123456789abcdef0123456789abcdef01234567"
ART = "cd" * 32


class ApprovalReuse(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = self._tmp.name
        self.tasks = os.path.join(self.tmp, "tasks")
        self.task = os.path.join(self.tasks, "task-mini")
        shutil.copytree(TASK, self.task)
        self.intent_md = os.path.join(self.task, "supplied", "gherkin", "intent.md")
        self.edit(self.intent_md, lambda t: t.replace("add-numbers", "task-mini"))
        self.home = os.path.join(self.tmp, "home")
        self.cache = os.path.join(self.tmp, "approval-cache")
        self.run_dir = os.path.join(self.tmp, "runs", "exp-mini")
        self.kogen = os.path.join(self.home, "artifacts", ART)
        os.makedirs(os.path.dirname(self.kogen))
        shutil.copy2(FAKE, self.kogen)
        self.lanes = [{"name": "base", "sha": SHA, "patch": None, "settings": {}},
                      {"name": "patched", "sha": SHA, "patch": None, "settings": {}}]
        self.write_run()
        env = mock.patch.dict(os.environ, {"KOGEN_LANES_HOME": self.home, "FAKE_KOGEN_TASK": TASK,
                                           "LANES_APPROVAL_CACHE": self.cache})
        env.start()
        self.addCleanup(env.stop)
        approvecache._release_memo.clear()

    @staticmethod
    def edit(path, change):
        with open(path) as f:
            text = f.read()
        with open(path, "w") as f:
            f.write(change(text))

    def write_run(self, lock=None):
        exp = {"id": "exp-mini", "phase": "build", "intent_form": "gherkin", "reps": 1, "deadline_s": 60,
               "cost_cap_usd": 100, "kogen": {"repo": "https://example.invalid/kogen.git"}, "tasks": ["task-mini"],
               "hosts": ["local"], "decision_rule": {"kind": "paired-pass-rate"}, "lanes": self.lanes}
        common.write_json(os.path.join(self.run_dir, "experiment.json"), exp)
        common.write_json(os.path.join(self.run_dir, "lanes.lock.json"), lock or [
            {"name": l["name"], "sha": SHA, "patch_sha256": None, "artifact_sha256": ART} for l in self.lanes])

    def preflight(self, deadline_s=preflight.DEADLINE_S, run_dir=None, **env):
        """In-process; `(refusals, lines, real approvals)`."""
        lines, calls = [], []
        real = preflight._approve

        def counted(*a, **k):
            calls.append(a[0])
            return real(*a, **k)

        with mock.patch.dict(os.environ, env), mock.patch.object(preflight, "DEADLINE_S", deadline_s), \
             mock.patch.object(preflight, "_approve", side_effect=counted):
            bad = preflight.preflight(run_dir or self.run_dir, self.tasks, out=lines.append)
        return bad, lines, len(calls)

    def entries(self, suffix=".json"):
        return [p for p in glob.glob(os.path.join(self.cache, "*", "*" + suffix))
                if suffix != ".json" or not p.endswith(".refused.json")]

    # 1. reuse on identical inputs

    def test_identical_inputs_reuse_the_approval(self):
        bad, lines, calls = self.preflight()
        self.assertEqual((bad, calls), (0, 1), lines)  # both lanes run the same Kogen with the same settings
        self.assertIn("reused", lines[1])
        bad, lines, calls = self.preflight()
        self.assertEqual((bad, calls), (0, 0), lines)
        self.assertTrue(all(": ok: approved " in l and "reused" in l for l in lines), lines)
        rec = common.read_json(self.entries()[0])
        self.assertRegex(rec["approval_hash"], r"^[0-9a-f]{64}$")
        self.assertTrue(lines[0].split("approved ")[1].startswith(rec["approval_hash"][:8]))

    def test_in_run_preflight_after_lanes_preflight_does_no_approval_work(self):
        self.assertEqual(self.preflight()[:2][0], 0)
        hosts = os.path.join(self.tmp, "hosts.json")
        common.write_json(hosts, {"local": {"target": "local", "slots": 1}})
        source = os.path.join(self.tmp, "experiment.json")
        shutil.copyfile(os.path.join(self.run_dir, "experiment.json"), source)
        self.assertEqual(dispatch.plan_main([source, "--run-dir", self.run_dir, "--tasks", self.tasks]), 0)
        started, calls = [], []
        real = preflight._approve

        def run_cell(host, cell, artifact):
            started.append(cell)
            common.write_json(os.path.join(common.cell_dir(self.run_dir, cell), "result.json"),
                              {"outcome": "landed", "totals": {}, "stages": []})
            return True

        with mock.patch.object(preflight, "_approve", side_effect=lambda *a, **k: calls.append(1) or real(*a, **k)), \
             mock.patch.object(dispatch.Host, "run_cell", run_cell), mock.patch.object(dispatch, "verify_inputs"):
            code = dispatch.run_all(self.run_dir, self.tasks, hosts, log=lambda m: None)
        self.assertEqual((code, len(calls), len(started)), (0, 0, 2))

    def test_a_later_unit_with_the_same_kogen_reuses_and_another_sha_does_not(self):
        self.assertEqual(self.preflight()[2], 1)
        later = os.path.join(self.tmp, "runs", "exp-later")
        shutil.copytree(self.run_dir, later)
        bad, lines, calls = self.preflight(run_dir=later)
        self.assertEqual((bad, calls), (0, 0), lines)
        self.assertIn("in exp-mini task-mini", lines[0])
        common.write_json(os.path.join(later, "lanes.lock.json"), [
            {"name": l["name"], "sha": "f" * 40, "patch_sha256": None, "artifact_sha256": ART} for l in self.lanes])
        self.assertEqual(self.preflight(run_dir=later)[2], 1)

    # 2. a miss on every changed input

    def test_every_changed_input_misses(self):
        self.assertEqual(self.preflight()[2], 1)
        changes = {
            "start/": lambda: self.edit(self.start_file(), lambda t: t + "\n"),
            "start/ new file": self.new_start_file,
            "task.toml": lambda: self.edit(os.path.join(self.task, "task.toml"), lambda t: "# changed\n" + t),
            "supplied Intent": lambda: self.edit(self.intent_md, lambda t: t + "\n"),
            "approval deadline": lambda: self.edit(os.path.join(self.task, "task.toml"),
                                                   lambda t: "approve_timeout_s = 119\n" + t),
            "lane models": lambda: (self.lanes[0]["settings"].update(models={"build": "openai/gpt-5.1 low"}),
                                    self.lanes[1]["settings"].update(models={"build": "openai/gpt-5.1 low"}),
                                    self.write_run()),
            "Kogen sha": lambda: self.write_run([{"name": l["name"], "sha": "e" * 40, "patch_sha256": None,
                                                  "artifact_sha256": ART} for l in self.lanes]),
            "patch": lambda: self.write_run([{"name": l["name"], "sha": "e" * 40, "patch_sha256": "9" * 64,
                                              "artifact_sha256": ART} for l in self.lanes]),
            "Kogen executable": lambda: self.edit(self.kogen, lambda t: t + "\n# rebuilt\n"),
            "environment": lambda: os.environ.__setitem__("GOFLAGS", "-mod=mod"),
        }
        for name, change in changes.items():
            with self.subTest(name):
                change()
                approvecache._release_memo.clear()
                bad, lines, calls = self.preflight()
                self.assertEqual((bad, calls), (0, 1), lines)  # a fresh real approval, then the twin lane reuses it
                self.assertNotIn("reused", lines[0])
                self.assertEqual(self.preflight()[2], 0)  # and it is now reusable itself
        os.environ.pop("GOFLAGS", None)

    def start_file(self):
        for dirpath, _, names in sorted(os.walk(os.path.join(self.task, "start"))):
            for name in sorted(names):
                if not os.path.islink(os.path.join(dirpath, name)):
                    return os.path.join(dirpath, name)

    def new_start_file(self):
        with open(os.path.join(self.task, "start", f"added-{time.monotonic_ns()}.txt"), "w") as f:
            f.write("x\n")

    def test_key_covers_node_npm_entry_and_harness_code(self):
        args = dict(exp={"intent_form": "gherkin"}, run_dir=self.run_dir, task=self.task, slug="task-mini",
                    supplied=os.path.join(self.task, "supplied", "gherkin"), kogen=self.kogen, deadline_s=120,
                    lane=self.lanes[0], artifact=None)
        entry = os.path.join(self.tmp, "npm-entry")
        os.makedirs(entry)
        common.write_json(os.path.join(entry, "manifest.json"), {"inputs": "a"})
        config = f"  setup:\n    - '(cd web && /py /nm.py restore --entry {entry})'\n"
        base = approvecache.key(config=config, node={"path": "/n", "version": "22.1.0"}, **args)[0]
        self.assertNotEqual(base, approvecache.key(config=config, node={"path": "/n", "version": "22.2.0"}, **args)[0])
        common.write_json(os.path.join(entry, "manifest.json"), {"inputs": "b"})
        self.assertNotEqual(base, approvecache.key(config=config, node={"path": "/n", "version": "22.1.0"}, **args)[0])
        with mock.patch.object(approvecache, "CODE", approvecache.CODE + ("approval.py",)):
            self.assertNotEqual(base, approvecache.key(config=config, node={"path": "/n", "version": "22.1.0"}, **args)[0])

    def test_dispatch_only_environment_does_not_change_the_key(self):
        self.assertEqual(self.preflight()[2], 1)
        shim = os.path.join(self.tmp, ".lanes-shim")
        os.makedirs(shim)
        bad, lines, calls = self.preflight(PATH=shim + os.pathsep + os.environ["PATH"], SLOTS="3", DAYDIR="x",
                                           GIT_AUTHOR_NAME="Kogen Lanes", LANES_SHARED_GOCACHE="/tmp/g",
                                           TMPDIR=self.tmp, LANES_ENV="/x/run-u/lanes.env")
        self.assertEqual((bad, calls), (0, 0), lines)

    # 3. a deferred approval still defers

    def test_timeout_is_never_stored_and_still_defers(self):
        for attempt in range(2):
            bad, lines, calls = self.preflight(deadline_s=1, FAKE_KOGEN_APPROVE_DELAY_S="3")
            self.assertEqual((bad, calls), (0, 2), lines)  # no lane may borrow the other's unfinished approval
            self.assertTrue(all("DEFERRED" in l for l in lines[:2]), lines)
            self.assertEqual(approval.pending(self.run_dir), {"task-mini"})
            self.assertEqual(self.entries() + self.entries(".refused.json"), [])
            os.remove(os.path.join(self.run_dir, "PLAN.json"))  # a fresh unit, not the in-run skip of debt

    def test_paired_retry_reuses_only_the_lane_that_approved(self):
        self.lanes[1]["settings"] = {"models": {"build": "openai/gpt-5.1 high"}}  # two distinct keys
        self.write_run()
        real, seen = preflight._approve, []

        def slow_base(task, slug, supplied, kogen, config, deadline_s, refusal_context=None):
            seen.append(refusal_context[2])
            if refusal_context[2] == "base" and len(seen) < 3:
                return False, preflight.ApprovalTimeout("approve refused (timed out)"), None
            return real(task, slug, supplied, kogen, config, deadline_s, refusal_context)

        lines = []
        with mock.patch.object(preflight, "_approve", side_effect=slow_base):
            self.assertEqual(preflight.preflight(self.run_dir, self.tasks, out=lines.append), 0)
            self.assertEqual(approval.pending(self.run_dir), {"task-mini"})
            self.assertEqual(preflight.preflight(self.run_dir, self.tasks, out=lines.append, task_ids=["task-mini"],
                                                 stage="after_cells"), 0)
        self.assertEqual(seen, ["base", "patched", "base"])  # base retried for real; patched reused
        self.assertEqual(approval.pending(self.run_dir), set())
        self.assertIn("reused", lines[-1])

    # 4. a refused approval is never reused

    def test_refusal_is_not_stored_as_an_approval(self):
        for attempt in range(2):
            bad, lines, calls = self.preflight(FAKE_KOGEN_LINT="refuse")
            self.assertEqual((bad, calls), (2, 2), lines)
            self.assertTrue(all("REFUSED" in l for l in lines), lines)
        self.assertEqual(self.entries(), [])
        self.assertEqual(len(self.entries(".refused.json")), 1)

    def test_a_refusal_under_the_same_key_blocks_an_earlier_approval(self):
        self.assertEqual(self.preflight()[2], 1)
        refused = [False]
        real = preflight._approve

        def flaky(*a, **k):
            return (False, "approve refused (exit 1):\n    intent/lint: flaky", None) if refused[0] else real(*a, **k)

        digest = common.read_json(self.entries()[0])["key"]
        approvecache.store(digest, {}, False, False, None, {"experiment": "other"})  # as a concurrent unit refusing
        refused[0] = True
        lines = []
        with mock.patch.object(preflight, "_approve", side_effect=flaky) as approve:
            bad = preflight.preflight(self.run_dir, self.tasks, out=lines.append)
        self.assertEqual((bad, approve.call_count), (2, 2), lines)
        self.assertIsNone(approvecache.lookup(digest))

    def test_off_without_the_cache_variable(self):
        with mock.patch.dict(os.environ):
            del os.environ["LANES_APPROVAL_CACHE"]
            self.assertEqual(self.preflight()[2], 2)
            self.assertEqual(self.preflight()[2], 2)
        self.assertFalse(os.path.exists(self.cache))


if __name__ == "__main__":
    unittest.main()
