import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from lanes import common, costguard, dispatch, live
from tests import test_dispatch
from tests.test_dispatch import FAKE_LANES, entry

REAL_LANES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


class Reap(unittest.TestCase):
    """Phantom live cells: the host cap of 1 must not stay taken by a cell that was killed hard."""

    setUp, write_lock, set_exp, plan, events_lines, read, results = (
        test_dispatch.Dispatch.setUp, test_dispatch.Dispatch.write_lock, test_dispatch.Dispatch.set_exp, test_dispatch.Dispatch.plan, test_dispatch.Dispatch.events_lines,
        test_dispatch.Dispatch.read, test_dispatch.Dispatch.results)

    def start(self, hold, **env):
        common.write_json(self.hosts, {"local": {"target": "local", "slots": 1}})
        self.set_exp(reps=1)
        self.assertEqual(self.plan().returncode, 0)
        self.hold = os.path.join(self.tmp, "hold.pid")
        env = dict(self.env, FAKE_LIVE=REAL_LANES, FAKE_COST="0.5", **env)
        if hold:
            env["FAKE_HOLD"] = self.hold
        return subprocess.Popen([sys.executable, entry("lanes-run"), self.run_dir, "--tasks", self.tasks,
                                 "--hosts", self.hosts, "--lanes-dir", FAKE_LANES, "--skip-preflight"],
                                env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def wait_for(self, path):
        end = time.time() + 20
        while time.time() < end and not os.path.exists(path):
            time.sleep(0.05)
        self.assertTrue(os.path.exists(path))
        time.sleep(0.3)  # the pid is written after live.json
        return int(self.read(path))

    def fault(self, **env):
        proc = self.start(True, **env)
        pid = self.wait_for(self.hold)
        os.kill(pid, signal.SIGKILL)
        out, err = proc.communicate(timeout=60)
        return proc.returncode, err

    def test_killed_cell_is_reaped_and_the_next_one_runs(self):
        code, err = self.fault(FAKE_WS_GONE="1")
        cells = [c["cell"] for c in common.read_jsonl(os.path.join(self.run_dir, "plan.jsonl"))]
        first = next(c for c in cells if not os.path.isfile(os.path.join(common.cell_dir(self.run_dir, c), "result.json")))
        second = next(c for c in cells if c != first)
        d = common.cell_dir(self.run_dir, first)
        estimate = 5 * 2.0  # five unknown-usage requests at the $2 allowance
        line = [l for l in err.splitlines() if "reaped phantom cell" in l]
        self.assertEqual(len(line), 1, err)
        self.assertRegex(line[0], rf"^local: reaped phantom cell {first} \(pid \d+ gone; spend settled at \$10\.0000, upper estimate\)$")
        self.assertEqual(common.read_json(os.path.join(d, "spent.json")), {"usd": estimate})
        self.assertTrue(os.path.isfile(os.path.join(d, "live.json.reaped")))
        self.assertFalse(os.path.exists(os.path.join(d, "live.json")))
        self.assertEqual(set(self.results()), {second}, err)  # the second cell was admitted and finished
        self.assertEqual(self.events_lines("end "), [f"end {second} local"])
        self.assertAlmostEqual(costguard.estimate(self.run_dir), estimate + 0.5)  # the reaped cell is in the spend
        self.assertEqual(code, 1, err)  # a cell without result.json: "some cell failed", not a hang or a crash

    def test_reaped_cell_with_its_workspace_is_settled_at_the_spend_its_logs_show(self):
        proc = self.start(True)
        pid = self.wait_for(self.hold)
        ws = [os.path.join(self.run_dir, n) for n in os.listdir(self.run_dir) if n.startswith("ws-")][0]
        log = os.path.join(ws, ".kogen", "local", "runs", "r1")
        os.makedirs(log)
        with open(os.path.join(log, "log.jsonl"), "w") as f:
            f.write(json.dumps({"event": "request", "model": "openai/gpt-x",
                                "usage": {"input_tokens": 1000, "cached_input_tokens": 0, "output_tokens": 100}}) + "\n")
        known = costguard.workspace_spend(ws)
        os.kill(pid, signal.SIGKILL)
        _, err = proc.communicate(timeout=60)
        spent = [common.read_json(os.path.join(dp, "spent.json")) for dp, _, fs in os.walk(self.run_dir) if "spent.json" in fs]
        self.assertEqual(spent, [{"usd": round(known, 8)}])
        self.assertIn("reaped phantom cell", err)

    def test_live_json_of_a_reused_pid_is_reaped(self):
        d = os.path.join(self.run_dir, "cells", "task-mini", "r1", "base")
        os.makedirs(d)
        ws = os.path.join(self.tmp, "ws")
        os.makedirs(ws)
        info = live.record(ws, "h1")  # this very process: alive, but another start time was recorded
        common.write_json(os.path.join(d, "live.json"), dict(info, start="ticks:1"))
        lines = []
        self.assertEqual(costguard.reap_phantoms(self.run_dir, log=lines.append), ["task-mini/r1/base"])
        self.assertRegex(lines[0], rf"^h1: reaped phantom cell task-mini/r1/base \(pid {os.getpid()} reused by another process; ")
        self.assertTrue(os.path.isfile(os.path.join(d, "spent.json")))

    def test_running_cell_is_never_reaped(self):
        d = os.path.join(self.run_dir, "cells", "task-mini", "r1", "base")
        os.makedirs(d)
        ws = os.path.join(self.tmp, "ws")
        os.makedirs(ws)
        common.write_json(os.path.join(d, "live.json"), live.record(ws, "h1"))
        self.assertEqual(costguard.reap_phantoms(self.run_dir), [])
        self.assertEqual(sorted(os.listdir(d)), ["live.json"])
        # also a genuinely running fake cell, with the workspace gone: only its dead pid would make it a phantom
        proc = self.start(True)
        self.wait_for(self.hold)
        self.assertEqual(costguard.reap_phantoms(self.run_dir), [])
        proc.kill()
        os.kill(int(self.read(self.hold)), signal.SIGKILL)
        proc.communicate(timeout=30)

    def test_a_killed_process_nobody_has_waited_for_is_a_phantom(self):
        d = os.path.join(self.run_dir, "cells", "task-mini", "r1", "base")
        os.makedirs(d)
        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
        ws = os.path.join(self.tmp, "ws")
        os.makedirs(ws)
        info = {"workspace": ws, "pid": child.pid, "start": live.proc_start(child.pid), "node": None}
        common.write_json(os.path.join(d, "live.json"), info)
        self.assertEqual(costguard.reap_phantoms(self.run_dir), [])
        child.kill()
        end = time.time() + 10
        while time.time() < end and not live.zombie(child.pid):
            time.sleep(0.05)
        self.assertTrue(live.zombie(child.pid))  # dead, but its parent (this test) has not collected it
        self.assertEqual(costguard.reap_phantoms(self.run_dir, log=lambda m: None), ["task-mini/r1/base"])
        child.wait()

    def test_old_live_json_is_a_phantom_only_when_its_workspace_is_gone(self):
        d = os.path.join(self.run_dir, "cells", "task-mini", "r1", "base")
        os.makedirs(d)
        ws = os.path.join(self.tmp, "ws")
        os.makedirs(ws)
        common.write_json(os.path.join(d, "live.json"), {"workspace": ws})
        self.assertEqual(costguard.reap_phantoms(self.run_dir), [])
        os.rmdir(ws)
        lines = []
        self.assertEqual(costguard.reap_phantoms(self.run_dir, "h2", log=lines.append), ["task-mini/r1/base"])
        self.assertIn("h2: reaped phantom cell task-mini/r1/base (workspace gone; spend settled at $10.0000", lines[0])

    def test_cost_guard_reads_a_reaped_cell_instead_of_failing_closed(self):
        d = os.path.join(self.run_dir, "cells", "task-mini", "r1", "base")
        os.makedirs(d)
        common.write_json(os.path.join(d, "live.json"), {"workspace": os.path.join(self.tmp, "gone")})
        self.assertEqual(costguard.estimate(self.run_dir, retry_s=0.2), 10.0)  # no CostCapError
        self.assertEqual(costguard.estimate(self.run_dir, retry_s=0.2), 10.0)  # and not counted twice

    def test_estimate_is_the_run_mean_when_that_is_larger(self):
        for lane, usd in (("base", 30.0), ("patched", 20.0)):
            d = os.path.join(self.run_dir, "cells", "task-mini", "r1", lane)
            os.makedirs(d)
            common.write_json(os.path.join(d, "result.json"), {"totals": {"cost_usd": usd}})
        self.assertEqual(costguard.phantom_estimate(self.run_dir, None), 25.0)



if __name__ == "__main__":
    unittest.main()


class HostGate(unittest.TestCase):
    """The host gate counts live cells across every run dir, after reaping the phantoms and the leftovers of all of them."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.runs = os.path.join(self.tmp, "runs")
        self.capf = os.path.join(self.tmp, "host-cap")
        self.log = []
        nograde = mock.Mock(return_value=subprocess.CompletedProcess([], 0, stdout="", stderr=""))
        for p in (mock.patch.object(dispatch.subprocess, "run", nograde), mock.patch.object(dispatch.os, "cpu_count", return_value=4)):
            p.start()
            self.addCleanup(p.stop)

    def cell(self, run, name="base", info="running", result=False):
        d = os.path.join(self.runs, run, "cells", "task-mini", "r1", name)
        os.makedirs(d)
        ws = os.path.join(self.tmp, f"ws-{run}-{name}")
        os.makedirs(ws)
        if info == "running":
            info = live.record(ws, "h1")  # this process
        elif info == "dead":
            child = subprocess.Popen([sys.executable, "-c", "pass"])
            child.wait()
            info = {"workspace": ws, "pid": child.pid, "start": "ticks:1", "node": None}
        common.write_json(os.path.join(d, "live.json"), info)
        if result:
            common.write_json(os.path.join(d, "result.json"), {})
        return d

    def gate(self, text, load=0.5):
        with open(self.capf, "w") as f:
            f.write(text)
        with mock.patch.object(dispatch.os, "getloadavg", return_value=(load, 0, 0)):
            return dispatch.gate_admits(self.runs, self.capf, "local", self.log.append)

    def test_admits_below_the_cap_at_low_load_and_holds_otherwise(self):
        self.cell("run-a")
        self.cell("run-b")
        self.assertTrue(self.gate("3")[0])
        ok, live_n, *_ = self.gate("2")  # live 2 >= cap 2
        self.assertEqual((ok, live_n), (False, 2))
        self.assertFalse(self.gate("3", load=4.5)[0])  # load above 4 cpus x 1.0
        self.assertTrue(self.gate("3 1.5", load=4.5)[0])  # factor 1.5: limit 6
        self.assertFalse(self.gate("3 1.5", load=6.5)[0])
        self.assertTrue(self.gate("0", load=1)[0])  # cap 0: only the load counts
        self.assertEqual(self.log, [])  # nothing to reap

    def test_phantom_in_another_run_does_not_block_and_is_reaped(self):
        d = self.cell("run-other", info="dead")
        shutil.rmtree(os.path.join(self.tmp, "ws-run-other-base"))  # no logs left to read: the upper estimate
        self.cell("run-mine")
        ok, live_n, *_ = self.gate("2")
        self.assertEqual((ok, live_n), (True, 1))
        self.assertEqual(common.read_json(os.path.join(d, "spent.json")), {"usd": 10.0})
        self.assertTrue(os.path.isfile(os.path.join(d, "live.json.reaped")))
        self.assertFalse(os.path.exists(os.path.join(d, "live.json")))
        self.assertEqual(len(self.log), 1)
        self.assertRegex(self.log[0], r"^local: reaped phantom cell task-mini/r1/base \(pid \d+ gone; ")

    def test_leftover_live_json_of_a_finished_cell_is_moved_aside(self):
        d = self.cell("run-done", result=True)  # its pid is this live process, but the cell is over
        ok, live_n, *_ = self.gate("1")
        self.assertEqual((ok, live_n), (True, 0))
        self.assertTrue(os.path.isfile(os.path.join(d, "live.json.stale-finished")))
        self.assertFalse(os.path.exists(os.path.join(d, "live.json")))
        self.assertFalse(os.path.exists(os.path.join(d, "spent.json")))  # no spend change
        self.assertEqual(self.log, [])

    def test_a_running_cell_in_another_run_still_counts(self):
        d = self.cell("run-other")
        self.cell("run-mine")
        ok, live_n, *_ = self.gate("2")
        self.assertEqual((ok, live_n), (False, 2))
        self.assertEqual(sorted(os.listdir(d)), ["live.json"])  # not reaped
        self.assertEqual(self.log, [])

class HostGateAdmission(HostGate):
    """An admitted cell counts from admission, not from its live.json; a grade takes a place like a cell."""

    def token(self, **kw):
        return dispatch.Admission(self.capf, **kw)

    def test_admitted_cell_without_live_json_counts_then_hands_over_to_its_live_json(self):
        self.cell("run-a")
        tok = self.token(run_dir=os.path.join(self.runs, "run-b"))  # picked nothing yet: counts
        ok, live_n, *_ = self.gate("2")
        self.assertEqual((ok, live_n), (False, 2))
        tok.bind("task-mini/r1/base")  # picked its cell, no live.json yet: still counts
        self.assertEqual(self.gate("2")[:2], (False, 2))
        d = self.cell("run-b")  # live.json appears: counted once, by the cell
        self.assertEqual(self.gate("3")[:2], (True, 2))
        os.remove(os.path.join(d, "live.json"))  # finished: result.json, no live.json
        common.write_json(os.path.join(d, "result.json"), {})
        self.assertEqual(self.gate("2")[:2], (True, 1))
        tok.release()
        self.assertFalse(os.path.exists(tok.path))

    def test_tokens_of_dead_owners_and_old_tokens_are_dropped(self):
        child = subprocess.Popen([sys.executable, "-c", "pass"])
        child.wait()
        dead = self.token(pid=child.pid)
        old = self.token()
        old.rec["time"] = time.time() - dispatch.ADMIT_MAX_S - 5
        old._write()
        self.assertEqual(self.gate("1")[:2], (True, 0))
        self.assertFalse(os.path.exists(dead.path) or os.path.exists(old.path))

    def test_grade_token_and_a_lanes_grade_process_count_once(self):
        self.cell("run-a")
        tok = self.token(kind="grade")
        self.assertEqual(self.gate("4")[:2], (True, 2))
        dispatch.subprocess.run.return_value = subprocess.CompletedProcess([], 0, stdout="123\n", stderr="")  # its lanes-grade
        self.assertEqual(self.gate("4")[:2], (True, 2))
        dispatch.subprocess.run.return_value = subprocess.CompletedProcess([], 0, stdout="123\n456\n", stderr="")  # an ungated one too
        self.assertEqual(self.gate("4")[:2], (True, 3))
        tok.release()

    def test_wait_grade_waits_for_room_and_blocks_cells_meanwhile(self):
        self.cell("run-a")
        self.cell("run-b")
        with open(self.capf, "w") as f:
            f.write("2")
        got = []
        with mock.patch.object(dispatch.os, "getloadavg", return_value=(0.5, 0, 0)):
            self.assertIsNone(dispatch.wait_grade(self.runs, self.capf, "local", self.log.append, poll=0.05, max_wait=0.2))
            self.assertEqual(os.listdir(os.path.join(self.tmp, dispatch.ADMIT_DIR)), [])  # gave its place up
            import threading
            t = threading.Thread(target=lambda: got.append(dispatch.wait_grade(self.runs, self.capf, "local", self.log.append, poll=0.05)))
            t.start()
            time.sleep(0.3)  # waiting: its token already holds a place, so a cell is not admitted into it
            self.assertEqual(os.listdir(os.path.join(self.tmp, dispatch.ADMIT_DIR)) != [], True)
            os.remove(os.path.join(self.runs, "run-a", "cells", "task-mini", "r1", "base", "live.json"))
            t.join(5)
            self.assertFalse(t.is_alive())
        self.assertEqual(len(got), 1)
        self.assertIsNotNone(got[0])
        self.assertEqual(self.gate("2")[:2], (False, 2))  # one cell + the grade
        got[0].release()
        self.assertEqual([l for l in self.log if "holding the grade" in l][:1] != [], True)

    def test_bind_refreshes_a_token_that_aged_while_its_runner_was_stopped(self):
        tok = self.token(run_dir=os.path.join(self.runs, "run-b"))
        tok.rec["time"] = time.time() - dispatch.ADMIT_MAX_S + 1  # about to expire
        tok._write()
        tok.rec["time"] = time.time() - dispatch.ADMIT_MAX_S - 100  # the runner slept past it, then wakes and binds
        tok.bind("task-mini/r1/base")
        self.assertEqual(self.gate("2")[:2], (True, 1))  # counted, not dropped as old

    def test_no_host_cap_file_no_grade_wait(self):
        tok = dispatch.wait_grade(self.runs, self.capf, "local", self.log.append, poll=0.05, max_wait=0.1)
        self.assertIsNotNone(tok)
        tok.release()


class HostGateRace(unittest.TestCase):
    """Four slots, host cap 2, cells whose workspace copy takes longer than the settle: never more than 2 at work."""

    setUp, write_lock, set_exp, plan, events_lines, read, results = (
        test_dispatch.Dispatch.setUp, test_dispatch.Dispatch.write_lock, test_dispatch.Dispatch.set_exp, test_dispatch.Dispatch.plan, test_dispatch.Dispatch.events_lines,
        test_dispatch.Dispatch.read, test_dispatch.Dispatch.results)

    def spans(self, path):
        starts, ends = {}, {}
        for line in open(path).read().splitlines():
            k, cell, t = line.split()
            (starts if k == "s" else ends)[cell] = float(t)
        pts = sorted([(t, 1) for t in starts.values()] + [(t, -1) for t in ends.values()])
        cur = peak = 0
        for _, d in pts:
            cur += d
            peak = max(peak, cur)
        return peak, len(starts)

    def run_capped(self, cap):
        root = os.path.join(self.tmp, "root")
        self.run_dir = os.path.join(root, "runs", "run1")
        with open(os.path.join(root, "host-cap") if os.makedirs(root) is None else "", "w") as f:
            f.write(f"{cap} 1000")
        common.write_json(self.hosts, {"local": {"target": "local", "slots": 4}})
        self.set_exp(reps=2)
        self.assertEqual(self.plan().returncode, 0)
        span = os.path.join(self.tmp, "span.txt")
        env = dict(self.env, FAKE_LIVE=REAL_LANES, FAKE_PREP="1.2", FAKE_SLEEP="0.6", FAKE_SPAN=span)
        with mock.patch.dict(os.environ, env), mock.patch.object(dispatch, "ADMIT_SETTLE_S", 0.0):
            code = dispatch.run_all(self.run_dir, self.tasks, self.hosts, lanes_dir=FAKE_LANES, skip_preflight=True, log=lambda m: None)
        self.assertEqual(code, 0)
        return self.spans(span)

    def test_admitted_cells_never_exceed_the_cap_while_they_prepare(self):
        peak, n = self.run_capped(2)
        self.assertEqual(n, 4)
        self.assertLessEqual(peak, 2)
        self.assertEqual(os.listdir(os.path.join(self.tmp, "root", dispatch.ADMIT_DIR)), [])  # every token released
