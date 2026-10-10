import shutil
import os
import resource
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

from kogen_conformance.process_control import cleanup_case_cwd
from kogen_conformance.runner import run_case, run_cases
from kogen_conformance.quint_runner import load_quint_cases, run_quint_case
from kogen_conformance.quint_runner import SUITE_ROOT


class ProcessCleanupTest(unittest.TestCase):
    def test_quint_case_descriptors_return_to_baseline_under_low_limit(self):
        if os.name != "posix":
            self.skipTest("RLIMIT_NOFILE regression check requires POSIX")
        cases = load_quint_cases(SUITE_ROOT / "cases" / "quint" / "init")
        case = next(row for row in cases if row["id"] == "quint.init.seed-20267010")
        def descriptor_count():
            # Listing /dev/fd counts its own transient directory descriptor on
            # macOS. Probe descriptor numbers instead so the count is stable.
            current_soft, _ = resource.getrlimit(resource.RLIMIT_NOFILE)
            return sum(1 for fd in range(min(current_soft, 2048)) if _is_open_fd(fd))

        def _is_open_fd(fd):
            try:
                os.fstat(fd)
                return True
            except OSError:
                return False

        previous = resource.getrlimit(resource.RLIMIT_NOFILE)
        soft, hard = previous
        low = min(128, hard)
        try:
            resource.setrlimit(resource.RLIMIT_NOFILE, (low, hard))
            baseline = descriptor_count()
            with tempfile.TemporaryDirectory(prefix="kc2-fd-limit-") as workdir:
                for iteration in range(16):
                    result = run_quint_case(case, str(Path(__file__).parents[2] / "core/target/release/kogen"),
                                            keep=False, timeout_s=10, workdir=workdir)
                    self.assertNotEqual(result["status"], "error", result.get("failures"))
                    self.assertEqual(descriptor_count(), baseline,
                                     f"open FD count grew after case {iteration + 1}: {result.get('id')}")
        finally:
            resource.setrlimit(resource.RLIMIT_NOFILE, previous)

    def test_same_group_cwd_child_is_killed_without_signaling_runner_group(self):
        with tempfile.TemporaryDirectory(prefix="kc2-same-group-cleanup-test-") as directory:
            child = subprocess.Popen(
                ["python3", "-c", "while True: pass"], cwd=directory,
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            try:
                self.assertEqual(os.getpgid(child.pid), os.getpgrp())
                notes = cleanup_case_cwd(directory)
                self.assertIsNotNone(child.poll(), f"cwd-owned child {child.pid} survived cleanup: {notes}")
                probe = subprocess.run(
                    ["/usr/sbin/lsof", "-t", "-a", "-d", "cwd", "+D", directory],
                    capture_output=True, text=True, timeout=3,
                )
                self.assertIn(probe.returncode, (0, 1), probe.stderr)
                self.assertEqual(probe.stdout.strip(), "")
            finally:
                if child.poll() is None:
                    child.kill()
                child.wait(timeout=2)

    def test_run_cleanup_catches_delayed_detached_child(self):
        with tempfile.TemporaryDirectory(prefix="kc2-delayed-cleanup-test-") as directory:
            root = Path(directory)
            fake_kogen = root / "fake-kogen"
            fake_kogen.write_text(
                "#!/usr/bin/env python3\n"
                "import subprocess, sys\n"
                "if sys.argv[1:] == ['last']:\n"
                "    subprocess.Popen(['sh', '-c', 'sleep 0.2; while :; do :; done'],\n"
                "        cwd='.', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,\n"
                "        stderr=subprocess.DEVNULL, start_new_session=True)\n"
                "",
                encoding="utf-8",
            )
            fake_kogen.chmod(0o755)
            workdir = root / "work"
            results_file = root / "results.jsonl"
            case = {"id": "cleanup.delayed-detached-child", "title": "Delayed detached child",
                    "steps": [{"argv": ["first"], "expect": {"exit": 0}},
                              {"argv": ["last"], "expect": {"exit": 0}}]}
            results, code = run_cases([case], str(fake_kogen), workdir=workdir,
                                      out_path=str(results_file), timeout_s=2)
            self.assertEqual(code, 0)
            self.assertEqual(results[0]["status"], "pass")
            probe = subprocess.run(
                ["/usr/sbin/lsof", "-t", "-a", "-d", "cwd", "+D", str(workdir)],
                capture_output=True, text=True, timeout=3,
            )
            self.assertIn(probe.returncode, (0, 1), probe.stderr)
            self.assertEqual(probe.stdout.strip(), "", f"surviving cwd-owned process(es): {probe.stdout}")

    def test_case_cleanup_kills_detached_process_with_case_cwd(self):
        with tempfile.TemporaryDirectory(prefix="kc2-cleanup-test-") as directory:
            root = Path(directory)
            fake_kogen = root / "fake-kogen"
            fake_kogen.write_text(
                "#!/usr/bin/env python3\n"
                "import subprocess\n"
                "subprocess.Popen(['sh', '-c', 'while :; do :; done'],\n"
                "    cwd='.', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,\n"
                "    stderr=subprocess.DEVNULL, start_new_session=True)\n",
                encoding="utf-8",
            )
            fake_kogen.chmod(0o755)
            result = run_case({
                "id": "cleanup.detached-child",
                "title": "Detached child cleanup",
                "steps": [{"argv": ["version"], "expect": {"exit": 0}}],
            }, str(fake_kogen), time_scale=0.01, keep=True, timeout_s=2)
            self.assertEqual(result["status"], "pass", result.get("failures"))
            sandbox = Path(result["sandbox"])
            try:
                probe = subprocess.run(
                    ["/usr/sbin/lsof", "-t", "-a", "-d", "cwd", "+D", str(sandbox)],
                    capture_output=True, text=True, timeout=3,
                )
                self.assertIn(probe.returncode, (0, 1), probe.stderr)
                self.assertEqual(probe.stdout.strip(), "", f"surviving cwd-owned process(es): {probe.stdout}")
            finally:
                shutil.rmtree(sandbox, ignore_errors=True)

    def test_invocation_timeout_returns_within_a_bounded_cleanup_window(self):
        with tempfile.TemporaryDirectory(prefix="kc2-timeout-test-") as directory:
            fake_kogen = Path(directory) / "fake-kogen"
            fake_kogen.write_text(
                "#!/usr/bin/env python3\n"
                "while True: pass\n",
                encoding="utf-8",
            )
            fake_kogen.chmod(0o755)
            started = time.monotonic()
            result = run_case({
                "id": "cleanup.hard-timeout",
                "title": "Hard invocation timeout",
                "steps": [{"argv": ["hang"], "expect": {"exit": 124}}],
            }, str(fake_kogen), time_scale=0.01, keep=False, timeout_s=0.1)
            elapsed = time.monotonic() - started
            self.assertEqual(result["status"], "pass", result.get("failures"))
            self.assertTrue(result["steps"][0]["timed_out"])
            self.assertLess(elapsed, 3.0, f"timeout cleanup took {elapsed:.3f}s")


if __name__ == "__main__":
    unittest.main()
