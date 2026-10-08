"""Published R70 subset of the operator's Linux sandbox helper.

Only base_args is required by the shared grader. Host paths are configurable
through BENCH_SYSROOT and BENCH_BWRAP for the grading host.
"""
import os


SYS_DIRS = ("usr", "bin", "sbin", "lib", "lib32", "lib64", "libx32", "etc", "opt")


def base_args(bwrap=None, net=False, sysroot=None):
    bwrap = bwrap or os.environ.get("BENCH_BWRAP", "bwrap")
    sysroot = sysroot or os.environ.get("BENCH_SYSROOT", "/")
    args = [bwrap, "--unshare-pid", "--unshare-ipc", "--unshare-uts", "--unshare-cgroup-try", "--die-with-parent", "--new-session"]
    if not net:
        args.append("--unshare-net")
    args += ["--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp", "--tmpfs", "/run", "--tmpfs", "/var", "--symlink", "../tmp", "/var/tmp"]
    for directory in SYS_DIRS:
        source = os.path.join(sysroot, directory)
        if os.path.islink(source):
            args += ["--symlink", os.readlink(source), "/" + directory]
        elif os.path.isdir(source):
            args += ["--ro-bind", source, "/" + directory]
    return args
