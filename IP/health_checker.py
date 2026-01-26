# IP/health_checker.py
"""
Health Checker - Runs static analysis and type checking for code health status.
Supports TypeScript (npm typecheck), Python (mypy, ruff, py_compile).
Feeds into Blue status (broken) for Woven Maps Code City.
"""
import subprocess
import shutil
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CheckerType(Enum):
    """Types of health checkers available."""
    TYPESCRIPT = "typescript"
    PYTHON_MYPY = "python_mypy"
    PYTHON_RUFF = "python_ruff"
    PYTHON_COMPILE = "python_compile"


@dataclass
class ParsedError:
    """Structured error with file, line, column, code, message."""
    file: str
    line: int
    column: int = 0
    error_code: str = ""
    message: str = ""
    severity: str = "error"  # "error" | "warning" | "info"
    
    def __str__(self) -> str:
        loc = f"{self.file}:{self.line}"
        if self.column:
            loc += f":{self.column}"
        code = f"[{self.error_code}] " if self.error_code else ""
        return f"{loc}: {code}{self.message}"


@dataclass
class HealthCheckResult:
    status: str  # "working" | "broken"
    errors: List[ParsedError] = field(default_factory=list)
    warnings: List[ParsedError] = field(default_factory=list)
    last_check: str = ""
    raw_output: str = ""
    checker_used: str = ""
    
    @property
    def error_count(self) -> int:
        return len(self.errors)
    
    @property
    def warning_count(self) -> int:
        return len(self.warnings)
    
    def get_errors_for_file(self, file_path: str) -> List[ParsedError]:
        """Get errors specific to a file path."""
        return [e for e in self.errors if file_path in e.file]


class HealthChecker:
    """Multi-language health checker for TypeScript and Python projects."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self._available_checkers: Dict[CheckerType, bool] = {}
        self._detect_available_checkers()
    
    def _detect_available_checkers(self):
        """Detect which checkers are available on the system."""
        # TypeScript (npm)
        has_package_json = (self.project_root / "package.json").exists()
        has_npm = shutil.which("npm") is not None
        self._available_checkers[CheckerType.TYPESCRIPT] = has_package_json and has_npm
        
        # Python checkers
        self._available_checkers[CheckerType.PYTHON_MYPY] = shutil.which("mypy") is not None
        self._available_checkers[CheckerType.PYTHON_RUFF] = shutil.which("ruff") is not None
        self._available_checkers[CheckerType.PYTHON_COMPILE] = True  # Always available with Python
    
    def get_available_checkers(self) -> List[CheckerType]:
        """Return list of available checkers."""
        return [k for k, v in self._available_checkers.items() if v]
    
    # =========================================================================
    # TypeScript Checking
    # =========================================================================
    
    def _parse_typescript_output(self, output: str) -> Tuple[List[ParsedError], List[ParsedError]]:
        """
        Parse TypeScript compiler output into structured errors.
        
        Format: src/file.ts(10,5): error TS2345: Argument of type...
        """
        errors = []
        warnings = []
        
        # Pattern: file.ts(line,col): error TSxxxx: message
        ts_pattern = re.compile(
            r'^(.+?)\((\d+),(\d+)\):\s+(error|warning)\s+(TS\d+):\s+(.+)$',
            re.MULTILINE
        )
        
        for match in ts_pattern.finditer(output):
            parsed = ParsedError(
                file=match.group(1),
                line=int(match.group(2)),
                column=int(match.group(3)),
                severity=match.group(4),
                error_code=match.group(5),
                message=match.group(6)
            )
            if parsed.severity == "error":
                errors.append(parsed)
            else:
                warnings.append(parsed)
        
        return errors, warnings
    
    def check_typescript(self, fiefdom_path: Optional[str] = None) -> HealthCheckResult:
        """
        Run TypeScript type checking via npm run typecheck.
        
        Args:
            fiefdom_path: If provided, filter results to this path only
        """
        if not self._available_checkers.get(CheckerType.TYPESCRIPT):
            return HealthCheckResult(
                status="working",
                checker_used="typescript (unavailable - no package.json or npm)",
                last_check=datetime.now().isoformat()
            )
        
        try:
            result = subprocess.run(
                ["npm", "run", "typecheck"],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=120,
            )
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return HealthCheckResult(
                status="broken",
                errors=[ParsedError(file="<timeout>", line=0, message="TypeScript check timed out")],
                checker_used="typescript",
                last_check=datetime.now().isoformat()
            )
        except FileNotFoundError:
            return HealthCheckResult(
                status="working",
                checker_used="typescript (npm not found)",
                last_check=datetime.now().isoformat()
            )
        
        errors, warnings = self._parse_typescript_output(output)
        
        # Filter to fiefdom if specified
        if fiefdom_path:
            errors = [e for e in errors if fiefdom_path in e.file]
            warnings = [w for w in warnings if fiefdom_path in w.file]
        
        return HealthCheckResult(
            status="broken" if errors else "working",
            errors=errors,
            warnings=warnings,
            last_check=datetime.now().isoformat(),
            raw_output=output,
            checker_used="typescript"
        )
    
    # =========================================================================
    # Python Checking - mypy
    # =========================================================================
    
    def _parse_mypy_output(self, output: str) -> Tuple[List[ParsedError], List[ParsedError]]:
        """
        Parse mypy output into structured errors.
        
        Format: file.py:10: error: Message [error-code]
        """
        errors = []
        warnings = []
        
        # Pattern: file.py:line:col: severity: message [code]
        mypy_pattern = re.compile(
            r'^(.+?):(\d+)(?::(\d+))?:\s+(error|warning|note):\s+(.+?)(?:\s+\[([^\]]+)\])?$',
            re.MULTILINE
        )
        
        for match in mypy_pattern.finditer(output):
            severity = match.group(4)
            if severity == "note":
                continue  # Skip notes
            
            parsed = ParsedError(
                file=match.group(1),
                line=int(match.group(2)),
                column=int(match.group(3)) if match.group(3) else 0,
                severity=severity,
                error_code=match.group(6) or "",
                message=match.group(5)
            )
            if severity == "error":
                errors.append(parsed)
            else:
                warnings.append(parsed)
        
        return errors, warnings
    
    def check_mypy(self, target_path: Optional[str] = None) -> HealthCheckResult:
        """
        Run mypy type checking on Python files.
        
        Args:
            target_path: Specific file or directory to check (default: project root)
        """
        if not self._available_checkers.get(CheckerType.PYTHON_MYPY):
            return HealthCheckResult(
                status="working",
                checker_used="mypy (not installed)",
                last_check=datetime.now().isoformat()
            )
        
        target = target_path or str(self.project_root)
        
        try:
            result = subprocess.run(
                ["mypy", target, "--no-error-summary", "--show-column-numbers"],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=180,
            )
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return HealthCheckResult(
                status="broken",
                errors=[ParsedError(file="<timeout>", line=0, message="mypy check timed out")],
                checker_used="mypy",
                last_check=datetime.now().isoformat()
            )
        except FileNotFoundError:
            return HealthCheckResult(
                status="working",
                checker_used="mypy (not found)",
                last_check=datetime.now().isoformat()
            )
        
        errors, warnings = self._parse_mypy_output(output)
        
        return HealthCheckResult(
            status="broken" if errors else "working",
            errors=errors,
            warnings=warnings,
            last_check=datetime.now().isoformat(),
            raw_output=output,
            checker_used="mypy"
        )
    
    # =========================================================================
    # Python Checking - ruff
    # =========================================================================
    
    def _parse_ruff_output(self, output: str) -> Tuple[List[ParsedError], List[ParsedError]]:
        """
        Parse ruff output into structured errors.
        
        Format: file.py:10:5: E501 Line too long
        """
        errors = []
        warnings = []
        
        # Pattern: file.py:line:col: CODE message
        ruff_pattern = re.compile(
            r'^(.+?):(\d+):(\d+):\s+([A-Z]+\d+)\s+(.+)$',
            re.MULTILINE
        )
        
        for match in ruff_pattern.finditer(output):
            code = match.group(4)
            # W = warning, E = error, F = fatal
            severity = "warning" if code.startswith("W") else "error"
            
            parsed = ParsedError(
                file=match.group(1),
                line=int(match.group(2)),
                column=int(match.group(3)),
                severity=severity,
                error_code=code,
                message=match.group(5)
            )
            if severity == "error":
                errors.append(parsed)
            else:
                warnings.append(parsed)
        
        return errors, warnings
    
    def check_ruff(self, target_path: Optional[str] = None) -> HealthCheckResult:
        """
        Run ruff linting on Python files.
        
        Args:
            target_path: Specific file or directory to check (default: project root)
        """
        if not self._available_checkers.get(CheckerType.PYTHON_RUFF):
            return HealthCheckResult(
                status="working",
                checker_used="ruff (not installed)",
                last_check=datetime.now().isoformat()
            )
        
        target = target_path or str(self.project_root)
        
        try:
            result = subprocess.run(
                ["ruff", "check", target, "--output-format=text"],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=120,
            )
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return HealthCheckResult(
                status="broken",
                errors=[ParsedError(file="<timeout>", line=0, message="ruff check timed out")],
                checker_used="ruff",
                last_check=datetime.now().isoformat()
            )
        except FileNotFoundError:
            return HealthCheckResult(
                status="working",
                checker_used="ruff (not found)",
                last_check=datetime.now().isoformat()
            )
        
        errors, warnings = self._parse_ruff_output(output)
        
        return HealthCheckResult(
            status="broken" if errors else "working",
            errors=errors,
            warnings=warnings,
            last_check=datetime.now().isoformat(),
            raw_output=output,
            checker_used="ruff"
        )
    
    # =========================================================================
    # Python Checking - py_compile (syntax check)
    # =========================================================================
    
    def check_python_syntax(self, file_path: str) -> HealthCheckResult:
        """
        Check Python file syntax using py_compile.
        Always available - uses Python's built-in compiler.
        
        Args:
            file_path: Path to Python file to check
        """
        errors = []
        full_path = self.project_root / file_path
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(full_path)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            if result.returncode != 0:
                # Parse syntax error
                output = result.stderr
                # Format: File "path", line X
                match = re.search(r'File "([^"]+)", line (\d+)', output)
                if match:
                    # Get the actual error message (usually on the last line)
                    lines = output.strip().split('\n')
                    message = lines[-1] if lines else "Syntax error"
                    
                    errors.append(ParsedError(
                        file=match.group(1),
                        line=int(match.group(2)),
                        error_code="SyntaxError",
                        message=message
                    ))
                else:
                    errors.append(ParsedError(
                        file=file_path,
                        line=0,
                        error_code="SyntaxError",
                        message=output.strip()
                    ))
        except subprocess.TimeoutExpired:
            errors.append(ParsedError(
                file=file_path,
                line=0,
                message="Syntax check timed out"
            ))
        except Exception as e:
            errors.append(ParsedError(
                file=file_path,
                line=0,
                message=str(e)
            ))
        
        return HealthCheckResult(
            status="broken" if errors else "working",
            errors=errors,
            last_check=datetime.now().isoformat(),
            checker_used="py_compile"
        )
    
    # =========================================================================
    # Unified Check Interface
    # =========================================================================
    
    def check_fiefdom(self, fiefdom_path: str) -> HealthCheckResult:
        """
        Run appropriate health check for a fiefdom based on file type.
        Auto-detects whether to use TypeScript or Python checkers.
        
        Args:
            fiefdom_path: Relative path from project root
            
        Returns:
            HealthCheckResult with combined errors from all applicable checkers
        """
        full_path = self.project_root / fiefdom_path
        
        # Determine file types in fiefdom
        has_python = False
        has_typescript = False
        python_files = []
        
        if full_path.is_file():
            ext = full_path.suffix.lower()
            has_python = ext == '.py'
            has_typescript = ext in {'.ts', '.tsx', '.js', '.jsx'}
            if has_python:
                python_files.append(fiefdom_path)
        else:
            for f in full_path.rglob('*'):
                if f.is_file():
                    ext = f.suffix.lower()
                    if ext == '.py':
                        has_python = True
                        python_files.append(str(f.relative_to(self.project_root)))
                    elif ext in {'.ts', '.tsx', '.js', '.jsx'}:
                        has_typescript = True
        
        all_errors: List[ParsedError] = []
        all_warnings: List[ParsedError] = []
        checkers_used = []
        raw_outputs = []
        
        # Run TypeScript check if applicable
        if has_typescript and self._available_checkers.get(CheckerType.TYPESCRIPT):
            ts_result = self.check_typescript(fiefdom_path)
            all_errors.extend(ts_result.errors)
            all_warnings.extend(ts_result.warnings)
            checkers_used.append("typescript")
            if ts_result.raw_output:
                raw_outputs.append(ts_result.raw_output)
        
        # Run Python checks if applicable
        if has_python:
            # Priority: ruff > mypy > py_compile
            if self._available_checkers.get(CheckerType.PYTHON_RUFF):
                ruff_result = self.check_ruff(fiefdom_path)
                all_errors.extend(ruff_result.errors)
                all_warnings.extend(ruff_result.warnings)
                checkers_used.append("ruff")
                if ruff_result.raw_output:
                    raw_outputs.append(ruff_result.raw_output)
            
            if self._available_checkers.get(CheckerType.PYTHON_MYPY):
                mypy_result = self.check_mypy(fiefdom_path)
                all_errors.extend(mypy_result.errors)
                all_warnings.extend(mypy_result.warnings)
                checkers_used.append("mypy")
                if mypy_result.raw_output:
                    raw_outputs.append(mypy_result.raw_output)
            
            # Always do syntax check as fallback if no other Python checkers
            if not (self._available_checkers.get(CheckerType.PYTHON_RUFF) or 
                    self._available_checkers.get(CheckerType.PYTHON_MYPY)):
                for py_file in python_files:
                    syntax_result = self.check_python_syntax(py_file)
                    all_errors.extend(syntax_result.errors)
                    checkers_used.append("py_compile")
        
        # Fallback: if nothing ran, at least do syntax check on Python files
        if not checkers_used and has_python:
            for py_file in python_files:
                syntax_result = self.check_python_syntax(py_file)
                all_errors.extend(syntax_result.errors)
            checkers_used.append("py_compile (fallback)")
        
        return HealthCheckResult(
            status="broken" if all_errors else "working",
            errors=all_errors,
            warnings=all_warnings,
            last_check=datetime.now().isoformat(),
            raw_output="\n---\n".join(raw_outputs),
            checker_used=", ".join(checkers_used) if checkers_used else "none"
        )
    
    def check_all_fiefdoms(
        self, fiefdom_paths: List[str]
    ) -> Dict[str, HealthCheckResult]:
        """
        Run health check for multiple fiefdoms.
        Optimizes by running project-wide checks once and filtering.
        """
        results = {}
        
        # Run project-wide checks once
        ts_result = None
        ruff_result = None
        mypy_result = None
        
        if self._available_checkers.get(CheckerType.TYPESCRIPT):
            ts_result = self.check_typescript()
        
        if self._available_checkers.get(CheckerType.PYTHON_RUFF):
            ruff_result = self.check_ruff()
        
        if self._available_checkers.get(CheckerType.PYTHON_MYPY):
            mypy_result = self.check_mypy()
        
        # Filter results per fiefdom
        for fiefdom in fiefdom_paths:
            errors = []
            warnings = []
            checkers = []
            
            if ts_result:
                errors.extend(ts_result.get_errors_for_file(fiefdom))
                checkers.append("typescript")
            
            if ruff_result:
                errors.extend(ruff_result.get_errors_for_file(fiefdom))
                checkers.append("ruff")
            
            if mypy_result:
                errors.extend(mypy_result.get_errors_for_file(fiefdom))
                checkers.append("mypy")
            
            results[fiefdom] = HealthCheckResult(
                status="broken" if errors else "working",
                errors=errors,
                warnings=warnings,
                last_check=datetime.now().isoformat(),
                checker_used=", ".join(checkers)
            )
        
        return results


if __name__ == "__main__":
    # Quick test
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    target = sys.argv[2] if len(sys.argv) > 2 else None
    
    checker = HealthChecker(root)
    
    print(f"\n=== Health Checker Report ===")
    print(f"Project: {root}")
    print(f"Available checkers: {[c.value for c in checker.get_available_checkers()]}")
    
    if target:
        result = checker.check_fiefdom(target)
    else:
        # Quick Python check on the IP directory if it exists
        ip_dir = Path(root) / "IP"
        if ip_dir.exists():
            result = checker.check_fiefdom("IP")
        else:
            result = checker.check_fiefdom(".")
    
    print(f"\nChecker(s) used: {result.checker_used}")
    print(f"Status: {result.status}")
    print(f"Errors: {result.error_count}")
    print(f"Warnings: {result.warning_count}")
    
    if result.errors:
        print(f"\n--- Errors ---")
        for err in result.errors[:10]:  # Show first 10
            print(f"  {err}")
        if len(result.errors) > 10:
            print(f"  ... and {len(result.errors) - 10} more")
