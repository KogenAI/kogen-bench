"""Root-confined filesystem permission and removal helpers."""
import os
from pathlib import Path
import shutil
import stat


def _guarded_path(root, path, allow_missing=False):
    root = Path(root).resolve(strict=True)
    raw = Path(path)
    if '..' in raw.parts:
        raise ValueError('Refusing path with parent traversal: ' + str(path))
    candidate = raw if raw.is_absolute() else root / raw
    candidate = Path(os.path.abspath(candidate))
    try:
        relative = candidate.relative_to(root)
    except ValueError as error:
        raise ValueError('Path is outside target root: ' + str(candidate)) from error

    resolved = candidate.resolve(strict=not allow_missing)
    if resolved != root and root not in resolved.parents:
        raise ValueError('Path resolves outside target root: ' + str(candidate))

    current = root
    for part in relative.parts:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            if allow_missing:
                break
            raise
        if stat.S_ISLNK(info.st_mode):
            raise ValueError('Refusing symlink path: ' + str(current))
    return candidate


def safe_chmod(root, path, mode):
    """Change mode only for a non-symlink path contained by root."""
    candidate = _guarded_path(root, path)
    os.chmod(candidate, mode, follow_symlinks=False)


def safe_rmtree(root, path, ignore_errors=False):
    """Remove a real directory tree after enforcing the same root boundary."""
    if not shutil.rmtree.avoids_symlink_attacks:
        raise RuntimeError('Safe recursive removal is unavailable on this platform')
    candidate = _guarded_path(root, path, allow_missing=True)
    if not candidate.exists():
        return
    if not candidate.is_dir():
        raise ValueError('Refusing to recursively remove a non-directory: ' + str(candidate))
    shutil.rmtree(candidate, ignore_errors=ignore_errors)
