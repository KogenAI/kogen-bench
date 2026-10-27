"""Load and validate `experiment.json` (format in lanes/FORMATS.md)."""

import math
import os
import re
import sys

from . import common

PHASES = ("shape", "build", "e2e", "probe")
INTENT_FORMS = ("gherkin", "gherkin-lean", "gherkin-quint", "prose")
_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_SHA = re.compile(r"^[0-9a-f]{40}$")
_ROLE = re.compile(r"^[a-z][a-z0-9_-]*$")
_MISSING = object()
_MODEL = re.compile(r"^[^\s/]+/\S+ \S+$")  # "provider/model effort"


CHATGPT = "chatgpt"  # the provider of a lane that names none (or `openai/`, `chatgpt/`): `cost_cap_usd` covers it


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


def _probe_lane(lane, f):
    """A probe lane runs a command on corpus items; a Kogen sha, patch and settings are optional (FORMATS, Probe)."""
    probe = _kind(lane.get("probe"), dict, f + ".probe", "an object with a command (a list of strings) and args")
    cmd = _kind(probe.get("command"), list, f + ".probe.command", "a non-empty list of strings")
    if not cmd or not all(isinstance(a, str) and a for a in cmd):
        _fail(f + ".probe.command", "must be a non-empty list of non-empty strings")
    _kind(probe.get("args", {}), dict, f + ".probe.args", "an object")
    if set(probe) - {"command", "args"}:
        _fail(f + ".probe", "has only command and args")
    if "dry_run_ok" in lane and not isinstance(lane["dry_run_ok"], bool):
        _fail(f + ".dry_run_ok", "must be true or false")
    if lane.get("patch") is not None:
        _fail(f + ".patch", "a probe lane has no patch")
    lane["patch"] = None
    lane.setdefault("settings", {})


def _lane(lane, i, probe=False):
    f = f"lanes[{i}]"
    _kind(lane, dict, f, "an object")
    _name(lane.get("name"), f + ".name")
    if probe:
        _probe_lane(lane, f)
    if "sha" in lane or not probe:
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


CLAUDE_CODE = "claude-code"


def lane_providers(lane):
    """The providers a lane's `settings.models` name, `openai` and `chatgpt` as one; ChatGPT when it names none."""
    names = {spec.split("/", 1)[0] for spec in lane["settings"].get("models", {}).values()}
    return {CHATGPT if n in ("openai", CHATGPT) else n for n in names} or {CHATGPT}


def lane_provider(lane):
    """The provider a lane's spend counts against: its one non-ChatGPT provider, else ChatGPT. A lane that pairs the
    claude-code executor with one priced provider (CC build, API review) counts its dollars against the priced one."""
    other = lane_providers(lane) - {CHATGPT}
    priced = other - {CLAUDE_CODE}
    return next(iter(priced or other)) if other else CHATGPT


def cap_providers(lane):
    """Every provider whose caps a new cell of the lane must pass: its non-ChatGPT providers, else ChatGPT."""
    return (lane_providers(lane) - {CHATGPT}) or {CHATGPT}


def _provider_caps(exp):
    caps = _kind(exp.get("provider_caps", {}), dict, "provider_caps",
                 'an object like {"opencode-go": {"cells": 8}}')
    for name, cap in caps.items():
        f = f"provider_caps.{name}"
        _name(name, "provider_caps key")
        if name == CHATGPT:
            _fail(f, "ChatGPT is capped by cost_cap_usd")
        _kind(cap, dict, f, 'an object with "cells" and/or "usd"')
        if not cap or set(cap) - {"cells", "usd"}:
            _fail(f, 'must have "cells" and/or "usd", and nothing else')
        if "cells" in cap and (isinstance(cap["cells"], bool) or not isinstance(cap["cells"], int) or cap["cells"] < 1):
            _fail(f + ".cells", "must be an integer of at least 1")
        if "usd" in cap:
            usd = _kind(cap["usd"], (int, float), f + ".usd", "a number of USD")
            if not math.isfinite(usd) or usd <= 0:
                _fail(f + ".usd", "must be a finite positive number")


def validate(exp):
    """Return `exp` if valid, else raise ExperimentError."""
    _kind(exp, dict, "experiment", "an object")
    _name(exp.get("id"), "id")
    if exp.get("phase") not in PHASES:
        _fail("phase", "must be one of " + ", ".join(PHASES))
    if exp["phase"] == "probe":
        return _validate_probe(exp)
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
    if "cost_cap_usd" in exp:  # required only to run cells (costguard.caps)
        cap = _kind(exp["cost_cap_usd"], (int, float), "cost_cap_usd", "a number of USD")
        if not math.isfinite(cap) or cap <= 0:
            _fail("cost_cap_usd", "must be a finite positive number")
    _provider_caps(exp)
    hosts = _kind(exp.get("hosts"), list, "hosts", "a list of host names")
    for i, h in enumerate(hosts):
        _name(h, f"hosts[{i}]")
    rule = _kind(exp.get("decision_rule"), dict, "decision_rule", "an object")
    if not isinstance(rule.get("kind"), str) or not rule["kind"]:
        _fail("decision_rule.kind", "must be a non-empty string")
    if exp.get("kind") not in (None, "climb"):
        _fail("kind", "must be absent or 'climb'")
    if exp.get("kind") == "climb":
        _climb(exp)
    elif rule["kind"] == "keep_revert":
        _fail("decision_rule.kind", "keep_revert needs a climb experiment (kind: climb)")
    return exp


PROBE_RULES = ("descriptive", "task_sign", "keep_revert")
GRADERS = ("set_recall_precision_at_budget", "exact_match", "command")


def _validate_probe(exp):
    """A probe experiment: a corpus folder instead of tasks, lanes with a probe command, a grader."""
    _kind(exp.get("corpus"), str, "corpus", "a path to a corpus folder, relative to the experiment")
    if not exp["corpus"]:
        _fail("corpus", "must be a non-empty path")
    lanes = _kind(exp.get("lanes"), list, "lanes", "a non-empty list")
    if not lanes:
        _fail("lanes", "must be a non-empty list")
    for i, lane in enumerate(lanes):
        _lane(lane, i, probe=True)
    names = [lane["name"] for lane in lanes]
    if len(set(names)) != len(names):
        _fail("lanes", "names must be unique")
    for key in ("tasks", "intent_form"):
        if key in exp:
            _fail(key, "a probe experiment has no tasks or Intent form (its items come from the corpus)")
    if "kogen" in exp:
        _kind(exp["kogen"], dict, "kogen", "an object")
    if "items" in exp:
        items = _kind(exp["items"], list, "items", "a non-empty list of item ids")
        if not items:
            _fail("items", "must be a non-empty list of item ids")
        for i, t in enumerate(items):
            _name(t, f"items[{i}]")
        if len(set(items)) != len(items):
            _fail("items", "ids must be unique")
    if _kind(exp.get("reps"), int, "reps", "an integer") < 1:
        _fail("reps", "must be at least 1")
    deadline = _kind(exp.get("deadline_s"), (int, float), "deadline_s", "a number")
    if not math.isfinite(deadline) or deadline <= 0:
        _fail("deadline_s", "must be a finite positive number")
    if "cost_cap_usd" in exp:
        cap = _kind(exp["cost_cap_usd"], (int, float), "cost_cap_usd", "a number of USD")
        if not math.isfinite(cap) or cap <= 0:
            _fail("cost_cap_usd", "must be a finite positive number")
    _provider_caps(exp)
    exp.setdefault("hosts", [])
    for i, h in enumerate(_kind(exp["hosts"], list, "hosts", "a list of host names")):
        _name(h, f"hosts[{i}]")
    grader = _kind(exp.get("grader"), dict, "grader", "an object with a kind")
    if grader.get("kind") not in GRADERS:
        _fail("grader.kind", "must be one of " + ", ".join(GRADERS))
    if grader["kind"] == "command":
        cmd = grader.get("command")
        if not isinstance(cmd, list) or not cmd or not all(isinstance(a, str) and a for a in cmd):
            _fail("grader.command", "must be a non-empty list of non-empty strings")
    for key in ("sets", "keys"):
        if key in grader and (not isinstance(grader[key], list) or not all(isinstance(a, str) for a in grader[key])):
            _fail(f"grader.{key}", "must be a list of names")
    if exp.get("kind") is not None:
        _fail("kind", "a probe experiment has none (use decision_rule keep_revert with a split)")
    split = exp.get("split")
    if split is not None:
        _kind(split, dict, "split", "an object with train and test lists of item ids")
        for part in ("train", "test"):
            ids = _kind(split.get(part), list, f"split.{part}", "a non-empty list of item ids")
            if not ids:
                _fail(f"split.{part}", "must be a non-empty list of item ids")
            for i, t in enumerate(ids):
                _name(t, f"split.{part}[{i}]")
            if len(set(ids)) != len(ids):
                _fail(f"split.{part}", "ids must be unique")
        if set(split["train"]) & set(split["test"]):
            _fail("split", "train and test must be disjoint")
        if "items" in exp and set(split["train"]) | set(split["test"]) != set(exp["items"]):
            _fail("split", "train and test together must be exactly the experiment's items")
    _probe_rule(exp, names)
    return exp


def _probe_rule(exp, names):
    rule = _kind(exp.get("decision_rule"), dict, "decision_rule", "an object")
    kind = rule.get("kind")
    if kind not in PROBE_RULES:
        _fail("decision_rule.kind", "a probe experiment uses one of " + ", ".join(PROBE_RULES))
    if kind == "descriptive":
        return
    for key in ("baseline", "candidate"):
        if rule.get(key) not in names:
            _fail(f"decision_rule.{key}", "must name a lane of the experiment")
    if rule["baseline"] == rule["candidate"]:
        _fail("decision_rule", "baseline and candidate must be two lanes")
    if not isinstance(rule.get("metric"), str) or not rule["metric"]:
        _fail("decision_rule.metric", "must name a metric (for example touched_files.file.recall)")
    if rule.get("better", "higher") not in ("higher", "lower"):
        _fail("decision_rule.better", "must be higher or lower")
    for key in ("min_gain", "min_effect"):
        if key in rule and (isinstance(rule[key], bool) or not isinstance(rule[key], (int, float))
                            or not math.isfinite(rule[key]) or rule[key] < 0):
            _fail(f"decision_rule.{key}", "must be a finite number, 0 or more")
    if "max_p" in rule and (isinstance(rule["max_p"], bool) or not isinstance(rule["max_p"], (int, float))
                            or not 0 < rule["max_p"] <= 1):
        _fail("decision_rule.max_p", "must be a number greater than 0 and at most 1")
    if kind == "keep_revert":
        if exp.get("split") is None:
            _fail("decision_rule.kind", "keep_revert needs a split of train and test item ids")
        if "improves" in rule and (not isinstance(rule["improves"], dict) or set(rule["improves"]) != {"test", "max_p"}
                                   or rule["improves"]["test"] != "task_sign"):
            _fail("decision_rule.improves", 'must be {"test": "task_sign", "max_p": p}')
        rng = rule.get("range", 1)
        if isinstance(rng, bool) or not isinstance(rng, (int, float)) or not math.isfinite(rng) or rng <= 0:
            _fail("decision_rule.range", "must be a positive number: the width of the metric's range")


def _leaves(value, prefix=""):
    if isinstance(value, dict):
        return {k: v for key, sub in value.items() for k, v in _leaves(sub, f"{prefix}{key}.").items()}
    return {prefix.rstrip("."): value}


def _climb(exp):
    """A climb experiment: baseline vs one candidate change, tasks split into train and test."""
    lanes = exp["lanes"]
    if [lane["name"] for lane in lanes] != ["baseline", "candidate"]:
        _fail("lanes", "a climb experiment has exactly two lanes, named baseline and candidate")
    base, cand = lanes
    patched = base["patch"] != cand["patch"]
    old, new = _leaves(base["settings"]), _leaves(cand["settings"])
    changed = sorted(k for k in old.keys() | new.keys() if old.get(k, _MISSING) != new.get(k, _MISSING))
    if base["sha"] != cand["sha"]:
        _fail("lanes", "baseline and candidate must use the same Kogen sha (change the patch or one setting)")
    if patched and changed:
        _fail("lanes", "candidate differs by a patch and by settings; change one thing")
    if not patched and len(changed) != 1:
        _fail("lanes", "candidate must differ by one patch or exactly one setting "
                       f"(differs in {len(changed)} settings and no patch)")
    split = _kind(exp.get("split"), dict, "split", "an object with train and test lists of task ids")
    ids = {}
    for part in ("train", "test"):
        ids[part] = _kind(split.get(part), list, f"split.{part}", "a non-empty list of task ids")
        if not ids[part]:
            _fail(f"split.{part}", "must be a non-empty list of task ids")
        for i, t in enumerate(ids[part]):
            _name(t, f"split.{part}[{i}]")
        if len(set(ids[part])) != len(ids[part]):
            _fail(f"split.{part}", "ids must be unique")
    if set(ids["train"]) & set(ids["test"]):
        _fail("split", "train and test must be disjoint")
    if set(ids["train"]) | set(ids["test"]) != set(exp["tasks"]):
        _fail("split", "train and test together must be exactly the experiment's tasks")
    effect = _kind(exp.get("min_effect"), (int, float), "min_effect", "a number (a pass-rate difference)")
    if not math.isfinite(effect) or not 0 < effect <= 1:
        _fail("min_effect", "must be greater than 0 and at most 1 (a pass-rate difference)")
    ref = exp.get("noise_ref")
    if not isinstance(ref, str) or not ref.strip():
        _fail("noise_ref", "must be a non-empty path string to a noise record")
    if _kind(exp.get("round"), int, "round", "an integer") < 1:
        _fail("round", "must be at least 1")
    if "parent" not in exp:
        _fail("parent", "is required (null or the previous round's id)")
    if exp["parent"] is None:
        if exp["round"] != 1:
            _fail("parent", "is required after round 1")
    else:
        _name(exp["parent"], "parent")
        if exp["round"] == 1:
            _fail("parent", "must be null in round 1")
        if exp["parent"] == exp["id"]:
            _fail("parent", "must be another round")
    rule = exp["decision_rule"]
    if rule["kind"] != "keep_revert":
        _fail("decision_rule.kind", "a climb experiment uses keep_revert")
    if "improves" in rule:
        imp = _kind(rule["improves"], dict, "decision_rule.improves", 'an object like {"test": "task_sign", "max_p": 0.1}')
        if set(imp) != {"test", "max_p"} or imp["test"] != "task_sign":
            _fail("decision_rule.improves", 'must be {"test": "task_sign", "max_p": p} and nothing else')
        p = imp["max_p"]
        if isinstance(p, bool) or not isinstance(p, (int, float)) or not 0 < p < 1:
            _fail("decision_rule.improves.max_p", "must be a number greater than 0 and less than 1")


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
