from pathlib import Path


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
        "Code scanning alerts",
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


def test_trivy_workflow_uploads_sarif_findings_without_email():
    workflow_path = REPOSITORY_ROOT / ".github" / "workflows" / "trivy-scan.yml"
    workflow = workflow_path.read_text(encoding="utf-8")

    for expected_text in (
        "  schedule:",
        '    - cron: "0 4 * * 1"',
        "  workflow_dispatch:",
        "  security-events: write",
        "trivy fs --scanners vuln --exit-code 0 --format sarif --output trivy-results.sarif .",
        "uses: github/codeql-action/upload-sarif@v3",
        "sarif_file: trivy-results.sarif",
        "category: trivy-filesystem",
    ):
        assert expected_text in workflow

    for forbidden_text in (
        "pull_request:",
        "action-send-mail",
        "secrets.SMTP_",
        "secrets.EMAIL_",
        "trivy-report",
        "GITHUB_STEP_SUMMARY",
        "uses: actions/upload-artifact@v4",
    ):
        assert forbidden_text not in workflow
