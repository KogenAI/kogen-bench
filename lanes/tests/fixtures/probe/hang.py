"""Fake probe that never answers and leaves a child behind; args.pidfile gets the child's pid."""
import json
import subprocess
import sys
import time

req = json.load(sys.stdin)
child = subprocess.Popen(["sleep", "300"])
open(req["args"]["pidfile"], "w").write(str(child.pid))
time.sleep(300)
