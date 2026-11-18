"""Acceptance driver for lanes.common._require_group_gone; prints one JSON object."""
import json
import os
import signal
import subprocess
import sys
import time

sys.path.insert(0, os.path.abspath("lanes"))
from lanes import common  # noqa: E402

mode = sys.argv[1]
real_killpg = os.killpg
calls = []


def recording_killpg(pgid, sig):
    calls.append(int(sig))
    return real_killpg(pgid, sig)


def start_group(member_seconds):
    # The leader exits 0 at once; one member of the same group outlives it.
    proc = subprocess.Popen(
        ["sh", "-c", "sleep %s >/dev/null 2>&1 </dev/null & exit 0" % member_seconds],
        start_new_session=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
    proc.wait()
    return proc


out = {"mode": mode, "raised": None, "elapsed": None, "signals": []}
proc = None
try:
    if mode == "permission":
        def denied(pgid, sig):
            raise PermissionError(1, "not permitted")
        os.killpg = denied
        pgid, start = 4242, time.monotonic()
    else:
        if mode == "outlives":
            common.GROUP_GONE_TIMEOUT_S = 0.3
        proc = start_group("30" if mode == "outlives" else "0.5")
        pgid = proc.pid
        os.killpg = recording_killpg
        common._killpg = lambda p, s: calls.append(int(s))
        start = time.monotonic()
    try:
        common._require_group_gone(pgid)
        out["raised"] = None
    except common.CustodyUnknown:
        out["raised"] = "CustodyUnknown"
    except BaseException as e:
        out["raised"] = type(e).__name__
    out["elapsed"] = round(time.monotonic() - start, 3)
    out["signals"] = [s for s in calls if s != 0]
finally:
    os.killpg = real_killpg
    if proc is not None:
        try:
            real_killpg(proc.pid, signal.SIGKILL)
        except OSError:
            pass
print(json.dumps(out))
