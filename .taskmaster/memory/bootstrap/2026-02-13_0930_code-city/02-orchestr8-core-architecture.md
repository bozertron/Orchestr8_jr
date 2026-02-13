# Orchestr8 Core Architecture Reference

## Entrypoints and core runtime

- Main entry: `orchestr8.py`
- Plugin shell target: `IP/plugins/06_maestro.py`
- Code City visuals: `IP/woven_maps.py`

## State topology

- Root state built via `mo.state()` channels and `STATE_MANAGERS` lookup map.
- Plugins loaded in explicit order using dynamic module loading.

## Health pipeline

1. File change event
2. HealthWatcher debounce
3. HealthChecker analysis
4. State update
5. Code City render status update

## Canon constraints

- Three-state colors only: Gold (working), Teal (broken), Purple (combat).
- Status precedence: combat > broken > working.
- Emergence-only motion policy (no breathing/pulsing).
