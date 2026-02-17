# Phase 08: Real-Time Design UI System

## Phase Overview

Research and plan for a real-time design UI system that combines:
- EPO settings system (from Agent 02 analysis)
- Collabkit Void Design System
- Orchestr8 codebase visualization
- Tauri desktop packaging

## Core Vision

A particle-based invisible UI system where:
1. Components are invisible by default (same color as background)
2. Text-based interfaces are the default (fields representing variable options)
3. Start simple: text + boxes + buttons
4. Make pretty later

## Decisions (Locked)

1. **Marimo-first architecture** - Per README.AGENTS, runtime canon is marimo-first
2. **Tauri packaging path preserved** - App-first, no premature packaging lock-in
3. **Void Design System** - Use Collabkit's Void Design System as visual foundation

## Claude's Discretion

1. Research best approaches for particle-based UI
2. Determine optimal starting complexity (text+boxes vs. immediate visual richness)
3. Decide on integration order (settings first vs. visual foundation first)

## Research Domains Required

1. **Collabkit Void Design System** - Complete analysis of `VOID_DESIGN_SYSTEM_SOT.md`
2. **EPO Settings Integration** - How settings UI fits into design system
3. **Real-time Design Tools** - Existing patterns for live UI editing
4. **Particle-based Rendering** - Canvas/WebGL approaches for Orchestr8 integration
5. **Text-first Interface Patterns** - How to make text interfaces beautiful

## Constraints

- Must preserve Code City render contract (WIDGET/IFRAME)
- Visual contract authority remains with Orchestr8_jr
- No mandatory IDE plugin dependency for core controls
