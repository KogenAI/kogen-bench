#!/usr/bin/env python3
"""Run argv fully detached (double fork + setsid) so a supervisor restart cannot kill it."""
import os, sys
log = sys.argv[1]; argv = sys.argv[2:]
if os.fork(): sys.exit(0)
os.setsid()
if os.fork(): os._exit(0)
os.chdir(os.path.expanduser('~'))
fd = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
os.dup2(fd, 1); os.dup2(fd, 2)
os.dup2(os.open('/dev/null', os.O_RDONLY), 0)
os.execvp(argv[0], argv)
