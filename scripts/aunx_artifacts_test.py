#!/usr/bin/env python3
"""Exercise public-data rejection and installable zip boundaries on fixtures."""
import importlib.util
import re
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import zipfile

HERE = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check = load("check")
pack = load("pack")


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="aunx-fixture-", dir=HERE)
        self.root = Path(self.directory.name)
        self.addCleanup(self.directory.cleanup)
        self.addCleanup(patch.stopall)
        patch.object(check, "ROOT", self.root).start()
        patch.object(pack, "ROOT", self.root).start()
        patch.object(check.subprocess, "run", return_value=subprocess.CompletedProcess(
            ["git", "ls-files"], 0, stdout=b"", stderr=b"")).start()
        (self.root / "LICENSE").write_text("Fixture MIT license\n")
        (self.root / "CREDITS.md").write_text("\n".join(
            "https://github.com/" + repo for repo in (
                "rtk-ai/rtk", "hovtgc/x-spaces-transcription", "The-40-Thieves/codecalc",
                "AnswerDotAI/llms-txt", "unclecode/crawl4ai")))
        (self.root / "logos").mkdir()
        for slug in check.SLUGS:
            folder = self.root / "skills" / slug
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(f"---\nname: {slug}\ndescription: "
                "Use this fixture to exercise a realistic public skill artifact validation workflow.\n---\n"
                "# Fixture\n")
            (folder / "LICENSE.txt").write_text("Fixture MIT license\n")
            fields = {field: "Fixture content" for field in check.FIELDS}
            fields.update(Name="Fixture", Tags="ai-agents, testing")
            fields["Repo link"] = f"https://github.com/aunysillyme-dev/aunx-skills/tree/main/skills/{slug}"
            (folder / "listing.md").write_text("\n".join(
                f"## {field}\n\n{fields[field]}\n" for field in check.FIELDS))
            # Only the PNG header is used by the dimension contract.
            (self.root / "logos" / (slug + ".png")).write_bytes(
                b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", 512, 512))
            (self.root / "logos" / (slug + ".svg")).write_text("<svg/>")
            (self.root / "demos" / slug).mkdir(parents=True)

    def test_frontmatter_internal_metadata(self):
        prefix = "---\nname: fixture\n"
        block = "metadata:\n  internal: true\n"
        self.assertEqual(check.frontmatter(prefix + block + "---\n"),
                         {"name": "fixture", "metadata": {"internal": True}})
        for invalid in ("metadata:\n  other: x\n", "metadata:\n",
                        "metadata:\n  internal: false\n", block + block,
                        block + "name: after\n", "metadata: flat\n" + block):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                check.frontmatter(prefix + invalid + "---\n")

    def test_scrub_rejects_repo_and_zip_without_echoing_private_text(self):
        self.assertEqual(check.validate([]), [])
        marker = "synthetic-sensitive-marker"
        (self.root / "README.md").write_text("Public text\n" + marker.upper())
        dist = self.root / "dist"
        dist.mkdir()
        with zipfile.ZipFile(dist / "fixture.zip", "w") as archive:
            archive.writestr("fixture/SKILL.md", "ordinary\n" + marker)
        errors = check.validate([re.compile(marker, re.I)])
        self.assertTrue(any("README.md:2:" in item for item in errors))
        self.assertTrue(any("fixture.zip!fixture/SKILL.md:2:" in item for item in errors))
        self.assertTrue(all(marker not in item.casefold() for item in errors))

    def test_invalid_dimensions_frontmatter_credit_and_listing_are_rejected(self):
        slug = check.SLUGS[0]
        folder = self.root / "skills" / slug
        (folder / "SKILL.md").write_text("---\nname: other\ndescription: short\n---\ncodecalc\n")
        (folder / "listing.md").write_text("## Name\n\n" + "x" * 61)
        (self.root / "logos" / (slug + ".png")).write_bytes(b"not a PNG")
        errors = check.validate([])
        for message in ("name differs", "40-1024", "requires Credits", "missing Summary",
                        "exceeds 60", "expected PNG"):
            self.assertTrue(any(message in item for item in errors), message)

    def test_pack_has_installable_root_and_excludes_marketplace_data(self):
        folder = self.root / "skills" / check.SLUGS[0]
        (folder / "scripts").mkdir()
        helper = folder / "scripts" / "aunx-helper.py"
        helper.write_text("#!/usr/bin/env python3\nprint('fixture')\n")
        helper.chmod(0o755)
        with patch.object(sys, "argv", ["pack.py", "--version", "1.2.3"]):
            self.assertEqual(pack.main(), 0)
        archives = sorted((self.root / "dist").glob("*.zip"))
        self.assertEqual(len(archives), 10)
        for archive_path in archives:
            with zipfile.ZipFile(archive_path) as archive:
                slug = archive_path.name.removesuffix("-1.2.3.zip")
                self.assertTrue({slug + "/SKILL.md", slug + "/LICENSE.txt"} <= set(archive.namelist()))
                self.assertTrue(all(name.startswith(slug + "/") for name in archive.namelist()))
                self.assertFalse(any("listing.md" in name or "demos/" in name for name in archive.namelist()))

    def test_pack_rejects_extensionless_shipped_file(self):
        folder = self.root / "skills" / check.SLUGS[0]
        (folder / "scripts").mkdir()
        helper = folder / "scripts" / "aunx-helper"
        helper.write_text("#!/usr/bin/env python3\nprint('fixture')\n")
        with patch.object(sys, "argv", ["pack.py", "--version", "1.2.3"]):
            with self.assertRaisesRegex(ValueError, "shipped file must have an extension"):
                pack.main()


if __name__ == "__main__":
    unittest.main()
