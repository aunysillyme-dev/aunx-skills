import copy
from contextlib import redirect_stderr
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest
from unittest import mock
import os

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/aunx-decompose/skills/decompose/scripts/decompose.py"
sys.dont_write_bytecode = True
sys.path.insert(0, str(SCRIPT.parent))
import decompose


class DecomposeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.store = Path(self.temp.name) / "user/recipes.json"
        patcher = mock.patch.dict(os.environ, {"DECOMPOSE_RECIPES": str(self.store)})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.card = {"mode": "build", "ask": "build it", "paths": "/tmp/example.py",
                     "scope": "the supplied file", "data": "private", "voice": "no"}
        self.steps = decompose.decompose(self.card)

    def test_build_expands_in_order(self):
        self.assertEqual([s["kind"] for s in self.steps],
                         ["frame", "code", "test-run", "audit-needed", "ship"])
        self.assertEqual(decompose.validate(self.steps), [])
        self.assertEqual(self.steps[1]["paths"], ["/tmp/example.py"])
        self.assertTrue(all(step["needs"]["tools"] == [] for step in self.steps))

    def test_research_defaults_and_card_tools(self):
        steps = decompose.decompose({"kind": "research", "ask": "find evidence"})
        self.assertEqual([step["needs"]["tools"] for step in steps], [["web"], ["web"], [], []])
        steps = decompose.decompose({"kind": "research", "tools": ["docs", "docs"]})
        self.assertEqual([step["needs"]["tools"] for step in steps],
                         [["docs", "web"], ["docs", "web"], ["docs"], ["docs"]])

    def test_skip_ship_and_rewire_custom_recipe(self):
        for flag in ("push", "ship"):
            steps = decompose.decompose(dict(self.card, **{flag: "no"}))
            self.assertNotIn("ship", [step["kind"] for step in steps])
            self.assertEqual(decompose.validate(steps), [])
        custom = copy.deepcopy(self.steps)
        custom.append(dict(custom[0], id="after", deps=["ship"], inputs=["step:ship"]))
        self.store.parent.mkdir(parents=True)
        self.store.write_text(json.dumps({"custom": {"steps": custom}}))
        steps = decompose.decompose({"kind": "custom", "push": "no"})
        self.assertEqual(steps[-1]["deps"], ["audit-needed"])
        self.assertEqual(steps[-1]["inputs"], ["step:audit-needed"])
        self.assertEqual(decompose.validate(steps), [])

    def test_card_tools_syntax(self):
        for value in ('web, docs', '["web", "docs"]', '"web, docs"'):
            with self.subTest(value=value):
                card = decompose.parse_task('---\nkind: read\ntools: ' + value + '\n---\n')
                self.assertEqual(card["tools"], ["docs", "web"])
                self.assertTrue(all(step["needs"]["tools"] == ["docs", "web"]
                                    for step in decompose.decompose(card)))

    def test_malformed_needs_tools_rejected(self):
        for value in (None, "web", [False], [""], ["web docs"]):
            with self.subTest(value=value):
                self.steps[0]["needs"]["tools"] = value
                self.assertIn("frame: invalid needs.tools", decompose.validate(self.steps))
        self.steps[0]["needs"].pop("tools")
        self.assertIn("frame: invalid needs.tools", decompose.validate(self.steps))

    def test_cycle_rejected(self):
        self.steps[0]["deps"] = ["ship"]
        self.assertIn("dependency cycle", decompose.validate(self.steps))

    def test_nested_write_paths_rejected(self):
        self.steps[-1]["paths"] = ["/tmp/example.py/child"]
        self.assertTrue(any("overlapping write paths" in e for e in decompose.validate(self.steps)))

    def test_validate_cli_rejects_cycle_and_overlap(self):
        cycle = copy.deepcopy(self.steps)
        cycle[0]["deps"] = ["ship"]
        overlap = copy.deepcopy(self.steps)
        overlap[-1]["paths"] = ["/tmp/example.py/child"]
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            path = Path(tmp) / "steps.json"
            for steps, reason in ((cycle, "cycle"), (overlap, "overlapping write paths")):
                path.write_text(json.dumps(steps))
                result = subprocess.run([sys.executable, str(Path(decompose.__file__)),
                                         "--validate", str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertIn(reason, result.stderr)

    def test_unknown_recipe_returns_schema_and_exit_three(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            card = Path(tmp) / "card.md"
            card.write_text('---\nmode: other\nask: "question"\n---\n')
            result = subprocess.run([sys.executable, str(Path(decompose.__file__)), str(card)],
                                    capture_output=True, text=True)
        self.assertEqual(result.returncode, 3)
        self.assertIn("DECOMPOSE needs-model", result.stderr)
        self.assertEqual(json.loads(result.stdout)["type"], "array")

    def test_candidate_recipe_save_and_validate(self):
        decompose.save_recipe("custom", copy.deepcopy(self.steps))
        data = json.loads(self.store.read_text())
        self.assertEqual(data["custom"]["status"], "candidate")
        self.assertEqual(decompose.decompose({"kind": "custom"}), self.steps)
        expanded = decompose.decompose({"kind": "custom", "tools": "docs"})
        self.assertTrue(all(step["needs"]["tools"] == ["docs"] for step in expanded))
        self.assertEqual(decompose.decompose({"kind": "custom"}), self.steps)

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              capture_output=True, text=True)

    def write_steps(self, steps):
        path = Path(self.temp.name) / "steps.json"
        path.write_text(json.dumps(steps))
        return path

    def test_all_bundled_recipes(self):
        for name, kinds in (
                ("fix", ["reproduce", "code", "test-run"]),
                ("research", ["search", "fetch", "extract", "synthesize"]),
                ("read", ["read", "extract"]), ("audit", ["audit"])):
            with self.subTest(recipe=name):
                steps = decompose.decompose(dict(self.card, mode=name))
                self.assertEqual([step["kind"] for step in steps], kinds)
                self.assertEqual(decompose.validate(steps), [])

    def test_card_fields_and_comments(self):
        card = decompose.parse_task('---\nkind: fix # comment\nask: "fix #1" # tail\n'
                                    'verify: first\nverify: second\n---\n'
                                    '**Purpose.** Repair it.\n**Scope of build.** One file.\n'
                                    '**Denied actions.** Publishing.\n')
        self.assertEqual(card["kind"], "fix")
        self.assertEqual(card["ask"], "fix #1")
        self.assertEqual(card["verify"], ["first", "second"])
        self.assertEqual(card["purpose"], "Repair it.")
        self.assertEqual(card["scope"], "One file.")
        self.assertEqual(card["denied"], "Publishing.")

    def test_invalid_cards(self):
        for text in ("no frontmatter", "---\nkind: read", "---\nbad field\n---",
                     "---\nkind: read\nkind: fix\n---", '---\nask: "x" extra\n---'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                decompose.parse_task(text)

    def test_schema_errors(self):
        for steps in (None, {}, [], [None]):
            with self.subTest(steps=steps):
                self.assertTrue(decompose.validate(steps))
        for field in ("id", "kind", "inputs", "outputs", "deps", "paths", "needs"):
            steps = copy.deepcopy(self.steps)
            del steps[0][field]
            with self.subTest(field=field):
                self.assertTrue(decompose.validate(steps))
        for field in ("inputs", "outputs", "deps", "paths"):
            for value in ("text", [False], [""]):
                steps = copy.deepcopy(self.steps)
                steps[0][field] = value
                with self.subTest(field=field, value=value):
                    self.assertIn("frame: invalid " + field, decompose.validate(steps))

    def test_needs_schema(self):
        for field in ("cpu", "ram_gb", "disk_gb"):
            for value in (None, True, -1, "1", float("nan"), float("inf")):
                steps = copy.deepcopy(self.steps)
                steps[0]["needs"][field] = value
                with self.subTest(field=field, value=value):
                    self.assertIn("frame: invalid needs." + field, decompose.validate(steps))
        self.steps[0]["needs"]["gpu"] = 0
        self.assertIn("frame: invalid needs.gpu", decompose.validate(self.steps))

    def test_huge_needs_integers_exit_two_without_traceback(self):
        for field in ("cpu", "ram_gb", "disk_gb"):
            with self.subTest(field=field):
                steps = copy.deepcopy(self.steps)
                steps[0]["needs"][field] = 10 ** 309
                result = self.run_cli("--validate", self.write_steps(steps))
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("frame: invalid needs." + field, result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_id_and_unknown_kind(self):
        self.steps[1]["id"] = "frame"
        self.steps[0]["kind"] = "unknown"
        errors = decompose.validate(self.steps)
        self.assertIn("duplicate step id: frame", errors)
        self.assertIn("unknown kind: unknown", errors)

    def test_unknown_dependency(self):
        self.steps[0]["deps"] = ["missing"]
        result = self.run_cli("--validate", self.write_steps(self.steps))
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown dependency missing", result.stderr)

    def test_relative_write_path(self):
        self.steps[1]["paths"] = ["relative/file.py"]
        result = self.run_cli("--validate", self.write_steps(self.steps))
        self.assertEqual(result.returncode, 2)
        self.assertIn("write path must be absolute", result.stderr)

    def test_overlap_variants_and_sibling_paths(self):
        for path in ("/tmp/example.py", "/tmp/example.py/child", "/tmp"):
            self.steps[-1]["paths"] = [path]
            with self.subTest(path=path):
                self.assertTrue(any("overlapping write paths" in error
                                    for error in decompose.validate(self.steps)))
        self.steps[-1]["paths"] = ["/tmp/example.py-other"]
        self.assertEqual(decompose.validate(self.steps), [])

    def test_symlink_overlap(self):
        directory = Path(self.temp.name)
        real = directory / "real"
        real.mkdir()
        alias = directory / "alias"
        alias.symlink_to(real, target_is_directory=True)
        self.steps[1]["paths"] = [str(real)]
        self.steps[-1]["paths"] = [str(alias / "child")]
        self.assertTrue(any("overlapping write paths" in error
                            for error in decompose.validate(self.steps)))

    def test_casefolded_write_paths_overlap(self):
        directory = Path(self.temp.name)
        self.steps[1]["paths"] = [str(directory / "README.md")]
        for path in ("readme.md", "readme.md/child", "."):
            with self.subTest(path=path):
                self.steps[-1]["paths"] = [str(directory / path)]
                result = self.run_cli("--validate", self.write_steps(self.steps))
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("overlapping write paths", result.stderr)

    def test_hardlink_write_paths_overlap(self):
        real = Path(self.temp.name) / "real"
        real.write_text("shared")
        alias = real.with_name("alias")
        os.link(real, alias)
        self.steps[1]["paths"] = [str(real)]
        self.steps[-1]["paths"] = [str(alias)]
        result = self.run_cli("--validate", self.write_steps(self.steps))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("overlapping write paths", result.stderr)

    def test_waves_branch_join_and_input_order(self):
        base = copy.deepcopy(self.steps[0])
        steps = [dict(base, id="join", deps=["left", "right"]),
                 dict(base, id="left", deps=["root"]),
                 dict(base, id="root", deps=[]),
                 dict(base, id="independent", deps=[]),
                 dict(base, id="right", deps=["root"])]
        result = self.run_cli("--validate", self.write_steps(steps), "--waves")
        self.assertEqual(result.returncode, 0, result.stderr)
        waves = json.loads(result.stdout)
        self.assertEqual([[step["id"] for step in wave] for wave in waves],
                         [["root", "independent"], ["left", "right"], ["join"]])
        self.assertEqual(waves[0][0], steps[2])

    def test_waves_card_and_task_alias(self):
        card = Path(self.temp.name) / "card.md"
        card.write_text('---\nkind: read\nask: "Read the report"\n---\n')
        result = self.run_cli(card, "--waves")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([[step["id"] for step in wave] for wave in json.loads(result.stdout)],
                         [["read"], ["extract"]])
        result = self.run_cli("--task", card)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([step["id"] for step in json.loads(result.stdout)], ["read", "extract"])

    def test_waves_reject_invalid_graph(self):
        self.steps[0]["deps"] = ["ship"]
        result = self.run_cli("--validate", self.write_steps(self.steps), "--waves")
        self.assertEqual(result.returncode, 2)
        self.assertIn("dependency cycle", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_recipe_merge_user_over_bundle(self):
        self.store.parent.mkdir(parents=True)
        self.store.write_text(json.dumps({"build": {"kinds": ["read"]},
                                          "custom": {"kinds": ["audit"]},
                                          "tools_by_kind": {"read": ["docs"]},
                                          "scopes": {"read": "Read the custom source."}}))
        self.assertEqual([s["kind"] for s in decompose.decompose(self.card)], ["read"])
        self.assertEqual(decompose.decompose({"kind": "custom"})[0]["kind"], "audit")
        self.assertEqual(decompose.decompose({"kind": "read"})[0]["needs"]["tools"], ["docs"])
        self.assertEqual(decompose.decompose({"kind": "research"})[0]["needs"]["tools"], ["web"])
        self.assertIn("extract", decompose.load_recipes()["scopes"])
        card = Path(self.temp.name) / "card.md"
        card.write_text('---\nkind: build\n---\n')
        result = self.run_cli(card)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]["kind"], "read")

    def test_default_save_location(self):
        with mock.patch.dict(os.environ), mock.patch.object(Path, "home", return_value=Path(self.temp.name)):
            os.environ.pop("DECOMPOSE_RECIPES", None)
            decompose.save_recipe("custom", self.steps)
        saved = Path(self.temp.name) / ".claude/decompose/recipes.json"
        self.assertEqual(json.loads(saved.read_text())["custom"]["steps"], self.steps)

    def test_save_cli_keeps_plugin_unchanged(self):
        def snapshot():
            return {str(path.relative_to(decompose.PLUGIN_ROOT)): path.read_bytes() if path.is_file() else None
                    for path in decompose.PLUGIN_ROOT.rglob("*")}
        before = snapshot()
        result = self.run_cli("--validate", self.write_steps(self.steps), "--save-recipe", "custom")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "DECOMPOSE valid\n")
        self.assertEqual(snapshot(), before)
        self.assertEqual(set(json.loads(self.store.read_text())), {"custom"})

    def test_save_preserves_user_recipes_and_rejects_duplicates(self):
        decompose.save_recipe("one", self.steps)
        decompose.save_recipe("two", self.steps)
        self.assertEqual(set(json.loads(self.store.read_text())), {"one", "two"})
        before = self.store.read_bytes()
        for name in ("one", "build", "bad name"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                decompose.save_recipe(name, self.steps)
        self.assertEqual(self.store.read_bytes(), before)

    def concurrent_saves(self, fallback=False, duplicate=False):
        self.store.parent.mkdir(parents=True, exist_ok=True)
        self.store.write_text("{}")
        self.store.with_name(self.store.name + ".lock").unlink(missing_ok=True)
        steps = self.write_steps(self.steps)
        worker = textwrap.dedent('''
            import sys
            import time
            from pathlib import Path
            sys.dont_write_bytecode = True
            if sys.argv[6] == "True":
                sys.modules["fcntl"] = None
            sys.path.insert(0, sys.argv[1])
            import decompose
            replace = decompose.os.replace
            def delayed_replace(source, target):
                Path(sys.argv[4]).touch()
                deadline = time.monotonic() + 1
                while not Path(sys.argv[5]).exists() and time.monotonic() < deadline:
                    time.sleep(0.01)
                replace(source, target)
            decompose.os.replace = delayed_replace
            sys.exit(decompose.main(["--validate", sys.argv[2], "--save-recipe", sys.argv[3]]))
        ''')
        names = ("one", "one" if duplicate else "two")
        ready = [Path(self.temp.name) / ("ready-" + str(i)) for i in range(2)]
        for marker in ready:
            marker.unlink(missing_ok=True)
        processes = [subprocess.Popen(
            [sys.executable, "-c", worker, str(SCRIPT.parent), str(steps), name,
             str(ready[i]), str(ready[1 - i]), str(fallback)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for i, name in enumerate(names)]
        try:
            outputs = [process.communicate(timeout=10) for process in processes]
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                process.communicate()
        codes = sorted(process.returncode for process in processes)
        self.assertEqual(codes, [0, 2] if duplicate else [0, 0], outputs)
        self.assertEqual(set(json.loads(self.store.read_text())), set(names))
        if duplicate:
            self.assertTrue(any("recipe already exists: one" in err for out, err in outputs))

    def test_concurrent_saves_preserve_both_recipes(self):
        for fallback in (False, True):
            with self.subTest(fallback=fallback):
                self.concurrent_saves(fallback=fallback)

    def test_concurrent_saves_reject_duplicate_name(self):
        for fallback in (False, True):
            with self.subTest(fallback=fallback):
                self.concurrent_saves(fallback=fallback, duplicate=True)

    def test_fallback_lock_timeout_exit_two(self):
        self.store.parent.mkdir(parents=True)
        lock = self.store.with_name(self.store.name + ".lock")
        lock.write_text("held")
        stderr = io.StringIO()
        with mock.patch.object(decompose, "fcntl", None), mock.patch.object(
                decompose.time, "monotonic", side_effect=[0, 10]), redirect_stderr(stderr):
            code = decompose.main(["--validate", str(self.write_steps(self.steps)),
                                   "--save-recipe", "custom"])
        self.assertEqual(code, 2)
        self.assertIn("timed out waiting for recipe lock", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())
        self.assertEqual(lock.read_text(), "held")
        self.assertFalse(self.store.exists())

    def test_fallback_lock_released_after_write_failure(self):
        with mock.patch.object(decompose, "fcntl", None):
            with mock.patch.object(decompose.os, "replace", side_effect=OSError("replace failed")):
                with self.assertRaisesRegex(OSError, "replace failed"):
                    decompose.save_recipe("custom", self.steps)
            self.assertFalse(self.store.with_name(self.store.name + ".lock").exists())
            self.assertEqual(list(self.store.parent.glob(".recipes-*")), [])
            decompose.save_recipe("custom", self.steps)
        self.assertEqual(set(json.loads(self.store.read_text())), {"custom"})

    def test_cannot_save_inside_plugin_or_through_symlink(self):
        alias = Path(self.temp.name) / "plugin-alias"
        alias.symlink_to(decompose.PLUGIN_ROOT, target_is_directory=True)
        for directory in (decompose.PLUGIN_ROOT, alias):
            with self.subTest(directory=directory), mock.patch.dict(
                    os.environ, {"DECOMPOSE_RECIPES": str(directory / "new/recipes.json")}):
                result = self.run_cli("--validate", self.write_steps(self.steps), "--save-recipe", "custom")
                self.assertEqual(result.returncode, 2)
                self.assertIn("outside the plugin directory", result.stderr)
        self.assertFalse((decompose.PLUGIN_ROOT / "new").exists())

    def test_casefolded_plugin_directory_exit_two(self):
        root = Path(self.temp.name) / "plugins/aunx-decompose"
        target = root.with_name("AUNX-DECOMPOSE") / "skills/decompose/recipes.json"
        stderr = io.StringIO()
        with mock.patch.object(decompose, "PLUGIN_ROOT", root), mock.patch.dict(
                os.environ, {"DECOMPOSE_RECIPES": str(target)}), redirect_stderr(stderr):
            code = decompose.main(["--validate", str(self.write_steps(self.steps)),
                                   "--save-recipe", "custom"])
        self.assertEqual(code, 2, stderr.getvalue())
        self.assertIn("outside the plugin directory", stderr.getvalue())
        self.assertFalse(target.parent.exists())

    def test_plugin_directory_samefile_alias_rejected(self):
        self.store.parent.mkdir(parents=True)
        samefile = os.path.samefile
        def alias_match(left, right):
            if Path(left) == self.store.parent and Path(right) == decompose.PLUGIN_ROOT:
                return True
            return samefile(left, right)
        with mock.patch.object(os.path, "samefile", side_effect=alias_match):
            with self.assertRaisesRegex(ValueError, "outside the plugin directory"):
                decompose.user_recipes_path()

    def test_save_invalid_steps_does_not_create_store(self):
        self.steps[0]["deps"] = ["ship"]
        result = self.run_cli("--validate", self.write_steps(self.steps), "--save-recipe", "bad")
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.store.exists())

    def test_malformed_json_and_missing_file_exit_two(self):
        path = self.write_steps(self.steps)
        path.write_text("{")
        for target in (path, path.with_name("missing.json")):
            with self.subTest(target=target):
                result = self.run_cli("--validate", target)
                self.assertEqual(result.returncode, 2)
                self.assertIn("DECOMPOSE error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_malformed_user_recipe_exit_two(self):
        self.store.parent.mkdir(parents=True)
        card = Path(self.temp.name) / "card.md"
        card.write_text('---\nkind: custom\n---\n')
        for data in ([], {"custom": []}, {"custom": {"steps": [None]}},
                     {"custom": {"kinds": ["unknown"]}}, {"tools_by_kind": []}):
            self.store.write_text(json.dumps(data))
            with self.subTest(data=data):
                result = self.run_cli(card)
                self.assertEqual(result.returncode, 2)
                self.assertIn("DECOMPOSE error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_deeply_nested_steps_json_exit_two(self):
        path = Path(self.temp.name) / "nested.json"
        path.write_text("[" * 200000 + "]" * 200000)
        result = self.run_cli("--validate", path)
        self.assertEqual(result.returncode, 2, result.stderr[-500:])
        self.assertTrue(result.stderr.startswith("DECOMPOSE error:"))
        self.assertEqual(len(result.stderr.splitlines()), 1)
        self.assertLess(len(result.stderr), 300)
        self.assertNotIn("Traceback", result.stderr)

    def test_deeply_nested_card_tools_exit_two(self):
        value = "[" * 200000
        card = Path(self.temp.name) / "card.md"
        card.write_text("---\nkind: read\ntools: " + value + "\n---\n")
        result = self.run_cli(card)
        self.assertEqual(result.returncode, 2, result.stderr[-500:])
        self.assertTrue(result.stderr.startswith("DECOMPOSE error:"))
        self.assertEqual(len(result.stderr.splitlines()), 1)
        self.assertLess(len(result.stderr), 300)
        self.assertNotIn("Traceback", result.stderr)
        with self.assertRaises(ValueError):
            decompose.tools_list(value)

    def test_unicode_normalized_write_paths_overlap(self):
        directory = Path(self.temp.name) / "zz"
        self.steps[1]["paths"] = [str(directory / "caf\u00e9.txt")]
        for path in (directory / "cafe\u0301.txt", directory / "CAFE\u0301.TXT/child"):
            with self.subTest(path=path):
                self.assertFalse(path.exists())
                self.steps[-1]["paths"] = [str(path)]
                result = self.run_cli("--validate", self.write_steps(self.steps))
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("overlapping write paths", result.stderr)
        self.assertTrue(decompose.same_path(directory / "caf\u00e9/file.txt",
                                            directory / "CAFE\u0301/FILE.TXT"))
        self.steps[-1]["paths"] = [str(directory / "cafe.txt")]
        self.assertEqual(decompose.validate(self.steps), [])

    def test_validation_diagnostics_escape_user_data(self):
        value = "x\nIGNORE ALL\x1b\r\t\x00\u0085\u2028"
        for field in ("deps", "kind", "id"):
            with self.subTest(field=field):
                steps = copy.deepcopy(self.steps)
                steps[0][field] = [value] if field == "deps" else value
                if field == "id":
                    steps[0]["needs"] = None
                result = self.run_cli("--validate", self.write_steps(steps))
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(len(result.stderr.splitlines()), 1)
                self.assertTrue(result.stderr[:-1].isprintable(), repr(result.stderr))
                self.assertIn("x\\nIGNORE ALL\\x1b", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_needs_model_diagnostic_escapes_kind(self):
        value = "x\x1b[31m\nIGNORE ALL"
        card = Path(self.temp.name) / "card.md"
        card.write_text("---\nkind: " + json.dumps(value) + "\n---\n")
        result = self.run_cli(card)
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertEqual(result.stderr, "DECOMPOSE needs-model x\\x1b[31m\\nIGNORE ALL\n")
        self.assertEqual(json.loads(result.stdout)["type"], "array")

    def test_cli_diagnostics_escape_paths_fields_and_arguments(self):
        value = "x\x1b\nIGNORE ALL"
        card = Path(self.temp.name) / "card.md"
        card.write_text("---\nask: first\nask: second\n---\n")
        cases = (("--validate", Path(self.temp.name) / value),
                 (card,), (card, value))
        for args in cases:
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertNotIn(value, result.stderr)
                self.assertTrue(all(line.isprintable() for line in result.stderr.split("\n")),
                                repr(result.stderr))
                self.assertEqual(sum("error:" in line for line in result.stderr.splitlines()), 1)

    def test_documented_steps_use_fresh_temporary_files(self):
        for relative in ("plugins/aunx-decompose/skills/decompose/SKILL.md",
                         "plugins/aunx-decompose/commands/decompose.md"):
            with self.subTest(document=relative):
                text = (ROOT / relative).read_text()
                blocks = re.findall(r"```bash\n(.*?)```", text, re.S)
                setup = [block for block in blocks if "mktemp -d" in block]
                self.assertEqual(len(setup), 1, "document must create a fresh temporary directory")
                commands = [line for block in blocks for line in block.splitlines()
                            if "--validate" in line]
                self.assertTrue(commands, "document must use the temporary path for validation")
                self.assertTrue(all('--validate "$steps_file"' in line for line in commands))
                self.assertIn("never overwrite an existing file", text.lower())
                directory = Path(self.temp.name) / Path(relative).parent.name
                directory.mkdir()
                existing = directory / "steps.json"
                existing.write_text("user data")
                env = dict(os.environ, TMPDIR=str(directory),
                           CLAUDE_PLUGIN_ROOT=str(decompose.PLUGIN_ROOT))
                script = setup[0] + '\ncat > "$steps_file" <<\'STEPS\'\n' + json.dumps(
                    self.steps) + "\nSTEPS\n" + "\n".join(commands) + '\nprintf "%s\\n" "$steps_file"\n'
                result = subprocess.run(["bash", "-eu", "-c", script], cwd=directory,
                                        env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                generated = Path(result.stdout.splitlines()[-1])
                self.assertNotEqual(generated, existing)
                self.assertEqual(json.loads(generated.read_text()), self.steps)
                self.assertEqual(existing.read_text(), "user data")


if __name__ == "__main__":
    unittest.main()
