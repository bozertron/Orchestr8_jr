# MASTER_ROADMAP.md Integration Guide

- Source: `SOT/MASTER_ROADMAP.md`
- Total lines: `690`
- SHA256: `9a76ca463d3252796ced8431d1e09d2c08b609e185c5a7dd6e3532bfd0de6c1f`
- Memory chunks: `6`
- Observation IDs: `139..144`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `SOT/MASTER_ROADMAP.md:51` **Goal**: Replace all legacy brand references with "orchestr8"
- `SOT/MASTER_ROADMAP.md:55` - Brand text in 06_maestro.py
- `SOT/MASTER_ROADMAP.md:68` 1. `orchestr8` button → Returns to home state
- `SOT/MASTER_ROADMAP.md:69` 2. `collabor8` button → Opens agent dropdown (slides LEFT)
- `SOT/MASTER_ROADMAP.md:70` 3. `JFDI` button → Opens TicketPanel (slides RIGHT)
- `SOT/MASTER_ROADMAP.md:79` **Files:** `IP/plugins/06_maestro.py` (lines 892-920)
- `SOT/MASTER_ROADMAP.md:85` **Goal**: HealthChecker influences Code City colors
- `SOT/MASTER_ROADMAP.md:89` 1. Instantiate HealthChecker in 06_maestro.py
- `SOT/MASTER_ROADMAP.md:91` 3. Buildings show Gold/Blue/Purple based on health
- `SOT/MASTER_ROADMAP.md:95` - `health = HealthChecker(project_root)` exists
- `SOT/MASTER_ROADMAP.md:99` **Files:** `IP/plugins/06_maestro.py`, `IP/health_checker.py`, `IP/woven_maps.py`
- `SOT/MASTER_ROADMAP.md:109` 1. Parse existing campaign logs from `.orchestr8/campaigns/`
- `SOT/MASTER_ROADMAP.md:119` **Files:** `IP/briefing_generator.py`, `IP/plugins/06_maestro.py`
- `SOT/MASTER_ROADMAP.md:139` **Files:** `IP/combat_tracker.py`, `IP/plugins/06_maestro.py`
- `SOT/MASTER_ROADMAP.md:155` - ✅ Branding (orchestr8)
- `SOT/MASTER_ROADMAP.md:157` - ✅ Health Integration (HealthChecker)
- `SOT/MASTER_ROADMAP.md:193` **Files:** New `IP/mission_manager.py`, update `IP/plugins/06_maestro.py`
- `SOT/MASTER_ROADMAP.md:205` 1. **Collabor8 Panel** (Lines 1037-1057 in 06_maestro.py)
- `SOT/MASTER_ROADMAP.md:210` 2. **Summon Panel** (Lines 1081-1095 in 06_maestro.py)
- `SOT/MASTER_ROADMAP.md:221` **Files:** `IP/plugins/06_maestro.py`, `IP/carl_core.py`
- `SOT/MASTER_ROADMAP.md:243` **Files:** `IP/carl_core.py`, `IP/briefing_generator.py`, `IP/plugins/06_maestro.py`
- `SOT/MASTER_ROADMAP.md:262` | Generator | `01_generator.py` | Persist phase state to `.orchestr8/generator_state.json` |
- `SOT/MASTER_ROADMAP.md:290` Add to `orchestr8_settings.toml`:
- `SOT/MASTER_ROADMAP.md:315` **Files:** `orchestr8_settings.toml`, spawner, health_checker, connection_verifier
- `SOT/MASTER_ROADMAP.md:355` - [ ] `marimo run orchestr8.py` runs clean with all features working

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
