"""The probe phase: cheap funnel steps run as commands over a corpus of items (FORMATS.md, "Probe").

A cell is (item, rep, lane). The lane's command reads `{"input", "args"}` on stdin and writes
`{"output", "usage"}` on stdout; the harness measures it, grades the output against the item's hidden
`expected` and records the cell like any other (`result.json`, `evaluation.json`), so the cost guard,
`lanes-run` and `lanes-report` need no special cases beyond the hooks that call this module.
"""

import datetime
import json
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from fractions import Fraction

from . import common, costguard, experiment, noise, plan_hashes, report, usage

KILL_GRACE_S = 2.0
GRADER_DEADLINE_S = 60
TAIL_BYTES = 2000
COUNTERS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_tokens")
RESOURCES = ("wall_s", "cpu_s", "peak_rss_kb", "cost_usd")  # metrics every ok cell has besides the grader's
CORPUS_NOTE = "probe-corpus.json"  # in the run dir: where the corpus was when the run was planned (private)


class ProbeError(ValueError):
    """The probe cannot be planned, started or recorded (nothing is written)."""


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


# ---- corpus -----------------------------------------------------------------------------

def load_corpus(corpus, exp=None):
    """`{id: item}` from `<corpus>/items.jsonl`, in file order, only the experiment's `items` when it names some."""
    path = os.path.join(corpus, "items.jsonl")
    try:
        rows = common.read_jsonl(path)
    except OSError as e:
        raise ProbeError(f"{path}: {e.strerror or e}") from None
    except ValueError as e:
        raise ProbeError(f"{path}: not JSON lines ({e})") from None
    items = {}
    for i, row in enumerate(rows):
        where = f"{path} line {i + 1}"
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not re.fullmatch(experiment._NAME.pattern, row["id"]):
            raise ProbeError(f"{where}: needs a string id of letters, digits, '.', '_' or '-'")
        if not isinstance(row.get("input"), dict) or not isinstance(row.get("expected"), dict):
            raise ProbeError(f"{where}: input and expected must be objects")
        if row["id"] in items:
            raise ProbeError(f"{where}: duplicate item id {row['id']}")
        items[row["id"]] = row
    if exp is not None and exp.get("items"):
        missing = [i for i in exp["items"] if i not in items]
        if missing:
            raise ProbeError(f"items not in the corpus: {', '.join(missing)}")
        items = {i: items[i] for i in exp["items"]}
    if not items:
        raise ProbeError(f"{path}: no items")
    return items


def item_dir(corpus, item):
    """The folder an item's input refers to: `input.dir` or `input.repo` inside the corpus, else the corpus."""
    for key in ("dir", "repo"):
        rel = item["input"].get(key)
        if isinstance(rel, str) and rel and not os.path.isabs(rel) and ".." not in rel.replace("\\", "/").split("/"):
            path = os.path.join(corpus, rel)
            if os.path.isdir(path):
                return path
    return corpus


def corpus_hashes(corpus, items):
    return {"tree": common.sha256_tree(corpus), "items": {i: plan_hashes.sha256_json(r) for i, r in items.items()}}


def base_dir(run_dir):
    """The experiment's folder when the run was planned: command elements that name a file are relative to it."""
    note = os.path.join(run_dir, CORPUS_NOTE)
    return common.read_json(note).get("base") if os.path.isfile(note) else None


def resolve(argv, base):
    """`argv` with every element that names an existing file or folder relative to `base` made absolute (the
    command runs in a temp dir, so a bare `probe.py` next to the experiment would not be found there)."""
    out = []
    for a in argv:
        path = os.path.join(base, a) if base and not os.path.isabs(a) else None
        out.append(os.path.abspath(path) if path and os.path.exists(path) else a)
    return out


def _file_hashes(argv, base):
    """sha256 of each element of `argv` that resolves to a file or folder, by argv index (no path is written)."""
    return {str(i): common.sha256_tree(a) if os.path.isdir(a) else common.sha256_file(a)
            for i, a in enumerate(resolve(argv, base)) if os.path.isabs(a) and os.path.exists(a)}


def plan_lane_hashes(exp, exp_path, base):
    """The lane hashes of `plan_hashes`, plus each lane's probe object and command files, and the grader's."""
    lanes = plan_hashes.lane_hashes(exp, exp_path)
    for lane in exp["lanes"]:
        lanes[lane["name"]].update(probe=plan_hashes.sha256_json(lane["probe"]),
                                   files=_file_hashes(lane["probe"]["command"], base))
    grader = {"config": plan_hashes.sha256_json(exp["grader"]),
              "files": _file_hashes(exp["grader"].get("command", []), base)}
    return lanes, grader


def corpus_path(run_dir, explicit=None):
    """The corpus folder of a probe run: the flag, else the path `lanes-plan` recorded in the run dir."""
    if explicit:
        return os.path.abspath(os.path.expanduser(explicit))
    note = os.path.join(run_dir, CORPUS_NOTE)
    if os.path.isfile(note):
        return common.read_json(note)["path"]
    raise ProbeError("no corpus: pass --corpus or set KOGEN_LANES_CORPUS")


def is_probe(run_dir):
    try:
        return experiment.load(os.path.join(run_dir, "experiment.json"))["phase"] == "probe"
    except (OSError, ValueError):
        return False


# ---- plan and verify ----------------------------------------------------------------------

def plan(exp, exp_path, run_dir, explicit=None):
    """Write the run dir of a probe experiment: experiment.json, PLAN.json, plan.jsonl, the corpus note."""
    from . import dispatch  # plan order is shared with the other phases
    corpus = os.path.abspath(os.path.expanduser(explicit)) if explicit else os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(exp_path)), exp["corpus"]))
    items = load_corpus(corpus, exp)
    split = exp.get("split")
    if split and not (set(split["train"]) | set(split["test"])) <= set(items):
        raise ProbeError("split names items that are not in the corpus")
    if split and "items" not in exp and set(split["train"]) | set(split["test"]) != set(items):
        raise ProbeError("train and test together must be exactly the corpus items (or name `items`)")
    base = os.path.dirname(os.path.abspath(exp_path))
    lanes, grader = plan_lane_hashes(exp, exp_path, base)
    plan_doc = {"experiment": {k: v for k, v in exp.items() if k != "hosts"},
                "hashes": {"corpus": corpus_hashes(corpus, items), "lanes": lanes, "grader": grader}, "lock": None}
    os.makedirs(run_dir, exist_ok=True)
    shutil.copyfile(exp_path, os.path.join(run_dir, "experiment.json"))
    common.write_json(os.path.join(run_dir, CORPUS_NOTE), {"path": corpus, "base": base})
    common.write_json(os.path.join(run_dir, "PLAN.json"), plan_doc)
    with open(os.path.join(run_dir, "plan.jsonl"), "w", encoding="utf-8") as f:
        for c in dispatch.make_plan({**exp, "tasks": list(items)}):
            f.write(json.dumps(c, sort_keys=True) + "\n")


def verify_inputs(run_dir, exp, corpus):
    """Refuse to start when the corpus, an item, or a lane's command differs from the PLAN.json hashes."""
    path = os.path.join(run_dir, "PLAN.json")
    if not os.path.isfile(path):
        raise ProbeError("PLAN.json is missing: run lanes-plan first")
    plan_doc = common.read_json(path)
    if {k: v for k, v in exp.items() if k != "hosts"} != plan_doc["experiment"]:
        raise ProbeError("experiment.json no longer matches PLAN.json")
    got = corpus_hashes(corpus, load_corpus(corpus, exp))
    if got["items"] != plan_doc["hashes"]["corpus"]["items"]:
        raise ProbeError("corpus items no longer match PLAN.json")
    if got["tree"] != plan_doc["hashes"]["corpus"]["tree"]:
        raise ProbeError("corpus files no longer match PLAN.json")
    lanes, grader = plan_lane_hashes(exp, os.path.join(run_dir, "experiment.json"), base_dir(run_dir))
    if plan_doc["hashes"]["lanes"] != lanes or plan_doc["hashes"].get("grader") != grader:
        raise ProbeError("lane or grader commands, their files or settings no longer match PLAN.json")


# ---- running a command ---------------------------------------------------------------------

def _exit_code(status):
    code = os.waitstatus_to_exitcode(status)
    return code if code >= 0 else 128 - code


def spawn(argv, stdin_bytes, env, deadline_s, stdout_path, stderr_path):
    """Run `argv` in its own process group and a fresh temp cwd, under a deadline.

    Not `common.run`: the leader is reaped here with `wait4`, which is what yields its rusage.

    Returns `{exit_code, timed_out, wall_s, cpu_s, peak_rss_kb}`; exit 124 on the deadline, 127 when the
    command cannot start. The whole group is killed (TERM, then KILL) on the deadline or an interrupt, and
    stragglers of an exited leader are killed too, so nothing outlives the call. CPU seconds and peak RSS come
    from the leader's `wait4` rusage, which includes the descendants it waited for.
    """
    with tempfile.TemporaryDirectory(prefix="lanes-probe-") as tmp:
        stdin_path = os.path.join(tmp, "stdin.json")
        with open(stdin_path, "wb") as f:
            f.write(stdin_bytes)
        work = os.path.join(tmp, "cwd")
        os.makedirs(work)
        t0 = time.monotonic()
        with open(stdin_path, "rb") as si, open(stdout_path, "wb") as so, open(stderr_path, "wb") as se:
            try:
                proc = subprocess.Popen(argv, cwd=work, env=env, stdin=si, stdout=so, stderr=se, start_new_session=True)
            except OSError as e:
                se.write(f"cannot start {argv[0]}: {e.strerror or e}\n".encode())
                return {"exit_code": 127, "timed_out": False, "wall_s": 0.0, "cpu_s": 0.0, "peak_rss_kb": 0,
                        "exec_error": True}
            done, timed_out, killed_at = None, False, None
            try:
                while done is None:
                    pid, status, ru = os.wait4(proc.pid, os.WNOHANG)
                    if pid:
                        done = (status, ru)
                        break
                    if killed_at is None and time.monotonic() - t0 > deadline_s:
                        timed_out, killed_at = True, time.monotonic()
                        common._killpg(proc.pid, signal.SIGTERM)
                    elif killed_at is not None and time.monotonic() - killed_at > KILL_GRACE_S:
                        common._killpg(proc.pid, signal.SIGKILL)
                    time.sleep(0.02)
            except BaseException:
                common._killpg(proc.pid, signal.SIGKILL)
                os.wait4(proc.pid, 0)
                raise
            common._killpg(proc.pid, signal.SIGKILL)  # stragglers of an exited leader
        proc.returncode = os.waitstatus_to_exitcode(done[0])
        ru = done[1]
        rss = ru.ru_maxrss // 1024 if sys.platform == "darwin" else ru.ru_maxrss  # bytes on macOS, KiB on Linux
        return {"exit_code": 124 if timed_out else _exit_code(done[0]), "timed_out": timed_out,
                "wall_s": round(time.monotonic() - t0, 4), "cpu_s": round(ru.ru_utime + ru.ru_stime, 4),
                "peak_rss_kb": int(rss)}


def _tail(path):
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            f.seek(max(0, f.tell() - TAIL_BYTES))
            return f.read().decode(errors="replace")
    except OSError:
        return ""


def parse_reply(path):
    """`(output, usage rows)` from a probe command's stdout; ProbeError names what is wrong."""
    try:
        with open(path, encoding="utf-8") as f:
            reply = json.load(f)
    except (OSError, ValueError) as e:
        raise ProbeError(f"stdout is not JSON ({e})") from None
    if not isinstance(reply, dict) or not isinstance(reply.get("output"), dict):
        raise ProbeError('stdout must be a JSON object with an "output" object')
    rows = reply.get("usage", [])
    if not isinstance(rows, list):
        raise ProbeError('"usage" must be a list')
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ProbeError(f"usage[{i}] must be an object")
        for key in ("model", "provider"):
            if row.get(key) is not None and not isinstance(row[key], str):
                raise ProbeError(f"usage[{i}].{key} must be a string or null")
        for key in COUNTERS:
            v = row.get(key)
            if v is not None and (isinstance(v, bool) or not isinstance(v, int) or v < 0):
                raise ProbeError(f"usage[{i}].{key} must be a non-negative integer or null")
        if None not in (row.get("input_tokens"), row.get("cached_input_tokens")) \
                and row["cached_input_tokens"] > row["input_tokens"]:
            raise ProbeError(f"usage[{i}]: cached_input_tokens is more than input_tokens")
    return reply["output"], rows


def usage_cost(rows):
    """USD of a probe's usage rows, priced as the cost guard prices requests (unpriced models and unknown
    counters at its fallbacks). Zero rows cost nothing: a probe may run no model."""
    calc, table, rates = costguard.pricing()
    total = 0.0
    for row in rows:
        tokens = {k: row.get(k) for k in COUNTERS}
        if None in (tokens["input_tokens"], tokens["cached_input_tokens"], tokens["output_tokens"]):
            total += costguard._at_top(costguard.FALLBACK_TOKENS, rates)
            continue
        cost, _ = usage.request_cost(row.get("model"), tokens, table, calc)
        total += cost if cost is not None else costguard._at_top(tokens, rates)
    return total


def totals(rows, wall_s, cost):
    sums = {k: (None if any(r.get(k) is None for r in rows) else sum(r[k] for r in rows)) for k in COUNTERS}
    return {"requests": len(rows), **sums, "wall_s": wall_s, "cost_usd": round(cost, 8)}


def _provider(name):
    return experiment.CHATGPT if name in ("openai", experiment.CHATGPT) else name


def command_env(corpus, item):
    return dict(os.environ, LANES_CORPUS=corpus, LANES_PROBE_ITEM_DIR=item_dir(corpus, item))


def execute(exp, lane, item, corpus, out, base=None):
    """Run one probe command on one item into the folder `out`, grade it; return the cell's measurements.

    Writes `stdout.raw`, `stderr.txt` and, when the reply is valid, `output.json` and `evaluation.json`
    there. The command never sees `expected`."""
    os.makedirs(out, exist_ok=True)
    payload = json.dumps({"input": item["input"], "args": lane["probe"].get("args", {})}).encode()
    stdout, stderr = os.path.join(out, "stdout.raw"), os.path.join(out, "stderr.txt")
    started = now()
    res = spawn(resolve(lane["probe"]["command"], base), payload, command_env(corpus, item), exp["deadline_s"], stdout, stderr)
    res.update(started=started, ended=now(), usage=[], stderr_tail=_tail(stderr), detail=None)
    if res["timed_out"]:
        res["outcome"] = "timeout"
    elif res.get("exec_error"):
        res["outcome"] = "exec_error"
    elif res["exit_code"]:
        res["outcome"] = f"exit_{res['exit_code']}"
    else:
        try:
            output, rows = parse_reply(stdout)
            res["usage"] = rows
            wrong = {r["provider"] for r in rows if r.get("provider") and _provider(r["provider"]) != experiment.lane_provider(lane)}
            if wrong:  # the lane's `settings.models` decide whose cap a probe's spend counts against
                raise ProbeError(f"usage names provider {', '.join(sorted(wrong))} but the lane's spend counts against "
                                 f"{experiment.lane_provider(lane)}: declare it in the lane's settings.models")
            common.write_json(os.path.join(out, "output.json"), output)
            grader = exp["grader"]
            if grader["kind"] == "command":
                grader = {**grader, "command": resolve(grader["command"], base)}
            metrics = grade(grader, item, output, lane)
            common.write_json(os.path.join(out, "evaluation.json"), {
                "grader": grader["kind"], "metrics": metrics, "undefined": undefined_sets(grader, item)})
            res["outcome"] = "ok"
        except ProbeError as e:
            res["outcome"], res["detail"] = ("grader_error" if os.path.isfile(os.path.join(out, "output.json"))
                                             else "bad_output"), str(e)
    return res


def run_cell(run_dir, cell, corpus, host="local", force=False):
    """Run one probe cell and write its cell dir; returns `result.json` as a dict. `result.json` is written last."""
    item_id, rep, lane_name = cell.split("/")
    exp = experiment.load(os.path.join(run_dir, "experiment.json"))
    lane = next((l for l in exp["lanes"] if l["name"] == lane_name), None)
    items = load_corpus(corpus, exp)
    if lane is None or item_id not in items or not re.fullmatch(r"r\d+", rep):
        raise ProbeError(f"unknown cell {cell}: lane, rep or item not found")
    plan_path = os.path.join(run_dir, "PLAN.json")
    if os.path.isfile(plan_path):
        want = common.read_json(plan_path)["hashes"]["corpus"]["items"].get(item_id)
        if want != plan_hashes.sha256_json(items[item_id]):
            raise ProbeError(f"item {item_id} no longer matches PLAN.json")
    out = common.cell_dir(run_dir, cell)
    try:
        costguard.check_start(run_dir, exp, cell)
    except costguard.CostCapError as e:
        raise ProbeError(str(e)) from None
    if os.path.exists(os.path.join(out, "result.json")) and not force:
        raise ProbeError(f"{cell} is already done (result.json exists); use --force to rerun")
    try:
        costguard.retire(run_dir, cell, out)
    except Exception as e:
        raise ProbeError(f"cannot keep the spend of the earlier attempt of {cell} ({e}); not starting") from None
    os.makedirs(out)
    res = execute(exp, lane, items[item_id], corpus, out, base_dir(run_dir))
    cost = usage_cost(res["usage"])
    result = {"cell": cell, "lane": lane_name, "phase": "probe", "exit_code": res["exit_code"],
              "outcome": res["outcome"], "detail": res["detail"], "started": res["started"], "ended": res["ended"],
              "wall_s": res["wall_s"], "cpu_s": res["cpu_s"], "peak_rss_kb": res["peak_rss_kb"], "host": host,
              "stderr_tail": res["stderr_tail"], "usage": res["usage"], "stages": [],
              "totals": totals(res["usage"], res["wall_s"], cost)}
    common.write_json(os.path.join(out, "result.json"), result)
    return result


# ---- graders -------------------------------------------------------------------------------

def _eq(a, b):
    """JSON equality: a boolean is not a number; 1 and 1.0 are the same number."""
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_eq(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_eq(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    return type(a) is type(b) and a == b


def _number(v):
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v)


def _prf(hit_expected, n_expected, hit_claims, n_claims):
    recall = hit_expected / n_expected
    precision = hit_claims / n_claims if n_claims else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"recall": recall, "precision": precision, "f1": f1}


def _overlap(claim, sym):
    return (claim.get("path") == sym["path"] and isinstance(claim.get("start"), int) and isinstance(claim.get("end"), int)
            and claim["start"] <= sym["end"] and sym["start"] <= claim["end"])


def _set_names(config, item):
    return config.get("sets") or [k for k, v in item["expected"].items() if isinstance(v, list)]


def undefined_sets(config, item):
    """`{set: reason}` for the expected sets a grader scores that this item has none of: an absent or empty set
    gives no metric (it is normal, e.g. `read_files` exists only for real runs), not a failure."""
    if config["kind"] != "set_recall_precision_at_budget":
        return {}
    out = {}
    for name in _set_names(config, item):
        want = item["expected"].get(name)
        if want is None:
            out[name] = "expected set absent"
        elif isinstance(want, list) and not want:
            out[name] = "expected set empty"
    return out


def grade_sets(config, item, output, lane):
    """`set_recall_precision_at_budget`: the ranked list cut at the token budget, scored per expected set."""
    ranked = output.get("ranked")
    if not isinstance(ranked, list) or not all(
            isinstance(r, dict) and isinstance(r.get("path"), str) and _number(r.get("tokens")) and r["tokens"] >= 0
            for r in ranked):
        raise ProbeError('output.ranked must be a list of {"path", "tokens", ...} objects')
    budget = (lane["probe"].get("args") or {}).get("token_budget", item["input"].get("token_budget"))
    if budget is not None and (not _number(budget) or budget < 0):
        raise ProbeError("token_budget must be a non-negative number")
    kept, used = [], 0
    for r in ranked:  # the longest prefix that fits
        if budget is not None and used + r["tokens"] > budget:
            break
        kept.append(r)
        used += r["tokens"]
    metrics = {"tokens_used": used, "items_kept": len(kept)}
    claimed = {r["path"] for r in kept}
    for name in _set_names(config, item):
        want = item["expected"].get(name)
        if want is None:
            continue
        if not isinstance(want, list):
            raise ProbeError(f"expected.{name} is not a list")
        syms = [e for e in want if isinstance(e, dict)]
        if not all(isinstance(e, str) or (isinstance(e, dict) and isinstance(e.get("path"), str)) for e in want):
            raise ProbeError(f"expected.{name} must hold paths or objects with a path")
        paths = {e["path"] if isinstance(e, dict) else e for e in want}
        if not paths:
            continue
        for key, v in _prf(len(paths & claimed), len(paths), len(paths & claimed), len(claimed)).items():
            metrics[f"{name}.file.{key}"] = v
        if syms and all(isinstance(e.get("start"), int) and isinstance(e.get("end"), int) for e in syms):
            claims = [r for r in kept if isinstance(r.get("start"), int) and isinstance(r.get("end"), int)]
            hit_syms = sum(1 for e in syms if any(_overlap(r, e) for r in claims))
            hit_claims = sum(1 for r in claims if any(_overlap(r, e) for e in syms))
            for key, v in _prf(hit_syms, len(syms), hit_claims, len(claims)).items():
                metrics[f"{name}.symbol.{key}"] = v
    return metrics


def grade_exact(config, item, output):
    keys = config.get("keys")
    got, want = (output, item["expected"]) if not keys else (
        {k: output.get(k) for k in keys}, {k: item["expected"].get(k) for k in keys})
    return {"exact": 1.0 if _eq(got, want) else 0.0}


def grade_command(config, item, output):
    """The grader command gets `{item, output}` on stdin and prints a JSON object of numeric metrics."""
    with tempfile.TemporaryDirectory(prefix="lanes-grade-") as tmp:
        out, err = os.path.join(tmp, "out"), os.path.join(tmp, "err")
        res = spawn(config["command"], json.dumps({"item": item, "output": output}).encode(), dict(os.environ),
                    config.get("deadline_s", GRADER_DEADLINE_S), out, err)
        if res["exit_code"]:
            why = "timed out" if res["timed_out"] else f"exit {res['exit_code']}"
            raise ProbeError(f"grader command failed ({why}): {_tail(err)[-200:].strip()}")
        try:
            with open(out, encoding="utf-8") as f:
                metrics = json.load(f)
        except ValueError:
            raise ProbeError("grader output is not JSON") from None
    if not isinstance(metrics, dict) or not metrics or not all(_number(v) for v in metrics.values()):
        raise ProbeError("grader output must be a JSON object of numbers")
    return metrics


def grade(config, item, output, lane):
    """The metrics `{name: number}` of one output; ProbeError when the output cannot be graded."""
    kind = config["kind"]
    if kind == "set_recall_precision_at_budget":
        return grade_sets(config, item, output, lane)
    if kind == "exact_match":
        return grade_exact(config, item, output)
    return grade_command(config, item, output)


# ---- pre-flight ----------------------------------------------------------------------------

def preflight(run_dir, corpus, out=print):
    """Refusals before any cell: corpus readable, commands executable, files present, and a dry run of
    the first item for each lane that declares `"dry_run_ok": true` (the only lanes that may run with no model)."""
    exp = experiment.load(os.path.join(run_dir, "experiment.json"))
    bad = 0
    try:
        items = load_corpus(corpus, exp)
    except ProbeError as e:
        out(f"corpus: REFUSED: {e}")
        return 1
    out(f"corpus: ok: {len(items)} item(s)")
    commands = [(l["name"], l["probe"]["command"]) for l in exp["lanes"]]
    if exp["grader"]["kind"] == "command":
        commands.append(("grader", exp["grader"]["command"]))
    base = base_dir(run_dir)
    for name, argv in commands:
        found = resolve(argv, base)  # what will run: files next to the experiment are made absolute
        problems = [] if shutil.which(found[0]) else [f"{argv[0]} is not an executable (or not found)"]
        problems += [f"{a} does not exist" for a, f in zip(argv[1:], found[1:])
                     if f == a and (os.path.isabs(a) or a.startswith(("./", "../"))) and not os.path.exists(a)]
        bad += bool(problems)
        out(f"{name}: {'REFUSED: ' + '; '.join(problems) if problems else 'ok: command found'}")
    first = next(iter(items.values()))
    for lane in exp["lanes"]:
        if lane.get("dry_run_ok") is not True:
            continue
        with tempfile.TemporaryDirectory(prefix="lanes-dry-") as tmp:
            res = execute(exp, lane, first, corpus, tmp, base)
        ok = res["outcome"] == "ok"
        bad += not ok
        out(f"{lane['name']}: dry run on {first['id']}: {'ok' if ok else 'REFUSED: ' + res['outcome'] + ' ' + (res['detail'] or res['stderr_tail'].strip()[-200:])}")
    return bad


# ---- report --------------------------------------------------------------------------------

def _load(run_dir, exp):
    """One entry per planned cell: its plan line, result, metrics (grader metrics plus RESOURCES, ok cells only)
    and the grader's `undefined` sets."""
    cells = []
    for p in common.read_jsonl(os.path.join(run_dir, "plan.jsonl")):
        d = common.cell_dir(run_dir, p["cell"])
        read = lambda name: common.read_json(os.path.join(d, name)) if os.path.isfile(os.path.join(d, name)) else None
        result, ev = read("result.json"), read("evaluation.json")
        metrics = None
        if result and result.get("outcome") == "ok" and ev:
            metrics = {**ev["metrics"], "wall_s": result["wall_s"], "cpu_s": result["cpu_s"],
                       "peak_rss_kb": result["peak_rss_kb"], "cost_usd": result["totals"]["cost_usd"]}
        # "*": why a set-based metric is missing from an ok cell that does not list its set: the item has no such set
        gone = {"*": "expected set absent"} if exp["grader"]["kind"] == "set_recall_precision_at_budget" else {}
        cells.append({"plan": p, "result": result, "metrics": metrics, "undefined": {**gone, **(ev or {}).get("undefined", {})}})
    return cells


def _mean(values):
    return math.fsum(values) / len(values)


def _interval(values):
    """Student t 95% interval of the mean of per-item means (the item is the unit); None below two items."""
    n = len(values)
    if n < 2:
        return None
    m = _mean(values)
    sd = math.sqrt(math.fsum((v - m) ** 2 for v in values) / (n - 1))
    half = noise.t95(n - 1) * sd / math.sqrt(n)
    return [round(m - half, 6), round(m + half, 6)]


def item_means(cells, lane):
    """`{metric: {item: mean over the item's ok reps}}` of one lane."""
    per = {}
    for c in cells:
        if c["plan"]["lane"] == lane and c["metrics"]:
            for k, v in c["metrics"].items():
                per.setdefault(k, {}).setdefault(c["plan"]["task"], []).append(v)
    return {k: {i: _mean(v) for i, v in items.items()} for k, items in per.items()}


def _ok_items(cells, lane):
    """`{item: undefined sets}` of the items with an ok cell on `lane`."""
    return {c["plan"]["task"]: c["undefined"] for c in cells if c["plan"]["lane"] == lane and c["metrics"]}


def _why(undefined, metric):
    return undefined.get(metric.split(".")[0], undefined.get("*", "not reported by the grader"))


def _left_out(cells, lane, metric, means, ids):
    """`{item: reason}` for the items `means` (one lane's item means of `metric`) does not cover."""
    ok = _ok_items(cells, lane)
    return {i: "no ok cell" if i not in ok else _why(ok[i], metric) for i in ids if i not in means}


def _count(reasons):
    out = {}
    for r in reasons.values():
        out[r] = out.get(r, 0) + 1
    return dict(sorted(out.items()))


def _lane_report(lane, cells, ids):
    mine = [c for c in cells if c["plan"]["lane"] == lane["name"]]
    means = item_means(cells, lane["name"])
    metrics = {}
    for k, v in sorted(means.items()):  # items covered, and the others left out with the reason
        left = _left_out(cells, lane["name"], k, v, ids)
        metrics[k] = {"mean": _mean(list(v.values())), "ci": _interval(list(v.values())), "items": len(v),
                      "left_out": {"count": len(left), "reasons": _count(left)}}
    return {"name": lane["name"], "cells": {"planned": len(mine), "finished": sum(1 for c in mine if c["result"]),
                                            "ok": sum(1 for c in mine if c["metrics"])},
            "outcomes": _count({c["plan"]["cell"]: c["result"]["outcome"] if c["result"] else "not_run" for c in mine}),
            "items": len(ids), "metrics": metrics}


def _pairs(rule, cells, metric, means, ids):
    """`(diffs, ungraded, left_out)` over `ids`: `diffs` is `{item: signed candidate - baseline}` as exact
    fractions. An item with no ok cell on a lane is `ungraded`; one with ok cells on both whose metric is
    undefined on a lane (an empty or absent expected set) is `left_out` with the reason, not a missing cell."""
    sign = -1 if rule.get("better") == "lower" else 1
    lanes = (rule["baseline"], rule["candidate"])
    ok = [_ok_items(cells, n) for n in lanes]
    ungraded = [i for i in ids if not all(i in o for o in ok)]
    base, cand = (means[n] for n in lanes)
    diffs = {i: sign * (report.ratio(cand[i]) - report.ratio(base[i])) for i in ids if i in base and i in cand}
    left = {i: _why(next(o[i] for n, o in zip(lanes, ok) if i not in means[n]), metric)
            for i in ids if i not in ungraded and i not in diffs}
    return diffs, ungraded, left


def _sign_counts(diffs):
    wins, losses = sum(1 for d in diffs.values() if d > 0), sum(1 for d in diffs.values() if d < 0)
    return wins, losses, report.binomial_tail(wins, wins + losses), report.binomial_tail(losses, wins + losses)


def _num(v):
    return report.ratio_decimal(v) if isinstance(v, Fraction) else v


def _left_text(left):
    return f"; {len(left)} item(s) left out, metric undefined ({', '.join(f'{r}: {n}' for r, n in _count(left).items())})" if left else ""


def verdict(exp, cells, lanes, ids):
    rule = exp["decision_rule"]
    kind = rule["kind"]
    out = lambda decision, line, **kw: {"kind": kind, "decision": decision, "line": f"Rule {kind}: {line}", **kw}
    if kind == "descriptive":
        return out("none", "no decision, results only")
    metric = rule["metric"]
    means = {l["name"]: item_means(cells, l["name"]) for l in lanes}
    if not any(metric in means[n] for n in (rule["baseline"], rule["candidate"])):
        return out("invalid_rule", f"no cell has the metric {metric}")
    means = {n: m.get(metric, {}) for n, m in means.items()}
    what = f"candidate {rule['candidate']} vs baseline {rule['baseline']} on {metric}" \
           + (" (lower is better)" if rule.get("better") == "lower" else "")
    incomplete = lambda ungraded, left, **kw: out(
        "incomplete", f"{what}: {len(ungraded)} item(s) have no ok cell on a lane: {', '.join(ungraded)}"
        + _left_text(left), ungraded=ungraded, left_out=left, **kw)
    if kind == "task_sign":
        diffs, ungraded, left = _pairs(rule, cells, metric, means, ids)
        if ungraded:
            return incomplete(ungraded, left)
        if not diffs:
            return out("incomplete", f"{what}: no item has the metric defined on both lanes" + _left_text(left), left_out=left)
        wins, losses, p, p_rev = _sign_counts(diffs)
        gain = sum(diffs.values()) / len(diffs)
        sign = report._sign(wins, losses, gain * 100, report.ratio(rule.get("min_gain", 0)) * 100, rule.get("max_p", 1))
        decision = "unresolved" if wins + losses == 0 else sign["decision"]
        return out(decision, f"{what}: {decision.upper()}: mean difference {float(gain):+.4f} over {len(diffs)} items, "
                   f"candidate-better {wins}, baseline-better {losses}, ties {len(diffs) - wins - losses}, "
                   f"sign test p {sign['p']} (min_gain {rule.get('min_gain', 0)}, max_p {rule.get('max_p', 1)})"
                   + _left_text(left), gain=_num(gain), candidate_better=wins, baseline_better=losses, p=sign["p"],
                   p_reverse=sign["p_reverse"], left_out=left)
    splits, ungraded, left, width = {}, [], {}, rule.get("range", 1)
    for part in ("train", "test"):
        diffs, missing, gone = _pairs(rule, cells, metric, means, exp["split"][part])
        ungraded += missing
        left.update(gone)
        wins, losses, _, _ = _sign_counts(diffs)
        mean = sum(diffs.values()) / len(diffs) if diffs else Fraction(0)
        splits[part] = {"tasks": len(diffs), "difference_exact": report.ratio_decimal(mean), "difference": float(mean),
                        "difference_ci": report.hoeffding(mean, len(diffs), low=-width, high=width),
                        "candidate_better": wins, "baseline_better": losses}
    if ungraded:
        return incomplete(ungraded, left, splits=splits)
    if any(s["tasks"] == 0 for s in splits.values()):
        return out("incomplete", f"{what}: a split has no item with the metric defined on both lanes" + _left_text(left),
                   left_out=left, splits=splits)
    improves = rule.get("improves")
    r = report.keep_revert(splits, rule.get("min_effect", 0), improves)
    nums = "; ".join(f"{n} {s['difference']:+.4f} ({s['tasks']} items, candidate-better {s['candidate_better']}, "
                     f"baseline-better {s['baseline_better']}"
                     + ("" if improves else f", Hoeffding 95% [{s['difference_ci'][0]:.4f}, {s['difference_ci'][1]:.4f}]") + ")"
                     for n, s in splits.items())
    test = f"exact sign test over items, max_p {improves['max_p']}" if improves else f"Hoeffding 95% over items, range {width}"
    return out(r["decision"], f"{what}: {r['decision'].upper()} [{r['case']}]: {nums} (min_effect {rule.get('min_effect', 0)}; {test})"
               + _left_text(left), case=r["case"], splits=splits, left_out=left)


def report_probe(run_dir, exp):
    """`report.json` content of a probe run: per lane and metric the mean over items, the cost, the verdict."""
    cells = _load(run_dir, exp)
    ids = list(dict.fromkeys(c["plan"]["task"] for c in cells))
    lanes = [_lane_report(l, cells, ids) for l in exp["lanes"]]
    return {"experiment": exp["id"], "phase": "probe", "decision_rule": exp["decision_rule"], "grader": exp["grader"],
            "items": len(ids), "reps": exp["reps"], "lanes": lanes, "cost": report.cost_section(run_dir, exp, cells),
            "verdict": verdict(exp, cells, lanes, ids)}


def _left_cell(left):
    return "0" if not left["count"] else f"{left['count']} ({', '.join(f'{r}: {n}' for r, n in left['reasons'].items())})"


def render(rep):
    out = [f"# Report: {rep['experiment']} (probe)", "", f"**Verdict:** {rep['verdict']['line']}", "",
           f"{rep['items']} items, {rep['reps']} rep(s) per lane. A metric is the mean over items of each item's mean "
           "over its ok reps; the interval is Student t 95% with the item as the unit (n/a below two items). Only ok "
           "cells count; the others are listed as outcomes. Expected symbols marked `new` are scored like the rest. A metric is undefined for an item whose expected set "
           "is absent or empty; that item is left out of the metric's statistics and rules, with the reason.", "",
           "## Lanes", ""]
    out += report._table(["lane", "cells planned/finished/ok", "outcomes"],
                         [[l["name"], "/".join(str(v) for v in l["cells"].values()),
                           ", ".join(f"{k} {v}" for k, v in l["outcomes"].items()) or "none"] for l in rep["lanes"]])
    names = sorted({k for l in rep["lanes"] for k in l["metrics"]},
                   key=lambda k: (k in RESOURCES, k))  # grader metrics first, then time, CPU, memory and cost
    for name in names:
        out += ["", f"### {name}", ""]
        out += report._table(["lane", "mean", "95% interval (items)", "items covered", "items left out"],
                             [[l["name"], f"{l['metrics'][name]['mean']:.4f}", report._ci_text(l["metrics"][name]["ci"]),
                               l["metrics"][name]["items"], _left_cell(l["metrics"][name]["left_out"])]
                              for l in rep["lanes"] if name in l["metrics"]])
    out += report._render_cost(rep["cost"])
    return "\n".join(out) + "\n"
