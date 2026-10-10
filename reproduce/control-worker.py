#!/usr/bin/env python3
"""Grade only fresh reference and no-op worktrees; print aggregate verdicts."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import time


COPY_MAX_BYTES = 2 * 1024**3
COPY_TIMEOUT_SECONDS = 120
BUILD_CACHE_DIRS = {"target", "_build", "build"}


class CandidateCopyError(RuntimeError):
    pass


def copy_candidate_tree(source, target, max_bytes=COPY_MAX_BYTES,
                        timeout_seconds=COPY_TIMEOUT_SECONDS):
    """Copy a candidate without following links or copying special files."""
    deadline = time.monotonic() + timeout_seconds
    total = 0

    def check_time():
        if time.monotonic() > deadline:
            raise CandidateCopyError(f"copy exceeded {timeout_seconds} second limit")

    source_fd = target_fd = None
    try:
        source_fd = os.open(os.fspath(source), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        os.mkdir(target, 0o700)
        target_fd = os.open(target, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)

        def copy_dir(src_fd, dst_fd):
            nonlocal total
            check_time()
            with os.scandir(src_fd) as entries:
                for entry in entries:
                    check_time()
                    name = entry.name
                    if name == ".git":
                        continue
                    try:
                        mode = entry.stat(follow_symlinks=False).st_mode
                    except FileNotFoundError:
                        continue
                    if name in BUILD_CACHE_DIRS and (stat.S_ISDIR(mode) or stat.S_ISLNK(mode)):
                        continue
                    if stat.S_ISLNK(mode):
                        link = os.readlink(name, dir_fd=src_fd)
                        total += len(os.fsencode(link))
                        if total > max_bytes:
                            raise CandidateCopyError(f"copy exceeded {max_bytes} byte limit")
                        os.symlink(link, name, dir_fd=dst_fd)
                    elif stat.S_ISDIR(mode):
                        os.mkdir(name, 0o700, dir_fd=dst_fd)
                        child_src = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                            dir_fd=src_fd)
                        child_dst = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                            dir_fd=dst_fd)
                        try:
                            copy_dir(child_src, child_dst)
                        finally:
                            os.close(child_src)
                            os.close(child_dst)
                        os.chmod(name, stat.S_IMODE(mode), dir_fd=dst_fd, follow_symlinks=False)
                    elif stat.S_ISREG(mode):
                        src_file = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                                           dir_fd=src_fd)
                        try:
                            info = os.fstat(src_file)
                            if not stat.S_ISREG(info.st_mode):
                                continue
                            if total + info.st_size > max_bytes:
                                raise CandidateCopyError(f"copy exceeded {max_bytes} byte limit")
                            dst_file = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                               0o600, dir_fd=dst_fd)
                            try:
                                while True:
                                    check_time()
                                    block = os.read(src_file, 1024 * 1024)
                                    if not block:
                                        break
                                    total += len(block)
                                    if total > max_bytes:
                                        raise CandidateCopyError(f"copy exceeded {max_bytes} byte limit")
                                    view = memoryview(block)
                                    while view:
                                        written = os.write(dst_file, view)
                                        view = view[written:]
                                os.fchmod(dst_file, stat.S_IMODE(info.st_mode))
                            finally:
                                os.close(dst_file)
                        finally:
                            os.close(src_file)
                    # FIFOs, sockets, devices and other special entries are omitted.
                    check_time()

        copy_dir(source_fd, target_fd)
        check_time()
        return total
    except CandidateCopyError:
        raise
    except Exception as exc:
        raise CandidateCopyError(f"copy failed: {exc}") from exc
    finally:
        if target_fd is not None:
            os.close(target_fd)
        if source_fd is not None:
            os.close(source_fd)


def copy_error_record(task_id, reason):
    return {"task": task_id, "pass_": False, "stage": "copy-error",
            "reason": str(reason)[:500]}


def run(argv, **kwargs):
    return subprocess.run(argv, check=True, **kwargs)


def sandbox(task_dir: Path, work: Path, log_path=None):
    profile = Path(__file__).with_name("sandbox-profile.sh")
    env = {**os.environ, "HOME": "/tmp/home", "PYTHONDONTWRITEBYTECODE": "1",
           "PATH": "/srv/bh/bench/toolchains/go-1.27.1/bin:"
                   "/srv/bh/bench/toolchains/rust-1.97.1/bin:"
                   "/srv/bh/bench/toolchains/bun-1.4.2/bin:"
                   "/srv/bh/bench/toolchains/gleam-1.18.1/bin:"
                   "/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:"
                   "/opt/bench/mise/installs/erlang/29.0.3/bin:"
                   "/opt/bench/mise/installs/node/24.20.0/bin:"
                   "/opt/bench/mise/installs/ruby/3.4.8/bin:"
                   "/srv/bh/bench/toolchains/python-3.14.7/bin:/usr/bin:/bin",
           "PYTHONPATH": "/srv/bh/bench/toolchains/python-3.14.7/lib/python3.14/site-packages",
           "RUSTUP_HOME": "/opt/bench/rustup", "CARGO_NET_OFFLINE": "true",
           "GOTOOLCHAIN": "local", "GOPROXY": "off"}
    proc = subprocess.run([str(profile), "grade", str(work), str(task_dir), "--",
                           "/bin/bash", "/task/hidden/grade.sh", "/work"],
                          env=env, capture_output=True, text=True, timeout=1200)
    if log_path is not None:
        log_path.write_text(proc.stdout + "\n--- stderr ---\n" + proc.stderr)
    verdict = None
    for line in reversed(proc.stdout.splitlines()):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict) and ("pass_" in record or "pass" in record):
            verdict = bool(record.get("pass_", record.get("pass")))
            break
    if verdict is None or proc.returncode not in (0, 1):
        raise RuntimeError(f"grader infrastructure failure (rc={proc.returncode})")
    return verdict


def reference_root(reference: Path) -> Path:
    """Return the shallowest directory of a published reference tree that holds its Makefile."""
    if reference.is_symlink():
        raise RuntimeError("reference tree root is a symlink")
    if (reference / "Makefile").is_file() and not (reference / "Makefile").is_symlink():
        return reference
    def safe_makefile(makefile: Path) -> bool:
        if makefile.is_symlink():
            return False
        cursor = makefile.parent
        while cursor != reference:
            if cursor.is_symlink():
                return False
            cursor = cursor.parent
        return not reference.is_symlink()

    found = sorted((p.parent for p in reference.glob("*/Makefile") if safe_makefile(p)), key=str) or \
        sorted((p.parent for p in reference.glob("*/*/Makefile") if safe_makefile(p)), key=str)
    if len(found) != 1:
        raise RuntimeError("reference tree has no unique Makefile root")
    return found[0]


def copy_reference(source: Path, work: Path):
    """Overlay reference files onto the base checkout without the kit's root-only modes."""
    for item in sorted(source.rglob("*")):
        if item.is_symlink():
            raise RuntimeError("reference tree contains a symlink")
        rel = item.relative_to(source)
        if ".git" in rel.parts:
            continue
        target = work / rel
        cursor = target
        unsafe = False
        while cursor == target or cursor != work.parent:
            if cursor.is_symlink():
                unsafe = True
                break
            cursor = cursor.parent
        if unsafe or not target.resolve().is_relative_to(work.resolve()):
            raise RuntimeError("reference target escapes work tree")
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(item, target)
            with item.open("rb") as handle:
                executable = handle.read(2) == b"#!"
            os.chmod(target, 0o755 if executable else 0o644)


def control(kit: Path, task_id: str):
    task = kit / "tasks" / task_id
    if not task.is_dir() or not (task / "task.json").is_file():
        raise RuntimeError("task kit unavailable")
    meta = json.loads((task / "task.json").read_text())
    bundle_name = meta.get("base_bundle")
    if not bundle_name or meta.get("base_missing"):
        raise RuntimeError("task base is not bundled")
    bundle = kit / "tasks" / bundle_name
    digest = hashlib.sha256(bundle.read_bytes()).hexdigest()
    if digest != meta["base_bundle_sha256"]:
        raise RuntimeError("task base digest mismatch")
    grader = task / "hidden" / "grade.sh"
    if not grader.is_file():
        raise RuntimeError("official hidden grader unavailable")
    reference = task / "hidden" / "sealed" / "reference"
    patch = task / "hidden" / "sealed" / "reference.patch"
    if not reference.is_dir() and not patch.is_file():
        raise RuntimeError("reference is not published")
    with tempfile.TemporaryDirectory(prefix="kogen-controls-", dir="/srv/bh/bench/work") as tmp:
        tmp = Path(tmp)
        outcomes = {}
        for variant in ("noop", "reference"):
            run(["/usr/local/bin/bench-disk-floor", "/srv/bh/bench"])
            work = tmp / variant
            run(["git", "clone", "-q", str(bundle), str(work)])
            run(["git", "-C", str(work), "checkout", "-q", meta["base_sha"]])
            if variant == "reference":
                if patch.is_file():
                    run(["git", "-C", str(work), "apply", "--whitespace=nowarn", str(patch)])
                else:
                    copy_reference(reference_root(reference), work)
            log_path = None
            keep = os.environ.get("KOGEN_CONTROLS_KEEP")
            if keep:  # opt-in diagnostics: root-only, host-local; never copied off-host or printed
                log_dir = Path(keep) / task_id / variant
                log_dir.mkdir(parents=True, exist_ok=True)
                for part in (Path(keep), Path(keep) / task_id, log_dir):
                    os.chmod(part, 0o700)
                log_path = log_dir / "grader.log"
            outcomes[variant] = sandbox(task, work, log_path)
            if log_path is not None:
                os.chmod(log_path, 0o600)
        return outcomes


def main():
    kit = Path(sys.argv[1]).resolve()
    if sys.argv[2] == "grade-candidate":
        task_id = sys.argv[3]
        task = kit / "tasks" / task_id
        result = Path(sys.argv[5]).resolve()
        temp_root = Path(sys.argv[6]) if len(sys.argv) > 6 else Path("/srv/bh/bench/work")
        with tempfile.TemporaryDirectory(prefix="kogen-grade-", dir=temp_root) as tmp:
            work = Path(tmp) / "candidate"
            try:
                copy_candidate_tree(sys.argv[4], work)
            except CandidateCopyError as exc:
                record = copy_error_record(task_id, exc)
                (result / "grader.log").write_text(f"copy-error: {record['reason']}\n")
                (result / "grade.json").write_text(json.dumps(record) + "\n")
                print(json.dumps({"task": task_id, "grade_pass": False,
                                  "stage": "copy-error", "reason": record["reason"]}))
                return 1
            passed = sandbox(task, work, result / "grader.log")
        counts = {}
        for line in (result / "grader.log").read_text().splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict) and ("pass_" in record or "pass" in record):
                counts = {k: record[k] for k in ("tests", "failures", "errors", "skipped", "tests_ran") if k in record}
        (result / "grade.json").write_text(json.dumps({"task": task_id, "pass_": passed, **counts}) + "\n")
        print(json.dumps({"task": task_id, "grade_pass": passed}))
        return 0 if passed else 1
    failed = False
    for task_id in sys.argv[2:]:
        try:
            result = control(kit, task_id)
            admitted = result["reference"] and not result["noop"]
            print(json.dumps({"task": task_id, "reference_pass": result["reference"],
                              "noop_fail": not result["noop"], "admitted": admitted}), flush=True)
            failed |= not admitted
        except (OSError, KeyError, ValueError, RuntimeError, subprocess.CalledProcessError,
                subprocess.TimeoutExpired) as exc:
            print(json.dumps({"task": task_id, "admitted": False,
                              "error": str(exc)[:180]}), flush=True)
            failed = True
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
