"""Check and package this skills collection; report account differences without values."""

import argparse
import copy
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import zipfile

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
SLUG = r"[a-z0-9]+(?:[.-][a-z0-9]+)*"
PRERELEASE = r"(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
SEMVER = (r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
          + rf"(?:-{PRERELEASE}(?:\.{PRERELEASE})*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?")


class CheckError(Exception):
    """A fixed error code, with no source values or parser excerpts."""


def require(condition, code):
    if not condition:
        raise CheckError(code)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "json_duplicate_key")
        result[key] = value
    return result


def parse_json(text):
    try:
        result = json.loads(text, object_pairs_hook=unique_object)
    except (ValueError, UnicodeError):
        raise CheckError("json_invalid") from None
    require(isinstance(result, dict), "json_object_required")
    return result


class UniqueSafeLoader(yaml.SafeLoader):
    pass


def yaml_mapping(loader, node):
    loader.flatten_mapping(node)
    return unique_yaml_object(loader.construct_pairs(node))


def unique_yaml_object(pairs):
    result = {}
    for key, value in pairs:
        require(isinstance(key, str), "frontmatter_string_keys_required")
        require(key not in result, "frontmatter_duplicate_key")
        result[key] = value
    return result


UniqueSafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, yaml_mapping)


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def check_skill(path):
    require(path.stat().st_size <= 1024 * 1024, "skill_too_large")
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)(.*)\Z", text, re.S)
    require(match is not None, "frontmatter_missing")
    try:
        data = yaml.load(match[1], Loader=UniqueSafeLoader)
    except yaml.YAMLError:
        raise CheckError("frontmatter_invalid") from None
    require(isinstance(data, dict), "frontmatter_mapping_required")
    require(data.get("name") == path.parent.name, "skill_name_mismatch")
    require(nonblank(data.get("description")), "skill_description_required")
    require(nonblank(match[2]), "skill_body_required")


def check_sources(root):
    require(not root.is_symlink(), "source_symlink")
    for path in (root / "plugin.json", root / "LICENSE", root / "skills"):
        require(path.exists() and not path.is_symlink(), "component_missing_or_symlink")
    manifest = parse_json((root / "plugin.json").read_bytes())
    require(manifest.get("$schema") == SCHEMA, "manifest_schema")
    require(isinstance(manifest.get("name"), str) and len(manifest["name"]) <= 64
            and re.fullmatch(SLUG, manifest["name"]), "manifest_name")
    require(isinstance(manifest.get("version"), str)
            and re.fullmatch(SEMVER, manifest["version"]), "manifest_version")
    require(nonblank(manifest.get("description")), "manifest_description")
    require(isinstance(manifest.get("author"), dict)
            and nonblank(manifest["author"].get("name")), "manifest_author")
    interface = manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})
    require(isinstance(interface, dict), "manifest_interface")
    for field in ("displayName", "shortDescription", "longDescription", "developerName"):
        require(nonblank(interface.get(field)), "interface_text_required")
    require(len(interface["shortDescription"]) <= 30, "interface_subtitle_too_long")
    require(isinstance(interface.get("capabilities"), list)
            and all(nonblank(item) for item in interface["capabilities"]), "interface_capabilities")
    if "defaultPrompt" in interface:
        prompts = interface["defaultPrompt"]
        require(nonblank(prompts) or (isinstance(prompts, list) and 1 <= len(prompts) <= 3
                and all(nonblank(p) for p in prompts)), "interface_prompts")
    legacy = parse_json((root / ".claude-plugin/plugin.json").read_bytes())
    require(all(manifest.get(k) == legacy.get(k) for k in
                ("name", "version", "description", "license", "author")), "legacy_metadata_mismatch")
    for catalog_path in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
        catalog = parse_json((root / catalog_path).read_bytes())
        plugins = catalog.get("plugins", [])
        require(len(plugins) == 1 and plugins[0].get("name") == manifest["name"], "catalog_plugin_mismatch")
        source = plugins[0].get("source")
        require(source == "./" or source == {"source": "local", "path": "./"}, "catalog_source_mismatch")
        if "metadata" in catalog:
            require(catalog["metadata"].get("description") == manifest["description"], "catalog_description_mismatch")
    files = [root / "plugin.json", root / "LICENSE"]
    skills = []
    for path in sorted((root / "skills").rglob("*")):
        require(not path.is_symlink(), "source_symlink")
        require(not path.name.startswith("."), "hidden_skill_component")
        if path.is_file():
            files.append(path)
            if path.name == "SKILL.md":
                require(path.parent.parent == root / "skills"
                        and re.fullmatch(SLUG, path.parent.name), "skill_location")
                check_skill(path)
                skills.append(path.parent.name)
    require(bool(skills), "skills_missing")
    require(all((p / "SKILL.md").is_file() for p in (root / "skills").iterdir()
                if p.is_dir()), "skill_entrypoint_missing")
    return manifest, files, skills


def check_archive(root, archive):
    manifest, files, skills = check_sources(root)
    expected = {manifest["name"] + "/" + p.relative_to(root).as_posix(): p for p in files}
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)), "archive_duplicate_path")
        require(set(names) == set(expected), "archive_inventory_mismatch")
        for info in infos:
            parts = PurePosixPath(info.filename)
            require(not parts.is_absolute() and ".." not in parts.parts, "archive_unsafe_path")
            require(not stat.S_ISLNK(info.external_attr >> 16), "archive_symlink")
            source = expected[info.filename]
            require(info.file_size == source.stat().st_size, "archive_stale_content")
            data = z.read(info)
            if info.filename.endswith("/plugin.json"):
                parse_json(data)
            require(data == source.read_bytes(), "archive_stale_content")
    return {"ok": True, "checks": "sources_and_archive", "files": len(files), "skills": len(skills)}


def pack(root, output):
    manifest, files, _ = check_sources(root)
    require(not output.resolve().is_relative_to(root.resolve()), "archive_must_be_outside_source")
    require(not output.exists(), "archive_output_exists")
    with zipfile.ZipFile(output, "x", zipfile.ZIP_DEFLATED) as z:
        for path in files:
            z.write(path, manifest["name"] + "/" + path.relative_to(root).as_posix())
    return check_archive(root, output)


def account_source(root, output, version):
    """Derive an alpha package without editing the shared GitHub source."""
    manifest, files, skills = check_sources(root)
    require(not manifest["extensions"]["com.openai"]["interface"]["displayName"].endswith("-alpha")
            and not any(name.endswith("-alpha") for name in skills), "account_source_requires_canonical")
    require(re.fullmatch(SEMVER, version), "manifest_version")
    require(not output.exists(), "account_source_output_exists")
    if output.resolve().is_relative_to(root.resolve()):
        relative = output.resolve().relative_to(root.resolve())
        require(relative.parts and relative.parts[0] == ".acceptance-local",
                "account_source_must_be_private")
    metadata = [root / name for name in (".claude-plugin/plugin.json",
                ".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json")]
    require(all(p.is_file() and not p.is_symlink() for p in metadata), "source_symlink")
    output.mkdir(parents=True)
    for path in files + metadata:
        relative = path.relative_to(root)
        parts = list(relative.parts)
        if parts[0] == "skills":
            parts[1] += "-alpha"
        target = output.joinpath(*parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative.parts[0] == "skills" and path.name == "SKILL.md":
            text = path.read_text(encoding="utf-8")
            match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)(.*)\Z", text, re.S)
            data = yaml.load(match[1], Loader=UniqueSafeLoader)
            data["name"] = parts[1]
            target.write_text("---\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
                              + "---\n" + match[2], encoding="utf-8")
        else:
            shutil.copy2(path, target)
    manifest["version"] = version
    interface = manifest["extensions"]["com.openai"]["interface"]
    interface["displayName"] += "-alpha"
    (output / "plugin.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    legacy_path = output / ".claude-plugin/plugin.json"
    legacy = parse_json(legacy_path.read_bytes())
    legacy["version"] = version
    legacy_path.write_text(json.dumps(legacy, ensure_ascii=False, indent=2) + "\n")
    _, packaged, skills = check_sources(output)
    return {"ok": True, "version": version, "files": len(packaged), "skills": len(skills)}


def compare_account(root, readback):
    """Only fixed field paths and counts reach stdout; values stay in the input file."""
    local, files, _ = check_sources(root)
    require(readback.get("next_offset") is None, "account_inventory_incomplete")
    require(not readback.get("missing_paths") and not readback.get("size_limited_paths"), "account_read_incomplete")
    contents = readback.get("contents", {})
    require(isinstance(contents, dict) and "plugin.json" in contents, "account_manifest_missing")
    remote = parse_json(contents["plugin.json"])
    normalized = copy.deepcopy(remote)
    normalizations = []
    for field in ("name", "email"):
        old = normalized.get("author", {})
        new = local.get("author", {})
        if (field in old) != (field in new) or old.get(field) != new.get(field):
            normalizations.append("author." + field)
            if field in new:
                old[field] = new[field]
            else:
                old.pop(field, None)
    local_ui = local["extensions"]["com.openai"]["interface"]
    remote_ui = normalized.get("extensions", {}).get("com.openai", {}).get("interface", {})
    if remote_ui.get("developerName") != local_ui["developerName"]:
        normalizations.append("extensions.com.openai.interface.developerName")
        remote_ui["developerName"] = local_ui["developerName"]
    differences = []
    known = {"$schema", "name", "version", "description", "license", "author", "extensions"}
    for field in sorted(known):
        if normalized.get(field) != local.get(field) or (field in normalized) != (field in local):
            differences.append(field)
    if {k: v for k, v in normalized.items() if k not in known} != {k: v for k, v in local.items() if k not in known}:
        differences.append("other_manifest_fields")
    expected = {p.relative_to(root).as_posix() for p in files}
    inventory = {item["path"] for item in readback.get("files", [])}
    inventory_ok = inventory in (expected, expected | {".codex-plugin/plugin.json"})
    component_mismatches = sum(contents.get(p.relative_to(root).as_posix()) != p.read_text(encoding="utf-8")
                               for p in files if p.relative_to(root).as_posix() != "plugin.json")
    if ".codex-plugin/plugin.json" in inventory:
        require(".codex-plugin/plugin.json" in contents, "account_overlay_missing")
        overlay = parse_json(contents[".codex-plugin/plugin.json"])
        expected_overlay = {key: remote[key]
                            for key in ("name", "version", "description", "author", "license")}
        interface = copy.deepcopy(remote["extensions"]["com.openai"]["interface"])
        interface.setdefault("category", "Other")
        interface.setdefault("defaultPrompt", None)
        expected_overlay.update(interface=interface, keywords=remote.get("keywords", []),
                                skills="./skills")
        if overlay != expected_overlay:
            differences.append("compatibility_manifest")
    return {"ok": not differences and inventory_ok and component_mismatches == 0,
            "manifest_differences": differences, "account_normalizations": normalizations,
            "inventory_matches": inventory_ok, "component_mismatches": component_mismatches}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check")
    check.add_argument("--archive", type=Path)
    package = sub.add_parser("pack")
    package.add_argument("--output", type=Path, required=True)
    account = sub.add_parser("compare-account")
    account.add_argument("--readback", type=Path, required=True)
    source = sub.add_parser("account-source")
    source.add_argument("--output", type=Path, required=True)
    source.add_argument("--version", required=True)
    args = parser.parse_args()
    try:
        if args.command == "account-source":
            result = account_source(args.root, args.output, args.version)
        elif args.command == "pack":
            result = pack(args.root, args.output)
        elif args.command == "compare-account":
            result = compare_account(args.root, parse_json(args.readback.read_bytes()))
        elif args.archive:
            result = check_archive(args.root, args.archive)
        else:
            _, files, skills = check_sources(args.root)
            result = {"ok": True, "checks": "sources", "files": len(files), "skills": len(skills)}
    except CheckError as error:
        result = {"ok": False, "error": str(error)}
    except (OSError, ValueError, UnicodeError, TypeError, KeyError, AttributeError, zipfile.BadZipFile, RuntimeError):
        result = {"ok": False, "error": "input_unreadable_or_invalid"}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
