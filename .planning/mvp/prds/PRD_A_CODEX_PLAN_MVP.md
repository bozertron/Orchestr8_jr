# PRD: a_codex_plan Core Integration To MVP

## 1. Objective

Deliver marimo-first core services and capability integrations that pass canonical replay and converge into MVP runtime.

## 2. Problem

Value-add features exist in multiple forms, but need deterministic integration into a stable core runtime without UI coupling drift.

## 3. In Scope

- Core service modules under `orchestr8_next`.
- Capability packet implementations from approved extraction and settlement outputs.
- Integration test suites and smoke reports.
- Canonical artifact delivery with proof.

## 4. Out of Scope

- Final canonical visual placement decisions.
- Packaging/compliance before core-complete approval.

## 5. Functional Requirements

1. Implement approved packet scopes exactly as bounded.
2. Add/maintain integration tests for each packet slice.
3. Keep compatibility with marimo-first runtime expectations.
4. Deliver all outputs to canonical artifact destination.
5. Provide exact command/pass evidence on completion.

## 6. Non-Functional Requirements

1. Clear module boundaries and contract compliance.
2. Deterministic test behavior.
3. No direct dependency on deprecated or non-approved paths.

## 7. Integration Requirements

1. Consume approved C-lane extraction packets only.
2. Align with settlement transfer specs and acceptance matrix.
3. Preserve existing accepted functionality during new integration.

## 8. Acceptance Criteria

1. Packet-required files exist and lint/closeout gates pass.
2. Packet test suites pass in lane and canonical replay.
3. Canonical lane marks packet `ACCEPTED`.

## 9. Evidence Requirements

- Implementation file list.
- Test command output with pass counts.
- Canonical artifact copy + `ls -l` proof.

## 10. Risks and Mitigations

- Risk: implementation outruns spec clarity.
- Mitigation: settlement hook/matrix alignment before coding.

- Risk: regression from rapid packet execution.
- Mitigation: packet-level integration tests + replay gate.

