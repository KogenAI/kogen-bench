#!/usr/bin/env python3
"""Count descriptive audit signals in Codex JSONL run logs."""

import ipaddress
import json
import re
import sys
from urllib.parse import urlsplit


COUNT_FIELDS = ("web_search", "cmd_fetch", "cmd_url", "cmd_hidden_source")
HIDDEN_SOURCE_RE = re.compile(
    r"github\.com|githubusercontent|codeload\.github|kogen-bench|gitlab\.com|bitbucket\.org",
    re.IGNORECASE,
)
HTTP_URL_RE = re.compile(r"https?://[^\s\"'<>`]+", re.IGNORECASE)
GIT_URL_RE = re.compile(r"(?:https?://[^\s\"'<>`]+|git@[^\s\"'<>`]+|ssh://[^\s\"'<>`]+)", re.IGNORECASE)
GIT_ACTION_RE = re.compile(
    r"\bgit\b(?:(?!\bgit\b).)*?\b(clone|fetch|pull|ls-remote)\b|"
    r"\bgit\b(?:(?!\bgit\b).)*?\bsubmodule\b|"
    r"\bgit\b(?:(?!\bgit\b).)*?\bremote\s+add\b",
    re.IGNORECASE,
)


def _url_host(url):
    """Return a URL's hostname, or None when the token is not a usable URL."""
    token = url.rstrip(".,;:!?)]}")
    try:
        parsed = urlsplit(token if "://" in token else "ssh://" + token)
        return parsed.hostname
    except ValueError:
        return None


def _is_loopback_host(host):
    if not host:
        return False
    host = host.rstrip(".").lower()
    if host == "localhost" or host == "0.0.0.0":
        return True
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return False
    return address.is_loopback or address.is_unspecified


def _command_counts(command):
    http_hosts = [
        _url_host(match.group(0)) for match in HTTP_URL_RE.finditer(command)
    ]
    non_loopback_http = any(host and not _is_loopback_host(host) for host in http_hosts)
    cmd_url = int(non_loopback_http)

    # A shell wrapper such as bash -lc 'curl ...' still contains the invoked
    # command. Restrict this signal to command-name tokens and pair it with a
    # non-loopback HTTP URL.
    has_transfer = re.search(r"\b(?:curl|wget)\b", command, re.IGNORECASE) is not None
    cmd_fetch = has_transfer and non_loopback_http

    if GIT_ACTION_RE.search(command):
        for match in GIT_URL_RE.finditer(command):
            host = _url_host(match.group(0))
            if host and not _is_loopback_host(host):
                cmd_fetch = True
                break

    return int(cmd_fetch), cmd_url, int(HIDDEN_SOURCE_RE.search(command) is not None)


def _walk_dicts(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_dicts(child)


def _dedupe_item_events(events):
    """For item lifecycle pairs, retain completion, otherwise first start."""
    chosen = []
    by_id = {}
    for event in events:
        if not isinstance(event, dict):
            chosen.append(event)
            continue
        item = event.get("item")
        lifecycle = event.get("type")
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            chosen.append(event)
            continue
        if lifecycle not in ("item.started", "item.completed"):
            chosen.append(event)
            continue
        item_id = item["id"]
        if item_id not in by_id:
            by_id[item_id] = len(chosen)
            chosen.append(event)
        elif lifecycle == "item.completed":
            chosen[by_id[item_id]] = event
    return chosen


def _run_counts(path):
    counts = {field: 0 for field in COUNT_FIELDS}
    counts["unparsable"] = 0
    counts["output_mentions_github"] = 0
    events = []
    try:
        with open(path, "r", encoding="utf-8") as stream:
            for line in stream:
                try:
                    events.append(json.loads(line))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    counts["unparsable"] += 1
    except FileNotFoundError:
        return None

    for event in _dedupe_item_events(events):
        for node in _walk_dicts(event):
            event_type = node.get("type")
            if isinstance(event_type, str) and "web_search" in event_type.lower():
                counts["web_search"] += 1

        item = event.get("item") if isinstance(event, dict) else None
        if not isinstance(item, dict) or item.get("type") != "command_execution":
            continue
        command = item.get("command")
        if isinstance(command, str):
            fetch, url, hidden = _command_counts(command)
            counts["cmd_fetch"] += fetch
            counts["cmd_url"] += url
            counts["cmd_hidden_source"] += hidden
        output = item.get("aggregated_output")
        if isinstance(output, str) and "github.com" in output.lower():
            counts["output_mentions_github"] += 1

    counts["flagged"] = sum(counts[field] for field in COUNT_FIELDS)
    return counts


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) < 2:
        print("usage: audit_cell.py RESULTS_DIR RUN_ID...", file=sys.stderr)
        return 2
    results_dir, *run_ids = argv
    for run_id in run_ids:
        counts = _run_counts(f"{results_dir}/{run_id}/codex.jsonl")
        result = {"run_id": run_id}
        if counts is None:
            result["missing"] = True
        else:
            result.update(counts)
        print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
