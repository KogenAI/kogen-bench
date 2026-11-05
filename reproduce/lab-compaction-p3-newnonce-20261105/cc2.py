#!/usr/bin/env python3
"""Phase 2 launcher: the pinned Claude Code client with a clean env and a PER-CELL home
(HOME=<cell>/cellhome, CLAUDE_CONFIG_DIR=<cell>/cellhome/.claude), so anything the agent installs (hooks, settings) and the
session transcript stay inside the cell and never touch the shared login home. The OAuth token is read from the
login home 0600 file into the env (never argv, never printed).
usage: cc2.py <login-home-name> <client-version> <timeout-s> <cell-home> <claude args...>"""
import json, os, sys

kh, ver, tmo, chome = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
login_dir = os.path.expanduser("~") + "/" + kh + "/.kogen"
os.makedirs(chome + "/.claude", exist_ok=True)
env = {"HOME": chome, "PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "en_US.UTF-8",
       "CLAUDE_CONFIG_DIR": chome + "/.claude", "DISABLE_AUTOUPDATER": "1",
       "CLAUDE_CODE_OAUTH_TOKEN": json.load(open(login_dir + "/credentials/claude-code.json"))["api_key"]}
os.execve("/usr/bin/perl", ["perl", "-e", "alarm shift; exec @ARGV", tmo, login_dir + "/claude-code/" + ver + "/claude"] + sys.argv[5:], env)
