# packaging/benford-lens-macos.spec
# -*- mode: python ; coding: utf-8 -*-
import tomllib
from pathlib import Path

project_root = Path(SPECPATH).resolve().parent
with (project_root / "pyproject.toml").open("rb") as project_file:
    package_version = tomllib.load(project_file)["project"]["version"]

# macOS requires a numeric CFBundleShortVersionString. Development suffixes remain
# represented by the source metadata while the app bundle uses its numeric release line.
bundle_version = package_version.split(".dev", maxsplit=1)[0]

a = Analysis(
    [str(project_root / "src" / "benford_lens" / "__main__.py")],
    pathex=[str(project_root / "src")],
    binaries=[],
    datas=[(str(project_root / "resources" / "i18n"), "resources/i18n")],
    hiddenimports=["matplotlib.backends.backend_qtagg"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="benford-lens",
    debug=False,
    strip=False,
    upx=True,
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name="benford-lens",
)
app = BUNDLE(
    coll,
    name="Benford Lens.app",
    icon=str(project_root / "resources" / "icons" / "macos" / "benford-lens.icns"),
    bundle_identifier="dev.benfordlens.app",
    version=bundle_version,
    info_plist={"CFBundleVersion": bundle_version},
)
