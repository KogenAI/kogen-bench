"""Black-box process supervision contract. Assertions map to task-2 prompt clauses."""
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import pytest

BIN = os.environ["KOGEN_TASK_BIN"]


def invoke(args, timeout=8, input_data=None):
    return subprocess.run([BIN, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          input=input_data, timeout=timeout, check=False)


def cmd(script, *args):
    return ["supervise", "--timeout-ms", "1200", "--grace-ms", "100", "--", "/bin/sh", "-c", script, "sh", *map(str, args)]


def status(kind, exit_code, term, kill, reaped=1):
    return f"status={kind} exit_code={exit_code} term_sent={term} kill_sent={kill} reaped={reaped}\n".encode()


def proc_state(pid):
    try:
        text = Path(f"/proc/{pid}/stat").read_text()
        return text[text.rfind(")") + 2:].split()[0]
    except (FileNotFoundError, ProcessLookupError):
        return None


def assert_not_live(pid):
    state = proc_state(pid)
    assert state is None or state in {"Z", "X"}


def live_process_groups():
    groups = set()
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            raw = (entry / "stat").read_text()
            fields = raw[raw.rfind(")") + 2:].split()
            if fields[0] not in {"Z", "X"}:
                groups.add(int(fields[2]))
        except (FileNotFoundError, ProcessLookupError, PermissionError, ValueError, IndexError):
            continue
    return groups


@pytest.mark.parametrize("args", [[], ["supervise", "--timeout-ms", "1", "--grace-ms", "1"],
                                  ["supervise", "--timeout-ms", "1", "--grace-ms", "1", "--"],
                                  ["supervise", "--timeout-ms", "1", "--timeout-ms", "2", "--grace-ms", "1", "--", "/bin/true"]])
def test_invalid_command_or_option_shape(args):
    """Prompt: exact ordered CLI, required separator and required command; all argument failures return 2."""
    result = invoke(args)
    assert (result.returncode, result.stdout, result.stderr) == (2, b"", b"error: invalid arguments\n")


@pytest.mark.parametrize("value", ["0", "60001", "-1", "1.0", " 1", "x", ""])
def test_timeout_value_must_be_decimal_in_range(value):
    """Prompt: timeout is unsigned ASCII decimal in the inclusive range 1..60000."""
    result = invoke(["supervise", "--timeout-ms", value, "--grace-ms", "2", "--", "/bin/true"])
    assert (result.returncode, result.stdout, result.stderr) == (2, b"", b"error: invalid arguments\n")


def test_grace_value_must_be_in_range():
    """Prompt: grace is bounded above by 60000 milliseconds."""
    result = invoke(["supervise", "--timeout-ms", "1", "--grace-ms", "60001", "--", "/bin/true"])
    assert (result.returncode, result.stdout, result.stderr) == (2, b"", b"error: invalid arguments\n")


def test_unknown_option_before_separator_is_rejected():
    """Prompt: unknown options before the literal separator are invalid arguments."""
    result = invoke(["supervise", "--timeout-ms", "1", "--grace-ms", "1", "--verbose", "--", "/bin/true"])
    assert (result.returncode, result.stdout, result.stderr) == (2, b"", b"error: invalid arguments\n")


def test_command_that_cannot_start_has_exact_diagnostic(tmp_path):
    """Prompt: an unstartable executable returns 127 with the exact diagnostic and no status line."""
    missing = str(tmp_path / "missing-command")
    result = invoke(["supervise", "--timeout-ms", "100", "--grace-ms", "100", "--", missing])
    assert (result.returncode, result.stdout, result.stderr) == (127, b"", b"error: cannot start command\n")


def test_stdin_is_empty_and_streams_forwarded():
    """Prompt: child stdin is empty/EOF; stdout and stderr are byte-identical."""
    result = invoke(cmd("cat; printf 'out\\000tail'; printf 'err\\n' >&2"), input_data=b"ignored")
    assert result.returncode == 0
    assert result.stdout == b"out\x00tail"
    assert result.stderr == b"err\n" + status("exited", 0, "false", "false")


def test_normal_nonzero_exit_is_preserved():
    """Prompt: a normally completed command returns its 0..255 exit status."""
    result = invoke(cmd("exit 37"))
    assert (result.returncode, result.stdout, result.stderr) == (37, b"", status("exited", 37, "false", "false"))


def test_direct_signal_exit_is_encoded_as_128_plus_signal():
    """Prompt: a signaled direct child maps to 128 plus its signal number."""
    result = invoke(cmd("kill -TERM $$"))
    assert result.returncode == 143
    assert result.stderr == status("exited", 143, "false", "false")


def test_timeout_returns_124_even_when_term_is_handled():
    """Prompt: every timeout returns 124, including a command that exits on SIGTERM."""
    script = "import signal,time\nsignal.signal(signal.SIGTERM, lambda *_: exit(0))\nwhile True: time.sleep(.01)\n"
    result = invoke(["supervise", "--timeout-ms", "250", "--grace-ms", "500", "--", sys.executable, "-c", script])
    assert result.returncode == 124
    assert result.stderr == status("timeout", 124, "true", "false")


def test_ignored_term_causes_kill_and_no_running_direct_child(tmp_path):
    """Prompt: an ignored SIGTERM is followed by SIGKILL and no live group member remains."""
    pidfile = tmp_path / "pid"
    script = "import os,signal,sys,time\nsignal.signal(signal.SIGTERM, signal.SIG_IGN)\nopen(sys.argv[1], 'w').write(str(os.getpid()))\nwhile True: time.sleep(.01)\n"
    result = invoke(["supervise", "--timeout-ms", "250", "--grace-ms", "100", "--", sys.executable, "-c", script, str(pidfile)])
    assert result.returncode == 124
    assert result.stderr == status("timeout", 124, "true", "true")
    assert_not_live(int(pidfile.read_text()))


def test_descendant_keeps_group_alive_after_direct_child_exits(tmp_path):
    """Prompt: descendants keep the group alive after the direct child exits and must be killed."""
    pidfile = tmp_path / "grandchild"
    script = "import os,signal,sys,time\npid = os.fork()\nif pid == 0:\n signal.signal(signal.SIGTERM, signal.SIG_IGN)\n open(sys.argv[1], 'w').write(str(os.getpid()))\n time.sleep(30)\n os._exit(0)\n"
    result = invoke(["supervise", "--timeout-ms", "250", "--grace-ms", "80", "--", sys.executable, "-c", script, str(pidfile)])
    assert pidfile.exists()
    assert result.returncode == 124
    assert result.stderr == status("timeout", 124, "true", "true")
    assert_not_live(int(pidfile.read_text()))


def test_finished_descendant_does_not_force_timeout():
    """Prompt: normal completion waits for the whole process group, not only the direct child."""
    result = invoke(cmd("(sleep .04) & wait"))
    assert result.returncode == 0
    assert result.stderr == status("exited", 0, "false", "false")


def test_argument_bytes_are_not_reparsed_by_supervisor():
    """Prompt: arguments after -- pass through without shell parsing or reinterpretation."""
    result = invoke(["supervise", "--timeout-ms", "1200", "--grace-ms", "100", "--", "/usr/bin/printf", "%s", "a b;$HOME"])
    assert result.returncode == 0
    assert result.stdout == b"a b;$HOME"
    assert result.stderr == status("exited", 0, "false", "false")


def test_one_millisecond_timeout_is_accepted():
    """Prompt: a timeout value of the inclusive lower bound is valid."""
    result = invoke(["supervise", "--timeout-ms", "1", "--grace-ms", "1", "--", "/bin/sleep", "0.2"])
    assert result.returncode == 124
    assert result.stderr.startswith(b"status=timeout exit_code=124 term_sent=true kill_sent=")


def test_sixty_thousand_millisecond_values_are_accepted():
    """Prompt: timeout and grace values of the inclusive upper bound are valid."""
    result = invoke(["supervise", "--timeout-ms", "60000", "--grace-ms", "60000", "--", "/bin/true"])
    assert result.returncode == 0
    assert result.stderr == status("exited", 0, "false", "false")


def test_fifty_concurrent_trees_all_finish_without_leaks(tmp_path):
    """Prompt: 50 simultaneous sleeping command trees finish with no live group members."""
    pidfiles = [tmp_path / f"tree-{index}" for index in range(50)]
    script = "printf '%s' \"$$\" > \"$1\"; (sleep .2) & wait"
    procs = [
        subprocess.Popen([BIN, *cmd(script, pidfile)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for pidfile in pidfiles
    ]
    try:
        for process in procs:
            out, err = process.communicate(timeout=30)
            assert process.returncode == 0
            assert out == b""
            assert err == status("exited", 0, "false", "false")
    finally:
        for process in procs:
            if process.poll() is None:
                process.kill()
                process.wait()
    groups = {int(pidfile.read_text()) for pidfile in pidfiles}
    assert groups.isdisjoint(live_process_groups())
