#!/usr/bin/env python3
"""Exercise the lane record writer against the current strict Standard schema."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'reproduce/fixtures/record-contract'
sys.path.insert(0, str(ROOT / 'reproduce'))

import standard_record
import validate_round
from missing_reasons import load_legend

FIXTURE_INPUTS = (
    'plan.json', 'codex.jsonl', 'launch-snapshot.json',
    'lane-timing.json', 'boundary-samples.json', 'receipt-sha256.txt',
)


def _strict_report(row: dict, schema_path: Path, temp_root: Path) -> dict:
    """Validate one emitted row in an isolated copy of validate_round's inputs."""
    validator_root = temp_root / 'validator'
    (validator_root / 'schema').mkdir(parents=True)
    (validator_root / 'results').mkdir()
    round_id = row.get('audit_round') or row.get('round_id')
    if not isinstance(round_id, str) or not round_id:
        raise ValueError('fixture record has no round identity')
    round_root = validator_root / 'rounds' / round_id
    round_root.mkdir(parents=True)
    schema_target = validator_root / 'schema/run-record.schema.json'
    shutil.copyfile(schema_path, schema_target)
    shutil.copyfile(ROOT / 'results/missing-reasons.json',
                    validator_root / 'results/missing-reasons.json')
    for name in ('README.md', 'MEASURED.md'):
        (round_root / name).write_text('synthetic record-contract fixture\n')

    schema = json.loads(schema_target.read_text(encoding='utf-8'))
    current_schema = schema['$defs']['current']
    schema_errors = validate_round.schema_errors(
        row, current_schema, schema, str(row.get('cell_id', '<missing>')),
    )

    old_root, old_codes = validate_round.ROOT, validate_round.MISSING_CODES
    try:
        validate_round.ROOT = validator_root
        validate_round.MISSING_CODES = load_legend(
            validator_root / 'results/missing-reasons.json',
        )
        gaps = validate_round.gaps([row])
        fields = {
            path: {
                'count': sum(counts.values()),
                'reasons': counts,
                'affects_verdict': 'strict completion',
            }
            for path, counts in gaps.items()
        }
        declaration = {
            'round': round_id,
            'cells': 1,
            'fields': fields,
            'gap_sources': validate_round.gap_sources([row]),
            'protocol_deviations': ['synthetic fixture has missing capture fields'] if gaps else [],
        }
        (round_root / 'MISSING.md').write_text(
            '```json\n' + json.dumps(declaration, sort_keys=True) + '\n```\n',
        )
        report = validate_round.validate(round_id, [row], strict=True)
    finally:
        validate_round.ROOT, validate_round.MISSING_CODES = old_root, old_codes

    model = row.get('model')
    effective_model_set = isinstance(model, dict) and isinstance(model.get('effective'), str) and bool(model['effective'])
    report['schema_valid'] = not schema_errors
    report['schema_errors'] = schema_errors
    report['model_effective_set'] = effective_model_set
    report['contract_ok'] = (
        report['missing'] == 0 and report['schema_valid'] and not report['errors']
        and report['strict_release_eligible'] and effective_model_set
    )
    return report


def validate_fixture(schema_path: Path | None = None) -> dict:
    """Run standard_record.finalize on the checked-in synthetic cell inputs."""
    schema_path = Path(schema_path) if schema_path is not None else ROOT / 'schema/run-record.schema.json'
    if schema_path.is_symlink() or not schema_path.is_file():
        raise ValueError('record-contract schema must be a regular file')
    with tempfile.TemporaryDirectory(prefix='record-contract-') as temporary:
        temp_root = Path(temporary)
        result_dir = temp_root / 'result'
        result_dir.mkdir()
        for name in FIXTURE_INPUTS:
            source = FIXTURE / name
            if source.is_symlink() or not source.is_file():
                raise ValueError(f'record-contract fixture input is unavailable: {name}')
            shutil.copyfile(source, result_dir / name)

        # Protected synthetic receipts go through the same safe_rows path as host receipts.
        manifest = standard_record.read_json(FIXTURE / 'manifest.json')
        grade = standard_record.read_json(FIXTURE / 'grade.json')
        if not manifest or not grade:
            raise ValueError('safe_rows could not read the synthetic fixture receipts')
        manifest_bytes = (json.dumps(manifest, sort_keys=True) + '\n').encode('utf-8')
        (result_dir / 'manifest.json').write_bytes(manifest_bytes)
        (result_dir / 'grade.json').write_text(
            json.dumps(grade, sort_keys=True) + '\n', encoding='utf-8',
        )
        (result_dir / 'receipt-sha256.txt').write_text(
            hashlib.sha256(manifest_bytes).hexdigest() + '\n', encoding='ascii',
        )

        standard_record.finalize(result_dir)
        record_path = result_dir / 'standard.json'
        row = json.loads(record_path.read_text(encoding='utf-8'))
        return _strict_report(row, schema_path, temp_root)


if __name__ == '__main__':
    result = validate_fixture()
    print(json.dumps({
        'contract_ok': result['contract_ok'],
        'missing': result['missing'],
        'schema_valid': result['schema_valid'],
        'schema_errors': len(result['schema_errors']),
        'model_effective_set': result['model_effective_set'],
        'errors': len(result['errors']),
    }, sort_keys=True))
    raise SystemExit(0 if result['contract_ok'] else 1)
