# INTERNAL_TASKS_BEFORE_IP.md Integration Guide

- Source: `one integration at a time/docs/INTERNAL_TASKS_BEFORE_IP.md`
- Total lines: `426`
- SHA256: `a3e29114e89420f226886f010387058df8ec3e8da3ff7149601f5bb279211ec9`
- Memory chunks: `4`
- Observation IDs: `443..446`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.

## Anchor Lines

- `one integration at a time/docs/INTERNAL_TASKS_BEFORE_IP.md:56` **Goal:** Create the `.orchestr8/` structure that everything else depends on
- `one integration at a time/docs/INTERNAL_TASKS_BEFORE_IP.md:60` ├── .orchestr8/tickets/
- `one integration at a time/docs/INTERNAL_TASKS_BEFORE_IP.md:61` ├── .orchestr8/tickets/archive/
- `one integration at a time/docs/INTERNAL_TASKS_BEFORE_IP.md:62` ├── .orchestr8/state/
- `one integration at a time/docs/INTERNAL_TASKS_BEFORE_IP.md:78` ├── Create IP/styles/orchestr8.css
- `one integration at a time/docs/INTERNAL_TASKS_BEFORE_IP.md:127` └── Cache to .orchestr8/mermaid-cache.md
- `one integration at a time/docs/INTERNAL_TASKS_BEFORE_IP.md:142` ├── Add [🔄 REFRESH] button to maestro
- `one integration at a time/docs/INTERNAL_TASKS_BEFORE_IP.md:161` ├── [Files][Matrix][Graph]═══[maestro]═══[Search][Deploy][⏎]
- `one integration at a time/docs/INTERNAL_TASKS_BEFORE_IP.md:180` ├── Read .orchestr8/tickets/*.md
- `one integration at a time/docs/INTERNAL_TASKS_BEFORE_IP.md:412` - [ ] `.orchestr8/` structure exists with sample data

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
