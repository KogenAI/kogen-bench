#!/usr/bin/env python3
"""Runner-mechanics stub: records calls and replays fixed external transcripts."""
import atexit
import json
import os
from pathlib import Path
import signal
import socket
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TRANSCRIPTS = json.loads((HERE / "fake_transcripts.json").read_text())


def record(value):
    target = os.environ.get("ARCH_SELFTEST_CALLS")
    if target:
        with open(target, "a") as stream:
            stream.write(json.dumps(value) + "\n")


def register():
    registry = os.environ.get("ARCH_SELFTEST_REGISTRY")
    if not registry:
        return
    directory = Path(registry)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{os.getpid()}.json"
    path.write_text(json.dumps({"pid": os.getpid(), "ppid": os.getppid(), "command": " ".join(sys.argv)}))
    atexit.register(lambda: path.unlink(missing_ok=True))
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))


def flag(name):
    return sys.argv[sys.argv.index(name) + 1]


def main():
    register()
    if len(sys.argv) < 2:
        return 2
    if sys.argv[1] == "coordinator":
        data, port = Path(flag("--data")), int(flag("--port"))
        data.mkdir(parents=True, exist_ok=True)
        counter = Path(os.environ.get("ARCH_SELFTEST_COUNTER", "/tmp/arch-selftest-counter"))
        mode = os.environ.get("ARCH_SELFTEST_FAKE_MODE", "pass")
        if mode == "flaky":
            count = int(counter.read_text()) if counter.exists() else 0
            counter.write_text(str(count + 1))
            mode = "pass" if count == 0 else "fail-status"
        if mode == "hang":
            while True:
                time.sleep(1)
        listener = socket.socket()
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("[IP omitted]", port))
        listener.listen()
        print(json.dumps({"type":"coordinator_ready", "version":1, "address":f"[IP omitted]:{port}",
                          "data":str(data.resolve()), "pid":os.getpid()}), flush=True)
        while True:
            conn, _ = listener.accept()
            with conn, conn.makefile("rwb") as stream:
                for line in stream:
                    record({"kind":"protocol_call", "bytes":line.decode(errors="replace").rstrip("\n")})
                    stream.write((json.dumps(TRANSCRIPTS["wire_status_response"], separators=(",", ":")) + "\n").encode())
                    stream.flush()
    command = sys.argv[1]
    record({"kind":"cli_call", "argv":sys.argv[1:]})
    if command == "status":
        mode = os.environ.get("ARCH_SELFTEST_FAKE_MODE", "pass")
        counter = Path(os.environ.get("ARCH_SELFTEST_COUNTER", "/tmp/arch-selftest-counter"))
        failed_repetition = mode == "fail-status" or (mode == "flaky" and counter.exists() and int(counter.read_text()) > 1)
        output = TRANSCRIPTS["cli_status_failure_stdout"] if failed_repetition else TRANSCRIPTS["cli_status_stdout"]
        sys.stdout.write(output)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
