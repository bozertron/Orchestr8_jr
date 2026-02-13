# gi8.md Integration Guide

- Source: `one integration at a time/Staging/Connection - Files/gi8.md`
- Total lines: `1566`
- SHA256: `f710d8113c05c9941c2e789f83f44b3bbb4e08626b64ebf31dfdfa3e7da1136f`
- Memory chunks: `14`
- Observation IDs: `745..758`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Constraint-heavy document: treat as canonical rules, not optional guidance.
- Behavioral sequencing risk: mode transitions need explicit state machine handling.

## Anchor Lines

- `one integration at a time/Staging/Connection - Files/gi8.md:176` The Orchestr8 platform primarily utilizes **SQLite** for its backend data storage. The schema definitions are located in `src-tauri/src/database/schema.rs` within the `initialize_database_tables` function. This function creates tables in the main application database (`scaffolder_data.sqlite`). Additionally, a separate SQLite database (`history.sqlite`) is created for each LLM entity to store its interaction history, managed by `initialize_entity_history_db`.
- `one integration at a time/Staging/Connection - Files/gi8.md:180` The following `CREATE TABLE` statements are sourced directly from `src-tauri/src/database/schema.rs`:
- `one integration at a time/Staging/Connection - Files/gi8.md:219` *   *Note on Foreign Key:* The `llm_entity_id` is an `INTEGER`. The original DDL in `schema.rs` has `FOREIGN KEY (llm_entity_id) REFERENCES LLM_Entities(entity_id)`. However, the `LlmEntities` table's primary key is `id TEXT`. This suggests a potential mismatch or that `llm_entity_id` in `Integr8_Engineers` should ideally reference an integer primary key in `LlmEntities` if one existed, or `llm_entity_id` itself should be `TEXT` to match `LlmEntities.id`. Given `Integr8Engineer.llm_entity_id` is `number` in `integr8Store.ts`, it's likely intended to be an integer. This might imply `LlmEntities.id` is *also* an integer in some contexts or there's an implicit conversion/lookup. For this report, the corrected FK references `LlmEntities(id)` assuming `llm_entity_id` stores a string that matches `LlmEntities.id` or there's an underlying integer PK in `LlmEntities` that is not explicitly shown but implied by the `INTEGER` type here. The `llmStore.ts` uses string IDs for `LlmEntityConfig.id`. This area might require further clarification in the actual DB implementation vs. DDL.
- `one integration at a time/Staging/Connection - Files/gi8.md:253` These definitions from `schema.rs` provide the ground truth for these tables.
- `one integration at a time/Staging/Connection - Files/gi8.md:257` *   Based on the review of `schema.rs` and `interactions.rs`, Orchestr8 primarily uses **SQLite**.
- `one integration at a time/Staging/Connection - Files/gi8.md:258` *   `schema.rs` details the main application database (`scaffolder_data.sqlite`) and also mentions a separate `history.sqlite` created per LLM entity for interaction logs. No other database systems (e.g., PostgreSQL, MongoDB) are indicated in these core database files.
- `one integration at a time/Staging/Connection - Files/gi8.md:350` *   `GraphViewState`: For saving and restoring the visual state of the graph (layout, zoom, pan, selection, filters).
- `one integration at a time/Staging/Connection - Files/gi8.md:376` *   **`src/lib/maestro_security.ts`**: This file implements secure key storage using `@tauri-apps/plugin-stronghold`.
- `one integration at a time/Staging/Connection - Files/gi8.md:379` *   `initializeStronghold()`: Sets up the Stronghold vault (`maestro-vault.hold`) and client. It uses a hardcoded password (`maestro-secure-password`) for the vault, noting that a more secure approach should be considered for production.
- `one integration at a time/Staging/Connection - Files/gi8.md:382` *   **Usage**: This service is likely used by `llmStore.ts` or similar stores/services when saving LLM configurations that include API keys. Instead of storing the raw API key, the `keyId` returned by `encryptKey` would be stored in the database (e.g., in the `LlmEntities.api_key` field, which was noted in the schema as potentially storing a placeholder or reference). When an API call needs to be made, the `keyId` is used to `decryptKey` to retrieve the actual API key just-in-time.
- `one integration at a time/Staging/Connection - Files/gi8.md:383` *   **Limitations for Auth**: This service focuses on credential/secret management. It does not appear to handle user authentication (login sessions, user identity) or role-based authorization within the application itself. Those aspects might be managed by other systems or are simpler in the current architecture (e.g., relying on local user context without explicit login, or user roles defined in a database table like `Users` or `UserProfiles` if they exist). The `UserProfiles` table in `schema.rs` suggests user identity management, but the direct link to authentication flow isn't clear from `maestro_security.ts` alone.
- `one integration at a time/Staging/Connection - Files/gi8.md:455` *   **View State Persistence**: Placeholder logic for saving/loading graph view state (zoom, pan, layout), possibly via `localStorage`.
- `one integration at a time/Staging/Connection - Files/gi8.md:471` *   **Purpose**: This component is **not a generic code editor** for arbitrary file types. It serves as a dynamic, schema-driven editor for "Product Requirements Documents" (PRDs). PRDs appear to be structured data where fields are defined by a `_schema` object, specifying field types (Text, Long Text, Number, Boolean, Date), labels, etc.
- `one integration at a time/Staging/Connection - Files/gi8.md:472` *   **Technology**: It dynamically renders Naive UI input components (`NInput`, `NInputNumber`, `NSwitch`, `NDatePicker`, `NTextarea`) based on the field types defined in the PRD's schema. It does **not** use Monaco Editor, CodeMirror, or similar code editing libraries.
- `one integration at a time/Staging/Connection - Files/gi8.md:475` *   Allows editing of existing PRD fields based on their schema-defined type.
- `one integration at a time/Staging/Connection - Files/gi8.md:476` *   Supports adding new fields to the PRD schema (via an `AddFieldForm.vue` child component).
- `one integration at a time/Staging/Connection - Files/gi8.md:531` *   `NButton`, `NButtonGroup`: Used extensively for actions, often with icons (`NIcon`). Examples include zoom controls, save, cancel, refresh, export, etc.
- `one integration at a time/Staging/Connection - Files/gi8.md:717` *   `activeTopLeftComponent`, `activeTopRightComponent`, `activeTopMiddleComponent`: Strings indicating which dynamic Vue component should be rendered in these respective panel areas.
- `one integration at a time/Staging/Connection - Files/gi8.md:855` Tauri commands in Orchestr8 form the bridge between the Rust backend and the Vue.js frontend, enabling frontend components and Pinia stores to invoke Rust functions and receive results. The architecture is characterized by modularity, standardized error handling, and clear data modeling.
- `one integration at a time/Staging/Connection - Files/gi8.md:863` *   Some commands might also reside in other top-level modules like `src-tauri/src/maestro_modules/` (e.g., `seeg_engine.rs`).
- `one integration at a time/Staging/Connection - Files/gi8.md:958` *   `start_seeg_execution(initial_step_id: String) -> CommandResult<String>` (from `maestro_modules::seeg_engine.rs`)
- `one integration at a time/Staging/Connection - Files/gi8.md:975` *   **Workflow Management** (from `maestro_workflow.rs`):
- `one integration at a time/Staging/Connection - Files/gi8.md:1037` *   Each plugin must export an `analyzeDataFunction(projectPath, options): Promise<AnalysisResult<any>>`.
- `one integration at a time/Staging/Connection - Files/gi8.md:1362` *   **Purpose**: This script is **not an analyzer** but a **generator** of boilerplate code for a new Tauri backend (equivalent to `src-tauri`). It creates the directory structure and core files like `Cargo.toml`, `src/main.rs`, `src/database/schema.rs`, and `tauri.conf.json`.
- `one integration at a time/Staging/Connection - Files/gi8.md:1369` *   Sets up `tauri-plugin-sql` (preloading `maestro-scaffolder.sqlite`) and `tauri-plugin-log`.

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
