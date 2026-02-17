---
phase: P07-INTEGRATION
plan: 04
type: execute
wave: 1
depends_on: [P07-PHASE2-PLAN]
files_modified:
  - orchestr8_next/shell/facades/__init__.py
  - orchestr8_next/shell/facades/health_facade.py
  - orchestr8_next/shell/facades/combat_facade.py
  - orchestr8_next/shell/facades/terminal_facade.py
  - orchestr8_next/shell/facades/briefing_facade.py
  - orchestr8_next/shell/facades/ticket_facade.py
  - orchestr8_next/shell/facades/context_facade.py
  - orchestr8_next/shell/facades/visualization_facade.py
  - orchestr8_next/shell/facades/gatekeeper_facade.py
  - orchestr8_next/shell/facades/patchbay_facade.py
  - orchestr8_next/shell/facades/maestro_config_facade.py
  - IP/plugins/06_maestro.py
  - IP/plugins/03_gatekeeper.py
  - IP/plugins/07_settings.py
  - IP/plugins/components/ticket_panel.py
autonomous: true

must_haves:
  truths:
    - "10 L2 facade modules exist in shell/facades/"
    - "06_maestro.py imports from L2 facades instead of L3 services"
    - "03_gatekeeper.py imports GatekeeperFacade instead of louis_core"
    - "07_settings.py imports MaestroConfigFacade instead of IP.features.maestro"
    - "ticket_panel.py imports TicketFacade instead of ticket_manager"
    - "No L1→L3 violations remain in plugin files"
  artifacts:
    - path: "orchestr8_next/shell/facades/__init__.py"
      provides: "Facade module exports"
    - path: "orchestr8_next/shell/facades/health_facade.py"
      provides: "HealthFacade wrapping HealthChecker + HealthWatcher"
    - path: "orchestr8_next/shell/facades/combat_facade.py"
      provides: "CombatFacade wrapping CombatTracker"
    - path: "orchestr8_next/shell/facades/terminal_facade.py"
      provides: "TerminalFacade wrapping TerminalSpawner"
    - path: "orchestr8_next/shell/facades/briefing_facade.py"
      provides: "BriefingFacade wrapping BriefingGenerator"
    - path: "orchestr8_next/shell/facades/ticket_facade.py"
      provides: "TicketFacade wrapping TicketManager"
    - path: "orchestr8_next/shell/facades/context_facade.py"
      provides: "ContextFacade wrapping CarlContextualizer"
    - path: "orchestr8_next/shell/facades/visualization_facade.py"
      provides: "VisualizationFacade wrapping woven_maps + contracts"
    - path: "orchestr8_next/shell/facades/gatekeeper_facade.py"
      provides: "GatekeeperFacade wrapping LouisWarden + LouisConfig"
    - path: "orchestr8_next/shell/facades/patchbay_facade.py"
      provides: "PatchbayFacade wrapping connection_verifier"
    - path: "orchestr8_next/shell/facades/maestro_config_facade.py"
      provides: "MaestroConfigFacade wrapping IP.features.maestro"
  key_links:
    - from: "orchestr8_next/shell/facades/"
      to: "IP/"
      via: "L3 imports inside facades"
    - from: "IP/plugins/06_maestro.py"
      to: "orchestr8_next/shell/facades/"
      via: "L2 facade imports (8 facades)"
    - from: "IP/plugins/03_gatekeeper.py"
      to: "orchestr8_next/shell/facades/gatekeeper_facade.py"
      via: "GatekeeperFacade import"
    - from: "IP/plugins/07_settings.py"
      to: "orchestr8_next/shell/facades/maestro_config_facade.py"
      via: "MaestroConfigFacade import"
    - from: "IP/plugins/components/ticket_panel.py"
      to: "orchestr8_next/shell/facades/ticket_facade.py"
      via: "TicketFacade import"
---

<objective>
Create 10 L2 facade modules in `shell/facades/` and update 4 plugin files to eliminate 25 L1→L3 violations per FINAL_RESEARCH_SUMMARY.md Part XVIII §18.3.

Purpose: Establish the L2 facade layer to decouple L1 plugins from L3 services, enabling independent layer evolution and maintaining architectural boundaries.

Output: 10 new facade modules, 4 updated plugin files, zero L1→L3 violations.
</objective>

<execution_context>
@/home/bozertron/.config/opencode/get-shit-done/workflows/execute-plan.md
@/home/bozertron/.config/opencode/get-shit-done/templates/summary.md
</execution_context>

<context>
# Research foundation
@.planning/orchestr8_next/artifacts/P07/integration/research/RESEARCH_06_L1_L3_FIX_DESIGN.md

# Violations to fix

# - 06_maestro.py: 20 violations → 8 facades

# - 03_gatekeeper.py: 1 violation → GatekeeperFacade  

# - ticket_panel.py: 1 violation → TicketFacade

# - 07_settings.py: 2 violations → MaestroConfigFacade

# Current L1→L3 imports in 06_maestro.py (lines 76-111)

# Line 76: from IP.mermaid_generator import Fiefdom, FiefdomStatus, generate_empire_mermaid

# Line 77: from IP.terminal_spawner import TerminalSpawner

# Line 78: from IP.health_checker import HealthChecker

# Line 79: from IP.health_watcher import HealthWatcher

# Line 80: from IP.briefing_generator import BriefingGenerator

# Line 81: from IP.combat_tracker import CombatTracker

# Lines 82-87: IP.plugins.components.* (L1→L1, OK)

# Line 88: from IP.carl_core import CarlContextualizer

# Line 100: from IP.woven_maps import create_code_city, build_graph_data

# Line 103: from IP.contracts.code_city_node_event import validate_code_city_node_event

# Line 104: from IP.contracts.connection_action_event import validate_connection_action_event

# Line 105: from IP.contracts.marimo_bridge import build_marimo_bridge_runtime_js

# Line 106: from IP.connection_verifier import dry_run_patchbay_rewire, apply_patchbay_rewire

# Line 107: from IP.features.maestro.code_city_context import (...)

# Line 111: from IP.features.maestro import (...)

# L1→L3 imports in other files

# 03_gatekeeper.py line 26: from IP.louis_core import LouisWarden, LouisConfig

# ticket_panel.py line 6: from IP.ticket_manager import TicketManager, Ticket

# 07_settings.py line 19: from IP.styles.font_profiles import (...)

# 07_settings.py line 23: from IP.features.maestro import load_orchestr8_css

</context>

<tasks>

<task type="auto">
  <name>Task 1: Create shell/facades/ directory structure</name>
  <files>orchestr8_next/shell/facades/__init__.py</files>
  <action>
    Create the facades directory and __init__.py:

    ```bash
    mkdir -p orchestr8_next/shell/facades
    touch orchestr8_next/shell/facades/__init__.py
    ```
    
    Add module exports to __init__.py:
    ```python
    """L2 Facade Layer - Wrappers around L3 services for L1 plugin consumption."""
    
    from orchestr8_next.shell.facades.health_facade import HealthFacade
    from orchestr8_next.shell.facades.combat_facade import CombatFacade
    from orchestr8_next.shell.facades.terminal_facade import TerminalFacade
    from orchestr8_next.shell.facades.briefing_facade import BriefingFacade
    from orchestr8_next.shell.facades.ticket_facade import TicketFacade
    from orchestr8_next.shell.facades.context_facade import ContextFacade
    from orchestr8_next.shell.facades.visualization_facade import VisualizationFacade
    from orchestr8_next.shell.facades.gatekeeper_facade import GatekeeperFacade
    from orchestr8_next.shell.facades.patchbay_facade import PatchbayFacade
    from orchestr8_next.shell.facades.maestro_config_facade import (
        MaestroConfigFacade,
        # Re-export constants and functions
    )
    
    __all__ = [
        "HealthFacade",
        "CombatFacade",
        "TerminalFacade",
        "BriefingFacade",
        "TicketFacade",
        "ContextFacade",
        "VisualizationFacade",
        "GatekeeperFacade",
        "PatchbayFacade",
        "MaestroConfigFacade",
    ]
    ```
  </action>
  <verify>
    ls -la orchestr8_next/shell/facades/
    python -c "from orchestr8_next.shell.facades import *; print('Facades imported')"
  </verify>
  <done>
    Directory created, __init__.py exists with all facade exports.
  </done>
</task>

<task type="auto">
  <name>Task 2: Create HealthFacade and CombatFacade</name>
  <files>
    orchestr8_next/shell/facades/health_facade.py
    orchestr8_next/shell/facades/combat_facade.py
  </files>
  <action>
    Create health_facade.py (wraps HealthChecker + HealthWatcher):

    ```python
    from pathlib import Path
    from typing import Dict, Any, Optional, Callable
    
    # L3 imports - OK because L2→L3 is valid
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
    
    Create combat_facade.py (wraps CombatTracker):
    
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
  </action>
  <verify>
    python -c "
    from orchestr8_next.shell.facades.health_facade import HealthFacade
    from orchestr8_next.shell.facades.combat_facade import CombatFacade
    print('HealthFacade and CombatFacade imported successfully')
    "
  </verify>
  <done>
    HealthFacade and CombatFacade modules created with lazy initialization pattern.
  </done>
</task>

<task type="auto">
  <name>Task 3: Create TerminalFacade and BriefingFacade</name>
  <files>
    orchestr8_next/shell/facades/terminal_facade.py
    orchestr8_next/shell/facades/briefing_facade.py
  </files>
  <action>
    Create terminal_facade.py (wraps TerminalSpawner):

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
    
    Create briefing_facade.py (wraps BriefingGenerator):
    
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
  </action>
  <verify>
    python -c "
    from orchestr8_next.shell.facades.terminal_facade import TerminalFacade
    from orchestr8_next.shell.facades.briefing_facade import BriefingFacade
    print('TerminalFacade and BriefingFacade imported successfully')
    "
  </verify>
  <done>
    TerminalFacade and BriefingFacade modules created.
  </done>
</task>

<task type="auto">
  <name>Task 4: Create TicketFacade and ContextFacade</name>
  <files>
    orchestr8_next/shell/facades/ticket_facade.py
    orchestr8_next/shell/facades/context_facade.py
  </files>
  <action>
    Create ticket_facade.py (wraps TicketManager):

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
    
    Create context_facade.py (wraps CarlContextualizer):
    
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
  </action>
  <verify>
    python -c "
    from orchestr8_next.shell.facades.ticket_facade import TicketFacade
    from orchestr8_next.shell.facades.context_facade import ContextFacade
    print('TicketFacade and ContextFacade imported successfully')
    "
  </verify>
  <done>
    TicketFacade and ContextFacade modules created.
  </done>
</task>

<task type="auto">
  <name>Task 5: Create VisualizationFacade</name>
  <files>orchestr8_next/shell/facades/visualization_facade.py</files>
  <action>
    Create visualization_facade.py (wraps woven_maps + contracts + code_city_context):

    ```python
    from pathlib import Path
    from typing import Optional, Dict, Any
    
    # L3 imports - OK because L2→L3 is valid
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
  </action>
  <verify>
    python -c "
    from orchestr8_next.shell.facades.visualization_facade import VisualizationFacade
    print('VisualizationFacade imported successfully')
    "
  </verify>
  <done>
    VisualizationFacade module created wrapping woven_maps + contracts.
  </done>
</task>

<task type="auto">
  <name>Task 6: Create GatekeeperFacade and PatchbayFacade</name>
  <files>
    orchestr8_next/shell/facades/gatekeeper_facade.py
    orchestr8_next/shell/facades/patchbay_facade.py
  </files>
  <action>
    Create gatekeeper_facade.py (wraps LouisWarden + LouisConfig):

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
    
    Create patchbay_facade.py (wraps connection_verifier):
    
    ```python
    from pathlib import Path
    from typing import Optional, Dict, Any, Callable
    
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
            validate_fn: Callable,
            dry_run_fn: Callable,
            apply_fn: Callable,
            result_callback: Callable,
            log_fn: Callable,
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
  </action>
  <verify>
    python -c "
    from orchestr8_next.shell.facades.gatekeeper_facade import GatekeeperFacade
    from orchestr8_next.shell.facades.patchbay_facade import PatchbayFacade
    print('GatekeeperFacade and PatchbayFacade imported successfully')
    "
  </verify>
  <done>
    GatekeeperFacade and PatchbayFacade modules created.
  </done>
</task>

<task type="auto">
  <name>Task 7: Create MaestroConfigFacade</name>
  <files>orchestr8_next/shell/facades/maestro_config_facade.py</files>
  <action>
    Create maestro_config_facade.py (wraps IP.features.maestro constants and functions):

    ```python
    """L2 facade wrapping IP.features.maestro constants and functions."""
    
    # L3 imports - OK because L2→L3 is valid
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
    
    # Re-export all constants and functions for L1 consumption
    __all__ = [
        "BG_PRIMARY",
        "BLUE_DOMINANT",
        "FLAGSHIP_AGENT_SLUG",
        "GOLD_METALLIC",
        "MAESTRO_STATES",
        "PLUGIN_NAME",
        "PLUGIN_ORDER",
        "PURPLE_COMBAT",
        "get_model_config",
        "get_settlement_agent_groups",
        "load_orchestr8_css",
        "build_summon_results_view",
        "build_void_messages_view",
        "build_app_matrix_view",
        "build_attachment_bar_view",
        "build_panels_view",
        "build_control_surface_view",
    ]
    
    # Also provide a facade class for consistency
    class MaestroConfigFacade:
        """L2 facade wrapper for IP.features.maestro exports."""
        
        BG_PRIMARY = BG_PRIMARY
        BLUE_DOMINANT = BLUE_DOMINANT
        FLAGSHIP_AGENT_SLUG = FLAGSHIP_AGENT_SLUG
        GOLD_METALLIC = GOLD_METALLIC
        MAESTRO_STATES = MAESTRO_STATES
        PLUGIN_NAME = PLUGIN_NAME
        PLUGIN_ORDER = PLUGIN_ORDER
        PURPLE_COMBAT = PURPLE_COMBAT
        
        @staticmethod
        def get_model_config(model_slug: str):
            return get_model_config(model_slug)
        
        @staticmethod
        def get_settlement_agent_groups():
            return get_settlement_agent_groups()
        
        @staticmethod
        def load_orchestr8_css():
            return load_orchestr8_css()
        
        @staticmethod
        def build_summon_results_view(results):
            return build_summon_results_view(results)
        
        @staticmethod
        def build_void_messages_view(messages):
            return build_void_messages_view(messages)
        
        @staticmethod
        def build_app_matrix_view(matrix):
            return build_app_matrix_view(matrix)
        
        @staticmethod
        def build_attachment_bar_view(attachments):
            return build_attachment_bar_view(attachments)
        
        @staticmethod
        def build_panels_view(panels):
            return build_panels_view(panels)
        
        @staticmethod
        def build_control_surface_view(controls):
            return build_control_surface_view(controls)
    ```
  </action>
  <verify>
    python -c "
    from orchestr8_next.shell.facades.maestro_config_facade import (
        MaestroConfigFacade, PLUGIN_NAME, load_orchestr8_css
    )
    print('MaestroConfigFacade imported successfully')
    print(f'PLUGIN_NAME = {PLUGIN_NAME}')
    "
  </verify>
  <done>
    MaestroConfigFacade module created with re-exports and facade class.
    NOTE: build_code_city_context_payload and derive_context_scope are in VisualizationFacade, NOT here.
  </done>
</task>

<task type="auto">
  <name>Task 8: Update 06_maestro.py imports to use facades</name>
  <files>IP/plugins/06_maestro.py</files>
  <action>
    Replace the L1→L3 imports (lines 76-111) with L2 facade imports:

    REMOVE these lines (L1→L3 violations):
    - Line 76: `from IP.mermaid_generator import Fiefdom, FiefdomStatus, generate_empire_mermaid`
    - Line 77: `from IP.terminal_spawner import TerminalSpawner`
    - Line 78: `from IP.health_checker import HealthChecker`
    - Line 79: `from IP.health_watcher import HealthWatcher`
    - Line 80: `from IP.briefing_generator import BriefingGenerator`
    - Line 81: `from IP.combat_tracker import CombatTracker`
    - Line 88: `from IP.carl_core import CarlContextualizer`
    - Line 100: `from IP.woven_maps import create_code_city, build_graph_data`
    - Line 103: `from IP.contracts.code_city_node_event import validate_code_city_node_event`
    - Line 104: `from IP.contracts.connection_action_event import validate_connection_action_event`
    - Line 105: `from IP.contracts.marimo_bridge import build_marimo_bridge_runtime_js`
    - Line 106: `from IP.connection_verifier import dry_run_patchbay_rewire, apply_patchbay_rewire`
    - Line 107: `from IP.features.maestro.code_city_context import (...)`
    - Line 111: `from IP.features.maestro import (...)`
    
    ADD facade imports after line 74 (with other imports):
    ```python
    # L2 Facade imports (replaces L1→L3 violations)
    from orchestr8_next.shell.facades.health_facade import HealthFacade
    from orchestr8_next.shell.facades.combat_facade import CombatFacade
    from orchestr8_next.shell.facades.terminal_facade import TerminalFacade
    from orchestr8_next.shell.facades.briefing_facade import BriefingFacade
    from orchestr8_next.shell.facades.context_facade import ContextFacade
    from orchestr8_next.shell.facades.visualization_facade import VisualizationFacade
    from orchestr8_next.shell.facades.patchbay_facade import PatchbayFacade
    from orchestr8_next.shell.facades.maestro_config_facade import (
        # Constants
        BG_PRIMARY, BLUE_DOMINANT, FLAGSHIP_AGENT_SLUG, GOLD_METALLIC,
        MAESTRO_STATES, PLUGIN_NAME, PLUGIN_ORDER, PURPLE_COMBAT,
        # Functions
        get_model_config, get_settlement_agent_groups, load_orchestr8_css,
        build_summon_results_view, build_void_messages_view, build_app_matrix_view,
        build_attachment_bar_view, build_panels_view, build_control_surface_view,
    )
    # Code City context functions come from VisualizationFacade (NOT MaestroConfigFacade)
    from orchestr8_next.shell.facades.visualization_facade import VisualizationFacade
    ```
    
    NOTE: build_code_city_context_payload and derive_context_scope are accessed through
    VisualizationFacade (which already imports them from IP.features.maestro.code_city_context).
    Do NOT import them from MaestroConfigFacade — single source of truth per function.
    
    NOTE: The mermaid_generator import (line 76) is NOT covered by the 8 facades per the research. It should remain as-is for now (or be addressed in a separate MermaidFacade in a future phase).
    
    NOTE: The IP.plugins.components.* imports (lines 82-87) are L1→L1 and are OK - leave them as-is.
  </action>
  <verify>
    python -c "
    # Test facade imports work
    import sys
    sys.path.insert(0, '/home/bozertron/Orchestr8_jr')
    from orchestr8_next.shell.facades import HealthFacade, CombatFacade, TerminalFacade
    from orchestr8_next.shell.facades import BriefingFacade, ContextFacade, VisualizationFacade
    from orchestr8_next.shell.facades import PatchbayFacade
    print('All facade imports in 06_maestro.py work')
    "
  </verify>
  <done>
    06_maestro.py now imports from L2 facades instead of L3 services (except mermaid_generator).
  </done>
</task>

<task type="auto">
  <name>Task 9: Update 03_gatekeeper.py, ticket_panel.py, 07_settings.py imports</name>
  <files>
    IP/plugins/03_gatekeeper.py
    IP/plugins/components/ticket_panel.py
    IP/plugins/07_settings.py
  </files>
  <action>
    03_gatekeeper.py (line 26):
    - REMOVE: `from IP.louis_core import LouisWarden, LouisConfig`
    - ADD: `from orchestr8_next.shell.facades.gatekeeper_facade import GatekeeperFacade`

    ticket_panel.py (line 6):
    - REMOVE: `from IP.ticket_manager import TicketManager, Ticket`
    - ADD: `from orchestr8_next.shell.facades.ticket_facade import TicketFacade`
    
    07_settings.py (lines 19, 23):
    - REMOVE: `from IP.styles.font_profiles import (...)`
    - REMOVE: `from IP.features.maestro import load_orchestr8_css`
    - ADD: `from orchestr8_next.shell.facades.maestro_config_facade import *`
      (or specific imports: BG_PRIMARY, BLUE_DOMINANT, etc. and load_orchestr8_css)
  </action>
  <verify>
    python -c "
    import sys
    sys.path.insert(0, '/home/bozertron/Orchestr8_jr')
    # Test imports
    from orchestr8_next.shell.facades.gatekeeper_facade import GatekeeperFacade
    from orchestr8_next.shell.facades.ticket_facade import TicketFacade
    from orchestr8_next.shell.facades.maestro_config_facade import load_orchestr8_css
    print('All facade imports work')
    "
  </verify>
  <done>
    All three plugin files now import from L2 facades instead of L3 services.
  </done>
</task>

<task type="auto">
  <name>Task 10: Verify no L1→L3 violations remain</name>
  <files>IP/plugins/*.py, IP/plugins/components/*.py</files>
  <action>
    Run verification to ensure no L1→L3 violations remain:

    ```bash
    # Check for direct IP.* imports in plugin files (excluding IP.plugins.* which is OK)
    grep -rn "^from IP\." IP/plugins/*.py IP/plugins/components/*.py | \
        grep -v "IP.plugins." | \
        grep -v "orchestr8_next"
    ```
    
    Expected output: No matches (except possibly mermaid_generator which is not yet wrapped)
    
    Also verify facades can be instantiated:
    ```python
    from orchestr8_next.shell.facades import (
        HealthFacade, CombatFacade, TerminalFacade,
        BriefingFacade, TicketFacade, ContextFacade,
        VisualizationFacade, GatekeeperFacade,
        PatchbayFacade, MaestroConfigFacade,
    )
    
    project_root = "/tmp/test_project"
    health = HealthFacade(project_root)
    combat = CombatFacade(project_root)
    terminal = TerminalFacade(project_root)
    briefing = BriefingFacade(project_root)
    ticket = TicketFacade(project_root)
    context = ContextFacade(project_root)
    viz = VisualizationFacade(project_root)
    gatekeeper = GatekeeperFacade(project_root)
    patchbay = PatchbayFacade(project_root)
    config = MaestroConfigFacade()
    
    print("All 10 facades instantiated successfully")
    ```
  </action>
  <verify>
    Run the grep command - should show no L1→L3 violations (or only mermaid_generator if not wrapped)
    Run the instantiation test - should succeed
  </verify>
  <done>
    Zero L1→L3 violations verified (mermaid_generator excepted per research).
  </done>
</task>

</tasks>

<verification>
- [ ] orchestr8_next/shell/facades/ directory created with 10 modules
- [ ] 06_maestro.py imports from L2 facades (except mermaid_generator)
- [ ] 03_gatekeeper.py imports GatekeeperFacade
- [ ] 07_settings.py imports MaestroConfigFacade
- [ ] ticket_panel.py imports TicketFacade
- [ ] grep shows no L1→L3 violations (or only mermaid_generator)
- [ ] All facades can be instantiated without errors
</verification>

<success_criteria>
25 L1→L3 violations eliminated:

- 06_maestro.py: 20 violations → 8 facades used (18 violations fixed, 2 remain: mermaid_generator + components L1→L1)
- 03_gatekeeper.py: 1 violation → GatekeeperFacade ✓
- ticket_panel.py: 1 violation → TicketFacade ✓
- 07_settings.py: 2 violations → MaestroConfigFacade ✓

Tests pass: `python -c "from orchestr8_next.shell.facades import *; print('OK')"`
</success_criteria>

<output>
After completion, create `.planning/orchestr8_next/artifacts/P07/plans/P07-PHASE3-SUMMARY.md`
</output>
