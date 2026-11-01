"""Warm Go build cache per task: build the task's start tree once at staging, give every run a private copy.

`lanes-stage` copies `start/` and, in each Go module of it, runs `go build ./...`, `go vet ./...` and
`go test -count=1 -run '^$' ./...` (compiles the test binaries; runs no test and stores no test result) with an
empty `GOCACHE`. The entry `<root>/<key>/` holds that `gocache/` and `manifest.json` with its digest. The key is
the SHA-256 of the start tree, its module list, the commands and the Go toolchain as `go env` reports it in
each module under the run's environment (including `GOMODCACHE`). A changed task tree or toolchain is another key.

Modules the build downloads go into the run's own `GOMODCACHE`, as before, so they are fetched at staging and
not inside the approval deadline. The module cache is not copied: Go keys every non-GOROOT package by its
folder (without -trimpath), so modules at a per-run path would miss the build cache for every dependency.
Module versions are immutable and checked against go.sum. For the same reason the task's own and vendored
packages, which live in each run's new workspace folder, are compiled again; the standard library and
module-cache dependencies are reused.

Every approval and every cell, whatever its lane or executor, gets the same `GOCACHE`: one host-wide shared cache
(`<root>/shared`, also the cache grading uses). Go's build cache is
content-addressed and safe for concurrent writers, so sharing it never changes what a build produces; it only
stops every cell from growing a private cache of its own. Before a run, the task's staged entry is merged into the
shared cache (files the cache lacks are cloned in; nothing is overwritten), after the entry is checked against its
manifest. A missing, changed or corrupt entry merges nothing: the run builds from whatever the shared cache holds,
a cold build for that task, never a failed run. The shared cache is bounded by `trim` (gocache-trim on the hosts).
"""
import argparse
import ctypes
import datetime
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time

from . import approvecache

SCHEMA = 1
COMMANDS = (("go", "build", "./..."), ("go", "vet", "./..."), ("go", "test", "-count=1", "-run", "^$", "./..."))
# What the compiled output depends on besides the sources. GOMODCACHE is keyed because dependency action IDs
# include their folder; the GOCACHE path is not keyed.
TOOLCHAIN = ("GOVERSION", "GOOS", "GOARCH", "GOAMD64", "GOARM64", "CGO_ENABLED", "GOEXPERIMENT", "GOFLAGS",
             "GOMODCACHE")
SKIP_DIRS = {"vendor", "node_modules", "testdata", ".git", ".kogen"}
DEFAULT_ROOT = Path(__file__).resolve().parents[3] / "go-cache"
INFO = "go-cache.json"  # per cell: which entry it was seeded from; keys and digests only, no paths
INFO_SCHEMA = 2  # 2: shared cache (1: a private clone per run)
TRIM_GB = 20  # staging trims the shared cache to this size (never entries used in the last two hours)


def cache_root():
    return Path(os.environ.get("LANES_GO_CACHE") or DEFAULT_ROOT).resolve()


def base_env():
    """The environment Kogen inherits from `Cell`."""
    return {k: v for k, v in os.environ.items() if not k.startswith("KOGEN_LANES_")}


def modules(start):
    """Relative folders of `start` holding a `go.mod`, as the go command would see them (no vendor/testdata)."""
    found = []
    for dirpath, dirnames, filenames in os.walk(start):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith((".", "_"))
                             and not os.path.islink(os.path.join(dirpath, d)))
        if "go.mod" in filenames:
            found.append(Path(os.path.relpath(dirpath, start)).as_posix())
    return found


def toolchain(moddir, env):
    p = subprocess.run(["go", "env", "-json", *TOOLCHAIN], cwd=moddir, env=env, capture_output=True, text=True)
    if p.returncode:
        raise ValueError(f"go env failed in {moddir}: {p.stderr.strip()[-300:]}")
    return json.loads(p.stdout)


def key(task, env=None):
    """`(key, components)` for the task's start tree, or None when it has no Go module or no `go` on PATH."""
    start = Path(task) / "start"
    mods = modules(start)
    env = base_env() if env is None else env
    if not mods or not shutil.which("go", path=env.get("PATH")):
        return None
    components = {"schema": SCHEMA, "start": approvecache.tree(str(start)), "modules": mods,
                  "commands": [list(c) for c in COMMANDS],
                  "toolchain": {m: toolchain(start / m, env) for m in mods}}
    return hashlib.sha256(json.dumps(components, sort_keys=True).encode()).hexdigest(), components


def digest(path):
    """`{sha256, files, bytes}` of a cache folder (paths, executable bits, contents)."""
    files = size = 0
    for dirpath, _, filenames in os.walk(path):
        for n in filenames:
            files += 1
            size += os.lstat(os.path.join(dirpath, n)).st_size
    return {"sha256": approvecache.tree(str(path)), "files": files, "bytes": size}


def shared_dir():
    """The host-wide Go build cache every run and every grade uses: `<root>/shared`."""
    return (cache_root() / "shared").resolve()


def _add(src, dest):
    """Put a copy of `src` at `dest` unless something is there; atomic, so a reader never sees half a file."""
    if os.path.lexists(dest):
        return False
    if sys.platform == "darwin":
        if _libc().clonefile(os.fsencode(src), os.fsencode(dest), 0) == 0:
            return True
        if ctypes.get_errno() == errno.EEXIST:
            return False
    part = f"{dest}.seed-{os.getpid()}"
    try:
        shutil.copyfile(src, part)
        os.link(part, dest)  # fails when another run got there first
        return True
    except FileExistsError:
        return False
    finally:
        try:
            os.unlink(part)
        except FileNotFoundError:
            pass


def _libc():
    return ctypes.CDLL(None, use_errno=True)


def seed(gocache, shared):
    """Merge a staged entry's cache into the shared one; returns how many files were added. Idempotent and
    safe while runs use `shared`: Go names every file by its content or action, so a file already there is
    the same file. Fresh mtimes keep Go's own five-day trim from dropping just-seeded files."""
    added = 0
    now = time.time()
    for dirpath, _, filenames in os.walk(gocache):
        rel = os.path.relpath(dirpath, gocache)
        if rel != "." and not re.fullmatch(r"[0-9a-f]{2}", rel):
            continue  # Go's README and trim.txt are the shared cache's own
        if rel != ".":
            os.makedirs(os.path.join(shared, rel), exist_ok=True)
        for n in filenames:
            if rel != "." and _add(os.path.join(dirpath, n), os.path.join(shared, rel, n)):
                os.utime(os.path.join(shared, rel, n), (now, now))
                added += 1
    return added


def _unit(path):
    """`(mtime, bytes)` of one cache entry: a file, or a `-d` directory (a cached executable; Go refreshes the
    directory's mtime on use and removes it whole)."""
    st = os.stat(path)
    if not os.path.isdir(path):
        return st.st_mtime, st.st_size
    size = 0
    for dirpath, _, names in os.walk(path):
        size += sum(os.lstat(os.path.join(dirpath, n)).st_size for n in names)
    return st.st_mtime, size


def trim(shared, max_bytes, min_age=7200):
    """Delete least recently used entries (oldest mtime; Go refreshes it on use, at most once an hour, so
    `min_age` is two hours) until `shared` is at most `max_bytes`; never an entry modified in the last
    `min_age` seconds. Entries are Go's `-a` and `-d` files and `-d` directories. Returns `(before, after)`."""
    units, total, now = [], 0, time.time()
    for shard in sorted(os.listdir(shared)) if os.path.isdir(shared) else []:
        shard_dir = os.path.join(shared, shard)
        if not os.path.isdir(shard_dir):
            continue
        for n in os.listdir(shard_dir):
            path = os.path.join(shard_dir, n)
            try:
                mtime, size = _unit(path)
            except OSError:
                continue
            units.append((mtime, size, path))
            total += size
    before = total
    for mtime, size, path in sorted(units):
        if total <= max_bytes or now - mtime < min_age:
            break
        try:
            shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            total -= size
        except OSError:
            pass
    return before, total


def entry_ok(entry):
    """The manifest when the entry's cache matches it, else None."""
    try:
        manifest = json.loads((entry / "manifest.json").read_text())
        return manifest if digest(entry / "gocache")["sha256"] == manifest["gocache"]["sha256"] else None
    except (OSError, ValueError, KeyError, TypeError):
        return None


def stage(task, out=print):
    """Build the start tree once into a new entry (reused when an identical sound entry exists).

    Never raises: a task that cannot be staged runs cold."""
    name = Path(task).name
    try:
        env = base_env()
        found = key(task, env)
        if found is None:
            return None
        k, components = found
        root = cache_root()
        root.mkdir(parents=True, exist_ok=True)
        with open(root / (k + ".lock"), "a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            entry = root / k
            if entry.exists():
                if entry_ok(entry):
                    out(f"{name}: go cache reuse {k}")
                    return k
                aside = root / f"{k}.aside-corrupt-{datetime.datetime.now(datetime.timezone.utc):%Y%m%dT%H%M%SZ}"
                os.rename(entry, aside)
                out(f"{name}: go cache {k} did not match its manifest; moved aside and staged again")
            tmp = Path(tempfile.mkdtemp(prefix="staging-", dir=root))
            try:
                ws = tmp / "ws"
                shutil.copytree(Path(task) / "start", ws, symlinks=True,
                                ignore=shutil.ignore_patterns(".git", "node_modules"))
                (tmp / "gocache").mkdir()
                run_env = dict(env, GOCACHE=str(tmp / "gocache"))
                steps = []
                for m in components["modules"]:
                    for cmd in COMMANDS:
                        t0 = time.monotonic()
                        p = subprocess.run(list(cmd), cwd=ws / m, env=run_env, stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL)
                        steps.append({"module": m, "command": list(cmd), "exit": p.returncode,
                                      "seconds": round(time.monotonic() - t0, 3)})
                shutil.rmtree(ws)
                manifest = {"schema": SCHEMA, "key": k, "task": name, "components": components, "steps": steps,
                            "gocache": digest(tmp / "gocache"), "host": socket.gethostname(),
                            "staged_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
                (tmp / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
                os.rename(tmp, entry)
            finally:
                if tmp.exists():
                    shutil.rmtree(tmp, ignore_errors=True)
        failed = [f"{s['module']} {' '.join(s['command'][:2])}" for s in steps if s["exit"]]
        out(f"{name}: go cache staged {k} ({manifest['gocache']['files']} files"
            f"{'; nonzero: ' + ', '.join(failed) if failed else ''})")
        return k
    except Exception as e:  # staging is an optimization: never fail the unit's prep
        out(f"{name}: go cache not staged ({type(e).__name__}: {e}); its runs build cold")
        return None


def prepare(start, tmp=None):
    """`(env, info)` for one run: `GOCACHE` is the host-wide shared cache, seeded from the task's staged entry
    when that entry is sound. A missing, changed or corrupt entry seeds nothing (a cold build for the task, the
    shared cache still serves the standard library and any dependency another run built). Never raises; a task
    without Go gets `({}, ...)`, the environment as before. `tmp` is unused (runs no longer own a cache)."""
    t0 = time.monotonic()
    task = Path(start).parent
    info = {"schema": INFO_SCHEMA, "status": "cold", "shared": True}
    shared = None
    try:
        found = key(task)
        if found is None:
            return {}, {"schema": INFO_SCHEMA, "status": "none"}
        info["key"] = found[0]
        shared = shared_dir()
        shared.mkdir(parents=True, exist_ok=True)
        entry = cache_root() / found[0]
        if not (entry / "manifest.json").is_file():
            info["reason"] = "not staged"
        else:
            raw = (entry / "manifest.json").read_bytes()
            info["manifest_sha256"] = hashlib.sha256(raw).hexdigest()
            want = json.loads(raw)["gocache"]["sha256"]
            if digest(entry / "gocache")["sha256"] == want:
                info.update(status="warm", gocache_sha256=want, seeded_files=seed(entry / "gocache", shared))
            else:
                info["reason"] = "entry does not match the manifest"
    except Exception as e:  # never fail the run: build from the shared cache as it is
        info["reason"] = f"{type(e).__name__}: {e}"[:300]
    if shared is None:
        shared = shared_dir()
        shared.mkdir(parents=True, exist_ok=True)
    if info["status"] == "cold":
        print(f"go cache: cold build for {task.name} ({info.get('reason')})", file=sys.stderr)
    return {"GOCACHE": str(shared)}, dict(info, seconds=round(time.monotonic() - t0, 3))


def main(argv=None):
    """`lanes-stage` arguments: the experiment's tasks (`--run-dir`), the named ones, or the whole kit."""
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tasks", required=True)
    p.add_argument("--run-dir")
    p.add_argument("task_ids", nargs="*")
    a = p.parse_args(argv)
    try:
        tasks = a.task_ids
        if a.run_dir:
            experiment = json.loads((Path(a.run_dir) / "experiment.json").read_text())
            if experiment.get("phase") == "probe":
                return
            tasks = experiment["tasks"]
        tasks = tasks or sorted(t.name for t in Path(a.tasks).iterdir() if (t / "task.toml").is_file())
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(f"go cache: nothing staged ({e}); Go tasks build cold", flush=True)
        return
    for task in tasks:
        stage(Path(a.tasks) / task, out=lambda line: print(line, flush=True))
    try:  # the same bound the hosts' gocache-trim applies, so the shared cache never grows without limit
        before, after = trim(shared_dir(), TRIM_GB * 1024 ** 3)
        print(f"go cache: shared {before / 1024 ** 3:.1f} GB -> {after / 1024 ** 3:.1f} GB", flush=True)
    except OSError as e:
        print(f"go cache: shared cache not trimmed ({e})", flush=True)


if __name__ == "__main__":
    main()
