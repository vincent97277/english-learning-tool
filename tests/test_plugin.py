import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import plugin


class PluginChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        self.root.mkdir()
        for name in ("plugin.json", "LICENSE", ".claude-plugin", ".agents", "skills"):
            source = plugin.ROOT / name
            if source.is_dir():
                shutil.copytree(source, self.root / name)
            else:
                shutil.copy2(source, self.root / name)
        self.archive = Path(self.temp.name) / "plugin.zip"

    def readback(self):
        _, files, _ = plugin.check_sources(self.root)
        return {"files": [{"path": p.relative_to(self.root).as_posix()} for p in files],
                "contents": {p.relative_to(self.root).as_posix(): p.read_text() for p in files},
                "next_offset": None}

    def test_duplicate_json_key_blocks_packaging_without_echoing_key(self):
        path = self.root / "plugin.json"
        path.write_text('{"secret-marker":1,"secret-marker":2}')
        with self.assertRaisesRegex(plugin.CheckError, "^json_duplicate_key$"):
            plugin.pack(self.root, self.archive)
        self.assertFalse(self.archive.exists())

    def test_metadata_drift_blocks_packaging(self):
        path = self.root / ".claude-plugin/plugin.json"
        data = json.loads(path.read_text())
        data["version"] = "99.0.0"
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(plugin.CheckError, "legacy_metadata_mismatch"):
            plugin.check_sources(self.root)

    def test_yaml_types_and_duplicates_are_rejected(self):
        path = self.root / "skills/english-patterns/SKILL.md"
        for frontmatter in ("name: english-patterns\ndescription: true",
                            "name: english-patterns\nname: english-patterns\ndescription: explain"):
            with self.subTest(frontmatter=frontmatter):
                path.write_text("---\n" + frontmatter + "\n---\nExplain.")
                with self.assertRaises(plugin.CheckError):
                    plugin.check_sources(self.root)

    def test_nonsemantic_versions_are_rejected(self):
        for version in ("01.0.0", "1.0.0-01", "1.0.0-a..b", "1.0.0+"):
            self.assertIsNone(plugin.re.fullmatch(plugin.SEMVER, version))

    def test_stale_archive_is_rejected(self):
        self.assertTrue(plugin.pack(self.root, self.archive)["ok"])
        path = self.root / "skills/english-patterns/SKILL.md"
        original = path.read_text()
        changed = original.replace("English Patterns", "English Patternz", 1)
        self.assertNotEqual(original, changed)
        self.assertEqual(len(original.encode()), len(changed.encode()))
        path.write_text(changed)
        with self.assertRaisesRegex(plugin.CheckError, "archive_stale_content"):
            plugin.check_archive(self.root, self.archive)

    def test_unrelated_archive_files_are_rejected(self):
        plugin.pack(self.root, self.archive)
        with zipfile.ZipFile(self.archive, "a") as z:
            z.writestr("english-learning-tool/.env", "secret-marker")
        with self.assertRaisesRegex(plugin.CheckError, "archive_inventory_mismatch"):
            plugin.check_archive(self.root, self.archive)

    def test_symlink_is_not_packaged(self):
        (self.root / "skills/english-patterns/private.md").symlink_to(self.root / "LICENSE")
        with self.assertRaisesRegex(plugin.CheckError, "source_symlink"):
            plugin.pack(self.root, self.archive)

    def test_account_normalization_reports_paths_without_personal_values(self):
        data = self.readback()
        manifest = json.loads(data["contents"]["plugin.json"])
        manifest["author"] = {"name": "private-name-marker", "email": "private-email-marker@example.invalid"}
        manifest["extensions"]["com.openai"]["interface"]["developerName"] = "private-name-marker"
        data["contents"]["plugin.json"] = json.dumps(manifest)
        result = plugin.compare_account(self.root, data)
        self.assertTrue(result["ok"])
        self.assertEqual(len(result["account_normalizations"]), 3)
        self.assertNotIn("private-name-marker", json.dumps(result))
        self.assertNotIn("private-email-marker", json.dumps(result))

    def test_unexpected_fields_and_missing_components_fail_without_values(self):
        data = self.readback()
        manifest = json.loads(data["contents"]["plugin.json"])
        manifest["private-unknown-marker"] = "secret-marker"
        data["contents"]["plugin.json"] = json.dumps(manifest)
        del data["contents"]["LICENSE"]
        result = plugin.compare_account(self.root, data)
        self.assertFalse(result["ok"])
        self.assertIn("other_manifest_fields", result["manifest_differences"])
        self.assertEqual(result["component_mismatches"], 1)
        self.assertNotIn("marker", json.dumps(result))

    def test_support_file_named_plugin_json_is_compared(self):
        path = self.root / "skills/english-patterns/plugin.json"
        path.write_text('{"example": true}')
        data = self.readback()
        data["contents"]["skills/english-patterns/plugin.json"] = '{"example": false}'
        result = plugin.compare_account(self.root, data)
        self.assertFalse(result["ok"])
        self.assertEqual(result["component_mismatches"], 1)

    def test_real_cli_failure_does_not_echo_parser_input(self):
        (self.root / "plugin.json").write_text('{"private-email-marker@example.invalid":')
        result = subprocess.run([sys.executable, str(plugin.ROOT / "scripts/plugin.py"),
                                 "--root", str(self.root), "check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout), {"ok": False, "error": "json_invalid"})
        self.assertNotIn("private-email-marker", result.stdout + result.stderr)

    def test_account_source_has_unique_skill_names_without_changing_github_source(self):
        before = {p.relative_to(self.root): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        account = Path(self.temp.name) / "account"
        result = subprocess.run([sys.executable, str(plugin.ROOT / "scripts/plugin.py"),
                                 "--root", str(self.root), "account-source",
                                 "--version", "99.0.0", "--output", str(account)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        manifest, _, skills = plugin.check_sources(account)
        self.assertEqual(manifest["name"], "english-learning-tool")
        self.assertEqual(manifest["version"], "99.0.0")
        self.assertEqual(manifest["extensions"]["com.openai"]["interface"]["displayName"],
                         "English Learning Tool-alpha")
        self.assertEqual(set(skills), {"english-translator-alpha", "english-patterns-alpha",
                                      "english-back-translation-alpha"})
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes()
                                  for p in self.root.rglob("*") if p.is_file()})
        self.assertTrue(plugin.pack(account, self.archive)["ok"])

    def test_account_source_rejects_an_already_derived_account_package(self):
        account = Path(self.temp.name) / "account"
        command = [sys.executable, str(plugin.ROOT / "scripts/plugin.py")]
        first = subprocess.run(command + ["--root", str(self.root), "account-source",
                               "--version", "99.0.0", "--output", str(account)],
                               capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        second_output = Path(self.temp.name) / "second-account"
        second = subprocess.run(command + ["--root", str(account), "account-source",
                                "--version", "100.0.0", "--output", str(second_output)],
                                capture_output=True, text=True)
        self.assertNotEqual(second.returncode, 0)
        self.assertFalse(second_output.exists())


if __name__ == "__main__":
    unittest.main()
