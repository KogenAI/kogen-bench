#!/usr/bin/env python3
"""Per-cell HTTP CONNECT allowlist proxy over a Unix domain socket."""
import argparse
import datetime
import json
import os
import re
import selectors
import signal
import socket
import socketserver
import threading


DEFAULT_ALLOW = frozenset({("chatgpt.com", 443), ("ab.chatgpt.com", 443)})
AUTHORITY = re.compile(r"^(?:\[([^\]]+)\]|([^:\s]+)):(\d{1,5})$")


def load_allowlist(path=None):
    allowed = set(DEFAULT_ALLOW)
    path = path or os.environ.get("BENCH_EGRESS_ALLOW")
    if not path:
        return frozenset(allowed)
    with open(path, encoding="utf-8") as source:
        for number, raw in enumerate(source, 1):
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            # Accept host-pins entries as HOST=host or host[:port], one per line.
            if "=" in line:
                key, line = (part.strip() for part in line.split("=", 1))
                if key != "HOST":
                    raise ValueError(f"{path}:{number}: expected HOST=host")
            if ":" in line:
                match = AUTHORITY.fullmatch(line)
                if not match:
                    raise ValueError(f"{path}:{number}: expected host[:port]")
                host = (match.group(1) or match.group(2)).lower().rstrip(".")
                port = int(match.group(3))
            else:
                host, port = line.lower().rstrip("."), 443
            if not host or not (1 <= port <= 65535):
                raise ValueError(f"{path}:{number}: invalid host or port")
            allowed.add((host, port))
    return frozenset(allowed)


def parse_authority(value):
    match = AUTHORITY.fullmatch(value)
    if not match:
        return value, None
    host = (match.group(1) or match.group(2)).lower().rstrip(".")
    port = int(match.group(3))
    if not 1 <= port <= 65535:
        return host, None
    return host, port


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class ProxyServer(socketserver.ThreadingUnixStreamServer):
    daemon_threads = False
    block_on_close = True
    allow_reuse_address = True

    def __init__(self, socket_path, log_path, allowed=None, resolver=None,
                 connector=None, decision_only=False, socket_uid=None,
                 socket_gid=None):
        self.log_path = log_path
        self.allowed = allowed if allowed is not None else load_allowlist()
        # Injection seams intentionally support deterministic localhost-only tests.
        self.resolver = resolver or socket.getaddrinfo
        self.connector = connector
        self.decision_only = decision_only
        self.log_lock = threading.Lock()
        self.tunnel_lock = threading.Lock()
        self.tunnels = set()
        try:
            os.unlink(socket_path)
        except FileNotFoundError:
            pass
        super().__init__(socket_path, ProxyHandler)
        if socket_uid is not None or socket_gid is not None:
            os.chown(socket_path, -1 if socket_uid is None else socket_uid,
                     -1 if socket_gid is None else socket_gid)
        os.chmod(socket_path, 0o660)

    def connect_upstream(self, host, port):
        if self.connector is not None:
            return self.connector((host, port), timeout=10)
        last_error = None
        for _family, socktype, proto, _canonname, address in self.resolver(host, port, type=socket.SOCK_STREAM):
            upstream = socket.socket(_family, socktype, proto)
            upstream.settimeout(10)
            try:
                upstream.connect(address)
                upstream.settimeout(None)
                return upstream
            except OSError as error:
                last_error = error
                upstream.close()
        if last_error:
            raise last_error
        raise OSError("host lookup returned no stream addresses")

    def record(self, host, port, decision, up, down):
        row = {"ts": utc_now(), "host": host, "port": port,
               "decision": decision, "bytes_up": up, "bytes_down": down}
        with self.log_lock, open(self.log_path, "a", encoding="utf-8") as log:
            log.write(json.dumps(row, separators=(",", ":"), sort_keys=True) + "\n")
            log.flush()

    def track(self, sock):
        with self.tunnel_lock:
            self.tunnels.add(sock)

    def untrack(self, sock):
        with self.tunnel_lock:
            self.tunnels.discard(sock)

    def close_tunnels(self):
        with self.tunnel_lock:
            tunnels = tuple(self.tunnels)
        for tunnel in tunnels:
            try:
                tunnel.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                tunnel.close()
            except OSError:
                pass


class ProxyHandler(socketserver.StreamRequestHandler):
    def handle(self):
        host, port, decision, up, down = "", 0, "denied", 0, 0
        upstream = None
        recorded = False
        self.server.track(self.connection)

        def record():
            nonlocal recorded
            if not recorded:
                self.server.record(host, port, decision, up, down)
                recorded = True

        try:
            raw = self.rfile.readline(8193)
            if len(raw) > 8192 or not raw.endswith(b"\n"):
                record()
                self.wfile.write(b"HTTP/1.1 400 Bad Request\r\nConnection: close\r\n\r\n")
                return
            try:
                method, authority, _version = raw.decode("ascii").strip().split(" ", 2)
            except (UnicodeDecodeError, ValueError):
                record()
                self.wfile.write(b"HTTP/1.1 400 Bad Request\r\nConnection: close\r\n\r\n")
                return
            host, parsed_port = parse_authority(authority)
            port = parsed_port or 0
            # Consume headers before responding, with a hard bound.
            header_bytes = len(raw)
            while header_bytes <= 32768:
                line = self.rfile.readline(8193)
                header_bytes += len(line)
                if line in (b"\r\n", b"\n", b""):
                    break
            valid = method.upper() == "CONNECT" and parsed_port is not None
            if not valid or (host, port) not in self.server.allowed:
                record()
                self.wfile.write(b"HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\n")
                return
            decision = "allowed"
            if self.server.decision_only:
                record()
                self.wfile.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
                return
            try:
                # Production uses the host resolver and connector. Tests inject a
                # connector that deliberately maps allowed names to a local stub.
                upstream = self.server.connect_upstream(host, port)
                self.server.track(upstream)
            except OSError:
                record()
                self.wfile.write(b"HTTP/1.1 502 Bad Gateway\r\nConnection: close\r\n\r\n")
                return
            self.wfile.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            self.wfile.flush()
            up, down = self.relay(self.connection, upstream)
        finally:
            if upstream is not None:
                self.server.untrack(upstream)
                upstream.close()
            self.server.untrack(self.connection)
            record()

    @staticmethod
    def relay(client, upstream):
        totals = {client: 0, upstream: 0}
        peers = {client: upstream, upstream: client}
        with selectors.DefaultSelector() as selector:
            selector.register(client, selectors.EVENT_READ)
            selector.register(upstream, selectors.EVENT_READ)
            while selector.get_map():
                events = selector.select(timeout=60)
                if not events:
                    break
                for key, _ in events:
                    source = key.fileobj
                    try:
                        data = source.recv(65536)
                    except OSError:
                        data = b""
                    if not data:
                        selector.unregister(source)
                        destination = peers[source]
                        try:
                            destination.shutdown(socket.SHUT_WR)
                        except OSError:
                            pass
                        continue
                    destination = peers[source]
                    try:
                        destination.sendall(data)
                    except OSError:
                        try:
                            selector.unregister(source)
                        except (KeyError, ValueError):
                            pass
                        continue
                    totals[source] += len(data)
        return totals[client], totals[upstream]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--socket", required=True)
    parser.add_argument("--log", required=True)
    parser.add_argument("--allow-file")
    parser.add_argument("--socket-uid", type=int)
    parser.add_argument("--socket-gid", type=int)
    parser.add_argument("--decision-only", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    os.makedirs(os.path.dirname(os.path.abspath(args.log)), exist_ok=True)
    server = ProxyServer(args.socket, args.log, load_allowlist(args.allow_file),
                         decision_only=args.decision_only,
                         socket_uid=args.socket_uid, socket_gid=args.socket_gid)
    stopping = threading.Event()

    def terminate(_signum, _frame):
        if stopping.is_set():
            return
        stopping.set()
        server.close_tunnels()
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, terminate)
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.close_tunnels()
        server.server_close()
        try:
            os.unlink(args.socket)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    main()
