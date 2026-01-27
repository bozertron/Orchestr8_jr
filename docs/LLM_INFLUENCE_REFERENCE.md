# LLM Influence in Marimo: Complete Reference

**Purpose:** Every mechanism for influencing LLM behavior in our environment  
**Scope:** Internal work - no external IP needed  
**Status:** RESEARCH COMPLETE - READY FOR DISCUSSION

---

## Overview

Marimo provides **six distinct layers** of LLM influence, from global configuration to per-prompt injection. This document covers ALL of them.

---

## Layer 1: marimo.toml Global Configuration

**Location:** `~/.marimo.toml` or project `marimo.toml`  
**Scope:** All notebooks, all AI interactions

### 1.1 Model Selection

```toml
[ai.models]
# Three distinct roles with different cost/capability tradeoffs
chat_model = "anthropic/claude-sonnet-4-20250514"       # Chat panel conversations
edit_model = "anthropic/claude-sonnet-4-20250514"       # Ctrl+Shift+E refactoring, "Generate with AI"
autocomplete_model = "ollama/codellama"    # Tab completion (can use cheap/fast local)

# Add custom models to dropdown
custom_models = ["ollama/somemodel", "openrouter/deepseek/deepseek-chat"]
```

**Key Insight:** You can use different models for different tasks:
- **Expensive/smart** for editing and chat
- **Cheap/fast/local** for autocomplete
- **Privacy-sensitive** local model for proprietary code

### 1.2 Global Rules

**THE MOST IMPORTANT SETTING FOR ORCHESTR8**

```toml
[ai]
rules = """
- Use MaestroView.vue color variables (--gold-metallic: #D4AF37, --blue-dominant: #1fbdea, --purple-combat: #9D4EDD)
- The Void background is #0A0A0B, elevated surfaces are #121214
- Fiefdoms are directory scopes, generals are Claude Code instances
- Status colors: gold=working, blue=broken, purple=combat (general deployed)
- Use pathlib for all file operations, never os.path
- Python 3.12+ syntax required
- All UI elements use mo.ui.* components
- No breathing animations, no emojis in UI, no clock
- The Overton Anchor (bottom input bar) NEVER MOVES
- Always prefer polars over pandas
- Use JetBrains Mono or IBM Plex Mono fonts
- Type hints on all function signatures
"""
max_tokens = 4000  # Increase for complex responses
```

**These rules are injected into EVERY AI call.** This is how we train the AI to understand Orchestr8 conventions.

### 1.3 Provider-Specific Configuration

```toml
# Anthropic (Claude) - PRIMARY
[ai.anthropic]
api_key = "sk-ant-..."  # Or use ANTHROPIC_API_KEY env var

# OpenAI - SECONDARY
[ai.open_ai]
api_key = "sk-proj-..."

# Ollama - LOCAL MODELS
[ai.ollama]
base_url = "http://127.0.0.1:11434/v1"  # MUST include /v1

# OpenRouter - MULTI-PROVIDER
[ai.openrouter]
api_key = "sk-or-..."
base_url = "https://openrouter.ai/api/v1/"

# Custom OpenAI-compatible provider (e.g., Big Pickle if it has an API)
[ai.custom_providers.big_pickle]
api_key = "..."
base_url = "http://localhost:8080/v1"
```

---

## Layer 2: CLAUDE.md / AGENTS.md Project Files

**Location:** Project root or any directory  
**Scope:** Claude Code and similar agents running in terminal

These files provide standing orders when agents work on your codebase.

### 2.1 Recommended CLAUDE.md Structure

```markdown
# Marimo Notebook Assistant

## Project Context
- Project: Orchestr8_jr
- Runtime: Marimo (reactive Python notebook)
- Design Reference: MaestroView.vue

## Color System (EXACT VALUES)
- --gold-metallic: #D4AF37 (working status)
- --blue-dominant: #1fbdea (broken status)  
- --purple-combat: #9D4EDD (combat/deployed)
- --bg-primary: #0A0A0B (The Void)
- --bg-elevated: #121214 (surfaces)

## Terminology
- Fiefdom = directory scope assigned to a general
- General = Claude Code instance deployed to fix issues
- The Void = main dashboard interface
- Overton Anchor = fixed bottom input bar

## Code Requirements
1. All code must be complete and runnable
2. Use @app.cell decorator for all cells
3. Never redeclare variables across cells
4. Last expression in cell is automatically displayed
5. Access UI element values with .value (e.g., slider.value)
6. Create UI elements in one cell, reference in later cells

## Marimo Specifics
- Import marimo as mo in first cell
- Use mo.md() for markdown, mo.Html() for raw HTML
- Use mo.ui.* for all interactive elements
- Use mo.hstack(), mo.vstack(), mo.tabs() for layout
- Style with .style() method, not inline CSS when possible

## Forbidden
- No breathing animations
- No emojis in UI elements
- No clock display
- No moving the bottom input bar
```

### 2.2 Fiefdom-Specific CLAUDE.md

Each fiefdom can have its own CLAUDE.md with specialized instructions:

```markdown
# CLAUDE.md - IP/plugins/

## Your Fiefdom
**Path:** /home/bozertron/Orchestr8_jr/IP/plugins/
**Scope:** Marimo UI plugins for Orchestr8

## Files You Own
- 00_welcome.py through 06_maestro.py
- output_renderer.py

## Louis-Locked Files (DO NOT TOUCH)
- ../carl_core.py - Context gathering (separate fiefdom)
- ../louis_core.py - File locking (separate fiefdom)

## Styling Rules for This Fiefdom
- All plugins must apply MaestroView color variables
- Use CSS injection via mo.Html("<style>...")
- Named cells use @app.cell(name="cell_name")
```

---

## Layer 3: Prompt Templates (Conversation Starters)

**Use:** Copy-paste at start of conversation  
**Cost:** Only charged once per conversation (unlike rules)

### 3.1 Orchestr8 Development Template

```
I'm working on Orchestr8, a Marimo-based command center for coordinating Claude Code instances.

Key context:
- Colors: gold (#D4AF37) = working, blue (#1fbdea) = broken, purple (#9D4EDD) = combat
- Background: #0A0A0B (The Void), surfaces: #121214
- No animations, no emojis, no clock
- Bottom input bar is FIXED (Overton Anchor)

When generating code:
- Use mo.ui.* components
- Style with .style() method
- Apply CSS variables via mo.Html("<style>:root{...}</style>")
- Use pathlib, not os.path
- Python 3.12+ syntax
```

### 3.2 Styling-Specific Template

```
I need to style a Marimo component to match MaestroView.vue.

Reference colors:
:root {
    --gold-metallic: #D4AF37;
    --gold-dark: #B8860B;
    --gold-saffron: #F4C430;
    --blue-dominant: #1fbdea;
    --purple-combat: #9D4EDD;
    --bg-primary: #0A0A0B;
    --bg-elevated: #121214;
}

Requirements:
- Dark theme only
- Gold accents for interactive elements
- Blue for broken/error states
- Purple for active/combat states
- No breathing animations
```

---

## Layer 4: Variable Context (@mentions)

**Use:** Reference runtime values in prompts  
**Syntax:** `@variable_name`

### 4.1 How It Works

When you type `@df` in a prompt, Marimo injects the actual value/schema of that variable:

```python
# If df is a polars DataFrame with columns ['fiefdom', 'status', 'health']
# Typing "@df" in prompt gives the AI access to:
# - Column names
# - Data types
# - Sample values
```

### 4.2 Orchestr8 Use Cases

```python
# Reference fiefdom status data
@fiefdom_status  # AI sees: {"src/llm": "working", "src/modules": "broken"}

# Reference current theme configuration
@theme_config  # AI sees: {"bg_primary": "#0A0A0B", ...}

# Reference error messages
@health_check_errors  # AI sees: ["TypeError in line 42", ...]
```

---

## Layer 5: Chat Panel Modes

**Location:** Left sidebar chat panel  
**Three Modes:**

### 5.1 Manual Mode
- No tool access
- AI responds based only on conversation
- Best for: General questions, explanations

### 5.2 Ask Mode
- Read-only AI tools enabled
- Can inspect notebooks, read files
- Can use MCP Client servers
- Best for: Understanding code, finding patterns

### 5.3 Agent Mode (BETA)
- Full tool access including editing
- Can add, remove, update cells
- Can run stale cells
- Best for: Automated coding tasks

**THIS IS HUGE FOR ORCHESTR8** - Agent mode could potentially be used for automated general deployment.

---

## Layer 6: Per-Cell AI Context

**Use:** Cell-specific instructions via comments or docstrings

### 6.1 Cell Comments for AI

```python
@app.cell
def _():
    # AI: This cell handles fiefdom status display
    # AI: Use gold for working, blue for broken, purple for combat
    # AI: Never modify the color values
    status_display = mo.Html("""...""")
    return status_display
```

### 6.2 Docstrings for Functions

```python
@app.cell
def _():
    def render_fiefdom_card(name: str, status: str) -> mo.Html:
        """
        Render a fiefdom status card.
        
        AI Instructions:
        - status must be one of: 'working', 'broken', 'combat'
        - Use MaestroView color variables
        - Card background: #121214
        - Border color based on status
        """
        ...
```

---

## Layer 7: Custom HTML Head Injection

**Use:** Load external resources that affect AI-generated code

```html
<!-- head.html -->
<!-- AI can reference these when generating code -->
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono&display=swap" rel="stylesheet">

<style>
  :root {
    /* AI will see these variables when inspecting page */
    --gold-metallic: #D4AF37;
    --blue-dominant: #1fbdea;
    --purple-combat: #9D4EDD;
    --bg-primary: #0A0A0B;
    --bg-elevated: #121214;
  }
</style>
```

---

## Complete Influence Stack (Orchestr8 Recommended)

### File Structure

```
Orchestr8_jr/
├── .marimo.toml              # Global AI rules (Layer 1)
├── CLAUDE.md                 # Project-wide agent instructions (Layer 2)
├── pyproject.toml            # Project-level overrides
│   └── [tool.marimo.ai]
├── IP/
│   ├── styles/
│   │   └── orchestr8.css     # CSS variables AI should reference
│   ├── prompts/
│   │   └── orchestr8.md      # Prompt templates (Layer 3)
│   └── plugins/
│       └── CLAUDE.md         # Fiefdom-specific instructions
└── head.html                 # HTML head injection (Layer 7)
```

### marimo.toml (Master Configuration)

```toml
[ai.models]
chat_model = "anthropic/claude-sonnet-4-20250514"
edit_model = "anthropic/claude-sonnet-4-20250514"
autocomplete_model = "ollama/codellama"

[ai]
max_tokens = 4000
rules = """
# ORCHESTR8 DEVELOPMENT RULES

## Identity
You are assisting with Orchestr8, a Marimo-based command center for coordinating Claude Code instances ("generals") across codebases.

## Color System (MaestroView.vue Reference)
EXACT hex values - NO EXCEPTIONS:
- --gold-metallic: #D4AF37 (working status, interactive elements)
- --gold-dark: #B8860B (timestamps, secondary gold)
- --gold-saffron: #F4C430 (hover states)
- --blue-dominant: #1fbdea (broken status, UI default)
- --purple-combat: #9D4EDD (combat status, general deployed)
- --bg-primary: #0A0A0B (The Void background)
- --bg-elevated: #121214 (surfaces, panels, inputs)

## Terminology
- Fiefdom = directory scope assigned to a general
- General = Claude Code instance working in a fiefdom
- The Void = main dashboard (#0A0A0B background)
- Overton Anchor = bottom 5th input bar (NEVER MOVES)
- Scout = read-only analysis subagent
- Fixer = surgical code change subagent

## Status Meanings
- Gold/Working: All imports resolve, typecheck passes
- Blue/Broken: Has errors, needs attention
- Purple/Combat: General currently deployed and active

## Code Style
- Python 3.12+ syntax required
- Type hints on all function signatures
- Use pathlib for file operations, never os.path
- Prefer polars over pandas
- Use dataclasses for data structures

## Marimo Specifics
- Import marimo as mo in first cell
- Use @app.cell decorator
- Access UI values via .value attribute
- Create UI in one cell, reference in later cells
- Use mo.hstack(), mo.vstack(), mo.tabs() for layout
- Style via .style() method when possible
- For CSS injection: mo.Html("<style>:root{...}</style>")

## Design Prohibitions
- NO breathing animations
- NO emojis in UI elements
- NO clock display
- NO moving the Overton Anchor
- NO white backgrounds
- NO default Marimo colors (override everything)

## When Generating UI Code
1. Start with CSS variable injection
2. Use named cells: @app.cell(name="descriptive_name")
3. Apply status colors based on fiefdom health
4. Ensure all panels emerge from The Void
5. Test with dark theme only
"""

[ai.anthropic]
api_key = "sk-ant-..."  # Or ANTHROPIC_API_KEY env var

[ai.ollama]
base_url = "http://127.0.0.1:11434/v1"
```

---

## Discussion Points

### 1. Rule Priority Questions

- **Q:** How verbose should global rules be? Token cost vs. consistency trade-off.
- **Q:** Should fiefdom-specific rules override global rules?
- **Q:** How do we handle conflicting instructions?

### 2. Model Selection Questions

- **Q:** Claude for chat/edit, Ollama for autocomplete - good split?
- **Q:** Should we use cheaper models for certain tasks?
- **Q:** OpenRouter for redundancy?

### 3. Agent Mode Considerations

- **Q:** Can Agent mode be used for automated general deployment?
- **Q:** What are the safety boundaries?
- **Q:** How does it interact with Louis locks?

### 4. Big Pickle Integration

- **Q:** Does Big Pickle have an OpenAI-compatible API?
- **Q:** If so, can we add it as a custom provider?
- **Q:** What role would Big Pickle play vs Claude?

### 5. Local Model Use Cases

- **Q:** Ollama for embeddings - how to configure?
- **Q:** Local models for sensitive code analysis?
- **Q:** Speed vs. quality trade-off for autocomplete?

---

## Action Items After Discussion

1. [ ] Finalize marimo.toml rules content
2. [ ] Create master CLAUDE.md for project root
3. [ ] Create fiefdom-specific CLAUDE.md files
4. [ ] Set up Ollama for local autocomplete
5. [ ] Test Agent mode for potential general deployment
6. [ ] Document Big Pickle integration path (if applicable)

---

**END REFERENCE DOCUMENT**
