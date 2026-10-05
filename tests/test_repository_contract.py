from pathlib import Path
import json
import os
import subprocess
import sys
import textwrap


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def test_open_source_metadata_files_exist():
    for filename in (
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "SECURITY.md",
    ):
        assert (REPOSITORY_ROOT / filename).is_file()


def test_license_is_apache_version_two():
    license_text = (REPOSITORY_ROOT / "LICENSE").read_text(encoding="utf-8")

    assert "Apache License" in license_text
    assert "Version 2.0, January 2004" in license_text
    assert "END OF TERMS AND CONDITIONS" in license_text


def test_readme_documents_supported_checks_and_project_entry_points():
    readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")

    for expected_text in (
        ".\\run.ps1",
        "python -m pip install -r api-gateway/requirements.txt -r llm-service/requirements.txt",
        "python -m pytest -q tests",
        "npm run lint",
        "npm run build",
        "docker build -t securellm-llm:local ./llm-service",
        "docker run -d --name securellm-redis",
        "docker run -d --name securellm-llm",
        "ollama pull qwen2.5:1.5b",
        "http://localhost:5173",
        "flowchart TB",
        "POST /chat",
        "POST /generate",
        "GET /history",
        "DELETE /history",
        "GitHub Actions repository scan",
        "Monday at 04:00 UTC",
        "retained for 30 days",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "Apache License 2.0",
        "### Start the API and frontend",
        "It does not start Redis, Ollama, Docker, or the LLM container.",
    ):
        assert expected_text in readme


def test_all_sdd_documents_are_markdown_files():
    specs_directory = REPOSITORY_ROOT / "specs"

    assert specs_directory.is_dir()
    assert list(specs_directory.glob("*.md"))
    assert all(path.suffix == ".md" for path in specs_directory.iterdir())


def test_trivy_workflow_scans_and_reports_without_email():
    workflow_path = REPOSITORY_ROOT / ".github" / "workflows" / "trivy-scan.yml"
    workflow = workflow_path.read_text(encoding="utf-8")

    for expected_text in (
        "  schedule:",
        '    - cron: "0 4 * * 1"',
        "  workflow_dispatch:",
        "permissions:\n  contents: read",
        "trivy fs --scanners vuln --exit-code 0 --format json --output trivy-report.json .",
        "GITHUB_STEP_SUMMARY",
        "uses: actions/upload-artifact@v4",
        "trivy-report.json",
        "trivy-report.txt",
        "retention-days: 30",
    ):
        assert expected_text in workflow

    for forbidden_text in (
        "pull_request:",
        "action-send-mail",
        "secrets.SMTP_",
        "secrets.EMAIL_",
    ):
        assert forbidden_text not in workflow


def test_trivy_report_script_accepts_valid_json_without_vulnerabilities(tmp_path):
    workflow_path = REPOSITORY_ROOT / ".github" / "workflows" / "trivy-scan.yml"
    workflow = workflow_path.read_text(encoding="utf-8")
    report_script = workflow.split("python - <<'PY'\n", 1)[1].split("\n          PY", 1)[0]
    report_script = textwrap.dedent(report_script)
    (tmp_path / "trivy-report.json").write_text(
        json.dumps({"Results": []}),
        encoding="utf-8",
    )
    summary_path = tmp_path / "step-summary.md"
    environment = os.environ.copy()
    environment.update(
        {
            "SETUP_OUTCOME": "success",
            "SCAN_OUTCOME": "success",
            "REPOSITORY": "MALLADISARMA/secure-llm",
            "REF": "refs/heads/main",
            "GITHUB_STEP_SUMMARY": str(summary_path),
        }
    )

    result = subprocess.run(
        [sys.executable, "-c", report_script],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Trivy scan status: completed" in (tmp_path / "trivy-report.txt").read_text(
        encoding="utf-8"
    )
    assert "The filesystem scan completed; no vulnerabilities were found." in summary_path.read_text(
        encoding="utf-8"
    )
