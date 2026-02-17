# Autonomy Boundary: P07-FC-06 (or8_founder_console)

## Objective

Ship C2P Wave-4 MVP: observation sync + review queue for launch-ready packets.

## Scope

Founder tooling packet: comment ingestion + proposal queue

## Allowed Work

- Implement multi-repo founder comment scanner for @founder/@todo markers
- Store unprocessed intent in Founder Console review store
- Expose review API endpoints for approve-edit-launch flow
- Publish evidence report with command transcript

## Must Not Do

- Auto-dispatch packets without founder review gate
- Destructive memory controls

## Required Evidence

- /home/bozertron/or8_founder_console/services/intent_scanner.py
- /home/bozertron/or8_founder_console/routers/intent_queue.py
- /home/bozertron/or8_founder_console/tests/test_intent_scanner.py
- /home/bozertron/or8_founder_console/tests/test_intent_queue.py
- /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-06_REPORT.md

## Required Validation

```bash
python -m pytest tests/ -v
```
## Unlock Authority

- Unlocked by: Codex
- Effective: 2026-02-16
