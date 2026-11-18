"""Run the one named lanes test in-process once, recording signals and the leftover group's lifetime.

Usage: python3 -I observe.py <repo-root>; prints one JSON line.
"""
import io
import json
import os
import sys
import threading
import time
import unittest

sys.dont_write_bytecode = True
root = os.path.abspath(sys.argv[1])
os.chdir(os.path.join(root, "lanes"))
sys.path.insert(0, os.getcwd())
from lanes import common  # noqa: E402

NAME = "tests.test_common.Run.test_leftover_child_is_unknown_without_post_reap_signal"
rec = {"signals": [], "raised": False, "bound": None, "alive_after": None, "gone_after": None}
real_kill, real_killpg = os.kill, os.killpg


def kill(pid, sig):
    if sig != 0:
        rec["signals"].append(int(sig))
    return real_kill(pid, sig)


def killpg(pgid, sig):
    if sig != 0:
        rec["signals"].append(int(sig))
    return real_killpg(pgid, sig)


def group_alive(pgid):
    try:
        real_killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def watch_group(pgid, raised_at):
    while time.monotonic() - raised_at < 10:
        if not group_alive(pgid):
            rec["gone_after"] = round(time.monotonic() - raised_at, 3)
            return
        time.sleep(0.02)


original = common._require_group_gone
threads = []


def observed(pgid):
    try:
        original(pgid)
    except common.CustodyUnknown:
        raised_at = time.monotonic()
        rec["raised"] = True
        rec["bound"] = common.GROUP_GONE_TIMEOUT_S
        rec["alive_after"] = group_alive(pgid)
        t = threading.Thread(target=watch_group, args=(pgid, raised_at))
        t.start()
        threads.append(t)
        raise


os.kill, os.killpg = kill, killpg
common._require_group_gone = observed
result = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromName(NAME))
for t in threads:
    t.join(12)
rec["tests_run"] = result.testsRun
rec["ok"] = result.wasSuccessful() and not result.skipped
print(json.dumps(rec))
