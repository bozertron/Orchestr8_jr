"""Patchbay dry-run/apply rewire operations for connection graph workflows."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


def _normalize_rel_path(path_value: str) -> str:
    """Normalize a project-relative path for stable comparisons."""
    normalized = Path(path_value).as_posix().strip()
    if normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def _python_module_from_file(rel_path: str) -> str:
    """Convert a Python file path to a module import path."""
    path = Path(rel_path)
    if path.suffix == ".py":
        path = path.with_suffix("")

    parts = list(path.parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _js_specifier_from_paths(source_file: str, target_file: str) -> str:
    """Create a relative JS/TS import specifier from source to target."""
    source_dir = Path(source_file).parent
    rel = os.path.relpath(target_file, start=source_dir).replace(os.sep, "/")
    if not rel.startswith("."):
        rel = f"./{rel}"

    return re.sub(r"\.(ts|tsx|js|jsx|mjs|cjs)$", "", rel)


def _split_line_ending(line: str) -> Tuple[str, str]:
    """Split a line into content and newline suffix."""
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    return line, ""


def _rewrite_python_import_line(
    line_body: str,
    current_module: str,
    proposed_module: str,
) -> Optional[str]:
    """Rewrite a Python import line module path while preserving import form."""
    from_match = re.match(r"^(\s*)from\s+([.\w]+)(\s+import\s+.+)$", line_body)
    if from_match and from_match.group(2) == current_module:
        return f"{from_match.group(1)}from {proposed_module}{from_match.group(3)}"

    import_match = re.match(r"^(\s*)import\s+([.\w]+)(\s+as\s+\w+)?\s*$", line_body)
    if import_match and import_match.group(2) == current_module:
        alias = import_match.group(3) or ""
        return f"{import_match.group(1)}import {proposed_module}{alias}"

    return None


def _rewrite_js_import_line(
    line_body: str,
    current_specifier: str,
    proposed_specifier: str,
) -> Optional[str]:
    """Rewrite a JS/TS import specifier on the targeted line."""
    quote_patterns = [
        re.compile(r"(['\"])(" + re.escape(current_specifier) + r")\1"),
        re.compile(r"(`)(" + re.escape(current_specifier) + r")`"),
    ]

    for pattern in quote_patterns:

        def _replace(match: re.Match) -> str:
            quote = match.group(1)
            if quote == "`":
                return f"`{proposed_specifier}`"
            return f"{quote}{proposed_specifier}{quote}"

        rewritten, count = pattern.subn(_replace, line_body, count=1)
        if count > 0:
            return rewritten

    return None


def dry_run_patchbay_rewire(
    project_root: str,
    source_file: str,
    current_target: str,
    proposed_target: str,
) -> Dict[str, Any]:
    """
    Validate a patchbay rewire request without writing files.

    This is the first safe step toward drag-to-rewire behavior:
    it verifies the requested source/target relationship, checks compatibility,
    and returns a deterministic preview payload for UI/logging.
    """
    from IP.connection_verifier import ConnectionVerifier, ImportType, PatchbayDryRunResult

    verifier = ConnectionVerifier(project_root)
    source_norm = _normalize_rel_path(source_file)
    current_norm = _normalize_rel_path(current_target)
    proposed_norm = _normalize_rel_path(proposed_target)

    source_path = verifier.project_root / source_norm
    current_path = verifier.project_root / current_norm
    proposed_path = verifier.project_root / proposed_norm
    source_type = verifier._detect_file_type(source_norm)
    proposed_type = verifier._detect_file_type(proposed_norm)

    result = PatchbayDryRunResult(
        action="dry_run_rewire",
        source_file=source_norm,
        current_target=current_norm,
        proposed_target=proposed_norm,
        import_type=source_type.value,
        can_apply=False,
        checks={
            "sourceExists": source_path.is_file(),
            "currentTargetExists": current_path.is_file(),
            "proposedTargetExists": proposed_path.is_file(),
            "sourceImportsCurrentTarget": False,
            "sourceAlreadyImportsProposedTarget": False,
            "fileTypeCompatible": False,
        },
    )

    if not source_path.is_file():
        result.issues.append(f"Source file not found: {source_norm}")
        return result.to_dict()

    if not proposed_path.is_file():
        result.issues.append(f"Proposed target file not found: {proposed_norm}")
        return result.to_dict()

    if source_norm == proposed_norm:
        result.issues.append("Proposed target is the same as source file.")
        return result.to_dict()

    source_report = verifier.verify_file(source_norm)
    all_imports = (
        source_report.local_imports
        + source_report.broken_imports
        + source_report.external_imports
    )

    matched_current = None
    for imp in all_imports:
        if imp.resolved_path and _normalize_rel_path(imp.resolved_path) == current_norm:
            matched_current = imp
            break
        if imp.target_module == current_norm:
            matched_current = imp
            break

    if matched_current is None:
        result.issues.append(
            f"Source file does not currently import target: {current_norm}"
        )
        return result.to_dict()

    result.checks["sourceImportsCurrentTarget"] = True
    result.source_line = matched_current.line_number
    result.current_import_statement = matched_current.import_statement

    for imp in source_report.local_imports:
        if imp.resolved_path and _normalize_rel_path(imp.resolved_path) == proposed_norm:
            result.checks["sourceAlreadyImportsProposedTarget"] = True
            result.issues.append(
                f"Source file already imports proposed target: {proposed_norm}"
            )
            break

    if result.issues:
        return result.to_dict()

    compatible_pairs = {
        (ImportType.PYTHON, ImportType.PYTHON),
        (ImportType.JAVASCRIPT, ImportType.JAVASCRIPT),
        (ImportType.JAVASCRIPT, ImportType.TYPESCRIPT),
        (ImportType.TYPESCRIPT, ImportType.JAVASCRIPT),
        (ImportType.TYPESCRIPT, ImportType.TYPESCRIPT),
    }
    if (source_type, proposed_type) in compatible_pairs:
        result.checks["fileTypeCompatible"] = True
    else:
        result.issues.append(
            f"Incompatible file types: {source_type.value} -> {proposed_type.value}"
        )
        return result.to_dict()

    if source_type == ImportType.PYTHON:
        module_name = _python_module_from_file(proposed_norm)
        if not module_name:
            result.issues.append(
                f"Could not derive Python module path from target: {proposed_norm}"
            )
            return result.to_dict()
        result.proposed_import_statement = f"import {module_name}"
    elif source_type in {ImportType.JAVASCRIPT, ImportType.TYPESCRIPT}:
        specifier = _js_specifier_from_paths(source_norm, proposed_norm)
        result.proposed_import_statement = f"import ... from '{specifier}'"
    else:
        result.warnings.append(
            f"Import preview unavailable for file type: {source_type.value}"
        )

    if not current_path.is_file():
        result.warnings.append(
            "Current target path does not exist on disk; edge may come from unresolved import."
        )

    result.can_apply = True
    return result.to_dict()


def apply_patchbay_rewire(
    project_root: str,
    source_file: str,
    current_target: str,
    proposed_target: str,
    auto_rollback: bool = True,
) -> Dict[str, Any]:
    """
    Apply a patchbay rewire request with guardrails.

    Workflow:
    1) Run dry-run validator
    2) Rewrite only the targeted import line
    3) Re-verify source file imports
    4) Optionally rollback if post-write checks fail
    """
    from IP.connection_verifier import ConnectionVerifier, ImportType

    dry_run = dry_run_patchbay_rewire(
        project_root=project_root,
        source_file=source_file,
        current_target=current_target,
        proposed_target=proposed_target,
    )

    result: Dict[str, Any] = {
        "action": "apply_rewire",
        "applied": False,
        "rolledBack": False,
        "sourceFile": _normalize_rel_path(source_file),
        "currentTarget": _normalize_rel_path(current_target),
        "proposedTarget": _normalize_rel_path(proposed_target),
        "lineNumber": dry_run.get("sourceLine"),
        "beforeLine": None,
        "afterLine": None,
        "checks": {
            "dryRunPassed": bool(dry_run.get("canApply")),
            "proposedImportedAfterWrite": False,
            "currentTargetRemoved": False,
        },
        "issues": [],
        "warnings": [],
        "dryRun": dry_run,
    }

    if not dry_run.get("canApply"):
        result["issues"] = list(dry_run.get("issues") or ["Dry-run validation failed."])
        result["warnings"] = list(dry_run.get("warnings") or [])
        return result

    verifier = ConnectionVerifier(project_root)
    source_norm = _normalize_rel_path(source_file)
    current_norm = _normalize_rel_path(current_target)
    proposed_norm = _normalize_rel_path(proposed_target)
    source_path = verifier.project_root / source_norm

    if not source_path.is_file():
        result["issues"].append(f"Source file not found: {source_norm}")
        return result

    source_type = verifier._detect_file_type(source_norm)
    if source_type == ImportType.UNKNOWN:
        result["issues"].append("Unsupported source file type for apply_rewire.")
        return result

    line_number = int(dry_run.get("sourceLine") or 0)
    current_import_statement = str(dry_run.get("currentImportStatement") or "")
    if line_number <= 0:
        result["issues"].append("Dry-run did not provide a valid source line.")
        return result
    if not current_import_statement:
        result["issues"].append("Dry-run did not provide import statement metadata.")
        return result

    original_content = source_path.read_text(encoding="utf-8", errors="ignore")
    lines = original_content.splitlines(keepends=True)
    if line_number > len(lines):
        result["issues"].append(
            f"Dry-run source line {line_number} out of range for file: {source_norm}"
        )
        return result

    original_line = lines[line_number - 1]
    line_body, line_ending = _split_line_ending(original_line)
    rewritten_body: Optional[str] = None

    if source_type == ImportType.PYTHON:
        proposed_module = _python_module_from_file(proposed_norm)
        if not proposed_module:
            result["issues"].append(
                f"Could not derive Python module from proposed target: {proposed_norm}"
            )
            return result
        rewritten_body = _rewrite_python_import_line(
            line_body=line_body,
            current_module=current_import_statement,
            proposed_module=proposed_module,
        )
    elif source_type in {ImportType.JAVASCRIPT, ImportType.TYPESCRIPT}:
        proposed_specifier = _js_specifier_from_paths(source_norm, proposed_norm)
        rewritten_body = _rewrite_js_import_line(
            line_body=line_body,
            current_specifier=current_import_statement,
            proposed_specifier=proposed_specifier,
        )

    if rewritten_body is None:
        result["issues"].append(
            "Could not rewrite targeted import line; line content no longer matches expected pattern."
        )
        return result

    if rewritten_body == line_body:
        result["issues"].append("Rewrite produced no change.")
        return result

    lines[line_number - 1] = rewritten_body + line_ending
    updated_content = "".join(lines)

    result["beforeLine"] = line_body
    result["afterLine"] = rewritten_body

    source_path.write_text(updated_content, encoding="utf-8")

    post_verify = verifier.verify_file(source_norm)
    post_local_targets = {
        _normalize_rel_path(imp.resolved_path)
        for imp in post_verify.local_imports
        if imp.resolved_path
    }

    proposed_imported = proposed_norm in post_local_targets
    current_removed = current_norm not in post_local_targets

    result["checks"]["proposedImportedAfterWrite"] = proposed_imported
    result["checks"]["currentTargetRemoved"] = current_removed

    if not proposed_imported:
        result["issues"].append(
            "Post-write verification failed: proposed target not resolved as local import."
        )
    if not current_removed:
        result["warnings"].append(
            "Current target still appears in local imports (may be imported on another line)."
        )

    if result["issues"] and auto_rollback:
        source_path.write_text(original_content, encoding="utf-8")
        result["rolledBack"] = True
        result["applied"] = False
        return result

    result["applied"] = len(result["issues"]) == 0
    return result
