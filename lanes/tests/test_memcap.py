import json
import os
import subprocess
import sys
import time
import unittest

from lanes import common, dispatch, memcap, report

from tests import test_dispatch

OWN = memcap.own_cgroup()
DELEGATED = bool(OWN and memcap.delegated(OWN))
CAP = os.environ.get("MEMCAP_TEST_CAP", "100M")

PS = """  1     0   100
  2     1  2000
  3     2  3000
  4     3    10
  5     1  7000
  9     8  5000
"""


class Parsing(unittest.TestCase):
    def test_sizes(self):
        self.assertEqual(memcap.parse_size("4G"), 4 << 30)
        self.assertEqual(memcap.parse_size("512M"), 512 << 20)
        self.assertEqual(memcap.parse_size("1024K"), 1 << 20)
        self.assertEqual(memcap.parse_size("2T"), 2 << 40)
        self.assertEqual(memcap.parse_size("65536"), 65536)
        for bad in ("", "0", "0G", "-1G", "4g", "4GB", "1.5G", "G", " ", None, 4, True):
            with self.assertRaises(ValueError, msg=repr(bad)):
                memcap.parse_size(bad)

    def test_rss_sums_the_descendants_only(self):
        table = memcap.parse_ps(PS)
        self.assertEqual(memcap.tree(2, table), {2, 3, 4})
        self.assertEqual(memcap.tree_rss(2, table), (2000 + 3000 + 10) * 1024)
        self.assertEqual(memcap.tree_rss(1, table), (100 + 2000 + 3000 + 10 + 7000) * 1024)
        self.assertEqual(memcap.tree_rss(4, table), 10 * 1024)
        self.assertEqual(memcap.tree_rss(42, table), 0)  # gone
        self.assertEqual(memcap.tree_rss(9, table), 5000 * 1024)  # its parent is not in the table

    def test_ps_lines_that_are_not_numbers_are_skipped(self):
        self.assertEqual(memcap.parse_ps("1 0 5\nbad line here\n2 1\n"), {1: (0, 5)})

    def test_the_real_ps_sees_this_process(self):
        table = memcap.ps_table()
        self.assertIn(os.getpid(), table)
        self.assertGreater(memcap.tree_rss(os.getpid(), table), 0)

    def test_hosts_file(self):
        tmp = test_dispatch.tempfile.mkdtemp()
        self.addCleanup(test_dispatch.shutil.rmtree, tmp)
        path = os.path.join(tmp, "hosts.json")

        def load(**host):
            common.write_json(path, {"h": {"target": "local", **host}})
            return dispatch.load_hosts(path, ["h"])["h"]

        self.assertNotIn("cell_memory_max", load())
        self.assertEqual(load(cell_memory_max="4G")["cell_memory_max"], "4G")
        for bad in ("lots", "", 4, "0", None):
            with self.assertRaisesRegex(dispatch.DispatchError, "cell_memory_max"):
                load(cell_memory_max=bad)
        common.write_json(path, {"h": {"target": "far", "root": "/x", "cell_memory_max": "4G"}})
        with self.assertRaisesRegex(dispatch.DispatchError, "local hosts only"):
            dispatch.load_hosts(path, ["h"])

    def test_report_classes_it_as_plumbing_not_a_model_failure(self):
        result = {"outcome": "memory_cap"}
        self.assertEqual(report.classify(result, [], None, "build"), "incomplete")
        self.assertEqual(report.plumbing({"result": result, "class": "incomplete", "log": []}), "memory_cap")


HOG = ("import os,time\nkeep=[]\n"
       "for i in range(40):\n keep.append(bytearray(b'x'*(10<<20)))\n time.sleep(0.25)\ntime.sleep(30)\n")


class Watchdog(unittest.TestCase):
    def test_kills_a_process_tree_over_the_cap(self):
        parent = subprocess.Popen([sys.executable, "-c", f"import subprocess,sys;subprocess.run([sys.executable,'-c',{HOG!r}])"],
                                  start_new_session=True)
        self.addCleanup(lambda: (common._killpg(parent.pid, 9), parent.wait()))
        dog = memcap.Watchdog(parent.pid, 60 << 20, sample_s=0.3, grace_s=1).start()
        t0 = time.monotonic()
        parent.wait(timeout=20)
        dog.stop()
        self.assertLess(time.monotonic() - t0, 15)
        self.assertGreater(dog.hit["peak_rss"], 60 << 20)
        self.assertEqual(dog.hit["cap"], 60 << 20)

    def test_leaves_a_small_process_alone(self):
        p = subprocess.Popen([sys.executable, "-c", "import time;time.sleep(1.5)"], start_new_session=True)
        dog = memcap.Watchdog(p.pid, 1 << 30, sample_s=0.2, grace_s=1).start()
        self.assertEqual(p.wait(timeout=10), 0)
        dog.stop()
        self.assertIsNone(dog.hit)


class FaultTest(unittest.TestCase):
    """Two cells at once; one's child allocates past the cap and is killed and marked, the other finishes."""
    setUp = test_dispatch.Dispatch.setUp
    write_lock = test_dispatch.Dispatch.write_lock
    plan = test_dispatch.Dispatch.plan
    read = test_dispatch.Dispatch.read

    def fault(self):
        self.assertEqual(self.plan().returncode, 0)
        cells = [c["cell"] for c in common.read_jsonl(os.path.join(self.run_dir, "plan.jsonl"))]
        hog = cells[0]
        common.write_json(self.hosts, {"local": {"target": "local", "slots": 2, "cell_memory_max": CAP}})
        env = {"FAKE_HOG": hog, "FAKE_SLEEP": "4", "FAKE_EVENTS": self.events, "KOGEN_LANES_HOME": self.home,
               "FAKE_HOG_MAX_MB": str(memcap.parse_size(CAP) * 3 // 2 >> 20),
               "FAKE_HOG_STEP_MB": "10", "FAKE_HOG_HOLD": "30"}  # the hog stops at 1.5 times the cap
        logs = []
        old = {k: os.environ.get(k) for k in env}
        os.environ.update(env)
        self.addCleanup(lambda: [os.environ.pop(k) if v is None else os.environ.__setitem__(k, v) for k, v in old.items()])
        t0 = time.monotonic()
        code = dispatch.run_all(self.run_dir, self.tasks, self.hosts, lanes_dir=test_dispatch.FAKE_LANES,
                                skip_preflight=True, log=logs.append)
        self.assertLess(time.monotonic() - t0, 120)
        self.assertEqual(code, 0, logs)
        hogged = common.cell_dir(self.run_dir, hog)
        record = common.read_json(os.path.join(hogged, "memory-cap.json"))
        result = common.read_json(os.path.join(hogged, "result.json"))
        self.assertEqual(result["outcome"], "memory_cap")
        self.assertEqual(record["cap"], memcap.parse_size(CAP))
        self.assertGreaterEqual(record["peak_rss"], record["cap"] if record["mechanism"] == "watchdog" else 1)
        self.assertLess(record["peak_rss"], 1500 << 20)
        self.assertEqual(report.classify(result, [], None, "build"), "incomplete")
        for cell in cells[1:]:  # the neighbours and the later cells all finished, none was marked
            d = common.cell_dir(self.run_dir, cell)
            self.assertEqual(common.read_json(os.path.join(d, "result.json"))["cell"], cell)
            self.assertFalse(os.path.exists(os.path.join(d, "memory-cap.json")), cell)
        self.assertTrue(any("memory cap" in m and record["mechanism"] in m for m in logs), logs)
        if os.environ.get("MEMCAP_TEST_SHOW"):  # a transcript for the curious
            print("\n".join(logs), "\n" + json.dumps(record), "\nresult:", result["outcome"], flush=True)
        return record, logs

    @unittest.skipIf(DELEGATED, "the cgroup test covers a delegated cgroup")
    def test_watchdog(self):
        record, logs = self.fault()
        self.assertEqual(record["mechanism"], "watchdog")

    @unittest.skipUnless(DELEGATED, "needs a delegated cgroup v2 (systemd-run -p Delegate=yes)")
    def test_cgroup(self):
        record, logs = self.fault()
        self.assertEqual(record["mechanism"], "cgroup v2")


if __name__ == "__main__":
    unittest.main()
