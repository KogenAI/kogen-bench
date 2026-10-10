#!/usr/bin/python3
# kg-wrap.py — preserve the runner's PID and process group; signals reach kogen directly.
# KG_STATS timing/RSS logging is dropped because this process becomes kogen.
import os
import sys

real = os.environ["KG_REAL"]
os.execv(real, [real] + sys.argv[1:])
