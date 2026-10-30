import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

from lanes import approval, carry, common, dispatch, preflight, report

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
ART = "ab" * 32


class ApprovalDeferrals(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = self.tmp.name
        self.run = os.path.join(self.root, "runs", "exp-mini")
        self.tasks = os.path.join(self.root, "tasks")
        self.home = os.path.join(self.root, "home")
        self.env = mock.patch.dict(os.environ, {"KOGEN_LANES_HOME": self.home})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.exp = common.read_json(os.path.join(FIX, "experiment-good.json"))
        self.exp.update(id="exp-mini", tasks=["good", "slow"], reps=2,
                        decision_rule={"kind": "descriptive"})
        for task in self.exp["tasks"]:
            shutil.copytree(os.path.join(FIX, "task-mini"), os.path.join(self.tasks, task))
        for lane in self.exp["lanes"]:
            lane["patch"] = None
        self.source = os.path.join(self.root, "experiment.json")
        common.write_json(self.source, self.exp)
        common.write_json(os.path.join(self.run, "lanes.lock.json"),
                          [{"name": l["name"], "sha": l["sha"], "artifact_sha256": ART} for l in self.exp["lanes"]])
        self.assertEqual(dispatch.plan_main([self.source, "--run-dir", self.run, "--tasks", self.tasks]), 0)
        self.plan = common.read_jsonl(os.path.join(self.run, "plan.jsonl"))
        self.hosts = os.path.join(self.root, "hosts.json")
        common.write_json(self.hosts, {"local": {"target": "local", "slots": 2}})
        self.events, self.checks = [], []

    def execute(self, check):
        def run_cell(host, cell, artifact):
            self.events.append(cell)
            time.sleep(0.01)  # make the paired retry barrier observable with two slots
            common.write_json(os.path.join(common.cell_dir(self.run, cell), "result.json"),
                              {"outcome": "landed", "totals": {}, "stages": []})
            return True

        with mock.patch.object(preflight, "check_one", side_effect=check), \
             mock.patch.object(dispatch.Host, "run_cell", run_cell):
            return dispatch.run_all(self.run, self.tasks, self.hosts, log=lambda m: None)

    def check(self, recover=False, hard=False):
        def check(exp, run, tasks, task, lane, artifact):
            self.checks.append((task, lane["name"], len(self.events)))
            if task == "slow" and lane["name"] == "patched":
                if recover and self.events:
                    # Every ordinary cell has a result before any lane of this task is admitted.
                    for c in self.plan:
                        if c["task"] == "good":
                            self.assertTrue(os.path.isfile(os.path.join(common.cell_dir(run, c["cell"]), "result.json")))
                    return True, "approved later"
                if hard:
                    return False, "intent/lint: a timed out string is not a deadline"
                return False, preflight.ApprovalTimeout("approve refused (timed out): setup-1")
            return True, "approved"
        return check

    def test_one_timeout_runs_ordinary_tasks_and_keeps_all_cells(self):
        # Reproduce the 13-of-14 approved matrix rather than a single-task special case.
        for n in range(5):
            task = f"good-{n}"
            shutil.copytree(os.path.join(FIX, "task-mini"), os.path.join(self.tasks, task))
            self.exp["tasks"].insert(-1, task)
        common.write_json(self.source, self.exp)
        self.assertEqual(dispatch.plan_main([self.source, "--run-dir", self.run, "--tasks", self.tasks]), 0)
        self.plan = common.read_jsonl(os.path.join(self.run, "plan.jsonl"))
        self.assertEqual(self.execute(self.check()), 5)
        self.assertEqual(len(self.events), 24)
        self.assertTrue(all(not c.startswith("slow/") for c in self.events))
        initial = [row for row in self.checks if row[2] == 0]
        self.assertEqual(len(initial), 14)
        self.assertEqual(common.read_jsonl(os.path.join(self.run, "plan.jsonl")), self.plan)
        self.assertEqual(approval.pending(self.run), {"slow"})
        debt = approval.records(self.run)["slow"]
        self.assertEqual(debt["lanes"], ["base", "patched"])
        self.assertEqual([a["stage"] for a in debt["attempts"]], ["initial", "after_cells"])
        self.assertEqual(debt["attempts"][0]["results"][0]["ok"], True)

    def test_later_attempt_runs_every_deferred_lane_after_barrier(self):
        self.assertEqual(self.execute(self.check(recover=True)), 0)
        self.assertEqual(len(self.events), len(self.plan))
        self.assertTrue(all(c.startswith("good/") for c in self.events[:4]))
        self.assertTrue(all(c.startswith("slow/") for c in self.events[4:]))
        self.assertEqual(approval.pending(self.run), set())
        self.assertEqual(approval.records(self.run)["slow"]["state"], "approved")

    def test_final_gap_is_in_report_and_original_plan_and_resume(self):
        self.assertEqual(self.execute(self.check()), 5)
        rep = report.report(self.run)
        self.assertEqual(rep["verdict"]["decision"], "incomplete")
        self.assertEqual(rep["infrastructure_gaps"][0]["task"], "slow")
        self.assertTrue(all(l["cells"]["planned"] == 4 for l in rep["lanes"]))
        self.assertIn("Infrastructure gap", report.render(rep))
        self.assertEqual(common.read_json(os.path.join(self.run, "PLAN.json"))["experiment"]["tasks"], ["good", "slow"])
        before = len(self.events)
        def later(*args):
            self.assertEqual(args[3], "slow", "completed tasks must not incur new approval debt")
            return True, "approved on later unit"
        self.assertEqual(self.execute(later), 0)
        self.assertEqual(len(self.events) - before, 4)
        self.assertEqual(report.report(self.run)["infrastructure_gaps"], [])
        self.assertEqual(len(approval.records(self.run)["slow"]["attempts"]), 3)

    def test_non_timeout_refuses_before_any_cell(self):
        with self.assertRaises(dispatch.DispatchError):
            self.execute(self.check(hard=True))
        self.assertEqual(self.events, [])

    def test_non_timeout_on_retry_stops_with_original_refusal(self):
        first = self.check()
        def check(*args):
            if self.events and args[3] == "slow":
                return False, "intent/lint: real refusal"
            return first(*args)
        with self.assertRaisesRegex(dispatch.DispatchError, "deferred retry"):
            self.execute(check)
        self.assertTrue(all(c.startswith("good/") for c in self.events))

    def test_standalone_then_in_run_does_not_retry_early(self):
        with mock.patch.object(preflight, "check_one", side_effect=self.check()):
            self.assertEqual(preflight.preflight(self.run, self.tasks, out=lambda m: None), 0)
        self.checks.clear()
        self.assertEqual(self.execute(self.check(recover=True)), 0)
        self.assertTrue(all(n >= 4 for t, _, n in self.checks if t == "slow"))

    def test_carry_queue_retries_same_experiment_once_per_later_unit(self):
        self.assertEqual(self.execute(self.check()), 5)
        queue = os.path.join(self.root, "approval-carry")
        carry.enqueue(queue, self.run, self.tasks, "cgr", 2, "0.3")
        row_path = os.path.join(queue, "exp-mini.json")
        with mock.patch.object(carry.subprocess, "run") as invoke:
            carry.drain(queue, "/release/run-queued.sh", "exp-mini")
            invoke.assert_not_called()
            carry.drain(queue, "/release/run-queued.sh", "later-unit")
            self.assertEqual(invoke.call_count, 1)
            self.assertEqual(invoke.call_args.args[0],
                             ["/bin/bash", "/release/run-queued.sh", "cgr", "exp-mini", self.tasks, "2", "0.3"])
            self.assertEqual(invoke.call_args.kwargs["env"]["LANES_CARRY_ACTIVE"], "1")
        self.assertTrue(os.path.isfile(row_path))
        self.assertEqual(self.execute(lambda *args: (True, "approved")), 0)
        with mock.patch.object(carry.subprocess, "run") as invoke:
            carry.drain(queue, "/release/run-queued.sh", "later-unit")
            invoke.assert_not_called()
        self.assertFalse(os.path.exists(row_path))

    def test_retry_goes_through_host_admission(self):
        with open(os.path.join(self.root, "host-cap"), "w") as f:
            f.write("4\n")
        admissions = []
        original_init = dispatch.Runner.__init__
        def initialize(runner):
            original_init(runner)
            runner.stopped.wait = lambda seconds: False  # only elide the gate's settle/poll sleeps
        def admit(*args):
            admissions.append(len(self.events))
            return True, 0, 0, 4, 1, 4
        check = self.check(recover=True)
        def observed(*args):
            if args[3] == "slow" and self.events:
                self.assertGreaterEqual(admissions[-1], 4)
            return check(*args)
        with mock.patch.object(dispatch.Runner, "__init__", initialize), \
             mock.patch.object(dispatch, "gate_admits", side_effect=admit):
            self.assertEqual(self.execute(observed), 0)
        self.assertTrue(any(n >= 4 for n in admissions))

    def test_caps_prevent_deferred_retry_and_keep_debt(self):
        def blocked(*args):
            return "cost cap reached" if len(self.events) >= 4 else None
        with mock.patch.object(dispatch.costguard, "blocked", side_effect=blocked):
            self.assertEqual(self.execute(self.check(recover=True)), 3)
        self.assertEqual(approval.pending(self.run), {"slow"})
        self.assertEqual(len(approval.records(self.run)["slow"]["attempts"]), 1)

    def test_both_day_runners_carry_instead_of_marking_done(self):
        self.assertEqual(self.execute(self.check()), 5)
        fake = os.path.join(self.root, "fake-lanes")
        os.makedirs(os.path.join(fake, "bin"))
        with open(os.path.join(fake, "bin", "lanes-run"), "w") as f:
            f.write("import sys; sys.exit(5)\n")
        shutil.copy(os.path.join(HERE, "..", "bin", "lanes-carry"), os.path.join(fake, "bin", "lanes-carry"))
        for name, kind in (("day-runner.sh", "ccr"), ("day-runner-v3.sh", "cgr")):
            with self.subTest(name=name):
                with open(os.path.join(HERE, "..", "ops", name)) as f:
                    text = f.read()
                body = text[text.index("capped() {"):text.index("grade() {")]
                setup = '\n'.join([
                    'P=' + shlex.quote(self.root), 'LANES=' + shlex.quote(fake),
                    'KH=' + shlex.quote(self.root), 'SLOTS=2; DAYCAP=100; STOP_MARGIN=1',
                    'say() { :; }; today() { echo day; }; acc() { echo 0; }; acc_add() { :; }',
                    'cell_est() { echo 0.3; }; run_total() { echo 0; }; live_cells() { echo 0; }',
                    'wstate() { echo ok; }; wpct() { echo 0; }; wait_weekly() { exit 91; }; wait_next_day() { exit 92; }',
                    'calc() { python3 -c "import sys;print(eval(sys.argv[1]))" "$1"; }',
                    'ge() { python3 -c "import sys;sys.exit(0 if float(sys.argv[1])>=float(sys.argv[2]) else 1)" "$1" "$2"; }',
                    'sleep() { /bin/sleep 0.01; }; grade() { echo graded > "$P/partial-graded"; }',
                ])
                script = setup + '\n' + body + '\ncapped exp-mini ' + shlex.quote(self.tasks) + ' 0.3\nexit $?\n'
                p = subprocess.run(['/bin/sh', '-c', script], capture_output=True, text=True, timeout=20,
                                   env={**os.environ, 'PYTHONPATH': os.path.dirname(HERE),
                                        'PATH': os.path.dirname(sys.executable) + os.pathsep + os.environ['PATH']})
                self.assertEqual(p.returncode, 5, p.stdout + p.stderr)
                self.assertFalse(os.path.exists(os.path.join(self.run, "DONE")))
                self.assertFalse(os.path.exists(os.path.join(self.run, "GRADED")))
                self.assertTrue(os.path.isfile(os.path.join(self.root, "partial-graded")))
                row = common.read_json(os.path.join(self.root, "approval-carry", "exp-mini.json"))
                self.assertEqual((row["kind"], row["run_dir"]), (kind, self.run))
