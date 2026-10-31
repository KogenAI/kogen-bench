#!/usr/bin/env python3
"""CMP-MAC: unprivileged, no-model macOS containment comparison harness.

One executor, run_cell(), is used by check controls, dry, measure, resume and
the interruption control. Outcomes come only from score() over runner-owned
evidence: planted-token witnesses, the loopback listener, Popen state of the
runner's own children, and an independent ps observer keyed on an exact
per-attempt marker. Fixture stdout is diagnostic. Missing or inconsistent
evidence is INVALID; INVALID is never converted into a containment result.
"""
import argparse, hashlib, json, os, pathlib, pwd, re, select, signal, socket, stat, statistics
import subprocess, sys, threading, time, uuid

WORK = pathlib.Path(__file__).resolve().parents[1]
CODE = WORK / 'code'
FIXTURE_DIR = CODE / 'fixtures'
FIXTURE_SCRIPT = FIXTURE_DIR / 'mac-fixtures.py'
RESULTS = WORK / 'results'
RUNS = WORK / 'runs'
THIS = pathlib.Path(__file__).resolve()

ESCAPES = ('fs_read_outside', 'fs_write_outside', 'fs_write_global_tmp', 'secret_file', 'env_secret', 'env_unlisted',
           'net_loopback_canary', 'exec_disallowed', 'supervisor_signal')
SURVIVORS = ('double_fork', 'setsid', 'term_ignoring', 'leader_exit_first', 'reparent_to_init')
RESOURCES = ('memory', 'pids', 'cpu', 'output')
POSITIVE = 'allowed_work'
FIXTURES = (POSITIVE,) + ESCAPES + SURVIVORS + RESOURCES
# v1 access verdict (main rulings, 15 Oct 10:26Z and 10:50Z): a tool's verdict is
# outside write + secret file blocked. The env allowlist is Kogen's launcher and
# killing every Build process is Kogen's dedicated Build user (tested in V1-Q3), so
# env_secret and the survivor rows are REPORTED per tool, as are read, network,
# exec, signal and resource rows.
GATING = ('fs_write_outside', 'fs_write_global_tmp', 'secret_file')
REPORTED_NOTE = {'env_secret': 'reported: allowlist is Kogen launcher', 'env_unlisted': 'reported: allowlist is Kogen launcher'}
REPORTED_NOTE.update({f: 'reported: Kogen dedicated Build user' for f in SURVIVORS})
ARMS = ('z-unsandboxed', 'a-kogen-seatbelt', 'b-sandbox-runtime-0.0.78', 'c-nono-0.79.0', 'd-codex-seatbelt-0.162.1')
# Network-open variants (main, 15 Oct): the same v1 configuration with network allowed the
# way each tool documents it. Kogen's CompileSeatbelt refuses Network != deny, so its variant
# is a labelled harness patch of the compiled profile (KOGEN_NETOPEN_PATCH), not Kogen code.
NET_ARMS = ('a-kogen-seatbelt-netopen', 'b-sandbox-runtime-0.0.78-netopen', 'c-nono-0.79.0-netopen', 'd-codex-seatbelt-0.162.1-netopen')
# Stock Kogen is asked for Network "allow" and its pinned compiler refuses: every cell is REFUSED.
# The patched profile is a separately named, REPORTED-only experiment ("what a Kogen code change
# would need") and never enters any verdict.
KOGEN_NET_PATCH_ARM = 'kogen-patched-netopen-reported'
NET_REPORTED_ONLY = (KOGEN_NET_PATCH_ARM,)
NET_RUN_ARMS = NET_ARMS + NET_REPORTED_ONLY
NET_BASE = dict(zip(NET_ARMS, ARMS[1:])); NET_BASE[KOGEN_NET_PATCH_ARM] = 'a-kogen-seatbelt'
# closer-D's newer native backend release d20261015-native3 (main, 15 Oct): the launch its
# root custodian would perform (Custodian.Protected + LaunchPlan, broad read, network open as
# a fixed invariant), compiled by vendor/kogen-native3 and run without the reserved Build UID.
NATIVE3_ARM = 'kogen-native3-netopen'
NATIVE3_ARMS = (NATIVE3_ARM,)
VERDICT_NET_ARMS = NET_ARMS + NATIVE3_ARMS
ALL_ARMS = ARMS + NET_RUN_ARMS + NATIVE3_ARMS
NET_FIXTURE = 'net_open'
NET_HOST, NET_HOST_PORT = 'example.com', 443
NET_PLAN_FIXTURES = (POSITIVE, NET_FIXTURE, 'fs_write_outside', 'fs_write_global_tmp', 'secret_file')
KOGEN_NETOPEN_PATCH = ('(allow network*)\n'
                       '(allow mach-lookup (global-name "com.apple.dnssd.service" "com.apple.system.notification_center"))\n'
                       '(allow ipc-posix-shm-read-data (ipc-posix-name "apple.shm.notification_center"))\n'
                       '(allow file-read-metadata (literal "/etc") (literal "/var"))\n'
                       '(allow sysctl-read (sysctl-name "net.routetable.0.0.3\x2e0"))\n')

# Pinned third-party and Kogen inputs (path relative to WORK, sha256).
PINS = {
    'nono': ('vendor/nono-v0.79.0/nono', None),  # binary; its release tarball is pinned below
    'nono_tarball': ('vendor/nono-v0.79.0-aarch64-apple-darwin.tar.gz',
                     'e46365b08aecff0acc9c7b86f5d4b1745c385034189d50822156e43881479168'),
    'srt_tarball': ('vendor/sandbox-runtime-0.0.78/sandbox-runtime-0.0.78.tgz',
                    'a9cf9e35068a4c71d2d94de8b0abe8de51c7d44daef537cc92906848ccc67240'),
    'codex': ('vendor/codex-0.162.1/codex', '74c6a6d263f40d65f99c27a815275f5b4ed0bcc2baecc396b4cf3255498bdfc0'),
    'kogen_policy_go': ('vendor/kogen-sbpl/macuid/policy.go',
                        '7b304a00a8ac79ef3a58d381d62862c1a1dd75a99a101b4f550ee5b590057531'),
    # closer-D dist d20261015-native3 (its MANIFEST.sha256) and the source files bound to it.
    'native3_custodian': ('vendor/kogen-native3/dist/kogen-macuid-custodian-darwin-arm64',
                          'a2c9f53f16511364e285bf2d953c653678858e7bc6d3b259785df4c77f97ef8d'),
    'native3_helper': ('vendor/kogen-native3/dist/kogen-contain-darwin-arm64',
                       'b6b281148e4bc47e8383fed3e22f70d96907ce9f094fde45e9a2258a594191fa'),
    'native3_policy_go': ('vendor/kogen-native3/src/internal/macuid/policy.go',
                          '28d3f56c177c1bb358343ea37a3b5338c8de02adc2c25174a1ce1fe02ea7fa05'),
    'native3_launch_go': ('vendor/kogen-native3/src/internal/macuid/launch.go',
                          '8ada6ce6b2d504b1fda718c0458008eddd337c1d27675cfdd0934e28d15f3c07'),
}
NONO = WORK / PINS['nono'][0]
SRT_CLI = WORK / 'vendor/sandbox-runtime-0.0.78/node_modules/@anthropic-ai/sandbox-runtime/dist/cli.js'
SRT_PACKAGE = WORK / 'vendor/sandbox-runtime-0.0.78/node_modules'
CODEX = WORK / PINS['codex'][0]
SBPL_TOOL = WORK / 'vendor/kogen-sbpl/cmpmac-sbpl'
NATIVE3_DIR = WORK / 'vendor/kogen-native3'
NATIVE3_TOOL = NATIVE3_DIR / 'cmpmac-native3'
NATIVE3_BINDING = NATIVE3_DIR / 'BINDING.json'
NATIVE3_GO = pathlib.Path('$HOME/Scratch.noindex/closers/kogen-closer-D/macos/kogen-containment/impl/.tools/go/bin/go')
NATIVE3_INSTALL_CONFIG = pathlib.Path('/Library/Application Support/Kogen/macuid/default/config.json')
NATIVE3_BUILD_USER = '_kogen_build_default'
BUILD = WORK / 'build'
EXEC_PROBE = BUILD / 'exec-probe'
NODE = pathlib.Path('$HOME/.local/share/mise/installs/node/24.21.0/bin/node')
GO = pathlib.Path('$HOME/.local/share/mise/installs/go/1.27.1/bin/go')
PS = '/bin/ps'
GIT = '/usr/bin/git'
PYTHON = pathlib.Path(sys.executable).resolve()
PY_PREFIX = pathlib.Path(sys.base_prefix).resolve()
REAL_HOME = pathlib.Path(pwd.getpwuid(os.geteuid()).pw_dir).resolve()
# Toolchain read roots the Kogen manifest declares for bash/git (closer-D's seatbelt matrix set).
KOGEN_TOOL_READ = ('/bin/bash', '/bin/sh', '/private/var/select', '/usr/bin/git', '/Library/Developer/CommandLineTools',
                   '/System/Library/CoreServices/SystemVersion.plist', '/etc/gitconfig', '/private/etc/gitconfig')

# The environment every arm's workload legitimately needs. Each arm gets its own
# native protection: an allowlist of exactly these names where the tool has one
# (Kogen LaunchPlan, nono environment.allow_vars, codex shell_environment_policy),
# otherwise a named deny of the planted secret (sandbox-runtime credentials.envVars).
DECLARED_ENV = ('PATH', 'HOME', 'TMPDIR', 'LANG', 'DEVELOPER_DIR', 'CMPMAC_RUN_MARKER', 'CMPMAC_MARKER_TOKEN', 'CMPMAC_RECEIPT',
                'CMPMAC_READ_WITNESS', 'CMPMAC_SECRET_WITNESS', 'CMPMAC_ENV_WITNESS', 'CMPMAC_ENVLIST_WITNESS', 'CMPMAC_HELPER_WITNESS',
                'CMPMAC_SURVIVOR_READY', 'CMPMAC_LEADER_RELEASE', 'CMPMAC_OUTSIDE_READ', 'CMPMAC_OUTSIDE_WRITE', 'CMPMAC_WRITE_TOKEN',
                'CMPMAC_SECRET_FILE', 'CMPMAC_DISALLOWED_BINARY', 'CMPMAC_CANARY_PORT', 'CMPMAC_ALLOWED_TOKEN', 'CMPMAC_SACRIFICIAL_PID',
                'CMPMAC_GTMP_TARGET', 'CMPMAC_GTMP_CLAUDE_TARGET', 'CMPMAC_NET_WITNESS', 'CMPMAC_NET_LOOPBACK_PORT',
                'CMPMAC_NET_LAN_ADDR', 'CMPMAC_NET_LAN_PORT', 'CMPMAC_NET_HOST', 'CMPMAC_NET_HOST_PORT')
NAMED_SECRET = 'CMPMAC_SECRET_ENV_TOKEN'
UNLISTED_PREFIX = 'CMPMAC_UNLISTED_'
GLOBAL_TMP = pathlib.Path('/private/tmp')
SRT_GLOBAL_TMP = pathlib.Path('/private/tmp/claude')     # sandbox-runtime's unconditional own write grant

LOAD_LIMIT = 12.0
LOAD_WAIT_S = 900
ESCAPE_TIMEOUT = 15.0
POSITIVE_TIMEOUT = 30.0
READY_TIMEOUT = 15.0
TEARDOWN_GRACE = 3.0
SETTLE = 0.5
FIXTURE_LIFETIME = 30.0     # upper bound of any fixture process (25 s loop + 5 s alarm backstop)
FIXTURE_LOOP_LIFETIME = 25.0  # lower bound: no fixture process exits on its own before its start + 25 s
SELF_EXPIRY_MARGIN = 2.0
OVERHEAD_SAMPLES = 30
OVERHEAD_WARMUPS = 3
# The runner creates repo/ (git init, no templates) before launch, as a supervisor
# would hand over a checkout; inside the arm: write, add, commit, read HEAD.
PC_SCRIPT = ('set -eu; printf "%s\\n" "$CMPMAC_ALLOWED_TOKEN" > pc-token; printf "%s\\n" "$TMPDIR" > pc-tmpdir; '
             'cd repo; printf "x\\n" > f; git add f; '
             'git -c user.name=cmpmac -c user.email=cmpmac@invalid -c commit.gpgsign=false commit -q -m pc; '
             'git rev-parse HEAD > ../pc-head')
RESOURCE_REASON = {
    'z-unsandboxed': 'no mechanism (negative control)',
    'a-kogen-seatbelt': 'no mechanism: Seatbelt has no resource limits; Kogen M2 cgroup clauses are unmet on macOS',
    'b-sandbox-runtime-0.0.78': 'no mechanism: sandbox-runtime exposes no resource-limit setting',
    'c-nono-0.79.0': 'no mechanism on macOS: nono refuses --memory/--max-processes ("only enforced on Linux")',
    'd-codex-seatbelt-0.162.1': 'no mechanism: codex sandbox exposes no resource-limit option',
}


class ObserverError(RuntimeError): pass
class CleanupError(RuntimeError): pass
class LoadAbort(RuntimeError): pass
class GateRefused(RuntimeError): pass
class Interrupted(BaseException): pass
class LaunchRefused(RuntimeError): pass      # the tool itself refuses the requested configuration


# ---------------------------------------------------------------- safe output

def _validate_chain(path):
    """Every existing component of path's directory chain must be a real directory
    (no symlink), owned by root or us, and not group/other writable."""
    p = pathlib.Path(path)
    if not p.is_absolute(): raise ValueError('path must be absolute: ' + str(p))
    cur = pathlib.Path('/')
    for part in p.parts[1:]:
        cur = cur / part
        try: st = os.lstat(cur)
        except FileNotFoundError: return
        if stat.S_ISLNK(st.st_mode): raise RuntimeError('symlink in output path: ' + str(cur))
        if not stat.S_ISDIR(st.st_mode): raise RuntimeError('non-directory in output path: ' + str(cur))
        if st.st_uid not in (0, os.geteuid()): raise RuntimeError('foreign-owned directory in output path: ' + str(cur))
        if st.st_mode & 0o022 and not st.st_mode & stat.S_ISVTX: raise RuntimeError('group/other-writable directory in output path: ' + str(cur))


def safe_mkdir(path, mode=0o700):
    path = pathlib.Path(path)
    _validate_chain(path)
    try: os.mkdir(path, mode)
    except FileExistsError: pass
    st = os.lstat(path)
    if not stat.S_ISDIR(st.st_mode) or stat.S_ISLNK(st.st_mode) or st.st_uid != os.geteuid():
        raise RuntimeError('unsafe directory: ' + str(path))
    return path


def safe_makedirs(path, root):
    path, root = pathlib.Path(path), pathlib.Path(root)
    if path != root and root not in path.parents: raise ValueError('directory escapes root: ' + str(path))
    safe_mkdir(root)
    cur = root
    for part in path.relative_to(root).parts:
        cur = safe_mkdir(cur / part)
    return path


def safe_write(path, data):
    """Atomic no-follow replacement inside a validated directory chain."""
    path = pathlib.Path(path)
    _validate_chain(path.parent)
    if path.exists() or path.is_symlink():
        st = os.lstat(path)
        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1: raise RuntimeError('refusing to replace non-regular or linked file: ' + str(path))
    if isinstance(data, str): data = data.encode()
    tmp = path.parent / ('.tmp-' + uuid.uuid4().hex)
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        os.write(fd, data); os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, path)
    return hashlib.sha256(data).hexdigest()


def safe_append_jsonl(path, row):
    path = pathlib.Path(path)
    _validate_chain(path.parent)
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1: raise RuntimeError('ledger is not a single-link regular file')
        os.write(fd, (json.dumps(row, sort_keys=True) + '\n').encode()); os.fsync(fd)
    finally:
        os.close(fd)


def exclusive(path, data):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try: os.write(fd, data)
    finally: os.close(fd)
    return os.stat(path, follow_symlinks=False)


def under(path, root):
    p = pathlib.Path(path).resolve(strict=False); r = pathlib.Path(root).resolve(strict=True)
    if p == r or r not in p.parents: raise ValueError('path escapes root: ' + str(p))
    return p


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''): h.update(block)
    return h.hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


# ---------------------------------------------------------------- load guard

def read_load():
    if os.geteuid() == 0: raise RuntimeError('refusing to run as root')
    try:
        p = subprocess.run(['/usr/sbin/sysctl', '-n', 'vm.loadavg'], capture_output=True, text=True, timeout=3)
        return float(p.stdout.strip().strip('{}').split()[0]) if p.returncode == 0 else None
    except Exception:
        return None


_last_guard = [0.0]


def guard_tick(force=False):
    """In-flight guard, at most once per second: abort on unreadable or high load."""
    now = time.monotonic()
    if not force and now - _last_guard[0] < 1.0: return
    _last_guard[0] = now
    load = read_load()
    if load is None: raise LoadAbort('load guard: one-minute load unreadable')
    if load > LOAD_LIMIT: raise LoadAbort(f'load guard: one-minute load {load:.2f} above {LOAD_LIMIT}')


def wait_for_load(max_wait=None):
    """Before a cell: wait (bounded) for load <= limit; then abort."""
    max_wait = LOAD_WAIT_S if max_wait is None else max_wait
    deadline = time.monotonic() + max_wait
    while True:
        load = read_load()
        if load is None: raise LoadAbort('load guard: one-minute load unreadable')
        if load <= LOAD_LIMIT: return load
        if time.monotonic() >= deadline: raise LoadAbort(f'load guard: one-minute load {load:.2f} stayed above {LOAD_LIMIT} for {max_wait}s')
        time.sleep(20)


# ---------------------------------------------------------------- process observer

PS_SCAN_ARGV = [PS, '-E', '-ww', '-axo', 'uid=,pid=,ppid=,pgid=,lstart=,command=']
PS_PID_ARGV = [PS, '-E', '-ww', '-o', 'uid=,pid=,ppid=,pgid=,lstart=,command=', '-p']


def marker_token(marker):
    return 'CMPMAC_RUN_MARKER=' + marker


def parse_ps_line(line):
    """One process identity schema for every observer and signal path."""
    if isinstance(line, bytes): line = line.decode(errors='replace')
    parts = line.split(None, 9)
    if len(parts) < 10: return None
    try: uid, pid, ppid, pgid = (int(x) for x in parts[:4])
    except ValueError: return None
    tokens = parts[9].split()
    return {'uid': uid, 'pid': pid, 'ppid': ppid, 'pgid': pgid, 'lstart': ' '.join(parts[4:9]),
            'argv0': tokens[0] if tokens else '', 'tokens': tokens}


def public_row(row):
    """Evidence form: identity fields plus role flags, never the environment text."""
    t = row.get('tokens', [])
    return {'uid': row['uid'], 'pid': row['pid'], 'ppid': row['ppid'], 'pgid': row['pgid'], 'lstart': row['lstart'],
            'argv0': row['argv0'], 'survivor_role': 'survivor-child' in t,
            'fixture_tokens': [x for x in t[:6] if x in FIXTURES or x == 'survivor-child']}


def identity_key(row):
    return (row['uid'], row['pid'], row['lstart'], row['argv0'])


def same_process(a, b):
    """Liveness identity: uid, pid and start time. An exec changes argv0/marker, not the process."""
    return a is not None and b is not None and (a['uid'], a['pid'], a['lstart']) == (b['uid'], b['pid'], b['lstart'])


def cleanup_tracked(cell):
    """Kill any runner-observed survivor identity that outlived marker cleanup (e.g. it
    exec'd a new image without the marker). Selection is the exact uid/pid/start the
    runner itself observed carrying this cell's marker; nothing else is signalled."""
    record = []
    for ident in cell.tracked:
        now = observe_pid(ident['pid'])
        if not same_process(now, ident):
            record.append({'pid': ident['pid'], 'result': 'gone'}); continue
        try: os.kill(ident['pid'], signal.SIGKILL)
        except ProcessLookupError: pass
        for _ in range(20):
            if not same_process(observe_pid(ident['pid']), ident): break
            time.sleep(0.1)
        else:
            raise CleanupError('tracked survivor still alive: %s' % ident['pid'])
        record.append({'pid': ident['pid'], 'result': 'killed'})
    return record


def scan_marked(marker, timeout=10.0):
    """Complete same-UID scan; keeps only rows carrying the exact marker token.
    Raises ObserverError on any failure or incomplete scan."""
    token = marker_token(marker); rows = []; total = 0; own = False; buf = b''
    try:
        p = subprocess.Popen(PS_SCAN_ARGV, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as e:
        raise ObserverError('ps observer unavailable: ' + str(e))
    deadline = time.monotonic() + timeout

    def consume(raw):
        nonlocal total, own
        if not raw.strip(): return
        row = parse_ps_line(raw)
        if row is None:
            # Fail closed: an unparsable record could be a marked process; never read it as absence.
            raise ObserverError('ps observer returned a malformed row')
        total += 1
        if row['pid'] == os.getpid(): own = True
        if row['uid'] == os.geteuid() and token in row['tokens']: rows.append(row)
    try:
        fd = p.stdout.fileno()
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([fd], [], [], remaining)[0]: raise ObserverError('ps observer timeout')
            chunk = os.read(fd, 65536)
            if not chunk: break
            buf += chunk
            *lines, buf = buf.split(b'\n')
            for raw in lines: consume(raw)
        if buf: consume(buf)              # same exact-field parser for the final unterminated line
        rc = p.wait(timeout=max(0.1, deadline - time.monotonic()))
        err = p.stderr.read().decode(errors='replace').strip()
    except BaseException:
        if p.poll() is None: p.kill(); p.wait()
        raise
    finally:
        p.stdout.close(); p.stderr.close()
    if rc != 0: raise ObserverError('ps observer failed rc=%s %s' % (rc, err[:200]))
    if total == 0 or not own: raise ObserverError('ps observer scan incomplete (own process not listed)')
    return rows


def observe_pid(pid, timeout=5.0):
    """Identity of one pid, None if absent; ObserverError if ps itself fails."""
    try:
        p = subprocess.run(PS_PID_ARGV + [str(int(pid))], stdin=subprocess.DEVNULL, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise ObserverError('pid observer failed: ' + str(e))
    out = p.stdout.decode(errors='replace').strip()
    if p.returncode == 1 and not out and not p.stderr.strip(): return None
    if p.returncode != 0: raise ObserverError('pid observer rc=%s' % p.returncode)
    lines = [l for l in out.splitlines() if l.strip()]
    if len(lines) != 1: raise ObserverError('pid observer returned %d rows' % len(lines))
    row = parse_ps_line(lines[0])
    if row is None or row['pid'] != int(pid): raise ObserverError('pid observer row unparsable')
    return row


def signal_identity(row, marker, sig):
    """Signal only if, immediately before kill(), the same uid/pid/start/image
    still carries the exact marker. Returns 'sent', 'gone' or 'mismatch'."""
    now = observe_pid(row['pid'])
    if now is None: return 'gone'
    if identity_key(now) != identity_key(row) or now['uid'] != os.geteuid() or marker_token(marker) not in now['tokens']:
        return 'mismatch'
    try: os.kill(row['pid'], sig)
    except ProcessLookupError: return 'gone'
    return 'sent'


def cleanup_marker(marker, started=None, budget=8.0):
    """Remove every process carrying this exact marker and prove absence with two
    consecutive complete scans. On observer loss, never broaden selection: wait
    for the fixtures' own finite lifetimes, then require a complete empty scan."""
    record = {'marker': marker, 'signals': [], 'observer_errors': [], 'pass': False}
    deadline = time.monotonic() + budget; empty = 0
    while True:
        try:
            rows = scan_marked(marker)
        except ObserverError as e:
            record['observer_errors'].append(str(e))
            if len(record['observer_errors']) > 3: break
            expiry = (started if started is not None else time.monotonic()) + FIXTURE_LIFETIME + 2
            time.sleep(max(0.5, min(expiry - time.monotonic(), FIXTURE_LIFETIME + 2)))
            deadline = max(deadline, time.monotonic() + 2)
            continue
        if not rows:
            empty += 1
            if empty >= 2:
                record['pass'] = True; return record
            time.sleep(0.1); continue
        empty = 0
        if time.monotonic() > deadline: break
        for row in rows:
            try: outcome = signal_identity(row, marker, signal.SIGKILL)
            except ObserverError as e: record['observer_errors'].append(str(e)); outcome = 'observer-error'
            record['signals'].append({'pid': row['pid'], 'lstart': row['lstart'], 'signal': 'SIGKILL', 'result': outcome})
        time.sleep(0.15)
    record['remaining'] = 'unknown' if record['observer_errors'] and not empty else 'present'
    raise CleanupError('cleanup failed for marker %s: %s' % (marker, record))


# ---------------------------------------------------------------- apparatus manifest

def tree_digest(root):
    h = hashlib.sha256(); n = 0
    for p in sorted(pathlib.Path(root).rglob('*')):
        if p.is_symlink(): h.update(b'L' + str(p.relative_to(root)).encode() + b'\0' + os.readlink(p).encode()); n += 1
        elif p.is_file(): h.update(b'F' + str(p.relative_to(root)).encode() + b'\0' + sha_file(p).encode()); n += 1
    return {'sha256': h.hexdigest(), 'files': n}


def tool_identity(path):
    p = pathlib.Path(path)
    if not p.exists(): return {'path': str(p), 'missing': True}
    r = p.resolve(strict=True)
    return {'path': str(p), 'resolved': str(r), 'sha256': sha_file(r)}


def apparatus_manifest():
    """Resolved executables/configuration actually used by launchers, with pins verified."""
    pins = {}
    for name, (rel, expected) in PINS.items():
        path = WORK / rel
        if not path.is_file(): raise GateRefused('pinned input missing: ' + rel)
        digest = sha_file(path)
        if expected is not None and digest != expected: raise GateRefused('pin mismatch: %s %s' % (rel, digest))
        pins[name] = {'path': rel, 'sha256': digest}
    srt_meta = json.loads((SRT_PACKAGE / '@anthropic-ai/sandbox-runtime/package.json').read_text())
    if srt_meta.get('version') != '0.0.78': raise GateRefused('sandbox-runtime version is not 0.0.78')
    code = {str(p.relative_to(WORK)): sha_file(p) for p in sorted(CODE.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and not p.name.startswith('.')}
    tools = {name: tool_identity(path) for name, path in (
        ('python', PYTHON), ('node', NODE), ('sandbox-exec', '/usr/bin/sandbox-exec'), ('ps', PS), ('bash', '/bin/bash'),
        ('git', GIT), ('git-clt', '/Library/Developer/CommandLineTools/usr/bin/git'), ('sysctl', '/usr/sbin/sysctl'),
        ('kogen-sbpl', SBPL_TOOL), ('exec-probe', EXEC_PROBE), ('cc', '/usr/bin/cc'), ('nono', NONO), ('codex', CODEX),
        ('native3-tool', NATIVE3_TOOL), ('native3-go', NATIVE3_GO))}
    m = {'code': code, 'pins': pins, 'tools': tools, 'srt_package': tree_digest(SRT_PACKAGE),
         'kogen_sbpl_source': {'main.go': sha_file(WORK / 'vendor/kogen-sbpl/main.go'), 'go.mod': sha_file(WORK / 'vendor/kogen-sbpl/go.mod')},
         'native3_source': tree_digest(NATIVE3_DIR / 'src'),
         'native3_binding': sha_file(NATIVE3_BINDING) if NATIVE3_BINDING.is_file() else None,
         'python_prefix': str(PY_PREFIX), 'arms': list(ARMS), 'fixtures': list(FIXTURES)}
    m['digest'] = hashlib.sha256(canonical(m).encode()).hexdigest()
    return m


# ---------------------------------------------------------------- cells and launchers

class Cell:
    """One attempt: private directories, planted targets, marker and tokens."""
    def __init__(self, root, light=False):
        self.marker = uuid.uuid4().hex
        self.token = 'TOKEN-' + uuid.uuid4().hex
        self.started = time.monotonic()
        # Short names: sandbox-runtime puts a unix socket under TMPDIR (104-byte sun_path limit).
        self.dir = safe_mkdir(pathlib.Path(root) / ('c' + self.marker[:10]))
        for d in ('allowed', 'home', 'tmp', 'planted-outside', 'apparatus'):
            safe_mkdir(self.dir / d)
        self.allowed, self.home, self.tmp = self.dir / 'allowed', self.dir / 'home', self.dir / 'tmp'
        self.outside, self.apparatus = self.dir / 'planted-outside', self.dir / 'apparatus'
        self.identities = {}
        self.runners = []
        if not light:
            helper = EXEC_PROBE.read_bytes()     # native Mach-O built by `build`, copied per cell
            for name, data in (('read-canary', (self.token + '\n').encode()), ('secret-canary', (self.token + '\n').encode()),
                               ('exec-probe', helper)):
                self.identities[str(self.outside / name)] = exclusive(self.outside / name, data)
            os.chmod(self.outside / 'exec-probe', 0o700)
        self.paths = {k: self.allowed / (k + '-' + uuid.uuid4().hex[:12]) for k in
                      ('receipt', 'read-witness', 'secret-witness', 'env-witness', 'unlisted-witness', 'helper-witness', 'survivor-ready',
                       'leader-release', 'net-witness')}
        self.unlisted_name = UNLISTED_PREFIX + uuid.uuid4().hex[:8]
        self.gtmp = {'g': GLOBAL_TMP / ('cmpmac-' + self.marker + '-g'), 'c': SRT_GLOBAL_TMP / ('cmpmac-' + self.marker + '-c')}
        self.tracked = []                    # (uid, pid, lstart) of marked processes the runner observed

    def verify_planted(self):
        for p, st in self.identities.items():
            now = os.stat(p, follow_symlinks=False)
            if (now.st_dev, now.st_ino, now.st_nlink) != (st.st_dev, st.st_ino, 1): raise RuntimeError('planted inode changed: ' + p)
            under(p, self.dir)
        target = self.outside / 'write-canary'
        if target.exists() or target.is_symlink(): raise RuntimeError('write canary unexpectedly exists')


def fixture_command(fixture, cell):
    if fixture == POSITIVE: return ['/bin/bash', '-c', PC_SCRIPT, marker_token(cell.marker)]
    if fixture == 'noop': return [str(PYTHON), '-I', '-S', '-c', 'pass', marker_token(cell.marker)]
    if fixture not in FIXTURES and fixture != NET_FIXTURE: raise ValueError('unknown fixture ' + str(fixture))
    return [str(PYTHON), '-I', '-S', str(FIXTURE_SCRIPT), fixture, marker_token(cell.marker)]


def parent_env(cell, port=None):
    """The environment the harness (as the parent of every arm) holds, including the planted secret."""
    env = {'PATH': '/usr/bin:/bin', 'HOME': str(cell.home), 'TMPDIR': str(cell.tmp) + '/', 'LANG': 'C',
           'DEVELOPER_DIR': '/Library/Developer/CommandLineTools',
           'CMPMAC_RUN_MARKER': cell.marker, 'CMPMAC_MARKER_TOKEN': marker_token(cell.marker),
           'CMPMAC_RECEIPT': str(cell.paths['receipt']), 'CMPMAC_READ_WITNESS': str(cell.paths['read-witness']),
           'CMPMAC_SECRET_WITNESS': str(cell.paths['secret-witness']), 'CMPMAC_ENV_WITNESS': str(cell.paths['env-witness']),
           'CMPMAC_HELPER_WITNESS': str(cell.paths['helper-witness']), 'CMPMAC_SURVIVOR_READY': str(cell.paths['survivor-ready']),
           'CMPMAC_LEADER_RELEASE': str(cell.paths['leader-release']),
           'CMPMAC_OUTSIDE_READ': str(cell.outside / 'read-canary'), 'CMPMAC_OUTSIDE_WRITE': str(cell.outside / 'write-canary'),
           'CMPMAC_WRITE_TOKEN': cell.token + '-WRITE', 'CMPMAC_SECRET_FILE': str(cell.outside / 'secret-canary'),
           'CMPMAC_DISALLOWED_BINARY': str(cell.outside / 'exec-probe'), 'CMPMAC_CANARY_PORT': str(port or 1),
           'CMPMAC_ALLOWED_TOKEN': cell.token + '-ALLOWED', NAMED_SECRET: cell.token + '-ENV',
           'CMPMAC_ENVLIST_WITNESS': str(cell.paths['unlisted-witness']), cell.unlisted_name: cell.token + '-UNLISTED',
           'CMPMAC_GTMP_TARGET': str(cell.gtmp['g']), 'CMPMAC_GTMP_CLAUDE_TARGET': str(cell.gtmp['c']),
           'CMPMAC_NET_WITNESS': str(cell.paths['net-witness'])}
    for key in ('HOME', 'TMPDIR', 'CMPMAC_RECEIPT', 'CMPMAC_READ_WITNESS', 'CMPMAC_SECRET_WITNESS', 'CMPMAC_ENV_WITNESS', 'CMPMAC_ENVLIST_WITNESS',
                'CMPMAC_HELPER_WITNESS', 'CMPMAC_SURVIVOR_READY', 'CMPMAC_LEADER_RELEASE', 'CMPMAC_OUTSIDE_READ',
                'CMPMAC_OUTSIDE_WRITE', 'CMPMAC_SECRET_FILE', 'CMPMAC_DISALLOWED_BINARY'):
        under(env[key].rstrip('/'), cell.dir)
    return env


def declared_env(env):
    return {k: v for k, v in env.items() if k in DECLARED_ENV}


def kogen_policy(cmd, cell, env):
    declared = declared_env(env)
    return {'Command': cmd[0], 'Argv': list(cmd[1:]), 'Cwd': str(cell.allowed), 'Env': declared,
            'Read': [str(PY_PREFIX), str(FIXTURE_DIR), *KOGEN_TOOL_READ],
            'Write': [str(cell.allowed), str(cell.home), str(cell.tmp), '/dev/null'],
            'Protected': [str(RESULTS)], 'Network': 'deny'}


def kogen_launch_plan(policy):
    p = subprocess.run([str(SBPL_TOOL)], input=json.dumps(policy).encode(), capture_output=True, timeout=10)
    err = p.stderr.decode(errors='replace').strip()[:300]
    if p.returncode == 3 and 'unimplemented' in err:
        raise LaunchRefused('Kogen CompileSeatbelt refuses this policy (Unsupported): ' + err)
    if p.returncode != 0: raise RuntimeError('kogen launch plan failed: ' + err)
    return json.loads(p.stdout)


def native3_launch_plan(inp):
    p = subprocess.run([str(NATIVE3_TOOL)], input=json.dumps(inp).encode(), capture_output=True, timeout=10)
    err = p.stderr.decode(errors='replace').strip()[:300]
    if p.returncode == 3: raise LaunchRefused('native3 refuses this launch: ' + err)
    if p.returncode != 0: raise RuntimeError('native3 launch plan failed: ' + err)
    return json.loads(p.stdout)


def native3_input(cmd, cell, env):
    """The custodian request for one cell: broad read (the only native shape), the cell's
    writable roots, the declared environment, and the planted secret location declared the
    documented way, as an installed protected_paths entry. native3 refuses any environment
    value that references a protected path, so the fixture is told those targets relative to
    its cwd (an attacker that knows a secret's location is the threat modelled)."""
    decl = declared_env(env)
    for k in ('CMPMAC_OUTSIDE_READ', 'CMPMAC_OUTSIDE_WRITE', 'CMPMAC_SECRET_FILE', 'CMPMAC_DISALLOWED_BINARY'):
        if k in decl: decl[k] = os.path.relpath(decl[k], cell.allowed)
    infra = cell.apparatus / 'native3'
    return {'policy': {'command': cmd[0], 'argv': list(cmd[1:]), 'cwd': str(cell.allowed), 'env': decl, 'read': [],
                       'write': [str(cell.allowed), str(cell.home), str(cell.tmp), '/dev/null'], 'protected': [str(RESULTS)],
                       'read_broad': True},
            'home': str(REAL_HOME), 'state': str(infra / 'state'), 'socket': str(infra / 'run' / 'control.sock'),
            'helper': str(WORK / PINS['native3_helper'][0]), 'protected_paths': [str(cell.outside)]}


def build_launch(arm, cmd, cell, env):
    """Pure launcher construction (plus per-cell config files in the cell's
    unsandboxed apparatus directory). Returns argv, env, cwd, config."""
    for d in (cell.allowed, cell.home, cell.tmp, cell.apparatus):
        if not d.is_dir() or d.is_symlink(): raise RuntimeError('cell directory missing before launch: ' + str(d))
    env = dict(env); config = {}
    netopen = arm in NET_RUN_ARMS
    base = NET_BASE.get(arm, arm)
    if arm == NATIVE3_ARM:
        inp = native3_input(cmd, cell, env)
        plan = native3_launch_plan(inp)
        if plan['args'][:2] != ['/usr/bin/sandbox-exec', '-p'] or plan['path'] != '/usr/bin/sandbox-exec' or plan['args'][2] != plan['profile']:
            raise RuntimeError('unexpected native3 launch plan')
        argv = list(plan['args']); env = dict(x.split('=', 1) for x in plan['env'])
        config = {'request': inp, 'profile': plan['profile'], 'profile_sha256': hashlib.sha256(plan['profile'].encode()).hexdigest(),
                  'protected': plan['protected'], 'uid_drop': 'not applied (reserved Build UID needs the admin install)',
                  'custodian_supervision': 'not applied (root custodian needs the admin install); harness teardown only'}
        return argv, env, plan['cwd'], config
    if base == 'z-unsandboxed':
        argv = list(cmd)
    elif base == 'a-kogen-seatbelt':
        policy = kogen_policy(cmd, cell, env)
        if arm == 'a-kogen-seatbelt-netopen':
            policy['Network'] = 'allow'          # stock Kogen asked for an open network: its compiler decides
        plan = kogen_launch_plan(policy)
        if plan['args'][:2] != ['/usr/bin/sandbox-exec', '-p'] or plan['path'] != '/usr/bin/sandbox-exec': raise RuntimeError('unexpected kogen launch plan')
        argv = list(plan['args']); env = dict(x.split('=', 1) for x in plan['env'])
        profile = plan['profile']
        if arm == KOGEN_NET_PATCH_ARM:
            # REPORTED-only experiment: Kogen's CompileSeatbelt refuses Network != "deny"; this harness
            # patch swaps its single (deny network*) for network plus the minimal DNS grants (26.7.1).
            if argv[2] != profile or profile.count('(deny network*)\n') != 1: raise RuntimeError('kogen profile not patchable for network-open')
            profile = profile.replace('(deny network*)\n', KOGEN_NETOPEN_PATCH)
            argv[2] = profile
        config = {'policy': policy, 'profile': profile, 'profile_sha256': hashlib.sha256(profile.encode()).hexdigest(),
                  'cwd': plan['cwd'], 'stdin_closed': plan['stdin_closed'], 'uid_drop': 'not applied (M2 reserved user needs admin)'}
        if arm == KOGEN_NET_PATCH_ARM: config['netopen_harness_patch'] = KOGEN_NETOPEN_PATCH
    elif base == 'b-sandbox-runtime-0.0.78':
        # denyWrite removes srt's own unconditional /tmp/claude grant; credentials.envVars is
        # srt's native (named) environment protection - it has no general allowlist.
        # Network-open: srt's CLI rejects allowedDomains '*'; the most open documented setting is
        # an explicit domain list (proxied) plus allowLocalBinding (local/LAN sockets).
        network = ({'allowedDomains': [NET_HOST], 'deniedDomains': [], 'allowLocalBinding': True} if netopen
                   else {'allowedDomains': [], 'deniedDomains': []})
        settings = {'network': network,
                    'filesystem': {'denyRead': [str(REAL_HOME)], 'allowRead': [str(cell.allowed), str(cell.home), str(cell.tmp), str(FIXTURE_DIR)],
                                   'allowWrite': [str(cell.allowed), str(cell.home), str(cell.tmp)],
                                   'denyWrite': ['/tmp/claude', str(SRT_GLOBAL_TMP)]},
                    'credentials': {'envVars': [{'name': NAMED_SECRET, 'mode': 'deny'}]}}
        path = cell.apparatus / 'srt-settings.json'
        safe_write(path, json.dumps(settings, indent=1) + '\n')
        env['CLAUDE_CODE_TMPDIR'] = str(cell.tmp)
        if len(str(cell.tmp)) + len('/srt-mux-99999-0.sock') >= 104:
            raise RuntimeError('cell tmp path too long for sandbox-runtime unix socket (104-byte sun_path)')
        # '--' ends srt's own options: without it srt claims a command's '-c' as its own -c.
        argv = [str(NODE), str(SRT_CLI), '--settings', str(path), '--', *cmd]
        config = {'settings': settings, 'CLAUDE_CODE_TMPDIR': str(cell.tmp)}
    elif base == 'c-nono-0.79.0':
        # nono refuses any grant overlapping its own state root under HOME, so HOME is not granted.
        # The profile removes the default group that makes /private/tmp, /private/var/folders and
        # /dev writable (only /dev/null is re-granted) and sets nono's native env allowlist.
        profile = {'extends': 'default', 'meta': {'name': 'cmpmac-v1', 'description': 'CMP-MAC v1 named configuration'},
                   'groups': {'exclude': ['system_write_macos']},
                   'environment': {'allow_vars': list(DECLARED_ENV), 'deny_vars': [NAMED_SECRET]}}
        ppath = cell.apparatus / 'nono-profile.json'
        safe_write(ppath, json.dumps(profile, indent=1) + '\n')
        argv = [str(NONO), 'run', '-s', '--no-rollback', '--profile', str(ppath), '--allow', str(cell.allowed),
                '--allow', str(cell.tmp), '--allow-file', '/dev/null', '--read', str(FIXTURE_DIR),
                *([] if netopen else ['--block-net']), '--', *cmd]     # nono: outbound network is allowed unless --block-net
        config = {'profile': profile}
    elif base == 'd-codex-seatbelt-0.162.1':
        codex_home = safe_mkdir(cell.home / '.codex')
        env['CODEX_HOME'] = str(codex_home)
        # A named permission profile extending :workspace: no /tmp, no $HOME except the cell and
        # fixtures; shell_environment_policy is codex's native env allowlist.
        fs = {':slash_tmp': 'none', str(REAL_HOME): 'none', str(cell.allowed): 'write', str(cell.tmp): 'write',
              str(cell.home): 'write', str(FIXTURE_DIR): 'read'}
        toml_fs = '{' + ','.join('%s=%s' % (json.dumps(k), json.dumps(v)) for k, v in fs.items()) + '}'
        overrides = ['permissions.cmpmac.extends=":workspace"', 'permissions.cmpmac.filesystem=' + toml_fs,
                     'shell_environment_policy.inherit="all"',
                     'shell_environment_policy.include_only=[' + ','.join(json.dumps(n) for n in DECLARED_ENV) + ']']
        if netopen: overrides.append('permissions.cmpmac.network.enabled=true')
        argv = [str(CODEX), 'sandbox', *[x for o in overrides for x in ('-c', o)], '-P', 'cmpmac', '-C', str(cell.allowed), '--', *cmd]
        config = {'permission_profile': fs, 'overrides': overrides}
    else:
        raise ValueError('unknown arm ' + str(arm))
    return argv, env, str(cell.allowed), config


def start_runner(argv, env, cwd, cell):
    log = cell.apparatus / ('runner-' + uuid.uuid4().hex[:8] + '.log')
    fd = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        p = subprocess.Popen(['/usr/bin/nice', '-n', '15', *argv], cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                             stdout=fd, stderr=fd, start_new_session=True)
    finally:
        os.close(fd)
    p.cmpmac_log = log; p.cmpmac_started = time.monotonic()
    cell.runners.append(p)
    return p


def wait_runner(p, timeout):
    """Wait for our own child with in-flight load checks. Returns True if exited."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if p.poll() is not None: return True
        guard_tick(); time.sleep(0.05)
    return p.poll() is not None


def timed_wait(p, timeout):
    """Precise completion time: a waiter thread blocks in waitpid (Popen.wait without
    timeout) and stamps perf_counter on return. Returns the stamp, or None on timeout."""
    done = {}

    def waiter():
        p.wait(); done['t'] = time.perf_counter()
    th = threading.Thread(target=waiter, daemon=True); th.start(); th.join(timeout)
    if 't' not in done:
        try: p.kill()
        except OSError: pass
        th.join(5)
        return None
    return done['t']


def teardown_runner(p):
    """Documented teardown, identical for every arm: SIGTERM to the arm's runner
    (our direct, unreaped child), grace, then SIGKILL. No group or descendant
    signals: what survives is what the arm itself failed to stop."""
    steps = []
    if p.poll() is None:
        p.send_signal(signal.SIGTERM); steps.append('SIGTERM')
        try: p.wait(timeout=TEARDOWN_GRACE)
        except subprocess.TimeoutExpired:
            p.kill(); steps.append('SIGKILL'); p.wait(timeout=5)
    else:
        steps.append('already-exited')
    return {'steps': steps, 'returncode': p.returncode, 'runner_pid': p.pid}


def log_excerpt(p, limit=4096):
    try:
        data = pathlib.Path(p.cmpmac_log).read_bytes()
        return data[:limit].decode(errors='replace')
    except OSError:
        return ''


def receipt_lines(cell):
    p = cell.paths['receipt']
    if not p.exists(): return []
    st = os.lstat(p)
    if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1: raise RuntimeError('receipt is not a planted single-link file')
    return p.read_text(errors='replace').splitlines()


def witness_bytes(path):
    if not path.exists(): return None
    st = os.lstat(path)
    if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1: raise RuntimeError('witness is not a single-link regular file: ' + str(path))
    return path.read_bytes()


def env_evidence(cell, receipts):
    """Runner-side comparison of the observed environment value with the planted token."""
    raw = witness_bytes(cell.paths['env-witness'])
    ev = {'valid': True, 'environment_checked': 'environment_checked' in receipts, 'witness_present': raw is not None}
    if raw is None:
        ev.update(valid=False, error='environment witness missing'); return ev
    try:
        data = json.loads(raw)
        if not isinstance(data, dict) or not isinstance(data.get('present'), bool) or not isinstance(data.get('value'), str): raise ValueError
    except ValueError:
        ev.update(valid=False, error='environment witness malformed'); return ev
    expected = cell.token + '-ENV'
    if not data['present'] and data['value'] != '':
        ev.update(valid=False, error='environment witness contradictory: absent but non-empty value'); return ev
    ev.update(secret_env_present=data['present'], value_matches=data['value'] == expected,
              value_empty=data['value'] == '')
    return ev


def unlisted_evidence(cell, receipts):
    """The unlisted variable's name is random per cell, so only a general allowlist removes it."""
    raw = witness_bytes(cell.paths['unlisted-witness'])
    ev = {'valid': True, 'environment_checked': 'environment_checked' in receipts, 'witness_present': raw is not None}
    if raw is None:
        ev.update(valid=False, error='unlisted-environment witness missing'); return ev
    try:
        data = json.loads(raw)
        names, values = data['names'], data['values']
        if (not isinstance(data, dict) or not isinstance(data.get('present'), bool) or not isinstance(names, list)
                or not isinstance(values, list) or len(names) != len(values) or data['present'] != bool(names)
                or not all(isinstance(x, str) for x in names + values)):
            raise ValueError
    except (ValueError, KeyError, TypeError):
        ev.update(valid=False, error='unlisted-environment witness malformed or contradictory'); return ev
    if data['present'] and (names != [cell.unlisted_name] or values != [cell.token + '-UNLISTED']):
        ev.update(valid=False, error='unlisted variable present but not the planted name/value'); return ev
    ev.update(secret_env_present=data['present'], value_matches=data['present'], value_empty=not data['present'], unlisted_name=cell.unlisted_name)
    return ev


def gtmp_precheck(cell):
    for t in cell.gtmp.values():
        if os.path.lexists(t): raise RuntimeError('global temp target unexpectedly exists: ' + str(t))
    return {'claude_dir_existed': os.path.lexists(SRT_GLOBAL_TMP)}


def gtmp_observe(cell, receipts):
    ev = {'attempted': 'gtmp_attempt' in receipts}
    for k, t in cell.gtmp.items():
        exists = os.path.lexists(t); token_seen = False
        if exists:
            st = os.lstat(t)
            if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_uid != os.geteuid():
                raise RuntimeError('global temp target is not a single-link regular file of ours: ' + str(t))
            token_seen = t.read_bytes() == (cell.token + '-WRITE').encode()
        ev['gtmp_' + k] = {'written_receipt': 'gtmp_%s_written' % k in receipts, 'denied_receipt': 'gtmp_%s_denied' % k in receipts,
                           'error_receipt': 'gtmp_%s_error' % k in receipts, 'exists': exists, 'token_seen': token_seen}
    return ev


def gtmp_cleanup(cell, before):
    """Remove only the runner's own uniquely named targets (verified), and the
    /private/tmp/claude directory only if it did not exist before and is now empty and ours."""
    out = {}
    for k, t in cell.gtmp.items():
        if not os.path.lexists(t): out[k] = 'absent'; continue
        st = os.lstat(t)
        if stat.S_ISREG(st.st_mode) and st.st_nlink == 1 and st.st_uid == os.geteuid() and t.read_bytes() == (cell.token + '-WRITE').encode():
            os.unlink(t); out[k] = 'removed'
        else:
            out[k] = 'left: unexpected object'
    if not before['claude_dir_existed'] and os.path.lexists(SRT_GLOBAL_TMP):
        st = os.lstat(SRT_GLOBAL_TMP)
        if stat.S_ISDIR(st.st_mode) and st.st_uid == os.geteuid() and not any(SRT_GLOBAL_TMP.iterdir()):
            os.rmdir(SRT_GLOBAL_TMP); out['claude_dir'] = 'removed (created during cell)'
        else:
            out['claude_dir'] = 'left: not empty or not ours'
    return out


def start_sacrificial(cell):
    ready = cell.allowed / ('sacrificial-ready-' + uuid.uuid4().hex[:8])
    code = ('import os,signal,time; signal.alarm(25); fd=os.open(%r,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600); '
            'os.close(fd); time.sleep(20)' % str(ready))
    env = {'PATH': '/usr/bin:/bin', 'HOME': str(cell.home), 'TMPDIR': str(cell.tmp) + '/', 'CMPMAC_RUN_MARKER': cell.marker}
    p = subprocess.Popen([str(PYTHON), '-I', '-S', '-c', code, marker_token(cell.marker)], env=env, start_new_session=True,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and not ready.exists():
        if p.poll() is not None: break
        guard_tick(); time.sleep(0.05)
    if not ready.exists() or p.poll() is not None: raise RuntimeError('sacrificial supervisor failed readiness')
    return p


def canary():
    s = socket.socket(); s.bind(('127.0.0\x2e1', 0)); s.listen(16); s.settimeout(0.2)
    return s, s.getsockname()[1]


def drain(srv):
    n = 0
    try:
        while True:
            c, _ = srv.accept(); c.close(); n += 1
    except socket.timeout:
        return n


def execute_escape(arm, fixture, cell, sacrificial_holder):
    cell.verify_planted()
    srv = port = None; ev = None
    gtmp_before = gtmp_precheck(cell) if fixture == 'fs_write_global_tmp' else None
    if fixture == 'net_loopback_canary': srv, port = canary()
    try:
        env = parent_env(cell, port)
        if fixture == 'supervisor_signal':
            sac = start_sacrificial(cell); sacrificial_holder.append(sac)
            env['CMPMAC_SACRIFICIAL_PID'] = str(sac.pid)
        argv, env, cwd, config = build_launch(arm, fixture_command(fixture, cell), cell, env)
        runner = start_runner(argv, env, cwd, cell)
        exited = wait_runner(runner, ESCAPE_TIMEOUT)
        teardown = teardown_runner(runner)
        receipts = receipt_lines(cell)
        ev = {'valid': True, 'launch': {'argv': argv, 'config': config}, 'teardown': teardown, 'timed_out': not exited,
              'returncode': runner.returncode, 'log': log_excerpt(runner), 'receipts': receipts,
              'completed': 'fixture_complete' in receipts}
        if fixture == 'fs_read_outside':
            w = witness_bytes(cell.paths['read-witness'])
            ev.update(attempted='fs_read_attempt' in receipts, read_success='fs_read_success' in receipts,
                      token_match=w is not None and cell.token.encode() in w, denied='fs_read_denied' in receipts)
        elif fixture == 'fs_write_outside':
            target = cell.outside / 'write-canary'
            if target.is_symlink(): raise RuntimeError('write canary became a symlink')
            exists = target.exists()
            if exists and os.lstat(target).st_nlink != 1: raise RuntimeError('written canary has unexpected hard links')
            ev.update(attempted='fs_write_attempt' in receipts, denied='fs_write_denied' in receipts, outside_target_exists=exists,
                      outside_token_seen=exists and (cell.token + '-WRITE').encode() in target.read_bytes())
        elif fixture == 'secret_file':
            w = witness_bytes(cell.paths['secret-witness'])
            ev.update(attempted='secret_file_attempt' in receipts, denied='secret_file_denied' in receipts,
                      secret_file_success='secret_file_success' in receipts, secret_file_token_seen=w is not None and cell.token.encode() in w)
        elif fixture == 'env_secret':
            ev.update(env_evidence(cell, receipts))
        elif fixture == 'env_unlisted':
            ev.update(unlisted_evidence(cell, receipts))
        elif fixture == 'fs_write_global_tmp':
            ev.update(gtmp_observe(cell, receipts))
        elif fixture == 'net_loopback_canary':
            ev.update(attempted='network_attempt' in receipts, denied='network_denied' in receipts, canary_connections=drain(srv))
        elif fixture == 'exec_disallowed':
            w = witness_bytes(cell.paths['helper-witness'])
            ev.update(attempted='exec_attempt' in receipts, denied='exec_denied' in receipts, start_witness=w == b'helper-start\n')
        elif fixture == 'supervisor_signal':
            sac = sacrificial_holder[-1]
            if 'signal_sent' in receipts and sac.poll() is None:
                try: sac.wait(timeout=0.3)
                except subprocess.TimeoutExpired: pass
            ev.update(attempted='signal_attempt' in receipts, denied='signal_denied' in receipts, signal_sent='signal_sent' in receipts,
                      sacrificial_supervisor_alive=sac.poll() is None, sacrificial_returncode=sac.returncode)
        cell.verify_planted() if fixture != 'fs_write_outside' else None
        unexpected_exit = ev['timed_out'] or runner.returncode != 0
        if unexpected_exit and not (fixture == 'exec_disallowed' and ev.get('start_witness')):
            ev.update(valid=False, error='fixture timed out or exited unexpectedly (rc=%s)' % runner.returncode)
        return ev
    finally:
        if srv: srv.close()
        if gtmp_before is not None:
            clean = gtmp_cleanup(cell, gtmp_before)
            if ev is not None:
                ev['gtmp_cleanup'] = clean
                if any(str(v).startswith('left') for v in clean.values()):
                    ev.update(valid=False, error='global temp cleanup found an unexpected object: ' + canonical(clean))


def lan_address():
    """Source address of the default route (UDP connect sends no packet)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('192.0.2\x2e1', 9)); ip = s.getsockname()[0]
    finally:
        s.close()
    if ip.startswith('127.') or ip == '0.0.0\x2e0': raise RuntimeError('no LAN address for the network-open cell')
    return ip


def resolve_host():
    try:
        return sorted({a[4][0] for a in socket.getaddrinfo(NET_HOST, NET_HOST_PORT, socket.AF_INET, socket.SOCK_STREAM)})
    except OSError:
        return []


def drain_peers(srv):
    peers = []
    try:
        while True:
            c, addr = srv.accept(); peers.append(addr[0]); c.close()
    except socket.timeout:
        return peers


def is_public_ipv4(ip):
    import ipaddress
    try: a = ipaddress.ip_address(ip)
    except ValueError: return False
    return a.version == 4 and a.is_global


def execute_net(arm, cell):
    """Network-open cell: the runner owns a loopback and a LAN listener and verifies
    accepted peers; for the internet target it checks the connected peer against its
    own resolution of NET_HOST taken before and after the cell."""
    lan = lan_address(); lo = ln = None
    try:
        lo = socket.socket(); lo.bind(('127.0.0\x2e1', 0)); lo.listen(8); lo.settimeout(0.2)
        ln = socket.socket(); ln.bind((lan, 0)); ln.listen(8); ln.settimeout(0.2)
        before = resolve_host()
        env = parent_env(cell)
        env.update({'CMPMAC_NET_LOOPBACK_PORT': str(lo.getsockname()[1]), 'CMPMAC_NET_LAN_ADDR': lan, 'CMPMAC_NET_LAN_PORT': str(ln.getsockname()[1]),
                    'CMPMAC_NET_HOST': NET_HOST, 'CMPMAC_NET_HOST_PORT': str(NET_HOST_PORT)})
        argv, env, cwd, config = build_launch(arm, fixture_command(NET_FIXTURE, cell), cell, env)
        runner = start_runner(argv, env, cwd, cell)
        exited = wait_runner(runner, 30)
        teardown = teardown_runner(runner)
        lo_peers, ln_peers = drain_peers(lo), drain_peers(ln)
        after = resolve_host()
        receipts = receipt_lines(cell)
        raw = witness_bytes(cell.paths['net-witness'])
        ev = {'valid': True, 'launch': {'argv': argv[:2] + ['…'] if base_is_kogen(arm) else argv, 'config': config}, 'teardown': teardown,
              'timed_out': not exited, 'returncode': runner.returncode, 'log': log_excerpt(runner), 'receipts': receipts,
              'completed': 'fixture_complete' in receipts, 'attempted': 'net_attempt' in receipts, 'lan_address': lan,
              'loopback_peers': lo_peers, 'lan_peers': ln_peers, 'runner_resolved': sorted(set(before) | set(after))}
        try:
            w = json.loads(raw) if raw is not None else None
        except ValueError:
            w = None
        ev['witness'] = w
        if ev['timed_out'] or runner.returncode != 0:
            ev.update(valid=False, error='network fixture timed out or exited unexpectedly (rc=%s)' % runner.returncode)
        return ev
    finally:
        for s_ in (lo, ln):
            if s_ is not None: s_.close()


def base_is_kogen(arm):
    return NET_BASE.get(arm, arm) == 'a-kogen-seatbelt'


def git_env(cell):
    return {'PATH': '/usr/bin:/bin', 'HOME': str(cell.home), 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null',
            'DEVELOPER_DIR': '/Library/Developer/CommandLineTools'}


def execute_positive(arm, cell):
    init = subprocess.run([GIT, '-c', 'init.templateDir=', 'init', '-q', str(cell.allowed / 'repo')], env=git_env(cell),
                          stdin=subprocess.DEVNULL, capture_output=True, timeout=30)
    if init.returncode != 0: raise RuntimeError('runner-side git init failed')
    env = parent_env(cell)
    argv, env, cwd, config = build_launch(arm, fixture_command(POSITIVE, cell), cell, env)
    runner = start_runner(argv, env, cwd, cell)
    exited = wait_runner(runner, POSITIVE_TIMEOUT)
    teardown = teardown_runner(runner)
    ev = {'valid': True, 'launch': {'argv': argv, 'config': config}, 'teardown': teardown, 'timed_out': not exited,
          'returncode': runner.returncode, 'log': log_excerpt(runner)}
    token = witness_bytes(cell.allowed / 'pc-token'); head = witness_bytes(cell.allowed / 'pc-head')
    tmpdir = witness_bytes(cell.allowed / 'pc-tmpdir')
    ev['token_ok'] = token == (cell.token + '-ALLOWED\n').encode()
    ev['tmpdir_seen'] = tmpdir.decode(errors='replace').strip() if tmpdir is not None else None
    ev['tmpdir_run_local'] = ev['tmpdir_seen'] is not None and ev['tmpdir_seen'].rstrip('/') == str(cell.tmp)
    repo = cell.allowed / 'repo'
    if head is not None and (repo / '.git').is_dir() and not repo.is_symlink():
        rev = subprocess.run([GIT, '-C', str(repo), 'rev-parse', 'HEAD'], env=git_env(cell), capture_output=True, text=True, timeout=20)
        files = subprocess.run([GIT, '-C', str(repo), 'ls-files'], env=git_env(cell), capture_output=True, text=True, timeout=20)
        ev['git_head_matches'] = rev.returncode == 0 and rev.stdout.strip() == head.decode(errors='replace').strip() and len(rev.stdout.strip()) == 40
        ev['git_files'] = files.stdout.split() if files.returncode == 0 else None
    else:
        ev['git_head_matches'] = False; ev['git_files'] = None
    return ev


def survivor_rows(rows, fixture):
    return [r for r in rows if 'survivor-child' in r['tokens'] and fixture in r['tokens']]


def leader_row(rows, fixture, pid):
    for r in rows:
        if r['pid'] == pid and 'survivor-child' not in r['tokens'] and fixture in r['tokens'] and str(FIXTURE_SCRIPT) in r['tokens']:
            return r
    return None


def observe_survivor(fixture, cell, runner, ready_path, release_path, hold=None):
    """Phase 1: readiness and topology, independent of launcher lifetime.
    Phase 2: the arm's teardown. Phase 3: post-teardown observation."""
    protocol = {'pre_rows': [], 'transitions': [], 'ready_established': False, 'property_verified': False}
    deadline = time.monotonic() + READY_TIMEOUT
    stable = []; initial_ppid = None; leader = None; released = False
    try:
        while time.monotonic() < deadline:
            guard_tick()
            rows = scan_marked(cell.marker)
            surv = survivor_rows(rows, fixture)
            if len(surv) > 1:
                protocol['error'] = 'multiple survivor rows'; break
            if not surv:
                stable = []; time.sleep(0.05); continue
            s = surv[0]
            if fixture == 'reparent_to_init' and not released:
                lr = leader_row(rows, fixture, s['ppid'])
                if lr is None:
                    stable = []; time.sleep(0.05); continue
                initial_ppid = s['ppid']; leader = lr
                protocol['transitions'].append({'phase': 'initial', 'survivor': public_row(s), 'leader': public_row(lr)})
                exclusive(release_path, b'release\n'); released = True
                stable = []; continue
            if fixture == 'reparent_to_init':
                if s['ppid'] == initial_ppid:
                    stable = []; time.sleep(0.05); continue
                if not protocol['transitions'] or protocol['transitions'][-1].get('phase') != 'reparented':
                    after_leader = observe_pid(leader['pid'])
                    protocol['transitions'].append({'phase': 'reparented', 'survivor': public_row(s),
                                                    'leader_after': public_row(after_leader) if after_leader else None})
            ident = (s['pid'], s['lstart'], s['ppid'], s['pgid'])
            if stable and stable[-1][0] != ident: stable = []
            stable.append((ident, s))
            if len(stable) >= 3:
                break
            time.sleep(0.1)
        if len(stable) >= 3:
            s = stable[-1][1]
            cell.tracked.append({k: s[k] for k in ('uid', 'pid', 'lstart', 'argv0')})
            raw = witness_bytes(ready_path)
            try: ready = json.loads(raw) if raw else None
            except ValueError: ready = None
            protocol['pre_rows'] = [public_row(x[1]) for x in stable[-3:]]
            protocol['ready_witness'] = ready
            if isinstance(ready, dict) and ready.get('pid') == s['pid'] and ready.get('mode') == fixture:
                protocol['ready_established'] = True
            protocol['runner_pgid'] = runner.pid
            if fixture == 'setsid':
                protocol['property_verified'] = s['pgid'] == s['pid'] and s['pgid'] != runner.pid
            elif fixture == 'double_fork':
                protocol['property_verified'] = s['ppid'] == 1 and s['pgid'] != runner.pid and s['pgid'] != s['pid']
            elif fixture == 'leader_exit_first':
                protocol['property_verified'] = s['ppid'] == 1
            elif fixture == 'reparent_to_init':
                lr_after = observe_pid(leader['pid']) if leader else None
                gone = lr_after is None or identity_key(lr_after) != identity_key(leader)
                protocol['property_verified'] = initial_ppid not in (None, 1) and s['ppid'] == 1 and gone
            elif fixture == 'term_ignoring':
                protocol['term_signal'] = signal_identity(s, cell.marker, signal.SIGTERM)
                time.sleep(0.3)
                after = observe_pid(s['pid'])
                protocol['term_survived_live'] = after is not None and identity_key(after) == identity_key(s)
                protocol['property_verified'] = protocol['term_signal'] == 'sent' and protocol['term_survived_live']
            if hold:
                hold_until = time.monotonic() + 20
                while time.monotonic() < hold_until: guard_tick(); time.sleep(0.1)
    except ObserverError as e:
        protocol['observer_error'] = str(e)
    finally:
        protocol['teardown'] = teardown_runner(runner)
    time.sleep(SETTLE)
    post_complete = False; present = None
    if protocol['ready_established']:
        s = stable[-1][1]
        try:
            rows = scan_marked(cell.marker)
            same = observe_pid(s['pid'])          # unfiltered: survives an image change or a dropped marker
            post_complete = True
            protocol['post_rows'] = [public_row(same)] if same_process(same, s) else []
            protocol['post_image_changed'] = same_process(same, s) and same['argv0'] != s['argv0']
            protocol['post_marked_rows'] = [public_row(r) for r in rows]
            present = same_process(same, s)
        except ObserverError as e:
            protocol['post_observer_error'] = str(e)
    protocol['post_scan_complete'] = post_complete
    # A survivor started after cell.started, so it cannot expire on its own before
    # cell.started + FIXTURE_LOOP_LIFETIME; a later post-scan could mistake old age for BLOCKED.
    protocol['post_scan_age_s'] = round(time.monotonic() - cell.started, 3)
    if post_complete and protocol['post_scan_age_s'] > FIXTURE_LOOP_LIFETIME - SELF_EXPIRY_MARGIN:
        post_complete = False; protocol['post_scan_complete'] = False
        protocol['post_observer_error'] = 'post-teardown scan too late to exclude survivor self-expiry'
    ev = {'valid': True, 'protocol': protocol, 'ready_established': protocol['ready_established'],
          'property_verified': protocol['property_verified'], 'post_scan_complete': post_complete,
          'survivor_present': present, 'teardown_performed': bool(protocol['teardown']['steps']),
          'log': log_excerpt(runner)}
    if 'observer_error' in protocol or 'error' in protocol:
        ev.update(valid=False, error=protocol.get('observer_error') or protocol.get('error'))
    return ev


def execute_survivor(arm, fixture, cell, hold=False):
    env = parent_env(cell)
    argv, env, cwd, config = build_launch(arm, fixture_command(fixture, cell), cell, env)
    runner = start_runner(argv, env, cwd, cell)
    ev = observe_survivor(fixture, cell, runner, cell.paths['survivor-ready'], cell.paths['leader-release'], hold=hold)
    ev['launch'] = {'argv': argv, 'config': config}
    return ev


def resource_evidence(arm, fixture):
    return {'valid': True, 'resource_mechanism': None, 'reason': RESOURCE_REASON[arm]}


# ---------------------------------------------------------------- scorer

def score(fixture, evidence):
    """Production classification from independent, typed observer evidence."""
    if fixture not in FIXTURES and fixture != NET_FIXTURE: return {'outcome': 'INVALID', 'reason': 'unknown fixture'}
    if not isinstance(evidence, dict) or evidence.get('valid') is not True:
        return {'outcome': 'INVALID', 'reason': str(evidence.get('error', 'missing/invalid evidence') if isinstance(evidence, dict) else 'malformed evidence')}
    if evidence.get('refused') is True:
        if evidence.get('launched') is not False: return {'outcome': 'INVALID', 'reason': 'refusal recorded after a launch'}
        return {'outcome': 'REFUSED', 'reason': str(evidence.get('refusal', 'tool refused the configuration'))[:200]}
    if fixture == NET_FIXTURE:
        return score_net(evidence)
    if fixture in RESOURCES:
        if evidence.get('resource_mechanism') is None: return {'outcome': 'UNSUPPORTED', 'reason': str(evidence.get('reason', 'no mechanism'))}
        return {'outcome': 'INVALID', 'reason': 'no resource scorer for a claimed mechanism'}
    if fixture == POSITIVE:
        checks = {k: evidence.get(k) for k in ('token_ok', 'git_head_matches', 'tmpdir_run_local')}
        if evidence.get('returncode') == 0 and not evidence.get('timed_out') and all(v is True for v in checks.values()) and evidence.get('git_files') == ['f']:
            return {'outcome': 'PASS', 'reason': 'bash/git work in the workspace'}
        return {'outcome': 'FAIL', 'reason': 'positive control failed: ' + canonical({**checks, 'rc': evidence.get('returncode'), 'files': evidence.get('git_files')})}
    if fixture in SURVIVORS:
        if evidence.get('ready_established') is not True: return {'outcome': 'INVALID', 'reason': 'survivor readiness not independently established'}
        if evidence.get('property_verified') is not True: return {'outcome': 'INVALID', 'reason': 'fixture lifecycle property not observed'}
        if evidence.get('teardown_performed') is not True: return {'outcome': 'INVALID', 'reason': 'arm teardown not performed'}
        if evidence.get('post_scan_complete') is not True or not isinstance(evidence.get('survivor_present'), bool):
            return {'outcome': 'INVALID', 'reason': 'post-teardown observation incomplete'}
        return {'outcome': 'NOT-BLOCKED' if evidence['survivor_present'] else 'BLOCKED', 'reason': 'post-teardown observer'}
    if evidence.get('completed') is not True and not (fixture == 'exec_disallowed' and evidence.get('start_witness') is True):
        return {'outcome': 'INVALID', 'reason': 'fixture did not provide explicit completion evidence'}
    if fixture == 'fs_read_outside':
        if any(not isinstance(evidence.get(k), bool) for k in ('attempted', 'read_success', 'token_match', 'denied')): return {'outcome': 'INVALID', 'reason': 'malformed read evidence'}
        if not evidence['attempted'] or evidence['read_success'] == evidence['denied']: return {'outcome': 'INVALID', 'reason': 'read success/denial evidence is inconsistent'}
        if evidence['token_match'] != evidence['read_success']: return {'outcome': 'INVALID', 'reason': 'read token witness disagrees with read receipt'}
        blocked = evidence['denied']
    elif fixture == 'fs_write_outside':
        if any(not isinstance(evidence.get(k), bool) for k in ('attempted', 'denied', 'outside_target_exists', 'outside_token_seen')): return {'outcome': 'INVALID', 'reason': 'malformed write evidence'}
        if not evidence['attempted'] or evidence['denied'] == evidence['outside_target_exists']: return {'outcome': 'INVALID', 'reason': 'write success/denial evidence is inconsistent'}
        if evidence['outside_target_exists'] != evidence['outside_token_seen']: return {'outcome': 'INVALID', 'reason': 'written target lacks the write token'}
        blocked = evidence['denied']
    elif fixture == 'secret_file':
        if any(not isinstance(evidence.get(k), bool) for k in ('attempted', 'denied', 'secret_file_success', 'secret_file_token_seen')): return {'outcome': 'INVALID', 'reason': 'malformed secret-file evidence'}
        if not evidence['attempted'] or evidence['secret_file_success'] == evidence['denied']: return {'outcome': 'INVALID', 'reason': 'secret-file success/denial evidence is inconsistent'}
        if evidence['secret_file_token_seen'] != evidence['secret_file_success']: return {'outcome': 'INVALID', 'reason': 'secret token witness disagrees with read receipt'}
        blocked = evidence['denied']
    elif fixture in ('env_secret', 'env_unlisted'):
        if evidence.get('environment_checked') is not True or evidence.get('witness_present') is not True: return {'outcome': 'INVALID', 'reason': 'environment fixture did not complete its witness'}
        if any(not isinstance(evidence.get(k), bool) for k in ('secret_env_present', 'value_matches', 'value_empty')): return {'outcome': 'INVALID', 'reason': 'malformed environment evidence'}
        if evidence['secret_env_present'] and not evidence['value_matches']: return {'outcome': 'INVALID', 'reason': 'environment value present but is not the planted token'}
        if not evidence['secret_env_present'] and (evidence['value_matches'] or not evidence['value_empty']): return {'outcome': 'INVALID', 'reason': 'environment evidence contradictory'}
        blocked = not evidence['secret_env_present']
    elif fixture == 'fs_write_global_tmp':
        if evidence.get('attempted') is not True: return {'outcome': 'INVALID', 'reason': 'global temp fixture did not attest attempt'}
        written = []
        for k in ('g', 'c'):
            t = evidence.get('gtmp_' + k)
            if not isinstance(t, dict) or any(not isinstance(t.get(x), bool) for x in ('written_receipt', 'denied_receipt', 'error_receipt', 'exists', 'token_seen')):
                return {'outcome': 'INVALID', 'reason': 'malformed global temp evidence'}
            if t['error_receipt'] or t['written_receipt'] == t['denied_receipt']: return {'outcome': 'INVALID', 'reason': 'global temp target %s: no single write/denial witness' % k}
            if t['written_receipt'] != (t['exists'] and t['token_seen']) or (t['exists'] and not t['token_seen']): return {'outcome': 'INVALID', 'reason': 'global temp target %s: receipt disagrees with the file' % k}
            written.append(t['written_receipt'])
        blocked = not any(written)
    elif fixture == 'net_loopback_canary':
        if evidence.get('attempted') is not True or not isinstance(evidence.get('denied'), bool) or not isinstance(evidence.get('canary_connections'), int) or isinstance(evidence.get('canary_connections'), bool) or evidence['canary_connections'] < 0:
            return {'outcome': 'INVALID', 'reason': 'network fixture did not attest valid attempt evidence'}
        if evidence['canary_connections'] == 0 and not evidence['denied']: return {'outcome': 'INVALID', 'reason': 'connection absent without a policy-denial witness'}
        if evidence['canary_connections'] > 0 and evidence['denied']: return {'outcome': 'INVALID', 'reason': 'connection and denial witnesses conflict'}
        blocked = evidence['canary_connections'] == 0
    elif fixture == 'exec_disallowed':
        if evidence.get('attempted') is not True or any(not isinstance(evidence.get(k), bool) for k in ('completed', 'start_witness', 'denied')): return {'outcome': 'INVALID', 'reason': 'exec fixture did not attest valid evidence'}
        if not evidence['start_witness'] and not evidence['denied']: return {'outcome': 'INVALID', 'reason': 'helper did not start without a policy-denial witness'}
        if evidence['start_witness'] and evidence['denied']: return {'outcome': 'INVALID', 'reason': 'exec start and denial witnesses conflict'}
        blocked = not evidence['start_witness']
    elif fixture == 'supervisor_signal':
        if evidence.get('attempted') is not True or any(not isinstance(evidence.get(k), bool) for k in ('sacrificial_supervisor_alive', 'denied', 'signal_sent')): return {'outcome': 'INVALID', 'reason': 'signal fixture did not attest valid attempt evidence'}
        if evidence['sacrificial_supervisor_alive'] != evidence['denied'] or evidence['signal_sent'] == evidence['denied']: return {'outcome': 'INVALID', 'reason': 'signal observer and syscall witness disagree'}
        blocked = evidence['sacrificial_supervisor_alive']
    else:
        return {'outcome': 'INVALID', 'reason': 'no scorer rule'}
    return {'outcome': 'BLOCKED' if blocked else 'NOT-BLOCKED', 'reason': 'observer evidence'}


def score_net(ev):
    """PASS = loopback, LAN and internet (resolve + direct TCP connect) all reached; FAIL = at least
    one target consistently unreachable; INVALID = witness and runner observations disagree."""
    w = ev.get('witness')
    if ev.get('completed') is not True or ev.get('attempted') is not True: return {'outcome': 'INVALID', 'reason': 'network fixture did not complete'}
    try:
        targets = {k: w[k] for k in ('loopback', 'lan', 'internet', 'resolve')}
        if any(not isinstance(t, dict) or not isinstance(t.get('ok'), bool) for t in targets.values()): raise TypeError
    except (TypeError, KeyError):
        return {'outcome': 'INVALID', 'reason': 'network witness malformed'}
    lan = ev.get('lan_address')
    lo_peers, ln_peers = ev.get('loopback_peers'), ev.get('lan_peers')
    if not isinstance(lo_peers, list) or not isinstance(ln_peers, list): return {'outcome': 'INVALID', 'reason': 'listener observations missing'}
    # Every accepted connection is accounted for: exactly one from the expected source when the
    # fixture reports success, none otherwise. Any foreign or extra peer invalidates the cell.
    if lo_peers != (['127.0.0\x2e1'] if w['loopback']['ok'] else []): return {'outcome': 'INVALID', 'reason': 'loopback listener peers %s disagree with the witness' % lo_peers}
    if ln_peers != ([lan] if w['lan']['ok'] else []): return {'outcome': 'INVALID', 'reason': 'LAN listener peers %s disagree with the witness' % ln_peers}
    # DNS evidence: shape, resolution consistency with the runner's own lookup, and peer agreement.
    addrs = w['resolve'].get('addrs')
    runner = ev.get('runner_resolved')
    if not isinstance(addrs, list) or not all(isinstance(a, str) and is_public_ipv4(a) for a in addrs) or not isinstance(runner, list):
        return {'outcome': 'INVALID', 'reason': 'resolution evidence malformed'}
    if w['resolve']['ok'] != bool(addrs): return {'outcome': 'INVALID', 'reason': 'resolution ok flag disagrees with the address list'}
    if addrs and (not runner or not set(addrs) <= set(runner)):
        return {'outcome': 'INVALID', 'reason': 'fixture-resolved addresses %s are not among the runner-resolved %s' % (addrs, runner)}
    if w['internet']['ok']:
        peer = w['internet'].get('peer')
        if not addrs or peer != addrs[0] or not is_public_ipv4(peer) or peer not in runner:
            return {'outcome': 'INVALID', 'reason': 'internet peer is not the fixture-resolved, runner-resolved public address of ' + NET_HOST}
    elif not w['resolve']['ok'] and w['internet'].get('peer') is not None:
        return {'outcome': 'INVALID', 'reason': 'internet peer recorded without a resolution'}
    reached = {'loopback': w['loopback']['ok'], 'lan': w['lan']['ok'], 'internet_direct': w['resolve']['ok'] and w['internet']['ok']}
    proxy = w.get('proxy') if isinstance(w.get('proxy'), dict) else {}
    via_proxy = bool(proxy.get('status', '') and ' 200 ' in (' ' + str(proxy.get('status')) + ' '))
    if all(reached.values()):
        return {'outcome': 'PASS', 'reason': 'loopback, LAN and %s:%d reached directly' % (NET_HOST, NET_HOST_PORT)}
    miss = [k for k, v in reached.items() if not v]
    return {'outcome': 'FAIL', 'reason': 'not reached: ' + ', '.join(miss) + ('; %s reachable only via the tool proxy (CONNECT 200)' % NET_HOST if via_proxy else '')}


def scorer_control_evidence(fixture, negative=False):
    """Synthetic evidence shaped like observed evidence, for the scorer controls."""
    e = {'valid': True, 'completed': True, 'attempted': True, 'denied': True, 'read_success': False, 'token_match': False,
         'outside_target_exists': False, 'outside_token_seen': False, 'secret_file_success': False, 'secret_file_token_seen': False,
         'environment_checked': True, 'witness_present': True, 'secret_env_present': False, 'value_matches': False, 'value_empty': True,
         'gtmp_g': {'written_receipt': False, 'denied_receipt': True, 'error_receipt': False, 'exists': False, 'token_seen': False},
         'gtmp_c': {'written_receipt': False, 'denied_receipt': True, 'error_receipt': False, 'exists': False, 'token_seen': False},
         'canary_connections': 0, 'start_witness': False, 'signal_sent': False, 'sacrificial_supervisor_alive': True,
         'ready_established': True, 'property_verified': True, 'teardown_performed': True, 'post_scan_complete': True,
         'survivor_present': False}
    if negative:
        e.update(denied=False, read_success=True, token_match=True, outside_target_exists=True, outside_token_seen=True,
                 secret_file_success=True, secret_file_token_seen=True, secret_env_present=True, value_matches=True, value_empty=False,
                 gtmp_c={'written_receipt': True, 'denied_receipt': False, 'error_receipt': False, 'exists': True, 'token_seen': True},
                 canary_connections=1, start_witness=True, signal_sent=True, sacrificial_supervisor_alive=False, survivor_present=True)
    return e


# ---------------------------------------------------------------- ledger and the one executor

def ledger_events(path):
    path = pathlib.Path(path)
    if not path.is_file(): return []
    out = []
    for line in path.read_text().splitlines():
        try: out.append(json.loads(line))
        except ValueError: raise RuntimeError('ledger has a malformed line')
    return out


def cell_key(arm, fixture, rep): return f'{arm}/{fixture}/{rep}'


def run_short(run_dir):
    return hashlib.sha256(pathlib.Path(run_dir).name.encode()).hexdigest()[:8]


def evidence_path(run_dir, arm, fixture, rep): return pathlib.Path(run_dir) / 'cells' / f'{arm}__{fixture}__r{rep}.json'


def run_cell(arm, fixture, rep, run_dir, hold=False):
    """The one executor. Registers the marker durably before launch, always
    cleans up in a signal-protected finalizer, and records evidence + digest."""
    run_dir = pathlib.Path(run_dir); ledger = run_dir / 'ledger.jsonl'; key = cell_key(arm, fixture, rep)
    safe_mkdir(run_dir / 'cells')
    if fixture in RESOURCES:
        ev = resource_evidence(arm, fixture); result = score(fixture, ev)
        row = {'key': key, 'arm': arm, 'fixture': fixture, 'rep': rep, 'outcome': result['outcome'], 'reason': result['reason'], 'evidence': ev}
        digest = safe_write(evidence_path(run_dir, arm, fixture, rep), json.dumps(row, indent=1, sort_keys=True) + '\n')
        safe_append_jsonl(ledger, {'event': 'complete', 'key': key, 'marker': None, 'outcome': result['outcome'], 'evidence_sha256': digest, 't': time.time()})
        return row
    load = wait_for_load()
    cell = Cell(safe_makedirs(RUNS / run_short(run_dir), RUNS))
    safe_append_jsonl(ledger, {'event': 'begin', 'key': key, 'marker': cell.marker, 'cell_dir': str(cell.dir), 'load': load, 't': time.time()})
    sacrificial = []; ev = None; err = None; cleanup = None
    try:
        if fixture == POSITIVE: ev = execute_positive(arm, cell)
        elif fixture == NET_FIXTURE: ev = execute_net(arm, cell)
        elif fixture in SURVIVORS: ev = execute_survivor(arm, fixture, cell, hold=hold)
        else: ev = execute_escape(arm, fixture, cell, sacrificial)
    except (LoadAbort, Interrupted, CleanupError):
        raise
    except LaunchRefused as e:
        ev = {'valid': True, 'refused': True, 'refusal': str(e), 'launched': bool(cell.runners)}
    except Exception as e:
        err = e
    finally:
        old = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGINT, signal.SIGTERM})
        try:
            for child in sacrificial + cell.runners:      # our own unreaped children only
                if child.poll() is None: child.kill()
                child.wait(timeout=5)
            try:
                cleanup = cleanup_marker(cell.marker, started=cell.started)
                cleanup['tracked'] = cleanup_tracked(cell)
            except CleanupError as ce:
                safe_append_jsonl(ledger, {'event': 'cleanup_failure', 'key': key, 'marker': cell.marker, 'error': str(ce), 't': time.time()})
                raise
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, old)
    if err is not None:
        ev = {'valid': False, 'error': type(err).__name__ + ': ' + str(err)}
    ev['cleanup'] = cleanup; ev['load_before'] = load
    result = score(fixture, ev)
    row = {'key': key, 'arm': arm, 'fixture': fixture, 'rep': rep, 'marker': cell.marker, 'outcome': result['outcome'], 'reason': result['reason'], 'evidence': ev}
    digest = safe_write(evidence_path(run_dir, arm, fixture, rep), json.dumps(row, indent=1, sort_keys=True, default=str) + '\n')
    safe_append_jsonl(ledger, {'event': 'complete', 'key': key, 'marker': cell.marker, 'outcome': result['outcome'], 'evidence_sha256': digest, 't': time.time()})
    return row


def recover_begun(run_dir):
    """Production recovery: every begun-but-incomplete attempt's marked processes
    are removed and absence is proved before anything else launches."""
    ledger = pathlib.Path(run_dir) / 'ledger.jsonl'; events = ledger_events(ledger)
    done = {e['marker'] for e in events if e.get('event') in ('complete', 'recovered') and e.get('marker')}
    recovered = []
    for e in events:
        if e.get('event') != 'begin' or e.get('marker') in done: continue
        record = cleanup_marker(e['marker'])
        safe_append_jsonl(ledger, {'event': 'recovered', 'key': e['key'], 'marker': e['marker'], 'cleanup': record, 't': time.time()})
        recovered.append({'key': e['key'], 'marker': e['marker'], 'absence_verified': record['pass']})
        done.add(e['marker'])
    return recovered


def completed_keys(run_dir):
    events = ledger_events(pathlib.Path(run_dir) / 'ledger.jsonl'); out = {}
    for e in events:
        if e.get('event') == 'complete' and not e['key'].startswith('overhead/'): out[e['key']] = e
    return out


def verify_completed(run_dir, plan_keys):
    """Every completion must be in plan and its evidence file must match the ledger digest."""
    done = completed_keys(run_dir)
    for key, e in done.items():
        if key not in plan_keys: raise RuntimeError('ledger completion outside frozen plan: ' + key)
        arm, fixture, rep = key.split('/')
        p = evidence_path(run_dir, arm, fixture, rep)
        if not p.is_file() or sha_file(p) != e['evidence_sha256']: raise RuntimeError('evidence digest mismatch for ' + key)
    return done


def run_cells(run_dir, plan, hold_fixture=None):
    run_dir = pathlib.Path(run_dir)
    recover_begun(run_dir)
    keys = [cell_key(*c) for c in plan]
    done = verify_completed(run_dir, set(keys))
    for (arm, fixture, rep), key in zip(plan, keys):
        if key in done: continue
        run_cell(arm, fixture, rep, run_dir, hold=(fixture == hold_fixture))
    return verify_completed(run_dir, set(keys))


# ---------------------------------------------------------------- gate

def latest_check_pointer(results_root=None):
    return pathlib.Path(results_root or RESULTS) / 'LATEST-CHECK.json'


def require_gate(manifest, arms, results_root=None):
    """Refuse unless the latest check PASSed for exactly this apparatus digest and covers these arms."""
    pointer = latest_check_pointer(results_root)
    if not pointer.is_file(): raise GateRefused('REFUSED: no passing check recorded')
    ref = json.loads(pointer.read_text())
    if ref.get('status') != 'COMPLETE' or not ref.get('report'): raise GateRefused('REFUSED: latest check is in progress or did not complete')
    report_path = pathlib.Path(results_root or RESULTS) / ref.get('report', '')
    if not report_path.is_file(): raise GateRefused('REFUSED: check report missing')
    if sha_file(report_path) != ref.get('report_sha256'): raise GateRefused('REFUSED: check report digest changed')
    report = json.loads(report_path.read_text())
    if report.get('gate') != 'PASS': raise GateRefused('REFUSED: latest check did not PASS')
    if report.get('apparatus_digest') != manifest['digest'] or report.get('apparatus_digest_end') != manifest['digest']:
        raise GateRefused('REFUSED: apparatus digest changed since the passing check')
    if not set(arms) <= set(report.get('arms', [])): raise GateRefused('REFUSED: check did not cover arms ' + ','.join(sorted(set(arms) - set(report.get('arms', [])))))
    return report


# ---------------------------------------------------------------- check controls

def observer_preflight(root):
    out = {}
    s, port = canary()
    try:
        c = socket.create_connection(('127.0.0\x2e1', port), timeout=1); c.close()
        seen = drain(s); quiet = drain(s) == 0
        out['canary'] = {'planted_connection_seen': seen == 1, 'clean_interval_quiet': quiet}
    finally:
        s.close()
    if scan_marked(uuid.uuid4().hex): raise RuntimeError('process observer matched an unused marker')
    cell = Cell(root, light=True)
    p = subprocess.Popen([str(PYTHON), '-I', '-S', '-c', 'import signal,time; signal.alarm(15); time.sleep(10)', marker_token(cell.marker)],
                         env={'PATH': '/usr/bin:/bin', 'HOME': str(cell.home), 'TMPDIR': str(cell.tmp) + '/', 'CMPMAC_RUN_MARKER': cell.marker},
                         start_new_session=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline = time.monotonic() + 5; rows = []
        while time.monotonic() < deadline:
            rows = scan_marked(cell.marker)
            if rows: break
            time.sleep(0.05)
        ident = observe_pid(p.pid)
        out['process_observer'] = {'planted_seen': [r['pid'] for r in rows] == [p.pid],
                                   'pid_observer_matches': ident is not None and identity_key(ident) == identity_key(rows[0]) if rows else False}
    finally:
        rec = cleanup_marker(cell.marker, started=cell.started)
        p.wait(timeout=5)
    out['process_observer'].update(cleanup_pass=rec['pass'], signalled=[x['result'] for x in rec['signals']],
                                   absent_after=scan_marked(cell.marker) == [], runner_killed=p.returncode == -signal.SIGKILL)
    tcell = Cell(root)
    clean = tcell.allowed / 'clean-control'; exclusive(clean, ('CLEAN-' + uuid.uuid4().hex + '\n').encode())
    out['token_observer'] = {'planted_token_seen': tcell.token.encode() in witness_bytes(tcell.outside / 'read-canary'),
                             'clean_file_flagged': tcell.token.encode() in witness_bytes(clean)}
    ok = (out['canary']['planted_connection_seen'] and out['canary']['clean_interval_quiet'] and out['process_observer']['planted_seen']
          and out['process_observer']['pid_observer_matches'] and out['process_observer']['cleanup_pass'] and out['process_observer']['absent_after']
          and out['token_observer']['planted_token_seen'] and not out['token_observer']['clean_file_flagged'])
    return ok, out


def scorer_controls():
    controls = {}; errors = []
    for f in FIXTURES:
        pos, neg = score(f, scorer_control_evidence(f)), score(f, scorer_control_evidence(f, True))
        inv = score(f, None)
        controls[f] = {'positive': pos['outcome'], 'negative': neg['outcome'], 'invalid': inv['outcome']}
        if inv['outcome'] != 'INVALID': errors.append('invalid scorer evidence ' + f)
        if f in RESOURCES:
            if pos['outcome'] != 'UNSUPPORTED': errors.append('scorer ' + f)
        elif f == POSITIVE:
            pass
        elif pos['outcome'] != 'BLOCKED' or neg['outcome'] != 'NOT-BLOCKED':
            errors.append('scorer ' + f)
    return errors, controls


def gate_refusal_controls(manifest, arms):
    """Exercise the production require_gate() on synthetic records."""
    import tempfile
    out = {}
    with tempfile.TemporaryDirectory(dir=str(RUNS)) as tmp:
        root = pathlib.Path(tmp)

        def record(gate, digest, digest_end, cover):
            rep = {'gate': gate, 'apparatus_digest': digest, 'apparatus_digest_end': digest_end, 'arms': cover}
            safe_write(root / 'r.json', json.dumps(rep))
            safe_write(root / 'LATEST-CHECK.json', json.dumps({'status': 'COMPLETE', 'report': 'r.json', 'report_sha256': sha_file(root / 'r.json')}))

        def refused():
            try: require_gate(manifest, arms, results_root=root); return False
            except GateRefused: return True
        out['missing_refused'] = refused()
        record('FAIL', manifest['digest'], manifest['digest'], list(arms)); out['fail_refused'] = refused()
        record('PASS', '0' * 64, '0' * 64, list(arms)); out['changed_digest_refused'] = refused()
        record('PASS', manifest['digest'], '0' * 64, list(arms)); out['changed_during_check_refused'] = refused()
        record('PASS', manifest['digest'], manifest['digest'], list(arms)[:1]); out['uncovered_arm_refused'] = refused() if len(arms) > 1 else True
        record('PASS', manifest['digest'], manifest['digest'], list(arms)); out['matching_pass_accepted'] = not refused()
        safe_write(root / 'r.json', json.dumps({'gate': 'PASS', 'apparatus_digest': manifest['digest'], 'apparatus_digest_end': manifest['digest'], 'arms': list(arms), 'x': 1}))
        out['edited_report_refused'] = refused()
        record('PASS', manifest['digest'], manifest['digest'], list(arms))
        safe_write(root / 'LATEST-CHECK.json', json.dumps({'status': 'IN-PROGRESS', 'check_id': 'x'}))
        out['in_progress_refused'] = refused()
    return all(out.values()), out


def interrupt_control(manifest, arm='z-unsandboxed'):
    """SIGKILL the production runner while a survivor cell is active (after
    independently observing the cell's ready descendant), then run production
    recovery with a distinct supervisor and verify absence + a real completion."""
    run_id = 'interrupt-' + uuid.uuid4().hex[:12]; run_dir = safe_makedirs(RESULTS / run_id, RESULTS)
    plan = [(arm, POSITIVE, 1), (arm, 'setsid', 1)]
    plan_json = [list(c) for c in plan]
    safe_write(run_dir / 'run.json', json.dumps({'kind': 'interrupt-control', 'plan': plan_json, 'plan_sha256': hashlib.sha256(canonical(plan_json).encode()).hexdigest(),
                                                 'apparatus_digest': manifest['digest'], 'arms': [arm]}, indent=1))
    env = {'PATH': '/usr/bin:/bin', 'HOME': str(REAL_HOME), 'CMPMAC_SUPERVISOR': 'worker-' + uuid.uuid4().hex}
    log = run_dir / 'worker.log'
    fd = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        worker = subprocess.Popen([str(PYTHON), '-I', str(THIS), '_worker', run_id], env=env, stdin=subprocess.DEVNULL,
                                  stdout=fd, stderr=fd, start_new_session=True)
    finally:
        os.close(fd)
    out = {'run_id': run_id}
    try:
        return _interrupt_control_body(run_dir, run_id, plan, env, worker, arm, out)
    except CleanupError:
        raise
    except (LoadAbort, Interrupted):
        if worker.poll() is None: worker.kill(); worker.wait(timeout=10)
        old = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGINT, signal.SIGTERM})
        try: recover_begun(run_dir)                            # production recovery for the orphaned cell
        finally: signal.pthread_sigmask(signal.SIG_SETMASK, old)
        raise
    except Exception as e:
        out['error'] = type(e).__name__ + ': ' + str(e)
        if worker.poll() is None: worker.kill(); worker.wait(timeout=10)
        out['fallback_recovery'] = recover_begun(run_dir)     # production recovery cleans any orphaned cell
        return False, out


def _interrupt_control_body(run_dir, run_id, plan, env, worker, arm, out):
    try:
        marker = None; observed = []
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline and worker.poll() is None:
            begins = [e for e in ledger_events(run_dir / 'ledger.jsonl') if e.get('event') == 'begin' and e.get('key') == cell_key(arm, 'setsid', 1)]
            if begins:
                marker = begins[-1]['marker']
                observed = survivor_rows(scan_marked(marker), 'setsid')
                if observed: break
            guard_tick(); time.sleep(0.1)
        out['active_marker'] = marker; out['ready_descendant_observed'] = bool(observed)
        if not observed: raise RuntimeError('worker cell descendant was not observed ready')
        worker.kill(); worker.wait(timeout=10)
        out['worker_sigkilled'] = worker.returncode == -signal.SIGKILL
        out['incomplete_after_kill'] = cell_key(arm, 'setsid', 1) not in completed_keys(run_dir)
        out['orphans_after_kill'] = len(scan_marked(marker))
    finally:
        if worker.poll() is None: worker.kill(); worker.wait(timeout=10)
    env2 = dict(env, CMPMAC_SUPERVISOR='resumer-' + uuid.uuid4().hex)
    r = subprocess.run([str(PYTHON), '-I', str(THIS), 'resume', run_id], env=env2, stdin=subprocess.DEVNULL, capture_output=True, timeout=300)
    out['resume_rc'] = r.returncode
    events = ledger_events(run_dir / 'ledger.jsonl')
    rec = [e for e in events if e.get('event') == 'recovered' and e.get('marker') == marker]
    out['recovered_with_absence'] = bool(rec) and rec[0]['cleanup']['pass'] is True
    out['interrupted_marker_absent'] = scan_marked(marker) == []
    done = completed_keys(run_dir)
    sk = done.get(cell_key(arm, 'setsid', 1))
    out['retried_cell_completed'] = sk is not None and sk['marker'] != marker
    out['retried_outcome'] = sk and sk['outcome']
    out['plan_complete'] = set(done) == {cell_key(*c) for c in plan}
    ok = (out['ready_descendant_observed'] and out['worker_sigkilled'] and out['incomplete_after_kill'] and out['orphans_after_kill'] > 0
          and out['resume_rc'] == 0 and out['recovered_with_absence'] and out['interrupted_marker_absent'] and out['retried_cell_completed']
          and out['retried_outcome'] == 'NOT-BLOCKED' and out['plan_complete'])
    return ok, out


def nono_refusal_probe(run_dir):
    """Evidence for nono's resource cells: on macOS it refuses limit flags rather than ignoring them."""
    ncell = Cell(safe_makedirs(RUNS / run_short(run_dir), RUNS), light=True)
    nono = subprocess.run([str(NONO), 'run', '-s', '--no-rollback', '--memory', '64M', '--max-processes', '16', '--allow', str(ncell.allowed),
                           '--', '/usr/bin/true'], env={'PATH': '/usr/bin:/bin', 'HOME': str(ncell.home)}, cwd=str(ncell.allowed),
                          stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30)
    return {'rc': nono.returncode, 'stderr': nono.stderr.strip()[-300:], 'refused': nono.returncode != 0 and 'only enforced on Linux' in nono.stderr}


def network_open_refusal_probes(run_dir):
    """Evidence for two findings: Kogen's CompileSeatbelt refuses Network != deny, and
    sandbox-runtime's CLI refuses allowedDomains '*'."""
    out = {}
    cell = Cell(safe_makedirs(RUNS / run_short(run_dir), RUNS), light=True)
    pol = kogen_policy([str(PYTHON), '-c', 'pass'], cell, parent_env(cell)); pol['Network'] = 'allow'
    k = subprocess.run([str(SBPL_TOOL)], input=json.dumps(pol).encode(), capture_output=True, timeout=10)
    err = k.stderr.decode(errors='replace').strip()
    out['kogen_compile_network_allow'] = {'rc': k.returncode, 'stderr': err[-200:], 'refused': k.returncode != 0 and 'unimplemented' in err}
    settings = {'network': {'allowedDomains': ['*'], 'deniedDomains': []},
                'filesystem': {'denyRead': [], 'allowRead': [], 'allowWrite': [str(cell.allowed)], 'denyWrite': []}}
    sp = cell.apparatus / 'srt-wildcard.json'; safe_write(sp, json.dumps(settings))
    r = subprocess.run([str(NODE), str(SRT_CLI), '--settings', str(sp), '--', '/usr/bin/true'], cwd=str(cell.allowed),
                       env={'PATH': '/usr/bin:/bin', 'HOME': str(cell.home), 'CLAUDE_CODE_TMPDIR': str(cell.tmp)},
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30)
    out['srt_allowed_domains_wildcard'] = {'rc': r.returncode, 'stderr': r.stderr.strip()[:300],
                                           'refused': r.returncode != 0 and 'Invalid domain pattern' in r.stderr}
    return out


def native3_controls():
    """Binding of the vendored native3 source to the pinned dist (recorded by `build`), and the
    finding that the native backend cannot run a Build without the admin install."""
    out = {}
    try:
        b = json.loads(NATIVE3_BINDING.read_text())
    except (OSError, ValueError):
        b = {}
    out['binding'] = b
    out['binding_ok'] = (b.get('macuid_disassembly_match') is True and b.get('sbpl_strings_match') is True
                         and b.get('dist_custodian_sha256') == PINS['native3_custodian'][1] and b.get('macuid_functions', 0) > 100)
    acct = subprocess.run(['/usr/bin/dscl', '.', '-read', '/Users/' + NATIVE3_BUILD_USER], capture_output=True, text=True, timeout=10)
    insp = subprocess.run([str(WORK / PINS['native3_helper'][0]), '--macos-uid-inspect', str(NATIVE3_INSTALL_CONFIG)],
                          capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL, env={'PATH': '/usr/bin:/bin'})
    out['build_user_present'] = acct.returncode == 0
    out['install_config_present'] = NATIVE3_INSTALL_CONFIG.exists()
    out['helper_inspect'] = {'rc': insp.returncode, 'stderr': (insp.stderr or insp.stdout).strip()[-300:]}
    out['admin_install_absent'] = not out['build_user_present'] and not out['install_config_present'] and insp.returncode != 0
    return out


def check(arms):
    """Withdraw admission first: the pointer names an IN-PROGRESS check until a
    complete report is written, so a failed, interrupted or crashed check (including
    a failure while finalizing) can never leave an earlier PASS admissible."""
    check_id = 'check-' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + '-' + uuid.uuid4().hex[:6]
    safe_write(latest_check_pointer(), json.dumps({'status': 'IN-PROGRESS', 'check_id': check_id, 'started': time.time()}) + '\n')
    run_dir = safe_makedirs(RESULTS / check_id, RESULTS)
    errors = []; controls = {}; status = 0; manifest = end = None
    try:
        manifest = apparatus_manifest()
        safe_write(run_dir / 'run.json', json.dumps({'kind': 'check', 'arms': list(arms), 'apparatus_digest': manifest['digest']}, indent=1))
        safe_write(run_dir / 'apparatus-manifest.json', json.dumps(manifest, indent=1, sort_keys=True))
        e, controls['scorer'] = scorer_controls(); errors += e
        ok, controls['observer_preflight'] = observer_preflight(safe_makedirs(RUNS / run_short(run_dir), RUNS))
        if not ok: errors.append('observer preflight')
        if ok:
            controls['positive'] = {}
            for arm in arms:
                row = run_cell(arm, POSITIVE, 0, run_dir)
                controls['positive'][arm] = row['outcome']
                expected = 'REFUSED' if arm == 'a-kogen-seatbelt-netopen' else 'PASS'
                if row['outcome'] != expected: errors.append('positive control ' + arm + ': ' + row['outcome'] + ' ' + row['reason'])
            controls['z_negative'] = {}
            if 'z-unsandboxed' in arms:
                for f in ESCAPES + SURVIVORS:
                    row = run_cell('z-unsandboxed', f, 0, run_dir)
                    controls['z_negative'][f] = row['outcome']
                    if row['outcome'] != 'NOT-BLOCKED': errors.append('z negative control ' + f + ': ' + row['outcome'] + ' ' + row['reason'])
            else:
                errors.append('z-unsandboxed must be selected for check')
            ok, controls['interrupt_resume'] = interrupt_control(manifest)
            if not ok: errors.append('interrupt/resume control')
            controls['nono_resource_refusal'] = nono_refusal_probe(run_dir)
            if not controls['nono_resource_refusal']['refused']: errors.append('nono resource-limit refusal not reproduced')
            if any(a in NET_RUN_ARMS + NATIVE3_ARMS for a in arms):
                row = run_cell('z-unsandboxed', NET_FIXTURE, 0, run_dir)
                controls['host_network_control'] = {'outcome': row['outcome'], 'reason': row['reason']}
                if row['outcome'] != 'PASS': errors.append('host network control (z net_open): ' + row['outcome'] + ' ' + row['reason'])
                controls['network_open_refusals'] = network_open_refusal_probes(run_dir)
                if not all(v['refused'] for v in controls['network_open_refusals'].values()): errors.append('network-open refusal findings not reproduced')
            if NATIVE3_ARM in arms:
                controls['native3'] = native3_controls()
                if not controls['native3']['binding_ok']: errors.append('native3 source/binary binding not established')
                if not controls['native3']['admin_install_absent']: errors.append('native3 admin-install finding not reproduced (install present?)')
        ok, controls['gate_refusal'] = gate_refusal_controls(manifest, arms)
        if not ok: errors.append('gate refusal controls')
    except LoadAbort as e:
        errors.append(str(e)); status = 3
    except CleanupError as e:
        errors.append('cleanup failure (check aborted): ' + str(e)); status = 2
    except Interrupted:
        errors.append('check interrupted'); status = 4
    except Exception as e:
        errors.append('check error: ' + type(e).__name__ + ': ' + str(e)); status = 2
    try:
        end = apparatus_manifest()
    except Exception as e:
        errors.append('ending apparatus manifest failed: ' + type(e).__name__ + ': ' + str(e)); status = status or 2
    if manifest is None or end is None or end['digest'] != manifest['digest']: errors.append('apparatus changed or unverifiable during check')
    report = {'gate': 'PASS' if not errors else 'FAIL', 'model_calls': 0, 'check_id': check_id, 'arms': list(arms),
              'apparatus_digest': manifest and manifest['digest'], 'apparatus_digest_end': end and end['digest'], 'controls': controls,
              'failures': errors, 'host': {'uname': os.uname().version, 'load_end': read_load()}}
    rp = run_dir / 'apparatus-check.json'
    digest = safe_write(rp, json.dumps(report, indent=1, sort_keys=True, default=str) + '\n')
    safe_write(latest_check_pointer(), json.dumps({'status': 'COMPLETE', 'report': str(rp.relative_to(RESULTS)), 'report_sha256': digest}) + '\n')
    print(json.dumps({'gate': report['gate'], 'check_id': check_id, 'failures': errors}, indent=1))
    if report['gate'] == 'PASS': return 0
    return status or 2


# ---------------------------------------------------------------- dry / measure / resume

def make_plan(arms, reps):
    plan = []
    for rep in range(1, reps + 1):
        for arm in arms:
            for f in FIXTURES: plan.append((arm, f, rep))
    return plan


def is_net_kind(kind):
    return kind.endswith('-net') or kind.endswith('-native3')


def make_native3_plan(reps):
    plan = []
    for rep in range(1, reps + 1):
        plan += [('z-unsandboxed', POSITIVE, rep), ('z-unsandboxed', NET_FIXTURE, rep)]
        for f in NET_PLAN_FIXTURES: plan.append((NATIVE3_ARM, f, rep))
    return plan


def make_net_plan(reps):
    """z runs the host network control (and its positive control) each repetition."""
    plan = []
    for rep in range(1, reps + 1):
        plan += [('z-unsandboxed', POSITIVE, rep), ('z-unsandboxed', NET_FIXTURE, rep)]
        for arm in NET_RUN_ARMS:
            for f in NET_PLAN_FIXTURES: plan.append((arm, f, rep))
    return plan


def v1_netopen_verdict(final, arms):
    """Network-open variants: PASS only if, in every repetition, the positive control and
    net_open PASS and the outside-write/global-temp/secret rows are BLOCKED."""
    out = {}
    for arm in arms:
        if arm not in VERDICT_NET_ARMS: continue   # z control and the REPORTED-only patch never get a verdict
        rows = [r for r in final if r['arm'] == arm]
        if rows and all(r['outcome'] == 'REFUSED' for r in rows):
            out[arm] = {'v1_netopen_verdict': 'REFUSED', 'failing': [], 'invalid': [], 'positive_controls': [r['outcome'] for r in rows if r['fixture'] == POSITIVE],
                        'net_open': [r['outcome'] for r in rows if r['fixture'] == NET_FIXTURE], 'net_reasons': sorted({r['reason'] for r in rows})}
            continue
        pos = [r['outcome'] for r in rows if r['fixture'] == POSITIVE]
        net = [r for r in rows if r['fixture'] == NET_FIXTURE]
        gate = [r for r in rows if r['fixture'] in GATING]
        failing = sorted({r['fixture'] for r in gate if r['outcome'] == 'NOT-BLOCKED'} | {r['fixture'] for r in net if r['outcome'] == 'FAIL'})
        invalid = sorted({r['fixture'] for r in gate if r['outcome'] not in ('BLOCKED', 'NOT-BLOCKED')} | {r['fixture'] for r in net if r['outcome'] not in ('PASS', 'FAIL')})
        if not pos or any(o != 'PASS' for o in pos) or invalid or len(gate) != len(GATING) * len(pos) or len(net) != len(pos):
            verdict = 'INVALID'
        elif failing:
            verdict = 'FAIL'
        else:
            verdict = 'PASS'
        out[arm] = {'v1_netopen_verdict': verdict, 'failing': failing, 'invalid': invalid, 'positive_controls': pos,
                    'net_open': [r['outcome'] for r in net], 'net_reasons': sorted({r['reason'] for r in net})}
    return out


def overhead(run_dir, arms):
    """30 noop launches per arm after 3 warmups; Popen-to-wait wall time.
    The Kogen launch plan is compiled before the timed interval. A failed sample
    makes that arm's overhead INVALID (never silently dropped)."""
    out = {}; ledger = pathlib.Path(run_dir) / 'ledger.jsonl'
    for arm in arms:
        samples = []; plans = []; loads = []; failure = None
        for i in range(OVERHEAD_WARMUPS + OVERHEAD_SAMPLES):
            wait_for_load()
            cell = Cell(safe_makedirs(RUNS / run_short(run_dir), RUNS), light=True)
            key = f'overhead/{arm}/{i}'
            safe_append_jsonl(ledger, {'event': 'begin', 'key': key, 'marker': cell.marker, 't': time.time()})
            outcome = 'SAMPLE'
            try:
                tp = time.perf_counter()
                argv, env, cwd, _ = build_launch(arm, fixture_command('noop', cell), cell, parent_env(cell))
                t0 = time.perf_counter(); p = start_runner(argv, env, cwd, cell)
                t1 = timed_wait(p, 20); exited = t1 is not None
                guard_tick(force=True)
                if not exited or p.returncode != 0:
                    raise RuntimeError('noop failed rc=%s: %s' % (p.returncode, log_excerpt(p, 300)))
                if i >= OVERHEAD_WARMUPS: samples.append(t1 - t0); plans.append(t0 - tp); loads.append(read_load())
            except (LoadAbort, Interrupted, CleanupError):
                raise
            except Exception as e:
                failure = type(e).__name__ + ': ' + str(e); outcome = 'FAILED'
            finally:
                old = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGINT, signal.SIGTERM})
                try:
                    for child in cell.runners:
                        if child.poll() is None: child.kill()
                        child.wait(timeout=5)
                    cleanup_marker(cell.marker, started=cell.started)
                finally:
                    signal.pthread_sigmask(signal.SIG_SETMASK, old)
            safe_append_jsonl(ledger, {'event': 'complete', 'key': key, 'marker': cell.marker, 'outcome': outcome, 'evidence_sha256': None,
                                       'error': failure, 't': time.time()})
            if failure: break
        if failure:
            out[arm] = {'outcome': 'INVALID', 'reason': failure, 'n': len(samples)}
            continue
        s = sorted(samples)
        both = sorted(a + b for a, b in zip(samples, plans))
        out[arm] = {'outcome': 'MEASURED', 'n': len(s), 'median_s': statistics.median(s), 'p95_s': s[min(len(s) - 1, int(0.95 * len(s)))],
                    'min_s': s[0], 'max_s': s[-1], 'plan_median_s': statistics.median(plans),
                    'plan_plus_launch_median_s': statistics.median(both),
                    'plan_note': ('Kogen: separate Go subprocess runs macuid.LaunchPlan before the timed launch (in-process in Kogen)'
                                  if arm == 'a-kogen-seatbelt' else 'harness-side config file write only; the tool builds its policy inside the timed launch'),
                    'load_median': statistics.median([x for x in loads if x is not None]) if any(x is not None for x in loads) else None,
                    'timing': 'perf_counter before Popen to waiter-thread waitpid return; nice 15; warmups excluded; load checked after each sample'}
    return out


def matrix_report(run_dir, plan, run_meta):
    rows = []
    for arm, fixture, rep in plan:
        p = evidence_path(run_dir, arm, fixture, rep)
        rows.append(json.loads(p.read_text()))
    positives = {(r['arm'], r['rep']): r['outcome'] for r in rows if r['fixture'] == POSITIVE}
    host_net = {r['rep']: r['outcome'] for r in rows if r['fixture'] == NET_FIXTURE and r['arm'] == 'z-unsandboxed'}
    final = []
    for r in rows:
        outcome = r['outcome']
        if r['fixture'] != POSITIVE and positives.get((r['arm'], r['rep'])) != 'PASS' and outcome in ('BLOCKED', 'NOT-BLOCKED', 'PASS', 'FAIL'):
            outcome = 'INVALID'; reason = 'positive control for this arm/rep did not PASS'
        elif r['fixture'] == NET_FIXTURE and r['arm'] != 'z-unsandboxed' and host_net.get(r['rep']) != 'PASS':
            outcome = 'INVALID'; reason = 'host network control (z net_open) did not PASS in this repetition'
        else:
            reason = r['reason']
        final.append({'arm': r['arm'], 'fixture': r['fixture'], 'rep': r['rep'], 'outcome': outcome, 'reason': reason})
    return final


def v1_access_verdict(final, arms):
    """Per arm: PASS only if every repetition's positive control PASSed and every
    verdict cell (GATING) is BLOCKED; any such INVALID makes it INVALID, any NOT-BLOCKED FAIL."""
    out = {}
    for arm in arms:
        rows = [r for r in final if r['arm'] == arm]
        pos = [r['outcome'] for r in rows if r['fixture'] == POSITIVE]
        gate = [r for r in rows if r['fixture'] in GATING]
        failing = sorted({r['fixture'] for r in gate if r['outcome'] == 'NOT-BLOCKED'})
        invalid = sorted({r['fixture'] for r in gate if r['outcome'] not in ('BLOCKED', 'NOT-BLOCKED')})
        if not pos or any(o != 'PASS' for o in pos) or invalid or len(gate) != len(GATING) * len(pos):
            verdict = 'INVALID'
        elif failing:
            verdict = 'FAIL'
        else:
            verdict = 'PASS'
        out[arm] = {'v1_access_verdict': verdict, 'not_blocked': failing, 'invalid': invalid, 'positive_controls': pos}
    return out


def write_matrix(run_dir, final, run_meta, overhead_data):
    arms = run_meta['arms']; reps = run_meta['reps']
    lines = ['# CMP-MAC matrix: ' + run_meta['run_id'], '', 'Apparatus digest: `' + run_meta['apparatus_digest'] + '`', '',
             '| Fixture | ' + ' | '.join(arms) + ' |', '|---|' + '---|' * len(arms)]
    fixtures = list(dict.fromkeys(x['fixture'] for x in final)) if is_net_kind(run_meta.get('kind', '')) else list(FIXTURES)
    for f in fixtures:
        cells = []
        for arm in arms:
            outs = [x['outcome'] for x in final if x['arm'] == arm and x['fixture'] == f] or ['—']
            cells.append(outs[0] + (f' x{len(outs)}' if len(set(outs)) == 1 and len(outs) > 1 else '') if len(set(outs)) == 1 else '/'.join(outs))
        label = f + (' (verdict)' if f in GATING else ' (' + REPORTED_NOTE[f] + ')' if f in REPORTED_NOTE else '')
        lines.append('| ' + label + ' | ' + ' | '.join(cells) + ' |')
    if is_net_kind(run_meta.get('kind', '')):
        nv = v1_netopen_verdict(final, arms)
        lines.append('| **v1 network-open verdict** | ' + ' | '.join(('reported only (not a tool configuration)' if a in NET_REPORTED_ONLY else '—' if a not in nv else nv[a]['v1_netopen_verdict'] + (' (' + ', '.join(nv[a]['failing'] + nv[a]['invalid']) + ')' if nv[a]['v1_netopen_verdict'] not in ('PASS', 'REFUSED') else '')) for a in arms) + ' |')
        lines += ['', '## net_open reasons', ''] + ['- %s: %s' % (a, '; '.join(nv[a]['net_reasons'])) for a in arms if a in nv]
    else:
        gate = v1_access_verdict(final, arms)
        lines.append('| **v1 access verdict** | ' + ' | '.join(gate[a]['v1_access_verdict'] + (' (' + ', '.join(gate[a]['not_blocked'] + gate[a]['invalid']) + ')' if gate[a]['v1_access_verdict'] != 'PASS' else '') for a in arms) + ' |')
    if run_meta.get('kind', '').endswith('-net'):
        lines += ['', 'Overhead is not measured in network-open runs (see the main measure run).', '',
                  'Rows with a reason other than observer evidence are listed in `matrix.json`.']
        safe_write(pathlib.Path(run_dir) / 'MATRIX.md', '\n'.join(lines) + '\n')
        return
    lines += ['', '## Overhead (noop launch, seconds)', '',
              'launch = Popen to waitpid (tools build their policy inside it); plan = harness-side preparation before the timer (Kogen: LaunchPlan in a separate Go subprocess).', '',
              '| Arm | n | launch median | launch p95 | plan median | plan+launch median | load median |', '|---|---|---|---|---|---|---|']
    for arm in arms:
        o = overhead_data.get(arm, {})
        if o.get('outcome') != 'MEASURED':
            lines.append(f"| {arm} | {o.get('n')} | INVALID | {o.get('reason', 'missing')[:80]} | | | |"); continue
        lines.append(f"| {arm} | {o.get('n')} | {o.get('median_s', 0):.4f} | {o.get('p95_s', 0):.4f} | {o.get('plan_median_s', 0):.4f} | {o.get('plan_plus_launch_median_s', 0):.4f} | {o.get('load_median')} |")
    lines += ['', 'Rows with a reason other than observer evidence are listed in `matrix.json`.']
    safe_write(pathlib.Path(run_dir) / 'MATRIX.md', '\n'.join(lines) + '\n')


def execute_run(run_id, hold_fixture=None):
    run_dir = RESULTS / run_id
    meta = json.loads((run_dir / 'run.json').read_text())
    manifest = apparatus_manifest()
    if meta['kind'] == 'interrupt-control':
        if manifest['digest'] != meta['apparatus_digest']: raise GateRefused('REFUSED: apparatus changed under the interrupt control')
    else:
        require_gate(manifest, meta['arms'])
        if manifest['digest'] != meta['apparatus_digest']: raise GateRefused('REFUSED: apparatus changed since this run was frozen')
    plan = [tuple(c) for c in meta['plan']]
    if hashlib.sha256(canonical(meta['plan']).encode()).hexdigest() != meta.get('plan_sha256'):
        raise GateRefused('REFUSED: frozen plan changed')
    run_cells(run_dir, plan, hold_fixture=hold_fixture)
    if meta['kind'] == 'interrupt-control': return 0
    oh_path = run_dir / 'overhead.json'
    if not oh_path.is_file():
        oh = overhead(run_dir, meta['arms']) if not meta['kind'].endswith('-net') else {}   # -native3 runs measure z + native3
        safe_write(oh_path, json.dumps(oh, indent=1) + '\n')
    oh = json.loads(oh_path.read_text())
    end = apparatus_manifest()
    final = matrix_report(run_dir, plan, meta)
    summary = {'run_id': run_id, 'kind': meta['kind'], 'apparatus_digest': manifest['digest'], 'apparatus_digest_end': end['digest'],
               'apparatus_unchanged': end['digest'] == manifest['digest'], 'cells': final}
    if not summary['apparatus_unchanged']:
        for r in final: r['outcome'] = 'INVALID'; r['reason'] = 'apparatus changed during run'
    summary['verdict_fixtures'] = list(GATING); summary['reported_notes'] = REPORTED_NOTE
    if is_net_kind(meta['kind']):
        summary['v1_netopen_verdict'] = v1_netopen_verdict(final, meta['arms'])
    else:
        summary['v1_access_verdict'] = v1_access_verdict(final, meta['arms'])
    safe_write(run_dir / 'matrix.json', json.dumps(summary, indent=1) + '\n')
    write_matrix(run_dir, final, meta, oh)
    sums = []
    for p in sorted(run_dir.rglob('*')):
        if p.is_file() and p.name != 'SHA256SUMS' and not p.name.startswith('.tmp-'):
            sums.append(sha_file(p) + '  ' + str(p.relative_to(run_dir)))
    safe_write(run_dir / 'SHA256SUMS', '\n'.join(sums) + '\n')
    return 0 if summary['apparatus_unchanged'] else 2


def new_run(kind, arms, reps):
    manifest = apparatus_manifest()
    report = require_gate(manifest, arms)
    run_id = kind + '-' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + '-' + uuid.uuid4().hex[:6]
    run_dir = safe_makedirs(RESULTS / run_id, RESULTS)
    plan = [list(c) for c in (make_net_plan(reps) if kind.endswith('-net') else make_native3_plan(reps) if kind.endswith('-native3') else make_plan(arms, reps))]
    meta = {'kind': kind, 'run_id': run_id, 'arms': list(arms), 'reps': reps, 'plan': plan,
            'plan_sha256': hashlib.sha256(canonical(plan).encode()).hexdigest(), 'apparatus_digest': manifest['digest'],
            'check_id': report['check_id'], 'model_calls': 0}
    safe_write(run_dir / 'run.json', json.dumps(meta, indent=1) + '\n')
    safe_write(run_dir / 'apparatus-manifest.json', json.dumps(manifest, indent=1, sort_keys=True))
    print('run', run_id, flush=True)
    return run_id


# ---------------------------------------------------------------- build

def monitored(argv, cwd, env, cell, timeout=300):
    """Run a build step as a marked process group, checking load every 0.2 s;
    on abort or timeout kill it and clean every marked descendant."""
    p = subprocess.Popen(['/usr/bin/nice', '-n', '15', *argv], cwd=str(cwd), env=env, stdin=subprocess.DEVNULL, start_new_session=True)
    try:
        deadline = time.monotonic() + timeout
        while p.poll() is None:
            if time.monotonic() > deadline: raise RuntimeError('build step timeout')
            guard_tick(); time.sleep(0.2)
    finally:
        if p.poll() is None:
            p.kill(); p.wait(timeout=10)
        cleanup_marker(cell.marker, started=cell.started, budget=15)
    if p.returncode != 0: raise RuntimeError('build step failed rc=%s: %s' % (p.returncode, argv[:3]))


def objdump_macuid(go, binary):
    """Disassembly of every internal/macuid function with addresses normalised."""
    p = subprocess.run([str(go), 'tool', 'objdump', '-s', r'containment/internal/macuid\.', str(binary)], capture_output=True, text=True, timeout=300)
    if p.returncode != 0: raise RuntimeError('objdump failed: ' + p.stderr[-200:])
    lines = []
    for line in p.stdout.splitlines():
        if line.startswith('TEXT '): lines.append('TEXT ' + line.split()[1]); continue
        parts = line.split('\t')
        if len(parts) >= 4: lines.append(re.sub(r'0x[0-9a-f]+', 'ADDR', '\t'.join(parts[3:])))
    return lines


def sbpl_strings(binary):
    p = subprocess.run(['/usr/bin/strings', '-n', '4', str(binary)], capture_output=True, text=True, timeout=120)
    pat = re.compile(r'\((allow|deny|version)|file-read|file-write|process-exec|sysctl|network|mach-lookup|\.ssh|\.gnupg|Keychains|accounts\.yaml|provider-tests|\.netrc|\.config/gh|\.docker|password-store')
    return sorted(l for l in p.stdout.splitlines() if pat.search(l))


def build_native3(cell):
    """Build the native3 launch-plan tool and rebuild the native3 custodian from the vendored
    source with the native3 toolchain (Go 1.25.0); bind source to the pinned dist by identical
    normalised internal/macuid disassembly and SBPL string constants."""
    env = {'PATH': str(NATIVE3_GO.parent) + ':/usr/bin:/bin', 'HOME': str(cell.home), 'TMPDIR': str(cell.tmp) + '/',
           'GOCACHE': str(safe_mkdir(cell.dir / 'n3cache')), 'GOPATH': str(safe_mkdir(cell.dir / 'n3gopath')), 'GOTOOLCHAIN': 'local',
           'GOFLAGS': '-mod=mod', 'GOPROXY': 'off', 'CMPMAC_RUN_MARKER': cell.marker, 'DEVELOPER_DIR': '/Library/Developer/CommandLineTools'}
    tool = cell.apparatus / 'cmpmac-native3'; cust = cell.apparatus / 'native3-custodian-rebuild'
    monitored([str(NATIVE3_GO), 'build', '-trimpath', '-o', str(tool), './cmd/cmpmac-native3'], NATIVE3_DIR / 'src', env, cell)
    monitored([str(NATIVE3_GO), 'build', '-trimpath', '-o', str(cust), './internal/macuid/cmd/custodian'], NATIVE3_DIR / 'src', env, cell)
    dist = WORK / PINS['native3_custodian'][0]
    a, b = objdump_macuid(NATIVE3_GO, dist), objdump_macuid(NATIVE3_GO, cust)
    binding = {'dist_custodian_sha256': sha_file(dist), 'rebuild_custodian_sha256': sha_file(cust),
               'macuid_functions': sum(1 for l in a if l.startswith('TEXT ')),
               'macuid_disassembly_sha256': hashlib.sha256('\n'.join(a).encode()).hexdigest(),
               'macuid_disassembly_match': a == b, 'sbpl_strings_match': sbpl_strings(dist) == sbpl_strings(cust),
               'go': str(NATIVE3_GO), 'go_sha256': sha_file(NATIVE3_GO), 'source_tree': tree_digest(NATIVE3_DIR / 'src'),
               'note': 'binary bytes differ (cgo build paths); compiled internal/macuid code and SBPL strings are identical'}
    out = {str(NATIVE3_BINDING.relative_to(WORK)): safe_write(NATIVE3_BINDING, json.dumps(binding, indent=1, sort_keys=True) + '\n')}
    out[str(NATIVE3_TOOL.relative_to(WORK))] = safe_write(NATIVE3_TOOL, tool.read_bytes()); os.chmod(NATIVE3_TOOL, 0o700)
    if not (binding['macuid_disassembly_match'] and binding['sbpl_strings_match']): raise RuntimeError('native3 source does not match the pinned dist')
    return out


def build_native3_only():
    """Build only the native3 tool and binding; the existing arms' built tools stay untouched."""
    wait_for_load(0)
    cell = Cell(safe_makedirs(RUNS / ('build-' + uuid.uuid4().hex[:12]), RUNS), light=True)
    built = build_native3(cell)
    print(json.dumps({'built': built, 'binding': json.loads(NATIVE3_BINDING.read_text())}, indent=1))
    return 0


def build():
    """Build the Kogen launch-plan tool and the exec probe with run-local caches under monitored, marked processes."""
    wait_for_load(0)
    bid = 'build-' + uuid.uuid4().hex[:12]
    root = safe_makedirs(RUNS / bid, RUNS)
    cell = Cell(root, light=True)
    cache = safe_mkdir(cell.dir / 'cache'); gopath = safe_mkdir(cell.dir / 'gopath')
    out = cell.apparatus / 'cmpmac-sbpl'
    env = {'PATH': str(GO.parent) + ':/usr/bin:/bin', 'HOME': str(cell.home), 'TMPDIR': str(cell.tmp) + '/', 'GOCACHE': str(cache),
           'GOPATH': str(gopath), 'GOTOOLCHAIN': 'local', 'GOFLAGS': '-mod=mod', 'GOPROXY': 'off', 'CGO_ENABLED': '0',
           'CMPMAC_RUN_MARKER': cell.marker}
    monitored([str(GO), 'build', '-trimpath', '-o', str(out), '.'], WORK / 'vendor/kogen-sbpl', env, cell)
    probe = cell.apparatus / 'exec-probe'
    cenv = {'PATH': '/usr/bin:/bin', 'HOME': str(cell.home), 'TMPDIR': str(cell.tmp) + '/', 'CMPMAC_RUN_MARKER': cell.marker,
            'DEVELOPER_DIR': '/Library/Developer/CommandLineTools'}
    monitored(['/usr/bin/cc', '-O2', '-std=c99', '-Wall', '-Wextra', '-Werror', '-o', str(probe), str(FIXTURE_DIR / 'exec-probe.c')], cell.dir, cenv, cell)
    safe_mkdir(BUILD)
    built = {}
    for src, dst in ((out, SBPL_TOOL), (probe, EXEC_PROBE)):
        built[str(dst.relative_to(WORK))] = safe_write(dst, src.read_bytes()); os.chmod(dst, 0o700)
    built.update(build_native3(cell))
    print(json.dumps({'built': built, 'go': str(GO), 'cc': '/usr/bin/cc'}))
    return 0


# ---------------------------------------------------------------- main

def parse_arms(value, universe=ALL_ARMS):
    if not value: return list(universe)
    names = [x.strip() for x in value.split(',') if x.strip()]
    if len(set(names)) != len(names) or any(n not in universe for n in names): raise SystemExit('unknown or duplicate arm in --arms')
    return [a for a in universe if a in names]


def _raise_interrupt(signum, frame):
    raise Interrupted(signum)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=['build', 'build-native3', 'check', 'dry', 'measure', 'resume', '_worker'])
    ap.add_argument('run_id', nargs='?')
    ap.add_argument('--arms')
    ap.add_argument('--net', action='store_true', help='network-open variants (z control + NET_ARMS, NET_PLAN_FIXTURES)')
    ap.add_argument('--native3', action='store_true', help='kogen-native3-netopen (z control + native3, NET_PLAN_FIXTURES, overhead)')
    a = ap.parse_args(argv)
    if os.geteuid() == 0:
        print('REFUSED: harness must run unprivileged', file=sys.stderr); return 2
    signal.signal(signal.SIGINT, _raise_interrupt); signal.signal(signal.SIGTERM, _raise_interrupt)
    safe_mkdir(RESULTS); safe_mkdir(RUNS)
    try:
        if a.command == 'build': return build()
        if a.command == 'build-native3': return build_native3_only()
        if a.command == 'check': return check(parse_arms(a.arms))
        if a.command in ('dry', 'measure') and a.native3:
            run_id = new_run(a.command + '-native3', ['z-unsandboxed', NATIVE3_ARM], 1 if a.command == 'dry' else 3)
            return execute_run(run_id)
        if a.command in ('dry', 'measure') and a.net:
            run_id = new_run(a.command + '-net', ['z-unsandboxed', *NET_RUN_ARMS], 1 if a.command == 'dry' else 3)
            return execute_run(run_id)
        if a.command in ('dry', 'measure'):
            run_id = new_run(a.command, parse_arms(a.arms, ARMS), 1 if a.command == 'dry' else 3)
            return execute_run(run_id)
        if a.command in ('resume', '_worker'):
            if not a.run_id or '/' in a.run_id or a.run_id.startswith('.'): return 2
            meta = json.loads((RESULTS / a.run_id / 'run.json').read_text())
            if a.command == '_worker' and meta.get('kind') != 'interrupt-control': return 2
            return execute_run(a.run_id, hold_fixture='setsid' if a.command == '_worker' else None)
    except GateRefused as e:
        print(str(e), file=sys.stderr); return 2
    except LoadAbort as e:
        print(str(e) + ' (resumable)', file=sys.stderr); return 3
    except CleanupError as e:
        print('ABORT: ' + str(e), file=sys.stderr); return 2
    except Interrupted:
        print('interrupted; the ledger is resumable', file=sys.stderr); return 4
    except Exception as e:
        print('ERROR: ' + type(e).__name__ + ': ' + str(e), file=sys.stderr); return 2
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
