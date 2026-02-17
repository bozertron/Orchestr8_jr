# Architecture - Founder Console

## Suggested Stack
- Backend: FastAPI (gateway adapter + filesystem watch)
- UI: marimo + anywidget (initial), optional Tauri shell later
- Storage: SQLite (annotations, local view state)

## Data Sources
- Shared memory API (`/v1/memory/*`)
- Canonical check-in docs (`STATUS/BLOCKERS/GUIDANCE`)
- Canonical artifacts directory

## Core Services
1. PacketIndexer
2. ArtifactLoader
3. AnnotationService
4. CommsService
5. UnreadService
6. EventTimeline

## Contracts
See `contracts/FOUNDER_CONSOLE_CONTRACTS.md`.
