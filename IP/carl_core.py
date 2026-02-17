"""Carl Core - TypeScript Context Bridge
Orchestr8 v3.0

Bridge between Python and TypeScript analysis tools.
Executes unified-context-system.ts for deep project analysis.
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

from .health_checker import HealthChecker
from .connection_verifier import ConnectionVerifier
from .combat_tracker import CombatTracker
from .ticket_manager import TicketManager
from .louis_core import LouisWarden, LouisConfig

# Configuration
DEFAULT_TIMEOUT = 30  # seconds
TS_TOOL_PATH = "frontend/tools/unified-context-system.ts"
CONTEXT_OUTPUT_PATH = "docs/project-context.json"


class CarlContextualizer:
    """
    Context Bridge for TypeScript analysis tools.

    Executes unified-context-system.ts via npx tsx and parses results.
    """

    def __init__(
        self,
        root_path: str,
        timeout: int = DEFAULT_TIMEOUT,
        state_managers: Optional[Dict] = None,
    ):
        """
        Initialize Carl Contextualizer.

        Args:
            root_path: Project root directory
            timeout: Subprocess timeout in seconds (default: 30)
            state_managers: Optional state managers dict for integration
        """
        self.root = Path(root_path)
        self.timeout = timeout
        self.ts_tool = self.root / TS_TOOL_PATH
        self.context_file = self.root / CONTEXT_OUTPUT_PATH
        self.state_managers = state_managers or {}

        # Initialize signal sources for context aggregation
        self.health_checker = HealthChecker(str(self.root))
        self.connection_verifier = ConnectionVerifier(str(self.root))
        self.combat_tracker = CombatTracker(str(self.root))
        self.ticket_manager = TicketManager(str(self.root))

        # Louis initialization (may fail gracefully if not configured)
        try:
            louis_config = LouisConfig(str(self.root))
            self.louis_warden = LouisWarden(louis_config)
        except Exception:
            self.louis_warden = None

    def run_deep_scan(self) -> Dict[str, Any]:
        """
        Executes the TypeScript analyzer via subprocess.

        Returns:
            Dict containing analysis results or error information
        """
        if not self.ts_tool.exists():
            return {
                "error": f"TypeScript tool not found at {TS_TOOL_PATH}",
                "expected_path": str(self.ts_tool),
            }

        try:
            # Execute TypeScript tool with timeout
            result = subprocess.run(
                ["npx", "tsx", str(self.ts_tool)],
                cwd=str(self.root),
                check=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )

            if self.context_file.exists():
                with open(self.context_file, "r", encoding="utf-8") as f:
                    return json.load(f)

            return {
                "error": "Analysis ran but output file is missing.",
                "stdout": result.stdout,
                "expected_output": str(self.context_file),
            }

        except subprocess.TimeoutExpired:
            return {
                "error": f"Analysis timed out after {self.timeout} seconds",
                "timeout": self.timeout,
            }
        except subprocess.CalledProcessError as e:
            return {
                "error": f"Scanner failed with exit code {e.returncode}",
                "stderr": e.stderr if e.stderr else None,
                "stdout": e.stdout if e.stdout else None,
            }
        except FileNotFoundError:
            return {
                "error": "npx or tsx not found. Ensure Node.js 22+ is installed.",
                "hint": "Run 'npm install -g tsx' to install tsx globally",
            }
        except Exception as e:
            return {"error": str(e), "type": type(e).__name__}

    def get_file_context(self, rel_path: str) -> str:
        """Legacy fallback: reads file content for LLM injection."""
        full = self.root / rel_path
        if full.exists():
            return (
                f"<file path='{rel_path}'>\n{full.read_text(encoding='utf-8')}\n</file>"
            )
        return ""

    def gather_context(self, fiefdom_path: str) -> "FiefdomContext":
        """
        Aggregate context from all signal sources for a fiefdom.

        Carl collects data - he does NOT block operations.

        Args:
            fiefdom_path: Relative path to fiefdom (e.g., "IP/")

        Returns:
            FiefdomContext with aggregated data
        """
        health_result = self.health_checker.check_fiefdom(fiefdom_path)
        health = {
            "status": health_result.status,
            "errors": [
                {"file": e.file, "line": e.line, "message": e.message}
                for e in health_result.errors
            ],
            "warnings": [
                {"file": w.file, "line": w.line, "message": w.message}
                for w in health_result.warnings
            ],
        }

        conn_result = self.connection_verifier.verify_file(fiefdom_path)
        connections = {
            "imports_from": [imp.target_module for imp in conn_result.local_imports],
            "broken": [
                {"import": imp.target_module, "line": imp.line_number}
                for imp in conn_result.broken_imports
            ],
        }

        deployment = self.combat_tracker.get_deployment_info(fiefdom_path)
        combat = {
            "active": deployment is not None,
            "model": deployment.get("model", "") if deployment else "",
            "terminal_id": deployment.get("terminal_id", "") if deployment else "",
        }

        ticket_objs = self.ticket_manager.get_tickets_for_fiefdom(fiefdom_path)
        tickets = [f"{t.id}: {t.title}" for t in ticket_objs if t.status != "archived"]

        locks = []
        if self.louis_warden:
            protection = self.louis_warden.get_protection_status()
            for path, status in protection.items():
                if fiefdom_path in path and status.get("locked"):
                    locks.append({"file": path, "reason": "Louis protection"})

        return FiefdomContext(
            fiefdom=fiefdom_path,
            health=health,
            connections=connections,
            combat=combat,
            tickets=tickets,
            locks=locks,
        )

    def gather_context_json(self, fiefdom_path: str) -> str:
        """
        Get context as JSON string for UI display.

        Args:
            fiefdom_path: Relative path to fiefdom (e.g., "IP/")

        Returns:
            JSON string with indented formatting
        """
        ctx = self.gather_context(fiefdom_path)
        return json.dumps(asdict(ctx), indent=2)


@dataclass
class FiefdomContext:
    """
    Structured context output for fiefdoms.
    Structure is LOCKED per CONTEXT.md - do not modify fields.
    """

    fiefdom: str
    health: Dict[str, Any]
    connections: Dict[str, Any]
    combat: Dict[str, Any]
    tickets: List[str]
    locks: List[Dict[str, str]]
