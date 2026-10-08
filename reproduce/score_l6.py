#!/usr/bin/env python3
"""Score blinded L6 auditor verdicts using standard-library statistics."""

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

Z_95 = 1.959963984540054


def proportion_interval(successes, n):
    if n == 0:
        return None
    p = successes / n
    z2 = Z_95 * Z_95
    den = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / den
    half = Z_95 * math.sqrt((p * (1.0 - p) / n) + (z2 / (4.0 * n * n))) / den
    return [max(0.0, center - half), min(1.0, center + half)]


def integer(value):
    if value is None or value == "":
        return 0
    result = int(value)
    if result < 0:
        raise ValueError("token counts must be nonnegative")
    return result


def load_cases(path):
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    cases = {}
    for row in rows:
        case_id = row["blind_id"]
        outcome = row["outcome"].strip().lower()
        if case_id in cases or outcome not in ("pass", "fail"):
            raise ValueError("case list must have unique IDs and pass/fail outcomes")
        cases[case_id] = outcome
    return cases


def score(case_path, calls_path):
    cases = load_cases(case_path)
    grouped = defaultdict(list)
    seen = set()
    with calls_path.open(newline="") as stream:
        for row in csv.DictReader(stream):
            case_id = row["blind_id"]
            model = row["model"].strip()
            if case_id not in cases:
                raise ValueError("call refers to an unknown blind case")
            key = (model, case_id)
            if key in seen:
                raise ValueError("more than one call recorded for a model and case")
            seen.add(key)
            verdict = row.get("verdict", "").strip().lower()
            malformed = str(row.get("malformed", "")).strip().lower() in ("1", "true", "yes")
            if verdict not in ("veto", "allow"):
                malformed = True
                verdict = "allow"  # invalid output does not trigger a demotion
            grouped[model].append({
                "blind_id": case_id,
                "outcome": cases[case_id],
                "veto": verdict == "veto",
                "malformed": malformed,
                "tool_events": integer(row.get("tool_events")),
                "uncached": integer(row.get("uncached_input_tokens")),
                "cached": integer(row.get("cached_input_tokens")),
                "output": integer(row.get("output_tokens")),
            })

    results = {}
    for model, rows in sorted(grouped.items()):
        tp = fp = fn = tn = malformed = tool_events = 0
        tokens = Counter()
        for row in rows:
            bad = row["outcome"] == "fail"
            veto = row["veto"]
            if bad and veto:
                tp += 1
            elif not bad and veto:
                fp += 1
            elif bad:
                fn += 1
            else:
                tn += 1
            malformed += row["malformed"]
            tool_events += row["tool_events"]
            for key in ("uncached", "cached", "output"):
                tokens[key] += row[key]

        precision_n = tp + fp
        recall_n = tp + fn
        good_n = fp + tn
        precision = tp / precision_n if precision_n else None
        recall = tp / recall_n if recall_n else None
        false_dem = fp / good_n if good_n else None
        eligible = (
            len(rows) == len(cases)
            and precision is not None
            and false_dem is not None
            and tool_events == 0
            and precision >= 0.90
            and false_dem <= 0.05
        )
        results[model] = {
            "calls": len(rows),
            "cases_expected": len(cases),
            "invalid_responses": malformed,
            "tool_events": tool_events,
            "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "veto_precision": precision,
            "veto_precision_wilson95": proportion_interval(tp, precision_n),
            "recall": recall,
            "recall_wilson95": proportion_interval(tp, recall_n),
            "false_demotion_rate_good": false_dem,
            "false_demotion_wilson95": proportion_interval(fp, good_n),
            "tokens": {
                "uncached_input": tokens["uncached"],
                "cached_input": tokens["cached"],
                "output": tokens["output"],
                "total": sum(tokens.values()),
            },
            "automatic_demotion_eligible_by_preregistered_point_targets": eligible,
            "recommendation": "automatic_demotion_eligible_by_replay_rule" if eligible else "advisory_only",
        }
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=Path("case_list.csv"))
    parser.add_argument("--calls", type=Path, default=Path("calls.csv"))
    args = parser.parse_args()
    print(json.dumps(score(args.cases, args.calls), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
