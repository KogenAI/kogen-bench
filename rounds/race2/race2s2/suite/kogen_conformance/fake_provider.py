"""Loopback Responses SSE provider used by black-box conformance cases.

The request route is the backend Responses route used by Kogen. The server
accepts any path ending in ``/responses`` so it can serve both the owned
``/backend-api/codex/responses`` and injected ``/v1/responses`` routes.
"""

from __future__ import annotations

import base64
import hashlib
import http.server
import json
import random
import socketserver
import threading
import time
import urllib.parse
from typing import Any


DEFAULT_USAGE = {
    "input_tokens": 120,
    "input_tokens_details": {"cached_tokens": 20},
    "output_tokens": 30,
    "output_tokens_details": {"reasoning_tokens": 10},
    "total_tokens": 150,
}
OAUTH_SCOPE = "openid profile email offline_access resource.invoke chatgpt.tokens.use.direct"
OAUTH_KID = "kogen-conformance-fake"
_RSA_LOCK = threading.Lock()
_RSA_KEY: tuple[int, int, int] | None = None
_SHA256_PREFIX = bytes.fromhex("3031300d060960864801650304020105000420")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _int_bytes(number: int) -> bytes:
    return number.to_bytes((number.bit_length() + 7) // 8, "big")


def _is_probable_prime(number: int, rng: random.SystemRandom, rounds: int = 32) -> bool:
    if number < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if number % prime == 0:
            return number == prime
    d, shifts = number - 1, 0
    while d % 2 == 0:
        d //= 2
        shifts += 1
    for _ in range(rounds):
        value = pow(rng.randrange(2, number - 2), d, number)
        if value in (1, number - 1):
            continue
        for _ in range(shifts - 1):
            value = pow(value, 2, number)
            if value == number - 1:
                break
        else:
            return False
    return True


def _prime(bits: int, rng: random.SystemRandom) -> int:
    while True:
        candidate = rng.getrandbits(bits) | (1 << (bits - 1)) | (1 << (bits - 2)) | 1
        if _is_probable_prime(candidate, rng):
            return candidate


def _rsa_key() -> tuple[int, int, int]:
    global _RSA_KEY
    with _RSA_LOCK:
        if _RSA_KEY is None:
            rng = random.SystemRandom()
            exponent = 65537
            while True:
                p, q = _prime(1024, rng), _prime(1024, rng)
                if p == q:
                    continue
                try:
                    private = pow(exponent, -1, (p - 1) * (q - 1))
                except ValueError:
                    continue
                modulus = p * q
                if modulus.bit_length() == 2048:
                    _RSA_KEY = modulus, exponent, private
                    break
        return _RSA_KEY


def _signed_jwt(claims: dict[str, Any]) -> str:
    modulus, exponent, private = _rsa_key()
    header = {"alg": "RS256", "typ": "JWT", "kid": OAUTH_KID}
    signing = (_b64url(json.dumps(header, separators=(",", ":")).encode()) + "." +
               _b64url(json.dumps(claims, separators=(",", ":")).encode())).encode("ascii")
    digest_info = _SHA256_PREFIX + hashlib.sha256(signing).digest()
    size = (modulus.bit_length() + 7) // 8
    encoded = b"\x00\x01" + b"\xff" * (size - len(digest_info) - 3) + b"\x00" + digest_info
    signature = pow(int.from_bytes(encoded, "big"), private, modulus).to_bytes(size, "big")
    return signing.decode("ascii") + "." + _b64url(signature)


def _unsigned_jwt(claims: dict[str, Any]) -> str:
    header = _b64url(b'{"alg":"none","typ":"JWT"}')
    payload = _b64url(json.dumps(claims, separators=(",", ":")).encode())
    return f"{header}.{payload}.{_b64url(b'fake')}"


def make_injected_auth(path: str, account_id: str = "acct_kogen_conformance") -> None:
    claims = {
        "iss": "https://auth.openai.com",
        "sub": "kogen-conformance-user",
        "iat": int(time.time()),
        "exp": int(time.time()) + 86_400,
        "https://api.openai.com/auth": {
            "chatgpt_account_id": account_id,
            "chatgpt_plan_type": "plus",
        },
    }
    with open(path, "w", encoding="utf-8") as auth_file:
        json.dump({"tokens": {"access_token": _unsigned_jwt(claims), "account_id": account_id}}, auth_file)
    try:
        import os
        os.chmod(path, 0o600)
    except OSError:
        pass


class FakeProviderState:
    def __init__(self, script: list[dict[str, Any]] | None = None, stream_delay_ms: int = 0):
        self.lock = threading.RLock()
        self.script = [dict(row) for row in (script or [])]
        self.cursor = 0
        self.requests: list[dict[str, Any]] = []
        self.oauth_requests: list[dict[str, Any]] = []
        self.stream_delay_ms = max(0, int(stream_delay_ms))
        self.next_response_id = 1
        self.oauth_config: dict[str, Any] = {
            "subject": "kogen-conformance-user",
            "email": "kogen-conformance@invalid.example",
            "account_id": "acct_kogen_conformance",
            "access_token": "kogen-fake-access",
            "refresh_token": "kogen-fake-refresh",
            "expires_in": 3600,
        }
        self.active_script_id: str | None = None
        self.gate_arrivals: dict[str, threading.Event] = {}
        self.gate_releases: dict[str, threading.Event] = {}
        self.oidc_script: str | None = None
        self.oidc_authorization: dict[str, str] | None = None
        self.oidc_code = "kogen-conformance-authorization-code"

    def configure_script(self, script_id: str, script: list[dict[str, Any]]) -> None:
        with self.lock:
            self.script = [dict(row) for row in script]
            self.cursor = 0
            self.requests = []
            self.next_response_id = 1
            self.active_script_id = script_id
            gate_names = {str(row["gate"]) for row in script if row.get("gate")}
            self.gate_arrivals = {name: threading.Event() for name in gate_names}
            self.gate_releases = {name: threading.Event() for name in gate_names}

    def configure_openid(self, script_id: str, account_id: str, label: str) -> None:
        with self.lock:
            self.oidc_script = script_id
            self.oidc_authorization = None
            self.oidc_code = "kogen-conformance-" + script_id + "-code"
            self.oauth_config.update({
                "subject": "kogen-conformance-" + label,
                "email": label + "@invalid.example",
                "account_id": account_id,
                "access_token": "kogen-fake-access-" + label,
                "refresh_token": "kogen-fake-refresh-" + label,
                "expires_in": 3600,
            })

    def wait_gate(self, script_id: str, label: str, timeout_s: float) -> bool:
        with self.lock:
            if script_id != self.active_script_id or label not in self.gate_arrivals:
                return False
            arrived = self.gate_arrivals[label]
        return arrived.wait(max(0.0, timeout_s))

    def release_gate(self, script_id: str, label: str) -> bool:
        with self.lock:
            if script_id != self.active_script_id or label not in self.gate_releases:
                return False
            released = self.gate_releases[label]
        released.set()
        return True

    def remaining(self) -> list[int]:
        with self.lock:
            return list(range(self.cursor + 1, len(self.script) + 1))

    def all_requests(self) -> list[dict[str, Any]]:
        with self.lock:
            return json.loads(json.dumps(self.requests))

    def all_oauth_requests(self) -> list[dict[str, Any]]:
        with self.lock:
            return json.loads(json.dumps(self.oauth_requests))

    def take(self, record: dict[str, Any]) -> dict[str, Any] | None:
        with self.lock:
            index = self.cursor
            self.requests.append(record)
            if index >= len(self.script):
                record["script_index"] = None
                record["script_error"] = "no scripted provider response remains"
                return None
            item = self.script[index]
            self.cursor += 1
            record["script_index"] = index
            expected = item.get("expect") or {}
            mismatches = _expectation_mismatches(record, expected)
            if mismatches:
                record["script_error"] = mismatches
                return None
            return item


def _expectation_mismatches(actual: Any, expected: Any, path: str = "") -> list[str]:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [f"{path or '$'} expected an object"]
        out: list[str] = []
        for key, value in expected.items():
            if key not in actual:
                out.append(f"{path}/{key} is missing")
            else:
                out.extend(_expectation_mismatches(actual[key], value, f"{path}/{key}"))
        return out
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) < len(expected):
            return [f"{path or '$'} does not contain the expected list prefix"]
        out = []
        for index, value in enumerate(expected):
            out.extend(_expectation_mismatches(actual[index], value, f"{path}/{index}"))
        return out
    if actual != expected:
        return [f"{path or '$'} expected {expected!r}, got {actual!r}"]
    return []


class FakeProvider:
    def __init__(self, script: list[dict[str, Any]] | None = None, stream_delay_ms: int = 0):
        self.state = FakeProviderState(script, stream_delay_ms)
        self._server: http.server.ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None
        self.url = ""

    def start(self) -> "FakeProvider":
        state = self.state

        class Handler(http.server.BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, _format: str, *_args: Any) -> None:
                return

            def _body(self) -> bytes:
                length = int(self.headers.get("Content-Length", "0"))
                return self.rfile.read(length) if length else b""

            def _send(self, status: int, body: bytes, content_type: str = "application/json",
                      headers: dict[str, str] | None = None) -> None:
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Connection", "close")
                for name, value in (headers or {}).items():
                    self.send_header(name, value)
                self.end_headers()
                try:
                    self.wfile.write(body)
                    self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    pass

            def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler protocol
                if self.path == "/.well-known/openid-configuration":
                    base = self.server.base_url  # type: ignore[attr-defined]
                    self._send(200, json.dumps({
                        "issuer": "https://auth.openai.com",
                        "authorization_endpoint": base + "/authorize",
                        "token_endpoint": base + "/token",
                        "jwks_uri": base + "/jwks",
                        "revocation_endpoint": base + "/revoke",
                    }).encode())
                    return
                if urllib.parse.urlsplit(self.path).path == "/authorize":
                    query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
                    required = ("state", "nonce", "redirect_uri", "code_challenge", "code_challenge_method")
                    missing = [key for key in required if not query.get(key)]
                    if missing or query.get("code_challenge_method", [""])[0] != "S256":
                        self._send(400, json.dumps({"error": "invalid_authorization_request",
                                                   "missing": missing}).encode())
                        return
                    with state.lock:
                        state.oidc_authorization = {key: values[0] for key, values in query.items() if values}
                    callback = query["redirect_uri"][0]
                    separator = "&" if "?" in callback else "?"
                    location = callback + separator + urllib.parse.urlencode({
                        "code": state.oidc_code, "state": query["state"][0],
                    })
                    self.send_response(302)
                    self.send_header("Location", location)
                    self.send_header("Content-Length", "0")
                    self.send_header("Connection", "close")
                    self.end_headers()
                    return
                if self.path == "/jwks":
                    modulus, exponent, _private = _rsa_key()
                    jwk = {"kty": "RSA", "kid": OAUTH_KID, "alg": "RS256", "use": "sig",
                           "n": _b64url(_int_bytes(modulus)), "e": _b64url(_int_bytes(exponent))}
                    self._send(200, json.dumps({"keys": [jwk]}).encode())
                    return
                if self.path.startswith("/_fake/"):
                    if self.path == "/_fake/requests":
                        body = state.all_requests()
                    elif self.path == "/_fake/oauth":
                        body = state.all_oauth_requests()
                    elif self.path == "/_fake/remaining":
                        body = state.remaining()
                    else:
                        self._send(404, b'{"error":"not_found"}')
                        return
                    self._send(200, json.dumps(body).encode())
                    return
                self._send(404, b'{"error":"not_found"}')

            def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler protocol
                raw = self._body()
                if self.path.endswith("/responses"):
                    try:
                        body = json.loads(raw.decode("utf-8"))
                    except (UnicodeDecodeError, json.JSONDecodeError):
                        body = None
                    record = {
                        "path": self.path,
                        "headers": {key.lower(): value for key, value in self.headers.items()},
                        "body": body,
                        "role": _infer_role(body),
                        "tools": _tool_names(body),
                    }
                    item = state.take(record)
                    if item is None:
                        mismatch = record.get("script_error", "script mismatch")
                        payload = json.dumps({"error": {"message": str(mismatch), "type": "fake_script_mismatch"}}).encode()
                        self._send(400, payload)
                    else:
                        self._serve_script(item)
                    return
                if self.path == "/token":
                    form = urllib.parse.parse_qs(raw.decode("utf-8", "replace"))
                    state.oauth_requests.append({"path": self.path, "form": form})
                    if form.get("grant_type", [""])[0] == "authorization_code":
                        with state.lock:
                            authorization = dict(state.oidc_authorization or {})
                        code = form.get("code", [""])[0]
                        verifier = form.get("code_verifier", [""])[0]
                        challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest()) if verifier else ""
                        if code != state.oidc_code or not authorization or challenge != authorization.get("code_challenge"):
                            self._send(400, b'{"error":"invalid_code_or_pkce"}')
                            return
                        now = int(time.time())
                        config = state.oauth_config
                        claims = {
                            "iss": "https://auth.openai.com", "sub": config["subject"],
                            "aud": form.get("client_id", [authorization.get("client_id", "kogen-conformance-owned")])[0],
                            "iat": now, "exp": now + int(config["expires_in"]),
                            "email": config["email"], "nonce": authorization["nonce"],
                            "https://api.openai.com/auth": {
                                "chatgpt_account_id": config["account_id"], "chatgpt_plan_type": "plus",
                            },
                        }
                        tokens = {
                            "access_token": config["access_token"],
                            "refresh_token": config["refresh_token"],
                            "id_token": _signed_jwt(claims), "expires_in": config["expires_in"],
                            "scope": OAUTH_SCOPE,
                        }
                        self._send(200, json.dumps(tokens).encode())
                        return
                    if form.get("grant_type", [""])[0] != "refresh_token":
                        self._send(400, b'{"error":"unsupported_grant_type"}')
                        return
                    config = state.oauth_config
                    now = int(time.time())
                    claims = {
                        "iss": "https://auth.openai.com", "sub": config["subject"],
                        "aud": form.get("client_id", ["kogen-conformance-owned"])[0],
                        "iat": now, "exp": now + int(config["expires_in"]),
                        "email": config["email"],
                        "https://api.openai.com/auth": {
                            "chatgpt_account_id": config["account_id"], "chatgpt_plan_type": "plus",
                        },
                    }
                    tokens = {
                        "access_token": config["access_token"],
                        "refresh_token": config["refresh_token"],
                        "id_token": _signed_jwt(claims), "expires_in": config["expires_in"],
                        "scope": OAUTH_SCOPE,
                    }
                    self._send(200, json.dumps(tokens).encode())
                    return
                if self.path == "/revoke":
                    state.oauth_requests.append({"path": self.path, "body": raw.decode("utf-8", "replace")})
                    self._send(200, b"{}")
                    return
                if self.path == "/_fake/reset":
                    with state.lock:
                        state.requests.clear()
                        state.oauth_requests.clear()
                        state.cursor = 0
                        state.next_response_id = 1
                    self._send(200, b"{}")
                    return
                self._send(404, b'{"error":"not_found"}')

            def _serve_script(self, item: dict[str, Any]) -> None:
                gate = item.get("gate")
                if gate:
                    label = str(gate)
                    with state.lock:
                        arrived = state.gate_arrivals.setdefault(label, threading.Event())
                        released = state.gate_releases.setdefault(label, threading.Event())
                    arrived.set()
                    released.wait()
                error = str(item.get("error", ""))
                if error:
                    self._serve_error(error, item)
                    return
                usage = item.get("usage", DEFAULT_USAGE)
                items: list[dict[str, Any]] = []
                for call_index, call in enumerate(item.get("tool_calls", []), 1):
                    arguments = call.get("arguments", {})
                    encoded_arguments = arguments if isinstance(arguments, str) else json.dumps(arguments, separators=(",", ":"))
                    items.append({
                        "type": "function_call", "status": "completed",
                        "call_id": call.get("call_id", f"call_{state.next_response_id}_{call_index}"),
                        "name": call["name"], "arguments": encoded_arguments,
                    })
                final_text = item.get("assistant_text", item.get("final_text"))
                if final_text is not None:
                    items.append({
                        "type": "message", "id": f"msg_{state.next_response_id}",
                        "status": "completed", "role": "assistant",
                        "content": [{"type": "output_text", "text": str(final_text), "annotations": []}],
                    })
                response_id = item.get("response_id", f"resp_{state.next_response_id}")
                state.next_response_id += 1
                response = {
                    "id": response_id, "object": "response", "status": "completed",
                    "model": item.get("model", "gpt-6.1-sol"), "output": items, "usage": usage,
                }
                frames = []
                for output_item in items:
                    frames.append({"type": "response.output_item.done", "item": output_item})
                frames.append({"type": "response.completed", "response": response})
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "close")
                self.end_headers()
                delay_ms = max(0, int(item.get("delay_ms", state.stream_delay_ms)))
                try:
                    for frame in frames:
                        wire = ("event: " + frame["type"] + "\ndata: " +
                                json.dumps(frame, separators=(",", ":")) + "\n\n").encode("utf-8")
                        self.wfile.write(wire)
                        self.wfile.flush()
                        if delay_ms:
                            time.sleep(delay_ms / 1000.0)
                except (BrokenPipeError, ConnectionResetError):
                    pass

            def _serve_error(self, error: str, item: dict[str, Any]) -> None:
                alias = error.lower().replace("-", "_")
                status = 500
                if alias in ("401", "unauthorized", "auth", "http_401"):
                    status = 401
                    body = {"error": {"message": "invalid_token", "type": "authentication_error", "code": "invalid_token"}}
                elif alias in ("429", "usage_limit", "usage_limit_429", "http_429"):
                    status = 429
                    body = {"error": {"message": "usage_limit", "type": "usage_limit", "code": "usage_limit"},
                            "retry_after_ms": int(item.get("retry_after_ms", 0))}
                elif alias in ("5xx", "500", "502", "503", "server_error", "http_5xx"):
                    status = int(item.get("status", 503 if alias in ("5xx", "server_error", "http_5xx") else alias))
                    body = {"error": {"message": "provider_overload", "type": "server_error", "code": "overloaded"}}
                elif alias in ("malformed_sse", "malformed"):
                    self.send_response(200)
                    self.send_header("Content-Type", "text/event-stream")
                    self.send_header("Connection", "close")
                    self.end_headers()
                    try:
                        self.wfile.write(b"event: response.completed\ndata: {not-json}\n\n")
                        self.wfile.flush()
                    except (BrokenPipeError, ConnectionResetError):
                        pass
                    return
                elif alias in ("slow", "slow_stream"):
                    slow_item = dict(item)
                    slow_item.pop("error", None)
                    slow_item["delay_ms"] = int(item.get("delay_ms", 2000))
                    self._serve_script(slow_item)
                    return
                elif alias in ("usage_limit_sse", "stream_usage_limit"):
                    self.send_response(200)
                    self.send_header("Content-Type", "text/event-stream")
                    self.send_header("Connection", "close")
                    self.end_headers()
                    frame = {"type": "error", "error": {"message": "usage_limit", "type": "usage_limit", "code": "usage_limit"}}
                    try:
                        self.wfile.write(("event: error\ndata: " + json.dumps(frame) + "\n\n").encode())
                        self.wfile.flush()
                    except (BrokenPipeError, ConnectionResetError):
                        pass
                    return
                else:
                    status = int(item.get("status", 500))
                    body = {"error": {"message": error, "type": "fake_provider_error"}}
                headers = {}
                retry_after_ms = item.get("retry_after_ms")
                if status in (429, 503) and retry_after_ms is not None:
                    headers["Retry-After"] = str(max(0, int(retry_after_ms)) / 1000.0)
                self._send(status, json.dumps(body).encode(), headers=headers)

        class Server(http.server.ThreadingHTTPServer):
            # Close all accepted sockets before the owning case returns.
            daemon_threads = False
            allow_reuse_address = True

            def server_bind(self) -> None:
                # Avoid HTTPServer's reverse DNS lookup. On macOS that leaves
                # a persistent mDNS socket in a long-running scorer process.
                socketserver.TCPServer.server_bind(self)
                self.server_name = str(self.server_address[0])
                self.server_port = int(self.server_address[1])

        self._server = Server(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self._server.server_address[1]}"
        self._server.base_url = self.url  # type: ignore[attr-defined]
        self._thread = threading.Thread(target=self._server.serve_forever, name="kogen-fake-provider", daemon=True)
        self._thread.start()
        return self

    def seed_owned_credential(self, home: str, expires_in: int = 3600) -> None:
        import os
        os.makedirs(os.path.join(home, ".kogen", "credentials"), exist_ok=True)
        now = int(time.time())
        client_id = "kogen-conformance-owned"
        claims = {
            "iss": "https://auth.openai.com", "sub": self.state.oauth_config["subject"],
            "aud": client_id, "iat": now, "exp": now + max(600, expires_in),
            "email": self.state.oauth_config["email"],
            "https://api.openai.com/auth": {
                "chatgpt_account_id": self.state.oauth_config["account_id"], "chatgpt_plan_type": "plus",
            },
        }
        credential = {
            "client_id": client_id, "access_token": "kogen-fake-access-old",
            "refresh_token": "kogen-fake-refresh", "id_token": _signed_jwt(claims),
            "expires_at": now + max(600, expires_in),
            "scopes": OAUTH_SCOPE.split(), "subject": self.state.oauth_config["subject"],
            "email": self.state.oauth_config["email"], "host_id": "kogen-conformance-host",
        }
        path = os.path.join(home, ".kogen", "credentials", "chatgpt-default.json")
        with open(path, "w", encoding="utf-8") as cred_file:
            json.dump(credential, cred_file)
        os.chmod(path, 0o600)

    def configure_script(self, script_id: str, script: list[dict[str, Any]]) -> None:
        self.state.configure_script(script_id, script)

    def configure_openid(self, script_id: str, account_id: str, label: str) -> None:
        self.state.configure_openid(script_id, account_id, label)

    def wait_gate(self, script_id: str, label: str, timeout_s: float = 60.0) -> bool:
        return self.state.wait_gate(script_id, label, timeout_s)

    def release_gate(self, script_id: str, label: str) -> bool:
        return self.state.release_gate(script_id, label)

    def close(self) -> None:
        with self.state.lock:
            for released in self.state.gate_releases.values():
                released.set()
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
        if self._thread is not None:
            self._thread.join(timeout=2)

    def __enter__(self) -> "FakeProvider":
        return self.start()

    def __exit__(self, _type: Any, _value: Any, _traceback: Any) -> None:
        self.close()


def _infer_role(body: Any) -> str:
    if not isinstance(body, dict):
        return "unknown"
    text_parts = [str(body.get("instructions", ""))]
    for item in body.get("input", []):
        if not isinstance(item, dict):
            continue
        content = item.get("content")
        if isinstance(content, list):
            text_parts.extend(str(part.get("text", "")) for part in content if isinstance(part, dict))
        elif isinstance(content, str):
            text_parts.append(content)
    joined = "\n".join(text_parts)
    if "You are Kogen Intent shaper." in joined:
        return "shaper"
    if "You are Kogen's acceptance test auditor." in joined or "You are Kogen's requirement auditor." in joined:
        return "auditor"
    if "You are Kogen's builder." in joined:
        return "builder"
    return "unknown"


def _tool_names(body: Any) -> list[str]:
    if not isinstance(body, dict):
        return []
    names = [tool.get("name") for tool in body.get("tools", []) if isinstance(tool, dict) and tool.get("name")]
    for item in body.get("input", []):
        if isinstance(item, dict) and item.get("type") == "additional_tools":
            names.extend(tool.get("name") for tool in item.get("tools", [])
                         if isinstance(tool, dict) and tool.get("name"))
    return sorted(set(names))
