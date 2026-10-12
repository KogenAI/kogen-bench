"""Linux lane mounts and admission. No infrastructure or network operations."""
import os
import platform
import subprocess
import contextlib
import fcntl
from pathlib import Path

PROFILE = Path('/benchmark-root/kits/current/reproduce/sandbox-profile.sh')


@contextlib.contextmanager
def linux_gap_lock():
    if platform.system()!='Linux':raise RuntimeError('Linux execution only')
    # Same lock as bench-run-lane: prevents admission racing a measured launch.
    with Path('/benchmark-root/launch.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        require_linux_gap()
        yield


def require_linux_gap():
    if platform.system()!='Linux':
        raise RuntimeError('Linux scoring/validation only; no Mac execution path')
    proc=subprocess.run(['systemctl','list-units','--type=service','--state=running',
                         '--no-legend','bench-*.service'],capture_output=True,text=True,check=True)
    if proc.stdout.strip():
        raise RuntimeError('a measured benchmark unit is running; wait for a scoring gap')


def grade_prefix(repo, taskdir):
    if not PROFILE.is_file():raise RuntimeError('existing lane grading wrapper missing')
    return [str(PROFILE),'grade',str(repo),str(taskdir),'--']


def acceptance_prefix(repo):
    """Whitelist mounts; /work/bin is read-only even when tests run as host root."""
    if platform.system()!='Linux':raise RuntimeError('acceptance isolation requires Linux bwrap')
    repo=Path(repo).resolve()
    return ['/usr/bin/bwrap','--unshare-user','--unshare-pid','--unshare-ipc','--unshare-uts',
            '--unshare-net','--cap-drop','ALL','--die-with-parent','--new-session','--proc','/proc','--dev','/dev',
            '--tmpfs','/tmp','--dir','/tmp/bench-home','--tmpfs','/run','--tmpfs','/var',
            '--symlink','../tmp','/var/tmp','--dir','/benchmark-root',
            '--ro-bind','/usr','/usr','--ro-bind','/etc','/etc','--ro-bind','/opt/bench','/opt/bench',
            '--ro-bind','/benchmark-root/toolchains','/benchmark-root/toolchains',
            '--symlink','usr/bin','/bin','--symlink','usr/sbin','/sbin',
            '--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64',
            '--ro-bind',str(repo),'/work','--bind',str(repo/'acceptance'),'/work/acceptance',
            '--ro-bind',str(repo/'bin'),'/work/bin','--chdir','/work','--']


def mapped_args(args, repo, prefix):
    if '/usr/bin/bwrap' not in prefix:return args
    root=str(Path(repo).resolve())
    return [str(x).replace(root,'/work') for x in args]
