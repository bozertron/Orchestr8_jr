# barradeau_builder.py Integration Guide

- Source: `IP/barradeau_builder.py`
- Total lines: `440`
- SHA256: `pending`
- Role: **Barradeau Building Generator** — Particle-based 3D building generation using Delaunay triangulation

## Why This Is Painful

- Delaunay triangulation algorithm is complex — Bowyer-Watson requires careful implementation
- Particle placement must follow Barradeau edge-filtering technique exactly
- Color MUST use 0xD4AF37 (canonical gold), NOT 0xC9A962 from reference
- NO breathing animations — buildings EMERGE only

## Anchor Lines

- `IP/barradeau_builder.py:20` — `CONFIG = {...}` — All scaling constants in one place
- `IP/barradeau_builder.py:29` — `"COLOR_WORKING": 0xD4AF37` — Canonical gold (NOT 0xC9A962)
- `IP/barradeau_builder.py:30-32` — Three-state colors: gold, teal, purple
- `IP/barradeau_builder.py:49` — `@dataclass class Point2D` — 2D point for footprint
- `IP/barradeau_builder.py:59` — `@dataclass class Point3D` — 3D point with opacity/size
- `IP/barradeau_builder.py:83` — `@dataclass class BuildingData` — Output dataclass for JS
- `IP/barradeau_builder.py:109` — `class Delaunay` — Bowyer-Watson triangulation
- `IP/barradeau_builder.py:112` — `def triangulate()` — Main algorithm (ported from lines 727-803)
- `IP/barradeau_builder.py:186` — `class BarradeauBuilding` — Building generator
- `IP/barradeau_builder.py:227` — `def _calculate_dimensions()` — Height/footprint formulas (LOCKED)
- `IP/barradeau_builder.py:236` — `def _generate_footprint()` — Point generation for triangulation
- `IP/barradeau_builder.py:268` — `def _extrude_building()` — Barradeau particle placement
- `IP/barradeau_builder.py:299` — Edge length filtering (creates ethereal fade)

## Integration Use

- `BarradeauBuilding(path, line_count, export_count, status)` — Create building from file metrics
- `building.get_building_data()` — Get BuildingData for JSON serialization
- `get_status_color_hex(status)` — Get hex string for status ("#D4AF37")
- `get_status_color_int(status)` — Get int for Three.js (0xD4AF37)

## LOCKED Formulas

| Formula | Expression | Source |
|---------|------------|--------|
| Footprint | `2 + (lines × 0.008)` | CONFIG.BASE_FOOTPRINT + FOOTPRINT_SCALE |
| Height | `3 + (exports × 0.8)` | CONFIG.MIN_HEIGHT + HEIGHT_PER_EXPORT |
| Layer count | 15 | CONFIG.LAYER_COUNT |
| Taper | 0.015 | CONFIG.TAPER |
| Particles/unit | 1.2 | CONFIG.PARTICLES_PER_UNIT |

## Barradeau Technique

```
Delaunay Triangulation → Edge Extraction → Length-Based Filtering → Particle Placement
```

**Key insight**: Shorter edges get MORE particles. At higher layers, longer edges are filtered out entirely, creating the ethereal fade effect.

## Resolved Gaps

- [x] Delaunay triangulation ported from void-phase0-buildings.html
- [x] BarradeauBuilding class with particle/edge generation
- [x] BuildingData dataclass with to_json() for JS consumption
- [x] Canonical color system (0xD4AF37, 0x1fbdea, 0x9D4EDD)
- [x] Edge length filtering for ethereal fade effect
