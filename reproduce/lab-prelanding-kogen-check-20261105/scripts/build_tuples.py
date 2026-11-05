#!/usr/bin/env python3
"""Diagnostic arm B-tuple: for each sample row, the tuple the next adoption would pin if it ran at the landing time: the landed commit
for its own repo and the main head (first-parent, committer time <= landing done time) of every other component that kogen's cli/go.mod
requires at that kogen main (kogen-loop is always included: vendored). Writes tuples/tuple-<n>.txt ("repo sha" lines, loop first)."""
import json, os, re, subprocess, datetime as dt
MD = os.environ.get("MIRRORS_DIR", "mirrors"); D = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(D + "/sample.json"))
COMPS = ["kogen-loop", "kogen-coordinator", "kogen-verification", "kogen-shaping", "kogen-build", "kogen-executor", "kogen-setup", "kogen-review"]
g = lambda repo, *a: subprocess.run(["git", "--git-dir", f"{MD}/{repo}.git", *a], capture_output=True, text=True).stdout.strip()
os.makedirs(D + "/tuples", exist_ok=True)
for i, L in enumerate(S["sample"], 1):
    gomod = g("kogen", "show", L["kogen_main"] + ":cli/go.mod"); lines = []
    for c in COMPS:
        if c != "kogen-loop" and ("github.com/KogenAI/" + c + " ") not in gomod: continue
        sha = L["full"] if c == L["repo"] else g(c, "log", "--first-parent", "main", "--until=" + L["done"], "-1", "--format=%H")
        if sha: lines.append(f"{c} {sha}")
    open(D + f"/tuples/tuple-{i}.txt", "w").write("\n".join(lines) + "\n")
    print(i, L["role"], L["repo"], L["sha7"], [l.split()[0][6:9] + ":" + l.split()[1][:7] for l in lines])
