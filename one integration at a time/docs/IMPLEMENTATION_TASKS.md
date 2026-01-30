# Big Pickle Implementation Tasks

**Source:** ROADMAP_ORCHESTR8_V4.md (Technical Specifications)  
**Created:** 2026-01-26  
**Scope:** Core infrastructure implementation (no templates, no enhanced viz)

---

## Overview

These tasks extract the complete Python modules from the roadmap's Technical Specifications section. Each task includes the exact code to implement.

**OUT OF SCOPE (Handled elsewhere):**
- Enhanced Visualization (PyVis, blast radius) - Future phase
- CLAUDE.md template - LLM Behavior Spec
- Ticket structure template - LLM Behavior Spec
- BRIEFING.md template - LLM Behavior Spec  
- CAMPAIGN_LOG.md format - LLM Behavior Spec

---

## Phase 1: Core Python Modules

### Task BP-001: Create Mermaid Generator Module

**File:** `IP/mermaid_generator.py`  
**Effort:** 30 min  
**Dependencies:** None

```python
# IP/mermaid_generator.py
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class FiefdomStatus(Enum):
    WORKING = "working"    # Gold - healthy
    BROKEN = "broken"      # Blue - has errors
    COMBAT = "combat"      # Purple - general deployed

@dataclass
class Fiefdom:
    path: str
    status: FiefdomStatus
    connections: List[str]
    error_count: int = 0
    last_check: Optional[str] = None

# Color constants from MaestroView.vue
COLORS = {
    "working": {"fill": "#D4AF37", "stroke": "#B8860B", "text": "#000"},
    "broken": {"fill": "#1fbdea", "stroke": "#0891b2", "text": "#000"},
    "combat": {"fill": "#9D4EDD", "stroke": "#7c3aed", "text": "#fff"},
}

def generate_empire_mermaid(fiefdoms: List[Fiefdom]) -> str:
    """
    Generate Mermaid flowchart with gold/blue/purple coloring.

    Args:
        fiefdoms: List of Fiefdom objects

    Returns:
        Mermaid markdown string ready for mo.mermaid()
    """
    lines = ["graph TD"]

    # Create node ID mapping
    path_to_id = {f.path: f"N{i}" for i, f in enumerate(fiefdoms)}

    # Add nodes with labels
    for i, f in enumerate(fiefdoms):
        node_id = f"N{i}"
        label = Path(f.path).name
        # Add error count to broken nodes
        if f.status == FiefdomStatus.BROKEN and f.error_count > 0:
            label = f"{label} ({f.error_count})"
        lines.append(f'    {node_id}["{label}"]')

    # Add edges based on connections
    for f in fiefdoms:
        source_id = path_to_id[f.path]
        for conn in f.connections:
            if conn in path_to_id:
                target_id = path_to_id[conn]
                lines.append(f'    {source_id} --> {target_id}')

    # Add styles based on status
    lines.append("")
    for i, f in enumerate(fiefdoms):
        node_id = f"N{i}"
        colors = COLORS[f.status.value]
        lines.append(
            f'    style {node_id} fill:{colors["fill"]},'
            f'stroke:{colors["stroke"]},color:{colors["text"]}'
        )

    return "\n".join(lines)


def render_in_marimo(fiefdoms: List[Fiefdom]):
    """Render Mermaid graph in Marimo."""
    import marimo as mo
    mermaid_str = generate_empire_mermaid(fiefdoms)
    return mo.mermaid(mermaid_str)
```

**Verification:**
```python
python -c "from IP.mermaid_generator import FiefdomStatus, Fiefdom, generate_empire_mermaid; print('OK')"
```

---

### Task BP-002: Create Terminal Spawner Module

**File:** `IP/terminal_spawner.py`  
**Effort:** 45 min  
**Dependencies:** None

```python
# IP/terminal_spawner.py
import platform
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

class TerminalSpawner:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.state_file = self.project_root / ".orchestr8" / "state" / "fiefdom-status.json"

    def update_fiefdom_status(self, fiefdom_path: str, status: str) -> None:
        """Update fiefdom status in state file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        if self.state_file.exists():
            with open(self.state_file) as f:
                state = json.load(f)
        else:
            state = {"fiefdoms": {}}

        state["fiefdoms"][fiefdom_path] = {
            "status": status,
            "updated_at": datetime.now().isoformat()
        }

        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)

    def spawn(
        self,
        fiefdom_path: str,
        briefing_ready: bool = True,
        auto_start_claude: bool = False
    ) -> bool:
        """
        Spawn terminal at fiefdom path and update status to COMBAT.

        Args:
            fiefdom_path: Relative path from project root
            briefing_ready: Whether BRIEFING.md has been generated
            auto_start_claude: Whether to auto-run claude command

        Returns:
            True if spawn succeeded
        """
        abs_path = str(self.project_root / fiefdom_path)

        # Update status to COMBAT (purple)
        self.update_fiefdom_status(fiefdom_path, "combat")

        # Build startup message
        if briefing_ready:
            msg = 'echo "⚔️ BRIEFING.md ready. Type: claude --print \\"Read BRIEFING.md and begin.\\""'
        else:
            msg = 'echo "📜 Read CLAUDE.md for orders. Type: claude"'

        if auto_start_claude:
            msg += ' && claude --print "Read BRIEFING.md and begin."'
        else:
            msg += ' && bash'

        # Platform-specific spawn
        system = platform.system()

        try:
            if system == "Linux":
                # Try gnome-terminal first, fall back to xterm
                try:
                    subprocess.Popen([
                        'gnome-terminal',
                        '--working-directory', abs_path,
                        '--', 'bash', '-c', msg
                    ])
                except FileNotFoundError:
                    subprocess.Popen([
                        'xterm', '-e',
                        f'cd "{abs_path}" && {msg}'
                    ])

            elif system == "Darwin":  # macOS
                script = f'''
                tell application "Terminal"
                    do script "cd '{abs_path}' && {msg}"
                    activate
                end tell
                '''
                subprocess.Popen(['osascript', '-e', script])

            elif system == "Windows":
                subprocess.Popen([
                    'cmd', '/c', 'start', 'cmd', '/k',
                    f'cd /d "{abs_path}" && {msg}'
                ])

            return True

        except Exception as e:
            print(f"Failed to spawn terminal: {e}")
            # Revert status on failure
            self.update_fiefdom_status(fiefdom_path, "broken")
            return False

    def mark_combat_complete(self, fiefdom_path: str, success: bool) -> None:
        """
        Mark combat as complete. Called when general finishes.

        Args:
            fiefdom_path: The fiefdom that was worked on
            success: Whether the mission succeeded (for status update)
        """
        # Status will be updated by next health check
        # This just logs the completion
        self.update_fiefdom_status(
            fiefdom_path,
            "pending_health_check"
        )
```

**Verification:**
```python
python -c "from IP.terminal_spawner import TerminalSpawner; print('OK')"
```

---

### Task BP-003: Create Health Checker Module

**File:** `IP/health_checker.py`  
**Effort:** 45 min  
**Dependencies:** None

```python
# IP/health_checker.py
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class HealthCheckResult:
    status: str  # "working" | "broken"
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    last_check: str = ""
    raw_output: str = ""

class HealthChecker:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)

    def check_fiefdom(self, fiefdom_path: str) -> HealthCheckResult:
        """
        Run health check for a fiefdom.
        Currently uses npm run typecheck. Future: e2e, unit tests.

        Args:
            fiefdom_path: Relative path from project root (e.g., "src/modules/generator")

        Returns:
            HealthCheckResult with status, errors, warnings
        """
        result = subprocess.run(
            ["npm", "run", "typecheck"],
            cwd=str(self.project_root),
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )

        # TypeScript errors go to stdout, not stderr
        output = result.stdout + result.stderr
        errors = []
        warnings = []

        # Parse output for this fiefdom
        for line in output.split('\n'):
            # Check if error is in this fiefdom
            if fiefdom_path in line:
                if 'error TS' in line or 'error:' in line.lower():
                    errors.append(line.strip())
                elif 'warning' in line.lower():
                    warnings.append(line.strip())

        return HealthCheckResult(
            status="broken" if errors else "working",
            errors=errors,
            warnings=warnings,
            last_check=datetime.now().isoformat(),
            raw_output=output
        )

    def check_all_fiefdoms(self, fiefdom_paths: List[str]) -> Dict[str, HealthCheckResult]:
        """
        Run health check once and parse results for all fiefdoms.
        More efficient than running typecheck per fiefdom.
        """
        result = subprocess.run(
            ["npm", "run", "typecheck"],
            cwd=str(self.project_root),
            capture_output=True,
            text=True,
            timeout=120
        )

        output = result.stdout + result.stderr
        results = {}

        for fiefdom in fiefdom_paths:
            errors = []
            warnings = []
            for line in output.split('\n'):
                if fiefdom in line:
                    if 'error TS' in line or 'error:' in line.lower():
                        errors.append(line.strip())
                    elif 'warning' in line.lower():
                        warnings.append(line.strip())

            results[fiefdom] = HealthCheckResult(
                status="broken" if errors else "working",
                errors=errors,
                warnings=warnings,
                last_check=datetime.now().isoformat(),
                raw_output=""  # Only store once, not per fiefdom
            )

        return results
```

**Verification:**
```python
python -c "from IP.health_checker import HealthChecker, HealthCheckResult; print('OK')"
```

---

### Task BP-004: Create Briefing Generator Module

**File:** `IP/briefing_generator.py`  
**Effort:** 1 hour  
**Dependencies:** None

```python
# IP/briefing_generator.py
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import json

class BriefingGenerator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)

    def load_campaign_log(self, fiefdom_path: str, limit: int = 5) -> List[Dict]:
        """Load recent entries from CAMPAIGN_LOG.md."""
        log_path = self.project_root / fiefdom_path / "CAMPAIGN_LOG.md"
        if not log_path.exists():
            return []

        # Parse markdown entries (simplified - would need proper parser)
        entries = []
        # ... parsing logic ...
        return entries[-limit:]

    def get_locks_for_fiefdom(self, fiefdom_path: str) -> List[Dict]:
        """Get Louis locks relevant to this fiefdom."""
        config_path = self.project_root / ".louis-control" / "louis-config.json"
        if not config_path.exists():
            return []

        with open(config_path) as f:
            config = json.load(f)

        locks = []
        for filepath, lock_info in config.get("locks", {}).items():
            # Include locks in this fiefdom or that this fiefdom might touch
            if fiefdom_path in filepath or filepath.startswith("../"):
                locks.append({
                    "file": filepath,
                    "reason": lock_info.get("reason", "Protected"),
                    "locked_at": lock_info.get("locked_at", "Unknown")
                })
        return locks

    def generate(
        self,
        fiefdom_path: str,
        ticket_id: str,
        ticket_status: str,
        mission: str,
        errors: List[str],
        warnings: List[str],
        notes: List[Dict],
        context: Optional[Dict] = None
    ) -> str:
        """
        Generate BRIEFING.md with MAXIMUM context.

        We eat the tokens to do the job right the first time.
        """
        now = datetime.now()
        locks = self.get_locks_for_fiefdom(fiefdom_path)
        campaign_history = self.load_campaign_log(fiefdom_path, limit=5)

        # Default context if not provided
        if context is None:
            context = {
                "related_files": [],
                "imports_from": [],
                "exports_to": [],
                "patterns": []
            }

        briefing = f"""# ⚔️ MISSION BRIEFING: {ticket_id}

**Generated:** {now.isoformat()}
**Fiefdom:** {fiefdom_path}
**Absolute Path:** {self.project_root / fiefdom_path}
**Status:** You are being deployed to a {ticket_status.upper()} fiefdom

---

## 🎯 Objective

{mission}

## ❌ Current Errors ({len(errors)} total)

```
{chr(10).join(errors) if errors else "No errors recorded"}
```

## ⚠️ Warnings ({len(warnings)} total)

```
{chr(10).join(warnings) if warnings else "No warnings recorded"}
```

## 🔍 Carl's Reconnaissance

- **Error Count:** {len(errors)}
- **Warning Count:** {len(warnings)}
- **Related Files:** {', '.join(context.get('related_files', [])) or 'None identified'}
- **Connections:**
  - Imports from: {', '.join(context.get('imports_from', [])) or 'None identified'}
  - Exports to: {', '.join(context.get('exports_to', [])) or 'None identified'}
- **Patterns to Follow:** {', '.join(context.get('patterns', [])) or 'See CLAUDE.md'}

## 🔒 Louis's Restrictions

| File | Status | Reason |
|------|--------|--------|
"""

        if locks:
            for lock in locks:
                briefing += f"| `{lock['file']}` | 🔒 LOCKED | {lock['reason']} |\n"
        else:
            briefing += "| (none) | - | No locks in this fiefdom |\n"

        briefing += """
## 📜 Recent Campaign History

"""

        if campaign_history:
            for entry in campaign_history:
                briefing += f"""### {entry.get('ticket', 'Unknown')} ({entry.get('date', 'Unknown')}) - {entry.get('status', 'Unknown')}
- **Action:** {entry.get('summary', 'No summary')}
- **Lesson:** {entry.get('lesson', 'None recorded')}

"""
        else:
            briefing += "*No previous campaigns recorded. You are the first general here.*\n\n"

        briefing += """## 💬 Stacked Notes

| Time | Author | Note |
|------|--------|------|
"""

        if notes:
            for note in notes:
                briefing += f"| {note.get('time', '?')} | {note.get('author', '?')} | {note.get('text', '')} |\n"
        else:
            briefing += "| - | - | No notes yet |\n"

        briefing += f"""
## ✅ Health Check

```bash
npm run typecheck
# Victory = no errors containing "{fiefdom_path}"
```

## 📋 Your Checklist

1. [ ] Read CLAUDE.md for standing orders
2. [ ] Scan CAMPAIGN_LOG.md for recent lessons
3. [ ] Deploy Scout to analyze the problem
4. [ ] Deploy Fixer to make surgical changes
5. [ ] Deploy Validator to run health check
6. [ ] Update CAMPAIGN_LOG.md with your actions
7. [ ] Report outcome

---

**BEGIN MISSION**
"""

        return briefing

    def write_briefing(self, fiefdom_path: str, **kwargs) -> Path:
        """Generate and write BRIEFING.md to the fiefdom."""
        content = self.generate(fiefdom_path, **kwargs)
        briefing_path = self.project_root / fiefdom_path / "BRIEFING.md"
        briefing_path.write_text(content)
        return briefing_path
```

**Verification:**
```python
python -c "from IP.briefing_generator import BriefingGenerator; print('OK')"
```

---

## Phase 2: Git Hooks Integration

### Task BP-005: Create Git Pre-Commit Hook (Louis Enforcement)

**File:** `.git/hooks/pre-commit`  
**Effort:** 30 min  
**Dependencies:** `IP/louis_core.py` exists

```bash
#!/bin/bash
# .git/hooks/pre-commit
# Louis enforcement - check if changes are authorized

python3 -c "
import sys
import subprocess
from pathlib import Path

# Add IP directory to path
sys.path.insert(0, str(Path.cwd() / 'IP'))

try:
    from louis_core import Louis
    louis = Louis('.')
    
    # Get staged files
    result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                          capture_output=True, text=True)
    staged_files = result.stdout.strip().split('\n')
    
    blocked = []
    for filepath in staged_files:
        if filepath and louis.is_locked(filepath):
            blocked.append(filepath)
    
    if blocked:
        print('❌ BLOCKED BY LOUIS:')
        for f in blocked:
            print(f'   🔒 {f}')
        print('\nUse Louis to unlock files before committing.')
        sys.exit(1)
    
    print('✅ Louis: All files cleared for commit')
    sys.exit(0)
    
except ImportError:
    # Louis not available, allow commit
    print('⚠️ Louis not found, skipping lock check')
    sys.exit(0)
except Exception as e:
    print(f'⚠️ Louis check failed: {e}')
    sys.exit(0)
"
```

**Installation:**
```bash
chmod +x .git/hooks/pre-commit
```

---

### Task BP-006: Create Git Post-Commit Hook (Carl Health Check)

**File:** `.git/hooks/post-commit`  
**Effort:** 30 min  
**Dependencies:** `IP/carl_core.py` exists

```bash
#!/bin/bash
# .git/hooks/post-commit
# Notify Orchestr8 that files changed - trigger health checks

python3 -c "
import sys
from pathlib import Path

# Add IP directory to path
sys.path.insert(0, str(Path.cwd() / 'IP'))

try:
    from health_checker import HealthChecker
    from mermaid_generator import Fiefdom, FiefdomStatus, generate_empire_mermaid
    import json
    
    # Load fiefdom config
    config_path = Path('.orchestr8/state/fiefdom-status.json')
    if config_path.exists():
        with open(config_path) as f:
            state = json.load(f)
        
        fiefdom_paths = list(state.get('fiefdoms', {}).keys())
        
        if fiefdom_paths:
            checker = HealthChecker('.')
            results = checker.check_all_fiefdoms(fiefdom_paths)
            
            print('📊 Post-commit health check:')
            for path, result in results.items():
                icon = '🟡' if result.status == 'working' else '🔵'
                print(f'   {icon} {path}: {result.status.upper()}')
                if result.errors:
                    print(f'      Errors: {len(result.errors)}')
    
except ImportError as e:
    print(f'⚠️ Health check skipped: {e}')
except Exception as e:
    print(f'⚠️ Health check failed: {e}')
"

echo "✅ Post-commit hook complete"
```

**Installation:**
```bash
chmod +x .git/hooks/post-commit
```

---

## Phase 3: Orchestr8 State Directory

### Task BP-007: Create .orchestr8 Directory Structure

**Effort:** 15 min  
**Dependencies:** None

```bash
# Create directory structure
mkdir -p .orchestr8/tickets/archive
mkdir -p .orchestr8/state

# Create initial state file
cat > .orchestr8/state/fiefdom-status.json << 'EOF'
{
  "fiefdoms": {},
  "last_health_check": null,
  "version": "4.0"
}
EOF

# Create .gitignore for orchestr8
cat > .orchestr8/.gitignore << 'EOF'
# Keep tickets but ignore archives
tickets/archive/*
!tickets/archive/.gitkeep

# State files are local
state/*.json

# Mermaid cache is regenerated
mermaid-cache.md
EOF

# Create archive placeholder
touch .orchestr8/tickets/archive/.gitkeep
```

---

## Phase 4: Plugin Integration

### Task BP-008: Update 06_maestro.py to Use New Modules

**File:** `IP/plugins/06_maestro.py`  
**Effort:** 2 hours  
**Dependencies:** BP-001 through BP-004 complete

**Integration Points:**
1. Import `mermaid_generator` for graph rendering
2. Import `terminal_spawner` for deployment
3. Import `health_checker` for status updates
4. Import `briefing_generator` for deployment prep

**Key Changes:**
```python
# Add imports at top of 06_maestro.py
from IP.mermaid_generator import Fiefdom, FiefdomStatus, generate_empire_mermaid
from IP.terminal_spawner import TerminalSpawner
from IP.health_checker import HealthChecker
from IP.briefing_generator import BriefingGenerator

# Initialize in plugin
spawner = TerminalSpawner(project_root)
checker = HealthChecker(project_root)
briefing_gen = BriefingGenerator(project_root)

# Replace hardcoded mermaid with dynamic generation
# Replace manual status tracking with checker.check_all_fiefdoms()
# Add deploy button that calls spawner.spawn()
```

---

## Phase 5: Ticket System Backend

### Task BP-009: Create Ticket Manager Module

**File:** `IP/ticket_manager.py`  
**Effort:** 1.5 hours  
**Dependencies:** BP-007 complete

**Functions Required:**
- `create_ticket(fiefdom, errors, context)` → ticket_id
- `update_ticket_status(ticket_id, status)`
- `add_note(ticket_id, author, text)`
- `get_ticket(ticket_id)` → Ticket object
- `list_tickets(status_filter=None)` → List[Ticket]
- `archive_ticket(ticket_id)`

---

### Task BP-010: Create Ticket Panel UI Component

**File:** `IP/plugins/components/ticket_panel.py`  
**Effort:** 2 hours  
**Dependencies:** BP-009 complete

**Requirements:**
- Slides from RIGHT when triggered
- Searchable ticket list
- Click to expand ticket details
- Add note functionality
- Status filter dropdown

---

## Summary

| Task | Module | Effort | Phase |
|------|--------|--------|-------|
| BP-001 | mermaid_generator.py | 30 min | 1 |
| BP-002 | terminal_spawner.py | 45 min | 1 |
| BP-003 | health_checker.py | 45 min | 1 |
| BP-004 | briefing_generator.py | 1 hour | 1 |
| BP-005 | pre-commit hook | 30 min | 2 |
| BP-006 | post-commit hook | 30 min | 2 |
| BP-007 | .orchestr8 directory | 15 min | 3 |
| BP-008 | 06_maestro.py integration | 2 hours | 4 |
| BP-009 | ticket_manager.py | 1.5 hours | 5 |
| BP-010 | ticket_panel.py | 2 hours | 5 |

**Total Estimated Effort:** ~10 hours

---

**END IMPLEMENTATION TASKS**
