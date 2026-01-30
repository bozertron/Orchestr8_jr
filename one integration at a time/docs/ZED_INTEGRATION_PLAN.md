# Zed + Orchestr8 Integration Plan

**Created:** 2026-01-26  
**Status:** COMPREHENSIVE PLAN  
**Target:** Permanent symbiosis between Zed (engine) and Orchestr8 (soul)

---

## Executive Summary

Orchestr8 becomes a **Zed extension** that wraps our MCP server and provides:
1. Code Map visualization (Mermaid → eventually 3D metropolis)
2. maestro AI orchestration layer
3. Slash commands for codebase analysis
4. The "delightful experience" layer over Zed's high-performance editing

**Zed handles:** Text editing, LSP, debugging, venvs, Git, collaboration  
**Orchestr8 handles:** Visualization, navigation, AI orchestration, the "feel"

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTR8 ZED EXTENSION                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ MCP Server     │  │ Slash Commands │  │ Agent Panel    │    │
│  │ (Python)       │  │ (Rust/WASM)    │  │ Integration    │    │
│  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘    │
│          │                   │                   │              │
│          └───────────────────┼───────────────────┘              │
│                              │                                  │
│                    ┌─────────┴─────────┐                        │
│                    │  orchestr8_mcp.py │                        │
│                    │  (Tools)          │                        │
│                    └─────────┬─────────┘                        │
│                              │                                  │
├──────────────────────────────┼──────────────────────────────────┤
│                              │                                  │
│                    ┌─────────┴─────────┐                        │
│                    │     ZED CORE      │                        │
│                    │  (GPUI/Rust)      │                        │
│                    └───────────────────┘                        │
│                                                                 │
│   LSP │ Debugging │ Venvs │ Git │ Collaboration │ Terminal     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Extension Structure

```
orchestr8-zed/
├── extension.toml           # Extension manifest
├── Cargo.toml               # Rust dependencies
├── LICENSE                  # MIT (required by Zed)
├── src/
│   └── lib.rs               # Extension implementation
└── server/
    └── orchestr8_mcp.py     # Symlinked/bundled MCP server
```

### extension.toml

```toml
id = "orchestr8"
name = "Orchestr8"
version = "0.1.0"
schema_version = 1
authors = ["Electronic Pixel Orchestra Inc."]
description = "Code visualization, AI orchestration, and delightful developer experience"
repository = "https://github.com/bozertron/orchestr8-zed"

# MCP Server registration
[context_servers.orchestr8]

# Slash commands
[slash_commands.codemap]
description = "Generate a Code Map diagram for a directory"
requires_argument = true

[slash_commands.scan]
description = "Scan and analyze project structure"
requires_argument = true

[slash_commands.analyze]
description = "Analyze import dependencies"
requires_argument = true
```

### Cargo.toml

```toml
[package]
name = "orchestr8"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
zed_extension_api = "0.7.0"
```

### src/lib.rs

```rust
use zed_extension_api as zed;

struct Orchestr8Extension;

impl zed::Extension for Orchestr8Extension {
    fn new() -> Self {
        Self
    }

    fn context_server_command(
        &mut self,
        _context_server_id: &zed::ContextServerId,
        _project: &zed::Project,
    ) -> Result<zed::Command, String> {
        // Return command to start MCP server
        Ok(zed::Command {
            command: "python".to_string(),
            args: vec![
                self.get_server_path()?,
            ],
            env: vec![],
        })
    }

    fn run_slash_command(
        &self,
        command: zed::SlashCommand,
        args: Vec<String>,
        worktree: Option<&zed::Worktree>,
    ) -> Result<zed::SlashCommandOutput, String> {
        match command.name.as_str() {
            "codemap" => self.run_codemap(args, worktree),
            "scan" => self.run_scan(args, worktree),
            "analyze" => self.run_analyze(args, worktree),
            _ => Err(format!("Unknown command: {}", command.name)),
        }
    }
}

impl Orchestr8Extension {
    fn get_server_path(&self) -> Result<String, String> {
        // Return path to orchestr8_mcp.py
        // Could be bundled or system-installed
        Ok("/home/bozertron/Orchestr8_jr/orchestr8_mcp.py".to_string())
    }

    fn run_codemap(
        &self,
        args: Vec<String>,
        worktree: Option<&zed::Worktree>,
    ) -> Result<zed::SlashCommandOutput, String> {
        let path = args.first()
            .or_else(|| worktree.map(|w| w.root_path().to_string()))
            .ok_or("No path provided")?;
        
        // Generate mermaid diagram
        let diagram = self.generate_mermaid(&path)?;
        
        Ok(zed::SlashCommandOutput {
            text: format!("```mermaid\n{}\n```", diagram),
            sections: vec![zed::SlashCommandOutputSection {
                range: (0..diagram.len() + 14).into(),
                label: format!("Code Map: {}", path),
            }],
        })
    }

    fn run_scan(
        &self,
        args: Vec<String>,
        worktree: Option<&zed::Worktree>,
    ) -> Result<zed::SlashCommandOutput, String> {
        // Similar implementation
        todo!()
    }

    fn run_analyze(
        &self,
        args: Vec<String>,
        worktree: Option<&zed::Worktree>,
    ) -> Result<zed::SlashCommandOutput, String> {
        // Similar implementation
        todo!()
    }

    fn generate_mermaid(&self, path: &str) -> Result<String, String> {
        // Call Python MCP server or implement directly
        todo!()
    }
}

zed::register_extension!(Orchestr8Extension);
```

---

## Integration Points

### 1. MCP Server → Zed Agent Panel

Zed's Agent Panel can use MCP servers for context. Our `orchestr8_mcp.py` provides:

| Tool | Zed Usage |
|------|-----------|
| `scan_directory` | Provide project structure context to AI |
| `generate_mermaid_diagram` | Visual Code Map in chat |
| `analyze_imports` | Dependency context for refactoring |
| `get_file_info` | Detailed file analysis |

### 2. Slash Commands → Quick Actions

In Zed's assistant, users can type:
- `/codemap src/` → Generate Code Map
- `/scan .` → Scan current project  
- `/analyze --pattern "*.py"` → Analyze Python imports

### 3. Status Bar Integration (Future)

- maestro state indicator (OFF/OBSERVE/ON)
- Current project health
- Active agent count

---

## stereOS Codebase Transition Plan

### Current Location
```
/home/bozertron/Orchestr8_jr/
├── IP/                      # stereOS components
│   ├── plugins/             # Marimo UI plugins
│   ├── orchestr8_app.py     # Main Marimo app
│   ├── carl_core.py         # Contextualizer
│   ├── connie.py            # Converter
│   └── louis_core.py        # Core logic
├── 888/                     # Skills library
└── orchestr8_mcp.py         # MCP server (already created)
```

### Transition Steps

#### TODAY (Phase 0: Foundation)

1. **Create Zed extension scaffold**
   ```bash
   mkdir -p ~/Orchestr8_jr/orchestr8-zed/src
   cd ~/Orchestr8_jr/orchestr8-zed
   ```

2. **Install as dev extension in Zed**
   - Open Zed
   - Extensions → Install Dev Extension
   - Select `orchestr8-zed` directory

3. **Test MCP server connection**
   - Open Agent Panel in Zed
   - Verify Orchestr8 tools appear

#### WEEK 1 (Phase 1: MCP Integration)

| Task | Description | Est. |
|------|-------------|------|
| Extension scaffold | Create extension.toml, Cargo.toml, src/lib.rs | 2h |
| MCP server binding | Implement context_server_command | 2h |
| Test in Zed | Verify tools appear in Agent Panel | 1h |
| Slash command: /codemap | Generate Mermaid from slash command | 2h |
| Slash command: /scan | Project scan from slash command | 1h |

#### WEEK 2 (Phase 2: UI Layer)

| Task | Description | Est. |
|------|-------------|------|
| Port maestro CSS | Convert 06_maestro.py styles to Zed theme | 4h |
| Create Orchestr8 theme | Custom Zed theme matching UI spec | 4h |
| Status bar item | maestro state indicator | 2h |

#### WEEK 3+ (Phase 3: Advanced)

| Task | Description | Est. |
|------|-------------|------|
| Webview panel | Code Map visualization (if Zed supports) | 8h |
| Agent integration | Connect 888 skills to Zed | 8h |
| Public Services | SQLite/Vector/Graph integration | 16h |

---

## What Runs Where

### In Zed (Native)
- All text editing
- LSP (basedpyright for Python)
- Debugging (debugpy)
- Terminal (integrated)
- Git operations
- File tree

### In Orchestr8 Extension (WASM)
- Slash command handling
- MCP server spawning
- Status bar updates
- Theme/styling

### In orchestr8_mcp.py (Python subprocess)
- Directory scanning
- Mermaid generation
- Import analysis
- File metadata

### TBD: Marimo vs Zed
The Marimo app (`IP/orchestr8_app.py`) could:
1. **Option A:** Run alongside Zed as separate window for rich visualizations
2. **Option B:** Be deprecated in favor of Zed webviews (if supported)
3. **Option C:** Become the "standalone mode" for non-Zed users

**Recommendation:** Option A for now, evaluate Option B as Zed webview support matures.

---

## Commands to Run TODAY

```bash
# 1. Create extension directory
mkdir -p ~/Orchestr8_jr/orchestr8-zed/src

# 2. Create extension.toml
cat > ~/Orchestr8_jr/orchestr8-zed/extension.toml << 'EOF'
id = "orchestr8"
name = "Orchestr8"
version = "0.1.0"
schema_version = 1
authors = ["Electronic Pixel Orchestra Inc."]
description = "Code visualization and AI orchestration"
repository = "https://github.com/bozertron/orchestr8-zed"

[context_servers.orchestr8]
EOF

# 3. Create Cargo.toml
cat > ~/Orchestr8_jr/orchestr8-zed/Cargo.toml << 'EOF'
[package]
name = "orchestr8"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
zed_extension_api = "0.7.0"
EOF

# 4. Create MIT LICENSE
cat > ~/Orchestr8_jr/orchestr8-zed/LICENSE << 'EOF'
MIT License

Copyright (c) 2026 Electronic Pixel Orchestra Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# 5. Create src/lib.rs (minimal starter)
cat > ~/Orchestr8_jr/orchestr8-zed/src/lib.rs << 'EOF'
use zed_extension_api as zed;

struct Orchestr8Extension;

impl zed::Extension for Orchestr8Extension {
    fn new() -> Self {
        Self
    }

    fn context_server_command(
        &mut self,
        _context_server_id: &zed::ContextServerId,
        _project: &zed::Project,
    ) -> Result<zed::Command, String> {
        Ok(zed::Command {
            command: "python".to_string(),
            args: vec![
                "/home/bozertron/Orchestr8_jr/orchestr8_mcp.py".to_string(),
            ],
            env: vec![],
        })
    }
}

zed::register_extension!(Orchestr8Extension);
EOF

# 6. Install in Zed as dev extension
# (Do this manually in Zed UI: Extensions → Install Dev Extension → select orchestr8-zed/)
```

---

## Success Criteria

### Immediate (Today)
- [ ] Extension scaffold created
- [ ] Installs in Zed without errors
- [ ] MCP server connects to Agent Panel

### Short-term (This Week)
- [ ] /codemap slash command works
- [ ] /scan slash command works
- [ ] Tools appear in Agent Panel

### Medium-term (This Month)
- [ ] Status bar integration
- [ ] Custom Orchestr8 theme for Zed
- [ ] Full 888 skills accessible via MCP

### Long-term (Q2 2026)
- [ ] Code Map 3D visualization (webview or separate window)
- [ ] Public Services integration
- [ ] Complete stereOS → Zed migration

---

## Notes

- Zed extensions are compiled to WASM and run sandboxed
- MCP servers run as separate processes (our Python server)
- Zed's webview support is evolving - monitor for Code Map opportunities
- Rust must be installed via rustup (not homebrew) for extension development

---

**END INTEGRATION PLAN**
