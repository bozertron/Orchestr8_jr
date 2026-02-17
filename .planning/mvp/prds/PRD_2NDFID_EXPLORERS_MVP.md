# PRD: 2ndFid_explorers Extraction Lane To MVP

## 1. Objective

Produce a continuous stream of clean-room extraction packets that materially accelerate Orchestr8/Code City MVP delivery.

## 2. Problem

High-value patterns exist in 2ndFid, but direct lift is risky and often misaligned with Orchestr8 contracts.

## 3. In Scope

- Line-by-line source analysis.
- Extraction packet authoring with provenance and risk classification.
- Clean-room conversion plans targeted to Orchestr8 contracts.
- Canonical artifact delivery with proof.

## 4. Out of Scope

- Direct code integration into canonical runtime.
- Licensing-risky direct lifts.

## 5. Functional Requirements

1. Deliver packet pairs per active wave (`C*`).
2. Include source path provenance and concept summary.
3. Include Orchestr8 value statement and target contracts.
4. Include risk class + licensing flag.
5. Include integration recommendations for core lane.

## 6. Non-Functional Requirements

1. Consistent packet format for rapid review.
2. High signal-to-noise extraction selection.
3. Actionable conversion detail, not generic summaries.

## 7. Acceptance Criteria

1. Required extraction packet files are in canonical artifacts path.
2. Closeout gate passes for each extraction packet.
3. Canonical lane marks packet `ACCEPTED`.

## 8. Evidence Requirements

- Packet docs in canonical path.
- Copy proof command output.
- Shared memory completion ping.

## 9. Risks and Mitigations

- Risk: extraction outputs too abstract for implementation.
- Mitigation: explicit target contract mapping and integration notes.

- Risk: licensing ambiguity.
- Mitigation: explicit licensing flag + escalation note per packet.

