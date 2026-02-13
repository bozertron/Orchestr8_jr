# Terminal 4: Data Modules — Briefing + Carl + Tickets

Read the shared context first: `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md`

**Files to analyze:**
1. `IP/briefing_generator.py` (180 lines) — context generation for LLM deployments
2. `IP/carl_core.py` (98 lines) — context gatherer (known to be "hollow")
3. `IP/ticket_manager.py` (260 lines) — JFDI ticket system
4. `IP/plugins/components/ticket_panel.py` — TicketPanel UI component
5. `IP/plugins/components/deploy_panel.py` — "House a Digital Native?" deploy modal

Read ALL FIVE completely. Then for each:

1. Every class and method with full signatures
2. What's implemented vs what's stubbed — exact line numbers
3. How it's consumed by 06_maestro.py
4. What "done" looks like for each file

**Specific known issues to investigate:**
- `briefing_generator.load_campaign_log()` — is it a stub? What does it return?
- `carl_core.py` — what does it actually do? Does it just dump JSON?
- `ticket_panel.py` — JFDI button in 06_maestro.py opens a PLACEHOLDER instead of using this. Why? How to fix?
- `deploy_panel.py` — does the deploy workflow actually work end-to-end?

**Write report to:** `.planning/codebase/DATA-MODULES-ANALYSIS.md`
