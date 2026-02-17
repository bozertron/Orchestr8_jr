You are the execution agent for `or8_founder_console`.

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

1. Read `README.AGENTS`, `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`, and `.planning/orchestr8_next/execution/LONG_RUN_MODE.md` from Orchestr8_jr.
2. Send checkout to codex with `requires_ack=true`:
`/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=<packet_id>; scope=<scope>; files=<files>; tests=<tests>; eta=<eta>"`
3. Execute only the packet specified by your launch prompt + active boundary.
4. Produce:
- `artifacts/<PACKET_REPORT>.md`
- command outputs + pass counts
- canonical delivery proof into `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/`
5. Send completion ping and idle.
