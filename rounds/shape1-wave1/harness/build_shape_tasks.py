#!/usr/bin/env python3
"""Package public-only shaping tasks using the existing overlay builder."""
import json
import shutil
import subprocess
import sys
from shape_common import ROOT, LANGS, digest, snapshot, task_source, write_json

INSTRUCTION = b"""# Shape the feature as executable acceptance tests

Specify the following public task. Do not implement the feature.
Write INTENT.md with uniquely numbered observable acceptance criteria, and
native executable tests under acceptance/: Rust cargo test with a standalone
acceptance/Cargo.toml; Go go test with an acceptance package; TS/Bun bun test
with *.test.ts files. Use native assertions (Rust assert!, Go testing.T
Error/Fatal, Bun expect). Runtime panics, crashes and throws do not prove a
failed acceptance assertion. Exercise the CLI as a black box. Scoring supplies
SHAPE_APP (the already built bin/app) and SHAPE_REPO (public fixture directory).
Use temporary directories for test data. Do not rebuild, replace or modify the
application. Do not change existing repository files. A Quint model is optional
and must live under acceptance/. Only inspect this repository and the public
prompt; do not look for evaluation material or other workspaces.

The task's public goal and constraints follow verbatim:

"""
STUB = b'#!/bin/sh\nprintf \'%s\\n\' \'{"pass_":false,"tests":0,"failures":0,"errors":0,"skipped":0,"tests_ran":false,"stage":"shape-not-scored"}\'\n'


def build():
    plan = json.loads((ROOT/'plan.json').read_text())
    targets = []
    for row in plan['tasks']:
        task = row['id']; source = task_source(task)
        target = ROOT/'tasks'/('shape-'+task)
        if target.exists():
            raise ValueError('refusing to replace an existing shape task')
        manifest = {'task':task, 'languages':{}}
        for lang in LANGS:
            base = source/'bases'/lang
            count = subprocess.check_output(['git','-C',str(base),'rev-list','--all','--count'],text=True).strip()
            if count != '1':
                raise ValueError('base history must contain exactly one public commit')
            copied = target/'bases'/lang
            shutil.copytree(base,copied,symlinks=True,ignore=shutil.ignore_patterns(
                'target','bin','.cache','node_modules','__pycache__'))
            if snapshot(copied) != row['source_snapshots']['bases'][lang]:
                raise ValueError('public base changed since the original registration')
            prompt = source/f'prompt-{lang}.md'
            if digest(prompt) != row['prompt_sha256'][lang]:
                raise ValueError('original public prompt changed')
            combined = target/f'prompt-{lang}.md'
            combined.write_bytes(INSTRUCTION+prompt.read_bytes())
            # Required by the existing builder; deliberately no solution files.
            (target/'reference'/lang).mkdir(parents=True)
            manifest['languages'][lang] = {'original_prompt_sha256':digest(prompt),
                'shaping_prompt_sha256':digest(combined),'base_snapshot':snapshot(copied)}
        (target/'hidden').mkdir()
        grader = target/'grader-entrypoint'; grader.write_bytes(STUB); grader.chmod(0o755)
        write_json(target/'shape-task-manifest.json',manifest)
        targets.append(target.name)
    out = ROOT/'overlays'; out.mkdir()
    subprocess.run([sys.executable,str(ROOT.parent/'core4/tools/build_overlay.py'),
        '--root',str(ROOT/'tasks'),'--family','shape1',*targets],cwd=out,check=True)
    write_json(out/'MANIFEST.json',{p.name:digest(p) for p in sorted(out.glob('*.tar'))})


if __name__ == '__main__':
    build()
