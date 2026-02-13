# VISION-ALIGNMENT.md Integration Guide

- Source: `.planning/VISION-ALIGNMENT.md`
- Total lines: `270`
- SHA256: `c469aebdc271f8c900cb00048c0c462830bfb2e8a2f9b4bce460d3216003ed32`
- Memory chunks: `4`
- Observation IDs: `49..52`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- JS/Python bridge risk: event transport and payload validation can silently fail.
- Visual canon risk: color/motion contract regressions are easy to introduce.
- Behavioral sequencing risk: mode transitions need explicit state machine handling.

## Anchor Lines

- `.planning/VISION-ALIGNMENT.md:5` **Status:** LOCKED — All decisions finalized
- `.planning/VISION-ALIGNMENT.md:11` This document captures the vision alignment session that established the foundational decisions for Orchestr8's development. These decisions are **LOCKED** and should not be changed without explicit Founder approval.
- `.planning/VISION-ALIGNMENT.md:20` │  orchestr8 (Marimo, Python)                                     │
- `.planning/VISION-ALIGNMENT.md:26` │  The orchestra practices on orchestr8 itself first.             │
- `.planning/VISION-ALIGNMENT.md:62` | **Sitting Room** | Particles morph into collaboration space for human+LLM discussion |
- `.planning/VISION-ALIGNMENT.md:71` - Breathing animations (FORBIDDEN — things EMERGE, not breathe)
- `.planning/VISION-ALIGNMENT.md:81` | **VS Code integration** | postMessage bridge to Marimo iframe |
- `.planning/VISION-ALIGNMENT.md:83` | **Health visualization** | Building TEAL → Room with error GLOWS → Click to enter Sitting Room |
- `.planning/VISION-ALIGNMENT.md:88` File Change → HealthWatcher → HealthChecker → STATE_MANAGERS → Code City
- `.planning/VISION-ALIGNMENT.md:110` | **Location** | `.orchestr8/campaigns/` |
- `.planning/VISION-ALIGNMENT.md:135` | **Signal sources** | HealthChecker, ConnectionVerifier, CombatTracker, TicketManager, LouisWarden |
- `.planning/VISION-ALIGNMENT.md:186` /* Gold Variations */
- `.planning/VISION-ALIGNMENT.md:213` ### 4. Sitting Room Collaboration
- `.planning/VISION-ALIGNMENT.md:215` When a room (function) has an issue, click to enter the Sitting Room — particles morph into a presentation area where human and LLM collaborate on fixes.
- `.planning/VISION-ALIGNMENT.md:225` The vscode-marimo extension provides telemetry via postMessage bridge:
- `.planning/VISION-ALIGNMENT.md:228` VS Code Extension → File Watcher → Telemetry Aggregator → postMessage → Marimo iframe
- `.planning/VISION-ALIGNMENT.md:248` ├── 06_maestro.py      # Main UI (Summon panel needs Carl)
- `.planning/VISION-ALIGNMENT.md:260` 2. Wire HealthChecker to Code City
- `.planning/VISION-ALIGNMENT.md:268` **Document Status:** LOCKED

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
