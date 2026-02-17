# Resume Prompt - a_codex_plan (P07-B7)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are executing packet `P07-B7`.

## Packet

- Packet ID: `P07-B7`
- Scope: Core integration packet: SettingsService + Phreak token wiring

## Objective

Ship Phreak/CSE foundation with settings-driven behavior and stable integration tests.

## Preconditions (required)

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread a_codex_plan P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
```

Read:
- `/home/bozertron/Orchestr8_jr/README.AGENTS`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B7_A_CODEX_PLAN.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `/home/bozertron/a_codex_plan/.planning/orchestr8_next/AESTHETIC_STRATEGY.md`
- `/home/bozertron/a_codex_plan/.planning/orchestr8_next/PHREAK_MODE_INTEGRATION_PLAN.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B6_INTEGRATION_SMOKE_REPORT.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send a_codex_plan codex P07 checkout true "packet=P07-B7; scope=settings service + phreak token + integration hardening; files=<files>; tests=<tests>; eta=<eta>"
```

Worklist + lint:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-B7 a_codex_plan
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/prompts/RESUME_POST_B6_A_CODEX_PLAN.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B7_A_CODEX_PLAN.md
```

## Required outputs

- `/home/bozertron/a_codex_plan/orchestr8_next/settings/service.py`
- `/home/bozertron/a_codex_plan/orchestr8_next/settings/schema.py`
- `/home/bozertron/a_codex_plan/orchestr8_next/city/command_surface.py`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B7_INTEGRATION_SMOKE_REPORT.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B7_INTEGRATION_SMOKE_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B7_INTEGRATION_SMOKE_REPORT.md
```

Validation:

```bash
pytest tests/integration/test_temporal_state.py tests/integration/test_city_tour_service.py tests/integration/test_agent_conversation.py -q
pytest tests/integration/test_settings_service.py -q
```
Closeout + ping:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-B7
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-B7 long-run bundle complete; updated TODO + evidence posted"
```
