#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
version="${1:-}"

if [[ ! "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Usage: $0 <major.minor.patch>" >&2
    exit 1
fi

project_version="$({
    sed -n 's/^version = "\([^"]*\)"$/\1/p' "$project_root/pyproject.toml"
} | head -n 1)"
if [[ "$project_version" != "$version" ]]; then
    echo "Release version $version does not match pyproject.toml version $project_version." >&2
    exit 1
fi

dist_dir="$project_root/dist"
app_path="$dist_dir/Benford Lens.app"
archive_path="$dist_dir/Benford-Lens-$version-macOS-arm64.zip"
checksum_path="$archive_path.sha256"
executable_relative="Benford Lens.app/Contents/MacOS/benford-lens"
work_dir="$project_root/build/release-macos"
extract_dir="$(mktemp -d)"
log_file="$(mktemp)"
forbidden_qt_pattern='qt(canvaspainter|coap|graphs|grpc|httpserver|lottie|mqtt|networkauth|qmlcompiler|quick3d|quicktimeline|virtualkeyboard|waylandcompositor)'

if command -v uv >/dev/null 2>&1; then
    pyinstaller=(uv run pyinstaller)
elif [[ -x "$project_root/.venv/bin/pyinstaller" ]]; then
    pyinstaller=("$project_root/.venv/bin/pyinstaller")
else
    echo "PyInstaller is unavailable. Run 'uv sync --locked --group dev' first." >&2
    exit 1
fi

cleanup() {
    rm -rf "$extract_dir"
    rm -f "$log_file"
}
trap cleanup EXIT

run_startup_smoke_test() {
    local executable="$1"
    QT_QPA_PLATFORM=offscreen "$executable" >"$log_file" 2>&1 &
    local app_pid=$!
    sleep 8
    if ! kill -0 "$app_pid" 2>/dev/null; then
        wait "$app_pid" || true
        cat "$log_file" >&2
        echo "The packaged application exited before the 8-second smoke interval." >&2
        return 1
    fi
    kill "$app_pid"
    wait "$app_pid" 2>/dev/null || true
}

verify_notice_bundle() {
    local resources_path="$1"
    local required_path
    for required_path in \
        "$resources_path/THIRD_PARTY_NOTICES.md" \
        "$resources_path/docs/qt-relinking.md" \
        "$resources_path/third_party_licenses/GPL-3.0.txt" \
        "$resources_path/third_party_licenses/LGPL-3.0.txt" \
        "$resources_path/third_party_licenses/PYTHON_DISTRIBUTIONS.txt" \
        "$resources_path/third_party_licenses/QT_ATTRIBUTIONS.md" \
        "$resources_path/third_party_licenses/QT_LICENSE_TEXTS.txt"; do
        if [[ ! -s "$required_path" ]]; then
            echo "Required packaged notice is missing or empty: $required_path" >&2
            return 1
        fi
    done
}

verify_forbidden_qt_modules_absent() {
    local bundle_path="$1"
    local findings
    findings="$(find "$bundle_path" -type f -print | grep -Ei "$forbidden_qt_pattern" || true)"
    if [[ -n "$findings" ]]; then
        echo "Unused GPL-only Qt module files were packaged:" >&2
        echo "$findings" >&2
        return 1
    fi
}

cd "$project_root"
if [[ -d "$project_root/.venv" ]]; then
    chflags -R nohidden "$project_root/.venv"
fi
"${pyinstaller[@]}" packaging/benford-lens-macos.spec \
    --distpath "$dist_dir" \
    --workpath "$work_dir" \
    --noconfirm

bundle_version="$(/usr/libexec/PlistBuddy \
    -c 'Print :CFBundleShortVersionString' "$app_path/Contents/Info.plist")"
build_version="$(/usr/libexec/PlistBuddy \
    -c 'Print :CFBundleVersion' "$app_path/Contents/Info.plist")"
if [[ "$bundle_version" != "$version" || "$build_version" != "$version" ]]; then
    echo "Unexpected macOS bundle versions: $bundle_version / $build_version" >&2
    exit 1
fi

architectures="$(lipo -archs "$app_path/Contents/MacOS/benford-lens")"
if [[ "$architectures" != "arm64" ]]; then
    echo "Expected an arm64 application, got: $architectures" >&2
    exit 1
fi

translation_count="$(find "$app_path/Contents/Resources/resources/i18n" \
    -maxdepth 1 -name '*.qm' -type f | wc -l | tr -d ' ')"
if [[ "$translation_count" != "6" ]]; then
    echo "Expected six compiled translation catalogs, found $translation_count." >&2
    exit 1
fi

verify_notice_bundle "$app_path/Contents/Resources"
verify_forbidden_qt_modules_absent "$app_path"

xattr -cr "$app_path"
codesign --sign - --force --all-architectures --timestamp --deep "$app_path"
codesign --verify --deep --strict "$app_path"
run_startup_smoke_test "$app_path/Contents/MacOS/benford-lens"

rm -f "$archive_path" "$checksum_path"
ditto -c -k --sequesterRsrc --keepParent "$app_path" "$archive_path"
ditto -x -k "$archive_path" "$extract_dir"

codesign --verify --deep --strict "$extract_dir/Benford Lens.app"
verify_notice_bundle "$extract_dir/Benford Lens.app/Contents/Resources"
verify_forbidden_qt_modules_absent "$extract_dir/Benford Lens.app"
run_startup_smoke_test "$extract_dir/$executable_relative"

(
    cd "$dist_dir"
    shasum -a 256 "$(basename "$archive_path")" >"$(basename "$checksum_path")"
)

echo "Archive: $archive_path"
echo "Checksum: $checksum_path"
echo "Architecture: $architectures"
echo "Signature: ad-hoc integrity verified (not Developer ID/notarized)"
echo "Startup smoke test: PASS"
