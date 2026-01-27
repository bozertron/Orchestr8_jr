# Internal Tasks Before External IP Integration

**Purpose:** Complete everything that doesn't require stereOS, Orchestr8_sr, or actu8  
**Created:** 2026-01-26  
**Status:** READY FOR EXECUTION

---

## Task Classification

### ✅ INTERNAL (Execute Now)

| Task ID | Title | Dependencies | Status |
|---------|-------|--------------|--------|
| 21 | E2E Universal Bridge Test | 18 (done) | PENDING |
| 22 | Multi-Manifest Dynamic UI Test | 21 | PENDING |
| 23 | Apply MaestroView Colors | None | PENDING |
| 24 | Mermaid Status Graph | 23 | PENDING |
| 26 | Carl Health Check Integration | 24 | PENDING |
| 27 | Runtime Directories Creation | None | PENDING |
| 28 | Fixed Overton Anchor | 23 | PENDING |
| 29 | Tickets Panel (NEW system) | 25, 27 | PENDING* |
| 30 | BRIEFING.md Generation | 26, 27 | PENDING |
| 31 | CAMPAIGN_LOG.md System | 27, 30 | PENDING |
| 32 | Git Hooks (Louis + Carl) | 26 | PENDING |

*Task 29 originally depended on stereOS import, but Taskmaster built a NEW system instead. Internal.

### 🔴 EXTERNAL (Defer Until IP Integration)

| Task ID | Title | External Dependency |
|---------|-------|---------------------|
| 25 | Fiefdom List with Deploy | actu8 terminal spawn |
| N/A | ChangeChecker Integration | stereOS/Orchestr8_sr files |
| N/A | Connection Verifier | stereOS ParserPack |

### 🆕 NEW INTERNAL TASKS (LLM Integration)

These are NOT in tasks.json yet - need to be added:

| New ID | Title | Priority |
|--------|-------|----------|
| 33 | Configure marimo.toml for LLM Providers | P0 |
| 34 | Setup Anthropic (Claude) Integration | P0 |
| 35 | Setup Ollama for Local Models/Embeddings | P1 |
| 36 | Create Custom AI Rules for Orchestr8 | P1 |
| 37 | Explore Agent Mode for Cell Editing | P2 |
| 38 | Document LLM Integration Patterns | P2 |

---

## Phase A: Foundation (No External IP)

### A1: Runtime Infrastructure

**Goal:** Create the `.orchestr8/` structure that everything else depends on

```
Task 27: Runtime Directories Creation
├── .orchestr8/tickets/
├── .orchestr8/tickets/archive/
├── .orchestr8/state/
│   └── fiefdom-status.json (initial)
└── CLAUDE.md templates for test fiefdoms
```

**Effort:** 1-2 hours  
**Blocker for:** Tasks 29, 30, 31

---

### A2: Styling Foundation

**Goal:** Apply MaestroView.vue colors to all plugins

```
Task 23: MaestroView Color Palette
├── Create IP/styles/orchestr8.css
├── Configure pyproject.toml with custom_css
├── Apply :root CSS variables
└── Verify dark void background (#0A0A0B)
```

**Reference:** Big Pickle/MARIMO_STYLING_TASKS.md (already created)  
**Effort:** 4-6 hours  
**Blocker for:** Tasks 24, 28

---

### A3: Core Tools Verification

**Goal:** Confirm Carl and Louis work before integrating them

```
Task 21: E2E Universal Bridge Test
├── Start Marimo
├── Navigate to Universal Bridge tab
├── Verify Scaffold Parsers accordion
├── Execute discovery command
└── Verify JSON table rendering

Task 22: Multi-Manifest Test
├── Create 99_test.json
├── Restart Marimo
├── Verify both accordions appear
├── Remove 99_test.json
└── Verify cleanup
```

**Effort:** 1-2 hours  
**Blocker for:** None (validation only)

---

## Phase B: Visualization (No External IP)

### B1: Mermaid Graph

**Goal:** Show fiefdom status as interactive graph

```
Task 24: Mermaid Status Graph
├── Import Carl from IP/carl_core.py
├── Generate graph from fiefdom-status.json
├── Apply gold/blue/purple colors via classDefs
├── Add click handlers (if possible in Marimo)
└── Cache to .orchestr8/mermaid-cache.md
```

**Note:** Carl already exists at `IP/carl_core.py` - this is INTERNAL  
**Effort:** 3-4 hours  
**Blocker for:** Task 26

---

### B2: Health Check Integration

**Goal:** Wire Carl's health checks to update graph

```
Task 26: Carl Health Check Integration
├── Add [🔄 REFRESH] button to maestro
├── Call carl.check_health_all_fiefdoms()
├── Update fiefdom-status.json
├── Regenerate Mermaid graph
└── Auto-create tickets for broken fiefdoms
```

**Effort:** 2-3 hours  
**Blocker for:** Tasks 30, 32

---

### B3: Fixed Input Bar

**Goal:** The Overton Anchor that NEVER MOVES

```
Task 28: Fixed Overton Anchor
├── position: fixed; bottom: 0; height: 20vh
├── [Files][Matrix][Graph]═══[maestro]═══[Search][Deploy][⏎]
├── Command input with mo.ui.text_area
├── Deploy button (disabled until actu8 integrated)
└── Style with --bg-elevated
```

**Effort:** 2-3 hours  
**Blocker for:** None

---

## Phase C: Wisdom System (No External IP)

### C1: Tickets (NEW System)

**Goal:** Internal ticket system without stereOS import

```
Task 29: Tickets Panel
├── Read .orchestr8/tickets/*.md
├── Display as cards with status
├── Search/filter by status/keyword
├── Slide-right animation
└── Archive to tickets/archive/
```

**Note:** Taskmaster built a NEW system - no stereOS dependency  
**Effort:** 3-4 hours  
**Blocker for:** Task 30

---

### C2: Briefing Generation

**Goal:** Generate BRIEFING.md for general deployment

```
Task 30: BRIEFING.md Generation
├── Read CLAUDE.md from fiefdom
├── Get Carl's file inventory
├── Get open ticket content
├── Get CAMPAIGN_LOG.md tail(10)
└── Write combined BRIEFING.md
```

**Note:** Terminal spawn (actu8) is EXTERNAL - this just generates the file  
**Effort:** 2-3 hours  
**Blocker for:** Task 31

---

### C3: Campaign Log

**Goal:** Append-only wisdom accumulation

```
Task 31: CAMPAIGN_LOG.md System
├── def append_campaign_log(fiefdom, ticket_id, status, actions, lessons)
├── Template format from PRD
├── Atomic writes with Louis lock
└── No duplication on append
```

**Effort:** 2 hours  
**Blocker for:** None

---

### C4: Git Hooks

**Goal:** Automate Louis + Carl on commit

```
Task 32: Git Hooks
├── .git/hooks/pre-commit (Louis validation)
├── .git/hooks/post-commit (Carl health check)
├── chmod +x on hooks
└── Test with dummy commits
```

**Effort:** 1-2 hours  
**Blocker for:** None

---

## Phase D: LLM Integration (NEW - No External IP)

### D1: Provider Configuration

**Goal:** Setup marimo.toml for AI capabilities

```
Task 33: Configure marimo.toml
├── Create/update marimo.toml
├── Set chat_model = "anthropic/claude-sonnet-4-20250514"
├── Set edit_model = "anthropic/claude-sonnet-4-20250514"
├── Optional: autocomplete_model = "ollama/codellama"
└── Verify in Marimo settings panel
```

**Config File Location:** `marimo config show | head`

```toml
[ai.models]
chat_model = "anthropic/claude-sonnet-4-20250514"
edit_model = "anthropic/claude-sonnet-4-20250514"
# autocomplete_model = "ollama/codellama"

[ai.anthropic]
api_key = "sk-ant-..."  # User provides
```

**Effort:** 30 minutes  
**Blocker for:** Tasks 34, 35

---

### D2: Claude Integration

**Goal:** Enable Claude as the AI assistant in Marimo

```
Task 34: Anthropic/Claude Setup
├── pip install anthropic (if not present)
├── Get API key from Anthropic Console
├── Add to marimo.toml [ai.anthropic]
├── Test chat panel
└── Test Ctrl/Cmd-Shift-E refactor
```

**This integrates YOU into Orchestr8**  
**Effort:** 30 minutes  
**Blocker for:** None

---

### D3: Local Models (Optional)

**Goal:** Setup Ollama for local embeddings/completion

```
Task 35: Ollama Setup
├── Install Ollama (if not present)
├── ollama pull codellama
├── ollama serve (port 11434)
├── Configure marimo.toml [ai.ollama]
│   └── base_url = "http://127.0.0.1:11434/v1"
└── Test autocomplete with local model
```

**Benefits:**
- No API costs for embeddings
- Faster autocomplete
- Privacy for sensitive code

**Effort:** 1 hour  
**Blocker for:** None

---

### D4: Custom AI Rules

**REMOVED** - Working on this directly with Emperor. See `Big Pickle/LLM_INFLUENCE_REFERENCE.md`

---

### D5: Agent Mode Exploration

**Goal:** Test Marimo's agent mode for automated editing

```
Task 37: Agent Mode Testing
├── Enable Agent mode in chat panel
├── Test: "Add a button to refresh Carl health check"
├── Verify cell editing works
├── Document capabilities and limitations
└── Evaluate for general deployment workflow
```

**Effort:** 1 hour  
**Blocker for:** None

---

### D6: Documentation

**Goal:** Document LLM integration for future reference

```
Task 38: LLM Integration Docs
├── Document provider configuration
├── Document custom rules
├── Document agent mode usage
├── Add to style guide or CLAUDE.md
└── Note: Big Pickle integration path
```

**Effort:** 1 hour  
**Blocker for:** None

---

## Execution Order

```
Phase A (Foundation)
─────────────────────
Task 27 ──────────────┬──► Task 29 ──► Task 30 ──► Task 31
                      │
Task 23 ──────────────┼──► Task 24 ──► Task 26 ──► Task 32
         │            │
         └──► Task 28 │
                      │
Task 21 ──► Task 22 ──┘

Phase D (LLM - Parallel)
────────────────────────
Task 33 ──┬──► Task 34
          ├──► Task 35
          ├──► Task 36
          └──► Task 37 ──► Task 38
```

---

## Estimated Timeline

| Phase | Tasks | Effort | Cumulative |
|-------|-------|--------|------------|
| A1: Runtime | 27 | 1-2 hrs | 2 hrs |
| A2: Styling | 23 | 4-6 hrs | 8 hrs |
| A3: Verification | 21, 22 | 1-2 hrs | 10 hrs |
| B1-B3: Visualization | 24, 26, 28 | 7-10 hrs | 20 hrs |
| C1-C4: Wisdom | 29-32 | 8-11 hrs | 31 hrs |
| D1-D6: LLM | 33-38 | 4-5 hrs | 36 hrs |

**Total Internal Work:** ~36 hours before external IP needed

---

## What We CANNOT Do Until External IP

1. **actu8 Terminal Spawn** - Need the terminal component from stereOS
2. **ChangeChecker** - Need connection verifier from stereOS/Orchestr8_sr  
3. **Deploy Button Functionality** - Blocked by actu8
4. **Full General Workflow** - Need terminal to actually deploy generals

---

## Success Criteria (Before External IP)

- [ ] `.orchestr8/` structure exists with sample data
- [ ] All plugins use MaestroView colors
- [ ] Mermaid graph renders with correct status colors
- [ ] Carl health check updates graph
- [ ] Tickets panel shows/searches tickets
- [ ] BRIEFING.md generates correctly
- [ ] CAMPAIGN_LOG.md appends correctly
- [ ] Git hooks fire on commit
- [ ] Claude accessible in Marimo chat panel
- [ ] Custom AI rules enforced
- [ ] Ollama running for local completion (optional)

---

**END INTERNAL TASKS**
