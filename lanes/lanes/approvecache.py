"""Reuse of successful preflight approvals whose every input is identical (`LANES_APPROVAL_CACHE`).

A preflight approval is a deterministic local check: Kogen `intent approve` in a scratch workspace built from
the task's `start/`, its `task.toml` commands, the supplied Intent and the lane's settings. Its key covers all
of that: the task inputs, the supplied Intent, the slug and Intent form, the generated `.kogen/project.yaml`
(lane models, setup/check/acceptance commands, the npm cache entry each setup restores), each npm entry's
manifest, the approval deadline, the Kogen executable and its whole release folder, the lane's lock entry
(Kogen sha, patch and artifact hashes), Node, the environment Kogen inherits, and the harness code that
builds the workspace. Only `ok` approvals with a printed SHA-256 are stored. Timeouts are never stored; a
real refusal leaves a marker that blocks reuse for that key. Without `LANES_APPROVAL_CACHE` nothing changes.
"""

import datetime
import hashlib
import json
import os
import re
import shutil
import socket
import tomllib

from . import common

SCHEMA = 1
HASH = re.compile(r"^[0-9a-f]{64}$")
CODE = ("approvecache.py", "cell.py", "common.py", "node_modules.py", "preflight.py")
# Never reach Kogen or do not change what approve decides; everything else in the environment is keyed.
#   KOGEN_LANES_*: Cell removes them. GIT_AUTHOR/COMMITTER_*: the workspace repo sets its own identity.
#   SLOTS, DAYDIR, DAYCAP, LANES_*: dispatch and grading settings of the shell scripts, not read by approve.
#   TMPDIR, LANES_ENV: per-unit scratch paths (the host's queue entry script); the workspace path is never an input.
SKIP_ENV = {"TMPDIR", "LANES_ENV", "PWD", "OLDPWD", "SHLVL", "_", "SLOTS", "DAYDIR", "DAYCAP", "TERM", "SSH_CLIENT", "SSH_CONNECTION",
            "SSH_TTY", "SSH_AUTH_SOCK", "GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL", "GIT_COMMITTER_NAME",
            "GIT_COMMITTER_EMAIL", "LANES_CARRY_ACTIVE", "LANES_SHARED_GOCACHE", "LANES_NM_CACHE", "LANES_DIR",
            "LANES_NPMFIX_HARNESS", "LANES_APPROVAL_CACHE", "LANES_GUARD_LOG"}
SKIP_PREFIX = ("KOGEN_LANES_", "XPC_", "__CF")
SHIM_DIR = ".lanes-shim"  # the day runners' killall/pkill guards only
TOOLS = ("node", "npm", "npx", "go", "gofmt", "git", "mix", "elixir", "erl", "python3", "make", "bash", "sh", "cargo")
_release_memo = {}


def root():
    """The cache folder, or None when reuse is off."""
    path = os.environ.get("LANES_APPROVAL_CACHE")
    return os.path.abspath(path) if path else None


def tree(path, exclude=()):
    """Digest of a folder: every entry's path and type, symlink targets, executable bits and file contents."""
    h = hashlib.sha256()
    if not os.path.isdir(path):
        h.update(b"absent")
        return h.hexdigest()
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames.sort()
        rel_dir = os.path.relpath(dirpath, path).replace(os.sep, "/")
        links = [d for d in dirnames if os.path.islink(os.path.join(dirpath, d))]
        dirnames[:] = [d for d in dirnames if d not in links and not (rel_dir == "." and d in exclude)]
        h.update(f"d {rel_dir}\n".encode())
        for name in sorted(filenames + links):
            if rel_dir == "." and name in exclude:
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, path).replace(os.sep, "/")
            if os.path.islink(full):
                h.update(f"l {os.readlink(full)} {rel}\n".encode())
            else:
                mode = "x" if os.stat(full).st_mode & 0o111 else "f"
                h.update(f"{mode} {common.sha256_file(full)} {rel}\n".encode())
    return h.hexdigest()


def _file(path):
    return common.sha256_file(path) if os.path.isfile(path) else "absent"


def kogen_digest(kogen, release):
    """The executable and, for an unpacked release, the whole release folder (its `node-path` is keyed apart)."""
    st = os.stat(kogen)
    memo = (os.path.realpath(kogen), st.st_ino, st.st_size, st.st_mtime_ns, release)
    if memo not in _release_memo:
        _release_memo[memo] = {"kogen": common.sha256_file(kogen),
                               "release": tree(release, exclude=("node-path", "node-path.tmp")) if release else None}
    return _release_memo[memo]


def environment():
    """What Kogen and the setup/check commands inherit: the environment (values hashed, never stored), the PATH
    without the guard-shim folder and repeated entries, what each common tool resolves to, and the global mise
    configuration that picks tool versions behind mise shims."""
    env = {k: v for k, v in os.environ.items() if k not in SKIP_ENV and not k.startswith(SKIP_PREFIX)}
    seen, path = set(), []
    for entry in os.environ.get("PATH", "").split(os.pathsep):
        if entry and os.path.basename(entry.rstrip("/")) != SHIM_DIR and entry not in seen:
            seen.add(entry)
            path.append(entry)
    env["PATH"] = os.pathsep.join(path)
    tools = {}
    for name in TOOLS:
        found = shutil.which(name, path=env["PATH"])
        if found:
            real = os.path.realpath(found)
            st = os.stat(real)
            tools[name] = [found, real, st.st_size, st.st_mtime_ns]
    home = os.environ.get("HOME", "")
    mise_dir = os.environ.get("MISE_CONFIG_DIR") or os.path.join(home, ".config", "mise")
    configs = {p: _file(p) for p in (os.path.join(mise_dir, "config.toml"), os.path.join(home, ".tool-versions"),
                                    os.path.join(home, ".mise.toml"))}
    kogen_home = os.path.join(home, ".kogen")
    kogen_config = {n: _file(os.path.join(kogen_home, n)) for n in sorted(os.listdir(kogen_home))
                    if os.path.isfile(os.path.join(kogen_home, n))} if os.path.isdir(kogen_home) else {}
    return {"env": hashlib.sha256(json.dumps(env, sort_keys=True).encode()).hexdigest(), "env_names": sorted(env),
            "tools": tools, "mise_config": configs, "kogen_home_config": kogen_config}


def lock_entry(run_dir, lane, artifact):
    if artifact is not None:
        return {"artifact": os.path.realpath(artifact)}
    for entry in common.read_json(os.path.join(run_dir, "lanes.lock.json")):
        if entry.get("name") == lane:
            return {k: entry.get(k) for k in ("sha", "patch_sha256", "artifact_sha256", "kogen_version")}
    return {"missing": lane}


def npm_entries(config):
    """Every npm cache entry the setup commands restore, by its manifest."""
    entries = sorted(set(re.findall(r"--entry (\S+?)'?(?:\)|$|\s)", config, re.M)))
    return {e: _file(os.path.join(e, "manifest.json")) for e in entries}


def key(exp, run_dir, task, slug, supplied, kogen, config, deadline_s, lane, artifact, node):
    """`(key, components)`: the digest of every approval input, and the per-input digests behind it."""
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(task, "task.toml"), "rb") as f:
        tomllib.load(f)  # the same parse check_one made
    env = environment()
    components = {
        "schema": SCHEMA,
        "host": socket.gethostname(),
        "task_toml": _file(os.path.join(task, "task.toml")),
        "start": tree(os.path.join(task, "start")),
        "supplied": tree(supplied),
        "intent_form": exp["intent_form"],
        "slug": slug,
        "project_yaml": hashlib.sha256(config.encode()).hexdigest(),
        "npm_entries": npm_entries(config),
        "deadline_s": deadline_s,
        "lane_lock": lock_entry(run_dir, lane["name"], artifact),
        "kogen": kogen_digest(kogen, os.path.dirname(os.path.dirname(kogen))
                              if os.path.isfile(os.path.join(os.path.dirname(os.path.dirname(kogen)), "install.sh"))
                              else None),
        "node": node,
        "environment": {k: v for k, v in env.items() if k != "env_names"},
        "harness": {n: _file(os.path.join(here, n)) for n in CODE},
    }
    digest = hashlib.sha256(json.dumps(components, sort_keys=True).encode()).hexdigest()
    return digest, components


def _paths(digest):
    base = os.path.join(root(), digest[:2])
    return os.path.join(base, digest + ".json"), os.path.join(base, digest + ".refused.json")


def lookup(digest):
    """The stored record for an identical earlier `ok` approval, or None (missing, malformed or refused once)."""
    if root() is None:
        return None
    ok_path, refused_path = _paths(digest)
    if os.path.exists(refused_path):
        return None
    try:
        rec = common.read_json(ok_path)
    except (OSError, ValueError):
        return None
    if rec.get("schema") != SCHEMA or rec.get("key") != digest or rec.get("ok") is not True \
            or not HASH.match(str(rec.get("approval_hash", ""))):
        return None
    return rec


def store(digest, components, ok, timeout, approval_hash, context):
    """Record an `ok` approval with its SHA-256, or mark a real refusal; a timeout leaves no trace here."""
    if root() is None or timeout:
        return
    ok_path, refused_path = _paths(digest)
    utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        if ok and approval_hash and HASH.match(approval_hash):
            common.write_json(ok_path + f".{os.getpid()}", {
                "schema": SCHEMA, "key": digest, "ok": True, "approval_hash": approval_hash, "utc": utc,
                "context": context, "components": components})
            os.replace(ok_path + f".{os.getpid()}", ok_path)
        elif not ok:
            common.write_json(refused_path + f".{os.getpid()}", {"schema": SCHEMA, "key": digest, "utc": utc,
                                                                  "context": context})
            os.replace(refused_path + f".{os.getpid()}", refused_path)
    except OSError:
        pass  # reuse is an optimization; the approval result itself stands
