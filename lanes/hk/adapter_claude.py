"""CCMAC's Claude Code-alone lane, reusing the frozen bare runner and the lanes grader.

Only the staged HK experiments opt in. This module never runs a model on import.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

STUDY = "@STUDY@"
SUPPORT = Path(__file__).resolve().parents[3]
RESERVE_USD = 20.0  # Guard allowance, never reported as measured cost.


def bare_module():
    name = "hk_frozen_bare"
    if name not in sys.modules:
        # The original module imports pubmetrics and lanes. The latter is already
        # the pinned package; no active harness file is changed.
        sys.path.insert(0, str(SUPPORT))
        spec = importlib.util.spec_from_file_location(name, SUPPORT / "lanes_bare.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def _claude_host(run_dir, host):
    """The Claude Code binary and seat of this run's hosts.json, the same ones the Kogen arm's executor uses."""
    h = json.loads(Path(run_dir, "hosts.json").read_text())[host]
    return h["claude_bin"], h["kogen_token_home"]


def run(run_dir, cell_id, tasks, exp, lane, host, keep=False, force=False):
    from . import cell, common, costguard, live, node_modules
    driver = lane.get("driver")
    arm = {"codex-alone": "codex", "claude-code-alone": "claude"}.get(driver)
    if exp.get("hk_study") != STUDY or os.environ.get("HK_STUDY") != STUDY:
        raise cell.CellError("CCMAC alone driver requires the registered adapter")
    models = lane["settings"]["models"]
    if exp.get("phase") != "e2e" or arm != "claude" or list(models) != ["build"] or not models["build"].startswith("claude-code/"):
        raise cell.CellError("CCMAC Claude Code-alone settings differ from registration")
    spec = models["build"].split("/", 1)[1]
    model, effort = spec.split()
    kogen = [l for l in exp["lanes"] if l.get("driver") == "kogen-e2e"]
    if len(kogen) != 1 or set(kogen[0]["settings"]["models"].values()) != {"claude-code/" + spec}:
        raise cell.CellError("CCMAC arms must use the same model and effort for every role")
    claude_bin, token_home = _claude_host(run_dir, host)
    if claude_bin != exp["hk_claude_bin"] or os.path.realpath(claude_bin) != claude_bin or "/current/" in claude_bin:
        raise cell.CellError("CCMAC Claude Code binary is not the registered fixed release path")
    task_id, rep, lane_name = cell_id.split("/")
    out = common.cell_dir(run_dir, cell_id)
    if os.path.exists(out):
        # A partial attempt must be audited by the owner, never silently retired.
        raise cell.CellError("CCMAC cell directory already exists; use a separately registered replacement")
    costguard.check_start(run_dir, exp, cell_id)
    os.makedirs(out)
    tmp = tempfile.mkdtemp(prefix="ccmac-claude-")
    ws = os.path.join(tmp, "ws")
    os.makedirs(ws)
    info = dict(live.record(tmp, host), arm=arm, hk_study=STUDY)
    common.write_json(os.path.join(out, costguard.LIVE), info)
    os.rmdir(ws)  # The bare runner makes its workspace with copytree.
    bare = bare_module()
    a = argparse.Namespace(
        arm=arm, model=model, effort=effort, host=host, claude_bin=claude_bin, claude_token_home=token_home,
        claude_config_dir=None, deadline_s=exp["deadline_s"], cpu_profile=False,
    )
    task = os.path.join(tasks, task_id)
    try:
        tt, _, _ = bare.load_task_inputs(task, exp["intent_form"])
        tt = dict(tt, setup=node_modules.setup(task, tt.get("setup") or []))
        result = bare.bare_cell(a, cell_id, lane_name, task, tt, exp["intent_form"], ws, tmp, out)
        result.update(hk_study=STUDY, pipeline=driver, claude_bin=claude_bin,
                      repetition_block=exp["hk_repetition_block"],
                      adapter_sha256=common.sha256_file(__file__))
        common.write_json(os.path.join(out, "result.json"), result)
        return result
    finally:
        # Preserve unfinished workspace/spend on an exception for owner audit.
        if os.path.isfile(os.path.join(out, "result.json")):
            Path(out, costguard.LIVE).unlink(missing_ok=True)
            if not keep:
                shutil.rmtree(tmp)


def codex_spend(cell_dir):
    """None for ordinary lanes; conservative guard estimate for HK's Codex lane."""
    from . import common, costguard, usage
    p = Path(cell_dir)
    result = json.loads((p / "result.json").read_text()) if (p / "result.json").exists() else {}
    info = json.loads((p / "live.json").read_text()) if (p / "live.json").exists() else {}
    if (result or info).get("hk_study") != STUDY or (result or info).get("arm") != "codex":
        return None
    measured = (result.get("totals") or {}).get("cost_usd")
    if measured is not None:
        return float(measured)
    stream = p / "usage-events.jsonl"
    rec = bare_module().parse_codex(str(stream)) if stream.exists() else {}
    counts = {k: rec.get(k) for k in ("input_tokens", "cached_input_tokens", "output_tokens")}
    if any(v is None for v in counts.values()):
        return RESERVE_USD
    calc, table, rates = costguard.pricing()
    value, _ = usage.request_cost("gpt-6.1-terra", counts, table, calc)
    return value if value is not None else costguard._unpriced_cost("gpt-6.1-terra", counts, table, calc, rates)
