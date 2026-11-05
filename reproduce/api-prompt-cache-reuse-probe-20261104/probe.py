#!/usr/bin/env python3
"""Prompt-cache reuse probe over stdlib HTTP.
Key: the ANTHROPIC_API_KEY environment variable; never printed.
Cell cap USD 5 (hard stop at 90%). Usage: ANTHROPIC_API_KEY=... python3 -I probe.py OUT.jsonl"""
import json, os, sys, time, uuid, urllib.request, urllib.error

CAP = 5.00
_k = os.environ["ANTHROPIC_API_KEY"]
PRICE = {"claude-sonnet-5-5": (2.0, 2.5, 0.20, 10.0), "claude-haiku-5-5": (0.10, 0.125, 0.01, 0.50)}  # in, write5m, read, out ($/MTok)
BETA = "mid-conversation-output-config-2026-07-01"
nonce = uuid.uuid4().hex
spent = 0.0
words = ("The build agent edits files, runs tests, and reports a short summary. "
         "Rule {i}: keep diffs small, never touch unrelated files, and record every decision. ")
system_text = f"[run {nonce}] You are a terse assistant.\n" + "".join(words.format(i=i) for i in range(260))
tools = [
    {"name": "read_file", "description": "Read a file by path.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "run_tests", "description": "Run the test suite.",
     "input_schema": {"type": "object", "properties": {"target": {"type": "string"}}}},
]
system = [{"type": "text", "text": system_text, "cache_control": {"type": "ephemeral"}}]
user1_text = f"[ctx {nonce}] " + "".join(f"Context note {i}: the module tree is stable. " for i in range(120))
USER1 = {"role": "user", "content": [
    {"type": "text", "text": user1_text, "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": "Reply with the single word OK."}]}


def cost(model, u):
    pin, pw, pr, po = PRICE[model]
    return (u["input"] * pin + u["write"] * pw + u["read"] * pr + u["out"] * po) / 1e6


def post(body, beta):
    h = {"x-api-key": _k, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    if beta:
        h["anthropic-beta"] = BETA
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", json.dumps(body).encode(), h)
    try:
        return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read()[:300].decode(errors='replace')}")


def call(label, model, effort, thinking="omit", messages=None, beta=False, note=""):
    global spent
    if spent >= CAP * 0.9:
        print("STOP: near cap", spent); sys.exit(2)
    kw = dict(model=model, max_tokens=3000, system=system, tools=tools, messages=messages or [USER1])
    if effort is not None:
        kw["output_config"] = {"effort": effort}
    if thinking in ("adaptive", "between_tools"):
        kw["thinking"] = {"type": thinking}
    row = dict(label=label, model=model, effort=effort, thinking=thinking, note=note)
    try:
        r = post(kw, beta)
        u = r["usage"]
        usage = dict(input=u.get("input_tokens", 0), write=u.get("cache_creation_input_tokens") or 0,
                     read=u.get("cache_read_input_tokens") or 0, out=u.get("output_tokens", 0))
        c = cost(model, usage); spent += c
        row.update(usage=usage, cost=round(c, 6), stop=r.get("stop_reason"), spent=round(spent, 6))
    except Exception as e:  # noqa
        row.update(error=f"{type(e).__name__}: {str(e)[:300]}")
    print(json.dumps(row), flush=True)
    with open(sys.argv[1], "a") as f:
        f.write(json.dumps(row) + "\n")
    time.sleep(2)
    return row


S, H = "claude-sonnet-5-5", "claude-haiku-5-5"
call("a", S, "low", "adaptive", note="create expected")
call("b", S, "low", "adaptive", note="baseline read")
call("c", S, "high", "adaptive", note="effort low->high")
call("c2", S, "low", "adaptive", note="back to low after c wrote at high")
call("d1", S, "low", "omit", note="thinking omitted (= default adaptive?)")
call("d2", S, "low", "between_tools", note="thinking off (between_tools)")
call("e", H, "low", "adaptive", note="different model, same prefix (expect miss)")
call("h1", H, "low", "adaptive", note="haiku baseline read")
call("h2", H, "high", "adaptive", note="haiku effort low->high")
call("f0", S, "low", "adaptive", beta=True, note="beta warm: [user1]")
msgs = [USER1, {"role": "assistant", "content": "OK"},
        {"role": "system", "content": [], "output_config": {"effort": "high"}},
        {"role": "user", "content": "Reply with the single word DONE."}]
call("f1", S, "low", "adaptive", messages=msgs, beta=True, note="per-message effort high via system msg")
print("TOTAL_SPENT", round(spent, 6))
