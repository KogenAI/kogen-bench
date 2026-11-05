#!/usr/bin/env python3
"""Phase 3 stage A: model-free compaction detectors (stdlib only).

Arm 2, transcript watcher: fires on a compaction ENTRY in the harness transcript.
  Claude Code: {"type":"system","subtype":"compact_boundary"} or a user entry with isCompactSummary true.
  Codex: a top-level {"type":"compacted"} entry or an event_msg of type context_compacted.
Arm 3, token-drop detector: fires on a call whose context tokens fell against the previous call's
  by >= DROP_FRAC (0.40) AND by >= DROP_ABS (5000). Fixed a priori (Studio r2), not tuned.
  Context tokens of a call: Claude = input + cache_read + cache_creation of that call's usage
  (the LAST iteration for `claude -p` json results); Codex = token_count last_token_usage.input_tokens.

A "turn" below is one model call (an assistant message with usage / one token_count event).
Latency = model calls completed after the compaction before the detector fires
(arm 2 reads the entry itself, so 0; arm 3 can only see the drop in the next call's usage, so >= 1).
"""
import json, sys, os

DROP_FRAC = 0.40
DROP_ABS = 5000


def ctx_claude(u):
    return (u.get('input_tokens') or 0) + (u.get('cache_read_input_tokens') or 0) + (u.get('cache_creation_input_tokens') or 0)


def events_claude(lines):
    """Yield ('call', ctx) and ('compact', kind) in file order. Main chain only (no sidechains).
    Streaming splits one API message over several entries: the last entry of a message.id wins,
    so a call is emitted when the next different id (or a non-assistant entry) arrives."""
    pend = None  # (id, ctx)
    out = []
    def flush():
        nonlocal pend
        if pend is not None:
            out.append(('call', pend[1]))
            pend = None
    for l in lines:
        try:
            d = json.loads(l)
        except Exception:
            continue
        if d.get('isSidechain'):
            continue
        t = d.get('type')
        if t == 'system' and d.get('subtype') == 'compact_boundary':
            flush(); out.append(('compact', 'compact_boundary'))
        elif t == 'user' and d.get('isCompactSummary'):
            flush(); out.append(('compact', 'isCompactSummary'))
        elif t == 'assistant':
            m = d.get('message') or {}
            u = m.get('usage')
            if not u or m.get('model') == '<synthetic>':
                continue
            c = ctx_claude(u)
            if c == 0:
                continue
            mid = m.get('id') or d.get('uuid')
            if pend is not None and pend[0] != mid:
                flush()
            pend = (mid, c)
        elif t in ('user',):
            flush()
    flush()
    return out


def events_codex(lines):
    out = []
    for l in lines:
        try:
            d = json.loads(l)
        except Exception:
            continue
        t = d.get('type'); p = d.get('payload') if isinstance(d.get('payload'), dict) else {}
        if t == 'compacted':
            out.append(('compact', 'compacted'))
        elif t == 'event_msg' and p.get('type') == 'context_compacted':
            out.append(('compact', 'context_compacted'))
        elif t == 'event_msg' and p.get('type') == 'token_count':
            info = p.get('info') or {}
            lu = info.get('last_token_usage') or {}
            c = lu.get('input_tokens') or 0
            if c:
                out.append(('call', c))
    return out


def score(events, truth_kinds=None):
    """events: list of ('call',ctx) / ('compact',kind). Ground truth = the compaction entries.
    Returns dict with counts. Arm 2 fires at each compact entry (latency 0). Arm 3 fires on a drop;
    a drop is a hit if a compaction entry lies between the previous call and this call (or, for
    entries written right after the call, the nearest in the window) else a false alarm.
    Several compact entries with no call between them count as one compaction (one boundary + one
    summary entry per compaction in Claude Code)."""
    # collapse compact entries with no call between them
    comps = []  # index in call sequence AFTER which compaction happened (number of calls before it)
    calls = []
    ncomp_entries = 0
    for k, v in events:
        if k == 'call':
            calls.append(v)
        else:
            ncomp_entries += 1
            if not comps or comps[-1] != len(calls):
                comps.append(len(calls))
    drops = []  # index i of the call (0-based) where ctx[i] dropped vs ctx[i-1]
    for i in range(1, len(calls)):
        a, b = calls[i - 1], calls[i]
        if a - b >= DROP_ABS and (a - b) >= DROP_FRAC * a:
            drops.append(i)
    hit = 0; lat3 = []; matched = set()
    missed = []
    for c in comps:
        # compaction after c calls: the first call that can show it is call index c
        # (entry written before the next call). Drop expected at index c (or the next few if the
        # compaction was the last event, no later call exists -> not observable)
        if c >= len(calls):
            missed.append(('unobservable', c)); continue
        cand = [d for d in drops if d == c]
        if cand:
            hit += 1; matched.add(cand[0]); lat3.append(1)
        else:
            missed.append(('nodrop', c, calls[c - 1] if c else None, calls[c]))
    fa = [d for d in drops if d not in matched]
    return dict(calls=len(calls), compactions=len(comps), compact_entries=ncomp_entries,
                arm2_hits=len(comps), arm2_misses=0,
                arm3_hits=hit, arm3_unobservable=sum(1 for m in missed if m[0] == 'unobservable'),
                arm3_miss_nodrop=sum(1 for m in missed if m[0] == 'nodrop'),
                arm3_false_alarms=len(fa), arm3_latency_calls=lat3,
                missed_detail=[m for m in missed if m[0] == 'nodrop'][:20],
                fa_detail=[(d, calls[d - 1], calls[d]) for d in fa][:20])


def load(path, kind):
    with open(path, errors='replace') as f:
        lines = f.readlines()
    return events_claude(lines) if kind == 'claude' else events_codex(lines)


if __name__ == '__main__':
    kind, path = sys.argv[1], sys.argv[2]
    print(json.dumps(score(load(path, kind))))
