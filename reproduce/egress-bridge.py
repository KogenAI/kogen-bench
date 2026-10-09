#!/usr/bin/env python3
"""Expose a host Unix-socket CONNECT proxy on loopback inside a net namespace."""
import argparse
import os
import socket
import subprocess
import threading


def pump(source, destination):
    try:
        while True:
            data = source.recv(65536)
            if not data:
                break
            destination.sendall(data)
    except OSError:
        pass
    finally:
        try:
            destination.shutdown(socket.SHUT_WR)
        except OSError:
            pass


def command_environment(base_env, port):
    env = base_env.copy()
    proxy = f"http://localhost:{port}"
    env.update({"HTTPS_PROXY": proxy, "HTTP_PROXY": proxy, "ALL_PROXY": proxy,
                "https_proxy": proxy, "http_proxy": proxy, "all_proxy": proxy,
                "NO_PROXY": "localhost,127.0.0.1,::1",
                "no_proxy": "localhost,127.0.0.1,::1"})
    return env


def bridge(client, socket_path):
    try:
        remote = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        remote.connect(socket_path)
    except OSError:
        client.close()
        return
    threads = [threading.Thread(target=pump, args=(client, remote), daemon=True),
               threading.Thread(target=pump, args=(remote, client), daemon=True)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    client.close()
    remote.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unix-socket", required=True)
    parser.add_argument("--port", type=int, default=18765)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        parser.error("a command after -- is required")
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("localhost", args.port))
    listener.listen(32)
    listener.settimeout(0.5)

    def accept_loop():
        while not stop.is_set():
            try:
                client, _ = listener.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            threading.Thread(target=bridge, args=(client, args.unix_socket), daemon=True).start()

    stop = threading.Event()
    thread = threading.Thread(target=accept_loop, daemon=True)
    thread.start()
    try:
        return subprocess.call(args.command, env=command_environment(os.environ, args.port))
    finally:
        stop.set()
        listener.close()
        thread.join(timeout=1)


if __name__ == "__main__":
    raise SystemExit(main())
