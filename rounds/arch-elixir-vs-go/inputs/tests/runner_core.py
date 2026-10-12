"""Standard-library-only black-box fixture and process isolation helpers."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
import signal
import socket
import subprocess
import time


class Failure(AssertionError):
    pass


def check(value, message):
    if not value:
        raise Failure(message)  # unscored-mechanics: generic runner timeout/diagnostic


def eventually(predicate, timeout=10, label="condition"):
    end = time.monotonic() + timeout
    last = None
    while time.monotonic() < end:
        try:
            value = predicate()
            if value:
                return value
        except (OSError, ValueError, KeyError) as exc:
            last = str(exc)
        time.sleep(0.1)
    raise Failure(f"Timed out waiting for {label}" + (f": {last}" if last else ""))  # unscored-mechanics: generic runner timeout/diagnostic


def process_rows():
    result = subprocess.run(["ps", "-ww", "-axo", "pid=,ppid=,stat=,command="],
                            capture_output=True, text=True, timeout=5)
    check(result.returncode == 0, "ps failed")  # unscored-mechanics: process-table observer health
    rows = {}
    for line in result.stdout.splitlines():
        fields = line.strip().split(None, 3)
        if len(fields) == 4:
            try:
                rows[int(fields[0])] = (int(fields[1]), fields[2], fields[3])
            except ValueError:
                continue
    return rows


def marked_processes(marker):
    return {pid for pid, (_, state, command) in process_rows().items()
            if marker in command and not state.startswith("Z") and pid != os.getpid()}


def cleanup_processes(marker, roots=()):
    """Observe command markers AND PPID ancestry; handle detached grandchildren."""
    excluded = {os.getpid()}
    rows = process_rows()
    current = os.getpid()
    while current in rows:
        current = rows[current][0]
        if current in excluded:
            break
        excluded.add(current)
    targets = set(roots) | {p for p, (_, _, cmd) in rows.items() if marker in cmd}
    changed = True
    while changed:
        before = set(targets)
        targets.update(p for p, (parent, _, _) in rows.items() if parent in targets)
        changed = targets != before
    targets -= excluded
    for sig in (signal.SIGTERM, signal.SIGKILL):
        for pid in targets:
            try:
                os.kill(pid, sig)
            except ProcessLookupError:
                pass
        if targets:
            time.sleep(0.15)
    survivors = marked_processes(marker) - excluded
    for pid in survivors:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    end = time.monotonic() + 1
    while survivors and time.monotonic() < end:
        time.sleep(0.05)
        survivors = marked_processes(marker) - excluded
    return sorted(survivors)


def unused_port():
    with socket.socket() as sock:
        sock.bind(("[IP omitted]", 0))
        return sock.getsockname()[1]


class FixtureBase:
    def __init__(self, binary, root):
        self.binary = str(Path(binary).resolve())
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.port = unused_port()
        self.address = f"[IP omitted]:{self.port}"
        self.processes = []
        self.logs = []
        self.env = {**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null",
                    "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0",
                    "PYTHONDONTWRITEBYTECODE": "1"}

    def run(self, args, cwd=None, timeout=10, good=True):
        result = subprocess.run([str(a) for a in args], cwd=cwd,
                                capture_output=True, text=True, timeout=timeout, env=self.env)
        if good:
            check(result.returncode == 0,  # clause: SPEC-2
                  f"Command failed ({result.returncode}): {args}\n"
                  f"stdout={result.stdout[-3000:]}\nstderr={result.stderr[-3000:]}")
        return result

    def cli(self, *args, timeout=10, good=True):
        return self.run([self.binary, *args], timeout=timeout, good=good)

    def start(self, *args):
        log = open(self.root / f"process-{len(self.processes)}.log", "ab", buffering=0)
        self.logs.append(log)
        proc = subprocess.Popen([self.binary, *map(str, args)], stdout=log,
                                stderr=subprocess.STDOUT, start_new_session=True, env=self.env)
        self.processes.append(proc)
        return proc

    def kill(self, proc):
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=5)

    def close(self):
        survivors = cleanup_processes(str(self.root), [p.pid for p in self.processes if p.poll() is None])
        for proc in self.processes:
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                pass
        for log in self.logs:
            log.close()
        check(not survivors, f"Cleanup left processes alive: {survivors}")  # unscored-mechanics: generic runner/process cleanup mechanics

    def git(self, repo, *args, good=True):
        return self.run(["git", "-C", repo, *args], good=good).stdout.strip()

    def repository(self, name="repo", bare=True):
        repo = self.root / (name + "-seed" if bare else name)
        repo.mkdir()
        self.run(["git", "init", "-q", repo])
        self.git(repo, "config", "user.name", "ARCH fixture")
        self.git(repo, "config", "user.email", "[email omitted]")
        self.git(repo, "config", "commit.gpgsign", "false")
        self.git(repo, "config", "core.autocrlf", "false")
        self.git(repo, "config", "core.hooksPath", "/dev/null")
        (repo / "base.txt").write_text("base\n")
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-qm", "fixture base")
        base = self.git(repo, "rev-parse", "HEAD")
        if bare:
            target = self.root / (name + ".git")
            self.run(["git", "clone", "--bare", "-q", repo, target])
            return target, base
        return repo, base

    def patch(self, name, contents=None, target=None):
        target = target or f"{name}.txt"
        contents = contents or f"{name}\n"
        lines = contents.splitlines()
        patch = self.root / f"{name}.patch"
        patch.write_text(f"diff --git a/{target} b/{target}\nnew file mode 100644\n"
                         f"--- /dev/null\n+++ b/{target}\n@@ -0,0 +1,{len(lines)} @@\n"
                         + "".join(f"+{line}\n" for line in lines))
        return patch

    def path(self, name):
        return self.root / name

    def shell_path(self, name):
        return shlex.quote(str(self.path(name)))

    def marker(self, name):
        return f"printf 'ready\\n' > {self.shell_path(name)}"

    def gate(self, name):
        return f"while [ ! -f {self.shell_path(name)} ]; do sleep 0.1; done"

    def await_file(self, name, timeout=10):
        return eventually(lambda: self.path(name).exists(), timeout, f"marker {name}")

    def release(self, name):
        self.path(name).touch()

    def diagnostics(self):
        return {path.name: path.read_text(errors="replace")[-6000:]
                for path in self.root.glob("process-*.log")}
