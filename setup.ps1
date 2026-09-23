$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

if (Test-Path -LiteralPath '.venv\Scripts\python.exe') {
    $python = (Resolve-Path -LiteralPath '.venv\Scripts\python.exe').Path
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 -m venv .venv
    $python = (Resolve-Path -LiteralPath '.venv\Scripts\python.exe').Path
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python -m venv .venv
    $python = (Resolve-Path -LiteralPath '.venv\Scripts\python.exe').Path
} else {
    $bundled = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (-not (Test-Path -LiteralPath $bundled)) {
        throw 'Python 3.11+ is required. Install Python, then rerun setup.ps1.'
    }
    & $bundled -m venv .venv
    $python = (Resolve-Path -LiteralPath '.venv\Scripts\python.exe').Path
}

& $python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw 'pip upgrade failed.' }
& $python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
Write-Host 'Setup complete. Run .\run.ps1 after setting OPENAI_API_KEY.'
