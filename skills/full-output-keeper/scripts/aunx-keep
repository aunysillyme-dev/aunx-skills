#!/usr/bin/env python3
"""Run commands with a bounded display and a seven-day full-output cache."""

import argparse
from collections import deque
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time
import uuid


RETENTION = 7 * 24 * 60 * 60
ID_PATTERN = re.compile(r"[0-9a-f]{32}")


def cache_dir(create=False):
    root = Path(os.environ.get("AUNX_KEEP_CACHE") or
                str(Path(os.environ.get("XDG_CACHE_HOME", "~/.cache")).expanduser() / "aunx-keep"))
    root = root.expanduser()
    if create:
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not root.exists():
        return root
    info = root.lstat()
    if not stat.S_ISDIR(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o700:
        raise OSError("cache directory must be a real directory with mode 0700")
    if hasattr(os, "getuid") and info.st_uid != os.getuid():
        raise OSError("cache directory must be owned by the current user")
    return root


def private_open(path, write=False):
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL if write else os.O_RDONLY
    fd = os.open(path, flags | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        info = os.fstat(fd)
        if (not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600
                or info.st_nlink != 1):
            raise OSError("cache entry must be a private regular file")
        if hasattr(os, "getuid") and info.st_uid != os.getuid():
            raise OSError("cache entry must be owned by the current user")
        return os.fdopen(fd, "wb" if write else "rb")
    except BaseException:
        os.close(fd)
        raise


def prune(root):
    cutoff = time.time() - RETENTION
    for path in root.iterdir():
        if not re.fullmatch(r"[0-9a-f]{32}\.(log|json|part)", path.name):
            continue
        info = path.lstat()
        if stat.S_ISREG(info.st_mode) and info.st_mtime < cutoff:
            path.unlink()


def nonnegative(value):
    result = int(value)
    if result < 0:
        raise argparse.ArgumentTypeError("use a nonnegative integer")
    return result


def emit(data):
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()


def bounded_view(path, limit, budget, tail):
    chosen = deque()
    size = 0
    with private_open(path) as stream:
        for number, line in enumerate(stream, 1):
            if not tail and (len(chosen) == limit or size + len(line) > budget):
                break
            chosen.append((number, line))
            size += len(line)
            if tail:
                while chosen and (len(chosen) > limit or size > budget):
                    size -= len(chosen.popleft()[1])
    return chosen, size


def run(args, command):
    root = cache_dir(create=True)
    prune(root)
    ident = uuid.uuid4().hex
    part = root / (ident + ".part")
    count = size = 0
    last = b""
    capture_error = None
    rc = None
    try:
        with private_open(part, write=True) as output:
            try:
                child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except OSError as exc:
                print(f"aunx-keep: command did not start: {exc}", file=sys.stderr)
                return 127 if isinstance(exc, FileNotFoundError) else 126
            with child:
                for chunk in iter(lambda: child.stdout.read(65536), b""):
                    size += len(chunk)
                    count += chunk.count(b"\n")
                    last = chunk[-1:]
                    if capture_error is None:
                        try:
                            output.write(chunk)
                        except OSError as exc:
                            capture_error = exc
                rc = child.wait()
                rc = 128 - rc if rc < 0 else rc
            if capture_error is None:
                try:
                    output.flush()
                except OSError as exc:
                    capture_error = exc
        if capture_error is not None:
            print(f"aunx-keep: capture incomplete: {capture_error}; command exit {rc}; no retrieval id", file=sys.stderr)
            return rc
        count += int(bool(size) and last != b"\n")
        completed = root / (ident + ".log")
        part.rename(completed)
        with private_open(root / (ident + ".json"), write=True) as metadata:
            metadata.write(json.dumps({"created": time.time(), "exit": rc, "bytes": size,
                                       "lines": count}).encode("utf-8"))
        view, shown_size = bounded_view(completed, args.tail if args.tail is not None else args.head,
                                       args.max_bytes, args.tail is not None)
        try:
            for _, line in view:
                # Reserve the helper's last line as its only authoritative footer.
                emit(b"(command output) " + line if line.startswith(b"[aunx-keep ") else line)
            if view and not view[-1][1].endswith(b"\n"):
                emit(b"\n")
            first, final = (view[0][0], view[-1][0]) if view else (0, 0)
            emit(f"[aunx-keep {ident}: lines {first}-{final} of {count}; {shown_size} of {size} bytes; exit {rc}; retrieve: aunx-keep read {ident}]\n".encode())
        except BrokenPipeError:
            # Keep the child's status authoritative even when the display closes.
            sys.stdout = open(os.devnull, "w")
        return rc
    except OSError as exc:
        if rc is None:
            raise
        print(f"aunx-keep: output storage/display failed: {exc}; command exit {rc}; retrieval may be unavailable", file=sys.stderr)
        return rc
    finally:
        if part.exists():
            part.unlink()


def read_output(args):
    if not ID_PATTERN.fullmatch(args.id):
        raise ValueError("id must be the 32 hexadecimal characters printed by a run")
    root = cache_dir()
    try:
        with private_open(root / (args.id + ".json")) as stream:
            metadata = json.load(stream)
    except FileNotFoundError:
        print("aunx-keep: retrieval id not found", file=sys.stderr)
        return 3
    if metadata["created"] < time.time() - RETENTION:
        print("aunx-keep: retrieval id expired (seven-day retention)", file=sys.stderr)
        return 3
    pattern = re.compile(args.grep.encode(), re.I if args.ignore_case else 0) if args.grep else None
    start, end = args.lines or (1, float("inf"))
    with private_open(root / (args.id + ".log")) as stream:
        if args.lines is None and pattern is None:
            for chunk in iter(lambda: stream.read(65536), b""):
                emit(chunk)
        else:
            for number, line in enumerate(stream, 1):
                if number > end:
                    break
                if number >= start and (pattern is None or pattern.search(line.rstrip(b"\n"))):
                    emit(str(number).encode() + b":" + line if pattern else line)
    return 0


def line_range(value):
    if not re.fullmatch(r"[1-9][0-9]*:[1-9][0-9]*", value):
        raise argparse.ArgumentTypeError("use an inclusive line range such as 10:20")
    start, end = map(int, value.split(":"))
    if start > end:
        raise argparse.ArgumentTypeError("range start must not exceed its end")
    return start, end


def main():
    argv = sys.argv[1:]
    if argv and argv[0] == "read":
        parser = argparse.ArgumentParser(prog="aunx-keep read")
        parser.add_argument("id")
        parser.add_argument("--lines", type=line_range)
        parser.add_argument("--grep")
        parser.add_argument("-i", "--ignore-case", action="store_true")
        return read_output(parser.parse_args(argv[1:]))
    parser = argparse.ArgumentParser(description=__doc__, prog="aunx-keep")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--head", type=nonnegative, default=40)
    group.add_argument("--tail", type=nonnegative)
    parser.add_argument("--max-bytes", type=nonnegative, default=12000)
    parser.add_argument("-c", dest="shell", help="run a string with the POSIX shell")
    split = argv.index("--") if "--" in argv else len(argv)
    args = parser.parse_args(argv[:split])
    direct = argv[split + 1:] if split < len(argv) else None
    if (args.shell is None) == (direct is None) or direct == []:
        parser.error("use -c STRING or -- COMMAND ARGUMENTS")
    return run(args, ["/bin/sh", "-c", args.shell] if args.shell is not None else direct)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, re.error) as exc:
        print(f"aunx-keep: {exc}", file=sys.stderr)
        sys.exit(1)
