import json
import os
import signal
import subprocess
import sys
import time
import unittest

from lanes import common, costguard, live
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
