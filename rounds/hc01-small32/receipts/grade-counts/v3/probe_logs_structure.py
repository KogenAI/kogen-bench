#!/usr/bin/env python3
"""AMENDMENT-5 integer-only structure probe of one retained validation-family logs file.
Prints ONLY integers, booleans and fixed labels: no log text, test names or values.
Usage (as root on US): python3 - < probe_logs_structure.py LOGS_FILE"""
import io, json, re, sys, tarfile
CHECKS = ("protected_paths", "hidden", "suite", "migration")
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
EXUNIT = re.compile(r"^(?:\d+ doctests?, )?(?:\d+ propert(?:y|ies), )?\d+ tests?, \d+ failures?\b")
RESULT = re.compile(r"^Result: \d+/\d+ passed$")
FINISHED = re.compile(r"^Finished in [\d.]+ seconds")

def lines_of(data):
    return [ANSI.sub("", l).strip() for l in data.decode("utf-8", "replace").splitlines()]

def idx(lines, pred):
    return [i for i, l in enumerate(lines) if pred(l)]

def probe_text(lines):
    return {
        "n_lines": len(lines),
        "exunit_summary_idx": idx(lines, lambda l: bool(EXUNIT.match(l))),
        "result_line_idx": idx(lines, lambda l: bool(RESULT.match(l))),
        "finished_in_idx": idx(lines, lambda l: bool(FINISHED.match(l))),
        "check_name_line_idx": {c: idx(lines, lambda l, c=c: c in l.lower())[:40] for c in CHECKS},
    }

path = sys.argv[1]
data = open(path, "rb").read()
out = {"bytes": len(data)}
try:
    tf = tarfile.open(fileobj=io.BytesIO(data))
    members = [m for m in tf.getmembers() if m.isfile()]
    out["kind"] = "tar"
    out["members"] = [{"member_index": k, "path_has_check": {c: (c in m.name.lower()) for c in CHECKS},
                       **probe_text(lines_of(tf.extractfile(m).read()))} for k, m in enumerate(members)]
except tarfile.TarError:
    out["kind"] = "file"
    out.update(probe_text(lines_of(data)))
print(json.dumps(out, sort_keys=True))
