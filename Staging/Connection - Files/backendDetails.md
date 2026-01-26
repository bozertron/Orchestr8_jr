# Backend Implementation Details & Mysteries

This file tracks the review of backend Rust modules, noting their function, connections, and any unresolved questions.

---

**File:** `src-tauri/src/lib.rs`

**Function:** Appears to define a library entry point and an alternative Tauri application setup (`run` function). It declares some top-level modules (`db`, `error`, `state`) and defines several Tauri commands directly: placeholder CRUD commands for `Report`s and an implemented `run_command` for executing shell commands.

**Connections:**
*   **In:** Potentially the main library entry if used as a dependency. The `run` function sets up a Tauri instance, initializes DB/State (similar to `main.rs` but using `block_on`), and registers the commands defined *within this file*. Uses `db`, `error`, `state` modules.
*   **Out:** Defines placeholder DB commands and an implemented `run_command`. Provides an alternative `run` function to start Tauri.

**Mysteries:**
*   **Dual Entry Points:** Why are both `main.rs` and `lib.rs` present with full Tauri application setup logic? Which one is the intended primary entry point? (`main.rs` seems more complete with logging).
*   **Command Definition Location:** Why are these specific commands (especially the implemented `run_command`) defined here instead of in the `src/commands/` modules as planned? The `invoke_handler` in `main.rs` is commented out, while the one here is active for *these* commands.
*   **`run_command` Purpose:** What is the intended use of the generic `run_command`? Does it relate to or replace parts of the planned DAC-O scaffolding logic? (Note: Implementation uses `cmd /C`, Windows-specific).
*   **`block_on` Usage:** The `run` function uses `block_on` in the setup closure, which is generally discouraged.

---

**File:** `src-tauri/src/main.rs`

**Function:** The main entry point for the Tauri backend application. It initializes the async runtime (`tokio`), configures logging (`tauri_plugin_log`), sets up the Tauri application builder, registers plugins (`log`, `sql`), declares all backend modules, and uses the `.setup()` hook to asynchronously initialize the database pool (`db::connection::init_db_pool`) and create/register the shared `AppState` (`state::AppState`).

**Connections:**
*   **In:** Application entry point. Pulls in modules (`commands`, `db`, `error`, `models`, `scaffold`, `state`, `webrtc`, `ws`) and uses functions/structs from them (e.g., `init_db_pool`, `AppState`). Uses Tauri's core builder API and plugins.
*   **Out:** Builds and runs the Tauri application. Initializes critical shared resources like the database pool and application state. Will eventually register command handlers via `.invoke_handler()`.

**Mysteries:**
*   Command handler registration (`invoke_handler`) is commented out, pending command implementation.
*   WebSocket and WebRTC initialization logic is not yet present, aligning with TODOs elsewhere.

---

**File:** `src-tauri/src/error.rs`

**Function:** Defines the central error handling mechanism using the `thiserror` crate. Creates a custom `DacoError` enum with variants for various error sources (DB, IO, Tauri, WS, WebRTC, Scaffold, Config, etc.). Implements `Serialize` so errors can be returned from Tauri commands to the frontend. Defines a standard `Result<T>` type alias for the application.

**Connections:**
*   **In:** Used throughout the backend codebase wherever functions can fail. The `Result<T>` type is the standard return type for fallible operations. `#[from]` attributes handle conversions from underlying error types (`sqlx::Error`, `std::io::Error`, `tauri::Error`).
*   **Out:** Provides the `DacoError` enum and `Result<T>` type alias for use across the backend. The `Serialize` implementation enables error propagation to the frontend.

**Mysteries:**
*   The `WebSocket` and `WebRTC` error variants currently just hold strings; they might need to be more specific later depending on the chosen libraries and error details needed.

---

**File:** `src-tauri/src/state/app_state.rs`

**Function:** Defines the main `AppState` struct, which holds shared application state managed by Tauri. Currently contains the database connection pool (`SqlitePool`) wrapped in a `tokio::sync::Mutex` for safe concurrent access from async command handlers. Includes a `new` constructor.

**Connections:**
*   **In:** Instantiated in `main.rs` with the database pool from `db::connection`. Managed by Tauri and injected into command handlers via the `tauri::State<AppState>` parameter.
*   **Out:** Provides access (behind a mutex) to the shared database pool and eventually other shared state (WebSocket, WebRTC - marked as TODO) for use within command handlers.

**Mysteries:**
*   None. Uses standard Tauri state management patterns with `tokio::sync::Mutex` for async safety. The TODO for WS/WebRTC state is expected.

---

**File:** `src-tauri/src/state/mod.rs`

**Function:** Standard Rust module declaration file (`mod.rs`). Declares the `app_state` sub-module and re-exports the `AppState` struct for easier access.

**Connections:**
*   **In:** Used by `main.rs` to declare the state module and potentially by any module needing access to the `AppState` struct (via `use crate::state::AppState;`).
*   **Out:** Exposes the `app_state` module and the `AppState` struct.

**Mysteries:**
*   None. Standard state management organization.

---

**File:** `src-tauri/src/webrtc/connection.rs`

**Function:** Intended to hold the core WebRTC connection logic (creating peer connections, handling signaling via WebSocket, managing data channels/media streams). Currently empty, awaiting implementation (Phase 3).

**Connections:**
*   **In:** Likely managed by a struct/manager exposed via `webrtc/mod.rs`. Will interact heavily with the WebSocket server (`ws/server.rs`) for signaling. Called by chat commands or state logic to initiate/manage calls.
*   **Out:** Manages P2P connections for real-time communication.

**Mysteries:**
*   None. File is empty as expected at this stage.

---

**File:** `src-tauri/src/webrtc/mod.rs`

**Function:** Standard Rust module declaration file (`mod.rs`). Declares the `connection` sub-module intended to hold the WebRTC implementation details (signaling, peer connections for video/audio/screen share).

**Connections:**
*   **In:** Used by modules needing to initiate or manage WebRTC connections, likely chat command handlers (`commands/chat_commands.rs`) or potentially directly from `main.rs`/`lib.rs` or state management.
*   **Out:** Exposes the `connection` module, which will contain the core WebRTC logic.

**Mysteries:**
*   None. Standard module organization.

---

**File:** `src-tauri/src/ws/types.rs`

**Function:** Intended to define the data structures (structs, enums) for messages exchanged over the WebSocket connection (e.g., signaling messages, chat messages). Currently empty, awaiting implementation (Phase 3).

**Connections:**
*   **In:** Used by `ws/server.rs` to serialize/deserialize incoming and outgoing messages. Also potentially used by command handlers or other logic that needs to construct or interpret WebSocket messages.
*   **Out:** Defines the message contracts for WebSocket communication.

**Mysteries:**
*   None. File is empty as expected at this stage.

---

**File:** `src-tauri/src/ws/server.rs`

**Function:** Intended to hold the core WebSocket server implementation (handling client connections, message routing, potentially room management). Currently empty, awaiting implementation (Phase 3).

**Connections:**
*   **In:** Likely initialized and managed from `main.rs` or `lib.rs`. Will interact with `ws/types.rs` for message structures, potentially `state/app_state.rs` for shared state (like connected clients), and command handlers (`commands/*.rs`) for triggering actions based on messages.
*   **Out:** Manages WebSocket connections, sends/receives messages defined in `ws/types.rs`.

**Mysteries:**
*   None. File is empty as expected at this stage.

---

**File:** `src-tauri/src/ws/mod.rs`

**Function:** Standard Rust module declaration file (`mod.rs`). Declares the sub-modules for WebSocket functionality: `server` (for the server logic) and `types` (for message structures).

**Connections:**
*   **In:** Used by `main.rs` (or potentially `lib.rs`) to initialize and manage the WebSocket server logic. Also used by modules needing access to WebSocket message types (e.g., command handlers).
*   **Out:** Exposes the `server` and `types` modules.

**Mysteries:**
*   None. Standard module organization. Commented-out re-exports are likely future convenience additions.

---

**File:** `src-tauri/src/scaffold/files.rs`

**Function:** Intended to hold the Rust implementation for the DAC-O 'files' scaffolding feature (retrieving content of specific files by index). Currently empty, awaiting implementation/porting (Phase 3).

**Connections:**
*   **In:** Called by a command handler in `commands/daco_commands.rs`. Will need file indices and access to the target project's file system.
*   **Out:** Will generate report content (likely a String) containing the concatenated content of the requested files.

**Mysteries:**
*   None. File is empty as expected at this stage.

---

**File:** `src-tauri/src/scaffold/ui.rs`

**Function:** Intended to hold the Rust implementation for the DAC-O 'ui' scaffolding feature (analyzing UI component usage, particularly Naive UI). Currently empty, awaiting implementation/porting (Phase 3).

**Connections:**
*   **In:** Called by a command handler in `commands/daco_commands.rs`. Will need to parse Vue (`.vue`) and potentially TypeScript/JavaScript files in the target project.
*   **Out:** Will generate report content (likely a String) summarizing UI component usage.

**Mysteries:**
*   None. File is empty as expected at this stage.

---

**File:** `src-tauri/src/scaffold/types.rs`

**Function:** Intended to hold the Rust implementation for the DAC-O 'types' scaffolding feature (analyzing TypeScript type definitions). Currently empty, awaiting implementation/porting (Phase 3).

**Connections:**
*   **In:** Called by a command handler in `commands/daco_commands.rs`. Will need to parse TypeScript (`.ts`, `.d.ts`) files in the target project. May accept filter patterns.
*   **Out:** Will generate report content (likely a String) summarizing found type definitions.

**Mysteries:**
*   None. File is empty as expected at this stage.

---

**File:** `src-tauri/src/scaffold/commands.rs`

**Function:** Intended to hold the Rust implementation for the DAC-O 'commands' scaffolding feature (analyzing Tauri command definitions and invocations). Currently empty, awaiting implementation/porting (Phase 3).

**Connections:**
*   **In:** Called by a command handler in `commands/daco_commands.rs`. Will need to parse Rust (`src-tauri`) and TypeScript/JavaScript (`src`) files in the target project.
*   **Out:** Will generate report content (likely a String) summarizing command usage.

**Mysteries:**
*   None. File is empty as expected at this stage.

---

**File:** `src-tauri/src/scaffold/routes.rs`

**Function:** Intended to hold the Rust implementation for the DAC-O 'routes' scaffolding feature (analyzing Vue Router routes). Currently empty, awaiting implementation/porting (Phase 3).

**Connections:**
*   **In:** Called by a command handler in `commands/daco_commands.rs`. Will need to parse TypeScript/JavaScript files in the target project.
*   **Out:** Will generate report content (likely a String) summarizing route definitions.

**Mysteries:**
*   None. File is empty as expected at this stage.

---

**File:** `src-tauri/src/scaffold/stores.rs`

**Function:** Intended to hold the Rust implementation for the DAC-O 'stores' scaffolding feature (analyzing Pinia stores). Currently empty, awaiting implementation/porting (Phase 3).

**Connections:**
*   **In:** Called by a command handler in `commands/daco_commands.rs`. Will need to parse TypeScript/JavaScript files in the target project.
*   **Out:** Will generate report content (likely a String) summarizing store details (state, getters, actions).

**Mysteries:**
*   None. File is empty as expected at this stage.

---

**File:** `src-tauri/src/scaffold/overview.rs`

**Function:** Intended to hold the Rust implementation for the DAC-O 'overview' scaffolding feature (generating file index, structure summary, etc.). Currently empty, awaiting implementation/porting (Phase 3).

**Connections:**
*   **In:** Called by a command handler in `commands/daco_commands.rs` when the 'overview' feature is invoked. Will likely require access to the target project's file system.
*   **Out:** Will generate report content (likely a String) to be returned by the command handler and potentially saved to a file and/or the database (`LastOutput` model).

**Mysteries:**
*   None. File is empty as expected at this stage.

---

**File:** `src-tauri/src/scaffold/mod.rs`

**Function:** Standard Rust module declaration file (`mod.rs`). Declares the sub-modules containing the core logic for each DAC-O scaffolding feature (`overview`, `stores`, `routes`, `commands`, `types`, `ui`, `files`).

**Connections:**
*   **In:** Used by `commands/daco_commands.rs` to call the specific scaffolding functions defined in the sub-modules.
*   **Out:** Exposes the individual scaffolding logic modules. Functions within these modules will likely perform file system operations, code analysis, and report generation.

**Mysteries:**
*   None. Standard module organization. Commented-out re-exports are likely future convenience additions.

---

**File:** `src-tauri/src/commands/db_commands.rs`

**Function:** Intended to hold Tauri command handlers for general database operations (e.g., fetching specific records by ID, potentially some admin/debug functions). Currently empty, awaiting implementation (Phase 3).

**Connections:**
*   **In:** Functions defined here will be registered as Tauri commands in `main.rs` and invoked from the frontend. Will interact directly with `db/queries.rs` and the `SharedPool` from `db/connection.rs`.
*   **Out:** Provides command handlers callable from the frontend, likely returning `Result`s containing specific data fetched from the database.

**Mysteries:**
*   None. File is empty as expected at this stage.

---

**File:** `src-tauri/src/commands/daco_commands.rs`

**Function:** Intended to hold Tauri command handlers for DAC-O specific actions (running scaffolders, managing directories, handling outputs). Currently empty, awaiting implementation (Phase 3).

**Connections:**
*   **In:** Functions defined here will be registered as Tauri commands in `main.rs` and invoked from the frontend (likely via `services/tauriApi.ts` and triggered from `components/daco/*.vue`). Will interact heavily with `scaffold/*.rs`, `models/daco.rs`, `db/queries.rs`, and `state/app_state.rs`.
*   **Out:** Provides command handlers callable from the frontend. Will return `Result`s containing generated report content, file paths, directory listings, or success/failure status.

**Mysteries:**
*   None. File is empty as expected at this stage.

---

**File:** `src-tauri/src/commands/chat_commands.rs`

**Function:** Intended to hold Tauri command handlers specifically for chat-related functionality (sending messages, fetching history, managing groups, etc.). Currently empty, awaiting implementation (Phase 3).

**Connections:**
*   **In:** Functions defined here will be registered as Tauri commands in `main.rs` and invoked from the frontend (likely via `services/tauriApi.ts`). Will interact with `models/chat.rs`, `db/queries.rs`, `state/app_state.rs`, and potentially `ws/*.rs` or `webrtc/*.rs`.
*   **Out:** Provides command handlers callable from the frontend. Will return `Result`s containing data or success/failure status.

**Mysteries:**
*   None. File is empty as expected at this stage.

---

**File:** `src-tauri/src/commands/mod.rs`

**Function:** Standard Rust module declaration file (`mod.rs`). Declares the sub-modules containing Tauri command handlers: `chat_commands`, `daco_commands`, and `db_commands`. Makes functions within these modules accessible under the `crate::commands::` path.

**Connections:**
*   **In:** Used by `main.rs` (via `mod commands;`) to discover and register the command handler functions defined in the sub-modules.
*   **Out:** Exposes the `chat_commands`, `daco_commands`, and `db_commands` modules.

**Mysteries:**
*   None. Standard module organization.

---

**File:** `src-tauri/src/models/daco.rs`

**Function:** Defines structs specific to the DAC-O tool's data:
    *   `DacoFeature`: Represents a scaffolding feature/command (e.g., 'overview').
    *   `LastOutput`: Stores the content of the most recently generated output, potentially allowing edits.
    *   `Directory`: Tracks directories relevant to DAC-O (installed, explored, created).
    All structs derive standard traits (`sqlx::FromRow`, `serde`).

**Connections:**
*   **In:** Used by DAC-O command handlers (`commands/daco_commands.rs`), scaffolding logic (`scaffold/*.rs`), database queries (`db/queries.rs`), and potentially state (`state/app_state.rs`) to manage DAC-O features, track outputs, and handle relevant directories.
*   **Out:** Defines the core data structures for DAC-O specific operations.

**Mysteries:**
*   The `command` field in `DacoFeature` might be legacy if the original TS command execution is fully replaced by Rust logic.
*   The `LastOutput` struct's ID "Should always be 'current'" implies a specific storage/retrieval pattern (e.g., single-row table, always fetching latest).
*   The `edited_content` field in `LastOutput` suggests in-app editing of generated reports.
*   The different `dir_type` values in `Directory` hint at specific tracking mechanisms.

---

**File:** `src-tauri/src/models/config.rs`

**Function:** Defines the `Config` struct, likely used for storing key-value application settings in the database. Includes fields for the setting `key`, `value`, and an `is_default` flag. Derives standard traits (`sqlx::FromRow`, `serde`).

**Connections:**
*   **In:** Used by database queries and command handlers related to loading, saving, or managing application configuration/settings. Potentially used by `state/app_state.rs` to hold loaded configuration.
*   **Out:** Defines the structure for configuration entries stored in the database or managed in application state.

**Mysteries:**
*   None. Straightforward key-value storage model.

---

**File:** `src-tauri/src/models/chat.rs`

**Function:** Defines multiple structs related to chat functionality:
    *   `Chat`: Represents a 1-on-1 chat session.
    *   `ChatsCache`: Represents a cached message in a 1-on-1 chat.
    *   `GroupChat`: Represents a group chat session.
    *   `GroupChatMember`: Links users to group chats.
    *   `GroupChatsCache`: Represents a cached message in a group chat.
    *   `MediaDocument`: Represents uploaded files/media.
    All structs derive necessary traits (`sqlx::FromRow`, `serde`) and use `String` for IDs and `DateTime<Utc>` for timestamps.

**Connections:**
*   **In:** These structs will be used extensively by chat-related command handlers (`commands/chat_commands.rs`), database queries (`db/queries.rs`), WebSocket logic (`ws/*.rs`), and potentially application state (`state/app_state.rs`) for managing chat sessions, messages, members, and media.
*   **Out:** Defines the core data structures for all chat-related operations. Instances will be created, stored, retrieved, and serialized/deserialized throughout the chat features.

**Mysteries:**
*   None currently. The structure seems logical for supporting the planned chat features. The commented-out `uuid` import reinforces the decision to use `String` IDs.

---

**File:** `src-tauri/src/models/user.rs`

**Function:** Defines the `User` struct, representing an application user. Includes fields for ID (UUID string), name, profile image path/URL, settings (as a JSON string), and creation timestamp. Provides a `new` constructor to generate users with default values and a UUID. Derives traits for `sqlx` database mapping and `serde` serialization.

**Connections:**
*   **In:** Used by database queries (`db/queries.rs`), command handlers (`commands/*.rs`), and potentially application state (`state/app_state.rs`) for creating, storing, retrieving, and managing user data. The `new` function is likely called by user creation commands.
*   **Out:** Defines the `User` struct. Instances are created, serialized/deserialized, and stored/retrieved from the database or state.

**Mysteries:**
*   Minor: The comment on the `id` field mentions a "potential 'default_user'". What's the specific use case envisioned for a non-UUID default user ID?
*   Storing `settings` as a JSON string requires consistent serialization/deserialization logic where it's used.

---

**File:** `src-tauri/src/models/mod.rs`

**Function:** Standard Rust module declaration file (`mod.rs`). It declares the sub-modules within the `models` directory (`chat`, `config`, `daco`, `user`), making their contents accessible under the `crate::models::` path.

**Connections:**
*   **In:** Used by any module that needs access to the data models defined in the sub-modules (e.g., `main.rs`, `commands/*.rs`, `db/queries.rs`). Accessed via `mod models;` or `use crate::models::*`.
*   **Out:** Exposes the `chat`, `config`, `daco`, and `user` modules. Currently lacks re-exports mentioned in a comment.

**Mysteries:**
*   None. The commented-out re-export is likely a planned future addition for convenience.

---

**File:** `src-tauri/src/db/queries.rs`

**Function:** Defines the data structures (structs) that represent database entities, specifically the `Report` struct for DAC-O outputs. Uses `sqlx::FromRow` for mapping database rows to the struct and `serde` for serialization/deserialization. Also contains placeholders for actual database query functions.

**Connections:**
*   **In:** The `Report` struct is likely used by command handlers (`commands/*.rs`) when creating or retrieving report data. Query functions (when implemented) will take the `SharedPool` from `db/connection.rs` as input.
*   **Out:** Defines the `Report` struct used elsewhere. Query functions (when implemented) will return `Result`s containing `Report` instances or vectors of them, interacting with the database via the `sqlx::SqlitePool`.

**Mysteries:**
*   None currently. The file is primarily definitions and placeholders, as expected per the plan. The note about using `chrono::DateTime` for `created_at` is a good future consideration.

---

**File:** `src-tauri/src/db/connection.rs`

**Function:** Handles the setup and management of the SQLite database connection pool using `sqlx`. It initializes the connection, ensures the database file exists, runs migrations, and provides a shared pool (`SharedPool`) for other parts of the application.

**Connections:**
*   **In:** Called by `main.rs` (or potentially `lib.rs` based on the `pub` keyword) during application setup (`init_db_pool`) to get the pool. The `AppHandle` is passed in to resolve the application data directory.
*   **Out:** Provides the `SharedPool` (via `DbManager` struct or directly) to be used by database query functions (likely in `db/queries.rs` and command handlers in `commands/*.rs`) to interact with the database. Uses `tokio` for async file operations and `sqlx` for all database interactions. Depends on `crate::error` for error handling.

**Mysteries:**
*   Why are the `.create_if_missing(true)` and `sqlx::migrate!("./migrations")` lines commented with `// Removed artifact`? These seem crucial for DB initialization and migration. Need clarification on whether these are truly artifacts or necessary code that was commented out.

---
