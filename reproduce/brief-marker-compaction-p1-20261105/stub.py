#!/usr/bin/env python3
"""Tiny Studio stand-in: an MCP stdio server (stdlib only).

Env:
  STUB_CELL    cell directory (cell.json is read from it; calls.jsonl is appended)
cell.json:
  mode     marker | firstmsg | none
  reserve  0 | 1   (1 = return the brief in the response of a call whose marker is missing/stale)
  ticket, prefix  the per-cell rule values (R1, R2)
  brief_rev       brief revision label (the marker hashes it with a nonce)

Tools:
  studio_start  issues the brief (and the marker, in marker mode)
  studio_note   the loop's work call; the stub checks the rules and the marker and logs everything
"""
import hashlib, json, os, sys, time

CELL = os.environ["STUB_CELL"]
CFG = json.load(open(os.path.join(CELL, "cell.json")))
LOG = os.path.join(CELL, "calls.jsonl")
MODE, RESERVE = CFG["mode"], int(CFG.get("reserve", 0))
MARKER = "SB-" + hashlib.sha256((CFG["brief_rev"] + CFG["nonce"]).encode()).hexdigest()[:8]
BASE_FIRST = os.path.join(CELL, "first.last")


FILLER = [
    "Keep each answer under 120 words.",
    "Prefer plain words over jargon; define any acronym on first use.",
    "Never invent numbers; say 'unknown' when a figure is not given.",
    "Write in British English spelling.",
    "Do not use bullet characters other than '(1)', '(2)', '(3)'.",
    "Never mention competitors by name.",
    "Do not ask the user questions during the loop; make a reasonable choice and continue.",
    "Never paste code longer than three lines into a note.",
    "Use UTC for any time you mention.",
]


def brief():
    rules = FILLER[:4] + [
        "Every studio_note call carries ticket=\"" + CFG["ticket"] + "\".",
        "Every studio_note text starts with the tag \"[" + CFG["prefix"] + "]\".",
    ] + FILLER[4:]
    if MODE == "marker":
        rules.append("Every Studio call (studio_start, studio_note) carries marker=\"" + MARKER + "\" (the marker of this brief).")
    if MODE == "firstmsg":
        rules.append("Every Studio call carries first=<the first 8 words, verbatim, of the FIRST user message currently in your context window>.")
    return "\n".join(["STUDIO BRIEF rev " + CFG["brief_rev"] + " (standing rules for this loop; they stay in force for the whole loop):"]
                     + ["R%d. %s" % (i + 1, r) for i, r in enumerate(rules)])


def norm(s):
    return " ".join("".join(c for c in w.lower() if c.isalnum()) for w in (s or "").split()[:8])


def log(rec):
    rec["t"] = time.time()
    with open(LOG, "a") as f:
        f.write(json.dumps(rec) + "\n")


def check_signal(args):
    """Return (detected, why) for the hook-free signal of this mode."""
    if MODE == "marker":
        m = args.get("marker")
        if m is None or m == "":
            return True, "missing"
        return (m != MARKER), ("stale" if m != MARKER else "ok")
    if MODE == "firstmsg":
        f = norm(args.get("first"))
        if not f:
            return True, "missing"
        # Studio cannot see the conversation; it compares the agent-reported prefix with the LAST one it saw.
        prev = open(BASE_FIRST).read() if os.path.exists(BASE_FIRST) else None
        open(BASE_FIRST, "w").write(f)
        if prev is None:
            return False, "baseline"
        return (f != prev), ("changed" if f != prev else "ok")
    return False, "n/a"


def call_tool(name, args):
    if name == "studio_start":
        det, why = check_signal(args) if MODE == "firstmsg" else (False, "start")
        log({"tool": name, "args": args, "signal": why})
        return brief() + "\nAcknowledge the rules, then wait for the next step."
    if name == "studio_note":
        det, why = check_signal(args)
        r1 = args.get("ticket") == CFG["ticket"]
        r2 = str(args.get("text", "")).startswith("[" + CFG["prefix"] + "]")
        served = bool(det and RESERVE)
        log({"tool": name, "args": args, "signal": why, "detected": det, "r1": r1, "r2": r2, "reserved": served})
        out = "noted step " + str(args.get("step"))
        if served:
            out += "\nYour Studio brief is missing or out of date. Current brief follows; apply it from now on.\n" + brief()
        return out
    raise KeyError(name)


TOOLS = [
    {"name": "studio_start", "description": "Fetch the Studio brief for this loop. Call once at the start.",
     "inputSchema": {"type": "object", "properties": {"marker": {"type": "string"}, "first": {"type": "string"}}}},
    {"name": "studio_note", "description": "Record one loop step in Studio.",
     "inputSchema": {"type": "object", "properties": {
         "step": {"type": "integer"}, "text": {"type": "string"}, "ticket": {"type": "string"},
         "marker": {"type": "string"}, "first": {"type": "string"}}, "required": ["step", "text"]}},
]


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        mid, meth = msg.get("id"), msg.get("method")
        if mid is None:
            continue  # notification
        if meth == "initialize":
            res = {"protocolVersion": msg.get("params", {}).get("protocolVersion", "2025-06-18"),
                   "capabilities": {"tools": {}}, "serverInfo": {"name": "studio-stub", "version": "1"}}
            log({"tool": "_initialize"})
        elif meth == "tools/list":
            res = {"tools": TOOLS}
        elif meth == "tools/call":
            p = msg.get("params", {})
            try:
                res = {"content": [{"type": "text", "text": call_tool(p.get("name"), p.get("arguments") or {})}]}
            except KeyError:
                res = {"content": [{"type": "text", "text": "unknown tool"}], "isError": True}
        elif meth == "ping":
            res = {}
        else:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "no method"}}) + "\n")
            sys.stdout.flush()
            continue
        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": mid, "result": res}) + "\n")
        sys.stdout.flush()


def hook():
    """Claude Code SessionStart hook (matcher "compact"): log the event; print the brief if hook_reserve=1."""
    try:
        ev = json.load(sys.stdin)
    except ValueError:
        ev = {}
    with open(os.path.join(CELL, "hooks.jsonl"), "a") as f:
        f.write(json.dumps({"t": time.time(), "event": ev.get("hook_event_name"), "source": ev.get("source")}) + "\n")
    if int(CFG.get("hook_reserve", 0)):
        sys.stdout.write("Context was compacted. Your Studio brief, re-served:\n" + brief() + "\n")


if __name__ == "__main__":
    hook() if sys.argv[1:] == ["--hook"] else main()
