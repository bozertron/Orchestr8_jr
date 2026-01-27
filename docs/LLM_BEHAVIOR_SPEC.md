# LLM Behavior Specification

**Created:** 2026-01-26  
**Status:** EMPEROR APPROVED  
**Scope:** All LLM integration, API configuration, and behavioral rules for Orchestr8

---

## Table of Contents

1. [Model Selection Strategy](#model-selection-strategy)
2. [API Key Configuration](#api-key-configuration)
3. [Provider List](#provider-list)
4. [Rule Enforcement (Standing Orders)](#rule-enforcement-standing-orders)
5. [Agent Mode Tiers](#agent-mode-tiers)
6. [Template Specifications](#template-specifications)
7. [marimo.toml Configuration](#marimotoml-configuration)

---

## 1. Model Selection Strategy

### Primary Chat: maestro

**CRITICAL:** The primary chat LLM is ALWAYS named `maestro` (lowercase 'm').

- User's choice of underlying model
- Pre-populate toml with placeholder: `[modelnamelikethis]`
- API field placeholder: `[APIlikethis]`
- Potential future: pipe-in integration with external tools

### Edit/Refactor Models

No default - load all supported options:
- OpenAI
- Anthropic
- Open Router
- x.AI (if supported)
- OpenCode (if supported)
- Groq (if supported)
- Perplexity (if supported)

### Autocomplete

Local model via:
- Ollama
- vLLM (if supported)

### Embeddings

Local models, two focused purposes:
1. **Embeddings** - Vector similarity search
2. **Document work/creation** - RAG, summarization

### Big Pickle

**Big Pickle = OpenCode**

When configured, Big Pickle provides regular assistance as an implementation partner.

---

## 2. API Key Configuration

### Storage Strategy

**Priority:** Easiest option for single-user workflow.

| Aspect | Decision |
|--------|----------|
| Storage location | Settings UI (config file backing) |
| Scope | **Global keys** (not per-project) |
| Security | Basic config - vault implementation deferred to commercial phase |

### Why Global Keys?

> "Again, let's make my life easier here, guys!" - Emperor

Single user = simplicity over security theater.

---

## 3. Provider List

### Tier 1: Core Providers (Pre-configured)

From user's explicit list:
- **OpenAI** - GPT-4, GPT-4o, etc.
- **Anthropic** - Claude models
- **Open Router** - Model aggregator
- **x.AI** - Grok models
- **OpenCode** - Big Pickle's home
- **Groq** - Fast inference
- **Perplexity** - Search-augmented

### Tier 2: Extended Providers

Standard industry providers:
- **Google** - Gemini models
- **Mistral** - European alternative
- **Cerebras** - Fast inference
- **Deepseek** - Cost-effective
- **Minimax** - Specialized models
- **HuggingFace** - Open source hub

### Tier 3: Reference Implementation

Look at provider lists from:
- **Kilocode** - IDE extension provider patterns
- **Cline** - Agent-style provider patterns
- **stereOS** - Potential UI concept boost (not Python)

### UI Requirement

> "Let's front-load the effort and just make a nice UI for it all."

Settings panel should present:
1. Provider selector
2. API key input per provider
3. Model selector per provider
4. Test connection button
5. Usage/quota display (if available)

---

## 4. Rule Enforcement (Standing Orders)

### Core Philosophy

> "If we see a problem, we attempt to solve it. Immediately, and with savage and relentless vigor."

### EPO Standards (Non-Negotiable)

| Rule | Violation = | Why |
|------|-------------|-----|
| **No mocks** | Door | "It's more work!" - creates technical debt |
| **No stubs** | Door | Must be "literally life and death" |
| **No unused imports** | Door | Without understanding why they're there |
| **No "fail silently"** | Door | Fix the actual problem |
| **Always read before edit** | Door | Prevents errors from ignorance |

### The EPO Principle

> "Just, think about what you're doing, respect the people you work with, and you'll get nuttin' but love."

### What This Means for LLMs

1. Don't create mock implementations to "move fast"
2. Don't stub out functions with `pass` or `TODO`
3. Don't remove imports without tracing their purpose
4. Don't wrap errors in try/except silence
5. Always read file context before modifying

---

## 5. Agent Mode Tiers

### The Four Tiers

| Tier | Name | Permissions | Use Case |
|------|------|-------------|----------|
| **1** | Catastrophic Block | BLOCKED | Actions that could nuke codebase |
| **2** | Standard | DEFAULT | Look around, copy, implement freely |
| **3** | Ticket-Scoped | Restricted | Only explicit file on ticket |
| **4** | Read-Only | Planning | Research, analysis, no writes |

### Default Settings

- **Generals (Claude instances, Big Pickle)**: Tier 2
- **Unknown/New LLMs**: Tier 4 until promoted

### Self-Engagement Rule

**CRITICAL:** LLMs must NOT self-engage Agent mode.

If an LLM engages Agent mode without human activation:
1. Louis' lock-farm trips
2. LLM output is blocked
3. LLM must explain why they ignored the rules

> "When it's engaged by the human user. If an LLM engages Agent mode on their own, it'll trip Louis' lock-farm."

### Tier 3 Rationale

> "Only the very explicit file that is on your ticket. No 'looking around in an area you have no idea about, and just starting to pound on code'"

This prevents the common failure mode where LLMs:
- Wander into unfamiliar code areas
- Make assumptions about architecture
- "Fix" things that aren't broken
- Create cascading errors from ignorance

### Max Tokens

**None.** Fill 'yer boots.

No artificial limits on context or output.

---

## 6. Template Specifications

### CLAUDE.md (Standing Orders)

The standing orders document that ALL LLM Generals must follow.

**Contents:**
- EPO rules (no mocks, no stubs, read-before-edit)
- Naming conventions (maestro = lowercase)
- Agent mode tier system
- Fiefdom/General hierarchy
- Color semantics (gold=working, blue=broken, purple=combat)
- Communication style expectations

### BRIEFING.md (Mission Context)

Mission-specific context for current work.

**Auto-generated from:**
- Current ticket/task details
- Related file context
- Recent CAMPAIGN_LOG entries
- Known issues in scope

### CAMPAIGN_LOG.md (Wisdom)

Historical knowledge and lessons learned.

**Accumulates:**
- Successful solutions
- Failed approaches (don't repeat)
- Architecture decisions and rationale
- Inter-fiefdom dependencies discovered

### Ticket Structure

**Core Principle:** All available data, auto-populated.

**Auto-population triggers:**
- Warnings during execution
- Errors during execution
- Test failures
- Blue spots on codemap

**When clicking a blue spot (broken circuit):**

> "ALL the data we can acquire on that explicit circuit in every way should be available to the engineers."

Data to include:
- Error message(s)
- Stack trace
- Related file paths
- Recent changes to affected files
- Dependencies (upstream/downstream)
- Last successful state (if known)
- Related tickets/history
- Suggested diagnostic steps

---

## 7. marimo.toml Configuration

### Template (Pre-populated)

```toml
# Orchestr8 LLM Configuration
# Generated: 2026-01-26
# API keys: Fill in your own values

[ai]
# No max_tokens limit - "Fill 'yer boots"
rules = """
# ORCHESTR8 STANDING ORDERS (EPO STANDARDS)

## Core Philosophy
If we see a problem, we attempt to solve it. Immediately, and with savage and relentless vigor.

## Non-Negotiable Rules
1. NEVER use mocks unless literally life-or-death emergency
2. NO stubs, EVER - must be life-or-death to justify
3. NEVER remove unused imports without understanding WHY they exist
4. NEVER use "fail silently" tricks - FIX THE ACTUAL PROBLEM
5. ALWAYS read a file before editing it

## Naming Conventions
- Primary chat LLM is always "maestro" (lowercase 'm')
- Status colors: gold=working, blue=broken, purple=combat
- Fiefdoms are directory scopes, Generals are Claude Code instances

## Agent Mode
- Only engage when human activates
- Self-engagement trips Louis' lock-farm
- Default tier for Generals: 2 (Standard)

## The EPO Principle
Think about what you're doing. Respect the people you work with.
"""

[ai.models]
# Primary chat - maestro (your choice of model)
chat_model = "[modelnamelikethis]"

# Edit/Refactor - your choice
edit_model = "[modelnamelikethis]"

# Autocomplete - local model
autocomplete_model = "ollama/[modelnamelikethis]"

[ai.providers]
# Tier 1: Core Providers
[ai.providers.anthropic]
api_key = "[APIlikethis]"
enabled = true

[ai.providers.openai]
api_key = "[APIlikethis]"
enabled = true

[ai.providers.openrouter]
api_key = "[APIlikethis]"
enabled = true

[ai.providers.xai]
api_key = "[APIlikethis]"
enabled = true

[ai.providers.opencode]
api_key = "[APIlikethis]"
enabled = true
# Big Pickle's home

[ai.providers.groq]
api_key = "[APIlikethis]"
enabled = true

[ai.providers.perplexity]
api_key = "[APIlikethis]"
enabled = true

# Tier 2: Extended Providers
[ai.providers.google]
api_key = "[APIlikethis]"
enabled = true

[ai.providers.mistral]
api_key = "[APIlikethis]"
enabled = true

[ai.providers.cerebras]
api_key = "[APIlikethis]"
enabled = true

[ai.providers.deepseek]
api_key = "[APIlikethis]"
enabled = true

[ai.providers.minimax]
api_key = "[APIlikethis]"
enabled = true

[ai.providers.huggingface]
api_key = "[APIlikethis]"
enabled = true

# Local Providers (no API key needed)
[ai.providers.ollama]
enabled = true
base_url = "http://localhost:11434"

[ai.providers.vllm]
enabled = false
base_url = "http://localhost:8000"

[ai.embeddings]
# Local embeddings model
model = "ollama/[embeddingmodellikethis]"

[ai.documents]
# Document processing model
model = "ollama/[documentmodellikethis]"
```

---

## UI Requirements Summary

### Settings Panel Features

1. **Provider List**
   - All Tier 1 and Tier 2 providers pre-listed
   - Enable/disable toggle per provider
   - API key input field per provider
   - Model selector dropdown per provider
   - Test connection button
   - Usage/quota display (where API supports)

2. **Reference for UI Pattern**
   - Kilocode provider UI
   - Cline provider UI
   - stereOS settings (conceptual boost, not Python)

3. **Key Entry Workflow**
   - User fills in after setup
   - Settings persist to config file
   - Global scope (not per-project)

---

## Status

| Component | Status |
|-----------|--------|
| Model selection strategy | SPECIFIED |
| API key handling | SPECIFIED |
| Provider list | SPECIFIED |
| Rule enforcement | SPECIFIED |
| Agent mode tiers | SPECIFIED |
| Templates | SPECIFIED |
| marimo.toml template | READY TO DEPLOY |

---

**END SPECIFICATION**
