"""Cost guard: the spend estimate of a run dir and its soft and hard caps (FORMATS.md, "Cost cap").

Spend = finished cells' `totals.cost_usd` + the live spend of running cells, read from their Kogen run
logs and shaping events as requests complete + the ledger of earlier attempts that were thrown away.
A request that cannot be priced counts at a conservative fallback:

- a model with no price row, or a price cost_calc cannot give: if `reproduce/guard-estimates.json` lists
  the model (`{"models": {model: {"as": priced model, "note": why}}}`), the request's tokens at the rates of
  the priced model named by `as`; otherwise the request's tokens at the highest input, cached-input and
  output rate in `reproduce/price-table-v1.json`. A guard estimate is for this spend estimate only: reported
  costs (`usage.request_cost`, records, result totals, exports) never read it, so an unpriced model stays
  unpriced (`cost_usd` null, `cost_reason` `unlisted_model`) in every published figure. The price table is
  hash-pinned, so the estimates live in their own file;
- a request with unknown usage (null counters, or a build request whose four counters are all 0, which
  Kogen logs for unknown): `FALLBACK_TOKENS`, an allowance above the largest request seen in real logs
  (53,940 uncached input tokens), at those rates. It is an allowance, not a proven bound.

The guard fails closed on real errors: unreadable or unparsable usage, no price table, a crash of the guard
(see `Watcher`, `check_start`). A source that is gone because its attempt finished or was retired is not an
error: the steps that move spend from one record to the next (live workspace -> result.json or spent.json,
cell dir -> ledger) hold the run dir's lock (`locked`), and readers take it too, so each attempt is counted
exactly once. A source gone with no final record is retried for `RETRY_S` seconds, then the guard fails closed.
A cell that died hard leaves a phantom `live.json`; `reap_phantoms` settles it into a `spent.json` first, so it
is a final record and not a gone source.
`cost_cap_usd` covers ChatGPT-priced spend only; `provider_caps` cap the cells (and optionally the USD) of every
other provider; a provider's first rate-limit failure stops new cells of that provider (`rate-limit-stop.json`).
`python3 -m lanes.costguard cells <run-dir>` prints `{cell: usd}` (the controller polls it on remote hosts).
"""

import contextlib
import fcntl
import glob
import json
import os
import re
import shutil
import sys
import threading
import time

from . import common, experiment, live, usage

HARD_FACTOR = 1.25  # hard cap = HARD_FACTOR * cost_cap_usd
FALLBACK_TOKENS = {"input_tokens": 100_000, "cached_input_tokens": 0, "output_tokens": 20_000}
LIVE = "live.json"    # in a running cell's dir: its workspace and the pid and start time of its lanes-cell
STALE = "live.json.stale-finished"  # a `live.json` left beside a `result.json`, moved aside by `reap_phantoms`
REAPED = "live.json.reaped"  # a phantom `live.json` (its process died hard), moved aside by `reap_phantoms`
PHANTOM_REQUESTS = 5  # requests a phantom cell is assumed to have spent when nothing else is known (see `phantom_estimate`)
SPENT = "spent.json"  # in a cell dir that stopped without result.json: what it had spent
LEDGER = "cost-ledger.jsonl"  # in the run dir: spend of attempts whose cell dir was thrown away
STOP = "cost-stop.json"       # in the run dir: which cap stopped the run
RATE = "rate-limit-stop.json"  # in the run dir: the providers that hit a rate or usage limit
LIMIT_WORDS = ("usage_limit", "rate_limit", "rate-limit", "too_many_requests")  # in a Kogen error class or reason
LOCK = ".cost.lock"           # in the run dir: the spend lock
RETRY_S = 5.0  # how long a source that is gone without a final record is retried before failing closed
GUARD_ESTIMATES = os.path.join(os.path.dirname(__file__), "..", "..", "reproduce", "guard-estimates.json")
_pricing = None
_estimates = None


class CostCapError(Exception):
    """The run dir has no cap, has reached it, or its spend cannot be read."""


class _Gone(Exception):
    """A spend source is gone and its attempt has no final record (yet)."""


@contextlib.contextmanager
def locked(run_dir, exclusive=True):
    """The run dir's spend lock: steps that move spend between records hold it exclusively, readers shared."""
    fd = None
    if os.path.isdir(run_dir):
        fd = os.open(os.path.join(run_dir, LOCK), os.O_RDWR | os.O_CREAT, 0o644)
        fcntl.flock(fd, fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)  # releases the lock


def _retrying(run_dir, fn, exclusive=False, retry_s=None, before=None):
    """`fn()` under the lock; a source gone without a final record is retried (lock released), then fails closed.
    `before()` runs ahead of every try, lock not held (a process that just died may need a moment to be seen dead)."""
    end = time.monotonic() + (RETRY_S if retry_s is None else retry_s)
    while True:
        if before:
            before()
        try:
            with locked(run_dir, exclusive):
                return fn()
        except (FileNotFoundError, _Gone) as e:
            if time.monotonic() >= end:
                raise CostCapError(f"a spend source is gone with no final record ({e}); the cost guard fails closed") \
                    from None
        time.sleep(0.1)


def caps(exp):
    """`(soft, hard)` in USD; CostCapError, with how to add the cap, when the experiment has none."""
    cap = exp.get("cost_cap_usd")
    if cap is None:
        raise CostCapError('experiment.json has no "cost_cap_usd": add it (a positive number of USD; the '
                           'hard cap is 1.25 times it), then run lanes-plan again so PLAN.json carries it')
    return cap, cap * HARD_FACTOR


def pricing():
    """`(cost_calc, table, top rates)`, loaded once per process; raises when they cannot be loaded."""
    global _pricing
    if _pricing is None:
        calc = usage._cost_calc()
        table = calc.load_table()
        _pricing = calc, table, usage.top_rates(table)
    return _pricing


def guard_estimates():
    """`{model: {"as": priced model, "note": ...}}` of `guard-estimates.json`, loaded once; {} when the file is
    absent (older checkouts and remote hosts without it keep the highest-rate fallback). A malformed file or an
    `as` that has no complete price row in the table raises: the guard fails closed."""
    global _estimates
    if _estimates is None:
        _estimates = {}
        if os.path.isfile(GUARD_ESTIMATES):
            rows = common.read_json(GUARD_ESTIMATES)["models"]
            table = pricing()[1]["models"]
            for model, row in rows.items():
                target = table.get(row["as"])
                if not isinstance(row.get("note"), str) or not isinstance(target, dict) \
                        or any(not isinstance(target.get(k), (int, float)) for k in usage.RATES):
                    raise ValueError(f"{GUARD_ESTIMATES}: {model} must have a note and an `as` with a complete price row")
                _estimates[model] = row
    return _estimates


def _unpriced_cost(model, tokens, table, calc, rates):
    """Guard spend of a request that has no price: at its `guard_estimates` model's rates, else at the top rates."""
    row = guard_estimates().get(model) or guard_estimates().get((model or "").split("/", 1)[-1])
    if row:
        cost, _ = usage.request_cost(row["as"], tokens, table, calc)
        if cost is not None:
            return cost
    return _at_top(tokens, rates)


def _at_top(tokens, rates):
    uncached = tokens["input_tokens"] - tokens["cached_input_tokens"]
    return (uncached * rates["input"] + tokens["cached_input_tokens"] * rates["cached_input"]
            + tokens["output_tokens"] * rates["output"]) / 1e6


def log_spend(events, shape_events):
    """USD of the requests in a build log and shaping events, unknown prices at the fallback."""
    calc, table, rates = pricing()
    total = 0.0
    requests = [(r["model"], r["usage"], False) for r in usage.shape_requests(shape_events)]
    for e in events or []:
        if e.get("event") == "request":
            u = e.get("usage") or {}
            tokens = {k: u.get(v) for k, v in usage.USAGE_KEYS.items()}
            requests.append((e.get("model"), tokens, all(v == 0 for v in tokens.values())))
    for model, tokens, zero_unknown in requests:
        counts = [tokens.get(k) for k in ("input_tokens", "cached_input_tokens", "output_tokens")]
        if zero_unknown or None in counts:
            total += _at_top(FALLBACK_TOKENS, rates)
            continue
        if any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in counts) or counts[1] > counts[0]:
            raise ValueError(f"unparsable usage of a {model} request: {tokens}")
        cost, _ = usage.request_cost(model, tokens, table, calc)
        total += cost if cost is not None else _unpriced_cost(model, tokens, table, calc, rates)
    return total


def _read(path):
    """Events of a log being written. Only the text after the last newline may be a line still being
    written (skipped when it is not JSON yet); any other line that is not a JSON object raises."""
    with open(path, "rb") as f:
        lines = f.read().split(b"\n")
    out = []
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError:
            if i == len(lines) - 1:
                continue
            raise ValueError(f"{path}: line {i + 1} is not JSON") from None
        if not isinstance(event, dict):
            raise ValueError(f"{path}: line {i + 1} is not an event")
        out.append(event)
    return out


def _read_saved(path):
    """A log saved in a finished cell dir; [] when the cell has none (no build, no shaping)."""
    return _read(path) if os.path.isfile(path) else []


def workspace_spend(ws):
    """Spend so far of a cell workspace: its build run logs and shaping events."""
    events = [e for p in sorted(glob.glob(os.path.join(ws, ".kogen", "local", "runs", "*", "log.jsonl")))
              for e in _read(p)]
    shaping = [e for p in sorted(glob.glob(os.path.join(ws, ".kogen", "local", "shaping", "*", "events.ndjson")))
               for e in _read(p)]
    return log_spend(events, shaping)


def cell_spend(cell_dir):
    """USD of one cell dir: finished, running (live workspace) or stopped without a result."""
    path = os.path.join(cell_dir, "result.json")
    if os.path.isfile(path):
        totals = common.read_json(path).get("totals") or {}
        cost = totals.get("cost_usd") if totals.get("cost_complete", True) else None  # a partial sum falls back to the log estimate
        if cost is not None:
            return float(cost)
        return log_spend(_read_saved(os.path.join(cell_dir, "run-log", "log.jsonl")),
                         _read_saved(os.path.join(cell_dir, "shaping-events.ndjson")))
    if os.path.isfile(os.path.join(cell_dir, LIVE)):
        ws = common.read_json(os.path.join(cell_dir, LIVE))["workspace"]
        if os.path.isdir(ws):
            return workspace_spend(ws)
        if not os.path.isfile(os.path.join(cell_dir, SPENT)):
            raise _Gone(f"{cell_dir}: workspace {ws} is gone and the cell left no result.json or {SPENT}")
    if os.path.isfile(os.path.join(cell_dir, SPENT)):
        return float(common.read_json(os.path.join(cell_dir, SPENT))["usd"])
    return 0.0


def phantom_estimate(run_dir, ws):
    """Upper estimate in USD of a phantom cell's spend. The spend its workspace logs still show when they can be
    read (the cell logged every request that finished; one in flight is not in them). Otherwise the larger of an
    allowance of `PHANTOM_REQUESTS` unknown-usage requests (`FALLBACK_TOKENS` at the top rates, as `log_spend`
    counts a request with unknown usage) and the mean cost of the run's finished cells."""
    if ws and os.path.isdir(ws):
        try:
            return workspace_spend(ws)
        except (OSError, ValueError):
            pass
    allowance = PHANTOM_REQUESTS * _at_top(FALLBACK_TOKENS, pricing()[2])
    done = []
    for path in glob.glob(os.path.join(run_dir, "cells", "*", "r*", "*", "result.json")):
        try:
            cost = (common.read_json(path).get("totals") or {}).get("cost_usd")
        except (OSError, ValueError):
            continue
        if isinstance(cost, (int, float)) and not isinstance(cost, bool):
            done.append(float(cost))
    return max(allowance, sum(done) / len(done) if done else 0.0)


def reap_phantoms(run_dir, host=None, log=None):
    """Settle every phantom `live.json` under the run dir (`live.phantom`): write the cell's `spent.json` with
    `phantom_estimate` (unless it already has a `result.json` or `spent.json`), move `live.json` to `REAPED`, log
    one line. A `live.json` beside a `result.json` is moved to `STALE` (no spend change, no line). One locked step per cell, judged again under the lock. Returns the cells reaped."""
    log = log or (lambda m: print(m, file=sys.stderr))
    reaped = []
    for path in sorted(glob.glob(os.path.join(run_dir, "cells", "*", "r*", "*", LIVE))):
        cell_dir = os.path.dirname(path)
        if os.path.isfile(os.path.join(cell_dir, "result.json")):  # finished: its live.json is a leftover, whoever owns the pid
            with locked(run_dir):
                try:
                    os.replace(path, os.path.join(cell_dir, STALE))  # no spend change: result.json is the record
                except OSError:
                    pass  # the cell removed it itself
            continue
        try:
            if not live.phantom(common.read_json(path)):
                continue
        except (OSError, ValueError, KeyError):
            continue  # gone or half written: the cell is ending or starting
        with locked(run_dir):
            try:
                info = common.read_json(path)
            except (OSError, ValueError):
                continue
            why = live.phantom(info)
            if not why:
                continue
            cell = os.path.relpath(cell_dir, os.path.join(run_dir, "cells")).replace(os.sep, "/")
            if os.path.isfile(os.path.join(cell_dir, "result.json")) or os.path.isfile(os.path.join(cell_dir, SPENT)):
                usd = cell_spend(cell_dir)  # settled already: the process died between its steps
            else:
                usd = round(phantom_estimate(run_dir, info.get("workspace")), 8)
                common.write_json(os.path.join(cell_dir, SPENT), {"usd": usd})
            os.replace(path, os.path.join(cell_dir, REAPED))
        log(f"{info.get('host') or host or 'local'}: reaped phantom cell {cell} ({why}; "
            f"spend settled at ${usd:.4f}, upper estimate)")
        reaped.append(cell)
    return reaped


def cell_spends(run_dir):
    """`{cell: usd}` of the cell dirs under the run dir (no lock; see `snapshot`)."""
    cells = os.path.join(run_dir, "cells")
    return {os.path.relpath(p, cells).replace(os.sep, "/"): cell_spend(p)
            for p in glob.glob(os.path.join(cells, "*", "r*", "*")) if os.path.isdir(p)}


def snapshot(run_dir, retry_s=None):
    """`(cell_spends, ledger rows)` read under the lock, retried while a source is gone."""
    def read():
        path = os.path.join(run_dir, LEDGER)
        ledger = [(e["cell"], float(e["usd"])) for e in (common.read_jsonl(path) if os.path.isfile(path) else [])]
        return cell_spends(run_dir), ledger
    # reaping takes the lock itself: a phantom becomes a spent.json before it is read, on every try
    return _retrying(run_dir, read, retry_s=retry_s, before=lambda: reap_phantoms(run_dir))


def _append(run_dir, cell, usd):
    with open(os.path.join(run_dir, LEDGER), "a", encoding="utf-8") as f:
        f.write(json.dumps({"cell": cell, "usd": usd}, sort_keys=True) + "\n")


def ledger_add(run_dir, cell, usd):
    with locked(run_dir):
        _append(run_dir, cell, usd)


def retire(run_dir, cell, out, retry_s=None):
    """Throw away an old attempt's cell dir, keeping what it spent in the ledger (one locked step)."""
    reap_phantoms(run_dir)
    def move():
        if os.path.isdir(out):
            usd = cell_spend(out)
            if usd > 0:
                _append(run_dir, cell, usd)
            shutil.rmtree(out)
    _retrying(run_dir, move, exclusive=True, retry_s=retry_s)


def estimate(run_dir, per_lane=False, extra=None, retry_s=None):
    """Spend of the run dir in USD (rounded to 1e-8); with `per_lane`, `{lane: usd}` too.

    `extra` is `{cell: usd}` seen elsewhere (live spend on remote hosts); a cell counts the larger value.
    """
    spends, ledger = snapshot(run_dir, retry_s)
    for cell, usd in (extra or {}).items():
        spends[cell] = max(spends.get(cell, 0.0), usd)
    rows = list(spends.items()) + ledger
    lanes = {}
    for cell, usd in rows:
        lanes[cell.split("/")[-1]] = lanes.get(cell.split("/")[-1], 0.0) + usd
    total = round(sum(lanes.values()), 8)
    return (total, {k: round(v, 8) for k, v in sorted(lanes.items())}) if per_lane else total


def require_provider_caps(exp):
    """Before a cell starts: every provider other than ChatGPT that a lane uses needs a `provider_caps` entry
    (older run dirs lack it; read-only commands never ask). CostCapError says how to add it."""
    caps_ = exp.get("provider_caps") or {}
    for lane in exp.get("lanes", []):
        names = experiment.lane_providers(lane) - {experiment.CHATGPT}
        if len(names - {experiment.CLAUDE_CODE}) > 1:
            raise CostCapError(f"lane {lane['name']} names more than one non-ChatGPT provider: " + ", ".join(sorted(names)))
        for name in names:
            if not caps_.get(name):
                raise CostCapError(f'lane {lane["name"]} uses provider {name}: add "provider_caps": {{"{name}": '
                                   '{"cells": N}} to experiment.json (the cost cap covers ChatGPT only), then run '
                                   "lanes-plan again so PLAN.json carries it")


def lane_providers(exp):
    """`{lane: provider}` of the experiment's lanes (none for an experiment dict without lanes)."""
    return {l["name"]: experiment.lane_provider(l) for l in exp.get("lanes", [])}


def lane_cap_providers(exp):
    """`{lane: set of providers}` whose caps the lane's cells count against (`experiment.cap_providers`)."""
    return {l["name"]: experiment.cap_providers(l) for l in exp.get("lanes", [])}


def provider_spend(run_dir, exp, extra=None, retry_s=None):
    """`{provider: usd}`: the estimate split by the provider of each cell's lane (ChatGPT when unknown)."""
    _, lanes = estimate(run_dir, per_lane=True, extra=extra, retry_s=retry_s)
    names, out = lane_providers(exp), {}
    for lane, usd in lanes.items():
        p = names.get(lane, experiment.CHATGPT)
        out[p] = out.get(p, 0.0) + usd
    return {p: round(v, 8) for p, v in out.items()}


def started_cells(run_dir, exp, ignore=None):
    """`{provider: set of cells}` with a cell dir or a ledger line (a retired attempt still counts as started)."""
    names, out = lane_cap_providers(exp), {}
    cells = os.path.join(run_dir, "cells")
    found = {os.path.relpath(p, cells).replace(os.sep, "/") for p in glob.glob(os.path.join(cells, "*", "r*", "*"))
             if os.path.isdir(p)}
    path = os.path.join(run_dir, LEDGER)
    found |= {e["cell"] for e in (common.read_jsonl(path) if os.path.isfile(path) else [])}
    for cell in found - {ignore}:
        for p in names.get(cell.split("/")[-1], {experiment.CHATGPT}):
            out.setdefault(p, set()).add(cell)
    return out


def usd_caps(exp):
    """`{provider: (soft, hard)}` for the USD caps: ChatGPT's `cost_cap_usd` and any `provider_caps.<p>.usd`."""
    out = {p: (c["usd"], c["usd"] * HARD_FACTOR) for p, c in (exp.get("provider_caps") or {}).items() if "usd" in c}
    if exp.get("cost_cap_usd") is not None:
        out[experiment.CHATGPT] = caps(exp)
    return out


def rate_limited(run_dir):
    """`{provider: {cell, reason, at}}` from `rate-limit-stop.json`."""
    path = os.path.join(run_dir, RATE)
    return common.read_json(path) if os.path.isfile(path) else {}


def _limit_fields(failure):
    """The reason when a Kogen `provider_failure` record (`http_status`, `code`, `type`, `event_kind`) is a limit."""
    if not isinstance(failure, dict):
        return None
    if str(failure.get("http_status")) == "429":
        return "http_429"
    for k in ("code", "type"):
        v = failure.get(k)
        if isinstance(v, str) and any(w in v.lower() for w in LIMIT_WORDS):
            return v
    return None


def find_rate_limit(cell_dir):
    """The reason when a cell's saved logs show it failed on a rate or usage limit, else None.

    Kogen's structured records, in order: a build `outcome` event's `provider_failure` (written after the
    retries failed; a 429 a retry recovered is not one); a shaping `provider_call` that failed (`error` set)
    with `provider.provider_failure`; an event's `error`, `reason`, `code` or `outcome` class naming a limit;
    and, in stdout, Kogen's `provider/<reason>:` error line (reason names a limit) and its
    `provider failure: {json}` line. Free text is the last fallback, only for a `provider/<reason>:` line whose
    detail says HTTP 429, where Kogen gave no class."""
    for name in (os.path.join("run-log", "log.jsonl"), "shaping-events.ndjson"):
        path = os.path.join(cell_dir, name)
        for e in (_read_saved(path) if os.path.isfile(path) else []):
            prov = e.get("provider") if isinstance(e.get("provider"), dict) else {}
            found = (_limit_fields(e.get("provider_failure")) if e.get("event") == "outcome" else None) \
                or (_limit_fields(prov.get("provider_failure")) if e.get("event") == "provider_call" and e.get("error") else None)
            for k in ("error", "reason", "code", "outcome"):
                v = e.get(k)
                if not found and isinstance(v, str) and any(w in v.lower() for w in LIMIT_WORDS):
                    found = v
            if found:
                return found
    path = os.path.join(cell_dir, "stdout.txt")
    if os.path.isfile(path):
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                m = re.match(r"\s*provider failure: (\{.*\})\s*$", line)
                if m:
                    try:
                        found = _limit_fields(json.loads(m.group(1)))
                    except ValueError:
                        found = None
                    if found:
                        return found
                m = re.match(r"provider/([a-z_]+):(.*)", line)
                if m and (any(w in m.group(1) for w in LIMIT_WORDS) or re.search(r"\bHTTP 429\b", m.group(2))):
                    return "provider/" + m.group(1)
    return None


def note_rate_limit(run_dir, exp, cell):
    """After a cell: record the first rate-limit failure of its provider. Returns the reason, or None."""
    reason = find_rate_limit(common.cell_dir(run_dir, cell))
    if reason is None:
        return None
    provider = lane_providers(exp).get(cell.split("/")[-1], experiment.CHATGPT)
    with locked(run_dir):
        marks = rate_limited(run_dir)
        marks.setdefault(provider, {"cell": cell, "reason": reason, "rate_limited": True,
                                    "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        common.write_json(os.path.join(run_dir, RATE), marks)
    return reason


def blocked(exp, lane, spends, started, limits=None):
    """Why a new cell of `lane` may not start: a soft cap of its provider reached, its cell cap used up, or
    the provider rate limited. None when it may. `spends` is `provider_spend`, `started` is `started_cells`."""
    for provider in sorted(experiment.cap_providers(next(l for l in exp["lanes"] if l["name"] == lane))):
        cap = usd_caps(exp).get(provider)
        spent = spends.get(provider, 0.0)
        if cap and spent >= cap[0]:
            if provider == experiment.CHATGPT:
                return f"cost cap reached: spend ${spent:.4f} of the ${cap[0]:g} cap; no new cell starts"
            return f"cost cap reached: {provider} spend ${spent:.4f} of the ${cap[0]:g} cap; no new {provider} cell starts"
        cells = ((exp.get("provider_caps") or {}).get(provider) or {}).get("cells")
        if cells is not None and len(started.get(provider, ())) >= cells:
            return f"{provider} cell cap reached: {cells} cell(s) started; no new {provider} cell starts"
        if provider in (limits if limits is not None else {}):
            mark = limits[provider]
            return f"{provider} is rate limited ({mark['reason']} at {mark['cell']}); no new {provider} cell starts"
    return None


def over_hard(exp, spends, provider=None):
    """`[(provider, spent, hard)]` of the USD caps (of `provider` only, when given) whose hard limit is reached."""
    return [(p, spends[p], hard) for p, (_, hard) in usd_caps(exp).items()
            if provider in (None, p) and spends.get(p, 0.0) >= hard]


def record_stop(run_dir, cap, spent, provider=experiment.CHATGPT):
    """Note which cap stopped the run; a hard stop overrides a soft one, never the reverse."""
    path = os.path.join(run_dir, STOP)
    if cap == "hard" or not os.path.exists(path):
        common.write_json(path, {"cap": cap, "spent_usd": round(spent, 8), "provider": provider,
                                 "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})


def clear_stop(run_dir):
    """A new `lanes-run` starts without the stop note of the last one."""
    if os.path.exists(os.path.join(run_dir, STOP)):
        os.remove(os.path.join(run_dir, STOP))


def check_start(run_dir, exp, cell=None):
    """Refuse to start a cell once a soft cap of its provider is reached, its provider is rate limited, or
    when spend cannot be read. Without `cell`, the lane is taken as ChatGPT."""
    caps(exp)
    require_provider_caps(exp)
    lane = cell.split("/")[-1] if cell else None
    try:
        pricing()  # no price table, no guard: refuse rather than run uncapped
        spends = provider_spend(run_dir, exp)
        started = started_cells(run_dir, exp, ignore=cell) if cell else {}
        limits = rate_limited(run_dir)
    except Exception as e:
        raise CostCapError(f"cannot read the run's spend ({e}); the cost guard fails closed") from None
    provider = lane_providers(exp).get(lane, experiment.CHATGPT)
    why = blocked(exp, lane, spends, started, limits) if lane in lane_providers(exp) else (
        f"cost cap reached: spend ${spends.get(provider, 0.0):.4f} of the ${caps(exp)[0]:g} cap; no new cell starts"
        if spends.get(provider, 0.0) >= caps(exp)[0] else None)
    if why:
        if why.startswith("cost cap"):
            record_stop(run_dir, "soft", spends.get(provider, 0.0), provider)
        raise CostCapError(why)


class Watcher:
    """Thread that sets `tripped` once the hard cap of its cell's provider is reached (any, without `provider`), or the spend cannot be read."""

    def __init__(self, run_dir, exp, interval_s=None, provider=None):
        self.run_dir, self.exp, self.provider = run_dir, exp, provider
        caps(exp)
        self.interval = float(os.environ.get("LANES_COST_WATCH_S", 0.5)) if interval_s is None else interval_s
        self.tripped, self.error, self.spent = threading.Event(), None, None
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def _loop(self):
        while not self._stop.wait(self.interval):
            try:
                spends = provider_spend(self.run_dir, self.exp)
                self.spent = spends.get(experiment.CHATGPT, 0.0)
                hit = over_hard(self.exp, spends, self.provider)
                if hit:
                    record_stop(self.run_dir, "hard", hit[0][1], hit[0][0])
                    self.tripped.set()
                    return
            except Exception as e:  # fail closed: a guard that cannot read the spend stops the cell
                self.error = f"{type(e).__name__}: {e}"
                print(f"cost guard: {self.error}; stopping the cell", file=sys.stderr)
                self.tripped.set()
                return

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *exc):
        self._stop.set()
        self._thread.join(5)


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "cells":
        sys.exit("usage: python3 -m lanes.costguard cells <run-dir>")
    print(json.dumps(snapshot(sys.argv[2])[0], sort_keys=True))
