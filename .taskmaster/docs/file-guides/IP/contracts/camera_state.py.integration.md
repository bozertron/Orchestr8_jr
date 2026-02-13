# contracts/camera_state.py Integration Guide

- Source: `IP/contracts/camera_state.py`
- Total lines: `44`
- SHA256: `37753c3c24ae0cb9dc16aae5be8158021073776240a0bd11910a64645f546b73`
- Role: **Camera State Schema** — Code City camera position, mode, and animation state

## Why This Is Painful

- Camera modes must match JS expectations in woven_maps.py template
- Position bounds must be validated before sending to renderer
- Return stack navigation state must be preserved across mode transitions

## Anchor Lines

- `IP/contracts/camera_state.py:4` — `CameraMode = Literal["overview", "dive", "focus", "room", "sitting_room"]` — Mode type
- `IP/contracts/camera_state.py:7` — `@dataclass class CameraState` — State dataclass
- `IP/contracts/camera_state.py:9-12` — Core fields: mode, position, target, zoom
- `IP/contracts/camera_state.py:13-15` — Default fields: return_stack, transition_ms, easing
- `IP/contracts/camera_state.py:17` — `def clamp_zoom()` — Zoom bounds utility
- `IP/contracts/camera_state.py:22` — `def normalize_position()` — Position bounds utility
- `IP/contracts/camera_state.py:31` — `def get_default_camera_state()` — Factory function

## Integration Use

- **Initial state**: `get_default_camera_state()` provides bird's eye view
- **Mode transitions**: Create new CameraState with different mode, preserving return_stack
- **Bounds validation**: Call `clamp_zoom()` and `normalize_position()` before rendering

## Default Camera State

| Field | Value | Purpose |
|-------|-------|---------|
| mode | "overview" | Bird's eye view |
| position | (0.0, 500.0, 800.0) | Above and behind scene |
| target | (0.0, 0.0, 0.0) | Looking at origin |
| zoom | 1.0 | Normal zoom |
| transition_ms | 1500 | 1.5s transitions |
| easing | "easeInOutCubic" | Smooth easing |

## Camera Modes

| Mode | Purpose |
|------|---------|
| overview | Full Code City view |
| dive | Zooming into a fiefdom |
| focus | Single building focus |
| room | Inside a function/class |
| sitting_room | Deep detail view |

## Resolved Gaps

- [x] All camera modes defined as Literal type
- [x] clamp_zoom() constrains to safe range (0.1-10.0)
- [x] normalize_position() clamps to scene bounds
- [x] get_default_camera_state() provides sensible defaults
