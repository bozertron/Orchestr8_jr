# Technology Stack

**Analysis Date:** 2026-01-30

## Languages

**Primary:**
- Python 3.14.2 - Core application and all plugin development
- JavaScript/TypeScript (support only) - Import resolution verification in `IP/connection_verifier.py`, not used for application code

**Secondary:**
- HTML/CSS - UI rendering and custom styling in `IP/styles/`

## Runtime

**Environment:**
- Python 3.12+ (required per `orchestr8.py` docstring)
- Currently running: Python 3.14.2

**Package Manager:**
- pip
- Lockfile: Not present (requirements specified in documentation only)

## Frameworks

**Core:**
- Marimo 0.19.6 - Reactive Python notebook framework for UI
  - Used in `orchestr8.py` (entry point: `marimo.App()`)
  - All plugin rendering uses marimo's reactive state system
  - Provides UI components: `mo.ui.text()`, `mo.ui.tabs()`, `mo.md()`, `mo.Html()`, `mo.vstack()`, `mo.hstack()`

**Data Processing:**
- pandas - Data manipulation and table operations
  - Used in database conversion (`IP/connie.py`)
  - Used for data export/import operations

**Analysis & Visualization:**
- networkx - Graph data structures for dependency analysis
  - Used in `IP/connection_verifier.py` for import graph building
  - Supports node relationship tracking and traversal

**Visualization:**
- pyvis - Network visualization library
  - Used for interactive graph visualization in code city views

**Template Generation:**
- jinja2 - Template engine for diagram and document generation
  - Used in `IP/mermaid_generator.py` for Mermaid diagram templates

## Key Dependencies

**Critical:**
- marimo 0.19.6 - Application framework (UI, state management, reactivity)
- anthropic (optional, pip-installed separately) - Claude API integration for chat
  - Try/except handling in `IP/plugins/06_maestro.py`
  - Required for AI conversation features; app still functions without it

**Infrastructure:**
- pandas - Database/CSV handling
- networkx - Graph algorithms
- pyvis - Interactive visualization
- jinja2 - Template generation
- toml - Configuration file parsing (`pyproject_orchestr8_settings.toml`)

**Standard Library Heavy:**
- json - State persistence (`.orchestr8/combat_state.json`)
- sqlite3 - Database operations
- pathlib - File system navigation
- subprocess - External tool invocation (health checkers, terminals)
- dataclasses - Data structures throughout codebase
- enum - State enumerations (CombatTracker, HealthCheckResult)
- threading/time - Concurrent operations

## Configuration

**Environment:**
- Configuration via `pyproject_orchestr8_settings.toml` (340+ lines)
- Settings organized into sections:
  - agents (director, professor, doctor)
  - tools (actu8, senses, cre8, communic8, integr8, innov8)
  - local_models (document, image, audio, video, embedding)
  - integration (OnlyOffice, Thunderbird, Audacity, GIMP, Blender)
  - public_services (SQLite, vector, graph databases)
  - privacy, performance, UI, logging, experimental, backup

**Required Environment Variables** (from `.env.example`):
- ANTHROPIC_API_KEY (required) - Format: sk-ant-api03-...
- PERPLEXITY_API_KEY (optional)
- OPENAI_API_KEY (optional)
- GOOGLE_API_KEY (optional)
- MISTRAL_API_KEY (optional)
- XAI_API_KEY (optional)
- GROQ_API_KEY (optional)
- OPENROUTER_API_KEY (optional)
- AZURE_OPENAI_API_KEY (optional)
- OLLAMA_API_KEY (optional)
- GITHUB_API_KEY (optional)

**Build/Development:**
- No build process required (Python notebooks run directly)
- Development: `marimo edit orchestr8.py` (hot reload)
- Production: `marimo run orchestr8.py`
- VS Code configuration: `Orchestr8_jr.code-workspace`

## Platform Requirements

**Development:**
- Python 3.12+
- pip package manager
- Local file system access
- Terminal capability for subprocess calls (npm, mypy, ruff detection)

**Production:**
- Marimo runtime environment
- Access to configured external services (optional):
  - Anthropic API endpoint
  - Local LLM servers (Ollama)
  - Neo4j graph database (if enabled)
  - FAISS vector index (if enabled)
- External applications (optional):
  - OnlyOffice, Thunderbird, Audacity, GIMP, Blender (via subprocess)
- File system: `.orchestr8/` directory for state persistence

## Supported Languages (via IP/connection_verifier.py)

**Static Analysis:**
- Python: import statement parsing
- JavaScript/TypeScript: import/require pattern matching
- Relative path resolution
- Package import validation (stdlib vs external vs local)

---

*Stack analysis: 2026-01-30*
