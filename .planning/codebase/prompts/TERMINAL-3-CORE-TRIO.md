# Terminal 3: Core Trio — Connection + Health + Combat

Long-run mode: read `/home/bozertron/Orchestr8_jr/README.AGENTS`, `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`, and `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` before executing this prompt.


Read the shared context first: `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md`

These 3 modules feed data into Code City node colors. They're the data pipeline.

**Files to analyze:**
1. `IP/connection_verifier.py` (902 lines) — builds import graph = Code City edges
2. `IP/health_checker.py` (601 lines) — determines node colors (Gold/Teal)
3. `IP/combat_tracker.py` (114 lines) — tracks LLM deployments (Purple)

Read ALL THREE completely. Then for each:

1. Every class and method with signatures and return types
2. Data structures: What format does output take? Dicts, lists, dataclasses?
3. Integration surface: How does 06_maestro.py or woven_maps.py consume this?
4. Is it actually called? By what? Are results used?
5. Stubs/incomplete: Any TODO, placeholder returns, pass statements
6. External dependencies (networkx? subprocess?)
7. What data woven_maps.py NEEDS vs what's available
8. Config: Does it read from orchestr8_settings.toml?

**Critical question:** Health data is supposed to color Code City nodes. Trace the FULL pipeline: health_checker → ??? → woven_maps node colors. Where does it break?

**Write report to:** `.planning/codebase/CORE-TRIO-ANALYSIS.md`


