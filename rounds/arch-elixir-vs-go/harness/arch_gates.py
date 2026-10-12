#!/usr/bin/env python3
"""ARCH-specific frozen launch gates. No inherited L2/L3 admission is implied."""
from pathlib import Path
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from arch_config import ARMS, CORES, MODEL, EFFORT, CONSTRAINTS, load, arms_for_host, dump, digest
from arch_snapshot import inventory, tree_hash
from arch_score import normalize, PROFILE

CHECKS = ('spec_lint', 'contradictions', 'quint', 'mechanics')

def check_tool_version(tool, flag, expected, env, cwd, timeout=15):
    output = subprocess.check_output([tool, flag], env=env, cwd=str(cwd), text=True, timeout=timeout)
    if expected not in output:
        raise ValueError('Toolchain version differs in arm workspace: ' + str(cwd))
    return output

def frozen_files(root):
    config = load(root)
    arms = arms_for_host(config['host'])
    names = ['ARCH-CONFIG.json', 'ARMS', 'CODEX-VERSION', 'KIT-PINS-v2.json',
             'BRIEF-ARCH.tmpl', 'MAINTENANCE-ARCH.md', 'DESIGN-ARCH.md', 'DECISION-RULE-ARCH.md',
             'AMENDMENT-1-STUDIO-DECIDES.md', 'AMENDMENT-1-STUDIO-DECIDES.sha256']
    names += [p.name for p in root.glob('arch_*.py')]
    names += ['BRIEF-' + arm + '.md' for arm in arms]
    for arm in arms:
        names += [arm + '/.kit-env.sh', arm + '/AGENTS.md', 'out/' + arm + '/environment.json']
        names += [arm + '/mise.toml']
        names += [(p.relative_to(root)).as_posix() for p in (root / arm / '.kit-tools').glob('*')
                  if p.name in ('arch_tooltimer.py', 'go', 'mix')]
    for folder in ('spec', 'inputs/spec', 'tests'):
        names += [p.relative_to(root).as_posix() for p in (root / folder).rglob('*')
                  if p.is_file() and p.suffix in ('.py', '.sh', '.md', '.qnt', '.feature') and
                  '.tmp' not in p.parts and 'results' not in p.parts and '__pycache__' not in p.parts]
    return sorted(set(names))

def case_inventory(root):
    result = subprocess.check_output([sys.executable, str(root / 'tests/run_hidden.py'), '--list'],
                                     text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    cases = {}
    for line in result.splitlines():
        match = re.match(r'^(\S+) \[([BFM])\] ', line)
        if not match or match[1] in cases:
            raise ValueError('Unrecognized or duplicate case inventory line')
        cases[match[1]] = match[2]
    if set(cases.values()) != {'B', 'F', 'M'}:
        raise ValueError('All three groups must be present')
    return cases

def freeze(root):
    root = Path(root).resolve()
    if (root / 'ARCH-START.json').exists() or (root / 'ARCH-FREEZE.json').exists():
        raise ValueError('Freeze is single-use and must precede launch')
    cases = case_inventory(root)
    files = {name: digest(root / name) for name in frozen_files(root)}
    amendment_sha = (root / 'AMENDMENT-1-STUDIO-DECIDES.sha256').read_text().strip()
    if files['AMENDMENT-1-STUDIO-DECIDES.md'] != amendment_sha:
        raise ValueError('Studio decision amendment hash differs from its seal pin')
    rule_pin = root / 'RULE-SHA256.txt'
    if not rule_pin.is_file() or files['DECISION-RULE-ARCH.md'] not in rule_pin.read_text():
        raise ValueError('Job E rule hash receipt is missing or does not match')
    payload = dict(schema=1, files=files, cases=cases,
                   decision=dict(fault_margin=3, token_ratio=1.5, min_valid=3,
                                 default_direction='G', rule_sha256=files['DECISION-RULE-ARCH.md']),
                   caps_seconds=dict(build=5400, maintenance=1800), soft_cores=CORES,
                   model=MODEL, effort=EFFORT,
                   disclosures=['Simulated two nodes on one host.', 'macOS-only containment semantics.',
                                'Passability by analysis unless dual witnesses are explicitly ordered.',
                                'Single model and effort; four observations per treatment.',
                                'Tie goes to G by design.',
                                'CPU and access enforcement are sampled/static at race5 level.'])
    dump(root / 'ARCH-FREEZE.json', payload)
    (root / 'ARCH-FREEZE.sha256').write_text(digest(root / 'ARCH-FREEZE.json') + '\n')
    return payload

def _frozen_arm(name):
    parts = Path(name).parts
    if parts and parts[0] in ARMS:
        return parts[0]
    if len(parts) > 1 and parts[0] == 'out' and parts[1] in ARMS:
        return parts[1]
    return None

def check_freeze(root, only_arm=None, skip_arm_files=False):
    root = Path(root)
    if digest(root / 'ARCH-FREEZE.json') != (root / 'ARCH-FREEZE.sha256').read_text().strip():
        raise ValueError('Freeze manifest changed')
    frozen = json.loads((root / 'ARCH-FREEZE.json').read_text())
    for name, sha in frozen['files'].items():
        file_arm = _frozen_arm(name)
        if only_arm is not None and file_arm != only_arm:
            continue
        if skip_arm_files and file_arm is not None:
            continue
        if digest(root / name) != sha:
            raise ValueError('Frozen file changed: ' + name)
    if case_inventory(root) != frozen['cases']:
        raise ValueError('Hidden inventory changed after freeze')
    if frozen['decision'] != dict(fault_margin=3, token_ratio=1.5, min_valid=3,
                                  default_direction='G', rule_sha256=frozen['files']['DECISION-RULE-ARCH.md']):
        raise ValueError('Decision constants differ from ARCH')
    return frozen

def proof_file(entry, base):
    path = Path(entry['path']).expanduser()
    if not path.is_absolute():
        path = base / path
    if digest(path) != entry['sha256']:
        raise ValueError('Gate proof hash changed: ' + str(path))
    return json.loads(path.read_text())

def passability(evidence, frozen, base):
    expected = frozen['cases']
    if evidence.get('mode') == 'analysis':
        analysis = evidence['analysis']
        if set(analysis['per_case']) != set(expected):
            raise ValueError('Passability does not cover every frozen case')
        for case, checks in analysis['per_case'].items():
            if set(checks) != set(CHECKS) or any(checks[key] is not True for key in CHECKS):
                raise ValueError('Case is not passable by analysis: ' + case)
        for name in CHECKS:
            artifact = proof_file(analysis['checks'][name], base)
            if not (artifact.get('passed') is True or artifact.get('status') in ('pass', 'passed', 'passable-by-analysis')):
                raise ValueError('Passability artifact is not passing: ' + name)
            for path, sha in artifact.get('inputs', {}).items():
                if path in frozen['files'] and frozen['files'][path] != sha:
                    raise ValueError('Passability used stale input: ' + path)
        bindings = analysis['input_hashes']
        relevant = {p: sha for p, sha in frozen['files'].items() if p.startswith(('spec/', 'tests/'))}
        if any(bindings.get(p) != sha for p, sha in relevant.items()):
            raise ValueError('Analysis is not bound to all frozen test/spec inputs')
    elif evidence.get('mode') == 'dual-witness':
        if evidence.get('explicit_witness_order') is not True:
            raise ValueError('Witness branch requires an explicitly recorded user order')
        for host in ('studio',):
            for language in ('Elixir', 'Go'):
                entries = evidence['witness'][host][language]
                reps = 0
                for entry in entries:
                    raw = proof_file(entry, base)
                    result = normalize(raw, ['B', 'F', 'M'], expected, reps=raw.get('reps'))
                    if not all(row['passed'] == row['total'] for row in result['groups'].values()):
                        raise ValueError('Witness failed a frozen case')
                    reps += raw['reps']
                    if raw.get('spec_sha256') != {n: frozen['files']['spec/' + n] for n in ('SPEC.md', 'PROTOCOL.md')}:
                        raise ValueError('Witness used stale spec')
                if reps != 3:
                    raise ValueError('Both witnesses must pass exactly 3/3 on Studio')
    else:
        raise ValueError('Unknown passability mode')
    if not isinstance(evidence.get('drop_list'), list):
        raise ValueError('Drop list must be recorded, including an empty list')

def validate_dry_receipt(proof, frozen):
    if (proof.get('host') != 'studio' or proof.get('mode') != 'dry' or proof.get('passed') is not True or
            proof.get('contract_sha256') != contract_hash(frozen) or
            proof.get('arms') != ['arch-e1', 'arch-g1'] or proof.get('cap_seconds') != 600):
        raise ValueError('Production evidence requires a passing one-wave Studio dry receipt')
    audits = proof.get('audit_runs')
    analyzers = proof.get('analyzer_runs')
    def positive_metrics(wall, cases):
        return (isinstance(wall, (int, float)) and not isinstance(wall, bool) and wall > 0 and
                isinstance(cases, int) and not isinstance(cases, bool) and cases > 0)
    arm_score = positive_metrics(proof.get('arm_scoring_wall_seconds', proof.get('scoring_wall_seconds')),
                                 proof.get('arm_scored_case_count', proof.get('scored_case_count')))
    reference_score = (proof.get('scored_reference') is True and
                       bool(proof.get('reference_snapshots')) and
                       positive_metrics(proof.get('reference_scoring_wall_seconds'),
                                        proof.get('reference_scored_case_count')))
    if (not (arm_score or reference_score) or
            not isinstance(audits, int) or isinstance(audits, bool) or audits <= 0 or
            not isinstance(analyzers, int) or isinstance(analyzers, bool) or analyzers <= 0):
        raise ValueError('Production evidence requires a passing one-wave Studio dry receipt with scoring, audit, and analyzer metrics')

def verify(root, evidence_path, dry=False, platform_checks=True):
    root = Path(root).resolve(); config = load(root)
    evidence_path = Path(evidence_path).expanduser().resolve()
    frozen = check_freeze(root)
    evidence = json.loads(evidence_path.read_text())
    passability(evidence, frozen, evidence_path.parent)
    if not dry:
        proof = proof_file(evidence['dry']['studio'], evidence_path.parent)
        validate_dry_receipt(proof, frozen)
    if dry and config['host'] != 'studio':
        raise ValueError('Dry cells are run only on Studio')
    normalized = []
    arms = arms_for_host(config['host'])
    for arm in arms:
        brief = (root / ('BRIEF-' + arm + '.md')).read_text()
        constraint = CONSTRAINTS['E' if arm.startswith('arch-e') else 'G']
        normalized.append(brief.replace(constraint, '{CONSTRAINT}'))
        if tree_hash(root / arm / 'spec') != tree_hash(root / 'inputs/spec'):
            raise ValueError('Visible spec differs for ' + arm)
        env = json.loads((root / 'out' / arm / 'environment.json').read_text())
        if float(env['ARCH_SOFT_CORES']) != CORES[config['host']]:
            raise ValueError('CPU environment differs')
        if arm.startswith('arch-g') and any(tool in env['PATH'] for tool in ('/elixir/', '/erlang/')):
            raise ValueError('G arm has an Elixir/OTP toolchain on PATH')
    if len(set(normalized)) != 1:
        raise ValueError('Briefs differ beyond the one constraint sentence')
    if platform_checks:
        if os.uname().sysname != 'Darwin':
            raise ValueError('ARCH production is macOS-only')
        cli = subprocess.check_output([config['codex_executable'], '--version'], text=True).strip()
        if cli != (root / 'CODEX-VERSION').read_text().strip():
            raise ValueError('Installed Codex differs from frozen lever version')
        for arm in arms:
            env = dict(os.environ, **json.loads((root / 'out' / arm / 'environment.json').read_text()))
            for tool, flag, version in [('go', 'version', 'go1.27.1')] + (
                    [('elixir', '--version', 'Elixir 1.20.4')] if arm.startswith('arch-e') else []):
                check_tool_version(tool, flag, version, env, root / arm, timeout=15)
        for tool in ('git', 'ps', 'sandbox-exec'):
            if not shutil.which(tool):
                raise ValueError('Required launch tool missing: ' + tool)
        subprocess.run(['ps', '-axo', 'pid=,ppid=,pgid=,time=,stat=,lstart='],
                       check=True, stdout=subprocess.DEVNULL)
        test = ('import socket,errno; s=socket.socket(); s.settimeout(.2); '
                '\ntry: s.connect(("[IP omitted]",9))\nexcept OSError as e: '
                'assert e.errno in (errno.EPERM,errno.EACCES),repr(e)\nelse: raise AssertionError("remote network allowed")\n'
                'x=socket.socket();x.bind(("[IP omitted]",0));x.listen();'
                'y=socket.socket();y.connect(x.getsockname());z,_=x.accept();z.close();y.close();x.close()')
        subprocess.run(['sandbox-exec', '-p', PROFILE, sys.executable, '-c', test], check=True, timeout=5)
        visible_bytes = sum((root / arm / p).stat().st_size for arm in arms
                            for p, kind, sha, links in inventory(root / arm) if kind != 'link')
        if shutil.disk_usage(root).free < max(10 * 1024**3, visible_bytes * 28):
            raise ValueError('Insufficient free disk for snapshots and score copies')
        # Recompute the full race 5 kit manifest; write only inside this new harness.
        manifest = root / 'out/kit-manifest.sha256'
        subprocess.run(['/bin/bash', str(root / 'kitsum.sh')], check=True, stdout=subprocess.DEVNULL,
                       env=dict(os.environ, RACE3_KIT_DIR=config['kit'], RACE_KIT_MANIFEST=str(manifest)))
        if digest(manifest) != config['kit_pins']['race5_full_kit_manifest_sha256']:
            raise ValueError('Full race 5 kit pin differs')
    dump(root / 'out/ARCH-ADMISSION.json', dict(passed=True, mode='dry' if dry else 'production',
                                               evidence_sha256=digest(evidence_path),
                                               contract_sha256=contract_hash(frozen), platform_checked=platform_checks,
                                               passability_mode=evidence['mode'], drop_list=evidence['drop_list']))
    return frozen

def contract_hash(frozen):
    # Host paths and cache settings may differ; protocol/spec/tests/prompts/rule/code must agree.
    import hashlib
    portable = {path: sha for path, sha in frozen['files'].items()
                if path != 'ARCH-CONFIG.json' and not path.startswith(('arch-e', 'arch-g', 'out/'))}
    return hashlib.sha256(json.dumps(portable, sort_keys=True).encode()).hexdigest()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=('freeze', 'verify'))
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--evidence', type=Path)
    p.add_argument('--dry', action='store_true')
    args = p.parse_args()
    if args.mode == 'freeze':
        freeze(args.root)
    elif not args.evidence:
        p.error('--evidence is required for verify')
    else:
        verify(args.root, args.evidence, args.dry)
    print('ARCH ' + args.mode + ' passed')

if __name__ == '__main__':
    main()
