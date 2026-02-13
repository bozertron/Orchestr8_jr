# base_panel.py Integration Guide

- Source: `one integration at a time/IP--888/panel_foundation/base_panel.py`
- Total lines: `275`
- SHA256: `0ec8e148ed4b46bbec1ebfb112900f12a9c8182eeb32972024acc53c2177f933`
- Memory chunks: `3`
- Observation IDs: `650..652`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/IP--888/panel_foundation/base_panel.py:3` Base Panel - Abstract base class that ALL [name]8 tools must implement
- `one integration at a time/IP--888/panel_foundation/base_panel.py:73` All panels must implement this interface to work with Orchestr8's
- `one integration at a time/IP--888/panel_foundation/base_panel.py:110` config: Panel configuration from orchestr8_settings.toml

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
