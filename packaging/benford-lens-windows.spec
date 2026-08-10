# packaging/benford-lens-windows.spec
# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

project_root = Path(SPECPATH).resolve().parent

forbidden_qt_components = (
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
)


def allowed_qt_entry(entry):
    """Exclude unused Qt modules that Qt 6.11 lists as GPL-only for open-source users."""
    searchable = " ".join(str(part) for part in entry[:2]).lower()
    return not any(component in searchable for component in forbidden_qt_components)

a = Analysis(
    [str(project_root / "src" / "benford_lens" / "__main__.py")],
    pathex=[str(project_root / "src")],
    binaries=[],
    datas=[
        (str(project_root / "resources" / "i18n"), "resources/i18n"),
        (str(project_root / "THIRD_PARTY_NOTICES.md"), "."),
        (str(project_root / "third_party_licenses"), "third_party_licenses"),
        (str(project_root / "docs" / "qt-relinking.md"), "docs"),
    ],
    hiddenimports=["matplotlib.backends.backend_qtagg"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "PySide6.QtCanvasPainter",
        "PySide6.QtCoap",
        "PySide6.QtGraphs",
        "PySide6.QtGraphsWidgets",
        "PySide6.QtGrpc",
        "PySide6.QtHttpServer",
        "PySide6.QtLottie",
        "PySide6.QtMqtt",
        "PySide6.QtNetworkAuth",
        "PySide6.QtQmlCompiler",
        "PySide6.QtQuick3D",
        "PySide6.QtQuickTimeline",
        "PySide6.QtVirtualKeyboard",
        "PySide6.QtWaylandCompositor",
    ],
    noarchive=False,
)
a.binaries = [entry for entry in a.binaries if allowed_qt_entry(entry)]
a.datas = [entry for entry in a.datas if allowed_qt_entry(entry)]
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
