#!/usr/bin/env python3
"""Frozen structural and keyed-value checker for LAB-01 outputs."""
import csv
from decimal import Decimal, InvalidOperation
import json
import math
from pathlib import Path
import struct
import sys
import xml.etree.ElementTree as ET

LANGS = {"Elixir", "Go"}
CONDS = set("ABCD")
HOSTS = {"studio", "macbook"}
SPEC = {
    "tables.csv": {
        "header": ["language", "condition", "studio_final", "macbook_final", "median", "spread", "median_minus_A"],
        "key": ("language", "condition"),
        "keys": {(lang, cond) for lang in LANGS for cond in CONDS},
        "cells": ["studio_final", "macbook_final", "median", "spread", "median_minus_A"],
        "integer": {"studio_final", "macbook_final", "spread"},
        "empty": lambda row, field: field == "median_minus_A" and row["condition"] == "A",
        "total": 40,
    },
    "bootstrap.csv": {
        "header": ["language", "condition", "stat", "lo", "hi"],
        "key": ("language", "condition", "stat"),
        "keys": {(lang, cond, stat) for lang in LANGS for cond in CONDS for stat in
                 (("median",) if cond == "A" else ("median", "paired_diff_vs_A"))},
        "cells": ["lo", "hi"], "integer": set(),
        "empty": lambda row, field: False, "total": 28,
    },
    "token_cost.csv": {
        "header": ["language", "condition", "host", "total_tokens", "final", "tokens_per_case"],
        "key": ("language", "condition", "host"),
        "keys": {(lang, cond, host) for lang in LANGS for cond in CONDS for host in HOSTS},
        "cells": ["total_tokens", "final", "tokens_per_case"],
        "integer": {"total_tokens", "final", "tokens_per_case"},
        "empty": lambda row, field: False, "total": 48,
    },
    "plot_data.csv": {
        "header": ["language", "condition", "host", "final", "total_tokens_millions"],
        "key": ("language", "condition", "host"),
        "keys": {(lang, cond, host) for lang in LANGS for cond in CONDS for host in HOSTS},
        "cells": ["final", "total_tokens_millions"],
        "integer": {"final"}, "empty": lambda row, field: False, "total": 32,
    },
}


def valid_labels(row, filename):
    if row.get("language") not in LANGS or row.get("condition") not in CONDS:
        return False
    if filename in ("token_cost.csv", "plot_data.csv") and row.get("host") not in HOSTS:
        return False
    if filename == "bootstrap.csv" and row.get("stat") not in {"median", "paired_diff_vs_A"}:
        return False
    return True


def number(value):
    try:
        result = Decimal(value)
    except (InvalidOperation, ValueError):
        return None
    if not result.is_finite():
        return None
    return result


def read_csv(path, config, filename):
    structural = True
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            header = reader.fieldnames
            rows = list(reader)
    except (OSError, UnicodeError, csv.Error):
        return False, []
    if header != config["header"] or len(rows) != len(config["keys"]):
        structural = False
    keys = []
    for row in rows:
        if None in row or not valid_labels(row, filename):
            structural = False
            continue
        key = tuple(row.get(field, "") for field in config["key"])
        keys.append(key)
        if any(field not in row for field in config["header"]):
            structural = False
        for field in config["cells"]:
            raw = row.get(field)
            if config["empty"](row, field):
                if raw != "":
                    # A's delta is specified empty. A nonempty numeric field is
                    # rejected as a structural-contract violation.
                    structural = False
                continue
            parsed = number(raw or "")
            if parsed is None:
                structural = False
            elif field in config["integer"] and parsed != parsed.to_integral_value():
                structural = False
    if len(keys) != len(set(keys)) or set(keys) != config["keys"]:
        structural = False
    return structural, rows


def compare_csv(out_path, expected_path, filename, config):
    out_ok, out_rows = read_csv(out_path, config, filename)
    exp_ok, exp_rows = read_csv(expected_path, config, filename)
    structural = out_ok and exp_ok
    total = config["total"]
    if not structural:
        return {"structural_ok": False, "cells_correct": 0, "cells_total": total}
    by_key = {tuple(row[k] for k in config["key"]): row for row in exp_rows}
    correct = 0
    for row in out_rows:
        key = tuple(row[k] for k in config["key"])
        ref = by_key[key]
        for field in config["cells"]:
            value, target = row[field], ref[field]
            if config["empty"](row, field):
                matches = value == target == ""
            else:
                a, b = number(value), number(target)
                if a is None or b is None:
                    matches = False
                elif field in config["integer"]:
                    matches = a == b and a == a.to_integral_value()
                else:
                    matches = abs(a - b) <= Decimal("0.001")
            correct += int(matches)
    return {"structural_ok": True, "cells_correct": correct, "cells_total": total}


def plot_file_ok(out_dir):
    png = out_dir / "token_cost.png"
    if png.is_file():
        try:
            raw = png.read_bytes()
            if len(raw) < 24 or raw[:8] != b"\x89PNG\r\n\x1a\n" or raw[12:16] != b"IHDR":
                return False
            width, height = struct.unpack(">II", raw[16:24])
            return width >= 300 and height >= 200
        except OSError:
            return False
    svg = out_dir / "token_cost.svg"
    if not svg.is_file():
        return False
    try:
        root = ET.parse(svg).getroot()
        if root.tag.split("}")[-1] != "svg":
            return False
        markers = 0
        for element in root.iter():
            tag = element.tag.split("}")[-1].lower()
            cls = (element.attrib.get("class", "") + " " + element.attrib.get("data-marker", "")).lower()
            if tag in {"circle", "ellipse"} or "marker" in cls:
                markers += 1
        return markers >= 16
    except (ET.ParseError, OSError):
        return False


def check(out_dir, expected_dir):
    out_dir, expected_dir = Path(out_dir), Path(expected_dir)
    results = {name: compare_csv(out_dir / name, expected_dir / name, name, config)
               for name, config in SPEC.items()}
    plot_ok = plot_file_ok(out_dir)
    numbers_correct = all(item["structural_ok"] and item["cells_correct"] == item["cells_total"]
                          for item in results.values())
    return {"files": results, "plot_file_ok": plot_ok,
            "plot_semantic_ok": None, "numbers_correct": numbers_correct}


def main(argv):
    if len(argv) != 3:
        raise SystemExit("usage: check.py OUT_DIR EXPECTED_DIR")
    print(json.dumps(check(argv[1], argv[2]), sort_keys=True))


if __name__ == "__main__":
    main(sys.argv)
