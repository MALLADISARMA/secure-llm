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
        "python -m pytest -q tests",
        "npm run lint",
        "npm run build",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "Apache License 2.0",
    ):
        assert expected_text in readme


def test_all_sdd_documents_are_markdown_files():
    specs_directory = REPOSITORY_ROOT / "specs"

    assert specs_directory.is_dir()
    assert list(specs_directory.glob("*.md"))
    assert all(path.suffix == ".md" for path in specs_directory.iterdir())
