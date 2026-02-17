# Orchestr8 Code City Cutover Checklist

## Objective

Verify seamless transition from Legacy Frame to AnyWidget rendering.

## Pre-Flight

- [x] All P05 Parity Tests Pass.
- [x] Reliability Harness Passes.
- [x] Environment: `ORCHESTR8_RENDER_MODE="WIDGET"` (Default).

## Cutover Steps

1. **Set Mode**: Ensure `ORCHESTR8_RENDER_MODE` is unset or explicitly "WIDGET".
2. **Verify**: Run `pytest tests/city/test_parity.py -vv`.
3. **Launch**: Run `marimo run orchestr8_next/city/notebook.py --headless`.
4. **Confirm**: Check `CodeCityWidget` initializes (Test `test_parity_widget_initialization`).

## Rollback Trigger

- [ ] Render mode fails to initialize.
- [ ] Critical performance degradation (>1s blocking main thread).
- [ ] Data inconsistency between Widget and Contract.

## Evidence

- Attach test output to `CUTOVER_REPORT.md`.
