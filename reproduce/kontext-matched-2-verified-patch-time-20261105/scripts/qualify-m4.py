#!/usr/bin/env python3
"""Local red/green qualification harness for the Kogen-vs-direct benchmark cases.

    python3 qualify.py CASE CANDIDATE --out FOLDER [options]

CASE       gin | kogen | axios | ripgrep | faker | crane | gin405 | axios-timeout | rg-ignore | m2 and r4 cases (see CASES)
           r4 (kontext-matched-2 amendment 4): crane-* cases, kind 'zig' (Zig 0.16.0 on PATH, shared ZIG_*_CACHE_DIR)
CANDIDATE  `base` (control, expected RED), `ref` (control, expected GREEN) or
           the PATH of a source tree (expected GREEN).

Every run happens in a disposable snapshot (a clone/copy of the candidate in a
fresh temp directory).  The hidden test.patch is applied by overlaying the test
files that `base + test.patch` produces, so a candidate that edited or deleted
those files still gets the official tests.  fix.patch is applied only on
the `ref` control.  Crane has no patches: its hidden test is the embedded copy
of the old `streams` gate, and `ref` overlays cases/crane/ref.

Files written to FOLDER
    result.json     verdict, timings, command, evidence.  INTERNAL: names tests.
    raw.log         unfiltered merged stdout+stderr (capped).  INTERNAL.
    diagnostic.txt  bounded, sanitized output that is safe to show an agent.

Exit status
    0  outcome matches the expectation (base: intended red, ref/PATH: green)
    1  conclusive but unexpected (control invalid, or candidate red)
    2  inconclusive: setup/environment failure, timeout, tests did not run,
       red that cannot be attributed to the intended behaviour, usage error

No network, no installs: Go runs with GOPROXY=off and GOTOOLCHAIN=local, cargo
with CARGO_NET_OFFLINE and rustup auto-install disabled.  Every subprocess has
a timeout and runs in its own process group that is killed on expiry.
"""
import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW_CAP = 16 * 1024 * 1024
UTIL_TIMEOUT = 120  # copy / patch / probe steps

CASES = {
    'gin': dict(
        kind='go', cwd='.', timeout=300, patched=True,
        cmd=['go', 'test', '-v', '.', '-run', '^TestContext.*Bind'],
        name_filter=r'^TestContext.*Bind', verbose=True),
    'kogen': dict(
        kind='go', cwd='cli', timeout=600, patched=True,
        cmd=['go', 'test', './provider'], verbose=False),
    'axios': dict(
        kind='mocha', cwd='.', timeout=300, patched=True,
        cmd=['node', 'node_modules/mocha/bin/mocha.js', '-R', 'tap', '--timeout', '30000', '--exit',
             'test/unit/regression/bugs.js'],
        run_files=['test/unit/regression/bugs.js'], deps=['node_modules']),
    'ripgrep': dict(
        kind='cargo', cwd='.', timeout=1800, patched=True,
        cmd=['cargo', 'test', '--locked', '--package', 'ripgrep', '--test', 'integration', '--',
             'regression::r2574'],
        filter='regression::r2574'),
    'faker': dict(
        kind='ruby', cwd='.', timeout=300, patched=True,
        cmd=['bundle', 'exec', 'ruby', 'test/faker/default/test_faker_internet.rb', '-v', '-n', '/email/'],
        name_filter=r'email'),
    'crane': dict(kind='crane', cwd='.', timeout=120, patched=False, cmd=None),
    # --- second-cohort confirmation cases (cases/<name>/ holds the patches) ---
    # -v is needed so the judge can see the hidden test pass; the extra names are
    # existing NoRoute/NoMethod routing checks that must keep passing.
    'gin405': dict(
        kind='go', cwd='.', timeout=300, patched=True,
        cmd=['go', 'test', '-v', './', '-run',
             '^(TestMethodNotAllowedNoRoute|TestNoRouteWithoutGlobalHandlers|TestNoRouteWithGlobalHandlers'
             '|TestNoMethodWithoutGlobalHandlers|TestNoMethodWithGlobalHandlers)$'],
        name_filter=r'^TestMethodNotAllowedNoRoute$', verbose=True),
    # test.patch only edits an assertion inside an existing `it`, so the hidden
    # title is declared here; the neighbouring plain-timeout test is kept as a check.
    'axios-timeout': dict(
        kind='mocha', cwd='.', timeout=300, patched=True,
        mocha_bin='mocha',  # older Mocha: executable is bin/mocha (no .js)
        cmd=['node', 'node_modules/mocha/bin/mocha', '-R', 'tap', '--timeout', '30000', '--exit',
             'test/unit/adapters/http.js', '--grep',
             'should respect the (timeoutErrorMessage|timeout) property'],
        run_files=['test/unit/adapters/http.js'], deps=['node_modules'],
        hidden_titles=['should respect the timeoutErrorMessage property']),
    'rg-ignore': dict(
        kind='cargo', cwd='.', timeout=1800, patched=True,
        cmd=['cargo', 'test', '--locked', '--package', 'ripgrep', '--test', 'integration', '--',
             'regression::r2208'],
        filter='regression::r2208'),
    # --- kontext-matched-2 cases (SWE-bench Multilingual instances; cases/<name>/ built by mk_case.py) ---
    'gin3741': dict(
        kind='go', cwd='.', timeout=300, patched=True,
        cmd=['go', 'test', '-v', '.', '-run', '^TestColorForStatus$'],
        name_filter=r'^TestColorForStatus$', verbose=True),
    'gin3820': dict(
        kind='go', cwd='.', timeout=300, patched=True,
        cmd=['go', 'test', '-v', './binding', '-run', '^TestMappingBaseTypes$'],
        name_filter=r'^TestMappingBaseTypes$', verbose=True),
    'bat2201': dict(
        kind='cargo', cwd='.', timeout=1800, patched=True,
        cmd=['cargo', 'test', '--locked', '--test', 'integration_tests', '--',
             'disable_pager_if_disable_paging_flag_comes_after_paging'],
        filter='disable_pager_if_disable_paging_flag_comes_after_paging'),
    'bat2650': dict(
        kind='cargo', cwd='.', timeout=1800, patched=True,
        cmd=['cargo', 'test', '--locked', '--test', 'integration_tests', '--',
             'highlighting_independant_from_map_syntax_case'],
        filter='highlighting_independant_from_map_syntax_case'),
    'tokio6752': dict(
        kind='cargo', cwd='.', timeout=1800, patched=True,
        cmd=['cargo', 'test', '--locked', '-p', 'tokio-util', '--features', 'full', '--test', 'time_delay_queue', '--',
             'wake_after_remove_last'],
        filter='wake_after_remove_last'),
    'caddy4943': dict(
        kind='go', cwd='.', timeout=600, patched=True,
        cmd=['go', 'test', '-v', './modules/logging', '-run', '^TestCookieFilter$'],
        name_filter=r'^TestCookieFilter$', verbose=True),
    'caddy6115': dict(
        kind='go', cwd='.', timeout=600, patched=True,
        cmd=['go', 'test', '-v', './modules/caddyhttp/reverseproxy', '-run', '^(TestCookieHashPolicy|TestCookieHashPolicyWithSecureRequest)$'],
        name_filter=r'^TestCookieHashPolicyWithSecureRequest$', verbose=True),
    'jekyll9141': dict(
        kind='ruby', cwd='.', timeout=600, patched=True,
        cmd=['bundle', 'exec', 'ruby', '-I', 'test', 'test/test_site.rb', '-v', '-n', '/static files/'],
        name_filter=r'static files', shoulda=True),
    # --- kontext-matched-2 r4: Crane (github.com/zig-whatwg/crane) native-test cases; cases/<name>/ built by mk-crane-case.sh.
    # Hidden check = the fix commit's own new test file, run through the repository's own build (-Dtest-file).
    'crane-cssesc': dict(
        kind='zig', cwd='.', timeout=900, patched=True, test_file='tests/css/om1_name_eql_escapes_test.zig',
        cmd=['zig', 'build', 'test', '-Dspec=css', '-Dtest-file=tests/css/om1_name_eql_escapes_test.zig', '--summary', 'all']),
    'crane-xmlpe': dict(
        kind='zig', cwd='.', timeout=900, patched=True, test_file='tests/xml/xm1_entity_declaration_test.zig',
        cmd=['zig', 'build', 'test', '-Dspec=xml', '-Dtest-file=tests/xml/xm1_entity_declaration_test.zig', '--summary', 'all']),
    'crane-cssshape': dict(
        kind='zig', cwd='.', timeout=900, patched=True, test_file='tests/css/ci1_shape_scalar_extended_units_test.zig',
        cmd=['zig', 'build', 'test', '-Dspec=css', '-Dtest-file=tests/css/ci1_shape_scalar_extended_units_test.zig', '--summary', 'all']),
    'axios4731': dict(
        kind='mocha', cwd='.', timeout=300, patched=True, mocha_bin='mocha',
        cmd=['node', 'node_modules/mocha/bin/mocha', '-R', 'tap', '--timeout', '30000', '--exit',
             'test/unit/adapters/http.js', '--grep', 'should properly support default max body length'],
        run_files=['test/unit/adapters/http.js'], deps=['node_modules'],
        hidden_titles=['should properly support default max body length (follow-redirects as well)']),
}

# ------------------------------------------------------------------ crane ----
# Copied verbatim from crane-old-gate.py (gate `streams`): the hidden test.
STREAMS_DRIVER = r'''
import importlib.util, json, os, sys, tempfile

src = sys.argv[1]
spec = importlib.util.spec_from_file_location('wpt_progress_under_test', src)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

failures = []
def check(name, fn):
    try:
        fn()
        print('PASS', name)
    except AssertionError as e:
        failures.append(name)
        print('FAIL', name, '::', e)
    except Exception as e:
        failures.append(name)
        print('FAIL', name, ':: unexpected', type(e).__name__, e)

with tempfile.TemporaryDirectory() as d:
    m.RESULTS = os.path.join(d, 'wpt-results')
    m.STATE = os.path.join(d, 'state', 'state.json')
    m.HISTORY = os.path.join(d, 'wpt-results', 'progress-history.json')
    os.makedirs(os.path.join(m.RESULTS, 'sweep-0123abcde'))
    os.makedirs(os.path.join(m.RESULTS, 'heap-1111aaaaa'))

    def write(rel, recs, mtime):
        fn = os.path.join(m.RESULTS, rel)
        with open(fn, 'w') as f:
            for r in recs:
                f.write(json.dumps(r) + '\n')
        os.utime(fn, (mtime, mtime))
        return fn

    # Real journals (older) ...
    write('journal.jsonl',
          [{'path': 'a.html', 'status': 'OK', 'passed': 4},
           {'path': 'b.html', 'status': 'OK', 'passed': 2}], 1000)
    write('sweep-0123abcde/journal.shard1.jsonl',
          [{'path': 'c.html', 'status': 'TIMEOUT', 'passed': 0}], 1100)
    # ... and FALSE journals beside them: result streams (per-subtest detail),
    # newer than every journal, whose lines also carry `path` and `status`.
    write('sweep-0123abcde/journal.wptreport.jsonl',
          [{'path': 'b.html', 'status': 'CRASH', 'passed': 0},
           {'path': 'only-in-stream.html', 'status': 'ERROR', 'passed': 0}], 2000)
    write('journal.wptreport.jsonl',
          [{'path': 'a.html', 'status': 'CRASH', 'passed': 0}], 2100)

    state = {}
    def load():
        state['records'], state['files'] = m.load_results()

    def c_journals_consumed():
        load()
        r = state['records']
        assert r.get('c.html', {}).get('status') == 'TIMEOUT', ('shard journal in label dir not consumed', r.get('c.html'))
        assert r.get('a.html') is not None and r.get('b.html') is not None, 'top-level journal paths missing'
        assert any(v.get('_sub_hw_pre', 0) + v.get('_sub_hw', 0) >= 4 for v in r.values() if v['path'] == 'a.html'), 'journal counts lost'
        names = [os.path.basename(f) for f in state['files']]
        assert 'journal.jsonl' in names and 'journal.shard1.jsonl' in names, names

    def c_stream_not_a_journal():
        load()
        r = state['records']
        assert r['b.html']['status'] == 'OK', ('result stream superseded the journal record', r['b.html'])
        assert r['a.html']['status'] == 'OK', ('top-level result stream superseded the journal record', r['a.html'])
        assert 'only-in-stream.html' not in r, 'a path found only in a result stream became a record'

    def c_files_list():
        load()
        bad = [f for f in state['files'] if f.endswith('.wptreport.jsonl')]
        assert not bad, ('result streams listed among the journals read', bad)

    def c_state_clean():
        load()
        saved = json.load(open(m.STATE))
        assert saved['b.html']['status'] == 'OK' and 'only-in-stream.html' not in saved, 'accumulated state polluted by a stream'

    def c_heap_trend():
        # Real single-process journal: heap grows 10 kB/file. A newer false
        # journal beside it grows 900 kB/file; the trend must be the real one's.
        write('heap-1111aaaaa/journal.jsonl',
              [{'path': f'h{i}.html', 'status': 'OK', 'passed': 1, 'index': i, 'heap_used_kb': 50000 + 10 * i}
               for i in range(40)], 3000)
        write('heap-1111aaaaa/journal.wptreport.jsonl',
              [{'path': f'h{i}.html', 'status': 'OK', 'passed': 1, 'index': i, 'heap_used_kb': 50000 + 900 * i}
               for i in range(40)], 3500)
        t = m.heap_trend()
        assert t is not None, 'no trend at all'
        assert not t['journal'].endswith('.wptreport.jsonl'), ('trend read from a result stream', t['journal'])
        assert abs(t['kb_per_file'] - 10) < 0.5, ("slope is not the journal's", t['kb_per_file'])

    check('journals-still-consumed', c_journals_consumed)
    check('result-stream-is-not-a-journal-record', c_stream_not_a_journal)
    check('result-stream-not-in-files-read', c_files_list)
    check('state-not-polluted', c_state_clean)
    check('heap-trend-skips-result-stream', c_heap_trend)

print('RESULT', 'RED' if failures else 'GREEN', failures)
sys.exit(1 if failures else 0)
'''


# ---------------------------------------------------------------- helpers ----

class Inconclusive(Exception):
    """Environment/setup problem: nothing can be said about the behaviour."""


def now():
    return time.monotonic()


def run_cmd(cmd, cwd, env, timeout, raw_path=None, cap=RAW_CAP):
    """Run with a hard timeout in its own process group.  Returns dict."""
    start = now()
    timed_out = False
    sink = open(raw_path, 'wb') if raw_path else None
    written = [0]
    try:
        p = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, start_new_session=True)
    except OSError as e:
        if sink:
            sink.close()
        return dict(rc=None, timed_out=False, elapsed=now() - start, error=f'{type(e).__name__}: {e}', out=b'')
    chunks = []

    def pump():
        for block in iter(lambda: p.stdout.read(65536), b''):
            if sink and written[0] < cap:
                part = block[:cap - written[0]]
                sink.write(part)
                written[0] += len(part)
                if written[0] >= cap:
                    sink.write(b'\n[raw log truncated at cap]\n')
            if not sink and sum(map(len, chunks)) < cap:
                chunks.append(block)

    t = threading.Thread(target=pump, daemon=True)
    t.start()
    try:
        p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(p.pid, sig)
            except OSError:
                break
            try:
                p.wait(timeout=5)
                break
            except subprocess.TimeoutExpired:
                continue
    t.join(timeout=10)
    try:
        # Grandchildren that outlived the group kill: make sure nothing lingers.
        os.killpg(p.pid, signal.SIGKILL)
    except OSError:
        pass
    if sink:
        sink.close()
    return dict(rc=p.returncode, timed_out=timed_out, elapsed=now() - start, error=None, out=b''.join(chunks))


def clone_tree(src, dst):
    """Copy the contents of src into the (existing) dst; APFS clone when possible."""
    src, dst = str(src), str(dst)
    attempts = []
    if sys.platform == 'darwin':
        attempts.append(['cp', '-cR', src + '/.', dst])
    attempts.append(['cp', '-R', src + '/.', dst])
    for cmd in attempts:
        r = run_cmd(cmd, None, os.environ.copy(), UTIL_TIMEOUT)
        if r['rc'] == 0 and not r['timed_out']:
            return
    raise Inconclusive(f'could not copy {src} into the snapshot')


def git_apply(patch, root):
    env = dict(os.environ, GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    r = run_cmd(['git', 'apply', '--whitespace=nowarn', str(patch)], str(root), env, UTIL_TIMEOUT)
    if r['rc'] != 0:
        detail = r['error'] or r['out'].decode('utf-8', 'replace')[:300] or 'git apply failed or timed out'
        raise Inconclusive(f'{Path(patch).name} does not apply cleanly: {detail}')


def patch_files(text):
    files = []
    for m in re.finditer(r'^diff --git a/(\S+) b/(\S+)$', text, re.M):
        files.append(m.group(2))
    return files


def patch_sections(text):
    """{file: section text}"""
    parts = re.split(r'(?m)^(?=diff --git )', text)
    out = {}
    for part in parts:
        m = re.match(r'diff --git a/(\S+) b/(\S+)', part)
        if m:
            out[m.group(2)] = part
    return out


def patch_content_lines(*texts):
    """Stripped content of added/removed lines (what must never reach an agent)."""
    secrets = set()
    for text in texts:
        for line in text.splitlines():
            if line[:1] in '+-' and not line.startswith(('+++', '---')):
                s = line[1:].strip()
                if len(s) >= 12 and re.search(r'[A-Za-z0-9]{3}', s):
                    secrets.add(s)
    return secrets


def overlay_tests(case_dir, base, snap):
    """Overlay test files produced by base+test.patch onto the snapshot."""
    patch = case_dir / 'test.patch'
    text = patch.read_text()
    files = patch_files(text)
    with tempfile.TemporaryDirectory(prefix='qualify-scratch-') as scratch:
        for f in files:
            if (base / f).is_file():
                (Path(scratch) / f).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(base / f, Path(scratch) / f)
        git_apply(patch, scratch)
        for f in files:
            src, dst = Path(scratch) / f, snap / f
            if src.is_file():
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.is_symlink() or dst.exists():
                    dst.unlink()
                shutil.copy2(src, dst)
            elif dst.exists():
                dst.unlink()
    return files, text


# --------------------------------------------------------------- environment ----

ENV_KEEP = ('PATH', 'HOME', 'USER', 'LOGNAME', 'LANG', 'LC_ALL', 'LC_CTYPE', 'TERM', 'SHELL', 'TMPDIR',
            'GOPATH', 'GOMODCACHE', 'GOCACHE', 'GOROOT', 'NVM_DIR', 'GEM_HOME', 'GEM_PATH',
            'BUNDLE_PATH', 'BUNDLE_APP_CONFIG', 'BUNDLE_USER_HOME', 'BUNDLE_USER_CACHE', 'SSL_CERT_FILE')


def build_env(spec, args, snap, tmp):
    env = {k: os.environ[k] for k in ENV_KEEP if k in os.environ}
    env.setdefault('PATH', '/usr/bin:/bin')
    env.update(CI='1', NO_COLOR='1', TMPDIR=str(tmp))
    kind = spec['kind']
    extra_path = []
    if kind == 'go':
        env.update(GOPROXY='off', GOTOOLCHAIN='local', GOFLAGS='-buildvcs=false', GOSUMDB='off', GONOSUMDB='*')
    elif kind == 'cargo':
        ch = args.cargo_home or os.environ.get('QUALIFY_CARGO_HOME') or os.environ.get('CARGO_HOME')
        rh = args.rustup_home or os.environ.get('QUALIFY_RUSTUP_HOME') or os.environ.get('RUSTUP_HOME')
        if ch:
            env['CARGO_HOME'] = ch
            extra_path.append(str(Path(ch) / 'bin'))
        if rh:
            env['RUSTUP_HOME'] = rh
        if args.rust_bin:
            extra_path.insert(0, args.rust_bin)
        tc = args.rust_toolchain or os.environ.get('QUALIFY_RUST_TOOLCHAIN')
        if tc:
            env['RUSTUP_TOOLCHAIN'] = tc
        env.update(CARGO_NET_OFFLINE='true', RUSTUP_AUTO_INSTALL='0', CARGO_TERM_COLOR='never',
                   CARGO_INCREMENTAL='0')
        if args.cargo_target_dir:
            env['CARGO_TARGET_DIR'] = str(Path(args.cargo_target_dir).resolve())
        else:
            env['CARGO_TARGET_DIR'] = str(snap / 'target')
    elif kind == 'zig':  # r4: shared, content-addressed Zig caches (dependencies prefetched; no network needed)
        for k in ('ZIG_GLOBAL_CACHE_DIR', 'ZIG_LOCAL_CACHE_DIR'):
            if os.environ.get(k):
                env[k] = os.environ[k]
    elif kind == 'ruby':
        if args.ruby_bin:
            extra_path.append(args.ruby_bin)
        env.update(BUNDLE_GEMFILE=str(snap / 'Gemfile'), BUNDLE_DISABLE_VERSION_CHECK='1')
    for kv in args.env or []:
        k, _, v = kv.partition('=')
        env[k] = v
    if extra_path:
        env['PATH'] = os.pathsep.join(extra_path + [env['PATH']])
    return env


# ------------------------------------------------------------------ judges ----
# Each judge returns dict(verdict=green|red|inconclusive, intended=bool|None,
# reason=str, evidence=[...], hidden=[...]).  `strict` is True for controls: a
# red is only `intended` when it is attributable to the hidden test.

def J(verdict, reason, intended=None, evidence=None, hidden=None, **kw):
    d = dict(verdict=verdict, reason=reason, intended=intended, evidence=evidence or [], hidden=hidden or [])
    d.update(kw)
    return d


GO_SETUP = re.compile(
    r'cannot find module|no required module|go: downloading|dial tcp|lookup \S+ on|GOPROXY|missing go\.sum|'
    r'updates to go\.(mod|sum) needed|go: .*requires go >=|toolchain|cannot find package|no matching versions|'
    r'is not in std|read-only file system|operation not permitted|go: command not found|'
    r'go\.mod file not found|errors parsing go\.mod|inconsistent vendoring|build cache is required', re.I)
GO_ERR = re.compile(r'^(?:vet: )?(\S+\.go):(\d+):(?:\d+:)? (.*)$')
GO_INTENDED_ERR = re.compile(
    r'undefined|has no field or method|not declared|undeclared|cannot use|too many arguments|'
    r'not enough arguments|unknown field|assignment mismatch|does not implement|missing return|'
    r'cannot refer to unexported|invalid operation|cannot infer', re.I)


def go_hidden_names(case, spec, test_text):
    names = set()
    for m in re.finditer(r'^\+func (Test\w+)\(', test_text, re.M):
        names.add(m.group(1))
    for m in re.finditer(r'^@@[^@]*@@.*?\bfunc (Test\w+)\(', test_text, re.M):
        names.add(m.group(1))
    flt = spec.get('name_filter')
    if flt:
        rx = re.compile(flt)
        names = {n for n in names if rx.search(n)}
    return sorted(names)


def judge_go(spec, ctx, text, rc, timed_out):
    hidden = go_hidden_names(ctx['case'], spec, ctx['test_text'])
    touched = [Path(f).name for f in ctx['test_files']]
    fails = sorted(set(re.findall(r'^\s*--- FAIL: (Test\w+)', text, re.M)))
    passes = set(re.findall(r'^\s*--- PASS: (Test\w+)', text, re.M))
    hidden_fail = [n for n in fails if n in hidden]
    errs = [GO_ERR.match(l.strip()) for l in text.splitlines()]
    errs = [(m.group(1), m.group(3)) for m in errs if m]
    if rc == 0 and not timed_out:
        ok_line = re.search(r'^ok\s', text, re.M)
        if not ok_line or 'no tests to run' in text:
            return J('inconclusive', 'exit 0 but no ok line / no tests to run', hidden=hidden)
        if spec.get('verbose'):
            missing = [n for n in hidden if n not in passes]
            if missing or not hidden:
                return J('inconclusive', 'hidden tests not seen passing: %s' % missing, hidden=hidden)
        return J('green', 'all tests pass', hidden=hidden)
    if hidden_fail:
        return J('red', 'hidden tests failed', True, evidence=hidden_fail, hidden=hidden)
    if GO_SETUP.search(text) and not errs:
        return J('inconclusive', 'setup failure: ' + GO_SETUP.search(text).group(0), hidden=hidden)
    if errs:
        intended = [e for e in errs if Path(e[0]).name in touched and GO_INTENDED_ERR.search(e[1])]
        other = [e for e in errs if e not in intended]
        if intended and not other:
            return J('red', 'test build fails on the missing behaviour', True,
                     evidence=[f'{f}: {m}' for f, m in intended[:5]], hidden=hidden)
        return J('red', 'build errors not attributable to hidden tests', False,
                 evidence=[f'{f}: {m}' for f, m in errs[:5]], hidden=hidden)
    if GO_SETUP.search(text):
        return J('inconclusive', 'setup failure: ' + GO_SETUP.search(text).group(0), hidden=hidden)
    if fails or 'panic:' in text:
        return J('red', 'non-hidden tests failed / panic', False, evidence=fails[:5], hidden=hidden)
    return J('inconclusive', 'non-zero exit without recognisable test or compile failure', hidden=hidden)


NET_ERR = re.compile(r'ENOTFOUND|EAI_AGAIN|ECONNREFUSED|ENETUNREACH|EHOSTUNREACH|getaddrinfo|ETIMEDOUT|ECONNRESET|'
                     r'socket hang up|certificate|CERT_|network', re.I)
SANDBOX_ERR = re.compile(r'EPERM|EACCES|operation not permitted|listen EADDRINUSE', re.I)


def parse_tap(text):
    tests, cur = [], None
    for line in text.splitlines():
        m = re.match(r'^(not )?ok \d+ (.*)$', line)
        if m:
            cur = dict(ok=not m.group(1), title=m.group(2).strip(), block=[])
            tests.append(cur)
        elif cur is not None and not line.startswith('#') and not re.match(r'^\d+\.\.\d+', line):
            cur['block'].append(line)
    return tests


def judge_mocha(spec, ctx, text, rc, timed_out):
    sections = patch_sections(ctx['test_text'])
    hidden = list(spec.get('hidden_titles', []))
    for f, sec in sections.items():
        if f in spec['run_files']:
            hidden += [m.group(2) for m in re.finditer(r'''^\+\s*it\((['"`])(.*?)\1''', sec, re.M)]
    tests = parse_tap(text)
    if not tests:
        return J('inconclusive', 'no TAP test results (load/setup failure)', hidden=hidden)
    def is_hidden(t):
        return any(h in t['title'] for h in hidden)
    hid = [t for t in tests if is_hidden(t)]
    if not hidden or not hid:
        return J('inconclusive', 'hidden test not found in TAP output', hidden=hidden)
    bad_h = [t for t in hid if not t['ok']]
    if bad_h:
        blk = '\n'.join(sum((t['block'] for t in bad_h), []))
        if SANDBOX_ERR.search(blk) or NET_ERR.search(blk):
            return J('inconclusive', 'hidden test failed on environment error', evidence=[bad_h[0]['title']], hidden=hidden)
        intended = bool(re.search(r'AssertionError|ERR_ASSERTION', blk))
        return J('red', 'hidden test failed', intended, evidence=[t['title'] for t in bad_h], hidden=hidden)
    others = [t for t in tests if not t['ok'] and not is_hidden(t)]
    tolerated, real = [], []
    for t in others:
        (tolerated if NET_ERR.search('\n'.join(t['block'])) else real).append(t['title'])
    if real:
        return J('red', 'non-hidden tests failed', False, evidence=real[:5], hidden=hidden, tolerated=tolerated)
    return J('green', 'hidden tests pass' + (' (offline-only failures tolerated)' if tolerated else ''),
             hidden=hidden, tolerated=tolerated)


CARGO_SETUP = re.compile(
    r'no such command|command not found|rustup could not choose|toolchain .* is not installed|'
    r'failed to (get|download|fetch|load source|query)|unable to update registry|attempting to make an HTTP request|'
    r'network failure|offline|couldn.t resolve|failed to select a version|the lock file .* needs to be updated|'
    r'linker .* not found|linking with .* failed|failed to run custom build|failed to create directory|'
    r'Read-only file system|Operation not permitted|no override and no default toolchain', re.I)


def judge_cargo(spec, ctx, text, rc, timed_out):
    hidden = re.findall(r'^\+rgtest!\((\w+)', ctx['test_text'], re.M)
    name = spec['filter']
    ok = re.search(r'^test %s \.\.\. ok$' % re.escape(name), text, re.M)
    failed = re.search(r'^test %s \.\.\. FAILED$' % re.escape(name), text, re.M)
    if rc == 0 and ok:
        return J('green', 'target test passes', hidden=hidden)
    if failed:
        return J('red', 'target test failed', True, evidence=['test %s ... FAILED' % name], hidden=hidden)
    if CARGO_SETUP.search(text):
        return J('inconclusive', 'setup failure: ' + CARGO_SETUP.search(text).group(0), hidden=hidden)
    if re.search(r'^error(\[E\d+\])?: ', text, re.M):
        return J('red', 'build error', False, evidence=re.findall(r'^error.*$', text, re.M)[:3], hidden=hidden)
    if rc == 0:
        return J('inconclusive', 'exit 0 but target test not seen passing', hidden=hidden)
    return J('inconclusive', 'non-zero exit without recognisable test or compile failure', hidden=hidden)


RUBY_SETUP = re.compile(
    r'LoadError|cannot load such file|Could not find .* in (any of the )?(gems|locally)|Bundler::|BundlerError|'
    r'GemNotFound|bundle install|Gem::|command not found|No such file or directory - bundle|'
    r'requires Ruby version|Your Ruby version', re.I)


def judge_ruby(spec, ctx, text, rc, timed_out):
    hidden = sorted(set(re.findall(r'^\+\s*def (test_\w+)', ctx['test_text'], re.M)))
    hidden = [h for h in hidden if re.search(spec['name_filter'], h)]
    if spec.get('shoulda'):  # m2: shoulda `should "title"` blocks; -v prints `<title> = 0.00 s = .|F|E`
        titles = re.findall(r'^\+\s*should "(.*?)" do', ctx['test_text'], re.M)
        pf = re.search(r'(\d+) (?:runs?|tests?), (\d+) assertions?, (\d+) failures?, (\d+) errors?', text)
        if not titles or not pf:
            return J('inconclusive', 'no shoulda titles / minitest summary', hidden=titles)
        runs, _, fails, errors = map(int, pf.groups())
        st = {t: re.search(re.escape(t) + r'\.?\s+(?:=\s+)?[\d.]+ (?:s )?= ([.FE])', text) for t in titles}
        if any(m is None for m in st.values()):
            return J('inconclusive', 'hidden test not found in output', hidden=titles)
        bad = [t for t, m in st.items() if m.group(1) != '.']
        if bad:
            return J('red', 'hidden tests failed', True, evidence=bad, hidden=titles)
        if rc == 0 and runs > 0 and fails == 0 and errors == 0:
            return J('green', 'all selected tests pass', hidden=titles)
        return J('red', 'non-hidden tests failed', False, hidden=titles)
    tu = re.search(r'^(\d+) tests?, (\d+) assertions?, (\d+) failures?, (\d+) errors?', text, re.M)  # m2: test-unit (faker)
    if tu:
        runs, _, fails, errors = map(int, tu.groups())
        st = {h: re.search(r'^\s*' + re.escape(h) + r':\s+([.FE])', text, re.M) for h in hidden}
        if not hidden or any(m is None for m in st.values()):
            return J('inconclusive', 'hidden test-unit tests not found in output', hidden=hidden)
        bad = [h for h, m in st.items() if m.group(1) != '.']
        if bad:
            return J('red', 'hidden tests failed', True, evidence=bad, hidden=hidden)
        if rc == 0 and runs > 0 and fails == 0 and errors == 0:
            return J('green', 'all selected tests pass', hidden=hidden)
        return J('red', 'non-hidden tests failed', False, hidden=hidden)
    summary = re.search(r'(\d+) runs?, (\d+) assertions?, (\d+) failures?, (\d+) errors?', text)
    if not summary:
        why = RUBY_SETUP.search(text)
        return J('inconclusive', 'no minitest summary' + (': ' + why.group(0) if why else ''), hidden=hidden)
    runs, _, fails, errors = map(int, summary.groups())
    if rc == 0 and runs > 0 and fails == 0 and errors == 0:
        seen = [h for h in hidden if re.search(r'#%s = [\d.]+ s = \.' % re.escape(h), text)]
        if hidden and len(seen) != len(hidden):
            return J('inconclusive', 'hidden tests not seen passing', hidden=hidden)
        return J('green', 'all selected tests pass', hidden=hidden)
    hf = [h for h in hidden if re.search(r'#%s = [\d.]+ s = [FE]' % re.escape(h), text)]
    if hf:
        env_err = RUBY_SETUP.search(text)
        if env_err:
            return J('inconclusive', 'setup failure: ' + env_err.group(0), hidden=hidden)
        return J('red', 'hidden tests failed', True, evidence=hf, hidden=hidden)
    return J('red', 'non-hidden tests failed', False, hidden=hidden)


def judge_crane(spec, ctx, text, rc, timed_out):
    fails = re.findall(r'^FAIL (\S+) :: (.*)$', text, re.M)
    if rc == 0 and re.search(r'^RESULT GREEN', text, re.M):
        return J('green', 'all streams checks pass')
    if rc == 1 and re.search(r'^RESULT RED', text, re.M):
        asserts = [n for n, m in fails if not m.startswith('unexpected')]
        if asserts:
            return J('red', 'streams checks failed by assertion', True, evidence=asserts)
        return J('red', 'streams checks raised unexpected errors', False, evidence=[n for n, _ in fails])
    return J('inconclusive', 'driver did not reach a result (import error or crash)')


ZIG_SETUP = re.compile(r'unable to (?:fetch|connect|download)|FileNotFound|AccessDenied|no such file or directory|'
                       r'invalid option: -D|unable to find zig|zig version .* (?:does not|is not)', re.I)


def judge_zig(spec, ctx, text, rc, timed_out):
    """r4: `zig build test -Dtest-file=F --summary all`; the hidden tests are the test blocks of F (test.patch)."""
    titles = re.findall(r'^\+test "(.*?)" \{', ctx['test_text'], re.M)
    stem = Path(spec['test_file']).stem
    run = re.search(r'run test %s (\d+) pass(?:, (\d+) skip)?(?:, (\d+) fail)?(?:, (\d+) leak)?(?:, (\d+) crash)? \((\d+) total\)'
                    % re.escape(stem), text)
    failed = sorted(set(m.group(1) for m in re.finditer(r"'%s\.test\.(.*?)' failed" % re.escape(stem), text)))
    hid_failed = [t for t in failed if t in titles] or ([t for t in titles if t in text and 'failed' in text] if not failed else [])
    if run:
        npass, nskip, nfail, nleak, ncrash, total = (int(x or 0) for x in run.groups())
        if rc == 0 and npass == total and total >= len(titles) and not nfail:
            return J('green', 'hidden test file passes (%d/%d) and the build test step succeeds' % (npass, total), hidden=titles)
        if nfail or nleak or ncrash or failed:
            if failed and all(t in titles for t in failed):
                return J('red', 'hidden tests failed', True, evidence=failed[:8], hidden=titles)
            return J('red', 'hidden test file failed (%d fail, %d leak, %d crash)' % (nfail, nleak, ncrash), bool(nfail),
                     evidence=failed[:8], hidden=titles)
        if rc != 0:
            return J('red', 'hidden test file passed but another build step failed', False,
                     evidence=re.findall(r'^error: .*$', text, re.M)[:3], hidden=titles)
    if re.search(r'compile test %s .*fail' % re.escape(stem), text) or re.search(r'^\S+\.zig:\d+:\d+: error: ', text, re.M):
        return J('red', 'compile error', False, evidence=re.findall(r'^\S+\.zig:\d+:\d+: error: .*$', text, re.M)[:3], hidden=titles)
    if ZIG_SETUP.search(text):
        return J('inconclusive', 'setup failure: ' + ZIG_SETUP.search(text).group(0), hidden=titles)
    return J('inconclusive', 'hidden test file run not seen in the build summary', hidden=titles)


JUDGES = dict(zig=judge_zig, go=judge_go, mocha=judge_mocha, cargo=judge_cargo, ruby=judge_ruby, crane=judge_crane)


# ----------------------------------------------------------------- prechecks ----

def which_in(env, name):
    return shutil.which(name, path=env['PATH'])


def precheck(spec, args, snap, env, base):
    """Raise Inconclusive when the toolchain/dependencies are absent (never installs)."""
    kind = spec['kind']
    exe = spec['cmd'][0] if spec['cmd'] else sys.executable
    if kind != 'crane' and not which_in(env, exe):
        hint = ''
        if kind == 'cargo':
            hint = ' (pass --cargo-home/--rustup-home/--rust-bin or set QUALIFY_CARGO_HOME / QUALIFY_RUSTUP_HOME)'
        if kind == 'ruby':
            hint = ' (pass --ruby-bin DIR of a Ruby >= required)'
        raise Inconclusive(f'{exe!r} not found on PATH{hint}')
    if kind == 'zig':
        r = run_cmd(['zig', 'version'], str(snap), env, 60)
        if r['rc'] != 0:
            raise Inconclusive('zig does not run')
    if kind == 'mocha' and not (snap / 'node_modules' / 'mocha' / 'bin' / spec.get('mocha_bin', 'mocha.js')).is_file():
        raise Inconclusive('node_modules/mocha missing: npm ci has not completed')
    if kind == 'cargo':
        if not (snap / 'Cargo.lock').is_file():
            raise Inconclusive('Cargo.lock missing (--locked)')
        r = run_cmd(['cargo', '--version'], str(snap), env, 60)
        if r['rc'] != 0:
            raise Inconclusive('cargo does not run: ' + (r['error'] or r['out'].decode('utf-8', 'replace')[:300]))
        r = run_cmd(['rustc', '--version'], str(snap), env, 60)
        if r['rc'] != 0:
            raise Inconclusive('rustc does not run (toolchain not installed offline?): '
                               + r['out'].decode('utf-8', 'replace')[:300])
    if kind == 'ruby':
        gemspec = (snap / 'faker.gemspec')
        need = re.search(r"required_ruby_version\s*=\s*'>=\s*([\d.]+)'", gemspec.read_text()) if gemspec.is_file() else None
        r = run_cmd(['ruby', '-e', 'print RUBY_VERSION'], str(snap), env, 30)
        have = r['out'].decode().strip()
        if r['rc'] != 0 or not re.match(r'\d+(\.\d+)+', have):
            raise Inconclusive('ruby does not run')
        if need:
            tup = lambda s: tuple(int(x) for x in s.split('.'))
            if tup(have) < tup(need.group(1)):
                raise Inconclusive(f'system Ruby {have} < required {need.group(1)} (use --ruby-bin)')
        r = run_cmd(['bundle', '--version'], str(snap), env, 30)
        if r['rc'] != 0:
            raise Inconclusive('bundler does not run')
        r = run_cmd(['bundle', 'check'], str(snap), env, 60)
        if r['rc'] != 0:
            raise Inconclusive('bundle check failed (gems not installed; not installing): '
                               + r['out'].decode('utf-8', 'replace')[:200].replace('\n', ' '))


# ------------------------------------------------------------- sanitisation ----

ANSI = re.compile(r'\x1b\[[0-9;?]*[ -/]*[@-~]|\x1b\][^\x07]*\x07')


def sanitize(text, replacements, secrets, max_bytes, line_cap=300):
    text = ANSI.sub('', text).replace('\r\n', '\n').replace('\r', '\n')
    for old, new in sorted(replacements, key=lambda p: -len(p[0])):
        if old:
            text = text.replace(old, new)
    out, dropped, skip_next = [], 0, False
    for line in text.splitlines():
        if skip_next:
            skip_next = False
            if line.startswith((' ', '\t')):
                dropped += 1
                continue
        if re.search(r'File ".*[\\/]gate-driver[\\/]driver\.py", line', line):
            skip_next, dropped = True, dropped + 1
            continue
        s = line.strip()
        bad = (s.startswith('diff --git') or re.search(r'test\.patch|reference\.patch|/cases/|hidden', line, re.I)
               or any(sec in line for sec in secrets))
        if bad:
            dropped += 1
            continue
        out.append(line[:line_cap] + ('…' if len(line) > line_cap else ''))
    # Mark omissions compactly at the end rather than leaving gaps in the stream.
    body = re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).strip('\n')
    if dropped:
        body += f'\n[{dropped} line(s) omitted by the sanitizer]'
    data = body.encode('utf-8', 'replace')
    if len(data) > max_bytes:
        head, tail = int(max_bytes * 0.4), int(max_bytes * 0.6)
        body = (data[:head].decode('utf-8', 'ignore').rsplit('\n', 1)[0] + '\n[... output truncated ...]\n'
                + data[-tail:].decode('utf-8', 'ignore').split('\n', 1)[-1])
    return body + '\n'


# --------------------------------------------------------------------- main ----

def main(argv=None):
    ap = argparse.ArgumentParser(description='Red/green qualification of a benchmark case.')
    ap.add_argument('case', choices=sorted(CASES))
    ap.add_argument('candidate', help='base | ref | PATH of a source tree')
    ap.add_argument('--out', required=True, help='output folder (created)')
    ap.add_argument('--expect', choices=['red', 'green'], help='default: base=red, ref/PATH=green')
    ap.add_argument('--timeout', type=int, help='test-command timeout in seconds (per-case default)')
    ap.add_argument('--max-diag-bytes', type=int, default=6000)
    ap.add_argument('--cases-root', default=str(HERE / 'cases'))
    ap.add_argument('--work-root', help='parent directory for the disposable snapshot')
    ap.add_argument('--keep-snapshot', action='store_true')
    ap.add_argument('--cargo-home')
    ap.add_argument('--rustup-home')
    ap.add_argument('--rust-bin', help='directory containing cargo and rustc')
    ap.add_argument('--rust-toolchain')
    ap.add_argument('--cargo-target-dir', help='shared target dir (default: inside the snapshot)')
    ap.add_argument('--ruby-bin', help='directory with a Ruby >= required, bundle')
    ap.add_argument('--env', action='append', metavar='K=V', help='extra environment for the test command')
    args = ap.parse_args(argv)

    spec = CASES[args.case]
    cases_root = Path(args.cases_root).resolve()
    case_dir = cases_root / args.case
    base = case_dir / 'base'
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    out = out.resolve()
    expect = args.expect or ('red' if args.candidate == 'base' else 'green')
    timeout = args.timeout or spec['timeout']

    if args.candidate in ('base', 'ref'):
        label = args.candidate
        source = base
    else:
        source = Path(args.candidate).resolve()
        label = str(source)
        if not source.is_dir():
            print(f'qualify: candidate {args.candidate} is not a directory', file=sys.stderr)
            return 2
    if not base.is_dir():
        print(f'qualify: {base} missing', file=sys.stderr)
        return 2

    result = dict(case=args.case, candidate=label, expect=expect, started=time.strftime('%Y-%m-%dT%H:%M:%S%z'),
                  timeout_s=timeout, command=spec['cmd'] and list(spec['cmd']), cwd=spec['cwd'])
    raw_path, diag_path = out / 'raw.log', out / 'diagnostic.txt'
    raw_path.write_bytes(b'')
    tmp_parent = Path(tempfile.mkdtemp(prefix='qualify-', dir=args.work_root))
    snap = tmp_parent / 'snap'
    snap.mkdir()
    (tmp_parent / 'tmp').mkdir()
    replacements = []
    secrets = set()
    text, rc, timed_out, elapsed = '', None, False, 0.0
    t_total = now()
    try:
        try:
            t0 = now()
            clone_tree(source, snap)
            result['copy_s'] = round(now() - t0, 3)
            if args.candidate not in ('base', 'ref') and spec.get('deps'):
                for d in spec['deps']:
                    if not (snap / d).exists() and (base / d).exists():
                        (snap / d).parent.mkdir(parents=True, exist_ok=True)
                        run_cmd(['cp', '-cR' if sys.platform == 'darwin' else '-R', str(base / d), str(snap / d)],
                                None, os.environ.copy(), UTIL_TIMEOUT)
                        result.setdefault('deps_from_base', []).append(d)
            ctx = dict(case=args.case, test_text='', test_files=[])
            if spec['patched']:
                ctx['test_files'], ctx['test_text'] = overlay_tests(case_dir, base, snap)
                ref_text = ''
                if args.candidate == 'ref':
                    git_apply(case_dir / 'fix.patch', snap)
                    ref_text = (case_dir / 'fix.patch').read_text()
                secrets = patch_content_lines(ctx['test_text'], (case_dir / 'fix.patch').read_text()
                                              if (case_dir / 'fix.patch').is_file() else ref_text)
                result['test_files'] = ctx['test_files']
            elif args.candidate == 'ref':
                clone_tree(case_dir / 'ref', snap)
                for pyc in snap.rglob('__pycache__'):
                    shutil.rmtree(pyc, ignore_errors=True)
            env = build_env(spec, args, snap, tmp_parent / 'tmp')
            if spec['kind'] == 'crane':
                target = snap / 'tools' / 'wpt_progress.py'
                if not target.is_file():
                    raise Inconclusive('tools/wpt_progress.py missing in the candidate')
                gate = tmp_parent / 'gate-driver'
                gate.mkdir()
                (gate / 'driver.py').write_text(STREAMS_DRIVER)
                cmd, cwd = [sys.executable, '-I', str(gate / 'driver.py'), str(target)], str(tmp_parent / 'tmp')
                replacements.append((str(gate), '<gate>'))
            else:
                precheck(spec, args, snap, env, base)
                cmd, cwd = list(spec['cmd']), str(snap / spec['cwd'])
            result['command'] = [c if c != str(target) else 'tools/wpt_progress.py' for c in cmd] if spec['kind'] == 'crane' else cmd
            r = run_cmd(cmd, cwd, env, timeout, raw_path=raw_path)
            rc, timed_out, elapsed = r['rc'], r['timed_out'], r['elapsed']
            if r['error']:
                raise Inconclusive('could not start command: ' + r['error'])
            text = raw_path.read_bytes().decode('utf-8', 'replace')
            if timed_out:
                judged = J('inconclusive', f'timeout after {timeout}s')
            else:
                judged = JUDGES[spec['kind']](spec, ctx, text, rc, timed_out)
        except Inconclusive as e:
            judged = J('inconclusive', str(e))
            text = raw_path.read_text(errors='replace') if raw_path.exists() else ''
            if not text:
                raw_path.write_text(f'[harness] {e}\n')
                text = f'{e}\n'
    finally:
        for p in {str(snap), os.path.realpath(snap), str(tmp_parent), os.path.realpath(tmp_parent)}:
            replacements.append(('file://' + p + '/', 'file://./'))
            replacements.append((p + '/', ''))
            replacements.append((p, '.'))
        replacements.append((str(cases_root), '<cases>'))
        replacements.append((str(Path.home()), '~'))
        if args.keep_snapshot:
            result['snapshot'] = str(snap)
        else:
            shutil.rmtree(tmp_parent, ignore_errors=True)

    # Controls must show the *intended* behaviour; an unattributable red is not usable.
    verdict, intended = judged['verdict'], judged['intended']
    if verdict == 'red' and args.candidate in ('base', 'ref') and not intended:
        judged = dict(judged, verdict='inconclusive',
                      reason='control red is not attributable to the intended behaviour: ' + judged['reason'])
        verdict = 'inconclusive'
    accepted = verdict == expect and (verdict != 'red' or args.candidate not in ('base', 'ref') or intended is True)
    result.update(verdict=verdict, intended=intended, accepted=accepted, reason=judged['reason'],
                  evidence=judged['evidence'], hidden_tests=judged['hidden'], exit=rc, timed_out=timed_out,
                  elapsed_s=round(elapsed, 3), total_s=round(now() - t_total, 3), raw_log=str(raw_path),
                  diagnostic=str(diag_path))
    if 'tolerated' in judged:
        result['tolerated_env_failures'] = judged['tolerated']
    header = (f'case: {args.case}  candidate: {args.candidate if args.candidate in ("base", "ref") else "tree"}\n'
              f'verdict: {verdict}  exit: {rc if not timed_out else "timeout"}  elapsed: {elapsed:.1f}s\n---\n')
    diag_path.write_text(header + sanitize(text, replacements, secrets, args.max_diag_bytes))
    (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(f'{args.case} {args.candidate}: verdict={verdict} intended={intended} expect={expect} '
          f'accepted={accepted} exit={rc} elapsed={elapsed:.1f}s :: {judged["reason"]}')
    if accepted:
        return 0
    return 2 if verdict == 'inconclusive' else 1


if __name__ == '__main__':
    sys.exit(main())
