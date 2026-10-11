#!/usr/bin/env python3
"""Validate installed final inputs and render the race documents before freeze."""
from pathlib import Path
import hashlib
from scoring_config import counts, scored_ids
from validity import tree_hash
from mode_policy import read_mode, render_policy

ROOT = Path(__file__).resolve().parent
NAMES = {'rust': 'Rust', 'go': 'Go', 'ts': 'TypeScript on Bun',
         'ex': 'Elixir', 'py': 'Python'}


def main():
    mode = read_mode(ROOT)
    values, bugs = counts(ROOT)
    ids = scored_ids(ROOT)
    sha = tree_hash(ROOT / 'inputs', frozen=True)
    if sha != (ROOT / 'inputs.sha').read_text().strip():
        raise ValueError('inputs.sha differs from installed final inputs')
    ncases = ROOT / 'inputs/NCASES'
    if ncases.exists() and int(ncases.read_text()) != values['N_total']:
        raise ValueError('inputs/NCASES differs from COUNTS.txt')
    substitutions = {'{N}': str(values['N_scored']), '{TARGET}': str(values['target']),
                     '{INPUTS_SHA}': sha}
    def render(text):
        text = render_policy(text, mode)
        for token, value in substitutions.items():
            text = text.replace(token, value)
        return text
    template = render((ROOT / 'BRIEF.tmpl').read_text())
    for arm, name in NAMES.items():
        (ROOT / f'BRIEF-{arm}.md').write_text(template.replace('LANGNAME', name).replace('LANGID', arm))
    target = f"TARGET/N = {values['target']}/{values['N_scored']}\n\n"
    target += 'Reach all N_scored cases (100%) as scored passes. Implement the complete spec.\n'
    target += f"The runner inventories {values['N_total']} cases; {len(bugs)} are excluded from scoring.\n\nExcluded IDs:\n\n"
    target += ''.join(f'- {cid}\n' for cid in sorted(bugs)) or '(none)\n'
    (ROOT / 'TARGET.md').write_text(target)
    decision = ROOT / 'DECISION-RULE-v5.md'
    decision.write_text(render((ROOT / 'DECISION-RULE-v5.tmpl').read_text()))
    (ROOT / 'DECISION-RULE.sha256').write_text(hashlib.sha256(decision.read_bytes()).hexdigest() + '  DECISION-RULE-v5.md\n')
    (ROOT / 'COUNTS.txt').write_text(''.join(f'{key}={values[key]}\n' for key in ('N_total', 'N_scored', 'target', 'excluded')))
    (ROOT / 'SCORE_CASES.txt').write_text('\n'.join(ids) + '\n')
    print(f"PASS final inputs: target={values['target']}/{values['N_scored']}, total={values['N_total']}, sha={sha}")


if __name__ == '__main__':
    main()
