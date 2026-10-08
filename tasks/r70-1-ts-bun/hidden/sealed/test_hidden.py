"""Black-box contract checks for task 1; clause references are in each docstring."""
import json
import os
from pathlib import Path
import signal
import subprocess
import time

import pytest


BIN = Path(os.environ["KOGEN_TASK_BIN"])


def invoke(*args, timeout=8):
    return subprocess.run([str(BIN), *map(str, args)], capture_output=True, timeout=timeout)


def add(store, job_id, argv):
    return invoke("queue", "add", "--store", store, "--id", job_id,
                  "--argv", json.dumps(argv, ensure_ascii=False, separators=(",", ":")))


def executable(tmp_path, body):
    path = tmp_path / "job.sh"
    path.write_text("#!/bin/sh\nset -eu\n" + body)
    path.chmod(0o755)
    return str(path)


def test_add_creates_store_and_reports_id(tmp_path):
    """Add contract: missing directories are created and success is exact."""
    store = tmp_path / "new" / "queue"
    result = invoke("queue", "add", "--argv", '["/bin/true"]', "--id", "first", "--store", store)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"queued first\n", b"")
    assert store.is_dir()


def test_invalid_id_rejected(tmp_path):
    """Argument contract: IDs start alphanumeric and use only the listed alphabet."""
    result = add(tmp_path / "s", "_bad", ["/bin/true"])
    assert (result.returncode, result.stdout, result.stderr) == (2, b"", b"error: invalid arguments\n")


def test_id_length_limit(tmp_path):
    """Argument contract: IDs are at most 64 characters."""
    result = add(tmp_path / "s", "a" * 65, ["/bin/true"])
    assert (result.returncode, result.stdout, result.stderr) == (2, b"", b"error: invalid arguments\n")


@pytest.mark.parametrize("argv", ["not-json", "{}", "[]", '["", "x"]', '[1]', '["a", null]'])
def test_invalid_json_or_argv(tmp_path, argv):
    """Argument contract: argv is a JSON array of one or more nonempty strings."""
    result = invoke("queue", "add", "--store", tmp_path / "s", "--id", "x", "--argv", argv)
    assert (result.returncode, result.stdout, result.stderr) == (2, b"", b"error: invalid arguments\n")


def test_unknown_option_rejected(tmp_path):
    """Argument contract: unknown options are invalid and produce no stdout."""
    result = invoke("queue", "status", "--store", tmp_path / "s", "--extra")
    assert (result.returncode, result.stdout, result.stderr) == (2, b"", b"error: invalid arguments\n")


def test_repeated_option_rejected(tmp_path):
    """Argument contract: each required option appears exactly once."""
    result = invoke("queue", "status", "--store", tmp_path / "s", "--store", tmp_path / "s")
    assert (result.returncode, result.stdout, result.stderr) == (2, b"", b"error: invalid arguments\n")


def test_missing_and_extra_arguments_rejected(tmp_path):
    """Argument contract: options have values and commands accept no extra arguments."""
    missing = invoke("queue", "status", "--store")
    extra = invoke("queue", "run", "--store", tmp_path / "s", "surplus")
    assert (missing.returncode, missing.stdout, missing.stderr) == (2, b"", b"error: invalid arguments\n")
    assert (extra.returncode, extra.stdout, extra.stderr) == (2, b"", b"error: invalid arguments\n")


def test_duplicate_id_exact_error(tmp_path):
    """Add contract: a repeated ID fails with the specified message and code."""
    store = tmp_path / "s"
    assert add(store, "same", ["/bin/true"]).returncode == 0
    result = add(store, "same", ["/bin/false"])
    assert (result.returncode, result.stdout, result.stderr) == (3, b"", b"error: duplicate job id\n")


def test_empty_store_run_and_status_are_silent(tmp_path):
    """Empty queue contract: both commands print nothing and return zero."""
    store = tmp_path / "s"
    run = invoke("queue", "run", "--store", store)
    status = invoke("queue", "status", "--store", store)
    assert (run.returncode, run.stdout, run.stderr) == (0, b"", b"")
    assert (status.returncode, status.stdout, status.stderr) == (0, b"", b"")


def test_pending_status_order(tmp_path):
    """Status contract: pending jobs appear once in insertion order."""
    store = tmp_path / "s"
    add(store, "b", ["/bin/true"])
    add(store, "a", ["/bin/true"])
    result = invoke("queue", "status", "--store", store)
    assert result.stdout == b"b pending\na pending\n"
    assert result.returncode == 0 and result.stderr == b""


def test_run_captures_outputs_and_json_key_order(tmp_path):
    """Run contract: separate output capture, compact JSON, fixed ordered keys."""
    store = tmp_path / "s"
    script = executable(tmp_path, "printf 'out %s\\n' \"$1\"\nprintf 'err\\n' >&2\n")
    assert add(store, "job", [script, 'q"\\x']).returncode == 0
    result = invoke("queue", "run", "--store", store)
    assert result.stdout.endswith(b"\n") and result.stdout.count(b"\n") == 1
    row = result.stdout.decode().removesuffix("\n")
    assert list(json.loads(row)) == ["id", "attempt", "exit_code", "stdout", "stderr", "status"]
    assert row == '{"id":"job","attempt":1,"exit_code":0,"stdout":"out q\\\"\\\\x\\n","stderr":"err\\n","status":"succeeded"}'
    assert result.returncode == 0 and result.stderr == b""


def test_run_passes_arguments_without_shell(tmp_path):
    """Argv contract: metacharacters remain ordinary child argument bytes."""
    store = tmp_path / "s"
    marker = tmp_path / "owned"
    script = executable(tmp_path, "printf '%s\\n' \"$1\"\n")
    value = f"x;touch {marker}"
    add(store, "safe", [script, value])
    result = invoke("queue", "run", "--store", store)
    assert json.loads(result.stdout) ["stdout"] == value + "\n"
    assert not marker.exists()


def test_run_continues_after_failure_and_statuses(tmp_path):
    """Run contract: nonzero children are recorded and do not stop later jobs."""
    store = tmp_path / "s"
    add(store, "bad", ["/bin/sh", "-c", "echo no; exit 7"])
    add(store, "signal", ["/bin/sh", "-c", "kill -TERM $$"])
    add(store, "good", ["/bin/echo", "yes"])
    result = invoke("queue", "run", "--store", store)
    rows = [json.loads(line) for line in result.stdout.splitlines()]
    assert [(r["id"], r["exit_code"], r["status"]) for r in rows] == [
        ("bad", 7, "failed"), ("signal", 143, "failed"), ("good", 0, "succeeded")]
    assert result.returncode == 0
    assert invoke("queue", "status", "--store", store).stdout == b"bad failed 7\nsignal failed 143\ngood succeeded\n"


def test_completed_jobs_do_not_run_twice(tmp_path):
    """Completion contract: committed jobs are not executed by later runs."""
    store = tmp_path / "s"
    marker = tmp_path / "count"
    script = executable(tmp_path, f"echo x >> '{marker}'\n")
    add(store, "once", [script])
    assert len(invoke("queue", "run", "--store", store).stdout.splitlines()) == 1
    assert invoke("queue", "run", "--store", store).stdout == b""
    assert marker.read_text().splitlines() == ["x"]


def test_child_invalid_utf8_is_replaced(tmp_path):
    """Output contract: invalid child UTF-8 bytes decode using replacement."""
    store = tmp_path / "s"
    script = executable(tmp_path, "printf '\\377'\nprintf '\\376' >&2\n")
    add(store, "bytes", [script])
    row = json.loads(invoke("queue", "run", "--store", store).stdout)
    assert row["stdout"] == "\ufffd" and row["stderr"] == "\ufffd"


def test_missing_executable_is_recorded(tmp_path):
    """Spawn contract: an unavailable executable is a failed completed job."""
    store = tmp_path / "s"
    add(store, "missing", [str(tmp_path / "absent")])
    result = invoke("queue", "run", "--store", store)
    row = json.loads(result.stdout)
    assert (row["exit_code"], row["stderr"], row["status"]) == (127, "exec failed\n", "failed")
    assert result.returncode == 0


def test_store_io_error_is_exact(tmp_path):
    """Store error contract: a non-directory path returns the exact error and code."""
    file_path = tmp_path / "file"
    file_path.write_text("x")
    result = invoke("queue", "status", "--store", file_path)
    assert (result.returncode, result.stdout, result.stderr) == (4, b"", b"error: store failure\n")


def test_sigkill_before_commit_retries_and_counts_attempts(tmp_path):
    """Recovery contract: killed in-flight work stays pending and next start increments attempt."""
    store = tmp_path / "s"
    marker = tmp_path / "starts"
    script = executable(tmp_path, f"if [ ! -f '{marker}' ]; then\n  echo start >> '{marker}'\n  sleep 30\nelse\n  echo start >> '{marker}'\nfi\n")
    add(store, "recover", [script])
    proc = subprocess.Popen([str(BIN), "queue", "run", "--store", str(store)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and not marker.exists():
        time.sleep(0.02)
    assert marker.exists()
    os.killpg(proc.pid, signal.SIGKILL)
    proc.wait(timeout=3)
    assert invoke("queue", "status", "--store", store).stdout == b"recover pending\n"
    result = invoke("queue", "run", "--store", store)
    row = json.loads(result.stdout)
    assert row["attempt"] == 2
    assert marker.read_text().splitlines() == ["start", "start"]


def test_add_and_status_wait_for_running_job(tmp_path):
    """Lock contract: status and add wait for the full duration of a run."""
    store = tmp_path / "s"
    marker = tmp_path / "started"
    script = executable(tmp_path, f"touch '{marker}'\nsleep 0.45\n")
    add(store, "slow", [script])
    run = subprocess.Popen([str(BIN), "queue", "run", "--store", str(store)],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and not marker.exists():
        time.sleep(0.01)
    assert marker.exists()
    started = time.monotonic()
    status = invoke("queue", "status", "--store", store)
    elapsed = time.monotonic() - started
    run.wait(timeout=5)
    assert status.returncode == 0 and elapsed >= 0.20
    assert status.stdout == b"slow succeeded\n"


def test_add_waits_and_is_not_part_of_current_run(tmp_path):
    """Lock contract: an add racing a run waits, then remains pending after that run."""
    store = tmp_path / "s"
    marker = tmp_path / "started"
    script = executable(tmp_path, f"touch '{marker}'\nsleep 0.45\n")
    add(store, "slow", [script])
    run = subprocess.Popen([str(BIN), "queue", "run", "--store", str(store)],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and not marker.exists():
        time.sleep(0.01)
    assert marker.exists()
    started = time.monotonic()
    result = add(store, "later", ["/bin/true"])
    elapsed = time.monotonic() - started
    run.wait(timeout=5)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"queued later\n", b"")
    assert elapsed >= 0.20
    assert invoke("queue", "status", "--store", store).stdout == b"slow succeeded\nlater pending\n"
