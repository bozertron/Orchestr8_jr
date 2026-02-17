# Artifact Delivery Contract (Cross-Repo)

Purpose: prevent report/evidence drift across lanes by enforcing canonical destination delivery.

## Canonical Destination

Canonical root:
- `/home/bozertron/Orchestr8_jr`

Artifact destination pattern:
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/`

## Mandatory Fields in Completion Report

1. `source_path` (lane repo)
2. `destination_path` (canonical repo)
3. `copy_command`
4. `verification_output` (`ls -l` or `test -f`)
5. `checksum` (recommended for critical reports)

## Required Delivery Commands

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/
cp <lane_source_file> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/<target_name>
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/<target_name>
```

Optional checksum:

```bash
sha256sum /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/<target_name>
```

## Acceptance Rule

- Canonical lane may reject or delay review if destination evidence is missing.
- Relative paths like `reports/...` are insufficient without canonical delivery proof.
