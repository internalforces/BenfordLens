"""Generate the checked-in Python distribution license bundle from the locked environment.

This maintenance script reads only local package metadata. It never opens a network connection.
The generated files are committed so normal source use and packaging remain offline.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "third_party_licenses"
LICENSE_BUNDLE = OUTPUT_DIR / "PYTHON_DISTRIBUTIONS.txt"
INVENTORY = OUTPUT_DIR / "PYTHON_DISTRIBUTIONS.json"

EXPECTED_DISTRIBUTIONS = {
    # Runtime on both packaged targets.
    "contourpy": "1.3.3",
    "cycler": "0.12.1",
    "et_xmlfile": "2.0.0",
    "fonttools": "4.63.0",
    "kiwisolver": "1.5.0",
    "matplotlib": "3.11.1",
    "numpy": "2.4.6",
    "openpyxl": "3.1.5",
    "packaging": "26.2",
    "pandas": "3.0.5",
    "pillow": "12.3.0",
    "pyparsing": "3.3.2",
    "pyside6_essentials": "6.11.1",
    "python-dateutil": "2.9.0.post0",
    "scipy": "1.17.1",
    "shiboken6": "6.11.1",
    "six": "1.17.0",
    # Packaging tools. They are documented even when their Python packages are not copied into
    # the application; the PyInstaller bootloader is part of the generated executable.
    "altgraph": "0.17.5",
    "pyinstaller": "6.21.0",
    "pyinstaller-hooks-contrib": "2026.6",
    "setuptools": "83.0.0",
}

# Installed only on one packaged target. Their notices are maintained separately so the inventory
# can be generated on macOS, Windows, or Linux CI without cross-installing wheels. License files
# embedded in native wheels may still contain platform-specific library paths.
PLATFORM_SPECIFIC_DISTRIBUTIONS = {
    "macholib": "1.16.4",
    "pefile": "2024.8.26",
    "pywin32-ctypes": "0.2.3",
    "tzdata": "2026.3",
}

_LICENSE_FILE = re.compile(r"(?i)(^|/)(?:license[^/]*|copying[^/]*|notice[^/]*)$")


def _distribution(name: str) -> importlib.metadata.Distribution:
    distribution = importlib.metadata.distribution(name)
    expected = EXPECTED_DISTRIBUTIONS[name]
    if distribution.version != expected:
        raise RuntimeError(
            f"{name} version mismatch: expected {expected}, found {distribution.version}"
        )
    return distribution


def _license_documents(
    distribution: importlib.metadata.Distribution,
) -> list[tuple[str, str]]:
    documents: list[tuple[str, str]] = []
    for entry in sorted(distribution.files or (), key=str):
        logical_path = str(entry)
        if not _LICENSE_FILE.search(logical_path):
            continue
        path = distribution.locate_file(entry)
        if not path.is_file():
            continue
        documents.append((logical_path, path.read_text(encoding="utf-8", errors="replace")))

    metadata_license = distribution.metadata.get("License") or ""
    if not documents and (len(metadata_license) >= 80 or "\n" in metadata_license):
        documents.append(("METADATA: License", metadata_license))
    return documents


def generate(output_dir: Path = OUTPUT_DIR) -> None:
    """Regenerate the deterministic bundle and source-file hash inventory."""
    output_dir.mkdir(parents=True, exist_ok=True)
    license_bundle = output_dir / LICENSE_BUNDLE.name
    inventory_path = output_dir / INVENTORY.name
    bundle_parts = [
        "Python distribution licenses for Benford Lens\n",
        "Generated from the exact local Python 3.11 lock environment.\n",
        "See THIRD_PARTY_NOTICES.md for scope, source availability, and Qt notices.\n",
    ]
    inventory: dict[str, object] = {
        "schema_version": 1,
        "python": "3.11",
        "distributions": [],
        "platform_specific_locked_distributions": PLATFORM_SPECIFIC_DISTRIBUTIONS,
    }

    for name in sorted(EXPECTED_DISTRIBUTIONS):
        distribution = _distribution(name)
        documents = _license_documents(distribution)
        canonical_name = distribution.metadata.get("Name") or name
        bundle_parts.append("\n" + "=" * 79 + "\n")
        bundle_parts.append(f"{canonical_name} {distribution.version}\n")
        bundle_parts.append("=" * 79 + "\n")

        document_inventory = []
        if not documents:
            expression = distribution.metadata.get("License-Expression")
            legacy = distribution.metadata.get("License")
            bundle_parts.append(
                "License metadata only; the applicable full text is provided by the manual "
                "license files named in THIRD_PARTY_NOTICES.md.\n"
            )
            bundle_parts.append(f"Metadata: {expression or legacy or 'not declared'}\n")
        for logical_path, text in documents:
            normalized = text.rstrip() + "\n"
            bundle_parts.append(f"\n--- {logical_path} ---\n\n{normalized}")
            document_inventory.append(
                {
                    "path": logical_path,
                    "sha256": hashlib.sha256(normalized.encode()).hexdigest(),
                }
            )

        inventory["distributions"].append(  # type: ignore[union-attr]
            {
                "name": canonical_name,
                "version": distribution.version,
                "license_expression": distribution.metadata.get("License-Expression"),
                "license_documents": document_inventory,
            }
        )

    bundle = "".join(bundle_parts)
    inventory["license_bundle_sha256"] = hashlib.sha256(bundle.encode()).hexdigest()
    license_bundle.write_text(bundle, encoding="utf-8", newline="\n")
    inventory_path.write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    generate(parser.parse_args().output_dir)
