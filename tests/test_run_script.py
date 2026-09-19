from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RUN_SCRIPT = REPOSITORY_ROOT / "run.ps1"


def test_run_script_starts_services_without_visible_terminals():
    script = RUN_SCRIPT.read_text(encoding="utf-8")

    assert "Start-Process $pythonExecutable" in script
    assert "Start-Process $npmExecutable" in script
    assert "-WindowStyle Hidden" in script
    assert "-NoExit" not in script


def test_run_script_bootstraps_backend_and_frontend_dependencies():
    script = RUN_SCRIPT.read_text(encoding="utf-8")

    assert "-m venv $venvDirectory" in script
    assert "-m pip install -r $requirementsFile" in script
    assert "Get-FileHash $requirementsFile" in script
    assert "& $npmExecutable ci --prefix $frontendDirectory" in script
    assert "Get-FileHash $frontendLockFile" in script


def test_run_script_redirects_service_logs():
    script = RUN_SCRIPT.read_text(encoding="utf-8")

    for log_name in (
        "$apiOutputLog",
        "$apiErrorLog",
        "$frontendOutputLog",
        "$frontendErrorLog",
    ):
        assert log_name in script


def test_run_script_uses_expected_service_directories():
    script = RUN_SCRIPT.read_text(encoding="utf-8")

    assert 'Join-Path $root "api-gateway"' in script
    assert 'Join-Path $root "frontend"' in script
    assert '"-m", "uvicorn", "app.main:app"' in script
    assert '"run", "dev"' in script