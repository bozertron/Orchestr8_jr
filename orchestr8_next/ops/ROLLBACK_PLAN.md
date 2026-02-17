# Orchestr8 Code City Rollback Plan

## Purpose

Procedure to revert Code City visualization to legacy iframe if AnyWidget fails.

## Trigger Criteria

- `test_parity_widget_initialization` FAILURE.
- Runtime Javascript Error in Widget.
- User reported black screen / missing WebGL context.

## Rollback Procedure

1. **Stop**: Terminate running Marimo session.
2. **Set Environment**: `export ORCHESTR8_RENDER_MODE="IFRAME"`.
3. **Verify**: Run `pytest tests/city/test_parity.py -vv` (Focus on `test_parity_iframe_serialization`).
4. **Launch**: Run `marimo run orchestr8_next/city/notebook.py --headless`.
5. **Confirm**: Check HTML/Three.js legacy path loads.

## Post-Rollback

- Log incident in `artifacts/P06/ROLLBACK_REPORT.md`.
- Determine RC for AnyWidget failure before next attempt.

## Evidence

- Attach successful iframe parity test output.
