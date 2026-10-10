"""Case loader and black-box step executor.

Cases are JSON so generated trace adapters can write them without depending
on the language of the implementation under test.
"""

from __future__ import annotations

import concurrent.futures
import fnmatch
import glob
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Callable

from .fake_provider import FakeProvider, make_injected_auth
from .process_control import cleanup_case_cwd, implementation_environment, run_process


SUITE_ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = SUITE_ROOT / "cases"
GIT_NAME = "Kogen Conformance"
GIT_EMAIL = "conformance@kogen.invalid"
TOKEN = re.compile(r"\{\{([^{}]+)\}\}")
CAPTURE = re.compile(r"^capture:(hash|time|id):([A-Za-z_][A-Za-z0-9_.-]*)$")
CAPTURE_REGEX = re.compile(r"^capture:([A-Za-z_][A-Za-z0-9_.-]*)\|(.+)$", re.DOTALL)
REFERENCE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*$")
TYPE_PATTERNS = {
    "hash": r"[0-9a-fA-F]{7,64}",
    "time": r"(?:[0-9]{1,20}|[0-9]{4}-[0-9T:.+Z-]{5,})",
    "id": r"[A-Za-z0-9_.:-]+",
}


class CaseError(Exception):
    """Malformed case input or a harness setup error."""


# Executors keep the JSON runner decoupled from future case formats.
CASE_EXECUTORS: dict[str, Callable[..., dict[str, Any]] | None] = {
    "json": None,
    "quint": None,
    "gherkin": None,
}


def register_case_executor(kind: str, executor: Callable[..., dict[str, Any]]) -> None:
    if kind not in CASE_EXECUTORS:
        raise ValueError(f"unknown conformance case kind: {kind}")
    CASE_EXECUTORS[kind] = executor


class Comparator:
    """Subset comparator with typed captures shared for all case steps."""

    def __init__(self) -> None:
        self.captures: dict[str, str] = {}

    def compare(self, actual: Any, expected: Any, path: str = "$", mode: str = "equals") -> list[str]:
        if isinstance(expected, dict) and any(key in expected for key in (
            "equals", "contains", "not_contains", "regex", "startswith", "endswith"
        )):
            failures: list[str] = []
            for key, value in expected.items():
                if key == "equals":
                    failures.extend(self.compare(actual, value, path, "equals"))
                elif key == "contains":
                    failures.extend(self.compare(actual, value, path, "contains"))
                elif key == "not_contains":
                    rendered = _as_text(actual)
                    if _render_pattern(value, self.captures, unanchored=True)[0].search(rendered):
                        failures.append(f"{path}: unexpectedly contains {value!r}")
                elif key == "regex":
                    try:
                        matched = re.search(str(value), _as_text(actual), re.MULTILINE | re.DOTALL)
                    except re.error as error:
                        failures.append(f"{path}: invalid expected regex: {error}")
                    else:
                        if not matched:
                            failures.append(f"{path}: does not match regex {value!r}")
                elif key == "startswith":
                    if not _as_text(actual).startswith(_resolve_refs(str(value), self.captures)):
                        failures.append(f"{path}: does not start with {value!r}")
                elif key == "endswith":
                    if not _as_text(actual).endswith(_resolve_refs(str(value), self.captures)):
                        failures.append(f"{path}: does not end with {value!r}")
            return failures

        if isinstance(expected, dict):
            if not isinstance(actual, dict):
                return [f"{path}: expected object, got {_type_name(actual)}"]
            failures = []
            for key, value in expected.items():
                if key not in actual:
                    failures.append(f"{path}.{key}: missing")
                else:
                    failures.extend(self.compare(actual[key], value, f"{path}.{key}"))
            return failures

        if isinstance(expected, list):
            if not isinstance(actual, list):
                return [f"{path}: expected array, got {_type_name(actual)}"]
            if len(actual) < len(expected):
                return [f"{path}: expected at least {len(expected)} rows, got {len(actual)}"]
            failures = []
            for index, value in enumerate(expected):
                failures.extend(self.compare(actual[index], value, f"{path}[{index}]"))
            return failures

        if isinstance(expected, str) and TOKEN.search(expected):
            rendered = _as_text(actual)
            pattern, group_names = _render_pattern(expected, self.captures, unanchored=(mode == "contains"))
            match = pattern.search(rendered) if mode == "contains" else pattern.fullmatch(rendered)
            if not match:
                return [f"{path}: {rendered!r} does not match placeholder pattern {expected!r}"]
            for group_name, capture_name in group_names.items():
                value = match.group(group_name)
                old = self.captures.get(capture_name)
                if old is not None and old != value:
                    return [f"{path}: capture {capture_name!r} changed from {old!r} to {value!r}"]
                self.captures[capture_name] = value
            return []

        if isinstance(expected, str) and isinstance(actual, (str, int, float)) and not isinstance(actual, bool):
            resolved = _resolve_refs(expected, self.captures)
            if mode == "contains":
                if resolved not in str(actual):
                    return [f"{path}: {actual!r} does not contain {expected!r}"]
                return []
            if resolved != str(actual):
                return [f"{path}: expected {expected!r}, got {actual!r}"]
            return []
        if actual != expected:
            return [f"{path}: expected {expected!r}, got {actual!r}"]
        return []


def _as_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return "null"
    if isinstance(value, (bool, int, float)):
        return str(value).lower() if isinstance(value, bool) else str(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def _type_name(value: Any) -> str:
    return "null" if value is None else type(value).__name__


def _resolve_refs(value: str, captures: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        token = match.group(1)
        return captures[token] if token in captures else match.group(0)
    return TOKEN.sub(replace, value)


def _render_pattern(value: Any, captures: dict[str, str], unanchored: bool = False) -> tuple[re.Pattern[str], dict[str, str]]:
    source = str(value)
    pieces: list[str] = []
    group_names: dict[str, str] = {}
    cursor = 0
    for match in TOKEN.finditer(source):
        pieces.append(re.escape(source[cursor:match.start()]))
        token = match.group(1)
        capture = CAPTURE.fullmatch(token)
        custom = CAPTURE_REGEX.fullmatch(token)
        if capture:
            kind, name = capture.groups()
            if name in captures:
                pieces.append(re.escape(captures[name]))
            else:
                group = _unique_group(name, list(group_names))
                pieces.append(f"(?P<{group}>{TYPE_PATTERNS[kind]})")
                group_names[group] = name
        elif custom:
            name, expression = custom.groups()
            if name in captures:
                pieces.append(re.escape(captures[name]))
            else:
                try:
                    re.compile(expression)
                except re.error:
                    expression = r".+?"
                group = _unique_group(name, list(group_names))
                pieces.append(f"(?P<{group}>{expression})")
                group_names[group] = name
        elif REFERENCE.fullmatch(token) and token in captures:
            pieces.append(re.escape(captures[token]))
        else:
            pieces.append(re.escape(match.group(0)))
        cursor = match.end()
    pieces.append(re.escape(source[cursor:]))
    expression = "".join(pieces)
    if not unanchored:
        expression = "\\A" + expression + "\\Z"
    return re.compile(expression, re.DOTALL), group_names


def _unique_group(name: str, current: list[str]) -> str:
    safe = re.sub(r"\W", "_", name)
    return safe if safe not in current else f"{safe}_{len(current)}"


def load_cases(patterns: list[str] | None = None) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    paths = sorted(path for path in CASES_DIR.rglob("*.json")
                   if not path.name.endswith(".manifest.json") and not path.name.endswith(".itf.json"))
    for path in paths:
        try:
            case = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise CaseError(f"invalid case file {path}: {error}") from error
        if not isinstance(case, dict) or not isinstance(case.get("id"), str):
            raise CaseError(f"{path}: case requires a string id")
        if not case["id"].strip():
            raise CaseError(f"{path}: case id must not be empty")
        if not isinstance(case.get("steps"), list) or not case["steps"]:
            raise CaseError(f"{path}: case requires a non-empty steps array")
        if any(not isinstance(step, dict) for step in case["steps"]):
            raise CaseError(f"{path}: every step must be an object")
        case["_file"] = str(path.relative_to(SUITE_ROOT))
        if patterns and not any(fnmatch.fnmatchcase(case["id"], pattern) or fnmatch.fnmatchcase(path.name, pattern)
                                for pattern in patterns):
            continue
        selected.append(case)
    from .quint_runner import load_quint_cases
    for trace in load_quint_cases(CASES_DIR):
        path = Path(trace["_file"])
        if patterns and not any(fnmatch.fnmatchcase(trace["id"], pattern)
                                or fnmatch.fnmatchcase(path.name, pattern) for pattern in patterns):
            continue
        selected.append(trace)
    from .gherkin_runner import load_feature_cases
    feature_dirs = [SUITE_ROOT / "features-src", CASES_DIR]
    for case in load_feature_cases(feature_dirs):
        path = Path(case["_file"])
        if patterns and not any(fnmatch.fnmatchcase(case["id"], pattern)
                                or fnmatch.fnmatchcase(path.name, pattern) for pattern in patterns):
            continue
        selected.append(case)
    seen: set[str] = set()
    for case in selected:
        if case["id"] in seen:
            raise CaseError(f"duplicate case id: {case['id']}")
        seen.add(case["id"])
    return selected


def _patterns(raw: str | None) -> list[str] | None:
    if not raw:
        return None
    return [part.strip() for part in raw.split(",") if part.strip()]


class CaseWorld:
    def __init__(self, case: dict[str, Any], kogen: str, time_scale: float, keep: bool,
                 timeout_s: float = 60.0, workdir: str | Path = "/tmp"):
        self.case = case
        self.kogen = kogen
        self.keep = keep
        self.timeout_s = timeout_s
        self.root = Path(tempfile.mkdtemp(prefix="kc2-case-", dir=str(workdir))).resolve()
        self.home = self.root / "home"
        self.tmp = self.root / "tmp"
        self.checkout = self.root / "checkout"
        self.gitconfig = self.home / ".gitconfig"
        self.auth_path = self.root / "auth.json"
        self.fake: FakeProvider | None = None
        self.closed = False
        self.comparator = Comparator()
        self.results: list[dict[str, Any]] = []
        self.failures: list[str] = []
        self.case_time_scale = case.get("time_scale", time_scale)
        try:
            for directory in (self.home, self.tmp, self.checkout):
                directory.mkdir(parents=True, exist_ok=True)
            self._write_gitconfig()
            self._init_repo()
            self._write_initial_files()
            self._initial_commit()
            self._start_fake()
        except Exception:
            if self.fake:
                self.fake.close()
            shutil.rmtree(self.root, ignore_errors=True)
            raise

    def _write_gitconfig(self) -> None:
        text = """[user]
\tname = Kogen Conformance
\temail = conformance@kogen.invalid
[init]
\tdefaultBranch = main
[commit]
\tgpgsign = false
[tag]
\tgpgsign = false
[core]
\tautocrlf = false
[protocol "file"]
\tallow = always
[advice]
\tdetachedHead = false
"""
        self.gitconfig.write_text(text, encoding="utf-8")

    def _base_env(self) -> dict[str, str]:
        inherited_path = os.environ.get("PATH", "/usr/bin:/bin")
        env = {
            "HOME": str(self.home),
            "TMPDIR": str(self.tmp),
            "TMP": str(self.tmp),
            "TEMP": str(self.tmp),
            "PATH": inherited_path,
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "USER": os.environ.get("USER", "kogen"),
            "LOGNAME": os.environ.get("LOGNAME", os.environ.get("USER", "kogen")),
            "SHELL": "/bin/sh",
            "GIT_CONFIG_GLOBAL": str(self.gitconfig),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_AUTHOR_NAME": GIT_NAME,
            "GIT_AUTHOR_EMAIL": GIT_EMAIL,
            "GIT_COMMITTER_NAME": GIT_NAME,
            "GIT_COMMITTER_EMAIL": GIT_EMAIL,
            "KOGEN_CREDENTIAL_STORE": "file",
            "KOGEN_TIME_SCALE": str(self.case_time_scale),
        }
        env.update(implementation_environment())
        if self.fake:
            env["KOGEN_PROVIDER_URL"] = self.fake.url + "/v1/responses"
            env["KOGEN_AUTH_URL"] = self.fake.url
            auth_mode = self.case.get("auth", "injected")
            if auth_mode == "injected":
                env["KOGEN_AUTH_PATH"] = str(self.auth_path)
        for name, value in (self.case.get("env") or {}).items():
            env[name] = self._substitute(str(value))
        return self._enforce_sandbox_env(env)

    def environment(self, extra: dict[str, Any] | None = None) -> dict[str, str]:
        env = self._base_env()
        if extra:
            for name, value in extra.items():
                env[name] = self._substitute(str(value))
        return self._enforce_sandbox_env(env)

    def _enforce_sandbox_env(self, env: dict[str, str]) -> dict[str, str]:
        # Cases may add or override ordinary variables, while the isolation,
        # credential-store and Git identity guarantees stay runner-owned.
        env.update({
            "HOME": str(self.home), "TMPDIR": str(self.tmp), "TMP": str(self.tmp), "TEMP": str(self.tmp),
            "GIT_CONFIG_GLOBAL": str(self.gitconfig), "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_COUNT": "0",
            "GIT_AUTHOR_NAME": GIT_NAME, "GIT_AUTHOR_EMAIL": GIT_EMAIL,
            "GIT_COMMITTER_NAME": GIT_NAME, "GIT_COMMITTER_EMAIL": GIT_EMAIL,
            "KOGEN_CREDENTIAL_STORE": "file",
        })
        env.pop("GIT_CONFIG_PARAMETERS", None)
        for name in tuple(env):
            if name.startswith(("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_")):
                env.pop(name, None)
        return env

    def _substitute(self, value: str) -> str:
        replacements = {
            "${SANDBOX}": str(self.root), "${HOME}": str(self.home),
            "${TMPDIR}": str(self.tmp), "${CHECKOUT}": str(self.checkout),
            "${AUTH_PATH}": str(self.auth_path), "${FAKE_URL}": self.fake.url if self.fake else "",
        }
        for token, replacement in replacements.items():
            value = value.replace(token, replacement)
        return _resolve_refs(value, self.comparator.captures)

    def _init_repo(self) -> None:
        result = subprocess.run(
            ["git", "init", "--initial-branch=main", str(self.checkout)],
            cwd=self.root, env=self._base_env(), capture_output=True, text=True,
        )
        if result.returncode:
            raise CaseError(f"git init failed: {result.stderr.strip()}")
        self._git(["config", "user.name", GIT_NAME])
        self._git(["config", "user.email", GIT_EMAIL])
        self._git(["config", "commit.gpgsign", "false"])
        self._git(["config", "tag.gpgsign", "false"])
        self._git(["config", "init.defaultBranch", "main"])

    def _write_initial_files(self) -> None:
        files = self.case.get("files", {})
        if not isinstance(files, dict):
            raise CaseError(f"{self.case['id']}: files must be a JSON object")
        for name, content in files.items():
            path = self._safe_project_path(name)
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, dict) and "base64" in content:
                import base64
                path.write_bytes(base64.b64decode(content["base64"], validate=True))
            else:
                path.write_text(str(content), encoding="utf-8")

    def _initial_commit(self) -> None:
        if not self.case.get("initial_commit", False):
            return
        self._git(["add", "-A"])
        result = self._git(["commit", "-m", "Conformance fixture"], check=False)
        if result.returncode and "nothing to commit" not in result.stdout + result.stderr:
            raise CaseError(f"initial fixture commit failed: {result.stderr.strip()}")

    def _start_fake(self) -> None:
        provider = self.case.get("provider")
        if not provider:
            return
        if isinstance(provider, list):
            script = provider
            delay = 0
        elif isinstance(provider, dict):
            script = provider.get("script", [])
            delay = provider.get("stream_delay_ms", 0)
        else:
            raise CaseError(f"{self.case['id']}: provider must be an array or object")
        if not isinstance(script, list) or any(not isinstance(step, dict) for step in script):
            raise CaseError(f"{self.case['id']}: provider script must be an array of objects")
        self.fake = FakeProvider(script, delay).start()
        auth_mode = self.case.get("auth", "injected")
        if auth_mode == "injected":
            make_injected_auth(str(self.auth_path))
        elif auth_mode == "owned":
            self.fake.seed_owned_credential(str(self.home))
        elif auth_mode != "none":
            raise CaseError(f"{self.case['id']}: auth must be injected, owned, or none")

    def _safe_project_path(self, name: str) -> Path:
        path = (self.checkout / name).resolve()
        try:
            path.relative_to(self.checkout)
        except ValueError as error:
            raise CaseError(f"project path escapes checkout: {name}") from error
        return path

    def _git(self, argv: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(["git", *argv], cwd=self.checkout, env=self._base_env(),
                                capture_output=True, text=True)
        if check and result.returncode:
            raise CaseError(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
        return result

    def run_step(self, index: int, step: dict[str, Any]) -> dict[str, Any]:
        raw_argv = step.get("argv")
        if not isinstance(raw_argv, list) or not all(isinstance(arg, str) for arg in raw_argv):
            raise CaseError(f"{self.case['id']} step {index}: argv must be a list of strings")
        argv = [self._substitute(arg) for arg in raw_argv]
        env = self.environment(step.get("env"))
        timeout = min(float(step.get("timeout_s", self.case.get("timeout_s", self.timeout_s))), self.timeout_s)
        stdin = step.get("stdin")
        if "stdin_b64" in step:
            import base64
            stdin_bytes = base64.b64decode(step["stdin_b64"], validate=True)
        else:
            stdin_bytes = None if stdin is None else str(stdin).encode("utf-8")
        output_limit = int(step.get("output_limit_bytes", 2_000_000))
        command = run_process([self.kogen, *argv], cwd=self.checkout, env=env,
                              stdin=stdin_bytes, timeout_s=timeout)
        stdout_bytes, stderr_bytes = command.stdout, command.stderr
        timed_out = command.timed_out
        elapsed_ms = command.elapsed_ms
        if len(stdout_bytes) > output_limit:
            stdout_bytes = stdout_bytes[-output_limit:]
        if len(stderr_bytes) > output_limit:
            stderr_bytes = stderr_bytes[-output_limit:]
        stdout = stdout_bytes.decode("utf-8", "replace")
        stderr = stderr_bytes.decode("utf-8", "replace")
        exit_code = 124 if timed_out else int(command.returncode)
        status_rows = None
        needs_status = bool((step.get("observe") or {}).get("status_json")) or "status_rows" in (step.get("expect") or {})
        if _is_status_json(argv):
            status_rows = _parse_json_lines(stdout)
        elif needs_status:
            status_run = run_process([self.kogen, "status", "--json"], cwd=self.checkout, env=env,
                                     timeout_s=timeout)
            status_rows = _parse_json_lines(status_run.stdout.decode("utf-8", "replace"))
            if status_run.returncode != 0:
                self.failures.append(f"step {index}: observation command kogen status --json exited {status_run.returncode}: {status_run.stderr.decode('utf-8', 'replace').strip()}")
        result = {
            "index": index, "argv": argv, "exit": exit_code, "stdout": stdout,
            "stderr": stderr, "elapsed_ms": elapsed_ms, "timed_out": timed_out,
        }
        if status_rows is not None:
            result["status_rows"] = status_rows
        expected = step.get("expect") or {}
        if "exit" in expected:
            self.failures.extend(self.comparator.compare(exit_code, expected["exit"], f"step {index}.exit"))
        for key, actual in (("stdout", stdout), ("stderr", stderr)):
            if key in expected:
                self.failures.extend(self.comparator.compare(actual, expected[key], f"step {index}.{key}"))
        if "status_rows" in expected:
            self.failures.extend(self.comparator.compare(status_rows, expected["status_rows"], f"step {index}.status_rows"))
        observation = self._observe(step.get("observe") or {}, status_rows, env, timeout, index)
        if observation:
            result["observed"] = observation
        if "observe" in step:
            compare_spec = {key: value for key, value in step["observe"].items() if key != "status_json"}
            self.failures.extend(self.comparator.compare(observation, compare_spec, f"step {index}.observed"))
        return result

    def _observe(self, spec: dict[str, Any], status_rows: Any, env: dict[str, str], timeout: float,
                 index: int) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if "git" in spec or "head" in spec:
            snapshot = self._git_snapshot()
            if "git" in spec:
                result["git"] = {key: snapshot[key] for key in ("branch_heads", "refs")}
            if "head" in spec:
                result["head"] = snapshot["head"]
        if "files" in spec:
            file_values: dict[str, str | None] = {}
            for name in spec["files"]:
                path = self._safe_project_path(name)
                try:
                    file_values[name] = path.read_text(encoding="utf-8")
                except FileNotFoundError:
                    file_values[name] = None
                except UnicodeDecodeError:
                    file_values[name] = {"base64": _encode_base64(path.read_bytes())}  # type: ignore[assignment]
            result["files"] = file_values
        if "status_rows" in spec or spec.get("status_json"):
            if status_rows is None:
                status_run = run_process([self.kogen, "status", "--json"], cwd=self.checkout, env=env,
                                         timeout_s=timeout)
                status_rows = _parse_json_lines(status_run.stdout.decode("utf-8", "replace"))
                if status_run.returncode:
                    self.failures.append(f"step {index}: kogen status --json exited {status_run.returncode}: {status_run.stderr.decode('utf-8', 'replace').strip()}")
            result["status_rows"] = status_rows
        if "provider_requests" in spec or "provider_oauth" in spec:
            requests = self.fake.state.all_requests() if self.fake else []
            oauth = self.fake.state.all_oauth_requests() if self.fake else []
            if "provider_requests" in spec:
                result["provider_requests"] = requests
            if "provider_oauth" in spec:
                result["provider_oauth"] = oauth
        return result

    def _git_snapshot(self) -> dict[str, Any]:
        branches: dict[str, str] = {}
        refs: dict[str, str] = {}
        for line in self._git(["for-each-ref", "--format=%(refname) %(objectname)"]).stdout.splitlines():
            try:
                ref, sha = line.split(" ", 1)
            except ValueError:
                continue
            refs[ref] = sha
            if ref.startswith("refs/heads/"):
                branches[ref.removeprefix("refs/heads/")] = sha
        has_head = self._git(["rev-parse", "--verify", "HEAD"], check=False)
        if has_head.returncode:
            head: dict[str, Any] = {"sha": None, "branch": None, "subject": None,
                                    "body": None, "trailers": {}, "changed_paths": []}
        else:
            sha = has_head.stdout.strip()
            branch_result = self._git(["branch", "--show-current"], check=False)
            subject = self._git(["show", "-s", "--format=%s", "HEAD"]).stdout.rstrip("\n")
            body = self._git(["show", "-s", "--format=%B", "HEAD"]).stdout.rstrip("\n")
            # git interpret-trailers reads a commit message from stdin.
            trailers_raw = subprocess.run(["git", "interpret-trailers", "--parse"], cwd=self.checkout,
                                          env=self._base_env(), input=body, capture_output=True, text=True)
            trailers: dict[str, Any] = {}
            for line in trailers_raw.stdout.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    trailers.setdefault(key.strip(), []).append(value.strip())
            changed = self._git(["diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "HEAD"]).stdout.splitlines()
            head = {"sha": sha, "branch": branch_result.stdout.strip() or None,
                    "subject": subject, "body": body, "trailers": trailers,
                    "changed_paths": changed}
            refs["HEAD"] = sha
        return {"branch_heads": branches, "refs": refs, "head": head}

    def finish(self) -> dict[str, Any]:
        if self.fake:
            requests = self.fake.state.all_requests()
            for index, request in enumerate(requests):
                if request.get("script_error"):
                    self.failures.append(f"provider request {index + 1}: {request['script_error']}")
            provider = self.case.get("provider")
            allow_unused = bool(self.case.get("provider_allow_unconsumed", False))
            if isinstance(provider, dict):
                allow_unused = bool(provider.get("allow_unconsumed", allow_unused))
            remaining = self.fake.state.remaining()
            if remaining and not allow_unused:
                self.failures.append(f"provider script has unused response(s): {remaining}")
            if "provider_expect" in self.case:
                self.failures.extend(self.comparator.compare(requests, self.case["provider_expect"], "provider_expect"))
            if "provider_oauth_expect" in self.case:
                oauth = self.fake.state.all_oauth_requests()
                self.failures.extend(self.comparator.compare(oauth, self.case["provider_oauth_expect"], "provider_oauth_expect"))
        return {
            "kind": "case", "id": self.case["id"], "title": self.case.get("title", ""),
            "file": self.case.get("_file"), "status": "pass" if not self.failures else "fail",
            "steps": self.results, "failures": self.failures,
            "captures": self.comparator.captures,
            "provider_requests": self.fake.state.all_requests() if self.fake else [],
            "provider_oauth": self.fake.state.all_oauth_requests() if self.fake else [],
            "sandbox": str(self.root) if self.keep else None,
        }

    def close(self) -> list[str]:
        if self.closed:
            return []
        self.closed = True
        if self.fake:
            self.fake.close()
        cleanup_failures = cleanup_case_cwd(self.root)
        if not self.keep:
            shutil.rmtree(self.root, ignore_errors=True)
        return cleanup_failures


def _encode_base64(data: bytes) -> str:
    import base64
    return base64.b64encode(data).decode("ascii")


def _parse_json_lines(text: str) -> list[Any] | dict[str, Any]:
    rows = []
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as error:
            return {"parse_error": f"line {number}: {error}", "text": text}
    return rows


def _is_status_json(argv: list[str]) -> bool:
    return len(argv) >= 1 and argv[0] == "status" and "--json" in argv[1:]


def run_case(case: dict[str, Any], kogen: str, time_scale: float, keep: bool,
             timeout_s: float = 60.0, workdir: str | Path = "/tmp") -> dict[str, Any]:
    kind = case.get("_kind", "json")
    executor = CASE_EXECUTORS.get(kind)
    if kind == "quint" and executor is None:
        from .quint_runner import run_quint_case
        executor = run_quint_case
        CASE_EXECUTORS["quint"] = executor
    if kind == "gherkin" and executor is None:
        from .gherkin_runner import run_gherkin_case
        executor = run_gherkin_case
        CASE_EXECUTORS["gherkin"] = executor
    if kind != "json":
        if executor is None:
            return {"kind": "case", "id": case.get("id", "<invalid>"), "title": case.get("title", ""),
                    "file": case.get("_file"), "status": "error",
                    "failures": [f"no executor is registered for {kind} cases"], "steps": []}
        return executor(case, kogen, time_scale=time_scale, keep=keep, timeout_s=timeout_s, workdir=workdir)
    world: CaseWorld | None = None
    try:
        world = CaseWorld(case, kogen, time_scale, keep, timeout_s=timeout_s, workdir=workdir)
        for index, step in enumerate(case.get("steps", []), 1):
            try:
                result = world.run_step(index, step)
            except subprocess.TimeoutExpired as error:
                world.failures.append(f"step {index}: status observation timed out after {error.timeout}s")
                result = {"index": index, "error": str(error)}
            world.results.append(result)
        cleanup_notes = world.close()
        result = world.finish()
        if cleanup_notes:
            result["teardown_notes"] = cleanup_notes
        return result
    except Exception as error:
        if world is None:
            return {"kind": "case", "id": case.get("id", "<invalid>"), "status": "error",
                    "failures": [f"harness error: {type(error).__name__}: {error}"], "steps": []}
        world.failures.append(f"harness error: {type(error).__name__}: {error}")
        cleanup_notes = world.close()
        result = world.finish()
        if cleanup_notes:
            result["teardown_notes"] = cleanup_notes
        result["status"] = "error"
        return result
    finally:
        if world:
            world.close()


def run_cases(cases: list[dict[str, Any]], kogen: str, jobs: int = 1, time_scale: float = 0.01,
              keep: bool = False, verbose: bool = False, out_path: str = "results.jsonl",
              timeout_s: float = 60.0, workdir: str | Path = "/tmp") -> tuple[list[dict[str, Any]], int]:
    executable = os.path.realpath(kogen)
    if not os.path.isfile(executable) or not os.access(executable, os.X_OK):
        raise CaseError(f"kogen executable is missing or not executable: {executable}")
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    work_root = Path(workdir).expanduser().resolve()
    work_root.mkdir(parents=True, exist_ok=True)
    if not work_root.is_dir():
        raise CaseError(f"run workdir is not a directory: {work_root}")
    metadata = {"kind": "meta", "suite": "kogen-conformance", "suite_version": "0.1.0",
                "started": started, "kogen": executable, "time_scale": time_scale,
                "case_count": len(cases), "jobs": jobs, "timeout_s": timeout_s,
                "workdir": str(work_root)}
    try:
        with open(executable, "rb") as binary:
            metadata["implementation_sha256"] = hashlib.sha256(binary.read()).hexdigest()
    except OSError as error:
        raise CaseError(f"cannot read kogen executable: {error}") from error
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    output_lock = threading.Lock()
    with out.open("w", encoding="utf-8") as result_file:
        result_file.write(json.dumps(metadata, sort_keys=True) + "\n")
        result_file.flush()

        def save(result: dict[str, Any]) -> None:
            if "failure_classification" not in result:
                category = "suite_bug" if result.get("status") == "error" else "implementation_gap"
                failures = result.get("failures", [])
                result["failure_classification"] = {
                    "implementation_gap": failures if category == "implementation_gap" else [],
                    "spec_step_ambiguity": [],
                    "suite_bug": failures if category == "suite_bug" else [],
                }
            with output_lock:
                results.append(result)
                result_file.write(json.dumps(result, sort_keys=True, ensure_ascii=False) + "\n")
                result_file.flush()
                mark = {"pass": "PASS", "fail": "FAIL", "error": "ERR ", "blocked": "BLCK"}.get(result["status"], "ERR ")
                print(f"{mark} {result['id']}", flush=True)
                if verbose and result.get("failures"):
                    for message in result["failures"]:
                        print(f"     {message}", flush=True)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
            futures = [pool.submit(run_case, case, executable, time_scale, keep, timeout_s, work_root) for case in cases]
            for future in concurrent.futures.as_completed(futures):
                save(future.result())
        teardown_notes = cleanup_case_cwd(work_root)
        if teardown_notes:
            result_file.write(json.dumps({"kind": "teardown", "notes": teardown_notes}, sort_keys=True) + "\n")
            result_file.flush()
    return results, 0 if results and all(row["status"] == "pass" for row in results) else 1


def summary(results_path: str) -> dict[str, Any]:
    counts = {"pass": 0, "fail": 0, "error": 0, "blocked": 0}
    ids: dict[str, list[str]] = {key: [] for key in counts}
    teardown_notes: list[str] = []
    with open(results_path, encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("kind") == "teardown":
                teardown_notes.extend(row.get("notes", []))
                continue
            if row.get("kind") == "meta":
                continue
            status = row.get("status", "error")
            if status not in counts:
                status = "error"
            counts[status] += 1
            ids[status].append(row.get("id", f"line-{number}"))
    return {"counts": counts, "ids": ids, "total": sum(counts.values()),
            "teardown_notes": teardown_notes}
