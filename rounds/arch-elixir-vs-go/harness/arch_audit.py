"""ARCH voiding audit, reusing lever command-policy recognition."""
from pathlib import Path
import json
import os
import re
import shlex
from arch_config import MODEL, EFFORT
from arch_command_policy import kogen_touch, provider_call, network_execution

CONTEXT = re.compile(r'(?<!\\)"type"\s*:\s*"turn_context"')
READ = re.compile(r'\b(?:cat|head|tail|less|more|rg|grep|find|ls|stat|cp|sed|awk|source|readlink|open|read_text|read_bytes|readFile|File\.read)\b|(?:^|[;&]\s*)\.\s|<(?!<)')

def outside_reads(command, workspace, allowed_roots=()):
    if not READ.search(command):
        return []
    workspace = Path(workspace).resolve()
    expanded = command.replace('${PWD}', str(workspace)).replace('$PWD', str(workspace))
    expanded = expanded.replace('${HOME}', str(Path.home())).replace('$HOME', str(Path.home()))
    try:
        words = shlex.split(expanded, comments=True)
    except ValueError:
        words = expanded.split()
    candidates = words + re.findall(r'["\x27]([^"\x27\n]+)["\x27]', expanded)
    candidates += re.findall(r'(?:~?/|\.\.?/)[^\s"\x27<>;|()]+', expanded)
    found = []
    allowed = [Path(p).resolve() for p in allowed_roots]
    home = Path.home().resolve()
    system_roots = [Path('/Library/Developer'), Path('/usr'), Path('/opt/homebrew'), Path('/System'),
                    home / '.local/share/mise']
    kit_parts = re.compile(r'^race\d+-kit$')
    for value in candidates:
        value = value.strip(';,()')
        if not value or value.startswith('-') or '://' in value or '/' not in value:
            continue
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = workspace / path
        path = path.resolve()
        if path == workspace or workspace in path.parents:
            continue
        if any(path == root or root in path.parents for root in allowed):
            continue
        if any(path == root or root in path.parents for root in system_roots):
            continue
        if any(kit_parts.match(part) for part in path.parts):
            continue
        protected = (workspace.parent == path or workspace.parent in path.parents or
                     path == home or home in path.parents or
                     any(part.startswith('.codex') or part in ('.aws', 'Areas', 'CloudDocs', 'Mobile Documents', 'iCloud')
                         for part in path.parts) or
                     any(re.match(r'^(?:arch|lever|race\d+)(?:-|$)', part) for part in path.parts))
        if protected:
            found.append(str(path))
    return sorted(set(found))

def command_from_event(event):
    item = event.get('item') or event.get('payload') or event
    if not isinstance(item, dict):
        return None, None
    kind = item.get('type', '')
    if kind == 'command_execution':
        return item.get('command'), item
    if kind in ('function_call', 'tool_call'):
        name = str(item.get('name', ''))
        if 'apply_patch' in name:
            arguments = item.get('arguments') or ''
            text = arguments if isinstance(arguments, str) else json.dumps(arguments)
            if re.search(r'\*\*\* (?:Update|Add|Delete) File:\s*(?:[^\n]*?/)?spec/', text):
                return '__ARCH_FROZEN_SPEC_WRITE__', item
        if re.search(r'spawn_agent|followup_task|collaboration', name):
            return '__ARCH_FORBIDDEN_DELEGATION__', item
        if re.search(r'exec_command|shell|run_command', name):
            arguments = item.get('arguments') or {}
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except ValueError:
                    arguments = {}
            if isinstance(arguments, dict):
                return arguments.get('cmd') or arguments.get('command'), item
        if re.search(r'web[._]?search|web[._]run', name, re.I):
            return None, item
    if str(kind).startswith('web_search'):
        return None, item
    return None, None

def audit_events(paths, workspace, allowed_roots=()):
    flags, network_commands = [], 0
    for path in paths:
        for number, line in enumerate(Path(path).read_text(errors='replace').splitlines(), 1):
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if not isinstance(event, dict):
                continue
            command, item = command_from_event(event)
            reasons = []
            if command == '__ARCH_FORBIDDEN_DELEGATION__':
                reasons.append('reviewer/subagent delegation')
            elif command == '__ARCH_FROZEN_SPEC_WRITE__':
                reasons.append('frozen spec modification')
            elif command:
                if isinstance(command, list):
                    command = shlex.join(map(str, command))
                if not isinstance(command, str):
                    continue
                network_commands += int(network_execution(command))
                if kogen_touch(command):
                    reasons.append('Kogen denylist command')
                if provider_call(command):
                    reasons.append('real model-provider call')
                if re.search(r'(?:>>?\s*["\x27]?(?:\./)?spec/|\bsed\s+-i[^\n]*\bspec/|\brm\s+[^\n]*\bspec/)', command):
                    reasons.append('frozen spec modification')
                if outside_reads(command, workspace, allowed_roots):
                    reasons.append('protected outside read')
                if re.search(r'\b(?:codex\s+(?:exec|review|resume|fork)|claude\b|aider\b)', command):
                    reasons.append('additional model session')
            elif item and kogen_touch(json.dumps(item)):
                reasons.append('Kogen denylist web/tool access')
            for reason in reasons:
                flags.append(dict(file=Path(path).name, line=number, reason=reason))
    return dict(flags=flags, permitted_network_commands=network_commands,
                enforcement='static command/event audit; sampled CPU membership; no OS-complete access or packet tracing')

def actual_model_receipts(sessions, thread_ids, workspace, cutoff):
    from arch_tokens import timestamp
    contexts, paths = [], []
    for thread_id in thread_ids:
        matches = list(Path(sessions).rglob('*' + thread_id + '*.jsonl'))
        if len(matches) != 1:
            raise ValueError('Missing/ambiguous model receipt rollout: ' + thread_id)
        paths += matches
        for line in matches[0].read_text().splitlines():
            if not CONTEXT.search(line):
                continue
            event = json.loads(line)
            if event.get('type') != 'turn_context' or timestamp(event['timestamp']) > timestamp(cutoff):
                continue
            payload = event['payload']
            reasoning = payload.get('reasoning') or {}
            effort = payload.get('effort') or payload.get('reasoning_effort') or payload.get('model_reasoning_effort')
            if isinstance(reasoning, dict):
                effort = effort or reasoning.get('effort')
            contexts.append(dict(thread_id=thread_id, model=payload.get('model'), effort=effort,
                                 cwd=payload.get('cwd'), timestamp=event['timestamp']))
    if not contexts or any(row['model'] != MODEL or row['effort'] != EFFORT or
                           Path(row['cwd'] or '/missing').resolve() != Path(workspace).resolve() for row in contexts):
        raise ValueError('Wrong or missing actual model/effort/cwd receipt')
    if {row['thread_id'] for row in contexts} != set(thread_ids):
        raise ValueError('A session has no actual model receipt')
    return contexts, paths
