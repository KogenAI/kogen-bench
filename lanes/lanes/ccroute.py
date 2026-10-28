"""Running cells on the Claude Code (CC) subscription executor: the login preflight and the dry-cell check.

A lane role `"claude-code/<model> <effort>"` makes Kogen run its builder with the CC executor (`cell.role_entry`).
CC runs need, per host, a hosts-file `claude_config_dir` (an existing folder holding the CC login; it reaches the
cell as `CLAUDE_CONFIG_DIR`) and optionally `claude_bin` (the `claude` executable; default `$CLAUDE_BIN` on a local
host, else `claude` on PATH). `preflight` runs `claude auth status --json` under the cell environment and refuses
unless `loggedIn` is true. Nothing the command prints is shown. `check_run_log` is the dry-cell check
(`lanes-ccdry`): Kogen's run log must hold the executor's events.
"""

import json
import os
import shlex
import shutil
import subprocess

from . import common

PREFIX = "claude-code/"
TIMEOUT_S = 60
# what Kogen's CC adapter strips from the child (cli/executor/claudecode/args.go); the check must not see them either
STRIPPED = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL", "ANTHROPIC_PROFILE",
            "CLAUDE_CODE_OAUTH_TOKEN", "CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX", "CLAUDE_CODE_USE_FOUNDRY")


def uses_claude_code(exp):
    """True when any lane role of the experiment names the CC executor."""
    return any(spec.startswith(PREFIX) for lane in exp.get("lanes", [])
               for spec in (lane.get("settings") or {}).get("models", {}).values())


def lane_uses_claude_code(lane):
    return uses_claude_code({"lanes": [lane]})


def cell_env(config_dir):
    """The environment a cell's Kogen gets, as far as the CC login depends on it (HOME is the process's own)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("KOGEN_LANES_") and k not in STRIPPED}
    env["CLAUDE_CONFIG_DIR"] = config_dir
    return env


def _logged_in(text):
    try:
        data = json.loads(text)
    except ValueError:
        return None
    return data.get("loggedIn") is True if isinstance(data, dict) else None


def check_host(name, cfg, ssh):
    """`(ok, one-line message)` for one host: a Kogen home holding a stored Claude Code token (`kogen_token_home`), or
    else config dir set and present, then `claude auth status --json`."""
    token_home = cfg.get("kogen_token_home")
    if token_home:  # `kogen provider login claude-code` (stdin) stored a token there; Kogen's cells use it, not a CC login
        cred = os.path.join(token_home, ".kogen", "credentials", "claude-code.json")
        if cfg["target"] != "local":
            try:
                p = subprocess.run([*ssh, cfg["target"], f"test -s {shlex.quote(cred)}"], capture_output=True,
                                   timeout=TIMEOUT_S, stdin=subprocess.DEVNULL)
            except (OSError, subprocess.TimeoutExpired) as e:
                return False, f"{name}: cannot check the stored token ({type(e).__name__})"
            present = p.returncode == 0
        else:
            present = os.path.isfile(cred) and os.path.getsize(cred) > 0
        if present:
            return True, f"{name}: Kogen stored token in {token_home}"
        return False, f"{name}: no stored Claude Code token in {token_home} (run kogen provider login claude-code there)"
    config_dir = cfg.get("claude_config_dir")
    if not config_dir:
        return False, f"{name}: CLAUDE_CONFIG_DIR is not set (hosts file: claude_config_dir)"
    remote = cfg["target"] != "local"
    claude = cfg.get("claude_bin") or (None if remote else os.environ.get("CLAUDE_BIN")) or "claude"
    try:
        if remote:
            drop = " ".join("-u " + v for v in STRIPPED)
            command = (f"test -d {shlex.quote(config_dir)} || exit 3; env {drop} CLAUDE_CONFIG_DIR={shlex.quote(config_dir)} "
                       f"{shlex.quote(claude)} auth status --json")
            p = subprocess.run([*ssh, cfg["target"], command], capture_output=True, text=True, timeout=TIMEOUT_S,
                               stdin=subprocess.DEVNULL)
            if p.returncode == 3:
                return False, f"{name}: CLAUDE_CONFIG_DIR {config_dir} is not an existing directory"
        else:
            if not os.path.isdir(config_dir):
                return False, f"{name}: CLAUDE_CONFIG_DIR {config_dir} is not an existing directory"
            env = cell_env(config_dir)
            path = shutil.which(claude, path=env.get("PATH"))
            if not path:
                return False, f"{name}: claude not found ({claude}); put it on PATH or set CLAUDE_BIN"
            p = subprocess.run([path, "auth", "status", "--json"], env=env, capture_output=True, text=True,
                               timeout=TIMEOUT_S, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, f"{name}: cannot run claude auth status ({type(e).__name__})"
    state = _logged_in(p.stdout)
    if state:
        return True, f"{name}: claude is logged in"
    if state is None:
        return False, f"{name}: claude auth status gave no JSON (exit {p.returncode})"
    return False, f"{name}: claude is not logged in (loggedIn false) for CLAUDE_CONFIG_DIR {config_dir}"


def preflight(exp, hosts, out=print, ssh=None):
    """Refusal count over the experiment's hosts (`{name: {target, claude_config_dir, ...}}`); 0 when no lane uses CC.
    With no hosts at all a CC run is refused once."""
    if not uses_claude_code(exp):
        return 0
    if not hosts:
        out("preflight: a lane uses claude-code: pass the hosts file (--hosts) to check CLAUDE_CONFIG_DIR and the login")
        return 1
    ssh = ssh or shlex.split(os.environ.get("LANES_SSH", "ssh -o BatchMode=yes -o ConnectTimeout=20"))
    bad = 0
    for name, cfg in hosts.items():
        ok, message = check_host(name, cfg, ssh)
        bad += not ok
        out(f"claude-code preflight: {'ok' if ok else 'REFUSED'}: {message}")
    return bad


def check_run_log(cell_dir):
    """`(ok, message)` for a finished cell: its run log (`run-log/log.jsonl`) shows the CC executor ran, i.e. an
    `executor_started` event for claude-code and a round that started. A native `request` instead means Kogen fell
    back to a provider."""
    path = os.path.join(cell_dir, "run-log", "log.jsonl")
    if not os.path.isfile(path):
        return False, "no run log (Kogen never started a build)"
    try:
        events = common.read_jsonl(path)
    except ValueError:
        return False, "the run log is not readable JSON lines"
    names = {e.get("event") for e in events if isinstance(e, dict)}
    started = [e for e in events if isinstance(e, dict) and e.get("event") == "executor_started"]
    if not started:
        if "request" in names:
            return False, "Kogen fell back to a native provider (build requests, no executor_started event)"
        return False, "the executor never started (no executor_started event in the run log)"
    if started[0].get("executor") != "claude-code":
        return False, f"the executor was {started[0].get('executor')!r}, not claude-code"
    if "executor_round_started" not in names:
        return False, "the executor started but ran no round (no executor_round_started event)"
    return True, f"the claude-code executor ran ({sum(1 for e in events if str(e.get('event')).startswith('executor_'))} executor events)"
