#!/usr/bin/env python3
"""macOS fixture actions for CMP-MAC.

Stdout is diagnostic only. cmp_mac.py scores runner-owned witnesses and its own
process observer. Every fixture process has an independent finite lifetime:
its own monotonic deadline plus a SIGALRM backstop (alarm survives exec, so an
exec'd survivor keeps the bound even if its loop is stalled).
"""
import errno, json, os, signal, socket, subprocess, sys, time

LIFETIME = 25.0          # seconds, per process, from that process's own start
ALARM = int(LIFETIME) + 5
SURVIVORS = ('double_fork', 'setsid', 'term_ignoring', 'leader_exit_first', 'reparent_to_init')
NOFOLLOW = getattr(os, 'O_NOFOLLOW', 0)


def bounded():
    """Start this process's own lifetime bound and return its deadline."""
    signal.alarm(ALARM)
    return time.monotonic() + LIFETIME


def emit(name, state, **fields):
    tail = ' '.join(f'{k}={v}' for k, v in fields.items())
    print(f'FIXTURE={name} OUTCOME={state}' + ((' ' + tail) if tail else ''), flush=True)


def receipt(name):
    # Runner supplies this destination under this cell's allowed directory.
    p = os.environ['CMPMAC_RECEIPT']
    flags = os.O_WRONLY | os.O_CREAT | NOFOLLOW
    try:
        fd = os.open(p, flags | os.O_EXCL, 0o600)
    except FileExistsError:
        fd = os.open(p, flags | os.O_APPEND, 0o600)
    try:
        os.write(fd, (name + '\n').encode())
    finally:
        os.close(fd)


def witness(path, data):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | NOFOLLOW, 0o600)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)


def denial(name, error):
    receipt(name + '_denied' if error.errno in (errno.EACCES, errno.EPERM) else name + '_error')


def hold(deadline, release=None):
    """Finite wait; returns early only when the runner-created release file appears."""
    while time.monotonic() < deadline:
        if release is not None and os.path.exists(release):
            return True
        time.sleep(0.1)
    return False


def exec_survivor(mode):
    """Replace this process with the survivor role; argv carries the role and marker
    so the runner's independent ps observer can identify it without fixture output."""
    argv = [sys.executable, '-I', '-S', os.path.abspath(__file__), 'survivor-child', mode,
            os.environ['CMPMAC_MARKER_TOKEN']]
    os.execv(sys.executable, argv)


def survivor_child(mode):
    # Lifetime and TERM disposition are established before READY is written.
    deadline = bounded()
    if mode == 'term_ignoring':
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
    witness(os.environ['CMPMAC_SURVIVOR_READY'],
            json.dumps({'pid': os.getpid(), 'mode': mode}).encode() + b'\n')
    emit(mode, 'READY', PID=os.getpid(), PPID=os.getppid())
    hold(deadline)
    os._exit(0)


def survivor_leader(name):
    deadline = bounded()
    if name == 'double_fork':
        child = os.fork()
        if child == 0:
            bounded()
            os.setsid()                    # leave the runner's session and group
            if os.fork():
                os._exit(0)                # intermediate exits; grandchild is reparented
            exec_survivor(name)
        os.waitpid(child, 0)
        emit(name, 'LEADER-HOLD', PID=os.getpid())
        hold(deadline)
    elif name == 'setsid':
        child = os.fork()
        if child == 0:
            bounded()
            os.setsid()                    # a non-leader child, so setsid succeeds
            exec_survivor(name)
        emit(name, 'LEADER-HOLD', PID=os.getpid())
        hold(deadline)
    elif name == 'term_ignoring':
        child = os.fork()
        if child == 0:
            bounded()
            signal.signal(signal.SIGTERM, signal.SIG_IGN)   # inherited across exec
            exec_survivor(name)
        emit(name, 'LEADER-HOLD', PID=os.getpid())
        hold(deadline)
    elif name == 'leader_exit_first':
        child = os.fork()
        if child == 0:
            bounded()
            exec_survivor(name)
        emit(name, 'LEADER-EXIT', PID=os.getpid())
        os._exit(0)
    elif name == 'reparent_to_init':
        child = os.fork()
        if child == 0:
            bounded()
            exec_survivor(name)
        # Exit only after the runner has observed PPID == this leader.
        released = hold(deadline, os.environ['CMPMAC_LEADER_RELEASE'])
        emit(name, 'LEADER-EXIT', PID=os.getpid(), RELEASED=released)
        os._exit(0)
    os._exit(0)


def main(name):
    if os.geteuid() == 0:
        raise SystemExit('refusing to run fixture as root')
    if name == 'survivor-child':
        survivor_child(sys.argv[2])
        return
    if name in SURVIVORS:
        survivor_leader(name)
        return
    bounded()
    if name == 'noop':
        return
    if name == 'fs_read_outside':
        try:
            receipt('fs_read_attempt')
            data = open(os.environ['CMPMAC_OUTSIDE_READ'], 'rb').read()
            receipt('fs_read_success')
            witness(os.environ['CMPMAC_READ_WITNESS'], data)
            emit(name, 'READ', bytes=len(data))
        except OSError as e:
            denial('fs_read', e); emit(name, 'ERROR', error=type(e).__name__)
    elif name == 'fs_write_outside':
        try:
            receipt('fs_write_attempt')
            fd = os.open(os.environ['CMPMAC_OUTSIDE_WRITE'], os.O_WRONLY | os.O_CREAT | os.O_EXCL | NOFOLLOW, 0o600)
            os.write(fd, os.environ['CMPMAC_WRITE_TOKEN'].encode()); os.close(fd); emit(name, 'WRITE')
        except OSError as e:
            denial('fs_write', e); emit(name, 'ERROR', error=type(e).__name__)
    elif name == 'secret_file':
        try:
            receipt('secret_file_attempt')
            data = open(os.environ['CMPMAC_SECRET_FILE'], 'rb').read(); receipt('secret_file_success')
            witness(os.environ['CMPMAC_SECRET_WITNESS'], data)
        except OSError as e:
            denial('secret_file', e); emit(name, 'FILE-ERROR', error=type(e).__name__)
        emit(name, 'CHECKED')
    elif name == 'env_secret':
        # The observed value itself goes to a runner-owned witness; the runner,
        # not this fixture, compares it with the planted token.
        value = os.environ.get('CMPMAC_SECRET_ENV_TOKEN')
        witness(os.environ['CMPMAC_ENV_WITNESS'],
                json.dumps({'present': value is not None, 'value': value if value is not None else ''}).encode() + b'\n')
        receipt('environment_checked')
        emit(name, 'CHECKED')
    elif name == 'env_unlisted':
        # A variable whose name nobody configured: only a general allowlist removes it.
        found = sorted(k for k in os.environ if k.startswith('CMPMAC_UNLISTED_'))
        witness(os.environ['CMPMAC_ENVLIST_WITNESS'],
                json.dumps({'present': bool(found), 'names': found, 'values': [os.environ[k] for k in found]}).encode() + b'\n')
        receipt('environment_checked')
        emit(name, 'CHECKED')
    elif name == 'fs_write_global_tmp':
        # Two targets outside every grant: the shared /private/tmp, and sandbox-runtime's own
        # /private/tmp/claude grant (its parent directory may first have to be created).
        receipt('gtmp_attempt')
        token = os.environ['CMPMAC_WRITE_TOKEN'].encode()
        for key, var in (('g', 'CMPMAC_GTMP_TARGET'), ('c', 'CMPMAC_GTMP_CLAUDE_TARGET')):
            target = os.environ[var]
            try:
                if key == 'c':
                    try: os.mkdir(os.path.dirname(target), 0o700)
                    except FileExistsError: pass
                fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | NOFOLLOW, 0o600)
                os.write(fd, token); os.close(fd); receipt('gtmp_%s_written' % key)
            except OSError as e:
                receipt('gtmp_%s_denied' % key if e.errno in (errno.EACCES, errno.EPERM) else 'gtmp_%s_error' % key)
        emit(name, 'CHECKED')
    elif name == 'net_loopback_canary':
        receipt('network_attempt')
        try:
            with socket.create_connection(('127.0.0\x2e1', int(os.environ['CMPMAC_CANARY_PORT'])), timeout=2):
                pass
            emit(name, 'CONNECTED')
        except OSError as e:
            denial('network', e); emit(name, 'CONNECT-ERROR', error=type(e).__name__)
    elif name == 'exec_disallowed':
        receipt('exec_attempt')
        try:
            p = subprocess.Popen([os.environ['CMPMAC_DISALLOWED_BINARY']], stdin=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            p.wait(timeout=2); emit(name, 'EXECUTED', returncode=p.returncode)
        except subprocess.TimeoutExpired:
            p.kill(); p.wait(); emit(name, 'EXEC-TIMEOUT')
        except OSError as e:
            denial('exec', e); emit(name, 'EXEC-ERROR', error=type(e).__name__)
    elif name == 'supervisor_signal':
        receipt('signal_attempt')
        try:
            os.kill(int(os.environ['CMPMAC_SACRIFICIAL_PID']), signal.SIGTERM); receipt('signal_sent'); emit(name, 'SIGNAL-SENT')
        except OSError as e:
            denial('signal', e); emit(name, 'SIGNAL-ERROR', error=type(e).__name__)
    else:
        raise SystemExit('unknown fixture: ' + name)
    receipt('fixture_complete')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('fixture name required')
    main(sys.argv[1])
