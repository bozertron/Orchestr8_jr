//! Orchestr8 Zed Extension
//!
//! Provides:
//! - MCP Server integration for Code Map tools
//! - Slash commands (/codemap, /scan, /analyze, /fileinfo)
//! - Future: Status bar integration, custom theme
//!
//! Architecture:
//! - This Rust/WASM extension spawns orchestr8_mcp.py as MCP server
//! - Zed's Agent Panel connects to the MCP server for tools
//! - Slash commands provide quick access to common operations

use zed_extension_api as zed;

/// Main extension struct
struct Orchestr8Extension {
    /// Path to the MCP server Python script
    server_path: Option<String>,
}

impl zed::Extension for Orchestr8Extension {
    fn new() -> Self {
        Self {
            server_path: None,
        }
    }

    /// Called when Zed needs to start the MCP server
    fn context_server_command(
        &mut self,
        _context_server_id: &zed::ContextServerId,
        _project: &zed::Project,
    ) -> Result<zed::Command, String> {
        // Get path to MCP server
        let server_path = self.get_server_path()?;
        
        Ok(zed::Command {
            command: "python".to_string(),
            args: vec![server_path],
            env: vec![],
        })
    }

    /// Handle slash commands in the Assistant
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
            "fileinfo" => self.run_fileinfo(args),
            _ => Err(format!("Unknown command: {}", command.name)),
        }
    }

    /// Provide completions for slash command arguments
    fn complete_slash_command_argument(
        &self,
        command: zed::SlashCommand,
        _args: Vec<String>,
    ) -> Result<Vec<zed::SlashCommandArgumentCompletion>, String> {
        match command.name.as_str() {
            "codemap" => Ok(vec![
                zed::SlashCommandArgumentCompletion {
                    label: "directory (default: current)".to_string(),
                    new_text: ".".to_string(),
                    run_command: true,
                },
                zed::SlashCommandArgumentCompletion {
                    label: "overview".to_string(),
                    new_text: "--type overview".to_string(),
                    run_command: true,
                },
                zed::SlashCommandArgumentCompletion {
                    label: "imports".to_string(),
                    new_text: "--type imports".to_string(),
                    run_command: true,
                },
            ]),
            "analyze" => Ok(vec![
                zed::SlashCommandArgumentCompletion {
                    label: "Python files".to_string(),
                    new_text: "*.py".to_string(),
                    run_command: true,
                },
                zed::SlashCommandArgumentCompletion {
                    label: "TypeScript files".to_string(),
                    new_text: "*.ts".to_string(),
                    run_command: true,
                },
                zed::SlashCommandArgumentCompletion {
                    label: "All files".to_string(),
                    new_text: "*".to_string(),
                    run_command: true,
                },
            ]),
            _ => Ok(vec![]),
        }
    }
}

impl Orchestr8Extension {
    /// Get the path to the MCP server script
    fn get_server_path(&self) -> Result<String, String> {
        // For now, hardcode the path
        // TODO: Make this configurable or bundle the server
        let path = "/home/bozertron/Orchestr8_jr/orchestr8_mcp.py";
        
        // Verify the file exists
        // Note: In WASM we can't directly check filesystem,
        // so we trust the path for now
        Ok(path.to_string())
    }

    /// Generate a Code Map diagram
    fn run_codemap(
        &self,
        args: Vec<String>,
        worktree: Option<&zed::Worktree>,
    ) -> Result<zed::SlashCommandOutput, String> {
        // Determine path
        let path = args.first()
            .map(|s| s.to_string())
            .or_else(|| worktree.map(|w| ".".to_string()))
            .unwrap_or_else(|| ".".to_string());

        // Determine diagram type
        let diagram_type = if args.iter().any(|a| a.contains("overview")) {
            "overview"
        } else if args.iter().any(|a| a.contains("imports")) {
            "imports"
        } else {
            "directory"
        };

        // For now, return a placeholder
        // The actual diagram generation happens via MCP tools
        let text = format!(
            "Use the Orchestr8 MCP tools in the Agent Panel to generate Code Maps:\n\n\
            ```\n\
            Tool: generate_mermaid_diagram\n\
            Path: {}\n\
            Type: {}\n\
            ```\n\n\
            Or use the Agent Panel directly with:\n\
            \"Generate a {} code map for {}\"",
            path, diagram_type, diagram_type, path
        );

        Ok(zed::SlashCommandOutput {
            text: text.clone(),
            sections: vec![zed::SlashCommandOutputSection {
                range: (0..text.len()).into(),
                label: format!("Code Map: {}", path),
            }],
        })
    }

    /// Scan project structure
    fn run_scan(
        &self,
        args: Vec<String>,
        worktree: Option<&zed::Worktree>,
    ) -> Result<zed::SlashCommandOutput, String> {
        let path = args.first()
            .map(|s| s.to_string())
            .or_else(|| worktree.map(|_| ".".to_string()))
            .unwrap_or_else(|| ".".to_string());

        let text = format!(
            "Use the Orchestr8 MCP tools in the Agent Panel:\n\n\
            ```\n\
            Tool: scan_directory\n\
            Path: {}\n\
            Max Depth: 3\n\
            ```\n\n\
            Or ask the Agent:\n\
            \"Scan the project structure at {}\"",
            path, path
        );

        Ok(zed::SlashCommandOutput {
            text: text.clone(),
            sections: vec![zed::SlashCommandOutputSection {
                range: (0..text.len()).into(),
                label: format!("Scan: {}", path),
            }],
        })
    }

    /// Analyze imports
    fn run_analyze(
        &self,
        args: Vec<String>,
        worktree: Option<&zed::Worktree>,
    ) -> Result<zed::SlashCommandOutput, String> {
        let pattern = args.first()
            .map(|s| s.to_string())
            .unwrap_or_else(|| "*".to_string());

        let path = worktree
            .map(|_| ".".to_string())
            .unwrap_or_else(|| ".".to_string());

        let text = format!(
            "Use the Orchestr8 MCP tools in the Agent Panel:\n\n\
            ```\n\
            Tool: analyze_imports\n\
            Path: {}\n\
            Pattern: {}\n\
            ```\n\n\
            Or ask the Agent:\n\
            \"Analyze import dependencies for {} files\"",
            path, pattern, pattern
        );

        Ok(zed::SlashCommandOutput {
            text: text.clone(),
            sections: vec![zed::SlashCommandOutputSection {
                range: (0..text.len()).into(),
                label: format!("Analyze: {}", pattern),
            }],
        })
    }

    /// Get file info
    fn run_fileinfo(
        &self,
        args: Vec<String>,
    ) -> Result<zed::SlashCommandOutput, String> {
        let path = args.first()
            .ok_or_else(|| "Please provide a file path".to_string())?;

        let text = format!(
            "Use the Orchestr8 MCP tools in the Agent Panel:\n\n\
            ```\n\
            Tool: get_file_info\n\
            Path: {}\n\
            ```\n\n\
            Or ask the Agent:\n\
            \"Get detailed info about {}\"",
            path, path
        );

        Ok(zed::SlashCommandOutput {
            text: text.clone(),
            sections: vec![zed::SlashCommandOutputSection {
                range: (0..text.len()).into(),
                label: format!("File Info: {}", path),
            }],
        })
    }
}

zed::register_extension!(Orchestr8Extension);
