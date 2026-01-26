# PRD: Orchestr8 v4.0 - The Codebase Command Center

**Version:** 4.0 Consolidated  
**Created:** 2026-01-26  
**Status:** READY FOR TASKMASTER PARSING  
**Authors:** Ben (Emperor) + Claude (Strategic Council)

---

## Executive Summary

Orchestr8 is a developer tool that enables a human operator ("The Emperor") to coordinate multiple Claude Code instances ("Generals") across a complex codebase without context window death.

**The Core Problem:**
```
Context loaded → Almost ready to execute → Context poisoned/compacted → Unusable output → Repeat
```

**The Solution:**
- Generals work in isolated fiefdoms (directories) with focused scope
- The Emperor sees a Mermaid status graph (gold/blue/purple nodes)
- Coordination happens through filesystem artifacts, not conversation
- Wisdom accumulates per-fiefdom via CAMPAIGN_LOG.md
- Trust is verified through health checks, not promises

**Key Principle:**
> "We'd rather have more agents out and actually complete the job than have fewer and have to do it again."

---

## I. Color System (Authoritative Reference: MaestroView.vue)

### Primary Colors - EXACT VALUES, NO EXCEPTIONS

| Variable | Hex | Usage |
|----------|-----|-------|
| `--blue-dominant` | `#1fbdea` | UI default, broken status, interactive elements |
| `--gold-metallic` | `#D4AF37` | UI highlight, working status, active states |
| `--gold-dark` | `#B8860B` | Maestro default, timestamps, secondary gold |
| `--gold-saffron` | `#F4C430` | Maestro highlight, hover states |
| `--purple-combat` | `#9D4EDD` | Combat status (general deployed) |
| `--bg-primary` | `#0A0A0B` | The Void background |
| `--bg-elevated` | `#121214` | Surface, elevated panels, inputs |

### Three-State System

| State | Color | Hex | Meaning |
|-------|-------|-----|---------|
| **Working** | Gold | `#D4AF37` | All imports resolve, typecheck passes |
| **Broken** | Blue | `#1fbdea` | Has errors, needs attention |
| **Combat** | Purple | `#9D4EDD` | General currently deployed and active |

### CSS Reference Block
```css
:root {
    --gold-metallic: #D4AF37;
    --gold-dark: #B8860B;
    --gold-saffron: #F4C430;
    --blue-dominant: #1fbdea;
    --purple-combat: #9D4EDD;
    --bg-primary: #0A0A0B;
    --bg-elevated: #121214;
}
```

---

## II. System Architecture

### The Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              👑 EMPEROR                                      │
│                         (Ben + Claude Strategic)                             │
│                                                                              │
│  Responsibilities:                                                           │
│  - Strategic decisions and priority setting                                  │
│  - Decree issuance                                                          │
│  - Final approval on architectural changes                                   │
│  - Reviews escalations from generals                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           🏰 ORCHESTR8                                       │
│                        (The Void Dashboard)                                  │
│                                                                              │
│  Responsibilities:                                                           │
│  - Display Mermaid status graph (gold/blue/purple)                          │
│  - Show interactive fiefdom list with stacking notes                        │
│  - Spawn terminals (actu8) for general deployment                           │
│  - Generate BRIEFING.md for context injection                               │
│  - Aggregate status from all fiefdoms                                       │
│  - Display error messages from terminals/consoles/builds                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │ ⚔️ GENERAL  │ │ ⚔️ GENERAL  │ │ ⚔️ GENERAL  │
            │  src/llm/   │ │ src/modules/│ │ src/platform│
            └─────────────┘ └─────────────┘ └─────────────┘
                    │               │               │
         ┌──────────┴──────────┐   │    ┌──────────┴──────────┐
         ▼                     ▼   ▼    ▼                     ▼
    ┌─────────┐           ┌─────────┐  ┌─────────┐       ┌─────────┐
    │ 🔍 Scout│           │ 🔧 Fixer│  │ ✓ Valid │       │ 📝 Git  │
    │(analyze)│           │ (edit)  │  │ (test)  │       │(commit) │
    └─────────┘           └─────────┘  └─────────┘       └─────────┘
```

### Component Responsibilities

| Component | Runtime | Responsibility |
|-----------|---------|----------------|
| Orchestr8 | Marimo (Python) | Dashboard, visualization, deployment |
| Carl | Python | Context gathering, health checks, Mermaid generation |
| Connie | Python | Database/schema conversion to LLM-friendly format |
| Louis | Python | File locking, permission enforcement |
| General | Claude Code (terminal) | Focused execution within fiefdom |
| Scout | Subagent (Task tool) | Read-only analysis, state reporting |
| Fixer | Subagent (Task tool) | Surgical code changes |
| Validator | Subagent (Task tool) | Test execution, health verification |
| Git Agent | Subagent (Task tool) | Commits, pushes, branch management |

### Critical Design Decision: Visibility

**The Emperor MUST see the subagent choreography.**

This was tested and failed when hidden. The Emperor needs to know:
- Which scouts are analyzing what
- Which fixers are modifying which files
- Which validators are running which tests
- Which commits are being made

---

## III. The Void: Primary Interface

### Layout Specification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ TOP ROW                                                                      │
│ [Home] ═══ ORCHESTR8 ═══════════════════════ [Agents] [Tickets] [Settings]  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                              THE VOID                                        │
│                                                                              │
│  ┌────────────────────────────────────────────┐  ┌────────────────────────┐ │
│  │         MERMAID STATUS GRAPH               │  │    FIEFDOM LIST       │ │
│  │                                            │  │                        │ │
│  │     ┌─────┐         ┌─────────┐           │  │  🟡 src/llm           │ │
│  │     │ llm │────────►│ modules │           │  │     Health: WORKING   │ │
│  │     └─────┘         └─────────┘           │  │                        │ │
│  │        │                │                  │  │  🔵 src/generator     │ │
│  │        ▼                ▼                  │  │     Health: BROKEN    │ │
│  │  ┌──────────┐    ┌───────────┐            │  │     [DEPLOY ▼]        │ │
│  │  │ platform │    │ generator │            │  │                        │ │
│  │  └──────────┘    └───────────┘            │  │  🟣 src/maestro       │ │
│  │                                            │  │     Health: COMBAT    │ │
│  │  🟡 = Working (Gold)                      │  │     General: Active   │ │
│  │  🔵 = Broken (Blue)                       │  │                        │ │
│  │  🟣 = Combat (Purple)                     │  │                        │ │
│  └────────────────────────────────────────────┘  └────────────────────────┘ │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ BOTTOM FIFTH - The Overton Anchor (NEVER MOVES)                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ [Emperor Command: ________________________________________________]     │ │
│ │ [Files] [Matrix] [Graph] ══════ [maestro] ══════ [Search] [Deploy] [⏎]  │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Layout Rules

1. **The Void** = `#0A0A0B` background, pure collaboration space
2. **Bottom Fifth** = "Overton anchor" - IT NEVER MOVES
3. **Top Row** = Fixed position, navigation only
4. **Panels** = Emerge via transitions (slide-down, slide-right, fade)

### Panel Emergence System

| Panel | Trigger | Direction | Content |
|-------|---------|-----------|---------|
| Tickets Panel | Click "Tickets" | Slides from RIGHT | All pending tickets, searchable |
| Agents Panel | Click "Agents" | Slides from TOP | Active generals, subagent status |
| Fiefdom Card | Click node or list item | EMERGES from void center | Detailed fiefdom status |
| Settings | Click "Settings" | Slides from RIGHT | Configuration options |

### Design Prohibitions (from MaestroView.vue)

> **NO breathing animations. NO emojis in UI. NO clock.**

- UI elements do not "load"; they **EMERGE from the void** when summoned
- The Input Bar is docked at the bottom 5th - **IT NEVER MOVES**

---

## IV. actu8: Terminal Integration

### Overview

**actu8** is the terminal component that enables general deployment. It must be imported from stereOS/Orchestr8_sr.

### RESEARCH QUESTIONS FOR TASKMASTER:

> **Q1:** Where exactly is the actu8 terminal component located in stereOS? What is the file path?

> **Q2:** What are actu8's dependencies? What needs to be installed/imported for it to work?

> **Q3:** Does actu8 have any Tauri-specific dependencies that need adaptation for Marimo context?

> **Q4:** What is the interface/API for spawning a terminal at a specific directory path?

### Expected Functionality

```python
# Desired interface
def spawn_actu8_terminal(fiefdom_path: str, briefing_ready: bool = True) -> None:
    """
    Spawn actu8 terminal at fiefdom path.
    
    Args:
        fiefdom_path: Absolute path to fiefdom
        briefing_ready: Whether BRIEFING.md has been generated
    """
    # Update fiefdom status to COMBAT (purple)
    update_fiefdom_status(fiefdom_path, "combat")
    
    # Spawn terminal at path
    # [Implementation depends on actu8 API - needs research]
    pass
```

---

## V. Ticket System Integration

### Overview

The ticket system drives general deployment by capturing:
- What's broken
- Where it's broken
- Context for fixing it
- History of attempts

### RESEARCH QUESTIONS FOR TASKMASTER:

> **Q5:** Where is the ticketing system located in stereOS? What files need to be imported?

> **Q6:** What is the ticket data structure/schema?

> **Q7:** How does the ticketing system integrate with the UI? What components display tickets?

> **Q8:** Is there a ticket search/filter API?

### Ticket Lifecycle

```
┌──────────┐     ┌─────────────┐     ┌──────────┐     ┌──────────┐
│ PENDING  │────►│ IN_PROGRESS │────►│ RESOLVED │     │ BLOCKED  │
└──────────┘     └─────────────┘     └──────────┘     └──────────┘
     │                  │                                   ▲
     │                  └───────────────────────────────────┘
     │                         (if general fails)
     │
     └── Auto-created by Carl when health check fails
```

### Ticket Storage

```
.orchestr8/
├── tickets/
│   ├── TICKET-042.md
│   ├── TICKET-043.md
│   └── archive/
│       └── TICKET-041.md (resolved)
└── state/
    └── fiefdom-status.json
```

### Escalation System

| Level | Trigger | Action |
|-------|---------|--------|
| **WARNING** | Non-blocking issue, TODO detected | Yellow indicator, note encouraged |
| **ERROR** | Blocking issue, build fails | Red indicator, deployment suggested |
| **CRITICAL** | Multiple failed attempts | Emperor notification required |

---

## VI. Fiefdom Management

### What is a Fiefdom?

A fiefdom is a **directory scope** assigned to a general. It can be:
- A top-level directory: `src/llm/`
- A subdirectory: `src/modules/generator/`
- A specific feature area: `src/platform/auth/`

### Fiefdom Structure

Each fiefdom that may receive a general needs:

```
src/modules/generator/
├── CLAUDE.md           # Standing orders (permanent)
├── BRIEFING.md         # Current mission (generated per deployment)
├── CAMPAIGN_LOG.md     # Accumulated wisdom (append-only)
└── [source files]
```

### CLAUDE.md Template (Standing Orders)

```markdown
# CLAUDE.md - [Fiefdom Name]

## Your Identity
You are a GENERAL assigned to [specific responsibility].
You have access to subagents: Scout, Fixer, Validator, Git Agent.
Use them. More agents completing work > fewer agents failing.

## Your Fiefdom
**Path:** [absolute path]
**Scope:** [what this directory handles]

## Files You Own (Can Modify)
- `file1.ts`
- `file2.ts`

## Files You Must Not Touch (Louis Locked)
- `../protected/file.ts` - Reason: [why locked]

## Health Check Command
```bash
npm run typecheck
# Your fiefdom is healthy when this passes with no errors in your scope
```

## When You're Done
1. Run health check
2. Update CAMPAIGN_LOG.md with your actions
3. If VICTORY: Report success, specify what changed
4. If BLOCKED: Report what's blocking, suggest escalation
```

---

## VII. The Wisdom System

### The Core Insight

> "If an agent can hang around long enough in one fiefdom, it will literally gain wisdom. 'Last time this happened, someone broke the contact manager' is the ultimate feet-on-the-street hack, and it's totally free."

### How Wisdom Accumulates

```
General A deployed → Fixes bug → Writes to CAMPAIGN_LOG.md → Departs
         │
         ▼
    Wisdom persists in filesystem
         │
         ▼
General B deployed → Reads CAMPAIGN_LOG.md → Has predecessor's knowledge
         │
         ▼
General B encounters similar issue → Already knows the gotcha → Fixes faster
```

### CAMPAIGN_LOG.md Format

```markdown
# CAMPAIGN_LOG: src/modules/generator

*Append-only log of all general deployments and lessons learned.*

---

## [2026-01-26 14:45] TICKET-042

**General:** Claude (session abc123)
**Status:** VICTORY
**Duration:** 23 minutes

### Mission
Fix type errors in generator module.

### Actions Taken
1. Deployed Scout to analyze import structure
2. Found BuildSpec import pointing to old location
3. Deployed Fixer to update import paths in 3 files
4. Deployed Validator - health check passed

### Lessons Learned
- ⚠️ BuildSpec moved to `src/llm/types.ts` during LLM refactor
- ⚠️ Always check import paths after any refactor in `src/llm/`

### Watch List
- `src/modules/maestro/` imports from generator - may need similar fix
```

---

## VIII. Tool Integration: Carl, Connie, Louis

### Carl (The Context Gatherer)

**Location:** `IP/carl_core.py`

**Responsibilities:**
- Scan fiefdoms and build file inventory
- Run health checks (typecheck, tests)
- Generate Mermaid status graph
- Provide context for briefings
- Track connections between files

### Connie (The Converter)

**Location:** `IP/connie.py`

**Status:** ✅ Already working

**Responsibilities:**
- Convert SQLite databases to LLM-friendly formats
- Export schemas as JSON, Markdown, or CSV
- Make opaque data structures readable

### Louis (The Locksmith)

**Location:** `IP/louis_core.py`

**Responsibilities:**
- Lock files at OS level (chmod 444)
- Maintain lock registry
- Integrate with git pre-commit hook
- Temporary unlock for approved writes

---

## IX. ChangeChecker Integration

### The Decision Gate

Before any write to disk:

```
1. INTERCEPT
   └── Hook into: git pre-commit, Claude Code hook, file watcher

2. CONTEXT CHECK (Carl)
   └── What file? What changed? What's the diff?
   └── Related files? Connections? Dependencies?

3. DECISION VALIDATION
   └── Require: Ticket ID OR Decision Explanation
   └── Cross-ref: Does explanation match the change type?

4. RELATIONSHIP MAPPING (Connie + ConnectionVerifier)
   └── AST analysis of the change
   └── Affected connections (imports, stores, routes)
   └── LLM-friendly summary of impact

5. ENFORCEMENT (Louis)
   └── If valid: Unlock file, allow write, log decision
   └── If invalid: Block write, explain what's missing
   └── Always: Record to audit trail
```

### Git Integration

```bash
# .git/hooks/post-commit (for tracking)
#!/bin/bash
python3 -c "
from IP.carl_core import Carl
carl = Carl('.')
carl.check_health_all_fiefdoms()
carl.update_mermaid_graph()
"

# .git/hooks/pre-commit (for enforcement)
#!/bin/bash
python3 -c "
from IP.louis_core import Louis
louis = Louis('.')
# Check staged files against locks
"
```

### Files to Migrate from stereOS/Orchestr8_sr

### RESEARCH QUESTIONS FOR TASKMASTER:

> **Q9:** What is the file structure of Orchestr8_sr? What valuable IP exists there?

> **Q10:** Which files from stereOS should be migrated to Orchestr8_jr for ChangeChecker?
> - `unified-context-system.ts` → Translate to Python or call via subprocess?
> - `verification.rs` → Keep in Rust, call via subprocess?
> - `ParserPack/*.rs` → Keep in Rust, call via subprocess?

> **Q11:** What is the relationship between Orchestr8_sr and Orchestr8_jr? What's the migration path?

---

## X. Current Implementation Status

### Existing Files (Verified)

| File | Status | Notes |
|------|--------|-------|
| `IP/plugins/00_welcome.py` | EXISTS | Needs MaestroView styling |
| `IP/plugins/01_generator.py` | EXISTS | 7-Phase Wizard, needs styling |
| `IP/plugins/02_explorer.py` | EXISTS | File explorer, needs styling |
| `IP/plugins/03_gatekeeper.py` | EXISTS | Louis UI, Lock All/Unlock All COMPLETE |
| `IP/plugins/04_connie_ui.py` | EXISTS | Database converter UI |
| `IP/plugins/05_universal_bridge.py` | EXISTS | Registry-based tool discovery COMPLETE |
| `IP/plugins/06_maestro.py` | EXISTS | THE VOID - primary interface |
| `IP/plugins/output_renderer.py` | EXISTS | Smart JSON/text rendering COMPLETE |
| `IP/plugins/05_cli_bridge.py.deprecated` | DEPRECATED | Replaced by universal_bridge |

### Completed Tasks (from v3.0)

- **Task 13:** Gatekeeper refactor with Lock All/Unlock All buttons
- **Task 18:** Universal Bridge with registry-based discovery
- **Task 19:** CLI Bridge retirement
- **Task 20:** Daco template creation

### Runtime Directories (To Be Created)

```
.orchestr8/
├── tickets/
│   └── archive/
├── state/
│   └── fiefdom-status.json
└── mermaid-cache.md
```

---

## XI. Implementation Phases

### Phase 1: Foundation (Week 1)

**Goal:** Basic Void with Mermaid graph and fiefdom list

| Task | Priority | Effort |
|------|----------|--------|
| Update `06_maestro.py` with Mermaid as primary | P0 | 2-3 hours |
| Implement fiefdom list component | P0 | 2-3 hours |
| Add Carl health check integration | P0 | 2-3 hours |
| Create CLAUDE.md templates for 3 fiefdoms | P0 | 1 hour |
| Integrate actu8 terminal spawner | P0 | TBD (needs research) |
| Test full deploy flow manually | P0 | 1 hour |

**Deliverable:** Can view graph, see broken nodes, spawn terminal at fiefdom

### Phase 2: Ticket System (Week 2)

**Goal:** Full ticket lifecycle with stacking notes

| Task | Priority | Effort |
|------|----------|--------|
| Import ticket system from stereOS | P0 | TBD (needs research) |
| Create ticket data structure | P0 | 1-2 hours |
| Implement ticket creation (auto from health check) | P0 | 2-3 hours |
| Build Tickets panel (slide from right) | P0 | 2-3 hours |
| Implement stacking notes | P1 | 2 hours |
| Add error aggregation to tickets | P1 | 2 hours |

**Deliverable:** Tickets auto-created, notes stack, searchable

### Phase 3: Wisdom System (Week 3)

**Goal:** CAMPAIGN_LOG.md and BRIEFING.md generation

| Task | Priority | Effort |
|------|----------|--------|
| Create CAMPAIGN_LOG.md structure | P0 | 1 hour |
| Implement campaign entry appending | P0 | 2 hours |
| Build BRIEFING.md generator | P0 | 3-4 hours |
| Integrate wisdom into briefings | P0 | 2 hours |
| Extract lessons learned automatically | P1 | 2-3 hours |

**Deliverable:** Generals inherit wisdom from predecessors

### Phase 4: ChangeChecker Integration (Week 4)

**Goal:** Git hooks and basic enforcement

| Task | Priority | Effort |
|------|----------|--------|
| Implement git pre-commit hook (Louis) | P0 | 2 hours |
| Implement git post-commit hook (Carl) | P0 | 2 hours |
| Add manual refresh button | P0 | 30 min |
| Integrate Connection Verifier (if available) | P1 | 4-6 hours |
| Add file watcher (optional) | P2 | 3 hours |

**Deliverable:** Changes trigger health checks, locks enforced

### Phase 5: Styling (Best Effort MaestroView Alignment)

**Goal:** Match MaestroView.vue aesthetic within Marimo constraints

### RESEARCH QUESTIONS FOR TASKMASTER:

> **Q12:** What CSS injection capabilities does Marimo have? Can we inject custom CSS variables?

> **Q13:** What font loading options exist in Marimo? Can we load JetBrains Mono, IBM Plex Mono?

> **Q14:** What animation capabilities exist in Marimo? Can we do emerge transitions?

> **Q15:** What mo.Html capabilities exist for custom-styled components?

| Task | Priority | Effort |
|------|----------|--------|
| Research Marimo CSS capabilities | P0 | 2 hours |
| Create app-level CSS injection | P1 | 2-3 hours |
| Apply color palette to all plugins | P1 | 4-6 hours |
| Style buttons with MaestroView patterns | P2 | 2-3 hours |
| Add emerge animations (if possible) | P3 | TBD |

**Deliverable:** Best-effort visual alignment with MaestroView.vue

---

## XII. File Structure

### Orchestr8_jr Directory Structure

```
Orchestr8_jr/
├── ROADMAP_ORCHESTR8_V4.md          # Strategic roadmap
├── CLAUDE.md                         # Project-level standing orders
├── orchestr8.py                      # Original Marimo app
│
├── IP/                               # The IP Protocol directory
│   ├── orchestr8_app.py             # Main Marimo application
│   ├── carl_core.py                 # Context gatherer
│   ├── connie.py                    # Database converter
│   ├── louis_core.py                # File locker
│   │
│   └── plugins/                     # Marimo plugins
│       ├── 00_welcome.py
│       ├── 01_generator.py
│       ├── 02_explorer.py
│       ├── 03_gatekeeper.py
│       ├── 04_connie_ui.py
│       ├── 05_universal_bridge.py
│       ├── 06_maestro.py            # THE VOID (primary)
│       └── output_renderer.py
│
├── .orchestr8/                      # Runtime state (to create)
│   ├── tickets/
│   └── state/
│
├── style/                           # Style reference
│   └── MAESTROVIEW_REFERENCE.md
│
├── PRDs/                            # Product requirements
│   └── PRD_ORCHESTR8_V4_CONSOLIDATED.md
│
└── Archive/                         # Archived reports
```

---

## XIII. For the Generals: Operating Manual

### Prime Directive

When you are deployed to a fiefdom:

1. **Read BRIEFING.md first** - Your current mission with full context
2. **Read CLAUDE.md second** - Your standing orders for this fiefdom
3. **Scan CAMPAIGN_LOG.md** - Learn from your predecessors
4. **Stay in scope** - Only modify files you own
5. **Respect Louis locks** - Don't touch protected files
6. **Use your subagents** - Scout, Fixer, Validator, Git Agent
7. **Run health check when done** - `npm run typecheck` or equivalent
8. **Update CAMPAIGN_LOG.md** - Record your actions and lessons
9. **Report clearly** - What changed, what's still broken (if anything)

**You succeed when your fiefdom turns from blue/purple to gold.**

### When to Escalate

Escalate to the Emperor when:
- You're blocked by a Louis lock that seems incorrect
- You discover architectural issues beyond your fiefdom
- Multiple fiefdoms need coordinated changes
- You've failed twice on the same issue
- The ticket scope seems wrong

---

## XIV. Open Research Questions Summary

The following questions require Taskmaster research mode to answer:

### actu8 Terminal
1. Where is actu8 located in stereOS?
2. What are actu8's dependencies?
3. Does actu8 have Tauri-specific dependencies needing adaptation?
4. What is actu8's spawn interface/API?

### Ticket System
5. Where is the ticketing system in stereOS?
6. What is the ticket data structure/schema?
7. How does the ticketing system integrate with UI?
8. Is there a ticket search/filter API?

### Integration with Orchestr8_sr
9. What is the file structure of Orchestr8_sr?
10. Which files should migrate for ChangeChecker?
11. What is the Orchestr8_sr to Orchestr8_jr migration path?

### Marimo Styling
12. What CSS injection capabilities does Marimo have?
13. What font loading options exist in Marimo?
14. What animation capabilities exist in Marimo?
15. What mo.Html capabilities exist?

---

## XV. Signatures

**Approved by:**
- Ben (Human Emperor) - 2026-01-26
- Claude (Strategic Council) - 2026-01-26

**Version:** 4.0 Consolidated  
**Status:** READY FOR TASKMASTER PARSING

---

*"We don't mark things for later. We execute against them immediately."*

---

**END PRD**
