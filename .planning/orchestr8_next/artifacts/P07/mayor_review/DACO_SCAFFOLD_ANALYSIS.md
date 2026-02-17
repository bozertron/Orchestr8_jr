# DAC-O Scaffold Pipeline Analysis
## Tier A - High Priority Acquisition Target

**Source:** `/home/bozertron/Documents/DAC-O/`  
**Target Integration:** Orchestr8 (`or8_founder_console`)  
**Analysis Date:** 2026-02-16

---

## Executive Summary

DAC-O (Distributed Alignment and Context Orchestration) represents a high-value acquisition target for Orchestr8 integration. The tool provides a mature 7-command scaffold pipeline for rapid context acquisition in Vue/Tauri projects, with direct relevance to the C2P (Comment-to-Packet) intent scanner being built in `or8_founder_console`.

---

## 1. Scaffold Pipeline Structure (7-File Pipeline)

### Command Files (in `src/commands/`)

| # | File | Command Type | Purpose |
|---|------|--------------|---------|
| 1 | `overview.ts` | `scaffold overview` | Generates comprehensive project overview with numbered file index, key config files, entry points, dependencies, directory structure |
| 2 | `storeParser.ts` | `scaffold stores` | Analyzes Pinia stores - extracts state, getters, and actions |
| 3 | `routeParser.ts` | `scaffold routes` | Analyzes Vue Router routes |
| 4 | `commandParser.ts` | `scaffold commands` | Analyzes Tauri commands + backend declarations) (frontend invocations |
| 5 | `typeParser.ts` | `scaffold types` | Analyzes TypeScript type definitions with optional filter pattern |
| 6 | `uiParser.ts` | `scaffold ui` | Analyzes UI components (particularly Naive UI) |
| 7 | `fileRetriever.ts` | `scaffold files` | Retrieves content of specific files by index from overview |

### CLI Entry Point

- **File:** `src/index.ts`
- **Framework:** yargs CLI parser
- **Output:** Saves to `alignmentAndContextCache/scaffold-{type}-{filter}-{N}.txt`

### Usage Examples

```bash
node dist/index.js scaffold overview
node dist/index.js scaffold stores
node dist/index.js scaffold routes
node dist/index.js scaffold commands
node dist/index.js scaffold types --filter Auth
node dist/index.js scaffold ui
node dist/index.js scaffold files --indices 1,5,10
```

---

## 2. SWC AST Parsing Integration

### Current State

- DAC-O is built as a **TypeScript/Vue/Tauri application** (not pure Rust)
- The documentation references **SWC parsers** (`swc_ecma_parser 0.146`) for AST parsing
- SWC provides ~30x faster parsing compared to tree-sitter for JS/TS

### Dependencies to Extract

From `package.json`:
- `@swc/core` or similar SWC packages
- `@babel/parser` (fallback parser)
- Vue-related: `vue`, `vue-router`, `pinia`, `naive-ui`
- Build: `vite`, `typescript`, `yargs`

### Architecture Note

The SWC integration appears to be **referenced in documentation** but the current implementation uses **regex/pattern matching** for scaffold generation. The SWC integration would be an enhancement for deeper AST analysis.

---

## 3. C2P Intent Scanner Connection

### Current C2P Pipeline (or8_founder_console)

**Location:** `/home/bozertron/or8_founder_console/services/intent_scanner.py`

The C2P intent scanner currently:
- Uses **regex-based** comment extraction (`TODO`, `FIXME`, `HACK`, `C2P:` markers)
- Works for small repos but won't scale to full codebase
- Outputs structured JSON of comments with line/column/context

### Integration Opportunity

| Component | Current | DAC-O Enhancement |
|-----------|---------|-------------------|
| Parser | Python regex | Rust SWC (30x faster) |
| Scale | Small repos | Full codebase |
| Output | JSON | Structured packets |

### Strategic Value

From `SOT/CODEBASE_TODOS/ANTIGRAVITY_IDEAS.md`:
> Build a Rust CLI binary from DAC-O's SWC deps that reads a file path and outputs structured JSON of all `TODO`, `FIXME`, `HACK`, `C2P:` comments with precise line/column/context.

---

## 4. Files to Extract

### Priority 1 - Core Pipeline (7 Files)

```
/home/bozertron/Documents/DAC-O/src/commands/
├── overview.ts          # Project structure analysis
├── storeParser.ts       # Pinia store extraction
├── routeParser.ts       # Vue Router analysis
├── commandParser.ts     # Tauri command analysis
├── typeParser.ts        # TypeScript type extraction
├── uiParser.ts          # UI component analysis
└── fileRetriever.ts     # File content retrieval
```

### Priority 2 - CLI Infrastructure

```
/home/bozertron/Documents/DAC-O/src/
├── index.ts             # Main CLI entry (yargs)
├── main.ts              # App bootstrap
├── App.vue              # Vue root component
├── types/               # TypeScript definitions
├── composables/         # Vue composables
└── utils/               # Utility functions
```

### Priority 3 - Configuration

```
/home/bozertron/Documents/DAC-O/
├── package.json         # Node dependencies
├── tsconfig.json        # TypeScript config
├── vite.config.mjs      # Vite build config
└── RTFM.md             # Command documentation
```

---

## 5. Integration Path to or8_founder_console

### Phase 1: Extract and Port (Week 1)

1. Copy the 7 command parsers to Orchestr8
2. Adapt from TypeScript to Python (or create Python bindings)
3. Create Marimo UI wrappers for each scaffold type

### Phase 2: SWC Integration (Week 2)

1. Create Rust CLI binary using SWC (`swc_ecma_parser`)
2. Input: File path → Output: JSON of comments with metadata
3. Wire into `intent_scanner.py` as faster alternative

### Phase 3: Unified Pipeline (Week 3)

1. Merge scaffold pipeline + C2P scanner
2. Add to Orchestr8 plugin system
3. Expose via `or8_founder_console` UI

### Integration Architecture

```
Orchestr8 (Marimo)
       │
       ▼
or8_founder_console
       │
       ├──▶ intent_scanner.py (Python regex - current)
       │
       └──▶ [NEW] swc_comment_extractor (Rust CLI - from DAC-O)
                    │
                    └──▶ JSON: {type, line, col, context}
```

---

## 6. Risk Assessment

| Risk | Level | Mitigation |
|------|-------|------------|
| TypeScript → Python port | Medium | Create Rust CLI wrapper instead of Python port |
| SWC version compatibility | Low | Use latest stable SWC; not tied to specific version |
| Performance regression | Low | SWC is 30x faster than current regex approach |
| Dependency bloat | Medium | Extract only needed SWC crates |

---

## 7. Recommendations

### Immediate Actions

1. **Extract** the 7 command parsers from DAC-O
2. **Create** Rust CLI binary for SWC-based comment extraction
3. **Wire** into existing `intent_scanner.py` as fast path

### Long-term Vision

- Build DAC-O-style scaffold pipeline for **all** codebases (not just Vue/Tauri)
- Integrate with Code City visualization in Orchestr8
- Enable real-time context acquisition for Settlement System agents

---

## Appendix: Sample Scaffold Output

From `scaffold-overview-1.txt`:

```
=== Numbered File Index ===
1: src-tauri/Cargo.lock
2: src-tauri/Cargo.toml
...
120: src/vite-env.d.ts

=== Key Config Files ===
- package.json: (Name: maestropremvp, Version: 0.0.0)
- vite.config.ts: (Found - Details TBD)
- tauri.conf.json: (ID: N/A, Version: N/A)

=== Entry Points ===
- src/main.ts: (Found)
- src-tauri/src/main.rs: (Found)
```

---

**Classification:** Tier A - High Priority Acquisition  
**Integration Owner:** P07 (or8_founder_console)  
**Next Review:** After Phase 1 completion

