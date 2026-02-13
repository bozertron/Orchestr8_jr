"""Tests for dry_run_patchbay_rewire() validation behavior."""

from pathlib import Path

from IP.connection_verifier import dry_run_patchbay_rewire, apply_patchbay_rewire


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_patchbay_dry_run_valid_python(tmp_path):
    write_file(tmp_path / "a.py", "import b\n")
    write_file(tmp_path / "b.py", "VALUE = 1\n")
    write_file(tmp_path / "c.py", "VALUE = 2\n")

    result = dry_run_patchbay_rewire(
        project_root=str(tmp_path),
        source_file="a.py",
        current_target="b.py",
        proposed_target="c.py",
    )

    assert result["canApply"] is True
    assert result["sourceLine"] == 1
    assert result["currentImportStatement"] == "b"
    assert result["proposedImportStatement"] == "import c"
    assert result["checks"]["sourceImportsCurrentTarget"] is True
    assert result["issues"] == []


def test_patchbay_dry_run_missing_proposed_target(tmp_path):
    write_file(tmp_path / "a.py", "import b\n")
    write_file(tmp_path / "b.py", "VALUE = 1\n")

    result = dry_run_patchbay_rewire(
        project_root=str(tmp_path),
        source_file="a.py",
        current_target="b.py",
        proposed_target="missing.py",
    )

    assert result["canApply"] is False
    assert "Proposed target file not found: missing.py" in result["issues"]


def test_patchbay_dry_run_source_not_importing_current_target(tmp_path):
    write_file(tmp_path / "a.py", "import c\n")
    write_file(tmp_path / "b.py", "VALUE = 1\n")
    write_file(tmp_path / "c.py", "VALUE = 2\n")

    result = dry_run_patchbay_rewire(
        project_root=str(tmp_path),
        source_file="a.py",
        current_target="b.py",
        proposed_target="c.py",
    )

    assert result["canApply"] is False
    assert "Source file does not currently import target: b.py" in result["issues"]


def test_patchbay_dry_run_already_imports_proposed_target(tmp_path):
    write_file(tmp_path / "a.py", "import b\nimport c\n")
    write_file(tmp_path / "b.py", "VALUE = 1\n")
    write_file(tmp_path / "c.py", "VALUE = 2\n")

    result = dry_run_patchbay_rewire(
        project_root=str(tmp_path),
        source_file="a.py",
        current_target="b.py",
        proposed_target="c.py",
    )

    assert result["canApply"] is False
    assert "Source file already imports proposed target: c.py" in result["issues"]


def test_patchbay_dry_run_valid_javascript(tmp_path):
    write_file(tmp_path / "src/a.js", "import value from './b.js';\n")
    write_file(tmp_path / "src/b.js", "export const value = 1;\n")
    write_file(tmp_path / "src/c.js", "export const value = 2;\n")

    result = dry_run_patchbay_rewire(
        project_root=str(tmp_path),
        source_file="src/a.js",
        current_target="src/b.js",
        proposed_target="src/c.js",
    )

    assert result["canApply"] is True
    assert result["importType"] == "javascript"
    assert result["proposedImportStatement"] == "import ... from './c'"
    assert result["issues"] == []


def test_patchbay_apply_rewire_valid_python(tmp_path):
    write_file(tmp_path / "a.py", "import b\n")
    write_file(tmp_path / "b.py", "VALUE = 1\n")
    write_file(tmp_path / "c.py", "VALUE = 2\n")

    result = apply_patchbay_rewire(
        project_root=str(tmp_path),
        source_file="a.py",
        current_target="b.py",
        proposed_target="c.py",
    )

    assert result["applied"] is True
    assert result["rolledBack"] is False
    assert result["checks"]["dryRunPassed"] is True
    assert result["checks"]["proposedImportedAfterWrite"] is True
    assert result["checks"]["currentTargetRemoved"] is True
    assert "import c" in (tmp_path / "a.py").read_text(encoding="utf-8")


def test_patchbay_apply_rewire_valid_javascript(tmp_path):
    write_file(tmp_path / "src/a.js", "import value from './b.js';\n")
    write_file(tmp_path / "src/b.js", "export const value = 1;\n")
    write_file(tmp_path / "src/c.js", "export const value = 2;\n")

    result = apply_patchbay_rewire(
        project_root=str(tmp_path),
        source_file="src/a.js",
        current_target="src/b.js",
        proposed_target="src/c.js",
    )

    assert result["applied"] is True
    assert result["rolledBack"] is False
    content = (tmp_path / "src/a.js").read_text(encoding="utf-8")
    assert "./c" in content
    assert "./b.js" not in content


def test_patchbay_apply_rewire_blocked_when_dry_run_fails(tmp_path):
    write_file(tmp_path / "a.py", "import c\n")
    write_file(tmp_path / "b.py", "VALUE = 1\n")
    write_file(tmp_path / "c.py", "VALUE = 2\n")

    before = (tmp_path / "a.py").read_text(encoding="utf-8")
    result = apply_patchbay_rewire(
        project_root=str(tmp_path),
        source_file="a.py",
        current_target="b.py",
        proposed_target="c.py",
    )
    after = (tmp_path / "a.py").read_text(encoding="utf-8")

    assert result["applied"] is False
    assert result["checks"]["dryRunPassed"] is False
    assert after == before
