"""Offline preparation and bounded process handling shared by shape1 tools."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import signal
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME = Path.home()
MANAGER = Path(os.environ.get('SHAPE_SOURCE_ROOT', str(ROOT.parent))).resolve()
SEALED = Path(os.environ.get('SHAPE_SEALED_ROOT', '/benchmark-root/shape1-private' if platform.system()=='Linux' else str(HOME / 'bench-sealed' / 'shape1'))).resolve()
CELLS = HOME / "bench-cells"
LANGS = ("rust", "go", "ts-bun")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def reserve_json(path,data):
    """Atomic single-use reservation for an irreversible model-pass budget."""
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(data,indent=2,sort_keys=True)+'\n')


def task_source(task):
    plan = json.loads((ROOT / "plan.json").read_text())
    row = next((r for r in plan["tasks"] if r["id"] == task), None)
    if row is None:
        raise ValueError("task is not registered")
    return MANAGER / row["source"]


def tool_env(work):
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    if platform.system()=='Linux':
        pins=Path('/benchmark-root/toolchains')
        return {'HOME':'/tmp/bench-home','LANG':'C.UTF-8','CI':'1','MAKEFLAGS':'-e',
                'PATH':':'.join(str(pins/p/'bin') for p in ('go-1.27.1','rust-1.97.1','bun-1.4.2','python-3.14.7'))+':/opt/bench/tools/bin:/usr/bin:/bin',
                'PYTHONPATH':str(pins/'python-3.14.7/lib/python3.14/site-packages'),
                'RUSTUP_HOME':'/opt/bench/rustup','CARGO_HOME':'/tmp/cargo-home',
                'CARGO_NET_OFFLINE':'true','GOPROXY':'off','GOSUMDB':'off','GOTOOLCHAIN':'local',
                'GOROOT':str(pins/'go-1.27.1/go'),'GOMODCACHE':str(pins/'go-1.27.1/cache/gomodcache'),
                'GOCACHE':'/tmp/go-cache','GOLANGCI_LINT_CACHE':'/tmp/lint-cache',
                'BENCH_RUST_VENDOR':str(pins/'rust-1.97.1/vendor'),
                'BENCH_NODE_TEMPLATE':str(pins/'bun-1.4.2/node-template'),
                'BENCH_OFFLINE':'1','TMPDIR':'/tmp','PYTHONDONTWRITEBYTECODE':'1','NO_COLOR':'1'}
    script = HOME / "bench-toolchains/env.sh"
    if not script.is_file():
        raise RuntimeError("missing pinned ~/bench-toolchains/env.sh")
    p = subprocess.run(["/usr/bin/env", "-i", f"HOME={HOME}", "PATH=/usr/bin:/bin",
                        "/bin/bash", "-c", 'source "$1" >/dev/null 2>&1; env -0',
                        "shape-env", str(script)], capture_output=True, check=True)
    sourced = dict(x.decode().split("=", 1) for x in p.stdout.split(b"\0") if b"=" in x)
    names = {"PATH", "CARGO_HOME", "RUSTUP_HOME", "BENCH_RUST_VENDOR", "BENCH_NODE_TEMPLATE"}
    env = {k: v for k, v in sourced.items() if k in names}
    env.update(HOME=str(HOME), LANG="C.UTF-8", CI="1", MAKEFLAGS="-e",
               GOPROXY="off", GOSUMDB="off", GOTOOLCHAIN="local", GOFLAGS="-mod=mod",
               GOROOT=str(HOME / "bench-toolchains/go-1.27.1"),
               GOMODCACHE=str(work / "gomodcache"), GOCACHE=str(work / "gocache"),
               GOLANGCI_LINT_CACHE=str(work / "lintcache"),
               CARGO_NET_OFFLINE="true", RUSTUP_TOOLCHAIN="1.97.1", BENCH_OFFLINE="1",
               TMPDIR=str(work), PYTHONDONTWRITEBYTECODE="1", NO_COLOR="1")
    return env


def preflight(lang, env, dependencies=True):
    commands = {"rust": [("rustc", "--version"), ("cargo", "--version")],
                "go": [("go", "version"), ("golangci-lint", "version")],
                "ts-bun": [("bun", "--version")]}
    expected = {"rust": "1.97.1", "go": "1.27.1", "ts-bun": "1.4.2"}[lang]
    versions = {}
    for command in commands[lang]:
        p = subprocess.run(command, env=env, capture_output=True, text=True, timeout=30)
        versions[command[0]] = p.stdout.strip()
        if p.returncode or (command[0] != "golangci-lint" and expected not in p.stdout):
            raise RuntimeError(f"pinned {command[0]} {expected} unavailable")
    if dependencies and lang == "rust" and not Path(env["BENCH_RUST_VENDOR"]).is_dir():
        raise RuntimeError("offline Rust vendor directory missing")
    if dependencies and lang == "ts-bun":
        template = Path(env["BENCH_NODE_TEMPLATE"])
        if not (template / "node_modules/typescript/bin/tsc").is_file() or not (template / "bun.lock").is_file():
            raise RuntimeError("offline Bun node-template dependencies missing")
    return versions


def snapshot(repo):
    rows = {}
    for p in sorted(Path(repo).rglob("*")):
        rel = p.relative_to(repo)
        if any(x in {".git", "target", "node_modules", ".cache", "bin", "__pycache__"} for x in rel.parts):
            continue
        if p.is_symlink():
            raise ValueError(f"symlink in task input/output: {rel}")
        if p.is_file():
            rows[str(rel)] = digest(p)
    return rows


def copy_repo(source, target, task, lang, env):
    # Never copy Git history, which can contain a reference implementation.
    shutil.copytree(source, target, ignore=shutil.ignore_patterns(
        ".git", "target", "bin", ".cache", "node_modules", "__pycache__"), symlinks=True)
    if platform.system()=='Linux':
        snapshot(target)
        return []
    ports = []
    for p in target.rglob("*"):
        if p.is_symlink():
            raise ValueError(f"non-public symlink in repo: {p.relative_to(target)}")
        if not p.is_file():
            continue
        if p.name == "config.toml" and p.parent.name == ".cargo":
            import re
            text = p.read_text()
            changed = re.sub(r'directory\s*=\s*"[^"]+"',
                             'directory = ' + json.dumps(env["BENCH_RUST_VENDOR"]), text)
        elif p.suffix in {".sh", ".ts"} or p.name == "Makefile":
            text = p.read_text()
            import re
            changed = re.sub(r"/benchmark-root/toolchains/bun-[^/]+/node-template",
                             "${BENCH_NODE_TEMPLATE}", text)
            if platform.system() == "Darwin" and task == "c4-4" and p.name == "locking.ts":
                changed = changed.replace("libc.so.6", "/usr/lib/libSystem.B.dylib")
        else:
            continue
        if changed != text:
            for i, (old, new) in enumerate(zip(text.splitlines(), changed.splitlines()), 1):
                if old != new:
                    ports.append({"file": str(p.relative_to(target)), "line": i, "before": old, "after": new})
            p.write_text(changed)
    snapshot(target)
    return ports


def group_members(pgid):
    # killpg(..., 0) queries kernel existence without signaling a process. This
    # proves an empty process group even in a workspace that disallows /bin/ps.
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return []
    return [pgid]  # present; exact membership is immaterial to the empty proof


def fence(proc):
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(proc.pid, sig)
        except ProcessLookupError:
            pass
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            pass
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline and group_members(proc.pid):
            time.sleep(.05)
    remaining = group_members(proc.pid)
    if remaining:
        raise RuntimeError("process group did not empty; retain seal and block")


def run(argv, cwd, env, log, timeout=180, prefix=()):
    log = Path(log)
    log.parent.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    with log.open("wb") as f:
        proc = subprocess.Popen([*prefix, *map(str, argv)], cwd=cwd, env=env,
                                stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
        timed_out = False
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
        finally:
            fence(proc)
    return {"rc": proc.returncode, "timeout": timed_out, "wall_seconds": round(time.monotonic()-start, 3),
            "log_sha256": digest(log), "leftovers": 0}


def sandbox_prefix(denied, network=True):
    if platform.system() != "Darwin":
        raise RuntimeError("Linux isolation adapter not installed")
    profile = '(version 1) (allow default)'
    if network:
        profile += ' (deny network*)'
    for p in denied:
        profile += ' (deny file-read* file-write* (subpath ' + json.dumps(str(Path(p).resolve())) + '))'
    prefix = ["/usr/bin/sandbox-exec", "-p", profile]
    p = subprocess.run([*prefix, "/usr/bin/true"], capture_output=True)
    if p.returncode:
        raise RuntimeError("required Seatbelt isolation unavailable; refusing execution")
    return prefix
