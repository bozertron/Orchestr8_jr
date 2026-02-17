# TERMINAL-1-MAESTRO.md Integration Guide

- Source: `.planning/codebase/prompts/TERMINAL-1-MAESTRO.md`
- Total lines: `28`
- SHA256: `bfa1b62479a5bd2f5ffae46340a535586ed42ef1100b2380129f69f8ac7abd69`
- Memory chunks: `1`
- Observation IDs: `1021..1021`

## Why This Is Painful

- General integration risk: enforce tests around schema, state, and behavior contracts.

## Anchor Lines

- `.planning/codebase/prompts/TERMINAL-1-MAESTRO.md:1` # Terminal 1: 06_maestro.py Deep Analysis
- `.planning/codebase/prompts/TERMINAL-1-MAESTRO.md:7` **File:** `IP/plugins/06_maestro.py` (1297 lines)
- `.planning/codebase/prompts/TERMINAL-1-MAESTRO.md:13` 1. **Map every button** — what label, what handler, what it actually does vs what the UI spec says it should do
- `.planning/codebase/prompts/TERMINAL-1-MAESTRO.md:14` 2. **Map every panel** — Collabor8, JFDI, Summon, Tickets, Calendar, Comms, FileExplorer, Deploy. For each: is it a real component or placeholder HTML?

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
