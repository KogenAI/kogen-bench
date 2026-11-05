#!/usr/bin/env python3
"""Matched Claude Code benchmark: direct vs packet-assisted (plus optional 'bounded' arm).

    python3 build_bench.py --cases gin,axios --context ./kogen-context \
        --context-sha256 <hex> --out runs/new-dir [--bounded] [--preflight]

Primary comparison = two arms, `direct` and `assisted`, matched on issue, bounded initial
failure log, model, effort, tools and timeouts. `assisted` additionally gets the packet from
`<context> evidence --repo CHECKOUT --brief FILE --failure LOG --deadline 1s --bytes 6500
--ranges 6`. Optional third arm `bounded` (exploratory, --bounded): the model gets the same
packet and issue but NO tools and answers with JSON exact replacements; they are checked for
scope and unique anchors, applied, verified by qualify.py, and on failure the normal assisted
run is performed as a fallback (everything timed).

Grading is delegated to `qualify.py CASE (base|ref|PATH) --out DIR`, expected to exit 0 for
green, 1 for red and anything else for "could not run" (a fixture error, never a model
regression). Receipts (see --red/--green, default controls/CASE/{red,green}) must each hold a
summary and a sanitized failure; filenames are configurable (--summary-name, --diag-name).

This script never launches a model with --preflight, never touches git, installs nothing and
never edits qualify.py or README.md.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse, hashlib, json, os, platform, re, shutil, signal, subprocess, sys, tempfile, threading, time

ROOT = Path(__file__).resolve().parent
CLAUDE_VERSION = "2.1.318"
MODEL = "claude-sonnet-5-5"
EFFORT = "medium"
CLAUDE_TIMEOUT = 300          # hard cap per Claude attempt
RESULT_GRACE = 10             # s a process may outlive its complete result event (same for every arm)
CONTEXT_TIMEOUT = 15         # wall bound for the evidence child (its own --deadline is 1s)
EVIDENCE_ARGS = ["--deadline", "1s", "--bytes", "6500", "--ranges", "6"]
MAX_EDITS = 8

# Same allow-list for every arm/case: shell rg/find plus locally runnable test commands.
ALLOWED = ["Bash(rg *)", "Bash(find *)", "Bash(go test *)", "Bash(node *)", "Bash(npm test)",
           "Bash(npm test *)", "Bash(npm run test*)", "Bash(npx mocha *)", "Bash(mocha *)",
           "Bash(cargo test*)", "Bash(cargo check*)", "Bash(cargo build*)", "Bash(zig test *)",
           "Bash(zig build*)"]
DENIED = ["Bash(find * -exec *)", "Bash(find * -execdir *)", "Bash(find * -delete*)", "Bash(find * -ok *)"]
STRIP_ENV = ["CLAUDECODE", "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL",
             "ANTHROPIC_MODEL", "CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX",
             "CLAUDE_CODE_USE_FOUNDRY", "CLAUDE_CODE_OAUTH_TOKEN"]
OFFLINE_ENV = {"GOPROXY": "off", "GOTOOLCHAIN": "local", "GOFLAGS": "-mod=mod", "CARGO_NET_OFFLINE": "true",
               "npm_config_offline": "true", "npm_config_audit": "false", "npm_config_fund": "false",
               "npm_config_update_notifier": "false"}

PROMPT = """Implement this issue in the exact pre-fix {case} snapshot. Work only inside this checkout.
Rules: no network, no commits, no Git history, no remote or external solutions. You may run
existing tests only (locally runnable go test, node/npm/mocha, cargo or zig commands); do not
add test files. Preserve the repository's behavior and report the checks you ran.

ISSUE:
{issue}

The initial failing test output (sanitized, bounded) follows.
--- failure ---
{failure}
--- end failure ---
"""
FOLLOWUP = """

FOLLOW-UP (the only one): your earlier attempt is still in the workspace, but an independent
check still fails. Sanitized, bounded output of that check:
--- failure ---
{failure}
--- end failure ---
Fix the remaining behavior problem. Same rules as before.
"""
PACKET_INTRO = "\nOptional source evidence packet from the local retrieval tool follows as complete JSON. Verify it as needed.\n\n"
BOUNDED_PROMPT = """You cannot read files or run commands. Using only the issue, failing output and
evidence packet below, reply with ONLY a JSON object of this shape:
{{"edits": [{{"path": "relative/file", "original": "exact text shown in the packet, unique in the file",
"replacement": "new text"}}]}}
At most {n} edits. Each `original` must be copied exactly from source shown in the packet and
occur exactly once in its file. No prose, no code fences.

ISSUE:
{issue}

--- failure ---
{failure}
--- end failure ---
{intro}{packet}"""


# ------------------------------------------------------------------ helpers ----

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def now():
    return time.monotonic()


def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, default=str) + "\n")


def run_child(cmd, timeout, cwd=None, env=None, stdin_text=None, stdout_path=None, stderr_path=None):
    """Run a bounded child in its own process group; always return, never raise on timeout."""
    out = open(stdout_path, "wb") if stdout_path else subprocess.DEVNULL
    err = open(stderr_path, "wb") if stderr_path else subprocess.DEVNULL
    start, timed_out, rc = now(), False, None
    try:
        p = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.PIPE if stdin_text is not None else subprocess.DEVNULL,
                             stdout=out, stderr=err, start_new_session=True)
        try:
            p.communicate(input=stdin_text.encode() if stdin_text is not None else None, timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            try:
                p.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                pass
        rc = p.returncode
    except OSError as exc:
        rc = f"OSError: {exc}"
    finally:
        for f in (out, err):
            if hasattr(f, "close"):
                f.close()
    return {"rc": rc, "timed_out": timed_out, "secs": round(now() - start, 3)}


def kill_group(p, term_wait=5):
    """SIGTERM the process group, escalate to SIGKILL; return seconds until the leader was reaped."""
    t = now()
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(p.pid, sig)
        except ProcessLookupError:
            pass
        try:
            p.wait(timeout=term_wait if sig == signal.SIGTERM else 10)
            break
        except subprocess.TimeoutExpired:
            continue
    try:  # sweep stragglers left in the group after the leader exited
        os.killpg(p.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass
    return round(now() - t, 3)


def run_stream_child(cmd, timeout, grace, cwd, env, stdin_text, stdout_path, stderr_path):
    """Like run_child, but for `claude --output-format stream-json`.

    A result event counts only when it is a complete newline-terminated JSON line of type=result.
    If the process is still alive `grace` seconds after that, its process group is terminated and
    the event is the completion. Timings are kept apart: result_event_s (start -> complete result
    event), process_wall_s (start -> reaped), cleanup_s (time spent terminating after grace)."""
    err = open(stderr_path, "wb")
    start, timed_out, rc, t_result, cleanup_s, closed = now(), False, None, None, None, False
    buf = b""
    try:
        with open(stdout_path, "wb") as out, open(stdout_path, "rb") as rd:
            p = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=out, stderr=err,
                                 start_new_session=True)

            def feed():
                try:
                    p.stdin.write(stdin_text.encode())
                    p.stdin.close()
                except OSError:
                    pass
            threading.Thread(target=feed, daemon=True).start()

            def scan():
                nonlocal buf, t_result
                buf += rd.read()
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    if t_result is None and b'"result"' in line:
                        try:
                            ev = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if isinstance(ev, dict) and ev.get("type") == "result":
                            t_result = now()

            while p.poll() is None:
                scan()
                t = now()
                if t_result is not None and t - t_result >= grace:
                    closed, cleanup_s = True, kill_group(p)
                    break
                if t_result is None and t - start >= timeout:
                    timed_out, cleanup_s = True, kill_group(p)
                    break
                time.sleep(0.1)
            else:
                try:  # leader exited: sweep any leftover group members
                    os.killpg(p.pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass
            scan()
            rc = p.returncode
            if closed is False and timed_out is False and t_result is not None:
                cleanup_s = round(now() - t_result, 3)  # natural exit after the event
    except OSError as exc:
        rc = f"OSError: {exc}"
    finally:
        err.close()
    return {"rc": rc, "timed_out": timed_out, "closed_after_result": closed, "cleanup_s": cleanup_s,
            "secs": round(now() - start, 3),
            "result_event_s": None if t_result is None else round(t_result - start, 3)}


def bound_text(raw, limit):
    """Bound to <= limit UTF-8 bytes, keeping head and tail with a marker."""
    data = raw.decode("utf-8", "replace").encode("utf-8") if isinstance(raw, bytes) else raw.encode("utf-8")
    if len(data) <= limit:
        return data.decode("utf-8", "replace")
    marker = f"\n[... truncated {len(data) - limit} bytes ...]\n".encode()
    half = max((limit - len(marker)) // 2, 0)
    cut = data[:half].decode("utf-8", "ignore").encode() + marker + data[len(data) - half:].decode("utf-8", "ignore").encode()
    return cut[:limit].decode("utf-8", "ignore")


def find_named(d, names, pattern):
    """First existing file among `names` (comma list) in dir d, else first glob match."""
    for n in names.split(","):
        if n and (d / n).is_file():
            return d / n
    hits = sorted(p for p in d.glob(pattern) if p.is_file())
    return hits[0] if hits else None


def verdict(summary):
    """Best-effort 'red'/'green'/None from a qualify summary of unknown exact schema."""
    if not isinstance(summary, dict):
        return None
    for k in ("verdict", "status", "result", "outcome", "state"):
        v = summary.get(k)
        if isinstance(v, str):
            v = v.lower()
            if v in ("green", "pass", "passed", "ok", "success"):
                return "green"
            if v in ("red", "fail", "failed", "failure"):
                return "red"
    for k in ("green", "passed", "ok"):
        if isinstance(summary.get(k), bool):
            return "green" if summary[k] else "red"
    for k in ("exit_code", "returncode", "rc", "exit"):
        if isinstance(summary.get(k), int):
            return {0: "green", 1: "red"}.get(summary[k])
    return None


def strings_in(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from strings_in(k)
            yield from strings_in(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings_in(v)


# ------------------------------------------------------------------ context ----

class Bench:
    def __init__(self, opts, context):
        self.o, self.context = opts, context
        self.out = Path(opts.out).resolve()
        self.env = self.make_env()

    def make_env(self):
        env = dict(os.environ)
        for k in STRIP_ENV:
            env.pop(k, None)  # subscription auth only; no API key or base URL overrides
        env.update(OFFLINE_ENV)
        if self.o.zig_dir:
            env["PATH"] = str(Path(self.o.zig_dir).resolve()) + os.pathsep + env["PATH"]
        return env

    # --- receipts / diagnostics
    def receipt(self, case, kind):
        d = getattr(self.o, kind).get(case) or ROOT / "controls" / case / kind
        return Path(d).resolve()

    def read_receipt(self, d):
        """-> (summary_dict|None, sanitized_failure_path|None, problems)"""
        problems = []
        if not d.is_dir():
            return None, None, [f"missing receipt dir {d}"]
        sp = find_named(d, self.o.summary_name, "*summary*.json")
        summary = None
        if sp is None:
            problems.append(f"no summary in {d}")
        else:
            try:
                summary = json.loads(sp.read_text())
            except json.JSONDecodeError:
                problems.append(f"summary not JSON: {sp}")
        diag = find_named(d, self.o.diag_name, "*sanitized*")
        return summary, diag, problems

    def preflight_case(self, case):
        """Validate fixtures; returns (problems, info). Problems are fixture errors, not model results."""
        problems, info = [], {}
        c = ROOT / "cases" / case
        brief = c / "brief.txt"
        if not (brief.is_file() and brief.stat().st_size > 0):
            problems.append(f"{case}: cases/{case}/brief.txt missing or empty")
        if not (c / "base").is_dir():
            problems.append(f"{case}: cases/{case}/base missing")
        red, green = self.receipt(case, "red"), self.receipt(case, "green")
        if red == green:
            problems.append(f"{case}: red and green receipt dirs are the same")
        info.update(red=str(red), green=str(green))
        for kind, d in (("red", red), ("green", green)):
            summary, diag, probs = self.read_receipt(d)
            problems += [f"{case}/{kind}: {p}" for p in probs]
            v = verdict(summary) if summary is not None else None
            if summary is not None and v != kind and not (v is None and self.o.allow_unknown_verdict):
                problems.append(f"{case}/{kind}: summary verdict is {v!r}, expected {kind!r}")
            info[kind + "_verdict"] = v
            if kind == "red":
                if diag is None or not diag.read_bytes().strip():
                    problems.append(f"{case}/red: no non-empty sanitized failure (--diag-name={self.o.diag_name})")
                else:
                    info["failure_src"] = str(diag)
        return problems, info

    # --- phases
    def packet(self, source, issue, failure, adir, tag=""):
        """Run the evidence tool. Returns dict with text/valid/timing."""
        adir.mkdir(parents=True, exist_ok=True)
        cmd = [str(self.context), "evidence", "--repo", str(source), "--brief", str(issue),
               "--failure", str(failure), *EVIDENCE_ARGS]
        res = run_child(cmd, CONTEXT_TIMEOUT, cwd=self.out, env=self.env,
                        stdout_path=adir / f"packet{tag}.json", stderr_path=adir / f"packet{tag}.stderr")
        text = (adir / f"packet{tag}.json").read_text(errors="replace")
        try:
            obj = json.loads(text)
            valid = res["rc"] == 0 and not res["timed_out"]
        except json.JSONDecodeError:
            obj, valid = None, False
        return {"text": text, "obj": obj, "valid": valid, "secs": res["secs"], "rc": res["rc"],
                "timed_out": res["timed_out"], "bytes": len(text.encode())}

    def claude(self, source, prompt, adir, tools=True):
        adir.mkdir(parents=True, exist_ok=True)
        (adir / "prompt.txt").write_text(prompt)
        cmd = ["claude", "-p", "--model", MODEL, "--effort", EFFORT, "--output-format", "stream-json",
               "--verbose", "--no-session-persistence", "--strict-mcp-config", "--setting-sources", "project",
               "--disable-slash-commands"]
        if tools:
            cmd += ["--tools", "Bash,Glob,Grep,Read,Edit,Write", "--permission-mode", "acceptEdits",
                    "--allowedTools", *ALLOWED, "--disallowedTools", *DENIED]
        else:
            cmd += ["--tools", ""]
        cmd += ["--"]
        env = dict(self.env, ZIG_GLOBAL_CACHE_DIR=str(adir / "zig-cache"))
        res = run_stream_child(cmd, CLAUDE_TIMEOUT, self.o.result_grace, source, env, prompt,
                               adir / "events.jsonl", adir / "claude.stderr")
        result = {}
        for line in (adir / "events.jsonl").read_text(errors="replace").splitlines():
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(ev, dict) and ev.get("type") == "result":
                result = ev
        # error = infrastructure problem (not a timeout, which is a model-side outcome).
        # rc is ignored only when WE closed the group after a complete, non-error result.
        error = None
        if not res["timed_out"]:
            if result.get("is_error"):
                error = "is_error: " + str(result.get("result"))[:200]
            elif res["closed_after_result"] and result and res["result_event_s"] is not None:
                pass
            elif res["rc"] != 0:
                error = f"rc={res['rc']}"
            elif not result:
                error = "no result event"
        # attempt time = time to the completed event when there was one (same rule for all arms);
        # raw process wall and cleanup latency are recorded separately.
        done_s = res["result_event_s"] if (result and res["result_event_s"] is not None) else res["secs"]
        return {"secs": done_s, "process_wall_s": res["secs"], "result_event_s": res["result_event_s"],
                "agent_duration_ms": result.get("duration_ms"), "cleanup_s": res["cleanup_s"],
                "closed_after_result": res["closed_after_result"],
                "rc": res["rc"], "timed_out": res["timed_out"], "error": error,
                "text": result.get("result") if isinstance(result.get("result"), str) else "",
                "models": list((result.get("modelUsage") or {})), "usage": result.get("usage"),
                "turns": result.get("num_turns"), "cost_usd": result.get("total_cost_usd"),
                "denials": len(result.get("permission_denials") or [])}

    def grade(self, case, source, gdir, adir, n):
        cmd = [sys.executable, str(self.o.qualify), case, str(source), "--out", str(gdir)]
        res = run_child(cmd, self.o.grade_timeout, cwd=ROOT, env=self.env,
                        stdout_path=adir / f"grade{n}.stdout", stderr_path=adir / f"grade{n}.stderr")
        rc = res["rc"]
        state = "timeout" if res["timed_out"] else {0: "green", 1: "red"}.get(rc, "error")
        diag = find_named(gdir, self.o.diag_name, "*sanitized*") if gdir.is_dir() else None
        return {"state": state, "rc": rc, "secs": res["secs"], "diag": diag}

    def bounded_failure(self, src_path, dst):
        text = bound_text(Path(src_path).read_bytes(), self.o.failure_bytes)
        Path(dst).write_text(text)
        return text


def copy_base(case, tmp):
    source = tmp / "source"
    shutil.copytree(ROOT / "cases" / case / "base", source, symlinks=True,
                    ignore=shutil.ignore_patterns(".git"))
    return source


def diff_into(case, source, path):
    run_child(["diff", "-ruN", "-x", ".git", "-x", "node_modules", "-x", "target", "-x", ".zig-cache",
               str(ROOT / "cases" / case / "base"), str(source)], 60, stdout_path=path)


def new_tmp(B, case, arm):
    tmp = Path(tempfile.mkdtemp(prefix=f"bench-{case}-{arm}-")).resolve()
    if ROOT in tmp.parents or B.out in tmp.parents:
        raise RuntimeError("disposable source must live outside the grader/output tree")
    return tmp


# ------------------------------------------------------------- normal arms ----

def run_arm(B, case, arm, adir, issue_text, failure_text):
    """arm in direct|assisted. Fresh source, initial attempt, at most one follow-up."""
    adir.mkdir(parents=True, exist_ok=True)
    row = {"case": case, "arm": arm, "attempts": [], "excluded": None, "outcome": None}
    t0 = now()
    tmp = new_tmp(B, case, arm)
    try:
        source = copy_base(case, tmp)
        issue, failure_file = tmp / "issue.txt", tmp / "failure.log"
        issue.write_text(issue_text)
        failure_file.write_text(failure_text)
        cur_failure = failure_text
        for n in (1, 2):
            at = {"n": n}
            ad = adir / f"attempt{n}"
            ad.mkdir(parents=True, exist_ok=True)
            prompt = PROMPT.format(case=case, issue=issue_text, failure=failure_text) if n == 1 else \
                PROMPT.format(case=case, issue=issue_text, failure=failure_text) + FOLLOWUP.format(failure=cur_failure)
            if arm == "assisted":
                pk = B.packet(source, issue, failure_file, ad)
                at.update(retrieval_s=pk["secs"], packet_bytes=pk["bytes"], packet_valid=pk["valid"])
                if not pk["valid"]:
                    row["excluded"] = "setup_error: packet invalid"
                    row["attempts"].append(at)
                    break
                prompt += PACKET_INTRO + pk["text"]
            cl = B.claude(source, prompt, ad)
            at.update(claude_s=cl["secs"], claude_timed_out=cl["timed_out"], claude_error=cl["error"],
                      process_wall_s=cl["process_wall_s"], result_event_s=cl["result_event_s"],
                      agent_duration_ms=cl["agent_duration_ms"], cleanup_s=cl["cleanup_s"],
                      closed_after_result=cl["closed_after_result"],
                      models=cl["models"], turns=cl["turns"], usage=cl["usage"], cost_usd=cl["cost_usd"],
                      denials=cl["denials"])
            diff_into(case, source, ad / "changes.diff")
            if cl["error"]:
                row["excluded"] = "claude_error: " + cl["error"]
                row["attempts"].append(at)
                break
            gr = B.grade(case, source, ad / "grade", ad, n)
            at.update(grade_s=gr["secs"], grade=gr["state"])
            row["attempts"].append(at)
            if gr["state"] == "green":
                row["outcome"] = "green" if n == 1 else "green_after_followup"
                break
            if gr["state"] != "red":
                row["excluded"] = f"grade_{gr['state']}: fixture error, not a model result"
                break
            if n == 2:
                row["outcome"] = "red"
                break
            if gr["diag"] is None or not gr["diag"].read_bytes().strip():
                row["excluded"] = "setup_error: no sanitized diagnostics for follow-up"
                break
            cur_failure = B.bounded_failure(gr["diag"], adir / "failure.followup.log")
            failure_file = tmp / "failure2.log"
            failure_file.write_text(cur_failure)
        shutil.copytree(source, adir / "candidate", symlinks=True)
    except Exception as exc:  # fixture/runner problem; keep the run going
        row["excluded"] = f"runner_exception: {type(exc).__name__}: {exc}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    totals(row, now() - t0)
    return row


def totals(row, total):
    a = row["attempts"]
    first, rest = (a[0] if a else {}), a[1:]
    key = lambda d, k: d.get(k) or 0
    row["retrieval_s"] = round(sum(key(x, "retrieval_s") for x in a), 3)
    row["claude_s"] = round(sum(key(x, "claude_s") for x in a), 3)
    row["grade_s"] = round(sum(key(x, "grade_s") for x in a), 3)
    row["retry_s"] = round(sum(key(x, "retrieval_s") + key(x, "claude_s") + key(x, "grade_s") for x in rest), 3)
    row["first_attempt_s"] = round(key(first, "retrieval_s") + key(first, "claude_s") + key(first, "grade_s"), 3)
    row["total_s"] = round(total, 3)
    row["counts_for_model"] = row["excluded"] is None and row["outcome"] is not None


# ------------------------------------------------------------- bounded arm ----

def parse_edits(text):
    m = text.strip()
    if m.startswith("```"):
        m = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", m)
    i, j = m.find("{"), m.rfind("}")
    if i < 0 or j < i:
        raise ValueError("no JSON object in reply")
    edits = json.loads(m[i:j + 1]).get("edits")
    if not isinstance(edits, list) or not edits or len(edits) > MAX_EDITS:
        raise ValueError(f"edits must be a list of 1..{MAX_EDITS}")
    for e in edits:
        if not (isinstance(e, dict) and all(isinstance(e.get(k), str) for k in ("path", "original", "replacement"))):
            raise ValueError("each edit needs string path, original, replacement")
    return edits


def apply_edits(source, edits, packet_obj):
    """Check every edit (path in packet and inside source, original shown in packet and unique
    in the file) and only then write. Raises ValueError on the first violation."""
    shown = list(strings_in(packet_obj))
    blob = "\n".join(shown)
    contents, root = {}, Path(source).resolve()
    for i, e in enumerate(edits):
        rel = e["path"]
        p = (root / rel).resolve()
        if os.path.isabs(rel) or root not in p.parents or not p.is_file():
            raise ValueError(f"edit {i}: path outside source or missing: {rel}")
        if rel not in blob and rel.lstrip("./") not in blob:
            raise ValueError(f"edit {i}: path not shown in packet: {rel}")
        if not e["original"].strip() or e["original"] == e["replacement"]:
            raise ValueError(f"edit {i}: empty or no-op original")
        if not any(e["original"] in s for s in shown):
            raise ValueError(f"edit {i}: original not shown in packet")
        text = contents.get(p)
        if text is None:
            text = p.read_text()
        if text.count(e["original"]) != 1:
            raise ValueError(f"edit {i}: original occurs {text.count(e['original'])} times in {rel}")
        contents[p] = text.replace(e["original"], e["replacement"], 1)
    for p, text in contents.items():
        p.write_text(text)
    return sorted(str(p.relative_to(root)) for p in contents)


def run_bounded(B, case, adir, issue_text, failure_text):
    adir.mkdir(parents=True, exist_ok=True)
    row = {"case": case, "arm": "bounded", "excluded": None, "outcome": None, "fallback": None}
    t0 = now()
    tmp = new_tmp(B, case, "bounded")
    reason = None
    try:
        source = copy_base(case, tmp)
        issue, failure_file = tmp / "issue.txt", tmp / "failure.log"
        issue.write_text(issue_text)
        failure_file.write_text(failure_text)
        ad = adir / "attempt1"
        pk = B.packet(source, issue, failure_file, ad)
        row.update(retrieval_s=pk["secs"], packet_bytes=pk["bytes"], packet_valid=pk["valid"])
        if not pk["valid"]:
            row["excluded"] = "setup_error: packet invalid"
        else:
            prompt = BOUNDED_PROMPT.format(n=MAX_EDITS, issue=issue_text, failure=failure_text,
                                           intro=PACKET_INTRO, packet=pk["text"])
            cl = B.claude(source, prompt, ad, tools=False)
            row.update(claude_s=cl["secs"], claude_timed_out=cl["timed_out"], claude_error=cl["error"],
                       process_wall_s=cl["process_wall_s"], result_event_s=cl["result_event_s"],
                       agent_duration_ms=cl["agent_duration_ms"], cleanup_s=cl["cleanup_s"],
                       closed_after_result=cl["closed_after_result"],
                       models=cl["models"], usage=cl["usage"], cost_usd=cl["cost_usd"])
            if cl["error"]:
                reason = "claude_error: " + cl["error"]
            elif cl["timed_out"]:
                reason = "claude_timeout"
            else:
                t1 = now()
                try:
                    changed = apply_edits(source, parse_edits(cl["text"]), pk["obj"])
                    row["applied_files"] = changed
                except (ValueError, json.JSONDecodeError, OSError) as exc:
                    reason = f"edits_rejected: {exc}"
                row["apply_s"] = round(now() - t1, 3)
            if reason is None:
                gr = B.grade(case, source, ad / "grade", ad, 1)
                row.update(grade_s=gr["secs"], grade=gr["state"])
                diff_into(case, source, ad / "changes.diff")
                if gr["state"] == "green":
                    row["outcome"] = "bounded_green"
                    shutil.copytree(source, adir / "candidate", symlinks=True)
                elif gr["state"] == "red":
                    reason = "verification_red"
                else:
                    row["excluded"] = f"grade_{gr['state']}: fixture error, not a model result"
    except Exception as exc:
        row["excluded"] = f"runner_exception: {type(exc).__name__}: {exc}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if reason and row["excluded"] is None:
        fb = run_arm(B, case, "assisted", adir / "fallback", issue_text, failure_text)
        row["fallback"] = {"reason": reason, **{k: fb[k] for k in (
            "outcome", "excluded", "retrieval_s", "claude_s", "grade_s", "retry_s", "total_s")}}
        row["outcome"] = "fallback_" + str(fb["outcome"]) if fb["outcome"] else None
        row["excluded"] = fb["excluded"]
    row["total_s"] = round(now() - t0, 3)
    row["counts_for_model"] = row["excluded"] is None and row["outcome"] is not None
    return row


# --------------------------------------------------------------------- main ----

def run_case(args):
    B, idx, case, info = args
    cdir = B.out / case
    cdir.mkdir(parents=True, exist_ok=True)
    issue_text = (ROOT / "cases" / case / "brief.txt").read_text()
    failure_text = B.bounded_failure(info["failure_src"], cdir / "failure.initial.log")
    (cdir / "issue.txt").write_text(issue_text)
    write_json(cdir / "case.json", {**info, "failure_sha256": hashlib.sha256(failure_text.encode()).hexdigest(),
                                    "failure_bytes": len(failure_text.encode())})
    order = ["direct", "assisted"]
    if (idx + B.o.rotate) % 2:
        order.reverse()
    rows = []
    for arm in order + (["bounded"] if B.o.bounded else []):
        adir = cdir / arm
        if adir.exists():
            continue
        row = run_bounded(B, case, adir, issue_text, failure_text) if arm == "bounded" \
            else run_arm(B, case, arm, adir, issue_text, failure_text)
        row["pair_order"] = order
        write_json(adir / "summary.json", row)
        print(case, arm, row["outcome"], row["excluded"] or "", f"total={row['total_s']}s", flush=True)
        rows.append(row)
    return rows


def summarize(rows):
    by = {}
    for r in rows:
        by.setdefault(r["case"], {})[r["arm"]] = r
    pairs = []
    for case, arms in by.items():
        d, a = arms.get("direct"), arms.get("assisted")
        ok = bool(d and a and d["counts_for_model"] and a["counts_for_model"])
        pairs.append({"case": case, "matched": ok, "direct": d and (d["outcome"] or d["excluded"]),
                      "assisted": a and (a["outcome"] or a["excluded"])})
    tally = {}
    for p in pairs:
        if p["matched"]:
            for arm in ("direct", "assisted"):
                tally.setdefault(arm, {}).setdefault(p[arm], 0)
                tally[arm][p[arm]] += 1
    return {"pairs": pairs, "matched_pair_tally": tally,
            "excluded_rows": [{"case": r["case"], "arm": r["arm"], "why": r["excluded"]} for r in rows if r["excluded"]]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", required=True, help="comma-separated case names under cases/")
    ap.add_argument("--context", required=True, help="exact context executable (e.g. kogen-context)")
    ap.add_argument("--context-sha256", required=True, help="expected SHA-256 of --context")
    ap.add_argument("--out", required=True, help="NEW output directory")
    ap.add_argument("--red", action="append", default=[], metavar="CASE=DIR", help="red receipt dir override")
    ap.add_argument("--green", action="append", default=[], metavar="CASE=DIR", help="green receipt dir override")
    ap.add_argument("--qualify", default=str(ROOT / "qualify.py"))
    ap.add_argument("--summary-name", default="summary.json", help="comma list of receipt summary filenames")
    ap.add_argument("--diag-name", default="failure.sanitized.log",
                    help="comma list of sanitized-failure filenames (falls back to *sanitized* glob); raw logs are never sent")
    ap.add_argument("--allow-unknown-verdict", action="store_true", help="accept receipts whose summary has no recognizable verdict")
    ap.add_argument("--failure-bytes", type=int, default=4000, help="bound on the failure log given to every arm")
    ap.add_argument("--grade-timeout", type=int, default=600)
    ap.add_argument("--result-grace", type=float, default=RESULT_GRACE,
                    help="seconds a Claude process may outlive its complete result event before its process group is terminated (all arms)")
    ap.add_argument("--zig-dir", help="optional dir with zig to prepend to PATH")
    ap.add_argument("--bounded", action="store_true", help="also run exploratory third arm")
    ap.add_argument("--rotate", type=int, default=0, help="shift the direct/assisted dispatch rotation")
    ap.add_argument("--jobs", type=int, default=1, help="cases in parallel (1 keeps wall times clean)")
    ap.add_argument("--preflight", action="store_true", help="validate everything, launch no model")
    o = ap.parse_args()

    for kind in ("red", "green"):
        d = {}
        for item in getattr(o, kind):
            k, _, v = item.partition("=")
            if not v:
                sys.exit(f"--{kind} expects CASE=DIR, got {item!r}")
            d[k] = v
        setattr(o, kind, d)
    names = [n for n in o.cases.split(",") if n]
    if not names or len(set(names)) != len(names):
        sys.exit("--cases must be a non-empty list without duplicates")
    out = Path(o.out).resolve()
    if out.exists():
        sys.exit(f"--out {out} already exists; choose a new directory")
    ctx = Path(o.context).resolve()
    if not (ctx.is_file() and os.access(ctx, os.X_OK)):
        sys.exit(f"context {ctx} is not an executable file")
    got = sha256(ctx)
    if got != o.context_sha256.lower():
        sys.exit(f"context SHA-256 mismatch: got {got}, expected {o.context_sha256}")
    if not Path(o.qualify).is_file():
        sys.exit(f"qualify script not found: {o.qualify}")
    o.qualify = Path(o.qualify).resolve()
    ver = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=30).stdout.strip()
    if not ver.startswith(CLAUDE_VERSION):
        sys.exit(f"expected Claude Code {CLAUDE_VERSION}, got {ver!r}")

    out.mkdir(parents=True)
    staged = out / "tool" / ctx.name  # run the verified copy, not the original path
    staged.parent.mkdir()
    shutil.copy2(ctx, staged)
    if sha256(staged) != got:
        sys.exit("staged context copy hash changed")
    B = Bench(o, staged)

    infos, problems = {}, []
    for c in names:
        probs, info = B.preflight_case(c)
        problems += probs
        infos[c] = info
    # Fixture check for the evidence tool on a scratch copy (no model involved).
    if not problems:
        for c in names:
            tmp = new_tmp(B, c, "preflight")
            try:
                src = copy_base(c, tmp)
                (tmp / "issue.txt").write_text((ROOT / "cases" / c / "brief.txt").read_text())
                (tmp / "f.log").write_text(B.bounded_failure(infos[c]["failure_src"], out / f"{c}.preflight-failure.log"))
                pk = B.packet(src, tmp / "issue.txt", tmp / "f.log", out / "preflight" / c)
                infos[c]["preflight_packet"] = {k: pk[k] for k in ("valid", "bytes", "secs")}
                if not pk["valid"]:
                    problems.append(f"{c}: evidence packet invalid in preflight (rc={pk['rc']})")
            except Exception as exc:
                problems.append(f"{c}: preflight exception {exc}")
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
    meta = {"started": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "argv": sys.argv, "host": platform.platform(),
            "claude": ver, "model": MODEL, "effort": EFFORT, "context_sha256": got, "staged_context": str(staged),
            "qualify": str(o.qualify), "qualify_sha256": sha256(o.qualify), "cases": names,
            "claude_timeout_s": CLAUDE_TIMEOUT, "result_grace_s": o.result_grace, "allowed_tools": ALLOWED, "denied_tools": DENIED,
            "stripped_env": STRIP_ENV, "offline_env": OFFLINE_ENV, "evidence_args": EVIDENCE_ARGS,
            "failure_bytes": o.failure_bytes, "bounded_arm": o.bounded, "case_info": infos, "problems": problems}
    write_json(out / "meta.json", meta)
    if problems:
        print("PREFLIGHT FAILED (fixture problems, nothing launched):", *problems, sep="\n  ", file=sys.stderr)
        sys.exit(2)
    if o.preflight:
        print(f"preflight OK for {names}; no model launched. See {out / 'meta.json'}")
        return

    jobs = [(B, i, c, infos[c]) for i, c in enumerate(names)]
    with ThreadPoolExecutor(max_workers=max(1, o.jobs)) as pool:
        rows = [r for rs in pool.map(run_case, jobs) for r in rs]
    summary = summarize(rows)
    write_json(out / "summary.json", {"rows": rows, **summary})
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
