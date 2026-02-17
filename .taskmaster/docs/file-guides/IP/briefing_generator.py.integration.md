# briefing_generator.py Integration Guide

- Source: `IP/briefing_generator.py`
- Total lines: `248`
- SHA256: `71a90f00c0eb0077f48fdf482377cf0321067cf81475ebf7c1babbf4d6f9558d`
- Role: **Mission briefing compiler** — merges ticket context, campaign history, lock state, and Mermaid topology into deploy-ready briefings

## Why This Is Painful

- Pulls context from multiple stores (`.orchestr8/campaigns`, Louis locks, Carl context).
- Briefing output is user-facing and must stay policy/canon aligned.
- Diagram generation must gracefully degrade when connection context is sparse.

## Anchor Lines

- `IP/briefing_generator.py:14` `load_campaign_log(...)` JSON campaign loader
- `IP/briefing_generator.py:69` `build_fiefdom_diagram(...)`
- `IP/briefing_generator.py:106` `generate(...)`
- `IP/briefing_generator.py:174` Mermaid block embed in briefing body
- `IP/briefing_generator.py:229` checklist references `.orchestr8/campaigns/*.json`

## Integration Use

- Campaign history now reads structured JSON entries from `.orchestr8/campaigns/`.
- Mermaid topology is embedded in every generated briefing (fallback diagram when no graph context).
- Checklist language now points to campaign JSON flow, not deprecated `CAMPAIGN_LOG.md`.

## Open Gaps

- [ ] Campaign entry schema is flexible; no strict validation contract yet

