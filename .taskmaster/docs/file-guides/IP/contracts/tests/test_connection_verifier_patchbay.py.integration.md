# test_connection_verifier_patchbay.py Integration Guide

- Source: `IP/contracts/tests/test_connection_verifier_patchbay.py`
- Total lines: `153`
- SHA256: `ff64e694fc349c2e394c34a7b36281b1c1231787b6078ad193b6719f75a6dc74`
- Role: **Patchbay validator/apply tests** — covers dry-run success/fail and guarded apply behaviors

## Why This Is Painful

- Apply safety depends on strict negative-case tests, not only happy paths.
- Cross-language rewrite behavior must stay deterministic.

## Anchor Lines

- `IP/contracts/tests/test_connection_verifier_patchbay.py:13` dry-run Python success
- `IP/contracts/tests/test_connection_verifier_patchbay.py:80` dry-run JavaScript success
- `IP/contracts/tests/test_connection_verifier_patchbay.py:98` apply Python success
- `IP/contracts/tests/test_connection_verifier_patchbay.py:118` apply JavaScript success
- `IP/contracts/tests/test_connection_verifier_patchbay.py:137` apply blocked when dry-run fails (no file mutation)

## Integration Use

- Keep this file green before changing patchbay rewrite or rollback logic.
