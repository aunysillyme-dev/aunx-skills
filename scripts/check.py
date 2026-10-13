#!/usr/bin/env python3
"""Validate public skill artifacts; optionally scan text and zip members."""
import argparse
import ast
import re
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

from pack import pack_files

ROOT = Path(__file__).resolve().parents[1]
SLUGS = (
    "full-output-keeper", "number-guard", "x-spaces-transcriber",
    "docs-fetch-ladder", "absence-check", "instruction-weight",
    "rename-sweep", "ticket-gate", "client-work-to-template", "retro-to-rules",
)
FIELDS = (
    "Name", "Summary", "Price", "Full description", "Use cases", "Demo request",
    "Demo result", "FAQ", "Keywords", "Tags", "Compatibility",
    "Permissions notes", "Credits", "Repo link",
)
TAGS = set("ai-agents automation productivity documentation devops code-review "
           "developer-tools llm-ops research writing marketing project-management "
           "business-operations testing workflow-automation python".split())
# promo/ is the gitignored local render workspace for marketplace videos; it is never published.
EXCLUDED = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", "promo"}
UPSTREAM = re.compile(r"github\.com/(?!aunysillyme(?:-dev)?/)[\w.-]+/[\w.-]+"
                      r"|\b(?:rtk|codecalc|space-tape|Crawl4AI|AnswerDotAI|Whisper)\b", re.I)


def text_files():
    """Include ignored text artifacts too, with generated dependency trees excluded."""
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        if any(part in EXCLUDED for part in path.relative_to(ROOT).parts):
            continue
        try:
            raw = path.read_bytes()
            yield path.relative_to(ROOT).as_posix(), raw.decode("utf-8")
        except UnicodeDecodeError:
            continue


def frontmatter(text):
    """Parse the pack contract's flat YAML string mapping, rejecting other syntax."""
    lines = text.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise ValueError("missing closed YAML frontmatter")
    result = {}
    for line in lines[1:lines.index("---", 1)]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([a-z][a-z0-9_-]*):\s*(.+)", line)
        if not match:
            raise ValueError("expected flat YAML string fields")
        key, value = match.groups()
        if key in result:
            raise ValueError("duplicate frontmatter key: " + key)
        if value.startswith('"'):
            value = ast.literal_eval(value)
        elif value.startswith("'"):
            if not value.endswith("'"):
                raise ValueError("unclosed YAML quote")
            value = value[1:-1].replace("''", "'")
        elif re.search(r":\s|\s#", value) or value[0] in "[{>|&*!%@`":
            raise ValueError("quote description values with YAML punctuation")
        if not isinstance(value, str) or not value:
            raise ValueError("expected nonempty string")
        result[key] = value
    return result


def listing_fields(text):
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, re.M))
    result = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        key = match.group(1).casefold()
        if key in result:
            raise ValueError("duplicate listing field: " + key)
        result[key] = text[match.end():end].strip()
    return result


def scan(label, content, patterns, errors):
    for number, line in enumerate(content.splitlines(), 1):
        if chr(0x2014) in line:
            errors.append(f"{label}:{number}: prohibited punctuation")
        for index, pattern in enumerate(patterns, 1):
            if pattern.search(line):
                # Keep the private patterns and matched text out of public logs.
                errors.append(f"{label}:{number}: scrub pattern {index} matched")


def validate(patterns):
    errors = []
    actual = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
    if actual != set(SLUGS):
        errors.append("skills/: expected exactly the ten named packs")
    for slug in SLUGS:
        folder = ROOT / "skills" / slug
        try:
            for file in pack_files(folder):
                if not re.fullmatch(r"\.[A-Za-z0-9]+", file.suffix):
                    errors.append(f"skills/{slug}/{file.relative_to(folder)}: shipped file must have an extension")
            skill = (folder / "SKILL.md").read_text()
            metadata = frontmatter(skill)
            if metadata.get("name") != slug:
                errors.append(f"skills/{slug}/SKILL.md: name differs from folder")
            if not 40 <= len(metadata.get("description", "")) <= 1024:
                errors.append(f"skills/{slug}/SKILL.md: description must be 40-1024 characters")
            if UPSTREAM.search(skill) and not re.search(r"^#+ Credits\s*$", skill, re.M):
                errors.append(f"skills/{slug}/SKILL.md: upstream requires Credits")
            fields = listing_fields((folder / "listing.md").read_text())
            for field in FIELDS:
                if not fields.get(field.casefold()):
                    errors.append(f"skills/{slug}/listing.md: missing {field}")
            if len(fields.get("name", "")) > 60:
                errors.append(f"skills/{slug}/listing.md: Name exceeds 60 characters")
            expected = f"https://github.com/aunysillyme-dev/aunx-skills/tree/main/skills/{slug}"
            if expected not in fields.get("repo link", ""):
                errors.append(f"skills/{slug}/listing.md: incorrect Repo link")
            tags = set(re.findall(r"[a-z]+(?:-[a-z]+)*", fields.get("tags", "")))
            if not tags or not tags <= TAGS:
                errors.append(f"skills/{slug}/listing.md: invalid Tags")
            if (folder / "LICENSE.txt").read_bytes() != (ROOT / "LICENSE").read_bytes():
                errors.append(f"skills/{slug}/LICENSE.txt: must match root license")
            png = (ROOT / "logos" / (slug + ".png")).read_bytes()
            if (png[:8] != b"\x89PNG\r\n\x1a\n" or png[12:16] != b"IHDR"
                    or struct.unpack(">II", png[16:24]) != (512, 512)):
                errors.append(f"logos/{slug}.png: expected PNG at 512x512")
            if not (ROOT / "logos" / (slug + ".svg")).is_file():
                errors.append(f"logos/{slug}.svg: missing")
            if not (ROOT / "demos" / slug).is_dir():
                errors.append(f"demos/{slug}/: missing")
        except (OSError, ValueError, SyntaxError, struct.error) as exc:
            errors.append(f"skills/{slug}: {exc}")
    credits = ROOT / "CREDITS.md"
    if not credits.is_file():
        errors.append("CREDITS.md: missing")
    else:
        content = credits.read_text()
        for repo in ("rtk-ai/rtk", "hovtgc/x-spaces-transcription", "The-40-Thieves/codecalc",
                     "AnswerDotAI/llms-txt", "unclecode/crawl4ai"):
            if "https://github.com/" + repo not in content:
                errors.append("CREDITS.md: missing required upstream " + repo)
    for label, content in text_files():
        scan(label, content, patterns, errors)
    # Tracked text can live in an otherwise excluded directory.
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if tracked.returncode:
        errors.append("git ls-files failed: " + tracked.stderr.decode(errors="replace"))
    else:
        for name in tracked.stdout.decode().split("\0"):
            if name and any(part in EXCLUDED for part in Path(name).parts):
                try:
                    scan(name, (ROOT / name).read_text(), patterns, errors)
                except UnicodeDecodeError:
                    pass
                except OSError as exc:
                    errors.append(f"{name}: {exc}")
    for path in sorted((ROOT / "dist").glob("*.zip")):
        try:
            with zipfile.ZipFile(path) as archive:
                for member in archive.infolist():
                    raw = archive.read(member)
                    try:
                        scan(f"dist/{path.name}!{member.filename}", raw.decode("utf-8"), patterns, errors)
                    except UnicodeDecodeError:
                        pass
        except (OSError, zipfile.BadZipFile) as exc:
            errors.append(f"dist/{path.name}: {exc}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scrub", type=Path, help="external regex denylist, never copied into repo")
    args = parser.parse_args()
    patterns = []
    if args.scrub:
        denylist = args.scrub.resolve()
        if denylist == ROOT or ROOT in denylist.parents:
            parser.error("keep the denylist outside the repository")
        try:
            for line in denylist.read_text().splitlines():
                if line.strip() and not line.lstrip().startswith("#"):
                    patterns.append(re.compile(line.strip(), re.I))
        except (OSError, re.error):
            parser.error("cannot load external scrub file or compile its patterns")
    try:
        errors = validate(patterns)
    except OSError as exc:
        errors = [str(exc)]
    if errors:
        print("FAILED\n" + "\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASSED: {len(SLUGS)} packs, listings, licenses, logos, credits, text and zip scan; "
          f"{len(patterns)} external scrub patterns")
    return 0


if __name__ == "__main__":
    sys.exit(main())
