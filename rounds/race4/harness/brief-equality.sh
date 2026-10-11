#!/bin/bash
set -e
R=$(cd "$(dirname "$0")" && pwd)
PYTHONDONTWRITEBYTECODE=1 python3 - "$R" <<'PYCODE'
from pathlib import Path
import difflib,re,sys
root=Path(sys.argv[1]);template=(root/'BRIEF.tmpl').read_text()
sys.path.insert(0,str(root))
from scoring_config import counts
try:
    values,_=counts(root)
except (ValueError, AssertionError):
    values=None  # Preparation placeholders; start checks require final counts.
if values:
    template=template.replace('{TARGET}',str(values['target'])).replace('{N}',str(values['N_scored']))
names={'rust':'Rust','go':'Go','ts':'TypeScript on Bun','gleam':'Gleam (on the Erlang/BEAM target)','ex':'Elixir'}
failed=False
for path in sorted(root.glob('BRIEF-*.md')):
    arm=path.stem[len('BRIEF-'):]
    expected=template.replace('LANGNAME',names[arm]).replace('LANGID',arm)
    actual=path.read_text()
    # Match placeholder positions only, including arm-specific stack/work paths.
    ok=expected==actual
    if not ok:
        sys.stdout.writelines(difflib.unified_diff(expected.splitlines(True),actual.splitlines(True),fromfile='BRIEF.tmpl rendered for '+arm,tofile=path.name))
    print(('PASS ' if ok else 'FAIL ')+path.name)
    failed |= not ok
print('Brief equality: '+('FAIL' if failed else 'PASS'))
sys.exit(failed)
PYCODE
