"""Small language-neutral executor for the executable Gherkin suite."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import tempfile
import textwrap
import time
import urllib.parse
from pathlib import Path
from typing import Any

from .fake_provider import FakeProvider, _unsigned_jwt
from .process_control import cleanup_case_cwd, implementation_environment, kill_process_group, run_process
from .quint_runner import (
    CaptureProcess, TraceBlocked, _parse_jsonl, _process_identity,
    _same_process_identity,
)


Q = r'"((?:\\.|[^"\\])*)"'
STRING = r'((?:\\.|[^"\\])*)'
STEP_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (name, re.compile(r"\A" + pattern + r"\Z")) for name, pattern in [
        ("repo", rf'Given a temporary HOME and a Git repository on branch "{STRING}"'),
        ("committed_file", rf'Given the repository has committed file "{STRING}" containing:'),
        ("write_file", rf'Given file "{STRING}" contains:'),
        ("write_executable", rf'Given executable file "{STRING}" contains:'),
        ("provider_script", rf'Given fake provider script "{STRING}" is configured with auth "{STRING}"'),
        ("openid_script", rf'Given fake OpenID script "{STRING}" is configured'),
        ("project_check", rf'Given project check "{STRING}" returns "{STRING}" within (-?[0-9]+) milliseconds and Build budget (-?[0-9]+) milliseconds'),
        ("arm_barrier", rf'Given landing barrier "{STRING}" is armed'),
        ("clock_start", r"Given Kogen's test clock starts at (-?[0-9]+) milliseconds"),
        ("time_scale", rf'Given Kogen\'s time scale is "{STRING}"'),
        ("run_stdin", rf'When I run "{STRING}" with stdin:'),
        ("run", rf'When I run "{STRING}"'),
        ("start_background", rf'When I start "{STRING}" in the background as "{STRING}"'),
        ("wait_provider", rf'When I wait for provider script "{STRING}" at gate "{STRING}"'),
        ("release_provider", rf'When I release provider script "{STRING}" at gate "{STRING}"'),
        ("wait_barrier", rf'When I wait for landing barrier "{STRING}" as "{STRING}"'),
        ("release_barrier", rf'When I release landing barrier saved as "{STRING}"'),
        ("commit", rf'When I commit on branch "{STRING}" with subject "{STRING}" and file "{STRING}" containing:'),
        ("change_intent", rf'When I change one byte in the shaped Intent "{STRING}"'),
        ("clock_advance", r"When I advance Kogen's test clock by (-?[0-9]+) milliseconds"),
        ("kill_queue", r"When I kill the trace-owned detached Kogen queue process"),
        ("exit", r"Then the exit code is (-?[0-9]+)"),
        ("stdout_contains", rf'Then stdout contains "{STRING}"'),
        ("check_count", rf'Then project check "{STRING}" ran at least (-?[0-9]+) times'),
        ("approval_hash", rf'Then stdout captures the Intent approval hash as "{STRING}"'),
        ("file_exact", rf'Then the file "{STRING}" contains:'),
        ("file_absent", rf'Then the file "{STRING}" is absent'),
        ("file_includes", rf'Then the file "{STRING}" includes text "{STRING}"'),
        ("branch_subject", rf'Then branch "{STRING}" has head commit subject "{STRING}"'),
        ("branch_trailer", rf'Then branch "{STRING}" has head commit with only trailer "{STRING}"'),
        ("last_commit_paths", r"Then the last commit changes exactly:"),
        ("git_ignores", rf'Then Git ignores path "{STRING}"'),
        ("git_not_ignores", rf'Then Git does not ignore path "{STRING}"'),
        ("no_commit", r"Then there is no new commit"),
        ("status_intent", rf'Then "{STRING}" JSONL output has an intent row with status "{STRING}"'),
        ("background_frame", rf'Then background command "{STRING}" prints a frame containing "{STRING}"'),
        ("background_exit", rf'Then background command "{STRING}" eventually exits with code (-?[0-9]+)'),
        ("status_recovery", r"Then the latest status output reports a failed or interrupted intent with preserved unverified recovery and an expiry"),
        ("recovery_expired", r"Then status confirms expired recovery is removed and deletion is journaled"),
        ("account_paths", r"Then provider account choices are under temporary HOME and absent from repository"),
    ]
)


class FeatureInputError(Exception):
    """Malformed Gherkin or fixture configuration."""


class FeatureBlocked(Exception):
    """A documented operation cannot be verified on this host."""


def _decode_string(value: str) -> str:
    try:
        return json.loads('"' + value + '"')
    except json.JSONDecodeError as error:
        raise FeatureInputError(f"invalid Gherkin string parameter: {error}") from error


def _scenario_slug(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "scenario"


def load_feature_cases(feature_dirs: list[Path]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for directory in feature_dirs:
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.feature")):
            cases.extend(_parse_feature(path, directory))
    return cases


def _parse_feature(path: Path, root: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as error:
        raise FeatureInputError(f"cannot read feature {path}: {error}") from error
    relative = path.relative_to(root).with_suffix("").as_posix()
    file_id = relative.replace("/", ".")
    feature_tags: list[str] = []
    pending_tags: list[str] = []
    feature_title = path.stem
    current: dict[str, Any] | None = None
    cases: list[dict[str, Any]] = []
    index = 0
    while index < len(lines):
        raw = lines[index]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            index += 1
            continue
        if stripped.startswith("@"):
            pending_tags.extend(stripped.split())
            index += 1
            continue
        if stripped.startswith("Feature:"):
            feature_title = stripped[len("Feature:"):].strip()
            feature_tags = list(dict.fromkeys(pending_tags))
            pending_tags.clear()
            index += 1
            continue
        if stripped.startswith("Scenario:"):
            if current is not None:
                cases.append(current)
            title = stripped[len("Scenario:"):].strip()
            tags = list(dict.fromkeys(feature_tags + pending_tags))
            pending_tags.clear()
            current = {
                "id": f"feature.{file_id}.{_scenario_slug(title)}",
                "title": title,
                "file": str(path),
                "feature": feature_title,
                "tags": tags,
                "_file": str(path),
                "_kind": "gherkin",
                "_feature_steps": [],
            }
            index += 1
            continue
        if current is None:
            # Rule/Background/Examples are outside this suite vocabulary.
            if stripped.startswith(("Background:", "Rule:", "Scenario Outline:", "Examples:")):
                raise FeatureInputError(f"{path}:{index + 1}: unsupported Gherkin construct {stripped.split(':', 1)[0]}")
            index += 1
            continue
        step_match = re.match(r"^(Given|When|Then|And|But)\s+(.+)$", stripped)
        if step_match:
            keyword, text = step_match.groups()
            doc = None
            next_index = index + 1
            if next_index < len(lines) and lines[next_index].strip() in ('"""', "```"):
                marker = lines[next_index].strip()
                opening_indent = len(lines[next_index]) - len(lines[next_index].lstrip(" "))
                next_index += 1
                payload: list[str] = []
                while next_index < len(lines) and lines[next_index].strip() != marker:
                    row = lines[next_index]
                    prefix = " " * opening_indent
                    payload.append(row[opening_indent:] if row.startswith(prefix) else row)
                    next_index += 1
                if next_index >= len(lines):
                    raise FeatureInputError(f"{path}:{index + 1}: unterminated doc string")
                doc = "\n".join(payload) + ("\n" if payload else "")
                next_index += 1
            current["_feature_steps"].append({
                "keyword": keyword, "text": text, "docstring": doc, "line": index + 1,
            })
            index = next_index
            continue
        if stripped.startswith(("Background:", "Rule:", "Scenario Outline:", "Examples:")):
            raise FeatureInputError(f"{path}:{index + 1}: unsupported Gherkin construct {stripped.split(':', 1)[0]}")
        index += 1
    if current is not None:
        cases.append(current)
    if not cases:
        raise FeatureInputError(f"{path}: no Scenario blocks found")
    return cases


def _match_step(step: dict[str, Any]) -> tuple[str, list[str]]:
    text = step["text"]
    keyword = step["keyword"]
    prefixes = [keyword] if keyword in {"Given", "When", "Then"} else ["Given", "When", "Then"]
    for prefix in prefixes:
        full_text = f"{prefix} {text}"
        for name, pattern in STEP_PATTERNS:
            match = pattern.fullmatch(full_text)
            if match:
                values = [match.group(number) for number in range(1, pattern.groups + 1)]
                return name, values
    raise FeatureInputError(f"unimplemented STEPS.md pattern: {text}")


def _tool_call(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    return {"name": name, "arguments": arguments}


def _intent_content(slug: str = "farewell", title: str = "Create goodbye.txt",
                    source_acceptance: bool = False) -> str:
    acceptance = "\n## Acceptance\n- A1: goodbye.txt contains exactly Goodbye.\n\n## Verify\n- A1: test domain=app\n"
    if source_acceptance:
        acceptance = "\n## Acceptance\n- A1: farewell_message returns Goodbye.\n\n## Verify\n- A1: test domain=app\n"
    return (
        f"---\ntitle: {title}\nsize: small\ndomains: [app]\n---\n"
        "Create goodbye.txt containing exactly Goodbye.\n" + acceptance +
        "\n## Notes\nApproach: Use the project root file-creation path to add goodbye.txt with Goodbye while preserving unrelated files.\n"
    )


def _script_fixture(script_id: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    shaper = {"role": "shaper"}
    builder = {"role": "builder"}
    auditor = {"role": "auditor"}
    intent = _intent_content()
    if script_id in {"basic-farewell", "research-account-shape"}:
        script = [{"expect": shaper, "tool_calls": [_tool_call("write", {
            "path": ".kogen/intents/farewell/intent.md", "content": intent,
        })], "assistant_text": "The Intent is ready."}]
        contract = {"min": 1, "max": 1, "role": "shaper", "model": "gpt-6.1-sol",
                    "effort": "high", "tools": ["read", "search", "write"],
                    "input": "Write goodbye.txt with Goodbye."}
        if script_id == "research-account-shape":
            contract["account_id"] = "acct-research"
        return script, contract
    if script_id == "farewell-questions":
        return ([{"expect": shaper, "assistant_text":
                  "What tone should the goodbye use? Please choose a tone before I create an Intent."}],
                {"min": 1, "max": 1, "role": "shaper", "model": "gpt-6.1-sol",
                 "effort": "high", "tools": ["read", "search", "write"], "input": "tone"})
    if script_id == "cargo-farewell":
        source = (
            "use greeter::farewell_message;\n#[test]\nfn acceptance_a1() {\n"
            "    assert_eq!(farewell_message(), \"Goodbye\");\n}\n"
        )
        return ([{"expect": shaper, "tool_calls": [
            _tool_call("write", {"path": ".kogen/intents/farewell/intent.md",
                                  "content": _intent_content(title="Create farewell_message", source_acceptance=True)}),
            _tool_call("write", {"path": ".kogen/local/acceptance/farewell.rs", "content": source}),
        ], "assistant_text": "The Intent and acceptance source are ready."}],
                {"min": 1, "max": 1, "role": "shaper", "model": "gpt-6.1-sol",
                 "effort": "high", "tools": ["read", "search", "write"],
                 "input": "Write goodbye.txt with Goodbye."})
    if script_id == "no-provider-turns":
        return [], {"min": 0, "max": 0, "role": None, "model": None, "effort": None}
    if script_id in {"farewell-build", "farewell-build-held", "farewell-build-delayed", "farewell-build-crash"}:
        second: dict[str, Any] = {"expect": builder, "tool_calls": [_tool_call("finish", {})]}
        if script_id == "farewell-build-held":
            second["gate"] = "builder-next-turn"
        elif script_id == "farewell-build-crash":
            second["gate"] = "crash-after-edit"
        elif script_id == "farewell-build-delayed":
            second["delay_ms"] = 3000
        return ([
            {"expect": builder, "tool_calls": [_tool_call("shell", {"cmd": "printf Goodbye > goodbye.txt"})]},
            second,
        ], {"min": 2, "max": 2, "role": "builder", "model": "gpt-6-luna", "effort": "max",
            "tools": ["shell", "finish"]})
    if script_id == "farewell-build-hook":
        return ([
            {"expect": builder, "tool_calls": [_tool_call("shell", {"cmd": "printf Goodbye > goodbye.txt"})]},
            {"expect": builder, "tool_calls": [_tool_call("finish", {})]},
            {"expect": builder, "assistant_text": "The commit hook failed; no safe candidate repair is available."},
        ], {"min": 3, "max": 3, "role": "builder", "model": "gpt-6-luna", "effort": "max",
            "tools": ["shell", "finish"]})
    raise FeatureInputError(f"unknown fake provider script id {script_id!r} from FAKES.md")


class GherkinWorld:
    def __init__(self, case: dict[str, Any], kogen: str, timeout_s: float, keep: bool,
                 workdir: str | Path = "/tmp"):
        self.case = case
        self.kogen = str(Path(kogen).resolve())
        self.timeout_s = timeout_s
        self.keep = keep
        self.root = Path(tempfile.mkdtemp(prefix="kc2-feature-", dir=str(workdir))).resolve()
        self.home = self.root / "home"
        self.tmp = self.root / "tmp"
        self.repo = self.root / "repo"
        self.bin = self.root / "bin"
        self.control = self.root / "control"
        self.gitconfig = self.home / ".gitconfig"
        self.auth_path = self.root / "auth.json"
        self.fake: FakeProvider | None = None
        self.branch: str | None = None
        self.time_scale = "0.01"
        self.clock_path: Path | None = None
        self.barrier_dir: Path | None = None
        self.barriers: dict[str, dict[str, Any]] = {}
        self.captures: dict[str, str] = {}
        self.background: dict[str, CaptureProcess] = {}
        self.background_meta: dict[str, dict[str, Any]] = {}
        self.all_processes: list[CaptureProcess] = []
        self.pending_provider: tuple[str, dict[str, Any]] | None = None
        self.pending_openid: str | None = None
        self.pending_openid_oauth_index = 0
        self.current_auth = "absent"
        self.oauth_scripts: list[str] = []
        self.provider_transcripts: list[dict[str, Any]] = []
        self.results: list[dict[str, Any]] = []
        self.failure_records: list[dict[str, Any]] = []
        self.blocked_reasons: list[str] = []
        self.last_result: dict[str, Any] | None = None
        self.last_status: dict[str, Any] | None = None
        self.last_shape_intent_path: str | None = None
        self.last_command_before_ref: tuple[str, str | None] | None = None
        self.last_queue_launch_wall: float | None = None
        self.recovery_record: dict[str, Any] | None = None
        self.closed = False
        for directory in (self.home, self.tmp, self.repo, self.bin, self.control):
            directory.mkdir(parents=True, exist_ok=True)
        self.gitconfig.write_text(
            "[user]\n\tname = Kogen Conformance\n\temail = conformance@kogen.invalid\n"
            "[init]\n\tdefaultBranch = main\n[commit]\n\tgpgsign = false\n"
            "[tag]\n\tgpgsign = false\n[core]\n\tpager = cat\n\tquotepath = false\n"
            "[advice]\n\tdetachedHead = false\n", encoding="utf-8")
        self.gitconfig.chmod(0o600)

    def fail(self, message: str, category: str = "implementation_gap", line: int | None = None) -> None:
        record = {"message": message, "classification": category}
        if line is not None:
            record["line"] = line
        self.failure_records.append(record)

    def _ensure_fake(self) -> FakeProvider:
        if self.fake is None:
            self.fake = FakeProvider([]).start()
        return self.fake

    def _base_env(self) -> dict[str, str]:
        implementation_env = implementation_environment(self.bin)
        env = {
            "HOME": str(self.home), "TMPDIR": str(self.tmp), "TMP": str(self.tmp), "TEMP": str(self.tmp),
            "XDG_CONFIG_HOME": str(self.home / ".config"), **implementation_env,
            "LANG": "C.UTF-8", "LC_ALL": "C", "TZ": "UTC", "NO_COLOR": "1", "TERM": "dumb",
            "USER": os.environ.get("USER", "kogen"), "LOGNAME": os.environ.get("LOGNAME", "kogen"),
            "SHELL": "/bin/sh", "GIT_CONFIG_GLOBAL": str(self.gitconfig), "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_COUNT": "0", "GIT_TERMINAL_PROMPT": "0",
            "GIT_AUTHOR_NAME": "Kogen Conformance", "GIT_AUTHOR_EMAIL": "conformance@kogen.invalid",
            "GIT_COMMITTER_NAME": "Kogen Conformance", "GIT_COMMITTER_EMAIL": "conformance@kogen.invalid",
            "KOGEN_CREDENTIAL_STORE": "file", "KOGEN_TIME_SCALE": self.time_scale,
            "KOGEN_PROVIDER_URL": "http://127.0.0.1:1/disabled/responses",
        }
        if self.fake is not None:
            env["KOGEN_AUTH_URL"] = self.fake.url
        if self.current_auth in {"valid", "expired", "malformed"}:
            env["KOGEN_AUTH_PATH"] = str(self.auth_path)
        else:
            env.pop("KOGEN_AUTH_PATH", None)
        if self.pending_provider and self.fake:
            script_id, _contract = self.pending_provider
            env["KOGEN_PROVIDER_URL"] = f"{self.fake.url}/scripts/{urllib.parse.quote(script_id, safe='')}/responses"
        if self.pending_openid and self.fake:
            env["KOGEN_AUTH_URL"] = self.fake.url
            env.pop("KOGEN_AUTH_PATH", None)
        if self.clock_path:
            env["KOGEN_TEST_CLOCK_PATH"] = str(self.clock_path)
        if self.barrier_dir:
            env["KOGEN_TEST_BARRIER_DIR"] = str(self.barrier_dir)
        env.pop("GIT_CONFIG_PARAMETERS", None)
        for name in list(env):
            if name.startswith(("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_")):
                env.pop(name, None)
        return env

    def _git(self, args: list[str], check: bool = True, cwd: Path | None = None,
             input_text: str | None = None) -> subprocess.CompletedProcess[str]:
        if self.branch is None and args[:1] != ["init"]:
            raise FeatureInputError("Git fixture used before temporary repository setup")
        result = subprocess.run(["git", *args], cwd=str(cwd or self.repo), env=self._base_env(),
                                input=input_text, capture_output=True, text=True, timeout=10)
        if check and result.returncode != 0:
            raise FeatureInputError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
        return result

    def _repo_setup(self, branch: str) -> None:
        self.branch = branch
        result = subprocess.run(["git", "init", "--initial-branch", branch, str(self.repo)],
                                cwd=self.root, env=self._base_env(), capture_output=True,
                                text=True, timeout=10)
        if result.returncode:
            raise FeatureInputError(f"git init failed: {result.stderr.strip()}")
        for name, value in (("user.name", "Kogen Conformance"), ("user.email", "conformance@kogen.invalid"),
                            ("commit.gpgsign", "false"), ("tag.gpgsign", "false")):
            self._git(["config", name, value])
        self._ensure_fake()

    def _feature_path(self, value: str) -> Path:
        path = self.home / value[2:] if value.startswith("~/") else self.repo / value
        resolved = path.resolve(strict=False)
        try:
            resolved.relative_to(self.root)
        except ValueError as error:
            raise FeatureInputError(f"fixture path escapes the scenario directory: {value}") from error
        return resolved

    def _write_file(self, value: str, content: str, executable: bool = False) -> Path:
        path = self._feature_path(value)
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_name(path.name + f".tmp-{os.getpid()}-{time.time_ns()}")
        temp.write_bytes(content.encode("utf-8"))
        if executable:
            temp.chmod(0o755)
        os.replace(temp, path)
        return path

    def _commit_fixture(self, branch: str, subject: str, name: str, content: str) -> None:
        self._git(["switch", branch])
        path = self._write_file(name, content)
        relative = path.relative_to(self.repo).as_posix()
        self._git(["add", "--", relative])
        commit = self._git(["commit", "-m", subject], check=False)
        if commit.returncode != 0:
            raise FeatureInputError(f"fixture git commit failed: {commit.stderr.strip() or commit.stdout.strip()}")

    def _make_auth(self, mode: str) -> None:
        self.current_auth = mode
        if mode == "absent":
            self.auth_path.unlink(missing_ok=True)
            return
        if mode == "malformed":
            self.auth_path.write_bytes(b"{ definitely not JSON")
            self.auth_path.chmod(0o600)
            return
        wall = int(time.time())
        if self.clock_path:
            try:
                test_wall = json.loads(self.clock_path.read_text(encoding="utf-8"))["now_ms"] // 1000
                # Auth validation may use the system wall clock even when Kogen's
                # behavioral clock is injected. Keep valid fixtures valid in both
                # domains, and expired fixtures expired in both.
                wall = max(wall, test_wall)
            except (OSError, KeyError, json.JSONDecodeError, TypeError):
                pass
        expiry = wall + 3600 if mode == "valid" else wall - 1
        claims = {
            "iss": "https://auth.openai.com", "sub": "kogen-conformance-user",
            "iat": max(0, wall - 1), "exp": expiry,
            "https://api.openai.com/auth": {"chatgpt_account_id": "acct-test", "chatgpt_plan_type": "plus"},
        }
        self.auth_path.write_text(json.dumps({"tokens": {
            "access_token": _unsigned_jwt(claims), "account_id": "acct-test",
        }}), encoding="utf-8")
        self.auth_path.chmod(0o600)

    def _configure_provider(self, script_id: str, auth: str) -> None:
        valid_auth = {"valid", "expired", "malformed", "absent"}
        if auth not in valid_auth:
            raise FeatureInputError(f"unknown auth mode {auth!r}; expected valid, expired, malformed, or absent")
        server = self._ensure_fake()
        self._make_auth(auth)
        script, contract = _script_fixture(script_id)
        server.configure_script(script_id, script)
        self.pending_provider = (script_id, contract)

    def _configure_openid(self, script_id: str) -> None:
        accounts = {
            "login-default": ("acct-default", "default"),
            "login-research": ("acct-research", "research"),
            "logout-research": ("acct-research", "research"),
        }
        if script_id not in accounts:
            raise FeatureInputError(f"unknown OpenID script id {script_id!r} from FAKES.md")
        account_id, label = accounts[script_id]
        self._ensure_fake().configure_openid(script_id, account_id, label)
        self.current_auth = "absent"
        self.auth_path.unlink(missing_ok=True)
        self.pending_openid = script_id
        self.pending_openid_oauth_index = len(self.fake.state.all_oauth_requests())
        if not (self.bin / "open").exists():
            shim = (
                "#!/usr/bin/env python3\n"
                "import sys, urllib.request\n"
                "if len(sys.argv) != 2: raise SystemExit(2)\n"
                "try:\n    urllib.request.urlopen(sys.argv[1], timeout=5).read()\n"
                "except Exception as error:\n    print(error, file=sys.stderr); raise SystemExit(1)\n"
            )
            open_path = self.bin / "open"
            open_path.parent.mkdir(parents=True, exist_ok=True)
            open_path.write_text(shim, encoding="utf-8")
            open_path.chmod(0o755)
            for alias in ("xdg-open", "sensible-browser"):
                alias_path = self.bin / alias
                alias_path.write_text(shim, encoding="utf-8")
                alias_path.chmod(0o755)

    def _finalize_provider(self) -> None:
        if self.pending_provider is None:
            return
        script_id, contract = self.pending_provider
        assert self.fake is not None
        requests = self.fake.state.all_requests()
        errors = []
        if not contract["min"] <= len(requests) <= contract["max"]:
            errors.append(f"script {script_id}: expected {contract['min']}..{contract['max']} provider request(s), got {len(requests)}")
        remaining = self.fake.state.remaining()
        if remaining:
            errors.append(f"script {script_id}: unused response(s) remain: {remaining}")
        for index, request in enumerate(requests, 1):
            if request.get("script_error"):
                errors.append(f"script {script_id} request {index}: {request['script_error']}")
            if contract.get("role") and request.get("role") != contract["role"]:
                errors.append(f"script {script_id} request {index}: role expected {contract['role']}, got {request.get('role')}")
            body = request.get("body") if isinstance(request.get("body"), dict) else {}
            if contract.get("model") and body.get("model") != contract["model"]:
                errors.append(f"script {script_id} request {index}: model expected {contract['model']}, got {body.get('model')}")
            reasoning = body.get("reasoning") if isinstance(body.get("reasoning"), dict) else {}
            if contract.get("effort") and reasoning.get("effort") != contract["effort"]:
                errors.append(f"script {script_id} request {index}: effort expected {contract['effort']}, got {reasoning.get('effort')}")
            missing_tools = sorted(set(contract.get("tools", [])) - set(request.get("tools", [])))
            if missing_tools:
                errors.append(f"script {script_id} request {index}: permitted tool(s) missing: {missing_tools}")
            required = contract.get("input")
            if required and required.lower() not in _provider_input_text(body).lower():
                errors.append(f"script {script_id} request {index}: required request text {required!r} is absent")
            if contract.get("account_id"):
                header_text = json.dumps(request.get("headers", {}), sort_keys=True)
                if contract["account_id"] not in header_text and "kogen-fake-access-research" not in header_text:
                    errors.append(f"script {script_id} request {index}: selected account identity {contract['account_id']} is absent")
        for error in errors:
            self.fail(error, "implementation_gap")
        self.provider_transcripts.append({"script": script_id, "requests": requests,
                                          "expected": {key: value for key, value in contract.items()}})
        self.pending_provider = None

    def _finalize_openid(self) -> None:
        if self.pending_openid is None:
            return
        script_id = self.pending_openid
        assert self.fake is not None
        oauth = self.fake.state.all_oauth_requests()[self.pending_openid_oauth_index:]
        if script_id.startswith("login-"):
            auth_codes = [item for item in oauth if item.get("form", {}).get("grant_type") == ["authorization_code"]]
            if len(auth_codes) != 1:
                self.fail(f"OpenID script {script_id}: expected one authorization-code exchange, got {len(auth_codes)}",
                          "implementation_gap")
            authorization = self.fake.state.oidc_authorization or {}
            if not all(authorization.get(key) for key in ("state", "nonce", "code_challenge", "redirect_uri")):
                self.fail(f"OpenID script {script_id}: authorization omitted state, nonce, PKCE, or callback",
                          "implementation_gap")
        else:
            if not any(item.get("path") == "/revoke" for item in oauth):
                self.fail(f"OpenID script {script_id}: expected a revocation exchange", "implementation_gap")
        self.oauth_scripts.append(script_id)
        self.pending_openid = None

    def _before_ref(self) -> tuple[str, str | None] | None:
        if self.branch is None:
            return None
        ref = f"refs/heads/{self.branch}"
        result = self._git(["rev-parse", "--verify", ref], check=False)
        return ref, result.stdout.strip() if result.returncode == 0 else None

    def _expand_command(self, command: str) -> list[str]:
        words = re.split(r"[\x20\t\n\r\f\v]+", command.strip()) if command.strip() else []
        argv: list[str] = []
        for word in words:
            if word == "kogen":
                argv.append(self.kogen)
            elif word == "@repo":
                argv.append(str(self.repo))
            elif word == "@home":
                argv.append(str(self.home))
            else:
                def capture(match: re.Match[str]) -> str:
                    name = match.group(1)
                    if name not in self.captures:
                        raise FeatureInputError(f"unknown capture {name!r} in command")
                    return self.captures[name]
                argv.append(re.sub(r"\{\{([A-Za-z_][A-Za-z0-9_.-]*)\}\}", capture, word))
        if not argv:
            raise FeatureInputError("Kogen command line is empty")
        return argv

    def run_command(self, command: str, stdin: str | None = None) -> dict[str, Any]:
        argv = self._expand_command(command)
        if Path(argv[0]) != Path(self.kogen):
            raise FeatureInputError("command line must begin with the reserved kogen executable")
        before = self._before_ref()
        env = self._base_env()
        started_wall = time.time()
        if len(argv) > 1 and argv[1:3] == ["queue", "start"]:
            self.last_queue_launch_wall = started_wall
        completed = run_process(argv, cwd=self.repo, env=env,
                                stdin=None if stdin is None else stdin.encode("utf-8"),
                                timeout_s=self.timeout_s)
        exit_code = completed.returncode
        if exit_code < 0:
            exit_code = 128 + -exit_code
        stdout = completed.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
        stderr = completed.stderr.decode("utf-8", "replace").replace("\r\n", "\n")
        result = {
            "argv": argv, "exit": exit_code, "stdout": stdout, "stderr": stderr,
            "elapsed_ms": completed.elapsed_ms, "timed_out": completed.timed_out,
            "started_wall": started_wall, "cwd": str(self.repo),
        }
        self.last_result = result
        self.last_command_before_ref = before
        if completed.timed_out:
            self.fail(f"kogen invocation exceeded the hard {self.timeout_s:g}s timeout: {' '.join(argv[1:])}",
                      "implementation_gap")
        if len(argv) > 1 and argv[1] == "status":
            self.last_status = result
            if "--json" in argv[2:]:
                rows, error = _parse_jsonl(completed.stdout)
                result["json_rows"] = rows
                if error:
                    self.fail(f"status JSONL parse failed: {error}")
                elif isinstance(rows, list):
                    schema_errors = _validate_core_status_rows(rows)
                    for message in schema_errors:
                        self.fail("status JSONL schema: " + message)
        if len(argv) > 2 and argv[1:3] == ["intent", "shape"]:
            matches = re.findall(r"(?:\.kogen/)?intents/[A-Za-z0-9_.-]+/intent\.md", stdout)
            if len(set(matches)) == 1:
                self.last_shape_intent_path = matches[0] if matches[0].startswith(".kogen/") else "." + matches[0]
            elif matches:
                self.last_shape_intent_path = None
        self.results.append({"kind": "command", **result})
        self._finalize_provider()
        self._finalize_openid()
        return result

    def _status_json(self, command: str) -> list[dict[str, Any]]:
        result = self.run_command(command)
        rows = result.get("json_rows")
        if not isinstance(rows, list):
            self.fail(f"{command!r} did not produce valid JSONL status rows")
            return []
        return rows

    def _git_head(self, branch: str) -> tuple[str | None, str | None]:
        sha = self._git(["rev-parse", "--verify", f"refs/heads/{branch}"], check=False)
        if sha.returncode:
            return None, None
        subject = self._git(["show", "-s", "--format=%s", f"refs/heads/{branch}"]).stdout.rstrip("\n")
        return sha.stdout.strip(), subject

    def _run_step(self, step: dict[str, Any]) -> None:
        name, raw_values = _match_step(step)
        values = [_decode_string(value) if not value.lstrip("-").isdigit() else value for value in raw_values]
        doc = step.get("docstring")
        line = step.get("line")
        if name == "repo":
            if self.branch is not None:
                raise FeatureInputError("temporary HOME and repository may be initialized only once per scenario")
            self._repo_setup(values[0])
            return
        if name == "committed_file":
            if not doc:
                raise FeatureInputError("committed fixture file step requires a doc string")
            path = self._write_file(values[0], doc)
            self._git(["add", "--", path.relative_to(self.repo).as_posix()])
            commit = self._git(["commit", "-m", "Conformance fixture"], check=False)
            if commit.returncode:
                raise FeatureInputError(f"fixture commit failed: {commit.stderr.strip()}")
            return
        if name in {"write_file", "write_executable"}:
            if doc is None:
                raise FeatureInputError("file fixture step requires a doc string")
            self._write_file(values[0], doc, executable=(name == "write_executable"))
            return
        if name == "provider_script":
            self._configure_provider(values[0], values[1])
            return
        if name == "openid_script":
            self._configure_openid(values[0])
            return
        if name == "project_check":
            check_name, result_mode = values[0], values[1]
            timeout_ms, budget_ms = int(values[2]), int(values[3])
            if result_mode not in {"pass", "red", "timeout"} or timeout_ms <= 0 or budget_ms <= 0:
                raise FeatureInputError("project check requires pass/red/timeout and positive millisecond bounds")
            check_dir = self.repo / ".kogen" / "conformance"
            check_dir.mkdir(parents=True, exist_ok=True)
            counter = self.control / f"check-{check_name}.count"
            script_path = check_dir / f"check-{check_name}.py"
            code = (
                "#!/usr/bin/env python3\nimport pathlib, sys, time\n"
                f"counter = pathlib.Path({str(counter)!r})\n"
                "counter.parent.mkdir(parents=True, exist_ok=True)\n"
                "try: count = int(counter.read_text())\nexcept (OSError, ValueError): count = 0\n"
                "counter.write_text(str(count + 1))\n"
            )
            if result_mode == "timeout":
                code += f"time.sleep({max(2.0, timeout_ms / 1000.0 + 1.0)!r})\n"
            elif result_mode == "red":
                code += "print('contract check failed', file=sys.stderr)\nsys.exit(1)\n"
            else:
                code += "print('contract check passed')\n"
            script_path.write_text(code, encoding="utf-8")
            script_path.chmod(0o755)
            command_path = "./" + script_path.relative_to(self.repo).as_posix()
            config = (
                "name: project\nchecks:\n"
                f"  - name: {check_name}\n    argv: [{json.dumps(command_path)}]\n"
                f"    timeout_ms: {timeout_ms}\n"
                "domains:\n  app: [\"goodbye.txt\", \"src/**\"]\n"
                "build:\n"
                f"  budget_ms: {budget_ms}\n"
                "  roles:\n    builder:\n      model: gpt-6-luna\n      effort: max\n"
                "sandbox: false\n"
            )
            cfg = self.repo / ".kogen" / "project.yaml"
            cfg.parent.mkdir(parents=True, exist_ok=True)
            cfg.write_text(config, encoding="utf-8")
            self._git(["add", "--", ".kogen/project.yaml", script_path.relative_to(self.repo).as_posix()])
            commit = self._git(["commit", "-m", "Conformance check fixture"], check=False)
            if commit.returncode:
                raise FeatureInputError(f"project check fixture commit failed: {commit.stderr.strip()}")
            return
        if name == "arm_barrier":
            if self.barrier_dir is None:
                self.barrier_dir = self.control / "barriers"
                self.barrier_dir.mkdir(parents=True, exist_ok=True)
            arm = self.barrier_dir / (values[0] + ".arm")
            arm.write_bytes(b"armed\n")
            return
        if name == "clock_start":
            now_ms = int(values[0])
            if now_ms < 0:
                raise FeatureInputError("test clock must be nonnegative")
            self.clock_path = self.control / "clock.json"
            self._atomic_write(self.clock_path, json.dumps({"now_ms": now_ms}).encode(), 0o600)
            return
        if name == "time_scale":
            scale = float(values[0])
            if not (scale > 0 and scale < float("inf")):
                raise FeatureInputError("Kogen time scale must be positive and finite")
            self.time_scale = values[0]
            return
        if name in {"run", "run_stdin"}:
            self.run_command(values[0], doc if name == "run_stdin" else None)
            return
        if name == "start_background":
            handle = values[1]
            if handle in self.background:
                raise FeatureInputError(f"background handle {handle!r} is already registered")
            argv = self._expand_command(values[0])
            if Path(argv[0]) != Path(self.kogen):
                raise FeatureInputError("background command must begin with kogen")
            before = self._before_ref()
            started_wall = time.time()
            process = CaptureProcess.start(argv, str(self.repo), self._base_env(), b"",
                                           int(self.timeout_s * 1000))
            self.background[handle] = process
            self.all_processes.append(process)
            self.background_meta[handle] = {
                "argv": argv, "cwd": str(self.repo), "started_wall": started_wall,
                "started": process.started, "before_ref": before,
            }
            self.results.append({"kind": "background-start", "handle": handle, "argv": argv,
                                 "pid": process.process.pid, "started_wall": started_wall})
            return
        if name in {"wait_provider", "release_provider"}:
            if not self.fake:
                raise FeatureInputError("provider gate used before a fake provider was configured")
            if name == "wait_provider":
                failed_launch = self._failed_background_queue_launch()
                if failed_launch is not None:
                    self.fail(f"provider gate {values[0]}/{values[1]} cannot be reached because background queue command exited {failed_launch}",
                              "implementation_gap", line)
                    self._finalize_provider()
                    return
            operation_ok = (self.fake.wait_gate(values[0], values[1], self.timeout_s)
                            if name == "wait_provider" else self.fake.release_gate(values[0], values[1]))
            if not operation_ok:
                self.fail(f"provider gate {values[0]}/{values[1]} was not reached or did not exist", "implementation_gap", line)
            elif name == "wait_provider" and self.pending_provider and self.pending_provider[0] == values[0]:
                self._finalize_provider()
            return
        if name == "wait_barrier":
            if self.last_result is not None and self.last_result.get("exit", 0) != 0:
                self.fail(f"landing barrier {values[0]!r} cannot be reached because the preceding Kogen command exited {self.last_result['exit']}",
                          "implementation_gap", line)
                return
            failed_launch = self._failed_background_queue_launch()
            if failed_launch is not None:
                self.fail(f"landing barrier {values[0]!r} cannot be reached because background queue command exited {failed_launch}",
                          "implementation_gap", line)
                return
            try:
                binding, record = self._await_barrier(values[0], self.timeout_s)
            except FeatureInputError as error:
                self.fail(str(error), "implementation_gap", line)
                return
            name_binding = values[1]
            if name_binding in self.barriers:
                raise FeatureInputError(f"barrier binding {name_binding!r} is already used")
            self.barriers[name_binding] = record
            self.results.append({"kind": "barrier", "binding": name_binding, "point": binding,
                                 "ticket": record})
            return
        if name == "release_barrier":
            binding = values[0]
            if binding not in self.barriers:
                self.fail(f"landing barrier binding {binding!r} was never reached", "implementation_gap", line)
                return
            record = self.barriers[binding]
            arrival = Path(record["_path"])
            release_path = Path(record["release_path"]) if record.get("release_path") else arrival.with_suffix(".release")
            self._atomic_write(release_path, b"release\n", 0o600)
            return
        if name == "commit":
            self._commit_fixture(values[0], values[1], values[2], doc or "")
            return
        if name == "change_intent":
            if values[0] != "farewell":
                raise FeatureInputError(f"unknown shaped Intent slug {values[0]!r}")
            if not self.last_shape_intent_path:
                self.fail("most recent shape output did not report one Intent file path", "implementation_gap", line)
                return
            path = self._feature_path(self.last_shape_intent_path)
            if not path.is_file():
                raise FeatureInputError(f"reported shaped Intent does not exist: {path}")
            path.write_bytes(path.read_bytes() + b" ")
            return
        if name == "clock_advance":
            delta = int(values[0])
            if delta < 0 or self.clock_path is None:
                raise FeatureInputError("clock advance requires a nonnegative delta and a configured test clock")
            now = json.loads(self.clock_path.read_text(encoding="utf-8"))["now_ms"]
            self._atomic_write(self.clock_path, json.dumps({"now_ms": now + delta}).encode(), 0o600)
            return
        if name == "kill_queue":
            self._kill_detached_queue(line)
            return
        if name == "exit":
            if self.last_result is None:
                self.fail("exit-code assertion has no preceding foreground Kogen command", "suite_bug", line)
            elif self.last_result["exit"] != int(values[0]):
                self.fail(f"expected exit code {int(values[0])}, got {self.last_result['exit']}", "implementation_gap", line)
            return
        if name == "stdout_contains":
            if self.last_result is None or values[0] not in self.last_result["stdout"]:
                actual = "<no prior command>" if self.last_result is None else self.last_result["stdout"]
                self.fail(f"stdout does not contain {values[0]!r}; got {actual!r}", "implementation_gap", line)
            return
        if name == "check_count":
            counter = self.control / f"check-{values[0]}.count"
            try:
                count = int(counter.read_text(encoding="ascii"))
            except (OSError, ValueError):
                count = 0
            if count < int(values[1]):
                self.fail(f"project check {values[0]} ran {count} times, expected at least {values[1]}", "implementation_gap", line)
            return
        if name == "approval_hash":
            if self.last_result is None:
                raise FeatureInputError("approval hash capture requires a preceding review command")
            output = self.last_result["stdout"]
            matches = re.findall(r"kogen\s+intent\s+approve\s+farewell\s+([0-9a-fA-F]{6,64})(?=\s|$)", output)
            distinct = set(matches)
            if len(distinct) != 1:
                self.fail(f"review card must display one approval hash; found {sorted(distinct)!r}", "implementation_gap", line)
                return
            binding = values[0]
            if binding in self.captures and self.captures[binding] != next(iter(distinct)):
                raise FeatureInputError(f"capture {binding!r} is immutable")
            self.captures[binding] = next(iter(distinct))
            return
        if name in {"file_exact", "file_absent", "file_includes"}:
            path = self._feature_path(values[0])
            if name == "file_absent":
                if path.exists() or path.is_symlink():
                    self.fail(f"expected {values[0]} to be absent", "implementation_gap", line)
            elif name == "file_exact":
                if not path.is_file():
                    self.fail(f"expected file {values[0]} to exist", "implementation_gap", line)
                elif path.read_bytes() != (doc or "").encode("utf-8"):
                    self.fail(f"file {values[0]} bytes differ from the doc string", "implementation_gap", line)
            else:
                if not path.is_file():
                    self.fail(f"expected file {values[0]} to exist", "implementation_gap", line)
                elif values[1] not in path.read_bytes().decode("utf-8", "replace"):
                    self.fail(f"file {values[0]} does not include text {values[1]!r}", "implementation_gap", line)
            return
        if name == "branch_subject":
            _sha, subject = self._git_head(values[0])
            if subject != values[1]:
                self.fail(f"branch {values[0]} subject expected {values[1]!r}, got {subject!r}", "implementation_gap", line)
            return
        if name == "branch_trailer":
            sha, subject = self._git_head(values[0])
            if not sha or not subject:
                self.fail(f"branch {values[0]} has no committed head", "implementation_gap", line)
                return
            body = self._git(["show", "-s", "--format=%B", f"refs/heads/{values[0]}"]).stdout
            trailers = subprocess.run(["git", "interpret-trailers", "--parse"], cwd=self.repo,
                                      env=self._base_env(), input=body, capture_output=True, text=True, timeout=10)
            parsed = [entry.strip() for entry in trailers.stdout.splitlines() if entry.strip()]
            if parsed != [values[1]]:
                self.fail(f"branch {values[0]} trailers expected only {values[1]!r}, got {parsed!r}", "implementation_gap", line)
            return
        if name == "last_commit_paths":
            expected = sorted(row.strip() for row in (doc or "").splitlines() if row.strip())
            changed_result = self._git(
                ["diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "HEAD"],
                check=False,
            )
            changed = changed_result.stdout if changed_result.returncode == 0 else ""
            actual = sorted(row for row in changed.splitlines() if row)
            if actual != expected:
                self.fail(f"last commit paths expected {expected!r}, got {actual!r}", "implementation_gap", line)
            return
        if name in {"git_ignores", "git_not_ignores"}:
            args = ["check-ignore"] + (["--no-index"] if name == "git_not_ignores" else []) + ["--", values[0]]
            result = self._git(args, check=False)
            correct = result.returncode == (0 if name == "git_ignores" else 1)
            if not correct:
                self.fail(f"Git ignore check for {values[0]} returned {result.returncode}", "implementation_gap", line)
            return
        if name == "no_commit":
            if self.last_command_before_ref is None:
                raise FeatureInputError("no-new-commit assertion needs a preceding Kogen command")
            ref, before = self.last_command_before_ref
            now_result = self._git(["rev-parse", "--verify", ref], check=False)
            now = now_result.stdout.strip() if now_result.returncode == 0 else None
            if now != before:
                self.fail(f"Kogen command changed {ref}: {before!r} -> {now!r}", "implementation_gap", line)
            return
        if name == "status_intent":
            rows = self._status_json(values[0])
            intents = [row for row in rows if isinstance(row, dict) and row.get("type") == "intent"]
            if not any(row.get("status") == values[1] for row in intents):
                self.fail(f"status JSONL has no intent row with status {values[1]!r}", "implementation_gap", line)
            return
        if name == "background_frame":
            handle, text = values
            process = self._background_process(handle)
            deadline = time.monotonic() + self.timeout_s
            found = False
            while time.monotonic() < deadline:
                output, _err = process.output()
                if text in output.decode("utf-8", "replace"):
                    found = True
                    break
                if process.process.poll() is not None:
                    break
                time.sleep(0.01)
            if not found:
                self.fail(f"background command {handle} did not print frame containing {text!r}", "implementation_gap", line)
            elif text == "Building" and process.process.poll() is not None:
                self.fail("status watch exited after Building while its Build was still gated", "implementation_gap", line)
            return
        if name == "background_exit":
            handle, expected = values[0], int(values[1])
            process = self._background_process(handle)
            if not process.wait(int(self.timeout_s * 1000)):
                process.timed_out = True
                process.terminate(signal.SIGTERM)
                process.wait(250)
                kill_process_group(process.process.pid, grace_s=0.05)
                self.fail(f"background command {handle} exceeded the {self.timeout_s:g}s wait bound", "implementation_gap", line)
                return
            kill_process_group(process.process.pid, grace_s=0.05)
            actual = process.exit_code()
            if actual != expected:
                self.fail(f"background command {handle} exit expected {expected}, got {actual}", "implementation_gap", line)
            return
        if name == "status_recovery":
            self._assert_recovery(line)
            return
        if name == "recovery_expired":
            self._assert_recovery_expired(line)
            return
        if name == "account_paths":
            account_files = []
            for folder in (self.home / ".kogen", self.repo / ".kogen"):
                if folder.exists():
                    account_files.extend(path for path in folder.rglob("*") if path.is_file() and
                                         any(word in path.name.lower() for word in ("account", "credential", "provider")))
            under_home = any(path.is_relative_to(self.home) for path in account_files)
            under_repo = any(path.is_relative_to(self.repo) for path in account_files)
            if not under_home or under_repo:
                self.fail(f"account choice storage must be under temporary HOME only; files={list(map(str, account_files))!r}",
                          "implementation_gap", line)
            return
        raise FeatureInputError(f"step pattern {name!r} has no executor")

    def _background_process(self, handle: str) -> CaptureProcess:
        try:
            return self.background[handle]
        except KeyError as error:
            raise FeatureInputError(f"unknown background process handle {handle!r}") from error

    def _failed_background_queue_launch(self) -> int | None:
        for handle, metadata in reversed(list(self.background_meta.items())):
            argv = metadata.get("argv", [])
            if len(argv) < 3 or argv[1:3] != ["queue", "start"]:
                continue
            process = self.background.get(handle)
            if process is None or process.process.poll() is None:
                return None
            exit_code = process.exit_code()
            return exit_code if exit_code not in (None, 0) else None
        return None

    def _await_barrier(self, point: str, timeout_s: float) -> tuple[str, dict[str, Any]]:
        if self.barrier_dir is None:
            raise FeatureInputError("landing barrier wait requires an armed barrier fixture")
        deadline = time.monotonic() + timeout_s
        used = {record.get("_path") for record in self.barriers.values()}
        while time.monotonic() < deadline:
            for path in sorted(self.barrier_dir.glob("**/*.json")):
                if str(path) in used:
                    continue
                try:
                    record = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    continue
                if not isinstance(record, dict) or record.get("point") != point:
                    continue
                required = ("run_id", "workspace", "expected_base", "ordinal", "point")
                if any(key not in record for key in required):
                    raise FeatureInputError(f"barrier arrival {path} is missing a required field")
                record["_path"] = str(path)
                return point, record
            time.sleep(0.01)
        raise FeatureInputError(f"landing barrier {point!r} was not reached in {timeout_s:g}s")

    def _kill_detached_queue(self, line: int | None) -> None:
        status = self._status_json("kogen status --json")
        queue = next((row for row in status if isinstance(row, dict) and row.get("type") == "queue"), None)
        pid = queue.get("pid") if queue else None
        if type(pid) is not int or pid <= 0:
            self.fail("status JSONL did not report a detached queue PID", "implementation_gap", line)
            return
        try:
            identity = _process_identity(pid)
        except TraceBlocked as error:
            raise FeatureBlocked(str(error)) from error
        if identity is None:
            raise FeatureBlocked(f"cannot inspect detached queue PID {pid} on this host")
        if Path(str(identity.get("executable", ""))).resolve(strict=False) != Path(self.kogen).resolve(strict=False):
            raise FeatureInputError(f"queue PID {pid} is not the configured Kogen executable")
        if identity.get("tmpdir") != str(self.tmp):
            raise FeatureInputError(f"queue PID {pid} does not carry the scenario TMPDIR identity")
        if self.last_queue_launch_wall is None or identity.get("start_epoch", 0) < self.last_queue_launch_wall - 1:
            raise FeatureInputError(f"queue PID {pid} did not start during this scenario's queue command")
        current = _process_identity(pid)
        if current is None or not _same_process_identity(current, identity):
            raise FeatureInputError(f"queue PID {pid} process start identity changed before SIGKILL")
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError as error:
            raise FeatureInputError(f"queue PID {pid} exited before SIGKILL") from error
        self.results.append({"kind": "signal", "pid": pid, "signal": "SIGKILL", "identity": identity})

    def _assert_recovery(self, line: int | None) -> None:
        if self.last_status is None:
            self.fail("no preceding status output was captured", "implementation_gap", line)
            return
        result = self.last_status
        text = result["stdout"]
        rows = result.get("json_rows")
        recovery = None
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict) and row.get("type") == "intent":
                    records = row.get("recovery")
                    if isinstance(records, list) and records:
                        recovery = records[0]
                        break
        status_text = json.dumps(rows) if isinstance(rows, list) else text
        if not re.search(r"failed|interrupted", status_text, re.IGNORECASE):
            self.fail("latest status does not show a failed or interrupted intent", "implementation_gap", line)
        if not re.search(r"unverified", status_text, re.IGNORECASE):
            self.fail("latest status does not mark preserved recovery unverified", "implementation_gap", line)
        if recovery is None:
            location_match = re.search(r"recovery:\s*(\S+)", text)
            expiry_match = re.search(r"expires? at Unix ms ([0-9]+)", text)
            if location_match and expiry_match:
                recovery = {"location": location_match.group(1), "expires_at_ms": int(expiry_match.group(1)),
                            "verification": "unverified"}
        if not isinstance(recovery, dict) or not recovery.get("expires_at_ms"):
            self.fail("latest status does not include a preserved recovery location and expiry", "implementation_gap", line)
            return
        self.recovery_record = recovery

    def _assert_recovery_expired(self, line: int | None) -> None:
        record = self.recovery_record
        if not record:
            self.fail("recovery expiry assertion lacks the prior recovery observation", "implementation_gap", line)
            return
        location = record.get("ref") or record.get("location") or (record.get("archive") or {}).get("path")
        if isinstance(location, str) and location.startswith("refs/"):
            result = self._git(["show-ref", "--verify", "--quiet", location], check=False)
            if result.returncode == 0:
                self.fail(f"expired recovery ref still exists: {location}", "implementation_gap", line)
        elif isinstance(location, str) and location:
            if self._feature_path(location).exists():
                self.fail(f"expired recovery archive still exists: {location}", "implementation_gap", line)
        rows = self._status_json("kogen status --json")
        if any(isinstance(row, dict) and row.get("type") == "intent" and row.get("recovery")
               for row in rows):
            self.fail("expired recovery remains listed in status JSONL", "implementation_gap", line)
        journal = record.get("journal")
        if not journal:
            # The overview row's journal is the run journal's parent directory.
            journal = self._find_journal()
        journal_path = self._feature_path(str(journal)) if journal else None
        if journal_path is not None and journal_path.is_dir():
            journal_path = journal_path / "events.jsonl"
        if journal_path is None or not journal_path.is_file():
            self.fail("cannot find the run journal for the expired recovery", "implementation_gap", line)
        else:
            content = journal_path.read_text(encoding="utf-8", errors="replace")
            if "recovery_expired" not in content:
                self.fail("run journal has no recovery_expired deletion event", "implementation_gap", line)

    def _find_journal(self) -> str | None:
        if self.last_status and isinstance(self.last_status.get("json_rows"), list):
            for row in self.last_status["json_rows"]:
                if isinstance(row, dict) and row.get("type") == "intent" and row.get("journal"):
                    return row["journal"]
        return None

    @staticmethod
    def _atomic_write(path: Path, data: bytes, mode: int = 0o600) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_name(path.name + f".tmp-{os.getpid()}-{time.time_ns()}")
        temp.write_bytes(data)
        temp.chmod(mode)
        os.replace(temp, path)

    def close(self) -> list[str]:
        if self.closed:
            return []
        self.closed = True
        for process in self.all_processes:
            try:
                process.terminate(signal.SIGTERM, group=True)
                if not process.wait(250):
                    process.terminate(signal.SIGKILL, group=True)
                    process.wait(250)
                kill_process_group(process.process.pid, grace_s=0.05)
            except OSError:
                pass
        if self.fake:
            self.fake.close()
            self.fake = None
        failures = cleanup_case_cwd(self.root)
        if not self.keep:
            shutil.rmtree(self.root, ignore_errors=True)
        return failures

    def result(self, status: str = "pass") -> dict[str, Any]:
        self._finalize_provider()
        self._finalize_openid()
        classifications: dict[str, list[str]] = {
            "implementation_gap": [], "spec_step_ambiguity": [], "suite_bug": [],
        }
        for failure in self.failure_records:
            category = failure["classification"]
            classifications.setdefault(category, []).append(failure["message"])
        if self.failure_records and status == "pass":
            status = "fail"
        if self.blocked_reasons:
            status = "blocked"
        tags = self.case.get("tags", [])
        quint_tags = sorted(tag[len("@quint:"):] for tag in tags if tag.startswith("@quint:"))
        core_tags = sorted(tag[len("@core:"):] for tag in tags if tag.startswith("@core:"))
        return {
            "kind": "case", "case_kind": "gherkin", "id": self.case["id"],
            "title": self.case.get("title", ""), "file": self.case.get("_file"),
            "status": status, "quint_tags": quint_tags, "core_tags": core_tags,
            "steps": self.results,
            "failures": [failure["message"] for failure in self.failure_records],
            "failure_classification": classifications,
            "blocked_reasons": self.blocked_reasons,
            "captures": self.captures,
            "provider_transcripts": self.provider_transcripts,
            "provider_oauth": self.fake.state.all_oauth_requests() if self.fake else [],
            "sandbox": str(self.root) if self.keep else None,
        }

    def run(self) -> dict[str, Any]:
        status = "pass"
        for step in self.case.get("_feature_steps", []):
            try:
                self._run_step(step)
                self.results.append({"line": step["line"], "keyword": step["keyword"],
                                     "text": step["text"], "status": "passed"})
            except FeatureBlocked as error:
                self.blocked_reasons.append(str(error))
                self.results.append({"line": step["line"], "keyword": step["keyword"],
                                     "text": step["text"], "status": "blocked", "error": str(error)})
                break
            except Exception as error:
                message = str(error)
                if "unimplemented STEPS.md pattern" in message:
                    classification = "spec_step_ambiguity"
                elif any(marker in message for marker in (
                    "unknown capture", "landing barrier '", "unknown barrier binding",
                    "status JSONL did not report a detached queue PID",
                    "most recent shape output did not report one Intent file path",
                    "recovery expiry assertion lacks the prior recovery observation",
                )):
                    classification = "implementation_gap"
                else:
                    classification = "suite_bug"
                self.fail(f"step executor error: {type(error).__name__}: {error}", classification, step.get("line"))
                self.results.append({"line": step["line"], "keyword": step["keyword"],
                                     "text": step["text"], "status": "error", "error": str(error)})
        if self.failure_records:
            status = "fail"
        result = self.result(status)
        cleanup_errors = self.close()
        if cleanup_errors:
            result.setdefault("teardown_notes", []).extend(cleanup_errors)
        return result


def _provider_input_text(body: dict[str, Any]) -> str:
    chunks: list[str] = []
    def visit(value: Any) -> None:
        if isinstance(value, dict):
            if isinstance(value.get("text"), str):
                chunks.append(value["text"])
            for key, item in value.items():
                if key != "text":
                    visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)
    visit(body.get("input"))
    return "\n".join(chunks)


def _validate_core_status_rows(rows: list[Any]) -> list[str]:
    failures: list[str] = []
    if not rows:
        return ["at least one queue row is required"]
    first = rows[0]
    if not isinstance(first, dict):
        return ["row 0 is not an object"]
    if first.get("type") == "intent_detail":
        if len(rows) != 1:
            failures.append("intent detail must contain exactly one row")
        detail_keys = {"schema", "type", "slug", "status", "build_id", "journal", "recovery", "verdict",
                       "approval", "approved_by", "base", "candidate", "landed_sha", "priority", "blocks_on",
                       "cache_hit_rate", "cache_measurement", "credential", "acceptance", "checks", "model_stages",
                       "findings", "failures", "sandbox", "budget"}
        if set(first) not in (detail_keys, detail_keys | {"agents"}):
            failures.append("intent detail keys do not match a CORE schema variant")
        if type(first.get("schema")) is not int or first.get("schema") != 1:
            failures.append("intent_detail.schema must be integer 1")
        if not isinstance(first.get("slug"), str) or not isinstance(first.get("status"), str):
            failures.append("intent_detail.slug and status must be strings")
        if not isinstance(first.get("recovery"), list):
            failures.append("intent_detail.recovery must be an array")
        for key in ("build_id", "journal", "approved_by", "landed_sha", "sandbox"):
            if first.get(key) is not None and not isinstance(first.get(key), str):
                failures.append(f"intent_detail.{key} must be a string or null")
        if type(first.get("priority")) is not int:
            failures.append("intent_detail.priority must be an integer")
        if not isinstance(first.get("blocks_on"), list) or any(not isinstance(value, str) for value in first.get("blocks_on", [])):
            failures.append("intent_detail.blocks_on must be a string array")
        for key in ("acceptance", "checks", "model_stages", "findings", "failures"):
            if not isinstance(first.get(key), list):
                failures.append(f"intent_detail.{key} must be an array")
        if not isinstance(first.get("budget"), dict) or set(first["budget"]) != {"budget_ms", "used_ms", "paused_ms"}:
            failures.append("intent_detail.budget has an invalid schema")
        if not isinstance(first.get("credential"), dict) or set(first["credential"]) != {"source", "label"}:
            failures.append("intent_detail.credential has an invalid schema")
        return failures
    if first.get("type") != "queue" or set(first) != {"schema", "type", "state", "pid", "queued", "next"}:
        return ["overview must begin with one queue row with the exact CORE key set"]
    if type(first.get("schema")) is not int or first.get("schema") != 1:
        failures.append("queue.schema must be integer 1")
    if first.get("state") not in {"stopped", "running"}:
        failures.append("queue.state must be stopped or running")
    if first.get("pid") is not None and (type(first.get("pid")) is not int or first["pid"] <= 0):
        failures.append("queue.pid must be a positive integer or null")
    if type(first.get("queued")) is not int or first["queued"] < 0:
        failures.append("queue.queued must be a nonnegative integer")
    if first.get("next") is not None and not isinstance(first.get("next"), str):
        failures.append("queue.next must be a string or null")
    expected_keys = {
        "intent": {"schema", "type", "slug", "status", "queue_position", "reason", "build_id", "build_status",
                   "stage", "elapsed_ms", "landed_sha", "priority", "blocks_on", "journal", "candidate_diff", "recovery"},
        "agent": {"schema", "type", "id", "role", "build", "status", "elapsed_ms", "activity", "events"},
    }
    rank = {"queue": 0, "intent": 1, "agent": 2}
    ranks: list[int] = []
    positions: list[int] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            failures.append(f"row {index} is not an object")
            continue
        kind = row.get("type")
        if kind not in rank:
            failures.append(f"row {index} has unknown type {kind!r}")
            continue
        ranks.append(rank[kind])
        if type(row.get("schema")) is not int or row.get("schema") != 1:
            failures.append(f"row {index}.schema must be integer 1")
        if kind == "queue" and set(row) != {"schema", "type", "state", "pid", "queued", "next"}:
            failures.append(f"row {index} queue keys do not match CORE schema")
        if kind != "queue" and set(row) != expected_keys[kind]:
            failures.append(f"row {index} {kind} keys do not match CORE schema")
        if kind == "intent":
            for key in ("slug", "status"):
                if not isinstance(row.get(key), str):
                    failures.append(f"row {index}.{key} must be a string")
            if row.get("status") not in {"building", "queued", "blocked", "failed", "parked", "interrupted", "draft", "landed"}:
                failures.append(f"row {index}.status is not a CORE Intent status")
            for key in ("reason", "build_id", "build_status", "stage", "landed_sha", "journal", "candidate_diff"):
                if row.get(key) is not None and not isinstance(row.get(key), str):
                    failures.append(f"row {index}.{key} must be a string or null")
            for key in ("queue_position", "elapsed_ms"):
                value = row.get(key)
                if value is not None and type(value) is not int:
                    failures.append(f"row {index}.{key} must be an integer or null")
                elif value is not None and value < 0:
                    failures.append(f"row {index}.{key} must be nonnegative")
            if type(row.get("priority")) is not int:
                failures.append(f"row {index}.priority must be an integer")
            if not isinstance(row.get("blocks_on"), list) or any(not isinstance(v, str) for v in row.get("blocks_on", [])):
                failures.append(f"row {index}.blocks_on must be a string array")
            recovery = row.get("recovery")
            if not isinstance(recovery, list) or any(not isinstance(value, dict) for value in recovery):
                failures.append(f"row {index}.recovery must be an object array")
            elif isinstance(recovery, list):
                for recovery_index, item in enumerate(recovery):
                    allowed = {"workspace", "base", "tree", "ref", "commit", "archive", "verification",
                               "preserved_at_ms", "expires_at_ms", "expired"}
                    if set(item) != allowed:
                        failures.append(f"row {index}.recovery[{recovery_index}] keys do not match CORE schema")
                    for key in ("workspace", "base", "tree", "ref", "commit", "verification"):
                        if item.get(key) is not None and not isinstance(item.get(key), str):
                            failures.append(f"row {index}.recovery[{recovery_index}].{key} must be a string or null")
                    for key in ("preserved_at_ms", "expires_at_ms"):
                        if key in item and type(item.get(key)) is not int:
                            failures.append(f"row {index}.recovery[{recovery_index}].{key} must be an integer")
                    if "expired" in item and type(item.get("expired")) is not bool:
                        failures.append(f"row {index}.recovery[{recovery_index}].expired must be boolean")
                    archive = item.get("archive")
                    if archive is not None and (not isinstance(archive, dict) or set(archive) != {"path", "manifest", "sha256"}):
                        failures.append(f"row {index}.recovery[{recovery_index}].archive has an invalid schema")
                    if archive is not None and isinstance(archive, dict) and any(not isinstance(archive.get(key), str)
                                                                                   for key in ("path", "manifest", "sha256")):
                        failures.append(f"row {index}.recovery[{recovery_index}].archive fields must be strings")
            position = row.get("queue_position")
            if position is not None:
                if type(position) is not int or position < 1:
                    failures.append(f"row {index}.queue_position must be null or positive")
                else:
                    positions.append(position)
        if kind == "agent":
            for key in ("id", "role", "status"):
                if not isinstance(row.get(key), str):
                    failures.append(f"row {index}.{key} must be a string")
            if row.get("build") is not None and not isinstance(row.get("build"), str):
                failures.append(f"row {index}.build must be a string or null")
            if row.get("elapsed_ms") is not None and type(row.get("elapsed_ms")) is not int:
                failures.append(f"row {index}.elapsed_ms must be an integer or null")
            if row.get("activity") is not None and not isinstance(row.get("activity"), str):
                failures.append(f"row {index}.activity must be a string or null")
            if row.get("events") is not None and not isinstance(row.get("events"), str):
                failures.append(f"row {index}.events must be a string or null")
    if ranks != sorted(ranks) or ranks.count(0) != 1:
        failures.append("overview rows are not ordered queue, intents, agents with exactly one queue row")
    if type(first.get("queued")) is int and positions != list(range(1, first["queued"] + 1)):
        failures.append(f"intent queue positions must be 1..queued in order, got {positions!r}")
    return failures


def run_gherkin_case(case: dict[str, Any], kogen: str, time_scale: float = 0.01,
                     keep: bool = False, timeout_s: float = 60.0,
                     workdir: str | Path = "/tmp") -> dict[str, Any]:
    try:
        world = GherkinWorld(case, kogen, timeout_s, keep, workdir=workdir)
    except Exception as error:
        return {"kind": "case", "case_kind": "gherkin", "id": case.get("id", "<invalid>"),
                "title": case.get("title", ""), "file": case.get("_file"), "status": "error",
                "quint_tags": [], "core_tags": [], "failures": [f"harness error: {type(error).__name__}: {error}"],
                "failure_classification": {"suite_bug": [str(error)]}, "steps": []}
    try:
        return world.run()
    except Exception as error:
        world.fail(f"scenario runner error: {type(error).__name__}: {error}", "suite_bug")
        result = world.result("error")
        cleanup_errors = world.close()
        if cleanup_errors:
            result["failures"].extend(cleanup_errors)
            result["failure_classification"].setdefault("suite_bug", []).extend(cleanup_errors)
        result["status"] = "error"
        return result
