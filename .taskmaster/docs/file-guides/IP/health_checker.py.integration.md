# health_checker.py Integration Guide

- Source: `IP/health_checker.py`
- Total lines: `623`
- SHA256: `cae9cb01cb7858c8a0f43ce8e4fc44b13ab8c48cc3e5155826f5170874ed332a`
- Role: **Health pipeline core** — runs static analysis (TypeScript/mypy/ruff/py_compile), produces HealthCheckResult feeding Blue status

## Why This Is Painful

- ~~Output not reaching Code City~~: **RESOLVED** — `build_code_city()` in 06_maestro.py now passes `get_health()` to `create_code_city()`, which calls `build_from_health_results()` to merge results into node colors.
- ~~`HealthCheckResult` lacks `to_dict()`~~: **RESOLVED** — `to_dict()` added (line 64) returning status, errors, warnings, counts, last_check, checker_used.
- `check_all_fiefdoms()` filters project-wide results per fiefdom, but never called: The optimized batch path (line 539) exists but 06_maestro.py calls individual `check_fiefdom()` through HealthWatcher instead.

## Anchor Lines

- `IP/health_checker.py:18` — `class CheckerType(Enum)` — typescript, python_mypy, python_ruff, python_compile
- `IP/health_checker.py:26` — `@dataclass class ParsedError` — file, line, column, error_code, message, severity
- `IP/health_checker.py:44` — `@dataclass class HealthCheckResult` — status (working|broken), errors, warnings, last_check
- `IP/health_checker.py:64` — `def to_dict()` — serialization for state storage and cross-component transport
- `IP/health_checker.py:88` — `class HealthChecker` — multi-language checker, auto-detects available tools
- `IP/health_checker.py:96` — `_detect_available_checkers()` — probes for npm, mypy, ruff at init
- `IP/health_checker.py:448` — `def check_fiefdom(fiefdom_path)` — unified check, auto-detects file type, runs applicable checkers
- `IP/health_checker.py:498` — Python check priority: `ruff > mypy > py_compile`
- `IP/health_checker.py:539` — `def check_all_fiefdoms()` — batch check, runs project-wide once then filters (not called)

## Integration Use

- `to_dict()`: **DONE** — `HealthCheckResult.to_dict()` available for consistent JSON serialization.
- Health flow: **DONE** — `refresh_health()` and `on_health_change()` store results in `STATE_MANAGERS["health"]`, `build_code_city()` passes them to `create_code_city(health_results=...)`.
- Test: Run `check_fiefdom("IP/")` and verify `HealthCheckResult.status` is "working" or "broken" with correct error count.

## Resolved Gaps

- [x] to_dict() added to HealthCheckResult for serialization consistency
- [x] Health results now flow end-to-end: HealthChecker → STATE_MANAGERS → create_code_city → build_from_health_results → colored nodes
