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
$env:REDIS_URL = if ($env:REDIS_URL) { $env:REDIS_URL } else { "redis://localhost:6379/0" }

$apiJob = Start-Job -Name "SecureLLM-API" -ArgumentList @(
    $pythonExecutable,
    $root,
    $apiDirectory,
    $apiOutputLog,
    $apiErrorLog,
    $env:REDIS_URL
) -ScriptBlock {
    param($python, $workingDirectory, $pythonPath, $outputLog, $errorLog, $redisUrl)

    Set-Location $workingDirectory
    $env:PYTHONPATH = $pythonPath
    $env:REDIS_URL = $redisUrl
    & $python -m uvicorn app.main:app --reload --port 8000 1> $outputLog 2> $errorLog
}

$frontendJob = Start-Job -Name "SecureLLM-Frontend" -ArgumentList @(
    $npmExecutable,
    $frontendDirectory,
    $frontendOutputLog,
    $frontendErrorLog
) -ScriptBlock {
    param($npm, $workingDirectory, $outputLog, $errorLog)

    Set-Location $workingDirectory
    & $npm run dev 1> $outputLog 2> $errorLog
}

try {
    Write-Host "API Gateway and frontend are running for this terminal session."
    Write-Host "API:      http://localhost:8000"
    Write-Host "Frontend: http://localhost:5173"
    Write-Host "Press Ctrl+C or close this terminal to stop the services."
    Write-Host "Logs:     $logDirectory"

    Wait-Job -Job $apiJob, $frontendJob | Out-Null
}
finally {
    Stop-Job -Job $apiJob, $frontendJob -ErrorAction SilentlyContinue
    Remove-Job -Job $apiJob, $frontendJob -Force -ErrorAction SilentlyContinue
}