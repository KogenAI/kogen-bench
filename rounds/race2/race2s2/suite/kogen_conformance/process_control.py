"""Bounded process-group and case-directory cleanup helpers."""

from __future__ import annotations

import os
import signal
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def implementation_environment(path_prefix: str | Path | None = None) -> dict[str, str]:
    """Return the explicitly inherited toolchain environment for Kogen.

    Case HOME directories are intentionally isolated, but Cargo and rustup
    need their real per-user homes to find toolchains. Keep this allowlist
    narrow: credentials and KOGEN_* variables are never copied from the host.
    """
    inherited_path = os.environ.get("PATH", os.defpath)
    path = os.pathsep.join(([str(path_prefix)] if path_prefix is not None else []) + [inherited_path])
    result = {"PATH": path}
    real_home = os.environ.get("HOME")
    for name in ("RUSTUP_HOME", "CARGO_HOME", "GOROOT", "GOTOOLCHAIN"):
        value = os.environ.get(name)
        if value:
            result[name] = value
        elif name in {"RUSTUP_HOME", "CARGO_HOME"} and real_home:
            default = Path(real_home) / {"RUSTUP_HOME": ".rustup", "CARGO_HOME": ".cargo"}[name]
            if default.is_dir():
                result[name] = str(default)
    return result


@dataclass
class ProcessResult:
    returncode: int
    stdout: bytes
    stderr: bytes
    timed_out: bool
    elapsed_ms: int


def _signal_group(pgid: int, sig: int) -> None:
    if os.name != "posix":
        return
    try:
        os.killpg(pgid, sig)
    except ProcessLookupError:
        pass
    except PermissionError:
        # Sandboxed hosts can deny group signaling even when the direct child
        # remains signalable. Callers also attempt the child PID and the final
        # case cwd sweep; cleanup must never turn a timeout into a hang/error.
        pass


def _group_exists(pgid: int) -> bool:
    if os.name != "posix":
        return False
    try:
        os.killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def kill_process_group(pgid: int, grace_s: float = 0.15) -> None:
    """Stop all remaining members of a command's private session/group."""
    if os.name != "posix":
        return
    _signal_group(pgid, signal.SIGTERM)
    deadline = time.monotonic() + max(0.0, grace_s)
    while _group_exists(pgid) and time.monotonic() < deadline:
        time.sleep(0.01)
    if _group_exists(pgid):
        _signal_group(pgid, signal.SIGKILL)


def run_process(argv: list[str], *, cwd: str | Path, env: dict[str, str],
                stdin: bytes | None = None, timeout_s: float = 60.0) -> ProcessResult:
    """Run one command in its own process group and always return by the bound."""
    timeout_s = max(0.001, float(timeout_s))
    started = time.monotonic()
    process = subprocess.Popen(
        argv, cwd=str(cwd), env=env,
        stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        start_new_session=(os.name == "posix"),
    )
    timed_out = False
    stdout = b""
    stderr = b""
    try:
        stdout, stderr = process.communicate(input=stdin, timeout=timeout_s)
    except subprocess.TimeoutExpired as first_timeout:
        timed_out = True
        stdout = first_timeout.output or b""
        stderr = first_timeout.stderr or b""
        kill_process_group(process.pid, grace_s=0.1)
        try:
            stdout, stderr = process.communicate(timeout=0.25)
        except subprocess.TimeoutExpired as second_timeout:
            # A child that deliberately called setsid() can retain inherited
            # pipes. The cwd sweep at case teardown owns that process; closing
            # our pipe ends here keeps this invocation's timeout hard.
            stdout = second_timeout.output or stdout
            stderr = second_timeout.stderr or stderr
            if process.stdout:
                process.stdout.close()
            if process.stderr:
                process.stderr.close()
            if process.stdin:
                process.stdin.close()
            try:
                process.wait(timeout=0.1)
            except subprocess.TimeoutExpired:
                try:
                    process.kill()
                except (ProcessLookupError, PermissionError):
                    pass
                try:
                    process.wait(timeout=0.1)
                except subprocess.TimeoutExpired:
                    pass
    finally:
        # Also reap descendants on a successful command. Kogen's detached
        # workers live outside this group and are caught by cleanup_case_cwd.
        kill_process_group(process.pid, grace_s=0.05)
        if process.poll() is None:
            try:
                process.wait(timeout=0.1)
            except subprocess.TimeoutExpired:
                try:
                    process.kill()
                except (ProcessLookupError, PermissionError):
                    pass
                try:
                    process.wait(timeout=0.1)
                except subprocess.TimeoutExpired:
                    pass
    return ProcessResult(
        returncode=124 if timed_out else (process.returncode if process.returncode is not None else 124),
        stdout=stdout, stderr=stderr, timed_out=timed_out,
        elapsed_ms=int((time.monotonic() - started) * 1000),
    )


def cleanup_case_cwd(root: str | Path, timeout_s: float = 2.0) -> list[str]:
    """Kill cwd-owned processes and report teardown actions/errors."""
    directory = Path(root).resolve()
    if not directory.exists():
        return []
    lsof = "/usr/sbin/lsof" if Path("/usr/sbin/lsof").exists() else "lsof"
    try:
        probe = subprocess.run(
            [lsof, "-t", "-a", "-d", "cwd", "+D", str(directory)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            timeout=timeout_s, env={"PATH": "/usr/bin:/bin:/usr/sbin", "LC_ALL": "C"}, cwd="/",
        )
    except FileNotFoundError:
        return ["required lsof executable is not available"]
    except subprocess.TimeoutExpired:
        return [f"lsof cwd scan timed out for {directory}"]
    except OSError as error:
        return [f"lsof cwd scan failed for {directory}: {error}"]
    # lsof returns 1 when it found no open cwd entries.
    if probe.returncode not in (0, 1):
        diagnostic = probe.stderr.strip()
        return [f"lsof cwd scan failed for {directory}: {diagnostic or probe.returncode}"]

    notes: list[str] = []
    scanned: set[int] = set()
    killed: set[int] = set()
    protected_groups = {os.getpgrp(), os.getpid(), os.getppid()}

    def terminate(pids: set[int], sig: int) -> None:
        for pid in sorted(pids):
            if pid == os.getpid():
                continue
            scanned.add(pid)
            try:
                pgid = os.getpgid(pid)
            except (ProcessLookupError, PermissionError):
                pgid = None
            # Detached workers often escape their launcher group. Signal both
            # the discovered process group and the exact cwd-owning PID.
            if pgid is not None and pgid > 1 and pgid not in protected_groups:
                try:
                    os.killpg(pgid, sig)
                except (ProcessLookupError, PermissionError):
                    pass
            try:
                os.kill(pid, sig)
                if sig == signal.SIGTERM:
                    killed.add(pid)
            except ProcessLookupError:
                pass
            except PermissionError as error:
                notes.append(f"cannot signal cwd-owned process {pid}: {error}")

    terminate(set(_parse_pids(probe.stdout)), signal.SIGTERM)
    # The final command may spawn a delayed detached child after its parent
    # exits. Rescan at each grace point before removing the case directory.
    for delay in (0.3, 0.7):
        time.sleep(delay)
        current = set(_parse_pids(_cwd_lsof(directory, timeout_s)))
        current.discard(os.getpid())
        if current:
            terminate(current, signal.SIGTERM)
    survivors = set(_parse_pids(_cwd_lsof(directory, timeout_s)))
    survivors.discard(os.getpid())
    if survivors:
        terminate(survivors, signal.SIGKILL)
        time.sleep(0.1)
        remaining = set(_parse_pids(_cwd_lsof(directory, timeout_s))) - {os.getpid()}
        if remaining:
            notes.append("processes still have cwd under directory: " + ", ".join(map(str, sorted(remaining))))
    if killed:
        notes.insert(0, "killed cwd-owned process(es): " + ", ".join(map(str, sorted(killed))))
    return notes


def _cwd_lsof(directory: Path, timeout_s: float) -> str:
    lsof = "/usr/sbin/lsof" if Path("/usr/sbin/lsof").exists() else "lsof"
    try:
        probe = subprocess.run(
            [lsof, "-t", "-a", "-d", "cwd", "+D", str(directory)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            timeout=timeout_s, env={"PATH": "/usr/bin:/bin:/usr/sbin", "LC_ALL": "C"}, cwd="/",
        )
        return probe.stdout if probe.returncode in (0, 1) else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def _parse_pids(raw: str) -> list[int]:
    output: list[int] = []
    for line in raw.splitlines():
        try:
            pid = int(line.strip())
        except ValueError:
            continue
        if pid > 0:
            output.append(pid)
    return output
