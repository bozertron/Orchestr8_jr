# CONTEXT.md Integration Guide

- Source: `.planning/phases/CONTEXT.md`
- Total lines: `391`
- SHA256: `0fe920306b2434b8ca5552830778a827b362b941cd4d665bdea2279e2c8bf1ea`
- Memory chunks: `5`
- Observation IDs: `53..57`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- JS/Python bridge risk: event transport and payload validation can silently fail.
- Visual canon risk: color/motion contract regressions are easy to introduce.
- Behavioral sequencing risk: mode transitions need explicit state machine handling.

## Anchor Lines

- `.planning/phases/CONTEXT.md:4` ## Status: AUTHORITATIVE
- `.planning/phases/CONTEXT.md:12` | **LOCKED** | Non-negotiable. Do exactly this. Violating these is a critical error. |
- `.planning/phases/CONTEXT.md:22` 1. **Wire HealthChecker to Code City** — Real-time health visualization is foundational
- `.planning/phases/CONTEXT.md:35` ### LOCKED Decisions
- `.planning/phases/CONTEXT.md:50` - **NO:** Breathing animations (FORBIDDEN — things EMERGE, not breathe)
- `.planning/phases/CONTEXT.md:55` - File names must be clearly labeled on panels
- `.planning/phases/CONTEXT.md:71` ### LOCKED Decisions
- `.planning/phases/CONTEXT.md:74` - **VS CODE INTEGRATION:** postMessage bridge to Marimo iframe
- `.planning/phases/CONTEXT.md:75` - **HEALTH VISUALIZATION FLOW:** Building TEAL → Room with error GLOWS → Click to enter Sitting Room
- `.planning/phases/CONTEXT.md:76` - **DATA FLOW:** `File Change → HealthWatcher → HealthChecker → STATE_MANAGERS → Code City`
- `.planning/phases/CONTEXT.md:100` ### LOCKED Decisions
- `.planning/phases/CONTEXT.md:102` - **LOCATION:** `.orchestr8/campaigns/`
- `.planning/phases/CONTEXT.md:124` ### LOCKED Decisions
- `.planning/phases/CONTEXT.md:126` - **SIGNAL SOURCES:** HealthChecker, ConnectionVerifier, CombatTracker, TicketManager, LouisWarden
- `.planning/phases/CONTEXT.md:132` ### Carl's Output Structure (LOCKED)
- `.planning/phases/CONTEXT.md:166` ### LOCKED Decisions
- `.planning/phases/CONTEXT.md:192` ### LOCKED Decisions
- `.planning/phases/CONTEXT.md:205` - **Gold dark:** `#B8860B` (borders, strokes)
- `.planning/phases/CONTEXT.md:206` - **Gold saffron:** `#F4C430` (highlights)
- `.planning/phases/CONTEXT.md:223` ### LOCKED Decisions
- `.planning/phases/CONTEXT.md:227` - **SITTING ROOM COLLABORATION:** When a room (function) has an issue, click to enter the Sitting Room — particles morph into a presentation area where human and LLM collaborate on fixes.
- `.planning/phases/CONTEXT.md:236` - Motion should feel like emergence, not animation
- `.planning/phases/CONTEXT.md:253` ### LOCKED Decisions
- `.planning/phases/CONTEXT.md:254` - **INTEGRATION METHOD:** postMessage bridge to Marimo iframe
- `.planning/phases/CONTEXT.md:255` - **DATA FLOW:** `VS Code Extension → File Watcher → Telemetry Aggregator → postMessage → Marimo iframe`

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
