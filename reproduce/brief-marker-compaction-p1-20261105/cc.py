#!/usr/bin/env python3
"""Launch the pinned Claude Code client with a clean env and the subscription OAuth token read from its 0600 file
(never in argv, never printed). usage: cc.py <client-home-name> <client-version> <timeout-s> <claude args...>"""
import json, os, sys

kh, ver, tmo = sys.argv[1], sys.argv[2], sys.argv[3]
home = os.path.expanduser("~") + "/" + kh + "/.kogen"
env = {"HOME": os.path.expanduser("~"), "PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "en_US.UTF-8",
       "CLAUDE_CONFIG_DIR": home + "/claude-code/config", "DISABLE_AUTOUPDATER": "1",
       "CLAUDE_CODE_OAUTH_TOKEN": json.load(open(home + "/credentials/claude-code.json"))["api_key"]}
os.execve("/usr/bin/perl", ["perl", "-e", "alarm shift; exec @ARGV", tmo, home + "/claude-code/" + ver + "/claude"] + sys.argv[4:], env)
