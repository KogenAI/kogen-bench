"""Static event-command policy. This is not packet capture or runtime tracing."""
import ast
import re
import shlex

PROVIDER = re.compile(r"(?<![a-z0-9.-])(?:api\.openai\.com|auth\.openai\.com|chatgpt\.com/backend-api|api\.anthropic\.com|generativelanguage\.googleapis\.com|aiplatform\.googleapis\.com|[a-z0-9.-]+\.openai\.azure\.com|[a-z0-9.-]+\.services\.ai\.azure\.com|bedrock-runtime\.[a-z0-9-]+\.amazonaws\.com|api\.(?:mistral\.ai|groq\.com|deepseek\.com|cohere\.(?:ai|com)|together\.(?:xyz|ai)|perplexity\.ai|fireworks\.ai|x\.ai)|openrouter\.ai/api)(?=$|[/\s\"':?])", re.I)
KOGEN = re.compile(r'KogenAI|(?<![a-z0-9.-])(?:www\.|bench\.)?kogen\.dev(?![a-z0-9.-])|github\.com[/:][^\s/\"\'<>]+/kogen[^\s\"\'<>]*', re.I)
HTTP_CALL = re.compile(r'\b(?:curl|wget|http|httpie|requests|urllib|urlopen|fetch|httpc|reqwest|ureq|httpx|aiohttp|axios|OpenAI|Anthropic)\b|\b(?:https?|net|Req|HTTPoison)\.(?:get|post|request)|\b(?:chat|responses|messages)\.create\b', re.I)
CODE_HTTP = re.compile(r'\b(?:fetch|urlopen|OpenAI|Anthropic)\s*\(|\b(?:requests|httpx|axios|https?|urllib\.request|Req|HTTPoison)\.(?:get|post|request|urlopen)!?\s*\(|\b(?:httpc|reqwest|ureq|aiohttp)\b[^\n]*\(', re.I)
PACKAGE = re.compile(r'^\s*(?:(?:env|command|sudo)\s+)?(?:git\s+(?:clone|fetch|pull|ls-remote)|cargo\s+(?:add|install|fetch|update)|go\s+(?:get|install|mod\s+(?:download|tidy))|(?:bun|npm|pnpm|yarn)\s+(?:add|install|ci|update|dlx)|mix\s+(?:deps\.(?:get|update)|hex|local\.hex)|gleam\s+(?:add|deps)|(?:pip3?|uv|gem|bundle|brew)\s+(?:install|add|sync|update))\b', re.I)
DATA_COMMAND = re.compile(r'^\s*(?:echo|printf|rg|grep|cat|head|tail|tee|sed|awk)\b')


def kogen_touch(value):
    # The local suite path conformance/bin/kogen-conformance does not match:
    # only the organization, remote repository URLs and domain names are denied.
    return bool(KOGEN.search(value))


def executable_text(command):
    """Drop data heredocs of cat/tee, retain interpreter heredocs and substitutions."""
    result, delimiters = [], []
    for line in command.splitlines():
        if delimiters:
            delimiter, quoted = delimiters[0]
            if line.strip() == delimiter:
                delimiters.pop(0)
            elif not quoted:
                for substitution in re.findall(r'\$\((.*?)\)|`(.*?)`', line):
                    result.extend(part for part in substitution if part)
            continue
        matches = list(re.finditer(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z_0-9]*)\1", line))
        if matches and re.match(r'^\s*(?:cat|tee)\b', line):
            delimiters = [(m[2], bool(m[1])) for m in matches]
        result.append(line)
    return '\n'.join(result)


def _python_requests(script):
    """Inspect executed call expressions, not string literals containing source."""
    try:
        tree = ast.parse(script)
    except SyntaxError:
        return None
    values = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    values[target.id] = node.value.value
    def strings(node):
        found = []
        for part in ast.walk(node):
            if isinstance(part, ast.Constant) and isinstance(part.value, str):
                found.append(part.value)
            elif isinstance(part, ast.Name) and part.id in values:
                found.append(values[part.id])
        return found
    requests = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = ast.unparse(node.func)
        if (re.search(r'(?:requests|urllib|httpx|aiohttp|http\.client|OpenAI|Anthropic)', name, re.I)
                or re.search(r'\.(?:get|post|request|urlopen|create)$', name)):
            requests.extend(strings(node))
        elif re.search(r'(?:subprocess\.(?:run|call|Popen|check_output|check_call)|os\.(?:system|popen)|exec|eval)$', name):
            requests.extend(value for value in strings(node) if HTTP_CALL.search(value) or '://' in value)
    return requests


def _javascript_requests(script):
    """Keep JS code separate from literal source text passed to file writers."""
    literals = {}
    def mask(match):
        token = '__literal_' + str(len(literals)) + '__'
        literals[token] = match[0][1:-1]
        return token
    code = re.sub(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|`(?:\\.|[^`\\])*`", mask, script)
    bindings = dict(re.findall(r'\b([A-Za-z_$][\w$]*)\s*=\s*(__literal_\d+__)', code))
    requests = []
    for match in CODE_HTTP.finditer(code):
        arguments = code[match.end():].split(')', 1)[0]
        tokens = re.findall(r'\b[A-Za-z_$][\w$]*\b', arguments)
        for token in tokens:
            value = literals.get(bindings.get(token, token))
            if value is not None:
                requests.append(value)
    return requests


def executed_requests(command):
    """Return destinations mentioned in executed HTTP-client command/code contexts."""
    text = executable_text(command)
    # Resolve simple URL bindings used by a later client command. Source file
    # heredocs have already been removed, so their assignments do not contribute.
    bindings = {}
    for binding in re.finditer(r"(?:^|[;\n])\s*(?:export\s+)?([A-Za-z_]\w*)=(['\"]?)(https?://[^\s;\"']+)\2", text):
        bindings[binding[1]] = binding[3]
    for name, value in bindings.items():
        text = re.sub(r'\$\{' + re.escape(name) + r'\}|\$' + re.escape(name) + r'\b', lambda _: value, text)
    found = []
    # Interpreter heredocs are a single program, even when URL/call span lines.
    heredoc = re.search(r"(?:^|\n)\s*(?:python[0-9.]*)(?:\s+-)?\s+<<-?\s*['\"]?([A-Za-z_]\w*)['\"]?[^\n]*\n(.*?)\n\1(?:\n|$)", text, re.S)
    if heredoc:
        requests = _python_requests(heredoc[2])
        found.extend(requests or [])
        text = text[:heredoc.start()] + text[heredoc.end():]
    # Keep quoted script strings intact; split only shell control operators.
    try:
        lexer = shlex.shlex(text, posix=True, punctuation_chars=';&|\n')
        lexer.whitespace = ' \t\r'
        lexer.whitespace_split = True
        lexer.commenters = '#'
        segments, segment = [], []
        for word in lexer:
            if word and all(char in ';&|\n' for char in word):
                if segment:
                    segments.append(segment); segment = []
            else:
                segment.append(word)
        if segment:
            segments.append(segment)
    except ValueError:
        segments = [text.split()]
    for words in segments:
        if not words:
            continue
        # Shell wrappers and environment bindings are not the invoked program.
        while words and (words[0] in ('env', 'command', 'sudo', 'do', 'then', 'exec')
                         or re.fullmatch(r'[A-Za-z_]\w*=.*', words[0])):
            words = words[1:]
        if not words:
            continue
        joined = ' '.join(words)
        program = words[0].rsplit('/', 1)[-1]
        # Command substitution executes even inside an echo/file-write command.
        for substitution in re.findall(r'\$\((.*?)\)|`(.*?)`', joined, re.S):
            found.extend(executed_requests(next(part for part in substitution if part)))
        shell_flag = next((word for word in words[1:] if re.fullmatch(r'-[a-z]*c[a-z]*', word)), None)
        if program in ('sh', 'bash', 'zsh') and shell_flag:
            index = words.index(shell_flag) + 1
            if index < len(words):
                found.extend(executed_requests(words[index]))
                continue
        if re.fullmatch(r'python[0-9.]*', program) and '-c' in words:
            index = words.index('-c') + 1
            if index < len(words):
                requests = _python_requests(words[index])
                if requests is not None:
                    found.extend(requests)
                    continue
        if program in ('node', 'bun', 'deno'):
            script_flag = next((word for word in words if word in ('-e', '--eval')), None)
            if script_flag and words.index(script_flag) + 1 < len(words):
                found.extend(_javascript_requests(words[words.index(script_flag) + 1]))
                continue
        if DATA_COMMAND.match(joined):
            continue
        # Node source writes: discard payload literals of common file-writing APIs.
        joined = re.sub(r"(?:writeFileSync|writeFile|write_text)\([^,]+,\s*(['\"])(?:(?!\1).)*?\1\s*\)", '', joined)
        if (program in ('curl', 'wget', 'http', 'httpie') or CODE_HTTP.search(joined)
                or (program in ('timeout', 'gtimeout', 'xargs')
                    and any(word in ('curl', 'wget', 'http', 'httpie') for word in words[1:]))):
            found.append(joined)
    return found


def provider_call(command):
    return any(PROVIDER.search(request) for request in executed_requests(command))


def network_execution(command):
    text = executable_text(command)
    return bool(executed_requests(text) or any(PACKAGE.search(segment) for segment in re.split(r'[;\n]|&&|\|\|', text)))
