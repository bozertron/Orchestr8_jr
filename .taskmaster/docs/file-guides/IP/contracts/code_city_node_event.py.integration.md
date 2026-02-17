# contracts/code_city_node_event.py Integration Guide

- Source: `IP/contracts/code_city_node_event.py`
- Total lines: `61`
- SHA256: `6b3e83fb7b126d9783802333c1f96747bea5e6b842727725cf25195afdf9a912`
- Role: **Node Click Event Schema** — Typed bridge between JS Code City events and Python handlers

## Why This Is Painful

- JS payload uses camelCase (nodeType, inCycle) but Python convention is snake_case
- Required vs optional fields must be validated before use
- Malformed payloads from iframe must be handled gracefully without crashing

## Anchor Lines

- `IP/contracts/code_city_node_event.py:4` — `CodeCityStatus = Literal["working", "broken", "combat"]` — Status type
- `IP/contracts/code_city_node_event.py:7` — `@dataclass class CodeCityNodeEvent` — Event dataclass
- `IP/contracts/code_city_node_event.py:9-11` — Required fields: path, status, loc
- `IP/contracts/code_city_node_event.py:12-17` — Optional fields with defaults
- `IP/contracts/code_city_node_event.py:19` — `def to_dict(self)` — Serialization via asdict()
- `IP/contracts/code_city_node_event.py:23` — `def validate_code_city_node_event(payload)` — Validation function
- `IP/contracts/code_city_node_event.py:28-30` — Required field check (path, status, loc)
- `IP/contracts/code_city_node_event.py:32-33` — Status enum validation
- `IP/contracts/code_city_node_event.py:49` — `EXAMPLE_NODE_EVENT` — Test fixture

## Integration Use

- **06_maestro.py bridge**: Receives postMessage from iframe, validates via `validate_code_city_node_event()`
- **woven_maps.py**: Emits structured payloads at line 2688 that match this schema
- **Validation flow**: raw_payload → validate_code_city_node_event() → CodeCityNodeEvent → to_dict()

## Field Mapping (JS → Python)

| JS Field | Python Field | Required | Notes |
|----------|--------------|----------|-------|
| path | path | Yes | File path |
| status | status | Yes | working/broken/combat |
| loc | loc | Yes | Line count |
| errors | errors | No | List of error strings |
| nodeType | nodeType | No | 'file' or 'directory' |
| centrality | centrality | No | 0-1 float |
| inCycle | inCycle | No | Boolean for import cycles |

## Resolved Gaps

- [x] Schema matches JS postMessage payload structure exactly
- [x] Validation raises ValueError with specific field name on missing required
- [x] Optional fields default to None or empty list
- [x] EXAMPLE_NODE_EVENT provides test fixture
