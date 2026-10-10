import importlib.util
import json
import os
import signal
from pathlib import Path
import socket
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
import unittest


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


proxy = load_module("egress_proxy", "egress-proxy.py")
bridge = load_module("egress_bridge", "egress-bridge.py")


class EgressProxyTests(unittest.TestCase):
    def setUp(self):
        # macOS limits AF_UNIX socket paths to 104 bytes. Keep the test's
        # temporary directory short even when the checkout path is long.
        self.temp = tempfile.TemporaryDirectory(dir="/tmp")
        self.socket_path = os.path.join(self.temp.name, "proxy.sock")
        self.log_path = os.path.join(self.temp.name, "egress.jsonl")
        try:
            self.start_server(proxy.ProxyServer(self.socket_path, self.log_path))
        except PermissionError as error:
            self.temp.cleanup()
            self.skipTest(f"AF_UNIX bind unavailable in this sandbox: {error}")

    def start_server(self, server):
        self.server = server
        self.thread = threading.Thread(target=server.serve_forever, daemon=True)
        self.thread.start()
        # shutdown() only waits if serve_forever has started. Wait until its
        # internal shutdown event clears so immediate test restarts are safe.
        stopped = server._BaseServer__is_shut_down
        deadline = time.monotonic() + 3
        while stopped.is_set() and time.monotonic() < deadline:
            time.sleep(0.001)
        self.assertFalse(stopped.is_set(), "proxy serve loop did not become ready")

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def tearDown(self):
        self.stop_server()
        self.temp.cleanup()

    def request(self, authority, payload=b""):
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.settimeout(3)
        client.connect(self.socket_path)
        client.sendall(f"CONNECT {authority} HTTP/1.1\r\nHost: {authority}\r\n\r\n".encode())
        response = bytearray()
        while b"\r\n\r\n" not in response:
            chunk = client.recv(1024)
            if not chunk:
                self.fail("proxy closed before completing its CONNECT response")
            response.extend(chunk)
        if payload and response.startswith(b"HTTP/1.1 200"):
            client.sendall(payload)
        return client, bytes(response)

    def rows(self, count=1):
        # A completed client close and the handler's final relay/log write can
        # race; wait for the durable record instead of assuming thread order.
        deadline = time.monotonic() + 3
        while True:
            try:
                with open(self.log_path, encoding="utf-8") as source:
                    rows = [json.loads(line) for line in source]
            except FileNotFoundError:
                rows = []
            if len(rows) >= count:
                return rows
            if time.monotonic() >= deadline:
                self.fail(f"expected {count} egress log row(s), found {len(rows)}")
            time.sleep(0.01)

    def test_github_denied_and_logged_without_payload(self):
        client, response = self.request("github.com:443", b"secret-payload")
        client.close()
        self.assertIn(b"403 Forbidden", response)
        rows = self.rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual((rows[0]["host"], rows[0]["port"], rows[0]["decision"]),
                         ("github.com", 443, "denied"))
        self.assertEqual(rows[0]["bytes_up"], 0)
        self.assertEqual(rows[0]["bytes_down"], 0)
        self.assertNotIn(b"secret-payload", Path(self.log_path).read_bytes())

    def test_allowed_name_uses_injected_local_resolver_and_counts_bytes(self):
        upstream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        upstream.bind(("localhost", 0))
        upstream.listen(1)
        port = upstream.getsockname()[1]

        def serve_stub():
            conn, _ = upstream.accept()
            with conn:
                self.assertEqual(conn.recv(16), b"hello")
                conn.sendall(b"world")
                conn.shutdown(socket.SHUT_WR)
            upstream.close()

        server_thread = threading.Thread(target=serve_stub, daemon=True)
        server_thread.start()
        self.stop_server()
        self.start_server(proxy.ProxyServer(
            self.socket_path, self.log_path,
            resolver=lambda _host, _port, type: [(socket.AF_INET, socket.SOCK_STREAM,
                                                  0, "", ("localhost", port))],
        ))

        client, response = self.request("chatgpt.com:443", b"hello")
        self.assertIn(b"200 Connection Established", response)
        client.shutdown(socket.SHUT_WR)
        self.assertEqual(client.recv(16), b"world")
        client.close()
        server_thread.join(timeout=2)
        rows = self.rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["decision"], "allowed")
        self.assertEqual(rows[0]["bytes_up"], 5)
        self.assertEqual(rows[0]["bytes_down"], 5)
        self.assertNotIn(b"hello", Path(self.log_path).read_bytes())
        self.assertNotIn(b"world", Path(self.log_path).read_bytes())

    def test_decision_only_allows_without_opening_upstream(self):
        self.stop_server()
        self.start_server(proxy.ProxyServer(self.socket_path, self.log_path, decision_only=True))
        client, response = self.request("chatgpt.com:443")
        client.close()
        self.assertIn(b"200 Connection Established", response)
        self.assertEqual(self.rows()[0]["decision"], "allowed")

    def test_sigterm_flushes_audit_and_removes_socket(self):
        self.stop_server()
        self.temp.cleanup()
        self.temp = tempfile.TemporaryDirectory(dir="/tmp")
        self.socket_path = os.path.join(self.temp.name, "proxy.sock")
        self.log_path = os.path.join(self.temp.name, "egress.jsonl")
        allow_path = os.path.join(self.temp.name, "allow.txt")
        upstream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        upstream.bind(("127.0.0.1", 0))
        upstream.listen(1)
        upstream_port = upstream.getsockname()[1]
        Path(allow_path).write_text(f"localhost:{upstream_port}\n")
        process = subprocess.Popen([
            "python3", str(HERE / "egress-proxy.py"), "--socket", self.socket_path,
            "--log", self.log_path, "--allow-file", allow_path,
        ])
        accepted = []

        def accept_upstream():
            conn, _ = upstream.accept()
            accepted.append(conn)

        accept_thread = threading.Thread(target=accept_upstream, daemon=True)
        accept_thread.start()
        try:
            deadline = time.monotonic() + 3
            while not os.path.exists(self.socket_path) and time.monotonic() < deadline:
                time.sleep(0.01)
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect(self.socket_path)
            authority = f"localhost:{upstream_port}"
            client.sendall(f"CONNECT {authority} HTTP/1.1\r\nHost: {authority}\r\n\r\n".encode())
            self.assertIn(b"200 Connection Established", client.recv(1024))
            process.send_signal(signal.SIGTERM)
            # Darwin does not consistently wake a worker's select() when the
            # same socket is closed from the SIGTERM handler; the relay's
            # existing poll bound is 60 seconds. Production lane hosts are Linux.
            process.wait(timeout=65 if sys.platform == "darwin" else 3)
            self.assertEqual(client.recv(1), b"")
            client.close()
            self.assertFalse(os.path.exists(self.socket_path))
            rows = [json.loads(row) for row in Path(self.log_path).read_text().splitlines()]
            self.assertEqual(len(rows), 1)
            self.assertEqual((rows[0]["host"], rows[0]["decision"]), ("localhost", "allowed"))
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=2)
            upstream.close()
            for conn in accepted:
                conn.close()
            accept_thread.join(timeout=1)


class EgressBridgeTests(unittest.TestCase):
    def test_bridge_does_not_require_net_admin_for_loopback(self):
        source = (HERE / "egress-bridge.py").read_text()
        self.assertNotIn("SIOCSIFFLAGS", source)
        self.assertNotIn("ioctl", source)

    def test_bridge_environment_bypasses_proxy_for_loopback(self):
        env = bridge.command_environment({"PATH": "/bin"}, 1234)
        expected = "localhost,127.0.0.1,::1"
        self.assertEqual(env["NO_PROXY"], expected)
        self.assertEqual(env["no_proxy"], expected)
        self.assertEqual(env["HTTP_PROXY"], "http://localhost:1234")

    def test_bridge_forwards_bytes_over_unix_socket(self):
        with tempfile.TemporaryDirectory(dir="/tmp") as temp:
            path = os.path.join(temp, "bridge.sock")
            unix_server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                unix_server.bind(path)
            except PermissionError as error:
                unix_server.close()
                self.skipTest(f"AF_UNIX bind unavailable in this sandbox: {error}")
            unix_server.listen(1)

            def unix_echo():
                conn, _ = unix_server.accept()
                with conn:
                    self.assertEqual(conn.recv(16), b"ping")
                    conn.sendall(b"pong")
                unix_server.close()

            worker = threading.Thread(target=unix_echo, daemon=True)
            worker.start()
            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listener.bind(("localhost", 0))
            listener.listen(1)
            port = listener.getsockname()[1]
            client = socket.create_connection(("localhost", port))
            accepted, _ = listener.accept()
            listener.close()
            handler = threading.Thread(target=bridge.bridge, args=(accepted, path), daemon=True)
            handler.start()
            client.sendall(b"ping")
            client.shutdown(socket.SHUT_WR)
            self.assertEqual(client.recv(16), b"pong")
            client.close()
            worker.join(timeout=2)
            handler.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
