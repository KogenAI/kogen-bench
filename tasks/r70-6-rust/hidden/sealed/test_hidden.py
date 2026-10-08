import json
import os
import subprocess
from pathlib import Path


BIN = os.environ["KOGEN_TASK_BIN"]


def ev(i, typ, job="alpha", ts=1):
    return {"id": i, "type": typ, "job": job, "ts": ts}


def line(x):
    return json.dumps(x, separators=(",", ":"))


def call(*args):
    return subprocess.run([BIN, *args], text=True, capture_output=True)


def log(tmp_path, data=b""):
    p = tmp_path / "events.jsonl"
    p.write_bytes(data)
    return p


def reconcile(p):
    return call("reconcile", "--log", str(p))


def append(p, event):
    return call("append", "--log", str(p), "--event", line(event))


def test_empty_log_has_exact_zero_status(tmp_path):
    p = log(tmp_path)
    r = reconcile(p)
    assert (r.returncode, r.stdout, r.stderr) == (0, "total=0\nqueued=0\nrunning=0\ndone=0\nfailed=0\n", "")


def test_missing_log_has_exact_zero_status(tmp_path):
    r = reconcile(tmp_path / "missing.jsonl")
    assert (r.returncode, r.stdout, r.stderr) == (0, "total=0\nqueued=0\nrunning=0\ndone=0\nfailed=0\n", "")


def test_unreadable_log_has_exact_access_error(tmp_path):
    p = tmp_path / "directory.jsonl"
    p.mkdir()
    r = reconcile(p)
    assert (r.returncode, r.stdout, r.stderr) == (1, "", "eventlog: cannot access log\n")


def test_reconcile_lifecycle_counts_all_states(tmp_path):
    data = [ev("e-a", "created", "a", 1), ev("e-b", "started", "a", 2), ev("e-c", "completed", "a", 3), ev("e-d", "created", "b", 1), ev("e-e", "created", "c", 1), ev("e-f", "started", "c", 2), ev("e-g", "failed", "c", 3)]
    p = log(tmp_path, ("\n".join(map(line, data)) + "\n").encode())
    r = reconcile(p)
    assert (r.returncode, r.stdout, r.stderr) == (0, "total=3\nqueued=1\nrunning=0\ndone=1\nfailed=1\n", "")


def test_json_key_order_is_arbitrary(tmp_path):
    p = log(tmp_path, b'{"ts":1,"job":"alpha","type":"created","id":"e-a"}\n')
    assert reconcile(p).stdout == "total=1\nqueued=1\nrunning=0\ndone=0\nfailed=0\n"


def test_out_of_order_lines_replay_by_timestamp(tmp_path):
    data = [ev("e-c", "completed", "a", 3), ev("e-a", "created", "a", 1), ev("e-b", "started", "a", 2)]
    p = log(tmp_path, ("\n".join(map(line, data)) + "\n").encode())
    assert reconcile(p).stdout.endswith("done=1\nfailed=0\n")


def test_interleaved_jobs_are_independent(tmp_path):
    data = [ev("e-a", "created", "a", 1), ev("e-b", "created", "b", 1), ev("e-c", "started", "b", 2), ev("e-d", "failed", "b", 3)]
    p = log(tmp_path, ("\n".join(map(line, data)) + "\n").encode())
    assert reconcile(p).stdout == "total=2\nqueued=1\nrunning=0\ndone=0\nfailed=1\n"


def test_final_truncated_fragment_is_ignored(tmp_path):
    p = log(tmp_path, (line(ev("e-a", "created")) + "\n{" ).encode())
    assert reconcile(p).stdout == "total=1\nqueued=1\nrunning=0\ndone=0\nfailed=0\n"


def test_final_complete_line_without_newline_is_ignored(tmp_path):
    p = log(tmp_path, line(ev("e-a", "created")).encode())
    assert reconcile(p).stdout == "total=0\nqueued=0\nrunning=0\ndone=0\nfailed=0\n"


def test_invalid_json_has_line_error(tmp_path):
    p = log(tmp_path, b'{nope}\n')
    r = reconcile(p)
    assert (r.returncode, r.stdout, r.stderr) == (1, "", "eventlog:1: invalid event\n")


def test_unknown_event_type_has_exact_error(tmp_path):
    p = log(tmp_path, (line(ev("e-a", "paused")) + "\n").encode())
    r = reconcile(p)
    assert (r.returncode, r.stdout, r.stderr) == (1, "", "eventlog:1: unknown event type 'paused'\n")


def test_unknown_key_is_rejected(tmp_path):
    x = ev("e-a", "created") | {"extra": 5}
    p = log(tmp_path, (line(x) + "\n").encode())
    assert reconcile(p).stderr == "eventlog:1: invalid event\n"


def test_missing_key_is_rejected(tmp_path):
    x = ev("e-a", "created")
    del x["job"]
    p = log(tmp_path, (line(x) + "\n").encode())
    assert reconcile(p).stderr == "eventlog:1: invalid event\n"


def test_duplicate_event_id_is_rejected_at_second_line(tmp_path):
    x = line(ev("e-a", "created"))
    p = log(tmp_path, (x + "\n" + x + "\n").encode())
    r = reconcile(p)
    assert (r.returncode, r.stdout, r.stderr) == (1, "", "eventlog:2: duplicate event id 'e-a'\n")


def test_duplicate_json_object_key_is_invalid(tmp_path):
    p = log(tmp_path, b'{"id":"e-a","id":"e-b","type":"created","job":"alpha","ts":1}\n')
    assert reconcile(p).stderr == "eventlog:1: invalid event\n"


def test_timestamp_must_be_nonnegative_integer(tmp_path):
    p = log(tmp_path, b'{"id":"e-a","type":"created","job":"alpha","ts":-1}\n')
    assert reconcile(p).stderr == "eventlog:1: invalid event\n"


def test_transition_error_uses_offending_physical_line(tmp_path):
    data = [ev("e-a", "created", "alpha", 1), ev("e-b", "completed", "alpha", 2)]
    p = log(tmp_path, ("\n".join(map(line, data)) + "\n").encode())
    r = reconcile(p)
    assert (r.returncode, r.stdout, r.stderr) == (1, "", "eventlog:2: invalid transition for job 'alpha'\n")


def test_timestamp_tie_is_transition_error(tmp_path):
    data = [ev("e-a", "created", "alpha", 1), ev("e-b", "started", "alpha", 1)]
    p = log(tmp_path, ("\n".join(map(line, data)) + "\n").encode())
    assert reconcile(p).stderr == "eventlog:2: invalid transition for job 'alpha'\n"


def test_duplicate_job_creation_is_invalid_transition(tmp_path):
    data = [ev("e-a", "created", "alpha", 1), ev("e-b", "created", "alpha", 2)]
    p = log(tmp_path, ("\n".join(map(line, data)) + "\n").encode())
    assert reconcile(p).stderr == "eventlog:2: invalid transition for job 'alpha'\n"


def test_append_creates_compact_jsonl_and_reports_id(tmp_path):
    p = tmp_path / "new.jsonl"
    r = append(p, ev("e-a", "created"))
    assert (r.returncode, r.stdout, r.stderr) == (0, "appended e-a\n", "")
    assert p.read_text() == '{"id":"e-a","type":"created","job":"alpha","ts":1}\n'


def test_append_duplicate_existing_id_fails(tmp_path):
    p = log(tmp_path, (line(ev("e-a", "created")) + "\n").encode())
    r = append(p, ev("e-a", "started", ts=2))
    assert (r.returncode, r.stdout, r.stderr) == (1, "", "eventlog:1: duplicate event id 'e-a'\n")


def test_append_rejects_truncated_existing_log(tmp_path):
    p = log(tmp_path, b'{"partial"')
    r = append(p, ev("e-a", "created"))
    assert (r.returncode, r.stdout, r.stderr) == (1, "", "eventlog:1: invalid event\n")


def test_append_invalid_argument_event_is_exact(tmp_path):
    p = tmp_path / "new.jsonl"
    r = call("append", "--log", str(p), "--event", "not-json")
    assert (r.returncode, r.stdout, r.stderr) == (1, "", "eventlog:1: invalid event\n")


def test_usage_errors_are_exact(tmp_path):
    r = call("reconcile", "--log")
    assert (r.returncode, r.stdout, r.stderr) == (2, "", "eventlog: usage error\n")
