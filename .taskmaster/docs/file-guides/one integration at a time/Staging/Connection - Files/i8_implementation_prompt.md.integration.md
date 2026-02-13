# i8_implementation_prompt.md Integration Guide

- Source: `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md`
- Total lines: `208`
- SHA256: `065a029c71ef2eaaffa5f46cac25cbace5da4209b9740e4aaeb96a4dccae561e`
- Memory chunks: `2`
- Observation IDs: `759..760`

## Why This Is Painful

- General integration risk: enforce tests around schema, state, and behavior contracts.

## Anchor Lines

- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:5` This document provides detailed instructions for implementing the first phase of the Integr8 feature extraction framework as outlined in `i8.md`. This implementation will focus on the database schema extensions, which form the foundation for storing and managing Integr8 engineers and their tasks.
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:11` 1. Access to the orchestr8 codebase at `C:/orchestr8`
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:13` 3. Understood the database schema and vector operations in the existing codebase
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:18` - `C:/orchestr8/src/views/ConnectionVerifier.vue`
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:19` - `C:/orchestr8/src/views/ConnectionGraphView.vue`
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:22` - `C:/orchestr8/src-tauri/src/database/schema.rs` - For adding the new database tables
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:23` - `C:/orchestr8/src-tauri/src/commands/mod.rs` - For registering the new commands
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:24` - `C:/orchestr8/src-tauri/src/main.rs` - For including the new commands in the application
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:27` - `C:/orchestr8/PRD Generator Outputs/Compiled/integr8handler.ts` - Core handler that needs to be integrated
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:33` 1. **Open the schema file**:
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:35` C:/orchestr8/src-tauri/src/database/schema.rs
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:38` 2. **Add the new Integr8 database tables at the end of the schema initialization function**:
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:40` Look for the `initialize_schema` function and add the new table creation SQL statements after the existing tables.
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:95` C:/orchestr8/src-tauri/src/commands/integr8_commands.rs
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:109` C:/orchestr8/src-tauri/src/commands/mod.rs
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:140` C:/orchestr8/src-tauri/src/main.rs
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:159` After implementing the database schema and commands, follow these steps to test:
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:166` 2. **Verify the database schema**:
- `one integration at a time/Staging/Connection - Files/i8_implementation_prompt.md:172` C:/Users/[Username]/AppData/Roaming/orchestr8/orchestr8.db

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
