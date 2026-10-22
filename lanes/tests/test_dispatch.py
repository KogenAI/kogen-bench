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

from lanes import common, dispatch

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
BIN = os.path.join(os.path.dirname(FIX), "..", "bin")
FAKE_LANES = os.path.join(FIX, "fake-lanes")
ART = "ab" * 32


def entry(name):
    return os.path.join(BIN, name)


class Dispatch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.home = os.path.join(self.tmp, "home")
        os.makedirs(os.path.join(self.home, "artifacts", ART))
        with open(os.path.join(self.home, "artifacts", ART, "kogen"), "w") as f:
            f.write("bin")
        self.tasks = os.path.join(self.tmp, "tasks")
        shutil.copytree(os.path.join(FIX, "task-mini"), os.path.join(self.tasks, "task-mini"))
        exp = common.read_json(os.path.join(FIX, "experiment-good.json"))
        exp["reps"] = 2
        self.exp_path = os.path.join(self.tmp, "experiment.json")
        common.write_json(self.exp_path, exp)
        os.makedirs(os.path.join(self.tmp, "patches"))
        with open(os.path.join(self.tmp, "patches", "p1.patch"), "w") as f:
            f.write("--- a\n+++ b\n")
        self.run_dir = os.path.join(self.tmp, "run")
        self.events = os.path.join(self.tmp, "events.txt")
        self.hosts = os.path.join(self.tmp, "hosts.json")
        common.write_json(self.hosts, {"local": {"target": "local", "slots": 2}})
        self.env = dict(os.environ, KOGEN_LANES_HOME=self.home, FAKE_EVENTS=self.events)
        self.env.pop("KOGEN_LANES_TASKS", None)

    def write_lock(self):
        os.makedirs(self.run_dir, exist_ok=True)
        common.write_json(os.path.join(self.run_dir, "lanes.lock.json"),
                          [{"name": n, "sha": "0" * 40, "patch_sha256": None, "artifact_sha256": ART,
                            "kogen_version": "v"} for n in ("base", "patched")])

    def set_exp(self, **fields):
        exp = common.read_json(self.exp_path)
        exp.update(fields)
        common.write_json(self.exp_path, exp)

    def plan(self, lock=True):
        if lock:
            self.write_lock()
        p = subprocess.run([sys.executable, entry("lanes-plan"), self.exp_path, "--run-dir", self.run_dir,
                            "--tasks", self.tasks], env=self.env, capture_output=True, text=True)
        return p

    def run_cmd(self, *extra, env=None, timeout=60):
        return subprocess.run([sys.executable, entry("lanes-run"), self.run_dir, "--tasks", self.tasks,
                               "--hosts", self.hosts, "--lanes-dir", FAKE_LANES, "--skip-preflight", *extra],
                              env=env or self.env, capture_output=True, text=True, timeout=timeout)

    def events_lines(self, prefix="cell "):
        if not os.path.exists(self.events):
            return []
        with open(self.events) as f:
            return [e for e in f.read().split("\n")[:-1] if e.startswith(prefix)]

    def read(self, path):
        with open(path) as f:
            return f.read()

    def results(self):
        out = {}
        for c in common.read_jsonl(os.path.join(self.run_dir, "plan.jsonl")):
            path = os.path.join(common.cell_dir(self.run_dir, c["cell"]), "result.json")
            if os.path.isfile(path):
                out[c["cell"]] = common.read_json(path)
        return out

    # ---- plan

    def test_rotation_is_balanced_and_deterministic(self):
        exp = {"id": "e1", "tasks": ["a", "b", "c"], "reps": 2,
               "lanes": [{"name": n} for n in ("x", "y", "z")]}
        cells = dispatch.make_plan(exp)
        self.assertEqual(cells, dispatch.make_plan(exp))
        self.assertEqual(len(cells), 18)
        firsts = [c["lane"] for c in cells if c["order"] == 0]
        self.assertEqual({firsts.count(n) for n in "xyz"}, {2})
        self.assertEqual(cells[0]["cell"], f"a/r1/{cells[0]['lane']}")
        self.assertNotEqual(cells, dispatch.make_plan(dict(exp, id="other-id-2")))

    def test_plan_refuses_without_lock(self):  # B2: lanes-build comes first
        p = self.plan(lock=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("run lanes-build first", p.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "PLAN.json")))
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "plan.jsonl")))
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "experiment.json")))  # L9: nothing written

    def test_run_refuses_plan_without_lock_hash_or_with_changed_lock(self):  # B2
        self.plan()
        plan_path = os.path.join(self.run_dir, "PLAN.json")
        good = common.read_json(plan_path)
        common.write_json(plan_path, dict(good, lock={"sha256": None, "artifacts": {}}))
        p = self.run_cmd()
        self.assertEqual((p.returncode, self.events_lines()), (2, []))
        self.assertIn("no lock hash", p.stderr)
        common.write_json(plan_path, good)
        lock = os.path.join(self.run_dir, "lanes.lock.json")
        data = common.read_json(lock)
        data[0]["kogen_version"] = "other"
        common.write_json(lock, data)
        p = self.run_cmd()
        self.assertEqual((p.returncode, self.events_lines()), (2, []))
        self.assertIn("lanes.lock.json no longer matches", p.stderr)

    def test_run_refuses_changed_experiment(self):  # m9
        self.plan()
        path = os.path.join(self.run_dir, "experiment.json")
        exp = common.read_json(path)
        exp["reps"] = 1
        common.write_json(path, exp)
        p = self.run_cmd()
        self.assertEqual((p.returncode, self.events_lines()), (2, []))
        self.assertIn("experiment.json no longer matches", p.stderr)

    def test_plan_files(self):
        self.plan()
        self.assertTrue(os.path.isfile(os.path.join(self.run_dir, "experiment.json")))
        cells = common.read_jsonl(os.path.join(self.run_dir, "plan.jsonl"))
        self.assertEqual(len(cells), 4)
        self.assertEqual(sorted(c["cell"] for c in cells),
                         sorted(f"task-mini/r{r}/{n}" for r in (1, 2) for n in ("base", "patched")))
        plan = common.read_json(os.path.join(self.run_dir, "PLAN.json"))
        self.assertIn("task-mini", plan["hashes"]["tasks"])
        self.assertNotIn("hosts", plan["experiment"])
        self.assertEqual(plan["lock"]["sha256"], common.sha256_file(os.path.join(self.run_dir, "lanes.lock.json")))
        self.assertEqual(plan["lock"]["artifacts"], {"base": ART, "patched": ART})

    # ---- run

    def test_run_resume_and_verify(self):
        self.plan()
        p = self.run_cmd()
        self.assertEqual(p.returncode, 0, p.stderr)
        res = self.results()
        self.assertEqual(len(res), 4)
        self.assertTrue(all(r["host"] == "local" and r["start"] for r in res.values()))
        self.assertEqual(len(self.events_lines()), 4)
        self.assertEqual(os.listdir(os.path.join(self.run_dir, "claims")), [])
        self.assertEqual(self.run_cmd().returncode, 0)  # resume: nothing left to run
        self.assertEqual(len(self.events_lines()), 4)
        # a changed hidden test makes the PLAN.json hashes stale
        os.remove(os.path.join(self.run_dir, "cells", "task-mini", "r1", "base", "result.json"))
        with open(os.path.join(self.tasks, "task-mini", "evaluator", "files", "extra.go"), "w") as f:
            f.write("package x\n")
        p = self.run_cmd()
        self.assertEqual(p.returncode, 2)
        self.assertIn("no longer matches", p.stderr)
        self.assertEqual(len(self.events_lines()), 4)

    def test_failed_cell_is_reported_not_retried(self):
        self.plan()
        env = dict(self.env, FAKE_FAIL="task-mini/r1/base")
        p = self.run_cmd(env=env)
        self.assertEqual(p.returncode, 1)
        self.assertEqual(len(self.results()), 3)
        self.assertEqual(sum("task-mini/r1/base" in e for e in self.events_lines()), 1)
        self.assertEqual(os.listdir(os.path.join(self.run_dir, "claims")), [])

    # ---- claims

    def test_claims_atomic_and_stale(self):
        os.makedirs(self.run_dir)
        claims = dispatch.Claims(self.run_dir, stale_s=3600)
        self.assertTrue(claims.take("t/r1/a", "h1"))
        self.assertFalse(claims.take("t/r1/a", "h2"))  # live: this process, fresh
        info = common.read_json(claims.path("t/r1/a"))
        self.assertEqual((info["host"], info["pid"]), ("h1", os.getpid()))
        # owner process gone
        dead = subprocess.Popen([sys.executable, "-c", "pass"])
        dead.wait()
        common.write_json(claims.path("t/r1/a"), {"host": "h1", "pid": dead.pid, "time": time.time()})
        self.assertTrue(claims.take("t/r1/a", "h2"))
        # owner alive but older than the deadline plus margin
        common.write_json(claims.path("t/r1/a"), {"host": "h1", "pid": os.getpid(), "time": time.time() - 7200})
        self.assertTrue(claims.take("t/r1/a", "h2"))
        claims.release("t/r1/a")
        claims.release("t/r1/a")
        self.assertEqual(os.listdir(claims.dir), [])

    def test_run_skips_live_claim_and_takes_stale_one(self):
        self.plan()
        claims = dispatch.Claims(self.run_dir, stale_s=3600)
        dead = subprocess.Popen([sys.executable, "-c", "pass"])
        dead.wait()
        common.write_json(claims.path("task-mini/r1/base"), {"host": "x", "pid": dead.pid, "time": time.time()})
        common.write_json(claims.path("task-mini/r2/base"), {"host": "x", "pid": os.getpid(), "time": time.time()})
        self.assertEqual(self.run_cmd().returncode, 0)
        self.assertEqual(set(self.results()), {"task-mini/r1/base", "task-mini/r1/patched", "task-mini/r2/patched"})

    # ---- lock command

    def test_lock_and_unlock_commands(self):
        self.plan()
        log = os.path.join(self.tmp, "lock.txt")
        p = self.run_cmd("--lock-cmd", f"echo lock {{host}} {{name}} >> {log}",
                         "--unlock-cmd", f"echo unlock {{host}} {{name}} >> {log}")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(self.read(log).split("\n")[:-1], ["lock local exp-mini", "unlock local exp-mini"])
        self.assertEqual(len(self.results()), 4)

    def test_lock_failure_refuses_to_start(self):
        self.plan()
        p = self.run_cmd("--lock-cmd", "exit 7")
        self.assertEqual(p.returncode, 2)
        self.assertIn("lock command failed for local", p.stderr)
        self.assertEqual(self.events_lines(), [])
        self.assertEqual(self.results(), {})

    # ---- remote through a fake ssh

    @unittest.skipUnless(shutil.which("rsync"), "rsync not installed")
    def test_remote_host(self):
        self.plan()
        root = os.path.join(self.tmp, "remote-root")
        common.write_json(self.hosts, {"local": {"target": "local"},
                                       "far": {"target": "far.invalid", "slots": 2, "root": root}})
        exp = common.read_json(self.exp_path)
        exp["hosts"] = ["far"]
        common.write_json(os.path.join(self.run_dir, "experiment.json"), exp)
        env = dict(self.env, LANES_SSH=os.path.join(FIX, "fake-ssh"))
        p = self.run_cmd(env=env)
        self.assertEqual(p.returncode, 0, p.stderr)
        res = self.results()
        self.assertEqual(len(res), 4)
        for r in res.values():
            self.assertEqual((r["host"], r["start"], r["evaluator"], r["artifact"]), ("far", True, False, True))
        self.assertFalse(os.path.exists(os.path.join(root, "tasks", "task-mini", "evaluator")))
        self.assertTrue(os.path.isfile(os.path.join(root, "lanes", "bin", "lanes-cell")))
        self.assertFalse(os.path.exists(os.path.join(root, "runs", "exp-mini", "cells", "task-mini", "r1", "base")))
        self.assertEqual(self.run_cmd(env=env).returncode, 0)
        self.assertEqual(len(self.events_lines()), 4)

    def remote_setup(self):
        self.plan()
        root = os.path.join(self.tmp, "remote-root")
        common.write_json(self.hosts, {"far": {"target": "far.invalid", "slots": 2, "root": root}})
        exp = common.read_json(os.path.join(self.run_dir, "experiment.json"))
        exp["hosts"] = ["far"]
        common.write_json(os.path.join(self.run_dir, "experiment.json"), exp)  # hosts are not in the PLAN
        return dict(self.env, LANES_SSH=os.path.join(FIX, "fake-ssh")), root

    def alive(self, pids):
        out = []
        for pid in pids:
            try:
                os.kill(pid, 0)
                out.append(pid)
            except ProcessLookupError:
                pass
        return out

    @unittest.skipUnless(shutil.which("rsync"), "rsync not installed")
    def test_remote_interrupt_kills_remote_groups(self):  # B1
        env, root = self.remote_setup()
        pids = os.path.join(self.tmp, "pids.txt")
        env.update(FAKE_SLEEP="30", FAKE_PIDS=pids)
        proc = subprocess.Popen([sys.executable, entry("lanes-run"), self.run_dir, "--tasks", self.tasks,
                                 "--hosts", self.hosts, "--lanes-dir", FAKE_LANES, "--skip-preflight"], env=env,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.addCleanup(proc.kill)
        end = time.time() + 30
        while time.time() < end and len(self.read(pids).split() if os.path.exists(pids) else []) < 2:
            time.sleep(0.1)
        started = [int(x) for x in self.read(pids).split()]
        self.assertEqual(len(started), 2)
        proc.send_signal(signal.SIGINT)
        self.assertEqual(proc.wait(timeout=30), 130)
        self.assertEqual(self.alive(started), [])
        self.assertEqual(os.listdir(os.path.join(self.run_dir, "claims")), [])
        self.assertEqual(self.results(), {})
        left = [f for f in os.listdir(os.path.join(root, "runs", "exp-mini")) if f.startswith("pgid-")]
        self.assertEqual(left, [])

    @unittest.skipUnless(shutil.which("rsync"), "rsync not installed")
    def test_remote_deadline_kills_remote_group(self):  # B1, deadline path
        self.set_exp(deadline_s=0.5)
        env, root = self.remote_setup()
        pids = os.path.join(self.tmp, "pids.txt")
        env.update(FAKE_SLEEP="30", FAKE_PIDS=pids)
        with mock.patch.dict(os.environ, env), mock.patch.object(dispatch, "MARGIN_S", 3):
            self.assertEqual(dispatch.run_all(self.run_dir, self.tasks, self.hosts, lanes_dir=FAKE_LANES, skip_preflight=True,
                                              log=lambda m: None), 1)
        started = [int(x) for x in self.read(pids).split()]
        self.assertEqual(self.alive(started), [])
        self.assertEqual(self.results(), {})

    @unittest.skipUnless(shutil.which("rsync"), "rsync not installed")
    def test_remote_ssh_255_kills_remote_group_before_cleanup(self):  # L9: lost connection, cell still running
        env, root = self.remote_setup()
        pids = os.path.join(self.tmp, "pids.txt")
        ssh = os.path.join(self.tmp, "ssh-drop")
        with open(ssh, "w") as f:  # run the command detached, wait for the cell to start, then drop like ssh
            f.write('#!/bin/sh\nshift\ncase "$*" in *lanes-cell*) ;; *) exec sh -c "$*";; esac\n'
                    'sh -c "$*" >/dev/null 2>&1 &\n'
                    'for i in $(seq 1 100); do test -s "$FAKE_PIDS" && break; sleep 0.1; done\n'
                    'exit 255\n')
        os.chmod(ssh, 0o755)
        env.update(FAKE_SLEEP="30", FAKE_PIDS=pids, LANES_SSH=ssh)
        with mock.patch.dict(os.environ, env):
            self.assertEqual(dispatch.run_all(self.run_dir, self.tasks, self.hosts, lanes_dir=FAKE_LANES, skip_preflight=True,
                                              log=lambda m: None), 1)
        started = [int(x) for x in self.read(pids).split()]
        self.assertTrue(started)
        self.assertEqual(self.alive(started), [])
        self.assertEqual(self.results(), {})

    @unittest.skipUnless(shutil.which("rsync"), "rsync not installed")
    def test_remote_255_without_pgid_leaves_the_dir(self):  # L9 m1: no pgid, no rm -rf
        env, root = self.remote_setup()
        ssh = os.path.join(self.tmp, "ssh-drop")
        with open(ssh, "w") as f:  # the cell never starts, so no pgid file exists
            f.write('#!/bin/sh\nshift\ncase "$*" in *lanes-cell*) exit 255;; esac\nexec sh -c "$*"\n')
        os.chmod(ssh, 0o755)
        keep = []
        for rep in ("r1", "r2"):
            for lane in ("base", "patched"):
                d = os.path.join(root, "runs", "exp-mini", "cells", "task-mini", rep, lane)
                os.makedirs(d)
                keep.append(os.path.join(d, "keep"))
                open(keep[-1], "w").close()
        env.update(LANES_SSH=ssh)
        with mock.patch.dict(os.environ, env):
            dispatch.run_all(self.run_dir, self.tasks, self.hosts, lanes_dir=FAKE_LANES, skip_preflight=True, log=lambda m: None)
        self.assertTrue(any(os.path.exists(k) for k in keep))

    @unittest.skipUnless(shutil.which("rsync"), "rsync not installed")
    def test_remote_failed_copy_back_is_not_a_result(self):  # m8
        env, root = self.remote_setup()
        real = dispatch.Host.rsync

        def flaky(host, src, dst, *opts):
            if src.endswith("/") and "--exclude" in opts and "/result.json" in opts and ":" in src:
                return 23, "partial transfer"
            return real(host, src, dst, *opts)

        with mock.patch.dict(os.environ, env), mock.patch.object(dispatch.Host, "rsync", flaky):
            self.assertEqual(dispatch.run_all(self.run_dir, self.tasks, self.hosts, lanes_dir=FAKE_LANES, skip_preflight=True,
                                              log=lambda m: None), 1)
        self.assertEqual(self.results(), {})

    def test_ssh_and_rsync_have_deadlines(self):  # m1
        slow = os.path.join(self.tmp, "slow-ssh")
        with open(slow, "w") as f:
            f.write("#!/bin/sh\nsleep 30\n")
        os.chmod(slow, 0o755)
        ctx = dispatch.Context(self.run_dir, self.tasks, FAKE_LANES, dispatch.Runner(), {"id": "e"})
        with mock.patch.dict(os.environ, {"LANES_SSH": slow}), mock.patch.object(dispatch, "MARGIN_S", 0.3):
            host = dispatch.Host("far", {"target": "t", "slots": 1, "root": "/x"}, ctx)
            t0 = time.time()
            self.assertEqual(host.sh("true")[0], 124)
            self.assertEqual(host.rsync("a/", "t:b/")[0], 124)
            self.assertLess(time.time() - t0, 10)
        with mock.patch.dict(os.environ):
            os.environ.pop("LANES_SSH", None)
            default = dispatch.Host("far", {"target": "t", "slots": 1, "root": "/x"}, ctx).ssh
        self.assertIn("BatchMode=yes", default)
        self.assertTrue(any(a.startswith("ConnectTimeout=") for a in default))

    def test_sibling_slot_does_not_rerun_a_running_cell(self):  # m2
        self.plan()
        env = dict(self.env, FAKE_SLEEP="1.0")
        real = dispatch.Claims  # claims count as stale after 0.3 s, while each cell takes 1 s

        def quick(run_dir, stale_s):
            return real(run_dir, 0.3)

        with mock.patch.dict(os.environ, env), mock.patch.object(dispatch, "Claims", quick):
            self.assertEqual(dispatch.run_all(self.run_dir, self.tasks, self.hosts, lanes_dir=FAKE_LANES, skip_preflight=True,
                                              log=lambda m: None), 0)
        starts = self.events_lines()
        self.assertEqual(len(starts), 4)
        self.assertEqual(len(set(starts)), 4)

    def test_claim_replaced_between_check_and_rename_is_kept(self):  # m3
        os.makedirs(self.run_dir)
        claims = dispatch.Claims(self.run_dir, stale_s=3600)
        dead = subprocess.Popen([sys.executable, "-c", "pass"])
        dead.wait()
        common.write_json(claims.path("t/r1/a"), {"host": "old", "pid": dead.pid, "time": time.time()})
        real, calls = claims._stale, []

        def racy(path):
            calls.append(path)
            if len(calls) == 1:  # the first controller sees a stale claim, then a rival replaces it
                verdict = real(path)
                os.unlink(path)
                common.write_json(path, {"host": "rival", "pid": os.getpid(), "time": time.time()})
                return verdict
            return real(path)

        claims._stale = racy
        self.assertFalse(claims.take("t/r1/a", "me"))
        self.assertEqual(common.read_json(claims.path("t/r1/a"))["host"], "rival")
        self.assertEqual(os.listdir(claims.dir), ["t__r1__a.json"])

    def test_host_unlocked_when_its_own_cells_are_done(self):  # m4
        self.set_exp(hosts=["a", "b"])
        self.plan()
        common.write_json(self.hosts, {"a": {"target": "local"}, "b": {"target": "local"}})
        env = dict(self.env, FAKE_SLEEP_b="2")
        p = self.run_cmd("--unlock-cmd", f"echo unlock {{host}} >> {self.events}", env=env)
        self.assertEqual(p.returncode, 0, p.stderr)
        lines = self.events_lines("")
        ends_b = [i for i, e in enumerate(lines) if e.startswith("end ") and e.endswith(" b")]
        self.assertTrue(ends_b)
        self.assertLess(lines.index("unlock a"), ends_b[-1])
        self.assertLess(ends_b[-1], lines.index("unlock b"))

    # ---- interrupt

    def test_interrupt_kills_own_groups_and_releases_claims(self):
        self.plan()
        pids = os.path.join(self.tmp, "pids.txt")
        env = dict(self.env, FAKE_SLEEP="30", FAKE_PIDS=pids)
        proc = subprocess.Popen([sys.executable, entry("lanes-run"), self.run_dir, "--tasks", self.tasks,
                                 "--hosts", self.hosts, "--lanes-dir", FAKE_LANES, "--skip-preflight"], env=env,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        end = time.time() + 20
        while time.time() < end and len(self.read(pids).split() if os.path.exists(pids) else []) < 2:
            time.sleep(0.1)
        started = [int(x) for x in self.read(pids).split()]
        self.assertEqual(len(started), 2)
        proc.send_signal(signal.SIGINT)
        self.assertEqual(proc.wait(timeout=20), 130)
        for pid in started:
            with self.assertRaises(ProcessLookupError):
                os.kill(pid, 0)
        self.assertEqual(os.listdir(os.path.join(self.run_dir, "claims")), [])
        self.assertEqual(self.results(), {})


if __name__ == "__main__":
    unittest.main()
