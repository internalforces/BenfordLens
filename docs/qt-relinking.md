# Replacing or Rebuilding the Qt Libraries

Benford Lens release packages use dynamically loaded Qt 6.11 libraries through PySide6 Essentials
6.11.1. This guide documents the package layout and practical replacement/rebuild path. It is not
legal advice and does not limit the rights provided by the GNU LGPLv3 or another applicable Qt
license.

## Source and notices

Start with [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md). The exact source tags, commits,
archive hash, third-party attributions, and license-text hashes are recorded under
`third_party_licenses/`. Benford Lens application source is available in this repository under the
MIT License.

## Rebuild from source

Use Python 3.11 on the target operating system:

```text
uv sync --frozen --group dev
```

The native packaging entry points are:

- macOS: `packaging/build-release-macos.sh`
- Windows ZIP/MSI: `packaging/build-release-windows.ps1`

The PyInstaller specifications are under `packaging/`. They keep Qt libraries separate and filter
unused Qt modules that Qt 6.11 lists as GPL-only for open-source users. A release build remains a
human-approved project operation; these instructions describe reproducibility and do not
authorize publication.

## Windows package layout

After extracting the portable ZIP, Qt libraries and plugins are under:

```text
benford-lens/_internal/PySide6/
```

Compatible rebuilt or modified Qt/PySide libraries can be placed in the corresponding paths while
the application is stopped. Keep the directory layout and the Qt/PySide ABI expected by the
application. Run `benford-lens.exe` from the extracted folder to test the replacement. The portable
ZIP is the simplest relinking test target because it does not require reinstalling the MSI.

## macOS package layout

After extracting the ZIP, use Finder's **Show Package Contents** command or inspect:

```text
Benford Lens.app/Contents/Frameworks/PySide6/
```

Replace compatible Qt frameworks/plugins in their corresponding paths while the application is
stopped. Modifying a library invalidates the bundle's existing ad-hoc integrity signature. After
replacement, create a new local ad-hoc signature before testing:

```text
codesign --force --deep --sign - "Benford Lens.app"
codesign --verify --deep --strict "Benford Lens.app"
```

The public package is not Developer ID signed or notarized, so this process does not remove a
trusted platform signature. macOS security policy may still require the same local approval steps
documented in the user guide.

## Installation information and restrictions

Benford Lens does not impose DRM or contractual restrictions on replacing the dynamically loaded
Qt libraries or studying their interaction with the application. A replacement must remain ABI-
compatible and may require rebuilding PySide/Shiboken together with Qt. The exact Qt for Python
source archive and Qt module tags are listed in the notices document.

If the checked-in instructions are insufficient for a particular release, open a GitHub issue
titled `Qt source request` after the repository becomes public and include the release version,
platform, and requested source or build detail.
