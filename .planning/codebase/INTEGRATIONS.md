# External Integrations

**Analysis Date:** 2026-01-30

## APIs & External Services

**LLM Providers (Multi-Model Support):**
- Anthropic Claude - Chat and analysis via anthropic SDK
  - SDK/Client: `anthropic` (imported in `IP/plugins/06_maestro.py`)
  - Auth: `ANTHROPIC_API_KEY` (required)
  - Usage: Optional - application continues without it if not installed

- OpenAI GPT - Via OpenRouter or direct
  - Auth: `OPENAI_API_KEY` (optional)

- Google Gemini
  - Auth: `GOOGLE_API_KEY` (optional)

- Mistral AI
  - Auth: `MISTRAL_API_KEY` (optional)

- xAI
  - Auth: `XAI_API_KEY` (optional)

- Groq
  - Auth: `GROQ_API_KEY` (optional)

- Perplexity
  - Auth: `PERPLEXITY_API_KEY` (optional)

- OpenRouter (meta-provider)
  - Auth: `OPENROUTER_API_KEY` (optional)

- Azure OpenAI
  - Auth: `AZURE_OPENAI_API_KEY` (optional)
  - Config: Endpoint in `.taskmaster/config.json`

**Local LLMs:**
- Ollama
  - Auth: `OLLAMA_API_KEY` (optional for remote instances)
  - Connection: Configurable in settings

## Data Storage

**Databases:**
- SQLite (local)
  - Connection: `.orchestr8/public_services.db`
  - Client: sqlite3 (Python standard library) and pandas
  - Purpose: Public services data, backup locations, state persistence
  - Example: `.orchestr8/combat_state.json` for LLM deployment tracking

- Neo4j (optional)
  - Connection: `bolt://localhost:7687` (default)
  - Credentials: `neo4j` user with password from settings
  - Purpose: Graph database for relationship tracking
  - Auto-backup: Enabled via `pyproject_orchestr8_settings.toml`

**Vector Storage:**
- FAISS (optional)
  - Embedding model: Local model configured in settings
  - Dimensions: 1536 (default)
  - Index type: FAISS
  - Similarity threshold: 0.8
  - Purpose: Vector search and semantic similarity

**File Storage:**
- Local filesystem only - No cloud storage integration detected
- State locations:
  - `.orchestr8/combat_state.json` - LLM deployment tracking
  - `.orchestr8/state/` - General state directory
  - `.orchestr8/tickets/` - Ticket system data
  - `.orchestr8/logs/system.log` - Application logs
  - `.orchestr8/backups/` - Local backups
  - `.orchestr8/public_services.db` - SQLite database

**Caching:**
- Model cache: 2048 MB (configurable)
- Preload models: ["document", "embedding"] by default
- Local embedding model: Path configurable in `[local_models.embedding]`

## Authentication & Identity

**Auth Provider:**
- Custom - API key based
  - Implementation: Environment variable injection
  - All external services use API keys from `.env` file
  - No OAuth/SSO integration

**Multi-LLM System:**
- Configuration in `[tools.communic8.multi_llm]`
- Parallel query support across multiple models
- Consolidation modes: "raw", "opinions", "summary"
- Response timeout: 60 seconds
- Models: ["claude", "gpt-4", "gemini"] (configurable)

## Monitoring & Observability

**Error Tracking:**
- None detected - No Sentry, Rollbar, or similar integration

**Logs:**
- Local file-based logging
  - Path: `.orchestr8/logs/system.log`
  - Max file size: 100 MB
  - Backup count: 5 rotations
  - Level: INFO (configurable: DEBUG, WARN, ERROR)
  - Subsystems: agents, tools, integration, escalation logging

**Health Checking:**
- `IP/health_checker.py` - Static analysis and type checking
  - TypeScript support (npm typecheck)
  - Python support (mypy, ruff, py_compile)
  - Results feed into Woven Maps visualization (Blue=broken, Gold=working)

## CI/CD & Deployment

**Hosting:**
- Local development only (no cloud deployment detected)
- Desktop application (Marimo notebook)

**CI Pipeline:**
- None detected - No GitHub Actions, GitLab CI, or similar

**Terminal/Shell Integration:**
- `IP/terminal_spawner.py` - Terminal session management
- Subprocess execution for:
  - Health checkers (npm, mypy, ruff)
  - External applications (OnlyOffice, Blender, GIMP, Audacity, Thunderbird)
  - Git operations (via subprocess)

## External Applications (Subprocess Integration)

**Office Suite:**
- OnlyOffice - Document editing
  - Executable: `/usr/bin/onlyoffice-desktopeditors`
  - Template directory: `~/.orchestr8/templates/onlyoffice`
  - Supported formats: .docx, .xlsx, .pptx
  - Auto-launch: Enabled

**Communications:**
- Thunderbird - Email client
  - Executable: `/usr/bin/thunderbird`
  - Profile path: `~/.thunderbird`
  - Contact integration: Enabled
  - Auto-sync: Enabled

**Audio:**
- Audacity - Audio editing
  - Executable: `/usr/bin/audacity`
  - Project directory: `~/.orchestr8/projects/audio`
  - Auto-export format: WAV

**Graphics:**
- GIMP - Image editing
  - Executable: `/usr/bin/gimp`
  - Plugin directory: `~/.orchestr8/plugins/gimp`
  - Auto-save format: PNG

**3D/Video:**
- Blender - 3D modeling and video editing
  - Executable: `/usr/bin/blender`
  - Project directory: `~/.orchestr8/projects/3d`
  - Python scripts path: `~/.orchestr8/scripts/blender`

## Code Analysis Integrations

**Import Verification:**
- `IP/connection_verifier.py` - Validates Python, JavaScript, TypeScript imports
  - Handles relative imports, package imports, circular dependencies
  - Maps to Woven Maps visualization colors

**Type Checking:**
- TypeScript: npm typecheck
- Python: mypy, ruff, py_compile
- Auto-detection of available checkers

**GitHub Integration:**
- GitHub API support for import/export
  - Auth: `GITHUB_API_KEY` (optional)

## Environment Configuration

**Required env vars:**
- ANTHROPIC_API_KEY - Mandatory for AI features

**Optional env vars:**
- LLM_PROVIDER_API_KEYs (OpenAI, Google, Mistral, xAI, Groq, Perplexity, OpenRouter, Azure)
- OLLAMA_API_KEY (for remote Ollama)
- GITHUB_API_KEY (for Git integration)

**Secrets location:**
- `.env` file at project root (per `.env.example`)
- `.taskmaster/config.json` - Azure endpoint configuration
- Settings file: `pyproject_orchestr8_settings.toml` (contains placeholders for secrets)

**Placeholder Secrets in Config:**
- `[neo4j_password]` - Neo4j authentication
- `[local_doc_model]`, `[local_image_model]`, etc. - Model paths
- `[APIlikethis]` - Barbara/custom model endpoints

## Webhooks & Callbacks

**Incoming:**
- None detected

**Outgoing:**
- None detected

## Privacy & Data Handling

**Privacy Controls (from settings):**
- Senses (multimodal input):
  - Explicit consent required
  - Capture indicator shown
  - No recording retention
  - Encryption enabled
  - Data retention: 0 days

- Communications:
  - P2P encryption
  - Message logging: Disabled
  - Contact sharing: Disabled
  - Query anonymization: Enabled

**Backup & Recovery:**
- Enabled: Automatic backups
- Interval: 6 hours
- Compression: Yes
- Encryption: Yes
- Retention: 30 days
- Locations:
  - Primary: `~/.orchestr8/backups/`
  - Secondary: `[external_drive_path]/orchestr8_backups/` (optional)
  - Cloud backup: Disabled

---

*Integration audit: 2026-01-30*
