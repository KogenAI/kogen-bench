#!/usr/bin/python3
# Static command audit: log permitted network activity; flag provider calls and
# protected outside reads. Frozen snapshot/receipt integrity checks follow.
import json, glob, os, re, shlex, sys
from pathlib import Path
from validity import tree_hash, file_hash
from receipts import collect
from mode_policy import read_mode
from command_policy import executable_text, kogen_touch, provider_call, network_execution
R = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser('~')
network = re.compile(r"\b(?:curl|wget|httpie|https?|ssh|scp|rsync)\b|\bgit\b[^;\n]*\b(?:clone|fetch|pull|ls-remote)\b|\bcargo\b[^;\n]*\b(?:add|install|fetch|build|check|test|update)\b|\bgo\b[^;\n]*\b(?:get|install|download|tidy)\b|\b(?:bun|npm|pnpm|yarn)\b[^;\n]*\b(?:add|install|ci|update|dlx|exec)\b|\bmix\s+(?:deps\.(?:get|update)|hex|local\.hex)|\bgleam\s+(?:add|deps|build)|\b(?:pip3?|uv|gem|bundle|brew)\b[^;\n]*\b(?:install|add|sync|update)\b|https?://|\b(?:requests|urllib|fetch|urlopen|httpc|reqwest)\b", re.I)
read = re.compile(r"\b(?:cat|head|tail|less|more|rg|grep|find|ls|stat|du|cp|sed|awk|source|readlink|realpath|open|read_text|read_bytes|readFile|readFileSync|File\.read|File\.stream)\b|(?:^|[;&]\s*)\.\s|<(?!<)")


def outside_reads(command, arm):
    command = '\n'.join(segment for segment in re.split(r'[;\n]|&&|\|\|', command)
                        if not re.match(r'^\s*(?:echo|printf)\b', segment))
    if not read.search(command):
        return []
    base = Path(R, arm).resolve()
    py_kits = {Path(R).parent.joinpath('race5-py-kit').resolve(),
               Path(os.environ.get('RACE5_PY_KIT_DIR', str(Path(R).parent/'race5-py-kit'))).resolve()}
    expanded = command.replace('${HOME}', home).replace('$HOME', home)
    # Shell words plus path literals embedded in Python/JS/etc. Resolve ../ and
    # symlinks before deciding whether a protected location is outside the arm.
    try:
        words = shlex.split(expanded, comments=True)
    except ValueError:
        words = expanded.split()
    candidates = words + re.findall(r"[\"']([^\"'\n]+)[\"']", expanded)
    candidates += re.findall(r"(?:~?/|\.\.?/)[^\s\"'<>;|()]+", expanded)
    found = []
    for raw in candidates:
        raw = raw.strip(';,()')
        if not raw or raw.startswith('-') or '://' in raw:
            continue
        if not ('/' in raw or raw.startswith('.codex')):
            continue
        path = Path(os.path.expanduser(raw))
        if not path.is_absolute():
            path = base / path
        path = path.resolve()
        if path == base or base in path.parents:
            continue
        parts = path.parts
        protected_storage = (any(p.startswith('.codex') for p in parts)
                             or any(p in ('Areas', 'iCloud', 'CloudDocs', 'Mobile Documents') for p in parts)
                             or Path(home, 'Library') == path or Path(home, 'Library') in path.parents)
        if not protected_storage and (any(path == kit or kit in path.parents for kit in py_kits)):
            continue
        protected = (any(p.startswith('.codex') for p in parts)
                     or 'Mobile Documents' in parts or 'CloudDocs' in parts
                     or 'iCloud' in parts or 'Areas' in parts
                     or (Path(home, 'Library') == path or Path(home, 'Library') in path.parents)
                     or any(re.fullmatch(r'race[0-9]+(?:[-_].*)?', p) for p in parts if p not in ('race3-kit', 'race5-py-kit'))
                     or any(Path(R, a) == path or Path(R, a) in path.parents
                            for a in Path(R, 'ARMS').read_text().split() if a != arm))
        if protected:
            found.append(str(path))
    return sorted(set(found))


flags = []
try:
    mode = read_mode(R)
    decision = Path(R, 'DECISION-RULE-v5.md')
    if decision.is_file() and ('## MODE: ' + mode + '\n') not in decision.read_text():
        flags.append('FLAG harness VOIDING MODE differs from decision rule')
except ValueError as error:
    flags.append('FLAG harness VOIDING invalid MODE: ' + str(error))
    mode = 'sealed'  # Continue auditing under the stricter policy.
logs = {a: [] for a in Path(R, 'ARMS').read_text().split()}
for f in sorted(glob.glob(R + '/out/*/turn-*.jsonl')):
    lang = Path(f).parent.name
    for number, line in enumerate(open(f, errors='ignore'), 1):
        try:
            e = json.loads(line)
        except (ValueError, TypeError):
            continue
        if not isinstance(e, dict):
            continue
        it = e.get('item') or e.get('payload') or (e if str(e.get('type', '')).startswith('web_search') else {})
        if not isinstance(it, dict):
            continue
        cmd = it.get('command') or ''
        if not cmd and it.get('type') in ('function_call', 'tool_call') and re.search(r'exec_command|shell|run_command', str(it.get('name', ''))):
            arguments = it.get('arguments') or {}
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except ValueError:
                    arguments = {}
            if isinstance(arguments, dict):
                cmd = arguments.get('cmd') or arguments.get('command') or ''
        if isinstance(cmd, list):
            cmd = shlex.join(map(str, cmd))
        # Only agent-issued commands/tool invocations; never scan assistant text,
        # tool output, or Codex-client traffic for provider names.
        web_event = (str(it.get('type', '')).startswith('web_search')
                     or (it.get('type') in ('function_call', 'tool_call')
                         and re.search(r'web[._]?search|web[._]run', str(it.get('name', '')), re.I)))
        if not cmd and web_event:
            logs.setdefault(lang, []).append(json.dumps({'event': Path(f).name, 'line': number, 'web': it}, sort_keys=True))
            # Scan queries, result URLs and open/find actions, including nested lists.
            web_text = json.dumps(it, ensure_ascii=False)
            if kogen_touch(web_text):
                flags.append('FLAG %s %s VOIDING Kogen denylist web_search event line %s' % (lang, Path(f).name, number))
            if mode == 'sealed':
                flags.append('FLAG %s %s VOIDING SEALED web_search event line %s' % (lang, Path(f).name, number))
        if not isinstance(cmd, str) or not cmd:
            continue
        if network.search(cmd):
            logs.setdefault(lang, []).append(json.dumps({'event': Path(f).name, 'line': number, 'command': cmd}, sort_keys=True))
        reasons = []
        executable = executable_text(cmd)
        if kogen_touch(cmd):
            reasons.append('VOIDING Kogen denylist command')
        if provider_call(cmd):
            reasons.append('VOIDING real model provider call')
        if mode == 'sealed' and network_execution(cmd):
            reasons.append('VOIDING SEALED network/download command')
        if outside_reads(executable, lang):
            reasons.append('protected outside read')
        if reasons:
            flags.append('FLAG %s %s %s: %s' % (lang, Path(f).name, ', '.join(reasons), cmd[:400]))
Path(R, 'out').mkdir(exist_ok=True)
for arm, rows in logs.items():
    # Rebuild deterministically from events, avoiding duplicates on repeat audits.
    Path(R, 'out', 'network-' + arm + '.log').write_text(''.join(row + '\n' for row in rows))
root = Path(R)
frozen = {name: tree_hash(root / 'inputs' / name) for name in ('spec', 'conformance')}
frozen['target'] = file_hash(root / 'TARGET.md')
for snapshot in sorted((root / 'snapshots').glob('*')):
    if not snapshot.is_dir(): continue
    for arm in (root / 'ARMS').read_text().split():
        if not (snapshot / arm).is_dir():
            stopped = snapshot / 'STOPPED_ARMS'
            omitted = stopped.read_text().split() if stopped.exists() else []
            if snapshot.name == f'TARGET-{arm}' or snapshot.name == 'FINAL' or (snapshot.name.startswith('T+') and arm not in omitted):
                flags.append('FLAG %s %s arm snapshot missing' % (arm, snapshot.name))
            continue
        for name, sha in frozen.items():
            marker = snapshot / arm / ('.%s.sha' % name)
            got = marker.read_text().strip() if marker.is_file() else 'missing'
            if got != sha:
                flags.append('FLAG %s %s %s hash expected=%s actual=%s' % (arm, snapshot.name, name, sha, got))
            if name == 'target':
                target = snapshot / arm / 'TARGET.md'
                if not target.is_file() or file_hash(target) != sha:
                    flags.append('FLAG %s %s TARGET.md content changed or missing' % (arm, snapshot.name))
flags.extend(collect(root))
for flag in flags: print(flag)
print('audit done')
sys.exit(bool(flags))
