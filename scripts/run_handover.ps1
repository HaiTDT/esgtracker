param([switch]$CheckOnly)
$ErrorActionPreference = 'Stop'
$applicationRoot = [IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
Set-Location -LiteralPath $applicationRoot
$interpreter = Join-Path $applicationRoot '.venv\Scripts\python.exe'
if (!(Test-Path -LiteralPath $interpreter)) {throw 'Missing .venv; follow docs/04-installation-and-configuration.md.'}
& $interpreter -B scripts/check_handover.py
if ($LASTEXITCODE -ne 0) {throw 'Handover document checks failed.'}
if (!$CheckOnly) { & $interpreter app.py }
