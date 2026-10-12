#!/usr/bin/env python3
"""Nonblank, noncomment physical LOC, with strings preserved and docs excluded."""
from pathlib import Path
import argparse
import io
import json
import os
import re
import tokenize
from arch_config import LOC_EXCLUDES, dump

LANGUAGES = {'.go': 'Go', '.ex': 'Elixir', '.exs': 'Elixir', '.py': 'Python',
             '.sh': 'Shell', '.bash': 'Shell', '.zsh': 'Shell', '.js': 'JavaScript',
             '.ts': 'TypeScript', '.rs': 'Rust', '.c': 'C', '.h': 'C', '.cpp': 'C++'}
GENERATED = re.compile(r'(?im)^\s*(?://|#|/\*|\*)\s*(?:code generated\b|@generated\b|generated (?:code|file)\b).*?(?:do not edit|$)')

def code_lines(text, language):
    if language == 'Python':
        kept = set()
        try:
            for token in tokenize.generate_tokens(io.StringIO(text).readline):
                if token.type not in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE,
                                      tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER):
                    kept.update(range(token.start[0], token.end[0] + 1))
            return sum(bool(line.strip()) and n in kept for n, line in enumerate(text.splitlines(), 1))
        except (tokenize.TokenError, IndentationError):
            raise ValueError('Cannot reliably count malformed Python')
    if language == 'Elixir':
        # Treat @doc/@moduledoc/@typedoc heredocs and single-line literals as documentation.
        text = re.sub(r'(?ms)^\s*@(moduledoc|doc|typedoc)\s+(?:~[sS])?("""|\x27\x27\x27).*?\2',
                      lambda m: '\n' * m[0].count('\n'), text)
        text = re.sub(r'(?m)^\s*@(moduledoc|doc|typedoc)\s+(?:false|"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27)\s*$', '', text)
    hash_comments = language in ('Elixir', 'Shell')
    output, i, quote, block = [], 0, None, False
    while i < len(text):
        char = text[i]
        if block:
            if text.startswith('*/', i):
                block = False
                i += 2
            else:
                if char == '\n':
                    output.append('\n')
                i += 1
        elif quote:
            output.append(char)
            if char == '\\' and quote != '`' and i + 1 < len(text):
                output.append(text[i + 1]); i += 2
            elif text.startswith(quote, i):
                if len(quote) == 3:
                    output.extend(text[i + 1:i + 3]); i += 3
                else:
                    i += 1
                quote = None
            else:
                i += 1
        elif (hash_comments and char == '#') or (not hash_comments and text.startswith('//', i)):
            end = text.find('\n', i)
            i = len(text) if end < 0 else end
        elif not hash_comments and text.startswith('/*', i):
            block = True; i += 2
        elif text.startswith('"""', i) or text.startswith("'''", i):
            quote = text[i:i + 3]; output.extend(quote); i += 3
        elif char in ('"', "'", '`'):
            quote = char; output.append(char); i += 1
        else:
            output.append(char); i += 1
    return sum(bool(line.strip()) for line in ''.join(output).splitlines())

def count(root, generated_paths=()):
    root = Path(root).resolve()
    totals, files, generated = {}, [], []
    for base, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in LOC_EXCLUDES and not (Path(base) / d).is_symlink())
        for name in sorted(names):
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            language = LANGUAGES.get(path.suffix)
            if path.is_symlink() or not language or name.startswith('.kit-'):
                continue
            if any(rel == p or rel.startswith(p.rstrip('/') + '/') for p in generated_paths):
                generated.append(rel); continue
            text = path.read_text()
            if GENERATED.search('\n'.join(text.splitlines()[:20])):
                generated.append(rel); continue
            loc = code_lines(text, language)
            totals[language] = totals.get(language, 0) + loc
            files.append(dict(path=rel, language=language, loc=loc))
    return dict(by_language=totals, files=files, excluded_generated=generated,
                excluded_components=sorted(LOC_EXCLUDES),
                method='nonblank noncomment physical lines; tests and kit seed source included; docs/ and spec/ excluded')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('workspace', type=Path)
    p.add_argument('--generated-manifest', type=Path)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    generated = json.loads(args.generated_manifest.read_text()) if args.generated_manifest else []
    dump(args.out, count(args.workspace, generated))

if __name__ == '__main__':
    main()
