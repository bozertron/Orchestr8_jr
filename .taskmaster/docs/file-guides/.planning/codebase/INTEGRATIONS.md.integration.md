# INTEGRATIONS.md Integration Guide

- Source: `.planning/codebase/INTEGRATIONS.md`
- Total lines: `238`
- SHA256: `4515307a2e7adccc501521c7b2f1da7789f036b5ca8c3a4dbb79552c3fadbce8`
- Memory chunks: `2`
- Observation IDs: `1016..1017`

## Why This Is Painful

- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/codebase/INTEGRATIONS.md:9` - SDK/Client: `anthropic` (imported in `IP/plugins/06_maestro.py`)
- `.planning/codebase/INTEGRATIONS.md:47` - Connection: `.orchestr8/public_services.db`
- `.planning/codebase/INTEGRATIONS.md:50` - Example: `.orchestr8/combat_state.json` for LLM deployment tracking
- `.planning/codebase/INTEGRATIONS.md:56` - Auto-backup: Enabled via `pyproject_orchestr8_settings.toml`
- `.planning/codebase/INTEGRATIONS.md:69` - `.orchestr8/combat_state.json` - LLM deployment tracking
- `.planning/codebase/INTEGRATIONS.md:70` - `.orchestr8/state/` - General state directory
- `.planning/codebase/INTEGRATIONS.md:71` - `.orchestr8/tickets/` - Ticket system data
- `.planning/codebase/INTEGRATIONS.md:72` - `.orchestr8/logs/system.log` - Application logs
- `.planning/codebase/INTEGRATIONS.md:73` - `.orchestr8/backups/` - Local backups
- `.planning/codebase/INTEGRATIONS.md:74` - `.orchestr8/public_services.db` - SQLite database
- `.planning/codebase/INTEGRATIONS.md:103` - Path: `.orchestr8/logs/system.log`
- `.planning/codebase/INTEGRATIONS.md:113` - Results feed into Woven Maps visualization (Blue=broken, Gold=working)
- `.planning/codebase/INTEGRATIONS.md:136` - Template directory: `~/.orchestr8/templates/onlyoffice`
- `.planning/codebase/INTEGRATIONS.md:150` - Project directory: `~/.orchestr8/projects/audio`
- `.planning/codebase/INTEGRATIONS.md:156` - Plugin directory: `~/.orchestr8/plugins/gimp`
- `.planning/codebase/INTEGRATIONS.md:162` - Project directory: `~/.orchestr8/projects/3d`
- `.planning/codebase/INTEGRATIONS.md:163` - Python scripts path: `~/.orchestr8/scripts/blender`
- `.planning/codebase/INTEGRATIONS.md:194` - Settings file: `pyproject_orchestr8_settings.toml` (contains placeholders for secrets)
- `.planning/codebase/INTEGRATIONS.md:232` - Primary: `~/.orchestr8/backups/`
- `.planning/codebase/INTEGRATIONS.md:233` - Secondary: `[external_drive_path]/orchestr8_backups/` (optional)

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
