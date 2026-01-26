# Orchestr8 MCP Server - IDE Integration Guide

This guide explains how to connect Orchestr8's Code Map tools to your IDE.

## What You Get

Once connected, your AI assistant (Claude, GPT, etc.) gains access to:

| Tool | Description |
|------|-------------|
| `scan_directory` | Analyze directory structure with file metadata |
| `generate_mermaid_diagram` | Create Code Map visualizations |
| `analyze_imports` | Map file dependencies and imports |
| `get_file_info` | Detailed analysis of specific files |

## Quick Start

```bash
# Install dependency
pip install fastmcp

# Test the server runs
python orchestr8_mcp.py
# Should show the Orchestr8 banner

# Run in dev mode with inspector
fastmcp dev orchestr8_mcp.py
```

---

## IDE Configuration

### VS Code / Cursor / Windsurf

These are all VS Code-based and use the same config format.

**Option A: Workspace config** (recommended)

Create `.vscode/mcp.json` in your project:
```json
{
  "mcpServers": {
    "orchestr8": {
      "command": "python",
      "args": ["/home/bozertron/Orchestr8_jr/orchestr8_mcp.py"],
      "env": {}
    }
  }
}
```

**Option B: User settings**

Add to `settings.json` → `"mcp.servers"`:
```json
{
  "mcp.servers": {
    "orchestr8": {
      "command": "python",
      "args": ["/home/bozertron/Orchestr8_jr/orchestr8_mcp.py"]
    }
  }
}
```

---

### Claude Desktop

Edit `~/.config/claude/claude_desktop_config.json` (Linux) or equivalent:

```json
{
  "mcpServers": {
    "orchestr8": {
      "command": "python",
      "args": ["/home/bozertron/Orchestr8_jr/orchestr8_mcp.py"]
    }
  }
}
```

---

### Qoder / This IDE

Already configured! The `.vscode/mcp.json` file is in place.

To verify:
1. Reload the window
2. Ask the AI assistant: "Use the scan_directory tool on this project"

---

### IntelliJ IDEA / JetBrains

1. Go to **Settings → Tools → AI Assistant → MCP Servers**
2. Add new server:
   - Name: `orchestr8`
   - Command: `python`
   - Arguments: `/home/bozertron/Orchestr8_jr/orchestr8_mcp.py`

---

## Usage Examples

Once connected, ask your AI assistant:

### Generate a Code Map
```
Use generate_mermaid_diagram on /home/bozertron/Orchestr8_jr 
with diagram_type="overview"
```

### Scan Project Structure
```
Use scan_directory on my project with max_depth=3
```

### Analyze Dependencies
```
Use analyze_imports on /home/bozertron/Orchestr8_jr 
with file_pattern="*.py"
```

### Get File Details
```
Use get_file_info on /home/bozertron/Orchestr8_jr/orchestr8.py
```

---

## Troubleshooting

### Server not responding
```bash
# Test if server loads
python orchestr8_mcp.py --help

# Check if fastmcp is installed
python -c "from fastmcp import FastMCP; print('OK')"
```

### Connection refused
- Ensure no other process is using the MCP port
- Restart your IDE after config changes

### Tools not appearing
- Restart the IDE
- Check the MCP server logs in IDE developer tools
- Verify the config path is correct (use absolute paths)

---

## Running as HTTP Server (Advanced)

For remote access or multi-client scenarios:

```python
# In orchestr8_mcp.py, change the last lines:
if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

Then connect via URL instead of stdio:
```json
{
  "mcpServers": {
    "orchestr8": {
      "url": "http://localhost:8000/mcp/"
    }
  }
}
```

---

## Next Steps

1. **Mermaid Rendering**: The diagrams are text - use a Mermaid extension to visualize
2. **Code Map UI**: Build the full Layer 0 visualization with Three.js
3. **Real-time Updates**: Add file watchers for live diagram updates
