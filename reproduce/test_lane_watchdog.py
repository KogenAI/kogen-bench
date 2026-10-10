import json
import subprocess
import tempfile
import time
import unittest
from unittest import mock
from pathlib import Path

import lane_watchdog


class LaneWatchdogTests(unittest.TestCase):
    def test_rechecks_runner_before_recording_stall(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            log = root / "codex.jsonl"
            stall = root / "stall.json"
            log.write_text('{"type":"turn.started"}\n')
            stopped = []
            ticks = iter([100, 102])
            with mock.patch.object(lane_watchdog, "running", side_effect=[True, False]):
                result = lane_watchdog.watch(
                    log, stall, 1, 123, "bench-test", poll_interval=0,
                    stop_unit=lambda unit: stopped.append(unit),
                    clock=lambda: next(ticks), sleep=lambda _: None,
                )
            self.assertEqual(result, 0)
            self.assertEqual(stopped, [])
            self.assertFalse(stall.exists())

    def test_deadline_stops_open_command_and_records_timeout(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            log = root / "codex.jsonl"
            timeout = root / "timeout.json"
            event = {"type": "item.started", "item": {
                "id": "cmd-1", "type": "command_execution", "command": "sleep"
            }}
            log.write_text(json.dumps(event) + "\n")
            agent = subprocess.Popen(["python3", "-c", "import time; time.sleep(10)"])
            stopped = []
            try:
                result = lane_watchdog.watch(
                    log, root / "stall.json", 1, agent.pid, "bench-test",
                    poll_interval=0.01, deadline=0.03, timeout_path=timeout,
                    stop_unit=lambda unit: (stopped.append(unit), agent.terminate()),
                )
                self.assertEqual(result, 11)
                self.assertEqual(stopped, ["bench-test"])
                self.assertTrue(json.loads(timeout.read_text())["timeout"])
            finally:
                if agent.poll() is None:
                    agent.kill()
                agent.wait(timeout=2)

    def test_stops_fake_agent_when_event_log_stops_changing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            log = root / "codex.jsonl"
            stall = root / "stall.json"
            agent = subprocess.Popen([
                "python3", "-c",
                "import pathlib,time; pathlib.Path(r'%s').write_text('{\"type\":\"turn.started\"}\\n'); time.sleep(10)" % log,
            ])
            stopped = []
            try:
                result = lane_watchdog.watch(
                    log, stall, 1, agent.pid, "bench-test", poll_interval=0.05,
                    stop_unit=lambda unit: (stopped.append(unit), agent.terminate()),
                )
                self.assertEqual(result, 10)
                self.assertEqual(stopped, ["bench-test"])
                record = json.loads(stall.read_text())
                self.assertEqual(record["stalled"], True)
                self.assertGreaterEqual(record["idle_seconds"], 1)
                self.assertTrue(record["utc"].endswith("Z"))
            finally:
                if agent.poll() is None:
                    agent.kill()
                agent.wait(timeout=2)

    def test_idle_open_command_is_not_a_stall(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            log = root / "codex.jsonl"
            stall = root / "stall.json"
            event = {"type": "item.started", "item": {
                "id": "cmd-1", "type": "command_execution", "command": "sleep 10"
            }}
            agent = subprocess.Popen([
                "python3", "-c",
                "import pathlib,time; pathlib.Path(r'%s').write_text(%r); time.sleep(1.3)"
                % (log, json.dumps(event) + "\n"),
            ])
            stopped = []
            try:
                result = lane_watchdog.watch(
                    log, stall, 1, agent.pid, "bench-test", poll_interval=0.05,
                    stop_unit=lambda unit: (stopped.append(unit), agent.terminate()),
                    sleep=lambda delay: (time.sleep(delay), agent.poll()),
                )
                self.assertEqual(result, 0)
                self.assertEqual(stopped, [])
                self.assertFalse(stall.exists())
            finally:
                if agent.poll() is None:
                    agent.kill()
                agent.wait(timeout=2)


if __name__ == "__main__":
    unittest.main()
