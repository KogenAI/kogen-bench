"""Who owns a cell's `live.json`: the process id and start time of its lanes-cell, and whether that process is gone.

A cell that dies hard (kill -9, a stopped run unit, a cgroup memory kill) cannot remove its `live.json`.
`phantom` tells a leftover from a running cell: its pid is not alive, or is alive with another start time
(the pid was reused). A `live.json` from before these fields (workspace only) is a phantom only when its
workspace folder is gone. A file written on another machine (a shared run dir) is never judged here.
"""

import os
import socket
import subprocess


def proc_start(pid):
    """A string that identifies the process `pid` for as long as it lives (its start time), or None when it
    cannot be read. Linux: field 22 of /proc/<pid>/stat (clock ticks since boot). Elsewhere: `ps -o lstart=`."""
    try:
        with open(f"/proc/{pid}/stat", "rb") as f:
            # the command name (field 2) may hold spaces and parentheses: count fields after the last ")"
            return "ticks:" + f.read().decode("utf-8", "replace").rsplit(")", 1)[1].split()[19]
    except (OSError, IndexError):
        pass
    try:
        out = subprocess.run(["ps", "-o", "lstart=", "-p", str(pid)], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return "lstart:" + " ".join(out.stdout.split()) if out.returncode == 0 and out.stdout.strip() else None


def zombie(pid):
    """True when `pid` has died and only waits for its parent to collect it (`kill(pid, 0)` still succeeds then)."""
    try:
        with open(f"/proc/{pid}/stat", "rb") as f:
            return f.read().decode("utf-8", "replace").rsplit(")", 1)[1].split()[0] == "Z"
    except (OSError, IndexError):
        pass
    try:
        out = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return False
    return out.stdout.strip().startswith("Z")


def record(workspace, host=None):
    """The fields of this process's `live.json`."""
    pid = os.getpid()
    return {"workspace": workspace, "pid": pid, "start": proc_start(pid), "host": host, "node": socket.gethostname()}


def phantom(info):
    """Why a `live.json` (its parsed fields) is a leftover, or None when its cell may still be running."""
    if info.get("node") not in (None, socket.gethostname()):
        return None
    pid = info.get("pid")
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        return None if os.path.isdir(info["workspace"]) else "workspace gone"
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return f"pid {pid} gone"
    except PermissionError:
        pass
    if zombie(pid):
        return f"pid {pid} gone"
    start = proc_start(pid)
    if start is not None and info.get("start") is not None and start != info["start"]:
        return f"pid {pid} reused by another process"
    return None
