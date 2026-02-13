# seeg before breakdown 05232025.txt Integration Guide

- Source: `one integration at a time/Staging/Connection - Files/seeg before breakdown 05232025.txt`
- Total lines: `759`
- SHA256: `ae59be7d8fa0e29f372ff40c985c7b6ab0e3f3c7a30e5ec409aee57a1944e383`
- Memory chunks: `7`
- Observation IDs: `789..795`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.

## Anchor Lines

- `one integration at a time/Staging/Connection - Files/seeg before breakdown 05232025.txt:1` // src-tauri/src/maestro_modules/seeg_engine.rs
- `one integration at a time/Staging/Connection - Files/seeg before breakdown 05232025.txt:18` use crate::maestro_modules::seeg_mcp_wrapper::{self, Step as McpStep};
- `one integration at a time/Staging/Connection - Files/seeg before breakdown 05232025.txt:21` use crate::maestro_modules::llm_clients::{LlmApiResponse, MockLlmClient, LlmClient};
- `one integration at a time/Staging/Connection - Files/seeg before breakdown 05232025.txt:22` use crate::maestro_modules::embeddings::{generate_embeddings_with_cache, EmbeddingProvider};
- `one integration at a time/Staging/Connection - Files/seeg before breakdown 05232025.txt:544` // Test with valid project ID (should return true)
- `one integration at a time/Staging/Connection - Files/seeg before breakdown 05232025.txt:549` // Test with invalid project ID (should return false)
- `one integration at a time/Staging/Connection - Files/seeg before breakdown 05232025.txt:590` let temp_dir = std::env::temp_dir().join(format!("maestro_seeg_verify_{}", Uuid::new_v4()));

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
