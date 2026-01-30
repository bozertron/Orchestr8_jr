# Integration Queue

**Last Updated:** 2026-01-30

---

## CRITICAL REQUIREMENT

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   EVERY SINGLE INTEGRATION requires Ben's approval before        ║
║   proceeding to the next item.                                   ║
║                                                                  ║
║   There is information not yet accounted for in this queue.     ║
║   Each integration must be pressure tested with Ben's feedback. ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Queue Order

| # | Item | Description | Lines | Status |
|---|------|-------------|-------|--------|
| 1 | `888/panel_foundation/` + `IP--888/` | Merge panel_foundation versions | ~950 | Pending |
| 2 | `888/director/` | Director agent - work allocation | ~460 | Pending |
| 3 | `888/professor/` | Professor agent - breakthrough engine | ~660 | Pending |
| 4 | `888/senses/` | Multimodal input (speech, gesture, ML) | ~5,855 | Pending |
| 5 | `888/calendar/` | Calendar adapter | ~490 | Pending |
| 6 | `888/communic8/` | Multi-LLM communications | ~225 | Pending |
| 7 | `888/actu8/` | Document generation | ~310 | Pending |
| 8 | `888/cre8/` | Creative suite | ~365 | Pending |
| 9 | `888/integr8/` | Code editor | ~370 | Pending |
| 10 | `888/innov8/` | Experimental sandbox | ~390 | Pending |
| 11 | `888/comms/` | Communications adapter | ~565 | Pending |
| 12 | `star-vector/` | Vector conversion tool | Large | Pending |
| 13 | `orchestr8-zed/` | Zed IDE extension | Rust | Pending |
| 14 | `calendar/` | Rust calendar system | Rust | Pending |
| 15 | `p2p/` | Rust P2P system | Rust | Pending |
| 16 | `frontend/` | Frontend tools | TBD | Pending |
| 17 | `orchestr8_mcp.py` | MCP server for IDE integration | ~490 | Pending |
| 18 | `orchestr8_standalone.py` | Legacy monolithic version (reference) | ~710 | Pending |
| 19 | `IP--orchestr8_app.py` | Redundant loader (merge or discard) | ~250 | Pending |

---

## Reference Materials (Do Not Integrate - For Context Only)

| Item | Purpose |
|------|---------|
| `docs/` | Archived spec documents |
| `PRDs/` | Product requirement documents |
| `Agent Deployment Strategy/` | Agent hierarchy documentation |
| `Big Pickle/` | Historical specs |
| `Context King/` | Historical specs |
| `UI Reference/` | MaestroView.vue reference |
| `FileExplorer/` | Vue component reference (Python equivalent exists) |
| `style/` | Style references |
| `Git Knowledge/` | Git documentation |

---

## Integration Protocol

For EACH integration:

1. **Proposal:** Claude presents what will be integrated and why
2. **Review:** Ben reviews and provides feedback
3. **Pressure Test:** Ben identifies gaps or conflicts
4. **Approval:** Ben explicitly approves proceeding
5. **Execute:** Claude performs the integration
6. **Validate:**
   - `marimo run orchestr8.py` works
   - `06_maestro.py` renders correctly
   - No regressions
7. **Update SOT:** Update `SOT.md` with new components
8. **Remove:** Delete integrated items from this directory
9. **Commit:** Commit with clear message

---

## Notes

- The 888 system has ~16,000 lines of code total
- `IP--888/` has a NEWER version of panel_foundation than `888/panel_foundation/`
- When merging panel_foundation, use IP--888/ as the base and port any missing features from 888/
- The senses module (~5,855 lines) is the largest single integration
- Rust systems (calendar/, p2p/) require different toolchain

---

## Completed Integrations

| Date | Item | Notes |
|------|------|-------|
| - | - | None yet |
