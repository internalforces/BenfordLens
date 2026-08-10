[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$Version
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ($Version -notmatch '^\d+\.\d+\.\d+$') {
    throw "Release versions must contain exactly three numeric parts: $Version"
}

$packagingDirectory = Split-Path -Parent $PSCommandPath
$projectRoot = Split-Path -Parent $packagingDirectory
$pyprojectPath = Join-Path $projectRoot "pyproject.toml"
$versionMatch = Select-String -LiteralPath $pyprojectPath -Pattern '^version = "([^"]+)"$'
if (-not $versionMatch) {
    throw "Could not read the project version from pyproject.toml."
}
$projectVersion = $versionMatch.Matches[0].Groups[1].Value
if ($projectVersion -ne $Version) {
    throw "Release version $Version does not match pyproject.toml version $projectVersion."
}

$distDirectory = Join-Path $projectRoot "dist"
$appSource = Join-Path $distDirectory "benford-lens"
$archivePath = Join-Path $distDirectory "Benford-Lens-$Version-windows-x64.zip"
$archiveChecksumPath = "$archivePath.sha256"
$msiDirectory = Join-Path $distDirectory "msi"
$msiPath = Join-Path $msiDirectory "Benford-Lens-$Version-windows-x64.msi"
$msiChecksumPath = "$msiPath.sha256"

& (Join-Path $packagingDirectory "build-windows-msi.ps1") `
    -Version $Version `
    -OutputDirectory $msiDirectory `
    -InstallSmokeTest
if ($LASTEXITCODE -ne 0) {
    throw "The Windows MSI build failed with exit code $LASTEXITCODE."
}

if (Test-Path -LiteralPath $archivePath) {
    Remove-Item -LiteralPath $archivePath -Force
}
if (Test-Path -LiteralPath $archiveChecksumPath) {
    Remove-Item -LiteralPath $archiveChecksumPath -Force
}
Compress-Archive -LiteralPath $appSource -DestinationPath $archivePath -CompressionLevel Optimal

$extractDirectory = Join-Path `
    ([System.IO.Path]::GetTempPath()) `
    ("BenfordLensRelease-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $extractDirectory | Out-Null

$appProcess = $null
try {
    Expand-Archive -LiteralPath $archivePath -DestinationPath $extractDirectory
    $sourceExecutable = Join-Path $appSource "benford-lens.exe"
    $extractedExecutable = Join-Path $extractDirectory "benford-lens\benford-lens.exe"
    $extractedNotice = Join-Path $extractDirectory "benford-lens\THIRD_PARTY_NOTICES.md"
    if (-not (Test-Path -LiteralPath $extractedExecutable -PathType Leaf)) {
        throw "The extracted Windows executable is missing: $extractedExecutable"
    }
    if (-not (Test-Path -LiteralPath $extractedNotice -PathType Leaf)) {
        throw "The extracted third-party notice is missing: $extractedNotice"
    }

    $sourceHash = (Get-FileHash -LiteralPath $sourceExecutable -Algorithm SHA256).Hash
    $extractedHash = (Get-FileHash -LiteralPath $extractedExecutable -Algorithm SHA256).Hash
    if ($sourceHash -ne $extractedHash) {
        throw "The extracted executable hash does not match the build output."
    }

    $previousQtPlatform = $env:QT_QPA_PLATFORM
    $env:QT_QPA_PLATFORM = "offscreen"
    try {
        $appProcess = Start-Process `
            -FilePath $extractedExecutable `
            -PassThru `
            -WindowStyle Hidden
        Start-Sleep -Seconds 8
        $appProcess.Refresh()
        if ($appProcess.HasExited) {
            throw "The extracted application exited early with code $($appProcess.ExitCode)."
        }
    } finally {
        if ($null -eq $previousQtPlatform) {
            Remove-Item Env:QT_QPA_PLATFORM -ErrorAction SilentlyContinue
        } else {
            $env:QT_QPA_PLATFORM = $previousQtPlatform
        }
        if ($appProcess -and -not $appProcess.HasExited) {
            Stop-Process -Id $appProcess.Id -Force
            Wait-Process -Id $appProcess.Id -ErrorAction SilentlyContinue
        }
    }
} finally {
    Remove-Item -LiteralPath $extractDirectory -Recurse -Force -ErrorAction SilentlyContinue
}

$archiveHash = Get-FileHash -LiteralPath $archivePath -Algorithm SHA256
[System.IO.File]::WriteAllText(
    $archiveChecksumPath,
    "$($archiveHash.Hash)  $([System.IO.Path]::GetFileName($archivePath))`n",
    [System.Text.Encoding]::ASCII
)

foreach ($requiredPath in @($archivePath, $archiveChecksumPath, $msiPath, $msiChecksumPath)) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
        throw "The expected release asset is missing: $requiredPath"
    }
}

$executableSignature = Get-AuthenticodeSignature -LiteralPath `
    (Join-Path $appSource "benford-lens.exe")
$msiSignature = Get-AuthenticodeSignature -LiteralPath $msiPath

Write-Output "Archive: $archivePath"
Write-Output "Archive SHA-256: $($archiveHash.Hash)"
Write-Output "MSI: $msiPath"
Write-Output "Executable signature: $($executableSignature.Status)"
Write-Output "MSI signature: $($msiSignature.Status)"
Write-Output "ZIP extraction/startup smoke test: PASS"
Write-Output "MSI install/startup/uninstall smoke test: PASS"
