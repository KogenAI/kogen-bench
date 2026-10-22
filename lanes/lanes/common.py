"""Shared helpers: JSON files, hashes, paths, and processes with deadlines."""

import hashlib
import json
import os
import signal
import subprocess
import time

DEFAULT_HOME = "~/.cache/kogen-lanes"


def lanes_home():
    """Root of private data (runs, Kogen cache). `KOGEN_LANES_HOME` or the default."""
    return os.path.abspath(os.path.expanduser(os.environ.get("KOGEN_LANES_HOME") or DEFAULT_HOME))


def runs_dir(experiment_id=None):
    base = os.path.join(lanes_home(), "runs")
    return os.path.join(base, experiment_id) if experiment_id else base


def cache_dir():
    return os.path.join(lanes_home(), "cache")


def cell_dir(run_dir, cell):
    """`cell` is `<task>/r<rep>/<lane>`."""
    return os.path.join(run_dir, "cells", *cell.split("/"))


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def dumps_json(data):
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def write_json(path, data):
    """Write sorted-key JSON with a trailing newline, atomically, creating parents."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(dumps_json(data))
    os.replace(tmp, path)


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_tree(root, exclude=(".git",)):
    """Digest of a directory: sorted relative paths, executable bit and content.

    Every symlink (also one to a directory) hashes as `l <target>` and is not followed.
    Names in `exclude` are skipped at any depth.
    """
    h = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in exclude)
        links = [d for d in dirnames if os.path.islink(os.path.join(dirpath, d))]
        dirnames[:] = [d for d in dirnames if d not in links]
        for name in sorted(filenames + links):
            if name in exclude:
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            if os.path.islink(path):
                line = f"l {os.readlink(path)} {rel}\n"
            else:
                mode = "x" if os.stat(path).st_mode & 0o111 else "f"
                line = f"{mode} {sha256_file(path)} {rel}\n"
            h.update(line.encode())
    return h.hexdigest()


def _killpg(pgid, sig):
    try:
        os.killpg(pgid, sig)
    except (ProcessLookupError, PermissionError):
        pass


def _kill_group(proc, grace_s=2.0):
    """TERM then KILL the process group this module started; reap the leader."""
    pgid = proc.pid  # start_new_session makes the child its own group leader
    _killpg(pgid, signal.SIGTERM)
    end = time.monotonic() + grace_s
    while time.monotonic() < end and proc.poll() is None:
        time.sleep(0.02)
    _killpg(pgid, signal.SIGKILL)
    proc.wait()


def run(cmd, cwd=None, env=None, deadline_s=None, stdout=None, stderr=None, stdin=None):
    """Run `cmd` in its own process group; return `(exit_code, timed_out)`.

    On the deadline or KeyboardInterrupt the whole group is killed (TERM, then KILL),
    so no descendant outlives the call. `env` replaces the environment when given.
    `stdout`, `stderr` and `stdin` are file objects or None, as for subprocess.
    """
    proc = subprocess.Popen(
        cmd, cwd=cwd, env=env, stdout=stdout, stderr=stderr, stdin=stdin, start_new_session=True
    )
    try:
        try:
            code = proc.wait(timeout=deadline_s)
            timed_out = False
        except subprocess.TimeoutExpired:
            _kill_group(proc)
            return proc.returncode, True
        # The leader exited; stragglers it left behind are still ours to stop.
        _killpg(proc.pid, signal.SIGKILL)
        return code, timed_out
    except BaseException:
        _kill_group(proc)
        raise
