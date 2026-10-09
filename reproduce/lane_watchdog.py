#!/usr/bin/env python3
"""Stop a benchmark unit after its Codex event log becomes idle."""

import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(
        timespec="seconds").replace("+00:00", "Z")


def snapshot(path):
    try:
        stat = Path(path).stat()
    except FileNotFoundError:
        return None
    return stat.st_size, stat.st_mtime_ns


def running(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


class CommandTracker:
    """Incrementally track command_execution items that have not completed."""

    def __init__(self):
        self.offset = 0
        self.pending = b""
        self.open_commands = set()
        self.inode = None

    def poll(self, path):
        try:
            with open(path, "rb") as source:
                stat = os.fstat(source.fileno())
                inode = (stat.st_dev, stat.st_ino)
                if self.inode != inode or stat.st_size < self.offset:
                    self.offset = 0
                    self.pending = b""
                    self.open_commands.clear()
                    self.inode = inode
                source.seek(self.offset)
                chunk = source.read()
                self.offset += len(chunk)
        except FileNotFoundError:
            self.offset = 0
            self.pending = b""
            self.open_commands.clear()
            self.inode = None
            return

        lines = (self.pending + chunk).split(b"\n")
        self.pending = lines.pop()
        for line in lines:
            self._consume(line)

    def _consume(self, line):
        try:
            event = json.loads(line)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return
        event_type = event.get("type")
        if event_type not in ("item.started", "item.completed"):
            return
        item = event.get("item")
        if not isinstance(item, dict) or item.get("type") != "command_execution":
            return
        item_id = item.get("id", event.get("item_id"))
        if item_id is None:
            item_id = "__anonymous_command_execution__"
        if event_type == "item.started":
            self.open_commands.add(item_id)
        else:
            self.open_commands.discard(item_id)
def watch(log_path, stall_path, idle_limit, pid, unit, poll_interval=1,
          stop_unit=None, clock=time.monotonic, sleep=time.sleep,
          deadline=None, timeout_path=None):
    stop_unit = stop_unit or (lambda name: subprocess.run(
        ["systemctl", "stop", name], check=False,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    last_snapshot = snapshot(log_path)
    last_change = clock()
    started = last_change
    commands = CommandTracker()
    while running(pid):
        sleep(poll_interval)
        commands.poll(log_path)
        current = snapshot(log_path)
        now = clock()
        if deadline is not None and now - started >= deadline:
            if not running(pid):
                return 0
            stop_unit(unit)
            if timeout_path:
                Path(timeout_path).write_text(json.dumps({
                    "timeout": True, "elapsed_seconds": int(now - started),
                    "utc": utc_now()
                }, sort_keys=True) + "\n", encoding="utf-8")
            return 11
        if current != last_snapshot:
            last_snapshot = current
            last_change = now
            continue
        idle = int(now - last_change)
        if idle >= idle_limit and not commands.open_commands:
            if not running(pid):
                return 0
            stop_unit(unit)
            Path(stall_path).write_text(json.dumps({
                "stalled": True, "idle_seconds": idle, "utc": utc_now()
            }, sort_keys=True) + "\n", encoding="utf-8")
            return 10
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) not in (5, 7):
        print("usage: lane_watchdog.py CODEX_JSONL STALL_JSON SECONDS PID UNIT [DEADLINE TIMEOUT_JSON]",
              file=sys.stderr)
        return 2
    log_path, stall_path, seconds, pid, unit = argv[:5]
    deadline = None
    timeout_path = None
    try:
        idle_limit, pid = int(seconds), int(pid)
        if len(argv) == 7:
            deadline = int(argv[5])
            timeout_path = argv[6]
    except ValueError:
        return 2
    if idle_limit < 1 or pid < 1 or (deadline is not None and deadline < 1) or not unit.startswith("bench-"):
        return 2
    return watch(log_path, stall_path, idle_limit, pid, unit,
                 deadline=deadline, timeout_path=timeout_path)


if __name__ == "__main__":
    raise SystemExit(main())
