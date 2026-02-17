# PRD: or8_founder_console To MVP

## 1. Objective

Provide founder-grade operational control over packet execution without requiring terminal-first workflow.

## 2. Problem

Review and decision throughput degrades when packet status, artifacts, guidance, and event history are fragmented.

## 3. In Scope

- Packet and readiness APIs.
- Review queue and decision hooks.
- Founder directives.
- Annotation and timeline endpoints.
- Test coverage proving endpoint behavior.

## 4. Out of Scope

- Replacing canonical check-ins as source of truth.
- Direct manipulation of runtime code in other lanes.

## 5. Functional Requirements

1. Show packet board/readiness summaries.
2. Support approve/rework decision capture.
3. Provide timeline and annotation context for decisions.
4. Preserve traceability to packet IDs and decisions.

## 6. Non-Functional Requirements

1. Endpoint behavior must be deterministic and test-covered.
2. API responses must be suitable for low-friction UI surfaces.
3. Decision auditability must be retained.

## 7. Acceptance Criteria

1. Packet-scoped founder workflows are complete via API.
2. Tests pass for all review, annotation, and timeline paths.
3. Canonical report is delivered and accepted.

## 8. Evidence Requirements

- Test command and pass counts.
- Endpoint manifest in report.
- Canonical artifact copy proof.

## 9. Risks and Mitigations

- Risk: data drift versus canonical check-ins.
- Mitigation: clear adapter contract and regular replay checks.

- Risk: API growth without governance.
- Mitigation: packet-bounded feature increments and acceptance gating.

