"""Quint ITF generation and black-box trace replay.

The decoder deliberately retains Quint's tagged values until the schema layer
has inspected them. This prevents ITF integers, sets, and sum constructors
from being mistaken for ordinary JSON data.
"""

from __future__ import annotations

import base64
import datetime
import hashlib
import http.server
import json
import os
import re
import socket
import socketserver
import shutil
import signal
import shlex
import stat
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.error
import urllib.request
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Callable

from .fake_provider import make_injected_auth
from .process_control import cleanup_case_cwd, implementation_environment, kill_process_group, run_process


SUITE_ROOT = Path(__file__).resolve().parents[1]
SPEC_ROOT = SUITE_ROOT.parent / "spec"
QUINT_ROOT = SUITE_ROOT.parent.parent / "quint-cli"
QUINT_SH = QUINT_ROOT / "quint.sh"
DEFAULT_KOGEN = SUITE_ROOT.parent / "core" / "target" / "release" / "kogen"
SCHEMA = 1
TOKEN_RE = re.compile(r"\$\$\{|\$\{([^{}]+)\}")
CAPTURE_RE = re.compile(r"^capture:([A-Za-z][A-Za-z0-9_.-]*):(oid|approval|hex|id|pid|ms|path)$")
NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_ID_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
INTEGER_RE = re.compile(r"^-?(?:0|[1-9][0-9]*)$")
DECIMAL_RE = re.compile(r"^-?(?:0|[1-9][0-9]*)\.[0-9]+$")
TYPE_PATTERNS = {
    "oid": r"(?:[0-9a-f]{40}|[0-9a-f]{64})",
    "approval": r"[0-9a-f]+",
    "hex": r"[0-9a-f]+",
    "id": r"[A-Za-z0-9_.:-]+",
    "pid": r"[1-9][0-9]*",
    "ms": r"(?:0|[1-9][0-9]*)",
    "path": r"/[^\r\n]+",
}


class QuintInputError(Exception):
    """Invalid generator or trace artifact input."""


@dataclass(frozen=True)
class Variant:
    tag: str
    value: Any


@dataclass(frozen=True)
class ITFMap:
    pairs: tuple[tuple[Any, Any], ...]


@dataclass(frozen=True)
class ITFSet:
    values: tuple[Any, ...]


def _json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise QuintInputError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> Any:
    raise QuintInputError(f"non-standard JSON number {value}")


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_json_object,
                          parse_float=Decimal, parse_int=int, parse_constant=_reject_json_constant)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise QuintInputError(f"cannot read JSON {path}: {error}") from error


def _canonical_json(value: Any) -> bytes:
    return _json_text(value).encode("utf-8")


def _json_text(value: Any, indent: int | None = None) -> str:
    number_re = re.compile(r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?$")

    def render(node: Any, depth: int) -> str:
        if node is None or type(node) in (bool, int) or isinstance(node, str):
            return json.dumps(node, ensure_ascii=False, separators=(",", ":"))
        if isinstance(node, Decimal):
            if not node.is_finite():
                raise QuintInputError("non-finite Decimal cannot be serialized as JSON")
            number = str(node)
            if not number_re.fullmatch(number):
                raise QuintInputError(f"invalid exact JSON decimal {number!r}")
            return number
        if isinstance(node, (list, tuple)):
            values = [render(child, depth + 1) for child in node]
            if not values:
                return "[]"
            if indent is None:
                return "[" + ",".join(values) + "]"
            pad, child_pad = " " * (indent * depth), " " * (indent * (depth + 1))
            return "[\n" + child_pad + (",\n" + child_pad).join(values) + "\n" + pad + "]"
        if isinstance(node, dict):
            if any(not isinstance(key, str) for key in node):
                raise QuintInputError("JSON object keys must be strings")
            values = [(json.dumps(key, ensure_ascii=False), render(child, depth + 1))
                      for key, child in sorted(node.items())]
            if not values:
                return "{}"
            if indent is None:
                return "{" + ",".join(key + ":" + child for key, child in values) + "}"
            pad, child_pad = " " * (indent * depth), " " * (indent * (depth + 1))
            return "{\n" + child_pad + (",\n" + child_pad).join(key + ": " + child for key, child in values) + "\n" + pad + "}"
        raise QuintInputError(f"unsupported JSON value {type(node).__name__}")

    if indent is not None and (type(indent) is not int or indent < 0):
        raise ValueError("indent must be a nonnegative integer or None")
    return render(value, 0)


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return ("record", tuple(sorted((key, _freeze(child)) for key, child in value.items())))
    if isinstance(value, list):
        return ("list", tuple(_freeze(child) for child in value))
    if isinstance(value, tuple):
        return ("tuple", tuple(_freeze(child) for child in value))
    if isinstance(value, ITFMap):
        return ("map", frozenset((_freeze(key), _freeze(child)) for key, child in value.pairs))
    if isinstance(value, ITFSet):
        return ("set", frozenset(_freeze(child) for child in value.values))
    if isinstance(value, Variant):
        return ("variant", value.tag, _freeze(value.value))
    if isinstance(value, Decimal):
        return ("decimal", value.normalize())
    if type(value) is bool:
        return ("bool", value)
    if type(value) is int:
        return ("int", value)
    if isinstance(value, str):
        return ("string", value)
    return value


def decode_itf(value: Any, path: str = "$ITF") -> Any:
    if isinstance(value, list):
        return [decode_itf(child, f"{path}[{index}]") for index, child in enumerate(value)]
    if not isinstance(value, dict):
        if value is None or isinstance(value, (str, bool, int, Decimal)):
            return value
        raise QuintInputError(f"{path}: unsupported ITF value {type(value).__name__}")
    if len(value) == 1:
        key, raw = next(iter(value.items()))
        if key == "#bigint":
            if not isinstance(raw, str) or not INTEGER_RE.fullmatch(raw):
                raise QuintInputError(f"{path}: malformed #bigint")
            return int(raw)
        if key == "#set":
            if not isinstance(raw, list):
                raise QuintInputError(f"{path}: #set payload must be a list")
            items = tuple(decode_itf(child, f"{path}.#set[{index}]") for index, child in enumerate(raw))
            frozen = [_freeze(child) for child in items]
            if len(frozen) != len(set(frozen)):
                raise QuintInputError(f"{path}: duplicate #set element")
            return ITFSet(items)
        if key == "#map":
            if not isinstance(raw, list):
                raise QuintInputError(f"{path}: #map payload must be a list")
            pairs: list[tuple[Any, Any]] = []
            seen: set[Any] = set()
            for index, pair in enumerate(raw):
                if not isinstance(pair, list) or len(pair) != 2:
                    raise QuintInputError(f"{path}: malformed #map entry {index}")
                key_value = decode_itf(pair[0], f"{path}.#map[{index}].key")
                marker = _freeze(key_value)
                if marker in seen:
                    raise QuintInputError(f"{path}: duplicate #map key {key_value!r}")
                seen.add(marker)
                pairs.append((key_value, decode_itf(pair[1], f"{path}.#map[{index}].value")))
            return ITFMap(tuple(pairs))
        if key == "#tup":
            if not isinstance(raw, list):
                raise QuintInputError(f"{path}: #tup payload must be a list")
            return tuple(decode_itf(child, f"{path}.#tup[{index}]") for index, child in enumerate(raw))
        if key.startswith("#"):
            raise QuintInputError(f"{path}: unsupported or undefined ITF tag {key}")
    malformed_tags = [key for key in value if key.startswith("#") and key != "#meta"]
    if malformed_tags:
        raise QuintInputError(f"{path}: ITF tags must be standalone values: {sorted(malformed_tags)}")
    if set(value) == {"tag", "value"}:
        tag = value["tag"]
        if not isinstance(tag, str) or not tag:
            raise QuintInputError(f"{path}: sum constructor has invalid tag")
        return Variant(tag, decode_itf(value["value"], f"{path}.{tag}"))
    return {key: decode_itf(child, f"{path}.{key}") for key, child in value.items()}


def _map(value: Any, path: str) -> dict[Any, Any]:
    if not isinstance(value, ITFMap):
        raise QuintInputError(f"{path}: expected Quint Map")
    result: dict[Any, Any] = {}
    for key, item in value.pairs:
        try:
            if key in result:
                raise QuintInputError(f"{path}: duplicate map key {key!r}")
            result[key] = item
        except TypeError as error:
            raise QuintInputError(f"{path}: map key must be scalar/hashable") from error
    return result


def _record(value: Any, path: str, required: tuple[str, ...] = ()) -> dict[str, Any]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise QuintInputError(f"{path}: expected record")
    missing = [key for key in required if key not in value]
    if missing:
        raise QuintInputError(f"{path}: missing field(s): {', '.join(missing)}")
    return value


def _variant(value: Any, tags: set[str], path: str) -> Variant:
    if not isinstance(value, Variant) or value.tag not in tags:
        actual = value.tag if isinstance(value, Variant) else type(value).__name__
        raise QuintInputError(f"{path}: expected one of {sorted(tags)}, got {actual}")
    return value


def _observation(value: Any, path: str) -> tuple[bool, Any]:
    variant = _variant(value, {"Unobserved", "Observe"}, path)
    if variant.tag == "Unobserved":
        if variant.value != ():
            raise QuintInputError(f"{path}: Unobserved must have unit payload")
        return False, None
    return True, variant.value


def _optional(value: Any, path: str) -> tuple[bool, Any]:
    variant = _variant(value, {"Missing", "Present"}, path)
    if variant.tag == "Missing":
        if variant.value != ():
            raise QuintInputError(f"{path}: Missing must have unit payload")
        return False, None
    return True, variant.value


def _bytes(value: Any, path: str) -> bytes:
    variant = _variant(value, {"Utf8", "Octets"}, path)
    if variant.tag == "Utf8":
        if not isinstance(variant.value, str):
            raise QuintInputError(f"{path}: Utf8 payload must be a string")
        return variant.value.encode("utf-8")
    if not isinstance(variant.value, list) or any(type(byte) is not int or not 0 <= byte <= 255 for byte in variant.value):
        raise QuintInputError(f"{path}: Octets payload must contain integers in 0..255")
    return bytes(variant.value)


def _substituted_bytes(value: Any, path: str, substitute: Callable[[str], str]) -> bytes:
    variant = _variant(value, {"Utf8", "Octets"}, path)
    if variant.tag == "Utf8":
        if not isinstance(variant.value, str):
            raise QuintInputError(f"{path}: Utf8 payload must be a string")
        return substitute(variant.value).encode("utf-8")
    return _bytes(value, path)


def _states(itf_path: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    raw = _read_json(itf_path)
    if not isinstance(raw, dict) or not isinstance(raw.get("states"), list) or not raw["states"]:
        raise QuintInputError(f"{itf_path}: ITF must contain a non-empty states array")
    decoded = decode_itf(raw)
    states = decoded["states"]
    variable_name = manifest["last_step_var"]
    seam_name = manifest["seam_var"]
    prior_index: int | None = None
    all_empty = True
    distinguishing_cli = False
    for ordinal, state in enumerate(states):
        _record(state, f"state {ordinal}")
        metadata = state.get("#meta")
        if "#meta" in state and not isinstance(metadata, dict):
            raise QuintInputError(f"{itf_path}: state {ordinal} #meta must be a record")
        if isinstance(metadata, dict) and "index" in metadata:
            index = metadata["index"]
            if type(index) is not int:
                raise QuintInputError(f"{itf_path}: state {ordinal} #meta.index must be integer")
            if prior_index is not None and index <= prior_index:
                raise QuintInputError(f"{itf_path}: state #meta.index must be strictly increasing")
            prior_index = index
        if variable_name not in state:
            raise QuintInputError(f"{itf_path}: state {ordinal} is missing {variable_name!r}")
        if seam_name not in state:
            raise QuintInputError(f"{itf_path}: state {ordinal} is missing {seam_name!r}")
        if not isinstance(state[variable_name], list):
            raise QuintInputError(f"{itf_path}: state {ordinal} {variable_name} must be a List")
        if state[variable_name]:
            all_empty = False
        for step_index, step in enumerate(state[variable_name]):
            _validate_step(step, f"state {ordinal} lastStep[{step_index}]")
            command_step = _variant(step, {"Cli", "Setup"}, f"state {ordinal} lastStep[{step_index}]")
            if command_step.tag == "Cli":
                cli = _record(command_step.value["cmd"], "Cli.cmd")
                expectation = _record(command_step.value["expect"], "Cli.expect")
                observed_exit, _ = _observation(expectation["exitCode"], "Cli.expect.exitCode")
                exit_value = _observation(expectation["exitCode"], "Cli.expect.exitCode")[1]
                distinguishing_cli = distinguishing_cli or (
                    observed_exit and exit_value != 1 and cli["argv"][:1] != ["version"])
    if len(states) > manifest["max_steps"] + 1:
        raise QuintInputError(f"{itf_path}: {len(states)} states exceed max_steps={manifest['max_steps']}")
    if all_empty:
        raise QuintInputError(f"{itf_path}: all lastStep lists are empty; trace provides no conformance coverage")
    if not distinguishing_cli:
        raise QuintInputError(f"{itf_path}: no asserted non-version CLI command distinguishes a working binary from exit-1/version-only stubs")
    _validate_seam(states[0][seam_name], "state 0 ioSeam")
    for ordinal, state in enumerate(states[1:], 1):
        _validate_seam(state[seam_name], f"state {ordinal} ioSeam")
        if state[seam_name] != states[0][seam_name]:
            raise QuintInputError(f"{itf_path}: ioSeam changes after init in state {ordinal}")
    required_seams: set[str] = set()
    required_scripts: set[str] = set()
    seam = states[0][seam_name]
    endpoint = _variant(seam["endpoint"], {"DefaultChatGPT", "ScriptedEndpoint", "InvalidEndpoint"}, "ioSeam.endpoint")
    if endpoint.tag == "ScriptedEndpoint":
        required_scripts.add(endpoint.value)
        required_seams.add("scripted_provider")
    if _optional(seam["wallClockMs"], "ioSeam.wallClockMs")[0]:
        required_seams.add("clock")
    if seam["barriers"]:
        required_seams.add("barriers")
    for state in states:
        for raw_step in state[variable_name]:
            step = _variant(raw_step, {"Cli", "Setup"}, "step")
            if step.tag == "Cli":
                command = step.value["cmd"]
                present, script_id = _optional(command["providerScript"], "Cmd.providerScript")
                if present:
                    required_scripts.add(script_id)
                    required_seams.add("scripted_provider")
                launch = _variant(command["launch"], {"Foreground", "Background"}, "Cmd.launch")
                if launch.tag == "Background":
                    required_seams.add("process")
                if command["argv"][:2] == ["provider", "login"]:
                    required_seams.add("openid")
            else:
                operation = _variant(step.value["op"], {"GitCommand", "WriteFile", "DeletePath", "SendSignal",
                    "AdvanceClock", "WaitRealMs", "AwaitExit", "AwaitOutput", "ProviderGate",
                    "AwaitBarrier", "ReleaseBarrier", "Inspect"}, "Setup.op")
                if operation.tag == "AdvanceClock":
                    required_seams.add("clock")
                if operation.tag in {"AwaitBarrier", "ReleaseBarrier"}:
                    required_seams.add("barriers")
                if operation.tag in {"SendSignal", "AwaitExit", "AwaitOutput"}:
                    required_seams.add("process")
                if operation.tag == "ProviderGate":
                    required_scripts.add(operation.value["script"])
                    required_seams.add("scripted_provider")
    missing_scripts = required_scripts - set(manifest["scripts"])
    if missing_scripts:
        raise QuintInputError(f"{itf_path}: ITF references missing provider script(s): {', '.join(sorted(missing_scripts))}")
    undeclared = required_seams - set(manifest["requires"]["seams"])
    if undeclared:
        raise QuintInputError(f"{itf_path}: manifest requires.seams omits {', '.join(sorted(undeclared))}")
    return states


def _has_distinguishing_cli(states: list[dict[str, Any]], last_var: str) -> bool:
    for state in states:
        for raw_step in state[last_var]:
            step = _variant(raw_step, {"Cli", "Setup"}, "generation step")
            if step.tag != "Cli":
                continue
            command = step.value["cmd"]
            expected = _record(step.value["expect"], "generation Cli.expect")
            observed, exit_code = _observation(expected["exitCode"], "generation Cli.expect.exitCode")
            if observed and exit_code != 1 and command["argv"][:1] != ["version"]:
                return True
    return False


def _validate_named_map(value: Any, path: str) -> dict[str, Any]:
    mapping = _map(value, path)
    if any(not isinstance(key, str) for key in mapping):
        raise QuintInputError(f"{path}: keys must be strings")
    return mapping


def _validate_step(value: Any, path: str) -> None:
    step = _variant(value, {"Cli", "Setup"}, path)
    if step.tag == "Cli":
        body = _record(step.value, path, ("cmd", "expect"))
        cmd = _record(body["cmd"], path + ".cmd", ("argv", "stdin", "env", "cwd", "providerScript", "launch", "timeoutMs"))
        if not isinstance(cmd["argv"], list) or any(not isinstance(arg, str) for arg in cmd["argv"]):
            raise QuintInputError(f"{path}.cmd.argv must be a list of strings")
        _bytes(cmd["stdin"], path + ".cmd.stdin")
        _validate_named_map(cmd["env"], path + ".cmd.env")
        if not isinstance(cmd["cwd"], str) or not cmd["cwd"] or type(cmd["timeoutMs"]) is not int or cmd["timeoutMs"] <= 0:
            raise QuintInputError(f"{path}.cmd has invalid cwd or timeoutMs")
        provider_present, provider_id = _optional(cmd["providerScript"], path + ".cmd.providerScript")
        if provider_present and (not isinstance(provider_id, str) or not provider_id):
            raise QuintInputError(f"{path}.cmd.providerScript Present payload must be a nonempty string")
        launch = _variant(cmd["launch"], {"Foreground", "Background"}, path + ".cmd.launch")
        if launch.tag == "Foreground" and launch.value != ():
            raise QuintInputError(f"{path}.cmd.launch Foreground must have unit payload")
        if launch.tag == "Background" and (not isinstance(launch.value, str) or not launch.value):
            raise QuintInputError(f"{path}.cmd.launch Background needs a nonempty handle")
        _validate_expect(body["expect"], path + ".expect")
        if launch.tag == "Foreground":
            observed, _ = _observation(body["expect"]["exitCode"], path + ".expect.exitCode")
            if not observed:
                raise QuintInputError(f"{path}: Foreground CLI completion must observe exitCode")
    else:
        body = _record(step.value, path, ("op", "expect"))
        op = _variant(body["op"], {"GitCommand", "WriteFile", "DeletePath", "SendSignal", "AdvanceClock",
                                   "WaitRealMs", "AwaitExit", "AwaitOutput", "ProviderGate", "AwaitBarrier",
                                   "ReleaseBarrier", "Inspect"}, path + ".op")
        _validate_setup(op, path + ".op")
        _validate_expect(body["expect"], path + ".expect")


def _validate_setup(op: Variant, path: str) -> None:
    if op.tag == "Inspect":
        if op.value != ():
            raise QuintInputError(f"{path}: Inspect must have unit payload")
        return
    if op.tag == "ReleaseBarrier":
        if not isinstance(op.value, str):
            raise QuintInputError(f"{path}: ReleaseBarrier needs a ticket binding")
        return
    if op.tag in {"AdvanceClock", "WaitRealMs"}:
        if type(op.value) is not int or op.value < 0:
            raise QuintInputError(f"{path}: {op.tag} requires a nonnegative integer")
        return
    if op.tag == "DeletePath":
        if not isinstance(op.value, str):
            raise QuintInputError(f"{path}: DeletePath needs a path")
        return
    if op.tag == "GitCommand":
        exec_record = _record(op.value, path, ("executable", "argv", "stdin", "env", "cwd", "timeoutMs"))
        if not isinstance(exec_record["executable"], str) or not isinstance(exec_record["argv"], list) or \
                not isinstance(exec_record["cwd"], str) or not exec_record["cwd"]:
            raise QuintInputError(f"{path}: malformed GitCommand Exec")
        if any(not isinstance(arg, str) for arg in exec_record["argv"]):
            raise QuintInputError(f"{path}: GitCommand argv must be strings")
        _bytes(exec_record["stdin"], path + ".stdin")
        _validate_named_map(exec_record["env"], path + ".env")
        if type(exec_record["timeoutMs"]) is not int or exec_record["timeoutMs"] <= 0:
            raise QuintInputError(f"{path}: timeoutMs must be positive")
        return
    if op.tag == "WriteFile":
        record = _record(op.value, path, ("path", "bytes", "mode"))
        if not isinstance(record["path"], str) or type(record["mode"]) is not int or not 0 <= record["mode"] <= 0o7777:
            raise QuintInputError(f"{path}: malformed WriteFile")
        _bytes(record["bytes"], path + ".bytes")
        return
    if op.tag == "SendSignal":
        record = _record(op.value, path, ("target", "signal", "processGroup"))
        if not all(isinstance(record[key], str) for key in ("target", "signal")) or type(record["processGroup"]) is not bool:
            raise QuintInputError(f"{path}: malformed SendSignal")
        if not record["target"] or not record["signal"]:
            raise QuintInputError(f"{path}: target and signal must be nonempty")
        return
    if op.tag in {"AwaitExit", "AwaitOutput"}:
        fields = ("handle", "timeoutMs") if op.tag == "AwaitExit" else ("handle", "stream", "pattern", "timeoutMs")
        record = _record(op.value, path, fields)
        if type(record["timeoutMs"]) is not int or record["timeoutMs"] <= 0:
            raise QuintInputError(f"{path}: timeoutMs must be positive")
        if not isinstance(record["handle"], str) or not record["handle"]:
            raise QuintInputError(f"{path}: handle must be a nonempty string")
        if op.tag == "AwaitOutput" and (record["stream"] not in {"stdout", "stderr"} or not isinstance(record["pattern"], str)):
            raise QuintInputError(f"{path}: AwaitOutput requires stdout/stderr and a string pattern")
        return
    if op.tag == "ProviderGate":
        record = _record(op.value, path, ("script", "gate", "operation", "timeoutMs"))
        if type(record["timeoutMs"]) is not int or record["timeoutMs"] <= 0:
            raise QuintInputError(f"{path}: timeoutMs must be positive")
        if any(not isinstance(record[field], str) or not record[field] for field in ("script", "gate")) or \
                not isinstance(record["operation"], str) or record["operation"] not in {"await", "release"}:
            raise QuintInputError(f"{path}: malformed ProviderGate selector or operation")
        return
    if op.tag == "AwaitBarrier":
        record = _record(op.value, path, ("point", "ticket", "timeoutMs"))
        if type(record["timeoutMs"]) is not int or record["timeoutMs"] <= 0:
            raise QuintInputError(f"{path}: timeoutMs must be positive")
        if any(not isinstance(record[field], str) or not record[field] for field in ("point", "ticket")):
            raise QuintInputError(f"{path}: malformed AwaitBarrier point/ticket")
        return
    raise QuintInputError(f"{path}: unsupported Setup constructor {op.tag}")


def _validate_expect(value: Any, path: str) -> None:
    expect = _record(value, path, ("exitCode", "stdoutLines", "stderr", "jsonRows", "statusRows", "git",
                                   "files", "jsonFiles", "timings", "relations"))
    enabled, observed = _observation(expect["exitCode"], f"{path}.exitCode")
    if enabled and type(observed) is not int:
        raise QuintInputError(f"{path}.exitCode Observe payload must be an integer")
    for field in ("stdoutLines",):
        enabled, observed = _observation(expect[field], f"{path}.{field}")
        if enabled:
            _validate_lines(observed, f"{path}.{field}")
    for field in ("jsonRows", "statusRows"):
        enabled, observed = _observation(expect[field], f"{path}.{field}")
        if enabled:
            _validate_rows(observed, f"{path}.{field}")
    enabled, observed = _observation(expect["git"], f"{path}.git")
    if enabled:
        _validate_git_expect(observed, f"{path}.git")
    stderr = _record(expect["stderr"], path + ".stderr", ("class", "text"))
    class_enabled, class_value = _observation(stderr["class"], path + ".stderr.class")
    if class_enabled and (not isinstance(class_value, str) or class_value not in {
            "empty", "warning", "usage", "environment", "provider", "decision", "bug", "sigterm", "no", "other"}):
        raise QuintInputError(f"{path}.stderr.class Observe payload is not a known stderr class")
    text_match = _variant(stderr["text"], {"IgnoreText", "ExactLines", "Pattern"}, path + ".stderr.text")
    if text_match.tag == "IgnoreText":
        if text_match.value != ():
            raise QuintInputError(f"{path}.stderr.text IgnoreText must have unit payload")
    elif text_match.tag == "ExactLines":
        _validate_lines(text_match.value, path + ".stderr.text")
    elif not isinstance(text_match.value, str):
        raise QuintInputError(f"{path}.stderr.text Pattern payload must be a string")
    for field in ("files", "jsonFiles", "timings"):
        _validate_named_map(expect[field], path + "." + field)
    files = _validate_named_map(expect["files"], path + ".files")
    for name, value in files.items():
        file_value = _variant(value, {"AbsentFile", "FileBytes", "FileSha256", "Symlink"}, f"{path}.files[{name!r}]")
        if file_value.tag == "AbsentFile" and file_value.value != ():
            raise QuintInputError(f"{path}.files[{name!r}] AbsentFile must have unit payload")
        if file_value.tag == "FileBytes":
            _bytes(file_value.value, f"{path}.files[{name!r}].bytes")
        if file_value.tag in {"FileSha256", "Symlink"} and not isinstance(file_value.value, str):
            raise QuintInputError(f"{path}.files[{name!r}] {file_value.tag} payload must be string")
    json_files = _validate_named_map(expect["jsonFiles"], path + ".jsonFiles")
    for name, rows in json_files.items():
        _validate_rows(rows, f"{path}.jsonFiles[{name!r}]")
    timings = _validate_named_map(expect["timings"], path + ".timings")
    for name, atom in timings.items():
        variant = _variant(atom, {"JInt", "JSymbol"}, f"{path}.timings[{name!r}]")
        if variant.tag == "JInt" and type(variant.value) is not int:
            raise QuintInputError(f"{path}.timings[{name!r}] JInt must contain an integer")
        if variant.tag == "JSymbol" and not isinstance(variant.value, str):
            raise QuintInputError(f"{path}.timings[{name!r}] JSymbol must contain a string")
    if not isinstance(expect["relations"], list):
        raise QuintInputError(f"{path}.relations must be a list")
    for index, relation in enumerate(expect["relations"]):
        variant = _variant(relation, {"Same", "Different", "IntRange", "IntDelta", "IntAtLeastDelta"}, f"{path}.relations[{index}]")
        relation_path = f"{path}.relations[{index}]"
        if variant.tag in {"Same", "Different"}:
            record = _record(variant.value, relation_path, ("left", "right"))
            if any(not isinstance(record[key], str) for key in ("left", "right")):
                raise QuintInputError(f"{relation_path} equality operands must be strings")
        elif variant.tag == "IntRange":
            record = _record(variant.value, relation_path, ("value", "min", "max"))
            if not isinstance(record["value"], str) or type(record["min"]) is not int or type(record["max"]) is not int:
                raise QuintInputError(f"{relation_path} IntRange has malformed operands")
        else:
            record = _record(variant.value, relation_path, ("later", "earlier", "delta"))
            if not isinstance(record["later"], str) or not isinstance(record["earlier"], str) or type(record["delta"]) is not int:
                raise QuintInputError(f"{relation_path} {variant.tag} has malformed operands")


def _validate_lines(value: Any, path: str) -> None:
    if not isinstance(value, list):
        raise QuintInputError(f"{path} must be a list of Line values")
    for index, line_value in enumerate(value):
        if not isinstance(line_value, list) or any(not isinstance(fragment, str) for fragment in line_value):
            raise QuintInputError(f"{path}[{index}] must be a list of string fragments")


def _validate_rows(value: Any, path: str) -> None:
    if not isinstance(value, list):
        raise QuintInputError(f"{path} must be a list of JsonRow values")
    for row_index, row_value in enumerate(value):
        row = _record(row_value, f"{path}[{row_index}]", ("atoms", "objects", "arrays"))
        atoms = _validate_named_map(row["atoms"], f"{path}[{row_index}].atoms")
        for pointer, atom in atoms.items():
            variant = _variant(atom, {"JNull", "JBool", "JInt", "JDecimal", "JString", "JSymbol"},
                               f"{path}[{row_index}].atoms[{pointer!r}]")
            if variant.tag == "JNull" and variant.value != ():
                raise QuintInputError(f"{path}[{row_index}] JNull must have unit payload")
            if variant.tag == "JDecimal" and (not isinstance(variant.value, str) or
                                                not DECIMAL_RE.fullmatch(variant.value)):
                raise QuintInputError(f"{path}[{row_index}] JDecimal must be a canonical decimal string")
            expected_type = {"JBool": bool, "JInt": int, "JDecimal": str, "JString": str, "JSymbol": str}.get(variant.tag)
            if expected_type is not None and type(variant.value) is not expected_type:
                raise QuintInputError(f"{path}[{row_index}] {variant.tag} payload has wrong type")
        if not isinstance(row["objects"], ITFSet) or any(not isinstance(pointer, str) for pointer in row["objects"].values):
            raise QuintInputError(f"{path}[{row_index}].objects must be a Set[str]")
        arrays = _validate_named_map(row["arrays"], f"{path}[{row_index}].arrays")
        if any(not isinstance(pointer, str) or type(length) is not int or length < 0 for pointer, length in arrays.items()):
            raise QuintInputError(f"{path}[{row_index}].arrays must map pointers to nonnegative integers")


def _validate_git_expect(value: Any, path: str) -> None:
    git = _record(value, path, ("branches", "kogenRefs", "head", "symbolicHead", "headTree", "indexTree",
                                "subject", "trailers", "changedPaths", "parents", "author", "committer"))
    for field in ("branches", "kogenRefs"):
        named = _record(git[field], path + "." + field, ("complete", "entries"))
        if type(named["complete"]) is not bool:
            raise QuintInputError(f"{path}.{field}.complete must be boolean")
        entries = _validate_named_map(named["entries"], path + "." + field + ".entries")
        for key, value in entries.items():
            present, payload = _optional(value, f"{path}.{field}.entries[{key!r}]")
            if present and not isinstance(payload, str):
                raise QuintInputError(f"{path}.{field}.entries[{key!r}] Present payload must be a string")
    for field in ("head", "symbolicHead"):
        observed, value = _observation(git[field], path + "." + field)
        if observed:
            present, payload = _optional(value, path + "." + field)
            if present and not isinstance(payload, str):
                raise QuintInputError(f"{path}.{field} Present payload must be a string")
    for field in ("headTree", "indexTree", "subject"):
        observed, value = _observation(git[field], path + "." + field)
        if observed and not isinstance(value, str):
            raise QuintInputError(f"{path}.{field} Observe payload must be a string")
    for field in ("trailers", "parents"):
        observed, value = _observation(git[field], path + "." + field)
        if observed and not isinstance(value, list):
            raise QuintInputError(f"{path}.{field} Observe payload must be a list")
        if observed and field == "trailers":
            for index, trailer in enumerate(value):
                item = _record(trailer, f"{path}.trailers[{index}]", ("key", "value"))
                if not isinstance(item["key"], str) or not isinstance(item["value"], str):
                    raise QuintInputError(f"{path}.trailers[{index}] key/value must be strings")
        if observed and field == "parents" and any(not isinstance(parent, str) for parent in value):
            raise QuintInputError(f"{path}.parents must contain strings")
    observed, value = _observation(git["changedPaths"], path + ".changedPaths")
    if observed and (not isinstance(value, ITFSet) or any(not isinstance(item, str) for item in value.values)):
        raise QuintInputError(f"{path}.changedPaths Observe payload must be Set[str]")
    for field in ("author", "committer"):
        observed, value = _observation(git[field], path + "." + field)
        if observed:
            identity = _record(value, path + "." + field, ("name", "email"))
            if not isinstance(identity["name"], str) or not isinstance(identity["email"], str):
                raise QuintInputError(f"{path}.{field} name/email must be strings")


def _validate_seam(value: Any, path: str) -> None:
    seam = _record(value, path, ("endpoint", "auth", "credentialStore", "timeScalePermille", "wallClockMs", "barriers"))
    endpoint = _variant(seam["endpoint"], {"DefaultChatGPT", "ScriptedEndpoint", "InvalidEndpoint"}, path + ".endpoint")
    auth = _variant(seam["auth"], {"NoAuth", "InjectedAuth", "InvalidAuth"}, path + ".auth")
    if seam["credentialStore"] != "file" or type(seam["timeScalePermille"]) is not int or seam["timeScalePermille"] <= 0:
        raise QuintInputError(f"{path}: invalid credential store or time scale")
    wall_present, wall_value = _optional(seam["wallClockMs"], path + ".wallClockMs")
    if wall_present and (type(wall_value) is not int or wall_value < 0):
        raise QuintInputError(f"{path}.wallClockMs Present payload must be a nonnegative integer")
    if type(seam["barriers"]) is not bool:
        raise QuintInputError(f"{path}.barriers must be boolean")
    if endpoint.tag in {"ScriptedEndpoint", "InvalidEndpoint"} and \
            (not isinstance(endpoint.value, str) or not endpoint.value):
        raise QuintInputError(f"{path}.endpoint payload must be a nonempty string")
    if endpoint.tag == "DefaultChatGPT" and endpoint.value != ():
        raise QuintInputError(f"{path}.endpoint DefaultChatGPT must have unit payload")
    if auth.tag == "InjectedAuth":
        credential = _record(auth.value, path + ".auth", ("accountId", "expiresAtSeconds"))
        if not isinstance(credential["accountId"], str) or not credential["accountId"] or \
                type(credential["expiresAtSeconds"]) is not int or credential["expiresAtSeconds"] < 0:
            raise QuintInputError(f"{path}.auth InjectedAuth credentials are invalid")
    if auth.tag == "InvalidAuth":
        _bytes(auth.value, path + ".auth")
    if auth.tag == "NoAuth" and auth.value != ():
        raise QuintInputError(f"{path}.auth NoAuth must have unit payload")


def _source_closure(model: Path) -> tuple[list[dict[str, str]], str, Path]:
    pending = [model.resolve()]
    found: dict[Path, bytes] = {}
    import_re = re.compile(r'\bimport\b[^\n]*?\bfrom\s+["\']([^"\']+)["\']')
    while pending:
        path = pending.pop()
        if path in found:
            continue
        try:
            data = path.read_bytes()
            source = data.decode("utf-8")
        except (OSError, UnicodeError) as error:
            raise QuintInputError(f"cannot read Quint source {path}: {error}") from error
        found[path] = data
        for import_path in import_re.findall(source):
            candidate = (path.parent / import_path).resolve()
            if candidate.suffix != ".qnt":
                candidate = candidate.with_suffix(".qnt")
            if not candidate.exists():
                raise QuintInputError(f"{path}: cannot resolve imported Quint source {import_path!r}")
            pending.append(candidate)
    common = Path(os.path.commonpath([str(path.parent) for path in found]))
    rows = []
    digest = hashlib.sha256()
    for path, data in sorted(found.items(), key=lambda item: item[0].relative_to(common).as_posix()):
        relative = path.relative_to(common).as_posix()
        row_digest = hashlib.sha256(data).hexdigest()
        rows.append({"path": relative, "sha256": row_digest})
        encoded_path = relative.encode("utf-8")
        digest.update(len(encoded_path).to_bytes(8, "big"))
        digest.update(encoded_path)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return rows, digest.hexdigest(), common


def _module_name(model: Path) -> str:
    try:
        text = model.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise QuintInputError(f"cannot read model {model}: {error}") from error
    match = re.search(r"\bmodule\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{", text)
    if not match:
        raise QuintInputError(f"{model}: cannot find a Quint module declaration")
    return match.group(1)


def _binary_metadata(kogen: Path, *, strict: bool = True, workdir: str | Path = "/tmp") -> tuple[str, str]:
    try:
        binary = kogen.resolve(strict=True)
        digest = hashlib.sha256(binary.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory(prefix="kc2-version-", dir=str(workdir)) as metadata_home:
            metadata_env = {"LC_ALL": "C", "HOME": metadata_home, "TMPDIR": metadata_home}
            metadata_env.update(implementation_environment())
            completed = run_process([str(binary), "version"], cwd=metadata_home,
                                    env=metadata_env, timeout_s=10)
            result = subprocess.CompletedProcess(
                [str(binary), "version"], completed.returncode,
                completed.stdout.decode("utf-8", "replace"), completed.stderr.decode("utf-8", "replace"))
    except (OSError, subprocess.SubprocessError) as error:
        raise QuintInputError(f"cannot read tested Kogen binary {kogen}: {error}") from error
    if result.returncode != 0 and strict:
        raise QuintInputError(f"tested Kogen binary version command exited {result.returncode}: {result.stderr.strip()}")
    version = (result.stdout + result.stderr).strip()
    if not version and strict:
        raise QuintInputError("tested Kogen binary returned an empty version")
    if not version:
        version = f"version command exited {result.returncode} without output"
    elif result.returncode != 0:
        version = f"version command exited {result.returncode}: {version}"
    return digest, version


def _run_quint(command: list[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory(prefix="kc2-quint-cli-", dir="/tmp") as home:
        temporary = Path(home) / "tmp"
        temporary.mkdir()
        return subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                              env={"PATH": "/usr/bin:/bin", "HOME": home, "TMPDIR": str(temporary),
                                   "LC_ALL": "C", "TZ": "UTC", "NO_COLOR": "1"})


def _parse_keyed_args(items: list[str], label: str) -> dict[str, str]:
    result = {}
    for item in items:
        if "=" not in item:
            raise QuintInputError(f"--{label} expects NAME=VALUE, got {item!r}")
        key, value = item.split("=", 1)
        if not key or key in result:
            raise QuintInputError(f"duplicate or empty --{label} key {key!r}")
        result[key] = value
    return result


def _load_script(path: Path) -> dict[str, Any]:
    value = _read_json(path)
    if not isinstance(value, dict) or type(value.get("schema")) is not int or value.get("schema") != 1 or \
            not isinstance(value.get("turns"), list):
        raise QuintInputError(f"{path}: script must be a version 1 envelope with turns")
    result = dict(value)
    result.pop("digest", None)
    turns = result["turns"]
    minimum = result.get("min_requests")
    maximum = result.get("max_requests")
    if type(minimum) is not int or type(maximum) is not int or not 0 <= minimum <= maximum <= len(turns):
        raise QuintInputError(f"{path}: invalid min_requests/max_requests")
    result["digest"] = hashlib.sha256(_canonical_json(result)).hexdigest()
    _validate_script(result, str(path))
    return result


def generate_traces(*, model: str, seed: int, traces: int, steps: int, out: str,
                    kogen: str | None = None, main: str | None = None, profile: str = "fast",
                    clause_ids: list[str] | None = None, witnesses: list[str] | None = None,
                    script_args: list[str] | None = None, fixture_args: list[str] | None = None,
                    fixture_map_args: list[str] | None = None, quint_timeout: int = 180,
                    jobs: int = 3, retry_vacuous: int = 0) -> list[str]:
    if seed < 0 or traces < 1 or steps < 1 or quint_timeout < 1 or not 1 <= jobs <= 3 or retry_vacuous < 0:
        raise QuintInputError("--seed must be nonnegative and --traces/--steps must be positive")
    model_argument = Path(model)
    model_path = (SUITE_ROOT / model_argument).resolve(strict=True) if not model_argument.is_absolute() else model_argument.resolve(strict=True)
    if model_path.suffix != ".qnt":
        raise QuintInputError("--model must name a .qnt file")
    if not QUINT_SH.is_file() or not os.access(QUINT_SH, os.X_OK):
        raise QuintInputError(f"pinned Quint launcher is unavailable: {QUINT_SH}")
    main_name = main or _module_name(model_path)
    source_rows, source_digest, source_root = _source_closure(model_path)
    binary_path = Path(kogen).resolve() if kogen else DEFAULT_KOGEN
    binary_digest, binary_version = _binary_metadata(binary_path)
    scripts: dict[str, Any] = {}
    for script_id, script_path in _parse_keyed_args(script_args or [], "script").items():
        scripts[script_id] = _load_script(Path(script_path).resolve(strict=True))
    fixtures: dict[str, Any] = {}
    fixture_sources: list[dict[str, str]] = []
    for fixture_path in fixture_map_args or []:
        path = Path(fixture_path).resolve(strict=True)
        try:
            source_name = path.relative_to(SPEC_ROOT.resolve()).as_posix()
        except ValueError as error:
            raise QuintInputError(f"--fixtures file must be under {SPEC_ROOT}: {path}") from error
        data = path.read_bytes()
        fixture_sources.append({"path": source_name, "sha256": hashlib.sha256(data).hexdigest()})
        mapping = json.loads(data)
        if not isinstance(mapping, dict):
            raise QuintInputError(f"{path}: provider fixture file must be an object keyed by script id")
        fixture_file = "schema" in mapping and "scripts" in mapping
        script_mapping = mapping.get("scripts", {}) if fixture_file else mapping
        if fixture_file and (mapping.get("schema") != 1 or not isinstance(script_mapping, dict)):
            raise QuintInputError(f"{path}: malformed legacy fixture bundle")
        for script_id, envelope in script_mapping.items():
            if script_id in scripts:
                raise QuintInputError(f"{path}: duplicate provider script id {script_id!r}")
            if not isinstance(envelope, dict):
                raise QuintInputError(f"{path}: script {script_id!r} must be an object")
            if fixture_file and script_id == "cli-openid" and "openid" in envelope:
                # The OpenID transcript is preserved as a fixture blob below. It is
                # not a Responses request script, but the shared Cmd schema carries
                # its fixture id for replay metadata.
                envelope = {"schema": 1, "turns": [], "min_requests": 0, "max_requests": 0}
            elif fixture_file and "schema" not in envelope:
                # Preserve legacy fixture bundles byte-for-byte in fixtures; only
                # entries selected by the schema-1 trace need runnable envelopes.
                continue
            bare = dict(envelope)
            bare.pop("digest", None)
            bare["turns"] = [dict(turn) for turn in bare.get("turns", [])]
            for turn in bare["turns"]:
                response = turn.get("response", {})
                for chunk in response.get("chunks", []):
                    chunk.setdefault("gate", None)
            bare["digest"] = hashlib.sha256(_canonical_json(bare)).hexdigest()
            _validate_script(bare, f"{path}[{script_id!r}]")
            scripts[script_id] = bare
    for name, fixture_path in _parse_keyed_args(fixture_args or [], "fixture").items():
        data = Path(fixture_path).resolve(strict=True).read_bytes()
        fixtures[name] = {"schema": 1, "digest": hashlib.sha256(data).hexdigest(),
                          "bytes": {"octets": list(data)}}
    requested_output = Path(out)
    if requested_output.is_absolute():
        output = requested_output.resolve()
    elif requested_output.parts and requested_output.parts[0] == "cases":
        output = (SUITE_ROOT / requested_output).resolve()
    else:
        output = (Path.cwd() / requested_output).resolve()
    allowed_roots = (SUITE_ROOT.resolve(), Path("/tmp").resolve())
    if not any(_is_within(output, allowed) for allowed in allowed_roots):
        raise QuintInputError("--out must be inside suite/ or /tmp/kc2*")
    if _is_within(output, Path("/tmp").resolve()):
        relative_tmp = output.relative_to(Path("/tmp").resolve())
        if not relative_tmp.parts or not relative_tmp.parts[0].startswith("kc2"):
            raise QuintInputError("temporary --out paths must use the /tmp/kc2* prefix")
    if not isinstance(profile, str) or not profile:
        raise QuintInputError("--profile must be a nonempty string")
    output.mkdir(parents=True, exist_ok=True)
    generated: list[str] = []
    try:
        quint_version_result = _run_quint([str(QUINT_SH), "--version"], QUINT_ROOT, 20)
    except (OSError, subprocess.SubprocessError) as error:
        raise QuintInputError(f"cannot execute pinned Quint launcher: {error}") from error
    quint_version = quint_version_result.stdout.strip()
    if quint_version_result.returncode or quint_version != "0.33.0":
        raise QuintInputError(f"expected Quint 0.33.0, got {quint_version or quint_version_result.stderr.strip()}")
    def generate_trace(offset: int, retry: int = 0) -> list[str]:
        trace_seed = seed + offset
        itf_name = f"trace-{trace_seed}.itf.json"
        itf_path = output / itf_name
        command = [str(QUINT_SH), "run", str(model_path), "--main", main_name, "--backend", "typescript",
                   "--seed", str(trace_seed), "--max-samples", "1", "--n-traces", "1",
                   "--max-steps", str(steps), "--invariant", "invariant", "--mbt", "--out-itf", str(itf_path)]
        try:
            attempt_timeout = min(quint_timeout, 120) if retry else quint_timeout
            result = _run_quint(command, model_path.parent, attempt_timeout)
        except subprocess.TimeoutExpired as error:
            if retry < retry_vacuous:
                return generate_trace(offset + traces, retry + 1)
            raise QuintInputError(f"Quint generation timed out for seed {trace_seed}") from error
        except OSError as error:
            raise QuintInputError(f"cannot execute Quint for seed {trace_seed}: {error}") from error
        if result.returncode:
            raise QuintInputError(f"Quint generation failed for seed {trace_seed}: {(result.stdout + result.stderr).strip()}")
        if not itf_path.is_file():
            raise QuintInputError(f"Quint did not write {itf_path.name}")
        itf = _read_json(itf_path)
        if not isinstance(itf, dict) or not isinstance(itf.get("states"), list) or not itf["states"]:
            raise QuintInputError(f"seed {trace_seed}: Quint wrote an invalid ITF trace")
        decoded = decode_itf(itf)
        keys = set(decoded["states"][0])
        last_var = _find_var(keys, "lastStep")
        seam_var = _find_var(keys, "ioSeam")
        states = decoded["states"]
        if not _has_distinguishing_cli(states, last_var):
            itf_path.unlink(missing_ok=True)
            (output / f"trace-{trace_seed}.manifest.json").unlink(missing_ok=True)
            if retry < retry_vacuous:
                # Keep each trace's retry stream disjoint: offsets retain their
                # modulo-trace index while the actual accepted seed is recorded.
                return generate_trace(offset + traces, retry + 1)
            raise QuintInputError(
                f"seed {trace_seed}: no asserted non-version Kogen command after {retry_vacuous + 1} bounded seed attempt(s)"
            )
        script_ids: set[str] = set()
        required_seams: set[str] = set()
        seam_record = states[0][seam_var]
        _validate_seam(seam_record, "generated ioSeam")
        endpoint = _variant(seam_record["endpoint"], {"DefaultChatGPT", "ScriptedEndpoint", "InvalidEndpoint"},
                            "generated ioSeam.endpoint")
        if endpoint.tag == "ScriptedEndpoint":
            script_ids.add(endpoint.value)
            required_seams.add("scripted_provider")
        if _optional(seam_record["wallClockMs"], "generated ioSeam.wallClockMs")[0]:
            required_seams.add("clock")
        if seam_record["barriers"]:
            required_seams.add("barriers")
        for state in states:
            for raw_step in state[last_var]:
                step = _variant(raw_step, {"Cli", "Setup"}, "generated step")
                if step.tag == "Cli":
                    command_record = step.value["cmd"]
                    selected, script_id = _optional(command_record["providerScript"], "generated providerScript")
                    if selected:
                        script_ids.add(script_id)
                        required_seams.add("scripted_provider")
                    launch = _variant(command_record["launch"], {"Foreground", "Background"}, "generated launch")
                    if launch.tag == "Background":
                        required_seams.add("process")
                    if command_record["argv"][:2] == ["provider", "login"]:
                        required_seams.add("openid")
                else:
                    op = _variant(step.value["op"], {"GitCommand", "WriteFile", "DeletePath", "SendSignal", "AdvanceClock",
                                                      "WaitRealMs", "AwaitExit", "AwaitOutput", "ProviderGate", "AwaitBarrier",
                                                      "ReleaseBarrier", "Inspect"}, "generated setup")
                    if op.tag == "AdvanceClock":
                        required_seams.add("clock")
                    if op.tag in {"AwaitBarrier", "ReleaseBarrier"}:
                        required_seams.add("barriers")
                    if op.tag in {"SendSignal", "AwaitExit", "AwaitOutput"}:
                        required_seams.add("process")
        missing_scripts = sorted(script_ids - set(scripts))
        # ScriptedEndpoint names the trace-local fallback URL. Concrete provider
        # turns are selected on each emitted command; a fallback alias therefore
        # has an explicit zero-request envelope unless a source fixture defines it.
        if endpoint.tag == "ScriptedEndpoint" and endpoint.value not in scripts:
            fallback = {"schema": 1, "turns": [], "min_requests": 0, "max_requests": 0}
            fallback["digest"] = hashlib.sha256(_canonical_json(fallback)).hexdigest()
            scripts[endpoint.value] = fallback
            if endpoint.value in missing_scripts:
                missing_scripts.remove(endpoint.value)
        if missing_scripts:
            raise QuintInputError(f"seed {trace_seed}: ITF references missing provider script(s): {', '.join(missing_scripts)}")
        manifest = {
            "io_schema": SCHEMA, "module": main_name, "model": str(model_path),
            "source_root": _display_path(source_root), "source_digest": source_digest, "sources": source_rows,
            "quint_version": quint_version, "backend": "typescript", "seed": str(trace_seed),
            "max_steps": steps, "last_step_var": last_var, "seam_var": seam_var,
            "binary_digest": binary_digest, "binary_version": binary_version,
            "scripts": scripts, "fixtures": fixtures, "fixture_sources": fixture_sources,
            "requires": {"platform": [], "tools": ["git"], "seams": sorted(required_seams)},
            "clause_ids": clause_ids or ["unassigned"],
            "witnesses": witnesses or [f"seed-{trace_seed}-unassigned"],
            "profile": profile, "command_line": command,
            "model_path": str(model_path), "itf_file": itf_name,
        }
        # Validate state/effect shape now. A generator can produce syntactically valid ITF with no coverage.
        _states(itf_path, manifest)
        manifest_path = output / f"trace-{trace_seed}.manifest.json"
        manifest_path.write_text(_json_text(manifest) + "\n", encoding="utf-8")
        return [str(itf_path), str(manifest_path)]

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(generate_trace, range(traces)))
    return [path for trace_paths in results for path in trace_paths]


def _find_var(keys: set[str], name: str) -> str:
    candidates = [key for key in keys if key == name or key.endswith("::" + name) or key.endswith("." + name)]
    if len(candidates) == 1:
        return candidates[0]
    raise QuintInputError(f"ITF must export exactly one {name} variable; found {sorted(candidates)}")


def _validate_manifest(manifest: Any, path: Path) -> dict[str, Any]:
    required = ("io_schema", "module", "model", "source_root", "source_digest", "sources", "quint_version", "backend", "seed",
                "max_steps", "last_step_var", "seam_var", "binary_digest", "binary_version", "scripts",
                "fixtures", "fixture_sources", "requires", "clause_ids", "witnesses", "profile", "command_line")
    _record(manifest, str(path), required)
    if type(manifest["io_schema"]) is not int or manifest["io_schema"] != 1:
        raise QuintInputError(f"{path}: unsupported io_schema {manifest['io_schema']!r}")
    for key in ("module", "model", "source_root", "source_digest", "quint_version", "backend", "seed", "last_step_var", "seam_var",
                "binary_digest", "binary_version", "profile"):
        if not isinstance(manifest[key], str) or not manifest[key]:
            raise QuintInputError(f"{path}: manifest field {key} must be a nonempty string")
    if manifest["quint_version"] != "0.33.0" or manifest["backend"] != "typescript":
        raise QuintInputError(f"{path}: expected Quint 0.33.0 with typescript backend")
    if not INTEGER_RE.fullmatch(manifest["seed"]) or int(manifest["seed"]) < 0:
        raise QuintInputError(f"{path}: seed must be a nonnegative decimal string")
    if type(manifest["max_steps"]) is not int or manifest["max_steps"] <= 0:
        raise QuintInputError(f"{path}: max_steps must be positive")
    if not HEX64_RE.fullmatch(manifest["binary_digest"]):
        raise QuintInputError(f"{path}: binary_digest must be lowercase SHA-256")
    if not HEX64_RE.fullmatch(manifest["source_digest"]):
        raise QuintInputError(f"{path}: source_digest must be lowercase SHA-256")
    if not isinstance(manifest["sources"], list) or not manifest["sources"]:
        raise QuintInputError(f"{path}: sources must be a nonempty list")
    for index, row in enumerate(manifest["sources"]):
        _record(row, f"{path}.sources[{index}]", ("path", "sha256"))
        source_name = row["path"]
        source_parts = Path(source_name).parts if isinstance(source_name, str) else ()
        if not isinstance(source_name, str) or not source_name or Path(source_name).is_absolute() or \
                ".." in source_parts or not isinstance(row["sha256"], str) or not HEX64_RE.fullmatch(row["sha256"]):
            raise QuintInputError(f"{path}: malformed sources[{index}]")
    source_paths = [row["path"] for row in manifest["sources"]]
    if len(source_paths) != len(set(source_paths)):
        raise QuintInputError(f"{path}: duplicate source paths")
    command = manifest["command_line"]
    if not isinstance(command, list) or not command or any(not isinstance(item, str) or not item for item in command):
        raise QuintInputError(f"{path}: command_line must be a nonempty string list")
    for key in ("scripts", "fixtures"):
        if not isinstance(manifest[key], dict):
            raise QuintInputError(f"{path}: {key} must be an object")
    fixture_sources = manifest["fixture_sources"]
    if not isinstance(fixture_sources, list):
        raise QuintInputError(f"{path}: fixture_sources must be a list")
    fixture_source_paths: set[str] = set()
    for index, row in enumerate(fixture_sources):
        _record(row, f"{path}.fixture_sources[{index}]", ("path", "sha256"))
        source_name = row["path"]
        source_parts = Path(source_name).parts if isinstance(source_name, str) else ()
        if not isinstance(source_name, str) or not source_name or Path(source_name).is_absolute() or \
                ".." in source_parts or not isinstance(row["sha256"], str) or not HEX64_RE.fullmatch(row["sha256"]):
            raise QuintInputError(f"{path}: malformed fixture_sources[{index}]")
        if source_name in fixture_source_paths:
            raise QuintInputError(f"{path}: duplicate fixture source path {source_name!r}")
        fixture_source_paths.add(source_name)
        fixture_path = (SPEC_ROOT / source_name).resolve()
        try:
            fixture_path.relative_to(SPEC_ROOT.resolve())
        except ValueError as error:
            raise QuintInputError(f"{path}: fixture source path escapes spec/: {source_name}") from error
        try:
            fixture_digest = hashlib.sha256(fixture_path.read_bytes()).hexdigest()
        except OSError as error:
            raise QuintInputError(f"{path}: cannot read fixture source {source_name!r}: {error}") from error
        if fixture_digest != row["sha256"]:
            raise QuintInputError(f"{path}: fixture source {source_name!r} digest mismatch")
    for script_id, script in manifest["scripts"].items():
        if not NAME_RE.fullmatch(script_id) or not isinstance(script, dict):
            raise QuintInputError(f"{path}: malformed script entry {script_id!r}")
        digest = script.get("digest")
        bare = dict(script)
        bare.pop("digest", None)
        if not isinstance(digest, str) or digest != hashlib.sha256(_canonical_json(bare)).hexdigest():
            raise QuintInputError(f"{path}: script {script_id!r} digest mismatch")
        _validate_script(script, f"{path}.scripts[{script_id!r}]")
    for fixture_name, fixture in manifest["fixtures"].items():
        if not NAME_RE.fullmatch(fixture_name) or not isinstance(fixture, dict):
            raise QuintInputError(f"{path}: malformed fixture entry {fixture_name!r}")
        if type(fixture.get("schema")) is not int or fixture["schema"] != 1:
            raise QuintInputError(f"{path}: fixture {fixture_name!r} must use schema 1")
        blob = fixture.get("bytes")
        if not isinstance(blob, dict) or ("utf8" in blob) == ("octets" in blob):
            raise QuintInputError(f"{path}: fixture {fixture_name!r} needs exactly one utf8/octets blob")
        data = blob["utf8"].encode() if "utf8" in blob and isinstance(blob["utf8"], str) else None
        if "octets" in blob and isinstance(blob["octets"], list) and all(type(item) is int and 0 <= item <= 255 for item in blob["octets"]):
            data = bytes(blob["octets"])
        if data is None or fixture.get("digest") != hashlib.sha256(data).hexdigest():
            raise QuintInputError(f"{path}: fixture {fixture_name!r} digest mismatch")
    if not isinstance(manifest["requires"], dict) or not manifest["requires"]:
        raise QuintInputError(f"{path}: requires must be a nonempty object")
    requires = manifest["requires"]
    if set(requires) != {"platform", "tools", "seams"}:
        raise QuintInputError(f"{path}: requires must contain exactly platform, tools, and seams")
    for key in ("platform", "tools", "seams"):
        values = requires[key]
        if not isinstance(values, list) or any(not isinstance(value, str) or not value for value in values) or \
                len(values) != len(set(values)):
            raise QuintInputError(f"{path}: requires.{key} must be a unique string list")
    if "git" not in requires["tools"]:
        raise QuintInputError(f"{path}: requires.tools must include git for the trace sandbox")
    for key in ("clause_ids", "witnesses"):
        if not isinstance(manifest[key], list) or not manifest[key] or any(not isinstance(item, str) or not item for item in manifest[key]):
            raise QuintInputError(f"{path}: {key} must be a nonempty string list")
    _verify_sources(manifest, path)
    return manifest


def _validate_script(script: dict[str, Any], label: str) -> None:
    if type(script.get("schema")) is not int or script.get("schema") != 1 or not isinstance(script.get("turns"), list):
        raise QuintInputError(f"{label}: expected schema 1 and turns")
    minimum, maximum = script.get("min_requests"), script.get("max_requests")
    if type(minimum) is not int or type(maximum) is not int or not 0 <= minimum <= maximum <= len(script["turns"]):
        raise QuintInputError(f"{label}: invalid request count bounds")
    gates = set()
    for index, turn in enumerate(script["turns"]):
        turn = _record(turn, f"{label}.turns[{index}]", ("request", "response"))
        request = _record(turn["request"], f"{label}.turns[{index}].request", ("method", "headers", "equals", "present"))
        if request["method"] != "POST" or not all(isinstance(request[key], dict) for key in ("headers", "equals")):
            raise QuintInputError(f"{label}.turns[{index}]: malformed request predicate")
        if any(not isinstance(name, str) or not isinstance(value, str) for name, value in request["headers"].items()):
            raise QuintInputError(f"{label}.turns[{index}].request.headers must map strings to strings")
        if not isinstance(request["present"], list) or any(not isinstance(pointer, str) for pointer in request["present"]):
            raise QuintInputError(f"{label}.turns[{index}]: present must be a string list")
        if any(not isinstance(pointer, str) for pointer in request["equals"]):
            raise QuintInputError(f"{label}.turns[{index}]: equals keys must be JSON pointers")
        required_fields = {"/model", "/reasoning/effort"}
        if not required_fields.issubset(request["equals"]):
            raise QuintInputError(f"{label}.turns[{index}]: request must pin /model and /reasoning/effort")
        if "/input" not in request["equals"] and "/input" not in request["present"]:
            raise QuintInputError(f"{label}.turns[{index}]: request must assert /input")
        response = _record(turn["response"], f"{label}.turns[{index}].response", ("status", "headers", "chunks", "disconnect"))
        if type(response["status"]) is not int or not 100 <= response["status"] <= 599:
            raise QuintInputError(f"{label}.turns[{index}]: invalid HTTP status")
        if not isinstance(response["headers"], dict) or not isinstance(response["chunks"], list) or type(response["disconnect"]) is not bool:
            raise QuintInputError(f"{label}.turns[{index}]: malformed response")
        if any(not isinstance(name, str) or not isinstance(value, str)
               for name, value in response["headers"].items()):
            raise QuintInputError(f"{label}.turns[{index}].response.headers must map strings to strings")
        for chunk_index, chunk in enumerate(response["chunks"]):
            chunk = _record(chunk, f"{label}.turns[{index}].chunks[{chunk_index}]", ("bytes", "gate", "delay_ms"))
            _script_blob(chunk["bytes"], lambda value: value)
            if chunk["gate"] is not None:
                if not isinstance(chunk["gate"], str) or not chunk["gate"] or chunk["gate"] in gates:
                    raise QuintInputError(f"{label}: gate labels must be unique nonempty strings")
                gates.add(chunk["gate"])
            if type(chunk["delay_ms"]) is not int or chunk["delay_ms"] < 0:
                raise QuintInputError(f"{label}: delay_ms must be nonnegative")


def _verify_sources(manifest: dict[str, Any], path: Path) -> None:
    source_root = Path(manifest["source_root"])
    if not source_root.is_absolute():
        source_root = (SUITE_ROOT.parent / source_root).resolve()
    if not source_root.is_dir():
        return
    digest = hashlib.sha256()
    for row in sorted(manifest["sources"], key=lambda item: item["path"]):
        source_path = (source_root / row["path"]).resolve()
        try:
            source_path.relative_to(source_root.resolve())
            data = source_path.read_bytes()
        except (OSError, ValueError) as error:
            raise QuintInputError(f"{path}: cannot verify source {row['path']!r}: {error}") from error
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise QuintInputError(f"{path}: source digest mismatch for {row['path']}")
        encoded_path = row["path"].encode("utf-8")
        digest.update(len(encoded_path).to_bytes(8, "big"))
        digest.update(encoded_path)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    if digest.hexdigest() != manifest["source_digest"]:
        raise QuintInputError(f"{path}: source_digest does not match sources")


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(SUITE_ROOT.parent).as_posix()
    except ValueError:
        return str(path)


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def load_quint_cases(cases_dir: Path) -> list[dict[str, Any]]:
    result = []
    for itf_path in sorted(cases_dir.rglob("*.itf.json")):
        manifest_path = itf_path.with_name(itf_path.name[:-len(".itf.json")] + ".manifest.json")
        if not manifest_path.is_file():
            raise QuintInputError(f"{itf_path}: missing companion manifest {manifest_path.name}")
        manifest = _validate_manifest(_read_json(manifest_path), manifest_path)
        _states(itf_path, manifest)
        relative = str(itf_path.relative_to(SUITE_ROOT))
        case_id = f"quint.{manifest['module']}.seed-{manifest['seed']}"
        result.append({"id": case_id, "title": f"{manifest['module']} seed {manifest['seed']}",
                       "_file": relative, "_kind": "quint", "_itf": str(itf_path),
                       "_manifest_file": str(manifest_path), "_manifest": manifest})
    return result


class ScriptedProvider:
    """Local fixture-only Responses server implementing manifest scripts."""

    def __init__(self, scripts: dict[str, Any], substitute: Callable[[str], str]):
        self.scripts = scripts
        self.substitute = substitute
        self.cursors = {script_id: 0 for script_id in scripts}
        self.selected_scripts: set[str] = set()
        self.logs: list[dict[str, Any]] = []
        self.errors: list[str] = []
        self.lock = threading.RLock()
        self.gates: dict[tuple[str, str], tuple[threading.Event, threading.Event]] = {}
        self.used_gates: set[tuple[str, str]] = set()
        self.server: http.server.ThreadingHTTPServer | None = None
        self.thread: threading.Thread | None = None
        self.url = ""
        owner = self

        class Handler(http.server.BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, _format: str, *_args: Any) -> None:
                return

            def do_POST(self) -> None:  # noqa: N802
                raw = self.rfile.read(int(self.headers.get("Content-Length", "0")))
                prefix = "/scripts/"
                if not self.path.startswith(prefix) or not self.path.endswith("/responses"):
                    self._error(404, "unknown scripted endpoint")
                    return
                script_id = urllib.parse.unquote(self.path[len(prefix):-len("/responses")])
                with owner.lock:
                    cursor = owner.cursors.get(script_id)
                    if cursor is None:
                        owner.errors.append(f"unexpected provider script id {script_id!r}")
                        owner.logs.append({"script": script_id, "turn": None, "method": self.command,
                                           "path": self.path, "error": "unexpected provider script id"})
                        self._error(400, "unexpected provider script")
                        return
                    turns = owner.scripts[script_id]["turns"]
                    if cursor >= len(turns):
                        owner.errors.append(f"script {script_id!r}: unexpected request {cursor + 1}")
                        owner._record(script_id, cursor, self, raw, None, "extra request")
                        self._error(400, "no scripted response remains")
                        return
                    turn = turns[cursor]
                    owner.cursors[script_id] += 1
                    record = owner._record(script_id, cursor, self, raw, turn, None)
                mismatch = owner._match_request(record, turn.get("request", {}))
                if mismatch:
                    with owner.lock:
                        owner.errors.extend(f"script {script_id!r} turn {cursor + 1}: {item}" for item in mismatch)
                        owner.logs[-1]["error"] = mismatch
                    self._error(400, "; ".join(mismatch))
                    return
                try:
                    owner._serve(self, script_id, turn.get("response", {}), record)
                except (BrokenPipeError, ConnectionResetError, OSError):
                    return
                except QuintInputError as error:
                    with owner.lock:
                        owner.errors.append(f"script {script_id!r} turn {cursor + 1}: {error}")
                    self._error(500, "invalid scripted response fixture")

            def _error(self, status: int, message: str) -> None:
                payload = json.dumps({"error": {"type": "fixture_error", "message": message}}).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.send_header("Connection", "close")
                self.end_headers()
                try:
                    self.wfile.write(payload)
                except (BrokenPipeError, ConnectionResetError):
                    pass

        class Server(http.server.ThreadingHTTPServer):
            # Join request handlers during server_close so accepted sockets do
            # not outlive the case and accumulate across parallel suite runs.
            daemon_threads = False
            allow_reuse_address = True

            def server_bind(self) -> None:
                # HTTPServer.server_bind reverse-resolves the bind address via
                # getfqdn; macOS leaves an mDNS resolver socket open per call.
                socketserver.TCPServer.server_bind(self)
                self.server_name = str(self.server_address[0])
                self.server_port = int(self.server_address[1])

        self.Handler = Handler
        self.Server = Server

    def start(self) -> "ScriptedProvider":
        self.server = self.Server(("127.0.0.1", 0), self.Handler)
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.thread = threading.Thread(target=self.server.serve_forever, name="kc2-quint-provider", daemon=True)
        self.thread.start()
        return self

    def _record(self, script_id: str, cursor: int, handler: Any, raw: bytes,
                turn: Any, error: str | None) -> dict[str, Any]:
        try:
            body = json.loads(raw.decode("utf-8"), object_pairs_hook=_json_object,
                              parse_float=Decimal, parse_int=int)
        except (UnicodeError, json.JSONDecodeError, QuintInputError):
            body = None
        record = {"script": script_id, "turn": cursor, "method": handler.command,
                  "path": handler.path, "headers": {name.lower(): value.strip() for name, value in handler.headers.items()},
                  "body": body, "request_bytes_sha256": hashlib.sha256(raw).hexdigest(),
                  "request_bytes_base64": base64.b64encode(raw).decode("ascii")}
        if error:
            record["error"] = error
        self.logs.append(record)
        return record

    def _match_request(self, record: dict[str, Any], expected: Any) -> list[str]:
        failures = []
        if not isinstance(expected, dict):
            return ["request predicate must be an object"]
        if "method" in expected and record["method"] != expected["method"]:
            failures.append(f"method expected {expected['method']!r}, got {record['method']!r}")
        headers = record["headers"]
        for name, value in expected.get("headers", {}).items():
            actual = headers.get(str(name).lower())
            want = self.substitute(str(value))
            if actual != want:
                failures.append(f"header {name!r} expected {want!r}, got {actual!r}")
        body = record["body"]
        if not isinstance(body, dict) and (expected.get("equals") or expected.get("present")):
            failures.append("request body is not a JSON object")
        for pointer, want in sorted(expected.get("equals", {}).items()):
            exists, actual = _json_pointer(body, str(pointer))
            resolved = _substitute_json(want, self.substitute)
            if not exists or actual != resolved:
                failures.append(f"JSON pointer {pointer!r} expected {resolved!r}, got {actual!r}" if exists
                                else f"JSON pointer {pointer!r} is missing")
        for pointer in expected.get("present", []):
            exists, _actual = _json_pointer(body, str(pointer))
            if not exists:
                failures.append(f"JSON pointer {pointer!r} is missing")
        return failures

    def _serve(self, handler: Any, script_id: str, response: dict[str, Any], request_record: dict[str, Any]) -> None:
        if not isinstance(response, dict):
            raise QuintInputError(f"script {script_id}: response must be an object")
        status = response.get("status", 200)
        headers = response.get("headers", {})
        chunks = response.get("chunks", [])
        if type(status) is not int or not 100 <= status <= 599 or not isinstance(headers, dict) or not isinstance(chunks, list):
            raise QuintInputError(f"script {script_id}: malformed response")
        disconnect = response.get("disconnect", False)
        if type(disconnect) is not bool:
            raise QuintInputError(f"script {script_id}: disconnect must be boolean")
        resolved_headers = {name: self.substitute(str(value)) for name, value in headers.items()
                            if str(name).lower() not in {"content-length", "connection", "transfer-encoding"}}
        prepared_chunks = []
        for chunk_index, chunk in enumerate(chunks):
            if not isinstance(chunk, dict) or "bytes" not in chunk:
                raise QuintInputError(f"script {script_id}: malformed response chunk {chunk_index}")
            data = _script_blob(chunk["bytes"], self.substitute)
            gate, delay = chunk.get("gate"), chunk.get("delay_ms", 0)
            if gate is not None and (not isinstance(gate, str) or not gate):
                raise QuintInputError(f"script {script_id}: gate must be null or a nonempty string")
            if type(delay) is not int or delay < 0:
                raise QuintInputError(f"script {script_id}: chunk delay_ms must be nonnegative")
            prepared_chunks.append((data, gate, delay))
        emitted_chunks = []
        request_record["response"] = {"status": status, "headers": dict(headers), "chunks": emitted_chunks,
                                      "disconnect": disconnect}
        handler.send_response(status)
        for name, value in resolved_headers.items():
            handler.send_header(str(name), value)
        handler.send_header("Connection", "close")
        handler.end_headers()
        for data, gate, delay in prepared_chunks:
            emitted = {"sha256": hashlib.sha256(data).hexdigest(),
                       "bytes_base64": base64.b64encode(data).decode("ascii"),
                       "gate": gate, "delay_ms": delay}
            emitted_chunks.append(emitted)
            if gate is not None:
                key = (script_id, gate)
                with self.lock:
                    if key in self.gates:
                        self.errors.append(f"duplicate gate arrival name {script_id}/{gate}")
                        raise QuintInputError(f"duplicate gate {script_id}/{gate}")
                    arrived, released = threading.Event(), threading.Event()
                    self.gates[key] = (arrived, released)
                arrived.set()
                if not released.wait(300):
                    self.errors.append(f"gate timed out: {script_id}/{gate}")
                    return
            if delay:
                time.sleep(delay / 1000)
            handler.wfile.write(data)
            handler.wfile.flush()
        if disconnect:
            try:
                handler.connection.shutdown(1)
            except OSError:
                pass

    def await_gate(self, script_id: str, gate: str, timeout_ms: int) -> bool:
        key = (script_id, gate)
        deadline = time.monotonic() + timeout_ms / 1000
        while time.monotonic() < deadline:
            with self.lock:
                entry = self.gates.get(key)
            if entry and entry[0].wait(max(0, deadline - time.monotonic())):
                return True
            time.sleep(min(0.01, max(0, deadline - time.monotonic())))
        return False

    def release_gate(self, script_id: str, gate: str) -> bool:
        with self.lock:
            entry = self.gates.get((script_id, gate))
        if not entry:
            return False
        entry[1].set()
        return True

    def select_script(self, script_id: str | None) -> None:
        if script_id in self.scripts:
            self.selected_scripts.add(script_id)

    def finish(self) -> list[str]:
        failures = list(self.errors)
        for script_id in sorted(self.selected_scripts):
            script = self.scripts[script_id]
            count = self.cursors[script_id]
            if not script["min_requests"] <= count <= script["max_requests"]:
                failures.append(f"script {script_id!r}: request count {count} outside [{script['min_requests']}, {script['max_requests']}]")
        return failures

    def close(self) -> None:
        with self.lock:
            for _arrived, released in self.gates.values():
                released.set()
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.thread:
            self.thread.join(timeout=2)


def _json_pointer(value: Any, pointer: str) -> tuple[bool, Any]:
    if pointer == "":
        return True, value
    if not pointer.startswith("/"):
        return False, None
    current = value
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and token in current:
            current = current[token]
        elif isinstance(current, list) and token.isdecimal() and (token == "0" or not token.startswith("0")):
            index = int(token)
            if index >= len(current):
                return False, None
            current = current[index]
        else:
            return False, None
    return True, current


def _substitute_json(value: Any, substitute: Callable[[str], str]) -> Any:
    if isinstance(value, str):
        return substitute(value)
    if isinstance(value, list):
        return [_substitute_json(item, substitute) for item in value]
    if isinstance(value, dict):
        return {key: _substitute_json(item, substitute) for key, item in value.items()}
    return value


def _script_blob(value: Any, substitute: Callable[[str], str]) -> bytes:
    if not isinstance(value, dict) or ("utf8" in value) == ("octets" in value):
        raise QuintInputError("provider byte blob needs exactly one of utf8 or octets")
    if "utf8" in value and isinstance(value["utf8"], str):
        return substitute(value["utf8"]).encode("utf-8")
    if "octets" in value and isinstance(value["octets"], list) and all(type(x) is int and 0 <= x <= 255 for x in value["octets"]):
        return bytes(value["octets"])
    raise QuintInputError("provider byte blob is malformed")


@dataclass
class CaptureProcess:
    process: subprocess.Popen[bytes]
    started: float
    started_wall: float
    stdout: bytearray
    stderr: bytearray
    stdout_first_ms: int | None = None
    stderr_first_ms: int | None = None
    threads: tuple[threading.Thread, threading.Thread] | None = None
    timed_out: bool = False
    safety_timeout_ms: int | None = None
    terminated: float | None = None
    watcher: threading.Thread | None = None

    @classmethod
    def start(cls, argv: list[str], cwd: str, env: dict[str, str], stdin: bytes,
              timeout_ms: int | None = None) -> "CaptureProcess":
        started_wall = time.time()
        process = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    start_new_session=(os.name == "posix"))
        capture = cls(process, time.monotonic(), started_wall, bytearray(), bytearray(),
                      safety_timeout_ms=timeout_ms)

        def pump(stream: Any, target: bytearray, field: str) -> None:
            try:
                while True:
                    block = stream.read(4096)
                    if not block:
                        break
                    if field == "stdout" and capture.stdout_first_ms is None:
                        capture.stdout_first_ms = int((time.monotonic() - capture.started) * 1000)
                    if field == "stderr" and capture.stderr_first_ms is None:
                        capture.stderr_first_ms = int((time.monotonic() - capture.started) * 1000)
                    target.extend(block)
            finally:
                stream.close()

        out_thread = threading.Thread(target=pump, args=(process.stdout, capture.stdout, "stdout"), daemon=True)
        err_thread = threading.Thread(target=pump, args=(process.stderr, capture.stderr, "stderr"), daemon=True)
        writer_thread: threading.Thread | None = None
        out_thread.start()
        err_thread.start()
        if stdin:
            def write_stdin() -> None:
                try:
                    process.stdin.write(stdin)
                    process.stdin.flush()
                except BrokenPipeError:
                    pass
                finally:
                    process.stdin.close()
            writer_thread = threading.Thread(target=write_stdin, daemon=True)
            writer_thread.start()
        elif process.stdin:
            process.stdin.close()
        capture.threads = (out_thread, err_thread) + ((writer_thread,) if writer_thread else ())

        def watch_exit() -> None:
            deadline = None if timeout_ms is None else capture.started + timeout_ms / 1000
            while process.poll() is None:
                if deadline is not None and time.monotonic() >= deadline:
                    capture.timed_out = True
                    kill_process_group(process.pid, grace_s=0.1)
                    try:
                        process.wait(timeout=0.2)
                    except subprocess.TimeoutExpired:
                        try:
                            process.kill()
                        except ProcessLookupError:
                            pass
                    break
                time.sleep(0.01)
            if capture.terminated is None:
                capture.terminated = time.monotonic()
            kill_process_group(process.pid, grace_s=0.05)
        capture.watcher = threading.Thread(target=watch_exit, daemon=True)
        capture.watcher.start()
        return capture

    def wait(self, timeout_ms: int) -> bool:
        deadline = time.monotonic() + max(0, timeout_ms) / 1000
        try:
            self.process.wait(timeout=max(0, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            return False
        if self.terminated is None:
            self.terminated = time.monotonic()
        for thread in self.threads or ():
            thread.join(timeout=max(0, deadline - time.monotonic()))
        return not any(thread.is_alive() for thread in self.threads or ())

    def terminate(self, sig: int = signal.SIGTERM, group: bool = True) -> None:
        try:
            if group and os.name == "posix":
                os.killpg(self.process.pid, sig)
            else:
                if self.process.poll() is not None:
                    return
                self.process.send_signal(sig)
        except ProcessLookupError:
            pass
        except PermissionError:
            if self.process.poll() is None:
                try:
                    self.process.send_signal(sig)
                except (ProcessLookupError, PermissionError):
                    pass

    def exit_code(self) -> int | None:
        result = self.process.poll()
        if result is None:
            return None
        if self.terminated is None:
            self.terminated = time.monotonic()
        return 128 + -result if result < 0 else result

    def output(self) -> tuple[bytes, bytes]:
        return bytes(self.stdout), bytes(self.stderr)


class TraceBlocked(Exception):
    """The trace requires a platform seam or tool that is not implemented."""


def _process_group_exists(pgid: int) -> bool:
    if os.name != "posix":
        return False
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _wait_group_gone(pgid: int, timeout_ms: int) -> bool:
    deadline = time.monotonic() + timeout_ms / 1000
    while time.monotonic() < deadline:
        if not _process_group_exists(pgid):
            return True
        time.sleep(0.01)
    return not _process_group_exists(pgid)


def _process_identity(pid: int) -> dict[str, Any] | None:
    """Return an OS start identity that can be rechecked before signaling."""
    if pid <= 0:
        return None
    if sys.platform.startswith("linux"):
        proc = Path("/proc") / str(pid)
        try:
            stat_fields = (proc / "stat").read_text(encoding="ascii")
            close = stat_fields.rfind(")")
            fields = stat_fields[close + 2:].split()
            start_ticks = int(fields[19])
            pgid = int(fields[2])
            boot_time = 0
            for line in Path("/proc/stat").read_text(encoding="ascii").splitlines():
                if line.startswith("btime "):
                    boot_time = int(line.split()[1])
                    break
            executable = str((proc / "exe").resolve(strict=True))
            command = (proc / "cmdline").read_bytes().decode("utf-8", "replace").replace("\0", " ").strip()
            environment = (proc / "environ").read_bytes().split(b"\0")
            tmpdir = next((entry.split(b"=", 1)[1].decode("utf-8", "replace")
                           for entry in environment if entry.startswith(b"TMPDIR=")), None)
            start_epoch = boot_time + start_ticks / os.sysconf("SC_CLK_TCK")
        except (OSError, ValueError, IndexError):
            return None
        return {"pid": pid, "start": start_ticks, "start_epoch": start_epoch,
                "executable": executable, "command": command, "pgid": pgid, "tmpdir": tmpdir}
    if sys.platform == "darwin":
        ps = shutil.which("ps", path="/usr/bin:/bin")
        if not ps:
            raise TraceBlocked("captured PID identity needs the host ps tool")

        def field(name: str) -> str | None:
            try:
                result = subprocess.run([ps, "-p", str(pid), "-o", name + "="], capture_output=True,
                                        env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"}, timeout=3)
            except PermissionError as error:
                raise TraceBlocked("host policy does not allow process identity inspection") from error
            if result.returncode:
                return None
            return result.stdout.decode("utf-8", "replace").strip()

        start_text, executable, command, group_text = (field("lstart"), field("comm"),
                                                        field("command"), field("pgid"))
        if not start_text or not executable or not command or not group_text:
            return None
        try:
            environment_result = subprocess.run([ps, "eww", "-p", str(pid), "-o", "command="],
                                                capture_output=True,
                                                env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"}, timeout=3)
        except PermissionError as error:
            raise TraceBlocked("host policy does not allow process environment inspection") from error
        if environment_result.returncode:
            return None
        environment_command = environment_result.stdout.decode("utf-8", "replace")
        tmpdir_match = re.search(r"(?:^|\s)TMPDIR=([^\s]+)", environment_command)
        tmpdir = tmpdir_match.group(1) if tmpdir_match else None
        try:
            start_epoch = datetime.datetime.strptime(start_text, "%a %b %d %H:%M:%S %Y").timestamp()
            pgid = int(group_text)
        except ValueError:
            return None
        return {"pid": pid, "start": start_text, "start_epoch": start_epoch,
                "executable": executable, "command": command, "pgid": pgid, "tmpdir": tmpdir}
    raise TraceBlocked(f"captured PID identity is not implemented on {sys.platform}")


def _same_process_identity(current: dict[str, Any], original: dict[str, Any]) -> bool:
    return all(current.get(key) == original.get(key)
               for key in ("pid", "start", "executable", "pgid", "tmpdir"))


class TraceWorld:
    def __init__(self, case: dict[str, Any], kogen: str, time_scale: float, keep: bool,
                 timeout_s: float = 60.0, workdir: str | Path = "/tmp"):
        self.case = case
        self.manifest = case["_manifest"]
        self.states = _states(Path(case["_itf"]), self.manifest)
        self.kogen = str(Path(kogen).resolve())
        self.time_scale = time_scale
        self.keep = keep
        self.invocation_timeout_ms = max(1, int(timeout_s * 1000))
        self.workdir = Path(workdir).resolve()
        self.root = Path(tempfile.mkdtemp(prefix="kc2-quint-", dir=str(self.workdir))).resolve()
        self.home = self.root / "home"
        self.repo = self.root / "repo"
        self.tmp = self.root / "tmp"
        self.bin = self.root / "bin"
        self.control = self.root / "control"
        self.fixtures = self.root / "fixtures"
        self.gitconfig = self.home / ".gitconfig"
        self.auth_path = self.home / ".kogen" / "auth.json"
        self.clock_path: Path | None = None
        self.barrier_dir: Path | None = None
        self.provider: ScriptedProvider | None = None
        self.processes: dict[str, CaptureProcess] = {}
        self.process_meta: dict[str, dict[str, Any]] = {}
        self.all_processes: list[CaptureProcess] = []
        self.owned_pids: dict[str, dict[str, Any]] = {}
        self.openid_servers: list[subprocess.Popen[bytes]] = []
        self.fixture_installations: dict[str, dict[str, str]] = {}
        self.captures: dict[str, tuple[str, Any]] = {
            "home": ("path", str(self.home)), "repo": ("path", str(self.repo)),
            "tmp": ("path", str(self.tmp)), "bin": ("path", str(self.bin)),
            "control": ("path", str(self.control)), "fixtures": ("path", str(self.fixtures)),
            "kogen": ("path", self.kogen),
        }
        self.results: list[dict[str, Any]] = []
        self.failures: list[str] = []
        self.errors: list[str] = []
        self.provider_failures: list[str] = []
        self.first_failure: dict[str, int] | None = None
        self.barrier_tickets: dict[str, dict[str, Any]] = {}
        self.started = time.monotonic()
        self.current_timings: dict[str, Any] = {}
        self.seam = self.states[0][self.manifest["seam_var"]]
        try:
            for directory in (self.home, self.repo, self.tmp, self.bin, self.control, self.fixtures):
                directory.mkdir(parents=True, exist_ok=True)
            self.binary_digest, self.binary_version = _binary_metadata(Path(self.kogen), strict=False,
                                                                        workdir=self.workdir)
            self._write_gitconfig()
            self._install_fixtures()
            self._install_seam()
            self._start_provider()
            self._init_repo()
        except Exception:
            self.close()
            raise

    def _write_gitconfig(self) -> None:
        self.gitconfig.write_text(
            "[user]\n\tname = Kogen Suite\n\temail = kogen-suite@example.invalid\n"
            "[init]\n\tdefaultBranch = main\n[commit]\n\tgpgsign = false\n"
            "[tag]\n\tgpgsign = false\n[core]\n\tpager = cat\n\tquotepath = false\n"
            "[advice]\n\tdetachedHead = false\n",
            encoding="utf-8")
        self.gitconfig.chmod(0o600)

    def _register_captured_pid(self, name: str, pid: int, result: dict[str, Any]) -> None:
        inherited = next((row for row in self.owned_pids.values() if row["pid"] == pid), None)
        if inherited:
            self.owned_pids[name] = inherited
            return
        direct = next((meta for meta in self.process_meta.values() if meta["pid"] == pid), None)
        if direct:
            handle = next(key for key, meta in self.process_meta.items() if meta is direct)
            self.owned_pids[name] = {"pid": pid, "handle": handle}
            return
        origin = result.get("origin_argv")
        if not isinstance(origin, list) or not origin or origin[0] != self.kogen:
            raise QuintInputError(f"PID capture {name!r} must come from a Kogen CLI result")
        identity = _process_identity(pid)
        if identity is None:
            raise TraceBlocked(f"captured PID {pid} could not be inspected on this host")
        if Path(identity["executable"]).name != Path(self.kogen).name:
            raise QuintInputError(f"captured PID {pid} is not running the tested Kogen executable")
        expected_tmpdir = result.get("process_env_tmpdir")
        if not isinstance(expected_tmpdir, str) or identity.get("tmpdir") != expected_tmpdir:
            raise TraceBlocked(f"captured PID {pid} lacks the trace's unique TMPDIR identity")
        try:
            Path(expected_tmpdir).resolve(strict=False).relative_to(self.root)
        except ValueError as error:
            raise QuintInputError(f"Kogen command TMPDIR escapes the trace sandbox: {expected_tmpdir}") from error
        launch_wall = result.get("process_started_wall")
        if not isinstance(launch_wall, (int, float)) or identity["start_epoch"] < launch_wall - 1.0 or \
                identity["start_epoch"] > time.time() + 1.0:
            raise QuintInputError(f"captured PID {pid} did not start during this trace-owned Kogen command")
        self.owned_pids[name] = {"pid": pid, "identity": identity}

    def _signal_captured_pid(self, name: str, sig: int, process_group: bool) -> dict[str, Any]:
        owned = self.owned_pids.get(name)
        if not owned:
            raise TraceBlocked(f"captured PID binding {name!r} has no verified process identity")
        handle = owned.get("handle")
        if handle:
            process = self.processes[handle]
            process.terminate(sig, group=process_group)
            return {"pid": owned["pid"], "process_group": process.process.pid if process_group else None}
        pid = owned["pid"]
        original = owned["identity"]
        current = _process_identity(pid)
        if current is None or not _same_process_identity(current, original):
            raise QuintInputError(f"captured PID {pid} is no longer the same trace-owned process")
        try:
            if process_group:
                os.killpg(current["pgid"], sig)
            else:
                os.kill(pid, sig)
        except ProcessLookupError as error:
            raise QuintInputError(f"captured PID {pid} exited before signal delivery") from error
        return {"pid": pid, "process_group": current["pgid"] if process_group else None}

    def _install_fixtures(self) -> None:
        for name, fixture in sorted(self.manifest["fixtures"].items()):
            blob = fixture["bytes"]
            if "utf8" in blob:
                data = self._resolve(blob["utf8"]).encode("utf-8")
            else:
                data = bytes(blob["octets"])
            path = self.fixtures / name
            _atomic_write(path, data, 0o600)
            self.fixture_installations[name] = {
                "path": str(path), "template_sha256": fixture["digest"],
                "installed_sha256": hashlib.sha256(data).hexdigest(),
            }
        if self._cli_fixture("server.py").is_file():
            browser = self.bin / "open"
            browser.write_text(
                "#!/usr/bin/env python3\n"
                "import sys, urllib.request\n"
                "if len(sys.argv) != 2: raise SystemExit(2)\n"
                "with urllib.request.urlopen(sys.argv[1], timeout=20) as response: response.read()\n",
                encoding="utf-8")
            browser.chmod(0o755)
            for alias in ("xdg-open", "sensible-browser"):
                target = self.bin / alias
                target.write_text(browser.read_text(encoding="utf-8"), encoding="utf-8")
                target.chmod(0o755)

    def _cli_fixture(self, name: str) -> Path:
        """Find a CLI fixture whether its manifest key is flat or source-relative."""
        for candidate in (self.fixtures / "cli-fixtures" / name, self.fixtures / name):
            if candidate.is_file():
                return candidate
        return self.fixtures / "cli-fixtures" / name

    def _start_openid(self, label: str) -> None:
        """Start the pinned fixture discovery/JWKS/OAuth server for one CLI command."""
        server_script = self._cli_fixture("server.py")
        if not server_script.is_file():
            raise QuintInputError("OpenID command requires cli-fixtures/server.py")
        control = self.control / f"openid-{label}-{len(self.openid_servers)}"
        control.mkdir(parents=True, exist_ok=True)
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
        base = f"http://127.0.0.1:{port}"
        log_path = control / "server.log"
        log = log_path.open("wb")
        environment = {"PATH": "/usr/bin:/bin", "HOME": str(self.home), "TMPDIR": str(self.tmp),
                       "LC_ALL": "C", "TZ": "UTC", "NO_COLOR": "1"}
        process = subprocess.Popen(
            [sys.executable, str(server_script), "serve", "--script", "cli-openid", "--port", str(port),
             "--control", str(control), "--label", label],
            cwd=str(server_script.parent), env=environment, stdin=subprocess.DEVNULL,
            stdout=log, stderr=subprocess.STDOUT, start_new_session=(os.name == "posix"))
        self.openid_servers.append(process)
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if process.poll() is not None:
                log.close()
                detail = log_path.read_text(encoding="utf-8", errors="replace")
                raise QuintInputError(f"OpenID fixture server exited: {detail[-1000:]}")
            try:
                with urllib.request.urlopen(base + "/.well-known/openid-configuration", timeout=0.2):
                    self.captures["auth"] = ("string", base)
                    log.close()
                    return
            except (OSError, urllib.error.URLError):
                time.sleep(0.02)
        log.close()
        raise QuintInputError(f"OpenID fixture server did not bind at {base}")

    def _base_env(self) -> dict[str, str]:
        env = {
            "HOME": str(self.home), "TMPDIR": str(self.tmp), "TMP": str(self.tmp), "TEMP": str(self.tmp),
            "XDG_CONFIG_HOME": str(self.home / ".config"), "LC_ALL": "C", "LANG": "C",
            "TZ": "UTC", "NO_COLOR": "1", "TERM": "dumb", "USER": "kogen-suite",
            "LOGNAME": "kogen-suite", "SHELL": "/bin/sh",
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": str(self.gitconfig),
            "GIT_TERMINAL_PROMPT": "0", "KOGEN_CREDENTIAL_STORE": "file",
        }
        env.update(implementation_environment(self.bin))
        if self.provider:
            env["KOGEN_AUTH_URL"] = self.provider.url
        endpoint = self.seam["endpoint"]
        if endpoint.tag == "ScriptedEndpoint":
            env["KOGEN_PROVIDER_URL"] = self._provider_url(endpoint.value)
        elif endpoint.tag == "InvalidEndpoint":
            env["KOGEN_PROVIDER_URL"] = self._resolve(endpoint.value)
        elif self.provider:
            # DefaultChatGPT traces are permitted only when they make no provider
            # request. Point at a local tripwire so a bad fixture cannot reach a
            # hosted endpoint.
            env["KOGEN_PROVIDER_URL"] = f"{self.provider.url}/scripts/__unexpected__/responses"
        auth = self.seam["auth"]
        if auth.tag == "InjectedAuth":
            env["KOGEN_AUTH_PATH"] = str(self.auth_path)
        elif auth.tag == "InvalidAuth":
            env["KOGEN_AUTH_PATH"] = str(self.auth_path)
        env["KOGEN_TIME_SCALE"] = _permille(self.seam["timeScalePermille"])
        if self.clock_path:
            env["KOGEN_TEST_CLOCK_PATH"] = str(self.clock_path)
        if self.barrier_dir:
            env["KOGEN_TEST_BARRIER_DIR"] = str(self.barrier_dir)
        return env

    def _init_repo(self) -> None:
        env = self._base_env()
        result = subprocess.run(["git", "init", "--initial-branch=main", str(self.repo)], cwd=self.root,
                                env=env, capture_output=True, timeout=15)
        if result.returncode:
            raise QuintInputError(f"trace Git initialization failed: {result.stderr.decode('utf-8', 'replace')}")
        for key, value in (("user.name", "Kogen Suite"), ("user.email", "kogen-suite@example.invalid"),
                           ("commit.gpgsign", "false"), ("tag.gpgsign", "false")):
            result = subprocess.run(["git", "config", key, value], cwd=self.repo, env=env,
                                    capture_output=True, timeout=10)
            if result.returncode:
                raise QuintInputError(f"cannot set isolated Git config {key}: {result.stderr.decode('utf-8', 'replace')}")

    def _install_seam(self) -> None:
        auth = self.seam["auth"]
        if auth.tag == "InjectedAuth":
            credential = auth.value
            account_id = credential["accountId"]
            expires = credential["expiresAtSeconds"]
            if type(expires) is not int or expires <= 0:
                raise QuintInputError("InjectedAuth expiresAtSeconds must be a positive integer")
            wall_present, wall_ms = _optional(self.seam["wallClockMs"], "ioSeam.wallClockMs")
            now_seconds = wall_ms // 1000 if wall_present else int(time.time())
            if expires <= now_seconds:
                raise QuintInputError("InjectedAuth must be valid at the trace's initial wall clock")
            self.auth_path.parent.mkdir(parents=True, exist_ok=True)
            make_injected_auth(str(self.auth_path), str(account_id))
            try:
                record = json.loads(self.auth_path.read_text(encoding="utf-8"))
                # The shared helper supplies a synthetic JWT; pin the requested expiry in its payload.
                token = record["tokens"]["access_token"]
                import base64 as _base64
                header, payload, signature = token.split(".")
                claims = json.loads(_base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
                claims["exp"] = expires
                claims["iat"] = min(now_seconds, expires - 1)
                payload = _base64.urlsafe_b64encode(json.dumps(claims, separators=(",", ":")).encode()).rstrip(b"=").decode()
                record["tokens"]["access_token"] = f"{header}.{payload}.{signature}"
                self.auth_path.write_text(json.dumps(record), encoding="utf-8")
                self.auth_path.chmod(0o600)
            except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
                raise QuintInputError(f"cannot create injected auth fixture: {error}") from error
        elif auth.tag == "InvalidAuth":
            self.auth_path.parent.mkdir(parents=True, exist_ok=True)
            self.auth_path.write_bytes(_substituted_bytes(auth.value, "ioSeam.auth", self._resolve))
            self.auth_path.chmod(0o600)
        wall_observed, wall_ms = _optional(self.seam["wallClockMs"], "ioSeam.wallClockMs")
        if wall_observed:
            self.clock_path = self.control / "clock.json"
            _atomic_write(self.clock_path, json.dumps({"now_ms": wall_ms}).encode(), 0o600)
        if self.seam["barriers"]:
            self.barrier_dir = self.control / "barriers"
            self.barrier_dir.mkdir()

    def _start_provider(self) -> None:
        scripts = self.manifest["scripts"]
        if not scripts:
            self.provider = None
            return
        self.provider = ScriptedProvider(scripts, self._resolve).start()

    def _provider_url(self, script_id: str) -> str:
        if not self.provider:
            raise QuintInputError(f"scripted endpoint {script_id!r} has no manifest script")
        if script_id not in self.manifest["scripts"]:
            raise QuintInputError(f"scripted endpoint references absent script {script_id!r}")
        return f"{self.provider.url}/scripts/{urllib.parse.quote(script_id, safe='')}/responses"

    def _resolve(self, text: str, allow_capture: bool = False) -> str:
        output: list[str] = []
        cursor = 0
        for match in TOKEN_RE.finditer(text):
            output.append(text[cursor:match.start()])
            token = match.group(1)
            if token is None:  # $${ escapes a literal ${
                output.append("${")
            else:
                if token.startswith("capture:"):
                    raise QuintInputError(f"capture token is not allowed in command/setup input: ${{{token}}}")
                reference = _parse_reference(token, self.captures)
                if reference is None:
                    raise QuintInputError(f"unbound placeholder ${{{token}}}")
                output.append(_render_bound(reference[1]))
            cursor = match.end()
        output.append(text[cursor:])
        return "".join(output)

    def _trace_path(self, value: str, *, must_exist_parent: bool = False) -> Path:
        resolved = self._resolve(value)
        path = Path(resolved)
        if not path.is_absolute():
            path = self.repo / path
        # Resolve existing parents while preserving a final symlink for DeletePath/Inspect.
        parent = path.parent.resolve(strict=False)
        normalized = parent / path.name
        try:
            normalized.relative_to(self.root)
        except ValueError as error:
            raise QuintInputError(f"path escapes trace sandbox: {value}") from error
        if must_exist_parent and not parent.exists():
            raise QuintInputError(f"path parent does not exist: {value}")
        return normalized

    def _environment(self, overrides: Any, script_id: str | None = None) -> dict[str, str]:
        env = self._base_env()
        mapping = _validate_named_map(overrides, "command env")
        baseline_provider_url = env.get("KOGEN_PROVIDER_URL")
        provider_url_was_set = False
        for key, value in mapping.items():
            variant = _variant(value, {"SetEnv", "UnsetEnv"}, f"env[{key}]")
            if variant.tag == "UnsetEnv":
                if variant.value != ():
                    raise QuintInputError(f"env[{key}]: UnsetEnv must have unit payload")
                if key in {"KOGEN_PROVIDER_URL", "KOGEN_AUTH_URL"}:
                    raise QuintInputError(f"cannot unset {key}: it would restore a hosted endpoint; use a loopback fixture")
                if key in {"HOME", "TMPDIR", "TMP", "TEMP", "GIT_CONFIG_NOSYSTEM", "KOGEN_CREDENTIAL_STORE"}:
                    raise QuintInputError(f"cannot unset sandbox isolation variable {key}")
                env.pop(key, None)
            else:
                if not isinstance(variant.value, str):
                    raise QuintInputError(f"env[{key}]: SetEnv requires a string")
                env[key] = self._resolve(variant.value)
                if key == "KOGEN_PROVIDER_URL":
                    provider_url_was_set = True
        for key in ("HOME", "TMPDIR", "TMP", "TEMP", "XDG_CONFIG_HOME", "KOGEN_AUTH_PATH",
                    "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM"):
            if key not in env:
                continue
            value = env[key]
            if not value:
                raise QuintInputError(f"{key} may not be empty in a trace command")
            candidate = Path(value)
            if not candidate.is_absolute():
                raise QuintInputError(f"{key} must be an absolute path inside the trace sandbox")
            try:
                candidate.resolve(strict=False).relative_to(self.root)
            except ValueError as error:
                raise QuintInputError(f"{key} escapes the trace sandbox") from error
        if env.get("KOGEN_CREDENTIAL_STORE") != "file":
            raise QuintInputError("KOGEN_CREDENTIAL_STORE is fixed to file inside the trace sandbox")
        if script_id:
            if script_id not in self.manifest["scripts"]:
                raise QuintInputError(f"command references missing provider script {script_id!r}")
            script_url = self._provider_url(script_id)
            explicit = env.get("KOGEN_PROVIDER_URL")
            endpoint = self.seam["endpoint"]
            if provider_url_was_set and explicit != script_url and endpoint.tag != "InvalidEndpoint":
                raise QuintInputError("Cmd.env conflicts with providerScript's local Responses endpoint")
            env["KOGEN_PROVIDER_URL"] = script_url
        elif provider_url_was_set and self.seam["endpoint"].tag != "InvalidEndpoint" and \
                env.get("KOGEN_PROVIDER_URL") != baseline_provider_url:
            raise QuintInputError("Cmd.env provider URL conflicts with ioSeam; use providerScript or InvalidEndpoint")
        for key in ("KOGEN_PROVIDER_URL", "KOGEN_AUTH_URL"):
            if key in env and not _loopback_or_invalid(env[key]):
                raise QuintInputError(f"{key} must use the local fixture server or an invalid non-URL value; internet access is disabled")
        for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
            if key in env and not _loopback_or_invalid(env[key]):
                raise QuintInputError(f"{key} must use loopback; internet access is disabled")
        for name in tuple(env):
            if name.startswith("KOGEN_") and name not in {
                "KOGEN_PROVIDER_URL", "KOGEN_AUTH_PATH", "KOGEN_CREDENTIAL_STORE", "KOGEN_AUTH_URL",
                "KOGEN_TIME_SCALE", "KOGEN_TEST_CLOCK_PATH", "KOGEN_TEST_BARRIER_DIR",
            }:
                env.pop(name, None)
        return env

    def _record_failure(self, message: str, state_index: int, step_index: int) -> None:
        self.failures.append(message)
        if self.first_failure is None:
            self.first_failure = {"state": state_index, "step": step_index}

    def _process_result(self, process: CaptureProcess, *, stdout: bytes | None = None,
                        stderr: bytes | None = None, finished: bool = True) -> dict[str, Any]:
        whole_out, whole_err = process.output()
        code = process.exit_code() if finished else None
        stdout = whole_out if stdout is None else stdout
        stderr = whole_err if stderr is None else stderr
        stdout_text = stdout.decode("utf-8", "replace")
        stderr_text = stderr.decode("utf-8", "replace")
        finished_at = process.terminated if process.terminated is not None else time.monotonic()
        timings: dict[str, int] = {"elapsed_ms": int(((finished_at if finished else time.monotonic()) - process.started) * 1000)}
        if process.stdout_first_ms is not None:
            timings["stdout_first_ms"] = int((process.started - self.started) * 1000) + process.stdout_first_ms
        if process.stderr_first_ms is not None:
            timings["stderr_first_ms"] = int((process.started - self.started) * 1000) + process.stderr_first_ms
        if finished:
            timings["exit_ms"] = int((finished_at - self.started) * 1000)
        self.current_timings = timings
        return {"exitCode": code, "stdout_bytes": stdout, "stderr_bytes": stderr,
                "stdout": stdout_text, "stderr": stderr_text,
                "stdoutLines": _normalized_lines(stdout_text), "stderrLines": _normalized_lines(stderr_text),
                "timings": timings, "timedOut": process.timed_out}

    def run(self) -> dict[str, Any]:
        status = "pass"
        try:
            requirements = self.manifest["requires"]
            missing = _missing_capabilities(requirements, self)
            if missing:
                raise TraceBlocked("required capability is unavailable: " + ", ".join(missing))
            for state_index, state in enumerate(self.states):
                for step_index, step in enumerate(state[self.manifest["last_step_var"]]):
                    try:
                        record = self._run_step(step, state_index, step_index, state)
                    except TraceBlocked:
                        raise
                    except Exception as error:
                        try:
                            action_step = _variant(step, {"Cli", "Setup"}, "step")
                            if action_step.tag == "Cli":
                                raw_argv = action_step.value["cmd"]["argv"]
                                action = "kogen " + " ".join(shlex.quote(arg) for arg in raw_argv)
                            else:
                                op = _variant(action_step.value["op"], {"GitCommand", "WriteFile", "DeletePath", "SendSignal",
                                    "AdvanceClock", "WaitRealMs", "AwaitExit", "AwaitOutput", "ProviderGate",
                                    "AwaitBarrier", "ReleaseBarrier", "Inspect"}, "Setup.op")
                                action = f"Setup.{op.tag}"
                        except Exception:
                            action = "unknown action"
                        message = (f"trace {self.case['id']} state {state_index} step {step_index} action {action}: "
                                   f"harness actual {type(error).__name__}: {error}; reproduce seed "
                                   f"{self.manifest['seed']}: {_reproduce_command(self.case, self.kogen)}")
                        self.errors.append(message)
                        self.first_failure = self.first_failure or {"state": state_index, "step": step_index}
                        self.results.append({"state": state_index, "step": step_index, "action": action,
                                             "kind": "harness-error", "error": f"{type(error).__name__}: {error}",
                                             "failures": [message]})
                        break
                    self.results.append(record)
                    if record.get("failures"):
                        self._record_failure(record["failures"][0], state_index, step_index)
                        break
                if self.failures or self.errors:
                    break
            if self.provider:
                provider_failures = self.provider.finish()
                if self.failures:
                    self.provider_failures.extend(provider_failures)
                else:
                    self.provider_failures.extend(provider_failures)
                if provider_failures:
                    self.failures.extend(f"provider: {failure}" for failure in provider_failures)
                    if self.first_failure is None:
                        last = next((row for row in reversed(self.results) if "state" in row and "step" in row), None)
                        self.first_failure = ({"state": last["state"], "step": last["step"]}
                                              if last else {"state": 0, "step": 0})
            for handle, process in self.processes.items():
                if process.process.poll() is None and process.safety_timeout_ms is not None and \
                        (time.monotonic() - self.process_meta[handle]["started"]) * 1000 >= process.safety_timeout_ms:
                    self.errors.append(f"background process {handle!r} exceeded its real safety timeout")
            if self.errors:
                status = "error"
            elif self.failures:
                status = "fail"
        except TraceBlocked as blocked:
            status = "blocked"
            self.errors.append(f"blocked(seam-or-capability): {blocked}; clauses={','.join(self.manifest['clause_ids'])}")
        except Exception as error:
            status = "error"
            self.errors.append(f"harness error: {type(error).__name__}: {error}")
        return {
            "kind": "case", "id": self.case["id"], "title": self.case["title"],
            "file": self.case["_file"], "status": status,
            "steps": self.results, "failures": self.failures + self.errors,
            "captures": {name: {"type": kind, "value": value} for name, (kind, value) in self.captures.items()},
            "provider_transcript": _plain(self.provider.logs) if self.provider else [],
            "provider_failures": self.provider_failures,
            "fixtures": _plain(self.fixture_installations),
            "seed": self.manifest["seed"], "first_failure": self.first_failure,
            "binary": self.kogen, "binary_digest": self.binary_digest,
            "binary_version": self.binary_version,
            "manifest_binary_digest": self.manifest["binary_digest"],
            "reproduce": _reproduce_command(self.case, self.kogen),
            "sandbox": str(self.root) if self.keep else None,
        }

    def close(self) -> list[str]:
        teardown_errors = []
        seen_pids: set[int] = set()
        for process in self.all_processes:
            if process.process.pid in seen_pids:
                continue
            seen_pids.add(process.process.pid)
            try:
                process.terminate(signal.SIGTERM, group=True)
                process.wait(1000)
                if os.name == "posix" and _process_group_exists(process.process.pid):
                    process.terminate(signal.SIGKILL, group=True)
                    if not _wait_group_gone(process.process.pid, 1000):
                        teardown_errors.append(f"unconfirmed teardown of trace process group {process.process.pid}")
                elif process.process.poll() is None:
                    process.terminate(signal.SIGKILL, group=False)
                    if not process.wait(1000):
                        teardown_errors.append(f"unconfirmed teardown of process {process.process.pid}")
            except OSError as error:
                teardown_errors.append(f"process teardown failed: {error}")
        for owned in self.owned_pids.values():
            pid = owned["pid"]
            if pid in seen_pids:
                continue
            try:
                current = _process_identity(pid)
                if current is None or not _same_process_identity(current, owned["identity"]):
                    continue
                os.killpg(current["pgid"], signal.SIGTERM)
                if not _wait_group_gone(current["pgid"], 1000):
                    os.killpg(current["pgid"], signal.SIGKILL)
                    if not _wait_group_gone(current["pgid"], 1000):
                        teardown_errors.append(f"unconfirmed teardown of captured process group {current['pgid']}")
            except ProcessLookupError:
                pass
            except (OSError, TraceBlocked) as error:
                teardown_errors.append(f"captured process teardown failed for {pid}: {error}")
        for process in self.all_processes:
            for thread in process.threads or ():
                thread.join(timeout=0.25)
            for stream in (process.process.stdin, process.process.stdout, process.process.stderr):
                if stream is not None and not stream.closed:
                    try:
                        stream.close()
                    except OSError as error:
                        teardown_errors.append(f"process pipe close failed for {process.process.pid}: {error}")
            if process.watcher is not None:
                process.watcher.join(timeout=0.25)
        if self.provider:
            try:
                self.provider.close()
            except Exception as error:
                teardown_errors.append(f"provider teardown failed: {error}")
            self.provider = None
        for process in self.openid_servers:
            if process.poll() is None:
                kill_process_group(process.pid, grace_s=0.1)
                try:
                    process.wait(timeout=0.25)
                except subprocess.TimeoutExpired:
                    try:
                        process.kill()
                    except ProcessLookupError:
                        pass
                    try:
                        process.wait(timeout=0.25)
                    except subprocess.TimeoutExpired:
                        teardown_errors.append(f"OpenID fixture server {process.pid} did not exit")
        if hasattr(self, "root") and self.root.exists():
            teardown_errors.extend(cleanup_case_cwd(self.root))
        if hasattr(self, "root") and self.root.exists() and not self.keep:
            shutil.rmtree(self.root, ignore_errors=True)
        return teardown_errors

    def _run_step(self, value: Any, state_index: int, step_index: int,
                  state: dict[str, Any]) -> dict[str, Any]:
        step_started = time.monotonic()
        step = _variant(value, {"Cli", "Setup"}, "step")
        action = state.get("mbt::actionTaken", "unknown")
        action_name = action if isinstance(action, str) else "unknown"
        if step.tag == "Setup":
            body = step.value
            operation = _variant(body["op"], {"GitCommand", "WriteFile", "DeletePath", "SendSignal", "AdvanceClock",
                                                "WaitRealMs", "AwaitExit", "AwaitOutput", "ProviderGate", "AwaitBarrier",
                                                "ReleaseBarrier", "Inspect"}, "setup op")
            cwd = str(self.repo)
            try:
                result, cwd, detail = self._run_setup(operation)
            except QuintInputError as error:
                message = str(error)
                is_wait_failure = (
                    operation.tag == "AwaitBarrier" and "AwaitBarrier timed out" in message or
                    operation.tag == "AwaitOutput" and "AwaitOutput timed out" in message or
                    operation.tag == "ProviderGate" and "ProviderGate await timed out" in message
                )
                if not is_wait_failure:
                    raise
                # A missing synchronization point is an observed implementation
                # result, not a malformed trace or a runner crash.
                for meta in self.process_meta.values():
                    meta["quiescent"] = True
                observed_stdout = observed_stderr = ""
                observed_stdout_bytes = observed_stderr_bytes = b""
                if operation.tag == "AwaitOutput":
                    handle = self._resolve(operation.value["handle"])
                    process = self._process_handle(handle)
                    observed_stdout_bytes, observed_stderr_bytes = process.output()
                    observed_stdout = _strict_text(observed_stdout_bytes, "stdout")
                    observed_stderr = _strict_text(observed_stderr_bytes, "stderr")
                elif operation.tag in {"ProviderGate", "AwaitBarrier"}:
                    script = self._resolve(operation.value["script"]) if operation.tag == "ProviderGate" else None
                    handle = next((name for name, meta in self.process_meta.items()
                                   if script is None or meta.get("provider_script") == script), None)
                    if handle is not None:
                        process = self._process_handle(handle)
                        observed_stdout_bytes, observed_stderr_bytes = process.output()
                        observed_stdout = _strict_text(observed_stdout_bytes, "stdout")
                        observed_stderr = _strict_text(observed_stderr_bytes, "stderr")
                result = {"exitCode": None, "stdout": "", "stderr": "", "stdout_bytes": b"",
                          "stderr_bytes": b"", "stdoutLines": [], "stderrLines": [],
                          "timings": {}, "timedOut": False, "observation_cwd": cwd,
                          "git_cwd": cwd}
                result.update({"stdout": observed_stdout, "stderr": observed_stderr,
                               "stdout_bytes": observed_stdout_bytes, "stderr_bytes": observed_stderr_bytes,
                               "stdoutLines": _normalized_lines(observed_stdout),
                               "stderrLines": _normalized_lines(observed_stderr)})
                detail = {"kind": operation.tag, "value": _plain(operation.value),
                          "wait_failure": message}
                if observed_stdout or observed_stderr:
                    detail["observed_process_output"] = {"stdout": observed_stdout, "stderr": observed_stderr}
            result.setdefault("timings", {})
            result["timings"]["elapsed_ms"] = int((time.monotonic() - step_started) * 1000)
            mode = "setup"
            action_description = f"Setup.{operation.tag}"
        else:
            body = step.value
            command = body["cmd"]
            argv = [self._resolve(arg) for arg in command["argv"]]
            cwd_path = self._trace_path(command["cwd"])
            cwd = str(cwd_path)
            if not cwd_path.is_dir():
                raise QuintInputError(f"CLI cwd does not exist or is not a directory: {cwd}")
            stdin = _substituted_bytes(command["stdin"], "Cmd.stdin", self._resolve)
            provider_present, provider_script = _optional(command["providerScript"], "Cmd.providerScript")
            provider_script = self._resolve(provider_script) if provider_present else None
            if argv[:2] in (["provider", "login"], ["provider", "logout"]):
                label = argv[argv.index("--as") + 1] if "--as" in argv else "default"
                self._start_openid(label)
            env = self._environment(command["env"], provider_script)
            launch = _variant(command["launch"], {"Foreground", "Background"}, "Cmd.launch")
            timeout_ms = min(command["timeoutMs"], self.invocation_timeout_ms)
            detail = {"kind": "Cli", "argv": [self.kogen, *argv], "cwd": cwd,
                      "env_overrides": self._resolved_env_record(command["env"]),
                      "stdin_base64": base64.b64encode(stdin).decode("ascii"),
                      "provider_script": provider_script, "launch": launch.tag,
                      "timeout_ms": timeout_ms}
            if launch.tag == "Background":
                self._assert_background_unobserved(body["expect"])
                handle = self._resolve(launch.value)
                if handle in self.processes:
                    raise QuintInputError(f"background handle {handle!r} already exists")
                process = CaptureProcess.start([self.kogen, *argv], cwd, env, stdin, timeout_ms)
                if self.provider:
                    self.provider.select_script(provider_script or (
                        self.seam["endpoint"].value if self.seam["endpoint"].tag == "ScriptedEndpoint" else None))
                self.processes[handle] = process
                self.all_processes.append(process)
                self.process_meta[handle] = {"argv": [self.kogen, *argv], "cwd": cwd, "pid": process.process.pid,
                                             "started": process.started, "started_wall": process.started_wall,
                                             "pgid": process.process.pid if os.name == "posix" else None,
                                             "env_tmpdir": env.get("TMPDIR"),
                                             "provider_script": provider_script, "quiescent": False}
                pid_binding = handle + ".pid"
                if NAME_RE.fullmatch(pid_binding):
                    if pid_binding in self.captures:
                        raise QuintInputError(f"background process pid binding {pid_binding!r} is already reserved")
                    self.captures[pid_binding] = ("pid", process.process.pid)
                result = {"exitCode": None, "stdout": "", "stderr": "", "stdout_bytes": b"", "stderr_bytes": b"",
                          "stdoutLines": [], "stderrLines": [], "timings": {}, "timedOut": False,
                          "process_started_wall": process.started_wall, "process_env_tmpdir": env.get("TMPDIR")}
                detail["pid"] = process.process.pid
            else:
                result = self._execute([self.kogen, *argv], cwd, env, stdin, timeout_ms)
                result["origin_argv"] = [self.kogen, *argv]
                if self.provider:
                    self.provider.select_script(provider_script or (
                        self.seam["endpoint"].value if self.seam["endpoint"].tag == "ScriptedEndpoint" else None))
            result["observation_cwd"] = cwd
            result["git_cwd"] = cwd
            mode = "cli"
            action_description = "kogen " + " ".join(shlex.quote(arg) for arg in argv)
        expectation = body["expect"]
        if not detail.get("wait_failure"):
            self._assert_snapshot_ready(expectation)
        mismatches = self._compare_expect(expectation, result, cwd, state_index, step_index)
        if detail.get("wait_failure"):
            mismatches.insert(0, detail["wait_failure"])
        if result.get("timedOut"):
            mismatches.insert(0, f"real runner safety timeout after {detail.get('timeout_ms', 'operation bound')} ms; captured output is retained")
        if mismatches:
            reproduce = _reproduce_command(self.case, self.kogen)
            mismatches = [f"trace {self.case['id']} state {state_index} step {step_index} action {action_description}: "
                          f"{mismatches[0]}; reproduce seed {self.manifest['seed']}: {reproduce}"] + mismatches[1:]
        record = {"state": state_index, "step": step_index, "action": action_description,
                  "transition": action_name, "kind": mode,
                  "operation": detail, "expect": _plain(expectation),
                  "result": _result_record(result), "failures": mismatches}
        return record

    def _resolved_env_record(self, value: Any) -> dict[str, Any]:
        result = {}
        for key, item in sorted(_validate_named_map(value, "env").items()):
            variant = _variant(item, {"SetEnv", "UnsetEnv"}, f"env[{key}]")
            result[key] = {"set": self._resolve(variant.value)} if variant.tag == "SetEnv" else {"unset": True}
        return result

    def _assert_background_unobserved(self, expect: Any) -> None:
        for key in ("exitCode", "stdoutLines", "jsonRows", "statusRows"):
            observed, _value = _observation(expect[key], "background expect." + key)
            if observed:
                raise QuintInputError(f"Background launch requires {key} to be Unobserved")
        stderr = expect["stderr"]
        observed, _value = _observation(stderr["class"], "background stderr.class")
        if observed or _variant(stderr["text"], {"IgnoreText", "ExactLines", "Pattern"}, "background stderr.text").tag != "IgnoreText":
            raise QuintInputError("Background launch requires stderr class/text to be unobserved")
        observed, _value = _observation(expect["git"], "background git")
        if observed or _validate_named_map(expect["files"], "background files") or \
                _validate_named_map(expect["jsonFiles"], "background jsonFiles"):
            raise QuintInputError("Background launch Git/files observations require a later readiness barrier")

    def _assert_snapshot_ready(self, expect: Any) -> None:
        git_observed, _ = _observation(expect["git"], "Expect.git")
        wants_snapshot = git_observed or bool(_validate_named_map(expect["files"], "Expect.files")) or \
                bool(_validate_named_map(expect["jsonFiles"], "Expect.jsonFiles"))
        if not wants_snapshot:
            return
        pending = [handle for handle, meta in self.process_meta.items()
                   if not meta.get("quiescent")]
        if pending:
            raise QuintInputError(f"Git/files observation requires readiness for background handle(s): {', '.join(pending)}")

    def _execute(self, argv: list[str], cwd: str, env: dict[str, str], stdin: bytes,
                 timeout_ms: int) -> dict[str, Any]:
        process = CaptureProcess.start(argv, cwd, env, stdin, timeout_ms)
        self.all_processes.append(process)
        completed = process.wait(timeout_ms)
        if not completed:
            process.timed_out = True
            process.terminate(signal.SIGTERM)
            if not process.wait(1000):
                process.terminate(signal.SIGKILL)
                process.wait(1000)
        kill_process_group(process.process.pid, grace_s=0.05)
        result = self._process_result(process, finished=True)
        result["exitCode"] = 124 if process.timed_out else process.exit_code()
        result["process_started_wall"] = process.started_wall
        result["process_env_tmpdir"] = env.get("TMPDIR")
        return result

    def _run_setup(self, operation: Variant) -> tuple[dict[str, Any], str, dict[str, Any]]:
        tag, data = operation.tag, operation.value
        cwd = str(self.repo)
        detail: dict[str, Any] = {"kind": tag, "value": _plain(data)}
        if tag == "GitCommand":
            executable = self._resolve(data["executable"])
            if executable != "git":
                raise QuintInputError(f"GitCommand executable must be exactly 'git', got {executable!r}")
            argv = [self._resolve(arg) for arg in data["argv"]]
            cwd_path = self._trace_path(data["cwd"])
            if not cwd_path.is_dir():
                raise QuintInputError(f"GitCommand cwd is not a directory: {cwd_path}")
            cwd = str(cwd_path)
            env = self._environment(data["env"])
            stdin = _substituted_bytes(data["stdin"], "GitCommand.stdin", self._resolve)
            _reject_network_git(argv)
            detail.update({"argv": ["git", *argv], "cwd": cwd,
                           "env_overrides": self._resolved_env_record(data["env"]),
                           "stdin_base64": base64.b64encode(stdin).decode("ascii"),
                           "timeout_ms": data["timeoutMs"]})
            result = self._execute(["git", *argv], cwd, env, stdin, data["timeoutMs"])
            result["observation_cwd"] = cwd
            result["git_cwd"] = cwd
            return result, cwd, detail
        if tag == "WriteFile":
            path = self._trace_path(data["path"])
            contents = _substituted_bytes(data["bytes"], "WriteFile.bytes", self._resolve)
            path.parent.mkdir(parents=True, exist_ok=True)
            _atomic_write(path, contents, data["mode"])
            detail = {"kind": tag, "path": str(path), "bytes_base64": base64.b64encode(contents).decode("ascii"),
                      "mode": data["mode"]}
        elif tag == "DeletePath":
            path = self._trace_path(data)
            if path.is_symlink() or path.is_file():
                path.unlink(missing_ok=True)
            elif path.is_dir():
                shutil.rmtree(path)
            detail = {"kind": tag, "path": str(path)}
        elif tag == "SendSignal":
            raw_target = data["target"]
            target = self._resolve(raw_target)
            handle = target if target in self.processes else None
            captured_name = None
            if not handle and raw_target.startswith("${") and raw_target.endswith("}"):
                token = raw_target[2:-1]
                binding = self.captures.get(token)
                if binding and binding[0] == "pid":
                    captured_name = token
            if not handle and not captured_name:
                raise QuintInputError("SendSignal target must be a trace-owned handle or typed captured PID")
            signal_value = _signal_number(data["signal"])
            if handle:
                process = self.processes[handle]
                process.terminate(signal_value, group=data["processGroup"])
                detail = {"kind": tag, "target": handle, "signal": data["signal"],
                          "process_group": data["processGroup"]}
            else:
                identity_record = self._signal_captured_pid(captured_name, signal_value, data["processGroup"])
                detail = {"kind": tag, "target": captured_name, "signal": data["signal"],
                          **identity_record}
        elif tag == "AdvanceClock":
            if not self.clock_path:
                raise TraceBlocked("AdvanceClock requires ioSeam.wallClockMs Present")
            try:
                record = json.loads(self.clock_path.read_text(encoding="utf-8"))
                now_ms = record["now_ms"]
            except (OSError, KeyError, json.JSONDecodeError, TypeError) as error:
                raise QuintInputError(f"invalid CORE clock seam file: {error}") from error
            if type(now_ms) is not int or now_ms < 0:
                raise QuintInputError("CORE clock seam now_ms must be a nonnegative integer")
            _atomic_write(self.clock_path, json.dumps({"now_ms": now_ms + data}).encode(), 0o600)
            detail = {"kind": tag, "delta_ms": data, "now_ms": now_ms + data}
        elif tag == "WaitRealMs":
            time.sleep(data / 1000)
            detail = {"kind": tag, "milliseconds": data}
        elif tag == "AwaitExit":
            handle = self._resolve(data["handle"])
            process = self._process_handle(handle)
            before = time.monotonic()
            if not process.wait(data["timeoutMs"]):
                raise QuintInputError(f"AwaitExit timed out for handle {handle!r}")
            kill_process_group(process.process.pid, grace_s=0.05)
            result = self._process_result(process, finished=True)
            result["timings"]["elapsed_ms"] = int((time.monotonic() - before) * 1000)
            self.process_meta[handle]["quiescent"] = True
            result["observation_cwd"] = self.process_meta[handle]["cwd"]
            result["git_cwd"] = self.process_meta[handle]["cwd"]
            result["origin_argv"] = self.process_meta[handle]["argv"]
            result["process_started_wall"] = process.started_wall
            result["process_env_tmpdir"] = self.process_meta[handle]["env_tmpdir"]
            detail = {"kind": tag, "handle": handle, "elapsed_ms": int((time.monotonic() - before) * 1000)}
            return result, result["git_cwd"], detail
        elif tag == "AwaitOutput":
            handle = self._resolve(data["handle"])
            process = self._process_handle(handle)
            stream = data["stream"]
            if stream not in ("stdout", "stderr"):
                raise QuintInputError("AwaitOutput stream must be stdout or stderr")
            expression = _portable_regex(self._resolve(data["pattern"]))
            wait_started = time.monotonic()
            deadline = time.monotonic() + data["timeoutMs"] / 1000
            match_end = None
            matched_bytes = b""
            while time.monotonic() < deadline:
                output = bytes(process.stdout if stream == "stdout" else process.stderr)
                text = _strict_text(output, stream)
                found = expression.search(_normalize_text(text))
                if found:
                    match_end = found.end()
                    matched_text = _normalize_text(text)[:match_end]
                    matched_bytes = matched_text.encode("utf-8")
                    break
                if process.process.poll() is not None:
                    break
                time.sleep(0.01)
            if match_end is None:
                raise QuintInputError(f"AwaitOutput timed out waiting for {stream} pattern {data['pattern']!r}")
            all_out, all_err = process.output()
            selected = matched_bytes
            result = self._process_result(process, stdout=selected if stream == "stdout" else all_out,
                                          stderr=selected if stream == "stderr" else all_err, finished=False)
            result["exitCode"] = None
            result["timings"]["elapsed_ms"] = int((time.monotonic() - wait_started) * 1000)
            result["timings"]["output_match_ms"] = int((time.monotonic() - self.started) * 1000)
            result["observation_cwd"] = self.process_meta[handle]["cwd"]
            result["git_cwd"] = self.process_meta[handle]["cwd"]
            result["origin_argv"] = self.process_meta[handle]["argv"]
            result["process_started_wall"] = process.started_wall
            result["process_env_tmpdir"] = self.process_meta[handle]["env_tmpdir"]
            self.process_meta[handle]["quiescent"] = True
            detail = {"kind": tag, "handle": handle, "stream": stream, "pattern": data["pattern"],
                      "matched_prefix_base64": base64.b64encode(matched_bytes).decode("ascii")}
            return result, result["git_cwd"], detail
        elif tag == "ProviderGate":
            if not self.provider:
                raise TraceBlocked("ProviderGate requires a local scripted provider")
            script, gate, operation_name = map(self._resolve, (data["script"], data["gate"], data["operation"]))
            if script not in self.manifest["scripts"]:
                raise QuintInputError(f"ProviderGate references missing script {script!r}")
            if operation_name == "await":
                if not self.provider.await_gate(script, gate, data["timeoutMs"]):
                    raise QuintInputError(f"ProviderGate await timed out: {script}/{gate}")
                for meta in self.process_meta.values():
                    if meta.get("provider_script") == script:
                        meta["quiescent"] = True
            elif operation_name == "release":
                if not self.provider.release_gate(script, gate):
                    raise QuintInputError(f"ProviderGate release references an unknown gate: {script}/{gate}")
            else:
                raise QuintInputError(f"unknown ProviderGate operation {operation_name!r}")
            detail = {"kind": tag, "script": script, "gate": gate, "operation": operation_name}
        elif tag == "AwaitBarrier":
            if not self.barrier_dir:
                raise TraceBlocked("AwaitBarrier requires ioSeam.barriers")
            point, ticket_name = self._resolve(data["point"]), self._resolve(data["ticket"])
            if not NAME_RE.fullmatch(ticket_name) or ticket_name in self.barrier_tickets or ticket_name in self.captures:
                raise QuintInputError(f"AwaitBarrier ticket binding is invalid or already used: {ticket_name!r}")
            ticket = self._await_barrier(point, data["timeoutMs"])
            for meta in self.process_meta.values():
                meta["quiescent"] = True
            self.barrier_tickets[ticket_name] = ticket
            for suffix in ("run_id", "workspace", "expected_base", "ordinal", "point"):
                if suffix in ticket:
                    self.captures[f"{ticket_name}.{suffix}"] = ("string" if suffix != "ordinal" else "int", ticket[suffix])
            self.captures[ticket_name] = ("ticket", ticket_name)
            detail = {"kind": tag, "point": point, "ticket": ticket_name, "metadata": ticket}
        elif tag == "ReleaseBarrier":
            ticket_name = self._resolve(data)
            ticket = self.barrier_tickets.get(ticket_name)
            if not ticket:
                raise QuintInputError(f"ReleaseBarrier references unknown ticket {ticket_name!r}")
            release_path = ticket.get("release_path")
            if not release_path:
                arrival = Path(ticket["_path"])
                release_path = str(arrival.with_suffix(".release"))
            path = self._trace_path(str(release_path))
            _atomic_write(path, b"release\n", 0o600)
            detail = {"kind": tag, "ticket": ticket_name, "release_path": str(path)}
        elif tag == "Inspect":
            detail = {"kind": tag}
        else:
            raise TraceBlocked(f"Setup operation {tag} is not implemented")
        elapsed = 0
        timings = {"elapsed_ms": elapsed}
        if tag == "Inspect":
            # Inspect marks the watch-launch baseline in trace-relative time.
            timings["exit_ms"] = int((time.monotonic() - self.started) * 1000)
        return {"exitCode": 0, "stdout": "", "stderr": "", "stdout_bytes": b"", "stderr_bytes": b"",
                "stdoutLines": [], "stderrLines": [], "timings": timings, "timedOut": False,
                "observation_cwd": cwd, "git_cwd": cwd}, cwd, detail

    def _process_handle(self, handle: str) -> CaptureProcess:
        if handle not in self.processes:
            raise QuintInputError(f"unknown background process handle {handle!r}")
        process = self.processes[handle]
        meta = self.process_meta[handle]
        timeout_ms = process.safety_timeout_ms
        if timeout_ms is not None and process.process.poll() is None and (time.monotonic() - meta["started"]) * 1000 > timeout_ms:
            process.timed_out = True
            process.terminate(signal.SIGTERM)
            if not process.wait(1000):
                process.terminate(signal.SIGKILL)
                process.wait(1000)
            raise QuintInputError(f"background process {handle!r} exceeded its real safety timeout")
        return process

    def _await_barrier(self, point: str, timeout_ms: int) -> dict[str, Any]:
        assert self.barrier_dir is not None
        deadline = time.monotonic() + timeout_ms / 1000
        while time.monotonic() < deadline:
            for path in sorted(self.barrier_dir.glob("**/*.json")):
                if str(path) in {row.get("_path") for row in self.barrier_tickets.values()}:
                    continue
                try:
                    record = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_json_object)
                except (OSError, json.JSONDecodeError, QuintInputError):
                    continue
                if isinstance(record, dict) and record.get("point") == point:
                    required = ("run_id", "workspace", "expected_base", "ordinal", "point")
                    missing = [key for key in required if key not in record]
                    if missing:
                        raise QuintInputError(f"barrier arrival {path} is missing {', '.join(missing)}")
                    for key in ("run_id", "workspace", "expected_base", "point"):
                        if not isinstance(record[key], str) or not record[key]:
                            raise QuintInputError(f"barrier arrival {path} has invalid {key}")
                    if type(record["ordinal"]) is not int or record["ordinal"] < 1:
                        raise QuintInputError(f"barrier arrival {path} has invalid 1-based ordinal")
                    if not GIT_ID_RE.fullmatch(record["expected_base"]):
                        raise QuintInputError(f"barrier arrival {path} has invalid expected_base object id")
                    record["_path"] = str(path)
                    return record
            time.sleep(0.01)
        raise QuintInputError(f"AwaitBarrier timed out at point {point!r}")

    def _compare_expect(self, expect: Any, result: dict[str, Any], cwd: str,
                        state_index: int, step_index: int) -> list[str]:
        return _compare_expect(self, expect, result, cwd, state_index, step_index)


def _compare_expect(world: TraceWorld, expect: Any, result: dict[str, Any], cwd: str,
                    state_index: int, step_index: int) -> list[str]:
    tentative = dict(world.captures)
    failures: list[str] = []
    expected_record = _record(expect, "Expect")
    label = f"state {state_index} step {step_index}"
    observed: dict[str, Any] = {}
    enabled, value = _observation(expected_record["exitCode"], "Expect.exitCode")
    if enabled:
        if type(value) is not int or result.get("exitCode") != value:
            failures.append(f"{label} exitCode: expected {value!r}, got {result.get('exitCode')!r}")
        observed["exitCode"] = result.get("exitCode")

    enabled, expected_lines = _observation(expected_record["stdoutLines"], "Expect.stdoutLines")
    if enabled:
        try:
            actual_lines = _normalized_lines(_strict_text(result.get("stdout_bytes", b""), "stdout"))
        except QuintInputError as error:
            actual_lines = []
            failures.append(f"{label} stdoutLines: {error}")
        if not isinstance(expected_lines, list) or len(expected_lines) != len(actual_lines):
            failures.append(f"{label} stdoutLines: expected {len(expected_lines) if isinstance(expected_lines, list) else 'a list'} lines, got {len(actual_lines)}")
        else:
            for index, fragments in enumerate(expected_lines):
                if not isinstance(fragments, list) or any(not isinstance(fragment, str) for fragment in fragments):
                    failures.append(f"{label} stdoutLines[{index}]: expected a Line (list of string fragments)")
                    continue
                expected_text = "".join(fragments)
                errors = _match_template(actual_lines[index], expected_text, tentative, world.root,
                                         f"{label} stdoutLines[{index}]")
                failures.extend(errors)
        observed["stdoutLines"] = result.get("stdoutLines", [])

    stderr_spec = _record(expected_record["stderr"], "Expect.stderr", ("class", "text"))
    enabled, expected_class = _observation(stderr_spec["class"], "Expect.stderr.class")
    if enabled:
        errors = _compare_stderr_class(str(expected_class), result)
        failures.extend(f"{label} stderr.class: {error}" for error in errors)
        observed["stderr.class"] = errors if errors else expected_class
    text_match = _variant(stderr_spec["text"], {"IgnoreText", "ExactLines", "Pattern"}, "Expect.stderr.text")
    if text_match.tag == "ExactLines":
        expected_err_lines = text_match.value
        try:
            actual_err_lines = _normalized_lines(_strict_text(result.get("stderr_bytes", b""), "stderr"))
        except QuintInputError as error:
            actual_err_lines = []
            failures.append(f"{label} stderr.text: {error}")
        if not isinstance(expected_err_lines, list) or len(expected_err_lines) != len(actual_err_lines):
            failures.append(f"{label} stderr.text: expected {len(expected_err_lines) if isinstance(expected_err_lines, list) else 'a list'} lines, got {len(actual_err_lines)}")
        else:
            for index, fragments in enumerate(expected_err_lines):
                if not isinstance(fragments, list) or any(not isinstance(fragment, str) for fragment in fragments):
                    failures.append(f"{label} stderr.text[{index}]: expected a Line")
                    continue
                failures.extend(_match_template(actual_err_lines[index], "".join(fragments), tentative,
                                                world.root, f"{label} stderr.text[{index}]"))
        observed["stderr.text"] = result.get("stderrLines", [])
    elif text_match.tag == "Pattern":
        if not isinstance(text_match.value, str):
            failures.append(f"{label} stderr Pattern payload is not a string")
        else:
            try:
                stderr_text = "\n".join(_normalized_lines(_strict_text(result.get("stderr_bytes", b""), "stderr")))
            except QuintInputError as error:
                failures.append(f"{label} stderr Pattern: {error}")
            else:
                errors = _match_pattern(stderr_text, text_match.value, tentative, world.root,
                                        f"{label} stderr Pattern")
                failures.extend(errors)
        observed["stderr.text"] = result.get("stderr", "")

    json_rows: list[dict[str, Any]] | None = None
    for field in ("jsonRows", "statusRows"):
        enabled, expected_rows = _observation(expected_record[field], "Expect." + field)
        if not enabled:
            continue
        if json_rows is None:
            json_rows, parse_error = _parse_jsonl(result.get("stdout_bytes", b""))
            if parse_error:
                failures.append(f"{label} {field}: {parse_error}")
                json_rows = []
        if field == "statusRows":
            failures.extend(f"{label} statusRows: {error}" for error in _validate_status_rows(json_rows or []))
        if not isinstance(expected_rows, list):
            failures.append(f"{label} {field}: expected a list of JsonRow records")
        elif len(expected_rows) != len(json_rows or []):
            failures.append(f"{label} {field}: expected {len(expected_rows)} rows, got {len(json_rows or [])}")
        else:
            for row_index, expected_row in enumerate(expected_rows):
                errors = _compare_json_row(json_rows[row_index], expected_row, tentative, world.root,
                                           f"{label} {field}[{row_index}]")
                failures.extend(errors)
        observed[field] = json_rows or []

    enabled, expected_git = _observation(expected_record["git"], "Expect.git")
    if enabled:
        try:
            actual_git = _git_snapshot(world, cwd)
            errors = _compare_git(expected_git, actual_git, tentative, world.root, f"{label} git")
            failures.extend(errors)
            observed["git"] = actual_git
        except (OSError, subprocess.SubprocessError, QuintInputError) as error:
            failures.append(f"{label} git observation: {error}")

    files = _validate_named_map(expected_record["files"], "Expect.files")
    file_actual = {}
    for raw_path, expectation in sorted(files.items(), key=lambda item: str(item[0])):
        try:
            path_value = _expected_key(str(raw_path), tentative)
        except QuintInputError as error:
            failures.append(f"{label} files path {raw_path!r}: {error}")
            continue
        path = world._trace_path(path_value)
        try:
            errors, snapshot = _compare_file(path, expectation, tentative, world.root,
                                             f"{label} files[{path_value!r}]")
        except (OSError, QuintInputError) as error:
            errors, snapshot = [str(error)], None
        failures.extend(errors)
        file_actual[path_value] = snapshot
    if files:
        observed["files"] = file_actual

    json_files = _validate_named_map(expected_record["jsonFiles"], "Expect.jsonFiles")
    json_file_actual = {}
    for raw_path, expected_rows in sorted(json_files.items(), key=lambda item: str(item[0])):
        try:
            path_value = _expected_key(str(raw_path), tentative)
        except QuintInputError as error:
            failures.append(f"{label} jsonFiles path {raw_path!r}: {error}")
            continue
        path = world._trace_path(path_value)
        try:
            data = path.read_bytes()
            rows, parse_error = _parse_jsonl(data)
        except OSError as error:
            rows, parse_error = [], f"cannot read file: {error}"
        json_file_actual[path_value] = rows
        if parse_error:
            failures.append(f"{label} jsonFiles[{path_value!r}]: {parse_error}")
        elif not isinstance(expected_rows, list) or len(expected_rows) != len(rows):
            failures.append(f"{label} jsonFiles[{path_value!r}]: expected {len(expected_rows) if isinstance(expected_rows, list) else 'a list'} rows, got {len(rows)}")
        else:
            for row_index, expected_row in enumerate(expected_rows):
                failures.extend(_compare_json_row(rows[row_index], expected_row, tentative, world.root,
                                                  f"{label} jsonFiles[{path_value!r}][{row_index}]"))
    if json_files:
        observed["jsonFiles"] = json_file_actual

    timing_expectations = _validate_named_map(expected_record["timings"], "Expect.timings")
    if timing_expectations:
        actual_timings = result.get("timings", {})
        observed["timings"] = dict(actual_timings)
        for name, expected_atom in sorted(timing_expectations.items()):
            if name not in actual_timings:
                failures.append(f"{label} timings[{name!r}]: measurement was not recorded")
                continue
            failures.extend(_compare_json_atom(actual_timings[name], expected_atom, tentative, world.root,
                                               f"{label} timings[{name!r}]", integer_only=True))

    relations = expected_record["relations"]
    if not isinstance(relations, list):
        failures.append(f"{label} relations must be a list")
    else:
        for index, relation in enumerate(relations):
            try:
                failures.extend(_compare_relation(relation, tentative, f"{label} relations[{index}]"))
            except QuintInputError as error:
                failures.append(f"{label} relations[{index}]: {error}")

    if not failures:
        for name, (kind, value) in tentative.items():
            previous = world.captures.get(name)
            if kind == "pid" and (previous is None or previous != (kind, value)):
                world._register_captured_pid(name, value, result)
        world.captures = tentative
    result["observed"] = observed
    return failures


def _compare_stderr_class(expected: str, result: dict[str, Any]) -> list[str]:
    stderr_bytes = result.get("stderr_bytes", b"")
    stderr_lines = result.get("stderrLines", [])
    code = result.get("exitCode")
    if expected == "empty":
        return [] if not stderr_bytes else ["expected empty stderr"]
    if expected == "warning":
        if code != 0:
            return [f"warning stderr requires exit 0, got {code}"]
        try:
            warning_lines = _normalized_lines(_strict_text(stderr_bytes, "stderr"))
        except QuintInputError as error:
            return [str(error)]
        if not warning_lines or any(not line.startswith("kogen: warning:") for line in warning_lines):
            return ["expected nonempty lines beginning 'kogen: warning:'"]
        return []
    if expected not in {"usage", "environment", "provider", "decision", "bug", "sigterm", "no", "other"}:
        return [f"unknown stderr class {expected!r}"]
    if not stderr_bytes:
        return [f"expected nonempty stderr for class {expected}"]
    class_codes = {"usage": 2, "environment": 3, "provider": 4, "decision": 5,
                   "bug": 70, "sigterm": 143, "no": 1}
    if expected in class_codes and code != class_codes[expected]:
        return [f"class {expected} requires exit {class_codes[expected]}, got {code}"]
    return []


def _parse_jsonl(data: bytes) -> tuple[list[dict[str, Any]], str | None]:
    if not data:
        return [], None
    try:
        text = data.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        return [], f"stdout/file is not valid UTF-8: {error}"
    # Split on LF only so spaces and blank rows remain visible.
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    rows = []
    for number, line in enumerate(lines, 1):
        if not line.strip():
            return [], f"line {number} is blank, not a JSON value"
        try:
            rows.append(json.loads(line, object_pairs_hook=_json_object,
                                   parse_float=Decimal, parse_int=int, parse_constant=_reject_json_constant))
        except (json.JSONDecodeError, QuintInputError) as error:
            return [], f"line {number} is not valid duplicate-free JSON: {error}"
    return rows, None


def _flatten_json(value: Any) -> dict[str, Any]:
    atoms: dict[str, Any] = {}
    objects: set[str] = set()
    arrays: dict[str, int] = {}

    def visit(node: Any, pointer: str) -> None:
        if isinstance(node, dict):
            objects.add(pointer)
            for key, child in node.items():
                escaped = str(key).replace("~", "~0").replace("/", "~1")
                visit(child, pointer + "/" + escaped)
        elif isinstance(node, list):
            arrays[pointer] = len(node)
            for index, child in enumerate(node):
                visit(child, pointer + "/" + str(index))
        elif node is None or isinstance(node, (str, bool, int, Decimal)):
            atoms[pointer] = node
        else:
            raise QuintInputError(f"JSON value contains unsupported scalar {type(node).__name__}")
    visit(value, "")
    return {"atoms": atoms, "objects": objects, "arrays": arrays}


def _compare_json_row(actual_value: Any, expected: Any, bindings: dict[str, tuple[str, Any]],
                      root: Path, label: str) -> list[str]:
    if not isinstance(expected, dict):
        return [f"{label}: expected JsonRow record"]
    try:
        actual = _flatten_json(actual_value)
        expected_atoms = _validate_named_map(expected["atoms"], label + ".atoms")
        expected_objects = expected["objects"]
        expected_arrays = _validate_named_map(expected["arrays"], label + ".arrays")
        if not isinstance(expected_objects, ITFSet):
            return [f"{label}.objects must be a Quint Set"]
    except (KeyError, QuintInputError) as error:
        return [f"{label}: malformed JsonRow: {error}"]
    failures = []
    try:
        paths_atoms = {_expected_key(str(key), bindings) for key in expected_atoms}
        paths_objects = {_expected_key(str(path), bindings) for path in expected_objects.values}
        expected_array_values = {_expected_key(str(path), bindings): length for path, length in expected_arrays.items()}
    except QuintInputError as error:
        return [f"{label}: {error}"]
    if paths_atoms != set(actual["atoms"]):
        failures.append(f"{label}.atoms: expected pointers {sorted(paths_atoms)!r}, got {sorted(actual['atoms'])!r}")
    for raw_path, atom in sorted(expected_atoms.items(), key=lambda item: str(item[0])):
        path = _expected_key(str(raw_path), bindings)
        if path in actual["atoms"]:
            failures.extend(_compare_json_atom(actual["atoms"][path], atom, bindings, root, f"{label}.atoms[{path!r}]"))
    if paths_objects != actual["objects"]:
        failures.append(f"{label}.objects: expected {sorted(paths_objects)!r}, got {sorted(actual['objects'])!r}")
    if expected_array_values != actual["arrays"]:
        failures.append(f"{label}.arrays: expected {expected_array_values!r}, got {actual['arrays']!r}")
    return failures


def _compare_json_atom(actual: Any, expected: Any, bindings: dict[str, tuple[str, Any]],
                       root: Path, label: str, integer_only: bool = False) -> list[str]:
    if not isinstance(expected, Variant):
        return [f"{label}: expected JsonAtom constructor"]
    tag, value = expected.tag, expected.value
    if integer_only and tag not in {"JInt", "JSymbol"}:
        return [f"{label}: timings allow only JInt or integer JSymbol"]
    if tag == "JNull":
        return [] if actual is None else [f"{label}: expected null, got {actual!r}"]
    if tag == "JBool":
        return [] if type(actual) is bool and actual == value else [f"{label}: expected boolean {value!r}, got {actual!r}"]
    if tag == "JInt":
        return [] if type(actual) is int and actual == value else [f"{label}: expected integer {value!r}, got {actual!r}"]
    if tag == "JDecimal":
        if not isinstance(value, str):
            return [f"{label}: JDecimal payload must be a string"]
        try:
            expected_decimal = Decimal(value)
        except InvalidOperation:
            return [f"{label}: invalid exact decimal {value!r}"]
        if not isinstance(actual, Decimal) or actual != expected_decimal:
            return [f"{label}: expected decimal {value!r}, got {actual!r}"]
        return []
    if tag == "JString":
        if not isinstance(value, str) or not isinstance(actual, str):
            return [f"{label}: expected string {value!r}, got {actual!r}"]
        return _match_template(actual, value, bindings, root, label)
    if tag == "JSymbol":
        if not isinstance(value, str):
            return [f"{label}: JSymbol payload must be a string"]
        return _compare_symbol(actual, value, bindings, root, label)
    return [f"{label}: unknown JsonAtom constructor {tag!r}"]


def _match_template(actual: str, expected: str, bindings: dict[str, tuple[str, Any]],
                    root: Path, label: str) -> list[str]:
    return _match_text(actual, expected, bindings, root, label, regex_mode=False)


def _match_pattern(actual: str, expected: str, bindings: dict[str, tuple[str, Any]],
                   root: Path, label: str) -> list[str]:
    return _match_text(actual, expected, bindings, root, label, regex_mode=True)


def _match_text(actual: str, expected: str, bindings: dict[str, tuple[str, Any]],
                root: Path, label: str, regex_mode: bool) -> list[str]:
    matches = list(TOKEN_RE.finditer(expected))
    for left, right in zip(matches, matches[1:]):
        if left.end() == right.start() and left.group(1) and right.group(1) and left.group(1).startswith("capture:") and right.group(1).startswith("capture:"):
            return [f"{label}: adjacent variable-length captures are ambiguous"]
    pieces: list[str] = []
    groups: list[tuple[str, str, str]] = []
    cursor = 0
    for match in matches:
        literal = expected[cursor:match.start()]
        if regex_mode:
            pieces.append(literal)
        else:
            pieces.append(re.escape(literal))
        token = match.group(1)
        if token is None:
            pieces.append(re.escape("${"))
            cursor = match.end()
            continue
        capture = CAPTURE_RE.fullmatch(token)
        if capture:
            name, kind = capture.groups()
            if name in bindings:
                bound_kind, bound_value = bindings[name]
                if not _compatible_capture_kind(bound_kind, kind):
                    return [f"{label}: capture {name!r} type changed from {bound_kind} to {kind}"]
                pieces.append(re.escape(_render_bound(bound_value)))
            else:
                group = f"cap_{len(groups)}"
                pieces.append(f"(?P<{group}>{TYPE_PATTERNS[kind]})")
                groups.append((group, name, kind))
        else:
            reference = _parse_reference(token, bindings)
            if reference is None:
                return [f"{label}: unbound or malformed placeholder ${{{token}}}"]
            _kind, bound_value = reference
            pieces.append(re.escape(_render_bound(bound_value)))
        cursor = match.end()
    tail = expected[cursor:]
    pieces.append(tail if regex_mode else re.escape(tail))
    expression = "\\A(?:" + "".join(pieces) + ")\\Z"
    if regex_mode:
        unsupported = _portable_pattern_error(expected)
        if unsupported:
            return [f"{label}: unsupported portable pattern: {unsupported}"]
    try:
        compiled = re.compile(expression, 0 if regex_mode else re.DOTALL)
    except re.error as error:
        return [f"{label}: invalid pattern: {error}"]
    match = compiled.fullmatch(actual)
    if not match:
        return [f"{label}: expected {expected!r}, got {actual!r}"]
    candidate = dict(bindings)
    for group, name, kind in groups:
        value: str | int = match.group(group)
        if kind in ("pid", "ms"):
            value = int(value)
        error = _validate_capture_value(value, kind, root)
        if error:
            return [f"{label}: capture {name!r}: {error}"]
        previous = candidate.get(name)
        if previous is not None and (previous[0] != kind or previous[1] != value):
            return [f"{label}: capture {name!r} changed from {previous[1]!r} to {value!r}"]
        candidate[name] = (kind, value)
    bindings.clear()
    bindings.update(candidate)
    return []


def _portable_pattern_error(pattern: str) -> str | None:
    if "(?" in pattern:
        return "lookaround, named groups, and engine extensions are not allowed"
    if re.search(r"\\[1-9]", pattern):
        return "backreferences are not allowed"
    # Python's shorthand classes and flags vary from the portable regex set.
    pattern = pattern.replace(r"[\s\S]", "")
    if re.search(r"\\[AbBdDsSwWZ]", pattern):
        return "engine-specific shorthand escapes are not allowed"
    return None


def _portable_regex(pattern: str) -> re.Pattern[str]:
    error = _portable_pattern_error(pattern)
    if error:
        raise QuintInputError(f"unsupported portable pattern: {error}")
    try:
        return re.compile(pattern)
    except re.error as error:
        raise QuintInputError(f"invalid portable pattern: {error}") from error


def _parse_reference(token: str, bindings: dict[str, tuple[str, Any]]) -> tuple[str, Any] | None:
    prefix = re.fullmatch(r"prefix:([A-Za-z][A-Za-z0-9_.-]*):([1-9][0-9]*)", token)
    if prefix:
        name, count = prefix.groups()
        binding = bindings.get(name)
        if not binding:
            return None
        return "string", _render_bound(binding[1])[:int(count)]
    if NAME_RE.fullmatch(token):
        binding = bindings.get(token)
        if binding:
            if binding[0] in {"ms", "pid"}:
                return "int", binding[1]
            return "string", binding[1]
        return binding
    return None


def _compatible_capture_kind(old: str, new: str) -> bool:
    return old == new


def _validate_capture_value(value: str | int, kind: str, root: Path) -> str | None:
    if kind in ("pid", "ms"):
        if type(value) is not int or value < (1 if kind == "pid" else 0):
            return f"expected {'positive' if kind == 'pid' else 'nonnegative'} integer"
        return None
    if not isinstance(value, str) or not re.fullmatch(TYPE_PATTERNS[kind], value):
        return f"value {value!r} does not match {kind} capture type"
    if kind == "path":
        candidate = Path(value).resolve(strict=False)
        try:
            candidate.relative_to(root)
        except ValueError:
            return "absolute path is outside the trace directory"
    return None


def _compare_symbol(actual: Any, expected: str, bindings: dict[str, tuple[str, Any]],
                    root: Path, label: str) -> list[str]:
    token = expected[2:-1] if expected.startswith("${") and expected.endswith("}") else expected
    capture = CAPTURE_RE.fullmatch(token)
    if capture:
        name, kind = capture.groups()
        expected_type = int if kind in ("pid", "ms") else str
        if type(actual) is not expected_type:
            return [f"{label}: JSymbol {kind} requires {'integer' if expected_type is int else 'string'}, got {actual!r}"]
        error = _validate_capture_value(actual, kind, root)
        if error:
            return [f"{label}: {error}"]
        previous = bindings.get(name)
        if previous:
            if not _compatible_capture_kind(previous[0], kind) or previous[1] != actual:
                return [f"{label}: capture {name!r} expected {previous[1]!r}, got {actual!r}"]
        else:
            bindings[name] = (kind, actual)
        return []
    reference = _parse_reference(expected[2:-1], bindings) if expected.startswith("${") and expected.endswith("}") else None
    if not reference:
        return [f"{label}: JSymbol must contain exactly one bound or typed capture token"]
    bound_kind, bound_value = reference
    if type(actual) is not type(bound_value) or actual != bound_value:
        return [f"{label}: expected typed symbol {bound_value!r}, got {actual!r}"]
    return []


def _expected_key(value: str, bindings: dict[str, tuple[str, Any]]) -> str:
    output = []
    cursor = 0
    for match in TOKEN_RE.finditer(value):
        output.append(value[cursor:match.start()])
        token = match.group(1)
        if token is None:
            output.append("${")
        else:
            if token.startswith("capture:"):
                raise QuintInputError(f"map/path key may not introduce capture {token!r}")
            reference = _parse_reference(token, bindings)
            if not reference:
                raise QuintInputError(f"map/path key has unbound placeholder {token!r}")
            output.append(_render_bound(reference[1]))
        cursor = match.end()
    output.append(value[cursor:])
    return "".join(output)


def _compare_relation(value: Any, bindings: dict[str, tuple[str, Any]], label: str) -> list[str]:
    relation = _variant(value, {"Same", "Different", "IntRange", "IntDelta", "IntAtLeastDelta"}, label)
    data = _record(relation.value, label)
    if relation.tag in {"Same", "Different"}:
        left_kind, left = _relation_operand(data.get("left"), bindings, label + ".left")
        right_kind, right = _relation_operand(data.get("right"), bindings, label + ".right")
        equal = left_kind == right_kind and type(left) is type(right) and left == right
        expected_equal = relation.tag == "Same"
        return [] if equal == expected_equal else [f"{label}: expected {relation.tag.lower()} values, got {left!r} and {right!r}"]
    if relation.tag == "IntRange":
        number_kind, number = _relation_operand(data.get("value"), bindings, label + ".value")
        low, high = data.get("min"), data.get("max")
        if number_kind != "int" or type(number) is not int or type(low) is not int or type(high) is not int or low > high:
            return [f"{label}: IntRange requires integer value and ordered bounds"]
        return [] if low <= number <= high else [f"{label}: {number} is outside inclusive range [{low}, {high}]"]
    later_kind, later = _relation_operand(data.get("later"), bindings, label + ".later")
    earlier_kind, earlier = _relation_operand(data.get("earlier"), bindings, label + ".earlier")
    delta = data.get("delta")
    if later_kind != "int" or earlier_kind != "int" or type(later) is not int or \
            type(earlier) is not int or type(delta) is not int:
        return [f"{label}: {relation.tag} requires integer operands"]
    actual_delta = later - earlier
    if relation.tag == "IntDelta":
        return [] if actual_delta == delta else [f"{label}: expected delta {delta}, got {actual_delta}"]
    return [] if actual_delta >= delta else [f"{label}: expected delta at least {delta}, got {actual_delta}"]


def _relation_operand(value: Any, bindings: dict[str, tuple[str, Any]], label: str) -> tuple[str, Any]:
    if type(value) is int:
        return "int", value
    if not isinstance(value, str):
        raise QuintInputError(f"{label}: relation operand must be a string token or integer")
    if value.startswith("${") and value.endswith("}"):
        reference = _parse_reference(value[2:-1], bindings)
        if not reference:
            raise QuintInputError(f"{label}: unbound relation token {value!r}")
        return reference
    if INTEGER_RE.fullmatch(value):
        return "int", int(value)
    if TOKEN_RE.search(value):
        raise QuintInputError(f"{label}: relation operands do not allow embedded tokens")
    return "string", value


def _validate_status_rows(rows: list[dict[str, Any]]) -> list[str]:
    failures = []
    if not rows:
        return ["at least one queue row is required"]
    if not isinstance(rows[0], dict):
        return ["status row 0 is not an object"]
    if rows[0].get("type") == "intent_detail":
        if len(rows) != 1:
            failures.append(f"intent detail must contain exactly one row, got {len(rows)}")
        if type(rows[0].get("schema")) is not int or rows[0].get("schema") != 1:
            failures.append("intent detail schema must be integer 1")
        return failures
    if type(rows[0].get("schema")) is not int or rows[0].get("schema") != 1 or rows[0].get("type") != "queue":
        failures.append("overview must begin with exactly one schema 1 queue row")
        return failures
    queue_count = sum(1 for row in rows if isinstance(row, dict) and row.get("type") == "queue")
    if queue_count != 1:
        failures.append(f"overview has {queue_count} queue rows, expected exactly one")
    rank = {"queue": 0, "intent": 1, "agent": 2}
    ranks = []
    positions = []
    queued_count = rows[0].get("queued")
    if type(queued_count) is not int or queued_count < 0:
        failures.append("queue.queued must be a nonnegative integer")
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            failures.append(f"row {index} is not an object")
            continue
        row_type = row.get("type")
        if row_type not in rank:
            failures.append(f"row {index} has unknown overview type {row_type!r}")
        else:
            ranks.append(rank[row_type])
        if type(row.get("schema")) is not int or row.get("schema") != 1:
            failures.append(f"row {index} schema is not integer 1")
        if row_type == "intent":
            position = row.get("queue_position")
            if position is not None:
                if type(position) is not int or position < 1:
                    failures.append(f"intent row {index} queue_position must be null or a positive 1-based integer")
                else:
                    positions.append(position)
    if ranks != sorted(ranks):
        failures.append("overview rows are not ordered queue, intent, then agents")
    if type(queued_count) is int and queued_count >= 0 and positions != list(range(1, queued_count + 1)):
        failures.append(f"intent queue positions must be 1..{queued_count} in order, got {positions!r}")
    return failures


def _git_snapshot(world: TraceWorld, cwd: str) -> dict[str, Any]:
    env = world._base_env()
    env["GIT_OPTIONAL_LOCKS"] = "0"

    def git(args: list[str], *, input_bytes: bytes | None = None, env_override: dict[str, str] | None = None) -> bytes:
        command_env = dict(env)
        if env_override:
            command_env.update(env_override)
        result = subprocess.run(["git", *args], cwd=cwd, env=command_env, input=input_bytes,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
        if result.returncode:
            raise QuintInputError(f"git {' '.join(args)} exited {result.returncode}: {result.stderr.decode('utf-8', 'replace').strip()}")
        return result.stdout

    top_raw = git(["rev-parse", "--show-toplevel"])
    repo = Path(top_raw.decode("utf-8", "strict").strip()).resolve()
    refs_raw = git(["for-each-ref", "--format=%(refname)%00%(objectname)"])
    refs: dict[str, str] = {}
    branches: dict[str, str] = {}
    kogen_refs: dict[str, str] = {}
    for line in refs_raw.decode("utf-8", "strict").splitlines():
        if not line:
            continue
        name, _, object_id = line.partition("\0")
        if not name or not object_id:
            raise QuintInputError("malformed git for-each-ref output")
        refs[name] = object_id
        if name.startswith("refs/heads/"):
            branches[name] = object_id
        if name.startswith("refs/kogen/"):
            kogen_refs[name] = object_id
    head_result = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=cwd, env=env,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
    if head_result.returncode == 0:
        head_id = head_result.stdout.decode("ascii", "strict").strip()
        head_info = git(["show", "-s", "--format=%T%x00%P%x00%an%x00%ae%x00%cn%x00%ce", "HEAD"])
        parts = head_info.decode("utf-8", "strict").rstrip("\n").split("\0")
        if len(parts) < 6:
            raise QuintInputError("malformed git show identity output")
        head_tree, parent_text, author_name, author_email, committer_name, committer_email = parts[:6]
        subject = git(["show", "-s", "--format=%s", "HEAD"]).decode("utf-8", "strict").rstrip("\n")
        message = git(["show", "-s", "--format=%B", "HEAD"])
        trailers_raw = subprocess.run(["git", "interpret-trailers", "--parse"], cwd=cwd, env=env,
                                      input=message, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
        if trailers_raw.returncode:
            raise QuintInputError(f"git interpret-trailers failed: {trailers_raw.stderr.decode('utf-8', 'replace')}")
        trailers = []
        for line in trailers_raw.stdout.decode("utf-8", "strict").splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                trailers.append({"key": key.strip(), "value": value.strip()})
        parent_ids = parent_text.split() if parent_text else []
        diff_args = ["diff-tree", "--no-commit-id", "--name-status", "-r", "-M", "-z"]
        if parent_ids:
            diff_args.extend([parent_ids[0], head_id])
        else:
            diff_args.extend(["--root", head_id])
        diff_tokens = git(diff_args).decode("utf-8", "strict").split("\0")
        if diff_tokens and diff_tokens[-1] == "":
            diff_tokens.pop()
        changed = set()
        cursor = 0
        while cursor < len(diff_tokens):
            status = diff_tokens[cursor]
            cursor += 1
            path_count = 2 if status.startswith(("R", "C")) else 1
            if cursor + path_count > len(diff_tokens):
                raise QuintInputError("malformed NUL-delimited git diff-tree output")
            changed.update(diff_tokens[cursor:cursor + path_count])
            cursor += path_count
        head = head_id
        author = {"name": author_name, "email": author_email}
        committer = {"name": committer_name, "email": committer_email}
    else:
        head_id = None
        head_tree = None
        subject = None
        trailers = []
        changed = set()
        parent_ids = []
        head = None
        author = None
        committer = None
    symbolic_result = subprocess.run(["git", "symbolic-ref", "-q", "HEAD"], cwd=cwd, env=env,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
    symbolic_head = symbolic_result.stdout.decode("utf-8", "strict").strip() if symbolic_result.returncode == 0 else None
    index_path_raw = git(["rev-parse", "--git-path", "index"]).decode("utf-8", "strict").strip()
    index_path = Path(index_path_raw)
    if not index_path.is_absolute():
        index_path = Path(cwd) / index_path
    isolated_index = world.tmp / f"index-observe-{threading.get_ident()}-{time.monotonic_ns()}"
    if index_path.exists():
        shutil.copyfile(index_path, isolated_index)
    isolated_env = {"GIT_INDEX_FILE": str(isolated_index)}
    if not index_path.exists():
        git(["read-tree", "--empty"], env_override=isolated_env)
    index_tree = git(["write-tree"], env_override=isolated_env).decode("ascii", "strict").strip()
    isolated_index.unlink(missing_ok=True)
    return {"branches": branches, "kogenRefs": kogen_refs, "refs": refs, "head": head,
            "symbolicHead": symbolic_head, "headTree": head_tree, "indexTree": index_tree,
            "subject": subject, "trailers": trailers, "changedPaths": changed,
            "parents": parent_ids, "author": author, "committer": committer, "repo": str(repo)}


def _compare_git(expected: Any, actual: dict[str, Any], bindings: dict[str, tuple[str, Any]],
                 root: Path, label: str) -> list[str]:
    try:
        record = _record(expected, label, ("branches", "kogenRefs", "head", "symbolicHead", "headTree", "indexTree",
                                          "subject", "trailers", "changedPaths", "parents", "author", "committer"))
    except QuintInputError as error:
        return [str(error)]
    failures: list[str] = []
    failures.extend(_compare_named(record["branches"], actual["branches"], bindings, root, label + ".branches"))
    failures.extend(_compare_named(record["kogenRefs"], actual["kogenRefs"], bindings, root, label + ".kogenRefs"))
    for field in ("head", "symbolicHead"):
        observed, wanted = _observation(record[field], label + "." + field)
        if observed:
            present, expected_value = _optional(wanted, label + "." + field)
            got = actual[field]
            if present != (got is not None):
                failures.append(f"{label}.{field}: expected {'present' if present else 'missing'}, got {got!r}")
            elif present:
                failures.extend(_match_template(str(got), str(expected_value), bindings, root, label + "." + field))
    string_fields = ("headTree", "indexTree", "subject")
    for field in string_fields:
        observed, wanted = _observation(record[field], label + "." + field)
        if observed:
            got = actual[field]
            if got is None:
                failures.append(f"{label}.{field}: expectation is invalid for an unborn HEAD")
            elif not isinstance(wanted, str):
                failures.append(f"{label}.{field}: expected a string")
            else:
                failures.extend(_match_template(got, wanted, bindings, root, label + "." + field))
    observed, wanted = _observation(record["trailers"], label + ".trailers")
    if observed:
        if actual["head"] is None:
            failures.append(f"{label}.trailers: expectation is invalid for an unborn HEAD")
        elif not isinstance(wanted, list) or len(wanted) != len(actual["trailers"]):
            failures.append(f"{label}.trailers: expected {len(wanted) if isinstance(wanted, list) else 'a list'}, got {len(actual['trailers'])}")
        else:
            for index, (want, got) in enumerate(zip(wanted, actual["trailers"])):
                item = _record(want, f"{label}.trailers[{index}]", ("key", "value"))
                for key in ("key", "value"):
                    failures.extend(_match_template(got[key], item[key], bindings, root,
                                                    f"{label}.trailers[{index}].{key}"))
    observed, wanted = _observation(record["changedPaths"], label + ".changedPaths")
    if observed:
        if actual["head"] is None:
            failures.append(f"{label}.changedPaths: expectation is invalid for an unborn HEAD")
        elif not isinstance(wanted, ITFSet):
            failures.append(f"{label}.changedPaths must be a Quint Set")
        else:
            expected_paths = {_expected_key(str(path), bindings) for path in wanted.values}
            if expected_paths != actual["changedPaths"]:
                failures.append(f"{label}.changedPaths: expected {sorted(expected_paths)!r}, got {sorted(actual['changedPaths'])!r}")
    observed, wanted = _observation(record["parents"], label + ".parents")
    if observed:
        if actual["head"] is None:
            failures.append(f"{label}.parents: expectation is invalid for an unborn HEAD")
        elif not isinstance(wanted, list) or len(wanted) != len(actual["parents"]):
            failures.append(f"{label}.parents: expected {len(wanted) if isinstance(wanted, list) else 'a list'}, got {len(actual['parents'])}")
        else:
            for index, (want, got) in enumerate(zip(wanted, actual["parents"])):
                failures.extend(_match_template(got, str(want), bindings, root, f"{label}.parents[{index}]"))
    for field in ("author", "committer"):
        observed, wanted = _observation(record[field], label + "." + field)
        if observed:
            if actual["head"] is None:
                failures.append(f"{label}.{field}: expectation is invalid for an unborn HEAD")
            elif not isinstance(wanted, dict):
                failures.append(f"{label}.{field}: expected Identity record")
            else:
                for key in ("name", "email"):
                    failures.extend(_match_template(actual[field][key], wanted[key], bindings, root,
                                                    f"{label}.{field}.{key}"))
    return failures


def _compare_named(expected: Any, actual: dict[str, str], bindings: dict[str, tuple[str, Any]],
                   root: Path, label: str) -> list[str]:
    try:
        record = _record(expected, label, ("complete", "entries"))
        if type(record["complete"]) is not bool:
            return [f"{label}.complete must be boolean"]
        entries = _validate_named_map(record["entries"], label + ".entries")
    except QuintInputError as error:
        return [str(error)]
    failures: list[str] = []
    expected_present: set[str] = set()
    for key, optional in sorted(entries.items(), key=lambda item: str(item[0])):
        name = _expected_key(str(key), bindings)
        present, value = _optional(optional, f"{label}.entries[{name!r}]")
        if present:
            expected_present.add(name)
            if name not in actual:
                failures.append(f"{label}[{name!r}] is missing")
            else:
                failures.extend(_match_template(actual[name], str(value), bindings, root, f"{label}[{name!r}]"))
        elif name in actual:
            failures.append(f"{label}[{name!r}] expected Missing, got {actual[name]!r}")
    if record["complete"] and set(actual) != expected_present:
        failures.append(f"{label} complete namespace: expected {sorted(expected_present)!r}, got {sorted(actual)!r}")
    return failures


def _compare_file(path: Path, expected: Any, bindings: dict[str, tuple[str, Any]], root: Path,
                  label: str) -> tuple[list[str], Any]:
    variant = _variant(expected, {"AbsentFile", "FileBytes", "FileSha256", "Symlink"}, label)
    try:
        info = path.lstat()
    except FileNotFoundError:
        if variant.tag == "AbsentFile":
            return [], {"kind": "absent"}
        return [f"{label}: file is absent"], {"kind": "absent"}
    if variant.tag == "AbsentFile":
        return [f"{label}: expected absence, file exists"], {"mode": stat.S_IMODE(info.st_mode)}
    if variant.tag == "Symlink":
        if not stat.S_ISLNK(info.st_mode):
            return [f"{label}: expected symlink, got {stat.S_IFMT(info.st_mode)}"], {"kind": "non-symlink"}
        target = os.readlink(path)
        if not isinstance(variant.value, str):
            return [f"{label}: Symlink target must be string"], {"target": target}
        return _match_template(target, variant.value, bindings, root, label), {"kind": "symlink", "target": target}
    if stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        return [f"{label}: expected regular file, got directory/symlink/special file"], {"kind": "non-regular"}
    data = path.read_bytes()
    snapshot = {"kind": "file", "sha256": hashlib.sha256(data).hexdigest(),
                "bytes_base64": base64.b64encode(data).decode("ascii"), "mode": stat.S_IMODE(info.st_mode)}
    if variant.tag == "FileSha256":
        if not isinstance(variant.value, str):
            return [f"{label}: FileSha256 needs string"], snapshot
        return _match_template(snapshot["sha256"], variant.value, bindings, root, label), snapshot
    expected_bytes = _bytes(variant.value, label + ".bytes")
    byte_variant = _variant(variant.value, {"Utf8", "Octets"}, label + ".bytes")
    if byte_variant.tag == "Utf8":
        try:
            actual_text = data.decode("utf-8", "strict")
        except UnicodeDecodeError as error:
            return [f"{label}: file bytes are not UTF-8: {error}"], snapshot
        return _match_template(actual_text, byte_variant.value, bindings, root, label), snapshot
    return ([] if data == expected_bytes else [f"{label}: exact octets differ (sha256 {snapshot['sha256']})"]), snapshot


def _loopback_or_invalid(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme and not parsed.netloc:
        return True
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    return parsed.hostname in {"127.0.0.1", "localhost", "::1"}


def _reject_network_git(argv: list[str]) -> None:
    consuming_options = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
    index = 0
    while index < len(argv):
        token = argv[index]
        if token in consuming_options:
            index += 2
            continue
        if token.startswith("-"):
            index += 1
            continue
        break
    if index >= len(argv):
        return
    command = argv[index]
    network = {"clone", "fetch", "pull", "push", "ls-remote", "send-pack", "receive-pack", "upload-pack",
               "http-backend", "daemon", "serve", "submodule"}
    if command in network:
        raise QuintInputError(f"GitCommand {command!r} may access the network; only local Git setup is allowed")
    if command == "remote" and any(word in {"update", "prune", "get-url"} for word in argv[index + 1:]):
        if "update" in argv[index + 1:] or "prune" in argv[index + 1:]:
            raise QuintInputError("GitCommand remote update/prune may access the network")
    local_commands = {
        "add", "am", "apply", "archive", "bisect", "blame", "branch", "cat-file", "checkout", "cherry-pick",
        "clean", "commit", "config", "describe", "diff", "diff-tree", "for-each-ref", "hash-object", "init",
        "interpret-trailers", "log", "ls-files", "merge", "merge-base", "mv", "read-tree", "rebase", "reflog",
        "remote", "replace", "reset", "rev-parse", "revert", "rm", "show", "show-ref", "status", "switch",
        "symbolic-ref", "tag", "update-index", "update-ref", "verify-tag", "worktree", "write-tree",
    }
    if command not in local_commands:
        raise QuintInputError(f"GitCommand {command!r} is not in the local-only Git command set")


def _missing_capabilities(requirements: dict[str, Any], world: TraceWorld | None = None) -> list[str]:
    missing = []
    platforms = requirements.get("platform", [])
    if isinstance(platforms, list) and platforms and sys.platform not in platforms:
        missing.append(f"platform {platforms!r} (host {sys.platform})")
    tools = requirements.get("tools", [])
    if not isinstance(tools, list):
        missing.append("malformed tool requirements")
    else:
        for tool in tools:
            if not isinstance(tool, str) or shutil.which(tool, path="/usr/bin:/bin") is None:
                missing.append(f"tool {tool!r}")
    seams = requirements.get("seams", [])
    if not isinstance(seams, list):
        missing.append("malformed seam requirements")
    else:
        available = {"scripted_provider", "clock", "barriers", "process", "git", "write_file", "openid"}
        for seam in seams:
            if seam not in available:
                missing.append(f"unimplemented seam {seam!r}")
            elif world is not None:
                if seam == "clock" and world.clock_path is None:
                    missing.append("clock (ioSeam.wallClockMs is Missing)")
                if seam == "barriers" and world.barrier_dir is None:
                    missing.append("barriers (ioSeam.barriers is false)")
                if seam == "scripted_provider" and (world.provider is None or not world.manifest["scripts"]):
                    missing.append("scripted_provider (manifest has no scripts)")
                if seam == "openid" and not world._cli_fixture("server.py").is_file():
                    missing.append("openid (manifest lacks the CLI OpenID fixture server)")
                if seam == "process" and os.name != "posix":
                    missing.append("process signals/background groups require POSIX")
    unknown = set(requirements) - {"platform", "tools", "seams"}
    if unknown:
        missing.extend(f"unknown capability group {key!r}" for key in sorted(unknown))
    return missing


def _strict_text(data: bytes, stream: str) -> str:
    try:
        return data.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise QuintInputError(f"{stream} is not valid UTF-8: {error}") from error


def _normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n")


def _normalized_lines(text: str) -> list[str]:
    normalized = _normalize_text(text)
    if normalized == "":
        return []
    if normalized.endswith("\n"):
        normalized = normalized[:-1]
    return normalized.split("\n")


def _permille(value: int) -> str:
    whole, remainder = divmod(value, 1000)
    if remainder == 0:
        return str(whole)
    return f"{whole}.{remainder:03d}".rstrip("0")


def _atomic_write(path: Path, data: bytes, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".tmp-{os.getpid()}-{threading.get_ident()}")
    with open(temporary, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(temporary, mode)
    os.replace(temporary, path)


def _signal_number(name: str) -> int:
    normalized = name.upper()
    signal_name = normalized.removeprefix("SIG")
    if signal_name not in {"TERM", "KILL", "INT"}:
        raise QuintInputError(f"unsupported conformance signal {name!r}; use TERM, KILL, or INT")
    normalized = "SIG" + signal_name
    value = getattr(signal, normalized, None)
    if not isinstance(value, int):
        raise QuintInputError(f"unknown signal name {name!r}")
    return value


def _render_bound(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _plain(value: Any) -> Any:
    if isinstance(value, Variant):
        return {"tag": value.tag, "value": _plain(value.value)}
    if isinstance(value, ITFMap):
        return {str(_plain(key)): _plain(item) for key, item in value.pairs}
    if isinstance(value, ITFSet):
        return [_plain(item) for item in value.values]
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, bytes):
        return {"base64": base64.b64encode(value).decode("ascii")}
    if isinstance(value, set):
        return sorted(_plain(item) for item in value)
    return value


def _result_record(result: dict[str, Any]) -> dict[str, Any]:
    return _plain(result)


def _sha_file(path: str) -> str:
    try:
        with open(path, "rb") as stream:
            return hashlib.sha256(stream.read()).hexdigest()
    except OSError:
        return ""


def _reproduce_command(case: dict[str, Any], kogen: str) -> str:
    manifest = case.get("_manifest", {})
    seed = manifest.get("seed", "unknown")
    return (f"kogen-conformance run --kogen {shlex.quote(kogen)} --case {shlex.quote(case['id'])} -v "
            f"# seed {seed}; ITF: {shlex.quote(case.get('_file', 'unknown'))}")


def run_quint_case(case: dict[str, Any], kogen: str, time_scale: float = 1.0,
                   keep: bool = False, timeout_s: float = 60.0,
                   workdir: str | Path = "/tmp") -> dict[str, Any]:
    try:
        binary = Path(kogen).resolve(strict=True)
        if not os.access(binary, os.X_OK):
            raise QuintInputError(f"Kogen binary is not executable: {binary}")
        world = TraceWorld(case, str(binary), time_scale, keep, timeout_s=timeout_s, workdir=workdir)
    except Exception as error:
        return {"kind": "case", "id": case.get("id", "<invalid>"), "title": case.get("title", ""),
                "file": case.get("_file"), "status": "error",
                "failures": [f"harness error: {type(error).__name__}: {error}"], "steps": [],
                "seed": case.get("_manifest", {}).get("seed"), "reproduce": _reproduce_command(case, kogen)}
    try:
        result = world.run()
    except Exception as error:
        result = {"kind": "case", "id": case["id"], "title": case.get("title", ""),
                  "file": case.get("_file"), "status": "error",
                  "failures": [f"harness error: {type(error).__name__}: {error}"], "steps": [],
                  "seed": world.manifest["seed"], "first_failure": None,
                  "reproduce": _reproduce_command(case, str(binary))}
    teardown_errors = world.close()
    if teardown_errors:
        result.setdefault("teardown_notes", []).extend(teardown_errors)
        result["sandbox"] = str(world.root) if keep else None
    elif keep:
        result["sandbox"] = str(world.root)
    else:
        result["sandbox"] = None
    return result








