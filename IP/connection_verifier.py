# IP/connection_verifier.py
"""
Connection Verifier - Validates that imports actually resolve to real files.
Feeds into Blue status (broken) for Woven Maps Code City.

Handles:
- Python: import foo, from foo import bar, from . import relative
- JavaScript/TypeScript: import X from 'path', require('path')
- Resolves relative imports
- Package imports (from package.submodule import thing)
"""

import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum


class ImportType(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    UNKNOWN = "unknown"


@dataclass
class ImportResult:
    """Result of checking a single import statement."""
    source_file: str
    import_statement: str
    target_module: str
    resolved_path: Optional[str]  # None if unresolved
    is_resolved: bool
    is_stdlib: bool  # True if it's a standard library import
    is_external: bool  # True if it's an external package
    line_number: int = 0


@dataclass
class FileConnectionResult:
    """All import verification results for a single file."""
    file_path: str
    total_imports: int = 0
    resolved_imports: int = 0
    broken_imports: List[ImportResult] = field(default_factory=list)
    external_imports: List[ImportResult] = field(default_factory=list)
    status: str = "working"  # "working" | "broken"


# Python standard library modules (common ones - not exhaustive)
PYTHON_STDLIB = {
    "os", "sys", "re", "json", "datetime", "pathlib", "typing", "collections",
    "itertools", "functools", "dataclasses", "enum", "abc", "io", "math",
    "random", "time", "threading", "multiprocessing", "subprocess", "shutil",
    "tempfile", "glob", "fnmatch", "linecache", "pickle", "copy", "pprint",
    "textwrap", "string", "codecs", "unicodedata", "struct", "hashlib",
    "hmac", "secrets", "logging", "warnings", "contextlib", "traceback",
    "inspect", "dis", "gc", "weakref", "types", "operator", "argparse",
    "configparser", "csv", "sqlite3", "socket", "http", "urllib", "email",
    "html", "xml", "unittest", "doctest", "asyncio", "concurrent", "queue",
    "heapq", "bisect", "array", "decimal", "fractions", "statistics",
    "zlib", "gzip", "bz2", "lzma", "zipfile", "tarfile", "base64",
    "binascii", "uuid", "platform", "signal", "errno", "ctypes"
}

# Node.js built-in modules
NODE_BUILTINS = {
    "fs", "path", "os", "http", "https", "url", "util", "events",
    "stream", "buffer", "crypto", "child_process", "cluster", "dns",
    "net", "readline", "repl", "tls", "dgram", "assert", "process",
    "module", "querystring", "string_decoder", "timers", "tty", "v8",
    "vm", "zlib", "perf_hooks", "async_hooks", "worker_threads"
}


class ConnectionVerifier:
    """Verifies that imports in source files actually resolve to real files."""
    
    def __init__(self, project_root: str, node_modules_path: Optional[str] = None):
        self.project_root = Path(project_root).resolve()
        self.node_modules = Path(node_modules_path) if node_modules_path else self.project_root / "node_modules"
        
        # Regex patterns for extracting imports WITH line numbers
        self.python_patterns = [
            # from package.module import thing
            re.compile(r'^from\s+([\w.]+)\s+import\s+', re.MULTILINE),
            # import package.module
            re.compile(r'^import\s+([\w.]+)(?:\s+as\s+\w+)?$', re.MULTILINE),
            # from . import relative
            re.compile(r'^from\s+(\.[.\w]*)\s+import\s+', re.MULTILINE),
        ]
        
        self.js_patterns = [
            # import X from 'path' or "path"
            re.compile(r'''import\s+.*?\s+from\s+['"]([^'"]+)['"]'''),
            # import 'path' (side-effect import)
            re.compile(r'''import\s+['"]([^'"]+)['"]'''),
            # require('path')
            re.compile(r'''require\s*\(\s*['"]([^'"]+)['"]\s*\)'''),
            # dynamic import('path')
            re.compile(r'''import\s*\(\s*['"]([^'"]+)['"]\s*\)'''),
        ]
    
    def _detect_file_type(self, file_path: str) -> ImportType:
        """Detect the type of source file."""
        ext = Path(file_path).suffix.lower()
        if ext == '.py':
            return ImportType.PYTHON
        elif ext in {'.js', '.jsx', '.mjs', '.cjs'}:
            return ImportType.JAVASCRIPT
        elif ext in {'.ts', '.tsx'}:
            return ImportType.TYPESCRIPT
        return ImportType.UNKNOWN
    
    def _resolve_python_import(
        self, 
        import_path: str, 
        source_file: Path
    ) -> Tuple[Optional[str], bool, bool]:
        """
        Resolve a Python import to a file path.
        
        Returns: (resolved_path, is_stdlib, is_external)
        """
        # Check if it's a relative import
        if import_path.startswith('.'):
            return self._resolve_relative_python_import(import_path, source_file)
        
        # Check stdlib
        root_module = import_path.split('.')[0]
        if root_module in PYTHON_STDLIB:
            return (None, True, False)
        
        # Try to resolve as local module
        parts = import_path.split('.')
        
        # Try as package (directory with __init__.py)
        package_path = self.project_root
        for part in parts:
            package_path = package_path / part
        
        if package_path.is_dir() and (package_path / '__init__.py').exists():
            return (str(package_path / '__init__.py'), False, False)
        
        # Try as module file
        module_path = self.project_root
        for part in parts[:-1]:
            module_path = module_path / part
        module_file = module_path / f"{parts[-1]}.py"
        
        if module_file.exists():
            return (str(module_file.relative_to(self.project_root)), False, False)
        
        # Try without subdirectories (flat import)
        flat_path = self.project_root / f"{parts[0]}.py"
        if flat_path.exists():
            return (str(flat_path.relative_to(self.project_root)), False, False)
        
        # Check common src directories
        for src_dir in ['src', 'lib', 'IP', 'plugins']:
            src_path = self.project_root / src_dir
            if src_path.exists():
                # Try package in src
                pkg_in_src = src_path
                for part in parts:
                    pkg_in_src = pkg_in_src / part
                if pkg_in_src.is_dir() and (pkg_in_src / '__init__.py').exists():
                    return (str((pkg_in_src / '__init__.py').relative_to(self.project_root)), False, False)
                
                # Try module in src
                mod_in_src = src_path / f"{parts[0]}.py"
                if mod_in_src.exists():
                    return (str(mod_in_src.relative_to(self.project_root)), False, False)
        
        # Unresolved - assume external package
        return (None, False, True)
    
    def _resolve_relative_python_import(
        self, 
        import_path: str, 
        source_file: Path
    ) -> Tuple[Optional[str], bool, bool]:
        """Resolve a relative Python import (from . import X, from ..module import Y)."""
        # Count leading dots
        dots = len(import_path) - len(import_path.lstrip('.'))
        module_part = import_path.lstrip('.')
        
        # Navigate up from source file's directory
        current = source_file.parent
        for _ in range(dots - 1):  # -1 because first dot is current package
            current = current.parent
        
        if not module_part:
            # from . import X - looking for __init__.py in current
            init_path = current / '__init__.py'
            if init_path.exists():
                return (str(init_path.relative_to(self.project_root)), False, False)
        else:
            # from .module import X
            parts = module_part.split('.')
            for part in parts[:-1]:
                current = current / part
            
            # Try as module file
            module_file = current / f"{parts[-1]}.py"
            if module_file.exists():
                return (str(module_file.relative_to(self.project_root)), False, False)
            
            # Try as package
            pkg_init = current / parts[-1] / '__init__.py'
            if pkg_init.exists():
                return (str(pkg_init.relative_to(self.project_root)), False, False)
        
        return (None, False, False)  # Broken relative import
    
    def _resolve_js_import(
        self, 
        import_path: str, 
        source_file: Path
    ) -> Tuple[Optional[str], bool, bool]:
        """
        Resolve a JavaScript/TypeScript import to a file path.
        
        Returns: (resolved_path, is_builtin, is_external)
        """
        # Check Node.js builtins
        if import_path in NODE_BUILTINS or import_path.startswith('node:'):
            return (None, True, False)
        
        # Relative import
        if import_path.startswith('.'):
            return self._resolve_relative_js_import(import_path, source_file)
        
        # Alias imports (e.g., @/components) - treat as local
        if import_path.startswith('@/') or import_path.startswith('~/'):
            alias_path = import_path[2:]  # Remove @/ or ~/
            return self._try_resolve_js_file(self.project_root / 'src' / alias_path, source_file)
        
        # Scoped package (@org/package)
        if import_path.startswith('@'):
            # External scoped package
            return (None, False, True)
        
        # Check node_modules
        if self.node_modules.exists():
            pkg_path = self.node_modules / import_path.split('/')[0]
            if pkg_path.exists():
                return (None, False, True)  # External package exists
        
        # Unresolved - assume external
        return (None, False, True)
    
    def _resolve_relative_js_import(
        self, 
        import_path: str, 
        source_file: Path
    ) -> Tuple[Optional[str], bool, bool]:
        """Resolve a relative JS/TS import."""
        base_dir = source_file.parent
        target = (base_dir / import_path).resolve()
        
        return self._try_resolve_js_file(target, source_file)
    
    def _try_resolve_js_file(
        self, 
        target: Path,
        source_file: Path
    ) -> Tuple[Optional[str], bool, bool]:
        """Try to resolve a JS/TS file path with various extensions."""
        # Extensions to try
        extensions = ['', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '/index.ts', '/index.tsx', '/index.js', '/index.jsx']
        
        for ext in extensions:
            full_path = Path(str(target) + ext)
            if full_path.is_file():
                try:
                    return (str(full_path.relative_to(self.project_root)), False, False)
                except ValueError:
                    return (str(full_path), False, False)
        
        return (None, False, False)  # Broken import
    
    def _extract_imports_with_lines(
        self, 
        content: str, 
        patterns: List[re.Pattern]
    ) -> List[Tuple[str, int]]:
        """Extract imports with their line numbers."""
        imports = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for pattern in patterns:
                matches = pattern.findall(line)
                for match in matches:
                    imports.append((match, line_num))
        
        return imports
    
    def verify_file(self, file_path: str) -> FileConnectionResult:
        """
        Verify all imports in a single file.
        
        Args:
            file_path: Path relative to project root
            
        Returns:
            FileConnectionResult with broken/resolved import details
        """
        full_path = self.project_root / file_path
        result = FileConnectionResult(file_path=file_path)
        
        if not full_path.exists():
            result.status = "broken"
            return result
        
        file_type = self._detect_file_type(file_path)
        if file_type == ImportType.UNKNOWN:
            return result
        
        try:
            content = full_path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            result.status = "broken"
            return result
        
        # Select patterns based on file type
        if file_type == ImportType.PYTHON:
            patterns = self.python_patterns
            resolver = self._resolve_python_import
        else:
            patterns = self.js_patterns
            resolver = self._resolve_js_import
        
        # Extract and verify imports
        imports = self._extract_imports_with_lines(content, patterns)
        seen = set()  # Dedupe
        
        for import_path, line_num in imports:
            if import_path in seen:
                continue
            seen.add(import_path)
            
            resolved_path, is_stdlib, is_external = resolver(import_path, full_path)
            
            import_result = ImportResult(
                source_file=file_path,
                import_statement=import_path,
                target_module=import_path,
                resolved_path=resolved_path,
                is_resolved=resolved_path is not None or is_stdlib or is_external,
                is_stdlib=is_stdlib,
                is_external=is_external,
                line_number=line_num
            )
            
            result.total_imports += 1
            
            if is_stdlib or is_external:
                result.external_imports.append(import_result)
                result.resolved_imports += 1
            elif resolved_path:
                result.resolved_imports += 1
            else:
                result.broken_imports.append(import_result)
        
        # Set status based on broken imports
        if result.broken_imports:
            result.status = "broken"
        
        return result
    
    def verify_project(
        self, 
        file_paths: Optional[List[str]] = None,
        extensions: Optional[Set[str]] = None
    ) -> Dict[str, FileConnectionResult]:
        """
        Verify imports across the entire project or specific files.
        
        Args:
            file_paths: Specific files to check (if None, scans project)
            extensions: File extensions to include (default: .py, .ts, .tsx, .js, .jsx)
            
        Returns:
            Dict mapping file path to FileConnectionResult
        """
        if extensions is None:
            extensions = {'.py', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs'}
        
        if file_paths is None:
            file_paths = []
            exclusions = {'node_modules', '.git', '__pycache__', '.venv', 'venv', '.env', 'dist', 'build'}
            
            for root, dirs, files in os.walk(self.project_root):
                dirs[:] = [d for d in dirs if d not in exclusions]
                
                for file in files:
                    if Path(file).suffix.lower() in extensions:
                        full_path = Path(root) / file
                        rel_path = full_path.relative_to(self.project_root)
                        file_paths.append(str(rel_path))
        
        results = {}
        for file_path in file_paths:
            results[file_path] = self.verify_file(file_path)
        
        return results
    
    def get_broken_imports_summary(
        self, 
        results: Dict[str, FileConnectionResult]
    ) -> List[Dict]:
        """
        Get a summary of all broken imports for display/reporting.
        
        Returns list of dicts with: file, import, line, suggestion
        """
        broken = []
        for file_path, result in results.items():
            for imp in result.broken_imports:
                broken.append({
                    "file": file_path,
                    "import": imp.import_statement,
                    "line": imp.line_number,
                    "suggestion": self._suggest_fix(imp)
                })
        return broken
    
    def _suggest_fix(self, imp: ImportResult) -> str:
        """Suggest a fix for a broken import."""
        target = imp.target_module
        
        # Look for similarly named files
        for root, _, files in os.walk(self.project_root):
            for f in files:
                name = Path(f).stem
                if name.lower() == target.split('.')[-1].lower():
                    rel = Path(root).relative_to(self.project_root) / f
                    return f"Did you mean: {rel}?"
        
        return "Module not found in project"


# Convenience function for orchestr8.py integration
def verify_all_connections(project_root: str, files_df) -> Tuple:
    """
    Drop-in replacement for orchestr8.verify_connections that actually resolves imports.
    
    Returns: (updated_files_df, edges_df) with accurate status badges
    """
    import pandas as pd
    
    verifier = ConnectionVerifier(project_root)
    edges = []
    
    for index, row in files_df.iterrows():
        result = verifier.verify_file(row["path"])
        
        # Update status based on verification
        if result.broken_imports:
            files_df.at[index, "status"] = "BROKEN"  # Maps to Blue
            files_df.at[index, "issues"] = len(result.broken_imports)
        elif result.total_imports > 10:
            files_df.at[index, "status"] = "COMPLEX"
        else:
            files_df.at[index, "status"] = "WORKING"  # Maps to Gold
        
        # Create edges for ALL imports (resolved and broken)
        for imp in result.broken_imports + result.external_imports:
            edges.append({
                "source": row["path"],
                "target": imp.resolved_path or imp.target_module,
                "type": "import",
                "resolved": imp.is_resolved,
                "line": imp.line_number
            })
        
        # Add resolved local imports
        for imp in [i for i in result.external_imports if i.resolved_path]:
            pass  # Already added above
    
    return files_df, pd.DataFrame(edges) if edges else pd.DataFrame()


if __name__ == "__main__":
    # Quick test
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    verifier = ConnectionVerifier(root)
    results = verifier.verify_project()
    
    print(f"\n=== Connection Verification Report ===")
    print(f"Project: {root}")
    print(f"Files checked: {len(results)}")
    
    broken_count = sum(1 for r in results.values() if r.status == "broken")
    print(f"Files with broken imports: {broken_count}")
    
    if broken_count:
        print(f"\n--- Broken Imports ---")
        for file_path, result in results.items():
            if result.broken_imports:
                print(f"\n{file_path}:")
                for imp in result.broken_imports:
                    print(f"  Line {imp.line_number}: {imp.import_statement}")
