"""Carl Core - TypeScript Context Bridge
Orchstr8 v3.0 - The Fortress Factory

Bridge between Python and TypeScript analysis tools.
Executes unified-context-system.ts for deep project analysis.
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

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

    def __init__(self, root_path: str, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize Carl Contextualizer.

        Args:
            root_path: Project root directory
            timeout: Subprocess timeout in seconds (default: 30)
        """
        self.root = Path(root_path)
        self.timeout = timeout
        self.ts_tool = self.root / TS_TOOL_PATH
        self.context_file = self.root / CONTEXT_OUTPUT_PATH

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
