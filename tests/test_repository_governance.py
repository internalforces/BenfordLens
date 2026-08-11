from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = PROJECT_ROOT / ".github" / "workflows"


def test_every_external_action_uses_a_full_commit_sha() -> None:
    uses_pattern = re.compile(r"^\s*(?:-\s*)?uses:\s*([^@\s]+)@([^\s#]+)", re.MULTILINE)
    found = []
    for workflow in WORKFLOW_DIR.glob("*.yml"):
        content = workflow.read_text(encoding="utf-8")
        for action, reference in uses_pattern.findall(content):
            found.append((action, reference))
            assert re.fullmatch(r"[0-9a-f]{40}", reference), (workflow.name, action, reference)
    assert found


def test_workflows_use_explicit_least_privilege_permissions() -> None:
    ci = (WORKFLOW_DIR / "ci.yml").read_text(encoding="utf-8")
    release = (WORKFLOW_DIR / "release.yml").read_text(encoding="utf-8")
    codeql = (WORKFLOW_DIR / "codeql.yml").read_text(encoding="utf-8")

    assert "permissions:\n  contents: read" in ci
    assert release.count("contents: write") == 1
    assert 'version: "latest"' not in release
    assert "permissions:\n  contents: read" in codeql
    assert "security-events: write" in codeql


def test_release_publisher_normalizes_nested_verified_assets() -> None:
    release = (WORKFLOW_DIR / "release.yml").read_text(encoding="utf-8")

    assert "find release-assets -type f -exec basename" in release
    assert 'source_path="$(find release-assets -type f -name "$filename" -print -quit)"' in release
    assert 'mv "$source_path" "$target_path"' in release
    assert "find release-assets -maxdepth 1 -type f -exec basename" not in release


def test_dependabot_covers_uv_and_github_actions() -> None:
    content = (PROJECT_ROOT / ".github" / "dependabot.yml").read_text(encoding="utf-8")
    assert 'package-ecosystem: "uv"' in content
    assert 'package-ecosystem: "github-actions"' in content
    assert content.count('interval: "weekly"') == 2


def test_release_and_workflow_paths_have_a_code_owner() -> None:
    content = (PROJECT_ROOT / ".github" / "CODEOWNERS").read_text(encoding="utf-8")
    for protected_path in (
        "/.github/workflows/",
        "/.github/release-notes/",
        "/.github/rulesets/",
        "/packaging/",
        "/third_party_licenses/",
        "/THIRD_PARTY_NOTICES.md",
    ):
        assert f"{protected_path} @internalforces" in content


def test_importable_rulesets_protect_main_and_release_tags() -> None:
    ruleset_dir = PROJECT_ROOT / ".github" / "rulesets"
    main = json.loads((ruleset_dir / "protect-main.json").read_text(encoding="utf-8"))
    tags = json.loads((ruleset_dir / "protect-release-tags.json").read_text(encoding="utf-8"))

    assert main["target"] == "branch"
    assert main["conditions"]["ref_name"]["include"] == ["~DEFAULT_BRANCH"]
    main_types = {rule["type"] for rule in main["rules"]}
    assert {"pull_request", "required_status_checks", "deletion", "non_fast_forward"} <= main_types
    status_rule = next(rule for rule in main["rules"] if rule["type"] == "required_status_checks")
    assert status_rule["parameters"]["required_status_checks"] == [{"context": "lint-type-test"}]

    assert tags["target"] == "tag"
    assert {rule["type"] for rule in tags["rules"]} == {"deletion", "non_fast_forward"}


def test_public_governance_and_package_metadata_are_complete() -> None:
    for filename in ("CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md", "SUPPORT.md"):
        content = (PROJECT_ROOT / filename).read_text(encoding="utf-8")
        assert content.strip()
        assert "dataset" in content.lower()

    project = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["project"]["license"] == "MIT"
    assert set(project["project"]["urls"]) == {
        "Homepage",
        "Repository",
        "Documentation",
        "Issues",
        "Changelog",
    }
