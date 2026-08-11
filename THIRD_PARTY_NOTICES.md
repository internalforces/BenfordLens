# Third-Party Notices

Benford Lens is distributed under the MIT License, but its source and packaged desktop
applications use third-party software under other licenses. Those third-party terms continue to
apply to their respective components. This is an engineering inventory and notice, not legal
advice or a conclusion about every possible use or distribution model.

The complete offline notice set consists of this file and the files in `third_party_licenses/`.
Release packages place the same set inside the application bundle or installation directory. The
checked-in files are deliberate; incidental license files collected by PyInstaller are not treated
as the compliance record.

## Exact audited targets

- Python 3.11.15
- macOS arm64 and Windows x64
- `uv.lock` resolved for Python 3.11 on both target platforms
- Qt for Python / PySide6 Essentials 6.11.1 and Shiboken6 6.11.1
- Qt 6.11.1 dynamically loaded libraries used by the packaged application
- PyInstaller 6.21.0 and PyInstaller Hooks Contrib 2026.6
- WixToolset.Sdk 5.0.2 for the Windows MSI

`third_party_licenses/PYTHON_DISTRIBUTIONS.json` records hashes for the license files extracted
from the native locked environment. `third_party_licenses/QT_SOURCES.json` records the exact Qt
source tags, commits or source-archive hash, and license-text hashes.

## Runtime Python distributions

| Component | Version | Primary license or license family | Upstream source |
|---|---:|---|---|
| contourpy | 1.3.3 | BSD-3-Clause | <https://github.com/contourpy/contourpy> |
| cycler | 0.12.1 | BSD-3-Clause | <https://github.com/matplotlib/cycler> |
| et_xmlfile | 2.0.0 | MIT | <https://foss.heptapod.net/openpyxl/et_xmlfile> |
| fonttools | 4.63.0 | MIT plus bundled notices | <https://github.com/fonttools/fonttools> |
| kiwisolver | 1.5.0 | BSD-3-Clause | <https://github.com/nucleic/kiwi> |
| Matplotlib | 3.11.1 | Matplotlib license plus bundled software/font licenses | <https://github.com/matplotlib/matplotlib> |
| NumPy | 2.4.6 | BSD-3-Clause plus bundled component licenses | <https://github.com/numpy/numpy> |
| openpyxl | 3.1.5 | MIT | <https://foss.heptapod.net/openpyxl/openpyxl> |
| packaging | 26.2 | Apache-2.0 OR BSD-2-Clause | <https://github.com/pypa/packaging> |
| pandas | 3.0.5 | BSD-3-Clause plus bundled notices | <https://github.com/pandas-dev/pandas> |
| Pillow | 12.3.0 | MIT-CMU plus bundled codec/library licenses | <https://github.com/python-pillow/Pillow> |
| pyparsing | 3.3.2 | MIT | <https://github.com/pyparsing/pyparsing> |
| PySide6 Essentials | 6.11.1 | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only, or Qt commercial terms when separately obtained | <https://code.qt.io/cgit/pyside/pyside-setup.git/> |
| python-dateutil | 2.9.0.post0 | Apache-2.0 OR BSD-3-Clause | <https://github.com/dateutil/dateutil> |
| SciPy | 1.17.1 | BSD-3-Clause plus bundled native/component licenses | <https://github.com/scipy/scipy> |
| Shiboken6 | 6.11.1 | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only, or Qt commercial terms when separately obtained | <https://code.qt.io/cgit/pyside/pyside-setup.git/> |
| six | 1.17.0 | MIT | <https://github.com/benjaminp/six> |
| tzdata (Windows) | 2026.3 | Apache-2.0; timezone data retains its upstream status/notices | <https://github.com/python/tzdata> |

Full distribution license documents and copyright notices are reproduced in
`third_party_licenses/PYTHON_DISTRIBUTIONS.txt` and
`third_party_licenses/PLATFORM_SPECIFIC_DISTRIBUTIONS.txt`. In particular, the NumPy, SciPy,
Pillow, and Matplotlib sections reproduce their upstream bundled-component inventories rather than
reducing those packages to a single headline license.

## Python runtime and native libraries

The standalone applications include Python 3.11.15. Its license and incorporated-software notices
are reproduced in `third_party_licenses/PYTHON-3.11.15.txt`. The packaged runtime also contains
native components supplied by the Python and project dependency wheels:

| Native component group | Where the applicable notices are reproduced |
|---|---|
| OpenSSL (`libssl` / `libcrypto`) | Apache-2.0 text in `QT_LICENSE_TEXTS.txt`; source at <https://github.com/openssl/openssl> |
| SQLite | public-domain dedication/blessing in `QT_LICENSE_TEXTS.txt`; source at <https://sqlite.org/src/> |
| mpdecimal | Python-compatible permissive notices in the Python source distribution; source at <https://www.bytereef.org/mpdecimal/> |
| libffi (Windows Python runtime) | MIT-style upstream license; source at <https://github.com/libffi/libffi> |
| OpenBLAS/LAPACK and GCC runtime libraries used by NumPy/SciPy wheels | NumPy and SciPy sections of `PYTHON_DISTRIBUTIONS.txt`, including the GCC Runtime Library Exception |
| HiGHS, Qhull, Boost, SuperLU, ARPACK/PROPACK, PocketFFT, and other SciPy/NumPy components | exact upstream notices embedded in the NumPy/SciPy license sections and their copied license files |
| Pillow wheel codec/image libraries, including AOM, Brotli, bzip2, FreeType, HarfBuzz, JPEG, LittleCMS, OpenJPEG, PNG, TIFF, WebP, XZ/liblzma, and zlib | Pillow section of `PYTHON_DISTRIBUTIONS.txt` |
| Matplotlib rendering code and bundled DejaVu, STIX, Computer Modern/BaKoMa, and Last Resort fonts | Matplotlib section of `PYTHON_DISTRIBUTIONS.txt` |

Exact native filenames vary between macOS and Windows wheels. Native package verification records
the final file inventory and checks that every packaged notice file is present.

## Qt and PySide6 boundary

The project installs the Community Edition `PySide6_Essentials` and `shiboken6` wheels. Qt for
Python describes its Community Edition as available under LGPLv3/GPLv3 terms, while Qt also offers
commercial packages under separate terms. Benford Lens does not claim or grant a Qt commercial
license.

The application imports Qt Core, GUI, Widgets, and the Matplotlib Qt backend. Future packages:

- keep Qt shared libraries as separate `.dll`, `.dylib`, `.so`, or `.framework` files;
- include the LGPLv3 and GPLv3 texts and prominent Qt/PySide notices;
- include exact Qt third-party attributions and license texts;
- provide corresponding-source and replacement/relinking information; and
- deny package entries for Qt modules that Qt 6.11 lists as GPL-only for open-source users and
  that Benford Lens does not use.

The denylist includes Qt Canvas Painter, CoAP, Graphs, GRPC, HTTP Server, Lottie Animation, MQTT,
Network Authorization, QML Compiler, Quick 3D, Quick 3D Physics, Quick Timeline, Virtual Keyboard,
and Wayland Compositor. The previous private v1.0.0 package included unused Qt Virtual Keyboard
files; those assets are not approved for public exposure and will be superseded by the notice-
complete patch release.

The full GNU LGPLv3 and GPLv3 texts are in `third_party_licenses/LGPL-3.0.txt` and
`third_party_licenses/GPL-3.0.txt`. Exact Qt/PySide source and third-party records are in:

- `third_party_licenses/QT_SOURCES.json`;
- `third_party_licenses/QT_ATTRIBUTIONS.md`; and
- `third_party_licenses/QT_LICENSE_TEXTS.txt`.

Replacement and rebuild instructions are in `docs/qt-relinking.md`.

### Corresponding source availability

The audited source points are:

- Qt Base 6.11.1: <https://github.com/qt/qtbase/tree/v6.11.1>
- Qt SVG 6.11.1: <https://github.com/qt/qtsvg/tree/v6.11.1>
- Qt for Python / PySide and Shiboken 6.11.1 source archive:
  <https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.11.1-src/pyside-setup-everywhere-src-6.11.1.tar.xz>

For at least three years after a notice-complete Benford Lens binary release, the maintainer
offers to provide a copy of the exact corresponding Qt/PySide source used for that release at no
more than the reasonable cost of transferring it. After the repository becomes public, request it
through a GitHub issue titled `Qt source request` and identify the Benford Lens release and target
platform. This offer is intended to keep source availability under the distributor's control; it
does not replace or narrow any rights provided by the applicable license.

Qt's own guidance should be reviewed before redistribution:

- <https://www.qt.io/licensing/open-source-lgpl-obligations>
- <https://www.qt.io/faq/qt-open-source-licensing>
- <https://doc.qt.io/qt-6/licensing.html>
- <https://doc.qt.io/qtforpython-6/>

## Packaging and build tools

These tools participate in producing release artifacts. They are documented even when their
Python/.NET implementation is not copied into the installed application.

| Tool/component | Version | License | Notice location |
|---|---:|---|---|
| PyInstaller | 6.21.0 | GPL-2.0-or-later with the PyInstaller bootloader/bundling exception; selected files also Apache-2.0 | `PYTHON_DISTRIBUTIONS.txt` |
| PyInstaller Hooks Contrib | 2026.6 | GPL-2.0-or-later with applicable exception/notice | `PYTHON_DISTRIBUTIONS.txt` |
| altgraph | 0.17.5 | MIT | `PYTHON_DISTRIBUTIONS.txt` |
| macholib (macOS build) | 1.16.4 | MIT | `PLATFORM_SPECIFIC_DISTRIBUTIONS.txt` |
| pefile (Windows build) | 2024.8.26 | MIT | `PLATFORM_SPECIFIC_DISTRIBUTIONS.txt` |
| pywin32-ctypes (Windows build) | 0.2.3 | permissive upstream license | `PLATFORM_SPECIFIC_DISTRIBUTIONS.txt` |
| setuptools | 83.0.0 | MIT plus vendored notices | `PYTHON_DISTRIBUTIONS.txt` |
| WixToolset.Sdk | 5.0.2 | Microsoft Reciprocal License | `WIX-5.0.2-MS-RL.txt` |

PyInstaller's official documentation states that its exception permits distribution of generated
bundles under the application's license subject to dependency licenses. WiX 5.0.2 is used only as
the installer build tool; the exact tag's MS-RL text is reproduced for transparency.

## Verification and updates

Before a release is approved:

1. `uv lock --check` must pass for Python 3.11 on both native targets.
2. `scripts/generate_third_party_licenses.py` must reproduce the checked-in Python inventory from
   the exact locked environment.
3. automated notice tests must cover every runtime distribution and required license file;
4. packaged-file checks must find this notice set in the macOS app, Windows ZIP, and MSI source
   tree;
5. the forbidden Qt module scan must have no finding; and
6. native package inspection must reconcile final libraries/fonts with this inventory.

If a dependency, Python runtime, Qt module, font, native wheel, PyInstaller version, or WiX version
changes, regenerate and review this notice set before distributing new binaries.
