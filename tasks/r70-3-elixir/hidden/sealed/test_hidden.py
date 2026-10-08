"""Black-box acceptance suite for the public Round 70 Task 3 contract."""
from __future__ import annotations

import json
import os
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

BIN = os.environ["KOGEN_TASK_BIN"]


class Server:
    def __init__(self, plans: list[tuple[int, list[tuple[float, bytes]]]]):
        self.plans = plans
        self.requests: list[tuple[str, str, str, bytes]] = []
        self.lock = threading.Lock()
        plans_ref = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, _format: str, *_args: object) -> None:
                pass

            def do_POST(self) -> None:  # noqa: N802
                length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(length)
                with plans_ref.lock:
                    plans_ref.requests.append((self.command, self.path, self.headers.get("Content-Type", ""), self.headers.get("Accept", ""), body))
                    index = len(plans_ref.requests) - 1
                status, chunks = plans_ref.plans[min(index, len(plans_ref.plans) - 1)]
                if status < 0:
                    time.sleep(-status / 1000)
                    status = 200
                if status == 0:
                    self.close_connection = True
                    self.connection.close()
                    return
                self.send_response(status)
                if status in (301, 302, 303, 307, 308):
                    self.send_header("Location", "/redirect-target")
                self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                self.send_header("Connection", "close")
                self.end_headers()
                self.close_connection = True
                try:
                    for delay, chunk in chunks:
                        if delay:
                            time.sleep(delay)
                        self.wfile.write(chunk)
                        self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    pass

            def do_GET(self) -> None:  # noqa: N802
                with plans_ref.lock:
                    plans_ref.requests.append((self.command, self.path, self.headers.get("Content-Type", ""), self.headers.get("Accept", ""), b""))
                self.send_response(200)
                self.send_header("Content-Length", "0")
                self.end_headers()

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.httpd.server_port}/v1/chat"

    def close(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=2)


def event(value: object) -> bytes:
    return b"data: " + json.dumps(value, separators=(",", ":")).encode() + b"\n\n"


def done() -> bytes:
    return b"data: [DONE]\n\n"


def launch(server: Server | None, tmp_path: Path, extra: list[str] | None = None, prompt: str = "hello", timeout: int = 1000):
    usage = tmp_path / "nested" / "usage.json"
    argv = [BIN, "model", "--url", server.url if server else "http://127.0.0.1:1/", "--prompt", prompt,
            "--idle-timeout-ms", str(timeout), "--usage-file", str(usage)]
    if extra:
        argv.extend(extra)
    return subprocess.run(argv, capture_output=True, check=False), usage


def run_plan(tmp_path: Path, plan: list[tuple[int, list[tuple[float, bytes]]]], **kwargs):
    server = Server(plan)
    try:
        result, usage = launch(server, tmp_path, **kwargs)
        return result, usage, server.requests
    finally:
        server.close()


def assert_success(result: subprocess.CompletedProcess[bytes], usage: Path, stdout: bytes = b"answer\n", record: bytes = b'{"input_tokens":3,"output_tokens":4}\n') -> None:
    assert (result.returncode, result.stdout, result.stderr) == (0, stdout, b"")
    assert usage.read_bytes() == record


def assert_failure(result: subprocess.CompletedProcess[bytes], usage: Path, code: int = 5) -> None:
    assert (result.returncode, result.stdout, result.stderr) == (code, b"", b"error: request failed\n")
    assert not usage.exists()


def test_success_posts_contract_and_writes_compact_usage(tmp_path: Path) -> None:
    """Request method, path, media headers, compact body and atomic output formats."""
    payload = event({"type": "text", "text": "answer", "trace": "ignored"}) + b'data: {"type":"usage","input_tokens":99,"input_tokens":3e0,"output_tokens":4,"trace":"ignored"}\n\n' + done()
    result, usage, requests = run_plan(tmp_path, [(200, [(0, payload)])])
    assert_success(result, usage)
    assert len(requests) == 1
    method, path, content_type, accept, body = requests[0]
    assert (method, path, content_type, accept, body) == ("POST", "/v1/chat", "application/json", "text/event-stream", b'{"prompt":"hello"}')


def test_empty_prompt_is_sent_and_empty_text_has_lf(tmp_path: Path) -> None:
    """TEXT may be empty; successful empty generated text still has the required LF."""
    result, usage, requests = run_plan(tmp_path, [(200, [(0, event({"type": "text", "text": ""}) + event({"type": "usage", "input_tokens": 0, "output_tokens": 0}) + done())])], prompt="")
    assert_success(result, usage, b"\n", b'{"input_tokens":0,"output_tokens":0}\n')
    assert requests[0][4] == b'{"prompt":""}'


def test_prompt_json_escaping_is_utf8(tmp_path: Path) -> None:
    """The request prompt is JSON escaped and UTF-8 encoded."""
    prompt = 'café "x"\\\n'
    usage_before = tmp_path / "nested" / "usage.json"
    usage_before.parent.mkdir()
    usage_before.write_bytes(b"old record\n")
    result, usage, requests = run_plan(tmp_path, [(200, [(0, event({"type": "usage", "input_tokens": 1, "output_tokens": 2}) + done())])], prompt=prompt)
    assert_success(result, usage, b"\n", b'{"input_tokens":1,"output_tokens":2}\n')
    assert json.loads(requests[0][4]) == {"prompt": prompt}


def test_multiple_text_events_append_and_last_usage_wins(tmp_path: Path) -> None:
    """Text events append verbatim, while each valid usage event replaces the previous one."""
    payload = event({"type": "text", "text": "a"}) + event({"type": "usage", "input_tokens": 1, "output_tokens": 1}) + event({"type": "text", "text": "b\n"}) + event({"type": "usage", "input_tokens": 9, "output_tokens": 2}) + done()
    result, usage, _ = run_plan(tmp_path, [(200, [(0, payload)])])
    assert_success(result, usage, b"ab\n\n", b'{"input_tokens":9,"output_tokens":2}\n')


def test_multiline_data_and_one_optional_space(tmp_path: Path) -> None:
    """Data lines join with LF and remove no more than one optional leading space."""
    payload = b'data: {"type":"text",\n' + b'data:  "text":"ok"}\n\n' + event({"type": "usage", "input_tokens": 2, "output_tokens": 0}) + done()
    result, usage, _ = run_plan(tmp_path, [(200, [(0, payload)])])
    assert_success(result, usage, b"ok\n", b'{"input_tokens":2,"output_tokens":0}\n')


def test_comments_unknown_sse_fields_and_crlf(tmp_path: Path) -> None:
    """Comment/empty/unknown field lines are ignored and CRLF is accepted."""
    payload = b': heartbeat\r\nunknown: ignored\r\n\r\ndata: {"type":"usage","input_tokens":4,"output_tokens":5}\r\n\r\ndata: [DONE]\r\n\r\n'
    result, usage, _ = run_plan(tmp_path, [(200, [(0, payload)])])
    assert_success(result, usage, b"\n", b'{"input_tokens":4,"output_tokens":5}\n')


def test_unknown_json_event_type_is_ignored(tmp_path: Path) -> None:
    """Object types other than text and usage are ignored."""
    payload = event({"type": "metadata", "text": 17}) + event({"type": "usage", "input_tokens": 0, "output_tokens": 0}) + done()
    result, usage, _ = run_plan(tmp_path, [(200, [(0, payload)])])
    assert_success(result, usage, b"\n", b'{"input_tokens":0,"output_tokens":0}\n')


def test_done_ignores_later_malformed_records(tmp_path: Path) -> None:
    """A DONE record ends parsing immediately and requires preceding usage."""
    payload = event({"type": "usage", "input_tokens": 1, "output_tokens": 2}) + done() + b"data: {bad}\n\n"
    result, usage, _ = run_plan(tmp_path, [(200, [(0, payload)])])
    assert_success(result, usage, b"\n", b'{"input_tokens":1,"output_tokens":2}\n')


def test_idle_timeout_retries_once_with_identical_request(tmp_path: Path) -> None:
    """An idle timeout closes an attempt and causes exactly one identical retry."""
    valid = event({"type": "usage", "input_tokens": 2, "output_tokens": 3}) + done()
    result, usage, requests = run_plan(tmp_path, [(200, [(0.35, valid)]), (200, [(0, valid)])], timeout=120)
    assert_success(result, usage, b"\n", b'{"input_tokens":2,"output_tokens":3}\n')
    assert len(requests) == 2 and requests[0] == requests[1]


def test_header_timeout_retries_once(tmp_path: Path) -> None:
    """Waiting too long for response headers is retryable once."""
    valid = event({"type": "usage", "input_tokens": 2, "output_tokens": 3}) + done()
    result, usage, requests = run_plan(tmp_path, [(-350, []), (200, [(0, valid)])], timeout=120)
    assert_success(result, usage, b"\n", b'{"input_tokens":2,"output_tokens":3}\n')
    assert len(requests) == 2 and requests[0] == requests[1]


def test_body_idle_timeout_resets_between_chunks(tmp_path: Path) -> None:
    """Each received body chunk resets the idle clock even when total time exceeds it."""
    chunks = [
        b": heartbeat\n\n",
        b'data: {"type":"usage","input_tokens":',
        b'1,"output_tokens":2}\n\n',
        done(),
    ]
    result, usage, requests = run_plan(tmp_path, [(200, [(0.08, chunk) for chunk in chunks])], timeout=120)
    assert_success(result, usage, b"\n", b'{"input_tokens":1,"output_tokens":2}\n')
    assert len(requests) == 1


def test_http_5xx_retries_once(tmp_path: Path) -> None:
    """HTTP 5xx is retryable exactly once; retry preserves the request."""
    valid = event({"type": "usage", "input_tokens": 7, "output_tokens": 8}) + done()
    result, usage, requests = run_plan(tmp_path, [(503, [(0, b"busy")]), (200, [(0, valid)])])
    assert_success(result, usage, b"\n", b'{"input_tokens":7,"output_tokens":8}\n')
    assert len(requests) == 2 and requests[0] == requests[1]


def test_two_5xx_attempts_fail_without_usage_file(tmp_path: Path) -> None:
    """The second retryable failure is final and PATH remains absent."""
    result, usage, requests = run_plan(tmp_path, [(500, [(0, b"")]), (599, [(0, b"")])])
    assert_failure(result, usage)
    assert len(requests) == 2


def test_non_5xx_status_is_not_retried(tmp_path: Path) -> None:
    """A non-2xx, non-5xx response fails once without retry."""
    result, usage, requests = run_plan(tmp_path, [(429, [(0, b"no")])])
    assert_failure(result, usage)
    assert len(requests) == 1


def test_redirect_is_not_followed_or_retried(tmp_path: Path) -> None:
    """A 3xx response fails after the original POST without following Location."""
    valid = event({"type": "usage", "input_tokens": 1, "output_tokens": 1}) + done()
    result, usage, requests = run_plan(tmp_path, [(302, [(0, valid)])])
    assert_failure(result, usage)
    assert len(requests) == 1 and requests[0][0:2] == ("POST", "/v1/chat")


def test_malformed_sse_is_not_retried(tmp_path: Path) -> None:
    """Malformed event JSON is non-retriable even when a second plan could succeed."""
    valid = event({"type": "usage", "input_tokens": 1, "output_tokens": 1}) + done()
    result, usage, requests = run_plan(tmp_path, [(200, [(0, b"data: {bad}\n\n")]), (200, [(0, valid)])])
    assert_failure(result, usage)
    assert len(requests) == 1


@pytest.mark.parametrize("payload", [
    b"data: [DONE]\n\n",  # no usage
    event({"type": "usage", "input_tokens": 1, "output_tokens": 2}),  # no DONE
    b"data: []\n\ndata: [DONE]\n\n",  # non-object JSON
    event({"type": "text", "text": 1}) + done(),  # wrong text field type
    event({"type": "usage", "input_tokens": True, "output_tokens": 2}) + done(),  # boolean is not numeric
    event({"type": "usage", "input_tokens": 1.5, "output_tokens": 2}) + done(),  # fractional count
])
def test_invalid_streams_fail_and_preserve_existing_usage(tmp_path: Path, payload: bytes) -> None:
    """DONE/usage requirements and malformed object/text/usage values are failures."""
    usage = tmp_path / "nested" / "usage.json"
    usage.parent.mkdir()
    usage.write_bytes(b"keep-me\n")
    result, _, requests = run_plan(tmp_path, [(200, [(0, payload)])])
    assert (result.returncode, result.stdout, result.stderr) == (5, b"", b"error: request failed\n")
    assert usage.read_bytes() == b"keep-me\n"
    assert len(requests) == 1


def test_invalid_utf8_is_non_retriable(tmp_path: Path) -> None:
    """Response bytes must decode as strict UTF-8 and malformed encoding is not retried."""
    result, usage, requests = run_plan(tmp_path, [(200, [(0, b"data: \xff\n\n")]), (200, [(0, done())])])
    assert_failure(result, usage)
    assert len(requests) == 1


@pytest.mark.parametrize("bad", [
    ["--unknown", "x"],
    ["--url", "http://127.0.0.1", "--url", "http://127.0.0.1"],
    ["--idle-timeout-ms", "0"],
    ["extra"],
])
def test_invalid_arguments_are_exact_and_do_not_connect(tmp_path: Path, bad: list[str]) -> None:
    """Unknown/duplicate/range/extra arguments use the exact CLI error and exit 2."""
    result, usage = launch(None, tmp_path, extra=bad)
    assert (result.returncode, result.stdout, result.stderr) == (2, b"", b"error: invalid arguments\n")
    assert not usage.exists()


def test_connection_failure_retries_once(tmp_path: Path) -> None:
    """A dropped connection is retried exactly once with the identical request."""
    valid = event({"type": "usage", "input_tokens": 1, "output_tokens": 2}) + done()
    result, usage, requests = run_plan(tmp_path, [(0, []), (200, [(0, valid)])])
    assert_success(result, usage, b"\n", b'{"input_tokens":1,"output_tokens":2}\n')
    assert len(requests) == 2 and requests[0] == requests[1]
