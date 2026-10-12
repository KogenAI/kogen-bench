#!/usr/bin/env python3
"""Unit checks for runner orchestration; the fake is deliberately not a witness."""
import json
import os
from pathlib import Path
import shlex
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
from runner_core import FixtureBase, cleanup_processes, eventually, marked_processes, process_rows

HERE = Path(__file__).resolve().parent

def localhost_bind_available():
    try:
        with socket.socket() as sock:
            sock.bind(("[IP omitted]", 0))
        return True
    except OSError:
        return False

NETWORK_AVAILABLE = localhost_bind_available()


class CoreTests(unittest.TestCase):
    def setUp(self):
        (HERE / ".tmp").mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="archh-unit-", dir=HERE / ".tmp")
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    @unittest.skipUnless(NETWORK_AVAILABLE, "localhost bind unavailable in this sandbox")
    def test_fixture_patch_and_marker_gate(self):
        fixture = FixtureBase("/usr/bin/true", self.root)
        repo, base = fixture.repository(bare=False)
        patch = fixture.patch("unit")
        fixture.git(repo, "apply", patch)
        self.assertEqual((repo / "unit.txt").read_text(), "unit\n")
        self.assertEqual(fixture.git(repo, "rev-parse", "HEAD"), base)
        command = fixture.marker("entered") + "; " + fixture.gate("release")
        child = subprocess.Popen(["/bin/sh", "-c", command])
        try:
            fixture.await_file("entered")
            self.assertIsNone(child.poll())
            fixture.release("release")
            self.assertEqual(child.wait(timeout=5), 0)
        finally:
            if child.poll() is None:
                child.kill()
                child.wait(timeout=5)

    def test_detached_process_observation_and_cleanup(self):
        import shutil
        script = self.root / "unique-descendant-script.py"
        shutil.copyfile(HERE / "descendant_fixture.py", script)
        prefix = str(self.root / "tree")
        child = subprocess.Popen([sys.executable, str(script), prefix], start_new_session=True)
        pids = []
        def own_snapshot():
            # Sandbox forbids ps. Known fixture PID markers supply a simulated
            # ps snapshot for this unit test; production always invokes real ps.
            return {pid: (child.pid if index == 1 else 1, "S", str(script))
                    for index, pid in enumerate(pids)
                    if self.alive(pid)}
        try:
            for kind in ("parent", "ordinary", "detached"):
                path = Path(prefix + f".{kind}.pid")
                eventually(lambda: path.exists(), 5, f"self-test {kind} PID")
                pids.append(int(path.read_text()))
            if hasattr(os, "getsid"):
                try:
                    self.assertNotEqual(os.getsid(pids[2]), os.getsid(child.pid))
                except PermissionError:
                    pass  # macOS sandbox also denies getsid for other PIDs.
            with patch("runner_core.process_rows", side_effect=own_snapshot):
                self.assertTrue(set(pids) <= marked_processes(str(script)))
                cleanup_processes(str(self.root), [child.pid])
        finally:
            for pid in pids + [child.pid]:
                try:
                    os.kill(pid, 9)
                except ProcessLookupError:
                    pass
            child.wait(timeout=5)

    @staticmethod
    def alive(pid):
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False

    def test_output_confinement(self):
        from run_hidden import safe_output
        self.assertEqual(safe_output("unit-result.json"), HERE / "unit-result.json")
        with self.assertRaises(ValueError):
            safe_output("../escaped-results.json")

    def test_catalog_groups_and_unique_ids(self):
        from cases import CASES
        self.assertEqual({group: sum(row[0] == group for row in CASES.values())
                          for group in ("B", "F", "M")}, {"B": 12, "F": 12, "M": 6})
        self.assertTrue(all(name.startswith(row[0]) and callable(row[2]) and bool(row[3]) and bool(row[4]) for name, row in CASES.items()))


class RunnerTests(unittest.TestCase):
    def setUp(self):
        (HERE / ".tmp").mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="archh-fake-unit-", dir=HERE / ".tmp")
        self.root = Path(self.temp.name)
        shim = self.root / "bin"
        shim.mkdir()
        (shim / "ps").symlink_to(HERE / "fake_ps.py")
        self.env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
                    "PATH": str(shim) + os.pathsep + os.environ["PATH"],
                    "ARCH_SELFTEST_REGISTRY": str(self.root / "registry"),
                    "ARCH_SELFTEST_COUNTER": str(self.root / "counter")}

    def tearDown(self):
        registry = self.root / "registry"
        for path in registry.glob("*.json"):
            try:
                os.kill(json.loads(path.read_text())["pid"], 9)
            except (OSError, ValueError, KeyError):
                pass
        self.temp.cleanup()

    def run_fake(self, mode="pass", cases="B01", reps=2, timeout=10):
        self.env["ARCH_SELFTEST_FAKE_MODE"] = mode
        output = self.root / "results.json"
        result = subprocess.run([sys.executable, str(HERE / "run_hidden.py"),
                                 "--kogen", str(HERE / "fake_kogen.py"),
                                 "--groups", "B", "--cases", cases, "--reps", str(reps),
                                 "--case-timeout", str(timeout), "--out", str(output)],
                                capture_output=True, text=True, env=self.env, timeout=35)
        self.assertTrue(output.exists(), f"Runner did not write results: {result.stdout}\n{result.stderr}")
        return result, json.loads(output.read_text())

    @unittest.skipUnless(NETWORK_AVAILABLE, "localhost bind unavailable in this sandbox")
    def test_fake_external_cli_protocol_and_repetition_success(self):
        result, report = self.run_fake(cases="B01")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(report["groups"]["B"], {"passed": 1, "total": 1})
        self.assertEqual(len(report["cases"]), 1)
        self.assertEqual(report["k_ids"]["K-14"]["per_rep"], [{"repetition": 1, "passed": 1, "total": 1}, {"repetition": 2, "passed": 1, "total": 1}])
        self.assertEqual(report["priority_k_ids"]["K-39"]["total"], 0)
        self.assertTrue(all(len(row["repetitions"]) == 2 and row["passed"] for row in report["cases"]))

    @unittest.skipUnless(NETWORK_AVAILABLE, "localhost bind unavailable in this sandbox")
    def test_one_failed_repetition_fails_whole_case(self):
        result, report = self.run_fake(mode="flaky")
        self.assertEqual(result.returncode, 1)
        row = report["cases"][0]
        self.assertEqual([rep["passed"] for rep in row["repetitions"]], [True, False])
        self.assertFalse(row["passed"])
        self.assertEqual(report["groups"]["B"]["passed"], 0)

    @unittest.skipUnless(NETWORK_AVAILABLE, "localhost bind unavailable in this sandbox")
    def test_hard_timeout_and_fake_daemon_cleanup(self):
        result, report = self.run_fake(mode="hang", reps=1, timeout=0.7)
        self.assertEqual(result.returncode, 1)
        repetition = report["cases"][0]["repetitions"][0]
        self.assertTrue(repetition["timed_out"])
        self.assertFalse(repetition["passed"])
        self.assertFalse(repetition["cleanup_survivors"])
        self.assertFalse(list((self.root / "registry").glob("*.json")), "Fake daemon survived timeout")

    def test_kid_report_aggregation_from_prerecorded_children(self):
        from run_hidden import aggregate_kid_results
        fixtures = [
            {"id":"B01", "k_ids":["K-07"], "passed":True,
             "repetitions":[{"passed":True}, {"passed":True}]},
            {"id":"F01", "k_ids":["K-07", "K-19"], "passed":False,
             "repetitions":[{"passed":True}, {"passed":False}]},
        ]
        report = aggregate_kid_results(fixtures, 2)
        self.assertEqual(report["K-07"]["per_rep"], [
            {"repetition":1,"passed":2,"total":2}, {"repetition":2,"passed":1,"total":2}])
        self.assertEqual(report["K-19"]["passed"], 0)
        self.assertEqual(report["K-39"]["total"], 0)

    def test_simulated_ps_parser_and_ancestry(self):
        import runner_core
        fake = subprocess.CompletedProcess([], 0, "999991 1 S /fixture/marker/python\n999992 999991 S /child\n999993 1 Z /fixture/marker/zombie\n", "")
        with patch("runner_core.subprocess.run", return_value=fake):
            rows = runner_core.process_rows()
            self.assertEqual(rows[999992][0], 999991)
            self.assertEqual(runner_core.marked_processes("/fixture/marker"), {999991})
        with patch("runner_core.process_rows", side_effect=[rows, {}, {}]), patch("runner_core.os.kill") as kill:
            runner_core.cleanup_processes("/fixture/marker")
            self.assertIn(999992, {call.args[0] for call in kill.call_args_list})


def main():
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    started = time.monotonic()
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    record = {"passed": result.wasSuccessful(), "tests_run": result.testsRun,
              "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
              "duration_s": round(time.monotonic() - started, 3),
              "scope": "runner unit self-test only; not witness passability",
              "process_observer": "simulated ps snapshots for sandbox; production uses actual ps"}
    (HERE / "selftest-results.json").write_text(json.dumps(record, indent=2) + "\n")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
