# DAC-O_rust_migration.md Integration Guide

- Source: `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md`
- Total lines: `161`
- SHA256: `2910e729a59d1916bddf848f5432ffa55d7cd94b8544f1c800f8688643659651`
- Memory chunks: `2`
- Observation IDs: `730..731`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:3` This document tracks the progress and plan for migrating Rust code from the DAC-O project into the orchestr8 project's Tauri backend (`src-tauri`).
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:8` * The monolithic `orchestr8/src-tauri/src/main.rs` file was refactored into a modular structure.
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:15` * `llm_chat_commands.rs`: (Renamed from `chat_commands.rs`) Holds existing orchestr8 commands for LLM interaction (`send_message`, `fetch_history`, etc.).
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:25` * All structs from the DAC-O `src/models/` directory (`chat.rs`, `config.rs`, `daco.rs`, `user.rs`) were migrated into `orchestr8/src-tauri/src/models.rs`.
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:26` * `sqlx`-specific attributes (`FromRow`, `#[sqlx(...)]`) were removed as orchestr8 uses `rusqlite`.
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:30` * Commands related to signaling (`signal_join`, `signal_leave`, `signal_send`, `signal_get_clients`) from `DAC-O/src/commands/chat_commands.rs` were moved into a new file: `orchestr8/src-tauri/src/commands/signal_chat_commands.rs`.
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:31` * Placeholders and TODO comments were added for dependencies on DAC-O state (`AppState`, `signaling_clients`) and types (`ClientInfo`, `ClientSignal`) that still need migration/definition within orchestr8.
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:36` * Used PowerShell to copy the remaining DAC-O Rust modules/files into the `orchestr8/src-tauri/src` structure:
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:37` * `C:\DAC-O\src-tauri\src\commands\db_commands.rs` -> `c:\orchestr8\src-tauri\src\commands\db_commands.rs`
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:38` * `C:\DAC-O\src-tauri\src\webrtc\` -> `c:\orchestr8\src-tauri\src\webrtc\` (recursive)
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:39` * `C:\DAC-O\src-tauri\src\ws\` -> `c:\orchestr8\src-tauri\src\ws\` (recursive)
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:40` * `C:\DAC-O\src-tauri\src\scaffold\` -> `c:\orchestr8\src-tauri\src\scaffold\` (recursive)
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:45` The following modules and files have been copied from DAC-O into the `orchestr8` project structure. They require refactoring for Tauri v2.5 compliance, integration with orchestr8's state/error handling, and eventual activation in `main.rs`.
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:62` * **Action:** No direct code migration needed. Focus on ensuring `orchestr8/src-tauri/src/database/schema.rs` supports tables needed by `db_commands.rs` and migrated models.
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:71` * **Status:** Copied to `orchestr8/src-tauri/src/webrtc/`. **Structurally Refactored (Phase 5). Core Logic Deferred.**
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:76` * **Status:** Copied to `orchestr8/src-tauri/src/ws/`. **Reviewed & Deemed Unnecessary (Phase 5).**
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:81` * **Status:** Copied to `orchestr8/src-tauri/src/scaffold/`. **Refactoring Deferred (Phase 5 Decision).**
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:86` * **Action:** As modules (`db_commands`, `signal_chat_commands`, `webrtc`, `ws`) are refactored, identify needed error variants and merge them into `orchestr8/src-tauri/src/error.rs`. Update refactored code to use `CommandError`.
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:99` ## Refactoring Checklist & Key Learnings (Tauri v2.5 / orchestr8)
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:101` This checklist synthesizes key patterns and learnings specific to refactoring DAC-O code for Tauri v2.5 within the **orchestr8** project structure. Refer to this during subsequent module migrations (`signal_chat_commands.rs`, `webrtc/`, etc.) to streamline the process and avoid repeated errors.
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:104` ***Type:** All commands requiring shared state must use `state: State<'_, AppState>`. (`AppState` is defined in `src-tauri/src/state.rs`).
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:108` ***DB Connection (`Option<Connection>`):** The `db_conn` field is `Mutex<Option<Connection>>`. After acquiring the lock (`let conn_guard = ...`), you **must** handle the `Option`: `let conn = conn_guard.as_ref().ok_or(CommandError::DbNotInitialized)?;`
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:109` *   **Initialization:** New state fields must be initialized in `main.rs` within the `.setup()` closure when creating `AppState`. Remember necessary imports (`HashMap`, `Arc`, `Uuid`, model types) in `main.rs`.
- `one integration at a time/Staging/Connection - Files/DAC-O_rust_migration.md:112` ***Return Type:** All Tauri commands **must** return `CommandResult<T>` (defined in `error.rs` as `Result<T, CommandError>`).

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
