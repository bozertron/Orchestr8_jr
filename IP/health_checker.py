# IP/health_checker.py
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class HealthCheckResult:
    status: str  # "working" | "broken"
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    last_check: str = ""
    raw_output: str = ""


class HealthChecker:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)

    def check_fiefdom(self, fiefdom_path: str) -> HealthCheckResult:
        """
        Run health check for a fiefdom.
        Currently uses npm run typecheck. Future: e2e, unit tests.

        Args:
            fiefdom_path: Relative path from project root (e.g., "src/modules/generator")

        Returns:
            HealthCheckResult with status, errors, warnings
        """
        result = subprocess.run(
            ["npm", "run", "typecheck"],
            cwd=str(self.project_root),
            capture_output=True,
            text=True,
            timeout=120,  # 2 minute timeout
        )

        # TypeScript errors go to stdout, not stderr
        output = result.stdout + result.stderr
        errors = []
        warnings = []

        # Parse output for this fiefdom
        for line in output.split("\n"):
            # Check if error is in this fiefdom
            if fiefdom_path in line:
                if "error TS" in line or "error:" in line.lower():
                    errors.append(line.strip())
                elif "warning" in line.lower():
                    warnings.append(line.strip())

        return HealthCheckResult(
            status="broken" if errors else "working",
            errors=errors,
            warnings=warnings,
            last_check=datetime.now().isoformat(),
            raw_output=output,
        )

    def check_all_fiefdoms(
        self, fiefdom_paths: List[str]
    ) -> Dict[str, HealthCheckResult]:
        """
        Run health check once and parse results for all fiefdoms.
        More efficient than running typecheck per fiefdom.
        """
        result = subprocess.run(
            ["npm", "run", "typecheck"],
            cwd=str(self.project_root),
            capture_output=True,
            text=True,
            timeout=120,
        )

        output = result.stdout + result.stderr
        results = {}

        for fiefdom in fiefdom_paths:
            errors = []
            warnings = []
            for line in output.split("\n"):
                if fiefdom in line:
                    if "error TS" in line or "error:" in line.lower():
                        errors.append(line.strip())
                    elif "warning" in line.lower():
                        warnings.append(line.strip())

            results[fiefdom] = HealthCheckResult(
                status="broken" if errors else "working",
                errors=errors,
                warnings=warnings,
                last_check=datetime.now().isoformat(),
                raw_output="",  # Only store once, not per fiefdom
            )

        return results
