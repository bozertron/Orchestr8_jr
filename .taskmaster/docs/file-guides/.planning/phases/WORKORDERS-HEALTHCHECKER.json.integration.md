# WORKORDERS-HEALTHCHECKER.json Integration Guide

- Source: `.planning/phases/WORKORDERS-HEALTHCHECKER.json`
- Total lines: `403`
- SHA256: `c91a217bb8ef4bace9315f8b2b618d054e5c709d2ddba4f587cacfccc33e31a5`
- Memory chunks: `4`
- Observation IDs: `1069..1072`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:10` "wave_description": "Add health state to STATE_MANAGERS in 06_maestro.py"
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:14` "wave_name": "HealthWatcher Module",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:20` "wave_description": "Bridge HealthChecker results to CodeNode status in woven_maps.py"
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:25` "wave_description": "Wire HealthWatcher to reactive state in 06_maestro.py"
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:38` "file": "IP/plugins/06_maestro.py",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:43` "summary": "Add health state getter/setter to STATE_MANAGERS",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:45` "After line 356 (get_logs, set_logs = STATE_MANAGERS[\"logs\"]), add new health state pair",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:46` "Use pattern: get_health, set_health = STATE_MANAGERS.get(\"health\", mo.state({}))",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:51` "constraints": {
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:54` "STATE_MANAGERS dict structure passed from orchestr8.py"
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:60` "No syntax errors when running marimo edit orchestr8.py",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:74` "file": "IP/plugins/06_maestro.py",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:79` "summary": "Create refresh_health() function to run HealthChecker on project root",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:83` "Inside: get HealthChecker instance, call check_fiefdom on get_root()",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:88` "constraints": {
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:91` "HealthChecker core logic in IP/health_checker.py"
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:97` "Function uses HealthChecker imported at line 77",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:116` "summary": "Create HealthWatcher class with watchdog integration and 100ms debounce",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:120` "Import HealthChecker from IP.health_checker",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:121` "Class HealthWatcher with __init__(self, project_root: str, callback: Callable)",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:125` "In _debounced_check(): call HealthChecker.check_fiefdom on changed file, invoke callback with result"
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:128` "constraints": {
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:137` "HealthWatcher class has start_watching() and stop_watching() methods",
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:166` "constraints": {
- `.planning/phases/WORKORDERS-HEALTHCHECKER.json:194` "summary": "Add build_from_health_results() function to merge HealthChecker output into nodes",

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
