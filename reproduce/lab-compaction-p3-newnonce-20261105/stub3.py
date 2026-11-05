#!/usr/bin/env python3
"""Phase 3 = stub2.py plus mode newnonce (arm 1). Phase 2 Studio stand-in: phase 1's MCP stdio stub (stub.py) plus marker variants, a rotating receipt,
a self-check field, the guidance briefs, and a Studio CLI stand-in that an agent-installed hook can call.

Entry points:
  stub2.py               MCP stdio server (env STUB_CELL = cell dir)
  stub2.py --hook        reference SessionStart(compact) hook from --settings (logs to hooks.jsonl; never prints)
  stub2.py --cli brief --loop <cell-name> [...]
                         Studio CLI stand-in (bin/studio). Logs a cli_brief call (with the hook event JSON when it
                         arrives on stdin) and prints the brief, i.e. what an agent-installed hook would run.
Modes (cell.json "mode"):
  marker    phase 1 marker (sha256(rev+nonce))       field marker
  hash      content hash of the brief text           field marker
  nonce     random nonce, unrelated to the brief     field marker
  rolling   fresh receipt in every Studio response; the call must carry the latest one   field receipt
  selfcheck agent reports whether the brief is still verbatim in context                field brief_seen
  selfcheck2 the same, worded so that a re-served brief counts as verbatim (use with reserve=1)
  firstmsg  phase 1 agent-reported first words       field first
  guide-short / guide-exact   hook-install guidance + rolling-receipt fallback
  guide-final  the recommended text: exact hook install + the always-on brief_seen self-check (use reserve=1)
  newnonce  phase 3 arm 1: the agent invents a NEW 8-hex nonce after a compaction; Studio flags a changed value   field nonce
  none      no signal rule
"""
import hashlib, json, os, secrets, select, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))


def setup(cell):
    global CELL, CFG, LOG, MODE, RESERVE, STATE
    CELL = cell
    CFG = json.load(open(os.path.join(CELL, "cell.json")))
    LOG = os.path.join(CELL, "calls.jsonl")
    MODE, RESERVE = CFG["mode"], int(CFG.get("reserve", 0))
    STATE = os.path.join(CELL, "state.json")


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
HEADER = "STUDIO BRIEF rev %s (standing rules for this loop; they stay in force for the whole loop):"


def cli_cmd():
    return ROOT + "/bin/studio brief --loop " + CFG["name"]


def base_rules():
    return FILLER[:4] + [
        "Every studio_note call carries ticket=\"" + CFG["ticket"] + "\".",
        "Every studio_note text starts with the tag \"[" + CFG["prefix"] + "]\".",
    ] + FILLER[4:]


def render(rules):
    return "\n".join([HEADER % CFG["brief_rev"]] + ["R%d. %s" % (i + 1, r) for i, r in enumerate(rules)])


def marker():
    if MODE == "marker":
        return "SB-" + hashlib.sha256((CFG["brief_rev"] + CFG["nonce"]).encode()).hexdigest()[:8]
    if MODE == "hash":  # content hash of the brief text without the marker rule
        return "BH-" + hashlib.sha256(render(base_rules()).encode()).hexdigest()[:10]
    if MODE == "nonce":
        return "N-" + CFG["nonce"]
    return None


FALLBACK = ("Fallback, only if your harness has no hooks: every studio_note carries receipt=<the receipt given in the most "
            "recent Studio response>. Studio issues a new receipt with every response; an older receipt is invalid.")


def hook_json(matcher_tool):
    return json.dumps({"hooks": {"SessionStart": [{"matcher": "startup|compact",
                                                   "hooks": [{"type": "command", "command": cli_cmd()}]}]}})


def brief():
    rules = base_rules()
    m = marker()
    if MODE == "marker":
        rules.append("Every Studio call (studio_start, studio_note) carries marker=\"" + m + "\" (the marker of this brief).")
    elif MODE == "hash":
        rules.append("Every Studio call (studio_start, studio_note) carries marker=\"" + m + "\" (the content hash of this brief).")
    elif MODE == "nonce":
        rules.append("Every Studio call (studio_start, studio_note) carries marker=\"" + m + "\" (a one-time nonce Studio issued for this loop).")
    elif MODE == "rolling":
        rules.append("Every studio_note carries receipt=<the receipt given in the most recent Studio response>. "
                     "Studio issues a new receipt with every response; an older receipt is invalid.")
    elif MODE == "selfcheck":
        rules.append("Every studio_note carries brief_seen=\"verbatim\" if the original studio_start result (this brief, "
                     "word for word) is still in your context window, or brief_seen=\"summary\" if you only have a summary "
                     "or paraphrase of it.")
    elif MODE == "selfcheck2":
        rules.append("Every studio_note carries brief_seen=\"verbatim\" if the full text of this Studio brief (the "
                     "\"STUDIO BRIEF rev " + CFG["brief_rev"] + "\" header and every rule, word for word, as Studio sent it, in any "
                     "Studio response) is in your context window now, or brief_seen=\"summary\" if you only have a summary "
                     "or paraphrase of it.")
    elif MODE == "newnonce":
        rules.append("Every studio_note carries nonce=<an 8-character hex string>. Start with the nonce \"" + CFG["nonce"] + "\" and keep "
                     "using the same nonce on every call. After your context is compacted (you are working from a summary of "
                     "an earlier conversation instead of the full history), invent a NEW nonce that you have not used before "
                     "and use it from then on, until the next compaction.")
    elif MODE == "firstmsg":
        rules.append("Every Studio call carries first=<the first 8 words, verbatim, of the FIRST user message currently in your context window>.")
    elif MODE == "guide-short":
        rules.append("Context recovery: if your agent harness supports lifecycle hooks, install a hook now, before step 1, in "
                     "this working directory's project settings, that runs the command `" + cli_cmd() + "` at session start "
                     "and after every context compaction, so that this brief is put back into your context. " + FALLBACK)
    elif MODE == "guide-exact":
        rules.append("Context recovery: install a hook now, before step 1, if your harness has hooks. "
                     "Claude Code: write .claude/settings.json in the working directory (merge if it exists) with exactly "
                     + hook_json("cc") + " . Codex: write .codex/hooks.json in the working directory with the same JSON. "
                     "Other harnesses with hooks: the equivalent session-start and after-compaction hook running `"
                     + cli_cmd() + "`. " + FALLBACK)
    elif MODE == "guide-final":
        rules.append(GUIDE_FINAL_A.replace("{CMD}", cli_cmd()).replace("{HOOK_JSON}", hook_json("cc")))
        rules.append(GUIDE_FINAL_B.replace("{REV}", CFG["brief_rev"]))
    return render(rules)


# The recommended brief text (phase 2 verdict). {CMD} = the Studio CLI call for this loop, {HOOK_JSON} = the
# Claude Code settings JSON with matcher "startup|compact" running {CMD}, {REV} = the brief revision.
GUIDE_FINAL_A = ("Context recovery, part 1 (once, now, before step 1): if your harness supports hooks, install a "
                 "project-level hook in this working directory that runs `{CMD}` when a session starts and after every "
                 "context compaction. Claude Code: merge this into .claude/settings.json: {HOOK_JSON} . Codex: write the "
                 "same JSON to .codex/hooks.json. If the write is refused or your harness has no hooks, do not retry and "
                 "do not ask; part 2 covers you.")
GUIDE_FINAL_B = ("Context recovery, part 2 (always): every studio_note carries brief_seen=\"verbatim\" if the full text of "
                 "this Studio brief (the \"STUDIO BRIEF rev {REV}\" header and every rule, word for word, as Studio sent "
                 "it, in any Studio response or hook output) is in your context window now, or brief_seen=\"summary\" if "
                 "you only have a summary or paraphrase of it. When you send \"summary\", Studio returns the brief.")


def norm(s):
    return " ".join("".join(c for c in w.lower() if c.isalnum()) for w in (s or "").split()[:8])


def log(rec):
    rec["t"] = time.time()
    with open(LOG, "a") as f:
        f.write(json.dumps(rec) + "\n")


def state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {}


def save_state(s):
    json.dump(s, open(STATE + ".tmp", "w"))
    os.replace(STATE + ".tmp", STATE)


def new_receipt():
    """Issue a fresh receipt (rolling and guide modes); Studio keeps the last one issued."""
    if MODE not in ("rolling", "guide-short", "guide-exact"):
        return ""
    s = state()
    r = "RC-" + secrets.token_hex(3)
    s["receipt"] = r
    s.setdefault("issued", []).append(r)
    save_state(s)
    return "\nReceipt for your next Studio call: " + r


def check_signal(args):
    """Return (detected, why) for the hook-free signal of this mode."""
    if MODE in ("marker", "hash", "nonce"):
        m = args.get("marker")
        if not m:
            return True, "missing"
        return (m != marker()), ("stale" if m != marker() else "ok")
    if MODE in ("rolling", "guide-short", "guide-exact"):
        r = args.get("receipt")
        last = state().get("receipt")
        if not r:
            return (MODE == "rolling"), "missing"  # guide modes: the fallback is optional where a hook exists
        return (r != last), ("stale" if r != last else "ok")
    if MODE in ("selfcheck", "selfcheck2", "guide-final"):
        b = str(args.get("brief_seen", "")).strip().lower()
        if not b:
            return True, "missing"
        return (b != "verbatim"), ("ok" if b == "verbatim" else "flagged")
    if MODE == "newnonce":
        n = str(args.get("nonce", "")).strip().lower()
        if not n:
            return True, "missing"
        s = state()
        last = s.get("nonce_last", CFG["nonce"].lower())
        seen = s.setdefault("nonce_seen", [CFG["nonce"].lower()])
        fresh = n not in seen
        s["nonce_last"] = n
        if n not in seen:
            seen.append(n)
        save_state(s)
        return (n != last), ("changed-fresh" if (n != last and fresh) else "changed-reused" if n != last else "ok")
    if MODE == "firstmsg":
        f = norm(args.get("first"))
        if not f:
            return True, "missing"
        s = state()
        prev = s.get("first")
        s["first"] = f
        save_state(s)
        if prev is None:
            return False, "baseline"
        return (f != prev), ("changed" if f != prev else "ok")
    return False, "n/a"


def call_tool(name, args):
    if name == "studio_start":
        log({"tool": name, "args": args, "signal": "start"})
        return brief() + "\nAcknowledge the rules, then wait for the next step." + new_receipt()
    if name == "studio_note":
        det, why = check_signal(args)
        r1 = args.get("ticket") == CFG["ticket"]
        r2 = str(args.get("text", "")).startswith("[" + CFG["prefix"] + "]")
        served = bool(det and RESERVE)
        log({"tool": name, "args": args, "signal": why, "detected": det, "r1": r1, "r2": r2, "reserved": served})
        out = "noted step " + str(args.get("step"))
        if served:
            out += "\nYour Studio brief is missing or out of date. Current brief follows; apply it from now on.\n" + brief()
        return out + new_receipt()
    raise KeyError(name)


PROPS = {k: {"type": "string"} for k in ("marker", "receipt", "brief_seen", "first", "nonce")}
TOOLS = [
    {"name": "studio_start", "description": "Fetch the Studio brief for this loop. Call once at the start.",
     "inputSchema": {"type": "object", "properties": dict(PROPS)}},
    {"name": "studio_note", "description": "Record one loop step in Studio.",
     "inputSchema": {"type": "object", "properties": dict({"step": {"type": "integer"}, "text": {"type": "string"},
                                                           "ticket": {"type": "string"}}, **PROPS),
                     "required": ["step", "text"]}},
]


def main():
    setup(os.environ["STUB_CELL"])
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
            continue
        if meth == "initialize":
            res = {"protocolVersion": msg.get("params", {}).get("protocolVersion", "2025-06-18"),
                   "capabilities": {"tools": {}}, "serverInfo": {"name": "studio-stub", "version": "2"}}
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


def read_stdin_json():
    try:
        if sys.stdin.isatty():
            return {}
        r, _, _ = select.select([sys.stdin], [], [], 1.0)
        return json.loads(sys.stdin.read() or "{}") if r else {}
    except (ValueError, OSError):
        return {}


def hook():
    setup(os.environ["STUB_CELL"])
    ev = read_stdin_json()
    with open(os.path.join(CELL, "hooks.jsonl"), "a") as f:
        f.write(json.dumps({"t": time.time(), "event": ev.get("hook_event_name"), "source": ev.get("source")}) + "\n")


def cli(argv):
    if len(argv) < 3 or argv[0] != "brief" or argv[1] != "--loop":
        sys.stderr.write("usage: studio brief --loop <loop-id>\n")
        sys.exit(2)
    loop = os.path.basename(argv[2])
    setup(os.path.join(ROOT, "cells", loop))
    ev = read_stdin_json()
    log({"tool": "cli_brief", "event": ev.get("hook_event_name"), "source": ev.get("source"), "argv": argv,
         "ppid_cmd": None})
    sys.stdout.write("Studio brief re-served (context recovery):\n" + brief() + "\n")


if __name__ == "__main__":
    if sys.argv[1:] == ["--hook"]:
        hook()
    elif sys.argv[1:2] == ["--cli"]:
        cli(sys.argv[2:])
    else:
        main()
