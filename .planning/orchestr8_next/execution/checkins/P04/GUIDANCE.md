# Guidance Log

Use this file for architect guidance drops and clarifications.

## Entry Template
- Date:
- Author:
- Context:
- Guidance:
- Impacted Files:
- Required Follow-up:

- Date: 2026-02-14 12:42:30
- Author: Codex
- Context: Founder requested cross-agent alignment after P04 backend completion report.
- Guidance:
  - P04 backend report is accepted in principle; keep strict contracts and bridge validation as the canonical pattern.
  - For headless execution, run:
    - `marimo run orchestr8_next/city/notebook.py --host 0.0.0.0 --port 2718 --headless --watch --no-token`
  - Provide startup log + one connectivity proof (`curl -I http://127.0.0.1:2718/` from container) in next STATUS update.
  - `GUIDANCE.md` is a file to read and append to, not create elsewhere:
    - `.planning/orchestr8_next/execution/checkins/P04/GUIDANCE.md`
    - When starting P05 packet, also use `.planning/orchestr8_next/execution/checkins/P05/GUIDANCE.md`.
  - For P05 AnyWidget pivot, keep one operational fallback path:
    - AnyWidget as primary runtime channel
    - Existing iframe bridge preserved behind a feature flag for rollback
  - Do not introduce runtime dependency on `marimo new` codegen path.
- Impacted Files:
  - `.planning/orchestr8_next/execution/checkins/P04/STATUS.md`
  - `.planning/orchestr8_next/execution/checkins/P04/BLOCKERS.md`
  - `.planning/orchestr8_next/execution/checkins/P05/STATUS.md`
  - `orchestr8_next/city/notebook.py`
- Required Follow-up:
  - Post timestamped acknowledgment in `P04/STATUS.md` with gate color and next three actions.
  - Include P05 kickoff plan with explicit fallback and rollback criteria.
