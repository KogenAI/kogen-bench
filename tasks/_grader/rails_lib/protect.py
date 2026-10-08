#!/usr/bin/env python3
"""Rails grader helper (grader-side only).
  protect.py check WORK SNAP TASK_ID   build/test-infrastructure paths of WORK must equal the pre-agent snapshot SNAP; prints TAMPER lines, exit 1 on any.
  protect.py receipt CHECKS_JSON VERIFIER_RB   the hidden run must have recorded results for its checks: none missing, none skip/error/fail.
Protected: gem sources (Gemfile*: plain gem lines only; lock: no source changes; .bundle), boot/env/test-environment config, database.yml, test_helper, system-test base class, shared test helpers.
Not protected (features legitimately change them): db/schema*.rb, migrations, config/application.rb, initializers, fixtures, other test files.
Per-task exemptions are the paths whose reference solution edits them."""
import json, os, re, sys

GEMFILES = [("Gemfile", "Gemfile.lock"), ("Gemfile.saas", "Gemfile.saas.lock")]
FILES = [".ruby-version", "config/boot.rb", "config/environment.rb",
         "config/environments/test.rb", "config/database.yml", "test/test_helper.rb", "test/application_system_test_case.rb", "Rakefile",
         "config.ru"]
DIRS = [".bundle", "test/test_helpers", "test/support"]
EXEMPT = {  # task dir name -> protected paths its reference solution legitimately edits
    "rails-tst-error-page-flake": ["test/test_helper.rb"],
    "rails-ft-web-push-device-delivery": ["test/test_helpers"],
    "rails-ft-mysql-fulltext-search-foundation": ["test/test_helpers"],
}
# Gemfile: only plain rubygems `gem "name"[, "version"...]` lines may be added or removed (no source/git/path/github/require/group/env logic).
# Gemfile.lock: GIT, PATH, PLATFORMS, RUBY VERSION, BUNDLED WITH sections and the GEM remote must be unchanged; the GEM specs and DEPENDENCIES may follow the Gemfile.
GEMLINE = re.compile(r'^\s*gem\s+"[\w.-]+"(?:,\s*"[~><=!\s\d.]+")*\s*$')


def gemfile_problem(a, b):
    import difflib
    for l in difflib.unified_diff(b.splitlines(), a.splitlines(), lineterm="", n=0):
        if l.startswith(("+++", "---", "@@")):
            continue
        if l[1:].strip() and not GEMLINE.match(l[1:]):
            return "changes more than plain gem lines: " + l[:80]
    return None


def lock_problem(a, b):
    def parts(t):
        secs = [x for x in t.split("\n\n") if x.strip()]
        fixed = sorted(x for x in secs if x.split("\n", 1)[0].strip() in ("GIT", "PATH", "PLATFORMS", "RUBY VERSION", "BUNDLED WITH") or x.startswith(("PLATFORMS", "RUBY VERSION", "BUNDLED WITH")))
        remotes = [l.strip() for x in secs if x.startswith("GEM") for l in x.splitlines() if l.strip().startswith("remote:")]
        return fixed, remotes
    return None if parts(a) == parts(b) else "changes GIT/PATH/PLATFORMS/remote/BUNDLED WITH sections"



def tree(root, rel):
    p = os.path.join(root, rel)
    if os.path.islink(p):
        return {rel: "symlink:" + os.readlink(p)}
    if os.path.isdir(p):
        out = {}
        for r, _, fs in os.walk(p):
            for f in fs:
                fp = os.path.join(r, f)
                out[os.path.relpath(fp, root)] = "symlink:" + os.readlink(fp) if os.path.islink(fp) else open(fp, "rb").read()
        return out
    if os.path.isfile(p):
        return {rel: open(p, "rb").read()}
    return {}


def check(work, snap, task):
    ex = EXEMPT.get(task, [])
    bad = []
    for rel in FILES + DIRS:
        if any(rel == e or rel.startswith(e + "/") for e in ex):
            continue
        a, b = tree(work, rel), tree(snap, rel)
        for k in sorted(set(a) | set(b)):
            if a.get(k) != b.get(k):
                bad.append(f"TAMPER: {k} " + ("removed" if k not in a else "added" if k not in b else "differs from the pre-agent snapshot"))
    for gf, lk in GEMFILES:
        for rel, fn in ((gf, gemfile_problem), (lk, lock_problem)):
            if any(rel == e for e in ex):
                continue
            a, b = tree(work, rel).get(rel), tree(snap, rel).get(rel)
            if a == b:
                continue
            if a is None or b is None:
                bad.append(f"TAMPER: {rel} " + ("removed" if a is None else "added")); continue
            prob = fn(a.decode(errors="replace"), b.decode(errors="replace"))
            if prob:
                bad.append(f"TAMPER: {rel} {prob}")
    print("\n".join(bad) if bad else "protected paths ok")
    return 1 if bad else 0


def receipt(checks, verifier):
    try:
        d = json.load(open(checks))
    except Exception as e:
        print(f"RECEIPT: no readable checks.json ({e})"); return 1
    res = d.get("checks") or {}
    need = len(re.findall(r'^\s*(?:test\s+["\']|def\s+test_)', open(verifier).read(), re.M))
    bad = {k: v for k, v in res.items() if v not in ("pass", "fail (allowed)")}
    if not res or bad or len(res) < need:
        print(f"RECEIPT: {len(res)} checks recorded, {need} expected, not passing: {bad}"); return 1
    print(f"receipt ok: {len(res)} hidden checks executed"); return 0


if __name__ == "__main__":
    if sys.argv[1] == "check":
        sys.exit(check(sys.argv[2], sys.argv[3], sys.argv[4]))
    sys.exit(receipt(sys.argv[2], sys.argv[3]))
