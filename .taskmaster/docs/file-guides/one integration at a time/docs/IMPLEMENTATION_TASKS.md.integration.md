# IMPLEMENTATION_TASKS.md Integration Guide

- Source: `one integration at a time/docs/IMPLEMENTATION_TASKS.md`
- Total lines: `799`
- SHA256: `c74009eeb72a983e2e6767bda2a6e2021d66863eea1ba97727009c6c4b778615`
- Memory chunks: `7`
- Observation IDs: `436..442`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:38` WORKING = "working"    # Gold - healthy
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:40` COMBAT = "combat"      # Purple - general deployed
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:134` self.state_file = self.project_root / ".orchestr8" / "state" / "fiefdom-status.json"
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:273` class HealthChecker:
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:357` python -c "from IP.health_checker import HealthChecker, HealthCheckResult; print('OK')"
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:482` briefing += f"| `{lock['file']}` | 🔒 LOCKED | {lock['reason']} |\n"
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:589` print('❌ BLOCKED BY LOUIS:')
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:634` from health_checker import HealthChecker
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:639` config_path = Path('.orchestr8/state/fiefdom-status.json')
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:647` checker = HealthChecker('.')
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:675` ### Task BP-007: Create .orchestr8 Directory Structure
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:682` mkdir -p .orchestr8/tickets/archive
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:683` mkdir -p .orchestr8/state
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:686` cat > .orchestr8/state/fiefdom-status.json << 'EOF'
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:694` # Create .gitignore for orchestr8
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:695` cat > .orchestr8/.gitignore << 'EOF'
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:708` touch .orchestr8/tickets/archive/.gitkeep
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:715` ### Task BP-008: Update 06_maestro.py to Use New Modules
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:717` **File:** `IP/plugins/06_maestro.py`
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:729` # Add imports at top of 06_maestro.py
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:732` from IP.health_checker import HealthChecker
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:737` checker = HealthChecker(project_root)
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:790` | BP-007 | .orchestr8 directory | 15 min | 3 |
- `one integration at a time/docs/IMPLEMENTATION_TASKS.md:791` | BP-008 | 06_maestro.py integration | 2 hours | 4 |

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
