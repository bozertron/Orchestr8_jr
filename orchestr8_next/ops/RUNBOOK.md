# Orchestr8 Code City Runbook (P06-WP03)

## Operational Procedures

### **Visualization (Code City)**

- **Startup**: `marimo run orchestr8_next/city/notebook.py`
- **Configuration**:
  - `ORCHESTR8_RENDER_MODE`: `WIDGET` (Default) | `IFRAME` (Fallback)

### **Regression Testing**

- Run Reliability Harness: `pytest tests/reliability/test_reliability.py -vv`
- Run Parity Checks: `pytest tests/city/test_parity.py -vv`

### **Incident Response**

- **Widget Crash / Black Screen**:
    1. Check browser console for errors.
    2. Execute Rollback Procedure: `orchestr8_next/ops/ROLLBACK_PLAN.md`
    3. Capture logs and restart in `IFRAME` mode.

### **Cutover Verification**

- See `orchestr8_next/ops/CUTOVER_CHECKLIST.md`

## Status & Monitoring

- Check `artifacts/P06/GATE_REVIEW.md` for latest validation status.
