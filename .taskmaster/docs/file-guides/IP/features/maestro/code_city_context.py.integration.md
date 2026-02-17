# code_city_context.py Integration Guide

- Source: `IP/features/maestro/code_city_context.py`
- Total lines: `294`
- SHA256: `1842458832b66353ef60b1afda3adb0162d6f1e8803532856bef821cc7d5003b`
- Role: **Code City context handoff assembler** — normalizes node click payloads into validated building/room context for Summon, Collabor8, and Sitting Room transitions

## Why This Is Painful

- Must reconcile raw node event payloads with Carl context, health signals, and lock data.
- Room extraction has language-specific behavior (AST for Python, best-effort fallback for others).
- Handoff payload shape must remain stable across multiple UI consumers.

## Anchor Lines

- `IP/features/maestro/code_city_context.py:18` `derive_context_scope(...)`
- `IP/features/maestro/code_city_context.py:167` `build_building_panel_for_node(...)`
- `IP/features/maestro/code_city_context.py:232` `select_room_entry(...)`
- `IP/features/maestro/code_city_context.py:261` `build_code_city_context_payload(...)`

## Integration Use

- Building panel payloads are validated through `validate_building_panel(...)` before UI handoff.
- Room-entry triggers (`broken_room_entry` / `combat_room_focus`) drive sitting-room transitions.
- Context scope fallback logic supports Summon queries even when no manual file selection exists.

## Open Gaps

- [ ] Non-Python room extraction remains heuristic-only (line-level granularity)

