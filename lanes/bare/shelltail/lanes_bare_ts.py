#!/usr/bin/env python3
"""lanes-bare: head-to-head cells for Kogen's loop, Codex CLI, Claude Code, Pi and OpenCode on the same task, graded by the lanes grader.

One cell = one task, one repetition, one arm. Arms:
  kogen   `kogen intent build` (the native loop; with the supplied Intent, exactly as lanes-cell does it)
  codex   `codex exec` (non-interactive, sandbox workspace-write, approvals never)
  claude  `claude -p` (bypass permissions, tools limited to the workspace tools, no web)
  pi      `pi -p --mode json` (isolated agent dir, OpenAI Codex subscription provider)
  opencode `opencode run --format json` (isolated config dir, ChatGPT OAuth provider)

The bare arms get one prompt: the task's request, the supplied acceptance scenarios and the project's check commands.
Every arm runs in a fresh git workspace made from the task's `start/`, under a deadline in its own process group.
The hidden tests (`evaluator/`) are never copied into the workspace: the cell dir gets `final-tree.tar` (git archive
of HEAD) and `result.json`, and `lanes.grading.grade_cell` (the existing grader) writes `evaluation.json`.

  lanes_bare.py cell  --tasks DIR --task NAME --arm ARM --run-dir DIR [--rep 1] [--lane NAME] ...
  lanes_bare.py batch BATCH.json --run-dir DIR [--slots N] [--max-cells N]
  lanes_bare.py summary RUN_DIR
"""

import argparse
import concurrent.futures
import collections
import datetime
import glob
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
import tomllib

LANES_DIR = os.environ.get("LANES_DIR") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # default: this repo's lanes/
PRIVATE = os.environ.get("LANES_PRIVATE") or os.path.expanduser("~/lanes-work")  # private work dir (agent logins, live markers)
sys.path.insert(0, LANES_DIR)
from lanes import cell as lcell  # noqa: E402
from lanes import common, grading, usage  # noqa: E402

DEADLINE_S = 3600
SETUP_S = 600
IDENTITY = lcell.IDENTITY
# Secrets and routing variables no agent child inherits; each arm adds back only what it needs.
STRIP_PREFIXES = ("KOGEN_LANES_", "ANTHROPIC_", "OPENAI_", "CLAUDE_", "CODEX_", "AWS_", "GOOGLE_", "AZURE_")
STRIP_NAMES = {"GITHUB_TOKEN", "GH_TOKEN", "HF_TOKEN", "NPM_TOKEN", "SSH_AUTH_SOCK"}
LEAK = re.compile(r"(/evaluator/|evaluate\.toml|TestHidden|lanes-private|research-private|kogen-bench-research|\.lab-eval)")
LEAK_AGENT_BIN = re.compile(r"(?:research-private/)?lanes-private/agents/pi-auth/bin")
CLAUDE_TOOLS = "Bash,Read,Edit,Write,Glob,Grep"
EVENTS_CAP = 200 * 1024 * 1024
USAGE_TAIL_CAP = 2 * 1024 * 1024
CODEX_BIN_DEFAULT = "/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex"


class BareError(Exception):
    pass


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


# --- task inputs ----------------------------------------------------------------------------------------------

def load_task_inputs(task_dir, form):
    with open(os.path.join(task_dir, "task.toml"), "rb") as f:
        tt = tomllib.load(f)
    supplied = os.path.join(task_dir, "supplied", form)
    feature = os.path.join(supplied, "acceptance.feature")
    return tt, supplied, (open(feature, encoding="utf-8").read() if os.path.isfile(feature) else "")


def bare_acceptance_command(tt, feature_rel):
    """The task's acceptance command with Kogen's two variables resolved for an agent that runs it by hand."""
    acc = tt.get("acceptance")
    if not acc:
        return None
    cmd = re.sub(r"\s*--format\s+message:\$KOGEN_ACCEPTANCE_REPORT", "", acc["run"])
    return cmd.replace("$KOGEN_ACCEPTANCE_FEATURES", feature_rel)


def feature_path(tt):
    steps = (tt.get("acceptance") or {}).get("steps_dir") or "features/steps"
    return os.path.join(os.path.dirname(steps) or "features", "acceptance.feature")


def build_prompt(task_dir, form):
    tt, _, feature = load_task_inputs(task_dir, form)
    request = open(os.path.join(task_dir, "request.md"), encoding="utf-8").read().strip()
    checks = [f"- {c['name']}: `{c['run']}`" for c in tt.get("check") or []]
    acc = bare_acceptance_command(tt, feature_path(tt))
    if acc:
        checks.append(f"- acceptance (the scenarios above): `{acc}`")
    protect = tt.get("protect") or []
    parts = [
        "You are working in the git repository in the current directory. Make the change described below so that it is "
        "complete and correct. Your work is judged afterwards by tests you cannot see, so follow the specification "
        "exactly, including its edge cases and error messages.",
        "# Request\n\n" + request,
    ]
    if feature.strip():
        parts.append(f"# Acceptance scenarios\n\nThey are in `{feature_path(tt)}`; the step definitions are already in "
                     f"the repository.\n\n```gherkin\n{feature.strip()}\n```")
    parts.append("# Checks\n\nProject dependencies are already installed. Run these before you finish; the work is "
                 "done when they all pass:\n\n" + "\n".join(checks))
    if tt.get("fix"):
        parts[-1] += "\n\nFormatting fix command: " + ", ".join(f"`{c}`" for c in tt["fix"])
    if protect:
        parts.append("# Rules\n\nDo not change these paths: " + ", ".join(f"`{p}`" for p in protect) +
                     ". Work only inside this directory. There is no network and no documentation lookup.")
    else:
        parts.append("# Rules\n\nWork only inside this directory. There is no network and no documentation lookup.")
    return "\n\n".join(parts) + "\n"


# --- workspace --------------------------------------------------------------------------------------------------

def git(ws, *args, env=None, check=True):
    r = subprocess.run(["git", "-C", ws, *args], capture_output=True, text=True, env=env)
    if check and r.returncode:
        raise BareError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def make_bare_workspace(ws, tmp, task_dir, form, tt):
    """start/ plus the supplied step files and the acceptance feature, committed as `Start`. No `.kogen/`."""
    shutil.copytree(os.path.join(task_dir, "start"), ws, symlinks=True)
    supplied = os.path.join(task_dir, "supplied", form)
    for dirpath, _, names in os.walk(supplied):
        for name in names:
            src = os.path.join(dirpath, name)
            rel = os.path.relpath(src, supplied)
            if rel == "intent.md" or (os.sep not in rel and rel.startswith("model.")):
                continue
            dst = os.path.join(ws, feature_path(tt) if rel == "acceptance.feature" else rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
    env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
           "XDG_CONFIG_HOME": os.path.join(tmp, "xdg"),
           "GIT_AUTHOR_NAME": IDENTITY["name"], "GIT_AUTHOR_EMAIL": IDENTITY["email"],
           "GIT_COMMITTER_NAME": IDENTITY["name"], "GIT_COMMITTER_EMAIL": IDENTITY["email"],
           "GIT_AUTHOR_DATE": lcell.START_DATE, "GIT_COMMITTER_DATE": lcell.START_DATE}
    git(ws, "init", "-q", "--initial-branch=main", env=env)
    for key, value in (("user.name", IDENTITY["name"]), ("user.email", IDENTITY["email"]),
                       ("commit.gpgsign", "false"), ("core.hooksPath", os.devnull)):
        git(ws, "config", key, value)
    with open(os.path.join(ws, ".git", "info", "exclude"), "a") as f:  # agent byproducts stay out of the tree
        f.write("/.claude/\n/.codex/\n/.agents/\n/AGENTS.md.local\n")
    git(ws, "add", "-A", env=env)
    git(ws, "commit", "-q", "-m", "Start", env=env)
    return env


def agent_env(tt, tmp, extra):
    """The environment of a bare agent: toolchain variables, PATH, HOME, the task env, private TMPDIR and caches."""
    env = {k: v for k, v in os.environ.items()
           if (k in grading.GO_VARS or k.startswith(grading.ENV_PREFIXES) or k.startswith(("MISE_", "LANES_GUARD")))
           and not k.startswith(STRIP_PREFIXES)}
    env.update(HOME=os.environ.get("HOME", "/"), PATH=os.environ.get("PATH", "/usr/bin:/bin"),
               LANG=os.environ.get("LANG", "C.UTF-8"), GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
               GIT_TERMINAL_PROMPT="0", CLAUDE_CODE_DISABLE_SUBSTITUTION_RM_PROMPT="1")  # headless: no prompt ever (29 Oct)
    env.update({k: str(v) for k, v in (tt.get("env") or {}).items()})
    t = os.path.join(tmp, "agent-tmp")
    os.makedirs(os.path.join(t, "npm"), exist_ok=True)
    env.update(TMPDIR=t, npm_config_cache=os.path.join(t, "npm"), npm_config_update_notifier="false")
    env.update(extra or {})
    return env


def run_setup(ws, tt, env, out):
    t0 = time.monotonic()
    for line in tt.get("setup") or []:
        with open(os.path.join(out, "setup.txt"), "a") as log:
            code, timed_out = common.run(["sh", "-c", line], cwd=ws, env=env, deadline_s=SETUP_S,
                                         stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        if code or timed_out:
            raise BareError(f"setup failed ({'timeout' if timed_out else code}): {line}")
    return round(time.monotonic() - t0, 3)


def protected_restore(ws, task_dir, tt):
    """Restore protected paths from start/ (Kogen refuses writes to them); returns the paths that had changed."""
    changed = []
    for p in tt.get("protect") or []:
        src, dst = os.path.join(task_dir, "start", p), os.path.join(ws, p)
        if os.path.isfile(src):
            if not os.path.isfile(dst) or open(src, "rb").read() != open(dst, "rb").read():
                changed.append(p)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)
                shutil.copymode(src, dst)
        elif os.path.exists(dst):
            changed.append(p)
    return changed


def finish_tree(ws, out, env):
    """Commit whatever the agent left (the ignore files decide what counts), archive HEAD like lanes-cell."""
    git(ws, "add", "-A", env=env, check=False)
    git(ws, "commit", "-q", "-m", "Agent work", "--allow-empty", env=env, check=False)
    tree = git(ws, "rev-parse", "HEAD^{tree}")
    git(ws, "archive", "--format=tar", "-o", os.path.join(out, "final-tree.tar"), "HEAD")
    # the agent's change as text: survives pruning of final-tree.tar and lets reviewers adjudicate rounds (29 Oct)
    with open(os.path.join(out, "final.diff"), "w") as f:
        f.write(git(ws, "diff", "--binary", "HEAD~1", "HEAD", env=env, check=False) + "\n")
    return tree


# --- the bare agents --------------------------------------------------------------------------------------------

def read_token(home):
    """The Claude Code token Kogen stored in `<home>/.kogen/credentials/claude-code.json`; used in memory only."""
    path = os.path.join(home, ".kogen", "credentials", "claude-code.json")
    try:
        with open(path, encoding="utf-8") as f:
            tok = json.load(f).get("api_key")
    except (OSError, ValueError):
        tok = None
    if not tok:
        raise BareError(f"no stored Claude Code token in {path}")
    return tok


def claude_command(a, claude_bin):
    cmd = [claude_bin, "-p", "--output-format", "stream-json", "--verbose", "--permission-mode", "bypassPermissions",
           "--tools", CLAUDE_TOOLS, "--no-session-persistence", "--disable-slash-commands", "--strict-mcp-config",
           "--setting-sources", "project"]
    if a.model:
        cmd += ["--model", a.model]
    if a.effort:
        cmd += ["--effort", a.effort]
    return cmd


def codex_command(a, codex_bin):
    cmd = [codex_bin, "exec", "--json", "--ephemeral", "--ignore-user-config", "--ignore-rules", "-s", "workspace-write",
           "-c", 'approval_policy="never"', "-c", 'web_search="disabled"']
    if a.model:
        cmd += ["-m", a.model]
    if a.effort:
        cmd += ["-c", f'model_reasoning_effort="{a.effort}"']
    return cmd + ["-"]


def pi_command(a, pi_bin, prompt):
    cmd = [pi_bin, "--print", "--mode", "json", "--no-session", "--provider", "openai-codex",
           "--tools", "read,bash,edit,write,grep,find,ls"]
    if a.model:
        cmd += ["--model", a.model]
    if a.effort:
        cmd += ["--thinking", a.effort]
    return cmd + [prompt]


def opencode_command(a, opencode_bin, ws, prompt):
    cmd = [opencode_bin, "run", "--format", "json", "--auto", "--dir", ws]
    if a.model:
        cmd += ["--model", "openai/" + a.model]
    if a.effort:
        cmd += ["--variant", a.effort]
    return cmd + [prompt]


def parse_open_usage(path, source):
    """Normalize usage from Pi JSON events or OpenCode message.updated JSON events."""
    rec = {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "reasoning_tokens": 0,
           "requests": 0, "tool_calls": 0, "models": [], "errors": []}
    seen = False
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        lines = []
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        kind = e.get("type") or e.get("event")
        d = e.get("data") or e.get("properties") or e.get("message") or e
        if source == "pi":
            msg = d.get("message") or d
            u = msg.get("usage") or d.get("usage") or {}
            model = msg.get("model") or d.get("model")
            if kind in ("message_end", "agent_end", "turn.completed") and u:
                seen = True
                rec["requests"] += 1
                cache_read = u.get("cacheRead", u.get("cached_input_tokens", 0)) or 0
                cache_write = u.get("cacheWrite", u.get("cache_creation_input_tokens", 0)) or 0
                rec["input_tokens"] += (u.get("input", u.get("input_tokens", 0)) or 0) + cache_read + cache_write
                rec["cached_input_tokens"] += cache_read
                rec["cache_creation_input_tokens"] = rec.get("cache_creation_input_tokens", 0) + cache_write
                rec["output_tokens"] += u.get("output", u.get("output_tokens", 0)) or 0
                rec["reasoning_tokens"] += u.get("reasoning", u.get("reasoning_tokens", 0)) or 0
            if kind in ("tool_execution_end", "tool_call"):
                rec["tool_calls"] += 1
        else:
            info = d.get("info") or d
            u = info.get("tokens") or info.get("usage") or {}
            cache = u.get("cache") or {}
            model = info.get("model")
            # `opencode run --format json` emits the CLI event stream: usage is
            # on part.tokens for step_finish (input excludes cache reads).
            if kind == "step_finish" and (e.get("part") or {}).get("tokens"):
                u = e["part"]["tokens"]
                cache = u.get("cache") or {}
                seen = True
                rec["requests"] += 1
                cache_read = cache.get("read", 0) or 0
                cache_write = cache.get("write", 0) or 0
                rec["input_tokens"] += (u.get("input", 0) or 0) + cache_read + cache_write
                rec["cached_input_tokens"] += cache_read
                rec["cache_creation_input_tokens"] = rec.get("cache_creation_input_tokens", 0) + cache_write
                rec["output_tokens"] += u.get("output", 0) or 0
                rec["reasoning_tokens"] += u.get("reasoning", 0) or 0
            elif kind == "message.updated" and u:
                seen = True
                rec["requests"] += 1
                cache_read = cache.get("read", 0) or u.get("cached", 0) or 0
                rec["input_tokens"] += (u.get("input", 0) or 0) + cache_read
                rec["cached_input_tokens"] += cache_read
                rec["output_tokens"] += u.get("output", 0) or 0
                rec["reasoning_tokens"] += u.get("reasoning", 0) or 0
            if kind in ("tool", "tool_use"):
                rec["tool_calls"] += 1
            if kind == "session.error" or kind == "error":
                rec["errors"].append(str(d.get("error") or d.get("message") or "agent error")[:300])
        if model and model not in rec["models"]:
            rec["models"].append(model)
    if not seen:
        rec.update(input_tokens=None, cached_input_tokens=None, output_tokens=None, reasoning_tokens=None)
    return rec


def loop_task(a, ws, tmp, prompt, tt):
    return {"protocol": "kogen-loop/v1", "root": ws,
            "role": {"provider": getattr(a, "provider", None) or "chatgpt", "model": a.model, "effort": a.effort, "base_url": ""},
            "instructions": "You are a coding agent working in the supplied repository.", "prompt": prompt,
            "tools": ["read_file", "write_file", "list_files", "search_text", "shell"],
            "protected": tt.get("protect") or [], "excluded": [], "terminal": ["finish"],
            "deadline_seconds": a.deadline_s,
            "session": {"dir": os.path.join(tmp, "loop-session"), "resume": False}, "requires": []}


def parse_loop(path):
    rec = {"input_tokens": None, "cached_input_tokens": None, "output_tokens": None,
           "reasoning_tokens": None, "requests": 0, "tool_calls": 0, "models": [], "errors": []}
    usage_seen = False
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        return rec
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        kind = e.get("type")
        if kind == "session.started":
            role = e.get("role") or {}
            if role.get("model"):
                rec["models"] = [role["model"]]
        elif kind == "request.started":
            rec["requests"] += 1
        elif kind == "response":
            u = e.get("usage") or {}
            if u.get("input") is not None:
                rec["input_tokens"] = (rec["input_tokens"] or 0) + u["input"]
            if u.get("cached") is not None:
                rec["cached_input_tokens"] = (rec["cached_input_tokens"] or 0) + u["cached"]
            if u.get("output") is not None:
                rec["output_tokens"] = (rec["output_tokens"] or 0) + u["output"]
            if u.get("reasoning") is not None:
                rec["reasoning_tokens"] = (rec["reasoning_tokens"] or 0) + u["reasoning"]
            usage_seen = usage_seen or any(u.get(k) is not None for k in ("input", "cached", "output", "reasoning"))
        elif kind == "tool.call":
            rec["tool_calls"] += 1
        elif kind == "error":
            rec["errors"].append(str(e.get("detail") or e.get("reason") or e.get("class"))[:300])
    if not usage_seen:
        rec.update(input_tokens=None, cached_input_tokens=None, output_tokens=None, reasoning_tokens=None)
    return rec


def parse_claude(path):
    """Tokens and counts from a `stream-json` transcript."""
    rec = {"input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "reasoning_tokens": None,
           "requests": None, "tool_calls": 0, "models": [], "client_cost_usd": None, "errors": []}
    last = None
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        return rec
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") == "assistant":
            for blk in (e.get("message") or {}).get("content") or []:
                if blk.get("type") == "tool_use":
                    rec["tool_calls"] += 1
        if e.get("type") == "result":
            last = e
    if last:
        u = last.get("usage") or {}
        cache_r, cache_w = u.get("cache_read_input_tokens") or 0, u.get("cache_creation_input_tokens") or 0
        rec.update(input_tokens=(u.get("input_tokens") or 0) + cache_r + cache_w, cached_input_tokens=cache_r,
                   cache_creation_input_tokens=cache_w, output_tokens=u.get("output_tokens"),
                   requests=last.get("num_turns"), client_cost_usd=last.get("total_cost_usd"),
                   models=sorted((last.get("modelUsage") or {}).keys()), result_subtype=last.get("subtype"))
        if last.get("is_error"):
            rec["errors"].append(str(last.get("result"))[:300])
    return rec


def parse_codex(path):
    rec = {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "reasoning_tokens": 0, "requests": 0,
           "tool_calls": 0, "models": [], "errors": []}
    seen = False
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        return {**rec, "input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "reasoning_tokens": None}
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        kind = e.get("type")
        if kind == "turn.completed":
            u = e.get("usage") or {}
            seen = True
            rec["requests"] += 1
            rec["input_tokens"] += u.get("input_tokens") or 0
            rec["cached_input_tokens"] += u.get("cached_input_tokens") or 0
            rec["output_tokens"] += u.get("output_tokens") or 0
            rec["reasoning_tokens"] += u.get("reasoning_output_tokens") or 0
        elif kind in ("item.completed", "item.started"):
            item = e.get("item") or {}
            if kind == "item.completed" and item.get("type") in ("command_execution", "file_change", "mcp_tool_call"):
                rec["tool_calls"] += 1
        elif kind == "turn.failed" or (kind == "error" and not str(e.get("message")).startswith("Reconnecting")):
            rec["errors"].append(str(e.get("message") or e.get("error"))[:300])
    if not seen:
        rec.update(input_tokens=None, cached_input_tokens=None, output_tokens=None, reasoning_tokens=None)
    return rec


def price(rec):
    """`cost_usd`, `cost_reason` from the lanes price table for a token record (cache writes priced as input)."""
    model = (rec.get("models") or [None])[0]
    try:
        usd, why = usage.request_cost(model, {k: rec.get(k) for k in ("input_tokens", "cached_input_tokens", "output_tokens")})
    except Exception as e:  # a missing table or an odd model name must not lose the cell
        return None, f"price error: {type(e).__name__}"
    return (None if usd is None else round(usd, 8)), why


def filtered_agent_run(cmd, cwd, env, deadline_s, events_path, stderr, stdin, arm, out):
    """Drain child stdout on a reader thread, filtering Pi deltas and capping the saved transcript."""
    sidecar = os.path.join(out, "usage-events.jsonl")
    tail = collections.deque()
    tail_size = 0
    state = {"size": 0, "capped": False}
    usage_types = {"message_end", "agent_end", "turn.completed", "step_finish", "message.updated",
                   "result", "response"}

    def reader(pipe):
        nonlocal tail_size
        with open(events_path, "wb") as saved, open(os.path.join(out, "events-arrival.jsonl"), "w") as arr:
            for n, line in enumerate(iter(pipe.readline, b"")):
                arr.write(json.dumps({"i": n, "t": now(), "m": round(time.monotonic(), 3)}) + "\n")
                arr.flush()
                keep = True
                try:
                    event = json.loads(line)
                    kind = event.get("type") or event.get("event")
                    if arm == "pi" and (kind == "message_update" or kind == "tool_execution_update"):
                        keep = False
                    if kind in usage_types:
                        tail.append(line)
                        tail_size += len(line)
                        while tail_size > USAGE_TAIL_CAP and tail:
                            tail_size -= len(tail.popleft())
                except (ValueError, TypeError):
                    pass
                if keep and not state["capped"]:
                    if state["size"] + len(line) > EVENTS_CAP:
                        state["capped"] = True
                    else:
                        saved.write(line)
                        state["size"] += len(line)
            pipe.close()

    proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=stderr,
                            stdin=stdin, start_new_session=True)
    thread = threading.Thread(target=reader, args=(proc.stdout,), daemon=True)
    thread.start()
    timed_out = False
    try:
        proc.wait(timeout=deadline_s)
    except subprocess.TimeoutExpired:
        common._kill_group(proc)
        timed_out = True
    finally:
        thread.join()
    common._killpg(proc.pid, __import__("signal").SIGKILL)
    if tail:
        with open(sidecar, "wb") as f:
            f.writelines(tail)
    return proc.returncode, timed_out, state["capped"], sidecar


def run_bare_agent(a, ws, tmp, out, tt, prompt, deadline_s):
    """Run the codex or claude child; returns (record, exit_code, timed_out, version)."""
    arm = a.arm
    extra = {}
    if arm == "claude":
        claude_bin = a.claude_bin or shutil.which("claude")
        if not claude_bin:
            raise BareError("claude not found on PATH (--claude-bin)")
        cfg = os.path.join(tmp, "claude-config")
        os.makedirs(cfg)
        extra = {"CLAUDE_CONFIG_DIR": cfg, "CLAUDE_CODE_OAUTH_TOKEN": read_token(a.claude_token_home),
                 "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "DISABLE_TELEMETRY": "1",
                 "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1", "DISABLE_AUTOUPDATER": "1"}
        cmd, bin_ = claude_command(a, claude_bin), claude_bin
    elif arm == "codex":
        codex_bin = a.codex_bin or shutil.which("codex") or CODEX_BIN_DEFAULT
        if not os.access(codex_bin, os.X_OK):
            raise BareError("codex not found (--codex-bin, or codex on PATH)")
        if not a.codex_home or not os.path.isdir(a.codex_home):
            raise BareError("--codex-home must be an existing CODEX_HOME holding the ChatGPT login")
        extra = {"CODEX_HOME": a.codex_home}
        cmd, bin_ = codex_command(a, codex_bin), codex_bin
    elif arm == "pi":
        pi_bin = a.pi_bin or shutil.which("pi") or os.path.join(PRIVATE, "agents/bin/pi")
        if not pi_bin:
            raise BareError("pi not found (--pi-bin)")
        # Pi's own sign-in dir, used in place (credentials are never copied); --no-session keeps cells from sharing state
        cfg = os.path.join(PRIVATE, "agents/pi-auth")
        node = shutil.which("node")
        extra = {"PI_CODING_AGENT_DIR": cfg,
                 "PATH": (os.path.dirname(node) + ":" if node else "") + os.environ.get("PATH", "/usr/bin:/bin")}
        settings_path = os.path.join(cfg, "settings.json")
        try:
            with open(settings_path, encoding="utf-8") as f:
                pi_settings = json.load(f)
        except (OSError, ValueError):
            pi_settings = {}
        pi_settings["shellCommandPrefix"] = "export PATH=" + json.dumps(extra["PATH"])
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(pi_settings, f, indent=2)
            f.write("\n")
        cmd, bin_ = pi_command(a, pi_bin, prompt), pi_bin
    elif arm == "opencode":
        opencode_bin = a.opencode_bin or shutil.which("opencode") or os.path.join(PRIVATE, "agents/npm/node_modules/.bin/opencode")
        if not opencode_bin:
            raise BareError("opencode not found (--opencode-bin)")
        cfg = os.path.join(tmp, "opencode-config")
        os.makedirs(cfg)
        auth_data = os.path.join(PRIVATE, "agents/opencode-auth/xdg")
        extra = {"OPENCODE_CONFIG_DIR": cfg, "XDG_DATA_HOME": auth_data,
                 "OPENCODE_DISABLE_AUTOUPDATE": "1"}
        cmd, bin_ = opencode_command(a, opencode_bin, ws, prompt), opencode_bin
    else:
        loop_bin = a.loop_bin or shutil.which("kogen-loop")
        if not loop_bin or not os.access(loop_bin, os.X_OK):
            raise BareError("kogen-loop not found (--loop-bin, or kogen-loop on PATH)")
        if not a.home or not os.path.isdir(a.home):
            raise BareError("--home must be an existing Kogen home holding the provider login")
        extra = {"HOME": a.home}
        cmd, bin_ = [loop_bin, "run", "--task", "-"], loop_bin
    env = agent_env(tt, tmp, extra)
    ver_cmd = [bin_, "version"] if arm == "loop" else [bin_, "--version"]
    ver = subprocess.run(ver_cmd, capture_output=True, text=True, env=env, timeout=60).stdout.strip()
    prompt_path = os.path.join(tmp, "prompt.md")
    with open(prompt_path, "w") as f:
        f.write(prompt)
    events = os.path.join(out, "events.jsonl")
    started = time.monotonic()
    if arm == "loop":
        with open(os.path.join(tmp, "task.json"), "w") as ft:
            json.dump(loop_task(a, ws, tmp, prompt, tt), ft)
        cmd = [bin_, "run", "--task", os.path.join(tmp, "task.json")]
    with open(os.path.join(out, "stderr.txt"), "w") as fe, open(prompt_path) as fi:
        code, timed_out, capped, usage_events = filtered_agent_run(
            cmd, ws, env, deadline_s, events, fe, fi, arm, out)
    wall = round(time.monotonic() - started, 3)
    parse_path = usage_events if capped and os.path.isfile(usage_events) else events
    rec = (parse_claude(parse_path) if arm == "claude" else parse_loop(parse_path) if arm == "loop" else
           parse_open_usage(parse_path, arm) if arm in ("pi", "opencode") else parse_codex(parse_path))
    rec["events_capped"] = capped
    rec["wall_s"] = wall
    return rec, code, timed_out, ver


# --- one cell ---------------------------------------------------------------------------------------------------

def leak_scan(paths):
    hits = {}
    for p in paths:
        try:
            text = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        text = LEAK_AGENT_BIN.sub("<pi-agent-bin>", text)
        for m in LEAK.findall(text):
            hits[m] = hits.get(m, 0) + 1
    return hits


def keep_loop_session(tmp, out):
    """Keep kogen-loop's private transcript in the cell; never copy its HOME or other files."""
    src = os.path.join(tmp, "loop-session", "session.json")
    if not os.path.isfile(src):
        return
    dst_dir = os.path.join(out, "loop-session")
    os.makedirs(dst_dir, mode=0o700, exist_ok=True)
    os.chmod(dst_dir, 0o700)
    dst = os.path.join(dst_dir, "session.json")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o600)


def run_cell(a):
    task_dir = os.path.join(a.tasks, a.task)
    lane = a.lane or a.arm
    cell = f"{a.task}/r{a.rep}/{lane}"
    out = common.cell_dir(a.run_dir, cell)
    if os.path.exists(os.path.join(out, "result.json")) and not a.force:
        raise BareError(f"{cell} is already done (result.json exists); use --force to rerun")
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    form = a.intent_form
    tt, supplied, _ = load_task_inputs(task_dir, form)
    slug = tt.get("name")
    lcell.check_supplied(supplied, slug)
    tmp = tempfile.mkdtemp(prefix="lanes-bare-")
    ws = os.path.join(tmp, "ws")
    try:
        if a.arm == "kogen":
            result = kogen_cell(a, cell, lane, task_dir, tt, slug, ws, tmp, out)
        else:
            result = bare_cell(a, cell, lane, task_dir, tt, form, ws, tmp, out)
    finally:
        if a.keep:
            print(f"kept workspace: {ws}", file=sys.stderr)
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    common.write_json(os.path.join(out, "result.json"), result)
    tar_path = os.path.join(out, "final-tree.tar")
    if not a.no_grade and os.path.isfile(tar_path) and os.path.getsize(tar_path) > 0:
        ev = grading.grade_cell(a.run_dir, cell, a.tasks)
        result["all_passed"] = ev.get("all_passed")
    elif not a.no_grade and result.get("outcome") != "harness_error":
        result.update(outcome="harness_error", detail="final-tree.tar is missing or empty",
                      errors=["final-tree.tar is missing or empty"])
    common.write_json(os.path.join(out, "result.json"), result)
    return result


def bare_cell(a, cell, lane, task_dir, tt, form, ws, tmp, out):
    started, t0 = now(), time.monotonic()
    prompt = build_prompt(task_dir, form)
    with open(os.path.join(out, "prompt.md"), "w") as f:
        f.write(prompt)
    git_env = make_bare_workspace(ws, tmp, task_dir, form, tt)
    result = {"cell": cell, "lane": lane, "arm": a.arm, "phase": "build", "model": a.model, "effort": a.effort,
              "started": started, "host": a.host, "prompt_sha256": common.sha256_file(os.path.join(out, "prompt.md")),
              "pass_trees": [], "first_green_tree": None, "intent_hash": None}
    try:
        setup_s = run_setup(ws, tt, agent_env(tt, tmp, {}), out)
        result["setup_wall_s"] = setup_s
        try:
            rec, code, timed_out, ver = run_bare_agent(a, ws, tmp, out, tt, prompt, a.deadline_s)
        finally:
            if a.arm == "loop":
                keep_loop_session(tmp, out)
    except Exception as e:
        result.update(outcome="harness_error", detail=f"{type(e).__name__}: {e}",
                      errors=[f"{type(e).__name__}: {e}"], exit_code=None, ended=now(),
                      wall_s=round(time.monotonic() - t0, 3), final_tree=None)
        with open(os.path.join(out, "final-tree.tar"), "wb"):
            pass
        return result
    restored = protected_restore(ws, task_dir, tt)
    result["final_tree"] = finish_tree(ws, out, git_env)
    if timed_out:
        outcome = "timeout"
    elif rec["errors"] or code:
        outcome = "agent_error"
    else:
        outcome = "finished"
    cost, why = price(rec)
    stage = {"stage": "agent", "wall_s": rec["wall_s"], "exit_code": code, **({"timed_out": True} if timed_out else {}),
             "outcome": outcome, **{k: rec.get(k) for k in usage.TOKENS}, "requests": rec.get("requests"),
             "tool_calls": rec.get("tool_calls"), "models": rec.get("models"), "cost_usd": cost, "cost_reason": why,
             **({"client_cost_usd": rec["client_cost_usd"]} if rec.get("client_cost_usd") is not None else {}),
             **({"cache_creation_input_tokens": rec["cache_creation_input_tokens"]}
                if rec.get("cache_creation_input_tokens") is not None else {})}
    totals = {k: stage[k] for k in (*usage.TOKENS, "requests", "tool_calls", "models", "cost_usd", "cost_reason")}
    totals["wall_s"] = rec["wall_s"]
    result.update(outcome=outcome, exit_code=code, ended=now(), wall_s=round(time.monotonic() - t0, 3),
                  agent_version=ver, stages=[stage], totals=totals, protect_restored=restored,
                  errors=rec["errors"], leak_suspects=leak_scan([os.path.join(out, "events.jsonl")]))
    if rec.get("events_capped"):
        result["events_capped"] = True
    return result


def kogen_cell(a, cell, lane, task_dir, tt, slug, ws, tmp, out):
    kogen = a.kogen or shutil.which("kogen")
    if not kogen:
        raise BareError("kogen not found (--kogen)")
    models = dict(m.split("=", 1) for m in (a.kogen_models or []))
    if not models:
        raise BareError("--kogen-model ROLE='provider/model effort' is required for the kogen arm")
    config = lcell.project_yaml(tt, models)
    lcell.make_workspace(ws, tmp, os.path.join(task_dir, "start"), config)
    lcell.install_supplied(ws, os.path.join(task_dir, "supplied", a.intent_form), slug)
    started, t0 = now(), time.monotonic()
    c = lcell.Cell(ws, os.path.abspath(kogen), out, a.deadline_s)
    root = lcell.release_root(os.path.abspath(kogen))
    if root:
        lcell.ensure_node_path(root)
    if a.home:
        c.env["HOME"] = a.home
    if a.claude_config_dir:
        c.env["CLAUDE_CONFIG_DIR"] = a.claude_config_dir
    version = c.version(tmp)
    intent_hash = c.approve(slug)
    if intent_hash:
        c.record("build", [c.invoke(["intent", "build", slug])])
    result = lcell._collect({"phase": "build"}, cell, lane, ws, slug, c, out, started, t0, version, intent_hash,
                            a.host, None)
    result.update(arm="kogen", models_config=models, tool_calls=None,
                  leak_suspects=leak_scan([os.path.join(out, "stdout.txt"), os.path.join(out, "stderr.txt")]
                                          + glob.glob(os.path.join(out, "run-log", "*"))))
    return result


# --- summary and batch ------------------------------------------------------------------------------------------

def executor_usage(cell_dir):
    """Kogen driving Claude Code: its result.json has no tokens; sum the executor transcripts (one result event per round)."""
    tot = {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "requests": 0, "cost_usd": 0.0}
    paths = glob.glob(os.path.join(cell_dir, "run-log", "**", "round-*.jsonl"), recursive=True)
    for path in paths:
        r = parse_claude(path)
        if r["input_tokens"] is None:
            continue
        for k in ("input_tokens", "cached_input_tokens", "output_tokens", "requests"):
            tot[k] += r.get(k) or 0
        tot["cost_usd"] += r.get("client_cost_usd") or 0
    return tot if paths and tot["input_tokens"] else {}


def summary_rows(run_dir):
    rows = []
    for rpath in sorted(glob.glob(os.path.join(run_dir, "cells", "*", "r*", "*", "result.json"))):
        d = os.path.dirname(rpath)
        r = common.read_json(rpath)
        epath = os.path.join(d, "evaluation.json")
        ev = common.read_json(epath) if os.path.isfile(epath) else {}
        t = r.get("totals") or {}
        if t.get("input_tokens") is None:
            t = {**t, **executor_usage(d)}
        rows.append({"cell": r["cell"], "arm": r.get("arm") or "kogen", "outcome": r.get("outcome"),
                     "pass": ev.get("all_passed"), "infra": ev.get("infrastructure"),
                     "passed": (ev.get("totals") or {}).get("passed"), "expected": (ev.get("totals") or {}).get("expected"),
                     "wall_s": r.get("wall_s"), "agent_wall_s": t.get("wall_s"), "input": t.get("input_tokens"),
                     "cached": t.get("cached_input_tokens"), "output": t.get("output_tokens"),
                     "reasoning": t.get("reasoning_tokens"), "requests": t.get("requests"), "usd": t.get("cost_usd"),
                     "leak": r.get("leak_suspects")})
    return rows


def print_summary(run_dir):
    rows = summary_rows(run_dir)
    print(f"{'cell':34} {'outcome':12} {'pass':5} {'tests':7} {'wall_s':>8} {'input':>9} {'cached':>9} {'output':>8} {'reason':>7} {'usd':>8} leak")
    for r in rows:
        tests = f"{r['passed']}/{r['expected']}" if r["expected"] is not None else "-"
        usd = "-" if r["usd"] is None else f"{r['usd']:.4f}"
        print(f"{r['cell']:34} {str(r['outcome']):12} {str(r['pass']):5} {tests:7} {r['wall_s']!s:>8} {r['input']!s:>9} "
              f"{r['cached']!s:>9} {r['output']!s:>8} {r['reasoning']!s:>7} {usd:>8} {'YES' if r['leak'] else '-'}")
    return rows


def arm_namespace(base, arm_spec, task, rep, run_dir, tasks):
    a = argparse.Namespace(**vars(base))
    a.task, a.rep, a.run_dir, a.tasks = task, rep, run_dir, tasks
    a.lane = arm_spec["name"]
    a.arm = arm_spec["arm"]
    a.model, a.effort = arm_spec.get("model"), arm_spec.get("effort")
    a.provider = arm_spec.get("provider")
    a.kogen_models = [f"{k}={v}" for k, v in (arm_spec.get("models") or {}).items()]
    for key in ("home", "claude_config_dir", "claude_token_home", "codex_home", "codex_bin", "claude_bin", "loop_bin", "kogen", "pi_bin", "opencode_bin"):
        if arm_spec.get(key):
            setattr(a, key, os.path.expanduser(arm_spec[key]))
    return a


def batch(args):
    spec = common.read_json(args.batch)
    tasks = os.path.expanduser(args.tasks or spec["tasks_dir"])
    run_dir = os.path.abspath(args.run_dir or os.path.join(os.path.dirname(os.path.abspath(args.batch)), spec["id"]))
    os.makedirs(run_dir, exist_ok=True)
    shutil.copyfile(args.batch, os.path.join(run_dir, "batch.json"))
    base = argparse.Namespace(rep=1, lane=None, force=False, keep=False, no_grade=False, host=args.host,
                              deadline_s=spec.get("deadline_s", DEADLINE_S), intent_form=spec.get("intent_form", "gherkin"),
                              kogen=None, kogen_models=None, home=None, claude_config_dir=None, claude_token_home=None,
                              codex_home=None, codex_bin=None, claude_bin=None, loop_bin=None, pi_bin=None, opencode_bin=None,
                              model=None, effort=None)
    for key in ("kogen", "home", "claude_config_dir", "claude_token_home", "codex_home", "codex_bin", "claude_bin", "loop_bin", "pi_bin", "opencode_bin"):
        if spec.get(key):
            setattr(base, key, os.path.expanduser(spec[key]))
    cells = []
    for rep in range(1, spec.get("reps", 1) + 1):  # rep-major, arms of one task adjacent: same host, same minute
        for task in spec["tasks"]:
            for arm in spec["arms"]:
                if os.path.isfile(common.cell_dir(run_dir, f"{task}/r{rep}/{arm['name']}") + "/result.json"):
                    continue
                cells.append(arm_namespace(base, arm, task, rep, run_dir, tasks))
    cells = cells[:args.max_cells] if args.max_cells else cells
    print(f"{len(cells)} cells to run, slots {args.slots}", file=sys.stderr)
    lock = threading.Lock()
    batch_id = re.sub(r"[^A-Za-z0-9_.-]", "_", str(spec["id"]))
    live_path = os.path.join(PRIVATE, f".bare-live.{batch_id}")
    live_count = 0
    heartbeat_stop = threading.Event()

    def write_live():
        line = f"{now()} live={live_count} batch={batch_id} slots={args.slots}\n"
        tmp = live_path + f".tmp.{os.getpid()}"
        with open(tmp, "w") as f:
            f.write(line)
        os.replace(tmp, live_path)

    def heartbeat():
        while not heartbeat_stop.wait(60):
            with lock:
                write_live()

    def stop_on_term(signum, frame):
        raise SystemExit(128 + signum)

    previous_term = signal.signal(signal.SIGTERM, stop_on_term)

    def one(a):
        nonlocal live_count
        with lock:
            live_count += 1
            write_live()
        try:
            r = run_cell(a)
            line = f"{a.task}/r{a.rep}/{a.lane}: {r['outcome']} pass={r.get('all_passed')} wall={r['wall_s']}s"
        except Exception as e:
            line = f"{a.task}/r{a.rep}/{a.lane}: ERROR {e}"
        finally:
            with lock:
                live_count -= 1
                write_live()
        with lock:
            print(line, file=sys.stderr, flush=True)

    try:
        os.makedirs(os.path.dirname(live_path), exist_ok=True)
        with lock:
            write_live()
        ticker = threading.Thread(target=heartbeat, daemon=True)
        ticker.start()
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(args.slots, 1)) as pool:
            list(pool.map(one, cells))
        print_summary(run_dir)
        return 0
    finally:
        heartbeat_stop.set()
        if "ticker" in locals():
            ticker.join()
        with lock:
            try:
                os.unlink(live_path)
            except FileNotFoundError:
                pass
        signal.signal(signal.SIGTERM, previous_term)


def add_common(p):
    p.add_argument("--host", default="local")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cell")
    c.add_argument("--tasks", required=True)
    c.add_argument("--task", required=True)
    c.add_argument("--arm", required=True, choices=["kogen", "codex", "claude", "loop", "pi", "opencode"])
    c.add_argument("--run-dir", required=True)
    c.add_argument("--rep", type=int, default=1)
    c.add_argument("--lane")
    c.add_argument("--model")
    c.add_argument("--effort")
    c.add_argument("--kogen-model", dest="kogen_models", action="append", metavar="ROLE=provider/model effort")
    c.add_argument("--kogen")
    c.add_argument("--home", help="HOME of the kogen process (its credentials folder)")
    c.add_argument("--claude-config-dir")
    c.add_argument("--claude-token-home", help="Kogen home whose stored Claude Code token the claude arm uses")
    c.add_argument("--claude-bin")
    c.add_argument("--codex-home", help="CODEX_HOME holding the ChatGPT login")
    c.add_argument("--codex-bin")
    c.add_argument("--loop-bin")
    c.add_argument("--pi-bin")
    c.add_argument("--opencode-bin")
    c.add_argument("--intent-form", default="gherkin")
    c.add_argument("--deadline-s", type=int, default=DEADLINE_S)
    c.add_argument("--keep", action="store_true")
    c.add_argument("--force", action="store_true")
    c.add_argument("--no-grade", action="store_true")
    add_common(c)
    b = sub.add_parser("batch")
    b.add_argument("batch")
    b.add_argument("--tasks")
    b.add_argument("--run-dir")
    b.add_argument("--slots", type=int, default=1)
    b.add_argument("--max-cells", type=int)
    add_common(b)
    s = sub.add_parser("summary")
    s.add_argument("run_dir")
    a = p.parse_args(argv)
    try:
        if a.cmd == "summary":
            print_summary(a.run_dir)
            return 0
        if a.cmd == "batch":
            return batch(a)
        a.run_dir = os.path.abspath(a.run_dir)
        a.tasks = os.path.expanduser(a.tasks)
        r = run_cell(a)
        print(f"{r['cell']}: {r['outcome']} all_passed={r.get('all_passed')} wall_s={r['wall_s']}")
        return 0
    except (BareError, grading.GradeError, lcell.CellError) as e:
        print(f"lanes-bare: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
