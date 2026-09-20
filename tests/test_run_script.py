from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RUN_SCRIPT = REPOSITORY_ROOT / "run.ps1"


def test_run_script_keeps_services_bound_to_the_launcher_session():
    script = RUN_SCRIPT.read_text(encoding="utf-8")

    assert 'Start-Job -Name "SecureLLM-API"' in script
    assert 'Start-Job -Name "SecureLLM-Frontend"' in script
    assert "Wait-Job -Job $apiJob, $frontendJob" in script
    assert "Stop-Job -Job $apiJob, $frontendJob" in script


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
    assert "& $python -m uvicorn app.main:app" in script
    assert "& $npm run dev" in script