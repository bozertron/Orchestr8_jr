# Integr8 Implementation Guide

## Overview

This document provides detailed instructions for implementing the first phase of the Integr8 feature extraction framework as outlined in `i8.md`. This implementation will focus on the database schema extensions, which form the foundation for storing and managing Integr8 engineers and their tasks.

## Prerequisites

Before beginning implementation, ensure you have:

1. Access to the orchestr8 codebase at `C:/orchestr8`
2. Reviewed the current ConnectionVerifier.vue and ConnectionGraphView.vue components
3. Understood the database schema and vector operations in the existing codebase

## Key Files to Reference

- **UI Components**:
  - `C:/orchestr8/src/views/ConnectionVerifier.vue`
  - `C:/orchestr8/src/views/ConnectionGraphView.vue`
  
- **Relevant Backend Files**:
  - `C:/orchestr8/src-tauri/src/database/schema.rs` - For adding the new database tables
  - `C:/orchestr8/src-tauri/src/commands/mod.rs` - For registering the new commands
  - `C:/orchestr8/src-tauri/src/main.rs` - For including the new commands in the application

- **Integration Point**:
  - `C:/orchestr8/PRD Generator Outputs/Compiled/integr8handler.ts` - Core handler that needs to be integrated

## Implementation Steps for Block 1: Database Schema Extensions

### Step 1: Update Database Schema

1. **Open the schema file**:
   ```
   C:/orchestr8/src-tauri/src/database/schema.rs
   ```

2. **Add the new Integr8 database tables at the end of the schema initialization function**:
   
   Look for the `initialize_schema` function and add the new table creation SQL statements after the existing tables.
   
   Here's what you need to add:
   
   ```rust
   // Integr8 tables
   conn.execute(
       "CREATE TABLE IF NOT EXISTS Integr8_Engineers (
           engineer_id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           llm_entity_id INTEGER NOT NULL,
           specialization TEXT NOT NULL,
           status TEXT NOT NULL DEFAULT 'Idle',
           current_task TEXT,
           progress REAL DEFAULT 0.0,
           last_update INTEGER,
           FOREIGN KEY (llm_entity_id) REFERENCES LLM_Entities(entity_id) ON DELETE CASCADE
       )",
       params![],
   )?;
   
   conn.execute(
       "CREATE TABLE IF NOT EXISTS Integr8_Tasks (
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
       )",
       params![],
   )?;
   
   conn.execute(
       "CREATE TABLE IF NOT EXISTS Integr8_Task_Results (
           result_id INTEGER PRIMARY KEY AUTOINCREMENT,
           task_id INTEGER NOT NULL,
           result_type TEXT NOT NULL,
           content TEXT NOT NULL,
           created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
           FOREIGN KEY (task_id) REFERENCES Integr8_Tasks(task_id) ON DELETE CASCADE
       )",
       params![],
   )?;
   ```

### Step 2: Create New Command File

1. **Create a new file for Integr8 commands**:
   ```
   C:/orchestr8/src-tauri/src/commands/integr8_commands.rs
   ```

2. **Implement the commands as specified in the i8.md Block 2**
   
   Copy the complete Rust code from Block 2 in the i8.md file to the new file. This includes:
   - Data structures for engineers and tasks
   - Commands for managing engineers and tasks
   - Helper functions for database operations

### Step 3: Update Command Module

1. **Open the command module file**:
   ```
   C:/orchestr8/src-tauri/src/commands/mod.rs
   ```

2. **Add a new module for Integr8 commands**:
   
   Find the list of module declarations at the top of the file and add:
   
   ```rust
   pub mod integr8_commands;
   ```

3. **Re-export the commands**:
   
   Find the section where commands are re-exported and add:
   
   ```rust
   // Integr8 commands
   pub use integr8_commands::{
       get_integr8_engineers,
       create_integr8_engineer,
       assign_integr8_task,
       get_integr8_task_status,
       update_integr8_task_progress,
       store_integr8_task_result,
   };
   ```

### Step 4: Register Commands in main.rs

1. **Open the main.rs file**:
   ```
   C:/orchestr8/src-tauri/src/main.rs
   ```

2. **Add the new commands to the tauri::Builder**:
   
   Find the `.invoke_handler(tauri::generate_handler![...])` section and add the Integr8 commands:
   
   ```rust
   // Integr8 commands
   commands::get_integr8_engineers,
   commands::create_integr8_engineer,
   commands::assign_integr8_task,
   commands::get_integr8_task_status,
   commands::update_integr8_task_progress,
   commands::store_integr8_task_result,
   ```

## Testing the Implementation

After implementing the database schema and commands, follow these steps to test:

1. **Build and run the application**:
   ```
   cargo tauri dev
   ```

2. **Verify the database schema**:
   
   Use an SQLite browser to check the database file and ensure the new tables have been created.
   
   The database file is typically located at:
   ```
   C:/Users/[Username]/AppData/Roaming/orchestr8/orchestr8.db
   ```

3. **Test the commands using Developer Tools**:
   
   Open developer tools in the running application and test the commands using the Tauri API:
   
   ```javascript
   // Example: Create an engineer
   await window.__TAURI__.invoke('create_integr8_engineer', {
     name: 'Test Engineer',
     llmEntityId: 1, // Use an existing LLM entity ID
     specialization: 'Feature Extraction'
   });
   
   // Example: Get engineers
   const engineers = await window.__TAURI__.invoke('get_integr8_engineers');
   console.log(engineers);
   ```

## Next Steps

After successfully implementing Block 1 (Database Schema Extensions), proceed to Block 2 (Frontend Store Implementation) which involves:

1. Creating the integr8Store.ts file
2. Implementing the store with appropriate state and actions
3. Creating the UI components for managing Integr8 engineers and tasks

Remember to regularly commit your changes with descriptive commit messages to track your progress.

## Support Resources

If you encounter any issues during implementation, refer to:

- Rust SQLite documentation: https://docs.rs/rusqlite/latest/rusqlite/
- Tauri command documentation: https://tauri.studio/docs/api/js/modules/tauri
- Vue.js and Pinia documentation for frontend store implementation
