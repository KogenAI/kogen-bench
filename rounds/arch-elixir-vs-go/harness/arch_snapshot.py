"""Copy under the sampled writer barrier; retain runnable Elixir build output."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import stat
import time
from arch_config import SNAPSHOT_EXCLUDES, dump
from arch_fs import safe_chmod, _guarded_path

def inventory(root, excludes=SNAPSHOT_EXCLUDES):
    root = Path(root).resolve()
    result = []
    for base, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in excludes)
        for name in sorted(files + [d for d in dirs if (Path(base) / d).is_symlink()]):
            if name in excludes:
                continue
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if path.is_symlink():
                target = path.resolve(strict=True)
                if target != root and root not in target.parents:
                    raise ValueError('Snapshot link escapes workspace: ' + rel)
                if os.path.isabs(os.readlink(path)):
                    raise ValueError('Snapshot link must be relocatable: ' + rel)
                value, kind = os.readlink(path).encode(), 'link'
                link_count = None
            elif stat.S_ISREG(info.st_mode):
                value, kind = path.read_bytes(), 'executable' if info.st_mode & 0o111 else 'file'
                link_count = info.st_nlink
            else:
                raise ValueError('Unsupported snapshot entry: ' + rel)
            result.append([rel, kind, hashlib.sha256(value).hexdigest(), link_count])
    return sorted(result)

def tree_hash(root, excludes=SNAPSHOT_EXCLUDES):
    content_inventory = [row[:3] for row in inventory(root, excludes)]
    return hashlib.sha256(json.dumps(content_inventory, separators=(',', ':')).encode()).hexdigest()

def capture(source, destination, barrier, label, phase):
    source, destination = Path(source), Path(destination)
    if destination.exists():
        raise ValueError('Snapshot already exists: ' + str(destination))
    started = time.monotonic()
    with barrier() as proof:
        before = tree_hash(source)
        source_manifest = inventory(source)
        shutil.copytree(source, destination, symlinks=True,
                        ignore=lambda directory, names: [n for n in names if n in SNAPSHOT_EXCLUDES])
        if tree_hash(destination) != before or tree_hash(source) != before:
            raise RuntimeError('Source changed during sampled writer barrier')
        # Record source hash before making the capture read-only; executable bits remain.
        for base, dirs, files in os.walk(destination, followlinks=False):
            for name in files:
                path = Path(base) / name
                if not path.is_symlink():
                    safe_chmod(destination, path, path.stat().st_mode & ~0o222)
            safe_chmod(destination, Path(base), 0o555)
    receipt = dict(label=label, phase=phase, source_hash=before, root=str(destination),
                   started_monotonic=started, completed_monotonic=time.monotonic(),
                   immutable=True, barrier=proof,
                   exclusions=sorted(SNAPSHOT_EXCLUDES),
                   hardlink_counts={row[0]: row[3] for row in source_manifest
                                    if row[1] in ('file', 'executable') and row[3] > 1},
                   runtime_build_output_retained=True)
    dump(destination.parent / (destination.name + '.capture.json'), receipt)
    return receipt

def writable_copy(source, destination):
    shutil.copytree(source, destination, symlinks=True)
    for base, dirs, files in os.walk(destination, followlinks=False):
        safe_chmod(destination, Path(base), 0o755)
        for name in files:
            path = Path(base) / name
            if not path.is_symlink():
                safe_chmod(destination, path, path.stat().st_mode | 0o200)

def copy_reference_snapshot(source, destination, allowed_roots):
    """Copy a sealed reference snapshot after strict source/root and symlink checks."""
    source = Path(os.path.abspath(source))
    allowed = [Path(root).resolve(strict=True) for root in allowed_roots]
    if not any(_is_under(source, root) for root in allowed):
        raise ValueError('Reference snapshot is outside allowed roots')
    # Reject symlinks in the source path itself, then validate all links inside it.
    valid_root = next(root for root in allowed if _is_under(source, root))
    _guarded_path(valid_root, source)
    if not source.is_dir():
        raise ValueError('Reference snapshot is not a directory')
    expected = tree_hash(source)
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise ValueError('Reference snapshot destination already exists')
    shutil.copytree(source, destination, symlinks=True)
    if tree_hash(destination) != expected:
        raise RuntimeError('Reference snapshot changed while copying')
    for base, dirs, files in os.walk(destination, followlinks=False):
        for name in files:
            path = Path(base) / name
            if not path.is_symlink():
                safe_chmod(destination, path, path.stat().st_mode & ~0o222)
        safe_chmod(destination, Path(base), 0o555)
    return dict(source_path=str(source), sha256=expected, root=str(destination), immutable=True)

def _is_under(path, root):
    try:
        Path(path).relative_to(Path(root))
        return True
    except ValueError:
        return False
