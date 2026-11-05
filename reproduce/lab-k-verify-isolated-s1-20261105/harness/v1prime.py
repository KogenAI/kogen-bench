#!/usr/bin/env python3
"""v1prime.py <label> <tree> ... : V1' static baseline over step files (features/steps/*.js) and acceptance features of a tree.
Rules (only what Stage 0 showed text can decide): fixed-number listen() port; write/mkdir/remove call on a literal absolute path outside scratch.
Prints one JSON line per hit and a summary line. No model, read-only."""
import re, sys, os, json, glob
PORT = re.compile(r'\.listen\(\s*(?!0\b)(\d{3,5})\b|\.listen\(\s*\{[^}]*\bport\s*:\s*(?!0\b)(\d{3,5})\b')
WRITE = re.compile(r'\b(?:mkdirSync|writeFileSync|appendFileSync|createWriteStream|rmSync|copyFileSync|renameSync|openSync|mkdir|writeFile|appendFile)\(\s*[\'"`](/(?:tmp|var/tmp|home|Users|opt|srv|etc|root|private|mnt|data)(?:/[^\'"`]*)?)[\'"`]')
def scan_text(txt):
    hits = []
    for i, l in enumerate(txt.split('\n'), 1):
        s = l.lstrip()
        if s.startswith(('//', '*', '#')): continue
        if PORT.search(l): hits.append(dict(cls='port', line=i, text=l.strip()[:160]))
        if WRITE.search(l): hits.append(dict(cls='path', line=i, text=l.strip()[:160]))
    return hits
def files(tree):
    return sorted(glob.glob(tree + '/features/steps/*.js') + glob.glob(tree + '/.kogen/intents/*/acceptance.feature'))
if __name__ == '__main__':
    label = sys.argv[1]; tot = 0; flagged = 0
    for tree in sys.argv[2:]:
        for f in files(tree):
            tot += 1; h = scan_text(open(f, errors='replace').read())
            if h: flagged += 1
            for x in h: print(json.dumps(dict(corpus=label, file=os.path.relpath(f, tree), **x)))
    print(json.dumps(dict(summary=label, files=tot, files_flagged=flagged)))
