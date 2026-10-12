#!/usr/bin/env python3
"""Bind job F proofs and its reviewed case ledger to this frozen harness."""
from pathlib import Path
import argparse
import json
from arch_config import dump, digest
from arch_gates import CHECKS, check_freeze, passability, proof_file, contract_hash, validate_dry_receipt

FILES = {'spec_lint': 'spec-lint.json', 'contradictions': 'contradictions.json',
         'quint': 'quint-check.json', 'mechanics': 'stub-dry-run.json'}

def reference(path):
    return dict(path=str(Path(path).expanduser().resolve()), sha256=digest(Path(path).expanduser()))

def build(root, analysis, ledger=None, dry_macbook=None, dry_studio=None, production=False):
    root, analysis = Path(root).resolve(), Path(analysis).expanduser().resolve()
    frozen = check_freeze(root)
    if production and not ledger:
        raise ValueError('Production evidence requires a reviewed case ledger')
    if ledger:
        ledger = json.loads(Path(ledger).expanduser().read_text())
        per_case = ledger['per_case']
        drop_list = ledger['drop_list']
        if production and dry_studio is None:
            raise ValueError('Production evidence requires the passing Studio dry receipt')
        if production:
            studio_receipt = json.loads(Path(dry_studio).expanduser().read_text())
            validate_dry_receipt(studio_receipt, frozen)
    else:
        per_case = {case: dict.fromkeys(CHECKS, False) for case in frozen['cases']}
        drop_list = []
    checks = {name: reference(analysis / path) for name, path in FILES.items()}
    # Bind proofs to inputs they actually examined; a new scaffold may not
    # silently relabel an old check as a check of the current suite.
    bindings = {}
    for entry in checks.values():
        for path, sha in proof_file(entry, analysis).get('inputs', {}).items():
            if path.startswith(('spec/', 'tests/')):
                if path in bindings and bindings[path] != sha:
                    raise ValueError('Job F proofs examined inconsistent input versions: ' + path)
                bindings[path] = sha
    result = dict(schema=1, mode='analysis', analysis=dict(per_case=per_case, checks=checks, input_hashes=bindings),
                  drop_list=drop_list, dry={})
    if ledger:
        passability(result, frozen, analysis)
    # MacBook evidence is descriptive only; even a failed optional receipt must
    # never block the Studio production evidence or verdict.
    if dry_macbook and Path(dry_macbook).expanduser().is_file():
        result['dry']['macbook'] = reference(dry_macbook)
    if dry_studio:
        result['dry']['studio'] = reference(dry_studio)
    return result

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--analysis', type=Path, required=True)
    p.add_argument('--reviewed-ledger', type=Path)
    p.add_argument('--dry-macbook', type=Path)
    p.add_argument('--dry-studio', type=Path)
    p.add_argument('--production', action='store_true', help='Require a passing Studio dry receipt for production evidence')
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    result = build(args.root, args.analysis, args.reviewed_ledger, args.dry_macbook, args.dry_studio,
                   production=args.production)
    dump(args.out, result)
    print('Evidence bound to reviewed proofs' if args.reviewed_ledger else 'Pending evidence scaffold; all per-case checks remain false')

if __name__ == '__main__':
    main()
