"""Durable, paired approval debt. The immutable experiment and cell set never shrink."""

import datetime
import os
import re
import shutil

from . import common


def records(run_dir):
    path = os.path.join(run_dir, "PLAN.json")
    return common.read_json(path).get("approval_deferrals", {}) if os.path.isfile(path) else {}


def pending(run_dir):
    return {t for t, r in records(run_dir).items() if r["state"] == "pending"}


def record(run_dir, task, results, stage):
    path = os.path.join(run_dir, "PLAN.json")
    plan = common.read_json(path) if os.path.isfile(path) else {}
    debt = plan.setdefault("approval_deferrals", {}).setdefault(task, {"attempts": []})
    debt["state"] = ("approved" if all(r["ok"] for r in results) else
                     "refused" if any(not r["ok"] and not r["timeout"] for r in results) else "pending")
    debt["lanes"] = [r["lane"] for r in results]
    debt["attempts"].append({"stage": stage, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                              "results": results})
    common.write_json(path, plan)


def gaps(run_dir):
    return [{"task": t, "lanes": r["lanes"], "reason": "approval_timeout" if r["state"] == "pending" else "approval_refused",
             "state": r["state"], "attempts": r["attempts"]}
            for t, r in sorted(records(run_dir).items()) if r["state"] != "approved"]


def save_refusal(run_dir, task, lane, calls, workspace, preflight=False):
    """Keep full approval streams, Kogen readiness reports and referenced reports/logs."""
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    name = f"{task}__{lane}__{stamp}"
    destinations = [os.path.join(run_dir, "approval-refusals")]
    if preflight:
        destinations.append(os.path.join(run_dir, "run-logs"))
    combined = []
    for i, call in enumerate(calls, 1):
        combined.append(f"=== approval invocation {i}; exit={call[0]} timed_out={call[1]} ===\n")
        combined.append("--- stdout ---\n" + call[2])
        combined.append("\n--- stderr ---\n" + (call[6] if len(call) > 6 else ""))
        combined.append("\n")
    content = "".join(combined)
    for dest in destinations:
        os.makedirs(dest, mode=0o700, exist_ok=True)
        os.chmod(dest, 0o700)
        path = os.path.join(dest, name + ".log")
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8", errors="replace") as f:
            f.write(content)
        report_dir = os.path.join(dest, name + ".reports")
        copied = []
        sources = []
        # Kogen stores its readiness report here even when the refusal text does not name the path.
        local_reports = os.path.join(workspace, ".kogen", "local")
        for root, dirs, names in os.walk(local_reports):
            dirs[:] = sorted(d for d in dirs if d in {"readiness", "reports", "logs"})
            for filename in sorted(names):
                source = os.path.join(root, filename)
                rel = os.path.relpath(source, workspace)
                parent = os.path.basename(root)
                if parent in {"readiness", "reports", "logs"} or filename.endswith(".log"):
                    sources.append((rel, source))
        refs = re.findall(r"(?im)\b(?:report|log)(?: file)?\s*[:=]\s*[\"']?([^\s\"',;]+)", content)
        for ref in refs:
            source = ref if os.path.isabs(ref) else os.path.join(workspace, ref)
            sources.append((ref, source))
        seen = set()
        for ref, source in sources:
            try:
                real = os.path.realpath(source)
                if real in seen or not os.path.isfile(real):
                    continue
                seen.add(real)
                target = os.path.join(report_dir, f"{len(copied)+1:02d}-{os.path.basename(real)}")
                os.makedirs(report_dir, mode=0o700, exist_ok=True)
                shutil.copy2(real, target)
                copied.append((ref, os.path.basename(target)))
            except OSError:
                continue
        if copied:
            with open(path, "a", encoding="utf-8") as f:
                f.write("\n=== copied Kogen report/log files ===\n")
                for ref, target in copied:
                    f.write(f"{ref} -> {os.path.basename(report_dir)}/{target}\n")
