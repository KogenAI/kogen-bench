#!/usr/bin/env python3
"""Sanitize phase accounting and emit one host's four-run summary."""
from pathlib import Path
import argparse
import json
from arch_config import load, dump, TOKEN_KEYS, treatment, wave_for_arm, pair_for_arm
from arch_snapshot import tree_hash
from arch_tokens import collect_phase, ids_from_turns
from arch_audit import actual_model_receipts, audit_events
from arch_loc import count as count_loc
from arch_repairs import count as count_repairs
from arch_tooltimer import collect as collect_times
from arch_gates import check_freeze, contract_hash

def finalize(root):
    root = Path(root).resolve(); config = load(root)
    start = json.loads((root / 'ARCH-START.json').read_text())
    freeze_error = None
    try:
        frozen = check_freeze(root, skip_arm_files=True)
    except Exception as error:
        frozen = json.loads((root / 'ARCH-FREEZE.json').read_text())
        freeze_error = str(error)
    rows, used_threads = [], set()
    for arm in start['arms']:
        reasons = ['Frozen harness input changed: ' + freeze_error] if freeze_error else []
        arm_freeze_error = None
        if not freeze_error:
            try:
                check_freeze(root, only_arm=arm)
            except Exception as error:
                arm_freeze_error = str(error)
                reasons.append('Frozen arm input changed: ' + arm_freeze_error)
        phases, accounting_errors = {}, []
        for phase in (('build',) if start['mode'] == 'dry' else ('build', 'maintenance')):
            directory = root / 'out' / arm / ('phase-' + phase)
            turns = sorted(directory.glob('turn-*.jsonl'), key=lambda p: int(p.stem.split('-')[-1]))
            snapshot = root / 'snapshots' / phase / 'FINAL' / arm
            if not (directory / 'PHASE.json').is_file():
                reasons.append('Missing phase FINAL/receipt: ' + phase)
                phases[phase] = dict(score={'scoring_error': 'Missing phase FINAL/receipt', 'groups': None},
                                     tokens=None, model_receipts=None, audit=None, loc={'by_language': {}},
                                     repairs={'repair_turns': 0, 'launched_turns': 0, 'no_pass_claim': True},
                                     build_test={'total_seconds': 0}, agent_wall_seconds=0, errors=['missing phase'])
                continue
            info = json.loads((directory / 'PHASE.json').read_text())
            infra_path = directory / 'INFRA-FAILURE.json'
            infra = json.loads(infra_path.read_text()) if infra_path.is_file() else None
            if infra:
                reasons.append('Infrastructure failure (' + phase + '): ' + infra.get('reason', 'unspecified'))
            score_path = root / 'out' / arm / ('score-' + phase + '.json')
            scored = json.loads(score_path.read_text()) if score_path.is_file() else dict(
                scoring_error='Missing score result', groups=None)
            if phase == 'build' and scored.get('scoring_error'):
                reasons.append('Build FINAL unscorable: ' + scored['scoring_error'])
            if not (snapshot / 'spec').is_dir():
                reasons.append('FINAL capture missing: ' + phase)
            elif tree_hash(snapshot / 'spec') != tree_hash(root / 'inputs/spec'):
                reasons.append('Frozen spec modified in ' + phase)
            tokens, model_receipts, audited = None, None, None
            try:
                ids = ids_from_turns(turns)
                if ids & used_threads:
                    reasons.append('Session reused across arms/phases')
                used_threads |= ids
                model_receipts, rollouts = actual_model_receipts(info['sessions'], ids, info['cwd'], info['kill_utc'])
                audited = audit_events([*turns, *rollouts], root / arm,
                                       [config['kit'], *config['toolchains'].values()])
                reasons += [flag['reason'] + ' (' + phase + ')' for flag in audited['flags']]
            except Exception as error:
                reasons.append('Wrong/missing model or audit receipt (' + phase + '): ' + str(error))
            try:
                tokens = collect_phase(turns, info['sessions'], info['cwd'], info['kill_utc'])
            except Exception as error:
                accounting_errors.append('Token extraction (' + phase + '): ' + str(error))
            phases[phase] = dict(score=scored, tokens=tokens, model_receipts=model_receipts,
                                 audit=audited, loc=count_loc(snapshot), repairs=count_repairs(turns),
                                 build_test=collect_times(root / arm / '.kitcache/build-test-times.jsonl',
                                                          phase, info['deadline']),
                                 agent_wall_seconds=info['agent_wall_seconds'], kill_utc=info['kill_utc'],
                                 infrastructure_failure=infra,
                                 cpu=info['cpu'], harness_errors=info['errors'])
        all_tokens = all(value['tokens'] is not None for value in phases.values())
        usage = {key: sum(value['tokens']['usage'][key] for value in phases.values()) for key in TOKEN_KEYS} if all_tokens else None
        build_repairs = phases['build']['repairs']
        maintenance_repairs = phases.get('maintenance', {}).get('repairs')
        repair_turns = build_repairs['repair_turns']
        if maintenance_repairs:
            repair_turns += (max(0, maintenance_repairs['launched_turns'] - 1)
                             if not build_repairs['no_pass_claim'] else maintenance_repairs['repair_turns'])
        row = dict(host=config['host'], arm=arm, treatment=treatment(arm), valid=not reasons,
                   wave=wave_for_arm(arm), pair=pair_for_arm(arm),
                   deciding=config['host'] == 'studio' and start['mode'] == 'production',
                   status='deciding' if config['host'] == 'studio' and start['mode'] == 'production' else 'descriptive',
                   invalid_reasons=sorted(set(reasons)), accounting_errors=accounting_errors, phases=phases,
                   total_tokens=usage['total_tokens'] if usage else None, total_token_usage=usage,
                   F=phases['build']['score'].get('groups', {}).get('F') if phases['build']['score'].get('groups') else None,
                   B=phases['build']['score'].get('groups', {}).get('B') if phases['build']['score'].get('groups') else None,
                   M=phases.get('maintenance', {}).get('score', {}).get('groups', {}).get('M') if phases.get('maintenance', {}).get('score', {}).get('groups') else None,
                   agent_wall_seconds=sum(value['agent_wall_seconds'] for value in phases.values()),
                   build_test_seconds=sum(value['build_test']['total_seconds'] for value in phases.values()),
                   repair_turns=repair_turns,
                   loc={phase: value['loc']['by_language'] for phase, value in phases.items()})
        dump(root / 'out' / arm / 'ARCH-RUN.json', row)
        rows.append(row)
    admission = json.loads((root / 'out/ARCH-ADMISSION.json').read_text())
    result = dict(schema=1, host=config['host'], mode=start['mode'], runs=rows,
                  deciding=config['host'] == 'studio' and start['mode'] == 'production',
                  optional_status=('interrupted' if config['host'] == 'macbook' and (root / 'STOP').exists() else
                                   'descriptive' if config['host'] == 'macbook' else None),
                  wave_schedule=start.get('wave_schedule', []),
                  freeze=frozen, contract_sha256=contract_hash(frozen),
                  evidence_sha256=admission['evidence_sha256'],
                  drop_list=admission['drop_list'], passability_mode=admission['passability_mode'])
    dump(root / 'out/ARCH-SUMMARY.json', result)
    if start['mode'] == 'dry':
        scores = [phase['score'] for row in rows for phase in row['phases'].values()]
        scored = [score for score in scores if not score.get('scoring_error')]
        arm_scoring_wall = sum(float(score.get('scoring_wall_seconds', 0) or 0) for score in scored
                               if int(score.get('scoring_case_count', 0) or 0) > 0)
        arm_case_count = sum(int(score.get('scoring_case_count', 0) or 0) for score in scored)
        reference_path = root / 'out/ARCH-REFERENCE-SCORING.json'
        reference = json.loads(reference_path.read_text()) if reference_path.is_file() else dict(
            reference_snapshots=[], scored_reference=False, scoring_wall_seconds=0, scored_case_count=0)
        ref_scoring_wall = float(reference.get('scoring_wall_seconds', 0) or 0)
        ref_case_count = int(reference.get('scored_case_count', 0) or 0)
        audit_runs = sum(1 for row in rows for phase in row['phases'].values() if phase.get('audit') is not None)
        analyzer_runs = len(rows)
        has_arm_score = any(float(score.get('scoring_wall_seconds', 0) or 0) > 0 and
                            int(score.get('scoring_case_count', 0) or 0) > 0 for score in scored)
        has_reference_score = (reference.get('scored_reference') is True and ref_scoring_wall > 0 and
                               ref_case_count > 0 and bool(reference.get('reference_snapshots')))
        scoring_wall = ref_scoring_wall if has_reference_score else arm_scoring_wall
        scored_case_count = ref_case_count if has_reference_score else arm_case_count
        dry = dict(host=config['host'], mode='dry', arms=list(start['arms']), cap_seconds=600,
                   contract_sha256=contract_hash(frozen),
                   scoring_wall_seconds=scoring_wall, scored_case_count=scored_case_count,
                   arm_scoring_wall_seconds=arm_scoring_wall, arm_scored_case_count=arm_case_count,
                   reference_scoring_wall_seconds=ref_scoring_wall,
                   reference_scored_case_count=ref_case_count,
                   reference_snapshots=reference.get('reference_snapshots', []),
                   scored_reference=has_reference_score,
                   audit_runs=audit_runs, analyzer_runs=analyzer_runs,
                   passed=(all(row['valid'] and row['total_tokens'] is not None and row['F'] is not None for row in rows)
                           and (has_arm_score or has_reference_score) and audit_runs > 0 and analyzer_runs > 0),
                   model=config['model'], effort=config['effort'])
        dump(root / 'out/ARCH-DRY.json', dry)
    return result

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    args = p.parse_args()
    finalize(args.root)
    print(str(args.root / 'out/ARCH-SUMMARY.json'))

if __name__ == '__main__':
    main()
