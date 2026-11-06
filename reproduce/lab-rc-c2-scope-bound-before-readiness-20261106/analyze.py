#!/usr/bin/env python3
"""RC-C2 step 2/3 (model-free): bytes per class of the scope estimate of the recorded attempt-1
package of a kept shaped tree. Re-implements the scope estimate of kogen-shaping shape/scope.go
(package bytes + HEAD size of every single-backtick span that is a tracked blob outside .kogen/ and
outside the package) and splits it by class. Prints class totals only, never a path.

usage: analyze.py <tree with HEAD> <slug> <dir holding the recorded package (proposed/)>
"""
import json, os, re, subprocess, sys, gzip

tree, slug, prop = sys.argv[1:4]
BOUND = 524288
TEXT_EXT = (".md", ".go", ".exs", ".ex", ".js", ".sh", ".yaml", ".yml", ".json", ".feature", ".qnt", ".txt")


def git(*a):
    return subprocess.run(["git", "-C", tree, *a], capture_output=True, check=True).stdout


# HEAD blobs with sizes (as scope.go headBlobs: ls-tree -r -l -z HEAD)
head = {}
for rec in git("ls-tree", "-r", "-l", "-z", "HEAD").decode("utf-8", "replace").split("\x00"):
    meta, _, name = rec.partition("\t")
    f = meta.split()
    if len(f) == 4 and f[1] == "blob":
        head[name] = int(f[3])

pkg_paths = []
for root, _, files in os.walk(prop):
    for fn in files:
        pkg_paths.append(os.path.relpath(os.path.join(root, fn), prop))
pkg_paths.sort()


def pclass(p):
    if p.endswith("/intent.md"):
        return "intent_text"
    if p.endswith("/acceptance.feature"):
        return "acceptance_feature"
    if p.endswith(".qnt"):
        return "model"
    return "step_files"


pkg = {}
for p in pkg_paths:
    pkg[p] = open(os.path.join(prop, p), "rb").read()
intent_text = pkg[[p for p in pkg if p.endswith("/intent.md")][0]].decode("utf-8", "replace")

named, seen = [], set()
for m in re.finditer(r"`([^`\n]+)`", intent_text):
    s = m.group(1)
    if s in head and s not in seen and s not in pkg and not s.startswith(".kogen/"):
        seen.add(s)
        named.append(s)

# generated: a tracked text file elsewhere says, on one line, that this path is generated/regenerated
text_blobs = {}
for p, sz in head.items():
    if p.endswith(TEXT_EXT) and sz <= 400_000 and not p.startswith(".kogen/local"):
        try:
            text_blobs[p] = git("show", "HEAD:" + p).decode("utf-8")
        except Exception:
            pass


def is_generated(p):
    for q, t in text_blobs.items():
        if q == p or q.startswith(".kogen/"):
            continue  # history of earlier Intents mentions many files; only the live docs and code count
        for line in t.splitlines():
            if p in line and re.search(r"regenerat|generated (from|by)|go run .* > ", line):
                return True
    return False


def nclass(p):
    if is_generated(p):
        return "named_generated_data"
    base = os.path.basename(p)
    if re.search(r"(_test\.(go|exs?)|\.test\.js)$", base) or p.startswith("test/"):
        return "named_tests"
    if p.startswith("features/"):
        return "named_acceptance_pins"  # existing features/steps files of other Intents
    if p.endswith(".md"):
        return "named_docs"
    if base.startswith("."):
        return "named_config"
    return "named_source_and_other"


classes = {}
files_by_class = {}
for p in pkg:
    c = pclass(p)
    classes[c] = classes.get(c, 0) + len(pkg[p])
for p in named:
    c = nclass(p)
    classes[c] = classes.get(c, 0) + head[p]
    files_by_class.setdefault(c, []).append(head[p])
pkg_bytes = sum(len(v) for v in pkg.values())
named_bytes = sum(head[p] for p in named)
estimate = pkg_bytes + named_bytes

# repetition inside the package, and package text copied from the HEAD tree
def lines_of(b):
    return [l.strip() for l in b.decode("utf-8", "replace").splitlines()]


allpkg_lines = {}
rep_bytes = 0       # bytes (with newline) of repeats beyond the first occurrence, lines >= 30 chars, whole package
feat_rep = 0        # same, acceptance.feature only (per-scenario repeats)
for p, b in pkg.items():
    local = {}
    for l in lines_of(b):
        if len(l) < 30:
            continue
        if l in allpkg_lines:
            rep_bytes += len(l) + 1
            if pclass(p) == "acceptance_feature":
                feat_rep += len(l) + 1
        allpkg_lines[l] = True
head_lines = set()
for q, t in text_blobs.items():
    if q.startswith(".kogen/intents/" + slug):
        continue
    for l in t.splitlines():
        l = l.strip()
        if len(l) >= 40:
            head_lines.add(l)
copied = 0
copied_in_named = 0
named_set = set(named)
named_lines = set()
for q in named_set:
    for l in (text_blobs.get(q, "")).splitlines():
        l = l.strip()
        if len(l) >= 40:
            named_lines.add(l)
for p, b in pkg.items():
    for l in lines_of(b):
        if len(l) >= 40 and l in head_lines:
            copied += len(l) + 1
        if len(l) >= 40 and l in named_lines:
            copied_in_named += len(l) + 1

gz = sum(len(gzip.compress(v)) for v in pkg.values())
authority = sum(len(pkg[p]) for p in pkg if pclass(p) in ("intent_text", "acceptance_feature", "model"))

out = {
    "scenarios_text_bytes": None,
    "estimate": estimate,
    "package_bytes": pkg_bytes,
    "named_files": len(named),
    "named_bytes": named_bytes,
    "classes": classes,
    "largest_class": max(classes, key=classes.get),
    "largest_share": round(max(classes.values()) / estimate, 4),
    "largest_file_bytes": max([head[p] for p in named] or [0]),
    "named_share": round(named_bytes / estimate, 4),
    "package_share": round(pkg_bytes / estimate, 4),
    "package_repeat_line_bytes": rep_bytes,
    "feature_repeat_line_bytes": feat_rep,
    "package_gzip_bytes": gz,
    "package_lines_also_in_head_bytes": copied,
    "package_lines_also_in_named_files_bytes": copied_in_named,
    "review_authority_bytes": authority,
    "step_file_bytes_not_in_review_prompt": classes.get("step_files", 0),
    "fits": {
        "gate_estimate": estimate <= BOUND,
        "generated_counted_zero": estimate - classes.get("named_generated_data", 0) <= BOUND,
        "generated_and_repeats_once": estimate - classes.get("named_generated_data", 0) - rep_bytes - copied_in_named <= BOUND,
        "package_only": pkg_bytes <= BOUND,
        "review_authority_only": authority <= BOUND,
    },
    "remaining": {
        "generated_counted_zero": estimate - classes.get("named_generated_data", 0),
        "generated_and_repeats_once": estimate - classes.get("named_generated_data", 0) - rep_bytes - copied_in_named,
        "package_only": pkg_bytes,
        "review_authority_only": authority,
    },
}
print(json.dumps(out, indent=1))
