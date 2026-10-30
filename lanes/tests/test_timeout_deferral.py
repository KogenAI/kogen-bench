import os
import shutil
import tempfile
import unittest
from unittest import mock

from lanes import common, dispatch, report, timeoutguard

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
ART = "ab" * 32


class TimeoutDeferral(unittest.TestCase):
    """A stub task that always times out (the fake deadline is the stub's outcome, so the test takes seconds)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = self.tmp.name
        self.tasks = os.path.join(self.root, "tasks")
        self.ledger = os.path.join(self.root, "ledger")
        env = mock.patch.dict(os.environ, {"KOGEN_LANES_HOME": os.path.join(self.root, "home"),
                                           "LANES_TIMEOUT_LEDGER": self.ledger})
        env.start()
        self.addCleanup(env.stop)
        self.hosts = os.path.join(self.root, "hosts.json")
        common.write_json(self.hosts, {"local": {"target": "local", "slots": 1}})
        for t in ("good", "slow"):
            shutil.copytree(os.path.join(FIX, "task-mini"), os.path.join(self.tasks, t))
        self.started = []

    def plan(self, exp_id, reps=3):
        exp = common.read_json(os.path.join(FIX, "experiment-good.json"))
        exp.update(id=exp_id, tasks=["good", "slow"], reps=reps, deadline_s=2, decision_rule={"kind": "descriptive"})
        exp["lanes"] = exp["lanes"][:1]
        for lane in exp["lanes"]:
            lane["patch"] = None
        run = os.path.join(self.root, "runs", exp_id)
        src = os.path.join(self.root, exp_id + ".json")
        common.write_json(src, exp)
        common.write_json(os.path.join(run, "lanes.lock.json"),
                          [{"name": l["name"], "sha": l["sha"], "artifact_sha256": ART} for l in exp["lanes"]])
        self.assertEqual(dispatch.plan_main([src, "--run-dir", run, "--tasks", self.tasks]), 0)
        return run

    def run_it(self, run, outcome_slow="timeout"):
        def run_cell(host, cell, artifact):
            self.started.append((os.path.basename(run), cell))
            out = outcome_slow if cell.startswith("slow/") else "landed"
            common.write_json(os.path.join(common.cell_dir(run, cell), "result.json"),
                              {"cell": cell, "outcome": out, "totals": {}, "stages": []})
            return True

        with mock.patch.object(dispatch.Host, "run_cell", run_cell):
            return dispatch.run_all(run, self.tasks, self.hosts, log=lambda m: None, skip_preflight=True)

    def slow_starts(self, exp_id):
        return [c for e, c in self.started if e == exp_id and c.startswith("slow/")]

    def test_two_timeouts_then_deferred_others_continue_override_readmits(self):
        r1 = self.plan("study-a-u1")
        self.assertEqual(self.run_it(r1), 0)
        self.assertEqual(len(self.slow_starts("study-a-u1")), 2, "slow runs twice, the third rep is deferred")
        self.assertEqual(len([1 for e, c in self.started if c.startswith("good/")]), 3, "other tasks continue")
        self.assertEqual(common.read_json(os.path.join(r1, "PLAN.json"))["timeout_deferrals"]["slow"]["reason"],
                         "deferred: 2 timeouts")
        self.assertIn("deferred: 2 timeouts", open(os.path.join(r1, "report.md")).read())
        self.assertEqual(report.report(r1)["verdict"]["decision"], "incomplete")
        # another experiment of the same study (host replicate suffix): never launched
        r2 = self.plan("study-a-e2")
        self.assertEqual(self.run_it(r2), 0)
        self.assertEqual(self.slow_starts("study-a-e2"), [])
        self.assertEqual(len([1 for e, c in self.started if e == "study-a-e2" and c.startswith("good/")]), 3)
        self.assertTrue(os.path.isfile(os.path.join(r2, "plan.jsonl")))
        self.assertEqual(len([c for c in common.read_jsonl(os.path.join(r2, "plan.jsonl")) if c["task"] == "slow"]), 3)
        self.assertIn("slow\t", open(os.path.join(self.ledger, "DEFERRED.tsv")).read())
        # a different study is not affected
        r3 = self.plan("study-b-u1")
        self.run_it(r3)
        self.assertEqual(len(self.slow_starts("study-b-u1")), 2)
        # override: counts restart; the task is admitted again
        info = timeoutguard.gaps(r2)[0]
        os.makedirs(os.path.dirname(info["override"]), exist_ok=True)
        open(info["override"], "w").close()
        r4 = self.plan("study-a-s4")
        self.run_it(r4)
        self.assertEqual(len(self.slow_starts("study-a-s4")), 2, "re-admitted: runs twice, then deferred again")
        self.assertEqual(timeoutguard.count(("study-a", "slow", timeoutguard.tool_of(
            common.read_json(os.path.join(r4, "experiment.json"))["lanes"][0]), common.read_json(
            os.path.join(r4, "experiment.json"))["lanes"][0]["sha"])), 2)

    def test_guard_off_without_ledger(self):
        os.environ.pop("LANES_TIMEOUT_LEDGER")
        r1 = self.plan("study-c-u1", reps=3)
        self.run_it(r1)
        self.assertEqual(len(self.slow_starts("study-c-u1")), 3)
        self.assertFalse(os.path.exists(self.ledger))

    def test_landed_cells_never_count(self):
        r1 = self.plan("study-d-u1", reps=3)
        self.run_it(r1, outcome_slow="landed")
        self.assertEqual(len(self.slow_starts("study-d-u1")), 3)
        self.assertEqual(timeoutguard.count(("study-d", "slow", "x", "y")), 0)


if __name__ == "__main__":
    unittest.main()
