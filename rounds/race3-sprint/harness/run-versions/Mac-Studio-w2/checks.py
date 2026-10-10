#!/usr/bin/python3
import difflib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from validity import codex_home, tree_hash
from scoring_config import counts

R = Path(__file__).resolve().parent
KIT = Path(os.environ.get('RACE3_KIT_DIR', '~/Scratch.noindex/race3-kit')).resolve()
NAMES = {'rust': 'Rust', 'go': 'Go', 'ts': 'TypeScript on Bun',
         'gleam': 'Gleam (on the Erlang/BEAM target)', 'ex': 'Elixir'}


def diff(want, got, left, right):
    print(''.join(difflib.unified_diff(want.splitlines(True), got.splitlines(True),
                                       fromfile=left, tofile=right)), end='')
    return want == got


def normalise_env(env, arm):
    # Preserve variable names, flags, and PATH order. Only known path roots and
    # shell bookkeeping vary; arbitrary variables (including caps) stay checked.
    result = {}
    for key, value in env.items():
        if key in ('_', 'SHLVL', 'OLDPWD'):
            continue
        value = value.replace(str(R / arm), '<ARM>').replace(str(KIT), '<KIT>')
        value = re.sub(r'~/[^/]+/\.local/share/mise/installs/([^/]+)/[^/:]+',
                       r'<TOOLCHAIN>/\1', value)
        result[key] = value
    return ''.join('%s=%s\n' % item for item in sorted(result.items()))


def run():
    failed = []
    def check(name, fn):
        try:
            ok = fn()
        except Exception as e:
            print(str(e)); ok = False
        print(('PASS ' if ok else 'FAIL ') + name)
        if not ok:
            failed.append(name)

    arms = (R / 'ARMS').read_text().split()
    def briefs():
        template = (R / 'BRIEF.tmpl').read_text()
        ok = True
        for arm, name in NAMES.items():
            # Replace only placeholder positions. A global replacement could
            # conceal edits to unrelated mentions of the language/arm name.
            pattern = re.escape(template).replace('LANGNAME', re.escape(name)).replace('LANGID', re.escape(arm))
            text = (R / ('BRIEF-%s.md' % arm)).read_text()
            expected = template.replace('LANGNAME', name).replace('LANGID', arm)
            if not re.fullmatch(pattern, text):
                normal = text.replace(name, 'LANGNAME').replace('/tmp/kc-' + arm, '/tmp/kc-LANGID')
                diff(template, normal, 'BRIEF.tmpl', 'BRIEF-%s.md (normalised)' % arm)
                ok = False
        return ok
    check('briefs', briefs)
    # Assembly mode requires no race directory, kit or credential paths.
    if '--assembly' in __import__('sys').argv or not any((R / arm).is_dir() for arm in arms):
        check('frozen-inputs', lambda: tree_hash(R / 'inputs', frozen=True) == (R / 'inputs.sha').read_text().strip())
        def assembly_counts():
            values, bugs = counts(R)
            text = (R / 'TARGET.md').read_text()
            listed = re.findall(r'^- (\S+)\t', text, re.M)
            reasons = dict(line.split('\t', 1) for line in (R / 'EXCLUDED-V2.txt').read_text().splitlines())
            return (int((R / 'inputs/NCASES').read_text()) == values['N_total']
                    and set(listed) == bugs == set(reasons) and len(listed) == len(bugs)
                    and f"{values['target']}/{values['N_scored']}" in text)
        check('target-spec-bugs', assembly_counts)
        check('suite-checks', lambda: subprocess.call([__import__('sys').executable, str(R/'suite-checks.py')]) == 0)
        print('SKIP host checks: kit, version, arm environments and auth require a prepared race directory')
        return bool(failed)

    def kit():
        output = subprocess.check_output(['bash', 'kitsum.sh'], cwd=str(R), text=True)
        match = re.search(r'\bhash ([0-9a-fA-F]{64})\b', output)
        if match is None:
            raise ValueError('kitsum.sh did not print a valid hash: ' + output.strip())
        sha = match.group(1).lower()
        if (R / 'out').is_dir():
            shutil.copyfile('/tmp/kit-manifest.sha256', R / 'out/kit-manifest.sha256')
            (R / 'out/kit.sha256').write_text(sha + '\n')
        print('kit sha256:', sha)
        pin = R / 'KIT-SHA256'
        return not pin.exists() or pin.read_text().strip() == sha
    check('kit', kit)
    def inputs():
        sha = tree_hash(R / 'inputs', frozen=True); print('inputs sha:', sha)
        return sha == (R / 'inputs.sha').read_text().strip()
    check('frozen-inputs', inputs)

    def version():
        got = subprocess.check_output(['/bin/bash', '-c', 'source "$1/env.sh"; codex --version',
                                       'checks', str(R)], cwd=str(R), text=True).strip()
        (R / 'out/codex-version.txt').write_text(got + '\n'); print(got)
        pin = R / 'CODEX-VERSION'
        return bool(got) and (not pin.exists() or pin.read_text().strip() == got)
    check('codex-version', version)

    def environments():
        baseline = None; ok = bool(arms)
        command = ('set -e; source "$1/env.sh"; source "$1/$2/.kit-env.sh"; '
                   'if [ -s "$1/CODEX_HOME" ]; then export CODEX_HOME=$(cat "$1/CODEX_HOME"); fi; '
                   'cd "$1/$2"; exec /usr/bin/python3 -c "import json,os;print(json.dumps(dict(os.environ)))"')
        for arm in arms:
            env = json.loads(subprocess.check_output(['/bin/bash', '-c', command, 'checks', str(R), arm],
                                                     cwd=str(R), text=True))
            raw = ''.join('%s=%s\n' % item for item in sorted(env.items()))
            (R / ('out/env-%s.txt' % arm)).write_text(raw)
            normal = normalise_env(env, arm)
            (R / ('out/env-%s.normalised.txt' % arm)).write_text(normal)
            if baseline is None:
                baseline = (arm, normal)
            else:
                ok = diff(baseline[1], normal, 'env-' + baseline[0], 'env-' + arm) and ok
        return ok
    check('arm-environments', environments)
    check('codex-auth', lambda: codex_home(R).is_dir() and (codex_home(R) / 'auth.json').is_file())

    def target():
        values, bugs = counts(R)
        reasons = dict(line.split('\t', 1) for line in (R / 'EXCLUDED-V2.txt').read_text().splitlines())
        text = (R / 'TARGET.md').read_text()
        listed = re.findall(r'^- (\S+)\t', text, re.M)
        n = int((R / 'inputs/NCASES').read_text())
        return (set(listed) == bugs == set(reasons) and len(listed) == len(bugs)
                and n == values['N_total']
                and f"{values['target']}/{values['N_scored']}" in text)
    check('target-spec-bugs', target)
    return bool(failed)


if __name__ == '__main__':
    raise SystemExit(run())
