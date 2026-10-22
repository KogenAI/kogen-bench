"""Load and validate `experiment.json` (format in lanes/FORMATS.md)."""

import math
import os
import re
import sys

from . import common

PHASES = ("shape", "build", "e2e")
INTENT_FORMS = ("gherkin", "gherkin-lean", "gherkin-quint", "prose")
_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_SHA = re.compile(r"^[0-9a-f]{40}$")
_ROLE = re.compile(r"^[a-z][a-z0-9_-]*$")
_MODEL = re.compile(r"^[^\s/]+/\S+ \S+$")  # "provider/model effort"


class ExperimentError(ValueError):
    """The message names the offending field."""


def _fail(field, why):
    raise ExperimentError(f"{field}: {why}")


def _kind(value, types, field, what):
    if isinstance(value, bool) or not isinstance(value, types):
        _fail(field, f"must be {what}")
    return value


def _name(value, field):
    if not isinstance(value, str) or not _NAME.match(value):
        _fail(field, "must be a short name of letters, digits, '.', '_' or '-'")
    return value


def _lane(lane, i):
    f = f"lanes[{i}]"
    _kind(lane, dict, f, "an object")
    _name(lane.get("name"), f + ".name")
    if not isinstance(lane.get("sha"), str) or not _SHA.match(lane["sha"]):
        _fail(f + ".sha", "must be 40 lowercase hex characters")
    if "patch" not in lane:
        _fail(f + ".patch", "is required (null or a relative path)")
    patch = lane["patch"]
    if patch is not None:
        if not isinstance(patch, str) or not patch:
            _fail(f + ".patch", "must be null or a path string")
        if os.path.isabs(patch) or ".." in patch.replace("\\", "/").split("/"):
            _fail(f + ".patch", "must be relative to the experiment file, without '..'")
    settings = _kind(lane.get("settings"), dict, f + ".settings", "an object")
    models = settings.get("models", {})
    _kind(models, dict, f + ".settings.models", "an object of role: 'provider/model effort'")
    for role, spec in models.items():
        if not _ROLE.match(role):
            _fail(f + f".settings.models.{role}", "role must be lowercase letters, digits, '_' or '-'")
        if not isinstance(spec, str) or not _MODEL.match(spec):
            _fail(f + f".settings.models.{role}", "must look like 'provider/model effort'")


def validate(exp):
    """Return `exp` if valid, else raise ExperimentError."""
    _kind(exp, dict, "experiment", "an object")
    _name(exp.get("id"), "id")
    if exp.get("phase") not in PHASES:
        _fail("phase", "must be one of " + ", ".join(PHASES))
    if exp["phase"] == "build" and exp.get("intent_form") not in INTENT_FORMS:
        _fail("intent_form", "is required for phase build: one of " + ", ".join(INTENT_FORMS))
    if exp["phase"] != "build" and exp.get("intent_form") not in (None, *INTENT_FORMS):
        _fail("intent_form", "must be one of " + ", ".join(INTENT_FORMS))
    kogen = _kind(exp.get("kogen"), dict, "kogen", "an object")
    if not isinstance(kogen.get("repo"), str) or not kogen["repo"]:
        _fail("kogen.repo", "must be a non-empty URL or path")
    lanes = _kind(exp.get("lanes"), list, "lanes", "a non-empty list")
    if not lanes:
        _fail("lanes", "must be a non-empty list")
    for i, lane in enumerate(lanes):
        _lane(lane, i)
    names = [lane["name"] for lane in lanes]
    if len(set(names)) != len(names):
        _fail("lanes", "names must be unique")
    tasks = _kind(exp.get("tasks"), list, "tasks", "a non-empty list of task ids")
    if not tasks:
        _fail("tasks", "must be a non-empty list of task ids")
    for i, t in enumerate(tasks):
        _name(t, f"tasks[{i}]")
    if len(set(tasks)) != len(tasks):
        _fail("tasks", "ids must be unique")
    if _kind(exp.get("reps"), int, "reps", "an integer") < 1:
        _fail("reps", "must be at least 1")
    deadline = _kind(exp.get("deadline_s"), (int, float), "deadline_s", "a number")
    if not math.isfinite(deadline) or deadline <= 0:
        _fail("deadline_s", "must be a finite positive number")
    hosts = _kind(exp.get("hosts"), list, "hosts", "a list of host names")
    for i, h in enumerate(hosts):
        _name(h, f"hosts[{i}]")
    rule = _kind(exp.get("decision_rule"), dict, "decision_rule", "an object")
    if not isinstance(rule.get("kind"), str) or not rule["kind"]:
        _fail("decision_rule.kind", "must be a non-empty string")
    return exp


def load(path):
    """Read and validate an experiment file; ExperimentError on any problem."""
    try:
        exp = common.read_json(path)
    except OSError as e:
        raise ExperimentError(f"{path}: {e.strerror or e}") from None
    except ValueError as e:
        raise ExperimentError(f"{path}: not valid JSON ({e})") from None
    return validate(exp)


def load_or_exit(path):
    """For entry points: print the error to stderr and exit 2 when invalid."""
    try:
        return load(path)
    except ExperimentError as e:
        print(f"experiment error: {e}", file=sys.stderr)
        raise SystemExit(2)


def patch_path(experiment_path, lane):
    """Absolute path of a lane's patch, or None."""
    if lane["patch"] is None:
        return None
    return os.path.join(os.path.dirname(os.path.abspath(experiment_path)), lane["patch"])
