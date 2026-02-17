# Phase 06: L1→L3 Violation Fix Design - Research

**Researched:** February 16, 2026
**Domain:** Layer Architecture / Cross-Layer Dependency Resolution
**Confidence:** HIGH

## Summary

This research identifies and designs L2 facade modules to fix cross-layer violations where L1 plugin files (in `IP/plugins/`) directly import L3 services (in `IP/` root-level modules). The analysis reveals 25 direct L1→L3 imports across 4 plugin files that violate the architectural layer boundaries. The solution involves creating thin L2 facade modules in `orchestr8_next/shell/` that wrap L3 services while providing a stable interface for L1 plugins.

**Primary recommendation:** Create 8 L2 facade modules in `orchestr8_next/shell/` that wrap the L3 services, then update all L1 plugins to import from the L2 facades instead of directly from L3 modules.

## Standard Stack

### Current Architecture (Violating)

| Layer | Location | Description |
|-------|----------|-------------|
| L1 (Plugins) | `IP/plugins/*.py` | UI plugins (06_maestro, 03_gatekeeper, etc.) |
| L2 (MISSING) | `orchestr8_next/shell/` | Facade layer (currently has only state management) |
| L3 (Services) | `IP/*.py` | Business logic (health_checker, combat_tracker, etc.) |

### Recommended Architecture (Fixed)

| Layer | Location | Purpose |
|-------|----------|---------|
| L1 (Plugins) | `IP/plugins/*.py` | Import from L2 facades only |
| L2 (Facades) | `orchestr8_next/shell/facades/*.py` | Thin wrappers around L3 services |
| L3 (Services) | `IP/*.py` | Unchanged - L3 imports L3 OK |

## L1→L3 Violations Identified

### File: 06_maestro.py (20 violations)

| Line | Import Statement | L3 Module | Used For |
|------|-----------------|-----------|----------|
| 76 | `from IP.mermaid_generator import Fiefdom, FiefdomStatus, generate_empire_mermaid` | L3 | Data generation |
| 77 | `from IP.terminal_spawner import TerminalSpawner` | L3 | Side effects (spawn terminal) |
| 78 | `from IP.health_checker import HealthChecker` | L3 | Data + side effects |
| 79 | `from IP.health_watcher import HealthWatcher` | L3 | Side effects (file watching) |
| 80 | `from IP.briefing_generator import BriefingGenerator` | L3 | Data generation |
| 81 | `from IP.combat_tracker import CombatTracker` | L3 | Data + side effects |
| 82-87 | Various `IP.plugins.components.*` imports | L1→L1 | These are OK (L1→L1) |
| 88 | `from IP.carl_core import CarlContextualizer` | L3 | Data generation |
| 100 | `from IP.woven_maps import create_code_city, build_graph_data` | L3 | Data generation |
| 103 | `from IP.contracts.code_city_node_event import validate_code_city_node_event` | L3 | Data validation |
| 104 | `from IP.contracts.connection_action_event import validate_connection_action_event` | L3 | Data validation |
| 105 | `from IP.contracts.marimo_bridge import build_marimo_bridge_runtime_js` | L3 | Data generation |
| 106 | `from IP.connection_verifier import dry_run_patchbay_rewire, apply_patchbay_rewire` | L3 | Side effects |
| 107 | `from IP.features.maestro.code_city_context import (...)` | L3 | Data generation |
| 111 | `from IP.features.maestro import (...)` | L3 | Constants + data |

### File: 03_gatekeeper.py (1 violation)

| Line | Import Statement | L3 Module | Used For |
|------|-----------------|-----------|----------|
| 26 | `from IP.louis_core import LouisWarden, LouisConfig` | L3 | Data + side effects |

### File: IP/plugins/components/ticket_panel.py (1 violation)

| Line | Import Statement | L3 Module | Used For |
|------|-----------------|-----------|----------|
| 6 | `from IP.ticket_manager import TicketManager, Ticket` | L3 | Data + side effects |

### File: 07_settings.py (2 violations)

| Line | Import Statement | L3 Module | Used For |
|------|-----------------|-----------|----------|
| 19 | `from IP.styles.font_profiles import (...)` | L3 | Data |
| 23 | `from IP.features.maestro import load_orchestr8_css` | L3 | Side effects |

### File: 05_universal_bridge.py (1 violation)

| Line | Import Statement | L3 Module | Used For |
|------|-----------------|-----------|----------|
| 45 | `from IP.plugins.output_renderer import detect_and_render_output` | L1 | OK (L1→L1) |

## L2 Facade Design

### Facade 1: HealthFacade
**File:** `orchestr8_next/shell/facades/health_facade.py`

```python
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from IP.health_checker import HealthChecker, HealthCheckResult
from IP.health_watcher import HealthWatcher

class HealthFacade:
    """L2 facade wrapping HealthChecker and HealthWatcher."""
    
    def __init__(self, project_root: str):
        self._project_root = Path(project_root)
        self._health_checker: Optional[HealthChecker] = None
        self._health_watcher: Optional[HealthWatcher] = None
        self._callback: Optional[Callable[[Dict[str, Any]], None]] = None
    
    def get_checker(self) -> HealthChecker:
        """Get or create HealthChecker instance."""
        if self._health_checker is None:
            self._health_checker = HealthChecker(str(self._project_root))
        return self._health_checker
    
    def check_fiefdom(self, fiefdom: str) -> HealthCheckResult:
        """Run health check on a fiefdom."""
        return self.get_checker().check_fiefdom(fiefdom)
    
    def get_results(self) -> Dict[str, Any]:
        """Get current health results as dict."""
        checker = self.get_checker()
        # Run check on IP by default
        result = checker.check_fiefdom("IP")
        return result.to_dict()
    
    def start_watching(self, root: Optional[Path] = None, callback: Optional[Callable] = None) -> None:
        """Start file watching with optional callback."""
        watch_root = root or self._project_root
        self._callback = callback
        
        def wrapped_callback(results: Dict[str, Any]) -> None:
            if self._callback:
                self._callback(results)
        
        self._health_watcher = HealthWatcher(str(watch_root), wrapped_callback)
        self._health_watcher.start_watching()
    
    def stop_watching(self) -> None:
        """Stop file watching."""
        if self._health_watcher:
            self._health_watcher.stop_watching()
```

**Migration path for 06_maestro.py:**
- Replace: `from IP.health_checker import HealthChecker` + `from IP.health_watcher import HealthWatcher`
- With: `from orchestr8_next.shell.facades.health_facade import HealthFacade`

---

### Facade 2: CombatFacade
**File:** `orchestr8_next/shell/facades/combat_facade.py`

```python
from pathlib import Path
from typing import Dict, Optional
from IP.combat_tracker import CombatTracker

class CombatFacade:
    """L2 facade wrapping CombatTracker."""
    
    def __init__(self, project_root: str):
        self._project_root = Path(project_root)
        self._tracker: Optional[CombatTracker] = None
    
    def _get_tracker(self) -> CombatTracker:
        if self._tracker is None:
            self._tracker = CombatTracker(str(self._project_root))
        return self._tracker
    
    def deploy(self, file_path: str, terminal_id: str, model: str = "unknown") -> None:
        """Mark file as having an LLM General deployed."""
        self._get_tracker().deploy(file_path, terminal_id, model)
    
    def withdraw(self, file_path: str) -> None:
        """Remove LLM General deployment from file."""
        self._get_tracker().withdraw(file_path)
    
    def is_in_combat(self, file_path: str) -> bool:
        """Check if file has active deployment."""
        return self._get_tracker().is_in_combat(file_path)
    
    def get_deployment_info(self, file_path: str) -> Optional[Dict]:
        """Get deployment info for a file."""
        return self._get_tracker().get_deployment_info(file_path)
    
    def get_active_deployments(self) -> Dict[str, dict]:
        """Get all active deployments."""
        return self._get_tracker().get_active_deployments()
    
    def cleanup_stale_deployments(self, max_age_hours: int = 24) -> int:
        """Remove deployments older than max_age_hours."""
        return self._get_tracker().cleanup_stale_deployments(max_age_hours)
```

**Migration path for 06_maestro.py:**
- Replace: `from IP.combat_tracker import CombatTracker`
- With: `from orchestr8_next.shell.facades.combat_facade import CombatFacade`

---

### Facade 3: TerminalFacade
**File:** `orchestr8_next/shell/facades/terminal_facade.py`

```python
from pathlib import Path
from typing import Optional
from IP.terminal_spawner import TerminalSpawner

class TerminalFacade:
    """L2 facade wrapping TerminalSpawner."""
    
    def __init__(self, project_root: str):
        self._project_root = Path(project_root)
        self._spawner: Optional[TerminalSpawner] = None
    
    def _get_spawner(self) -> TerminalSpawner:
        if self._spawner is None:
            self._spawner = TerminalSpawner(str(self._project_root))
        return self._spawner
    
    def spawn(
        self,
        fiefdom_path: str,
        briefing_ready: bool = True,
        auto_start_claude: bool = False,
    ) -> bool:
        """Spawn terminal at fiefdom path."""
        return self._get_spawner().spawn(
            fiefdom_path=fiefdom_path,
            briefing_ready=briefing_ready,
            auto_start_claude=auto_start_claude,
        )
    
    def update_fiefdom_status(self, fiefdom_path: str, status: str) -> None:
        """Update fiefdom status in state file."""
        self._get_spawner().update_fiefdom_status(fiefdom_path, status)
```

**Migration path for 06_maestro.py:**
- Replace: `from IP.terminal_spawner import TerminalSpawner`
- With: `from orchestr8_next.shell.facades.terminal_facade import TerminalFacade`

---

### Facade 4: BriefingFacade
**File:** `orchestr8_next/shell/facades/briefing_facade.py`

```python
from pathlib import Path
from typing import Optional, List, Dict, Any
from IP.briefing_generator import BriefingGenerator

class BriefingFacade:
    """L2 facade wrapping BriefingGenerator."""
    
    def __init__(self, project_root: str):
        self._project_root = Path(project_root)
        self._generator: Optional[BriefingGenerator] = None
    
    def _get_generator(self) -> BriefingGenerator:
        if self._generator is None:
            self._generator = BriefingGenerator(self._project_root)
        return self._generator
    
    def load_campaign_log(self, file_path: str) -> List[Dict[str, Any]]:
        """Load campaign context for a file."""
        return self._get_generator().load_campaign_log(file_path)
    
    def generate_briefing(self, target_path: str) -> Optional[str]:
        """Generate BRIEFING.md for target path."""
        return self._get_generator().generate_briefing(target_path)
```

**Migration path for 06_maestro.py:**
- Replace: `from IP.briefing_generator import BriefingGenerator`
- With: `from orchestr8_next.shell.facades.briefing_facade import BriefingFacade`

---

### Facade 5: TicketFacade
**File:** `orchestr8_next/shell/facades/ticket_facade.py`

```python
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from IP.ticket_manager import TicketManager, Ticket

@dataclass
class TicketData:
    """Simplified ticket data for L1 consumption."""
    id: str
    title: str
    status: str
    file_path: str

class TicketFacade:
    """L2 facade wrapping TicketManager."""
    
    def __init__(self, project_root: str):
        self._project_root = Path(project_root)
        self._manager: Optional[TicketManager] = None
    
    def _get_manager(self) -> TicketManager:
        if self._manager is None:
            self._manager = TicketManager(str(self._project_root))
        return self._manager
    
    def get_tickets(self) -> List[TicketData]:
        """Get all tickets."""
        return self._get_manager().get_tickets()
    
    def create_ticket(self, title: str, file_path: str, error: str) -> TicketData:
        """Create a new ticket."""
        ticket = self._get_manager().create_ticket(title, file_path, error)
        return TicketData(
            id=ticket.id,
            title=ticket.title,
            status=ticket.status,
            file_path=ticket.file_path,
        )
    
    def resolve_ticket(self, ticket_id: str) -> None:
        """Mark ticket as resolved."""
        self._get_manager().resolve_ticket(ticket_id)
```

**Migration paths:**
- 06_maestro.py: Replace component imports with facade
- ticket_panel.py: Replace `from IP.ticket_manager import TicketManager, Ticket`

---

### Facade 6: ContextFacade (Carl)
**File:** `orchestr8_next/shell/facades/context_facade.py`

```python
from pathlib import Path
from typing import Optional, Any
from IP.carl_core import CarlContextualizer

class ContextFacade:
    """L2 facade wrapping CarlContextualizer."""
    
    def __init__(self, project_root: str):
        self._project_root = Path(project_root)
        self._contextualizer: Optional[CarlContextualizer] = None
    
    def _get_contextualizer(self) -> CarlContextualizer:
        if self._contextualizer is None:
            self._contextualizer = CarlContextualizer(str(self._project_root))
        return self._contextualizer
    
    def gather_context(self, scope: str) -> Any:
        """Gather context for a given scope."""
        return self._get_contextualizer().gather_context(scope)
    
    def search(self, query: str, scope: Optional[str] = None) -> Any:
        """Search context with query."""
        return self._get_contextualizer().search(query, scope)
```

**Migration path for 06_maestro.py:**
- Replace: `from IP.carl_core import CarlContextualizer`
- With: `from orchestr8_next.shell.facades.context_facade import ContextFacade`

---

### Facade 7: VisualizationFacade (Woven Maps)
**File:** `orchestr8_next/shell/facades/visualization_facade.py`

```python
from pathlib import Path
from typing import Optional, Dict, Any
from IP.woven_maps import create_code_city, build_graph_data
from IP.contracts.code_city_node_event import validate_code_city_node_event
from IP.contracts.connection_action_event import validate_connection_action_event
from IP.contracts.marimo_bridge import build_marimo_bridge_runtime_js
from IP.features.maestro.code_city_context import (
    build_code_city_context_payload,
    derive_context_scope,
)

class VisualizationFacade:
    """L2 facade wrapping Woven Maps and Code City visualization."""
    
    def __init__(self, project_root: str):
        self._project_root = Path(project_root)
    
    def create_code_city(
        self,
        root: str,
        width: int = 1200,
        height: int = 680,
        health_results: Optional[Dict[str, Any]] = None,
    ):
        """Create Code City visualization."""
        return create_code_city(root, width, height, health_results)
    
    def build_graph_data(self, root: str) -> Dict[str, Any]:
        """Build graph data for visualization."""
        return build_graph_data(root)
    
    def validate_node_event(self, payload: dict) -> Any:
        """Validate node click event."""
        return validate_code_city_node_event(payload)
    
    def validate_connection_action(self, payload: dict) -> Any:
        """Validate connection action event."""
        return validate_connection_action_event(payload)
    
    def build_bridge_runtime_js(self) -> str:
        """Build Marimo bridge runtime JavaScript."""
        return build_marimo_bridge_runtime_js()
    
    def build_code_city_context(
        self,
        node_data: dict,
        project_root: Path,
        context: Any = None,
    ) -> Dict[str, Any]:
        """Build code city context payload."""
        return build_code_city_context_payload(node_data, project_root, context)
    
    def derive_context_scope(self, file_path: str) -> str:
        """Derive context scope from file path."""
        return derive_context_scope(file_path)
```

**Migration path for 06_maestro.py:**
- Replace: Multiple IP.woven_maps, IP.contracts.*, IP.features.maestro.* imports
- With: Single `from orchestr8_next.shell.facades.visualization_facade import VisualizationFacade`

---

### Facade 8: GatekeeperFacade
**File:** `orchestr8_next/shell/facades/gatekeeper_facade.py`

```python
from pathlib import Path
from typing import Optional, Dict, Any
from IP.louis_core import LouisWarden, LouisConfig

class GatekeeperFacade:
    """L2 facade wrapping LouisWarden and LouisConfig."""
    
    def __init__(self, project_root: str):
        self._project_root = Path(project_root)
        self._config: Optional[LouisConfig] = None
        self._warden: Optional[LouisWarden] = None
    
    def _get_config(self) -> LouisConfig:
        if self._config is None:
            self._config = LouisConfig(str(self._project_root))
        return self._config
    
    def _get_warden(self) -> LouisWarden:
        if self._warden is None:
            self._warden = LouisWarden(self._get_config())
        return self._warden
    
    def get_protection_status(self) -> Dict[str, Dict[str, Any]]:
        """Get protection status for all tracked files."""
        return self._get_warden().get_protection_status()
    
    def lock_file(self, file_path: str) -> None:
        """Lock a file (set to read-only)."""
        self._get_warden().lock_file(file_path)
    
    def unlock_file(self, file_path: str) -> None:
        """Unlock a file (set to read-write)."""
        self._get_warden().unlock_file(file_path)
    
    def lock_all(self) -> None:
        """Lock all protected files."""
        self._get_warden().lock_all()
    
    def unlock_all(self) -> None:
        """Unlock all protected files."""
        self._get_warden().unlock_all()
    
    def add_protected_path(self, path: str) -> None:
        """Add path to protection list."""
        self._get_warden().add_protected_path(path)
    
    def remove_protected_path(self, path: str) -> None:
        """Remove path from protection list."""
        self._get_warden().remove_protected_path(path)
    
    def install_git_hook(self) -> bool:
        """Install pre-commit hook."""
        return self._get_warden().install_git_hook()
```

**Migration path for 03_gatekeeper.py:**
- Replace: `from IP.louis_core import LouisWarden, LouisConfig`
- With: `from orchestr8_next.shell.facades.gatekeeper_facade import GatekeeperFacade`

---

### Facade 9: PatchbayFacade
**File:** `orchestr8_next/shell/facades/patchbay_facade.py`

```python
from pathlib import Path
from typing import Optional, Dict, Any
from IP.connection_verifier import dry_run_patchbay_rewire, apply_patchbay_rewire
from IP.features.maestro import handle_connection_action

class PatchbayFacade:
    """L2 facade wrapping Patchbay connection verification."""
    
    def __init__(self, project_root: str):
        self._project_root = Path(project_root)
    
    def dry_run(self, payload: dict) -> Dict[str, Any]:
        """Perform dry-run of patchbay rewire."""
        return dry_run_patchbay_rewire(payload)
    
    def apply(self, payload: dict) -> Dict[str, Any]:
        """Apply patchbay rewire."""
        return apply_patchbay_rewire(payload)
    
    def handle_action(
        self,
        payload: dict,
        project_root: Path,
        validate_fn,
        dry_run_fn,
        apply_fn,
        result_callback,
        log_fn,
    ) -> None:
        """Handle connection action."""
        handle_connection_action(
            payload,
            project_root=project_root,
            validate_connection_action_event=validate_fn,
            dry_run_patchbay_rewire=dry_run_fn,
            apply_patchbay_rewire=apply_fn,
            set_connection_action_result_payload=result_callback,
            log_action=log_fn,
        )
```

**Migration path for 06_maestro.py:**
- Replace: `from IP.connection_verifier import dry_run_patchbay_rewire, apply_patchbay_rewire`
- With: `from orchestr8_next.shell.facades.patchbay_facade import PatchbayFacade`

---

### Facade 10: MaestroConfigFacade
**File:** `orchestr8_next/shell/facades/maestro_config_facade.py`

```python
from IP.features.maestro import (
    BG_PRIMARY,
    BLUE_DOMINANT,
    FLAGSHIP_AGENT_SLUG,
    GOLD_METALLIC,
    MAESTRO_STATES,
    PLUGIN_NAME,
    PLUGIN_ORDER,
    PURPLE_COMBAT,
    get_model_config,
    get_settlement_agent_groups,
    load_orchestr8_css,
    build_summon_results_view,
    build_void_messages_view,
    build_app_matrix_view,
    build_attachment_bar_view,
    build_panels_view,
    build_control_surface_view,
)

# Re-export all constants and functions
__all__ = [
    "BG_PRIMARY", "BLUE_DOMINANT", "FLAGSHIP_AGENT_SLUG",
    "GOLD_METALLIC", "MAESTRO_STATES", "PLUGIN_NAME",
    "PLUGIN_ORDER", "PURPLE_COMBAT", "get_model_config",
    "get_settlement_agent_groups", "load_orchestr8_css",
    "build_summon_results_view", "build_void_messages_view",
    "build_app_matrix_view", "build_attachment_bar_view",
    "build_panels_view", "build_control_surface_view",
]
```

**Migration path for 06_maestro.py:**
- Replace: `from IP.features.maestro import (...)` (multiple items)
- With: `from orchestr8_next.shell.facades.maestro_config_facade import *`

---

## Migration Steps

### Step 1: Create L2 Facade Directory Structure

```bash
mkdir -p orchestr8_next/shell/facades
touch orchestr8_next/shell/facades/__init__.py
```

### Step 2: Create Each Facade Module

Create files listed above in `orchestr8_next/shell/facades/`

### Step 3: Update L1 Plugins

**06_maestro.py:**
```python
# BEFORE (violation)
from IP.health_checker import HealthChecker
from IP.health_watcher import HealthWatcher
from IP.combat_tracker import CombatTracker
from IP.terminal_spawner import TerminalSpawner
from IP.briefing_generator import BriefingGenerator
from IP.carl_core import CarlContextualizer
from IP.woven_maps import create_code_city, build_graph_data
from IP.contracts.code_city_node_event import validate_code_city_node_event
# ... 20+ violations

# AFTER (compliant)
from orchestr8_next.shell.facades.health_facade import HealthFacade
from orchestr8_next.shell.facades.combat_facade import CombatFacade
from orchestr8_next.shell.facades.terminal_facade import TerminalFacade
from orchestr8_next.shell.facades.briefing_facade import BriefingFacade
from orchestr8_next.shell.facades.context_facade import ContextFacade
from orchestr8_next.shell.facades.visualization_facade import VisualizationFacade
from orchestr8_next.shell.facades.patchbay_facade import PatchbayFacade
from orchestr8_next.shell.facades.maestro_config_facade import *
```

**03_gatekeeper.py:**
```python
# BEFORE
from IP.louis_core import LouisWarden, LouisConfig

# AFTER
from orchestr8_next.shell.facades.gatekeeper_facade import GatekeeperFacade
```

**IP/plugins/components/ticket_panel.py:**
```python
# BEFORE
from IP.ticket_manager import TicketManager, Ticket

# AFTER
from orchestr8_next.shell.facades.ticket_facade import TicketFacade
```

### Step 4: Verify No L1→L3 Imports Remain

```bash
grep -rn "^from IP\." IP/plugins/*.py | grep -v "IP.plugins.components" | grep -v "orchestr8_next"
```

Expected: No matches (except IP.plugins.* which is L1→L1 OK)

## Test Verification Plan

### Unit Tests for Each Facade

```python
# tests/shell/facades/test_health_facade.py
import pytest
from pathlib import Path
from orchestr8_next.shell.facades.health_facade import HealthFacade

def test_health_facade_initialization():
    facade = HealthFacade("/tmp/test_project")
    assert facade._project_root == Path("/tmp/test_project")
    assert facade._health_checker is None

def test_get_checker_creates_instance():
    facade = HealthFacade("/tmp/test_project")
    checker = facade.get_checker()
    assert checker is not None
    # Same instance on second call
    assert facade.get_checker() is checker
```

### Integration Tests

```python
# tests/shell/facades/test_integration.py
def test_facades_work_with_maestro():
    """Verify facades work within Maestro plugin context."""
    from orchestr8_next.shell.facades import (
        HealthFacade, CombatFacade, TerminalFacade,
        ContextFacade, VisualizationFacade,
    )
    
    project_root = "/tmp/test_orchestr8"
    Path(project_root).mkdir(exist_ok=True)
    
    health = HealthFacade(project_root)
    combat = CombatFacade(project_root)
    terminal = TerminalFacade(project_root)
    context = ContextFacade(project_root)
    viz = VisualizationFacade(project_root)
    
    # Verify all can be instantiated
    assert health is not None
    assert combat is not None
    assert terminal is not None
    assert context is not None
    assert viz is not None
```

### Architecture Verification

```bash
# Verify no L1→L3 violations remain
python -c "
import subprocess
import re

result = subprocess.run(
    ['grep', '-rn', '^from IP\\.', 'IP/plugins/'],
    capture_output=True, text=True
)

violations = []
for line in result.stdout.strip().split('\n'):
    if line:
        # Skip IP.plugins.* imports (L1→L1 is OK)
        if 'IP.plugins.' not in line:
            violations.append(line)

if violations:
    print('L1→L3 VIOLATIONS FOUND:')
    for v in violations:
        print(f'  {v}')
    exit(1)
else:
    print('✓ No L1→L3 violations found')
    print('✓ Only L1→L1 imports remain (IP.plugins.*)')
"
```

## Common Pitfalls

### Pitfall 1: Facade Instantiation in State
**Problem:** Creating new facade instances on every render causes state loss
**Solution:** Initialize facades once at plugin startup, pass through state managers

### Pitfall 2: Circular Imports
**Problem:** Facades importing from each other creates circular dependencies
**Solution:** Keep facades independent, import L3 directly if needed

### Pitfall 3: Side Effects in Facades
**Problem:** HealthWatcher spawns threads - must be managed carefully
**Solution:** Explicit start/stop methods, cleanup on plugin unload

### Pitfall 4: Path Resolution
**Problem:** L1 plugins may run from different working directories
**Solution:** Always use absolute paths resolved from project root

## Open Questions

1. **Component Panel Imports:** The `IP.plugins.components.*` imports in 06_maestro.py (lines 82-87) are L1→L1 and technically OK. Should these also be moved to facades for consistency?

2. **Shared State:** Currently each plugin creates its own facade instances. Should there be a shared facade manager for the entire application?

3. **L4→L3 Violations:** The task mentioned L4→L3/L5 violations in woven_maps.py. Analysis shows woven_maps.py imports from `IP.contracts.*` and `IP.features.*` - both are L3→L3 (OK). Need to verify if this is actually a violation.

4. **07_settings.py Violations:** The font_profiles and load_orchestr8_css imports may need additional facades or can be handled differently.

## Sources

### Primary (HIGH confidence)
- File inspection: `/home/bozertron/Orchestr8_jr/IP/plugins/06_maestro.py` - Lines 76-130
- File inspection: `/home/bozertron/Orchestr8_jr/IP/plugins/03_gatekeeper.py` - Line 26
- File inspection: `/home/bozertron/Orchestr8_jr/IP/health_checker.py` - HealthChecker class interface
- File inspection: `/home/bozertron/Orchestr8_jr/IP/combat_tracker.py` - CombatTracker class interface
- File inspection: `/home/bozertron/Orchestr8_jr/IP/terminal_spawner.py` - TerminalSpawner class interface

### Secondary (MEDIUM confidence)
- Directory structure analysis: orchestr8_next/shell/ has state management but no facades
- Layer architecture: L1=plugins, L2=missing, L3=services confirmed

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Verified through file inspection
- Architecture patterns: HIGH - Based on existing orchestr8_next structure
- Facade design: HIGH - Based on L3 service interfaces
- Pitfalls: MEDIUM - Based on typical Python architecture patterns

**Research date:** February 16, 2026
**Valid until:** June 2026 (stable architecture)
