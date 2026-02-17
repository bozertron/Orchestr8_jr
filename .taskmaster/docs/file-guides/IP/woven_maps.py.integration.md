# woven_maps.py Integration Guide

- Source: `IP/woven_maps.py`
- Total lines: `946`
- SHA256: `e3c253a1ffe66972216fe487ac8acc46ac584d0a554803cdeee23e42f1abc82e`
- Role: **Code City facade module** — canonical dataclasses/constants and compatibility wrappers that delegate rendering + graph assembly to `IP/features/code_city/*`

## Why This Is Painful

- Legacy assumptions still expect a monolithic renderer in this file.
- Runtime behavior now spans delegated modules and an external template file.
- Contract drift can occur if wrapper signatures diverge from feature-module internals.

## Anchor Lines

- `IP/woven_maps.py:69` canonical JS color map (`working/broken/combat`)
- `IP/woven_maps.py:212` `compute_building_geometry(...)` locked formula
- `IP/woven_maps.py:720` `build_graph_data(...)` wrapper
- `IP/woven_maps.py:795` `build_from_connection_graph(...)` wrapper
- `IP/woven_maps.py:816` `build_from_health_results(...)` wrapper
- `IP/woven_maps.py:911` `create_code_city(...)` wrapper

## Integration Use

- Patchbay panel runtime now lives in `IP/static/woven_maps_template.html`.
- Graph assembly lives in `IP/features/code_city/graph_builder.py`.
- Render composition lives in `IP/features/code_city/render.py`.

## Open Gaps

None at facade level; active runtime validation gap is tracked in `IP/static/woven_maps_template.html.integration.md` (Taskmaster `#24` browser artifact coverage).
