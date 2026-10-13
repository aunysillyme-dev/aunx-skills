"""Reproduce the synthetic Rename Sweep demonstration using Python stdlib."""
import json
from pathlib import Path
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parent
OLD = "cargo_delay"
NEW = "dispatch_delay"
SAMPLE = {
    "src/settings.py": 'def cargo_delay(config):\n    return config["cargo_delay"]\n',
    "config/settings.json": '{"cargo_delay": 2}\n',
    "docs/guide.md": '# Dispatch settings\n\nSet `cargo_delay` to control dispatch spacing.\n',
    "tests/test_settings.py": (
        'import json\nfrom pathlib import Path\nimport sys\n'
        'ROOT = Path(__file__).resolve().parents[1]\n'
        'sys.path.insert(0, str(ROOT / "src"))\n'
        'from settings import cargo_delay\n'
        'config = json.loads((ROOT / "config/settings.json").read_text())\n'
        'assert cargo_delay(config) == 2\n'
        'print("PASS: config reader returns the expected delay")\n'
    ),
    "ci/check.yml": 'name: Check delay\nenv:\n  CONFIG_KEY: cargo_delay\nsteps:\n  - run: python3 tests/test_settings.py\n',
    "notes/ticket.md": '# Config naming task\n\nUpdate the cargo_delay reader, sample, docs, and checks.\n',
    "history/release-notes.md": '# Historical release note\n\nThe sample originally used cargo_delay.\n',
}
ACTIVE = ("src", "config", "docs", "tests", "ci", "notes")

def write_fixture(root):
    for name, content in SAMPLE.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

def search(root, roots):
    hits = []
    for name in roots:
        folder = root / name
        if not folder.is_dir():
            raise RuntimeError(f"Missing declared root: {name}")
        for path in sorted(folder.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                    if OLD in line:
                        hits.append(f"{path.relative_to(root)}:{number}: {line}")
    return hits

def main():
    write_fixture(BASE / "before")
    write_fixture(BASE / "project")
    project = BASE / "project"
    before_hits = search(project, ACTIVE)
    if not before_hits:
        raise RuntimeError("Control search did not find the seeded old identifier")
    changed = []
    for name in SAMPLE:
        if name.startswith("history/"):
            continue
        path = project / name
        content = path.read_text(encoding="utf-8")
        path.write_text(content.replace(OLD, NEW), encoding="utf-8")
        changed.append(name)
    after_hits = search(project, ACTIVE)
    if after_hits:
        raise RuntimeError("Active old-name hits remain: " + repr(after_hits))
    for name in changed:
        if NEW not in (project / name).read_text(encoding="utf-8"):
            raise RuntimeError(f"New identifier missing: {name}")
    history_hits = search(project, ("history",))
    history = "history/release-notes.md"
    if (project / history).read_bytes() != (BASE / "before" / history).read_bytes():
        raise RuntimeError("Historical exception was changed")
    result = subprocess.run(
        [sys.executable, "tests/test_settings.py"], cwd=project,
        capture_output=True, text=True,
    )
    lines = [
        "Method: Python stdlib literal content search over declared real directories.",
        "Declared active roots: " + ", ".join(ACTIVE),
        "Control search completed: old identifier found before edit.",
        "Before hits:", *before_hits,
        "Changed active files:", *changed,
        f"Final active old-identifier hits: {len(after_hits)}; search completed successfully.",
        "Historical exception (preserved byte-for-byte):", *history_hits,
        "Behavior command: python3 tests/test_settings.py", result.stdout.rstrip(),
        f"Behavior exit code: {result.returncode}",
        "CI configuration was updated; no CI service was invoked.",
        "Open-ticket scope: synthetic local note only; external trackers excluded by request.",
        "Verdict: complete in the declared synthetic scope.",
    ]
    if result.stderr:
        lines.append(result.stderr.rstrip())
    proof = "\n".join(lines) + "\n"
    (BASE / "result.txt").write_text(proof, encoding="utf-8")
    print(proof, end="")
    return result.returncode

if __name__ == "__main__":
    raise SystemExit(main())
