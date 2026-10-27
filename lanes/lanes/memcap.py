"""An optional memory cap per local cell: a cgroup v2 child per cell when the dispatcher's cgroup is
delegated, else a watchdog that sums the resident set of the cell's process tree.

The cap stops one cell, never the run: the dispatcher records `memory-cap.json` in the cell dir and moves on."""

import os
import re
import signal
import subprocess
import sys
import threading
import time

from . import common

SAMPLE_S = 2.0  # watchdog: time between two sums of the tree's resident set
TERM_GRACE_S = 3.0  # watchdog: TERM first, KILL after this
CGROUP_ROOT = "/sys/fs/cgroup"
RECORD = "memory-cap.json"
SIZE = re.compile(r"(\d+)([KMGT]?)")
# The cell's process joins its cgroup before it runs anything: write its pid, then exec the command.
_JOIN = "import os,sys;open(sys.argv[1]+'/cgroup.procs','w').write(str(os.getpid()));os.execvp(sys.argv[2],sys.argv[2:])"


def parse_size(text):
    """Bytes of `"4G"`, `"512M"`, `"1024K"`, `"2T"` or plain digits (powers of 1024); ValueError otherwise."""
    m = SIZE.fullmatch(text.strip()) if isinstance(text, str) else None
    if not m or int(m.group(1)) < 1:
        raise ValueError(f"{text!r} is not a size like 4G, 512M or a number of bytes")
    return int(m.group(1)) * 1024 ** ("", "K", "M", "G", "T").index(m.group(2))


def ps_table():
    """`{pid: (ppid, rss_kb)}` of every process (`ps -A -o pid=,ppid=,rss=`, the same on macOS and Linux)."""
    out = subprocess.run(["ps", "-A", "-o", "pid=,ppid=,rss="], capture_output=True, text=True, check=True).stdout
    return parse_ps(out)


def parse_ps(text):
    table = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            table[int(parts[0])] = (int(parts[1]), int(parts[2]))
    return table


def tree(root, table):
    """`root` and every descendant of it in `table`, as a set of pids (empty when `root` is not there)."""
    if root not in table:
        return set()
    kids = {}
    for pid, (ppid, _) in table.items():
        kids.setdefault(ppid, []).append(pid)
    seen, todo = {root}, [root]
    while todo:
        for k in kids.get(todo.pop(), []):
            if k not in seen:
                seen.add(k)
                todo.append(k)
    return seen


def tree_rss(root, table):
    """Bytes of resident memory summed over `root` and its descendants."""
    return sum(table[p][1] for p in tree(root, table)) * 1024


def _signal(pids, sig):
    for pid in pids:
        try:
            os.kill(pid, sig)
        except (ProcessLookupError, PermissionError):
            pass


class Watchdog:
    """Every `SAMPLE_S` seconds sums the RSS of a process tree; above `cap` bytes kills it (TERM, then KILL)."""

    def __init__(self, root, cap, sample_s=SAMPLE_S, grace_s=TERM_GRACE_S, table=ps_table):
        self.root, self.cap, self.sample_s, self.grace_s, self.table = root, cap, sample_s, grace_s, table
        self.peak = 0
        self.hit = None  # {cap, peak_rss, at} once the cap was exceeded
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self._thread.start()
        return self

    def stop(self):
        self._stop.set()
        self._thread.join(self.grace_s + self.sample_s + 5)

    def _run(self):
        while not self._stop.wait(self.sample_s):
            try:
                table = self.table()
            except (OSError, subprocess.SubprocessError):
                continue
            rss = tree_rss(self.root, table)
            self.peak = max(self.peak, rss)
            if rss > self.cap:
                self.hit = {"cap": self.cap, "peak_rss": self.peak, "at": time.time()}
                self._kill(tree(self.root, table))
                return

    def _kill(self, pids):
        _signal(pids, signal.SIGTERM)
        common._killpg(self.root, signal.SIGTERM)
        end = time.monotonic() + self.grace_s
        while time.monotonic() < end and any(p in self.table() for p in pids):
            time.sleep(0.1)
        try:
            pids = pids | tree(self.root, self.table())  # what it started meanwhile
        except (OSError, subprocess.SubprocessError):
            pass
        _signal(pids, signal.SIGKILL)
        common._killpg(self.root, signal.SIGKILL)


# ---- cgroup v2 ------------------------------------------------------------------------------

def own_cgroup(root=CGROUP_ROOT):
    """The directory of this process's cgroup (v2), or None."""
    try:
        with open("/proc/self/cgroup", encoding="utf-8") as f:
            for line in f:
                if line.startswith("0::"):
                    path = os.path.join(root, line.strip()[3:].lstrip("/"))
                    return path if os.path.isdir(path) else None
    except OSError:
        pass
    return None


def delegated(path):
    """True when the cgroup at `path` lets this process make child cgroups under the memory controller."""
    try:
        with open(os.path.join(path, "cgroup.controllers"), encoding="utf-8") as f:
            has_memory = "memory" in f.read().split()
        return has_memory and all(os.access(os.path.join(path, n), os.W_OK) for n in ("cgroup.subtree_control", "cgroup.procs"))
    except OSError:
        return False


class Cgroups:
    """Child cgroups of a delegated cgroup. The dispatcher moves into a leaf (`dispatch`) first, as the
    "no internal processes" rule needs, and the memory controller is enabled for the children."""

    def __init__(self, base):
        self.base = base
        leaf = os.path.join(base, "dispatch")
        os.makedirs(leaf, exist_ok=True)
        with open(os.path.join(base, "cgroup.procs"), encoding="utf-8") as f:
            pids = [os.getpid()] + [int(p) for p in f.read().split() if int(p) != os.getpid()]
        for pid in pids:  # this process first, then its unit's others (a launching shell, say)
            with open(os.path.join(leaf, "cgroup.procs"), "w") as f:
                f.write(str(pid))
        with open(os.path.join(base, "cgroup.subtree_control"), "w") as f:
            f.write("+memory")

    def make(self, name, cap):
        path = os.path.join(self.base, "cell-" + name)
        os.makedirs(path, exist_ok=True)
        _write(os.path.join(path, "memory.max"), str(cap), must=True)
        _write(os.path.join(path, "memory.oom.group"), "1", must=True)  # one kill takes the whole cell
        _write(os.path.join(path, "memory.swap.max"), "0")  # swap must not hide a runaway
        return path


def _write(path, value, must=False):
    try:
        with open(path, "w") as f:
            f.write(value)
    except OSError:
        if must:
            raise


def _events(path):
    try:
        with open(os.path.join(path, "memory.events"), encoding="utf-8") as f:
            return {k: int(v) for k, v in (line.split() for line in f if line.strip())}
    except (OSError, ValueError):
        return {}


def _peak(path):
    try:
        with open(os.path.join(path, "memory.peak"), encoding="utf-8") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return None


_shared = {}
_shared_lock = threading.Lock()


def shared_cgroups():
    """`Cgroups` of this process when its cgroup is delegated (made once per process), else None."""
    with _shared_lock:
        if "cgroups" not in _shared:
            base = own_cgroup()
            _shared["cgroups"], _shared["why"] = None, "no cgroup v2 here"
            if base:
                _shared["why"] = f"cgroup {base} is not delegated"
                if delegated(base):
                    try:
                        _shared["cgroups"] = Cgroups(base)
                    except (OSError, ValueError) as e:  # e.g. EBUSY: a process of the cgroup cannot be moved
                        _shared["why"] = f"cgroup {base} cannot be set up ({e})"
        return _shared["cgroups"]


def why_not():
    """Why `shared_cgroups()` is None (after calling it)."""
    return _shared.get("why", "")


class Limiter:
    """The memory cap of one host: decides the mechanism once and hands out a `Guard` per cell."""

    def __init__(self, cap_text, log=print, host="local", cgroups=shared_cgroups):
        self.text, self.cap = cap_text, parse_size(cap_text)
        self.cgroups = cgroups()
        self.mechanism = "cgroup v2" if self.cgroups else "watchdog"
        log(f"{host}: cell memory cap {cap_text} enforced by the {self.mechanism}"
            + ("" if self.cgroups else f" (RSS of the cell's process tree every 2 s; {why_not()})"))

    def guard(self, name):
        return Guard(self, name)


class Guard:
    """One cell's cap. `wrap(cmd)` before the run, `attach(proc)` when it started, `finish()` after."""

    def __init__(self, limiter, name):
        self.limiter, self.name = limiter, name.replace("/", "__")
        self.path = self.dog = None

    def wrap(self, cmd):
        if not self.limiter.cgroups:
            return cmd
        self.path = self.limiter.cgroups.make(self.name, self.limiter.cap)
        return [sys.executable, "-c", _JOIN, self.path, *cmd]

    def attach(self, proc):
        if not self.limiter.cgroups:
            self.dog = Watchdog(proc.pid, self.limiter.cap).start()

    def finish(self):
        """`{cap, peak_rss, at, mechanism}` when the cap stopped the cell, else None; cleans up."""
        hit = None
        if self.dog:
            self.dog.stop()
            hit = self.dog.hit
        elif self.path:
            if _events(self.path).get("oom_kill", 0) > 0:
                hit = {"cap": self.limiter.cap, "peak_rss": _peak(self.path) or self.limiter.cap, "at": time.time()}
            _write(os.path.join(self.path, "cgroup.kill"), "1")  # stragglers
            for _ in range(20):
                try:
                    os.rmdir(self.path)
                    break
                except OSError:
                    time.sleep(0.1)
        if hit:
            hit = {**hit, "mechanism": self.limiter.mechanism}
            hit["at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(hit["at"]))
        return hit
