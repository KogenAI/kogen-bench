#!/usr/bin/env python3
"""Offline scored-suite lint and conservative command/outcome contradiction audit.

Key: command family + semantic outcome for questions, deadline, tamper, timeout
and rejected hooks. Otherwise use normalized exact argv + non-exit expectation
+ prior stimulus (setup operations and earlier commands, excluding all exits).
Normalization removes capture names, slugs and sandbox roots, never fixture
bytes. The conservative fallback avoids equating commands in different states.
This checks encoded expectations; it does not prove runtime satisfiability.
"""
import argparse
from collections import defaultdict
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'conformance'))
from kogen_conformance.runner import load_cases
from kogen_conformance.quint_runner import decode_itf, Variant, ITFMap, _plain
from kogen_conformance.gherkin_runner import _script_fixture

ALLOWED = {'/model', '/reasoning/effort'}
HEX = re.compile(r'(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])')


def plain(value):
    return _plain(value)


def walk(value):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def request_lint(value):
    errors = set()
    for node in walk(value):
        if not isinstance(node, dict):
            continue
        if {'method', 'headers', 'equals', 'present'} <= set(node):
            extra = (set(node['equals']) | set(node['present'])) - ALLOWED
            if extra or node['headers']:
                errors.add('request assertions beyond model/effort: ' + ','.join(sorted(extra)))
        if 'expect' in node and isinstance(node['expect'], dict):
            expected = node['expect']
            if 'body' in expected or 'role' in expected or 'headers' in expected:
                body = expected.get('body', {})
                if set(expected) - {'body'} or set(body) - {'model', 'reasoning'} or set(body.get('reasoning', {})) - {'effort'}:
                    errors.add('legacy request assertion beyond model/effort')
        if any(k in node for k in ('provider_expect', 'provider_oauth_expect', 'provider_requests')):
            errors.add('legacy provider request observation')
    return sorted(errors)


def without_exit(value):
    if isinstance(value, dict):
        return {k: without_exit(v) for k, v in value.items() if k not in {'exit', 'exitCode'}}
    if isinstance(value, list):
        return [without_exit(v) for v in value]
    return value


def canonical(value):
    text = json.dumps(without_exit(plain(value)), sort_keys=True, ensure_ascii=False)
    return re.sub(r'\$\{(?:capture|prefix):[^}]+\}|\{\{[^}]+\}\}', '<capture>', text)


def semantic(command, text):
    text = text.lower()
    if command[:2] == ['intent', 'shape'] and ('questions' in text or 'branching' in text):
        return 'questions-only'
    if command[:2] == ['queue', 'start']:
        if 'deadline' in text or 'budget-exhaust' in text:
            return 'deadline-expired'
        if 'tamper' in text or 'changed-tree' in text:
            return 'candidate-tampered'
        if 'hook' in text and ('denied' in text or 'reject' in text):
            return 'hook-rejected'
        if 'could-not-check' in text:
            return 'check-timeout'
    return None


def audit(cases):
    violations = {}; buckets = defaultdict(list); assertions = 0
    for case in cases:
        cid = case['id']; errors = []
        if case.get('_kind') == 'quint':
            manifest = case['_manifest']
            errors += request_lint(manifest['scripts'])
            trace = decode_itf(json.loads(Path(case['_itf']).read_text()))
            steps = [plain(step) for state in trace['states'] for step in state[manifest['last_step_var']]]
            history = []
            for step in steps:
                data = step.get('value', {})
                if step.get('tag') == 'Cli':
                    cmd = data['cmd']; argv = cmd['argv']; expected = data['expect']
                    approval_text = canonical({'cmd': cmd, 'expect': expected})
                    if argv[:2] == ['intent', 'approve'] or 'SHA-256:' in approval_text:
                        if HEX.search(approval_text): errors.append('literal 64-hex approval hash')
                    observed = expected['exitCode']
                    if observed['tag'] == 'Observe':
                        context = canonical(history + [cmd, expected])
                        outcome = semantic(argv, context)
                        key = (tuple(argv[:2]), outcome) if outcome else (tuple(argv), canonical(expected), canonical(history + [cmd]))
                        buckets[key].append((cid, observed['value'])); assertions += 1
                history.append(step)
        elif case.get('_kind') == 'gherkin':
            steps = case['_feature_steps']; context = []; argv = None
            import shlex
            for step in steps:
                text = step['text']; context.append(step)
                match = re.search(r'fake provider script "([^"]+)"', text)
                if match:
                    script, contract = _script_fixture(match.group(1));errors += request_lint(script)
                    if set(contract) - {'min','max','model','effort'}:errors.append('Gherkin request contract beyond model/effort')
                match = re.match(r'I run "([^"]+)"', text)
                if match: argv = shlex.split(match.group(1))[1:]
                match = re.fullmatch(r'the exit code is (\d+)', text)
                if match and argv:
                    outcome = semantic(argv, case['title'] + canonical(context))
                    key = (tuple(argv[:2]), outcome) if outcome else (tuple(argv), canonical(context[:-1]))
                    buckets[key].append((cid, int(match.group(1)))); assertions += 1
                if HEX.search(text) and ('approve' in text or 'hash' in text):errors.append('literal 64-hex approval hash')
        else:
            data = json.loads((ROOT.parent / 'conformance' / case['_file']).read_text());errors += request_lint(data)
            for index, step in enumerate(data['steps']):
                argv = step.get('argv', []); expect = step.get('expect', {})
                if argv[:2] == ['intent','approve'] and HEX.search(canonical(step)):errors.append('literal 64-hex approval hash')
                if 'exit' in expect:
                    key = (tuple(argv), canonical(expect), canonical(data['steps'][:index] + [{k:v for k,v in data.items() if k != 'steps'}]))
                    buckets[key].append((cid, expect['exit'])); assertions += 1
        if errors: violations[cid] = sorted(set(errors))
    conflicts = []
    for key, rows in buckets.items():
        if len({code for cid,code in rows}) > 1:
            conflicts.append({'key': repr(key), 'cases': sorted(set(rows))})
            for cid,code in rows:
                violations.setdefault(cid, []).append('contradictory expected exit for same command + outcome')
    return {'scored_cases': len(cases), 'exit_assertions': assertions, 'lint_and_conflict_cases': violations, 'conflicts': conflicts, 'coarse_key': __doc__}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exclude-offenders', action='store_true')
    args = parser.parse_args()
    all_cases = load_cases()
    excluded = dict(line.split('\t', 1) for line in (ROOT/'EXCLUDED-V2.txt').read_text().splitlines())
    report = audit([c for c in all_cases if c['id'] not in excluded])
    if args.exclude_offenders:
        for cid, reasons in report['lint_and_conflict_cases'].items():
            excluded[cid] = '; '.join(reasons)
        (ROOT/'EXCLUDED-V2.txt').write_text(''.join(f'{cid}\t{reason}\n' for cid,reason in sorted(excluded.items())))
        (ROOT/'SPEC-BUG-CASES.txt').write_text('\n'.join(sorted(excluded))+'\n')
    (ROOT/'SUITE-CHECKS.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'coarse_key'}, indent=2))
    return bool(report['lint_and_conflict_cases']) and not args.exclude_offenders

if __name__ == '__main__':
    raise SystemExit(main())
