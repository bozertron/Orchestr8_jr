# WORKORDERS-FILEWATCHER.json Integration Guide

- Source: `.planning/phases/WORKORDERS-FILEWATCHER.json`
- Total lines: `351`
- SHA256: `c8df721a45848d1a36b2d96c83ea564a8f06a169721ec229584aa738cf66ad2c`
- Memory chunks: `3`
- Observation IDs: `1066..1068`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/phases/WORKORDERS-FILEWATCHER.json:14` "title": "Create HealthWatcherManager class skeleton",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:20` "description": "Create the HealthWatcherManager class with constructor and type hints",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:23` "Class HealthWatcherManager defined with __init__ signature",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:31` "Initialize _health_checker from IP.health_checker.HealthChecker",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:134` "__all__ = [\"HealthWatcherManager\"] defined",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:138` "Module docstring: Real-time file watcher bridge for health checking"
- `.planning/phases/WORKORDERS-FILEWATCHER.json:143` "title": "Import HealthWatcherManager in orchestr8.py",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:144` "file": "orchestr8.py",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:149` "description": "Add import statement for HealthWatcherManager",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:151` "Import statement exists: from IP.health_watcher import HealthWatcherManager",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:161` "title": "Initialize HEALTH_WATCHER singleton in orchestr8.py",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:162` "file": "orchestr8.py",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:167` "description": "Create module-level HealthWatcherManager instance",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:170` "Initialized with PROJECT_ROOT, STATE_MANAGERS, watch_paths=[\"IP/\"]",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:171` "Placed after STATE_MANAGERS initialization"
- `.planning/phases/WORKORDERS-FILEWATCHER.json:174` "Format: HEALTH_WATCHER = HealthWatcherManager(project_root=PROJECT_ROOT, state_managers=STATE_MANAGERS, watch_paths=[\"IP/\"])",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:181` "file": "orchestr8.py",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:193` "Check for existing app lifecycle hooks in orchestr8.py",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:200` "title": "Add health state key to STATE_MANAGERS if missing",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:201` "file": "orchestr8.py",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:208` "STATE_MANAGERS[\"health\"] exists",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:212` "Check existing STATE_MANAGERS initialization",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:219` "title": "Subscribe 06_maestro.py to health state changes",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:220` "file": "IP/plugins/06_maestro.py",
- `.planning/phases/WORKORDERS-FILEWATCHER.json:227` "STATE_MANAGERS[\"health\"] accessed in render function",

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
