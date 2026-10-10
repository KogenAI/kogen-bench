#!/usr/bin/env python3
"""Relax case request predicates and capture implementation-owned approval hashes."""
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COUNTS = Counter()
HASHES = {
    '408a1fa6a5be2dbe258f81763c937e0a35ec601f882b089dc558548f29b44095': 't1Approval',
    '2a2349d8f335f8a0dc25fcfc389301231aad278e90d7c5abca50814c613c2504': 't1Reapproval',
    '7055a12f019e28bdf2ba447284cd78b8a2e8ff70f0f178c10867c133ee9dae7b': 't1GitApproval',
}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def patch_scripts(value):
    if isinstance(value, list):
        for child in value:
            patch_scripts(child)
    elif isinstance(value, dict):
        if value.get('schema') == 1 and isinstance(value.get('turns'), list):
            COUNTS['script_envelopes_scanned'] += 1
            for turn in value['turns']:
                request = turn['request']
                kept = {k: v for k, v in request['equals'].items()
                        if k in {'/model', '/reasoning/effort'}}
                COUNTS['equals_assertions_removed'] += len(request['equals']) - len(kept)
                request['equals'] = kept
                COUNTS['header_assertions_removed'] += len(request['headers'])
                request['headers'] = {}
                present = [p for p in request['present'] if p in {'/model', '/reasoning/effort'}]
                COUNTS['presence_assertions_removed'] += len(request['present']) - len(present)
                request['present'] = present
            minimum, maximum = value['min_requests'], value['max_requests']
            if value['turns'] and minimum == 0:
                value['min_requests'] = minimum = 1
                COUNTS['minimums_raised'] += 1
            if minimum == maximum and value['turns']:
                value['max_requests'] = maximum + 2
                # Spare terminal responses permit a repair round without replaying
                # side-effecting tool calls or barrier gates from the fixture.
                spare = copy.deepcopy(value['turns'][-1])
                for chunk in spare['response']['chunks']:
                    chunk['gate'] = None
                value['turns'].extend([copy.deepcopy(spare), copy.deepcopy(spare)])
                COUNTS['exact_bounds_relaxed'] += 1
                COUNTS['spare_turns_added'] += 2
            elif minimum == maximum == 0:
                COUNTS['empty_no_call_envelopes'] += 1
            if 'digest' in value:
                bare = {k: v for k, v in value.items() if k != 'digest'}
                digest = hashlib.sha256(canonical(bare).encode()).hexdigest()
                if value['digest'] != digest:
                    COUNTS['script_digests_refreshed'] += 1
                value['digest'] = digest
            return
        for child in value.values():
            patch_scripts(child)


def unobserved():
    return {'tag': 'Unobserved', 'value': {'#tup': []}}


def review_step(step, name):
    review = copy.deepcopy(step)
    cmd = review['value']['cmd']
    cmd['argv'] = cmd['argv'][:3]
    slug = cmd['argv'][2]
    expect = review['value']['expect']
    for key in ('git', 'jsonRows', 'statusRows'):
        expect[key] = unobserved()
    for key in ('files', 'jsonFiles', 'timings'):
        expect[key] = {'#map': []}
    expect['relations'] = []
    expect['exitCode'] = {'tag': 'Observe', 'value': {'#bigint': '5'}}
    if slug == 'git-spec':
        title = 'Improve greeting'
        brief = 'The project README shows the new greeting.'
        acceptance = 'README.md contains the candidate greeting. (test domain=app)'
        base = '${buildBase}'
    else:
        title = 'Status fixture'
        brief = 'Change greeting.txt.'
        acceptance = 'greeting.txt says hello. (test)'
        base = '${capture:' + name + 'Base:oid}'
    lines = [f'Intent: {slug} — {title}', 'SHA-256: ${capture:' + name + ':hex}',
             'Approver: Kogen Suite', 'Base: main at ' + base, 'Feasibility: not checked',
             '', 'Brief', '  ' + brief, '', 'Acceptance', '  - [A1] ' + acceptance, '']
    if slug == 'git-spec':
        lines += ['Warning: configured checks are already red on the base:',
                  'Hint: fix the base first, or scope the check, e.g. a changed-files format argv.', '']
    lines += ['Approve with:', f'  kogen intent approve {slug} ' + '${prefix:' + name + ':8}']
    expect['stdoutLines'] = {'tag': 'Observe', 'value': [[line] for line in lines]}
    COUNTS['review_calls_inserted'] += 1
    return review


def replace_hashes(value):
    if isinstance(value, str):
        for digest, name in HASHES.items():
            if digest in value:
                COUNTS['full_hash_literals_replaced'] += value.count(digest)
                value = value.replace(digest, '${' + name + '}')
            if digest[:8] in value:
                COUNTS['prefix_hash_literals_replaced'] += value.count(digest[:8])
                value = value.replace(digest[:8], '${prefix:' + name + ':8}')
        return value
    if isinstance(value, list):
        return [replace_hashes(v) for v in value]
    if isinstance(value, dict):
        return {k: replace_hashes(v) for k, v in value.items()}
    return value


def patch_approvals(data):
    for state in data.get('states', []):
        steps = state.get('lastStep', [])
        expanded = []
        for step in steps:
            if step.get('tag') == 'Cli':
                argv = step['value']['cmd']['argv']
                if argv[:2] == ['intent', 'approve'] and len(argv) >= 4 and argv[3] in HASHES:
                    expanded.append(review_step(step, HASHES[argv[3]]))
            expanded.append(step)
        state['lastStep'] = expanded
    return replace_hashes(data)


def patch_smoke(data):
    provider = data.get('provider', {})
    if not isinstance(provider, dict):
        return
    if provider.get('script') and not provider.get('allow_unconsumed'):
        provider['allow_unconsumed'] = True
        provider['script'].extend([copy.deepcopy(provider['script'][-1]) for _ in range(2)])
        COUNTS['legacy_spare_turns_added'] += 2
    for turn in provider.get('script', []):
        if 'expect' in turn:
            old = turn['expect']
            body = old.get('body', {})
            keep = {k: body[k] for k in ('model', 'reasoning') if k in body}
            if 'reasoning' in keep:
                keep['reasoning'] = {k: v for k, v in keep['reasoning'].items() if k == 'effort'}
            turn['expect'] = {'body': keep} if keep else {}
            COUNTS['legacy_request_expectations_removed'] += int(old != turn['expect'])
    if 'provider_expect' in data:
        COUNTS['legacy_request_observations_removed'] += len(data.pop('provider_expect'))
    if 'provider_oauth_expect' in data:
        COUNTS['legacy_oauth_request_observations_removed'] += len(data.pop('provider_oauth_expect'))
    for step in data.get('steps', []):
        obs = step.get('observe', {})
        if 'provider_requests' in obs:
            COUNTS['legacy_request_observations_removed'] += len(obs.pop('provider_requests'))


def main():
    report_path = ROOT / 'T1-CHANGES.md'
    previous = report_path.read_text() if report_path.exists() else ''
    changed = []
    for path in sorted((ROOT / 'cases').rglob('*.json')):
        original = path.read_text()
        data = json.loads(original)
        before = copy.deepcopy(data)
        patch_scripts(data)
        patch_smoke(data)
        if path.name.endswith('.itf.json'):
            data = patch_approvals(data)
        if data != before:
            # Generated files already use compact JSON; preserve their layout.
            compact = '\n' not in original.rstrip('\n')
            path.write_text(json.dumps(data, ensure_ascii=False,
                                       separators=(',', ':') if compact else None,
                                       indent=None if compact else 2) + '\n')
            changed.append(str(path.relative_to(ROOT)))
    COUNTS['case_files_changed'] = len(changed)
    if previous:
        if not changed:
            print('No changes; existing counts and report retained.')
            return
        prior_counts = dict((key, int(value)) for key, value in
                            re.findall(r'^- (\w+): (\d+)$', previous, re.M))
        for key, value in prior_counts.items():
            if key in {'script_envelopes_scanned', 'empty_no_call_envelopes'}:
                COUNTS[key] = max(COUNTS[key], value)
            elif key != 'case_files_changed':
                COUNTS[key] += value
        changed = sorted(set(changed) | set(re.findall(r'^- `(cases/[^`]+)`$', previous, re.M)))
        COUNTS['case_files_changed'] = len(changed)
    report = ['# T1 changes', '', 'Applied with `python3 conformance/bin/t1_patch.py`.', '',
              '- `cases/**/*.manifest.json`: retain only model/effort body predicates; clear request headers/presence assertions; relax positive exact bounds by +2, append two spare final responses with gates cleared, and refresh script digests.',
              '- `cases/quint/{status,recovery,git}/*.itf.json`: insert no-hash approval review cards; capture full hashes and use captures/prefixes for commands and observations, including status reapproval.',
              '- `cases/04-shape-approve-queue-land.json`: remove scripted role checks and provider/OAuth request observations, including exact list counts; allow unused responses and append two spare responses.',
              '- `bin/t1_patch.py`: reproducible case-only patch script.', '', 'Counts (this run):', '']
    report += [f'- {key}: {value}' for key, value in sorted(COUNTS.items())]
    report += ['', 'Exclusions: none.', '', 'Assembler notes:', '',
               '- The runner job must remove `_validate_script`\'s mandatory `/input` predicate. Current runner rejects these intentionally relaxed scripts until that patch is assembled. POST remains as a required schema discriminator; request headers are empty.',
               '- Empty 0/0 envelopes have no scripted response and represent no-call cases; retained. All call-bearing envelopes retain `min_requests >= 1`. Existing unequal bounds are retained.',
               '- Spare responses are copies of each script\'s final response (gates cleared); the original minimum is unchanged.',
               '- Source/fixture provenance digests are unchanged because no spec files were edited. Embedded script digests were recalculated.',
               '- Approval review cards use the runner\'s existing full-line capture syntax, following intent review cases. No implementation binary is present for end-to-end execution.', '', 'Changed case files:', '']
    report += ['- `' + p + '`' for p in changed]
    report_path.write_text('\n'.join(report) + '\n')
    print(json.dumps(dict(COUNTS), sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
