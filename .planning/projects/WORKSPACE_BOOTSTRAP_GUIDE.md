# Workspace Bootstrap Guide

These blueprints are intentionally in-repo only. Create external workspaces manually, then copy this structure.

## 1) Founder Console Workspace

Suggested workspace name:
- `or8_founder_console`

Suggested bootstrap:

```bash
mkdir -p ~/or8_founder_console/{app,backend,contracts,prompts,work_packets,docs,tests}
```

Copy-in sources from this repo:
- `.planning/projects/or8_founder_console/*`
- `scripts/agent_comms.sh`
- `scripts/agent_flags.sh`

## 2) Mingos Settlement Lab Workspace

Suggested workspace name:
- `mingos_settlement_lab`

Suggested bootstrap:

```bash
mkdir -p ~/mingos_settlement_lab/{corpus,synthesis,transfer,prompts,docs,work_packets,artifacts}
```

Copy-in sources from this repo:
- `.planning/projects/mingos_settlement_lab/*`
- `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`

## 3) Startup Rule

In each new workspace, first run prompt preflight from `README.AGENTS` + `HARD_REQUIREMENTS.md` + `LONG_RUN_MODE.md` before any packet work.
