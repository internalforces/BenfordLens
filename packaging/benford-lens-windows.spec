# packaging/benford-lens-windows.spec
# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

project_root = Path(SPECPATH).resolve().parent

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
    icon=str(project_root / "resources" / "icons" / "windows" / "benford-lens.ico"),
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=True, name="benford-lens")
