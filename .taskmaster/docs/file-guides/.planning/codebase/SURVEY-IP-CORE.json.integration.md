# SURVEY-IP-CORE.json Integration Guide

- Source: `.planning/codebase/SURVEY-IP-CORE.json`
- Total lines: `207`
- SHA256: `b31e7771e4004a6523bdb4f93787f1d8b28e04b4e873b0e0d9e71dfcf37bd45a`
- Memory chunks: `2`
- Observation IDs: `1032..1033`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/codebase/SURVEY-IP-CORE.json:46` "purpose": "TypeScript context bridge for unified project analysis",
- `.planning/codebase/SURVEY-IP-CORE.json:115` "critical_finding": "HealthChecker is imported in 06_maestro.py (line 77) but NEVER instantiated - requirement HLTH-01 not met",
- `.planning/codebase/SURVEY-IP-CORE.json:117` "exports": ["CheckerType", "ParsedError", "HealthCheckResult", "HealthChecker"],
- `.planning/codebase/SURVEY-IP-CORE.json:176` "critical_finding": "Does not currently accept health data from HealthChecker - requirement HLTH-02 not met",
- `.planning/codebase/SURVEY-IP-CORE.json:195` {"file": "IP/health_checker.py", "line": 1, "issue": "HealthChecker imported but never instantiated in 06_maestro.py", "requirement": "HLTH-01", "impact": "Health checking disabled"},
- `.planning/codebase/SURVEY-IP-CORE.json:196` {"file": "IP/woven_maps.py", "line": 1, "issue": "Does not accept health data from HealthChecker", "requirement": "HLTH-02", "impact": "Code City colors don't reflect file health"}

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
