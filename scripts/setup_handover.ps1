param([switch]$Install, [switch]$UseObservedConstraints)
$ErrorActionPreference = 'Stop'
$applicationRoot = [IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
Set-Location -LiteralPath $applicationRoot
if (!$Install) { Write-Output 'Preview only. Run with -Install to create a NEW .venv and install requirements (network required).'; exit 0 }
if (Test-Path -LiteralPath (Join-Path $applicationRoot '.venv')) {throw 'Existing .venv preserved; use pip manually or a clean checkout.'}
py -3.12 -m venv .venv
if ($LASTEXITCODE -ne 0) {throw 'Python 3.12 venv creation failed.'}
$interpreter = Join-Path $applicationRoot '.venv\Scripts\python.exe'
if ($UseObservedConstraints) { & $interpreter -m pip install -r requirements.txt -c docs/reference/dependency-constraints.txt }
else { & $interpreter -m pip install -r requirements.txt }
if ($LASTEXITCODE -ne 0) {throw 'Dependency install failed; environment preserved for diagnostics.'}
& $interpreter -m pip check
if ($LASTEXITCODE -ne 0) {throw 'Dependency check failed.'}
