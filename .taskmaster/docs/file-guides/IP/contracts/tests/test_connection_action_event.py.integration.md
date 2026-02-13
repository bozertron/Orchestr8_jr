# test_connection_action_event.py Integration Guide

- Source: `IP/contracts/tests/test_connection_action_event.py`
- Total lines: `103`
- SHA256: `434f9a069f01880528193ec0db85c848cc8bf699600b0849d5c5291248495230`
- Role: **Connection action schema tests** — validates dry-run/apply parsing and actor role normalization

## Why This Is Painful

- Write-capable action safety depends on schema test coverage.
- Actor role parsing must stay deterministic for permission checks.

## Anchor Lines

- `IP/contracts/tests/test_connection_action_event.py:12` full payload validation
- `IP/contracts/tests/test_connection_action_event.py:42` apply action + actor role normalization
- `IP/contracts/tests/test_connection_action_event.py:56` missing action failure
- `IP/contracts/tests/test_connection_action_event.py:64` invalid action failure

## Integration Use

- Run before changing action schema or role fields.
