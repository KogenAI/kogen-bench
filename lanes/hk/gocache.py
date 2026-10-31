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

Every approval and every cell, whatever its lane or executor, gets `GOCACHE` pointing at its own APFS clone of
the entry in its scratch folder, checked against the manifest before use. A missing, changed or corrupt entry
gives an empty private cache instead: a cold build, never a failed run. Go's own action IDs decide every reuse
inside the cache, so a warm entry makes a build faster but never different.
"""
import argparse
import ctypes
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
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
INFO = "go-cache.json"  # per cell: which entry it started from; keys and digests only, no paths


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


def clone(source, dest):
    """A private copy sharing disk blocks: one clonefile(2) of the tree, else `cp -cR`, else a plain copy."""
    if sys.platform == "darwin":
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.clonefile(os.fsencode(source), os.fsencode(dest), 0) == 0:
            return "clonefile"
        if os.path.lexists(dest):
            shutil.rmtree(dest)
        if subprocess.run(["/bin/cp", "-cR", str(source), str(dest)], capture_output=True).returncode == 0:
            return "cp -c"
        if os.path.lexists(dest):
            shutil.rmtree(dest)
    shutil.copytree(source, dest, symlinks=True)
    return "copy"


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


def prepare(start, tmp):
    """`(env, info)` for one run whose scratch folder is `tmp`: its own warm copy of the staged entry, or an
    empty private `GOCACHE` (cold) when the entry is missing, changed or corrupt. Never raises; a task without
    Go gets `({}, ...)`, the environment as before."""
    t0 = time.monotonic()
    task = Path(start).parent
    gocache = Path(tmp) / "go-cache"
    info = {"schema": SCHEMA, "status": "cold"}
    try:
        found = key(task)
        if found is None:
            return {}, {"schema": SCHEMA, "status": "none"}
        info["key"] = found[0]
        entry = cache_root() / found[0]
        if not (entry / "manifest.json").is_file():
            info["reason"] = "not staged"
        else:
            raw = (entry / "manifest.json").read_bytes()
            want = json.loads(raw)["gocache"]["sha256"]
            info["manifest_sha256"] = hashlib.sha256(raw).hexdigest()
            info["copy"] = clone(entry / "gocache", gocache)
            if digest(gocache)["sha256"] == want:
                info.update(status="warm", gocache_sha256=want)
                return {"GOCACHE": str(gocache)}, dict(info, seconds=round(time.monotonic() - t0, 3))
            info["reason"] = "copy does not match the manifest"
    except Exception as e:  # never fail the run: build cold instead
        info["reason"] = f"{type(e).__name__}: {e}"[:300]
    if os.path.lexists(gocache):
        shutil.rmtree(gocache, ignore_errors=True)
    gocache.mkdir(parents=True, exist_ok=True)
    info.pop("copy", None)
    print(f"go cache: cold build for {task.name} ({info.get('reason')})", file=sys.stderr)
    return {"GOCACHE": str(gocache)}, dict(info, seconds=round(time.monotonic() - t0, 3))


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


if __name__ == "__main__":
    main()
