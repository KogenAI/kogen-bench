"""Reject lane patches and settings that carry task-specific content (`lanes-leakcheck`).

A lane change must be general. This compares each lane's patch text and settings with what only
the tasks know: their ids and names (also as `task_name`, `TaskName`, `task name`), identifiers and
string literals from the start, reference and wrong trees and the hidden tests, whole hidden-test
lines, and word n-grams of earlier runs' failure output. Private files are read into memory to
compare and never written.

Words the task language and Kogen itself use are not task content: tokens and n-grams that also
occur in the Kogen source the lane is built on (`--kogen DIR`, default: the harness's clone at that
lane's sha), or in the patch's own context and removed lines, never count. Without a Kogen source
the check is stricter, not looser. Failure output is read from every cell whose `evaluation.json`
does not say `all_passed: true` (ungraded and shape cells included); passing cells hold nothing to
copy. A task folder without `task.toml`, `start/` or `evaluator/`, or a runs folder without
`cells/`, is an error (exit 2), never a clean result.

Only added text can leak. Text already present verbatim in the base prompt surface (the prompt files
under cli/agent/prompts/ at the lane's sha, plus the patch's own context and removed lines: the prompt
every arm sees before the patch) is not a leak, however the patch rewrites or moves the line around it.
So a string literal or hidden-test line is skipped when it occurs, whitespace folded, anywhere in that
prompt surface. The substring rule deliberately does not extend to the rest of Kogen's source: a task
made from a reverted Kogen feature can have its solution in the source at the lane's sha. The older
whole-identifier and whole-literal exemptions for Kogen's source are unchanged. A phrase that is new in
the patch is still compared. There are no per-hit exemptions.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import tomllib

from . import common, experiment

MIN_IDENT = 8  # shortest identifier compared; it must be snake_case or camelCase
MIN_LITERAL = 10  # shortest string literal compared (after whitespace is folded)
MIN_TEST_LINE = 24  # shortest hidden-test line compared
NGRAM = 8  # words per n-gram of run output
NGRAM_HITS = 3  # distinct shared n-grams that make a hit: a copied run of NGRAM + 2 words
MAX_FILE = 1 << 20
MAX_RUN_TEXT = 8 << 20  # per runs folder
RUN_FILES = ("evaluation.json", "stdout.txt", "stderr.txt")

_IDENT = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z_][A-Za-z0-9_]{%d,}" % (MIN_IDENT - 1))  # not `1_048_576`
_LITERAL = re.compile(r'"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\'|`([^`\n]*)`')
_WORD = re.compile(r"[a-z0-9_]+")
_SPECIFIC = re.compile(r"_|[a-z][A-Z]")


def _fold(text):
    return " ".join(text.split())


def _read(path, skipped=None):
    """Text of a file; None (and `path` added to `skipped`) when too large or not UTF-8."""
    try:
        if os.path.getsize(path) > MAX_FILE:
            raise UnicodeError("too large")
        with open(path, encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeError):
        if skipped is not None:
            skipped.append(path)
        return None


def _files(root, skipped=None):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            if not os.path.islink(path):
                text = _read(path, skipped)
                if text is not None:
                    yield os.path.relpath(path, root), text


def _is_diff(lines):
    return any(line.startswith("+++ ") for line in lines)


def _change_text(patch):
    """What a lane adds: the `+` lines and target paths of a diff, else the whole text."""
    lines = patch.splitlines()
    if not _is_diff(lines):
        return patch
    added = [line[1:] for line in lines if line.startswith("+") and not line.startswith("+++")]
    paths = [line[4:].split("\t")[0] for line in lines if line.startswith("+++ ")]
    paths += [line[len("rename to "):] for line in lines if line.startswith("rename to ")]
    return "\n".join(added + [p[2:] if p[:2] in ("a/", "b/") else p for p in paths if p != "/dev/null"])


def _context_text(patch):
    """What a diff keeps or removes: its context and `-` lines (they are Kogen's own words)."""
    lines = patch.splitlines()
    if not _is_diff(lines):
        return ""
    return "\n".join(line[1:] for line in lines
                     if line[:1] in (" ", "-") and not line.startswith(("--- ", "-- ")))


def _tokens(text):
    """`(identifiers, literals)` of a text: task-specific-looking names and folded string literals."""
    idents = {i for i in _IDENT.findall(text) if _SPECIFIC.search(i)}
    literals = set()
    for m in _LITERAL.finditer(text):
        lit = _fold("".join(g for g in m.groups() if g))
        if len(lit) >= MIN_LITERAL and re.search(r"[A-Za-z]", lit):
            literals.add(lit)
    return idents, literals


def _words(text):
    return " ".join(_WORD.findall(text.lower()))


class Known:
    """Words that are not task content: Kogen's source and the patch's own context."""

    def __init__(self, texts=(), surface=()):
        self.idents, self.literals, words = set(), set(), []
        folded = [_fold(text) for text in surface]
        for text in texts:
            i, lit = _tokens(text)
            self.idents |= i
            self.literals |= lit
            words.append(_words(text))
        self.words = "\n".join(words)
        self.folded = "\n".join(folded)

    def has_text(self, text):
        """True when the whitespace-folded `text` occurs verbatim in the base prompt surface."""
        return text in self.folded

    def has_gram(self, gram):
        return gram in self.words


class Reference:
    """What the tasks know, indexed for lookup. `source` strings never include file content."""

    def __init__(self):
        self.skipped = []
        self.names = {}  # lowercase id or name -> source
        self.idents = {}
        self.literals = {}  # folded literal -> source
        self.lines = {}  # folded hidden-test line -> source

    def add_task(self, tasks, task_id):
        root = os.path.join(tasks, task_id)
        for part, is_dir in (("", True), ("task.toml", False), ("start", True), ("evaluator", True)):
            path = os.path.join(root, part)
            if not (os.path.isdir(path) if is_dir else os.path.isfile(path)):
                raise ValueError(f"task {task_id}: {part or 'folder'} not found under {tasks}")
        self.names.setdefault(task_id.lower(), f"task id {task_id}")
        try:
            with open(os.path.join(root, "task.toml"), "rb") as f:
                name = tomllib.load(f).get("name")
        except (OSError, ValueError) as e:
            raise ValueError(f"task {task_id}: task.toml: {e}") from None
        if isinstance(name, str) and name:
            self.names.setdefault(name.lower(), f"task {task_id} name")
        trees = [("start", os.path.join(root, "start")), ("reference", os.path.join(root, "reference")),
                 ("hidden tests", os.path.join(root, "evaluator"))]
        wrong = os.path.join(root, "wrong")
        if os.path.isdir(wrong):
            trees += [(f"wrong/{w}", os.path.join(wrong, w)) for w in sorted(os.listdir(wrong))]
        for label, tree in trees:
            for rel, text in _files(tree, self.skipped):
                source = f"task {task_id} {label}: {rel}"
                idents, literals = _tokens(text)
                for ident in sorted(idents):
                    self.idents.setdefault(ident, source)
                for lit in sorted(literals):
                    self.literals.setdefault(lit, source)
                if label == "hidden tests":
                    for line in text.splitlines():
                        line = _fold(line)
                        if len(line) >= MIN_TEST_LINE:
                            self.lines.setdefault(line, source)


def _name_pattern(name):
    """The name in any spelling: `task-two`, `task_two`, `task two`, `taskTwo`, `TaskTwo`."""
    parts = [re.escape(p) for p in re.split(r"[-_ .]+", name) if p]
    return re.compile(r"(?<![A-Za-z0-9_-])" + r"[-_ ]?".join(parts) + r"(?![A-Za-z0-9_-])", re.I)


def _ngrams(text):
    words = _WORD.findall(text.lower())
    return {" ".join(words[i:i + NGRAM]) for i in range(len(words) - NGRAM + 1)}


def run_ngrams(run_dirs, notes=None):
    """`{n-gram: source}` over the failure output and run logs of earlier runs."""
    grams = {}
    for run in run_dirs:
        cells = os.path.join(run, "cells")
        if not os.path.isdir(cells):
            raise ValueError(f"runs folder {run} has no cells/")
        budget, skipped, cut = MAX_RUN_TEXT, [], False
        for dirpath, dirnames, filenames in os.walk(cells):
            dirnames.sort()
            if "result.json" in filenames and _passed(dirpath):
                dirnames[:] = []
                continue
            for name in sorted(filenames):
                rel = os.path.relpath(os.path.join(dirpath, name), cells).replace(os.sep, "/")
                if name not in RUN_FILES and "/run-log/" not in "/" + rel:
                    continue
                if budget <= 0:
                    cut = True
                    continue
                text = _read(os.path.join(dirpath, name), skipped)
                if text is None:
                    continue
                budget -= len(text)
                source = f"run {os.path.basename(os.path.normpath(run))}: {rel}"
                for g in _ngrams(text):
                    grams.setdefault(g, source)
        if notes is not None:
            if skipped:
                notes.append(f"run output skipped (over {MAX_FILE >> 20} MiB or not UTF-8): " + ", ".join(
                    os.path.relpath(p, run) for p in skipped[:5]) + (f" and {len(skipped) - 5} more" if len(skipped) > 5 else ""))
            if cut:
                notes.append(f"run {os.path.basename(os.path.normpath(run))}: over {MAX_RUN_TEXT >> 20} MiB of output; later cells not compared")
    return grams


def _passed(cell_dir):
    """True when the cell's `evaluation.json` says `all_passed: true`."""
    try:
        return common.read_json(os.path.join(cell_dir, "evaluation.json")).get("all_passed") is True
    except (OSError, ValueError, AttributeError):
        return False


PROMPT_SURFACE = "cli/agent/prompts/"


def kogen_texts(kogen, sha, notes=None):
    """`[(path, text)]` of the Kogen the lane builds on: a folder, else the harness's clone at `sha`."""
    if kogen:
        if not os.path.isdir(kogen):
            raise ValueError(f"--kogen {kogen}: not a folder")
        return list(_files(kogen))
    git_dir = os.path.join(common.lanes_home(), "kogen.git")
    texts = []
    if os.path.isdir(git_dir):
        with tempfile.TemporaryFile() as tar:
            code, _ = common.run(["git", "--git-dir", git_dir, "archive", "--format=tar", sha], stdout=tar,
                                 stderr=subprocess.DEVNULL, deadline_s=120)
            if not code:
                tar.seek(0)
                with tarfile.open(fileobj=tar) as t:
                    for m in t:
                        if m.isfile() and m.size <= MAX_FILE:
                            try:
                                texts.append((m.name, t.extractfile(m).read().decode("utf-8")))
                            except UnicodeError:
                                pass
    if not texts and notes is not None:
        notes.append(f"no Kogen source for {sha[:8]} (pass --kogen DIR): words Kogen shares with tasks may be flagged")
    return texts


def check_text(text, ref, grams=(), known=None):
    """Hits `(kind, what, source)` of one lane's change text against the reference."""
    known = known or Known()
    hits = []
    folded = _fold(text)
    for name, source in ref.names.items():
        if _name_pattern(name).search(text):
            hits.append(("task name", name, source))
    for ident in sorted(set(_IDENT.findall(text)) & ref.idents.keys() - known.idents):
        hits.append(("identifier", ident, ref.idents[ident]))
    for lit, source in ref.literals.items():
        if lit in folded and lit not in known.literals and not known.has_text(lit):
            hits.append(("string literal", lit, source))
    for line, source in ref.lines.items():
        if line in folded and not known.has_text(line):
            hits.append(("hidden-test line", line, source))
    shared = sorted(g for g in _ngrams(text) & grams.keys() if not known.has_gram(g)) if grams else []
    if len(shared) >= NGRAM_HITS:
        hits.append(("run output", f"{len(shared)} shared {NGRAM}-word runs, e.g. {shared[0]!r}", grams[shared[0]]))
    return hits


def check(exp_path, tasks, runs=(), kogen=None, notes=None):
    """`[(lane, kind, what, source)]` for every lane of the experiment.

    OSError when a patch is unreadable, ValueError when a task or runs folder is incomplete.
    Things worth a line to the user (skipped files, a missing Kogen source) are appended to `notes`.
    """
    exp = experiment.load(exp_path)
    if not os.path.isdir(tasks):
        raise ValueError(f"tasks folder {tasks} not found")
    ref = Reference()
    for task_id in exp["tasks"]:
        ref.add_task(tasks, task_id)
    if ref.skipped and notes is not None:
        rel = [os.path.relpath(p, tasks) for p in ref.skipped]
        notes.append(f"task files skipped (over {MAX_FILE >> 20} MiB or not UTF-8): " + ", ".join(rel[:5])
                     + (f" and {len(rel) - 5} more" if len(rel) > 5 else ""))
    grams = run_ngrams(runs, notes)
    kogen_by_sha = {}
    out = []
    for lane in exp["lanes"]:
        texts = [("settings", json.dumps(lane["settings"], sort_keys=True), "")]
        path = experiment.patch_path(exp_path, lane)
        if path:
            with open(path, encoding="utf-8", errors="replace") as f:
                raw = f.read()
            texts.append(("patch", _change_text(raw), _context_text(raw)))
        if lane["sha"] not in kogen_by_sha:
            kogen_by_sha[lane["sha"]] = kogen_texts(kogen, lane["sha"], notes)
        for where, text, context in texts:
            files = kogen_by_sha[lane["sha"]]
            surface = [text for path, text in files if path.startswith(PROMPT_SURFACE)]
            known = Known([text for _, text in files] + [context], surface + [context])
            for kind, what, source in check_text(text, ref, grams, known):
                out.append((f"{lane['name']} {where}", kind, what, source))
    return out


def format_hit(hit):
    where, kind, what, source = hit
    what = what if len(what) <= 80 else what[:77] + "..."
    return f"{where}: {kind} {what!r} (from {source})"


def main(argv=None):
    p = argparse.ArgumentParser(description="Reject lane patches and settings that contain task-specific content.")
    p.add_argument("experiment")
    p.add_argument("--tasks", default=os.environ.get("KOGEN_LANES_TASKS"), help="private tasks folder")
    p.add_argument("--kogen", metavar="DIR", help="Kogen source whose words never count (default: the harness's clone)")
    p.add_argument("--runs", nargs="*", default=[], metavar="DIR", help="earlier run folders whose failure output is compared")
    a = p.parse_args(argv)
    if not a.tasks:
        p.error("--tasks or KOGEN_LANES_TASKS is required")
    try:
        notes = []
        hits = check(a.experiment, a.tasks, a.runs, a.kogen, notes)
    except (experiment.ExperimentError, OSError, ValueError) as e:
        print(f"leakcheck: {e}", file=sys.stderr)
        return 2
    for note in notes:
        print(f"leakcheck: note: {note}", file=sys.stderr)
    for hit in hits:
        print(format_hit(hit))
    if hits:
        print(f"leakcheck: {len(hits)} hit(s); no cell may start", file=sys.stderr)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
