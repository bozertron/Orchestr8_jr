---
phase: P07-INTEGRATION
plan: 02
type: execute
wave: 1
depends_on: []
files_modified: []
autonomous: true

must_haves:
  truths:
    - "orchestr8_next/ root is free of test artifacts"
    - "Runbook documentation moved to proper location"
    - "No .log files remain in project root"
  artifacts:
    - path: ".planning/orchestr8_next/artifacts/P07/runbooks/"
      provides: "Consolidated location for operational runbooks"
    - path: "rollback_test.log"
      status: "moved to artifacts or deleted"
    - path: "cutover_test.log"
      status: "moved to artifacts or deleted"
  key_links:
    - from: "orchestr8_next/ops/"
      to: ".planning/orchestr8_next/artifacts/P07/runbooks/"
      action: "move markdown files"
---

<objective>
Clean up artifacts in orchestr8_next/ directory and move runbook documentation to proper location.

Purpose: Organize project structure by moving operational documentation to .planning/artifacts/ and ensuring no test outputs/logs remain in root directories.

Output: Clean orchestr8_next/ root, runbooks in .planning/artifacts/P07/runbooks/
</objective>

<execution_context>
@/home/bozertron/.config/opencode/get-shit-done/workflows/execute-plan.md
</execution_context>

<context>
# Current state from research:
- orchestr8_next/ops/ contains 3 markdown runbooks:
  - CUTOVER_CHECKLIST.md
  - ROLLBACK_PLAN.md
  - RUNBOOK.md
- orchestr8_next/ contains subdirectories: city/, ops/, shell/
- No .log files in orchestr8_next/ (but 2 logs at project root)
- resilience/breaker.py mentioned in research but directory not found

# Project root log files (outside orchestr8_next/)

- rollback_test.log
- cutover_test.log
- .planning/overwatch.log (already appropriate location)
</context>

<tasks>

<task type="auto">
  <name>Task 1: Identify artifact files in orchestr8_next/ root</name>
  <files>None</files>
  <action>
    Run ls -la on orchestr8_next/ to catalog all files and subdirectories.
    Check for:
    - Test output files (*.log, *.test, *test_output*)
    - Smoke reports (*smoke*.html, *smoke*.md)
    - Backup files (*.bak, *.backup)
    Document findings for next tasks.
  </action>
  <verify>`ls -la orchestr8_next/` shows only subdirectories (city/, ops/, shell/) and no loose artifact files</verify>
  <done>Complete inventory of orchestr8_next/ root contents documented</done>
</task>

<task type="auto">
  <name>Task 2: Move runbook docs to .planning/artifacts/</name>
  <files>
    - orchestr8_next/ops/CUTOVER_CHECKLIST.md
    - orchestr8_next/ops/ROLLBACK_PLAN.md
    - orchestr8_next/ops/RUNBOOK.md
  </files>
  <action>
    1. Create directory: .planning/orchestr8_next/artifacts/P07/runbooks/
    2. Move all 3 markdown files from orchestr8_next/ops/ to the new runbooks/ directory
    3. Verify move was successful with ls
  </action>
  <verify>All 3 files exist in .planning/orchestr8_next/artifacts/P07/runbooks/ AND are removed from orchestr8_next/ops/</verify>
  <done>3 runbook files moved to proper artifacts location</done>
</task>

<task type="auto">
  <name>Task 3: Clean a_codex_plan root test artifacts</name>
  <files>/home/bozertron/a_codex_plan/</files>
  <action>
    The a_codex_plan root has 37 loose .txt/.md/.log files that should be archived.

    1. Create archive directory:
    ```bash
    mkdir -p /home/bozertron/a_codex_plan/.planning/orchestr8_next/artifacts/P07/test_archives/
    ```

    2. Move test output files (14 files):
    ```bash
    cd /home/bozertron/a_codex_plan
    mv ACP_03_TEST_OUTPUT.txt ALL_B5_TESTS.txt B3_TEST_OUTPUT.txt B4_TEST_OUTPUT.txt \
       B5_TEST_OUTPUT.txt B6_FINAL_TESTS.txt B6_TEST_OUTPUT.txt TEST_CS_FAIL.txt \
       TEST_OUTPUT_B2.txt test_binary_output.txt test_graphs_output.txt \
       test_output.txt test_output_2.txt test_output_rel.txt \
       test_reliability_output.txt test_wiring_output.txt \
       .planning/orchestr8_next/artifacts/P07/test_archives/
    ```

    3. Move smoke reports (6 files):
    ```bash
    mv B1_INTEGRATION_SMOKE_REPORT.md B2_INTEGRATION_SMOKE_REPORT.md \
       B3_INTEGRATION_SMOKE_REPORT.md B4_INTEGRATION_SMOKE_REPORT.md \
       B5_INTEGRATION_SMOKE_REPORT.md B6_INTEGRATION_SMOKE_REPORT.md \
       .planning/orchestr8_next/artifacts/P07/test_archives/
    ```

    4. Move log files (6 files):
    ```bash
    mv curl_proof.log cutover_test.log marimo_startup.log marimo_startup_retry.log \
       rollback_test.log smoke_city.txt smoke_reliability.txt \
       .planning/orchestr8_next/artifacts/P07/test_archives/
    ```

    5. Move misc artifacts:
    ```bash
    mv inbox_dump.txt obs_1664.txt ping_completion_output.txt \
       .planning/orchestr8_next/artifacts/P07/test_archives/
    ```

    DO NOT move: pyproject.toml, pytest.ini, requirements.txt, .coverage
    (these are project config)
  </action>
  <verify>
    ls /home/bozertron/a_codex_plan/*.txt /home/bozertron/a_codex_plan/*.log 2>/dev/null | wc -l
    # Should return 0 (no loose artifacts in root)
    ls /home/bozertron/a_codex_plan/.planning/orchestr8_next/artifacts/P07/test_archives/ | wc -l
    # Should return 30+ files
  </verify>
  <done>All test artifacts, smoke reports, and logs moved to test_archives/. Root contains only project config files.</done>
</task>

</tasks>

<verification>
- [ ] orchestr8_next/ root contains only code directories (city/, shell/, optionally ops/ if empty)
- [ ] 3 runbook files exist in .planning/orchestr8_next/artifacts/P07/runbooks/
- [ ] No .log files in project root
- [ ] No test output files in project root
</verification>

<success_criteria>

1. orchestr8_next/ops/ markdown files moved to .planning/artifacts/P07/runbooks/
2. Project root has no loose .log files
3. Test output artifacts identified and cleaned
4. Runbook directory structure established for P07
</success_criteria>

<output>
After completion, create `.planning/orchestr8_next/artifacts/P07/plans/P07-PHASE1-SUMMARY.md`
</output>
