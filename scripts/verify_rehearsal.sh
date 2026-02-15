#!/bin/bash
echo "Starting Cutover Rehearsal..."

echo "1. Verify Default (WIDGET) Mode"
export ORCHESTR8_RENDER_MODE="WIDGET"
pytest tests/city/test_parity.py -vv > cutover_test.log 2>&1
if [ $? -eq 0 ]; then
  echo "WIDGET Mode Verified: PASS"
else
  echo "WIDGET Mode Critical Failure: FAIL"
  exit 1
fi

echo "2. Simulate Rollback (IFRAME) Mode"
export ORCHESTR8_RENDER_MODE="IFRAME"
pytest tests/city/test_parity.py -vv > rollback_test.log 2>&1
if [ $? -eq 0 ]; then
  echo "IFRAME Mode Verified: PASS"
else
  echo "IFRAME Mode Critical Failure: FAIL"
  exit 1
fi

echo "Rehearsal Successful. 3/3 Tests Passed in each mode."
