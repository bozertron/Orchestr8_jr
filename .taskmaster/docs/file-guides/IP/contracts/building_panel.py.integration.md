# building_panel.py Integration Guide

- Source: `IP/contracts/building_panel.py`
- Total lines: `134`
- SHA256: `6a4bd9ea1d9f9c00676df3ee075f4a9e8252859c803ac6dfb1b8dae64bc4ea40`
- Role: **Building inspection panel data contract** — defines BuildingPanel and BuildingRoom schemas for Code City building click events

## Why This Is Painful

- Contract-to-UI wiring gap: The schema is defined, but no runtime path generates BuildingPanel payloads from CodeNode data yet.
- Lock state integration: The contract includes `lock_state` and `locked` fields, but Louis integration is not yet wired to populate these.
- Room parsing complexity: BuildingRoom extraction from source files (functions/classes) requires AST parsing, not yet implemented in the woven_maps scan path.

## Anchor Lines

- `IP/contracts/building_panel.py:10` — `BuildingStatus = Literal["working", "broken", "combat"]` — canonical status type
- `IP/contracts/building_panel.py:14` — `class BuildingRoom` — represents a function or class inside a file (a "room")
- `IP/contracts/building_panel.py:18-19` — `line_start`, `line_end` — room boundaries for code navigation
- `IP/contracts/building_panel.py:20` — `room_type: Literal["function", "class", "method"]` — room classification
- `IP/contracts/building_panel.py:29` — `class BuildingPanel` — main data contract for building inspection panel
- `IP/contracts/building_panel.py:36` — `path: str` — file path (canonical identifier)
- `IP/contracts/building_panel.py:37` — `status: BuildingStatus` — working/broken/combat state
- `IP/contracts/building_panel.py:39-41` — `export_count`, `building_height`, `footprint` — geometry metadata using locked formulas
- `IP/contracts/building_panel.py:42-43` — `imports: List[str]`, `exports: List[str]` — file dependencies and public API
- `IP/contracts/building_panel.py:44` — `rooms: List[BuildingRoom]` — functions/classes inside the file
- `IP/contracts/building_panel.py:45-46` — `connections_in`, `connections_out` — files that import this / files this imports
- `IP/contracts/building_panel.py:47-48` — `lock_state`, `locked` — Louis lock system integration
- `IP/contracts/building_panel.py:60` — `def validate_building_panel(payload: dict)` — validation function with error handling
- `IP/contracts/building_panel.py:101` — `EXAMPLE_BUILDING_PANEL` — canonical example showing expected structure

## Integration Use

- When a user clicks a building (file) in Code City, the click handler should:
  1. Convert the clicked CodeNode into a BuildingPanel payload
  2. Validate using `validate_building_panel()`
  3. Pass the validated panel to the UI component
- Room extraction requires implementing AST-based scanning for Python files (and potentially JS/TS files)
- Lock state should be populated from Louis lock system queries before panel display

## Integration Gaps

- [ ] No runtime path exists to generate BuildingPanel from CodeNode click events
- [ ] Room extraction (AST parsing for functions/classes) not implemented in woven_maps
- [ ] Louis lock state integration not wired into panel payload generation
- [ ] Connection directionality (in vs out) needs ConnectionVerifier integration

## Resolved Gaps

- [x] BuildingPanel schema defined with all required fields
- [x] Validation function provides error handling and type safety
- [x] Geometry fields (height/footprint) match locked formulas from canon
- [x] Example payload demonstrates expected structure
