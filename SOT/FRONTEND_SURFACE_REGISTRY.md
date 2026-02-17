# FRONTEND SURFACE REGISTRY

Owner: Orchestr8_jr (Canonical Lane)
Status: ACTIVE - v1
Last Updated: 2026-02-15
Evidence Links: orchestr8_ui_reference.html, Observation #1464

## Purpose

Authoritative registry of all frontend surfaces, their ownership, and placement contracts.

## Visual Baseline Reference

- Source: `/home/bozertron/Downloads/orchestr8_ui_reference.html`
- Structure: Top row + Void + Lower Fifth rhythm
- Interaction: Control semantics per flagship identity rules

## Surface Registry

### Layer 0: Overlay System

| Surface ID | Name | Owner | Frozen | Description |
|------------|------|-------|--------|-------------|
| `OVERLAY_START` | Start Overlay | Orchestr8_jr | YES | Initial button layer, z-index 9999 |
| `OVERLAY_SCANLINES` | Scanlines | Orchestr8_jr | YES | CRT effect overlay, z-index 900 |

### Layer 1: Canvas Layer

| Surface ID | Name | Owner | Frozen | Description |
|------------|------|-------|--------|-------------|
| `CANVAS_3D` | Main Canvas | Orchestr8_jr | YES | Three.js particle system, z-index 100 |
| `CANVAS_IDLE` | Idle Particles | Orchestr8_jr | NO | particles.js idle state, z-index 0 |

### Layer 2: UI Layer (z-index 50)

#### Header Section

| Surface ID | Name | Owner | Frozen | Description |
|------------|------|-------|--------|-------------|
| `HEADER_CONTAINER` | Header Container | Orchestr8_jr | YES | 80px height, gradient background |
| `BTN_ORCHESTR8` | [orchestr8] Button | Orchestr8_jr | YES | Left header button |
| `BTN_COLLABOR8` | COLLABOR8 Button | Orchestr8_jr | YES | Center header button (accent) |
| `BTN_JFDI` | [JFDI] Button | Orchestr8_jr | YES | Right header button |

#### Main Section (The Void)

| Surface ID | Name | Owner | Frozen | Description |
|------------|------|-------|--------|-------------|
| `VOID_CONTAINER` | Main Container | Orchestr8_jr | YES | Flex center, void label display |
| `VOID_LABEL` | The Void Label | Orchestr8_jr | YES | 0.04 opacity text, 3rem font |

#### Footer Section (Lower Fifth)

| Surface ID | Name | Owner | Frozen | Description |
|------------|------|-------|--------|-------------|
| `FOOTER_CONTAINER` | Footer Container | Orchestr8_jr | YES | Control surface, gradient background |
| `INPUT_MAESTRO` | Maestro Input Bar | Orchestr8_jr | YES | Command input, centered |
| `DECK_ROW` | Button Deck Row | Orchestr8_jr | YES | Button groups container |
| `BTN_GRP_LEFT` | Left Button Group | Orchestr8_jr | NO | 4 mini buttons |
| `BTN_MAESTRO` | MAESTRO Button | Orchestr8_jr | YES | Center anchor, gold/teal |
| `BTN_GRP_RIGHT` | Right Button Group | Orchestr8_jr | NO | 6 mini buttons |

### Layer 3: Status Layer

| Surface ID | Name | Owner | Frozen | Description |
|------------|------|-------|--------|-------------|
| `STATUS_TEXT` | Status Text | Orchestr8_jr | NO | System phase indicator |

## Mini Button Inventory

### Left Group (4)

| Button | Label | Status | Notes |
|--------|-------|--------|-------|
| `MINI_APPS` | Apps | PLACEHOLDER | Future: Application launcher |
| `MINI_CALENDAR` | Calendar* | PLACEHOLDER | Asterisk = future feature |
| `MINI_COMMS` | Comms* | PLACEHOLDER | Asterisk = future feature |
| `MINI_FILES` | Files | PLACEHOLDER | Future: File browser |

### Right Group (6)

| Button | Label | Status | Notes |
|--------|-------|--------|-------|
| `MINI_SEARCH` | Search | PLACEHOLDER | Future: Search function |
| `MINI_RECORD` | Record | PLACEHOLDER | Future: Recording function |
| `MINI_PLAY` | Play | PLACEHOLDER | Future: Playback function |
| `MINI_PHREAK` | Phreak> | PLACEHOLDER | Italic style, special action |
| `MINI_SEND` | Send | PLACEHOLDER | Future: Send function |
| `MINI_ATTACH` | Attach | PLACEHOLDER | Future: Attachment function |

## Surface Addition Protocol

To add a new surface:

1. Submit packet with `FRONTEND_SURFACE_REGISTRY` update
2. Specify surface ID, name, owner, freeze status
3. Document visual placement rationale
4. Obtain Orchestr8_jr approval
5. Update this registry

## Color Token Reference

| Token | Value | Usage |
|-------|-------|-------|
| `--bg-obsidian` | #050505 | Background base |
| `--gold-dark` | #C5A028 | Primary accent |
| `--gold-light` | #F4C430 | Highlight accent |
| `--teal` | #00E5E5 | Secondary accent |
| `--text-grey` | #CCC | Standard text |

## Font Token Reference

| Token | Value | Usage |
|-------|-------|-------|
| `--font-header` | Marcellus SC | Headers, major labels |
| `--font-ui` | Poiret One | UI elements, buttons |
| `--font-data` | VT323 | Data displays, status |

## Change Log

| Date | Change | Authority |
|------|--------|-----------|
| 2026-02-15 | Initial registry | P07-A1 |
