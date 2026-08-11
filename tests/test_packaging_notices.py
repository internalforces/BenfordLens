from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LICENSE_DIR = PROJECT_ROOT / "third_party_licenses"

RUNTIME_VERSIONS = {
    "contourpy": "1.3.3",
    "cycler": "0.12.1",
    "et-xmlfile": "2.0.0",
    "fonttools": "4.63.0",
    "kiwisolver": "1.5.0",
    "matplotlib": "3.11.1",
    "numpy": "2.4.6",
    "openpyxl": "3.1.5",
    "packaging": "26.2",
    "pandas": "3.0.5",
    "pillow": "12.3.0",
    "pyparsing": "3.3.2",
    "pyside6-essentials": "6.11.1",
    "python-dateutil": "2.9.0.post0",
    "scipy": "1.17.1",
    "shiboken6": "6.11.1",
    "six": "1.17.0",
    "tzdata": "2026.3",
}

REQUIRED_NOTICE_FILES = {
    "GPL-3.0.txt",
    "LGPL-3.0.txt",
    "PLATFORM_SPECIFIC_DISTRIBUTIONS.txt",
    "PYTHON-3.11.15.txt",
    "PYTHON_DISTRIBUTIONS.json",
    "PYTHON_DISTRIBUTIONS.txt",
    "QT_ATTRIBUTIONS.md",
    "QT_LICENSE_TEXTS.txt",
    "QT_SOURCES.json",
    "WIX-5.0.2-MS-RL.txt",
}

FORBIDDEN_QT_COMPONENTS = {
    "qtcanvaspainter",
    "qtcoap",
    "qtgraphs",
    "qtgrpc",
    "qthttpserver",
    "qtlottie",
    "qtmqtt",
    "qtnetworkauth",
    "qtqmlcompiler",
    "qtquick3d",
    "qtquicktimeline",
    "qtvirtualkeyboard",
    "qtwaylandcompositor",
}


def _lock_packages() -> dict[str, set[str]]:
    lock = tomllib.loads((PROJECT_ROOT / "uv.lock").read_text(encoding="utf-8"))
    versions: dict[str, set[str]] = {}
    for package in lock["package"]:
        if "version" in package:
            versions.setdefault(package["name"], set()).add(package["version"])
    return versions


def test_minimal_qt_runtime_excludes_addons_distribution() -> None:
    project = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = project["project"]["dependencies"]
    assert any(item.startswith("pyside6-essentials") for item in dependencies)
    assert not any(item.split(">=", maxsplit=1)[0] == "pyside6" for item in dependencies)

    packages = _lock_packages()
    assert packages["pyside6-essentials"] == {"6.11.1"}
    assert "pyside6" not in packages
    assert "pyside6-addons" not in packages


def test_runtime_inventory_matches_python_311_lock() -> None:
    packages = _lock_packages()
    for name, version in RUNTIME_VERSIONS.items():
        assert version in packages[name]

    notices = (PROJECT_ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8").lower()
    normalized_notices = re.sub(r"[^a-z0-9]+", " ", notices)
    for name, version in RUNTIME_VERSIONS.items():
        assert re.sub(r"[^a-z0-9]+", " ", name) in normalized_notices
        assert version in notices


def test_notice_files_are_present_and_nonempty() -> None:
    assert (PROJECT_ROOT / "THIRD_PARTY_NOTICES.md").stat().st_size > 0
    assert (PROJECT_ROOT / "docs" / "qt-relinking.md").stat().st_size > 0
    assert REQUIRED_NOTICE_FILES <= {path.name for path in LICENSE_DIR.iterdir()}
    for filename in REQUIRED_NOTICE_FILES:
        assert (LICENSE_DIR / filename).stat().st_size > 0


def _assert_bundle_matches_recorded_hash(directory: Path) -> None:
    inventory = json.loads((directory / "PYTHON_DISTRIBUTIONS.json").read_text())
    bundle = (directory / "PYTHON_DISTRIBUTIONS.txt").read_bytes()
    assert hashlib.sha256(bundle).hexdigest() == inventory["license_bundle_sha256"]


def test_python_license_bundle_is_reproducible(tmp_path: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "generate_third_party_licenses.py"),
            "--output-dir",
            str(tmp_path),
        ],
        check=True,
    )
    generated = json.loads((tmp_path / "PYTHON_DISTRIBUTIONS.json").read_text())
    checked_in = json.loads((LICENSE_DIR / "PYTHON_DISTRIBUTIONS.json").read_text())
    for key in ("schema_version", "python", "platform_specific_locked_distributions"):
        assert generated[key] == checked_in[key]

    generated_versions = {
        distribution["name"].lower().replace("_", "-"): distribution["version"]
        for distribution in generated["distributions"]
    }
    checked_in_versions = {
        distribution["name"].lower().replace("_", "-"): distribution["version"]
        for distribution in checked_in["distributions"]
    }
    assert generated_versions == checked_in_versions
    for distribution in generated["distributions"]:
        assert all(len(document["sha256"]) == 64 for document in distribution["license_documents"])
    _assert_bundle_matches_recorded_hash(tmp_path)
    _assert_bundle_matches_recorded_hash(LICENSE_DIR)

    # The checked-in canonical bundle was generated on macOS arm64. Native-wheel license files
    # can name platform-specific library directories, so exact bytes are meaningful only there.
    if sys.platform == "darwin":
        for filename in ("PYTHON_DISTRIBUTIONS.txt", "PYTHON_DISTRIBUTIONS.json"):
            assert (tmp_path / filename).read_bytes() == (LICENSE_DIR / filename).read_bytes()


def test_python_inventory_contains_source_hashes() -> None:
    inventory = json.loads((LICENSE_DIR / "PYTHON_DISTRIBUTIONS.json").read_text())
    assert inventory["schema_version"] == 1
    assert inventory["platform_specific_locked_distributions"] == {
        "macholib": "1.16.4",
        "pefile": "2024.8.26",
        "pywin32-ctypes": "0.2.3",
        "tzdata": "2026.3",
    }
    generated_names = {
        distribution["name"].lower().replace("_", "-")
        for distribution in inventory["distributions"]
    }
    assert generated_names.isdisjoint(inventory["platform_specific_locked_distributions"])
    for distribution in inventory["distributions"]:
        for document in distribution["license_documents"]:
            assert len(document["sha256"]) == 64


def test_platform_specific_license_notices_are_preserved() -> None:
    inventory = json.loads((LICENSE_DIR / "PYTHON_DISTRIBUTIONS.json").read_text())
    notices = (LICENSE_DIR / "PLATFORM_SPECIFIC_DISTRIBUTIONS.txt").read_text()
    for name, version in inventory["platform_specific_locked_distributions"].items():
        assert f"{name} {version}" in notices
    assert "Copyright 2006-2010 - Bob Ippolito" in notices
    assert "Copyright 2010-2020 - Ronald Oussoren" in notices


def test_qt_inventory_identifies_exact_sources_and_license_hashes() -> None:
    inventory = json.loads((LICENSE_DIR / "QT_SOURCES.json").read_text())
    assert inventory["schema_version"] == 1
    assert len(inventory["qt_license_texts"]) >= 39
    assert all(len(item["sha256"]) == 64 for item in inventory["qt_license_texts"])

    sources = inventory["qt_sources"]
    assert sum(item["attribution_records"] for item in sources) == 82
    repositories = {item.get("repository"): item for item in sources if "repository" in item}
    assert repositories["qt/qtbase"]["tag"] == "v6.11.1"
    assert len(repositories["qt/qtbase"]["commit"]) == 40
    assert repositories["qt/qtsvg"]["tag"] == "v6.11.1"
    archive = next(item for item in sources if "source_archive" in item)
    assert archive["version"] == "6.11.1"
    assert len(archive["sha256"]) == 64


def test_specs_package_notices_and_filter_gpl_only_qt_modules() -> None:
    for filename in ("benford-lens-macos.spec", "benford-lens-windows.spec"):
        content = (PROJECT_ROOT / "packaging" / filename).read_text(encoding="utf-8").lower()
        assert "third_party_notices.md" in content
        assert "third_party_licenses" in content
        assert "qt-relinking.md" in content
        assert "a.binaries = [entry for entry in a.binaries if allowed_qt_entry(entry)]" in content
        for component in FORBIDDEN_QT_COMPONENTS:
            assert component in content


def test_native_release_checks_enforce_notice_and_qt_policy() -> None:
    scripts = [
        PROJECT_ROOT / "packaging" / "build-release-macos.sh",
        PROJECT_ROOT / "packaging" / "build-windows-msi.ps1",
        PROJECT_ROOT / "packaging" / "build-release-windows.ps1",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in scripts)
    assert "third_party_notices.md" in combined
    assert "qt_license_texts.txt" in combined
    assert "virtualkeyboard" in combined
