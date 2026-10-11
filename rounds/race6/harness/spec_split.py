#!/usr/bin/env python3
"""Manifest is authoritative; copy unchanged bytes, verify coverage and hashes."""
import csv, hashlib, re, shutil, posixpath
from pathlib import Path
from condition import condition
ROOT=Path(__file__).resolve().parent
CLASSES={'a':{'PROSE'},'b':{'PROSE','QUINT'},'c':{'PROSE','GHERKIN'},'d':{'PROSE','QUINT','GHERKIN','D-ONLY'}}
def rows(root=ROOT):
    with (Path(root)/'spec-split.tsv').open() as f: return list(csv.DictReader(f,delimiter='\t'))
def verify(root=ROOT):
    root=Path(root); manifest=rows(root)
    paths=[r['path'] for r in manifest]
    actual={p.relative_to(root/'inputs/spec').as_posix() for p in (root/'inputs/spec').rglob('*') if p.is_file()}
    assert len(paths)==len(set(paths)) and set(paths)==actual,'manifest must classify every spec file exactly once'
    for r in manifest:
        assert r['class'] in CLASSES['d'] and r['reason']
        assert hashlib.sha256((root/'inputs/spec'/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
    return manifest
def copy_spec(root,arm,destination):
    root=Path(root); destination=Path(destination)
    for row in verify(root):
        if row['class'] in CLASSES[condition(arm)]:
            target=destination/row['path']; target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(root/'inputs/spec'/row['path'],target)
            target.chmod(0o444)
    for p in sorted(destination.rglob('*'),reverse=True):
        if p.is_dir(): p.chmod(0o555)
    destination.chmod(0o555)
def render(root=ROOT):
    root=Path(root); manifest=verify(root); known={r['path'] for r in manifest}
    lines=['# SPEC-SPLIT\n','Generated from spec-split.tsv. Source bytes are never edited.\n','| Class | Files | Conditions |','|---|---:|---|']
    for cls in ('PROSE','QUINT','GHERKIN','D-ONLY'):
        lines.append(f"| {cls} | {sum(r['class']==cls for r in manifest)} | {', '.join(a for a,c in CLASSES.items() if cls in c)} |")
    lines+=['\n## File classification\n','| Path | Class | Reason |','|---|---|---|']
    lines += [f"| `{r['path']}` | {r['class']} | {r['reason']} |" for r in manifest]
    lines+=['\n## SUPERVISOR DECISION NEEDED\n','No unresolved classifications remain under the final explicit condition definitions. The following chosen classifications are retained as supervisor review disclosures, not permission to follow suite references.',
      '- `CORE.md`, `CORE-WIRE.md`, `CORE-OUTCOMES.md`: recommendation PROSE, as required; these cite hidden case filenames and CORE declares scored values normative for OPEN details. Preserve text, disclose the citations, and do not grant suite access.',
      '- `MODULE-PLAN.md`: recommendation PROSE, as requested; it is a clause-to-model/witness crosswalk and contains coverage guidance.',
      '- `SEAM-GAPS.md`: recommendation PROSE; prose about missing seams also discusses executable coverage.',
      '- `core-add/G5.md` and `core-add/G7.md`: recommendation PROSE; normative prose references scored cases and fixture observations. Keep text unchanged.',
      '- `quint/traces/**`: recommendation QUINT because the rule explicitly includes quint/**; these are exported spec traces, not the hidden suite cases.',
      '- `checks/*-typecheck.log`, `checks/*-test.log`, invariant logs: recommendation QUINT as Quint-specific checks. Generation/results/coverage logs and scripts stay D-ONLY.',
      '- `QUINT-SUITE.md`: recommendation QUINT; it is a model/runner contract, so B and D see its unchanged detailed text. INTERFACE.md itself remains minimal.']
    lines+=['\n## Dangling cross-references\n','Literal Markdown links, backticked paths, and spec/... tokens are resolved relative to their source and spec root. Included text is unchanged; unresolved pre-existing links are disclosed too.']
    for arm in 'abc':
        included={r['path'] for r in manifest if r['class'] in CLASSES[arm]}; refs=set()
        for path in sorted(included):
            p=root/'inputs/spec'/path
            if p.suffix not in ('.md','.qnt','.py','.feature','.json'): continue
            text=p.read_text(errors='replace')
            tokens=re.findall(r'\]\(([^)\s]+)\)|`([^`\n]+)`|\b(spec/[A-Za-z0-9_./*-]+)',text)
            for choices in tokens:
                token=next((v for v in choices if v),'').split('#')[0]
                if not token or '://' in token or ' ' in token: continue
                token=token.removeprefix('spec/').removeprefix('./')
                candidates={posixpath.normpath(token),posixpath.normpath((Path(path).parent/token).as_posix())}
                matches={v for v in known if any(v==c or v.startswith(c.rstrip('/')+'/') for c in candidates)}
                excluded=matches-included
                if token.startswith('conformance/') or '/conformance/' in token: refs.add((path,token,'hidden suite path excluded from every arm'))
                elif excluded: refs.add((path,token,', '.join(sorted(excluded))))
                elif not matches and re.search(r'\.(?:md|qnt|json|py|feature)$',token): refs.add((path,token,'missing in frozen spec'))
        lines.append(f'\n### {arm}\n')
        lines += [f'- `{p}` → `{t}`: {e}' for p,t,e in sorted(refs)] or ['(none)']
    (root/'SPEC-SPLIT.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__': render()
