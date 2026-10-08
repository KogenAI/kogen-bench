#!/usr/bin/env python3
"""bench: minimal benchmark runner for Kogen harness/model/effort/prompt experiments.

  bench run   EXPERIMENT.json | --name N --harness H --model M --effort E --prompt P --task T --rep 1
  bench table EXPERIMENT [EXPERIMENT ...] [--by harness,model,effort,prompt] [--csv]
  bench probe [--harness h,h] [--models probe.json]
  bench grade EXPERIMENT
  bench auth

One cell = (harness, model, effort, prompt variant, task item, repetition), run in a fresh
directory made from `git archive <base_sha>` plus a fresh `git init` (no history leaks).
Results: $BENCH_ROOT/results/<experiment>/<cell>/ (default BENCH_ROOT=~/bench). Stdlib only, Python 3.9+.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import platform
import random
import re
import shutil
import signal
import statistics
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harnesses as H  # noqa: E402
import sandbox as SB  # noqa: E402
import egress as EG  # noqa: E402
import status as ST  # noqa: E402
import locks as LK  # noqa: E402
import retention as RT  # noqa: E402
import concurrent_grade as CG  # noqa: E402

SCHEMA = 1
FINAL = ("ok", "error", "timeout", "infra_error")
# provider keys that would silently switch a subscription run to metered API billing
SCRUB_ENV = ["ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_OAUTH_TOKEN", "OPENAI_API_KEY", "OPENAI_BASE_URL",
             "GEMINI_API_KEY", "GOOGLE_API_KEY", "XAI_API_KEY", "GROK_DEPLOYMENT_KEY", "OPENROUTER_API_KEY",
             "COPILOT_GITHUB_TOKEN", "GH_TOKEN", "GITHUB_TOKEN", "CURSOR_API_KEY", "CURSOR_AUTH_TOKEN", "KIMI_API_KEY",
             "ZAI_API_KEY", "MINIMAX_API_KEY", "OPENCODE_API_KEY"]


def root():
    return H.root()


def results_dir():
    return Path(os.environ.get("BENCH_RESULTS", str(root() / "results")))


def tasks_dir():
    return Path(os.environ.get("BENCH_TASKS", str(root() / "tasks")))


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")


def slug(s):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", str(s)).strip("-") or "x"


def cell_id(c):
    return "__".join([slug(c["harness"]), slug(c.get("model") or "default"), slug(c.get("effort") or "default"),
                      slug(c.get("prompt") or "default"), slug(c["task"]), "r%d" % c.get("rep", 1)])


def write_json(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".%s.tmp" % LK.uuid.uuid4().hex)
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=False, default=str))
    os.replace(tmp, p)


def sh(argv, cwd=None, env=None, check=True, timeout=600, input=None):
    p = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, timeout=timeout, input=input)
    if check and p.returncode != 0:
        raise RuntimeError("%s failed (%d): %s" % (argv[:3], p.returncode, p.stderr.decode(errors="replace")[:500]))
    return p


# ------------------------------------------------------------------ tasks

PORTABLE_HOMES = ("${BENCH_HOME}", "${BENCH_HOME}", "/Users/${BENCH_USER}")  # homes that task.json files were authored with


def _relocate(o, home=None):
    """task.json carries absolute paths from the machine it was authored on (${BENCH_HOME}/bench/...). Map that home prefix onto this
    machine's home ($HOME; the runner's BENCH_ROOT is $HOME/bench by default) so the same task files work on the Studio, the MacBook and the
    Linux workers without staging edits. Only whole-prefix matches at a path boundary; other strings are untouched."""
    home = home or str(Path.home())
    if isinstance(o, str):
        for p in PORTABLE_HOMES:
            if p != home and (o == p or p + "/" in o):
                o = o.replace(p + "/", home + "/").replace(p + ":", home + ":")
                if o == p:
                    o = home
        return o
    if isinstance(o, list):
        return [_relocate(x, home) for x in o]
    if isinstance(o, dict):
        return {k: _relocate(v, home) for k, v in o.items()}
    return o


def load_task(task_id):
    """~/bench/tasks/<id>/task.json: {repo, base_sha | base_dir, prompt, setup, grade, timeout_s, env}.
    Falls back to a `base_sha` file and prompt.md. `_probe` is built in."""
    if task_id == "_probe":
        return {"id": "_probe", "empty": True, "prompt_text": "Reply with the single word OK.", "dir": None}
    d = tasks_dir() / task_id
    tj = d / "task.json"
    t = _relocate(json.loads(tj.read_text())) if tj.exists() else {}
    t.setdefault("id", task_id)
    t["dir"] = str(d)
    if "base_sha" not in t and (d / "base_sha").exists():
        t["base_sha"] = (d / "base_sha").read_text().strip()
    if not d.is_dir():
        raise SystemExit("task %s not found under %s" % (task_id, tasks_dir()))
    return t


def quarantine_reason(task_id):
    """task.json `quarantined` (non-empty string/true) -> reason text, else None. Quarantined tasks are not scored."""
    try:
        q = json.loads((tasks_dir() / task_id / "task.json").read_text()).get("quarantined")
    except (OSError, ValueError):
        return None
    if not q:
        return None
    return q if isinstance(q, str) else "quarantined"


def quarantine_report(ms):
    """Lines describing quarantined tasks seen in manifests ms plus the scored denominator per task family."""
    seen = {}
    for m in ms:
        t = (m.get("requested") or {}).get("task")
        if t and t not in seen:
            seen[t] = quarantine_reason(t)
    lines = []
    fams = set()
    for t, why in sorted(seen.items()):
        if why:
            n = sum(1 for m in ms if (m.get("requested") or {}).get("task") == t)
            lines.append("quarantined (not scored)  %s  [%d cells excluded]: %s" % (t, n, why))
            fams.add(t.split("-")[0])
    for fam in sorted(fams):
        tot = q = 0
        for d in sorted(tasks_dir().glob(fam + "-*/task.json")):
            if d.parent.name.startswith(fam + "-_"):
                continue
            tot += 1
            q += 1 if quarantine_reason(d.parent.name) else 0
        lines.append("%s: %d/%d tasks scored (%d quarantined)" % (fam, tot - q, tot, q))
    return lines


def task_prompt(task, variant):
    """Variant lookup: <task>/prompts/<variant>.md, else <task>/prompt.md for 'default', else a wrapper
    template $BENCH_ROOT/prompts/<variant>.md with {{TASK}} replaced by the task's prompt.md."""
    if "prompt_text" in task:
        return task["prompt_text"]
    d = Path(task["dir"])
    base = d / task.get("prompt", "prompt.md")
    for cand in (d / "prompts" / ("%s.md" % variant), ):
        if cand.exists():
            return cand.read_text()
    if variant in (None, "", "default"):
        return base.read_text()
    tpl = root() / "prompts" / ("%s.md" % variant)
    if tpl.exists():
        return tpl.read_text().replace("{{TASK}}", base.read_text())
    raise SystemExit("prompt variant %r not found for task %s" % (variant, task["id"]))


GIT_ENV_ARGS = ["-c", "user.name=bench", "-c", "user.email=bench@localhost", "-c", "commit.gpgsign=false"]


def prepare_workdir(task, work):
    """Fresh dir from `git archive` of the base (or copy of base_dir), then a brand-new one-commit repo."""
    work = Path(work)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    info = {}
    if task.get("empty"):
        pass
    elif task.get("base_sha"):
        repo = task.get("repo")
        if not repo:
            raise SystemExit("task %s has base_sha but no repo" % task["id"])
        arch = subprocess.Popen(["git", "-C", repo, "archive", task["base_sha"]], stdout=subprocess.PIPE)
        tar = subprocess.run(["tar", "-x", "-C", str(work)], stdin=arch.stdout, capture_output=True)
        arch.stdout.close()
        if arch.wait() != 0 or tar.returncode != 0:
            raise RuntimeError("git archive/tar failed for %s@%s: %s" % (repo, task["base_sha"], tar.stderr.decode()[:300]))
        info["base_sha"] = task["base_sha"]
    elif task.get("base_dir"):
        src = Path(task["base_dir"])
        if not src.is_absolute():
            src = Path(task["dir"]) / src
        shutil.copytree(src, work, dirs_exist_ok=True)
        info["base_dir"] = str(src)
    else:
        raise SystemExit("task %s needs base_sha (+repo) or base_dir" % task["id"])
    sh(["git", "init", "-q"], cwd=work)
    sh(["git"] + GIT_ENV_ARGS + ["commit", "-q", "--allow-empty", "-m", "base"] if task.get("empty") else ["git", "add", "-A"], cwd=work)
    if not task.get("empty"):
        sh(["git"] + GIT_ENV_ARGS + ["commit", "-q", "-m", "base"], cwd=work)
    info["fresh_base_commit"] = sh(["git", "rev-parse", "HEAD"], cwd=work).stdout.decode().strip()
    return info


def capture_diff(work, attempt_dir, base_commit):
    try:
        sh(["git", "add", "-A"], cwd=work)
        p = sh(["git", "diff", "--cached", "--binary", base_commit], cwd=work, check=False)
        Path(attempt_dir, "patch.diff").write_bytes(p.stdout)
        st = sh(["git", "diff", "--cached", "--shortstat", base_commit], cwd=work, check=False).stdout.decode().strip()
        return {"bytes": len(p.stdout), "shortstat": st or "no changes"}
    except Exception as ex:  # noqa: BLE001
        return {"error": str(ex)[:200]}


# ------------------------------------------------------------------ running one attempt

def child_env(extra):
    env = dict(os.environ)
    scrubbed = [k for k in SCRUB_ENV if k in env]
    for k in scrubbed:
        del env[k]
    env["PATH"] = "%s:%s" % (H.tools_bin(), env.get("PATH", "/usr/bin:/bin"))
    env["NO_COLOR"] = "1"
    env.update(extra or {})
    if SB.LINUX:
        env["PATH"] = SB._sl().with_shim(env.get("PATH"))
    return env, scrubbed


_version_cache = {}


def cli_version(h, env):
    if h not in _version_cache:
        w = H.wrapper_path(h)
        try:
            p = subprocess.run([str(w), "--version"], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30, env=env)
            _version_cache[h] = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout or p.stderr)).strip().splitlines()[0][:120] if (p.stdout or p.stderr).strip() else None
        except Exception as ex:  # noqa: BLE001
            _version_cache[h] = "unavailable: %s" % str(ex)[:60]
    return _version_cache[h]


def TURN_CAP_RX_search(text):
    return H.TURN_CAP_RX.search(text or "")


def kill_group(proc):
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        return
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        proc.wait()


def read_events(path):
    ev, bad = [], 0
    try:
        with open(path, errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except ValueError:
                    bad += 1
                    continue
                if isinstance(d, dict):
                    ev.append(d)
    except OSError:
        pass
    return ev, bad


def model_match(requested, observed):
    """True/False/None. Loose: provider prefix and [1m]/-build style suffixes are ignored."""
    if not observed:
        return None
    def norm(s):
        s = str(s).lower().split("/")[-1]
        return re.sub(r"(\[.*?\]|-build|-latest)$", "", s)
    r = norm(requested or "")
    if not r or r == "default":
        return None
    return any(norm(o) == r or r in norm(o) or norm(o) in r for o in observed)


def resolve_timeout(cell, task, opts):
    """ONE wall-clock limit per cell, identical for every harness. Precedence: --timeout on the command line, then the cell (experiment
    arm/file), the task, the experiment default, 1800. The harness-internal timeouts (kh/kh-cc/khr `--timeout`) are derived from this same
    value by the adapters (limit minus 20 s), so the runner's kill is always the outer bound."""
    for v in (opts.get("timeout_override"), cell.get("timeout_s"), task.get("timeout_s"), opts.get("timeout_s")):
        if v:
            return int(v)
    return 1800


def resolve_turn_cap(cell, task, opts):
    for v in (opts.get("max_turns_override"), cell.get("max_turns"), task.get("max_turns"), opts.get("max_turns")):
        if v:
            return int(v)
    return None


def reap_group(pid):
    """SIGKILL whatever is still alive in the harness's process group (descendants that outlive the leader). True if the group had members."""
    try:
        os.killpg(pid, 0)
    except (ProcessLookupError, PermissionError):
        return False
    try:
        os.killpg(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass
    return True


def egress_on():
    return os.environ.get("BENCH_EGRESS", "1") != "0"


def run_attempt(cell, exp, task, prompt, n, opts):
    ad = H.get(cell["harness"])
    cdir = results_dir() / exp / cell["cell_id"]
    adir = cdir / ("attempt-%d" % n)
    adir.mkdir(parents=True, exist_ok=True)
    work = adir / "work"
    rec = {"n": n, "started_at": now(), "status": None, "error_class": None, "errors": []}
    try:
        winfo = prepare_workdir(task, work)
    except Exception as ex:  # noqa: BLE001
        rec.update(status="infra_error", error_class="workdir", errors=[str(ex)[:500]], ended_at=now())
        return rec, None
    rec["workdir"] = dict(winfo, path=str(work))
    env, scrubbed = child_env(task.get("env"))
    if task.get("setup"):
        t0 = time.time()
        p = subprocess.run(task["setup"], shell=True, cwd=work, env=env, capture_output=True, text=True, timeout=task.get("setup_timeout_s", 1800))
        rec["setup"] = {"rc": p.returncode, "wall_s": round(time.time() - t0, 3), "stderr_tail": p.stderr[-300:]}
        if p.returncode != 0:
            rec.update(status="infra_error", error_class="setup", errors=["setup failed"], ended_at=now())
            return rec, None
        sh(["git", "add", "-A"], cwd=work, check=False)
        sh(["git"] + GIT_ENV_ARGS + ["commit", "-q", "--allow-empty", "-m", "setup"], cwd=work, check=False)
        winfo["fresh_base_commit"] = sh(["git", "rev-parse", "HEAD"], cwd=work).stdout.decode().strip()
    ctx = {"cwd": str(work), "attempt_dir": str(adir), "env": env, "no_config_probe": opts.get("no_config_probe")}
    timeout = resolve_timeout(cell, task, opts)
    cell = dict(cell, timeout_s=timeout)  # adapters derive their internal timeouts from the resolved value, never from a default
    argv = ad.build(cell, ctx)
    turn_cap = resolve_turn_cap(cell, task, opts)
    rec["limits"] = {"timeout_s": timeout, "turn_cap": turn_cap,
                     "turn_cap_enforced_by": (ad.max_turns_flag or None) if turn_cap else None,
                     "turn_cap_supported": bool(ad.max_turns_flag)}
    _extra = list(opts.get("extra_args", {}).get(cell["harness"], []))
    if turn_cap and ad.max_turns_flag and ad.max_turns_flag not in _extra:
        _extra = [ad.max_turns_flag, str(turn_cap)] + _extra
    if _extra and argv and argv[-1] in ("-p", "--", "-"):  # keep the trailing prompt marker last so extras are parsed as flags
        argv = argv[:-1] + _extra + [argv[-1]]
    else:
        argv = argv + _extra
    if ad.prompt_via == "stdin":
        stdin_data = prompt.encode()
        full = argv
        shown = argv + ["<prompt via stdin>"]
    else:
        stdin_data = None
        full = argv + [prompt]
        shown = argv + ["<prompt>"]
    rec["argv"] = shown
    px = None
    sb_key = None
    if SB.enabled():
        _sh = [str(H.homes() / x) for x in getattr(ad, "sandbox_homes", ())]
        if egress_on():
            px = EG.Proxy(adir / "egress.jsonl", "%s/%s/attempt-%d" % (exp, cell["cell_id"], n), EG.allowlist(cell["harness"], task.get("egress_allow")))
            px.__enter__()
            env.update(px.env())
            # registries are denied by the proxy: make the package managers fail fast from their caches instead of retrying (offline only when the task did not opt the registry in)
            _al = set(task.get("egress_allow") or [])
            for _k, _v, _h in (("HEX_OFFLINE", "1", "repo.hex.pm"), ("CARGO_NET_OFFLINE", "true", "index.crates.io")):
                if _h not in _al:
                    env.setdefault(_k, _v)
        full, pf = SB.wrap(full, cell["harness"], adir, H.homes(), H.tools_bin().parent, extra_ro=_sh, extra_rw=_sh,
                           egress_port=px.port if px else None, env=env, max_runtime=timeout + 120)
        sb_key = pf
        rec["sandbox"] = {"mode": SB.backend(), "profile": pf,
                          "egress": {"mode": "allowlist-proxy", "allow": px.allow, "log": "egress.jsonl"} if px else {"mode": "open"}}
    else:
        rec["sandbox"] = {"mode": "off"}
    write_json(adir / "config.json", H.snapshot_config(ad, cell, shown, ctx, scrubbed, task.get("env") or {}))
    if SB.LINUX and SB.enabled():  # night 2026-10-01: config probes ran as the runner and recreated home files (codex tmp/arg0 0700); hand the home back
        _a0 = H.homes() / cell["harness"] / "tmp" / "arg0"  # created by the runner-side codex config probe; the sandbox user must own its own
        if _a0.is_dir() and _a0.stat().st_uid == os.getuid():
            shutil.rmtree(_a0, ignore_errors=True)
        SB._sl().prepare_tree(H.homes() / cell["harness"])
    tpath = adir / "transcript.jsonl"
    t0m = time.monotonic()
    rec["run_started_at"] = now()
    timed_out = False
    with open(tpath, "wb") as out, open(adir / "stderr.txt", "wb") as err:
        try:
            proc = subprocess.Popen(full, cwd=work, env=env, stdin=subprocess.PIPE if stdin_data is not None else subprocess.DEVNULL,
                                    stdout=out, stderr=err, start_new_session=True)
        except OSError as ex:
            if px:
                px.__exit__()
            if sb_key:
                SB.teardown(sb_key)
            rec.update(status="infra_error", error_class="spawn", errors=[str(ex)], ended_at=now())
            return rec, None
        try:
            proc.communicate(input=stdin_data, timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            if sb_key:
                SB.kill(sb_key)
            kill_group(proc)
        except BrokenPipeError:
            proc.wait()
        except BaseException:  # night 2026-10-01 termfix: guard TERM/HUP -> kill the harness session before the runner exits
            if sb_key:
                SB.kill(sb_key)
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
            reap_group(proc.pid)
            if sb_key:
                SB.teardown(sb_key)
            if px:
                px.__exit__()
            raise
        stragglers = reap_group(proc.pid)  # descendants that outlive the leader (also after a clean exit)
    if sb_key:  # Linux: kill the whole cgroup/pid namespace and record the proof (macOS: no-op, the group reap above is the cleanup)
        td = SB.teardown(sb_key)
        rec["sandbox"]["teardown"] = td
        stragglers = stragglers or bool(td.get("killed_pids"))
    if px:
        px.__exit__()
        rec["contamination"] = EG.build_report(adir, task.get("contam_terms") or ())
    wall = time.monotonic() - t0m
    rec["stragglers_killed"] = bool(stragglers) and not timed_out
    rec["run_ended_at"] = now()
    rec["wall_s"] = round(wall, 3)
    rec["exit_code"] = proc.returncode
    rec["signal"] = -proc.returncode if proc.returncode and proc.returncode < 0 else None
    rec["timed_out"] = timed_out
    events, bad = read_events(tpath)
    rec["events"] = len(events)
    rec["unparsed_lines"] = bad
    ctx["cwd"] = str(work)
    ctx["home"] = str(ad.home())
    try:
        parsed = ad.parse(events, ctx)
    except Exception as ex:  # noqa: BLE001
        parsed = H.new_result()
        parsed["errors"].append("parser crashed: %r" % ex)
    stderr_txt = (adir / "stderr.txt").read_text(errors="replace")
    err_text = "\n".join(parsed["errors"] + [H.strip_benign(stderr_txt)[-2000:]])
    rec["error_class"] = H.classify_error(err_text) if (parsed["is_error"] or parsed["errors"] or proc.returncode not in (0, None) or not events) else None
    got_output = bool(events) and (parsed["final_text"] is not None or any(v is not None for v in parsed["usage"].values()))
    cap_hit = bool(turn_cap) and bool(TURN_CAP_RX_search(err_text)) and not timed_out
    if timed_out or parsed["extra"].get("timed_out"):
        rec["status"] = "timeout"
    elif proc.returncode == 0 and not parsed["is_error"] and got_output:
        rec["status"] = "ok"
    elif not got_output or rec["error_class"] in ("rate_limit", "auth", "network"):
        rec["status"] = "infra_error"
    else:
        rec["status"] = "error"
    rec["errors"] = parsed["errors"] + ([stderr_txt.strip()[-300:]] if rec["status"] not in ("ok",) and stderr_txt.strip() else [])
    # infra errors seen next to a timeout/error status (stream died, 429, auth, sandbox denial) mark the cell infra even when partial output exists
    if rec["status"] in ("error", "timeout") and rec["error_class"] in H.INFRA_CLASSES:
        rec["status_raw"] = rec["status"]
        rec["status"] = "infra_error"
    rec["failure_kind"] = H.failure_kind(rec["status"], rec["error_class"])
    if rec["status"] == "timeout":
        cause = "runner_wall_clock" if timed_out else "harness_internal_timeout"
    elif cap_hit:
        cause = "turn_cap"
    else:
        cause = None
    rec["timeout"] = {"limit_s": timeout, "elapsed_s": round(wall, 3), "cause": cause,
                      "enforced_by": "runner (communicate timeout + process-group kill)", "turn_cap": turn_cap}
    rec["diff"] = capture_diff(work, adir, winfo["fresh_base_commit"])
    rec["ended_at"] = now()
    if opts.get("grade") and not sealed_on() and task.get("grade") and rec["status"] in ("ok", "error", "timeout"):
        rec["grade"] = run_grade(task, work, adir)
    if opts.get("cleanup"):
        shutil.rmtree(work, ignore_errors=True)
    return rec, parsed


GRADE_INFRA_RX = re.compile(r"bwrap: |No permissions to create new namespace|systemd-run: |sandbox-exec|sandbox: |deny\(\d+\)|Operation not permitted|FS_PERMISSION_DENIED|command not found|No such file or directory: .*grade|"
                            r"snapshot failed|GRADER_ERROR|cannot restore", re.I)


# Harmless sandbox noise that carries an infra-looking phrase ("Operation not permitted"): git probing ~/.gitignore / ~/.config/git under the
# grade sandbox (macOS deny, Linux empty tmpfs home), mise/asdf writing or reading its cache or config in a denied home. A real FAIL must not
# turn into grader_error because of them, so these lines are dropped before the infra patterns are applied (any family, either platform).
BENIGN_NOISE_RX = re.compile(
    r"^(?:warning: unable to access '[^']*': (?:Operation not permitted|Permission denied|Read-only file system)"
    r"|mise\b.*(?:WARN|warn|Operation not permitted|Permission denied|Read-only file system).*"
    r"|.*\bmise\b.*(?:Operation not permitted|Permission denied|Read-only file system).*)$", re.I)


def strip_benign_grade_noise(out):
    return "\n".join(l for l in (out or "").splitlines() if not BENIGN_NOISE_RX.match(l.strip()))


def scratch_root():
    return root() / ".concurrent-grader" / "scratch"


def _rmtree(p):
    subprocess.run(["chmod", "-R", "u+rwx", str(p)], capture_output=True)
    shutil.rmtree(p, ignore_errors=True)


def tasks_rel(p):
    try:
        return os.path.relpath(os.path.realpath(str(p)), os.path.realpath(str(tasks_dir())))
    except ValueError:
        return None


def grade_refs(task):
    """Paths under tasks/ (relative) that a task's grade script / setup / env name, plus its own dir. Used to (a) pick the sealed files
    to restore for THIS task and (b) whitelist reads in the grading sandbox."""
    tdir = Path(task["dir"])
    text = ""
    g = tdir / task.get("grade", "grade.sh")
    if task.get("grade") and g.exists():
        text += g.read_text(errors="replace")
    text += json.dumps({k: task.get(k) for k in ("setup", "env", "repo", "base_dir", "grade_ro", "grade_rw")}, default=str)
    home = re.escape(str(Path.home()))
    rx = re.compile(r"(?:\$\{?HOME\}?|%s)/bench/tasks/([A-Za-z0-9._@+-]+(?:/[A-Za-z0-9._@+-]+)*)" % home)
    td = tasks_dir()
    refs = []
    for m in rx.finditer(text):
        w = m.group(1)
        if (td / w).exists() and not (td / w).is_dir():
            w = os.path.dirname(w) or w
        refs.append(w)
    me = tasks_rel(tdir)
    if me and me != ".":
        refs.append(me)
    return sorted(set(refs))


def sealed_rels_for_task(task, limit=25):
    """Sealed paths (lines of sealed-paths.txt) needed to grade this task: task.json `sealed` (explicit list, relative to tasks/) else
    the ones at or below the task's own dir and the dirs its grade script names. Never 'everything'."""
    f = root() / "sealed-paths.txt"
    allr = [l.strip() for l in f.read_text().splitlines() if l.strip()] if f.exists() else []
    want = [w.strip("/") for w in (task.get("sealed") or grade_refs(task))]
    rels = [r for r in allr if any(r == w or r.startswith(w + "/") or w.startswith(r + "/") for w in want)]
    if len(rels) > limit:
        raise RuntimeError("task %s would restore %d sealed paths (limit %d); list the needed ones in task.json \"sealed\"" % (task["id"], len(rels), limit))
    return rels


def grade_sandbox_paths(task):
    """(extra_ro, extra_rw) for the grading sandbox: the task's dir, the top-level dir of everything its grader names (rails-_base, synthetic,
    ...), tools, toolchain homes that exist, plus task.json grade_ro / grade_rw. Sealed files of OTHER tasks are simply not on disk."""
    td = tasks_dir()
    ro = {str(Path(task["dir"]))}
    for w in grade_refs(task):
        ro.add(str(td / w.split("/")[0]))
    ro.add(str(H.tools_bin().parent))
    rw = set()
    ok = (lambda p: SB._sl().reachable(p)) if SB.LINUX else (lambda p: True)  # Linux: only what the sandbox user can reach (a 0700 runner home is not)
    for d in (".cargo", ".bundle", ".gem"):
        if (Path.home() / d).exists() and ok(str(Path.home() / d)):
            rw.add(str(Path.home() / d))  # Linux: bound as a per-grade private COPY (sandbox_linux.wrap_grade), not the shared dir
    if (Path.home() / ".rustup").exists() and ok(str(Path.home() / ".rustup")):
        ro.add(str(Path.home() / ".rustup"))
    ro |= {os.path.expanduser(x) for x in task.get("grade_ro", [])}
    rw |= {os.path.expanduser(x) for x in task.get("grade_rw", [])}
    return sorted(ro), sorted(rw)


def grade_task_dirs(task):
    """(dirs whose answer files are masked in the grade sandbox, sibling trees to cut). The top-level tasks/<id> of the family tasks
    (Beltway, tally, Trackline) is a thin wrapper that execs tasks/<family>/tasks/<id>/grade.sh: sealed/ (reference.patch, negative controls,
    src, validation records) lives THERE, so masking only task["dir"] left the task's own answers readable to contestant code at grade time."""
    dirs = {str(Path(task["dir"]))}
    cut = set()
    td = tasks_dir()
    for w in grade_refs(task):
        if "/tasks/" in w:
            dirs.add(str(td / w))
            cut.add(str(td / w.split("/tasks/")[0] / "tasks"))
    return sorted(dirs), sorted(cut)


def grade_sandbox_enabled():
    if SB.LINUX:
        return os.environ.get("BENCH_GRADE_SANDBOX", "1") != "0" and SB.enabled()
    return os.environ.get("BENCH_GRADE_SANDBOX", "1") != "0" and shutil.which("sandbox-exec") is not None


# a test run leaves a framework summary (Minitest, ExUnit, cargo) or the family verdict JSON; a crash at boot (LoadError in a preload of
# rails-_lib, a broken grader script) leaves none. Crash without summary + a stack frame in grader-owned code = grader/infra, never model.
TEST_SUMMARY_RX = re.compile(r"\d+ runs?, \d+ assertions?, \d+ failures?|\d+ tests?, \d+ failures?|Result: \d+(?:/\d+)? passed|test result: (?:ok|FAILED)\.|\"checks\"\s*:")
GRADER_TRACE_RX = re.compile(r"/bench/(?:\.concurrent-grader/grade-[^/]+/)?(?:tasks|rails|tools|runner)/[^\s:)]*\.(?:rb|ex|exs|py|sh|pl|rs):\d+")


_ZERO_RX = re.compile(r"(?<![\w.])0 (?:runs?|tests?|passed)\b|Result: 0(?:/0)? passed")


def tests_ran(out):
    """True when the test framework printed a summary in the last phase (Rails: after '== hidden checks' once that phase started) that
    counts at least one test: `0 runs, 0 assertions` / `Result: 0/0 passed` / `test result: ok. 0 passed` (an empty selection) is NOT
    evidence that anything was verified. Several summaries (Rust prints one per test binary): any non-empty one is enough."""
    seg = (out or "").split("== hidden checks")[-1]
    for line in seg.splitlines():
        if TEST_SUMMARY_RX.search(line) and (not _ZERO_RX.search(line) or "FAILED" in line):
            return True
    return False


def classify_grade(rc, out, timed_out, require_summary=True):
    """Verdict of one grade run. A pass needs exit 0 AND evidence that tests really ran (a framework summary or the family verdict JSON):
    a wrapper/grade script that exits 0 after a crash before the tests, an empty test selection or a swallowed failure is a grader error
    (infra, no model verdict), never a pass. Task opt-out: task.json "allow_no_summary": true."""
    if timed_out:
        return "timeout", "model", "grade wall-clock limit (process group killed)"
    if rc == 0:
        if require_summary and not tests_ran(out):
            return "grader_error", "infra", "grade exited 0 but printed no test summary/verdict line: tests did not run, not a pass"
        return "pass", "model", None
    # Apple's SDK-discovery cache failure is harmless: xcrun still returns
    # the installed SDK, and Cargo can replay cached warnings on real failures.
    out = re.sub(r"(?m)^\s*(?:= note:\s*)?xcrun: error: couldn't create cache file '/(?:private/)?var/folders/[^']*/xcrun_db-[^']*' \(errno=Operation not permitted\)\n?", "", out or "")
    out = strip_benign_grade_noise(out)
    if rc in (99, 126, 127) or GRADE_INFRA_RX.search(out or ""):
        return "grader_error", "infra", "grader/sandbox/setup failure (rc=%s), not a model verdict" % rc
    if not tests_ran(out) and GRADER_TRACE_RX.search(out or ""):
        return "grader_error", "infra", "test command crashed before any test ran, inside grader-owned code (no test summary/verdict line): not a model verdict"
    return "fail", "model", None


def run_grade(task, work, attempt_dir=None):
    """Run task grade.sh in the work dir (HOLDOUT env points at <task>/holdout). Not part of wall time.
    Sandboxed (sandbox.grade_profile): reads only the work dir, this task's dir + what its grader names (which, in a sealed grade window,
    includes ONLY this task's restored sealed files), toolchains; no network; TMPDIR is a private scratch dir that is deleted afterwards.
    A timeout kills the whole process group."""
    g = Path(task["dir"]) / task["grade"]
    scratch = scratch_root() / ("g-%d-%s" % (os.getpid(), LK.uuid.uuid4().hex[:8]))
    scratch.mkdir(parents=True, mode=0o700, exist_ok=True)
    os.chmod(scratch, 0o700)
    env = dict(os.environ, HOLDOUT=str(Path(task["dir"]) / "holdout"), TASK_DIR=task["dir"], TMPDIR=str(scratch), GRADEBOX="1")
    env.update(MISE_LOG_LEVEL="error", GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")
    env["PATH"] = str(Path(__file__).resolve().parent / "bin") + os.pathsep + env.get("PATH", "/usr/bin:/bin")
    if SB.LINUX:
        env["PATH"] = SB._sl().with_shim(env.get("PATH"))
    if task.get("_private_grade"):
        env["PATH"] = "/Library/Developer/CommandLineTools/usr/bin:" + env["PATH"]
        # A private workspace has only one builder; Mix TCP compilation locks
        # are redundant and incompatible with complete network isolation.
        env["MIX_OS_CONCURRENCY_LOCK"] = "0"
        env["XCRUN_NOCACHE"] = "1"
    argv = ["bash", str(g)]

    sb = {"mode": "off"}
    gkey = None
    if grade_sandbox_enabled():
        ro, rw = grade_sandbox_paths(task) if not task.get("_private_grade") else ([], [])
        ro.append(str(Path(__file__).resolve().parent / "bin" / "mktemp"))
        pf = (Path(attempt_dir) / "grade-sandbox.sb") if attempt_dir else scratch / "grade-sandbox.sb"
        if task.get("_private_grade"):
            argv = CG.profile(sys.modules[__name__], task, work, scratch, pf, argv)
        else:
            tdirs, cut = grade_task_dirs(task)
            argv = SB.wrap_grade(argv, work, pf, extra_ro=ro, extra_rw=rw, scratch=scratch, task_dir=tdirs, deny_other=cut, env=env,
                                 max_runtime=task.get("grade_timeout_s", 1800) + 120)
        gkey = str(pf)
        sb = {"mode": SB.backend(), "profile": str(pf), "network": "denied (IP and non-private Unix sockets)" if task.get("_private_grade") else "denied (loopback and unix sockets allowed)"}
    t0 = time.time()
    timed_out = False
    try:
        with open(scratch / ".out", "wb") as fh:
            proc = subprocess.Popen(argv, cwd=work, env=env, stdin=subprocess.DEVNULL, stdout=fh, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                rc = proc.wait(timeout=task.get("grade_timeout_s", 1800))
            except subprocess.TimeoutExpired:
                timed_out = True
                if gkey:
                    SB.kill(gkey)
                kill_group(proc)
                rc = 124
            except BaseException:
                if gkey:
                    SB.kill(gkey)
                kill_group(proc)
                reap_group(proc.pid)
                raise
            reap_group(proc.pid)
            if gkey:
                sb["teardown"] = SB.teardown(gkey)
        out = (scratch / ".out").read_bytes().decode(errors="replace")
        tail = out[-1500:] + ("\ngrade timeout" if timed_out else "")
    finally:
        _rmtree(scratch)
    outcome, kind, cause = classify_grade(rc, out, timed_out, require_summary=not task.get("allow_no_summary"))
    return {"pass": outcome == "pass", "rc": rc, "outcome": outcome, "kind": kind, "cause": cause, "wall_s": round(time.time() - t0, 3),
            "output_tail": tail, "tests_ran": tests_ran(out), "sandbox": sb}



# ------------------------------------------------------------------ run/grade lock + sealed answers
# Sealed answers live on the MacBook (tools/sealctl). They are copied back to ~/bench/tasks only while `bench grade` holds the
# EXCLUSIVE lock, i.e. while no benchmark process (which holds the SHARED lock for its whole life) exists. Then they are deleted again.
import contextlib
import fcntl
import subprocess as _sp


def sealed_on():
    return os.environ.get("BENCH_SEALED", "1") != "0" and (root() / "sealed-paths.txt").exists()


def sealctl(*args):
    p = root() / "tools" / "sealctl"
    if not p.exists():  # a machine without a sealed store (e.g. a qualification tree): nothing to purge; a restore cannot work
        return _sp.CompletedProcess(list(args), 0 if args and args[0] == "purge" else 127, "", "sealctl not installed")
    return _sp.run([str(p)] + list(args), capture_output=True, text=True)


def sealctl_purge():
    r = sealctl("purge")
    if r.stdout.strip():
        print(r.stdout.strip(), flush=True)
    return r


@contextlib.contextmanager
def run_lock(exclusive, private_grade=False):
    """Global exclusion between benchmark processes (shared flock, held for their whole life) and grade/validation windows (exclusive
    flock). flock is released by the kernel when the holder dies, so it never goes stale. On top of it, the window marker written by
    sealctl restore names the window owner (pid): a live owner blocks runs; a dead owner's leftovers are purged (stale-window handling)."""
    f = open(root() / ".run.lock", "a+")
    request = reader = None
    try:
        if exclusive:
            request = LK.WindowRequest(root()).acquire()
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                print("waiting for running benchmarks / another grade window to finish before grading (sealed answers only exist while none run)...", flush=True)
                fcntl.flock(f, fcntl.LOCK_EX)
            sealctl_purge()  # crash recovery: leftovers of an interrupted grade
        else:
            LK.shared_run_lock(f, root(), private_grade=private_grade)
            st = LK.window_state(root())
            if st and st[0] == "open":
                raise SystemExit("a grade window is open (%s); wait for it to finish" % LK.describe(st[1]))
            if st or (root() / ".sealed-restored").exists():
                print("stale grade window (owner is gone): purging its sealed files", flush=True)
                sealctl_purge()
                if (root() / ".sealed-restored").exists():
                    raise SystemExit("sealed answers are still restored on this machine; run tools/sealctl purge")
        if not exclusive and not private_grade:
            reader = LK.WindowRequest(root(), directory=".run-readers", kind="reader").acquire()
        yield
    finally:
        if reader is not None:
            reader.release()
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
        if request is not None:
            request.release()


@contextlib.contextmanager
def grade_window(rels):
    """Restore exactly `rels` (sealed paths, relative to tasks/), yield, purge immediately (also on error/signal). Caller holds run_lock(True)."""
    if not sealed_on() or not rels:
        yield
        return

    def _sig(signum, frame):
        raise KeyboardInterrupt()
    old = {s: signal.signal(s, _sig) for s in (signal.SIGTERM, signal.SIGHUP)}
    try:
        r = sealctl(*(["restore"] + [x for rel in rels for x in ("--rel", rel)]))
        if r.returncode:
            raise RuntimeError("cannot restore sealed files %s from the MacBook: %s" % (rels[:3], (r.stdout + r.stderr)[-300:]))
        yield
    finally:
        sealctl_purge()
        for s_, h_ in old.items():
            signal.signal(s_, h_)


# ------------------------------------------------------------------ one cell (with retries)

def status_cfg(opts):
    """Pause settings: opts (CLI flags / experiment file `status`) over env BENCH_STATUS_PAUSE / _RECHECK_S / _MAX_WAIT_S."""
    e = os.environ.get
    return {"pause": opts.get("status_pause", e("BENCH_STATUS_PAUSE", "1") not in ("0", "off", "false")),
            "recheck_s": float(opts.get("status_recheck_s") or e("BENCH_STATUS_RECHECK_S", "60")),
            "max_wait_s": float(opts.get("status_max_wait_s") or e("BENCH_STATUS_MAX_WAIT_S", "7200"))}


def run_cell(cell, exp, opts, abort=None):
    cell = dict(cell)
    cell["cell_id"] = cell_id(cell)
    cdir = results_dir() / exp / cell["cell_id"]
    mpath = cdir / "manifest.json"
    try:
        lock = LK.CellLock(cdir, "run").acquire()
    except LK.Busy as ex:
        print("cell %s is busy (%s); not started" % (cell["cell_id"], ex.owner), file=sys.stderr, flush=True)
        return {"cell_id": cell["cell_id"], "status": "locked", "errors": [str(ex)]}
    try:
        return _run_cell_locked(cell, exp, opts, abort, cdir, mpath)
    finally:
        lock.release()


def _run_cell_locked(cell, exp, opts, abort, cdir, mpath):
    if mpath.exists() and not opts.get("force"):
        old = json.loads(mpath.read_text())
        if old.get("status") in FINAL:
            return old
    task = load_task(cell["task"])
    prompt = task_prompt(task, cell.get("prompt"))
    ad = H.get(cell["harness"])
    # provider status: wait out an active major/partial incident on the relevant component (lane-level pause), then record the
    # start snapshot. All best-effort: an unreachable status page never blocks or fails a cell.
    targets = ST.targets_for(cell["harness"], cell.get("model")) if ST.enabled() else []
    pauses = ST.wait_for_clear(targets, status_cfg(opts), abort, log=lambda msg: print("%s [%s]" % (msg, cell["cell_id"]), file=sys.stderr, flush=True))
    try:
        status_start = ST.snapshot(targets) if targets else None
    except Exception as e:  # noqa: BLE001
        status_start = {"error": "%s: %s" % (type(e).__name__, e)}
    env, scrubbed = child_env(None)
    m = {
        "schema": SCHEMA, "experiment": exp, "cell_id": cell["cell_id"], "status": "running",
        "harness": cell["harness"],
        "requested": {"model": cell.get("model"), "effort": cell.get("effort"), "prompt_variant": cell.get("prompt") or "default",
                      "task": cell["task"], "rep": cell.get("rep", 1)},
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "cli_version": cli_version(cell["harness"], env),
        "adapter_verified": ad.verified,
        "wrapper": {"path": str(H.wrapper_path(cell["harness"])), "sha256": H.sha256_file(H.wrapper_path(cell["harness"])),
                    "isolation_flags": ad.isolation_flags_note, "env_scrubbed": scrubbed},
        "host": {"node": platform.node(), "platform": platform.platform(), "python": platform.python_version(),
                 "load_avg": os.getloadavg()[0], "concurrency": opts.get("jobs", 1)},
        "runner": {"timeout_s": resolve_timeout(cell, task, opts), "turn_cap": resolve_turn_cap(cell, task, opts)},
        "started_at": now(),
        "provider_status": {"targets": targets, "start": status_start, "pauses": pauses, "end": None},
    }
    write_json(mpath, m)
    max_attempts = 1 + int(opts.get("retries", 0))
    attempts, parsed = [], None
    for n in range(1, max_attempts + 1):
        rec, parsed = run_attempt(cell, exp, task, prompt, n, opts)
        attempts.append(rec)
        retryable = rec["status"] == "infra_error" and rec.get("error_class") in H.RETRYABLE_CLASSES
        if rec["status"] == "ok" or not retryable or n == max_attempts:
            break
        time.sleep(min(30, 5 * n))
    last = attempts[-1]
    m["ended_at"] = now()
    try:
        m["provider_status"]["end"] = ST.snapshot(targets) if targets else None
    except Exception as e:  # noqa: BLE001
        m["provider_status"]["end"] = {"error": "%s: %s" % (type(e).__name__, e)}
    m["status"] = last["status"]
    m["error_class"] = last.get("error_class")
    m["failure_kind"] = last.get("failure_kind")  # infra | model | None (ok)
    m["timeout"] = last.get("timeout")
    m["limits"] = last.get("limits")
    m["attempts"] = [{k: a.get(k) for k in ("n", "status", "error_class", "failure_kind", "exit_code", "wall_s", "timed_out", "errors")} for a in attempts]
    m["retries"] = len(attempts) - 1
    m["wall_s"] = last.get("wall_s")
    m["total_wall_s_all_attempts"] = round(sum(a.get("wall_s") or 0 for a in attempts), 3)
    m["exit"] = {"code": last.get("exit_code"), "signal": last.get("signal"), "timed_out": last.get("timed_out")}
    m["errors"] = last.get("errors", [])
    m["artifacts"] = {"dir": "attempt-%d" % last["n"], "transcript": "attempt-%d/transcript.jsonl" % last["n"],
                      "config": "attempt-%d/config.json" % last["n"], "patch": "attempt-%d/patch.diff" % last["n"]}
    m["workdir"] = last.get("workdir")
    m["diff"] = last.get("diff")
    m["timestamps"] = {"run_started_at": last.get("run_started_at"), "run_ended_at": last.get("run_ended_at")}
    if last.get("contamination") is not None:
        m["contamination"] = last["contamination"]  # egress log + transcript grep (egress.py); flag=True means review the transcript
    m["sandbox"] = last.get("sandbox")
    if "grade" in last:
        m["grade"] = last["grade"]
    if parsed:
        req = cell.get("model")
        obs = list(parsed["observed_models"])
        m["session_id"] = parsed["session_id"]
        m["observed"] = {
            "models": parsed["observed_models"], "model_source": parsed["observed_model_source"],
            "model_match": model_match(req, obs),
            "helper_models": [o for o in obs if model_match(req, [o]) is False] if model_match(req, obs) else [],
            "effort": parsed["observed_effort"], "effort_source": parsed["observed_effort_source"],
            "effort_match": None if not parsed["observed_effort"] or not cell.get("effort") else parsed["observed_effort"] == cell["effort"],
            "cli_version_reported": parsed["cli_version_reported"], "requested_model_echo": parsed["requested_model_echo"],
        }
        m["usage"] = parsed["usage"]
        m["cost_usd"] = parsed["cost_usd"]
        m["cost_source"] = parsed["cost_source"]
        m["num_turns"] = parsed["num_turns"]
        m["final_text_head"] = (parsed["final_text"] or "")[:300]
        m["retry_events"] = parsed["retry_events"]
        m["runtime_reported"] = parsed["runtime"]
        m["extra"] = parsed["extra"]
    write_json(mpath, m)
    if "grade" in m:
        RT.post_grade(sys.modules[__name__], mpath)
    if abort is not None and m["status"] == "infra_error" and m.get("error_class") == "rate_limit":
        acct = H.account_of(cell["harness"])
        if acct and hasattr(abort, "limited"):
            abort.limited.add(acct)   # per-account limit: only that ChatGPT account's harnesses stop
        else:
            abort.set()
    return m


# ------------------------------------------------------------------ experiments

def expand_cells(spec):
    """Matrix -> ordered cell list. Order is randomised per (rep, task) with a fixed seed so arms are
    interleaved (paired design; spreads provider load) but deterministic and resumable."""
    seed = spec.get("seed", 1)
    prompts = spec.get("prompts") or ["default"]
    cells = []
    for rep in range(1, int(spec.get("reps", 1)) + 1):
        for task in spec["tasks"]:
            group = [dict(a, prompt=p, task=task, rep=rep, timeout_s=a.get("timeout_s", spec.get("timeout_s")))
                     for a in spec["arms"] for p in prompts]
            random.Random("%s/%s/%s" % (seed, task, rep)).shuffle(group)
            cells += group
    return cells


class Abort(threading.Event):
    """Global stop flag plus the set of rate-limited ChatGPT accounts (a 429 on account A must not stop account B's cells)."""
    def __init__(self):
        super().__init__()
        self.limited = set()


def run_experiment(exp, cells, opts):
    abort = Abort()
    dead_harness = set()
    results = []

    def one(c):
        if abort.is_set() or c["harness"] in dead_harness or H.account_of(c["harness"]) in abort.limited:
            return {"cell_id": cell_id(c), "status": "not_run"}
        m = run_cell(c, exp, opts, abort)
        if m.get("status") == "infra_error" and m.get("error_class") == "auth":
            dead_harness.add(c["harness"])
        print("%-11s %s  %s" % (m["status"], m["cell_id"], ("wall=%ss" % m.get("wall_s")) if m.get("wall_s") else ""), flush=True)
        return m
    jobs = max(1, int(opts.get("jobs", 1)))
    if jobs == 1:
        for c in cells:
            results.append(one(c))
    else:
        with ThreadPoolExecutor(jobs) as ex:
            results = list(ex.map(one, cells))
    if abort.limited:
        print("RATE-LIMITED account(s) %s: their remaining cells were not run. Re-run to resume." % ", ".join(sorted(abort.limited)), file=sys.stderr)
    if abort.is_set():
        print("ABORTED on first rate-limit (429): remaining cells not run. Re-run to resume.", file=sys.stderr)
    return results


def cmd_run(a):
    def _night_term(signum, frame):  # night 2026-10-01 termfix
        raise KeyboardInterrupt()
    for _s in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(_s, _night_term)
    if a.experiment_file:
        spec = json.loads(Path(a.experiment_file).read_text())
        exp = spec.get("name") or Path(a.experiment_file).stem
        cells = expand_cells(spec)
        opts = {"timeout_s": spec.get("timeout_s"), "retries": spec.get("retries", 0), "extra_args": spec.get("extra_args", {}),
                "max_turns": spec.get("max_turns")}
        sp = spec.get("status") or {}  # {"pause": true, "recheck_s": 60, "max_wait_s": 7200}
        for k, v in sp.items():
            opts["status_" + k] = v
    else:
        if not (a.harness and a.task):
            raise SystemExit("give an experiment file, or --harness and --task (and --name)")
        exp = a.name or "adhoc"
        cells = [{"harness": a.harness, "model": a.model, "effort": a.effort, "prompt": a.prompt, "task": a.task, "rep": a.rep}]
        opts = {"retries": 0, "extra_args": {}}
    for k in ("timeout", "retries"):
        if getattr(a, k) is not None:
            opts["timeout_s" if k == "timeout" else k] = getattr(a, k)
    if a.timeout is not None:
        opts["timeout_override"] = a.timeout  # beats cell/task/experiment values (resolve_timeout)
    if getattr(a, "max_turns", None) is not None:
        opts["max_turns_override"] = a.max_turns
    if a.no_status_pause:
        opts["status_pause"] = False
    for k in ("status_recheck_s", "status_max_wait_s"):
        if getattr(a, k) is not None:
            opts[k] = getattr(a, k)
    opts.update(jobs=a.jobs, force=a.force, grade=a.grade, cleanup=a.cleanup, no_config_probe=a.no_config_probe)
    if a.only:
        cells = [c for c in cells if a.only in cell_id(c)]
    if not getattr(a, "include_quarantined", False):
        skipped = sorted({c["task"] for c in cells if quarantine_reason(c["task"])})
        if skipped:
            cells = [c for c in cells if c["task"] not in skipped]
            print("skipping quarantined task(s) (use --include-quarantined to run): " + ", ".join(skipped))
    if a.dry_run:
        for c in cells:
            print(cell_id(c))
        print("%d cells" % len(cells))
        return 0
    write_json(results_dir() / exp / "experiment.json", {"name": exp, "created_at": now(), "cells": [cell_id(c) for c in cells], "opts": opts})
    if sealed_on() and not SB.enabled():
        raise SystemExit("sealed benchmark runs require the contestant sandbox")
    with run_lock(False):
        res = run_experiment(exp, cells, opts)
    if a.grade and sealed_on():
        cmd_grade(argparse.Namespace(experiment=exp, force=False))
    bad = [r for r in res if r["status"] != "ok"]
    infra = [r for r in bad if r.get("failure_kind") == "infra"]
    print("%d cells, %d ok, %d not ok%s" % (len(res), len(res) - len(bad), len(bad), (" (%d infra, not model failures)" % len(infra)) if infra else ""))
    return 0 if not bad else 1


# ------------------------------------------------------------------ grade / table

def cmd_grade(a):
    """Grade in private task/work/temp trees concurrently with sandboxed contestants.
    Shared global lock excludes legacy windows; per-task/cell locks and CPU slots
    serialize grading. Unsealed fixture roots retain the legacy path."""
    if sealed_on() and not SB.LINUX:
        def interrupted(signum, frame):
            raise KeyboardInterrupt()
        old = {sig: signal.signal(sig, interrupted) for sig in (signal.SIGTERM, signal.SIGHUP)}
        try:
            with run_lock(False, private_grade=True):
                return _grade_all(a, private=True)
        finally:
            for sig, handler in old.items():
                signal.signal(sig, handler)
    with run_lock(True):
        return _grade_all(a)


def _grade_all(a, private=False):
    groups = {}
    for mp in sorted((results_dir() / a.experiment).glob("*/manifest.json")):
        if getattr(a, "cell", None) and mp.parent.name != a.cell:
            continue
        m = json.loads(mp.read_text())
        if m.get("status") not in ("ok", "error", "timeout"):
            continue
        task = load_task(m["requested"]["task"])
        work = mp.parent / m["artifacts"]["dir"] / "work"
        if not task.get("grade") or not work.exists() or ("grade" in m and not a.force):
            continue
        groups.setdefault(m["requested"]["task"], []).append((mp, m, task, work))
    for tid, items in groups.items():
        task = items[0][2]
        with contextlib.ExitStack() as stack:
            try:
                rels = sealed_rels_for_task(task) if sealed_on() else []
                if private:
                    wait_s = stack.enter_context(CG.capacity(sys.modules[__name__], tid))
                    private_task = stack.enter_context(CG.task_tree(sys.modules[__name__], task, rels))
                else:
                    stack.enter_context(grade_window(rels))
            except Exception as ex:  # noqa: BLE001
                for mp, m, _, _ in items:
                    with LK.CellLock(mp.parent, "grade"):
                        m = json.loads(mp.read_text())
                        if "grade" in m and not a.force:
                            continue
                        m["grade"] = {"pass": False, "rc": None, "outcome": "restore_failed", "kind": "infra", "cause": str(ex)[:300], "output_tail": ""}
                        write_json(mp, m)
                        print(m["cell_id"], "INFRA (no sealed files: %s)" % str(ex)[:120])
                continue
            for mp, m, task, work in items:
                try:
                    with LK.CellLock(mp.parent, "grade"):
                        m = json.loads(mp.read_text())
                        if "grade" in m and not a.force:
                            continue
                        adir = mp.parent / m["artifacts"]["dir"]
                        m["grade"] = CG.grade(sys.modules[__name__], private_task, work, adir) if private else run_grade(task, work, adir)
                        if private:
                            m["grade"]["queue_wait_s"] = wait_s
                        m["grade"]["sealed_restored"] = rels
                        write_json(mp, m)
                        RT.post_grade(sys.modules[__name__], mp)
                        gv = grade_view(m["grade"])
                        print(m["cell_id"], "PASS" if gv["pass"] else ("INFRA/%s" % gv["outcome"] if gv["kind"] == "infra" else "FAIL/%s" % gv["outcome"]), flush=True)
                except LK.Busy as ex:
                    print(m["cell_id"], "SKIPPED (cell busy: %s)" % ex.owner)
    return 0


def cmd_window(a):
    """`bench window [--rel PATH ...] [--all] -- CMD ...`: run a validation/authoring command inside a sealed window. Exclusive lock, only the
    named sealed paths restored (default: --rel required; --all = the whole grading set), TMPDIR pointed at a private scratch dir that is
    deleted afterwards, purge (incl. residue sweep of shared temp dirs) when the command ends. Replaces the per-family grade_window.py."""
    cmd = list(a.cmd)
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        raise SystemExit("bench window [--rel PATH ...|--all] -- COMMAND ...")
    if not (a.rel or a.all):
        raise SystemExit("name what to restore with --rel PATH (relative to tasks/, repeatable) or --all")
    scratch = scratch_root() / ("w-%d-%s" % (os.getpid(), LK.uuid.uuid4().hex[:8]))
    with run_lock(True):
        scratch.mkdir(parents=True, mode=0o700, exist_ok=True)
        os.chmod(scratch, 0o700)
        try:
            if sealed_on():
                r = sealctl(*(["restore", "--all"] if a.all else ["restore"] + [x for rel in a.rel for x in ("--rel", rel)]))
                if r.returncode:
                    raise SystemExit("cannot restore: %s" % (r.stdout + r.stderr)[-300:])
            try:
                return subprocess.run(cmd, env=dict(os.environ, TMPDIR=str(scratch), BENCH_WINDOW_SCRATCH=str(scratch))).returncode
            finally:
                _rmtree(scratch)
        finally:
            sealctl_purge()


def load_manifests(exps):
    out = []
    for e in exps:
        p = Path(e)
        d = p if p.is_dir() else results_dir() / e
        for mp in sorted(d.glob("*/manifest.json")):
            try:
                out.append(json.loads(mp.read_text()))
            except ValueError:
                pass
    return out


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def fmt(v, nd=0):
    if v is None:
        return "-"
    return ("%.*f" % (nd, v)) if isinstance(v, float) else str(int(v)) if isinstance(v, int) else str(v)


def flag_incidents(ms, use_network=True):
    """{cell_id/experiment key -> [incident refs]} for runs overlapping a provider incident. Incident history is fetched now
    (one request per provider), so incidents opened after the run are caught too; snapshots stored in the manifest add
    what was already open at start/end."""
    hist, errs = {}, {}
    if use_network and ST.enabled():
        provs = {t["provider"] for m in ms for t in ST.targets_for(m.get("harness"), (m.get("requested") or {}).get("model"))}
        for p in sorted(provs):
            h, err = ST.history(p)
            if h is not None:
                hist[p] = h
            elif err and err != "no history endpoint":
                errs[p] = err
    return {id(m): ST.overlaps(m, hist) for m in ms}, errs


def cell_kind(m):
    """infra | model | None for a manifest; older manifests without failure_kind are classified from status/error_class."""
    if "failure_kind" in m:
        return m["failure_kind"]
    return H.failure_kind(m.get("status"), m.get("error_class"))


def grade_view(g):
    """Normalised grade record: {pass, outcome, kind}. kind 'infra' = grader error / sandbox denial / restore failure (no model verdict)."""
    out = g.get("outcome") or ("pass" if g.get("pass") else ("timeout" if g.get("rc") == 124 else "fail"))
    kind = g.get("kind") or ("infra" if out in ("grader_error", "infra", "restore_failed") else "model")
    return {"pass": bool(g.get("pass")), "outcome": out, "kind": kind}


def summarise(ms, by, flags=None):
    groups = {}
    for m in ms:
        r = m.get("requested", {})
        key = tuple({"harness": m.get("harness"), "model": r.get("model"), "effort": r.get("effort"),
                     "prompt": r.get("prompt_variant"), "task": r.get("task")}[k] for k in by)
        groups.setdefault(key, []).append(m)
    rows = []
    for key, g in sorted(groups.items(), key=lambda kv: tuple(str(x) for x in kv[0])):
        u = lambda k: [ (x.get("usage") or {}).get(k) for x in g]  # noqa: E731
        gr = [grade_view(x["grade"]) for x in g if "grade" in x]
        graded = [v["pass"] for v in gr if v["kind"] != "infra"]  # grader/sandbox/restore failures are not model verdicts
        costs = [x.get("cost_usd") for x in g if x.get("cost_usd") is not None]
        rows.append(list(key) + [
            len(g), sum(x["status"] == "ok" for x in g),
            sum(x["status"] == "timeout" for x in g), sum(cell_kind(x) == "model" and x["status"] == "error" for x in g),
            sum(cell_kind(x) == "infra" for x in g) + sum(v["kind"] == "infra" for v in gr),
            ("%d/%d" % (sum(graded), len(graded))) if graded else "-",
            fmt(med([x.get("wall_s") for x in g]), 1), fmt(med(u("input"))), fmt(med(u("cached_input"))), fmt(med(u("output"))),
            fmt(med(u("reasoning"))), fmt(round(sum(costs), 4) if costs else None, 4),
            sum(1 for x in g if (x.get("observed") or {}).get("model_match") is False),
            sum(x.get("retries", 0) for x in g),
            sum(1 for x in g if (x.get("contamination") or {}).get("flag"))]
            + ([sum(1 for x in g if flags.get(id(x)))] if flags is not None else []))
    head = list(by) + ["n", "ok", "timeout", "err_model", "infra", "graded", "wall_med_s", "in_med", "cache_med", "out_med", "reas_med", "cost_usd_sum", "model_mismatch", "retries"] + ["contam"] + (["incident"] if flags is not None else [])
    return head, rows


def cmd_table(a):
    ms = load_manifests(a.experiments)
    if not ms:
        print("no manifests found")
        return 1
    qlines = quarantine_report(ms)
    ms = [m for m in ms if not quarantine_reason((m.get("requested") or {}).get("task") or "")]
    if not ms:
        print("\n".join(qlines) or "no manifests found")
        return 1
    flags, errs = flag_incidents(ms, not a.no_status)
    head, rows = summarise(ms, a.by.split(","), flags)
    if a.csv:
        w = csv.writer(sys.stdout)
        w.writerow(head)
        w.writerows(rows)
        for ql in qlines:
            print("# " + ql)
        return 0
    cols = [head] + [[str(x) if x is not None else "-" for x in r] for r in rows]
    widths = [max(len(c[i]) for c in cols) for i in range(len(head))]
    for c in cols:
        print("  ".join(v.ljust(widths[i]) for i, v in enumerate(c)))
    if qlines:
        print()
        for ql in qlines:
            print(ql)
    hit = [(m, f) for m in ms for f in [flags.get(id(m))] if f]
    if hit:
        print("\nruns overlapping a provider incident (column `incident` = number of such runs; treat their timings/failures as suspect):")
        for m, f in hit:
            print("  %s/%s  %s" % (m.get("experiment"), m.get("cell_id"), "; ".join("%s [%s] %s (%s)" % (i["provider"], i["impact"], i["name"], i["source"]) for i in f)))
    if errs:
        print("\nincident history unavailable: " + ", ".join("%s (%s)" % kv for kv in errs.items()))
    print("\nN is small: report only large effects (~20 pts pass rate, ~30% time/quota); token 'in' = fresh input, cache = cache-read; "
          "cost is API-equivalent where reported, not subscription billing.")
    return 0


# ------------------------------------------------------------------ auth / probe

def cmd_status(a):
    hm = None
    if a.models:
        hm = [tuple(x.split(":", 1)) if ":" in x else (x, None) for x in a.models.split(",")]
    elif a.matrix:
        hm = [(h, s.get("model")) for h, specs in DEFAULT_PROBE.items() for s in specs]
    if a.json:
        keys = list(dict.fromkeys(t["provider"] for x in hm for t in ST.targets_for(*x))) if hm else list(ST.PROVIDERS)
        print(json.dumps({k: ST.fetch_provider(k, True) for k in keys}, indent=2))
        return 0
    print("\n".join(ST.status_lines(hm)))
    return 0


def cmd_auth(a):
    for h in H.ADAPTERS:
        st, d = H.auth_state(h)
        print("%-9s %-14s %s" % (h, st, d))
    return 0


DEFAULT_PROBE = {
    "claude": [{"model": "claude-sonnet-5-5", "effort": "low"}, {"model": "claude-opus-5-5", "effort": "low"}],
    "codex": [{"model": m, "effort": "low"} for m in ("gpt-6-sol", "gpt-6-luna", "gpt-6-astra")],
    "pi": [{"model": "openai-codex/" + m, "effort": "low"} for m in ("gpt-6-sol", "gpt-6-luna", "gpt-6-astra")]
          + [{"model": "xai/grok-4.7", "effort": "low"}, {"model": "opencode-go/kimi-k3", "effort": "low"}],
    "kh": [{"model": "opencode-go/" + m, "effort": "low"} for m in ("gpt-6-luna", "grok-4.7", "kimi-k3", "deepseek-v4-pro")],
    "khr": [{"model": "opencode-go/" + m, "effort": "low"} for m in ("gpt-6-luna", "grok-4.7", "kimi-k3", "deepseek-v4-pro")],
    "opencode": [{"model": "openai/" + m, "effort": "low"} for m in ("gpt-6-sol", "gpt-6-luna", "gpt-6-astra")]
                + [{"model": "xai/grok-4.7", "effort": "low"}, {"model": "opencode-go/kimi-k3", "effort": "low"}],
    "grok": [{"model": "default", "effort": "low"}, {"model": "grok-4.7", "effort": "low"}],
    "gemini": [{"model": "default"}],
    "copilot": [{"model": "default", "effort": "low"}],
    # cursor: retired (subscription cancelled 2026-09-29), not probed
}


def observability(m):
    o = m.get("observed") or {}
    u = m.get("usage") or {}
    models = list(o.get("models") or {})
    return {
        "harness": m["harness"], "model": m["requested"]["model"], "effort": m["requested"]["effort"], "status": m["status"],
        "served_model": ",".join(models) or None, "served_model_source": o.get("model_source"), "model_match": o.get("model_match"),
        "usage_reported": m["status"] == "ok" and any(v is not None for v in u.values()),
        "usage": {k: v for k, v in u.items() if v is not None}, "cached_reported": u.get("cached_input") is not None,
        "reasoning_reported": u.get("reasoning") is not None,
        "cost_usd": m.get("cost_usd"), "cost_source": m.get("cost_source"),
        "effort_echo": o.get("effort"), "effort_source": o.get("effort_source"),
        "session_id": bool(m.get("session_id")), "cli_version": m.get("cli_version"),
        "allowance_pct": (m.get("extra") or {}).get("allowance_used_percent_last"),
        "answer_ok": (m.get("final_text_head") or "").strip().strip(".").upper() == "OK",
        "wall_s": m.get("wall_s"), "error": (m.get("errors") or [None])[0] if m["status"] != "ok" else None,
    }


def probe_table(rows):
    def yn(v):
        return "yes" if v else "no"
    head = ["harness", "model", "effort", "status", "served model (source)", "usage", "cache", "reason", "cost", "effort echo", "sess", "ok"]
    out = [head]
    for r in rows:
        out.append([r["harness"], r["model"] or "-", r["effort"] or "-", r["status"],
                    ("%s (%s)" % (r["served_model"], r["served_model_source"])) if r["served_model"] else "none",
                    yn(r["usage_reported"]), yn(r["cached_reported"]), yn(r["reasoning_reported"]),
                    ("%s" % r["cost_usd"]) if r["cost_usd"] is not None else "none",
                    ("%s (%s)" % (r["effort_echo"], r["effort_source"])) if r["effort_echo"] else "none",
                    yn(r["session_id"]), yn(r["answer_ok"])])
    w = [max(len(str(c[i])) for c in out) for i in range(len(head))]
    return "\n".join("  ".join(str(v).ljust(w[i]) for i, v in enumerate(c)) for c in out)


def cmd_probe(a):
    with run_lock(False):
        return _cmd_probe(a)


def _cmd_probe(a):
    matrix = json.loads(Path(a.models).read_text()) if a.models else DEFAULT_PROBE
    want = a.harness.split(",") if a.harness else list(matrix)
    exp = "_probe-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    rows, skipped = [], []
    for h in want:
        st, detail = H.auth_state(h)
        if st != "logged_in" and not a.include_not_logged_in:
            skipped.append({"harness": h, "auth": st, "detail": detail})
            print("SKIP %-9s %s (%s)" % (h, st, detail))
            continue
        for spec in matrix.get(h, []):
            cell = dict(spec, harness=h, task="_probe", prompt="default", rep=1, timeout_s=a.timeout)
            m = run_cell(cell, exp, {"retries": 0, "timeout_s": a.timeout, "force": True, "status_pause": False}, None)
            rows.append(observability(m))
            print("%-11s %s/%s" % (m["status"], h, spec.get("model")), flush=True)
    res = {"experiment": exp, "created_at": now(), "prompt": "Reply with the single word OK.", "rows": rows, "skipped": skipped}
    write_json(results_dir() / exp / "probe.json", res)
    table = probe_table(rows)
    (results_dir() / exp / "probe.txt").write_text(table + "\n")
    print("\n" + table)
    if skipped:
        print("\nnot probed (not logged in / unknown): " + ", ".join("%s[%s]" % (s["harness"], s["auth"]) for s in skipped))
    print("\nresults: %s" % (results_dir() / exp))
    return 0


# ------------------------------------------------------------------ main

def main(argv=None):
    ap = argparse.ArgumentParser(prog="bench", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run an experiment file, or one cell")
    r.add_argument("experiment_file", nargs="?")
    r.add_argument("--name")
    r.add_argument("--harness")
    r.add_argument("--model")
    r.add_argument("--effort")
    r.add_argument("--prompt", default="default")
    r.add_argument("--task")
    r.add_argument("--rep", type=int, default=1)
    r.add_argument("--timeout", type=int, help="seconds per cell (default 1800)")
    r.add_argument("--retries", type=int, help="extra attempts on network/provider-stream/workdir/spawn infra errors only")
    r.add_argument("--max-turns", type=int, help="turn cap, passed to harnesses that have one (kh, khr, kh-cc, grok); recorded as unsupported for the others")
    r.add_argument("--jobs", type=int, default=1, help="parallel cells; wall times are only comparable at equal concurrency")
    r.add_argument("--force", action="store_true", help="re-run cells that already have a final manifest")
    r.add_argument("--grade", action="store_true", help="run task grade.sh right after each cell (excluded from wall time)")
    r.add_argument("--cleanup", action="store_true", help="delete the work dir after capturing patch.diff")
    r.add_argument("--only", help="substring filter on cell id")
    r.add_argument("--include-quarantined", action="store_true", help="also run tasks marked \"quarantined\" in task.json (skipped by default; never scored)")
    r.add_argument("--dry-run", action="store_true")
    r.add_argument("--no-status-pause", action="store_true", help="do not wait for provider incidents before starting a cell (status is still recorded)")
    r.add_argument("--status-recheck-s", type=float, help="seconds between status rechecks while paused (default 60, env BENCH_STATUS_RECHECK_S)")
    r.add_argument("--status-max-wait-s", type=float, help="give up waiting after this many seconds and start anyway (default 7200)")
    r.add_argument("--no-config-probe", action="store_true", help="skip the per-cell `mcp list`-style config commands")
    r.set_defaults(fn=cmd_run)
    t = sub.add_parser("table", help="summarise results")
    t.add_argument("experiments", nargs="+")
    t.add_argument("--by", default="harness,model,effort,prompt")
    t.add_argument("--csv", action="store_true")
    t.add_argument("--no-status", action="store_true", help="offline: skip fetching incident history (only manifest snapshots are used)")
    t.set_defaults(fn=cmd_table)
    g = sub.add_parser("grade", help="run grade.sh for finished cells")
    g.add_argument("experiment")
    g.add_argument("--cell", help="grade only this finished cell directory")
    g.add_argument("--force", action="store_true")
    g.set_defaults(fn=cmd_grade)
    w = sub.add_parser("window", help="run a validation command inside a sealed window (restore named paths, private TMPDIR, purge + temp sweep)")
    w.add_argument("--rel", action="append", help="sealed path relative to tasks/ (repeatable)")
    w.add_argument("--all", action="store_true", help="restore the whole grading set")
    w.add_argument("cmd", nargs=argparse.REMAINDER)
    w.set_defaults(fn=cmd_window)
    p = sub.add_parser("probe", help="tiny observability probe per logged-in harness x model")
    p.add_argument("--harness", help="comma list (default: all in matrix; logged-out ones are skipped)")
    p.add_argument("--models", help="JSON {harness: [{model, effort}]} overriding the default matrix")
    p.add_argument("--timeout", type=int, default=180)
    p.add_argument("--include-not-logged-in", action="store_true", help="probe even if auth state is not logged_in (e.g. keychain login invisible over SSH)")
    p.set_defaults(fn=cmd_probe)
    s = sub.add_parser("status", help="current provider status (Statuspage JSON); no model calls")
    s.add_argument("--matrix", action="store_true", help="only the providers/components our default probe matrix uses")
    s.add_argument("--models", help="comma list of harness:model to narrow to, e.g. codex:gpt-6-sol,claude:claude-opus-5-5")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_status)
    au = sub.add_parser("auth", help="show login state per harness (no secrets)")
    au.set_defaults(fn=cmd_auth)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
