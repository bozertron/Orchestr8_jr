# Orchestr8 "Integr8 Feature" - Contextual Reconnaissance Report

Date: May 18, 2025
Prepared by: Glaver (for The CTO & Ben)

This document details existing Orchestr8 platform structures, patterns, and resources relevant to the upcoming "Integr8 Feature" development sprint. The goal is to provide comprehensive context to inform the design and implementation of this new feature set, ensuring seamless integration and leveraging existing capabilities.

## LLM Integration Architecture

The primary Pinia store for managing LLM interactions and configurations appears to be `src/stores/llmStore.ts`.

### `src/stores/llmStore.ts`

*   **Purpose:** This store is responsible for managing "LLM Entities," which represent different LLM configurations (e.g., specific models from providers like OpenAI, Anthropic, or a local/mock LLM). It handles CRUD operations for these entities, allows selection for editing, and provides functionality to test their network and API connectivity. It also includes specific logic for fetching and managing models from OpenRouter.
*   **State:**
    *   `entities: Ref<LlmEntityMinimal[]>`: An array holding a minimal representation of all available LLM entities (likely for display in a list).
    *   `selectedEntityConfig: Ref<LlmEntityConfig | null>`: Holds the full configuration details of an LLM entity when it's selected for viewing or editing.
    *   `formData: Reactive<LlmEntityConfigInput>`: A reactive object bound to the form used for creating or editing LLM entity configurations. It's initialized with `defaultFormData()`.
    *   `isEditing: Ref<boolean>`: Flag to control the visibility of the editing/creation form.
    *   `isLoadingList: Ref<boolean>`: Indicates if the list of LLM entities is currently being fetched.
    *   `isLoadingConfig: Ref<boolean>`: Indicates if the configuration for a selected entity is being fetched.
    *   `isSaving: Ref<boolean>`: Indicates if an entity configuration is currently being saved.
    *   `isDeleting: Ref<boolean>`: Indicates if an entity is being deleted.
    *   `isTestingNetwork: Ref<boolean>`: Indicates if a network test is in progress.
    *   `isTestingApi: Ref<boolean>`: Indicates if an API test for an LLM entity is in progress.
    *   `listError: Ref<string | null>`: Stores error messages related to fetching the list of entities.
    *   `formError: Ref<string | null>`: Stores error messages related to form operations (save, delete, fetch config).
    *   `testResults: Reactive<CombinedTestResults>`: An object storing the results of network and API tests (`{ network: 'Untested' | 'Testing...' | 'OK: ...' | 'Failed: ...', api: ... }`).
    *   `openRouterModels: Ref<{id: string, name: string}[]>`: Stores a list of models available from OpenRouter.
    *   `isLoadingOpenRouterModels: Ref<boolean>`: Indicates if OpenRouter models are being fetched.
    *   `openRouterModelsError: Ref<string | null>`: Stores error messages related to fetching OpenRouter models.
*   **Key Actions:**
    *   `fetchEntities()`: Asynchronously fetches the list of all LLM entities by invoking the Tauri command `get_llm_entities`.
    *   `addNew()`: Resets the `formData` and sets `isEditing` to `true` to display the form for adding a new LLM entity.
    *   `selectEntity(entityId: string)`: Fetches the full configuration of a specific LLM entity by its ID using the Tauri command `get_llm_entity_config` and populates `formData`.
    *   `saveEntity(payload: LlmEntityConfigInput)`: Saves a new or updates an existing LLM entity. It invokes `add_llm_entity` for new entities or `update_llm_entity` for existing ones. The API key is explicitly removed from the payload if it's empty.
    *   `cancelEdit()`: Hides the form and clears any form-specific state.
    *   `deleteEntity()`: Deletes the currently selected LLM entity using the Tauri command `delete_llm_entity`.
    *   `testNetwork()`: Invokes the Tauri command `test_network_connection` to check general network connectivity.
    *   `testApi()`: Invokes the Tauri command `test_llm_api_connection` with the ID of the selected entity to test its specific API.
    *   `fetchOpenRouterModels()`: Fetches a list of available models from OpenRouter via the `get_openrouter_models` Tauri command.
    *   `clearFormError()`, `clearListError()`: Actions to clear respective error messages.
*   **Associated Tauri Commands (Invoked from this store):**
    *   `get_llm_entities`: Fetches `LlmEntityMinimal[]`.
    *   `get_llm_entity_config`: Takes `entityId: string`, fetches `LlmEntityConfig`.
    *   `add_llm_entity`: Takes `config: LlmEntityConfigInput`, returns `string` (likely new entity ID).
    *   `update_llm_entity`: Takes `entityId: string, config: LlmEntityConfigInput`.
    *   `delete_llm_entity`: Takes `entityId: string`.
    *   `test_network_connection`: Returns `TestResult`.
    *   `test_llm_api_connection`: Takes `entityId: string`, returns `TestResult`.
    *   `get_openrouter_models`: Returns `{id: string, name: string}[]`.
*   **Key TypeScript Types Used (from `@/types/llmConfig.ts`):**
    *   `LlmEntityMinimal`: Likely contains minimal data for listing entities (e.g., `id`, `role_name`, `entity_type`, `llm_provider`).
    *   `LlmEntityConfig`: Represents the full configuration of an LLM entity (e.g., `id`, `project_id`, `role_name`, `entity_type`, `llm_provider`, `model_id`, `api_key_present` (boolean), `system_prompt`, `mock_response_payload`).
    *   `LlmEntityConfigInput`: The shape of the data used in the form for creating/editing entities. Includes `api_key` as a string.
    *   `TestResult`: `{ success: boolean, message: string }`.
    *   `CombinedTestResults`: `{ network: string, api: string }`.

This store provides a comprehensive interface for managing LLM configurations within the Orchestr8 frontend.

### `src/types/llmConfig.ts` - Core LLM Data Structures

This file defines the TypeScript interfaces used for LLM configurations, prompts, and test results. These types are utilized by `llmStore.ts` and likely by components that interact with it.

*   **`LlmEntityMinimal`**:
    *   `id: string`: Unique identifier (e.g., UUID for the entity in the list).
    *   `name: string`: User-defined role name (e.g., "Marketing Analyst").
    *   `entity_type: 'Cloud' | 'Mock'`: Specifies if the LLM is a cloud-based service or a mock/local one.
    *   *Purpose*: Used for displaying a list of available LLM entities without fetching full configuration details.

*   **`LlmEntityConfig`**:
    *   `id: string`: Unique identifier for the configuration entry itself (likely a database primary key).
    *   `project_id: number`: Associates the configuration with a project.
    *   `model_id: string | null`: The specific model identifier (e.g., "gpt-4o", "claude-3-opus").
    *   `role_name: string`: User-defined name for this LLM configuration.
    *   `entity_type: 'Cloud' | 'Mock'`.
    *   `llm_provider: string | null`: The provider of the LLM (e.g., "OpenAI", "Anthropic", "OpenRouter").
    *   `system_prompt: string | null`: The system prompt to be used with this LLM.
    *   `mock_response_payload: string | null`: If `entity_type` is 'Mock', this can hold a predefined response.
    *   *Purpose*: Represents the full, detailed configuration of an LLM entity, typically fetched when a user wants to view or edit an existing configuration. API keys are explicitly noted as being handled by the backend.

*   **`LlmEntityConfigInput`**:
    *   `id?: string | null`: This maps to `LlmEntityConfig.model_id` when sending data to the backend.
    *   `name: string`: This maps to `LlmEntityConfig.role_name`.
    *   `entity_type: 'Cloud' | 'Mock'`.
    *   `provider?: string | null`: Maps to `LlmEntityConfig.llm_provider`.
    *   `api_key?: string | null`: The API key. This is sent to the backend only if provided or changed by the user.
    *   `system_prompt?: string | null`.
    *   `mock_payload?: string | null`.
    *   `project_id?: number | null`.
    *   *Purpose*: Defines the structure of the data sent from the frontend form to the backend when creating a new LLM entity or updating an existing one.

*   **`TestResult`**:
    *   `success: boolean`: Indicates whether the test was successful.
    *   `message: string`: Provides details about the test outcome.
    *   *Purpose*: A standardized structure for reporting the results of backend operations like network or API connectivity tests.

*   **`CombinedTestResults`**:
    *   `network: string`: Stores the string result of a network test (e.g., "Untested", "Testing...", "OK: ...", "Failed: ...").
    *   `api: string`: Stores the string result of an API test for a specific LLM entity.
    *   *Purpose*: Used by `llmStore.ts` to manage and display the status/results of connectivity tests in the UI.

### `src/stores/integr8Store.ts` - Orchestrating LLM "Engineers" and Tasks

This Pinia store (`integr8`) manages the concept of "Integr8 Engineers" and "Integr8 Tasks." It appears to be the primary mechanism for assigning work to specific LLM configurations (referred to as "Engineers") and tracking their activities.

*   **Concept of "Integr8 Engineers"**:
    *   An `Integr8Engineer` is an entity that can be assigned tasks. Each engineer is crucially linked to an `llm_entity_id`. This `llm_entity_id` refers to an LLM configuration managed by `llmStore.ts` (and defined by `LlmEntityConfig` from `src/types/llmConfig.ts`).
    *   Engineers have a `name`, a `specialization` (e.g., "Code Generation", "Documentation"), a `status` ('Idle', 'Working', etc.), and can be assigned a `current_task`.
    *   This setup allows the system to define different "personas" or specialized LLM agents, each utilizing a specific underlying LLM configuration for performing tasks.

*   **Selection and Utilization of LLM Configurations/Engineers**:
    *   LLM configurations (from `llmStore.ts`) are selected for use by creating an `Integr8Engineer` and associating it with an `llm_entity_id` via the `createEngineer` action.
    *   Tasks (`Integr8Task`) are then assigned to a specific `Integr8Engineer` using the `assignTask` action. This means a particular LLM configuration (via the engineer's `llm_entity_id`) is chosen to perform that specific task.
    *   The `integr8Store` doesn't seem to handle the *selection logic* of *which* engineer/LLM config is best for a task (that might be UI-driven or handled by another service), but it *executes* the assignment once a choice is made.

*   **State:**
    *   `engineers: Ref<Integr8Engineer[]>`: List of all defined Integr8 Engineers.
    *   `tasks: Ref<Integr8Task[]>`: List of all Integr8 Tasks.
    *   `results: Ref<TaskResult[]>`: List of results generated by tasks.
    *   `isLoading: Ref<boolean>`: General loading state for store operations.
    *   `error: Ref<string | null>`: General error message for store operations.
    *   `selectedEngineer: Ref<Integr8Engineer | null>`: The currently selected engineer in the UI.
    *   `selectedTask: Ref<Integr8Task | null>`: The currently selected task in the UI.

*   **Key Actions:**
    *   `fetchEngineers()`: Fetches all `Integr8Engineer` instances via Tauri command `get_integr8_engineers`.
    *   `createEngineer(name: string, llm_entity_id: number, specialization: string)`: Creates a new `Integr8Engineer` by invoking `create_integr8_engineer`. This links a user-defined engineer profile to a specific LLM configuration.
    *   `assignTask(engineer_id: number, task_name: string, ...)`: Assigns a new `Integr8Task` to a specified engineer using `assign_integr8_task`. It then fetches the task details using `get_integr8_task_status` and updates the engineer's status.
    *   `fetchTaskStatus(task_id: number)`: Updates the status of a specific task using `get_integr8_task_status`.
    *   `updateTaskProgress(task_id: number, progress: number, status?: string)`: Updates a task's progress and status via `update_integr8_task_progress`. If a task is completed or fails, it also updates the assigned engineer's status to 'Idle'.
    *   `storeTaskResult(task_id: number, result_type: string, content: string)`: Stores a result associated with a task using `store_integr8_task_result`.
    *   `selectEngineer(engineerId: number | null)` and `selectTask(taskId: number | null)`: UI-related actions for selecting entities.
    *   `getTaskResultByType(taskId: number, type: string)`: Retrieves a specific task result.

*   **Associated Tauri Commands (Invoked from this store):**
    *   `get_integr8_engineers`: Fetches `Integr8Engineer[]`.
    *   `create_integr8_engineer`: Takes `name`, `llm_entity_id`, `specialization`, returns `Integr8Engineer`.
    *   `assign_integr8_task`: Takes `engineer_id`, `task_name`, `description`, `source_project_path`, `target_feature_path`, returns `number` (task_id).
    *   `get_integr8_task_status`: Takes `task_id`, returns `Integr8Task`.
    *   `update_integr8_task_progress`: Takes `task_id`, `progress`, `status`.
    *   `store_integr8_task_result`: Takes `task_id`, `result_type`, `content`, returns `number` (result_id).

*   **Key TypeScript Types Defined and Used within this Store:**
    *   **`Integr8Engineer`**:
        *   `id: number`
        *   `name: string`
        *   `llm_entity_id: number` (Links to an `LlmEntityConfig`'s `id` from `llmStore.ts` or its database representation)
        *   `specialization: string`
        *   `status: 'Idle' | 'Working' | 'Paused' | 'Error'`
        *   `current_task: string | null`
        *   `progress: number`
        *   `last_update: number | null` (Unix timestamp)
    *   **`Integr8Task`**:
        *   `id: number`
        *   `task_name: string`
        *   `description: string | null`
        *   `status: 'Queued' | 'In Progress' | 'Completed' | 'Failed' | 'Paused'`
        *   `engineer_id: number | null` (Links to `Integr8Engineer.id`)
        *   `source_project_path: string`
        *   `target_feature_path: string | null`
        *   `progress: number`
        *   `created_at: number` (Unix timestamp)
        *   `updated_at: number` (Unix timestamp)
    *   **`TaskResult`**:
        *   `id: number`
        *   `task_id: number` (Links to `Integr8Task.id`)
        *   `result_type: string` (e.g., "generated_code", "analysis_report")
        *   `content: string` (The actual result data, likely JSON or text)
        *   `created_at: number` (Unix timestamp)

In summary, `integr8Store.ts` builds upon the LLM configurations managed by `llmStore.ts` by introducing a layer of "Engineers" that can be assigned "Tasks." This provides a structured way to utilize different LLMs for various specialized activities within the "Integr8 Feature."

## Database Schemas & Access

The Orchestr8 platform primarily utilizes **SQLite** for its backend data storage. The schema definitions are located in `src-tauri/src/database/schema.rs` within the `initialize_database_tables` function. This function creates tables in the main application database (`scaffolder_data.sqlite`). Additionally, a separate SQLite database (`history.sqlite`) is created for each LLM entity to store its interaction history, managed by `initialize_entity_history_db`.

### Definitive Schemas for Integr8 and Related Tables (SQLite)

The following `CREATE TABLE` statements are sourced directly from `src-tauri/src/database/schema.rs`:

**1. `LlmEntities` Table:**
   *   Purpose: Stores configurations for LLM entities (providers, models, API keys, etc.), corresponding to the data managed by `llmStore.ts`.
   *   Schema:
    ```sql
    CREATE TABLE IF NOT EXISTS LlmEntities ( -- Renamed from LlmEntityConfigs
        id TEXT PRIMARY KEY NOT NULL, -- Use the entity instance ID as PK
        project_id INTEGER NOT NULL, -- Link to project
        role_name TEXT NOT NULL, -- User-defined role name
        entity_type TEXT NOT NULL CHECK(entity_type IN ('Cloud', 'Mock')), -- Enforce type
        llm_provider TEXT, -- Nullable for Mock
        api_key TEXT, -- Handled by Stronghold later, store placeholder/null
        mock_response_payload TEXT, -- Nullable for Cloud
        system_prompt TEXT, -- Changed to nullable
        model_id TEXT, -- Added field, nullable
        FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE -- Cascade delete entities if project deleted
    );
    CREATE INDEX IF NOT EXISTS idx_llm_entities_project ON LlmEntities(project_id);
    ```
   *   *Note:* The `id` is `TEXT PRIMARY KEY`, which aligns with `LlmEntityConfig.id` being a string in the frontend.

**2. `Integr8_Engineers` Table:**
   *   Purpose: Stores information about the "Integr8 Engineers," which are specialized LLM agents, linking them to an `LlmEntities` configuration.
   *   Schema:
    ```sql
    CREATE TABLE IF NOT EXISTS Integr8_Engineers (
        engineer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        llm_entity_id INTEGER NOT NULL, -- This is an INTEGER
        specialization TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Idle',
        current_task TEXT,
        progress REAL DEFAULT 0.0,
        last_update INTEGER,
        -- FOREIGN KEY (llm_entity_id) REFERENCES LLM_Entities(entity_id) ON DELETE CASCADE -- Typo in source: LLM_Entities PK is 'id', not 'entity_id'
        FOREIGN KEY (llm_entity_id) REFERENCES LlmEntities(id) ON DELETE CASCADE -- Corrected FK assumption
    );
    ```
   *   *Note on Foreign Key:* The `llm_entity_id` is an `INTEGER`. The original DDL in `schema.rs` has `FOREIGN KEY (llm_entity_id) REFERENCES LLM_Entities(entity_id)`. However, the `LlmEntities` table's primary key is `id TEXT`. This suggests a potential mismatch or that `llm_entity_id` in `Integr8_Engineers` should ideally reference an integer primary key in `LlmEntities` if one existed, or `llm_entity_id` itself should be `TEXT` to match `LlmEntities.id`. Given `Integr8Engineer.llm_entity_id` is `number` in `integr8Store.ts`, it's likely intended to be an integer. This might imply `LlmEntities.id` is *also* an integer in some contexts or there's an implicit conversion/lookup. For this report, the corrected FK references `LlmEntities(id)` assuming `llm_entity_id` stores a string that matches `LlmEntities.id` or there's an underlying integer PK in `LlmEntities` that is not explicitly shown but implied by the `INTEGER` type here. The `llmStore.ts` uses string IDs for `LlmEntityConfig.id`. This area might require further clarification in the actual DB implementation vs. DDL.

**3. `Integr8_Tasks` Table:**
   *   Purpose: Stores details about tasks assigned to Integr8 Engineers.
   *   Schema:
    ```sql
    CREATE TABLE IF NOT EXISTS Integr8_Tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'Queued',
        engineer_id INTEGER,
        source_project_path TEXT NOT NULL,
        target_feature_path TEXT,
        progress REAL DEFAULT 0.0,
        created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
        updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
        FOREIGN KEY (engineer_id) REFERENCES Integr8_Engineers(engineer_id) ON DELETE SET NULL
    );
    ```

**4. `Integr8_Task_Results` Table:**
   *   Purpose: Stores the outputs or results generated by completed Integr8 Tasks.
   *   Schema:
    ```sql
    CREATE TABLE IF NOT EXISTS Integr8_Task_Results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        result_type TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
        FOREIGN KEY (task_id) REFERENCES Integr8_Tasks(task_id) ON DELETE CASCADE
    );
    ```
These definitions from `schema.rs` provide the ground truth for these tables.

### Other Database Systems

*   Based on the review of `schema.rs` and `interactions.rs`, Orchestr8 primarily uses **SQLite**.
*   `schema.rs` details the main application database (`scaffolder_data.sqlite`) and also mentions a separate `history.sqlite` created per LLM entity for interaction logs. No other database systems (e.g., PostgreSQL, MongoDB) are indicated in these core database files.

### Frontend Stores/Services Abstracting Database Interactions

*   **`src/stores/llmStore.ts`**: As previously detailed, this store manages `LlmEntities` (LLM configurations) and invokes Tauri commands for CRUD operations on them (e.g., `get_llm_entities`, `get_llm_entity_config`, `add_llm_entity`, `update_llm_entity`, `delete_llm_entity`). These commands interact with the `LlmEntities` table in the SQLite database.
*   **`src/stores/integr8Store.ts`**: This store manages `Integr8_Engineers`, `Integr8_Tasks`, and `Integr8_Task_Results`. It uses Tauri commands like `get_integr8_engineers`, `create_integr8_engineer`, `assign_integr8_task`, `get_integr8_task_status`, `store_integr8_task_result` which perform CRUD operations on the respective SQLite tables.
*   **`src/stores/chatStore.ts`**: (Presence inferred from open tabs and `database/interactions.rs`). This store likely handles chat functionalities. It would interact with Tauri commands (derived from functions in `database/interactions.rs`) such as:
    *   A command to persist new chat messages (using `persist_interaction`).
    *   A command to fetch chat history (using `get_chat_history`).
    *   Commands to update message statuses or find failed messages (using `update_message_status`, `find_last_failed_message`).
    These operations target the `InteractionHistory` table.

### Relevant Tauri Commands for Database Operations

Based on the frontend stores and backend Rust files (`integr8Store.ts`, `llmStore.ts`, `database/interactions.rs`, `workflow_engine/db.rs`), the following Tauri commands related to database operations can be identified or strongly inferred:

**For `LlmEntities` (LLM Configurations - likely from `llm_commands.rs` or `settings_commands.rs`):**
*   `get_llm_entities`: Fetches all LLM entity minimal representations.
*   `get_llm_entity_config` (or similar like `get_llm_entity` from `interactions.rs`): Fetches detailed configuration for a specific LLM entity.
*   `add_llm_entity`: Adds a new LLM entity configuration.
*   `update_llm_entity`: Updates an existing LLM entity configuration.
*   `delete_llm_entity`: Deletes an LLM entity.
*   `test_llm_api_connection` (from `llmStore.ts`): While not directly a CRUD op, it reads entity config to test.
*   `get_openrouter_models` (from `llmStore.ts`): Fetches models, potentially caching or interacting with a list in DB.

**For `Integr8_Engineers`, `Integr8_Tasks`, `Integr8_Task_Results` (likely from `integr8_commands.rs` or similar):**
*   `get_integr8_engineers`: Fetches all Integr8 engineers.
*   `create_integr8_engineer`: Creates a new Integr8 engineer.
*   `assign_integr8_task`: Creates and assigns a new task to an engineer.
*   `get_integr8_task_status`: Fetches the status and details of a specific task.
*   `update_integr8_task_progress`: Updates the progress and status of a task.
*   `store_integr8_task_result`: Stores the result of a completed task.

**For `InteractionHistory` (Chat - likely from `chat_commands.rs` or `interaction_commands.rs`):**
*   `persist_interaction_record` (or similar): Saves a new chat message/interaction. (Derived from `persist_interaction` in `interactions.rs`)
*   `get_chat_history`: Retrieves chat history. (Derived from `get_chat_history` in `interactions.rs`)
*   `update_message_status`: Updates a message's status. (Derived from `update_message_status` in `interactions.rs`)
*   `find_last_failed_user_message`: Finds the last user message that failed. (Derived from `find_last_failed_message` in `interactions.rs`)

**For `UserProfiles` (User Profile Management - likely from `user_profile_commands.rs`):**
*   `get_user_profile`: (from `database/user_profile.rs` re-export)
*   `upsert_user_profile`: (from `database/user_profile.rs` re-export)

**For General Workflow System (from `workflow_engine/db.rs`, exposed via various command modules):**
*   Commands related to creating and managing `Workflow_Definitions`, `Workflow_Steps`, `Workflow_Instances`, and `Workflow_Step_Instances`. Examples from `workflow_engine/db.rs` include:
    *   `create_workflow_instance`
    *   `find_start_steps`
    *   `queue_step_execution`
    *   `update_instance_status`
    *   `update_step_instance_status`
    *   `get_step_definition`
    *   `get_instance_context`
    *   `check_dependencies`
    *   `check_if_workflow_complete`

This list is not exhaustive but covers the primary database-interacting commands inferred from the analyzed files. The exact command names might vary slightly in `main.rs` or specific command modules.

## Core Frontend Services & Composables

This section investigates common frontend services and Vue composables.

### Graph Data Management (Potential `UniversalGraphService` Precursor)

The file `src/types/graph.ts` defines a rich set of TypeScript interfaces for graph data structures, strongly indicating client-side graph management capabilities. This could be a precursor to or form the foundation of a `UniversalGraphService`.

**Key Interfaces from `src/types/graph.ts`:**

*   **`GraphNode`**: Represents a node in the graph (e.g., component, file, module).
    *   `id: string`
    *   `label: string`
    *   `type: string` (e.g., 'component', 'store')
    *   `filePath?: string`
    *   `metrics?: NodeMetrics` (incoming/outgoing connections, complexity)
    *   Visual properties (`color`, `size`) and optional metadata.

*   **`GraphEdge`**: Represents a connection between nodes.
    *   `id: string`
    *   `source: string` (source node ID)
    *   `target: string` (target node ID)
    *   `type?: string` (e.g., 'import', 'stores-usage')
    *   `weight?: number`
    *   Visual properties and optional metadata.

*   **`GraphData`**: The complete graph structure.
    *   `nodes: GraphNode[]`
    *   `edges: GraphEdge[]`
    *   `metadata?: object` (generation timestamp, project ID, etc.)

*   **Supporting Interfaces**:
    *   `LayoutType`: Defines supported graph layouts ('force-directed', 'circular', etc.).
    *   `NodeMetrics`: For analytics on nodes.
    *   `GraphFilterOptions`: For filtering nodes and edges based on various criteria.
    *   `GraphViewState`: For saving and restoring the visual state of the graph (layout, zoom, pan, selection, filters).
    *   `GraphExportOptions`: Defines options for exporting the graph (format, metadata, dimensions).
    *   `GraphInstance`: A generic interface to represent the instance of the chosen graph visualization library (D3.js, VisNetwork, Cytoscape.js are mentioned as possibilities).

**Implications:**
The presence of these detailed types suggests that Orchestr8 has a robust system for representing, visualizing, and potentially manipulating graph data on the frontend. While a specific file named `UniversalGraphService.ts` hasn't been located yet, these types would be essential for such a service. Views like `ConnectionGraphView.vue` (seen in open tabs) likely consume and render data conforming to these types.

### Event Bus Service

*   No explicit `EventBusService.ts`, `emitter.ts`, or similar dedicated event bus file has been identified in `src/composables` or `src/lib`.
*   The `src/composables` directory currently only contains `useWebRTC.ts`.
*   The `src/lib/utils.ts` file contains various utility functions (timestamp formatting, input sanitization, debounce, ID generation) but does not include an event emitter or bus.
*   It's possible that global eventing is handled through other means (e.g., Pinia store actions acting as event relays, Vue's built-in provide/inject, or direct component-to-component events) or that a dedicated event bus is not a central pattern in this part of the application.

### Cache Service

*   A search for TypeScript files (`*.ts`) within the `src` directory with "cache" in their name yielded no results.
*   This suggests that there isn't a dedicated, centralized `CacheService.ts` file.
*   Caching mechanisms might be:
    *   Handled by specific data-fetching libraries if used (e.g., TanStack Query/Vue Query, though not yet identified).
    *   Implemented ad-hoc within individual Pinia stores or composables (e.g., storing fetched data in `ref` or `reactive` state variables and re-fetching based on certain conditions).
    *   Leveraged through browser caching for static assets, but this is different from an application-level data cache service.
*   Further investigation into individual stores that fetch data might reveal specific caching patterns.

### Authentication/Authorization and Secure Key Management

*   **`src/lib/maestro_security.ts`**: This file implements secure key storage using `@tauri-apps/plugin-stronghold`.
    *   **Purpose**: To encrypt and decrypt sensitive data, primarily API keys, ensuring they are not stored in plaintext.
    *   **Key Functions**:
        *   `initializeStronghold()`: Sets up the Stronghold vault (`maestro-vault.hold`) and client. It uses a hardcoded password (`maestro-secure-password`) for the vault, noting that a more secure approach should be considered for production.
        *   `encryptKey(key: string): Promise<string>`: Takes a string (e.g., an API key), encrypts it using Stronghold, and stores it. It returns a `keyId` (a reference to the stored key) rather than the encrypted data itself. It includes a fallback to Base64 encoding if Stronghold initialization or encryption fails.
        *   `decryptKey(keyId: string): Promise<string>`: Takes a `keyId`, retrieves the encrypted data from Stronghold, and decrypts it. It also includes logic to handle direct Base64 encoded strings as a fallback, likely for compatibility with keys stored before Stronghold integration.
    *   **Usage**: This service is likely used by `llmStore.ts` or similar stores/services when saving LLM configurations that include API keys. Instead of storing the raw API key, the `keyId` returned by `encryptKey` would be stored in the database (e.g., in the `LlmEntities.api_key` field, which was noted in the schema as potentially storing a placeholder or reference). When an API call needs to be made, the `keyId` is used to `decryptKey` to retrieve the actual API key just-in-time.
    *   **Limitations for Auth**: This service focuses on credential/secret management. It does not appear to handle user authentication (login sessions, user identity) or role-based authorization within the application itself. Those aspects might be managed by other systems or are simpler in the current architecture (e.g., relying on local user context without explicit login, or user roles defined in a database table like `Users` or `UserProfiles` if they exist). The `UserProfiles` table in `schema.rs` suggests user identity management, but the direct link to authentication flow isn't clear from `maestro_security.ts` alone.

### Advanced File System Operations

While a dedicated frontend service file (e.g., `fileSystemService.ts`) has not been explicitly identified, the backend provides several Tauri commands for advanced file system operations, defined in `src-tauri/src/commands/fs_commands.rs`. Frontend stores or components likely call these commands directly.

*   **Key Tauri Commands from `src-tauri/src/commands/fs_commands.rs`**:
    *   **`get_file_tree(project_root: String) -> CommandResult<Vec<FileNode>>`**:
        *   Recursively scans the directory at `project_root`.
        *   Returns a tree structure composed of `FileNode` objects. Each `FileNode` includes:
            *   `key: String` (full path)
            *   `label: String` (file/directory name)
            *   `is_leaf: bool`
            *   `children: Option<Vec<FileNode>>` (for directories)
        *   This command uses `walkdir` for traversal and `spawn_blocking` for asynchronous execution.
        *   It's a significant abstraction over basic `fs.readDir` as it provides the entire nested structure.
        *   Likely used by UI components like file explorers (e.g., potentially by `explorerStore.ts` or `Orchestr8DirectoryManager.vue`).

    *   **`read_file_binary(path: String) -> CommandResult<Vec<u8>>`**:
        *   Reads the specified file and returns its content as a byte array (`Vec<u8>`).
        *   Useful for handling non-text files or when specific encoding/decoding is needed on the frontend.

    *   **`create_daco_project_directory(path: String) -> CommandResult<()>`**:
        *   Creates a directory at the given `path`, including any necessary parent directories (similar to `mkdir -p`).
        *   The "daco" prefix suggests a specific use case within the application.

*   **Frontend Usage**:
    *   Instead of a dedicated frontend service, Pinia stores like `explorerStore.ts` (if it manages file tree state) or components themselves likely `invoke` these Tauri commands directly to interact with the file system in these more advanced ways.
    *   This approach centralizes the complex FS logic in the Rust backend, exposing a clear API to the frontend.

### Managing Application-Wide Settings or Configurations

*   **`src/stores/settingsStore.ts`**: This Pinia store is the primary mechanism for managing application-wide settings.
    *   **Purpose**: To hold and manage various user-configurable settings for the application.
    *   **Managed Settings (State)**:
        *   `theme: Ref<'light' | 'dark'>`: Stores the current theme preference. The store notes that `themeStore.ts` might be responsible for the actual UI toggling. Default is 'light'.
        *   `aiCreativityLevel: Ref<number>`: An example setting, defaults to `0.7`.
        *   `isContextAwarenessEnabled: Ref<boolean>`: Manages a context awareness feature flag. Default is `false`.
        *   `isNetworkingEnabled: Ref<boolean>`: Manages whether networking features are enabled. This state is initialized from and synchronized with the backend via Tauri commands. Default is `false` before initialization.
    *   **Key Actions**:
        *   `setTheme(newTheme: 'light' | 'dark')`: Updates the `theme` state. Includes a TODO for persistence.
        *   `setAiCreativity(level: number)`: Updates `aiCreativityLevel`. Includes a TODO for persistence.
        *   `toggleContextAwareness()`: Toggles `isContextAwarenessEnabled`. Includes a TODO for persistence.
        *   `initNetworkStatus()`: Asynchronously fetches the current networking status from the backend using the Tauri command `is_networking_enabled` and updates `isNetworkingEnabled`.
        *   `toggleNetworking()`: Asynchronously toggles the networking status by calling the Tauri command `set_networking_enabled` with the new desired state. Updates `isNetworkingEnabled` based on the backend's response.
        *   `loadSettings()`: Called on store initialization. Currently, its main role is to call `initNetworkStatus()`. Includes a TODO to load other settings.
    *   **Associated Tauri Commands** (likely defined in `src-tauri/src/commands/settings_commands.rs`):
        *   `is_networking_enabled`: Returns `boolean`.
        *   `set_networking_enabled(enabled: boolean)`: Returns `boolean` (previous state).
    *   **Persistence**:
        *   Networking status (`isNetworkingEnabled`) is persisted via backend Tauri commands.
        *   Other settings (`theme`, `aiCreativityLevel`, `isContextAwarenessEnabled`) have TODO comments indicating that their persistence mechanism (e.g., to localStorage or a general backend settings table) might not be fully implemented in this store or is handled elsewhere.
*   **`src-tauri/src/commands/settings_commands.rs`**: (Presence inferred from open tabs and `settingsStore.ts` actions). This backend Rust file likely defines the Tauri commands (`is_networking_enabled`, `set_networking_enabled`) that the `settingsStore.ts` invokes to manage the persisted state of network settings. Other application settings might also be managed here if they require backend persistence.

## UI Component Library & Patterns

This section details existing UI components and common patterns, with a focus on Naive UI usage.

### Generic Graph Visualization Components

*   **`src/views/ConnectionGraphView.vue`**: This is a sophisticated Vue component dedicated to visualizing graph data.
    *   **Purpose**: Displays project structures, component relationships, and supports a special "Feature Extraction Mode" for visualizing and interacting with components relevant to a feature extraction task.
    *   **Technology Used**:
        *   **UI Framework**: Built extensively with **Naive UI** components (NCard, NButton, NSelect, NSpin, NEmpty, NIcon, NTooltip, NDescriptions, NDrawer, NDataTable, NTabs, etc.).
        *   **Graph Data Types**: Consumes graph data structures (`GraphData`, `GraphNode`, `GraphEdge`) defined in `src/types/graph.ts`.
        *   **Graph Rendering Library**: The specific rendering library (e.g., D3.js, Cytoscape.js, VisNetwork) is not hardcoded but is intended to be integrated within the `initializeGraph` method. Comments in the code mention these libraries as possibilities. The component prepares a `div` ( `graphContainerRef`) to host the visualization.
    *   **Key Features**:
        *   **Data Loading**: Fetches graph data dynamically, with placeholders for Tauri commands like `get_project_graph_data` or `get_feature_extraction_graph_data`.
        *   **Layouts**: Supports dynamic selection of various graph layouts (Force Directed, Circular, Hierarchical, Radial, Grid).
        *   **Interactivity**: Zooming, view reset.
        *   **Filtering**: Provides UI for filtering nodes/edges by type and toggling isolated nodes.
        *   **Export**: UI for exporting the graph (PNG, SVG, JSON), though the implementation logic is placeholder.
        *   **View State Persistence**: Placeholder logic for saving/loading graph view state (zoom, pan, layout), possibly via `localStorage`.
        *   **Node Details Panel**: Displays information about a selected node (label, type, path, metrics).
        *   **Navigation**: Can navigate to a file viewer or highlight files in an explorer view based on node selection.
        *   **Feature Extraction Mode**: Adapts its UI and functionality when `route.query.mode === 'extract-feature'`, including:
            *   Displaying task-specific information.
            *   A drawer for selecting "extractable components" using an `NDataTable`.
            *   A drawer for showing diff views.
            *   Actions to "mark components for extraction."
    *   **Pinia Stores Used**:
        *   `useProjectStore()`: To access the `currentProject`.
        *   `useIntegr8Store()`: In "Feature Extraction Mode" to fetch task details.
    *   **Overall**: This component is a central piece for any graph-based visualization in Orchestr8, providing a rich set of features and a flexible architecture for plugging in a graph rendering library.

### Code Editor Components

*   **`src/components/PrdEditor.vue`**:
    *   **Purpose**: This component is **not a generic code editor** for arbitrary file types. It serves as a dynamic, schema-driven editor for "Product Requirements Documents" (PRDs). PRDs appear to be structured data where fields are defined by a `_schema` object, specifying field types (Text, Long Text, Number, Boolean, Date), labels, etc.
    *   **Technology**: It dynamically renders Naive UI input components (`NInput`, `NInputNumber`, `NSwitch`, `NDatePicker`, `NTextarea`) based on the field types defined in the PRD's schema. It does **not** use Monaco Editor, CodeMirror, or similar code editing libraries.
    *   **Features**:
        *   Fetches PRD data for the current project (Tauri command: `get_current_prd`).
        *   Allows editing of existing PRD fields based on their schema-defined type.
        *   Supports adding new fields to the PRD schema (via an `AddFieldForm.vue` child component).
        *   Proposes changes to a PRD, integrating with a change request system (Tauri command: `propose_prd_update`; uses `ChangeRequestForm.vue` and `useChangeRequestStore`).
        *   Allows creation of an initial PRD if one doesn't exist for a project.
        *   Fields are grouped into collapsible sections.
    *   **Relevance to generic code editing**: While it's an editor, it's specialized for PRD data structures and does not provide general-purpose code editing features like syntax highlighting for various languages, code completion, etc.

*   **`src/components/FileViewerWrapper.vue`**:
    *   **Purpose**: This component acts as a file tree navigator. It displays a directory structure and allows users to select files.
    *   **Technology**:
        *   Uses Naive UI's `NTree` component to render the file tree.
        *   Fetches the file tree structure using the `get_file_tree` Tauri command (from `fs_commands.rs`).
    *   **Code Editing**: This component itself does **not** contain a code editor. When a file is selected, it instantiates and shows the `src/views/FileContentViewer.vue` component, passing the selected file's path and name to it.
    *   **Conclusion**: It's a wrapper/launcher for the actual file content viewer.

*   **`src/views/FileContentViewer.vue`**:
    *   **Purpose**: This component displays the content of a selected file within a modal. It is primarily a **viewer**, not an editor for general code files.
    *   **Technology for Code Display**:
        *   Uses Naive UI's **`<n-code>` component** for displaying text-based files, including source code.
        *   Provides syntax highlighting by dynamically setting the `language` prop of `<n-code>` based on file extension.
        *   Supports line numbers and word wrap via `<n-code>` props.
    *   **Image Display**: Can display common image formats (PNG, JPG, SVG, etc.) using an `<img>` tag. Fetches image data as a data URL via a Tauri command (`read_file_as_data_url`).
    *   **Editing Capabilities**: **None observed for file content.** This component does not implement features for modifying the displayed code or text. It does not integrate Monaco Editor, CodeMirror, or similar rich text/code editing libraries.
    *   **Features**:
        *   Modal presentation (`NModal`).
        *   Fetches file content using Tauri commands (`read_file_content` for text, `read_file_as_data_url` for images).
        *   "Copy Content" functionality for text files (uses `@tauri-apps/plugin-clipboard-manager`).
        *   "Open Externally" functionality to open the file with the system's default application (uses `@tauri-apps/plugin-shell`).
    *   **Conclusion**: Orchestr8 uses Naive UI's `<n-code>` for syntax-highlighted code *viewing*. There is no evidence in this component of an integrated, full-featured code editor for in-app modification of general project files.

### Common UI Element Patterns (Naive UI)

Orchestr8 heavily leverages the **Naive UI** component library for its user interface. The following patterns and components have been observed across various views and components:

*   **Lists/Trees**:
    *   `NTree`: Used in `FileViewerWrapper.vue` for displaying hierarchical file structures.
    *   `NDataTable`: Used in `ConnectionGraphView.vue` (within a drawer) for selecting "extractable components," indicating its use for tabular list data with selection.
*   **Forms**:
    *   `NForm` and `NFormItem`: Used in `PrdEditor.vue` for structuring input fields.
    *   Various Naive UI input components are used within forms:
        *   `NInput` (for text)
        *   `NTextarea` (via `NInput` in `PrdEditor.vue`)
        *   `NInputNumber`
        *   `NSwitch` (for boolean toggles)
        *   `NDatePicker`
        *   `NSelect` (e.g., in `ConnectionGraphView.vue` for layout selection)
*   **Modals**:
    *   `NModal` (with `preset="card"`): Used in `FileContentViewer.vue` to display file content and in `PrdEditor.vue` to host the `ChangeRequestForm`. This is the standard way modals are implemented.
*   **Drawers**:
    *   `NDrawer` and `NDrawerContent`: Used in `ConnectionGraphView.vue` for the "Component Selection" and "Diff View" panels, indicating their use for side panels that slide out.
*   **Tables**:
    *   `NDataTable`: As mentioned under Lists, used for structured tabular data display with features like selection and pagination (implied by `pagination="{ pageSize: 10 }"` in `ConnectionGraphView.vue`).
*   **Notifications/Messages**:
    *   `useMessage()` (Naive UI hook): Used in `ConnectionGraphView.vue`, `PrdEditor.vue`, and `FileContentViewer.vue` to display global messages/notifications (e.g., `message.success()`, `message.error()`, `message.warning()`, `message.info()`). This is the standard pattern for user feedback.
    *   `NAlert`: Used for displaying more persistent, inline informational messages or errors (e.g., in `FileContentViewer.vue` for file loading errors, `FileViewerWrapper.vue` for status messages).
*   **Buttons**:
    *   `NButton`, `NButtonGroup`: Used extensively for actions, often with icons (`NIcon`). Examples include zoom controls, save, cancel, refresh, export, etc.
*   **Layout & Structure**:
    *   `NCard`: Frequently used to group content sections (e.g., controls bar in `ConnectionGraphView.vue`, node details panel).
    *   `NSpace`: Used for managing spacing and alignment of child elements (e.g., button groups, form actions).
    *   `NCollapse` and `NCollapseItem`: Used in `PrdEditor.vue` to organize form fields into collapsible sections.
    *   `NDivider`: Used for visual separation.
    *   `NSpin`: Used to indicate loading states (e.g., `ConnectionGraphView.vue`, `FileViewerWrapper.vue`, `FileContentViewer.vue`).
    *   `NEmpty`: Used to provide user-friendly messages when no data is available (e.g., no graph data, empty file tree).
    *   `NTag`: Used for displaying status labels or file extensions (e.g., in `FileContentViewer.vue`).
    *   `NTooltip`: Used to provide contextual help for buttons/icons.
    *   `NDescriptions` and `NDescriptionsItem`: Used for displaying key-value information (e.g., selected node details in `ConnectionGraphView.vue`).
    *   `NScrollbar`: Used for scrollable content areas.

**Overall Pattern**: The application consistently uses Naive UI components for building its interface, indicating a standardized approach to UI development. Complex views are composed by combining these standard Naive UI elements.

### Project Selector and File/Directory Tree View

*   **Project Selector**:
    *   The `src/stores/projectStore.ts` manages the list of projects (`projects` ref) and the currently selected project (`currentProject` ref). It provides actions like `loadProjects()` and `setCurrentProject()`.
    *   The `src/components/AppHeader.vue` component *displays* the `currentProjectId` (passed as a prop) but **does not contain a UI element (e.g., dropdown) for selecting or changing projects.**
    *   **Conclusion**: A dedicated "Project Selector" dropdown or similar UI control has not yet been identified in common locations like the `AppHeader`. Project selection might occur in a dedicated settings view, a command palette, or be managed when opening/creating projects through other means.

*   **File/Directory Tree View**:
    *   **`src/components/FileViewerWrapper.vue`**: This component serves as the primary file and directory tree view.
        *   **Capabilities**:
            *   Uses Naive UI's `NTree` component for rendering the hierarchical tree.
            *   Fetches the file tree structure for the `currentProject`'s `root_path` using the `get_file_tree` Tauri command.
            *   Allows users to navigate directories and select files.
            *   When a file is selected, it launches `src/views/FileContentViewer.vue` to display its content.
            *   Includes a refresh button to reload the tree.
            *   Handles empty states (no project selected, empty directory).
            *   Displays file/folder icons.
        *   This component is a key part of any file exploration or navigation feature.

## State Management (Pinia Stores)

Orchestr8 utilizes Pinia for state management. Stores are typically defined in the `src/stores/` directory. Key stores identified so far include:

### `src/stores/projectStore.ts`

*   **Purpose**: Manages the list of projects, the currently active project, and project-specific operations like file scanning and connection verification.
*   **Primary State Properties**:
    *   `projects: Ref<Project[]>`: An array holding all known projects.
    *   `currentProject: Ref<Project | null>`: The currently selected project object.
    *   `verificationSummary: Ref<VerificationSummary | null>`: Stores the result of the last project connection verification.
    *   Loading flags: `isLoadingProjects`, `isCreatingProject`, `isScanning`, `isLoadingVerification`.
*   **Key Actions**:
    *   `loadProjects()`: Fetches all projects from the backend (Tauri command: `get_projects`).
    *   `createProject(name: string, rootPath: string)`: Creates a new project (Tauri command: `create_project`).
    *   `setCurrentProject(project: Project | null)`: Sets the active project.
    *   `scanProjectFiles(projectId: number, rootPath: string)`: Initiates a file scan for a project (Tauri command: `scan_project_files`).
    *   `runVerification(options: VerificationOptions)`: Runs connection verification for the current project (Tauri command: `run_project_verification`).
*   **Relevance**: Central to any feature that operates within a project context, including selecting a project for integration tasks.

### `src/stores/settingsStore.ts`

*   **Purpose**: Manages application-wide user-configurable settings.
*   **Primary State Properties**:
    *   `theme: Ref<'light' | 'dark'>`: Current theme preference (though `themeStore.ts` might handle the UI toggle).
    *   `aiCreativityLevel: Ref<number>`: Example AI-related setting.
    *   `isContextAwarenessEnabled: Ref<boolean>`: Feature flag for context awareness.
    *   `isNetworkingEnabled: Ref<boolean>`: Controls networking features, synchronized with the backend.
*   **Key Actions**:
    *   `setTheme(newTheme: 'light' | 'dark')`: Updates theme.
    *   `setAiCreativity(level: number)`: Updates AI creativity level.
    *   `toggleContextAwareness()`: Toggles context awareness.
    *   `initNetworkStatus()`: Fetches networking status from backend (Tauri command: `is_networking_enabled`).
    *   `toggleNetworking()`: Toggles networking status via backend (Tauri command: `set_networking_enabled`).
    *   `loadSettings()`: Initializes settings, currently focused on network status.
*   **Relevance**: Provides access to global application settings that might influence how the `Integr8` feature or its underlying LLM interactions behave.

*(Note: `llmStore.ts` and `integr8Store.ts` have been detailed previously under the "LLM Integration Architecture" section.)*

### `src/stores/chatStore.ts`

*   **Purpose**: Manages the state for the chat interface, including message history, AI thinking status, user input, selection of active LLM entities for chat, an "Observe Mode," and an "Intercom" feature for quick access to configured LLMs/colleagues.
*   **Primary State Properties**:
    *   `chatHistory: Ref<InteractionRecord[]>`: Stores the list of chat messages.
    *   `isAiThinking: Ref<boolean>`: Indicates if an AI response is currently being generated.
    *   `currentMessage: Ref<string>`: Holds the content of the user's current input in the chat box.
    *   `availableLlmEntities: Ref<LlmEntity[]>`: List of LLM entities that can be used in the chat.
    *   `activeLlmEntityIds: Ref<Set<string>>`: A `Set` containing the IDs of LLM entities currently active/selected for participation in the chat.
    *   `isObserveModeEnabled: Ref<boolean>`: A flag to enable/disable an "Observe Mode."
    *   `intercomConfig: Ref<(IntercomSlotConfig | null)[]>`: An array (10 slots) for configuring quick-access "Intercom" slots, each potentially assigned to an LLM entity.
    *   `colleagueStatuses: Ref<ColleagueStatus[]>`: Stores real-time status information for "colleagues" (potentially other users or specialized AI agents).
*   **Key Actions**:
    *   **Chat Management**: `addMessage()`, `setAiThinking()`, `clearChatHistory()`.
    *   **LLM Selection for Chat**:
        *   `loadLlmEntities()`: Fetches available LLM entities (Tauri command: `get_llm_entities`).
        *   `toggleEntityActive(entityId: string)`: Adds or removes an LLM entity from the set of active participants in the chat.
        *   `toggleObserveMode()`: Toggles the observe mode.
    *   **Intercom Management**:
        *   `fetchIntercomConfig()`: Loads the Intercom slot configurations from the backend (Tauri command: `get_intercom_config`).
        *   `updateIntercomSlotConfig(index: number, config: IntercomSlotConfig | null)`: Updates a specific Intercom slot's configuration (Tauri command: `update_intercom_slot_config`).
    *   **Colleague Status**:
        *   `loadInitialColleagueStatuses()`: Fetches initial statuses (Tauri command: `get_initial_colleague_statuses`).
        *   `updateColleagueStatus(statusUpdate: ColleagueStatus)`: Updates a colleague's status (intended for real-time updates, e.g., via WebSockets).
*   **Relevance**: This store is central to user-LLM chat interactions. The `activeLlmEntityIds` and `intercomConfig` directly relate to how different LLMs are selected and utilized for communication. The "Observe Mode" might also be relevant for understanding LLM behavior during integration tasks.

### `src/stores/changeRequestStore.ts`

*   **Purpose**: Manages "Change Requests" within a project, likely related to PRD updates or other formal change proposals. It handles fetching, displaying details, and processing approvals or rejections of these requests.
*   **Primary State Properties**:
    *   `changeRequests: Ref<ChangeRequest[]>`: An array of change requests for the current project context.
    *   `selectedChangeRequest: Ref<ChangeRequest | null>`: The currently selected change request object.
    *   `isLoading: Ref<boolean>`: Indicates if change request operations are in progress.
    *   `error: Ref<string | null>`: Stores error messages from operations.
*   **Key Getters**:
    *   `hasPendingChanges: ComputedRef<boolean>`: A computed property that checks if any change requests have a 'pending' status.
*   **Key Actions**:
    *   `fetchChangeRequests(projectId: number)`: Loads all change requests for a specified project ID (Tauri command: `get_change_requests`).
    *   `fetchChangeRequestDetails(requestId: number)`: Retrieves the full details of a single change request (Tauri command: `get_change_request_details`).
    *   `approveRequest(requestId: number)`: Approves a specified change request (Tauri command: `approve_change_request`).
    *   `rejectRequest(requestId: number, reason: string | null)`: Rejects a specified change request, with an optional reason (Tauri command: `reject_change_request`).
    *   `clearStore()`: Resets the store to its initial state.
*   **Associated Tauri Commands**:
    *   `get_change_requests`
    *   `get_change_request_details`
    *   `approve_change_request`
    *   `reject_change_request`
*   **Dependencies**:
    *   Uses a `ChangeRequest` type from `src/types/changeRequest.ts`.
    *   Likely interacts with functionality in `PrdEditor.vue` where changes are proposed.
*   **Relevance**: Important for understanding the workflow around modifications to core project documents like PRDs. The `Integr8` feature might need to interact with this system if it proposes changes to such documents or if its operations are gated by an approval process.

### `src/stores/dacoStore.ts`

*   **Purpose**: Manages state related to a feature or toolset codenamed "DAC-O." This appears to involve the execution of specific DAC-O commands (potentially for scaffolding or code generation, e.g., `scaffold_feature_from_prd`) and tracking their output and status.
*   **Primary State Properties**:
    *   `lastOutput: Ref<string>`: Stores the output string from the most recently executed DAC-O command.
    *   `installPath: Ref<string>`: A configurable path, likely used as a target directory for DAC-O operations. Initialized with a placeholder value.
    *   `isCommandRunning: Ref<boolean>`: A flag indicating whether a DAC-O command is currently in progress.
    *   `commandError: Ref<string | null>`: Holds error messages resulting from DAC-O command execution.
*   **Key Actions**:
    *   `setLastOutput(output: string)`: Updates the `lastOutput` and resets error/loading states.
    *   `setInstallPath(path: string)`: Sets the `installPath`.
    *   `setCommandRunning(isRunning: boolean)`: Manages the `isCommandRunning` flag.
    *   `setCommandError(error: string | null)`: Sets an error message and indicates command completion.
*   **Tauri Command Interaction**: This store does not directly invoke Tauri commands. It is designed to be updated by other UI components or services that execute DAC-O related commands. These external pieces of code would use this store's actions to reflect the status and results of those commands.
*   **Relevance**: If the "Integr8 Feature" involves automated code generation, project scaffolding, or similar operations that might be part of the "DAC-O" toolset, this store provides context on how such operations are managed at a high level in the UI. The `create_daco_project_directory` command found in `fs_commands.rs` is likely related.

### `src/stores/explorerStore.ts`

*   **Purpose**: This store is intended for managing state related to file exploration.
*   **Current Status**: As of the review, this store is largely a **placeholder**.
    *   It defines a `FileNode` interface, consistent with the structure used by the `get_file_tree` Tauri command and components like `FileViewerWrapper.vue`.
    *   However, it currently returns an empty object (no shared state or actions are defined and exposed).
*   **State Management**: Comments within the file indicate that state related to the file tree (data, selection, loading status) is primarily managed locally within the component(s) that display the file explorer (e.g., `FileViewerWrapper.vue` or a potential `ExplorerView.vue`).
*   **Relevance**: While not actively used for shared state currently, its existence suggests a potential future direction. For now, file exploration logic and state appear to be component-localized.

### `src/stores/themeStore.ts`

*   **Purpose**: Manages the application's dark mode/light mode theme.
*   **Primary State Properties**:
    *   `isDarkMode: Ref<boolean>`: Holds the current state of dark mode. Initialized from `localStorage` (key: `darkMode`).
*   **Key Actions**:
    *   `setDarkMode(value: boolean)`: Updates `isDarkMode`, saves the preference to `localStorage`, and toggles a 'dark' CSS class on `document.documentElement` to apply the theme.
*   **Initialization**: An immediate watcher applies the theme (by adding/removing the 'dark' class) when the store is initialized.
*   **Relevance**: Controls the application's visual theme. The `settingsStore.ts` also contains a `theme` ref, which might indicate a shared responsibility or a slight duplication in theme state management that could be consolidated.

### `src/stores/userProfileStore.ts`

*   **Purpose**: Manages the user's profile information, including fetching and saving data to the backend.
*   **Primary State Properties**:
    *   `profile: Ref<UserProfileDetails | null>`: Holds the user's profile data (e.g., `userId`, `fullName`, `email`, `bio`, `otherPlatforms`).
    *   `isLoading: Ref<boolean>`: Loading state for profile operations.
    *   `error: Ref<string | null>`: Error messages from profile operations.
*   **Key Actions**:
    *   `fetchProfile()`: Fetches the user's profile using the Tauri command `get_user_profile_details`. Initializes a default local profile if none exists on the backend.
    *   `saveProfile(updatedProfileData: UserProfileDetails)`: Saves updated profile data to the backend via the `update_user_profile_details` Tauri command.
*   **Associated Tauri Commands**:
    *   `get_user_profile_details`
    *   `update_user_profile_details`
*   **Relevance**: Provides user identity information which could be used for attribution, personalization, or potentially permissions related to the `Integr8` feature.

### `src/stores/uiState.ts` (as `useUiStateStore`)

*   **Purpose**: This is a major store responsible for managing the global UI layout, visibility of different panels, active components within those panels, and some general UI states.
*   **Primary State Properties**:
    *   **File Tree Related**: `currentProjectRoot`, `fileTreeData` (for a file tree panel), `selectedNodeKey`.
    *   **General UI**: `isLoading` (general loading), `statusMessage`, `theme` (duplicates/complements `themeStore.ts`).
    *   **Multi-Panel Layout**:
        *   `panelVisibility`: A reactive object tracking visibility for up to 6 panels (`topLeft`, `topMiddle`, `topRight`, `bottomLeft`, `bottomMiddle`, `bottomRight`).
        *   `sidePanelWidths`: Manages widths of left/right side panels.
        *   `verticalLayoutState`: Controls vertical sizing ('default', 'topMax', 'bottomMax').
        *   `isMiddleColumnHorizontallyExpanded`: Flag for expanding the middle column.
        *   `activeTopLeftComponent`, `activeTopRightComponent`, `activeTopMiddleComponent`: Strings indicating which dynamic Vue component should be rendered in these respective panel areas.
        *   `selectedTopLeftEntityId`, `selectedTopRightEntityId`: IDs for entities displayed in top panels.
        *   `activeBottomLeftAction`, `activeBottomRightAction`: Tracks active actions in bottom panels.
*   **Key Actions**:
    *   Actions to manage file tree state: `setProjectRoot()`, `setFileTree()`, `setSelectedNode()`.
    *   Actions for general UI state: `setLoading()`, `setStatus()`, `setTheme()`.
    *   Extensive actions for managing the multi-panel layout:
        *   `togglePanelVisibility()`, `setPanelVisibility()`.
        *   `setSidePanelWidth()`.
        *   `setVerticalLayoutState()`.
        *   `toggleMiddlePanelHorizontalExpand()`.
        *   `setActivePanelComponent()` (for `topLeft`, `topRight`).
        *   `setActiveTopMiddleComponent()` (for `topMiddle`).
        *   `setSelectedPanelEntity()`.
        *   `setActiveBottomAction()`.
        *   `resetLayout()`.
    *   Placeholder actions for "IntercomBar" integration: `showPiCChat()`, `initiatePiCMessage()`.
*   **Relevance**: Crucial for understanding the application's overall UI structure. The `Integr8` feature will likely need to register its views/components with this store to be displayed in the appropriate UI panels (e.g., using `setActivePanelComponent` or `setActiveTopMiddleComponent`). The file tree state here might be used by `FileViewerWrapper.vue` or a main `ExplorerView.vue`.

### Common Patterns for Pinia Store Usage

Based on the reviewed store files and `src/main.ts`:

*   **Store Definition**:
    *   Stores are defined using the `defineStore` function from Pinia.
    *   The setup function syntax (`defineStore('storeName', () => { ... })`) is consistently used, leveraging Vue's Composition API (e.g., `ref`, `computed`, `reactive`).
    *   State, getters (as `computed` properties), and actions (as functions) are returned from the setup function.
    *   Example:
      ```typescript
      import { defineStore } from 'pinia';
      import { ref, computed } from 'vue';

      export const useExampleStore = defineStore('example', () => {
        const count = ref(0);
        const doubleCount = computed(() => count.value * 2);
        function increment() {
          count.value++;
        }
        return { count, doubleCount, increment };
      });
      ```

*   **Store Registration**:
    *   A global Pinia instance is created in `src/main.ts`: `const pinia = createPinia();`.
    *   This instance is then registered with the Vue application: `app.use(pinia);`.

*   **Store Usage**:
    *   Individual store modules (e.g., `projectStore.ts`, `chatStore.ts`) export their respective `useStoreName` hooks.
    *   The `src/stores/index.ts` file serves as a barrel file, re-exporting all individual store hooks. This allows components to import stores either directly from their module file or from the central `@/stores` path (assuming `@` is an alias for `src`).
    *   In Vue components or other composables/services, stores are accessed by calling their exported hook:
      ```typescript
      import { useExampleStore } from '@/stores/exampleStore'; // or '../stores/exampleStore'
      // ...
      const exampleStore = useExampleStore();
      // Access state: exampleStore.count
      // Access getters: exampleStore.doubleCount
      // Call actions: exampleStore.increment()
      ```
*   **Tauri Interaction**: Many stores interact with the Rust backend by `invoke`ing Tauri commands within their actions to fetch or persist data.
*   **Type Safety**: TypeScript interfaces are generally defined for store state and for the data structures passed to/from Tauri commands, promoting type safety.

## Routing (Vue Router)

The application uses Vue Router for navigation, configured in `src/router/index.ts`.

### View Registration

*   **Route Definitions**: Routes are defined in an array of `RouteRecordRaw` objects. Each route typically includes:
    *   `path: string`: The URL path (e.g., `/explorer`, `/graph`).
    *   `name: string`: A unique name for the route (e.g., `Explorer`, `ConnectionGraph`).
    *   `component: Component`: The Vue component for the view.
        *   **Eager Loading**: Some core components (like `ExplorerView` for the default route) are imported directly at the top of `index.ts`.
        *   **Lazy Loading**: Most views are lazy-loaded using dynamic `import()` statements (e.g., `component: () => import('../views/Integr8View.vue')`). This is a standard practice for code splitting and improving initial load time.
    *   `meta?: Record<string, any>`: Used for attaching metadata to routes, such as `meta: { title: 'Page Title' }`.
*   **History Mode**: `createWebHashHistory` is used, which is suitable for Tauri applications.
*   **Root Redirect**: The root path `/` redirects to `/explorer`.
*   **Scroll Behavior**: Custom scroll behavior is defined to scroll to the top on new navigations or restore position when using browser back/forward buttons.

### Navigation and Data Passing Patterns

*   **Programmatic Navigation**:
    *   Likely uses `router.push()` with either a path or a named route.
    *   Example observed in `ConnectionGraphView.vue`: `router.push({ path: '/explorer/file', query: { path: selectedNode.value.filePath }});`
*   **Declarative Navigation**:
    *   Standard `<router-link>` components are assumed to be used in templates for user-initiated navigation, though not directly visible in `index.ts`.
*   **Passing Data/State Between Views**:
    *   **Query Parameters**: This is an observed pattern. Data is passed via the `query` object in `router.push()`. For example, `ConnectionGraphView.vue` passes a file path as a query parameter. The `Integr8View` is also shown to receive `mode` and `task_id` as query parameters. Components access these via `route.query`.
    *   **Route Parameters**: While not explicitly defined in the provided `routes` array (e.g., `/user/:id`), this is a standard Vue Router feature and might be used elsewhere. If so, params would be part of the `path` string and accessible via `route.params`.
    *   **Props from Route**: The configuration to pass route params as component props (`props: true`) is not explicitly shown in the current route definitions but remains a possibility.
    *   **Pinia Stores**: Given the extensive use of Pinia, it is highly probable that complex or shared state between views is primarily managed through stores (e.g., `projectStore`, `uiStateStore`, `chatStore`). Views would access data directly from these stores upon activation rather than relying solely on router-based data passing for complex objects or persistent state.

## 7. Shared TypeScript Types (`src/types/`)

This category investigates globally shared TypeScript interfaces and type aliases defined within the `src/types/` directory that are relevant to the `Integr8` feature.

**Key Shared Types Relevant to `Integr8` (found in `src/types/`):**

1.  **LLM Configurations & Entities:**
    *   **`LlmEntityConfig`** (from `llmConfig.ts`): This is the primary, most comprehensive type for defining an LLM "Engineer" or configuration. It includes `id` (for the config entry), `project_id`, `model_id` (e.g., "gpt-4o"), `role_name`, `entity_type` ('Cloud' | 'Mock'), `llm_provider` (e.g., "OpenAI"), `system_prompt`, and `mock_response_payload`. Crucial for `Integr8`'s core functionality.
    *   **`LlmEntityConfigInput`** (from `llmConfig.ts`): Defines the data structure for creating or updating an `LlmEntityConfig` via forms or backend commands. Includes fields like `api_key` (handled securely by the backend).
    *   **`LlmEntityMinimal`** (from `llmConfig.ts`): A minimal representation (`id`, `name`, `entity_type`) of an LLM, likely used for populating lists or dropdowns where full details are not immediately needed.
    *   **`LlmEntity`** (from `chat.ts`): Similar to `LlmEntityMinimal`, providing `id`, `name`, `provider`, and `model`. Used in chat contexts for identifying and selecting LLMs.
    *   **`IntercomLlmConfig`** (from `intercom.ts`): A specialized LLM configuration structure (`role`, `model`, `system_prompt`, `temperature`, `entityId`) tailored for the "Intercom" feature, which provides quick access slots for LLMs/colleagues.

2.  **Interaction & Task Logging:**
    *   **`InteractionRecord`** (from `chat.ts`): A versatile type suitable for logging `Integr8` task steps, outputs, intermediate results, or any event stream. Key fields include `id`, `timestamp`, `sender` (which could be an `Integr8` Engineer ID), `content` (the actual log message or data), and `status`.

3.  **File & Code Structure Representation:**
    *   **`GraphNode`** (from `graph.ts`): Represents a file, component, module, or any other entity in a graph structure. Essential fields are `id`, `label`, `type` (e.g., 'file', 'component'), and an optional `filePath`. This serves as the `FileNode` concept and is vital if `Integr8` needs to process or visualize code/file relationships.

4.  **General Operation Results:**
    *   **`TestResult`** (from `llmConfig.ts`): A simple structure (`{ success: boolean; message: string; }`) for reporting the outcome of backend operations, such as connectivity tests. Potentially useful for indicating the success/failure of individual steps within an `Integr8` task.

5.  **Change Management (Potentially Related):**
    *   **`ChangeRequest`** (from `changeRequest.ts`): Defines the structure for a change request, including `id`, `projectId`, `status`, `proposedChanges`, etc. Relevant if `Integr8` tasks involve proposing or interacting with a formal change management system (e.g., for PRD updates).

**Types Mentioned as Examples but Not Explicitly Found as Standalone Interfaces in `src/types/`:**

*   **`Project`**:
    *   No dedicated `Project` interface (e.g., `ProjectType` or `ProjectDetails`) was found within the `src/types/` directory.
    *   However, the concept of a project is pervasive. A `projectId` (usually `number` or `string`) is a common field in many key types:
        *   `LlmEntityConfig` (from `llmConfig.ts`)
        *   `ChangeRequest` (from `changeRequest.ts`)
        *   `GraphData.metadata` (from `graph.ts`)
    *   The actual `Project` data structure is likely defined and managed within `src/stores/projectStore.ts` (which has a `projects: Ref<Project[]>` state) and its shape is inferred from backend responses to commands like `get_projects`.

*   **`AnalysisResult`**:
    *   A specific, generic `AnalysisResult` type for complex analysis outputs was not identified in `src/types/`.
    *   The `Integr8` feature, if it performs detailed analyses, might:
        *   Define its own specific result types tailored to the kind of analysis being performed.
        *   Utilize the `InteractionRecord` type (from `chat.ts`) to log textual or structured (e.g., JSON string in `content`) analysis results.
        *   Employ the simpler `TestResult` type (from `llmConfig.ts`) for basic success/failure reporting of analysis steps.
    *   The `TaskResult` type defined within `integr8Store.ts` (`{ id, task_id, result_type, content, created_at }`) is a strong candidate for storing more structured results from `Integr8` tasks, where `content` could hold serialized analysis data.

All identified globally relevant shared types are consistently defined within the `src/types/` directory, making it the central location for such definitions.

## 8. Tauri Command Architecture

Tauri commands in Orchestr8 form the bridge between the Rust backend and the Vue.js frontend, enabling frontend components and Pinia stores to invoke Rust functions and receive results. The architecture is characterized by modularity, standardized error handling, and clear data modeling.

### Command Registration and Organization

*   **Main Registration Point**: Commands are registered in `src-tauri/src/main.rs` using the `.invoke_handler(tauri::generate_handler![...])` method on the Tauri `Builder`. The `generate_handler!` macro takes a list of all command functions to be exposed.
*   **Modular Structure**:
    *   Commands are organized into separate Rust modules, primarily within the `src-tauri/src/commands/` directory (e.g., `fs_commands.rs`, `project_commands.rs`, `llm_chat_commands.rs`, `integr8_commands.rs`).
    *   The `src-tauri/src/commands/mod.rs` file declares these files as sub-modules and may re-export commands for easier access in `main.rs`.
    *   Some commands might also reside in other top-level modules like `src-tauri/src/maestro_modules/` (e.g., `seeg_engine.rs`).

### Conventions for Tauri Commands

Based on the review of `main.rs` and various command modules (`fs_commands.rs`, `project_commands.rs`, `db_commands.rs`, `llm_chat_commands.rs`, `integr8_commands.rs`, `seeg_engine.rs`, `error.rs`, `models.rs`):

1.  **Definition**:
    *   Commands are public asynchronous Rust functions: `pub async fn command_name(...) -> ...`.
    *   They are decorated with the `#[tauri::command]` attribute.

2.  **Naming**:
    *   Command function names consistently use `snake_case` (e.g., `get_file_tree`, `create_project`, `send_message`).
    *   Names often start with a verb indicating the action (get, create, update, delete, run, send, etc.).

3.  **Input Arguments**:
    *   **Simple Types**: Frontend arguments are passed as standard Rust types (e.g., `String`, `i64`, `i32`, `bool`, `usize`, `Vec<String>`, `Option<String>`).
    *   **Custom Structs**: For more complex inputs, commands accept custom Rust structs. These structs are typically defined in `src-tauri/src/models.rs` or sometimes within the specific module if the type is highly localized (e.g., `VerificationOptions` in `database.rs`, `Integr8Engineer` in `integr8_commands.rs`). These structs derive `serde::Deserialize` to be created from frontend JSON payloads.
    *   **Tauri `State`**: Commands can access shared application state (like database connections/paths or globally managed resources) by taking `state: tauri::State<'_, AppState>` as an argument. `AppState` is defined in `src-tauri/src/state.rs`.
    *   **Tauri `AppHandle`**: Commands can take `app_handle: tauri::AppHandle<R>` (where `R: Runtime`) to interact with the Tauri application instance (e.g., for event emission, window management), though it's often marked as unused if `State` provides sufficient access.

4.  **Return Types**:
    *   Commands consistently return a `CommandResult<T>`, which is a type alias for `Result<T, CommandError>` defined in `src-tauri/src/error.rs`.
    *   `T` represents the success payload type. This can be a simple Rust type, a collection (e.g., `Vec<MyStruct>`), a custom struct (often from `models.rs`), or `()` for commands that don't return data on success.
    *   `CommandError` is a comprehensive custom error enum (see below).

5.  **Asynchronous Operations & Blocking I/O**:
    *   Commands are `async fn`.
    *   For potentially blocking operations (especially file system I/O and database interactions), `tokio::task::spawn_blocking` is used to move the work to a dedicated thread pool. This prevents blocking the main asynchronous runtime, ensuring UI responsiveness.
    *   The result from `spawn_blocking` (a `JoinHandle`) is `await`ed, and its inner `Result` is typically propagated using `??`.

6.  **Error Handling**:
    *   The `CommandResult<T>` pattern ensures standardized error handling.
    *   The `CommandError` enum (defined in `src-tauri/src/error.rs` using `thiserror::Error`) covers a wide range of specific errors: database errors (`Rusqlite`), I/O errors (`Io`), task joining errors (`JoinError`), Tauri errors (`TauriError`), JSON parsing errors, and various application-specific errors (e.g., `LlmApiError`, `ProjectNotFound`, `NotImplemented`).
    *   `CommandError` implements `serde::Serialize` by converting the error to its string representation, allowing detailed error messages to be sent to the frontend.
    *   Standard Rust error propagation (the `?` operator) is used within command logic, with errors often being mapped to `CommandError` variants using `From` implementations or `map_err`.

7.  **Data Modeling & Serialization**:
    *   Data structures used as input arguments or return payloads are typically defined as Rust structs in `src-tauri/src/models.rs`.
    *   These structs derive `serde::Serialize` (for return types) and `serde::Deserialize` (for input arguments) to enable conversion to/from JSON for communication with the JavaScript frontend.
    *   `serde` attributes like `#[serde(rename_all = "camelCase")]` and `#[serde(skip_serializing_if = "Option::is_none")]` are used to align with frontend conventions and manage data representation.
    *   `serde_json::Value` is used for fields that require flexible JSON structures.

### Summary of Key Tauri Commands by Category

The following is a non-exhaustive list of representative commands, categorized by their primary function, based on `main.rs` and inspected command modules:

*   **File System I/O and Analysis**:
    *   `get_file_tree(project_root: String) -> CommandResult<Vec<FileNode>>`
    *   `read_file_binary(path: String) -> CommandResult<Vec<u8>>`
    *   `create_daco_project_directory(path: String) -> CommandResult<()>`

*   **Project Management (including PRD and Change Requests)**:
    *   `get_projects() -> CommandResult<Vec<Project>>`
    *   `create_project(name: String, root_path: String) -> CommandResult<Project>`
    *   `scan_project_files(project_id: i64, root_path: String) -> CommandResult<usize>`
    *   `run_project_verification(project_id: i64, options: VerificationOptions) -> CommandResult<VerificationSummary>`
    *   `get_current_prd(project_id: i64) -> CommandResult<Option<PrdVersion>>`
    *   `create_initial_prd(project_id: i64, user_id: String, initial_data: Value) -> CommandResult<PrdVersion>`
    *   `propose_prd_update(project_id: i64, prd_version_id: i64, proposed_changes: Value, user_id: String) -> CommandResult<ProposalResult>`
    *   `add_prd_field(project_id: i64, prd_version_id: i64, section_key: String, field_definition: NewFieldDefinition) -> CommandResult<()>`
    *   `add_prd_version(data: NewPrdVersionData) -> CommandResult<PrdVersion>`
    *   `add_change_request(data: NewChangeRequestData) -> CommandResult<i64>`
    *   `get_change_request_details(request_id: i64) -> CommandResult<Option<ChangeRequest>>`
    *   `update_change_request_status(request_id: i64, status: String, details: Option<Value>) -> CommandResult<()>`
    *   `get_change_requests_for_project(project_id: i64) -> CommandResult<Vec<ChangeRequest>>`

*   **Database Interactions (General)**:
    *   `get_all_reports_cmd() -> CommandResult<Vec<Report>>`
    *   `get_reports_by_type_cmd(report_type: String) -> CommandResult<Vec<Report>>`
    *   `get_report_by_id_cmd(id: i64) -> CommandResult<Option<Report>>`
    *   `store_report_cmd(report: Report) -> CommandResult<i64>`
    *   `delete_report_cmd(id: i64) -> CommandResult<usize>`
    *   (Many entity-specific commands also perform database interactions, e.g., `create_project`, `add_llm_entity`).

*   **LLM Calls & Configuration**:
    *   `send_message(message_content: String, active_entity_ids: Vec<String>) -> CommandResult<InteractionRecord>` (from `llm_chat_commands.rs`)
    *   `fetch_history(entity_id: String, limit: usize) -> CommandResult<Vec<InteractionRecord>>` (from `llm_chat_commands.rs`)
    *   `get_llm_entities() -> CommandResult<Vec<LlmEntityMinimal>>` (from `settings_commands.rs`)
    *   `get_llm_entity_config(entity_id: String) -> CommandResult<LlmEntityConfig>` (from `settings_commands.rs`)
    *   `add_llm_entity(config: LlmEntityConfigInput) -> CommandResult<String>` (from `settings_commands.rs`)
    *   `update_llm_entity(entity_id: String, config: LlmEntityConfigInput) -> CommandResult<()>` (from `settings_commands.rs`)
    *   `delete_llm_entity(entity_id: String) -> CommandResult<()>` (from `settings_commands.rs`)
    *   `test_network_connection() -> CommandResult<TestResult>` (from `settings_commands.rs`)
    *   `test_llm_api_connection(entity_id: String) -> CommandResult<TestResult>` (from `settings_commands.rs`)
    *   `get_openrouter_models() -> CommandResult<Vec<HashMap<String, String>>>` (from `settings_commands.rs`)

*   **Integr8 Feature Commands** (from `integr8_commands.rs`):
    *   `get_integr8_engineers() -> CommandResult<Vec<Integr8Engineer>>`
    *   `create_integr8_engineer(name: String, llm_entity_id: i64, specialization: String) -> CommandResult<Integr8Engineer>`
    *   `assign_integr8_task(engineer_id: i64, task_name: String, ...) -> CommandResult<i64>`
    *   `get_integr8_task_status(task_id: i64) -> CommandResult<Integr8Task>`
    *   `update_integr8_task_progress(task_id: i64, progress: f64, status: Option<String>) -> CommandResult<()>`
    *   `store_integr8_task_result(task_id: i64, result_type: String, content: String) -> CommandResult<i64>`

*   **SEEG Engine Interaction**:
    *   `start_seeg_execution(initial_step_id: String) -> CommandResult<String>` (from `maestro_modules::seeg_engine.rs`)

*   **User Profile Management** (from `user_profile_commands.rs`):
    *   `get_user_profile_details() -> CommandResult<Option<UserProfileDetails>>`
    *   `update_user_profile_details(profile_data: UserProfileDetails) -> CommandResult<()>`

*   **Scripting & Scaffolding** (from `script_commands.rs`):
    *   `list_cli_plugins() -> CommandResult<Vec<PluginInfo>>`
    *   `run_script_command(args: RunScriptArgs) -> CommandResult<String>`
    *   `scaffold_overview`, `scaffold_commands`, `scaffold_stores`, `scaffold_routes`, `scaffold_types`, `scaffold_ui`, `scaffold_files` (various specific scaffolding commands).

*   **Signaling & Real-time Communication** (from `signal_chat_commands.rs`):
    *   `signal_join(client_name: String) -> CommandResult<Uuid>`
    *   `signal_leave() -> CommandResult<()>`
    *   `signal_send(target_client_id: Uuid, message_type: String, payload: String) -> CommandResult<()>`
    *   `signal_get_clients() -> CommandResult<Vec<ClientInfo>>`

*   **Workflow Management** (from `maestro_workflow.rs`):
    *   `get_workflow_steps(definition_id: String) -> CommandResult<Vec<WorkflowStep>>`
    *   `add_workflow_step(step_data: WorkflowStep) -> CommandResult<String>`
    *   `update_workflow_step(step_data: WorkflowStep) -> CommandResult<()>`
    *   `complete_ui_step(step_instance_id: i64, output_data: Option<Value>) -> CommandResult<()>`

*   **Settings & Configuration** (from `settings_commands.rs`):
    *   `is_networking_enabled() -> CommandResult<bool>`
    *   `set_networking_enabled(enabled: bool) -> CommandResult<bool>`
    *   `get_intercom_config() -> CommandResult<Vec<Option<IntercomSlotConfig>>>`
    *   `update_intercom_slot_config(index: usize, config: Option<IntercomSlotConfig>) -> CommandResult<()>`
    *   `get_initial_colleague_statuses() -> CommandResult<Vec<ColleagueStatus>>`

*   **Legacy Chat Commands** (from `chat_commands.rs`):
    *   `legacy_fetch_history(entity_id: String, limit: usize, offset: usize) -> CommandResult<Vec<InteractionRecord>>`
    *   `legacy_retry_last_message(entity_id: String) -> CommandResult<InteractionRecord>`
    *   `legacy_clear_history_error(message_id: String) -> CommandResult<()>`

*   **Feature Extraction Commands** (from `feature_extraction_commands.rs`):
    *   `get_extractable_components(project_id: i64, feature_name: String) -> CommandResult<Vec<GraphNode>>`
    *   `verify_feature_extraction(project_id: i64, component_ids: Vec<String>) -> CommandResult<Value>`

This detailed command architecture enables robust and type-safe communication between the frontend and the Rust backend.

## 9. Existing Code Analysis & Integration Logic

This section investigates existing TypeScript/JavaScript logic for code analysis, particularly focusing on `integr8Handler.ts` and its associated parser plugins, as well as any other relevant backend analysis modules.

### `PRD Generator Outputs/Compiled/integr8handler.ts`

This TypeScript file (compiled to JavaScript and intended to be run by a Node.js-like environment, likely via `saveScaffoldReport.ts`) orchestrates a multi-faceted analysis process to generate an "Integration Report." It compares an "external project" against the "current project" (Orchestr8) focusing on specified "target pages" from the external project.

*   **Primary Purpose**: To analyze an external codebase in the context of the current Orchestr8 project and specific target files, then generate a comprehensive report.
*   **Execution Context**: It appears to be part of a CLI toolchain, invoked by `saveScaffoldReport.ts` (another compiled script in the same directory: `PRD Generator Outputs/Compiled/saveScaffoldReport.ts`). It uses CommonJS `require` for its dependencies (`path`, `fs-extra`).
*   **Key Inputs (`Integr8Args` interface)**:
    *   `externalProjectPath: string`: Path to the external codebase.
    *   `targetPages: string`: Comma-separated list of file paths (relative to `externalProjectPath`) that are the main focus.
    *   `outputDir: string`: Directory for the generated report.
    *   `targetPath?: string`: Path to the current Orchestr8 project (defaults to CWD), used for comparison.
*   **Primary Output**: A detailed textual report string, which is then passed to a `saveScaffoldReport` function (provided as an argument to `runIntegr8Command`) for file system persistence.

*   **Core Workflow**:
    1.  **Initialization**: Parses arguments, resolves paths.
    2.  **Parser Plugin Execution**:
        *   Dynamically loads and executes a series of "parser plugins" (JavaScript files expected to be in `PRD Generator Outputs/Compiled/prd src/`).
        *   Standard analysis types include: `overview`, `stores`, `routes`, `types`, `ui`, `commands`.
        *   Each parser plugin is expected to export an `analyzeDataFunction(projectPath, options)`.
        *   These analyses are run on both the `externalProjectPath` (with `currentProjectPath` passed as `comparePath` in options) and the `currentProjectPath` (without a `comparePath`).
    3.  **Target Page Content Retrieval**:
        *   Uses a dedicated `fileRetriever.js` parser plugin to fetch the content of the specified `targetPages` from the `externalProjectPath`.
    4.  **Migration Assistant Analysis**:
        *   After the initial analyses and file retrieval, the `migrationAssistantParser.js` plugin is invoked for *each* target page.
        *   It receives the analysis results from both projects and the content of the specific target page as input.
        *   The `migrationAssistantParser.js` is also expected to provide a `formatReportFunction` to structure its findings in the final report.
    5.  **Report Formatting & Saving**:
        *   Collects all results: general analyses for both projects, target page contents, and migration assistant outputs for each target page.
        *   Formats these into a single comprehensive text report.
        *   Calls the provided `saveScaffoldReport` function to save this report to the specified `outputDir`.

*   **Parser Plugins (`prd src/*.js`)**:
    *   Located in `PRD Generator Outputs/Compiled/prd src/`.
    *   Dynamically imported using `require(pathLib.join(__dirname, 'prd src', parserFilename))`.
    *   Each plugin must export an `analyzeDataFunction(projectPath, options): Promise<AnalysisResult<any>>`.
    *   The `options` object (`HandlerParserOptions`) can include `comparePath`, `filter`, `uiPattern`, etc., to guide the analysis.
    *   The `fileRetriever.js` plugin is used with `mode: 'path'` and an array of absolute file paths.
    *   The `migrationAssistantParser.js` is a key plugin that synthesizes information from other parsers and the target page content.

*   **Data Structure for Analysis Results (`AnalysisResult<T>`)**:
    *   A common structure is used for results from parsers:
        *   `AnalysisSuccess<T> = { success: true; data: T; }`
        *   `AnalysisError = { success: false; error: string; details?: any; }`
    *   The `data: T` field holds the specific structured output of a parser. For example, `fileRetriever`'s data contains a record of file paths to their content or error status. The structure of `T` varies per plugin.

*   **Role of `migrationAssistantParser.js`**:
    *   This plugin appears central to the integration analysis.
    *   It takes the context of a specific `targetPageContent` from the external project.
    *   It also receives the `externalAnalysisData` (results of `overview`, `stores`, etc., parsers run on the external project) and `currentAnalysisData` (results from the current Orchestr8 project).
    *   Its goal is likely to compare the target page with the patterns and structures found in both projects and provide migration/integration suggestions.
    *   It has its own `formatReportFunction` to present its findings, suggesting its output is more than just raw data.

This `integr8handler.ts` script provides a sophisticated, plugin-based system for analyzing an external project against the current Orchestr8 project, focusing on specific target files to generate an integration report.

#### Parser Plugin: `overview.js`

*   **Source**: `PRD Generator Outputs/Compiled/prd src/overview.js` (compiled from `overview.ts`)
*   **Purpose**: Generates a high-level overview of a project directory. This includes a file index, a summary of key configuration files (`package.json`, `vite.config.ts`, `tauri.conf.json`, `tsconfig.json`), identified entry points (`src/main.ts`, `src-tauri/src/main.rs`), core dependencies (from `package.json` and `Cargo.toml`), and a top-level directory structure.
*   **Key Function**: `analyzeDataFunction(targetPath, options)`
    *   `targetPath`: Absolute path to the project to analyze.
    *   `options.comparePath`: Optional absolute path to a second project for comparison.
*   **Analysis Logic**:
    *   Uses `fast-glob` to scan files in `src/`, `src-tauri/`, and the project root, ignoring common patterns like `node_modules`, `target`, etc.
    *   Reads and extracts basic information from key configuration files.
    *   Checks for the existence of predefined entry point files.
    *   Scans `package.json` and `src-tauri/Cargo.toml` for a predefined list of core frontend and backend dependencies.
    *   Lists top-level directories and sub-directories within `src/` and `src-tauri/`.
*   **Output Data Structure (`AnalysisResult.data` for `overview.js`)**:
    ```typescript
    // Inferred structure
    {
        primaryData: { // Data from targetPath
            targetPath: string;
            fileList: string[]; // Relative POSIX paths
            configSummary: string; // Formatted text summary
            entryPointSummary: string; // Formatted text summary
            dependencySummary: string; // Formatted text summary
            directorySummary: string; // Formatted text summary
        };
        compareData?: { // Data from options.comparePath, same structure as primaryData
            // ...
        };
        reportFileList: string[]; // Combined, sorted list of files from primary and (if comparing) compare (comparison files are prefixed with "[COMPARE] ")
        primaryFileList: string[]; // Unprefixed file list for primary target
    }
    ```
*   **Report Formatting**: Exports a `formatReportFunction(data)` that takes the analysis data and generates a detailed textual report with sections for the combined file index and summaries for both primary and (if applicable) comparison targets.
*   **Role in `integr8handler.ts`**: Provides foundational context about project structure and setup for both the external project and the current Orchestr8 project. This overview is likely used by the `migrationAssistantParser.js` to understand the broader context of the files being integrated.

#### Parser Plugin: `storeParser.js`

*   **Source**: `PRD Generator Outputs/Compiled/prd src/storeParser.js` (compiled from `storeParser.ts`)
*   **Purpose**: Analyzes Pinia store definition files (`.ts`) within a project using Abstract Syntax Tree (AST) parsing. It identifies `defineStore` calls and extracts details about each store.
*   **Key Function**: `analyzeDataFunction(targetPath, options)`
    *   `targetPath`: Absolute path to the project directory or a specific store file.
    *   `options.comparePath`: Optional absolute path to a second project/store file for comparison.
*   **Analysis Logic**:
    *   Uses `fast-glob` to find potential store files (typically in `src/stores/`, ignoring `index.ts` and test files).
    *   For each found file, it uses `@babel/parser` (with TypeScript plugin) to generate an AST.
    *   `@babel/traverse` is used to walk the AST and locate `defineStore` calls.
    *   It extracts:
        *   Store ID (the first argument to `defineStore`).
        *   The exported variable name if it's a named export.
        *   Whether the store uses the Options API or a Setup Function.
        *   For Options API stores: lists keys from `state` (object returned by state function), `getters` (object keys), and `actions` (object keys).
        *   For Setup Function stores: it analyzes the returned object from the setup function to identify `ref`/`reactive` variables (as state), `computed` properties (as getters), and returned functions (as actions).
*   **Output Data Structure (`AnalysisResult.data` for `storeParser.js`)**:
    ```typescript
    // Inferred structure
    {
        primaryStores: StoreInfo[]; // Array of stores found in targetPath
        compareStores?: StoreInfo[]; // Array of stores from options.comparePath
        primaryTargetPath: string;
        compareTargetPath?: string;
    }

    // Where StoreInfo is:
    {
        id: string | null; // Store ID
        filePath: string; // Relative path to the store file
        variableName?: string; // Exported variable name (e.g., useMyStore)
        isSetupStore: boolean; // True if it's a setup function store, false for options object
        stateKeys: string[]; // Names of state properties/refs
        getterKeys: string[]; // Names of getters/computed properties
        actionKeys: string[]; // Names of actions/functions
    }
    ```
*   **Report Formatting**: Exports a `formatReportFunction(data)` that generates a textual report detailing each store's properties for both primary and (if applicable) comparison targets. It also includes a summary of common and unique store IDs between the two projects.
*   **Role in `integr8handler.ts`**: This parser is crucial for understanding the state management patterns (Pinia stores) in both the external project and the current Orchestr8 project. This information is vital for the `migrationAssistantParser.js` to suggest how stores from an external project might be integrated or adapted.

#### Parser Plugin: `routeParser.js`

*   **Source**: `PRD Generator Outputs/Compiled/prd src/routeParser.js` (compiled from `routeParser.ts`)
*   **Purpose**: Analyzes Vue Router configuration files (e.g., `src/router/index.ts`) using AST parsing to identify and extract route definitions.
*   **Key Function**: `analyzeDataFunction(targetPath, options)`
    *   `targetPath`: Absolute path to the project directory or a specific router file.
    *   `options.comparePath`: Optional absolute path to a second project/router file for comparison.
*   **Analysis Logic**:
    *   Locates the router file (typically `src/router/index.ts` or `index.js`).
    *   Parses the file into an AST using `@babel/parser` (with TypeScript and JSX plugins).
    *   Traverses the AST with `@babel/traverse` to find the `routes` array, usually within a `createRouter({...})` call or a variable named `routes`.
    *   Recursively extracts route properties:
        *   `path`: The route path string.
        *   `name`: The route name string.
        *   `component`: The component associated with the route. It attempts to identify if it's an eagerly imported component (Identifier) or a dynamically imported one (`() => import('...')` or `import('...')`), extracting the import path for dynamic imports.
        *   `children`: Recursively parses nested route definitions.
*   **Output Data Structure (`AnalysisResult.data` for `routeParser.js`)**:
    ```typescript
    // Inferred structure
    {
        primaryRoutes: RouteDefinition[] | null; // Parsed routes for targetPath, or null on error
        compareRoutes?: RouteDefinition[] | null; // Parsed routes for comparePath, or null/undefined
        primaryRouterPath: string | null; // Path to the found primary router file
        compareRouterPath?: string | null; // Path to the found comparison router file
        primaryTargetPath: string;
        compareTargetPath?: string;
    }

    // Where RouteDefinition is:
    {
        path?: string;
        name?: string;
        component?: string; // e.g., "HomeView", "Dynamic(./views/AboutView.vue)"
        children?: RouteDefinition[];
    }
    ```
*   **Report Formatting**: Exports a `formatReportFunction(data)` that generates a textual report. It lists routes for the primary and (if applicable) comparison targets, showing path, name, component, and children. It also provides a summary of common and unique top-level route paths between the two projects.
*   **Role in `integr8handler.ts`**: Helps understand the navigation structure of the external project and the current Orchestr8 project. This is essential for the `migrationAssistantParser.js` to map or suggest how views and navigation from an external application might fit into Orchestr8.

#### Parser Plugin: `typeParser.js`

*   **Source**: `PRD Generator Outputs/Compiled/prd src/typeParser.js` (compiled from `typeParser.ts`)
*   **Purpose**: Lists TypeScript definition files (`.ts`) or, in a special mode, lists Product Requirement Document (PRD) files. For type files, it can load their content and supports filtering and comparison.
*   **Key Function**: `analyzeDataFunction(targetPath, options)`
    *   `targetPath`: Absolute path to the project directory or a specific `.ts` file.
    *   `options.filter`: If set to "Prd" (case-insensitive), it switches to PRD mode. Otherwise, this string is used to filter type files by relative path or content.
    *   `options.comparePath`: Optional path for comparison (for type files only, ignored in PRD mode).
*   **Analysis Logic**:
    *   **PRD Mode**: If `filter` is "Prd", it uses `fast-glob` to find all files in a `PRDs` subdirectory of `targetPath` and loads their content.
    *   **Types Mode**:
        *   Uses `fast-glob` to find `.ts` files, typically within `src/types` if `targetPath` is a directory.
        *   Loads content of these files. If a `filter` (other than "Prd") is provided, only files whose relative path or content (case-insensitively) matches the filter are included with content.
        *   If `comparePath` is given, the same process is applied to the comparison project.
    *   **Note**: Unlike `storeParser.js` or `routeParser.js`, this plugin **does not perform AST-level analysis** of the TypeScript type definition files. It primarily lists them and retrieves their raw content.
*   **Output Data Structure (`AnalysisResult.data` for `typeParser.js`)**:
    ```typescript
    // Inferred structure
    {
        mode: 'types' | 'prd';
        primaryFiles: FileInfo[]; // Array of {absolutePath, relativePath, content?, error?}
        compareFiles?: FileInfo[]; // If in types mode and comparePath provided
        primaryTargetPath: string;
        compareTargetPath?: string;
        filterUsed?: string; // Filter string used (undefined in PRD mode)
    }
    ```
*   **Report Formatting**: Exports a `formatReportFunction(data)` that lists the found files (and their content in code blocks) for the primary and (if applicable) comparison targets. For types mode with comparison, it also summarizes common and unique relative file paths.
*   **Role in `integr8handler.ts`**: Provides `integr8handler.ts` with a list and content of relevant TypeScript definition files (or PRD files). This allows the `migrationAssistantParser.js` to access type information from both projects, which is crucial for understanding data structures and ensuring type compatibility during integration.

#### Parser Plugin: `uiParser.js`

*   **Source**: `PRD Generator Outputs/Compiled/prd src/uiParser.js` (compiled from `uiParser.ts`)
*   **Purpose**: Analyzes Vue Single File Components (`.vue`) to identify which known UI libraries (e.g., NaiveUI, Vuetify) are imported and which specific components from those libraries are used.
*   **Key Function**: `analyzeDataFunction(targetPath, options)`
    *   `targetPath`: Absolute path to the project directory or a specific `.vue` file.
    *   `options.comparePath`: Optional absolute path to a second project/`.vue` file for comparison.
*   **Analysis Logic**:
    *   Uses `fast-glob` to find `.vue` files, typically within `src/components` and `src/views`.
    *   For each `.vue` file:
        *   Parses the SFC using `@vue/compiler-sfc` to get the `<script>` or `<script setup>` content.
        *   Parses this script content into an AST using `@babel/parser`.
        *   Traverses the AST with `@babel/traverse` to find `ImportDeclaration` nodes.
        *   Checks import sources against a predefined list of `KNOWN_UI_LIBRARIES` (e.g., 'naive-ui', 'vuetify', 'quasar').
        *   If a known library is imported, it records the library name and the names/aliases of imported components (e.g., `NButton`, `VTextField`).
    *   Categorizes components as 'View', 'Component', 'Sub-Component', or 'Other' based on their file path.
*   **Output Data Structure (`AnalysisResult.data` for `uiParser.js`)**:
    ```typescript
    // Inferred structure
    {
        primaryComponents: ComponentInfo[]; // Components from targetPath
        compareComponents?: ComponentInfo[]; // Components from options.comparePath
        primaryTargetPath: string;
        compareTargetPath?: string;
    }

    // Where ComponentInfo is:
    {
        relativePath: string;
        absolutePath: string;
        componentType: 'View' | 'Component' | 'Sub-Component' | 'Other';
        importedLibraries: LibraryUsage[];
    }

    // Where LibraryUsage is:
    {
        library: string; // e.g., "NaiveUI"
        importedComponents: { name: string; localName: string; }[]; // e.g., { name: "NButton", localName: "NButton" }
    }
    ```
*   **Report Formatting**: Exports a `formatReportFunction(data)` that generates a textual report. It lists Vue files (categorized by type) from the primary target that import known UI libraries, detailing which libraries and components are imported. For comparison, it provides a summary of commonly imported UI libraries and those unique to each target.
*   **Role in `integr8handler.ts`**: Identifies UI library dependencies and component usage patterns. This is critical for the `migrationAssistantParser.js` to assess UI compatibility and the effort required to integrate or adapt UI components from an external project, especially if different UI frameworks or versions are involved.

#### Parser Plugin: `commandParser.js`

*   **Source**: `PRD Generator Outputs/Compiled/prd src/commandParser.js` (compiled from `commandParser.ts`)
*   **Purpose**: This script is designed to analyze Tauri applications by identifying and cross-referencing Tauri commands. It looks for command declarations in Rust backend files (`#[tauri::command]`) and their corresponding invocations (`invoke('command_name')`) in frontend JavaScript/TypeScript/Vue files. It can also compare these findings between two different target paths.
*   **Key Function**: `analyzeDataFunction(targetPath, options)`
    *   `targetPath`: An absolute path to the primary project directory or a specific file to analyze.
    *   `options.comparePath` (optional): An absolute path to a secondary project directory or file for comparison.
*   **Analysis Logic**:
    1.  **Constants & Regex**: Defines default subdirectories for frontend code (`src`) and Tauri commands (`src-tauri/src/commands`). It uses `INVOKE_PATTERN` (handles `invoke<Type>(...)`) for frontend calls and `TAURI_COMMAND_PATTERN` (handles attributes/comments between decorator and `fn`) for backend declarations.
    2.  **`findInvokeCalls(basePath)`**: Scans frontend files (`.ts`, `.js`, `.vue`) using `fast-glob`, reads them, and uses `INVOKE_PATTERN` to extract command names and full invocation strings. Returns a `Map` of command names to arrays of `InvocationDetail` objects (`{ file: string, match: string }`).
    3.  **`findTauriCommandDeclarations(basePath)`**: Scans Rust files (`.rs`) recursively using `fast-glob`, reads them, and uses `TAURI_COMMAND_PATTERN` to extract command names and full declaration strings. Returns a `Map` of command names to objects (`{ file: string, match: string }`).
    4.  **`analyzeCommandData(targetPath, options)`**: Orchestrates the analysis. Calls `findInvokeCalls` and `findTauriCommandDeclarations` for the `targetPath` and, if provided, for `options.comparePath`. Structures the results.
    5.  **`formatCommandReport(data)`**: Formats the structured analysis data into a human-readable report. Lists invocations and declarations for primary and (if applicable) comparison targets. Includes a comparison summary (common/unique commands) and a cross-reference section for the primary target (invoked vs. declared).
*   **Output Data Structure (`AnalysisResult.data` for `commandParser.js`)**:
    ```typescript
    // Inferred structure
    interface InvocationDetail {
      file: string; // Path of the file where the invocation occurs
      match: string; // The full text of the invoke call
    }

    interface CommandInvocationInfo {
        details: InvocationDetail[]; // Array of invocation details
    }

    interface CommandDeclarationInfo {
      file: string; // Path of the file where the declaration occurs
      match: string; // The full text of the command declaration
    }

    interface CommandAnalysisData {
      primaryInvocations: { [commandName: string]: CommandInvocationInfo };
      primaryDeclarations: { [commandName: string]: CommandDeclarationInfo };
      compareInvocations?: { [commandName: string]: CommandInvocationInfo };
      compareDeclarations?: { [commandName: string]: CommandDeclarationInfo };
      primaryTargetPath: string;
      compareTargetPath?: string;
      primaryIsDirectory: boolean;
      compareIsDirectory?: boolean;
    }
    ```
*   **Role in `integr8handler.ts`**: This parser provides a detailed understanding of how the frontend and backend communicate via Tauri commands in both the external project and the current Orchestr8 project. This is essential for the `migrationAssistantParser.js` to analyze API surface compatibility, identify missing or mismatched commands, and guide the integration of backend-dependent features.

#### Parser Plugin: `fileRetriever.js`

*   **Source**: `PRD Generator Outputs/Compiled/prd src/fileRetriever.js` (compiled from `fileRetriever.ts`)
*   **Purpose**: Retrieves the content of specified files. It operates in "index" mode (using 1-based indices from a file list relative to a `targetPath`) or "path" mode (using absolute paths). It validates file existence, size (max 40KB), and skips common media/binary types.
*   **Key Function**: `analyzeDataFunction(targetPath, options)`
    *   `targetPath`: Base path context.
    *   `options.mode: 'index' | 'path'`: Retrieval mode.
    *   `options.indices?: string`: (For "index" mode) Comma-separated 1-based indices.
    *   `options.fileList?: string[]`: (For "index" mode) Array of relative file paths.
    *   `options.paths?: string[]`: (For "path" mode) Array of absolute file paths.
*   **Analysis Logic**:
    1.  **`readFileContent(absolutePath, filePathLabel)` (Helper)**: Checks existence, size, and media type. Reads UTF-8 content if valid. Returns `{ status, content }`.
    2.  **`analyzeDataFunction`**:
        *   **"index" mode**: Resolves indices against `fileList` and `targetPath`, then calls `readFileContent`.
        *   **"path" mode**: Iterates `options.paths`, calls `readFileContent`.
        *   Stores results keyed by index string or absolute path.
*   **Output Data Structure (`AnalysisResult.data` for `fileRetriever.js`)**:
    ```typescript
    // Inferred structure
    {
        results: {
            [identifier: string]: { // index string or absolutePath
                status: 'success' | 'error' | 'status_skipped';
                content: string; // File content or error/status message
                requestedIdentifier: string;
                absolutePath?: string;
                relativePath?: string; // 'index' mode
            }
        };
        retrievalMode: 'index' | 'path';
        targetPath: string;
    }
    ```
*   **Report Formatting**: Exports `formatReportFunction(data)` that creates a textual report listing each requested file's content (or status/error message), with appropriate headers.
*   **Role in `integr8handler.ts`**: Used in "path" mode to fetch the content of `targetPages` from the `externalProjectPath`. This content is then passed to `migrationAssistantParser.js` for further analysis.

#### Parser Plugin: `migrationAssistantParser.js`

*   **Source**: `PRD Generator Outputs/Compiled/prd src/migrationAssistantParser.js` (compiled from `migrationAssistantParser.ts`)
*   **Purpose**: Analyzes a specific "target page" (from an external project) against pre-analyzed data from both the external project and the current Orchestr8 project. It aims to identify potential integration problems and existing matches to guide migration.
*   **Key Function**: `analyzeDataFunction(targetPath, options)`
    *   `targetPath`: Path to the current Orchestr8 project (context).
    *   `options.externalAnalysisData`: Results from other parsers (overview, stores, etc.) run on the external project.
    *   `options.currentAnalysisData`: Results from other parsers run on the current Orchestr8 project.
    *   `options.targetPageContent: string`: Content of the external file being analyzed.
    *   `options.targetPageRelativePath: string`: Relative path of the target page.
*   **Analysis Logic**:
    1.  **`analyzeTargetPage(content, relativePath)` (Helper)**:
        *   Parses Vue SFCs (`@vue/compiler-sfc`) and script content (`@babel/parser`, `@babel/traverse`).
        *   Identifies script imports, `invoke()` calls, and (simplistically via regex) UI elements in the template.
        *   Returns sets of imports, invoked commands, and UI elements.
    2.  **`analyzeDataFunction` (Main)**:
        *   Calls `analyzeTargetPage` on `targetPageContent`.
        *   **Performs Comparisons (currently simplified, with TODOs for deeper analysis)**:
            *   **Imports**: Basic check against `currentAnalysisData.overview` file list for local imports.
            *   **Stores**: Placeholder check for a `requiredStoreId` against `externalAnalysisData.stores` and `currentAnalysisData.stores`.
            *   **Commands**: Checks `invokedCommands` from target page against `currentAnalysisData.commands` declarations.
            *   **Routes, UI Components, Types**: Marked as TODOs, not implemented.
        *   Collects findings into `problems` and `provisions` arrays.
*   **Output Data Structure (`AnalysisResult.data` for `migrationAssistantParser.js`)**:
    ```typescript
    // Inferred structure
    {
        targetPageRelativePath: string;
        problems: { type: string; name: string; details: string; category: string; }[];
        provisions: { type: string; name: string; details: string; category: string; }[];
    }
    ```
*   **Report Formatting**: Exports `formatReportFunction(data)` that generates a report for the target page, listing identified "Potential Integration Problems" and "Existing Provisions / Matches," grouped by category (e.g., Dependency, Store, Command).
*   **Role in `integr8handler.ts`**: This is a key synthesizer. `integr8handler.ts` calls this parser for each `targetPage`. It provides the results from all other parsers (overview, stores, commands, types, ui) for both projects, plus the target page's content. The `migrationAssistantParser.js` then attempts to provide integration advice for that specific page. The current implementation has several areas marked for future enhancement.

#### Parser Plugin: `backendGenParser.js` (Boilerplate Generator)

*   **Source**: `PRD Generator Outputs/Compiled/prd src/backendGenParser.js` (compiled from `backendGenParser.ts`)
*   **Purpose**: This script is **not an analyzer** but a **generator** of boilerplate code for a new Tauri backend (equivalent to `src-tauri`). It creates the directory structure and core files like `Cargo.toml`, `src/main.rs`, `src/database/schema.rs`, and `tauri.conf.json`.
*   **Key Function**: `generateBackendBoilerplate(outputBaseDir, options)`
    *   `outputBaseDir`: The target directory for the new backend structure.
    *   `options.projectName?`: Optional name for the project.
*   **Generated Boilerplate Highlights**:
    *   **`Cargo.toml`**: Includes Tauri v2 RC versions, `tauri-plugin-sql` (with sqlite, postgres, mysql features), `tauri-plugin-log`, `serde`, `tokio`, `thiserror`, `chrono`, `uuid`.
    *   **`src/main.rs`**:
        *   Sets up `tauri-plugin-sql` (preloading `maestro-scaffolder.sqlite`) and `tauri-plugin-log`.
        *   Defines a custom `Error` enum and `Result<T>` for command error handling.
        *   Includes placeholder Tauri commands: `get_file_tree` (iterative version), `run_verification`, and `initialize_feature_module`.
    *   **`src/database/schema.rs`**: Contains `CREATE TABLE` statements for a comprehensive schema designed to store code analysis artifacts. Key tables include:
        *   `ProjectFiles`: Information about scanned files.
        *   `Imports`: Details about import statements.
        *   `Exports`: Details about export statements.
        *   `Routes`: Vue Router route definitions.
        *   `Stores`: Pinia store definitions.
        *   `StoreProperties`: State, getters, actions of stores.
        *   `Commands`: Tauri command declarations.
        *   `CommandInvocations`: Frontend `invoke` calls.
        *   `VerificationIssues`: For storing analysis problems.
    *   **`tauri.conf.json`**: Configures build commands, product name, a restrictive initial allowlist (with dialog, path, some fs enabled), SQL and log plugin settings, and a permissive `dangerousFileSystemAccess` (noted for review).
*   **Relevance to `Integr8` Context**:
    *   While not an analyzer, it reveals the standard structure, dependencies, default commands, and importantly, the **database schema (`schema.rs`) intended for storing code analysis results** within the Orchestr8 ecosystem. This schema is likely populated by other analyzer parsers and is crucial for understanding how analysis data is persisted and structured.
    *   Provides a baseline for what a "Maestro Scaffolder" generated backend looks like.

#### Parser Plugin: `uiGenParser.js` (Boilerplate Generator)

*   **Source**: `PRD Generator Outputs/Compiled/prd src/uiGenParser.js` (compiled from `uiGenParser.ts`)
*   **Purpose**: This script is **not an analyzer** but a **generator** of boilerplate code for a new Vue.js frontend application. It sets up a project with Vue 3, Pinia, Vue Router, Naive UI, and Vite.
*   **Key Function**: `generateUiBoilerplate(outputBaseDir, options)`
    *   `outputBaseDir`: The target directory for the new frontend structure.
    *   `options.projectName?`: Optional name for the project.
*   **Generated Boilerplate Highlights**:
    *   **Project Setup**: `index.html`, `package.json` (with Vue, Pinia, Router, Naive UI, Tauri API deps), `vite.config.ts` (configured for Tauri), `.gitignore`.
    *   **`src/main.ts`**: Initializes Vue, Pinia, Router, and Naive UI.
    *   **`src/App.vue`**: Basic layout using Naive UI components (`NConfigProvider`, `NMessageProvider`, etc.) with a theme toggle placeholder and `<router-view />`.
    *   **`src/router/index.ts`**: Configures Vue Router (hash history) with a default `/` route to `ExplorerView.vue` and a title-setting navigation guard.
    *   **`src/stores/uiState.ts`**: Defines a `useUiStateStore` (Pinia) for managing global UI state like `currentProjectRoot`, `isLoading`, `fileTreeData`, `statusMessage`, `selectedNodeKey`. Includes a `FileNode` interface.
    *   **`src/views/ExplorerView.vue`**: A basic view component that allows selecting a project root, displays the path, and includes an `NTree` placeholder for a file tree (intended to be populated via a `get_file_tree` Tauri command and use `uiStateStore`).
*   **Relevance to `Integr8` Context**:
    *   While not an analyzer, it defines the **standard frontend stack (Vue 3, Pinia, Vue Router, Naive UI, Vite) and structure** for UIs generated by "Maestro Scaffolder."
    *   The boilerplate `uiStateStore.ts` and `ExplorerView.vue` provide insights into expected patterns for managing UI state and interacting with the file system via Tauri commands.
    *   This is a reference for how new UI elements related to `Integr8` might be scaffolded or integrated.

#### Parser Plugin: `featureFactory.js` (Briefing Generator & Orchestrator)

*   **Source**: `PRD Generator Outputs/Compiled/prd src/featureFactory.js` (compiled from `featureFactory.ts`)
*   **Purpose**: This script orchestrates the gathering of project context (by invoking other `scaffold` CLI commands for parsers like `overview`, `routes`, `stores`, etc.) and then synthesizes this information along with user-provided feature details into a "briefing document." This document is intended to guide an LLM in the step-by-step implementation of a new software feature.
*   **Key Function**: `generateFeatureFactoryBriefing(options)`
    *   `options.featureName: string`: Name of the new feature.
    *   `options.featureDesc: string`: User's description of the feature.
    *   `options.targetPath: string`: Path to the project for implementation.
    *   `options.outputDir: string`: Directory for the briefing document and temporary context files.
    *   `options.createUi?: boolean`, `options.createDb?: boolean`: Flags for UI/DB requirements.
    *   `options.cliPath?: string`: Optional path to the `cli.js` entry point.
*   **Core Workflow**:
    1.  **Context Scan**: Executes CLI commands (`node cli.js scaffold <type> ...`) for `overview`, `routes`, `stores`, `commands`, `types`, and `ui` parsers, saving their reports into a temporary directory.
    2.  **Context Synthesis (Current)**: Lists the paths to the generated context reports in the briefing document. (Future enhancements are planned for intelligent summarization).
    3.  **LLM Briefing Generation**: Creates a detailed text document that includes:
        *   User's feature request (name, description, UI/DB flags).
        *   The "Automated Project Context Summary" (list of report paths).
        *   A section for (currently placeholder) pre-provisioned files.
        *   **Detailed instructions for an LLM assistant**, emphasizing planning, step-by-step execution, generating one file at a time, providing clear placement/integration instructions, and waiting for confirmation after each step.
    4.  **Output**: Saves the briefing document to the specified output directory.
*   **Relevance to `Integr8` Context**:
    *   This script demonstrates a key **meta-process for LLM-assisted feature development** within the Orchestr8 ecosystem.
    *   It highlights which contextual information (overview, routes, stores, commands, types, UI) is deemed essential for building new features.
    *   The structured instructions for the LLM reveal a methodical approach to code generation and integration, which is a valuable pattern to understand for the `Integr8` feature's own design or its interaction with other LLM-driven processes.

### Backend Analysis, Comparison, and Dependency Mapping (Rust)

The Rust backend (`src-tauri/src/`) complements the JavaScript-based analysis tools with its own set of capabilities for code analysis, project comparison (implicitly), dependency management, and data parsing. These are relevant for the `Integr8` feature.

1.  **Native Code Parsers & Analyzers (`src-tauri/src/scaffold/`)**:
    *   This directory houses Rust modules that perform direct analysis of project files, similar to their JavaScript counterparts in `PRD Generator Outputs/Compiled/prd src/`.
    *   **`scaffold/commands.rs`**: Contains `scan_frontend_for_invokes` (finds `invoke(...)` calls) and `parse_tauri_commands` (finds `#[tauri::command]` declarations using regex).
    *   **`scaffold/overview.rs`**: Includes logic for generating project overviews, such as file listings and dependency summaries from `package.json` and `Cargo.toml`.
    *   **`scaffold/routes.rs`**: Implements `parse_routes_array` using the SWC (Speedy Web Compiler) library to analyze Vue Router configurations.
    *   **`scaffold/stores.rs`**: Uses SWC to parse Pinia store files and extract details.
    *   **`scaffold/files.rs`**: Contains `retrieve_files_by_index_core` for fetching file content.
    *   *Significance*: These Rust-native analyzers offer robust backend capabilities for understanding project structures, potentially used for performance-critical tasks or deeper integrations.

2.  **Workflow Engine (`src-tauri/src/workflow_engine/`)**:
    *   A core component for managing multi-step processes.
    *   **Dependency Management**: `workflow_engine/db.rs` features `check_dependencies` (ensures preceding workflow steps are complete) and `get_dependency_outputs` (fetches results from completed dependent steps).
    *   **Data Parsing/Mapping**: Extensive use of `serde_json` for parsing and mapping JSON data representing step context, inputs, and outputs (e.g., `utils::parse_optional_json`).
    *   *Relevance to `Integr8`*: Complex `Integr8` tasks could be modeled as workflows, leveraging the engine's state management, dependency tracking, and context propagation.

3.  **Database for Analysis Artifacts (`src-tauri/src/database/schema.rs`)**:
    *   Defines a comprehensive SQLite schema (likely in `maestro-scaffolder.sqlite` or a similar DB managed by `tauri-plugin-sql`) for storing code analysis results.
    *   Key tables include `ProjectFiles`, `Imports`, `Exports`, `Routes`, `Stores`, `Commands`, `CommandInvocations`, and `VerificationIssues`.
    *   *Relevance to `Integr8`*: This database is a central repository. `Integr8` could query it for existing project structures or contribute new analysis findings.

4.  **Feature Extraction Capabilities (`src-tauri/src/commands/feature_extraction_commands.rs`)**:
    *   Contains commands like `get_extractable_components` (intended to "Parse or analyze files to determine name, type, and dependencies") and `run_feature_extraction_verification` (intended for "dependency analysis" and "integrity checks").
    *   *Relevance to `Integr8`*: Highly relevant if `Integr8` involves identifying, analyzing, or preparing code for modularization or integration.

5.  **SEEG Engine (`src-tauri/src/maestro_modules/seeg_engine.rs` & `seeg_mcp_wrapper.rs`)**:
    *   The `seeg_engine.rs` includes an `execute_analysis_step` method, demonstrating analysis capabilities (e.g., reading and analyzing `commands.rs`).
    *   The `seeg_mcp_wrapper.rs` suggests interaction with an MCP server (e.g., `get_related_nodes_by_relation_type`), potentially for advanced analysis or knowledge graph operations.
    *   *Relevance to `Integr8`*: Indicates a system for executing structured analysis and potentially leveraging external knowledge or analysis tools via MCP.

6.  **Vector Operations & Semantic Analysis (`src-tauri/src/database/vector_ops.rs`)**:
    *   Provides functions like `get_similar_text_chunks`, `get_all_vector_records_for_entity`, and `cosine_similarity`.
    *   *Relevance to `Integr8`*: Indicates capabilities for semantic search or similarity analysis on textual data (which could be code, documentation, or PRDs), useful for finding related items or assessing similarity.

7.  **Model Context Protocol (MCP) Integration (`src-tauri/src/maestro_modules/mcp_client.rs`, `sdk_mcp_client.rs`)**:
    *   Modules for interacting with MCP servers, which can provide externalized tools and resources. Functions like `call_tool_mcp` are key.
    *   *Relevance to `Integr8`*: `Integr8` might use MCP to access specialized external analysis tools or knowledge graphs.

8.  **General Parsing and Data Handling**:
    *   The terms "parse," "scan," and "map" are found in various modules (e.g., parsing JSON in WebSocket messages in `ws/server.rs`, parsing Noir circuit inputs in `workflow_engine/handlers/noir.rs`). This shows a general capability to process diverse structured and unstructured data.

These backend capabilities suggest that Orchestr8 has a multi-layered approach to code analysis and integration, combining JavaScript-based tools (likely for broader, initial scans or CLI usage) with more deeply integrated Rust components for performance, direct data access, and complex workflow management. The `Integr8` feature can potentially leverage any of these layers.

#### Parser Plugin: `uiTemplateParser.js`

*   **Source**: `PRD Generator Outputs/Compiled/prd src/uiTemplateParser.js` (compiled from `uiTemplateParser.ts`)
*   **Purpose**: Analyzes the `<template>` section of Vue Single File Components (`.vue`) using **regular expressions** to identify UI element tags. It supports comparison and custom regex patterns. This differs from `uiParser.js` which analyzes the `<script>` section using AST.
*   **Key Function**: `analyzeUiTemplateData(targetPath, options)`
    *   `targetPath`: Path to the project directory or a specific `.vue` file.
    *   `options.comparePath?`: Optional path for comparison.
    *   `options.uiPattern?`: Optional regex string to identify UI element tags (defaults to Naive UI's `<n-...` convention).
*   **Analysis Logic**:
    1.  **Regex Compilation**: Prepares the regex pattern (ensuring global flag).
    2.  **File Scanning**: Uses `fast-glob` to find `.vue` files in `src/components` and `src/views` (if `targetPath` is a directory) or processes the single file.
    3.  **Template Analysis**: For each `.vue` file, reads its content and uses the compiled regex to extract all matching UI element tags from the entire file content (effectively the template).
    4.  Categorizes components as 'View', 'Component', 'Sub-Component', or 'Other'.
*   **Output Data Structure (`AnalysisResult.data` for `uiTemplateParser.js`)**:
    ```typescript
    // Inferred structure
    {
        primaryComponents: {
            relativePath: string;
            absolutePath: string;
            componentType: 'View' | 'Component' | 'Sub-Component' | 'Other';
            uiElements: string[]; // Array of unique UI element tags found
        }[];
        compareComponents?: { /* ...same structure... */ }[];
        primaryTargetPath: string;
        compareTargetPath?: string;
        patternUsed: string; // Source of the regex used
        patternFlags: string; // Flags of the regex used
    }
    ```
*   **Report Formatting**: Exports `formatReportFunction(data)` that generates a report listing UI elements found in each Vue file, categorized by component type. If comparing, it summarizes common and unique UI element tags.
*   **Relevance to `Integr8` Context**:
    *   Provides a direct look at the tags used within Vue templates, complementing the script-based analysis of `uiParser.js`.
    *   Useful for identifying usage of custom components, specific library components (if the pattern matches their tags), or general HTML tag patterns.
    *   Helps assess the nature and complexity of UI elements that might need integration or adaptation for the `Integr8` feature.

## 10. General Project Structure & Conventions

This section describes the typical directory structure and coding conventions observed in the Orchestr8 frontend codebase.

### Typical Frontend Directory Structure

The Orchestr8 frontend follows a conventional Vue.js project structure:

*   **`src/`**: The main source code directory.
    *   **`assets/`**: For static assets like images, fonts (though specific assets were not detailed in this reconnaissance).
    *   **`components/`**: Contains reusable Vue components. Sub-directories are used to group components belonging to a larger feature or a complex component (e.g., `src/components/ChangeRequests/`, `src/components/IntercomBarSubComponents/`, `src/components/Settings/`).
    *   **`composables/`**: Houses Vue Composition API functions (e.g., `useWebRTC.ts`). These are typically named with a `use` prefix.
    *   **`lib/`**: Contains utility functions, API interaction modules, security modules, and other library-like code (e.g., `maestro_api.ts`, `maestro_security.ts`, `prdDefinitions.ts`, `utils.ts`).
    *   **`router/`**: Contains the Vue Router configuration, primarily in `index.ts`.
    *   **`stores/`**: Home to Pinia state management modules. Each store is typically in its own file (e.g., `projectStore.ts`, `llmStore.ts`) and an `index.ts` likely serves as a barrel file to re-export all stores.
    *   **`types/`**: Central location for shared TypeScript type definitions and interfaces (`*.ts` files like `graph.ts`, `llmConfig.ts`).
    *   **`views/`**: Contains top-level Vue components that are mapped to routes in the router configuration. These represent distinct pages or views within the application.
    *   **Root of `src/`**: Holds the main application entry points, such as `main.ts` (Vue app initialization, plugin registration) and `App.vue` (the root Vue component).

### Coding Style, Linting, and Naming Conventions

Several conventions and practices are evident:

*   **Language**:
    *   **TypeScript** is pervasively used across the frontend (`.ts` files, `<script lang="ts">` in `.vue` files) and for the Node.js-based analysis scripts.
    *   **Rust** is used for the backend (Tauri commands and core logic).

*   **Vue.js**:
    *   The **Vue 3 Composition API** is consistently used for structuring components (`<script setup lang="ts">`) and Pinia stores (setup function syntax).

*   **State Management (Pinia)**:
    *   Stores are defined in `src/stores/`.
    *   Store files are named `featureNameStore.ts` (e.g., `projectStore.ts`).
    *   The exported store hook follows the `useFeatureNameStore` convention (e.g., `useProjectStore`).

*   **File & Variable Naming**:
    *   **Vue Components**: PascalCase (e.g., `AppHeader.vue`, `FileViewerWrapper.vue`).
    *   **TypeScript Files (.ts)**: Generally camelCase (e.g., `llmConfig.ts`, `integr8Store.ts`) or PascalCase for class-like structures if any.
    *   **Composables**: `useFeatureName.ts` (e.g., `useWebRTC.ts`).
    *   **Variables/Functions (TS/JS)**: camelCase is standard.
    *   **Rust Functions/Variables**: `snake_case` is standard, particularly for Tauri commands.

*   **Linting and Formatting**:
    *   The codebase exhibits consistent formatting (indentation, quotes, spacing), strongly suggesting the use of a code formatter like **Prettier**.
    *   Given the extensive TypeScript usage, an ESLint setup with TypeScript-specific plugins (e.g., `@typescript-eslint/eslint-plugin`) is highly probable for code quality and style enforcement. Specific linting rules are not detailed but adherence to common best practices is implied.

*   **Comments and Documentation**:
    *   JSDoc-style comments are frequently used in TypeScript files to document functions, parameters, and types, indicating a good practice for code maintainability.

*   **Modularity**:
    *   The codebase is generally well-modularized, with clear separation of concerns into components, views, stores, services (in `lib/`), composables, and types.
    *   The backend Rust code is also modular, with commands grouped by functionality in the `src-tauri/src/commands/` directory.

These conventions contribute to a structured and maintainable codebase.
