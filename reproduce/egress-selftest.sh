#!/usr/bin/env bash
# Model-free host check: the sandbox bridge reaches only proxy decisions.
set -euo pipefail
HERE=$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")
WORK=$(mktemp -d)
EGRESS_SOCKET=$WORK/.egress.sock
LOG=$WORK/egress.jsonl
cleanup() {
  if [[ -n ${proxy_pid:-} ]]; then
    kill "$proxy_pid" 2>/dev/null || true
    wait "$proxy_pid" 2>/dev/null || true
  fi
  rm -rf -- "$WORK"
}
trap cleanup EXIT
/usr/bin/python3 "$HERE/egress-proxy.py" --socket "$EGRESS_SOCKET" --log "$LOG" --decision-only &
proxy_pid=$!
for _ in {1..50}; do
  [[ -S $EGRESS_SOCKET ]] && break
  kill -0 "$proxy_pid" 2>/dev/null || exit 1
  sleep 0.1
done
[[ -S $EGRESS_SOCKET ]] || { echo 'egress proxy socket unavailable' >&2; exit 1; }
cat > "$WORK/probe.py" <<'PY'
import socket

def status(host):
    sock = socket.create_connection(("localhost", 18765), timeout=3)
    sock.sendall((f"CONNECT {host}:443 HTTP/1.1\r\nHost: {host}:443\r\n\r\n").encode())
    response = bytearray()
    while b"\r\n\r\n" not in response:
        response.extend(sock.recv(1024))
    sock.close()
    return bytes(response).split(b" ", 2)[1]

assert status("github.com") == b"403", "github.com was not denied"
assert status("chatgpt.com") == b"200", "chatgpt.com was not allowed"
PY
"$HERE/sandbox-profile.sh" agent "$WORK" "$EGRESS_SOCKET" -- /usr/bin/python3 /work/probe.py
/usr/bin/python3 - "$LOG" <<'PY'
import json,sys
rows=[json.loads(line) for line in open(sys.argv[1], encoding="utf-8")]
assert [(row["host"],row["decision"]) for row in rows] == [
    ("github.com","denied"),("chatgpt.com","allowed")]
print("Egress self-check: PASS (github denied; provider allowed; no fetch)")
PY
