"""Black-box tests for the public Agent loop CLI clauses."""
from __future__ import annotations

import json
import os
import socket
import subprocess
import threading
import time
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest


@dataclass
class Plan:
    status: int = 200
    chunks: list[tuple[float, bytes]] = field(default_factory=list)
    initial_delay: float = 0.0
    drop: bool = False


class FakeServer:
    """An in-process loopback-only Responses-style scripted SSE server."""

    def __init__(self, plans: list[Plan]):
        self.plans = list(plans)
        self.requests: list[dict[str, Any]] = []
        self.lock = threading.Lock()
        owner = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, _format: str, *_args: Any) -> None:
                return

            def do_POST(self) -> None:
                length = int(self.headers.get("Content-Length", "0"))
                raw = self.rfile.read(length)
                with owner.lock:
                    owner.requests.append(
                        {
                            "path": self.path,
                            "body": raw,
                            "session": self.headers.get("X-Session-ID"),
                            "accept": self.headers.get("Accept"),
                            "content_type": self.headers.get("Content-Type"),
                            "at": time.monotonic(),
                        }
                    )
                    plan = owner.plans.pop(0) if owner.plans else Plan(status=500)
                if plan.drop:
                    self.close_connection = True
                    try:
                        self.connection.shutdown(socket.SHUT_RDWR)
                    except OSError:
                        pass
                    self.connection.close()
                    return
                self.send_response(plan.status)
                self.send_header("Connection", "close")
                if plan.status == 200:
                    self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                else:
                    self.send_header("Content-Length", "0")
                self.end_headers()
                if plan.initial_delay:
                    time.sleep(plan.initial_delay)
                for delay, chunk in plan.chunks:
                    if delay:
                        time.sleep(delay)
                    try:
                        self.wfile.write(chunk)
                        self.wfile.flush()
                    except (BrokenPipeError, ConnectionResetError, OSError):
                        break
                self.close_connection = True

        class Server(ThreadingHTTPServer):
            daemon_threads = True
            allow_reuse_address = True

        self.server = Server(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        self.url = f"http://127.0.0.1:{self.server.server_port}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self) -> FakeServer:
        self.thread.start()
        return self

    def __exit__(self, *_args: Any) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)


def frame(name: str, data: dict[str, Any], *, crlf: bool = False) -> bytes:
    eol = "\r\n" if crlf else "\n"
    text = f"event: {name}{eol}data: {json.dumps(data, ensure_ascii=False, separators=(',', ':'))}{eol}{eol}"
    return text.encode("utf-8")


def complete(usage: dict[str, int] | None = None) -> bytes:
    if usage is None:
        usage = {"input_tokens": 10, "output_tokens": 3, "cached_tokens": 7}
    return frame(
        "response.completed",
        {
            "usage": {
                "input_tokens": usage["input_tokens"],
                "output_tokens": usage["output_tokens"],
                "input_tokens_details": {"cached_tokens": usage["cached_tokens"]},
            }
        },
    )


def text_plan(text: str, usage: dict[str, int] | None = None) -> Plan:
    parts = [text[: max(1, len(text) // 2)], text[max(1, len(text) // 2) :]]
    chunks = [(0.0, frame("response.output_text.delta", {"delta": part})) for part in parts if part]
    chunks.append((0.0, complete(usage)))
    return Plan(chunks=chunks)


def call_plan(calls: list[tuple[str, str, dict[str, Any]]]) -> Plan:
    chunks: list[tuple[float, bytes]] = []
    for call_id, name, arguments in calls:
        raw = json.dumps(arguments, ensure_ascii=False, separators=(",", ":"))
        split = max(1, len(raw) // 2)
        for delta in (raw[:split], raw[split:]):
            if delta:
                chunks.append(
                    (0.0, frame("response.function_call_arguments.delta", {"call_id": call_id, "name": name, "delta": delta}))
                )
    chunks.append((0.0, complete()))
    return Plan(chunks=chunks)


def input_raw(request: dict[str, Any]) -> str:
    body = request["body"].decode("utf-8")
    marker = '"input":'
    start = body.index(marker) + len(marker)
    value, _end = json.JSONDecoder().raw_decode(body, start)
    assert isinstance(value, list)
    return body[start : _end]


def base_args(server: FakeServer, root: Path, extra: list[str] | None = None) -> list[str]:
    workdir = root / "work"
    workdir.mkdir(parents=True, exist_ok=True)
    prompt = root / "prompt.txt"
    prompt.write_text("Find the answer.\n", encoding="utf-8")
    records = root / "records.jsonl"
    return [
        "loop",
        "run",
        "--prompt-file",
        str(prompt),
        "--server",
        server.url,
        "--records",
        str(records),
        "--workdir",
        str(workdir),
        *(extra or []),
    ]


def invoke(args: list[str], *, cwd: Path, timeout: float = 4.0) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    assert env.get("KOGEN_TASK_BIN"), "worker control must set KOGEN_TASK_BIN"
    return subprocess.run(
        [env["KOGEN_TASK_BIN"], *args],
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def records(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def outputs(request: dict[str, Any]) -> list[str]:
    return [item["output"] for item in json.loads(request["body"])["input"] if item.get("type") == "function_call_output"]


def test_final_text_is_exact_and_records_usage_and_request_size(tmp_path: Path) -> None:
    """Covers final answer bytes, endpoint/headers, body contract and JSONL fields."""
    answer = "København ✓"
    usage = {"input_tokens": 31, "output_tokens": 4, "cached_tokens": 28}
    with FakeServer([text_plan(answer, usage)]) as server:
        args = base_args(server, tmp_path, ["--session", "stable.session-1"])
        result = invoke(args, cwd=tmp_path)
    assert result.returncode == 0
    assert result.stdout == answer.encode("utf-8")
    assert result.stderr == b""
    assert len(server.requests) == 1
    request = server.requests[0]
    assert request["path"] == "/v1/responses"
    assert request["accept"] == "text/event-stream"
    assert request["content_type"] == "application/json"
    assert request["session"] == "stable.session-1"
    body = json.loads(request["body"])
    assert body["model"] == "fake-agent" and body["stream"] is True
    assert [tool["name"] for tool in body["tools"]] == ["read_file", "run_command"]
    assert body["input"][0] == {"role": "user", "content": [{"type": "input_text", "text": "Find the answer.\n"}]}
    rows = records(tmp_path / "records.jsonl")
    assert len(rows) == 1
    row = rows[0]
    assert set(row) == {"start_ms", "first_byte_ms", "end_ms", "outcome", "retries", "usage", "request_bytes", "history_items"}
    assert row["outcome"] == "ok" and row["retries"] == 0
    assert row["usage"] == {"input_tokens": 31, "output_tokens": 4, "cached_tokens": 28}
    assert row["request_bytes"] == len(request["body"])
    assert row["history_items"] == 1
    assert row["start_ms"] <= row["first_byte_ms"] <= row["end_ms"]


def test_required_command_line_is_enforced(tmp_path: Path) -> None:
    """Covers the single accepted command shape and exact usage failure."""
    env = os.environ.copy()
    result = subprocess.run([env["KOGEN_TASK_BIN"], "loop", "run"], cwd=tmp_path, env=env, capture_output=True)
    assert result.returncode == 2
    assert result.stdout == b""
    assert result.stderr == b"loop: invalid command line\n"


def test_unknown_options_duplicates_and_local_io_failures_are_exact(tmp_path: Path) -> None:
    """Covers CLI errors plus exact prompt, workdir and records file failures."""
    with FakeServer([text_plan("unused")]) as server:
        args = base_args(server, tmp_path, ["--unknown", "x"])
        unknown = invoke(args, cwd=tmp_path)
        args = base_args(server, tmp_path, ["--session", "one", "--session", "two"])
        duplicate = invoke(args, cwd=tmp_path)
        args = base_args(server, tmp_path, ["--first-byte-timeout-ms", "0"])
        invalid_timeout = invoke(args, cwd=tmp_path)
        args = base_args(server, tmp_path)
        prompt_index = args.index("--prompt-file") + 1
        args[prompt_index] = str(tmp_path / "missing-prompt.txt")
        missing_prompt = invoke(args, cwd=tmp_path)
        args = base_args(server, tmp_path)
        workdir_index = args.index("--workdir") + 1
        args[workdir_index] = str(tmp_path / "missing-workdir")
        missing_workdir = invoke(args, cwd=tmp_path)
        args = base_args(server, tmp_path)
        records_index = args.index("--records") + 1
        args[records_index] = str(tmp_path / "absent" / "records.jsonl")
        bad_records = invoke(args, cwd=tmp_path)
    for result in (unknown, duplicate, invalid_timeout):
        assert result.returncode == 2
        assert result.stdout == b""
        assert result.stderr == b"loop: invalid command line\n"
    assert missing_prompt.returncode == 1 and missing_prompt.stdout == b"" and missing_prompt.stderr == b"loop: cannot read prompt file\n"
    assert missing_workdir.returncode == 1 and missing_workdir.stdout == b"" and missing_workdir.stderr == b"loop: invalid workdir\n"
    assert bad_records.returncode == 1 and bad_records.stdout == b"" and bad_records.stderr == b"loop: cannot write records file\n"
    assert not server.requests


def test_read_file_tool_appends_result_then_returns_final_text(tmp_path: Path) -> None:
    """Covers read_file, tool result history, another request and exact final output."""
    work = tmp_path / "work"
    work.mkdir()
    (work / "notes.txt").write_text("alpha\nbeta\n", encoding="utf-8")
    plans = [call_plan([("c1", "read_file", {"path": "notes.txt"})]), text_plan("done")]
    with FakeServer(plans) as server:
        result = invoke(base_args(server, tmp_path), cwd=tmp_path)
    assert result.returncode == 0 and result.stdout == b"done" and result.stderr == b""
    assert len(server.requests) == 2
    history = json.loads(server.requests[1]["body"])["input"]
    assert history[-2] == {"type": "function_call", "call_id": "c1", "name": "read_file", "arguments": '{"path":"notes.txt"}'}
    assert history[-1] == {"type": "function_call_output", "call_id": "c1", "output": "alpha\nbeta\n"}


def test_run_command_uses_workdir_and_declared_environment(tmp_path: Path) -> None:
    """Covers command execution, workdir, PATH/HOME/LANG and result JSON shape."""
    plans = [call_plan([("cmd1", "run_command", {"command": "printf '%s|%s|%s' \"$PWD\" \"$HOME\" \"$PATH\""})]), text_plan("ok")]
    with FakeServer(plans) as server:
        result = invoke(base_args(server, tmp_path), cwd=tmp_path)
    assert result.returncode == 0 and result.stdout == b"ok"
    work = str(tmp_path / "work")
    expected = json.dumps({"exit_code": 0, "stdout": f"{work}|{work}|/usr/bin:/bin", "stderr": ""}, separators=(",", ":"))
    assert outputs(server.requests[1]) == [expected]


def test_multiple_tool_calls_execute_in_emitted_order(tmp_path: Path) -> None:
    """Covers preserving call order and appending each call/result pair."""
    (tmp_path / "work").mkdir()
    (tmp_path / "work" / "a.txt").write_text("A", encoding="utf-8")
    (tmp_path / "work" / "b.txt").write_text("B", encoding="utf-8")
    first = call_plan([("a", "read_file", {"path": "a.txt"}), ("b", "read_file", {"path": "b.txt"})])
    with FakeServer([first, text_plan("AB")]) as server:
        result = invoke(base_args(server, tmp_path), cwd=tmp_path)
    assert result.returncode == 0 and result.stdout == b"AB"
    history = json.loads(server.requests[1]["body"])["input"]
    assert [item.get("call_id") for item in history[1:]] == ["a", "a", "b", "b"]
    assert [item.get("output") for item in history if item.get("type") == "function_call_output"] == ["A", "B"]


def test_explicit_session_id_is_constant_across_turns(tmp_path: Path) -> None:
    """Covers X-Session-ID stability for every request in one conversation."""
    (tmp_path / "work").mkdir()
    (tmp_path / "work" / "x").write_text("x", encoding="utf-8")
    with FakeServer([call_plan([("a", "read_file", {"path": "x"})]), text_plan("x")]) as server:
        result = invoke(base_args(server, tmp_path, ["--session", "chosen-ID:42"]), cwd=tmp_path)
    assert result.returncode == 0
    assert [request["session"] for request in server.requests] == ["chosen-ID:42", "chosen-ID:42"]


def test_generated_sessions_differ_for_parallel_conversations(tmp_path: Path) -> None:
    """Covers one generated stable key per simultaneous CLI conversation."""
    with FakeServer([text_plan("a"), text_plan("b")]) as server:
        args_a = base_args(server, tmp_path / "a")
        args_b = base_args(server, tmp_path / "b")
        results: list[subprocess.CompletedProcess[bytes]] = []
        threads = [threading.Thread(target=lambda a=a: results.append(invoke(a, cwd=tmp_path))) for a in (args_a, args_b)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=5)
    assert len(results) == 2 and all(result.returncode == 0 for result in results)
    keys = [request["session"] for request in server.requests]
    assert len(keys) == 2 and all(keys) and len(set(keys)) == 2


def test_input_history_serialization_is_a_byte_prefix(tmp_path: Path) -> None:
    """Covers append-only history at the serialized JSON bytes seen by the server."""
    (tmp_path / "work").mkdir()
    (tmp_path / "work" / "x").write_text("x", encoding="utf-8")
    with FakeServer([call_plan([("a", "read_file", {"path": "x"})]), text_plan("x")]) as server:
        result = invoke(base_args(server, tmp_path), cwd=tmp_path)
    assert result.returncode == 0
    before, after = map(input_raw, server.requests)
    assert after.startswith(before[:-1] + ",")


def test_first_byte_timeout_retries_then_recovers(tmp_path: Path) -> None:
    """Covers first-body-byte timeout classification, retry index and recovery."""
    delayed = Plan(initial_delay=0.18, chunks=[(0, text_plan("late").chunks[0][1]), (0, complete())])
    with FakeServer([delayed, text_plan("ready")]) as server:
        extra = ["--first-byte-timeout-ms", "60", "--idle-timeout-ms", "300", "--max-retries", "1", "--backoff-ms", "0"]
        result = invoke(base_args(server, tmp_path, extra), cwd=tmp_path)
    assert result.returncode == 0 and result.stdout == b"ready"
    rows = records(tmp_path / "records.jsonl")
    assert [row["outcome"] for row in rows] == ["timeout", "ok"]
    assert [row["retries"] for row in rows] == [0, 1]
    assert rows[0]["first_byte_ms"] is None and rows[0]["usage"]["input_tokens"] is None


def test_first_byte_timeout_exhaustion_has_exact_failure(tmp_path: Path) -> None:
    """Covers bounded retries and the first-byte timeout exit contract."""
    plans = [Plan(initial_delay=0.16, chunks=[(0, frame("response.output_text.delta", {"delta": "late"}))]) for _ in range(2)]
    with FakeServer(plans) as server:
        extra = ["--first-byte-timeout-ms", "40", "--max-retries", "1", "--backoff-ms", "0"]
        result = invoke(base_args(server, tmp_path, extra), cwd=tmp_path, timeout=3)
    assert result.returncode == 10 and result.stdout == b""
    assert result.stderr == b"loop: first-byte timeout\n"
    assert [row["outcome"] for row in records(tmp_path / "records.jsonl")] == ["timeout", "timeout"]


def test_idle_stall_retries_then_recovers(tmp_path: Path) -> None:
    """Covers idle stall after a body byte, retry, and per-attempt records."""
    stalled = Plan(chunks=[(0, frame("response.output_text.delta", {"delta": "part"})), (0.2, complete())])
    with FakeServer([stalled, text_plan("whole")]) as server:
        extra = ["--first-byte-timeout-ms", "300", "--idle-timeout-ms", "60", "--max-retries", "1", "--backoff-ms", "0"]
        result = invoke(base_args(server, tmp_path, extra), cwd=tmp_path)
    assert result.returncode == 0 and result.stdout == b"whole"
    rows = records(tmp_path / "records.jsonl")
    assert [row["outcome"] for row in rows] == ["stall", "ok"]
    assert rows[0]["first_byte_ms"] is not None


def test_comment_keepalive_bytes_reset_idle_timer(tmp_path: Path) -> None:
    """Covers the rule that ignored SSE comment bytes still reset idle timeout."""
    chunks = [(0.04, b": keepalive\n\n") for _ in range(4)]
    chunks += [(0.0, frame("response.output_text.delta", {"delta": "kept"})), (0.0, complete())]
    with FakeServer([Plan(chunks=chunks)]) as server:
        extra = ["--first-byte-timeout-ms", "300", "--idle-timeout-ms", "90", "--max-retries", "0"]
        result = invoke(base_args(server, tmp_path, extra), cwd=tmp_path, timeout=3)
    assert result.returncode == 0 and result.stdout == b"kept"
    assert records(tmp_path / "records.jsonl")[0]["outcome"] == "ok"


def test_idle_stall_exhaustion_has_exact_failure(tmp_path: Path) -> None:
    """Covers bounded retries and the idle-stall exit contract."""
    stalled = Plan(chunks=[(0, b": first byte\n\n"), (0.18, complete())])
    with FakeServer([stalled, stalled]) as server:
        extra = ["--first-byte-timeout-ms", "250", "--idle-timeout-ms", "40", "--max-retries", "1", "--backoff-ms", "0"]
        result = invoke(base_args(server, tmp_path, extra), cwd=tmp_path, timeout=3)
    assert result.returncode == 11 and result.stdout == b""
    assert result.stderr == b"loop: stream stalled\n"
    rows = records(tmp_path / "records.jsonl")
    assert [row["outcome"] for row in rows] == ["stall", "stall"]


def test_transport_error_retries_same_request(tmp_path: Path) -> None:
    """Covers a dropped connection, transport outcome and unchanged retry body."""
    with FakeServer([Plan(drop=True), text_plan("recovered")]) as server:
        extra = ["--max-retries", "1", "--backoff-ms", "0"]
        result = invoke(base_args(server, tmp_path, extra), cwd=tmp_path)
    assert result.returncode == 0 and result.stdout == b"recovered"
    assert len(server.requests) == 2
    assert server.requests[0]["body"] == server.requests[1]["body"]
    assert server.requests[0]["session"] == server.requests[1]["session"]
    assert [row["outcome"] for row in records(tmp_path / "records.jsonl")] == ["transport", "ok"]


def test_overload_retries_with_exponential_backoff(tmp_path: Path) -> None:
    """Covers 5xx/429 overload retries, ordering and 1x then 2x backoff."""
    with FakeServer([Plan(status=503), Plan(status=429), text_plan("ok")]) as server:
        extra = ["--max-retries", "2", "--backoff-ms", "80"]
        result = invoke(base_args(server, tmp_path, extra), cwd=tmp_path)
    assert result.returncode == 0 and result.stdout == b"ok"
    arrivals = [request["at"] for request in server.requests]
    assert len(arrivals) == 3
    gap1, gap2 = arrivals[1] - arrivals[0], arrivals[2] - arrivals[1]
    assert gap1 >= 0.06 and gap2 >= 0.13 and gap2 > gap1
    assert [row["outcome"] for row in records(tmp_path / "records.jsonl")] == ["overload", "overload", "ok"]
    assert [row["retries"] for row in records(tmp_path / "records.jsonl")] == [0, 1, 2]


def test_retry_limit_is_bounded_and_reports_overload(tmp_path: Path) -> None:
    """Covers final overload exit after exactly max-retries plus one attempts."""
    with FakeServer([Plan(status=503), Plan(status=500)]) as server:
        extra = ["--max-retries", "1", "--backoff-ms", "0"]
        result = invoke(base_args(server, tmp_path, extra), cwd=tmp_path)
    assert result.returncode == 13 and result.stdout == b""
    assert result.stderr == b"loop: server overloaded\n"
    assert len(server.requests) == 2
    assert [row["outcome"] for row in records(tmp_path / "records.jsonl")] == ["overload", "overload"]


def test_rejected_http_status_is_not_retried(tmp_path: Path) -> None:
    """Covers non-200 non-retryable status, exact stderr and record outcome."""
    with FakeServer([Plan(status=400), text_plan("unused")]) as server:
        result = invoke(base_args(server, tmp_path, ["--max-retries", "5"]), cwd=tmp_path)
    assert result.returncode == 14 and result.stdout == b""
    assert result.stderr == b"loop: server rejected request\n"
    assert len(server.requests) == 1
    row = records(tmp_path / "records.jsonl")[0]
    assert row["outcome"] == "transport" and row["retries"] == 0


def test_invalid_sse_response_has_exact_failure(tmp_path: Path) -> None:
    """Covers malformed/unknown SSE events and no retry for invalid responses."""
    invalid = Plan(chunks=[(0, frame("response.unknown", {"x": 1}))])
    with FakeServer([invalid, text_plan("unused")]) as server:
        result = invoke(base_args(server, tmp_path, ["--max-retries", "3"]), cwd=tmp_path)
    assert result.returncode == 15 and result.stdout == b""
    assert result.stderr == b"loop: invalid response\n"
    assert len(server.requests) == 1
    assert records(tmp_path / "records.jsonl")[0]["outcome"] == "transport"


def test_read_file_rejects_paths_outside_workdir(tmp_path: Path) -> None:
    """Covers canonical workdir confinement and tool failure exit behavior."""
    (tmp_path / "work").mkdir()
    (tmp_path / "secret.txt").write_text("secret", encoding="utf-8")
    with FakeServer([call_plan([("escape", "read_file", {"path": "../secret.txt"})]), text_plan("unused")]) as server:
        result = invoke(base_args(server, tmp_path), cwd=tmp_path)
    assert result.returncode == 16 and result.stdout == b""
    assert result.stderr == b"loop: tool execution failed\n"
    assert len(server.requests) == 1
    assert records(tmp_path / "records.jsonl")[0]["outcome"] == "ok"


def test_run_command_rejects_absolute_and_parent_paths(tmp_path: Path) -> None:
    """Covers run_command path checks before invoking a local shell command."""
    for command in ("cat ../secret", "cat /etc/passwd"):
        with FakeServer([call_plan([("escape", "run_command", {"command": command})])]) as server:
            result = invoke(base_args(server, tmp_path), cwd=tmp_path)
        assert result.returncode == 16 and result.stdout == b""
        assert result.stderr == b"loop: tool execution failed\n"
        assert len(server.requests) == 1


def test_run_command_timeout_is_a_tool_failure(tmp_path: Path) -> None:
    """Covers the documented five-second local command limit."""
    with FakeServer([call_plan([("slow", "run_command", {"command": "sleep 6"})])]) as server:
        result = invoke(base_args(server, tmp_path), cwd=tmp_path, timeout=8)
    assert result.returncode == 16 and result.stdout == b""
    assert result.stderr == b"loop: tool execution failed\n"
    assert len(server.requests) == 1


def test_records_file_is_replaced_and_each_attempt_has_one_line(tmp_path: Path) -> None:
    """Covers truncation at run start and exactly one JSONL row per HTTP attempt."""
    records_path = tmp_path / "records.jsonl"
    records_path.write_text("old record\n", encoding="utf-8")
    with FakeServer([Plan(status=502), text_plan("new")]) as server:
        args = base_args(server, tmp_path, ["--max-retries", "1", "--backoff-ms", "0"])
        result = invoke(args, cwd=tmp_path)
    assert result.returncode == 0
    rows = records(records_path)
    assert len(rows) == len(server.requests) == 2
    assert [row["outcome"] for row in rows] == ["overload", "ok"]
    assert all(row["request_bytes"] == len(request["body"]) for row, request in zip(rows, server.requests, strict=True))
    assert all(row["history_items"] == 1 for row in rows)
    assert all(row["start_ms"] <= row["end_ms"] for row in rows)


def test_retry_body_is_identical_and_retry_cache_key_is_stable(tmp_path: Path) -> None:
    """Covers exact request reuse, stable session key and retry records."""
    with FakeServer([Plan(status=503), text_plan("ok")]) as server:
        args = base_args(server, tmp_path, ["--session", "cache-1", "--max-retries", "1", "--backoff-ms", "0"])
        result = invoke(args, cwd=tmp_path)
    assert result.returncode == 0
    assert server.requests[0]["body"] == server.requests[1]["body"]
    assert [request["session"] for request in server.requests] == ["cache-1", "cache-1"]
    rows = records(tmp_path / "records.jsonl")
    assert [row["retries"] for row in rows] == [0, 1]
    assert rows[0]["usage"] == {"input_tokens": None, "output_tokens": None, "cached_tokens": None}

def test_transport_exhaustion_has_exact_failure(tmp_path: Path) -> None:
    """Covers bounded dropped-connection retries and the transport exit contract."""
    with FakeServer([Plan(drop=True), Plan(drop=True)]) as server:
        extra = ["--max-retries", "1", "--backoff-ms", "0"]
        result = invoke(base_args(server, tmp_path, extra), cwd=tmp_path)
    assert result.returncode == 12 and result.stdout == b""
    assert result.stderr == b"loop: transport error\n"
    assert len(server.requests) == 2
    assert [row["outcome"] for row in records(tmp_path / "records.jsonl")] == ["transport", "transport"]

