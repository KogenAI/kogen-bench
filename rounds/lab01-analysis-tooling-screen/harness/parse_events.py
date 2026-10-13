#!/usr/bin/env python3
"""Extract shell proxies, edit IDs and cumulative usage from Codex JSON events."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys

FIELDS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens", "total_tokens")
SESSION_META = re.compile(r'(?<!\\)"type"\s*:\s*"session_meta"')
TOKEN_EVENT = re.compile(r'(?<!\\)"type"\s*:\s*"token_count"')
RUN_SH = re.compile(r"(?:^|[\s/])(?:\./)?run\.sh(?:\s|$)", re.I)
DOWNLOAD_COMMAND = re.compile(
    r"\b(?:uv\s+(?:sync|lock|add|pip)|mix\s+(?:deps(?:\.get|\.compile|\.update)?|local\.(?:hex|rebar))|go\s+mod\s+(?:download|tidy))\b",
    re.I,
)


def parse_time(value):
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def stream_events(paths):
    for path in paths:
        try:
            with path.open(errors="replace") as stream:
                for line in stream:
                    try:
                        yield path.name, json.loads(line)
                    except ValueError:
                        continue
        except OSError:
            continue


def command_metrics(paths):
    commands = {}
    edits = {}
    for filename, row in stream_events(paths):
        if not isinstance(row, dict):
            continue
        kind = row.get("type")
        item = row.get("item") or {}
        if not isinstance(item, dict):
            continue
        item_type = str(item.get("type", "")).lower()
        item_id = item.get("id")
        key = (filename, str(item_id)) if item_id is not None else (filename, json.dumps(item, sort_keys=True))
        if item_type == "command_execution":
            command = item.get("command") or ""
            record = commands.setdefault(key, {"command": command, "completed": False, "exit_code": None,
                                                "started_at": None, "completed_at": None,
                                                "duration_ms": None, "event_id": item_id})
            if command:
                record["command"] = command
            timestamp = row.get("timestamp")
            if kind == "item.started" and record["started_at"] is None:
                record["started_at"] = timestamp
            if kind == "item.completed":
                record["completed"] = True
                record["exit_code"] = item.get("exit_code")
                record["completed_at"] = timestamp
                duration = item.get("duration_ms")
                if type(duration) in (int, float) and duration >= 0:
                    record["duration_ms"] = float(duration)
        is_edit = (item_type in {"file_change", "file_edit", "apply_patch", "patch", "patch_apply"}
                   or (isinstance(item.get("changes"), list) and "command" not in item))
        if is_edit:
            edit_key = (filename, str(item_id)) if item_id is not None else (filename, json.dumps(item, sort_keys=True))
            record = edits.setdefault(edit_key, {"event_id": item_id or f"{filename}:unknown",
                                                  "source_file": filename,
                                                  "turn_id": row.get("turn_id"),
                                                  "type": item_type or "file_change",
                                                  "paths": set(), "timestamp": row.get("timestamp")})
            for change in item.get("changes", []) if isinstance(item.get("changes"), list) else []:
                if isinstance(change, dict):
                    path = change.get("path") or change.get("file_path")
                    if path:
                        record["paths"].add(str(path))
            path = item.get("path") or item.get("file_path")
            if path:
                record["paths"].add(str(path))
    nonzero, run_attempts = 0, 0
    download_durations = []
    for record in commands.values():
        if RUN_SH.search(record["command"]):
            run_attempts += 1
        code = record["exit_code"]
        if record["completed"] and isinstance(code, int) and code != 0:
            nonzero += 1
        elif record["completed"] and isinstance(code, str) and re.fullmatch(r"-?\d+", code) and int(code) != 0:
            nonzero += 1
        if DOWNLOAD_COMMAND.search(record["command"]):
            duration_s = record["duration_ms"] / 1000 if record["duration_ms"] is not None else None
            if duration_s is None and record["started_at"] and record["completed_at"]:
                start, end = parse_time(record["started_at"]), parse_time(record["completed_at"])
                if start is not None and end is not None and end >= start:
                    duration_s = (end - start).total_seconds()
            download_durations.append({"event_id": record["event_id"], "command": record["command"],
                                       "start": record["started_at"], "end": record["completed_at"],
                                       "duration_s": duration_s,
                                       "evidence": "explicit package-manager fetch/install command"})
    edit_rows = []
    for record in edits.values():
        edit_rows.append({"event_id": record["event_id"], "source_file": record["source_file"],
                          "turn_id": record["turn_id"],
                          "type": record["type"], "paths": sorted(record["paths"]),
                          "timestamp": record["timestamp"]})
    edit_rows.sort(key=lambda item: (str(item["timestamp"]), str(item["event_id"])))
    return nonzero, run_attempts, edit_rows, download_durations


def token_usage(paths, session_dir, workspace, cutoff):
    ids = set()
    for path in paths:
        try:
            with path.open(errors="replace") as stream:
                for line in stream:
                    try:
                        row = json.loads(line)
                    except ValueError:
                        continue
                    if not isinstance(row, dict) or row.get("type") != "thread.started":
                        continue
                    tid = row.get("thread_id")
                    if isinstance(tid, str) and re.fullmatch(r"[A-Za-z0-9_-]+", tid):
                        ids.add(tid)
        except OSError:
            continue
    no_data = {field: "NA" for field in FIELDS}
    if not ids:
        return {"available": False, "reason": "no thread.started IDs", "thread_ids": [],
                "threads": [], "totals": no_data, "cutoff": cutoff.isoformat()}

    session_dir = Path(session_dir)
    selected_threads = []
    errors = []
    for thread_id in sorted(ids):
        matches = list(session_dir.rglob(f"*{thread_id}*.jsonl")) if session_dir.is_dir() else []
        if len(matches) != 1:
            errors.append(f"{thread_id}: rollout match count {len(matches)}")
            continue
        meta = None
        selected = None
        previous = None
        out_of_order = False
        try:
            with matches[0].open(errors="replace") as stream:
                for line in stream:
                    if SESSION_META.search(line):
                        try:
                            row = json.loads(line)
                            if not isinstance(row, dict):
                                continue
                            payload = row.get("payload") or {}
                            if not isinstance(payload, dict):
                                continue
                            meta = {key: payload.get(key) for key in ("id", "cwd")}
                        except ValueError:
                            continue
                    elif TOKEN_EVENT.search(line):
                        try:
                            row = json.loads(line)
                        except ValueError:
                            continue
                        if not isinstance(row, dict):
                            continue
                        when = parse_time(row.get("timestamp"))
                        payload = row.get("payload") or {}
                        if not isinstance(payload, dict):
                            continue
                        info = payload.get("info") or {}
                        if not isinstance(info, dict):
                            continue
                        values = info.get("total_token_usage")
                        if when is None or not isinstance(values, dict):
                            continue
                        if previous is not None and when < previous:
                            out_of_order = True
                        previous = when
                        if when > cutoff:
                            continue
                        if selected is None or when >= selected[0]:
                            selected = (when, row.get("timestamp"), {field: values.get(field) for field in FIELDS})
        except OSError:
            errors.append(f"{thread_id}: rollout unreadable")
            continue
        if not meta or meta.get("id") != thread_id or meta.get("cwd") != str(workspace):
            errors.append(f"{thread_id}: session metadata mismatch")
            continue
        if selected is None:
            errors.append(f"{thread_id}: no eligible token count")
            continue
        if out_of_order:
            errors.append(f"{thread_id}: token timestamps out of order")
            continue
        usage = {}
        for field in FIELDS:
            value = selected[2].get(field)
            usage[field] = value if type(value) is int and value >= 0 else "NA"
            if usage[field] == "NA":
                errors.append(f"{thread_id}: missing or invalid {field}")
        if all(type(usage[field]) is int for field in FIELDS):
            if usage["total_tokens"] != usage["input_tokens"] + usage["output_tokens"]:
                errors.append(f"{thread_id}: total_tokens invariant failed")
            if usage["cached_input_tokens"] > usage["input_tokens"]:
                errors.append(f"{thread_id}: cached input invariant failed")
            if usage["reasoning_output_tokens"] > usage["output_tokens"]:
                errors.append(f"{thread_id}: reasoning invariant failed")
        selected_threads.append({"thread_id": thread_id, "last_token_event_ts": selected[1], "usage": usage})

    available = not errors and len(selected_threads) == len(ids)
    totals = {}
    for field in FIELDS:
        values = [item["usage"][field] for item in selected_threads]
        totals[field] = sum(values) if available and values and all(type(value) is int for value in values) else "NA"
    return {"available": available, "reason": "" if available else "; ".join(errors),
            "thread_ids": sorted(ids), "threads": selected_threads, "totals": totals,
            "cutoff": cutoff.isoformat()}


def parse(events_path, session_dir, workspace, cutoff_text):
    cutoff = parse_time(cutoff_text)
    if cutoff is None:
        raise ValueError("cutoff must be an ISO-8601 timestamp")
    path = Path(events_path)
    event_paths = sorted(path.glob("turn-*.jsonl")) if path.is_dir() else [path]
    nonzero, run_attempts, edits, download_durations = command_metrics(event_paths)
    usage = token_usage(event_paths, session_dir, workspace, cutoff)
    return {"nonzero_shell_events": nonzero, "run_sh_attempts": run_attempts,
            "edit_events": edits, "dependency_download_durations": download_durations,
            "token_usage": usage}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("events", help="Codex --json JSONL file or directory of turn JSONL files")
    parser.add_argument("--session-dir", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--cutoff", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    result = parse(args.events, args.session_dir, args.workspace, args.cutoff)
    body = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(body, encoding="utf-8")
    else:
        sys.stdout.write(body)


if __name__ == "__main__":
    main()
