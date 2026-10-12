#!/usr/bin/env python3
"""Build fixture: an ordinary child plus a double-forked setsid descendant."""
import os
from pathlib import Path
import subprocess
import sys
import time


def stay_alive(marker):
    Path(marker).write_text(str(os.getpid()) + "\n")
    while True:
        time.sleep(0.2)


def main():
    prefix = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "ordinary":
        stay_alive(prefix + ".ordinary.pid")
        return
    subprocess.Popen([sys.executable, str(Path(__file__).resolve()), prefix, "ordinary"])
    first = os.fork()
    if first == 0:
        os.setsid()
        second = os.fork()
        if second != 0:
            os._exit(0)
        stay_alive(prefix + ".detached.pid")
        os._exit(0)
    os.waitpid(first, 0)
    stay_alive(prefix + ".parent.pid")


if __name__ == "__main__":
    main()
