#!/usr/bin/env python3
"""Package one installable zip per skill using only the Python standard library."""
import argparse
import re
import stat
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def pack_files(folder):
    files = [folder / "SKILL.md", folder / "LICENSE.txt"]
    for name in ("references", "scripts"):
        files.extend(p for p in (folder / name).rglob("*") if p.is_file()
                     and not any(x in {"__pycache__", ".DS_Store"} for x in p.parts))
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="1.0.0")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[a-zA-Z0-9.-]+)?", args.version):
        parser.error("version must be a semantic version such as 1.0.0")
    output = args.output.resolve()
    if ROOT not in output.parents:
        parser.error("output must be inside the repository")
    output.mkdir(parents=True, exist_ok=True)
    folders = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    for folder in folders:
        files = pack_files(folder)
        if any(not p.is_file() or p.is_symlink() for p in files):
            raise ValueError(f"{folder.name}: missing required file or symlink")
        for file in files:
            if not re.fullmatch(r"\.[A-Za-z0-9]+", file.suffix):
                raise ValueError(f"{folder.name}/{file.relative_to(folder)}: shipped file must have an extension")
        path = output / f"{folder.name}-{args.version}.zip"
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file in sorted(files):
                member = zipfile.ZipInfo(f"{folder.name}/{file.relative_to(folder).as_posix()}")
                member.date_time = (2026, 1, 1, 0, 0, 0)
                member.compress_type = zipfile.ZIP_DEFLATED
                mode = 0o755 if file.stat().st_mode & 0o111 else 0o644
                member.external_attr = (stat.S_IFREG | mode) << 16
                archive.writestr(member, file.read_bytes())
        print(path.relative_to(ROOT))
    print(f"Packaged {len(folders)} skills at version {args.version}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as exc:
        print(f"pack failed: {exc}", file=sys.stderr)
        sys.exit(1)
