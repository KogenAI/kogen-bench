#!/usr/bin/env python3
"""ARCH decision from paired Studio waves; optional MacBook runs are descriptive."""
from pathlib import Path
import argparse
import json
from statistics import median
from arch_config import (STUDIO_ARMS, MACBOOK_ARMS, STUDIO_WAVES, PAIRS, CORES, dump, treatment)

def decide(rows, margin=3, ratio=1.5, min_valid=3, direction='G'):
    valid = {t: [r for r in rows if r['treatment'] == t and r['valid']] for t in ('E', 'G')}
    counts = {t: len(values) for t, values in valid.items()}
    medians = {t: dict(F=median(r['F']['passed'] for r in values) if values else None,
                      T=median(r['total_tokens'] for r in values) if values and all(r['total_tokens'] is not None for r in values) else None)
               for t, values in valid.items()}
    decision = dict(valid_runs=counts, medians=medians, fault_margin_threshold=margin,
                    token_ratio_threshold=ratio, default_direction=direction,
                    criterion_i=None, criterion_ii=None)
    if any(count < min_valid for count in counts.values()):
        return dict(**decision, outcome='inconclusive', recorded_direction=direction,
                    reason='Either treatment has fewer than ' + str(min_valid) + ' valid observations; propose rerun')
    fault_delta = medians['E']['F'] - medians['G']['F']
    decision.update(fault_delta=fault_delta, criterion_i=fault_delta >= margin)
    if any(value['T'] is None for value in medians.values()):
        return dict(**decision, outcome='inconclusive', recorded_direction=direction,
                    reason='Complete build+maintenance token accounting is unavailable; do not impute zero')
    decision['criterion_ii'] = medians['E']['T'] <= ratio * medians['G']['T']
    decision['token_limit_for_E'] = ratio * medians['G']['T']
    return dict(**decision, outcome='E' if decision['criterion_i'] and decision['criterion_ii'] else 'G')

def report(summaries):
    studios = [s for s in summaries if s.get('host') == 'studio']
    macbooks = [s for s in summaries if s.get('host') == 'macbook']
    if len(studios) != 1 or len(macbooks) > 1 or len(summaries) != len(studios) + len(macbooks):
        raise ValueError('Require exactly one Studio summary and at most one optional MacBook summary')
    studio = studios[0]
    if studio['mode'] != 'production' or studio.get('deciding') is False:
        raise ValueError('Only Studio production runs decide ARCH')
    frozen = studio['freeze']
    rules = frozen['decision']
    if (rules['fault_margin'], rules['token_ratio'], rules['min_valid']) != (3, 1.5, 3):
        raise ValueError('Decision contract differs from ARCH')
    rows = list(studio['runs'])
    grid = [r['arm'] for r in rows]
    if len(grid) != len(set(grid)) or set(grid) != set(STUDIO_ARMS):
        raise ValueError('All eight Studio cells must be recorded, including invalid cells')
    prescribed = {arm: wave for wave, arms in STUDIO_WAVES.items() for arm in arms}
    expected_counts = {g: sum(group == g for group in frozen['cases'].values()) for g in ('B', 'F', 'M')}
    for row in rows:
        if row['host'] != 'studio' or row['wave'] != prescribed[row['arm']]:
            raise ValueError('Studio arm assigned to the wrong wave')
        if row.get('pair') != pair_id(row['arm']):
            raise ValueError('Studio arm has incorrect preassigned pair')
        if row['treatment'] != ('E' if row['arm'].startswith('arch-e') else 'G'):
            raise ValueError('Treatment label does not match arm')
        if row['valid']:
            for group in ('B', 'F'):
                score = row[group]
                if score is None or score['total'] != expected_counts[group] or not 0 <= score['passed'] <= score['total']:
                    raise ValueError('Valid run has missing/invalid ' + group + ' score')
            if row['total_tokens'] is not None and (type(row['total_tokens']) is not int or row['total_tokens'] < 0):
                raise ValueError('Invalid total token count')
    included, excluded = [], []
    by_arm = {row['arm']: row for row in rows}
    for e_arm, g_arm in PAIRS[:4]:
        pair_rows = [by_arm[e_arm], by_arm[g_arm]]
        if all(row['valid'] and row['F'] is not None and row['total_tokens'] is not None for row in pair_rows):
            included.extend(pair_rows)
        else:
            excluded.append(dict(pair=pair_id(e_arm), arms=[e_arm, g_arm],
                                 reason='both paired runs must be valid with complete F and T'))
    decision = decide(included, rules['fault_margin'], rules['token_ratio'], rules['min_valid'], rules['default_direction'])
    decision['included_pairs'] = sorted({row['pair'] for row in included})
    decision['excluded_pairs'] = excluded
    wave_factor = {}
    for wave, wave_arms in STUDIO_WAVES.items():
        wave_rows = [row for row in included if row['wave'] == wave]
        values = decide(wave_rows, rules['fault_margin'], rules['token_ratio'], 1, rules['default_direction'])
        values['pair_count'] = len({row['pair'] for row in wave_rows})
        wave_factor[wave] = values
    sensitivities = {}
    for t in ('E', 'G'):
        valid = [r for r in included if r['treatment'] == t]
        sensitivity = {}
        for field in ('B', 'M', 'agent_wall_seconds', 'build_test_seconds', 'repair_turns'):
            nums = [r.get(field) for r in valid]
            nums = [x['passed'] if isinstance(x, dict) else x for x in nums if x is not None]
            sensitivity[field] = dict(n=len(nums), median=median(nums) if nums else None)
        languages = {lang for r in valid for phase in r.get('loc', {}).values() for lang in phase}
        sensitivity['LOC'] = {phase: {language: median(r.get('loc', {}).get(phase, {}).get(language, 0) for r in valid) if valid else None
                                             for language in sorted(languages)} for phase in ('build', 'maintenance')}
        sensitivities[t] = sensitivity
    optional_rows, optional_status = optional_report(macbooks[0] if macbooks else None)
    return dict(schema=2, decision=decision, per_host={'studio': decide(rows, min_valid=3)},
                sensitivities=sensitivities, runs=rows, optional_runs=optional_rows,
                optional_host_status=optional_status, wave_factor=wave_factor,
                rule_sha256=rules['rule_sha256'], contract_sha256=studio['contract_sha256'],
                disclosures=frozen['disclosures'], drop_list={'studio': studio.get('drop_list', []),
                    'macbook': macbooks[0].get('drop_list', []) if macbooks else ['optional host unavailable']},
                evidence_sha256={'studio': studio.get('evidence_sha256'),
                    'macbook': macbooks[0].get('evidence_sha256') if macbooks else None})

def pair_id(arm):
    for e_arm, _ in PAIRS:
        if arm == e_arm or arm.replace('g', 'e') == e_arm:
            return e_arm.replace('arch-e', 'pair-')
    raise ValueError('Unknown pair arm: ' + arm)

def optional_report(summary):
    by_arm = {row['arm']: row for row in summary.get('runs', [])} if summary else {}
    rows, interrupted = [], (summary is None or summary.get('optional_status') == 'interrupted' or
                              any(arm not in by_arm for arm in MACBOOK_ARMS))
    for arm in MACBOOK_ARMS:
        row = by_arm.get(arm)
        if row is None:
            row = dict(host='macbook', arm=arm, treatment=treatment(arm), valid=False,
                       invalid_reasons=['interrupted: optional host unavailable'], total_tokens=None,
                       B=None, F=None, M=None, deciding=False, wave='optional', pair=pair_id(arm))
            interrupted = True
        else:
            status = 'interrupted: optional host unavailable' if interrupted else 'descriptive only'
            row = dict(row, deciding=False, wave='optional', pair=pair_id(arm), status=status)
        rows.append(row)
    return rows, 'interrupted: optional host unavailable' if interrupted else 'descriptive only'

def markdown(result):
    decision = result['decision']
    lines = ['# ARCH results', '', 'Decision: **' + decision['outcome'] + '**.', '']
    if decision.get('reason'):
        lines += [decision['reason'] + '.', '']
    for t in ('E', 'G'):
        values = decision['medians'][t]
        lines.append(f"{t}: {decision['valid_runs'][t]} valid runs; median F={values['F']}; median tokens={values['T']}.")
    lines += ['', f"Criterion (i): {decision.get('fault_delta', 'unavailable')} ≥ 3 → {decision['criterion_i']}.",
              f"Criterion (ii): median E tokens ≤ 1.5 × median G tokens ({decision.get('token_limit_for_E', 'unavailable')}) → {decision['criterion_ii']}.",
              '', '| Host | Arm | Valid | B | F | M | Tokens | Agent wall s | Build/test s | Repair turns | LOC build → maintenance |',
              '|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|']
    def score(value):
        return f"{value['passed']}/{value['total']}" if value else 'unavailable'
    for row in sorted(result['runs'], key=lambda r: (r['host'], r['arm'])):
        loc = json.dumps(row.get('loc', {}), sort_keys=True)
        lines.append(f"| {row['host']} | {row['arm']} | {row['valid']} | {score(row['B'])} | {score(row['F'])} | {score(row.get('M'))} | {row['total_tokens']} | {row.get('agent_wall_seconds')} | {row.get('build_test_seconds')} | {row.get('repair_turns')} | {loc} |")
    lines += ['', 'Studio wave factor:', '', '| Wave | Arms | Included pairs | E median F/T | G median F/T |',
              '|---|---|---:|---|---|']
    for wave, values in result['wave_factor'].items():
        med = values['medians']
        lines.append(f"| {wave} | {', '.join(STUDIO_WAVES[wave])} | {values['pair_count']} | {med['E']['F']}/{med['E']['T']} | {med['G']['F']}/{med['G']['T']} |")
    lines += ['', 'Optional MacBook runs (descriptive only; excluded from the decision): ' +
              result['optional_host_status'] + '.', '',
              '| Arm | Valid | B | F | M | Tokens | Status |', '|---|---|---:|---:|---:|---:|---|']
    for row in result['optional_runs']:
        lines.append(f"| {row['arm']} | {row['valid']} | {score(row.get('B'))} | {score(row.get('F'))} | {score(row.get('M'))} | {row.get('total_tokens')} | {row.get('status', '; '.join(row.get('invalid_reasons', [])))} |")
    invalid = [r for r in result['runs'] if not r['valid']]
    lines += ['', 'Invalid runs:', '']
    lines += [f"- {r['host']}/{r['arm']}: " + '; '.join(r['invalid_reasons']) for r in invalid] or ['None.']
    lines += ['', 'Per-host results and sensitivities:', '', '```json',
              json.dumps(dict(per_host=result['per_host'], sensitivities=result['sensitivities']), indent=2), '```',
              '', 'Disclosures:', ''] + ['- ' + value for value in result['disclosures']]
    lines += ['', 'Drop list: ' + str(result['drop_list']) + '.', '',
              'Four observations per treatment form a pilot; these results do not establish broader effects.', '']
    return '\n'.join(lines)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('summaries', type=Path, nargs='+', help='Studio deciding summary, optionally followed by MacBook descriptive summary')
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--markdown', type=Path, required=True)
    args = p.parse_args()
    result = report([json.loads(path.read_text()) for path in args.summaries])
    dump(args.out, result)
    args.markdown.write_text(markdown(result))
    print('ARCH decision: ' + result['decision']['outcome'])

if __name__ == '__main__':
    main()
