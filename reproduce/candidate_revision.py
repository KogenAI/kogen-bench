#!/usr/bin/env python3
"""Read a work tree's commit pointer without invoking Git on agent-controlled data."""
from __future__ import annotations
import os
import re
import stat
import sys

NOFOLLOW = getattr(os, 'O_NOFOLLOW', 0)
NONBLOCK = getattr(os, 'O_NONBLOCK', 0)
DIRECTORY = getattr(os, 'O_DIRECTORY', 0)
MAX_BYTES = 1024 * 1024
COMMIT = re.compile(rb'[0-9a-f]{40}\Z')
REF = re.compile(rb'ref: (refs/[A-Za-z0-9._/-]+)\Z')
UNSAFE = object()


def read_regular_at(directory_fd: int, name: str) -> bytes | None:
    fd = None
    try:
        fd = os.open(name, os.O_RDONLY | NOFOLLOW | NONBLOCK, dir_fd=directory_fd)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
            return UNSAFE
        chunks = bytearray()
        while True:
            block = os.read(fd, min(65536, MAX_BYTES + 1 - len(chunks)))
            if not block:
                break
            chunks.extend(block)
            if len(chunks) > MAX_BYTES:
                return UNSAFE
        return bytes(chunks).strip()
    except FileNotFoundError:
        return None
    except OSError:
        return UNSAFE
    finally:
        if fd is not None:
            os.close(fd)


def open_directory_at(directory_fd: int, name: str) -> int | None:
    try:
        fd = os.open(name, os.O_RDONLY | DIRECTORY | NOFOLLOW | NONBLOCK,
                     dir_fd=directory_fd)
        if stat.S_ISDIR(os.fstat(fd).st_mode):
            return fd
        os.close(fd)
        return UNSAFE
    except FileNotFoundError:
        return None
    except OSError:
        return UNSAFE


def read_ref(git_fd: int, ref: bytes) -> bytes | None:
    parts = ref.decode('ascii').split('/')
    if (len(parts) < 3 or parts[0] != 'refs'
            or any(part in ('', '.', '..') or part.startswith('.')
                   or part.endswith('.lock') for part in parts)):
        return None
    current = os.dup(git_fd)
    try:
        for part in parts[:-1]:
            child = open_directory_at(current, part)
            if child is None:
                break
            if child is UNSAFE:
                return None
            os.close(current)
            current = child
        else:
            value = read_regular_at(current, parts[-1])
            if value is UNSAFE:
                return None
            if value is not None:
                return value if COMMIT.fullmatch(value) else None
    finally:
        os.close(current)
    packed = read_regular_at(git_fd, 'packed-refs')
    if packed is None or packed is UNSAFE:
        return None
    for line in packed.splitlines():
        fields = line.split()
        if len(fields) == 2 and fields[1] == ref and COMMIT.fullmatch(fields[0]):
            return fields[0]
    return None


def read_head(repository: str | os.PathLike[str]) -> str | None:
    root_fd = git_fd = None
    try:
        root_fd = os.open(repository, os.O_RDONLY | DIRECTORY | NOFOLLOW | NONBLOCK)
        git_fd = open_directory_at(root_fd, '.git')
        if git_fd is None or git_fd is UNSAFE:
            return None
        head = read_regular_at(git_fd, 'HEAD')
        if not head or head is UNSAFE:
            return None
        if COMMIT.fullmatch(head):
            return head.decode('ascii')
        match = REF.fullmatch(head)
        if not match:
            return None
        value = read_ref(git_fd, match.group(1))
        return value.decode('ascii') if value else None
    except OSError:
        return None
    finally:
        if isinstance(git_fd, int):
            os.close(git_fd)
        if root_fd is not None:
            os.close(root_fd)


if __name__ == '__main__':
    revision = read_head(sys.argv[1]) if len(sys.argv) == 2 else None
    if revision:
        print(revision)
