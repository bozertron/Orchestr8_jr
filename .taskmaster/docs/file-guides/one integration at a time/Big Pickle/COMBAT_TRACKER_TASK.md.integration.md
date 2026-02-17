# COMBAT_TRACKER_TASK.md Integration Guide

- Source: `one integration at a time/Big Pickle/COMBAT_TRACKER_TASK.md`
- Total lines: `61`
- SHA256: `a86855d8b47d124758186570869100aeabce4fd1809ac12a9cf3bb35dd9e6836`
- Memory chunks: `1`
- Observation IDs: `369..369`

## Why This Is Painful

- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/Big Pickle/COMBAT_TRACKER_TASK.md:13` Create `IP/combat_tracker.py` - tracks which files have an LLM General deployed (Purple/COMBAT status)
- `one integration at a time/Big Pickle/COMBAT_TRACKER_TASK.md:18` Location: `.orchestr8/combat_state.json`
- `one integration at a time/Big Pickle/COMBAT_TRACKER_TASK.md:22` "IP/plugins/06_maestro.py": {
- `one integration at a time/Big Pickle/COMBAT_TRACKER_TASK.md:43` - `mermaid_generator.py` can call `tracker.get_combat_files()` to set Purple status
- `one integration at a time/Big Pickle/COMBAT_TRACKER_TASK.md:44` - `terminal_spawner.py` should call `tracker.deploy()` when spawning
- `one integration at a time/Big Pickle/COMBAT_TRACKER_TASK.md:48` Create `.orchestr8/` if it doesn't exist (like `.git/`)

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
