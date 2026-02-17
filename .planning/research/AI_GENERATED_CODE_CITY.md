# AI-Generated Code City: The Killer Feature

**Research Date:** 2026-02-13

---

## The Vision

**"Research a codebase for 2 hours, then drop a killer prompt on an AI to generate a Code City visualization."**

This is actually possible with what's already built into marimo.

---

## What's Already Possible

### Marimo's `marimo new` Command

```bash
marimo new "Create a Code City visualization of this Python project"
```

This already generates an entire notebook from a prompt. We would craft a specialized prompt for Code City.

### The Integration Chain

```
Research Agents → Research Output → Killer Prompt → marimo new → Code City
```

---

## The Components

### 1. Research Phase (We Already Have This)

Our agent system can research:

- File structure
- Dependencies  
- Code complexity
- Health/status signals
- Agent activity

Output: Structured JSON describing the codebase

### 2. The Killer Prompt

```markdown
Create a Code City visualization in marimo that shows:

**Data from research:**
- 47 Python files across 5 fiefdoms
- Fiefdom "orchestr8_core" has 12 files, highest complexity
- 3 broken imports detected in IP/woven_maps.py
- Agent "Sol" was last active on 5 files

**Visualization requirements:**
- 3D city layout with buildings sized by complexity
- Color coding: gold=working, teal=broken, purple=combat
- Particle emergence animation for files loading
- Hover tooltips showing file status and errors
- Click to navigate into neighborhoods

**Technical requirements:**
- Use WebGPU with CPU fallback
- Include orbit controls and warp-dive on click
- Show neighborhood boundaries
- Include connection panel for import graph

Generate the complete marimo notebook code.
```

### 3. Reference Graphics

We can include:

- Screenshots of current Code City
- SOT locked colors (#D4AF37, #1fbdea, #9D4EDD)
- The orchestr8 layout (IP/plugins/06_maestro.py)
- Building formulas: height = 3 + (exports * 0.8)

---

## Tools at Our Disposal

### NiceGUI (Alternative UI)

From research:

- FastAPI backend, Vue/Quasar frontend
- WebSocket communication
- Active development (3.7.1 Feb 2026)
- Good for dashboards, but we're staying with marimo

### Marimo AI Features

| Feature | Status | Use for Code City |
|---------|--------|-------------------|
| `marimo new PROMPT` | ✅ Built-in | Generate notebook |
| Variable context (@df) | ✅ Built-in | Pass research data |
| Custom rules | ✅ Configurable | Enforce SOT |
| LLM providers | ✅ Multiple | Anthropic/OpenAI/Ollama |
| Generate with AI button | ✅ UI | Interactive generation |

---

## The Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. RESEARCH (2 hours)                                      │
│     - Survey codebase with agents                            │
│     - Extract: files, fiefdoms, imports, health, agents     │
│     - Output: research.json                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  2. CRAFT PROMPT                                            │
│     - Include research.json data                             │
│     - Reference graphics (colors, formulas, layout)          │
│     - Specify visualization requirements                     │
│     - Output: killer_prompt.md                              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  3. AI GENERATION                                           │
│     - Run: marimo new "$(cat killer_prompt.md)"             │
│     - AI generates Python code for Code City                │
│     - Output: generated_notebook.py                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  4. RENDER                                                  │
│     - marimo run generated_notebook.py                      │
│     - Code City visualization renders                       │
│     - Interactive: hover, click, warp-dive                  │
└─────────────────────────────────────────────────────────────┘
```

---

## What's Needed

### 1. Research Template

A standardized template for codebase research that produces:

- File list with metrics
- Fiefdom boundaries
- Import graph
- Health signals
- Agent activity

### 2. Code City Prompt Library

Pre-built prompts for common visualizations:

- "Overview" - Full city view
- "Broken only" - Just error buildings
- "Recent changes" - Files modified recently
- "Agent activity" - Show who worked where

### 3. Reference Graphics

Store in project:

- SOT color palette
- Building formula reference
- Layout screenshots
- Animation examples (emergence)

---

## Files to Create

| File | Purpose |
|------|---------|
| `.planning/research/AI_CODE_CITY_PROMPT_TEMPLATE.md` | Prompt template for AI |
| `.planning/research/AI_CODE_CITY_WORKFLOW.md` | Complete workflow |
| `.planning/research/AI_REFERENCE_GRAPHICS.md` | Reference materials |

---

## Next Steps

1. **Create prompt template** - Define the research output format
2. **Build reference graphics** - Document SOT colors, formulas, layouts
3. **Test `marimo new`** - Try generating a simple Code City
4. **Iterate** - Refine prompt based on output quality

---

## The Big Picture

This connects to the larger vision:

- **Research** = Settlement System surveys codebase
- **Killer Prompt** = Human-readable specification  
- **AI Generation** = Code writes itself
- **Code City** = Visual output

The AI doesn't just generate charts—it generates the entire interactive visualization. We're building "AI-generated Code City" as a first-class feature.
