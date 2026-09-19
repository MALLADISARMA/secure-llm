$ErrorActionPreference = "Stop"

$root = $PSScriptRoot
$apiDirectory = Join-Path $root "api-gateway"
$frontendDirectory = Join-Path $root "frontend"
$logDirectory = Join-Path $root "logs"
$requirementsFile = Join-Path $apiDirectory "requirements.txt"
$frontendLockFile = Join-Path $frontendDirectory "package-lock.json"
$frontendModulesDirectory = Join-Path $frontendDirectory "node_modules"
$venvDirectory = Join-Path $root ".venv"
$virtualEnvironmentPython = Join-Path $root ".venv\Scripts\python.exe"
$pythonExecutable = "python.exe"
$npmExecutable = (Get-Command npm.cmd -ErrorAction Stop).Source

New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null

if (-not (Test-Path $virtualEnvironmentPython)) {
    Write-Host "Creating Python virtual environment..."
    & $pythonExecutable -m venv $venvDirectory
}

$pythonExecutable = $virtualEnvironmentPython
$requirementsHash = (Get-FileHash $requirementsFile -Algorithm SHA256).Hash
$requirementsMarker = Join-Path $venvDirectory ".securellm-requirements.sha256"
if (-not (Test-Path $requirementsMarker) -or (Get-Content $requirementsMarker -Raw).Trim() -ne $requirementsHash) {
    Write-Host "Installing API Gateway dependencies..."
    & $pythonExecutable -m pip install -r $requirementsFile
    Set-Content -Path $requirementsMarker -Value $requirementsHash -NoNewline
}

$frontendLockHash = (Get-FileHash $frontendLockFile -Algorithm SHA256).Hash
$frontendLockMarker = Join-Path $frontendModulesDirectory ".securellm-package-lock.sha256"
if (-not (Test-Path $frontendModulesDirectory) -or -not (Test-Path $frontendLockMarker) -or (Get-Content $frontendLockMarker -Raw).Trim() -ne $frontendLockHash) {
    Write-Host "Installing frontend dependencies..."
    & $npmExecutable ci --prefix $frontendDirectory
    New-Item -ItemType Directory -Path $frontendModulesDirectory -Force | Out-Null
    Set-Content -Path $frontendLockMarker -Value $frontendLockHash -NoNewline
}

$apiOutputLog = Join-Path $logDirectory "api.log"
$apiErrorLog = Join-Path $logDirectory "api.error.log"
$frontendOutputLog = Join-Path $logDirectory "frontend.log"
$frontendErrorLog = Join-Path $logDirectory "frontend.error.log"
$env:PYTHONPATH = $apiDirectory

Start-Process $pythonExecutable `
    -WorkingDirectory $root `
    -WindowStyle Hidden `
    -ArgumentList @("-m", "uvicorn", "app.main:app", "--reload", "--port", "8000") `
    -RedirectStandardOutput $apiOutputLog `
    -RedirectStandardError $apiErrorLog

Start-Process $npmExecutable `
    -WorkingDirectory $frontendDirectory `
    -WindowStyle Hidden `
    -ArgumentList @("run", "dev") `
    -RedirectStandardOutput $frontendOutputLog `
    -RedirectStandardError $frontendErrorLog

Write-Host "API Gateway and frontend are starting in the background."
Write-Host "API:      http://localhost:8000"
Write-Host "Frontend: http://localhost:5173"
Write-Host "Logs:     $logDirectory"