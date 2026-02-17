"""
Orchestr8 MCP Server
====================
Plug Orchestr8 into ANY IDE that supports Model Context Protocol.

Provides tools for:
- Codebase scanning and analysis
- Mermaid diagram generation (Code Map)
- File relationship mapping
- Project structure visualization

Usage:
    # Run the server
    python orchestr8_mcp.py
    
    # Or with uvx (recommended)
    uvx fastmcp run orchestr8_mcp.py

IDE Configuration:
    See MCP_IDE_CONFIG.md for setup instructions for:
    - VS Code / Cursor / Windsurf
    - Claude Desktop
    - Any MCP-compatible IDE
"""

import os
import re
from pathlib import Path
from typing import Optional

try:
    from fastmcp import FastMCP
except ImportError:
    raise ImportError(
        "FastMCP not installed. Run: pip install fastmcp"
    )

# Initialize MCP Server
mcp = FastMCP(
    name="Orchestr8",
    instructions="""
    You are connected to Orchestr8, a codebase visualization and analysis tool.
    Use these tools to understand project structure, generate Code Maps (Mermaid diagrams),
    and analyze file relationships.
    """
)

# =============================================================================
# CONSTANTS
# =============================================================================

EXCLUSIONS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv", 
    ".env", "dist", "build", ".next", ".nuxt", "target",
    ".ruff_cache", ".pytest_cache", "__marimo__"
}

IMPORT_PATTERNS = [
    re.compile(r"(?:from|import)\s+['\"]([^'\"]+)['\"]"),  # JS/TS
    re.compile(r"^import\s+(\w+)", re.MULTILINE),          # Python: import x
    re.compile(r"^from\s+([\w.]+)\s+import", re.MULTILINE), # Python: from x import
    re.compile(r"#include\s*[<\"]([^>\"]+)[>\"]"),         # C/C++
    re.compile(r"use\s+([\w:]+)", re.MULTILINE),           # Rust
    re.compile(r"require\s*\(?\s*['\"]([^'\"]+)['\"]"),    # Node.js require
]

# File type categorization for Mermaid styling
FILE_CATEGORIES = {
    ".py": "python",
    ".js": "javascript", ".jsx": "javascript", ".ts": "typescript", ".tsx": "typescript",
    ".vue": "vue", ".svelte": "svelte",
    ".css": "style", ".scss": "style", ".less": "style",
    ".html": "markup", ".htm": "markup",
    ".json": "config", ".yaml": "config", ".yml": "config", ".toml": "config",
    ".md": "docs", ".rst": "docs", ".txt": "docs",
    ".rs": "rust", ".go": "go", ".java": "java",
    ".c": "c", ".cpp": "cpp", ".h": "header",
    ".sh": "shell", ".bash": "shell",
    ".sql": "database",
}


# =============================================================================
# TOOLS - Exposed to AI assistants via MCP
# =============================================================================

@mcp.tool
def scan_directory(
    path: str,
    max_depth: int = 10,
    include_hidden: bool = False
) -> dict:
    """
    Scan a directory and return its structure with file metadata.
    
    Args:
        path: Directory path to scan (absolute or relative to workspace)
        max_depth: Maximum directory depth to traverse
        include_hidden: Whether to include hidden files/directories
    
    Returns:
        Dictionary with 'files' list and 'summary' statistics
    """
    root_path = Path(path).expanduser().resolve()
    
    if not root_path.exists():
        return {"error": f"Path does not exist: {path}"}
    
    if not root_path.is_dir():
        return {"error": f"Path is not a directory: {path}"}
    
    files = []
    dir_count = 0
    total_size = 0
    
    for root, dirs, filenames in os.walk(root_path):
        # Calculate depth
        rel_root = Path(root).relative_to(root_path)
        depth = len(rel_root.parts)
        
        if depth > max_depth:
            dirs.clear()
            continue
        
        # Filter directories
        dirs[:] = [
            d for d in dirs 
            if d not in EXCLUSIONS 
            and (include_hidden or not d.startswith('.'))
        ]
        dir_count += len(dirs)
        
        for filename in filenames:
            if not include_hidden and filename.startswith('.'):
                continue
                
            full_path = Path(root) / filename
            rel_path = full_path.relative_to(root_path)
            ext = full_path.suffix.lower()
            
            try:
                size = full_path.stat().st_size
            except OSError:
                size = 0
            
            total_size += size
            
            files.append({
                "path": str(rel_path),
                "name": filename,
                "extension": ext,
                "category": FILE_CATEGORIES.get(ext, "other"),
                "size": size,
                "depth": depth
            })
    
    return {
        "root": str(root_path),
        "files": files,
        "summary": {
            "total_files": len(files),
            "total_directories": dir_count,
            "total_size_bytes": total_size,
            "file_types": _count_by_key(files, "extension"),
            "categories": _count_by_key(files, "category")
        }
    }


@mcp.tool
def generate_mermaid_diagram(
    path: str,
    diagram_type: str = "directory",
    max_depth: int = 3,
    show_sizes: bool = False
) -> str:
    """
    Generate a Mermaid diagram for a codebase.
    
    Args:
        path: Directory path to visualize
        diagram_type: Type of diagram - "directory" (tree), "imports" (dependency graph), or "overview" (category summary)
        max_depth: Maximum depth for directory diagrams
        show_sizes: Include file sizes in labels
    
    Returns:
        Mermaid diagram as a string
    """
    root_path = Path(path).expanduser().resolve()
    
    if not root_path.exists():
        return f"%%{{ERROR: Path does not exist: {path}}}%%"
    
    if diagram_type == "directory":
        return _generate_directory_mermaid(root_path, max_depth, show_sizes)
    elif diagram_type == "imports":
        return _generate_imports_mermaid(root_path)
    elif diagram_type == "overview":
        return _generate_overview_mermaid(root_path)
    else:
        return f"%%{{ERROR: Unknown diagram_type: {diagram_type}. Use 'directory', 'imports', or 'overview'}}%%"


@mcp.tool
def analyze_imports(
    path: str,
    file_pattern: Optional[str] = None
) -> dict:
    """
    Analyze import/dependency relationships in a codebase.
    
    Args:
        path: Directory path to analyze
        file_pattern: Optional glob pattern to filter files (e.g., "*.py")
    
    Returns:
        Dictionary with 'edges' (connections) and 'nodes' (files with import counts)
    """
    root_path = Path(path).expanduser().resolve()
    
    if not root_path.exists():
        return {"error": f"Path does not exist: {path}"}
    
    edges = []
    nodes = {}
    
    # Get files to analyze
    if file_pattern:
        files = list(root_path.rglob(file_pattern))
    else:
        files = [f for f in root_path.rglob("*") if f.is_file()]
    
    for file_path in files:
        # Skip excluded directories
        if any(excl in str(file_path) for excl in EXCLUSIONS):
            continue
        
        rel_path = str(file_path.relative_to(root_path))
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        
        # Find all imports
        imports = set()
        for pattern in IMPORT_PATTERNS:
            matches = pattern.findall(content)
            imports.update(matches)
        
        nodes[rel_path] = {
            "import_count": len(imports),
            "imports": list(imports)[:20]  # Limit to 20 for readability
        }
        
        for target in imports:
            edges.append({
                "source": rel_path,
                "target": target,
                "type": "import"
            })
    
    return {
        "root": str(root_path),
        "nodes": nodes,
        "edges": edges,
        "summary": {
            "total_files": len(nodes),
            "total_imports": len(edges),
            "most_imports": sorted(
                nodes.items(), 
                key=lambda x: x[1]["import_count"], 
                reverse=True
            )[:10]
        }
    }


@mcp.tool
def get_file_info(path: str) -> dict:
    """
    Get detailed information about a specific file.
    
    Args:
        path: Path to the file
    
    Returns:
        Dictionary with file metadata, imports, and health indicators
    """
    file_path = Path(path).expanduser().resolve()
    
    if not file_path.exists():
        return {"error": f"File does not exist: {path}"}
    
    if not file_path.is_file():
        return {"error": f"Path is not a file: {path}"}
    
    ext = file_path.suffix.lower()
    
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        lines = content.splitlines()
    except Exception as e:
        return {"error": f"Could not read file: {e}"}
    
    # Find imports
    imports = set()
    for pattern in IMPORT_PATTERNS:
        imports.update(pattern.findall(content))
    
    # Health indicators
    todo_count = content.count("TODO") + content.count("FIXME")
    has_tests = "test" in file_path.stem.lower() or "spec" in file_path.stem.lower()
    
    # Complexity indicators
    complexity = "normal"
    if len(imports) > 15:
        complexity = "high_imports"
    elif len(lines) > 500:
        complexity = "large_file"
    elif todo_count > 5:
        complexity = "needs_attention"
    
    return {
        "path": str(file_path),
        "name": file_path.name,
        "extension": ext,
        "category": FILE_CATEGORIES.get(ext, "other"),
        "size_bytes": file_path.stat().st_size,
        "line_count": len(lines),
        "imports": list(imports),
        "import_count": len(imports),
        "todo_count": todo_count,
        "is_test_file": has_tests,
        "complexity": complexity
    }


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _count_by_key(items: list, key: str) -> dict:
    """Count occurrences by a specific key."""
    counts = {}
    for item in items:
        val = item.get(key, "unknown")
        counts[val] = counts.get(val, 0) + 1
    return counts


def _generate_directory_mermaid(root_path: Path, max_depth: int, show_sizes: bool) -> str:
    """Generate a directory tree as Mermaid flowchart."""
    lines = ["graph TD"]
    node_id = 0
    id_map = {}
    
    def get_id(path_str: str) -> str:
        nonlocal node_id
        if path_str not in id_map:
            id_map[path_str] = f"n{node_id}"
            node_id += 1
        return id_map[path_str]
    
    root_id = get_id(str(root_path))
    lines.append(f"    {root_id}[{root_path.name}/]")
    
    for root, dirs, files in os.walk(root_path):
        rel_root = Path(root).relative_to(root_path)
        depth = len(rel_root.parts)
        
        if depth >= max_depth:
            dirs.clear()
            continue
        
        dirs[:] = [d for d in dirs if d not in EXCLUSIONS and not d.startswith('.')]
        
        parent_path = str(Path(root))
        parent_id = get_id(parent_path)
        
        # Add directories
        for d in dirs[:10]:  # Limit to 10 per level
            child_path = str(Path(root) / d)
            child_id = get_id(child_path)
            lines.append(f"    {parent_id} --> {child_id}[{d}/]")
        
        # Add files (limited)
        for f in files[:5]:  # Limit to 5 files per directory
            if f.startswith('.'):
                continue
            file_path = Path(root) / f
            file_id = get_id(str(file_path))
            label = f
            if show_sizes:
                try:
                    size = file_path.stat().st_size
                    label = f"{f}<br/>{_format_size(size)}"
                except:
                    pass
            lines.append(f"    {parent_id} --> {file_id}({label})")
    
    return "\n".join(lines)


def _generate_imports_mermaid(root_path: Path) -> str:
    """Generate an import dependency graph as Mermaid."""
    lines = ["graph LR"]
    edges = set()
    
    for file_path in root_path.rglob("*"):
        if not file_path.is_file():
            continue
        if any(excl in str(file_path) for excl in EXCLUSIONS):
            continue
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except:
            continue
        
        rel_path = file_path.relative_to(root_path)
        source = str(rel_path).replace("/", "_").replace(".", "_").replace("-", "_")
        
        for pattern in IMPORT_PATTERNS:
            for match in pattern.findall(content):
                target = match.replace("/", "_").replace(".", "_").replace("-", "_").replace("@", "")[:30]
                if (source, target) not in edges:
                    edges.add((source, target))
                    lines.append(f"    {source} --> {target}")
                    
                    if len(edges) > 100:  # Safety limit
                        lines.append("    %% Truncated at 100 edges")
                        return "\n".join(lines)
    
    return "\n".join(lines)


def _generate_overview_mermaid(root_path: Path) -> str:
    """Generate a category overview as Mermaid pie chart."""
    categories = {}
    
    for file_path in root_path.rglob("*"):
        if not file_path.is_file():
            continue
        if any(excl in str(file_path) for excl in EXCLUSIONS):
            continue
        
        ext = file_path.suffix.lower()
        cat = FILE_CATEGORIES.get(ext, "other")
        categories[cat] = categories.get(cat, 0) + 1
    
    lines = ['pie title File Categories']
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        lines.append(f'    "{cat}" : {count}')
    
    return "\n".join(lines)


def _format_size(size_bytes: int) -> str:
    """Format bytes into human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.0f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.0f}TB"


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                     ORCHESTR8 MCP SERVER                      ║
╠═══════════════════════════════════════════════════════════════╣
║  Tools available:                                             ║
║    • scan_directory    - Scan and analyze directory structure ║
║    • generate_mermaid  - Create Code Map diagrams             ║
║    • analyze_imports   - Map file dependencies                ║
║    • get_file_info     - Detailed file analysis               ║
╠═══════════════════════════════════════════════════════════════╣
║  Connect this server to your IDE:                             ║
║    • VS Code: Add to .vscode/mcp.json                        ║
║    • Cursor:  Add to .cursor/mcp.json                        ║
║    • Claude Desktop: Add to claude_desktop_config.json       ║
╚═══════════════════════════════════════════════════════════════╝
""")
    mcp.run()
