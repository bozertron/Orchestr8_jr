# DAC-O Rust Code Migration Plan & Progress

This document tracks the progress and plan for migrating Rust code from the DAC-O project into the orchestr8 project's Tauri backend (`src-tauri`).

## Summary of Work Done (Phase 1 & 2: Orchestr8 Refactor & DAC-O File Copy)

1. **Orchestr8 Backend Refactoring:**
    * The monolithic `orchestr8/src-tauri/src/main.rs` file was refactored into a modular structure.
    * Created modules:
        * `error.rs`: Contains `CommandError` enum and `CommandResult` type.
        * `models.rs`: Contains data structures (structs, enums) used across commands.
        * `state.rs`: Contains shared application state definition (`DbState`).
        * `utils.rs`: Contains helper functions (`add_optional_arg`, `add_bool_flag`).
        * `commands/`: Parent module for all Tauri commands.
            * `llm_chat_commands.rs`: (Renamed from `chat_commands.rs`) Holds existing orchestr8 commands for LLM interaction (`send_message`, `fetch_history`, etc.).
            * `project_commands.rs`: Holds commands for project management (`get_projects`, `create_project`, etc.).
            * `prd_commands.rs`: Holds commands for PRD operations (`get_current_prd`, etc.).
            * `settings_commands.rs`: Holds commands for settings (`get_llm_entities`, `get_intercom_config`, etc.).
            * `fs_commands.rs`: Holds commands for filesystem operations (`get_file_tree`, etc.).
            * `script_commands.rs`: Holds commands for running external Node.js scripts (`list_cli_plugins`, `run_script_command`, `scaffold_*`).
    * `main.rs` was updated to declare these modules and register commands from their new locations.
    * Compiler warnings related to unused imports/variables (due to stubbed functions) were cleaned up.

2. **DAC-O Model Migration:**
    * All structs from the DAC-O `src/models/` directory (`chat.rs`, `config.rs`, `daco.rs`, `user.rs`) were migrated into `orchestr8/src-tauri/src/models.rs`.
    * `sqlx`-specific attributes (`FromRow`, `#[sqlx(...)]`) were removed as orchestr8 uses `rusqlite`.
    * Necessary imports (`chrono`, `uuid`) were added/adjusted in `models.rs`.

3. **DAC-O Signaling Commands Initial Migration:**
    * Commands related to signaling (`signal_join`, `signal_leave`, `signal_send`, `signal_get_clients`) from `DAC-O/src/commands/chat_commands.rs` were moved into a new file: `orchestr8/src-tauri/src/commands/signal_chat_commands.rs`.
    * Placeholders and TODO comments were added for dependencies on DAC-O state (`AppState`, `signaling_clients`) and types (`ClientInfo`, `ClientSignal`) that still need migration/definition within orchestr8.
    * The new module was declared in `commands/mod.rs` and the commands were registered in `main.rs`.

4. **DAC-O Bulk File Copy:**
    * Adopted a "copy-first, refactor-later" strategy.
    * Used PowerShell to copy the remaining DAC-O Rust modules/files into the `orchestr8/src-tauri/src` structure:
        * `C:\DAC-O\src-tauri\src\commands\db_commands.rs` -> `c:\orchestr8\src-tauri\src\commands\db_commands.rs`
        * `C:\DAC-O\src-tauri\src\webrtc\` -> `c:\orchestr8\src-tauri\src\webrtc\` (recursive)
        * `C:\DAC-O\src-tauri\src\ws\` -> `c:\orchestr8\src-tauri\src\ws\` (recursive)
        * `C:\DAC-O\src-tauri\src\scaffold\` -> `c:\orchestr8\src-tauri\src\scaffold\` (recursive)
    * These files are now present in the project but are **not yet compiled or integrated** into the main application logic. They will be refactored "in situ".

## Modules/Files Copied (Awaiting Refactor & Integration)

The following modules and files have been copied from DAC-O into the `orchestr8` project structure. They require refactoring for Tauri v2.5 compliance, integration with orchestr8's state/error handling, and eventual activation in `main.rs`.

1. **`commands/db_commands.rs`:**
    * **Status:** **Refactored (Phase 3).**
    * **Action:** Functions refactored to use `rusqlite` via `DbState`. Error handling updated to use `CommandResult` and `CommandError`. Module declared in `commands/mod.rs`. Commands registered in `main.rs`. `Report` struct added to `models.rs`.
    * **Tauri v2.5:** State access (`state.inner().0.lock()`), error handling (`CommandResult`, `CommandError` variants), command signatures (`#[tauri::command]`, `async fn`), and async runtime usage (`tokio::process::Command`) confirmed/updated.
    * **Learnings/Issues Encountered:**
        * Initial refactor required careful mapping from `sqlx` patterns to `rusqlite`.
        * Correct import for `Report` model (`crate::models::Report`) was crucial; initially used `std::error::Report` by mistake.
        * The `Report` struct definition was missing from `models.rs` and had to be added, including `#[derive(Serialize, Deserialize)]`.
        * Correct `CommandError` variants needed identification (`LockError`, `ScriptExecutionError`, `Io`, `Database` via `#[from]`).
        * Correct access pattern for Tauri `State` tuple struct (`state.inner().0.lock()`) was necessary.
        * Debugging involved iterative fixes based on compiler feedback (`rustc` errors).
        * Related compiler errors surfaced in `signal_chat_commands.rs` (missing `Emitter` trait, `Runtime` generic issues), which were fixed or noted for later resolution.

2. **`db/` Module (from DAC-O):**
    * **Status:** Not copied (contains `sqlx` connection logic).
    * **Action:** No direct code migration needed. Focus on ensuring `orchestr8/src-tauri/src/database/schema.rs` supports tables needed by `db_commands.rs` and migrated models.

3. **`state.rs` (Signaling State Integration):**
    * **Status:** **Integrated (Phase 4).**
    * **Action:** Defined a unified `AppState` struct in `state.rs` containing both `db_conn: Mutex<Option<Connection>>` and `signaling_clients: Arc<Mutex<HashMap<Uuid, ClientInfo>>>`. Updated `main.rs` to initialize and manage this `AppState`. Updated `db_commands.rs`, `project_commands.rs`, and `signal_chat_commands.rs` to use `State<'_, AppState>` and access fields correctly (e.g., `state.db_conn`, `state.signaling_clients`).
    * **Preparatory Steps:** Moved placeholder `ClientInfo` and `ClientSignal` structs from `signal_chat_commands.rs` to `models.rs`. Updated imports accordingly.
    * **Learnings/Issues Encountered:** Required updating state access patterns across multiple command modules. Ensured necessary types (`Uuid`, `ClientInfo`, `HashMap`, `Arc`) were imported in `main.rs` for state initialization.

4. **`webrtc/` Module:**
    * **Status:** Copied to `orchestr8/src-tauri/src/webrtc/`. **Structurally Refactored (Phase 5). Core Logic Deferred.**
    * **Action:** `connection.rs` updated for `CommandResult`/`CommandError`, correct imports, and logging. Core WebRTC logic (connection handling, data channels) remains as TODOs and is deferred. Module declaration (`mod webrtc;`) and command registration in `main.rs` will happen *after* core logic implementation.
    * **Tauri v2.5:** Structural alignment (error handling, async, imports) confirmed. Core logic implementation will require careful attention to async runtime, state access, and event emission.

5. **`ws/` Module:**
    * **Status:** Copied to `orchestr8/src-tauri/src/ws/`. **Reviewed & Deemed Unnecessary (Phase 5).**
    * **Action:** Module reviewed. Contains types (`ClientInfo`, `ClientSignal`) redundant with `models.rs` and an empty `server.rs`. Signaling functionality is handled by `signal_chat_commands.rs` and Tauri events. This module is not needed and will likely be removed. No refactoring or integration planned.
    * **Tauri v2.5:** N/A.

6. **`scaffold/` Module:**
    * **Status:** Copied to `orchestr8/src-tauri/src/scaffold/`. **Refactoring Deferred (Phase 5 Decision).**
    * **Action:** Due to complexity and potential replacement by the existing Node.js script approach (`script_commands.rs`), the refactoring and integration of this module is deferred to a dedicated future step. It will not be addressed in the current migration pass. Eventual integration or removal TBD.

7. **`error.rs` (`DacoError` from DAC-O):**
    * **Status:** Not copied (represents DAC-O's specific errors).
    * **Action:** As modules (`db_commands`, `signal_chat_commands`, `webrtc`, `ws`) are refactored, identify needed error variants and merge them into `orchestr8/src-tauri/src/error.rs`. Update refactored code to use `CommandError`.

## Tauri v2.5 Compliance Considerations (Applied in `db_commands.rs` Refactor)

The following Tauri v2.5 points were addressed during the `db_commands.rs` refactoring:

* **State Management:** Accessing state via `State<'_, DbState>` and `state.inner().0.lock()`.
* **Async Runtime:** Using `async fn` for commands and `tokio::process::Command` for `run_external_command`.
* **Event Handling:** (Not directly used in `db_commands.rs`, but `Emitter` trait was added to `signal_chat_commands.rs`).
* **Command Signatures:** Ensured `#[tauri::command]` and `async fn` usage was correct. Handled `Runtime` generics where needed (though some issues remain in `signal_chat_commands.rs`).
* **Error Handling:** Ensured all commands return `crate::error::CommandResult<T>` and use appropriate `CommandError` variants.
* **Plugin Usage:** No specific v1 plugins were identified or needed replacement in `db_commands.rs`.

## Refactoring Checklist & Key Learnings (Tauri v2.5 / orchestr8)

This checklist synthesizes key patterns and learnings specific to refactoring DAC-O code for Tauri v2.5 within the **orchestr8** project structure. Refer to this during subsequent module migrations (`signal_chat_commands.rs`, `webrtc/`, etc.) to streamline the process and avoid repeated errors.

**1. State Management (`AppState`):**
    ***Type:** All commands requiring shared state must use `state: State<'_, AppState>`. (`AppState` is defined in `src-tauri/src/state.rs`).
    *   **Access:** Get the inner `AppState` struct: `let app_state = state.inner();`
    ***Field Access:** Access specific state fields directly: `app_state.db_conn`, `app_state.signaling_clients`.
    *   **Mutex Locking:** Lock mutexes using `.lock()` and map errors: `app_state.db_conn.lock().map_err(|e| CommandError::LockError(format!("db_conn lock failed: {}", e)))?` (Use the appropriate `CommandError` variant, likely `LockError`).
    ***DB Connection (`Option<Connection>`):** The `db_conn` field is `Mutex<Option<Connection>>`. After acquiring the lock (`let conn_guard = ...`), you **must** handle the `Option`: `let conn = conn_guard.as_ref().ok_or(CommandError::DbNotInitialized)?;`
    *   **Initialization:** New state fields must be initialized in `main.rs` within the `.setup()` closure when creating `AppState`. Remember necessary imports (`HashMap`, `Arc`, `Uuid`, model types) in `main.rs`.

**2. Error Handling (`CommandResult`, `CommandError`):**
    ***Return Type:** All Tauri commands **must** return `CommandResult<T>` (defined in `error.rs` as `Result<T, CommandError>`).
    *   **Error Mapping:** Map specific errors to appropriate `CommandError` variants (defined in `error.rs`).
        *Use `#[from]` implementations where available (e.g., `rusqlite::Error` maps to `CommandError::Database`, `std::io::Error` maps to `CommandError::Io`). Use `.map_err(CommandError::Database)` or `.map_err(CommandError::Io)`.
        *   Use specific variants for other cases: `CommandError::LockError(String)`, `CommandError::ScriptExecutionError { status, stderr }`, `CommandError::TauriError(tauri::Error)`. Check `error.rs` for exact variant names and required fields.
    *   **Serialization:** Ensure `CommandError` and any custom structs returned within `CommandResult` derive `Serialize`. (`CommandError` already derives `Serialize` via a manual `impl`).

**3. Database Operations (`rusqlite`):**
    ***Methods:** Use standard `rusqlite` methods (`prepare`, `query_map`, `query_row`, `execute`, `last_insert_rowid`, etc.) on the `Connection` obtained from `AppState`.
    *   **Parameters:** Use the `params![]` macro for binding parameters to SQL queries.
    *   **Optional Results:** Use `.optional()` from `rusqlite::OptionalExtension` after `query_row` if the query might validly return no rows (to avoid `QueryReturnedNoRows` errors). Remember `use rusqlite::OptionalExtension;`.

**4. Models (`models.rs`):**
    ***Location:** Define **all** shared data structs (used across multiple command modules or in `AppState`) in `src-tauri/src/models.rs`.
    *   **Derives:** Ensure structs derive `Debug`, `Clone`, and especially `Serialize`, `Deserialize` if they are used as command arguments, return types (within `CommandResult`), or stored in state that needs serialization (like for events).
    ***Imports:** Use `use crate::models::StructName;` to import them into command files.
    *   **Placeholders:** Move any temporary struct definitions from command files (often marked with `// Placeholder`) to `models.rs` *before* attempting to use them in `AppState` or across modules.

**5. Command Signatures (`#[tauri::command]`):**
    ***Attribute:** Mark all functions callable from JS with `#[tauri::command]`.
    *   **Async:** Use `async fn` for the function definition.
    ***Runtime Generic (`<R: Runtime>`):**
        *   **Required if using `AppHandle`:** If the command needs `app_handle: AppHandle<R>` (e.g., to use `.emit()`), the generic `<R: Runtime>` is required on the function signature.
        *   **May be required otherwise:** Even if `AppHandle` is *not* used, the `#[tauri::command]` macro might still require the generic `<R: Runtime>` on the function signature to resolve types correctly. If you get "type annotations needed" or "cannot satisfy `_: tauri::Runtime`" errors, try adding `<R: Runtime>` to the function signature. If `AppHandle` is truly unused, add it as an *unused* parameter: `_app_handle: AppHandle<R>`.

**6. Imports & Dependencies:**
    ***Standard:** Double-check necessary `use` statements in each file (e.g., `tauri::Emitter`, `uuid::Uuid`, `std::collections::HashMap`, `std::sync::Arc`, model types, error types).
    *   **`Cargo.toml`:** Verify crate dependencies are listed in `src-tauri/Cargo.toml`. Crucially, ensure required **features** are enabled (e.g., `uuid` needs `features = ["v4", "serde"]`).

**7. Module System Integration:**
    ***Declaration:** Declare new command modules (`*.rs` files within `commands/`) in `src-tauri/src/commands/mod.rs` using `pub mod module_name;`.
    *   **Registration:** Register all exported command functions in `src-tauri/src/main.rs` within the `tauri::generate_handler![]` macro. Use full paths for clarity (e.g., `commands::module_name::command_fn`).

**8. Tooling & Workflow:**
    ***`replace_in_file` Sensitivity:** This tool requires *exact* matches, including whitespace and comments. Edits can fail if the file content has changed slightly (e.g., due to previous edits or auto-formatting). Use precise, minimal SEARCH blocks.
    *   **`write_to_file` Fallback:** If `replace_in_file` fails repeatedly on complex changes, consider using `write_to_file` with the complete intended file content as a fallback.
    ***Iterative Debugging:** Expect compiler errors after changes. Read the errors carefully – they often pinpoint the exact issue (e.g., incorrect type, missing import, wrong state access pattern). Fix errors iteratively.
    *   **Contextual Checklist:** Add this checklist (or relevant parts) as a comment block at the top of files awaiting refactoring for easy reference.

## Next Steps (End of Phase 5)

Phase 5 involved reviewing the remaining copied modules (`webrtc`, `ws`, `scaffold`) and performing structural refactoring where necessary:
*   `webrtc/connection.rs` was updated for error handling, imports, and logging. Core logic remains deferred.
*   `ws/` module was reviewed and deemed unnecessary due to existing Tauri command/event signaling.
*   `scaffold/` module refactoring was explicitly deferred to a future phase due to complexity and potential replacement.

**The next major phase will involve:**
1.  **Integrating `WebRtcManager`:** Adding the `WebRtcManager` to `AppState` and implementing the necessary Tauri commands to interact with it (e.g., `webrtc_connect`, `webrtc_handle_signal`).
2.  **Implementing Core Logic:** Filling in the `// TODO` sections within `webrtc/connection.rs` to handle peer connection setup, data channels, etc.
3.  **Addressing `scaffold/`:** Deciding whether to refactor/integrate the Rust `scaffold` module or fully rely on/enhance the `script_commands.rs` Node.js approach.
4.  **Compilation & Debugging:** Attempting to compile the entire `src-tauri` crate and resolving any errors or warnings that arise from the migrated and refactored code.
