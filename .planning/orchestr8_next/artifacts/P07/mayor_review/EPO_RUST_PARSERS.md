# EPO Rust Parser Architecture - The Iceberg Map

> **Analysis Date**: 2026-02-16  
> **Source**: `/home/bozertron/EPO - JFDI - Maestro/`  
> **Purpose**: Map the vast Rust parser architecture that user referred to as "vast like an iceberg"

---

## Executive Summary

The EPO (Editor Preferences / Options - JFDI - Maestro) codebase contains a sophisticated multi-layered Rust parser architecture built on **`syn`** (the Rust AST parsing library). Unlike traditional parser implementations, EPO's approach integrates:

1. **syn** - For Rust source code AST parsing
2. **quote** - For code generation
3. **proc-macro2** - For procedural macro support
4. **Custom pattern intelligence** - For architectural enforcement

**Key Finding**: There is NO SWC integration in the current codebase. The SWC reference in earlier documentation appears to be aspirational or from a different branch. The actual parser stack is pure Rust using `syn`.

---

## Architecture Layers

### Layer 1: Core Parsing (syn + quote)

**Location**: `src-tauri/Cargo.toml`

```toml
[build-dependencies]
syn = { version = "2.0", features = ["full", "extra-traits", "parsing"] }
quote = "1.0"

[dependencies]
syn = { version = "2.0", features = ["full", "extra-traits", "parsing", "printing"] }
quote = "1.0"
proc-macro2 = "1.0"
```

**syn Features Used**:
- `full` - Complete AST representation
- `extra-traits` - Debug, Clone, etc. traits for all AST nodes
- `parsing` - Parser combinators
- `printing` - Code generation back to Rust

---

### Layer 2: Binary Toolchain

**Location**: `src-tauri/src/bin/type_checker/`

```
type_checker/
├── mod.rs                    # Module exports
├── analysis_core.rs          # Main orchestration (5-phase pipeline)
├── analysis_helpers.rs       # Helper functions
├── cli.rs                    # Command-line interface
├── file_discovery.rs         # File traversal
├── reporting.rs              # Output formatting
├── type_extraction.rs        # AST → Type registry
└── types.rs                  # Type definitions
```

**Key Files**:

| File | Purpose | Lines |
|------|---------|-------|
| `analysis_core.rs` | 5-phase analysis orchestration | ~80 |
| `type_extraction.rs` | Extracts types from syn::File AST | ~120 |
| `types.rs` | TypeRegistry, TypeDefinition, Visibility | ~90 |

**Type Extraction Pipeline**:
```
File → syn::parse_file() → syn::File AST → extract_types_from_ast() → TypeRegistry
```

**AST Node Handlers**:
- `syn::ItemStruct` → `register_struct_type()`
- `syn::ItemEnum` → `register_enum_type()`
- `syn::ItemTrait` → `register_trait_type()`
- `syn::ItemFn` → `register_fn_type()` (public only)
- `syn::ItemMod` → `register_mod_type()`

---

### Layer 3: jfdi_lib Type Checker (External Crate)

**Location**: `/home/bozertron/EPO - JFDI - Maestro/type_checker/`

```
type_checker/                          # 50+ files, ~15K LOC
├── build_time/                        # Build-time analysis
│   ├── build_time/                    # Pattern bible core (6 files)
│   │   ├── pattern_bible_core_analysis.rs
│   │   ├── pattern_bible_core_import_analysis.rs
│   │   ├── pattern_bible_core_initialization.rs
│   │   ├── pattern_bible_core_search.rs
│   │   └── pattern_bible_core_validation/
│   ├── contracts/                     # Architectural contracts (15 files)
│   │   ├── architectural_contracts.rs
│   │   ├── hyper_modular_integrity.rs
│   │   ├── module_validation.rs
│   │   └── patterns/                 # Pattern validation (14 files)
│   ├── intelligence/                 # Pattern intelligence (10 files)
│   │   ├── pattern_intelligence.rs
│   │   ├── import_analysis.rs
│   │   ├── core_intelligence/
│   │   └── helpers/                  # Helper modules
│   │       ├── batch_resolution/     # Import batch analysis
│   │       ├── contract_analysis/     # Contract validation
│   │       ├── import_detection/     # Import usage checking
│   │       └── pattern_analysis/     # Pattern risk forecasting
│   └── core/                          # Data models
├── runtime/                           # Runtime analysis
│   ├── analyzer/
│   │   ├── parser.rs                 # syn::File parser
│   │   ├── processor.rs              # AST processing
│   │   └── validator.rs              # Type validation
│   ├── config.rs
│   ├── error.rs
│   └── registry.rs
├── domain/                            # Message types
├── enforcement/                      # Architectural enforcement (20 files)
│   ├── architectural_guardian.rs
│   ├── ast_intelligence_helpers.rs
│   ├── error_task_pipeline.rs
│   └── filetree_sync_helpers/
├── auto_filter/                       # Context filtering (15 files)
├── llm_guidance/                      # LLM integration (15 files)
└── inspired_types.md                  # Type system vision
```

---

### Layer 4: Build Integration

**Location**: `src-tauri/src/bin/type-checker.rs`

```rust
// Binary entry point for standalone type checking
// Connects to jfdi_lib::type_checker::build_time::intelligence
```

**Compilation Targets**:
```toml
[[bin]]
name = "type-checker"
path = "src/bin/type-checker.rs"

[[bin]]
name = "test-enforcement"
path = "src/bin/test-enforcement.rs"
```

---

## Parser Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 1: Setup                               │
│  - Initialize diagnostics                                       │
│  - Trace project root                                           │
│  - Configure target directories                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│               PHASE 2: Intelligence Gathering                    │
│  - PatternIntelligence (modular contracts, usage patterns)       │
│  - File discovery (walkdir)                                      │
│  - Batch import resolution                                       │
│  - Contract violation detection                                  │
│  - Pattern risk forecasting                                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│               PHASE 3: Registry Building                         │
│  - Add contracts to TypeRegistry                                │
│  - Add patterns to TypeRegistry                                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│               PHASE 4: AST Type Extraction                       │
│  - Parse each .rs file with syn::parse_file()                   │
│  - Extract: struct, enum, trait, fn, mod                        │
│  - Compute module path from file path                           │
│  - Register in TypeRegistry                                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│               PHASE 5: Results Compilation                       │
│  - AnalysisSummary (files, types, errors, duration)             │
│  - TypeRegistry (all discovered types)                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Parsing Functions

### FileParser (Runtime)

```rust
// Located: type_checker/runtime/analyzer/parser.rs

pub fn parse_file(&self, file_path: &Path) -> Result<syn::File, AnalysisError> {
    let content = std::fs::read_to_string(file_path)?;
    let syntax_tree = syn::parse_file(&content)?;
    Ok(syntax_tree)
}
```

### Type Extraction (Binary)

```rust
// Located: src-tauri/src/bin/type_checker/type_extraction.rs

pub fn extract_types_from_ast(
    registry: &mut TypeRegistry,
    ast: &syn::File,
    file_path: &PathBuf,
    project_root: &PathBuf,
) {
    let module_path = compute_module_path(file_path, project_root);
    
    for item in &ast.items {
        match item {
            syn::Item::Struct(s) => register_struct_type(...),
            syn::Item::Enum(e) => register_enum_type(...),
            syn::Item::Trait(t) => register_trait_type(...),
            syn::Item::Fn(f) => register_fn_type(...),
            syn::Item::Mod(m) => register_mod_type(...),
            _ => {}
        }
    }
}
```

---

## Architectural Constraints

The system enforces **Pattern Bible** compliance:

| Constraint | Value | Enforcement |
|------------|-------|-------------|
| File size | ≤200 lines | clippy `too_many_lines = "deny"` |
| Function size | ≤30 lines | Manual + clippy warnings |
| Module organization | Hyper-modular | Contract validation |

---

## What Can Be Extracted for C2P Scanner

### Immediate Opportunities:

1. **syn-based AST Parser**
   - Already proven for Rust
   - Can be adapted for comment extraction
   - Fast, deterministic parsing

2. **Pattern Intelligence Framework**
   - Batch import resolution
   - Contract analysis
   - Pattern risk forecasting
   - Can be repurposed for C2P pattern detection

3. **Type Registry Architecture**
   - TypeRegistry: HashMap<String, TypeDefinition>
   - TypeDefinition: name, full_path, visibility, location
   - Extensible for comment/marker storage

4. **File Discovery Module**
   - Uses `walkdir` for recursive traversal
   - Configurable target directories
   - Can be reused for comment scanning

### Not Found (Aspirational):

- **SWC Integration**: Not present in current codebase
  - Earlier docs referenced SWC for TS/JS parsing
  - Current stack is Rust-only via syn
  - Would need separate SWC crate integration for JS/TS

---

## File Counts

| Component | Files | LOC (est.) |
|-----------|-------|------------|
| Binary toolchain | 7 | ~500 |
| jfdi_lib type_checker | 50+ | ~15,000 |
| Enforcement system | 20 | ~3,000 |
| Auto-filter | 15 | ~2,000 |
| LLM guidance | 15 | ~2,000 |
| **Total** | **100+** | **~22,000** |

---

## Notes

1. **No SWC Found**: Despite references in earlier documentation, the actual codebase uses pure Rust parsing via `syn`. The SWC integration may have been planned but not implemented.

2. **jfdi_lib is External**: The `type_checker/` directory at project root is a separate crate (`jfdi_lib`) that's referenced from `src-tauri/src/type_checker/mod.rs`.

3. **Integration Pattern**: The binary at `src-tauri/src/bin/type_checker/` bridges to `jfdi_lib` for the heavy lifting.

4. **C2P Fit**: The syn-based parser, file discovery, and type registry architecture are directly applicable to building a C2P comment scanner.

---

*Generated from analysis of `/home/bozertron/EPO - JFDI - Maestro/`
