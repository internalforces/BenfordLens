[CmdletBinding()]
param(
    [string]$Version,
    [string]$AppSource,
    [string]$OutputDirectory,
    [switch]$SkipPyInstaller,
    [switch]$InstallSmokeTest
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$env:DOTNET_CLI_TELEMETRY_OPTOUT = "1"
$env:DOTNET_NOLOGO = "1"
$env:DOTNET_SKIP_FIRST_TIME_EXPERIENCE = "1"

$packagingDirectory = Split-Path -Parent $PSCommandPath
$projectRoot = Split-Path -Parent $packagingDirectory

if ($env:OS -ne "Windows_NT") {
    throw "The Windows MSI can only be built on Windows."
}

if ([string]::IsNullOrWhiteSpace($Version)) {
    $pyprojectPath = Join-Path $projectRoot "pyproject.toml"
    $versionMatch = Select-String -LiteralPath $pyprojectPath -Pattern '^version = "([^\"]+)"$'
    if (-not $versionMatch) {
        throw "Could not read the project version from pyproject.toml."
    }
    $Version = $versionMatch.Matches[0].Groups[1].Value
}

if ($Version -notmatch '^\d+\.\d+\.\d+$') {
    throw "MSI versions must contain exactly three numeric parts: $Version"
}

if ([string]::IsNullOrWhiteSpace($AppSource)) {
    $AppSource = Join-Path $projectRoot "dist\benford-lens"
}
if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
    $OutputDirectory = Join-Path $projectRoot "dist\msi"
}

$AppSource = [System.IO.Path]::GetFullPath($AppSource)
$OutputDirectory = [System.IO.Path]::GetFullPath($OutputDirectory)
$iconPath = Join-Path $projectRoot "resources\icons\windows\benford-lens.ico"
$wixProject = Join-Path $packagingDirectory "benford-lens-installer.wixproj"
$pyInstaller = Join-Path $projectRoot ".venv\Scripts\pyinstaller.exe"

if (-not $SkipPyInstaller) {
    if (-not (Test-Path -LiteralPath $pyInstaller -PathType Leaf)) {
        throw "PyInstaller was not found at $pyInstaller. Run uv sync --group dev first."
    }
    & $pyInstaller `
        (Join-Path $packagingDirectory "benford-lens-windows.spec") `
        --distpath (Join-Path $projectRoot "dist") `
        --workpath (Join-Path $projectRoot "build\windows") `
        --noconfirm
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller failed with exit code $LASTEXITCODE."
    }
}

$mainExecutable = Join-Path $AppSource "benford-lens.exe"
if (-not (Test-Path -LiteralPath $mainExecutable -PathType Leaf)) {
    throw "The PyInstaller application was not found at $mainExecutable."
}
if (-not (Test-Path -LiteralPath $iconPath -PathType Leaf)) {
    throw "The Windows application icon was not found at $iconPath."
}

$dotnetCommand = Get-Command dotnet -ErrorAction SilentlyContinue
if ($dotnetCommand) {
    $dotnet = $dotnetCommand.Source
} else {
    $dotnetCandidates = @(
        (Join-Path $env:ProgramFiles "dotnet\dotnet.exe"),
        (Join-Path $env:LOCALAPPDATA "Microsoft\dotnet\dotnet.exe"),
        (Join-Path $env:LOCALAPPDATA "BenfordLensBuildTools\dotnet\dotnet.exe")
    )
    $dotnet = $dotnetCandidates | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } |
        Select-Object -First 1
}
if (-not $dotnet) {
    throw ".NET 8 SDK was not found. Install it before building the WiX installer."
}

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$intermediateDirectory = Join-Path $projectRoot "build\msi"
New-Item -ItemType Directory -Path $intermediateDirectory -Force | Out-Null

& $dotnet build $wixProject `
    --configuration Release `
    --nologo `
    "-p:AppVersion=$Version" `
    "-p:AppSource=$AppSource" `
    "-p:AppIcon=$iconPath" `
    "-p:OutputPath=$OutputDirectory\" `
    "-p:BaseIntermediateOutputPath=$intermediateDirectory\" `
    "-p:IntermediateOutputPath=$intermediateDirectory\Release\"
if ($LASTEXITCODE -ne 0) {
    throw "WiX failed with exit code $LASTEXITCODE."
}

$msiPath = Join-Path $OutputDirectory "Benford-Lens-$Version-windows-x64.msi"
if (-not (Test-Path -LiteralPath $msiPath -PathType Leaf)) {
    throw "WiX completed without producing the expected MSI: $msiPath"
}

$installer = New-Object -ComObject WindowsInstaller.Installer
$database = $installer.OpenDatabase($msiPath, 0)

function Get-MsiProperty {
    param([Parameter(Mandatory)][string]$Name)

    $query = "SELECT ``Value`` FROM ``Property`` WHERE ``Property``='$Name'"
    $view = $database.OpenView($query)
    $view.Execute() | Out-Null
    $record = $view.Fetch()
    if (-not $record) {
        return $null
    }
    return $record.StringData(1)
}

$expectedProperties = @{
    ProductName = "Benford Lens"
    ProductVersion = $Version
    Manufacturer = "Benford Lens"
    UpgradeCode = "{A256B439-D3D1-4538-B385-7DFAA4F5E283}"
    ARPNOMODIFY = "1"
}
foreach ($property in $expectedProperties.GetEnumerator()) {
    $actualValue = Get-MsiProperty -Name $property.Key
    if ($actualValue -ne $property.Value) {
        throw "Unexpected MSI $($property.Key): expected '$($property.Value)', got '$actualValue'."
    }
}
if ($null -ne (Get-MsiProperty -Name "ALLUSERS")) {
    throw "The MSI must remain a per-user package without an ALLUSERS property."
}

$fileView = $database.OpenView("SELECT ``File`` FROM ``File``")
$fileView.Execute() | Out-Null
$msiFileCount = 0
while ($fileView.Fetch()) {
    $msiFileCount++
}
$sourceFileCount = @(Get-ChildItem -LiteralPath $AppSource -File -Recurse).Count
if ($msiFileCount -ne $sourceFileCount) {
    throw "MSI file count $msiFileCount does not match source file count $sourceFileCount."
}

$signature = Get-AuthenticodeSignature -LiteralPath $msiPath
$hash = Get-FileHash -LiteralPath $msiPath -Algorithm SHA256
$checksumPath = "$msiPath.sha256"
"$($hash.Hash)  $([System.IO.Path]::GetFileName($msiPath))" |
    Set-Content -LiteralPath $checksumPath -Encoding ascii

Write-Output "MSI: $msiPath"
Write-Output "SHA-256: $($hash.Hash)"
Write-Output "Signature: $($signature.Status)"
Write-Output "Packaged files: $msiFileCount"

if ($InstallSmokeTest) {
    $installRoot = Join-Path $env:LOCALAPPDATA "Programs\Benford Lens"
    $shortcutRoot = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Benford Lens"
    $installerMarker = "HKCU:\Software\BenfordLens"
    if (
        (Test-Path -LiteralPath $installRoot) -or
        (Test-Path -LiteralPath $shortcutRoot) -or
        (Test-Path -LiteralPath $installerMarker)
    ) {
        throw "A Benford Lens installation already exists; refusing to overwrite it during testing."
    }

    $installLog = Join-Path $intermediateDirectory "install-smoke.log"
    $uninstallLog = Join-Path $intermediateDirectory "uninstall-smoke.log"
    $installArguments = @(
        "/i",
        ('"' + $msiPath + '"'),
        "/qn",
        "/norestart",
        "/l*v",
        ('"' + $installLog + '"')
    )
    $installProcess = Start-Process `
        -FilePath "msiexec.exe" `
        -ArgumentList $installArguments `
        -Wait `
        -PassThru `
        -WindowStyle Hidden
    if ($installProcess.ExitCode -ne 0) {
        throw "MSI install smoke test failed with exit code $($installProcess.ExitCode). See $installLog"
    }

    $appProcess = $null
    try {
        $installedExecutable = Join-Path $installRoot "benford-lens.exe"
        $shortcut = Join-Path $shortcutRoot "Benford Lens.lnk"
        if (-not (Test-Path -LiteralPath $installedExecutable -PathType Leaf)) {
            throw "The installed executable is missing: $installedExecutable"
        }
        if (-not (Test-Path -LiteralPath $shortcut -PathType Leaf)) {
            throw "The installed Start menu shortcut is missing: $shortcut"
        }
        $installedFileCount = @(Get-ChildItem -LiteralPath $installRoot -File -Recurse).Count
        if ($installedFileCount -ne $sourceFileCount) {
            throw "Installed file count $installedFileCount does not match source file count $sourceFileCount."
        }

        $previousQtPlatform = $env:QT_QPA_PLATFORM
        $env:QT_QPA_PLATFORM = "offscreen"
        try {
            $appProcess = Start-Process `
                -FilePath $installedExecutable `
                -PassThru `
                -WindowStyle Hidden
            Start-Sleep -Seconds 8
            $appProcess.Refresh()
            if ($appProcess.HasExited) {
                throw "The installed application exited early with code $($appProcess.ExitCode)."
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
        $uninstallArguments = @(
            "/x",
            ('"' + $msiPath + '"'),
            "/qn",
            "/norestart",
            "/l*v",
            ('"' + $uninstallLog + '"')
        )
        $uninstallProcess = Start-Process `
            -FilePath "msiexec.exe" `
            -ArgumentList $uninstallArguments `
            -Wait `
            -PassThru `
            -WindowStyle Hidden
        if ($uninstallProcess.ExitCode -ne 0) {
            throw "MSI uninstall smoke test failed with exit code $($uninstallProcess.ExitCode). See $uninstallLog"
        }
    }

    if (
        (Test-Path -LiteralPath $installRoot) -or
        (Test-Path -LiteralPath $shortcutRoot) -or
        (Test-Path -LiteralPath $installerMarker)
    ) {
        throw "MSI uninstall smoke test left Benford Lens files or registry data behind."
    }
    Write-Output "Install/startup/uninstall smoke test: PASS"
}
