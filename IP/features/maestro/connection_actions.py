"""Connection action bridge handling for Maestro -> Patchbay workflows."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Callable


def handle_connection_action(
    payload: dict,
    *,
    project_root_path: str | Path,
    validate_connection_action_event: Callable[[dict], Any],
    dry_run_patchbay_rewire: Callable[..., dict],
    apply_patchbay_rewire: Callable[..., dict],
    set_connection_action_result_payload: Callable[[str], None],
    log_action: Callable[[str], None],
) -> None:
    """
    Handle edge-level connection panel actions from Code City.

    Supported actions:
    - dry_run_rewire: validate a rewire request without writing files
    - apply_rewire: apply a rewire with guardrails and rollback checks
    """

    def emit_connection_action_result(result_payload: dict) -> None:
        """Push structured action result back to the UI bridge."""
        try:
            envelope = dict(result_payload or {})
            envelope["timestamp"] = datetime.now().isoformat()
            set_connection_action_result_payload(json.dumps(envelope))
        except Exception as e:
            log_action(f"Connection action result bridge error: {e}")

    if not payload:
        return

    try:
        event = validate_connection_action_event(payload)
    except ValueError as e:
        log_action(f"Invalid connection action payload: {e}")
        emit_connection_action_result(
            {
                "action": "invalid",
                "ok": False,
                "message": f"Invalid payload: {e}",
                "issues": [str(e)],
                "warnings": [],
            }
        )
        return
    except Exception as e:
        log_action(f"Connection action parse error: {e}")
        emit_connection_action_result(
            {
                "action": "invalid",
                "ok": False,
                "message": f"Parse error: {e}",
                "issues": [str(e)],
                "warnings": [],
            }
        )
        return

    if event.action not in {"dry_run_rewire", "apply_rewire"}:
        log_action(f"Unsupported connection action: {event.action}")
        emit_connection_action_result(
            {
                "action": event.action,
                "ok": False,
                "source": event.connection.source,
                "target": event.connection.target,
                "proposedTarget": event.proposedTarget,
                "message": f"Unsupported action: {event.action}",
                "issues": [f"Unsupported action: {event.action}"],
                "warnings": [],
            }
        )
        return

    source = event.connection.source
    target = event.connection.target
    proposed = (event.proposedTarget or "").strip()
    actor_role = (
        (event.actorRole or os.getenv("ORCHESTR8_ACTOR_ROLE", "operator"))
        .strip()
        .lower()
    )

    if not proposed:
        log_action(
            "Patchbay dry-run requires proposed target path (enter it in the connection panel input)."
        )
        emit_connection_action_result(
            {
                "action": event.action,
                "ok": False,
                "source": source,
                "target": target,
                "proposedTarget": proposed or None,
                "actorRole": actor_role,
                "message": "Proposed target path is required.",
                "issues": ["Proposed target path is required."],
                "warnings": [],
            }
        )
        return

    if event.action == "dry_run_rewire":
        try:
            dry_run = dry_run_patchbay_rewire(
                project_root=str(project_root_path),
                source_file=source,
                current_target=target,
                proposed_target=proposed,
            )

            if dry_run.get("canApply"):
                preview = dry_run.get("proposedImportStatement") or "<no preview>"
                log_action(
                    "Patchbay dry-run PASS: "
                    f"{source} -> replace {target} with {proposed} "
                    f"(line {dry_run.get('sourceLine', '?')}, preview: {preview})"
                )
                emit_connection_action_result(
                    {
                        "action": "dry_run_rewire",
                        "ok": True,
                        "source": source,
                        "target": target,
                        "proposedTarget": proposed,
                        "actorRole": actor_role,
                        "lineNumber": dry_run.get("sourceLine", 0),
                        "message": f"Dry-run PASS. Preview: {preview}",
                        "issues": [],
                        "warnings": dry_run.get("warnings", []),
                        "result": dry_run,
                    }
                )
            else:
                issues = dry_run.get("issues") or ["Unknown validation failure."]
                for issue in issues:
                    log_action(f"Patchbay dry-run BLOCKED: {issue}")
                warnings = dry_run.get("warnings") or []
                for warning in warnings:
                    log_action(f"Patchbay dry-run WARN: {warning}")
                emit_connection_action_result(
                    {
                        "action": "dry_run_rewire",
                        "ok": False,
                        "source": source,
                        "target": target,
                        "proposedTarget": proposed,
                        "actorRole": actor_role,
                        "lineNumber": dry_run.get("sourceLine", 0),
                        "message": "Dry-run BLOCKED.",
                        "issues": issues,
                        "warnings": warnings,
                        "result": dry_run,
                    }
                )
        except Exception as e:
            log_action(f"Patchbay dry-run error: {e}")
            emit_connection_action_result(
                {
                    "action": "dry_run_rewire",
                    "ok": False,
                    "source": source,
                    "target": target,
                    "proposedTarget": proposed,
                    "actorRole": actor_role,
                    "message": f"Dry-run error: {e}",
                    "issues": [str(e)],
                    "warnings": [],
                }
            )
        return

    raw_allowed_roles = os.getenv("ORCHESTR8_PATCHBAY_ALLOWED_ROLES", "founder,operator")
    allowed_roles = {
        role.strip().lower()
        for role in raw_allowed_roles.split(",")
        if role.strip()
    }
    if not allowed_roles:
        allowed_roles = {"founder", "operator"}

    apply_enabled = os.getenv("ORCHESTR8_PATCHBAY_APPLY", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    if not apply_enabled:
        msg = "Patchbay apply is disabled. Set ORCHESTR8_PATCHBAY_APPLY=1 to enable."
        log_action(msg)
        emit_connection_action_result(
            {
                "action": "apply_rewire",
                "ok": False,
                "source": source,
                "target": target,
                "proposedTarget": proposed,
                "actorRole": actor_role,
                "allowedRoles": sorted(allowed_roles),
                "message": msg,
                "issues": [msg],
                "warnings": [],
            }
        )
        return

    if actor_role not in allowed_roles:
        msg = (
            f"Patchbay apply denied for role '{actor_role}'. "
            f"Allowed roles: {', '.join(sorted(allowed_roles))}."
        )
        log_action(msg)
        emit_connection_action_result(
            {
                "action": "apply_rewire",
                "ok": False,
                "source": source,
                "target": target,
                "proposedTarget": proposed,
                "actorRole": actor_role,
                "allowedRoles": sorted(allowed_roles),
                "message": msg,
                "issues": [msg],
                "warnings": [],
            }
        )
        return

    try:
        apply_result = apply_patchbay_rewire(
            project_root=str(project_root_path),
            source_file=source,
            current_target=target,
            proposed_target=proposed,
            auto_rollback=True,
        )

        if apply_result.get("applied"):
            log_action(
                "Patchbay APPLY PASS: "
                f"{source}:{apply_result.get('lineNumber', '?')} "
                f"{target} -> {proposed}"
            )
            after_line = apply_result.get("afterLine")
            if after_line:
                log_action(f"Patchbay APPLY line now: {after_line}")
            emit_connection_action_result(
                {
                    "action": "apply_rewire",
                    "ok": True,
                    "source": source,
                    "target": target,
                    "proposedTarget": proposed,
                    "actorRole": actor_role,
                    "allowedRoles": sorted(allowed_roles),
                    "lineNumber": apply_result.get("lineNumber"),
                    "message": "Apply PASS.",
                    "issues": [],
                    "warnings": apply_result.get("warnings", []),
                    "result": apply_result,
                }
            )
        else:
            issues = apply_result.get("issues") or ["Unknown apply failure."]
            for issue in issues:
                log_action(f"Patchbay APPLY BLOCKED: {issue}")
            warnings = apply_result.get("warnings") or []
            for warning in warnings:
                log_action(f"Patchbay APPLY WARN: {warning}")
            if apply_result.get("rolledBack"):
                log_action("Patchbay APPLY rollback complete.")
            emit_connection_action_result(
                {
                    "action": "apply_rewire",
                    "ok": False,
                    "source": source,
                    "target": target,
                    "proposedTarget": proposed,
                    "actorRole": actor_role,
                    "allowedRoles": sorted(allowed_roles),
                    "lineNumber": apply_result.get("lineNumber"),
                    "message": "Apply BLOCKED.",
                    "issues": issues,
                    "warnings": warnings,
                    "rolledBack": bool(apply_result.get("rolledBack")),
                    "result": apply_result,
                }
            )
    except Exception as e:
        log_action(f"Patchbay apply error: {e}")
        emit_connection_action_result(
            {
                "action": "apply_rewire",
                "ok": False,
                "source": source,
                "target": target,
                "proposedTarget": proposed,
                "actorRole": actor_role,
                "allowedRoles": sorted(allowed_roles),
                "message": f"Apply error: {e}",
                "issues": [str(e)],
                "warnings": [],
            }
        )

