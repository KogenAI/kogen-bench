"""Build one Kogen artifact per lane: a sha plus an optional patch (format in lanes/FORMATS.md)."""

import argparse
import glob
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

from . import common, experiment

BUILD_DEADLINE_S = 3600
GIT_DEADLINE_S = 600
VERSION_DEADLINE_S = 60
GIT_ENV = {"GIT_TERMINAL_PROMPT": "0"}


class BuildError(Exception):
    pass


def _go_main_dir(tree):
    """Directory of the `package main` to build: `cmd/kogen` if present, else the first one found."""
    if os.path.isfile(os.path.join(tree, "cmd", "kogen", "main.go")):
        return "./cmd/kogen"
    for path in sorted(glob.glob(os.path.join(tree, "**", "*.go"), recursive=True)):
        if path.endswith("_test.go"):
            continue
        with open(path, encoding="utf-8", errors="replace") as f:
            if re.search(r"^package main\b", f.read(), re.M):
                return "./" + os.path.relpath(os.path.dirname(path), tree).replace(os.sep, "/")
    raise BuildError("no Go main package found")


def _build_go(tree, log):
    _run(["go", "build", "-trimpath", "-buildvcs=false", "-o", os.path.join(tree, ".lane-out", "kogen"), _go_main_dir(tree)], tree, log)
    return os.path.join(tree, ".lane-out", "kogen")


def _build_elixir(tree, log):
    _run(["sh", "packaging/package.sh"], tree, log)
    archives = glob.glob(os.path.join(tree, "dist", "kogen-*.tar.gz"))
    if len(archives) != 1:
        raise BuildError("packaging/package.sh did not produce exactly one archive")
    return archives[0]


def _build_marker(tree, log):
    """Tests only: a repo with `lane-build.sh` builds `lane-out` by running it."""
    _run(["sh", "lane-build.sh"], tree, log)
    return os.path.join(tree, "lane-out")


# (marker file at the tree root, builder). The first marker present wins. A builder returns the
# artifact path: an executable `kogen`, or a `.tar.gz` release holding `<top>/bin/kogen`.
DETECT = [
    ("mix.exs", _build_elixir),
    ("go.mod", _build_go),
]


def _run(cmd, cwd, log, deadline_s=BUILD_DEADLINE_S):
    with open(log, "ab") as out:
        code, timed_out = common.run(cmd, cwd=cwd, deadline_s=deadline_s, stdout=out, stderr=out)
    if timed_out or code != 0:
        raise BuildError(f"{' '.join(cmd[:3])} {'timed out' if timed_out else f'exited {code}'}; see {log}")


def _capture(cmd, deadline_s, cwd=None, env=None):
    """Run `cmd` in its own process group with a deadline; return `(exit_code, output, timed_out)`."""
    with tempfile.TemporaryFile() as out:
        code, timed_out = common.run(cmd, cwd=cwd, env=env, deadline_s=deadline_s, stdout=out, stderr=subprocess.STDOUT)
        out.seek(0)
        return code, out.read().decode(errors="replace").strip(), timed_out


def _git(args, git_dir=None, cwd=None):
    cmd = ["git"] + (["--git-dir", git_dir] if git_dir else []) + args
    code, out, timed_out = _capture(cmd, GIT_DEADLINE_S, cwd, dict(os.environ, **GIT_ENV))
    return code, ("timed out after %ss" % GIT_DEADLINE_S if timed_out else out)


def ensure_sha(repo, sha, home):
    """Path of the bare clone holding `sha`; clone once, fetch when the sha is missing."""
    git_dir = os.path.join(home, "kogen.git")
    if not os.path.isdir(git_dir):
        os.makedirs(home, exist_ok=True)
        part = tempfile.mkdtemp(prefix="kogen.git-", dir=home)  # renamed only when complete
        code, out = _git(["clone", "--bare", "--quiet", repo, os.path.join(part, "c")])
        if code:
            shutil.rmtree(part, ignore_errors=True)
            raise BuildError(f"cannot clone {repo}: {out}")
        os.rename(os.path.join(part, "c"), git_dir)
        os.rmdir(part)
    if _git(["cat-file", "-e", sha + "^{commit}"], git_dir)[0]:
        _git(["fetch", "--quiet", repo, "+refs/heads/*:refs/heads/*", "+refs/tags/*:refs/tags/*"], git_dir)
        if _git(["cat-file", "-e", sha + "^{commit}"], git_dir)[0]:
            _git(["fetch", "--quiet", repo, sha], git_dir)  # reachable only from another ref
        if _git(["cat-file", "-e", sha + "^{commit}"], git_dir)[0]:
            raise BuildError(f"sha {sha} is not in {repo}")
    return git_dir


def _kogen_version(artifact):
    tmp = tempfile.mkdtemp(prefix="lane-version-")
    try:
        exe = artifact
        if artifact.endswith(".tar.gz"):
            with tarfile.open(artifact) as t:
                # the data filter needs Python 3.12 (or a patched older one); the archive is our own
                t.extractall(tmp, **({"filter": "data"} if getattr(tarfile, "data_filter", None) else {}))
            exe = glob.glob(os.path.join(tmp, "*", "bin", "kogen"))[0]
        code, out, timed_out = _capture([exe, "version"], VERSION_DEADLINE_S)
        if timed_out:
            raise BuildError(f"`kogen version` timed out after {VERSION_DEADLINE_S}s")
        if code:
            raise BuildError(f"`kogen version` exited {code}")
        return out
    except (OSError, IndexError, tarfile.TarError) as e:
        raise BuildError(f"cannot run the built binary: {e}") from None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _build_tree(git_dir, sha, patch, home, log):
    """Build in a throwaway worktree; return the artifact path inside `tmp` (caller copies it)."""
    tmp = tempfile.mkdtemp(prefix="lane-wt-", dir=home)
    wt = os.path.join(tmp, "tree")
    code, out = _git(["worktree", "add", "--detach", wt, sha], git_dir)
    if code:
        shutil.rmtree(tmp, ignore_errors=True)
        raise BuildError(f"cannot check out {sha}: {out}")
    try:
        if patch:
            code, out = _git(["apply", "--3way", patch], cwd=wt)
            if code:
                raise BuildError(f"patch {patch} does not apply to {sha}: {out}")
        for marker, builder in DETECT:
            if os.path.exists(os.path.join(wt, marker)):
                return tmp, builder(wt, log)
        raise BuildError(f"no known build layout at {sha} (looked for {', '.join(m for m, _ in DETECT)})")
    except BaseException:
        _cleanup(git_dir, wt, tmp)
        raise


def _cleanup(git_dir, wt, tmp):
    _git(["worktree", "remove", "--force", wt], git_dir)
    shutil.rmtree(tmp, ignore_errors=True)
    _git(["worktree", "prune"], git_dir)


def _repo(repo, exp_path):
    """A URL stays as is; a relative path is taken from the experiment file's directory."""
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://|^[^/]+@[^/]+:", repo):
        return repo
    return os.path.join(os.path.dirname(os.path.abspath(exp_path)), os.path.expanduser(repo))


def build_lane(exp, lane, exp_path, home):
    """Return the lock entry for `lane`, building only when the input is not cached."""
    patch = experiment.patch_path(exp_path, lane)
    if patch and not os.path.isfile(patch):
        raise BuildError(f"lane {lane['name']}: patch file {lane['patch']} not found")
    patch_sha = common.sha256_file(patch) if patch else None
    key = hashlib.sha256(f"{lane['sha']}\n{patch_sha}\n".encode()).hexdigest()
    index = os.path.join(home, "artifacts", "by-input", key)
    entry = {"name": lane["name"], "sha": lane["sha"], "patch_sha256": patch_sha}
    if os.path.isfile(index):
        cached = common.read_json(index)
        if glob.glob(os.path.join(home, "artifacts", cached["artifact_sha256"], "*")):
            return dict(entry, **cached)
    git_dir = ensure_sha(_repo(exp["kogen"]["repo"], exp_path), lane["sha"], home)
    log = os.path.join(home, "artifacts", f"build-{key[:12]}.log")
    os.makedirs(os.path.dirname(log), exist_ok=True)
    open(log, "wb").close()
    tmp, built = _build_tree(git_dir, lane["sha"], patch, home, log)
    try:
        art_sha = common.sha256_file(built)
        dest_dir = os.path.join(home, "artifacts", art_sha)
        dest = os.path.join(dest_dir, os.path.basename(built))
        if not os.path.exists(dest):
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(built, dest + ".tmp")
            os.replace(dest + ".tmp", dest)
        version = _kogen_version(dest)
    finally:
        _cleanup(git_dir, os.path.join(tmp, "tree"), tmp)
    cached = {"artifact_sha256": art_sha, "kogen_version": version}
    common.write_json(index, cached)
    return dict(entry, **cached)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="lanes-build", description="Build one Kogen binary per lane.")
    ap.add_argument("experiment")
    ap.add_argument("--run-dir")
    args = ap.parse_args(argv)
    exp = experiment.load_or_exit(args.experiment)
    run_dir = args.run_dir or common.runs_dir(exp["id"])
    home = common.lanes_home()
    lock, done = [], {}
    try:
        for lane in exp["lanes"]:
            same = (lane["sha"], lane["patch"])
            if same in done:  # same sha and patch share one artifact
                lock.append(dict(done[same], name=lane["name"]))
                continue
            done[same] = build_lane(exp, lane, args.experiment, home)
            lock.append(done[same])
    except BuildError as e:
        print(f"lanes-build: {e}", file=sys.stderr)
        return 1
    common.write_json(os.path.join(run_dir, "lanes.lock.json"), lock)
    return 0
