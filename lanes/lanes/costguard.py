"""Cost guard: the spend estimate of a run dir and its soft and hard caps (FORMATS.md, "Cost cap").

Spend = finished cells' `totals.cost_usd` + the live spend of running cells, read from their Kogen run
logs and shaping events as requests complete + the ledger of earlier attempts that were thrown away.
A request that cannot be priced counts at a conservative fallback:

- a model with no price row, or a price cost_calc cannot give: the request's tokens at the highest
  input, cached-input and output rate in `reproduce/price-table-v1.json`;
- a request with unknown usage (null counters, or a build request whose four counters are all 0, which
  Kogen logs for unknown): `FALLBACK_TOKENS`, an allowance above the largest request seen in real logs
  (53,940 uncached input tokens), at those rates. It is an allowance, not a proven bound.

The guard fails closed on real errors: unreadable or unparsable usage, no price table, a crash of the guard
(see `Watcher`, `check_start`). A source that is gone because its attempt finished or was retired is not an
error: the steps that move spend from one record to the next (live workspace -> result.json or spent.json,
cell dir -> ledger) hold the run dir's lock (`locked`), and readers take it too, so each attempt is counted
exactly once. A source gone with no final record is retried for `RETRY_S` seconds, then the guard fails closed.
`python3 -m lanes.costguard cells <run-dir>` prints `{cell: usd}` (the controller polls it on remote hosts).
"""

import contextlib
import fcntl
import glob
import json
import os
import shutil
import sys
import threading
import time

from . import common, usage

HARD_FACTOR = 1.25  # hard cap = HARD_FACTOR * cost_cap_usd
FALLBACK_TOKENS = {"input_tokens": 100_000, "cached_input_tokens": 0, "output_tokens": 20_000}
LIVE = "live.json"    # in a running cell's dir: where its workspace is
SPENT = "spent.json"  # in a cell dir that stopped without result.json: what it had spent
LEDGER = "cost-ledger.jsonl"  # in the run dir: spend of attempts whose cell dir was thrown away
STOP = "cost-stop.json"       # in the run dir: which cap stopped the run
LOCK = ".cost.lock"           # in the run dir: the spend lock
RETRY_S = 5.0  # how long a source that is gone without a final record is retried before failing closed
_pricing = None


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


def _retrying(run_dir, fn, exclusive=False, retry_s=None):
    """`fn()` under the lock; a source gone without a final record is retried (lock released), then fails closed."""
    end = time.monotonic() + (RETRY_S if retry_s is None else retry_s)
    while True:
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
        rows = list(table["models"].values())
        _pricing = calc, table, {k: max(float(r[k]) for r in rows) for k in ("input", "cached_input", "output")}
    return _pricing


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
        total += cost if cost is not None else _at_top(tokens, rates)
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
        cost = (common.read_json(path).get("totals") or {}).get("cost_usd")
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
    return _retrying(run_dir, read, retry_s=retry_s)


def _append(run_dir, cell, usd):
    with open(os.path.join(run_dir, LEDGER), "a", encoding="utf-8") as f:
        f.write(json.dumps({"cell": cell, "usd": usd}, sort_keys=True) + "\n")


def ledger_add(run_dir, cell, usd):
    with locked(run_dir):
        _append(run_dir, cell, usd)


def retire(run_dir, cell, out, retry_s=None):
    """Throw away an old attempt's cell dir, keeping what it spent in the ledger (one locked step)."""
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


def record_stop(run_dir, cap, spent):
    """Note which cap stopped the run; a hard stop overrides a soft one, never the reverse."""
    path = os.path.join(run_dir, STOP)
    if cap == "hard" or not os.path.exists(path):
        common.write_json(path, {"cap": cap, "spent_usd": round(spent, 8),
                                 "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})


def clear_stop(run_dir):
    """A new `lanes-run` starts without the stop note of the last one."""
    if os.path.exists(os.path.join(run_dir, STOP)):
        os.remove(os.path.join(run_dir, STOP))


def check_start(run_dir, exp):
    """Refuse to start a cell once the soft cap is reached, or when spend cannot be read."""
    soft, _ = caps(exp)
    try:
        pricing()  # no price table, no guard: refuse rather than run uncapped
        spent = estimate(run_dir)
    except Exception as e:
        raise CostCapError(f"cannot read the run's spend ({e}); the cost guard fails closed") from None
    if spent >= soft:
        record_stop(run_dir, "soft", spent)
        raise CostCapError(f"cost cap reached: spend ${spent:.4f} of the ${soft:g} cap; no new cell starts")


class Watcher:
    """Thread that sets `tripped` once the run dir's estimate reaches the hard cap, or cannot be read."""

    def __init__(self, run_dir, exp, interval_s=None):
        self.run_dir, self.hard = run_dir, caps(exp)[1]
        self.interval = float(os.environ.get("LANES_COST_WATCH_S", 0.5)) if interval_s is None else interval_s
        self.tripped, self.error, self.spent = threading.Event(), None, None
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def _loop(self):
        while not self._stop.wait(self.interval):
            try:
                self.spent = estimate(self.run_dir)
                if self.spent >= self.hard:
                    record_stop(self.run_dir, "hard", self.spent)
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
