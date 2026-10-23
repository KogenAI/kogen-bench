"""Export a graded lane run as a kogen-bench round: Standard 1.2 records, bundles, PLAN, README.

Adapted from the Lab's export_bench_round.py: one record per graded cell, every field Kogen
b45ba32b does not log is a declared missing marker (never a guess), public files are scrubbed of
personal paths, hosts and credentials, and the output is checked with the bench validator.
The round is built in a temporary folder and scanned for leaks; only then is it moved into the
checkout, registered and validated, and a failure there restores the checkout as it was.
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

from . import common, experiment, plan_hashes, usage

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PHASES = ("setup", "shape", "plan", "develop", "review", "gate", "grade")
# Kogen stage records per Standard phase. The Lab maps develop = build + fix; here `repair` is the
# fix. Tokens are disjoint (a request is in one record); times are not: `review`/`verify` are sums
# of request wall time inside the build command, so they overlap `develop` (the build command).
PHASE_STAGES = {"shape": ("shape",), "develop": ("build", "repair"), "review": ("review",), "gate": ("verify",)}
STOP = {"landed": "completed", "timeout": "timeout"}
WHY = "DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE"
REGISTRY = ("rounds/STATUS.md", "rounds/index.json", "rounds/README.md", "reproduce/round-inventory.json")
SHAPE_KEYS = ("scenarios", "pass_on_reference", "fail_on_start", "wrong_caught", "wrong_total")
EVAL_KEYS = ("all_passed", "commands", "expected", "ids", "infrastructure", "grader_version") + SHAPE_KEYS
WITHHELD = {"withheld": "Host details are withheld by the public record policy."}
TOKEN_KEYS = ("input", "cached_input", "output", "reasoning")
# The Lab's path roots (privacy.go userPathRoots) are all kept: a path under any of them is private.
ROOTS = "Users|home|private|tmp|var|opt|srv|root|mnt|Volumes"
EMAIL = r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
CRED = r"\b(?:sk-ant-|sk-|eyJ|xai-|gho_)[A-Za-z0-9_.-]{8,}"
LEAK = [re.compile(p) for p in (EMAIL, CRED, rf"/(?:{ROOTS})/[^\s\"'<>)\]]*", r"~/[^\s\"']+", r"\b\d{1,3}(?:\.\d{1,3}){3}\b")]
# Patches are copied byte for byte (their hash is in PLAN.json), so they are only checked, and only
# for what cannot appear in honest code context: credentials, emails and home directories.
PATCH_LEAK = [re.compile(p) for p in (EMAIL, CRED, r"/(?:Users|home)/[^\s\"'<>)\]]+", r"~/[^\s\"']+")]


class ExportError(Exception):
    def __init__(self, message, code=1):
        super().__init__(message)
        self.code = code


# ---- privacy filter -------------------------------------------------------------------------

def scrub(value, hosts=()):
    """Replace personal paths, emails, credentials, IPs and the experiment's host names."""
    if isinstance(value, dict):
        return {scrub(k, hosts): scrub(v, hosts) for k, v in value.items()}
    if isinstance(value, list):
        return [scrub(v, hosts) for v in value]
    if not isinstance(value, str):
        return value
    for h in hosts:
        value = re.sub(rf"(?<![A-Za-z0-9.-]){re.escape(h)}(?![A-Za-z0-9-])", "[redacted host]", value)
    for rx in LEAK:
        value = rx.sub("[redacted]", value)
    return value


def leaks(text, hosts=(), patterns=LEAK):
    return [m.group(0) for rx in patterns for m in rx.finditer(text)] + [h for h in hosts if h in text]


def scan(folder, hosts):
    found = []
    for dirpath, _, files in os.walk(folder):
        for n in files:
            p = os.path.join(dirpath, n)
            rel = os.path.relpath(p, folder)
            patch = rel.split(os.sep)[0] == "patches"
            with open(p, encoding="utf-8", errors="replace") as f:
                hits = leaks(f.read(), hosts, PATCH_LEAK if patch else LEAK)
            found += [f"{rel}{' (patch rule: credentials, emails, home paths, hosts)' if patch else ''}: {h}" for h in hits[:3]]
    if found:
        raise ExportError("private data left in the export: " + "; ".join(found[:5]))


# ---- markers --------------------------------------------------------------------------------

def miss(code):
    return {"missing": code}


def na(why):
    return {"not_applicable": why}


def is_marker(v):
    return isinstance(v, dict) and len(v) == 1 and "missing" in v


def leaves(value, path=""):
    if isinstance(value, dict) and not any(k in value for k in ("missing", "not_applicable", "withheld")):
        for k, v in value.items():
            yield from leaves(v, f"{path}.{k}" if path else k)
    else:
        yield path, value


def utc(value, code):
    if isinstance(value, str):
        try:
            t = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
            if t.utcoffset() == datetime.timedelta(0):
                return value
        except ValueError:
            pass
    return miss(code)


def one(values, code):
    values = sorted({v for v in values if isinstance(v, str) and v})
    return values[0] if len(values) == 1 else miss(code)


# ---- one cell -> one record -----------------------------------------------------------------

def tokens(stages):
    """Standard counters summed over stage records; `input` excludes the cached part. None if any is unknown."""
    keys = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_tokens")
    if not stages or any(s.get(k) is None for s in stages for k in keys) or any("usage_zero_is_unknown" in s["missing"] for s in stages):
        return None
    i, c, o, r = (sum(s[k] for s in stages) for k in keys)
    return {"input": i - c, "cached_input": c, "output": o, "reasoning": r}


def phase_tokens(stages, phase):
    own = [stages[s] for s in PHASE_STAGES.get(phase, ()) if s in stages]
    if not own:
        return {k: na(f"Kogen logged no {phase} request in this cell.") for k in TOKEN_KEYS}
    return tokens(own) or {k: miss("m44") for k in TOKEN_KEYS}


def phase_time(stages, evaluation, phase):
    if phase == "plan":
        return na("Kogen has no separate plan phase.")
    if phase == "grade":  # the Lab declares grade time n/a; here the grader's own command wall time is known
        ms = [c.get("wall_ms") for c in evaluation.get("commands", []) if isinstance(c, dict)]
        return round(sum(ms) / 1000, 3) if ms and all(isinstance(m, int) for m in ms) else miss("m45")
    if phase == "setup":
        return miss("m45")
    own = [stages[s] for s in PHASE_STAGES[phase] if s in stages]
    if not own:
        return na(f"Kogen logged no {phase} stage in this cell.")
    wall = own[0].get("wall_s")  # build's wall already holds its repair requests
    return wall if isinstance(wall, (int, float)) else miss("m45")


def outcome_of(ev):
    """pass | fail | invalid. Shape cells (no `all_passed`): pass when every scenario passes on the
    reference tree, every one fails on the start tree and every known-wrong tree is caught; anything else
    is declared missing."""
    if ev.get("infrastructure"):
        return "invalid"
    if isinstance(ev.get("all_passed"), bool):
        return "pass" if ev["all_passed"] else "fail"
    if all(isinstance(ev.get(k), int) for k in SHAPE_KEYS):
        ok = (ev["scenarios"] > 0 and ev["pass_on_reference"] == ev["scenarios"]
              and ev["fail_on_start"] == ev["scenarios"] and ev["wrong_caught"] == ev["wrong_total"])
        return "pass" if ok else "fail"
    return miss("m32")


def stop_reason(res, events):
    outcomes = [e for e in events if e.get("event") == "outcome"]
    if outcomes and outcomes[-1].get("provider_failure"):
        return "provider_error"
    return STOP.get(res.get("outcome"), miss("m31"))


def public_cell(res, ev, hosts):
    """The scrubbed attempt and evaluation published in the bundle (the record's ledger hash covers them)."""
    keys = ("cell", "lane", "phase", "outcome", "exit_code", "started", "ended", "wall_s", "kogen_version",
            "intent_hash", "final_tree", "pass_trees", "stages", "totals")
    return scrub({k: res.get(k) for k in keys}, hosts), scrub({k: ev[k] for k in EVAL_KEYS if k in ev}, hosts)


def record(round_id, plan_sha, ctx, row, res, ev, events):
    lane, lock = ctx["lanes"][row["lane"]], ctx["lock"][row["lane"]]
    stages = {s["stage"]: s for s in res.get("stages", [])}
    totals = res.get("totals") or {}
    models = [m.split(" ")[0] for m in lane["settings"].get("models", {}).values()]
    efforts = [m.split(" ")[1] for m in lane["settings"].get("models", {}).values() if " " in m]
    effort = one([e.get("effort") for e in events if e.get("event") == "request"], "m73")
    cost = totals.get("cost_usd")
    calc = usage._cost_calc()
    start, end = utc(res.get("started"), "m69"), utc(res.get("ended"), "m68")
    attempts = miss("m60") if is_marker(start) or is_marker(end) else [{"attempt": 1, "start_utc": start, "end_utc": end}]
    toolchain = {k: miss("m95") for k in ("python", "ruby", "elixir", "erlang", "rust", "node")}
    toolchain["other_inventory"] = miss("m64")
    attempt, evaluation = public_cell(res, ev, ctx["experiment"].get("hosts", []))
    grader = ev.get("grader_version") or miss("m77")
    return {
        "schema_version": "1.2", "audit_round": round_id, "round_id": round_id,
        "cell_id": f"{round_id}-{row['task']}-r{row['rep']}-{row['lane']}",
        "task": {"id": row["task"], "base_repo": miss("m39"), "base_revision": {"kind": miss("m43"), "hash": miss("m42")}},
        "arm": row["lane"], "harness": "kogen-lanes",
        "model": {"requested": one(models, "m39"), "effective": one(totals.get("models", []), "m74")},
        "effort": {"requested": one(efforts, "m39"), "effective": miss("m73") if effort == "provider_default" else effort,
                   "runner_requested": one(efforts, "m39")},
        "recipe": (f"lane {lane['name']} kogen:{lane['sha']} patch_sha256:{lock.get('patch_sha256') or 'none'} "
                   f"artifact_sha256:{lock['artifact_sha256']} models:{json.dumps(lane['settings'].get('models', {}), sort_keys=True)}"),
        "host": {"id": miss("m39"), **{k: WITHHELD for k in ("spec_ref", "cpu", "vcpu", "ram_gib", "os", "kernel")}},
        "tools": {"harness": "kogen-lanes", "kogen": res.get("kogen_version") or lock.get("kogen_version") or lane["sha"],
                  "codex_cli": na("Kogen does not use Codex CLI."), "runner": miss("m83"), "grader": grader, "toolchains": toolchain},
        "sandbox": {"profile": miss("m87"), "profile_sha256": miss("m86"), "egress_profile": miss("m76"), "egress_allow": miss("m75")},
        "timing": {"phases_s": {p: phase_time(stages, ev, p) for p in PHASES},
                   "total_wall_s": res["wall_s"] if isinstance(res.get("wall_s"), (int, float)) else miss("m58"),
                   "timeout_cap_s": ctx["experiment"]["deadline_s"]},
        "tokens": {"phases": {p: phase_tokens(stages, p) for p in PHASES},
                   "total": tokens([{**totals, "missing": totals.get("missing", [])}]) or {k: miss("m10") for k in TOKEN_KEYS}},
        # The table version is read at export time, not recorded per cell (see ISSUES: L1b should log it in totals).
        "cost": {"usd": cost if cost is not None else miss("m70"), "price_table_version": calc.load_table().get("version") or miss("m89"),
                 "calculator_version": calc.VERSION,
                 "accounting": f"per-request {calc.VERSION}" + (f" ({totals['cost_reason']})" if totals.get("cost_reason") else "")
                 if cost is not None else miss("m70"),
                 "long_context_reconciled": miss("m07")},
        "outcome": outcome_of(ev),
        "stop_reason": stop_reason(res, events),
        "graded": True,
        "itt": {"class": "counted", "evidence_ref": na("Every graded cell counts; no exclusion was applied."), "cohort": "scored"},
        "kogen": {"landed": res.get("outcome") == "landed",
                  "best_candidate": res["final_tree"] if res.get("final_tree") else na("The cell produced no final tree.")},
        "grade": {"grader": grader, "tests_ran": not ev.get("infrastructure"), "timestamp": utc(ev.get("graded_at"), "m32")},
        # ledger_sha256 = plan_hashes.sha256_json({"attempt": <attempt.json>, "evaluation": <evaluation.json>}) of the bundle files.
        "provenance": {"ledger_sha256": plan_hashes.sha256_json({"attempt": attempt, "evaluation": evaluation}),
                       "manifest_sha256": plan_sha, "source_ref": "PLAN.json"},
        "timestamps": {"cell": {"start_utc": start, "end_utc": end},
                       "phases": {p: {"start_utc": miss("m88"), "end_utc": miss("m88")} for p in PHASES}, "attempts": attempts},
        "circumstances": {"load1_start": miss("m65"), "load1_end": miss("m65"), "concurrent_cells_start": miss("m66"),
                          "concurrent_cells_end": miss("m66"), "cap_start": miss("m08"), "cap_end": miss("m08"),
                          "queue": miss("m91"), "dispatcher_id": miss("m63"), "incidents": miss("m78"), "load_samples": miss("m93")},
        "environment": {**{k: WITHHELD for k in ("os", "kernel", "cpu_model", "cores", "ram_gib")},
                        "toolchains": toolchain, "network": {"profile": miss("m80"), "allowlist_hosts": miss("m79")},
                        "account_class": miss("m100")},
        "setup": {"task_base": {"kind": miss("m43"), "hash": miss("m42")}, "adapter_harness_sha": miss("m39"),
                  "sandbox_mode": miss("m85"), "sandbox_profile_sha256": miss("m84"), "deps_source": miss("m71"),
                  "kogen_sha": lane["sha"]},
    }


# ---- run directory --------------------------------------------------------------------------

def load_run(run_dir):
    exp_path = os.path.join(run_dir, "experiment.json")
    try:
        exp = experiment.load(exp_path)
        lock = {e["name"]: e for e in common.read_json(os.path.join(run_dir, "lanes.lock.json"))}
        plan = common.read_jsonl(os.path.join(run_dir, "plan.jsonl"))
    except (OSError, ValueError, experiment.ExperimentError, KeyError, TypeError) as e:
        raise ExportError(f"run dir {run_dir}: {e}") from None
    cells, skipped, started = [], [], 0
    for row in sorted(plan, key=lambda r: r.get("order", 0)):
        cd = common.cell_dir(run_dir, row["cell"])
        res, ev = os.path.join(cd, "result.json"), os.path.join(cd, "evaluation.json")
        started += os.path.isfile(res)
        if not (os.path.isfile(res) and os.path.isfile(ev)):
            skipped.append({"cell": row["cell"], "reason": "no result or no evaluation"})
            continue
        events = usage.read_log(os.path.join(cd, "run-log", "log.jsonl")) or []
        cells.append((row, common.read_json(res), common.read_json(ev), events))
    return {"experiment": exp, "exp_path": exp_path, "lanes": {l["name"]: l for l in exp["lanes"]}, "lock": lock,
            "plan_rows": plan, "cells": cells, "skipped": skipped, "started": started}


def load_plan(run_dir, ctx):
    """The run's PLAN.json, written before the run; it is never rebuilt here (that would hash today's inputs)."""
    path = os.path.join(run_dir, "PLAN.json")
    if not os.path.isfile(path):
        raise ExportError("the run dir has no PLAN.json; it must be written before the run (lanes-plan)", 2)
    plan = common.read_json(path)
    public = {k: v for k, v in ctx["experiment"].items() if k != "hosts"}
    if plan.get("experiment") != public:
        raise ExportError("PLAN.json's experiment differs from the run's experiment.json", 2)
    if plan.get("lock", {}).get("sha256") != common.sha256_file(os.path.join(run_dir, "lanes.lock.json")):
        raise ExportError("lanes.lock.json differs from the PLAN.json lock hash", 2)
    return plan


# ---- round documents ------------------------------------------------------------------------

def patch_lines(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    return (sum(1 for l in lines if l.startswith("+") and not l.startswith("+++")),
            sum(1 for l in lines if l.startswith("-") and not l.startswith("---")))


def lanes_table(ctx, plan):
    repo = ctx["experiment"]["kogen"]["repo"]
    base = re.sub(r"\.git$", "", repo) if re.match(r"https?://", repo) else None
    rows = ["| Lane | Base Kogen | Patch | Models | Artifact sha256 |", "| --- | --- | --- | --- | --- |"]
    for name, lane in ctx["lanes"].items():
        sha = f"[`{lane['sha'][:8]}`]({base}/commit/{lane['sha']})" if base else f"`{lane['sha'][:8]}`"
        patch = "none"
        if lane["patch"]:
            file = os.path.basename(lane["patch"])
            add, rem = patch_lines(experiment.patch_path(ctx["exp_path"], lane))
            patch = f"[{file}](patches/{name}/{file}) `{plan['hashes']['lanes'][name]['patch']}` +{add}/-{rem}"
        models = "; ".join(f"{r}: {m}" for r, m in sorted(lane["settings"].get("models", {}).items())) or "defaults"
        rows.append(f"| {name} | {sha} | {patch} | {models} | `{ctx['lock'][name]['artifact_sha256']}` |")
    return "\n".join(rows)


def results_table(ctx, records, evals):
    arms = {l: [(r, e) for r, e in zip(records, evals) if r["arm"] == l] for l in ctx["lanes"]}
    if ctx["experiment"]["phase"] == "shape":
        rows = ["| Lane | Cells | Cells passing the shape rule | Scenarios passing on reference | Wrong trees caught |",
                "| --- | ---: | ---: | ---: | ---: |"]
        for l, cells in arms.items():
            tot = lambda k: sum(e.get(k) or 0 for _, e in cells)
            rows.append(f"| {l} | {len(cells)} | {sum(r['outcome'] == 'pass' for r, _ in cells)} | "
                        f"{tot('pass_on_reference')} of {tot('scenarios')} | {tot('wrong_caught')} of {tot('wrong_total')} |")
        return "\n".join(rows) + "\n\nShape rule: all scenarios pass on the reference tree and every known-wrong tree is caught."
    rows = ["| Lane | Cells | All hidden tests passed |", "| --- | ---: | ---: |"]
    return "\n".join(rows + [f"| {l} | {len(c)} | {sum(r['outcome'] == 'pass' for r, _ in c)} |" for l, c in arms.items()])


def declaration(records, legend):
    counts = {}
    for r in records:
        for path, v in leaves(r):
            if is_marker(v):
                counts.setdefault(path, Counter())[v["missing"]] += 1
    fields, sources = {}, {"reconstructable": {}, "lost": {}}
    for path, codes in sorted(counts.items()):
        reasons = Counter()
        for c, n in codes.items():
            reasons[legend[c]["reason"]] += n
            src = legend[c]["reconstructable_from"]
            cat = "lost" if src in ("none", "not re-derivable from the public record") else "reconstructable"
            sources[cat].setdefault(path, Counter())[src] += n
        main = codes.most_common(1)[0][0]
        fields[path] = {"affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release "
                        "eligibility; they do not change the hidden-test outcomes reported on this page.",
                        "count": sum(codes.values()), "reason_code": main, "reasons": dict(sorted(reasons.items())),
                        "note": f"Kogen b45ba32b and the lane harness do not log this field. {legend[main]['reason']}."}
    return fields, {c: {p: dict(s) for p, s in d.items()} for c, d in sources.items()}


def missing_section(fields, legend):
    return "\n".join(f"- `{p}` ({d['count']} missing): {d['note']} Reason: {legend[d['reason_code']]['reason']} (`{d['reason_code']}`)."
                     for p, d in sorted(fields.items()))


def harness_commit():
    r = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True)
    sha = r.stdout.strip()
    return sha if r.returncode == 0 and re.fullmatch(r"[0-9a-f]{40}", sha) else "not recorded (harness not in a git checkout)"


def write_text(out, name, text):
    with open(os.path.join(out, name), "w", encoding="utf-8") as f:
        f.write(text)


def write_docs(out, round_id, date, ctx, plan, records, evals, legend):
    fields, gap_sources = declaration(records, legend)
    exp, n = ctx["experiment"], len(records)
    deviations = ["Cells ran in the kogen-lanes harness, not a registered kogen-bench protocol: no official grade receipts, sandbox, "
                  "venue, host or ITT receipts. Missing values remain unknown and are not zero measurements."]
    common.write_json(os.path.join(out, "MISSING-DECLARED.json"), {"round_id": round_id, "cells": n, "fields": fields})
    decl = {"round": round_id, "cells": n, "fields": {p: {k: d[k] for k in ("count", "reasons", "affects_verdict")} for p, d in fields.items()},
            "gap_sources": gap_sources, "protocol_deviations": deviations}
    lines = [f"# Missing data — {round_id}", "", f"Cells: {n}", "", "Declared gaps:"]
    lines += [f"- `{p}`: {d['count']} — " + "; ".join(f"{r} ({c})" for r, c in d["reasons"].items()) + f". {d['affects_verdict']}"
              for p, d in fields.items()] or ["- None."]
    write_text(out, "MISSING.md", "\n".join(lines + ["", "```json", json.dumps(decl, indent=2, sort_keys=True), "```", ""]))
    write_text(out, "MEASURED.md", f"# Measurement record — {round_id}\n\nQuestion: Hidden-test outcomes, per-stage usage, cost and time of {n} "
               f"lane cells are represented in Standard run record 1.2.\n\nRequired metrics: official benchmark outcome, stop cause, phase and "
               f"total time, normalized tokens, cost, venue, sandbox, and ITT receipts.\n\nCoverage: {n} records, one per graded cell, from "
               f"experiment `{exp['id']}` (phase `{exp['phase']}`).\n\nEffect of missing data: unavailable Standard fields prevent complete "
               f"capture and strict release eligibility. Raw model transcripts and tool output are not published.\n")
    used = {f"{r} {m}" for l in ctx["lanes"].values() for r, m in l["settings"].get("models", {}).items()}
    models = "; ".join(sorted(used)) or "the Kogen defaults"
    write_text(out, "README.md", f"""# {round_id}

A lane comparison of real Kogen builds: experiment `{exp['id']}`, phase `{exp['phase']}`, {len(exp['tasks'])} task(s), {exp['reps']} repetition(s), \
{len(ctx['lanes'])} lane(s). Descriptive: no official benchmark grade.

## Lanes

{lanes_table(ctx, plan)}

## Results

{results_table(ctx, records, evals)}

Decision rule `{exp['decision_rule']['kind']}` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | {len(ctx['plan_rows'])} |
| Started cells | {ctx['started']} |
| Finished cells | {ctx['started']} |
| Graded cells | {n} |
| ITT count | {n} |

## Metadata

Round date: {date}
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: {WHY} — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: {harness_commit()}
Model and effort: {models}
Task IDs: {', '.join(exp['tasks'])}
Command: lanes-run, lanes-grade and lanes-export on experiment `{exp['id']}`.
Kogen commits: {', '.join(sorted({l['sha'] for l in ctx['lanes'].values()}))}
Raw records: records.jsonl and the bundle in bundles/{round_id} preserve every cell's outcome and stages; a record's `ledger_sha256` \
hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; \
`--publish-private` adds the files after the round closes.

## What's missing and why
{missing_section(fields, legend)}
""")


def write_bundle(out, round_id, ctx, published):
    base = os.path.join(out, "bundles", round_id)
    common.write_json(os.path.join(base, "manifest.json"), {"experiment": ctx["experiment"]["id"], "phase": ctx["experiment"]["phase"],
                                                           "lanes": sorted(ctx["lanes"]), "cells": len(ctx["cells"])})
    common.write_json(os.path.join(base, "EXCLUDED.json"), {"round_id": round_id, "excluded": ctx["skipped"]})
    for (row, *_), (attempt, evaluation) in zip(ctx["cells"], published):
        d = os.path.join(base, "attempts", row["task"], f"r{row['rep']}", row["lane"], "a1")
        common.write_json(os.path.join(d, "attempt.json"), attempt)
        common.write_json(os.path.join(d, "evaluation.json"), evaluation)


# ---- registry -------------------------------------------------------------------------------

def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def read_bytes(path):
    if not os.path.isfile(path):
        return None
    with open(path, "rb") as f:
        return f.read()


def append(path, text):
    old = read_text(path)
    with open(path, "a", encoding="utf-8") as f:
        f.write(("" if old.endswith("\n") or not old else "\n") + text)


def register(bench, round_id, ctx, n):
    """Add the round to STATUS.md, index.json, README.md and round-inventory.json (idempotent)."""
    rounds = os.path.join(bench, "rounds")
    if not re.search(rf"^{re.escape(round_id)} \|", read_text(os.path.join(rounds, "STATUS.md")), re.M):
        append(os.path.join(rounds, "STATUS.md"), f"{round_id} | DESCRIPTIVE | {WHY} — lane comparison, {n} graded cells, "
               "hidden-test outcomes only.\n")
    ids = common.read_json(os.path.join(rounds, "index.json"))
    if round_id not in ids:
        common.write_json(os.path.join(rounds, "index.json"), ids + [round_id])
    path = os.path.join(bench, "reproduce", "round-inventory.json")
    inv = json.loads(read_text(path))
    if not any(e.get("round_id") == round_id for e in inv["rounds"]):
        base = os.path.join(rounds, round_id)
        files = sorted(os.path.relpath(os.path.join(d, f), bench) for d, _, fs in os.walk(base) for f in fs)
        inv["rounds"].append({"round_id": round_id, "script": None, "inputs": files, "replay_type": "analysis-only",
                              "full_execution_replayable": False,
                              "availability_note": "Records and bundles preserve the graded outcomes; model execution is rerun with the "
                              "reader's own login (lanes/reproduce.sh --rerun)."})
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(inv, indent=2, ensure_ascii=False) + "\n")
    if f"]({round_id}/README.md)" not in read_text(os.path.join(rounds, "README.md")):
        append(os.path.join(rounds, "README.md"), f"\n- [Lane comparison {round_id}]({round_id}/README.md) — **DESCRIPTIVE** "
               f"{n} graded cells across {len(ctx['lanes'])} lanes; hidden-test outcomes only.\n")


# ---- export ---------------------------------------------------------------------------------

def bench_root(out):
    root = os.path.dirname(os.path.dirname(os.path.abspath(out)))
    if not os.path.isfile(os.path.join(root, "reproduce", "validate_release.py")):
        raise ExportError(f"--out must be <kogen-bench>/rounds/<id>; {root} is not a kogen-bench checkout", 2)
    return root


def build_round(stage, run_dir, round_id, date, ctx, plan, legend):
    hosts = ctx["experiment"].get("hosts", [])
    for name, lane in ctx["lanes"].items():
        if lane["patch"]:
            src = experiment.patch_path(ctx["exp_path"], lane)
            dest = os.path.join(stage, "patches", name, os.path.basename(src))
            os.makedirs(os.path.dirname(dest))
            shutil.copyfile(src, dest)
    common.write_json(os.path.join(stage, "PLAN.json"), scrub(plan, hosts))
    plan_sha = common.sha256_file(os.path.join(stage, "PLAN.json"))
    records = [scrub(record(round_id, plan_sha, ctx, row, res, ev, events), hosts) for row, res, ev, events in ctx["cells"]]
    if len({r["cell_id"] for r in records}) != len(records):
        raise ExportError("cell ids are not unique")
    with open(os.path.join(stage, "records.jsonl"), "w", encoding="utf-8") as f:
        f.writelines(json.dumps(r, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n" for r in records)
    published = [public_cell(res, ev, hosts) for _, res, ev, _ in ctx["cells"]]
    write_bundle(stage, round_id, ctx, published)
    write_docs(stage, round_id, date, ctx, plan, records, [e for _, e in published], legend)
    scan(stage, hosts)
    return len(records)


def validate(bench, round_id, out, mode):
    if mode == "none":
        return 0
    if mode == "round":
        cmd = [sys.executable, "reproduce/validate_round.py", "--round", round_id, "--strict", "--records", os.path.join(out, "records.jsonl")]
    else:
        cmd = [sys.executable, "reproduce/validate_release.py", "--strict"]
    with tempfile.TemporaryFile("w+") as log:
        code, timed_out = common.run(cmd, cwd=bench, deadline_s=1800, stdout=log, stderr=subprocess.STDOUT)
        log.seek(0)
        lines = log.readlines()
    shown = [l for l in lines if '"verdict"' in l or "RELEASE GATE" in l or "NEW ROUNDS" in l] if code == 0 else lines[:60]
    sys.stdout.write("".join(shown))
    return 1 if timed_out else code


def export(run_dir, round_id, out, date=None, do_register=True, check="release"):
    """Build, scan, place, register and validate a round; returns the validator's exit code.
    Any failure leaves the checkout exactly as it was."""
    out = os.path.abspath(out)
    bench = bench_root(out)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", round_id) or round_id != os.path.basename(out):
        raise ExportError("--round-id must equal the name of the --out folder", 2)
    if os.path.isdir(out) and os.listdir(out):
        raise ExportError(f"{out} is not empty", 2)
    ctx = load_run(run_dir)
    plan = load_plan(run_dir, ctx)
    if not ctx["cells"]:
        raise ExportError("the run has no graded cell")
    legend = json.loads(read_text(os.path.join(bench, "results", "missing-reasons.json")))["codes"]
    date = date or datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    stage = tempfile.mkdtemp(prefix=f".{round_id}-", dir=os.path.dirname(out))
    snapshot = {p: read_bytes(os.path.join(bench, p)) for p in REGISTRY}
    placed = ok = False
    try:
        n = build_round(stage, run_dir, round_id, date, ctx, plan, legend)
        if os.path.isdir(out):
            os.rmdir(out)
        os.rename(stage, out)
        placed = True
        if do_register:
            register(bench, round_id, ctx, n)
        code = validate(bench, round_id, out, check)
        ok = code == 0
    finally:
        if not ok:
            shutil.rmtree(out if placed else stage, ignore_errors=True)
            for p, data in snapshot.items():
                if placed and data is not None:
                    with open(os.path.join(bench, p), "wb") as f:
                        f.write(data)
        shutil.rmtree(stage, ignore_errors=True)
    if ok:
        print(f"wrote {n} Standard 1.2 records to {out}")
    return code


# ---- publish-private ------------------------------------------------------------------------

CELL_FILES = ("final-tree.tar", "pass-trees", "intent")  # what lanes-grade reads from a cell besides result.json


def published_cell(reproduce_root, cell):
    """Where a round's `reproduce/` folder holds a cell's trees; the one definition of the layout."""
    return os.path.join(reproduce_root, "cells", *cell.split("/"))


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def published_hidden_files(stage, plan, task_ids):
    """sha256 of every file under each published `evaluator/`, keyed by its path relative to the round.
    Refuses when a published evaluator/ folder no longer hashes to the pre-run `hidden_tests` hash in PLAN.
    The source was checked just before the copy, so this guards the copy itself (a change in between)."""
    files, bad = {}, []
    for task in task_ids:
        folder = os.path.join(stage, "tasks", task, "evaluator")
        if common.sha256_tree(folder) != plan["hashes"]["tasks"][task]["hidden_tests"]:
            bad.append(f"reproduce/tasks/{task}/evaluator")
        for d, _, names in os.walk(folder):
            for name in names:
                path = os.path.join(d, name)
                files["/".join(("reproduce", os.path.relpath(path, stage).replace(os.sep, "/")))] = common.sha256_file(path)
    if bad:
        raise ExportError("published hidden tests differ from the PLAN.json hashes (nothing was published): " + ", ".join(bad))
    return dict(sorted(files.items()))


def rebind_records(out, old_sha, new_sha):
    """The marker changes PLAN.json's file hash; point each record's `manifest_sha256` at the published file
    (reproduce.py checks it). Records are only touched when they name the previous PLAN.json hash."""
    path = os.path.join(out, "records.jsonl")
    if old_sha == new_sha or not os.path.isfile(path):
        return
    rows = common.read_jsonl(path)
    for r in rows:
        prov = r.get("provenance", {})
        if prov.get("manifest_sha256") == old_sha:
            prov["manifest_sha256"] = new_sha
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n")


def publish_private(run_dir, out, tasks):
    """Check the private inputs against the PLAN hashes, then copy them and each graded cell's trees into the round.
    The whole `reproduce/` folder is built aside and swapped in, so a re-run yields the same files."""
    ctx = load_run(run_dir)
    exp, plan = ctx["experiment"], common.read_json(os.path.join(out, "PLAN.json"))
    bad = []
    for task in exp["tasks"]:
        got = plan_hashes.task_hashes(os.path.join(tasks, task), exp["phase"], exp.get("intent_form"))
        bad += [f"tasks/{task}/{k}" for k, v in got.items() if v != plan["hashes"]["tasks"][task].get(k)]
    for name, lane in ctx["lanes"].items():
        want = plan["hashes"]["lanes"][name]
        if plan_hashes.sha256_json(lane["settings"]) != want["settings"]:
            bad.append(f"settings/{name}")
        if lane["patch"]:
            copy = os.path.join(out, "patches", name, os.path.basename(lane["patch"]))
            if not os.path.isfile(copy) or common.sha256_file(copy) != want["patch"]:
                bad.append(f"patches/{name}")
    if bad:
        raise ExportError("private inputs differ from PLAN.json (nothing was copied): " + ", ".join(bad))
    work = tempfile.mkdtemp(prefix=".private-", dir=out)
    stage = os.path.join(work, "reproduce")
    try:
        for task in exp["tasks"]:
            shutil.copytree(os.path.join(tasks, task), os.path.join(stage, "tasks", task), ignore=shutil.ignore_patterns(".git"))
        for name, lane in ctx["lanes"].items():
            common.write_json(os.path.join(stage, "settings", f"{name}.json"), lane["settings"])
        grade = os.path.join(REPO, "lanes", "grade")
        common.write_json(os.path.join(stage, "grader.json"), {"source_sha256": common.sha256_tree(grade) if os.path.isdir(grade) else None})
        for row, _, _, _ in ctx["cells"]:
            src, dest = common.cell_dir(run_dir, row["cell"]), published_cell(stage, row["cell"])
            os.makedirs(dest)
            for name in CELL_FILES:
                if os.path.isdir(os.path.join(src, name)):
                    shutil.copytree(os.path.join(src, name), os.path.join(dest, name))
                elif os.path.isfile(os.path.join(src, name)):
                    shutil.copyfile(os.path.join(src, name), os.path.join(dest, name))
        files = published_hidden_files(stage, plan, exp["tasks"])
        dest = os.path.join(out, "reproduce")
        if os.path.isdir(dest):
            os.rename(dest, os.path.join(work, "previous"))
        try:
            os.rename(stage, dest)
        except OSError:
            if os.path.isdir(os.path.join(work, "previous")):
                os.rename(os.path.join(work, "previous"), dest)
            raise
        old_sha = common.sha256_file(os.path.join(out, "PLAN.json"))
        plan["publication"] = {"closed": True, "closed_at": plan.get("publication", {}).get("closed_at") or now_utc(), "files": files}
        common.write_json(os.path.join(out, "PLAN.json"), plan)
        rebind_records(out, old_sha, common.sha256_file(os.path.join(out, "PLAN.json")))
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main(argv=None):
    p = argparse.ArgumentParser(description="Export a graded lane run as a kogen-bench round.")
    p.add_argument("run_dir")
    p.add_argument("--round-id", required=True)
    p.add_argument("--out", required=True, help="<kogen-bench>/rounds/<round id>")
    p.add_argument("--tasks", default=os.environ.get("KOGEN_LANES_TASKS"), help="private tasks folder (--publish-private)")
    p.add_argument("--date", help="round date (YYYY-MM-DD, default today UTC)")
    p.add_argument("--no-register", action="store_true", help="do not touch rounds/STATUS.md, index.json, README.md, round-inventory.json")
    p.add_argument("--check", choices=("release", "round", "none"), default="release",
                   help="release: validate_release.py --strict (whole checkout, slow); round: validate_round.py --strict")
    p.add_argument("--publish-private", action="store_true", help="after the round closes: copy private inputs and check the PLAN hashes")
    a = p.parse_args(argv)
    try:
        if a.publish_private:
            if not a.tasks:
                p.error("--tasks or KOGEN_LANES_TASKS is required")
            publish_private(a.run_dir, a.out, a.tasks)
            return 0
        return 0 if export(a.run_dir, a.round_id, a.out, a.date, not a.no_register, a.check) == 0 else 1
    except (ExportError, plan_hashes.PlanError, OSError, ValueError) as e:
        print(f"export: {e}", file=sys.stderr)
        return getattr(e, "code", 1)


if __name__ == "__main__":
    sys.exit(main())
