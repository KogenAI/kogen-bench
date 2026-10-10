"""Command line for the conformance runner."""

from __future__ import annotations

import argparse
import json
import math
import sys

from . import __version__
from .runner import CaseError, load_cases, run_cases, summary
from .quint_runner import QuintInputError, generate_traces


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kogen-conformance")
    parser.add_argument("--version", action="version", version=f"kogen-conformance {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    gen = commands.add_parser("gen", help="generate seeded Quint ITF trace cases")
    gen.add_argument("--model", required=True, metavar="FILE.QNT")
    gen.add_argument("--seed", required=True, type=int)
    gen.add_argument("--traces", required=True, type=int)
    gen.add_argument("--steps", required=True, type=int)
    gen.add_argument("--out", required=True, metavar="DIR")
    gen.add_argument("--kogen", metavar="PATH", help="binary metadata source (default: ../core/target/release/kogen)")
    gen.add_argument("--main", metavar="MODULE", help="Quint main module (defaults to the module in --model)")
    gen.add_argument("--profile", default="fast")
    gen.add_argument("--clause", action="append", default=[], help="owned clause id; may be repeated")
    gen.add_argument("--witness", action="append", default=[], help="witness name; may be repeated")
    gen.add_argument("--script", action="append", default=[], metavar="ID=JSON", help="provider script envelope; may be repeated")
    gen.add_argument("--fixture", action="append", default=[], metavar="NAME=FILE", help="fixture byte template; may be repeated")
    gen.add_argument("--fixtures", action="append", default=[], metavar="FILE", help="provider fixture map (JSON object of id to script envelope); may be repeated")
    gen.add_argument("--quint-timeout", type=int, default=180, help="generation timeout per trace in seconds")
    gen.add_argument("--jobs", type=int, default=3, help="maximum concurrent Quint traces (1-3; default: 3)")
    gen.add_argument("--retry-vacuous", type=int, default=0,
                     help="bounded extra seeds per trace when no asserted non-version CLI command is generated")

    run = commands.add_parser("run", help="run black-box conformance cases")
    run.add_argument("--kogen", required=True, metavar="PATH", help="Kogen executable under test")
    run.add_argument("--case", metavar="GLOB", help="comma-separated case id or filename globs")
    run.add_argument("--jobs", type=int, default=1, help="number of cases to run concurrently (default: 1)")
    run.add_argument("-v", action="store_true", dest="verbose", help="show assertion failures")
    run.add_argument("--out", default="results.jsonl", help="JSON Lines result file (default: results.jsonl)")
    run.add_argument("--keep", action="store_true", help="preserve each per-case sandbox")
    run.add_argument("--workdir", default="/tmp", metavar="DIR",
                     help="root for all run temporary directories and final cwd sweep (default: /tmp)")
    run.add_argument("--time-scale", type=float, default=0.01,
                     help="default KOGEN_TIME_SCALE for cases that do not set one (default: 0.01)")
    run.add_argument("--timeout", type=float, default=60.0,
                     help="hard maximum seconds for each Kogen invocation (default: 60)")

    listing = commands.add_parser("list", help="list available cases")
    listing.add_argument("--case", metavar="GLOB", help="comma-separated case id or filename globs")

    summarize = commands.add_parser("summary", help="summarize a JSON Lines results file")
    summarize.add_argument("results", metavar="RESULTS.JSONL")
    summarize.add_argument("--json", action="store_true", help="print machine-readable JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "gen":
            paths = generate_traces(
                model=args.model, seed=args.seed, traces=args.traces, steps=args.steps,
                out=args.out, kogen=args.kogen, main=args.main, profile=args.profile,
                clause_ids=args.clause, witnesses=args.witness,
                script_args=args.script, fixture_args=args.fixture,
                fixture_map_args=args.fixtures, quint_timeout=args.quint_timeout, jobs=args.jobs,
                retry_vacuous=args.retry_vacuous,
            )
            for path in paths:
                print(path)
            return 0
        if args.command == "list":
            cases = load_cases(_split_patterns(args.case))
            for case in cases:
                print(f"{case['id']}\t{case.get('title', '')}\t{case['_file']}")
            return 0
        if args.command == "summary":
            report = summary(args.results)
            if args.json:
                print(json.dumps(report, indent=2, sort_keys=True))
            else:
                counts = report["counts"]
                print(f"cases: {report['total']}  pass: {counts['pass']}  fail: {counts['fail']}  error: {counts['error']}  blocked: {counts['blocked']}")
                for note in report.get("teardown_notes", []):
                    print(f"teardown: {note}")
                for status in ("fail", "error", "blocked"):
                    if report["ids"][status]:
                        print(f"{status}: {', '.join(report['ids'][status])}")
            return 0
        if args.jobs < 1:
            raise CaseError("--jobs must be a positive integer")
        if not math.isfinite(args.timeout) or args.timeout <= 0:
            raise CaseError("--timeout must be a positive finite number of seconds")
        cases = load_cases(_split_patterns(args.case))
        if not cases:
            raise CaseError("no cases selected")
        _results, exit_code = run_cases(
            cases, args.kogen, jobs=args.jobs, time_scale=args.time_scale,
            keep=args.keep, verbose=args.verbose, out_path=args.out, timeout_s=args.timeout,
            workdir=args.workdir,
        )
        report = summary(args.out)
        counts = report["counts"]
        print(f"\nsummary: {report['total']} cases; {counts['pass']} passed, {counts['fail']} failed, {counts['error']} errors, {counts['blocked']} blocked")
        for note in report.get("teardown_notes", []):
            print(f"teardown: {note}")
        print(f"results: {args.out}")
        return exit_code
    except (CaseError, QuintInputError, OSError, json.JSONDecodeError) as error:
        print(f"kogen-conformance: {error}", file=sys.stderr)
        return 2


def _split_patterns(value: str | None) -> list[str] | None:
    if not value:
        return None
    return [part.strip() for part in value.split(",") if part.strip()]
