"""Published R70 subset of the operator dispatcher used by the grader."""
import os
import pathlib
import shlex
import subprocess


def _is_bench_run(argv):
    return (len(argv) >= 3
            and os.path.basename(argv[0]).lower().startswith("python")
            and os.path.basename(argv[1]) == "bench.py"
            and argv[2] == "run")


def active():
    """Return active benchmark runner processes, matching count_cells semantics."""
    proc = pathlib.Path(os.environ.get("BENCH_PROC_ROOT", "/proc"))
    rows = []
    if proc.is_dir():
        for entry in proc.iterdir():
            if not entry.name.isdigit():
                continue
            try:
                raw = (entry / "cmdline").read_bytes()
                argv = [part.decode("utf-8", "replace") for part in raw.split(b"\0") if part]
            except OSError:
                continue
            if _is_bench_run(argv):
                rows.append((int(entry.name), argv))
        return rows
    try:
        output = subprocess.check_output(["ps", "-ww", "-axo", "pid=,command="], text=True)
    except (OSError, subprocess.CalledProcessError):
        return rows
    for line in output.splitlines():
        fields = line.strip().split(None, 1)
        if len(fields) != 2 or not fields[0].isdigit():
            continue
        try:
            argv = shlex.split(fields[1])
        except ValueError:
            continue
        if _is_bench_run(argv):
            rows.append((int(fields[0]), argv))
    return rows
