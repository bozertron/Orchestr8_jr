# Specification: Migration Assistant Parser Plugin

**Plugin Name:** `migrationAssistant` (tentative)
**File Name:** `migrationAssistantParser.ts` (source), `migrationAssistantParser.js` (compiled)

## 1. Purpose

To analyze the combined results from the `integr8` command (or potentially individual parser runs) for a specific target page/component from an external project and compare it against the current project's state. The goal is to explicitly identify potential integration challenges ("Problems") and existing compatible elements ("Provisions") within the current project, providing a clear roadmap for migration.

This plugin aims to bridge the gap between raw analysis data and actionable integration steps, significantly aiding developers (human or LLM) in the migration process.

## 2. Core Functionality (`analyzeDataFunction`)

**Input:**

*   `targetPath`: Absolute path to the *current* project root (for context).
*   `options`: An object containing the necessary data, likely passed from `integr8` or a dedicated command. This **must** include:
    *   `externalAnalysisData`: The structured analysis results for the *external* project (containing overview, stores, routes, types, ui, commands data).
    *   `currentAnalysisData`: The structured analysis results for the *current* project (same structure as above).
    *   `targetPageContent`: The source code of the specific target page/component being integrated.
    *   `targetPageRelativePath`: The relative path of the target page within the external project (for context).
    *   *(Optional)* Configuration flags to fine-tune the analysis (e.g., strictness level for conflicts).

**Processing:**

1.  **Dependency Analysis:**
    *   Parse the `targetPageContent` (likely using `@vue/compiler-sfc` and `@babel/parser` for the script block) to identify its direct imports (stores, components, utils, types).
    *   Compare these imports against the `currentAnalysisData`:
        *   **Problem:** Identify imports that have no corresponding export/definition found in the current project's analysis (missing stores, components, utils, types).
        *   **Problem:** Identify potential version conflicts if dependency versions are available in `overview` data for both projects.
        *   **Provision:** List imports that *do* have a match in the current project.
2.  **Store Integration Analysis:**
    *   Identify stores used by the `targetPageContent` (via imports).
    *   Compare the state keys, getters, and actions of these required stores (from `externalAnalysisData.stores`) with the corresponding stores in the `currentAnalysisData.stores`.
        *   **Problem:** Conflicting state/getter/action names with potentially different signatures or purposes.
        *   **Problem:** Missing state/getter/action required by the target page in the current project's store.
        *   **Provision:** Matching stores and their compatible members.
3.  **Route Integration Analysis:**
    *   Identify any child routes defined within the `targetPageContent` (if it's a layout or view component) or routes it navigates to programmatically.
    *   Compare required route names/paths against `currentAnalysisData.routes`.
        *   **Problem:** Route name/path conflicts.
        *   **Problem:** Routes the target page expects to navigate to that don't exist in the current project.
        *   **Provision:** Existing routes that match expectations.
4.  **Command Integration Analysis:**
    *   Parse `targetPageContent` for Tauri `invoke()` calls.
    *   Compare invoked command names against `currentAnalysisData.commands`.
        *   **Problem:** Commands invoked by the target page that are not declared in the current project's backend.
        *   **Provision:** Commands that exist in the current project.
5.  **UI Component Analysis:**
    *   Parse the template of `targetPageContent` (potentially using regex or a dedicated template parser if available) for UI component tags (e.g., `<n-button>`, `<v-text-field>`).
    *   Compare identified UI libraries/components against `currentAnalysisData.ui` (or `ui-template`).
        *   **Problem:** Usage of UI components from a library not present or configured in the current project.
        *   **Provision:** Usage of UI components that are available in the current project.
6.  **Type Compatibility Analysis:**
    *   Identify custom types imported/used by `targetPageContent`.
    *   Compare these against `currentAnalysisData.types`.
        *   **Problem:** Missing type definitions in the current project.
        *   **Problem:** Potential conflicts if types with the same name exist but have different structures (basic check, deep comparison might be too complex initially).
        *   **Provision:** Existing compatible types.

**Output (`AnalysisResult<MigrationAnalysisData>`):**

*   `success: true`
*   `data`: An object (`MigrationAnalysisData`) containing structured lists:
    *   `targetPageRelativePath`: string
    *   `problems`: Array of objects detailing issues (e.g., `{ type: 'MissingDependency', name: 'useExternalStore', details: 'Store not found in current project' }`, `{ type: 'CommandConflict', name: 'save_data', details: 'Command exists but signature might differ' }`).
    *   `provisions`: Array of objects detailing compatible elements (e.g., `{ type: 'StoreMatch', name: 'useCommonStore', details: 'Store ID matches' }`, `{ type: 'ExistingRoute', path: '/profile' }`).
    *   `recommendations`: (Optional) High-level suggested actions (e.g., "Install missing dependency X", "Resolve conflict in store Y", "Create new command Z").
*   OR `success: false`, `error: string`

## 3. Report Formatting (`formatReportFunction`)

**Input:** `MigrationAnalysisData`

**Processing:**

*   Format the `problems` and `provisions` lists into a human-readable Markdown report.
*   Group issues by category (Dependencies, Stores, Routes, Commands, UI, Types).
*   Clearly state the target page being analyzed.
*   Include any high-level recommendations.

**Output:** A formatted string (Markdown recommended).

## 4. CLI Integration (`saveScaffoldReport.ts`)

*   **Command Type:** `migrationAssistant`
*   **Description:** "Analyzes integration requirements for an external component/page against the current project."
*   **Supports Compare:** `false` (Comparison is inherent in its input data).
*   **Specific Options:** Define options to pass the required `externalAnalysisData`, `currentAnalysisData`, `targetPageContent`, and `targetPageRelativePath`. This likely means the `migrationAssistant` command wouldn't be run directly by the user but orchestrated by `integr8` or a future dedicated command that gathers the necessary inputs first. Alternatively, it could accept file paths to previously generated JSON reports from the `scaffold --json` command.

## 5. UI Integration (Conceptual)

*   A new button/action within the Orchestr8 UI, possibly enabled after running `integr8`.
*   When triggered, it would execute the `migrationAssistant` command/plugin, passing the relevant data from the `integr8` run for the selected target page.
*   Display the formatted report to the user.

## 6. Future Enhancements

*   Deeper type comparison.
*   Analysis of CSS/styling conflicts.
*   Suggestions for code modifications.
*   Configuration options for analysis strictness.
