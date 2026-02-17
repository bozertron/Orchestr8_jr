"""
06_maestro Plugin - The Void
Orchestr8 v3.0 - Central Command Interface

The heart of Orchestr8 - a unified command center inspired by MaestroView.
Implements the spatial UI pattern with:
- Top navigation bar (orchestr8 | collabor8 | JFDI)
- Central void for AI conversation emergence
- Bottom control surface (the Overton anchor)

Design Principles (from MaestroView.vue):
- NO breathing animations
- Messages EMERGE from the void
- UI elements do not 'load'; they EMERGE when summoned
- The Input Bar: Docked at bottom. It NEVER moves.

Colors (EXACT - NO EXCEPTIONS):
--blue-dominant: #1fbdea (UI default, Broken state)
--gold-metallic: #D4AF37 (UI highlight, Working state)
--gold-dark: #B8860B (Maestro default)
--gold-saffron: #F4C430 (Maestro highlight)
--bg-primary: #050505 (The Void)
--bg-elevated: #121214 (Surface)
--purple-combat: #9D4EDD (Combat state - General deployed)

Three-State System:
- Gold (#D4AF37): Working - All imports resolve, typecheck passes
- Blue (#1fbdea): Broken - Has errors, needs attention
- Purple (#9D4EDD): Combat - General currently deployed and active

Reference: UI Reference/MaestroView.vue
"""

# ============================================================================
# PATH RESOLUTION - Ensures IP package is importable when run directly
# ============================================================================
# This block allows the plugin to work both:
# 1. When run directly: python IP/plugins/06_maestro.py
# 2. When imported as part of the package via orchestr8 app
#
# The IP package lives at the project root level, so we need to ensure
# the project root is in sys.path before importing IP modules.
# ============================================================================
import sys
from pathlib import Path as _Path

# Resolve the project root (3 levels up: 06_maestro.py -> plugins -> IP -> project_root)
_THIS_FILE = _Path(__file__).resolve()
_PROJECT_ROOT = _THIS_FILE.parent.parent.parent

# Add project root to sys.path if not already present
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# Verify IP package is now importable (fail loudly if not, per user request)
try:
    import IP  # noqa: F401 - Import to verify package is accessible
except ImportError as e:
    raise ImportError(
        f"Failed to import IP package. "
        f"Project root '{_PROJECT_ROOT}' was added to sys.path but IP module not found. "
        f"Ensure the IP package exists at {_PROJECT_ROOT / 'IP'}. "
        f"Original error: {e}"
    ) from e

# ============================================================================
# STANDARD LIBRARY IMPORTS
# ============================================================================
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path
import uuid
import os

# Import new modules
from IP.mermaid_generator import Fiefdom, FiefdomStatus, generate_empire_mermaid
from IP.terminal_spawner import TerminalSpawner
from IP.health_checker import HealthChecker
from IP.health_watcher import HealthWatcher
from IP.briefing_generator import BriefingGenerator
from IP.combat_tracker import CombatTracker
from IP.plugins.components.ticket_panel import TicketPanel
from IP.plugins.components.calendar_panel import CalendarPanel
from IP.plugins.components.comms_panel import CommsPanel
from IP.plugins.components.file_explorer_panel import FileExplorerPanel
from IP.plugins.components.deploy_panel import DeployPanel
from IP.plugins.components.intent_panel import IntentPanel
from IP.carl_core import CarlContextualizer

# Optional: anthropic SDK for chat functionality
try:
    import anthropic

    HAS_ANTHROPIC = True
except ImportError:
    anthropic = None
    HAS_ANTHROPIC = False

# Import Woven Maps Code City visualization
from IP.woven_maps import create_code_city, build_graph_data

# Import contract validation for node click events and building panel
from IP.contracts.code_city_node_event import validate_code_city_node_event
from IP.contracts.connection_action_event import validate_connection_action_event
from IP.contracts.marimo_bridge import build_marimo_bridge_runtime_js
from IP.connection_verifier import dry_run_patchbay_rewire, apply_patchbay_rewire
from IP.features.maestro.code_city_context import (
    build_code_city_context_payload,
    derive_context_scope,
)
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
    handle_connection_action,
    load_orchestr8_css,
    build_summon_results_view,
    build_void_messages_view,
    build_app_matrix_view,
    build_attachment_bar_view,
    build_panels_view,
    build_control_surface_view,
)
import json


def render(STATE_MANAGERS: dict) -> Any:
    """
    Render the Maestro Command Center.

    Implements the MaestroView.vue spatial UI pattern:
    - Top row with navigation
    - Central void for message emergence
    - Bottom control surface

    Args:
        STATE_MANAGERS: Dictionary of state getters/setters

    Returns:
        Marimo UI element
    """
    import marimo as mo

    # ========================================================================
    # STATE MANAGEMENT
    # ========================================================================

    # Global state from STATE_MANAGERS
    get_root, set_root = STATE_MANAGERS["root"]
    get_selected, set_selected = STATE_MANAGERS["selected"]
    get_logs, set_logs = STATE_MANAGERS["logs"]
    get_health, set_health = STATE_MANAGERS["health"]
    flagship_agent = FLAGSHIP_AGENT_SLUG

    # Get available models from settings
    def get_available_models() -> list:
        """Load available models from pyproject_orchestr8_settings.toml."""
        try:
            import toml

            settings_file = Path("pyproject_orchestr8_settings.toml")
            if settings_file.exists():
                settings = toml.load(settings_file)
                models = (
                    settings.get("tools", {})
                    .get("communic8", {})
                    .get("multi_llm", {})
                    .get("default_models", [])
                )
                if models:
                    return models
        except Exception:
            pass
        return ["claude", "gpt-4", "gemini", "local"]

    available_models = get_available_models()

    # Local state - Panel visibility
    get_show_agents, set_show_agents = mo.state(False)
    get_show_terminal, set_show_terminal = mo.state(False)
    get_show_summon, set_show_summon = mo.state(False)
    get_show_settings, set_show_settings = mo.state(False)

    # Local state - Conversation
    get_messages, set_messages = mo.state([])
    get_user_input, set_user_input = mo.state("")

    # Local state - Attachments
    get_attached_files, set_attached_files = mo.state([])

    # Local state - View mode for THE VOID
    get_view_mode, set_view_mode = mo.state("city")  # "city" | "chat" | "matrix"

    # Maestro trigger state
    get_maestro_state, set_maestro_state = mo.state("ON")

    # Phreak SFX trigger counter (increment to replay)
    get_phreak_sfx_tick, set_phreak_sfx_tick = mo.state(0)

    # Combat refresh trigger - increments when combat state changes to refresh Code City
    get_combat_refresh, set_combat_refresh = mo.state(0)

    # Local state - Selected model
    model_config = get_model_config()
    config_model = model_config.get("model", "claude")
    # Ensure default_model is actually in available_models
    default_model = (
        config_model
        if config_model in available_models
        else (available_models[0] if available_models else "claude")
    )
    get_selected_model, set_selected_model = mo.state(default_model)

    # Initialize services
    project_root_path = get_root()
    combat_tracker = CombatTracker(project_root_path)
    briefing_generator = BriefingGenerator(project_root_path)
    terminal_spawner = TerminalSpawner(project_root_path)
    ticket_panel = TicketPanel(project_root_path)
    calendar_panel = CalendarPanel(project_root_path)
    comms_panel = CommsPanel(project_root_path)
    file_explorer_panel = FileExplorerPanel(project_root_path)
    deploy_panel = DeployPanel(project_root_path)
    intent_panel = IntentPanel(project_root_path)

    carl = CarlContextualizer(str(project_root_path))

    def on_health_change(results: dict) -> None:
        """Callback when health check completes - merges into health state."""
        current = get_health() or {}
        current.update(results)
        set_health(current)
        log_action(f"Health update: {len(results)} file(s) checked")

    health_watcher = HealthWatcher(str(project_root_path), on_health_change)

    def refresh_health() -> None:
        """Run HealthChecker on project root and update health state."""
        health_checker = HealthChecker(str(project_root_path))
        result = health_checker.check_fiefdom("IP")
        set_health({"IP": result})
        log_action(f"Health check complete: {result.status}")

    # Local state - Ticket panel visibility
    get_show_tickets, set_show_tickets = mo.state(False)

    # Local state - Calendar, Comms, FileExplorer panel visibility
    get_show_calendar, set_show_calendar = mo.state(False)
    get_show_comms, set_show_comms = mo.state(False)
    get_show_file_explorer, set_show_file_explorer = mo.state(False)

    # Local state - Deploy panel (House a Digital Native?)
    get_show_deploy, set_show_deploy = mo.state(False)

    # Local state - Intent panel (C2P Intent Queue)
    get_show_intents, set_show_intents = mo.state(False)
    get_intent_data, set_intent_data = mo.state([])

    get_clicked_node, set_clicked_node = mo.state(
        None
    )  # Node data from Code City click

    # Local state - Audio recording
    get_is_recording, set_is_recording = mo.state(False)
    get_audio_data, set_audio_data = mo.state(
        None
    )  # Stores recorded audio as bytes/numpy

    # Local state - Summon panel search
    get_summon_query, set_summon_query = mo.state("")
    get_summon_results, set_summon_results = mo.state([])
    get_summon_loading, set_summon_loading = mo.state(False)

    # Local state - Node click bridge channel (hidden input for JS->Python bridge)
    get_node_click_payload, set_node_click_payload = mo.state("")

    # Local state - Connection action bridge (edge panel actions from Code City)
    get_connection_action_payload, set_connection_action_payload = mo.state("")
    get_camera_nav_payload, set_camera_nav_payload = mo.state("")
    get_connection_action_result_payload, set_connection_action_result_payload = (
        mo.state("")
    )
    # Local state - normalized context from latest Code City selection
    get_code_city_context, set_code_city_context = mo.state({})

    # Local state - Collabor8 deployment controls
    settlement_agent_groups = get_settlement_agent_groups()
    get_agent_group, set_agent_group = mo.state("Explore")
    get_agent_id, set_agent_id = mo.state("surveyor")

    # ========================================================================
    # EVENT HANDLERS (Transliterated from MaestroView.vue)
    # ========================================================================

    def log_action(action: str) -> None:
        """Log action to system logs."""
        logs = get_logs()
        timestamp = datetime.now().strftime("%H:%M:%S")
        set_logs(logs + [f"[{timestamp}] [Maestro] {action}"])

    # Clean up stale combat deployments on startup (>24h auto-expires)
    try:
        combat_tracker.cleanup_stale_deployments(max_age_hours=24)
        log_action("Combat tracker: stale deployments cleaned")
    except Exception as e:
        log_action(f"Combat tracker cleanup error: {e}")

    def cycle_maestro_state() -> None:
        """Cycle maestro mode: ON -> OFF -> OBSERVE -> ON."""
        current = get_maestro_state()
        idx = MAESTRO_STATES.index(current) if current in MAESTRO_STATES else 0
        next_state = MAESTRO_STATES[(idx + 1) % len(MAESTRO_STATES)]
        set_maestro_state(next_state)
        log_action(f"@{flagship_agent} mode: {next_state}")

    def toggle_tickets() -> None:
        """Toggle ticket panel (slides from right)."""
        current = get_show_tickets()
        set_show_tickets(not current)
        ticket_panel.set_visible(not current)

    def toggle_intents() -> None:
        """Toggle intent panel (C2P Intent Queue - slides from right)."""
        current = get_show_intents()
        set_show_intents(not current)
        intent_panel.set_visible(not current)

        # Close other right panels for mutual exclusion
        if not current:
            set_show_tickets(False)
            ticket_panel.set_visible(False)
            set_show_calendar(False)
            calendar_panel.set_visible(False)
            set_show_comms(False)
            comms_panel.set_visible(False)
            set_show_file_explorer(False)
            file_explorer_panel.set_visible(False)
            log_action("Intent Queue panel opened")
        else:
            log_action("Intent Queue panel closed")

    def toggle_calendar() -> None:
        """Toggle calendar panel (slides from right)."""
        current = get_show_calendar()
        set_show_calendar(not current)
        calendar_panel.set_visible(not current)
        # Close other right panels for mutual exclusion
        if not current:
            set_show_comms(False)
            comms_panel.set_visible(False)
            set_show_file_explorer(False)
            file_explorer_panel.set_visible(False)
            log_action("Calendar panel opened")
        else:
            log_action("Calendar panel closed")

    def toggle_comms() -> None:
        """Toggle comms panel (slides from right)."""
        current = get_show_comms()
        set_show_comms(not current)
        comms_panel.set_visible(not current)
        # Close other right panels for mutual exclusion
        if not current:
            set_show_calendar(False)
            calendar_panel.set_visible(False)
            set_show_file_explorer(False)
            file_explorer_panel.set_visible(False)
            log_action("Comms panel opened")
        else:
            log_action("Comms panel closed")

    def toggle_file_explorer() -> None:
        """Toggle file explorer panel (slides from right)."""
        current = get_show_file_explorer()
        set_show_file_explorer(not current)
        file_explorer_panel.set_visible(not current)
        # Close other right panels for mutual exclusion
        if not current:
            set_show_calendar(False)
            calendar_panel.set_visible(False)
            set_show_comms(False)
            comms_panel.set_visible(False)
            log_action("File Explorer panel opened")
        else:
            log_action("File Explorer panel closed")

    def process_node_click(payload: dict) -> None:
        """
        Bridge function that validates node click payload and calls handle_node_click.
        Performs schema validation via contract before passing to handler.

        Args:
            payload: Raw node click data from JavaScript (dict)
        """
        if not payload:
            return

        try:
            # Validate payload via contract
            validated = validate_code_city_node_event(payload)
            # Pass validated data to handler
            handle_node_click(validated.to_dict())
        except ValueError as e:
            # Schema validation failed - log but don't crash UI
            log_action(f"Invalid node click payload: {e}")
        except Exception as e:
            # Unexpected error - log but don't crash UI
            log_action(f"Node click processing error: {e}")

    def process_connection_action(payload: dict) -> None:
        """Bridge edge panel actions to feature-sliced Patchbay handlers."""
        handle_connection_action(
            payload,
            project_root_path=project_root_path,
            validate_connection_action_event=validate_connection_action_event,
            dry_run_patchbay_rewire=dry_run_patchbay_rewire,
            apply_patchbay_rewire=apply_patchbay_rewire,
            set_connection_action_result_payload=set_connection_action_result_payload,
            log_action=log_action,
        )

    def handle_node_click(node_data: dict) -> None:
        """
        Handle click on Code City building node.

        Behavior by status:
        - broken: Auto-generate ticket payload from Carl context + health errors,
                  show deploy panel with enriched context
        - combat: Show "Agent active" status message
        - working: Show building info panel (read-only inspection)
        """
        if not node_data:
            return

        status = node_data.get("status", "working")
        file_path = node_data.get("path", "")
        set_selected(file_path)

        log_action(f"Building clicked: {file_path} ({status})")

        context_scope = derive_context_scope(file_path)
        context = None
        try:
            context = carl.gather_context(context_scope)
        except Exception as e:
            log_action(f"Carl context gathering failed for {context_scope}: {e}")

        try:
            code_city_context = build_code_city_context_payload(
                node_data,
                project_root=project_root_path,
                context=context,
            )
            set_code_city_context(code_city_context)
            room_entry = code_city_context.get("room_entry")
            if room_entry:
                log_action(
                    "Room entry trigger: "
                    f"{room_entry.get('name')} ({room_entry.get('room_type')}) "
                    f"[{room_entry.get('trigger')}]"
                )
        except Exception as e:
            log_action(f"Building panel context error: {e}")
            code_city_context = {
                "path": file_path,
                "status": status,
                "context_scope": context_scope,
            }
            set_code_city_context(code_city_context)

        if status == "broken":
            # Gather enriched context from Carl for broken nodes
            try:
                # Merge health errors from node + Carl context
                all_errors = list(node_data.get("errors", []))
                if context:
                    for health_err in context.health.get("errors", []):
                        err_msg = f"{health_err.get('file', file_path)}:{health_err.get('line', '?')} - {health_err.get('message', 'Unknown error')}"
                        if err_msg not in all_errors:
                            all_errors.append(err_msg)

                # Generate structured ticket payload
                ticket_payload = {
                    "path": file_path,
                    "status": status,
                    "errors": all_errors,
                    "suggested_action": f"Investigate and fix errors in {file_path.split('/')[-1]}",
                    "context": {
                        "health_status": context.health.get("status", "broken")
                        if context
                        else "broken",
                        "broken_imports": context.connections.get("broken", [])
                        if context
                        else [],
                        "tickets": context.tickets if context else [],
                        "locks": context.locks if context else [],
                        "combat_active": context.combat.get("active", False)
                        if context
                        else False,
                    },
                    "building_panel": code_city_context.get("building_panel", {}),
                    "room_entry": code_city_context.get("room_entry"),
                }

                log_action(
                    f"Ticket payload generated: {len(all_errors)} error(s), "
                    f"{len(context.tickets) if context else 0} ticket(s)"
                )

            except Exception as e:
                # Fallback to basic node data if Carl fails
                log_action(f"Carl context gathering failed: {e}")
                ticket_payload = {
                    "path": file_path,
                    "status": status,
                    "errors": node_data.get("errors", []),
                    "suggested_action": f"Investigate and fix errors in {file_path.split('/')[-1]}",
                    "context": code_city_context,
                }

            # Show deploy panel with enriched context
            set_clicked_node(ticket_payload)
            deploy_panel.show(
                file_path=file_path,
                status=status,
                errors=ticket_payload["errors"],
            )
            set_show_deploy(True)
            log_action(f"Deploy panel opened for {file_path}")
            if code_city_context.get("room_entry"):
                set_view_mode("sitting_room")
                log_action("Sitting Room engaged from broken-room trigger")

        elif status == "combat":
            # Already in combat - show status message
            deployment_info = combat_tracker.get_deployment_info(file_path)
            if deployment_info:
                model = deployment_info.get("model", "Unknown")
                log_action(f"Agent active on {file_path}: {model}")
            else:
                log_action(f"{file_path} is in COMBAT state")

        else:
            # Working file - show building info (read-only inspection)
            log_action(f"Selected (working): {file_path}")

    def handle_deploy() -> None:
        """
        Deploy the selected general to fix broken code.
        Building goes PURPLE. Joy ensues.
        """
        result = deploy_panel.deploy()

        if not result.get("success"):
            log_action(f"Deploy failed: {result.get('error')}")
            return

        file_path = result["file_path"]
        general = result["general"]
        mode = result["mode"]

        # Track deployment in combat tracker (building goes purple)
        combat_tracker.deploy(
            file_path=file_path,
            terminal_id=f"deploy-{datetime.now().strftime('%H%M%S')}",
            model=general,
        )

        # Trigger Code City refresh to show purple combat state
        set_combat_refresh(get_combat_refresh() + 1)

        log_action(f"DEPLOYED {general} to {file_path} ({mode} mode)")

        if mode == "terminal":
            # Spawn terminal with the general
            briefing_path = project_root_path / file_path
            if briefing_path.is_file():
                briefing_path = briefing_path.parent

            terminal_spawner.spawn(
                fiefdom_path=str(briefing_path),
                briefing_ready=True,
                auto_start_claude=True,
            )
            log_action(f"Terminal spawned for {file_path}")

        # Close deploy panel
        deploy_panel.hide()
        set_show_deploy(False)
        set_clicked_node(None)

    def close_deploy_panel() -> None:
        """Close the deploy panel without deploying."""
        deploy_panel.hide()
        set_show_deploy(False)
        set_clicked_node(None)
        log_action("Deploy panel closed")

    def toggle_collabor8() -> None:
        """Toggle Collabor8 panel."""
        current = get_show_agents()
        set_show_agents(not current)
        if not current:
            set_show_settings(False)
            log_action("Collabor8 panel opened")
        else:
            log_action("Collabor8 panel closed")

    def handle_jfdi() -> None:
        """JFDI is ticket-first: open/close TicketPanel from top row."""
        set_show_agents(False)
        set_show_settings(False)
        toggle_tickets()
        log_action("JFDI toggled ticket panel")

    def toggle_settings_panel() -> None:
        """Toggle Settings overlay from bottom controls."""
        current = get_show_settings()
        set_show_settings(not current)
        if not current:
            set_show_agents(False)
            log_action("Settings panel opened")
        else:
            log_action("Settings panel closed")

    def set_collabor8_group(group: str) -> None:
        """Update Collabor8 group and reset selected agent to first entry."""
        set_agent_group(group)
        agents = settlement_agent_groups.get(group, [])
        if agents:
            set_agent_id(agents[0]["id"])

    def deploy_selected_agent() -> None:
        """Mark selected file as in combat for chosen settlement agent."""
        selected_group = get_agent_group()
        selected_id = get_agent_id()
        group_agents = settlement_agent_groups.get(selected_group, [])
        agent = next((a for a in group_agents if a["id"] == selected_id), None)
        if not agent:
            return
        target = get_selected() or "IP/plugins/06_maestro.py"
        combat_tracker.deploy(
            file_path=target,
            terminal_id=f"settlement-{agent['id']}",
            model="settlement-agent",
        )
        # Trigger Code City refresh to show purple combat state
        set_combat_refresh(get_combat_refresh() + 1)
        log_action(f"Deployed {agent['name']} (T{agent['tier']}) to {target}")

    def handle_terminal() -> None:
        """Toggle terminal panel and spawn actu8 if opening."""
        current = get_show_terminal()
        set_show_terminal(not current)

        if not current:  # Opening terminal
            set_phreak_sfx_tick(get_phreak_sfx_tick() + 1)
            selected = get_selected()
            # Use selected file's directory or project root
            fiefdom_path = selected if selected else "."

            # Check if BRIEFING.md exists
            briefing_path = project_root_path / fiefdom_path
            if briefing_path.is_file():
                briefing_path = briefing_path.parent
            briefing_ready = (briefing_path / "BRIEFING.md").exists()

            # Spawn the terminal
            success = terminal_spawner.spawn(
                fiefdom_path=str(fiefdom_path),
                briefing_ready=briefing_ready,
                auto_start_claude=False,
            )

            if success:
                # Track in CombatTracker if file selected
                if selected:
                    combat_tracker.deploy(
                        file_path=selected,
                        terminal_id="actu8-terminal",
                        model="terminal",
                    )
                log_action(f"Terminal spawned at {fiefdom_path}")
            else:
                log_action(f"Failed to spawn terminal at {fiefdom_path}")
        else:
            log_action("Terminal closed")

    def handle_home_click() -> None:
        """Reset to home state - clear panels and messages."""
        set_messages([])
        set_show_agents(False)
        set_show_settings(False)
        set_show_terminal(False)
        set_show_summon(False)
        set_show_tickets(False)
        set_show_calendar(False)
        set_show_comms(False)
        set_show_file_explorer(False)
        set_code_city_context({})
        ticket_panel.set_visible(False)
        calendar_panel.set_visible(False)
        comms_panel.set_visible(False)
        file_explorer_panel.set_visible(False)
        set_view_mode("city")
        log_action("Reset to home state")

    def toggle_recording() -> None:
        """Toggle audio recording state."""
        current = get_is_recording()
        set_is_recording(not current)
        if not current:
            log_action("Recording started - speak into microphone")
            # In browser mode, would use JavaScript MediaRecorder API
            # For now, just toggle state
        else:
            log_action("Recording stopped")
            # Would capture audio data here

    def handle_playback() -> None:
        """Play back recorded audio."""
        audio = get_audio_data()
        if audio is not None:
            log_action("Playing audio...")
            # Would use mo.audio(audio) to play
        else:
            log_action("No audio recording available")

    def has_audio_recording() -> bool:
        """Check if there's audio data to play back."""
        return get_audio_data() is not None

    def handle_apps() -> None:
        """Show App Matrix in THE VOID."""
        set_view_mode("matrix")
        log_action("App Matrix opened")

    def handle_matrix() -> None:
        """
        Matrix button - raise coding software, LLMs, and Contacts.
        The unified view of your development environment.
        """
        try:
            import subprocess

            # Open VS Code or preferred editor
            editors = ["code", "cursor", "codium", "subl", "atom", "gedit"]
            for editor in editors:
                try:
                    subprocess.Popen([editor, str(project_root_path)])
                    log_action(f"Opened {editor} at {project_root_path}")
                    break
                except FileNotFoundError:
                    continue

            # Also show the agents panel (LLMs)
            set_show_agents(True)
            set_show_settings(False)
            log_action("Matrix: Code editor + Collabor8 panel")
        except Exception as e:
            log_action(f"Matrix error: {e}")

    def handle_files() -> None:
        """Open file explorer at project root."""
        try:
            import subprocess
            import platform

            system = platform.system()

            if system == "Linux":
                # Try various file managers
                for fm in ["nautilus", "dolphin", "thunar", "pcmanfm", "nemo"]:
                    try:
                        subprocess.Popen([fm, str(project_root_path)])
                        log_action(f"Opened {fm} at {project_root_path}")
                        return
                    except FileNotFoundError:
                        continue
            elif system == "Darwin":
                subprocess.Popen(["open", str(project_root_path)])
                log_action(f"Opened Finder at {project_root_path}")
            elif system == "Windows":
                subprocess.Popen(["explorer", str(project_root_path)])
                log_action(f"Opened Explorer at {project_root_path}")
        except Exception as e:
            log_action(f"Failed to open file explorer: {e}")

    def handle_send() -> None:
        """Send message to the void."""
        text = get_user_input().strip()
        if not text:
            return

        messages = list(get_messages())

        # Add user message
        user_msg = {
            "id": str(uuid.uuid4()),
            "role": "user",
            "content": text,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        }
        messages.append(user_msg)

        trigger_token = f"@{flagship_agent}"
        # Flagship trigger is local and respects ON/OFF/OBSERVE state.
        if text.lower().startswith(trigger_token.lower()):
            command = text[len(trigger_token) :].strip()
            state = get_maestro_state()
            set_view_mode("chat")

            if state == "OFF":
                assistant_content = f"[INFO] {trigger_token} is OFF. Use the {flagship_agent} button to cycle mode."
            elif state == "OBSERVE":
                set_show_summon(True)
                if command:
                    set_summon_query(command)
                    trigger_carl_search(command)
                assistant_content = f"[OBSERVE] {trigger_token} observing: {command or 'no query provided'}"
            else:
                set_show_summon(True)
                if command:
                    set_summon_query(command)
                    trigger_carl_search(command)
                assistant_content = (
                    f"[ON] {trigger_token} engaged: {command or 'summon panel opened'}"
                )

            messages.append(
                {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": assistant_content,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                }
            )
            set_messages(messages)
            set_user_input("")
            log_action(f"{trigger_token} trigger received ({state})")
            return

        set_view_mode("chat")

        optimistic_id = str(uuid.uuid4())
        optimistic_msg = {
            "id": optimistic_id,
            "role": "assistant",
            "content": "Thinking...",
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "optimistic": True,
        }
        messages.append(optimistic_msg)
        set_messages(messages)

        def finalize_optimistic(content: str) -> None:
            finalized = []
            for msg in messages:
                if msg.get("id") == optimistic_id:
                    updated = dict(msg)
                    updated["content"] = content
                    updated["optimistic"] = False
                    updated["timestamp"] = datetime.now().strftime("%H:%M:%S")
                    finalized.append(updated)
                else:
                    finalized.append(msg)
            set_messages(finalized)

        # LLM API Integration
        if not HAS_ANTHROPIC:
            # Anthropic not installed - graceful fallback
            finalize_optimistic(
                "[INFO] Chat requires the anthropic SDK.\n\nInstall with: `pip install anthropic`\n\nCode City visualization still works!"
            )
            set_user_input("")
            return

        try:
            # Initialize Anthropic client
            client = anthropic.Anthropic()

            # Generate context using BriefingGenerator
            selected_file = get_selected()
            context_parts = []

            if selected_file:
                # Add file context
                context_parts.append(f"Current file: {selected_file}")

                # Add campaign context if available
                campaign_context = briefing_generator.load_campaign_log(selected_file)
                if campaign_context:
                    context_parts.append("Recent campaign activity:")
                    for entry in campaign_context[:3]:  # Last 3 entries
                        context_parts.append(f"- {entry.get('summary', 'No summary')}")

            # Build system prompt
            system_prompt = """You are the General of the Orchestr8 command system. You provide concise, actionable responses to help developers manage their software projects. Focus on clarity and immediate next steps."""

            if context_parts:
                system_prompt += f"\n\nContext:\n" + "\n".join(context_parts)

            # Call Claude API with selected model from dropdown
            selected_model = get_selected_model()
            model_config = get_model_config()
            response = client.messages.create(
                model=selected_model,
                max_tokens=model_config["max_tokens"],
                system=system_prompt,
                messages=[{"role": "user", "content": text}],
            )

            # Extract response content
            response_content = (
                response.content[0].text
                if hasattr(response.content[0], "text")
                else str(response.content[0])
            )

            # Track deployment in CombatTracker if working on selected file
            if selected_file:
                combat_tracker.deploy(
                    file_path=selected_file,
                    terminal_id="maestro-chat",
                    model=selected_model,
                )
                # Trigger Code City refresh to show purple combat state
                set_combat_refresh(get_combat_refresh() + 1)

            # Create assistant message
            finalize_optimistic(response_content)

        except Exception as e:
            error_name = type(e).__name__
            if "AuthenticationError" in error_name:
                log_action(f"LLM Authentication Error: {str(e)}")
                finalize_optimistic(
                    "[WARNING] Authentication Error: Invalid ANTHROPIC_API_KEY\n\nPlease check your API key in environment variables."
                )
            elif "APIError" in error_name:
                log_action(f"LLM API Error: {str(e)}")
                finalize_optimistic(
                    f"[WARNING] LLM API Error: {str(e)}\n\nPlease check your ANTHROPIC_API_KEY environment variable and network connection."
                )
            else:
                log_action(f"Unexpected Error: {str(e)}")
                finalize_optimistic(f"[WARNING] Unexpected Error: {str(e)}")

        set_user_input("")
        log_action(f"Message sent: {text[:50]}...")

    def handle_attach() -> None:
        """Attach selected file to conversation."""
        selected = get_selected()
        if selected:
            attached = get_attached_files()
            if selected not in attached:
                set_attached_files(attached + [selected])
                log_action(f"Attached: {selected}")

    def remove_attachment(file_path: str) -> None:
        """Remove file from attachments."""
        attached = get_attached_files()
        set_attached_files([f for f in attached if f != file_path])

    def handle_summon() -> None:
        """Open summon (global search) overlay."""
        set_show_summon(not get_show_summon())
        log_action("Summon toggled")

    def trigger_carl_search(query: str, scope: Optional[str] = None) -> None:
        """
        Trigger Carl context search with query filter.
        Non-blocking - Carl collects, he doesn't block.
        """
        if not query or len(query) < 2:
            set_summon_results([])
            return

        set_summon_loading(True)
        log_action(f"Summon search: {query}")

        try:
            scoped_target = (
                scope
                or get_selected()
                or (get_code_city_context() or {}).get("context_scope")
                or "IP"
            )
            context = carl.gather_context(scoped_target)

            results = []
            context_dict = {
                "fiefdom": context.fiefdom,
                "scope": scoped_target,
                "health": {
                    "status": context.health.get("status", "working"),
                    "errors": context.health.get("errors", []),
                    "warnings": context.health.get("warnings", []),
                },
                "connections": context.connections,
                "combat": context.combat,
                "tickets": context.tickets,
                "locks": context.locks,
            }

            query_lower = query.lower()

            if (
                query_lower in context.fiefdom.lower()
                or query_lower in scoped_target.lower()
            ):
                results.append(context_dict)

            for err in context.health.get("errors", []):
                if query_lower in err.get("message", "").lower():
                    results.append(context_dict)
                    break

            for ticket in context.tickets:
                if query_lower in ticket.lower():
                    results.append(context_dict)
                    break

            if not results and len(query) >= 3:
                results.append(context_dict)

            set_summon_results(results)

        except Exception as e:
            log_action(f"Summon search error: {e}")
            set_summon_results([])
        finally:
            set_summon_loading(False)

    # ========================================================================
    # NODE CLICK BRIDGE
    # ========================================================================

    def on_node_click_bridge_change(payload_json: str) -> None:
        """
        Handler for the node click bridge channel.
        JavaScript writes JSON payload to hidden input, this processes it.
        """
        if not payload_json or not payload_json.strip():
            return

        try:
            payload = json.loads(payload_json)
            process_node_click(payload)
        except json.JSONDecodeError as e:
            log_action(f"Invalid JSON in node click bridge: {e}")
        except Exception as e:
            log_action(f"Node click bridge error: {e}")

    def on_connection_action_bridge_change(payload_json: str) -> None:
        """
        Handler for connection-panel action bridge channel.
        JavaScript writes JSON payload to hidden input, this processes it.
        """
        if not payload_json or not payload_json.strip():
            return

        try:
            payload = json.loads(payload_json)
            process_connection_action(payload)
        except json.JSONDecodeError as e:
            log_action(f"Invalid JSON in connection action bridge: {e}")
        except Exception as e:
            log_action(f"Connection action bridge error: {e}")

    def process_camera_navigation(payload: dict) -> None:
        """Handle camera navigation events from Code City for room/sitting handoff."""
        if not payload:
            return

        to_mode = str(payload.get("to", "")).strip().lower()
        from_mode = str(payload.get("from", "")).strip().lower()
        node = payload.get("node") if isinstance(payload.get("node"), dict) else {}
        node_path = str(node.get("path", "")).strip()

        if node_path:
            set_selected(node_path)
            current = dict(get_code_city_context() or {})
            current.setdefault("path", node_path)
            current.setdefault("status", node.get("status", "working"))
            current["camera_navigation"] = payload
            set_code_city_context(current)

        if to_mode in {"room", "sitting_room"}:
            set_view_mode("sitting_room")
            log_action(f"Camera navigation: {from_mode or 'unknown'} -> {to_mode}")
        elif to_mode == "overview":
            set_view_mode("city")
            log_action("Camera returned to overview")

    def on_camera_nav_bridge_change(payload_json: str) -> None:
        """Handler for camera navigation bridge channel."""
        if not payload_json or not payload_json.strip():
            return

        try:
            payload = json.loads(payload_json)
            process_camera_navigation(payload)
        except json.JSONDecodeError as e:
            log_action(f"Invalid JSON in camera navigation bridge: {e}")
        except Exception as e:
            log_action(f"Camera navigation bridge error: {e}")

    # Create hidden bridge elements
    node_click_bridge = mo.ui.text(
        value=get_node_click_payload(),
        on_change=on_node_click_bridge_change,
    )
    connection_action_bridge = mo.ui.text(
        value=get_connection_action_payload(),
        on_change=on_connection_action_bridge_change,
    )
    camera_nav_bridge = mo.ui.text(
        value=get_camera_nav_payload(),
        on_change=on_camera_nav_bridge_change,
    )
    connection_action_result_bridge = mo.ui.text(
        value=get_connection_action_result_payload()
    )

    # ========================================================================
    # UI BUILDERS
    # ========================================================================

    def build_top_row() -> Any:
        """Build top row: [orchestr8] [collabor8] [JFDI]."""
        top_buttons = mo.hstack(
            [
                mo.ui.button(label="orchestr8", on_click=lambda _: handle_home_click()),
                mo.ui.button(label="collabor8", on_click=lambda _: toggle_collabor8()),
                mo.ui.button(label="JFDI", on_click=lambda _: handle_jfdi()),
            ],
            gap=0.5,
            justify="start",
            align="center",
            wrap=True,
        )
        return top_buttons.style(
            {
                "width": "100%",
                "padding": "0.35rem 0",
                "border-bottom": "1px solid rgba(31, 189, 234, 0.2)",
            }
        )

    def build_code_city() -> Any:
        """
        Build the Woven Maps Code City visualization.
        Shows codebase as abstract cityscape with Gold/Blue/Purple status.

        Health pipeline:
            1. Start HealthWatcher for live file-change detection
            2. Run initial health scan if no results exist yet
            3. Pass health_results to create_code_city() for merge
            4. Track combat_refresh to trigger re-render when combat state changes
        """
        # Track combat_refresh to trigger re-render on combat state changes
        _ = get_combat_refresh()

        root = get_root()
        max_payload_raw = os.getenv("ORCHESTR8_CODE_CITY_MAX_BYTES", "9000000").strip()
        try:
            max_payload_bytes = max(1_000_000, int(max_payload_raw))
        except ValueError:
            max_payload_bytes = 9_000_000

        # Start health watcher on first Code City render
        try:
            health_watcher.start_watching()
        except Exception as e:
            log_action(f"Health watcher start error: {e}")

        if not root:
            return mo.Html("""
            <div class="void-center">
                <div class="void-placeholder">
                    Set a project root to visualize the codebase as a city.
                </div>
            </div>
            """)

        def _payload_size_bytes(city_result: Any) -> int:
            """Measure marimo Html payload size when available."""
            text = getattr(city_result, "text", None)
            if not isinstance(text, str):
                return 0
            return len(text.encode("utf-8"))

        try:
            # Run initial health check if no results exist yet
            health_data = get_health()
            if not health_data:
                try:
                    refresh_health()
                    health_data = get_health()
                except Exception as he:
                    log_action(f"Initial health check error: {he}")
                    health_data = {}

            # Create the Code City visualization with health data merged in.
            # Guard oversized inline payloads before marimo serializes output.
            result = create_code_city(
                root, width=1200, height=680, health_results=health_data or None
            )
            payload_size = _payload_size_bytes(result)
            if payload_size > max_payload_bytes:
                ip_root = Path(root) / "IP"
                if ip_root.is_dir() and str(ip_root) != str(root):
                    log_action(
                        "Code City payload too large at root; retrying with IP/ subroot "
                        f"({payload_size} bytes > {max_payload_bytes} bytes)."
                    )
                    result = create_code_city(
                        str(ip_root),
                        width=1200,
                        height=680,
                        health_results=health_data or None,
                    )
                    payload_size = _payload_size_bytes(result)

                if payload_size > max_payload_bytes:
                    log_action(
                        "Code City payload exceeded guardrail "
                        f"({payload_size} bytes > {max_payload_bytes} bytes)."
                    )
                    return mo.Html(f"""
                    <div class="void-center">
                        <div class="void-placeholder" style="max-width: 760px; line-height: 1.6;">
                            Code City payload exceeded safe render size
                            (<code>{payload_size:,}</code> bytes; limit <code>{max_payload_bytes:,}</code>).
                            <br><br>
                            Set a narrower project root, or increase limits:
                            <br>
                            <code>export ORCHESTR8_CODE_CITY_MAX_BYTES={max_payload_bytes * 2}</code>
                            <br>
                            <code>export MARIMO_OUTPUT_MAX_BYTES={max_payload_bytes * 2}</code>
                        </div>
                    </div>
                    """)
            if health_data:
                log_action(
                    f"Code City rendered with {len(health_data)} health result(s)"
                )
            return result
        except Exception as e:
            log_action(f"Code City error: {str(e)}")
            return mo.Html(f"""
            <div class="void-center">
                <div class="void-placeholder" style="color: {BLUE_DOMINANT};">
                    Error rendering Code City: {str(e)}
                </div>
            </div>
            """)

    def build_summon_results() -> Any:
        """Render search results as emergent cards."""
        return build_summon_results_view(
            mo,
            query=get_summon_query(),
            results=get_summon_results(),
            loading=get_summon_loading(),
            gold_color=GOLD_METALLIC,
            blue_color=BLUE_DOMINANT,
            purple_color=PURPLE_COMBAT,
        )

    def build_void_messages() -> Any:
        """Build the void emergence display."""
        return build_void_messages_view(mo, messages=get_messages())

    def build_app_matrix() -> Any:
        """Render App Matrix launcher view in THE VOID."""
        return build_app_matrix_view(
            mo,
            toggle_calendar=toggle_calendar,
            toggle_comms=toggle_comms,
            toggle_file_explorer=toggle_file_explorer,
            handle_jfdi=handle_jfdi,
            set_view_mode=set_view_mode,
            gold_color=GOLD_METALLIC,
        )

    def return_from_sitting_room() -> None:
        """Return from Sitting Room to Code City overview."""
        set_view_mode("city")
        log_action("Returned from Sitting Room to Code City")

    def build_sitting_room() -> Any:
        """Render a room-level inspection handoff surface."""
        context = get_code_city_context() or {}
        panel = context.get("building_panel") if isinstance(context, dict) else {}
        room = context.get("room_entry") if isinstance(context, dict) else {}

        if not isinstance(panel, dict) or not panel:
            return mo.Html("""
            <div class="void-center">
                <div class="void-placeholder">
                    Sitting Room has no active context. Select a broken room to enter.
                </div>
            </div>
            """)

        room_name = room.get("name", "N/A") if isinstance(room, dict) else "N/A"
        room_type = room.get("room_type", "room") if isinstance(room, dict) else "room"
        trigger = room.get("trigger", "manual") if isinstance(room, dict) else "manual"
        room_errors = room.get("errors", []) if isinstance(room, dict) else []
        error_items = (
            "".join(f"<li>{str(err)}</li>" for err in room_errors[:5])
            or "<li>No room-level errors mapped.</li>"
        )
        status = panel.get("status", "working")
        status_color = (
            PURPLE_COMBAT
            if status == "combat"
            else BLUE_DOMINANT
            if status == "broken"
            else GOLD_METALLIC
        )

        details = mo.Html(
            f"""
            <div class="void-center">
                <div class="panel-overlay" style="max-width:760px;">
                    <div class="panel-header">
                        <span class="panel-title">SITTING ROOM</span>
                    </div>
                    <div style="color:var(--text-secondary);font-size:11px;line-height:1.55;">
                        <div><strong>File:</strong> {panel.get("path", "unknown")}</div>
                        <div><strong>Status:</strong> <span style="color:{status_color};">{status}</span></div>
                        <div><strong>Room:</strong> {room_name} ({room_type})</div>
                        <div><strong>Trigger:</strong> {trigger}</div>
                        <div style="margin-top:10px;"><strong>Room Errors</strong></div>
                        <ul style="margin:6px 0 0 16px;padding:0;color:var(--text-secondary);">{error_items}</ul>
                    </div>
                </div>
            </div>
            """
        )
        return mo.vstack(
            [
                details,
                mo.ui.button(
                    label="Return to Code City",
                    on_click=lambda _: return_from_sitting_room(),
                ),
            ],
            gap=0.4,
        )

    def build_void_content() -> Any:
        """
        Build the main void content based on current view mode.
        - city: Code City
        - matrix: App Matrix launcher
        - chat: conversation emergence
        - sitting_room: room-level handoff context
        """
        mode = get_view_mode()
        mode_label = {
            "city": "CODE CITY",
            "matrix": "APP MATRIX",
            "chat": "CHAT",
            "sitting_room": "SITTING ROOM",
        }.get(mode, "CODE CITY")
        mode_color = {
            "city": GOLD_METALLIC,
            "matrix": PURPLE_COMBAT,
            "chat": BLUE_DOMINANT,
            "sitting_room": PURPLE_COMBAT,
        }.get(mode, GOLD_METALLIC)
        mode_indicator = mo.Html(f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:8px 0;
            margin-bottom:8px;
            border-bottom:1px solid rgba(31, 189, 234, 0.1);
        ">
            <span style="
                font-family:monospace;
                font-size:10px;
                letter-spacing:0.1em;
                color:{mode_color};
            ">{mode_label}</span>
        </div>
        """)

        if mode == "matrix":
            content = build_app_matrix()
        elif mode == "chat":
            content = build_void_messages()
        elif mode == "sitting_room":
            content = build_sitting_room()
        else:
            content = build_code_city()

        return mo.vstack([mode_indicator, content])

    def build_panels() -> Any:
        """Build conditional overlay panels."""
        return build_panels_view(
            mo,
            get_show_agents=get_show_agents,
            get_agent_group=get_agent_group,
            settlement_agent_groups=settlement_agent_groups,
            get_agent_id=get_agent_id,
            set_collabor8_group=set_collabor8_group,
            set_agent_id=set_agent_id,
            deploy_selected_agent=deploy_selected_agent,
            get_show_settings=get_show_settings,
            gold_color=GOLD_METALLIC,
            available_models=available_models,
            get_selected_model=get_selected_model,
            set_selected_model=set_selected_model,
            get_show_summon=get_show_summon,
            get_summon_query=get_summon_query,
            set_summon_query=set_summon_query,
            trigger_carl_search=trigger_carl_search,
            build_summon_results=build_summon_results,
            get_selected=get_selected,
            get_code_city_context=get_code_city_context,
            carl=carl,
            bg_primary=BG_PRIMARY,
            blue_color=BLUE_DOMINANT,
        )

    def build_attachment_bar() -> Any:
        """Build attachment chips if files are attached."""
        return build_attachment_bar_view(
            mo,
            attached_files=get_attached_files(),
            gold_color=GOLD_METALLIC,
        )

    def build_control_surface() -> Any:
        """Build the bottom control surface with 5-1-6 button rhythm."""
        return build_control_surface_view(
            mo,
            user_input=get_user_input(),
            set_user_input=set_user_input,
            flagship_agent=flagship_agent,
            cycle_maestro_state=cycle_maestro_state,
            get_maestro_state=get_maestro_state,
            handle_apps=handle_apps,
            toggle_calendar=toggle_calendar,
            toggle_comms=toggle_comms,
            toggle_file_explorer=toggle_file_explorer,
            handle_summon=handle_summon,
            toggle_recording=toggle_recording,
            handle_playback=handle_playback,
            has_audio_recording=has_audio_recording,
            handle_terminal=handle_terminal,
            handle_send=handle_send,
            handle_attach=handle_attach,
        )

    # ========================================================================
    # MAIN LAYOUT
    # ========================================================================

    # Inject CSS (loaded dynamically from IP/styles/orchestr8.css)
    css_injection = mo.Html(load_orchestr8_css())

    # Build components
    top_row = build_top_row()
    panels = build_panels()
    void_content = build_void_content()  # Code City or Chat based on mode
    attachment_bar = build_attachment_bar()
    control_surface = build_control_surface()

    # Ticket panel (slides from right when visible)
    ticket_panel_content = ticket_panel.render() if get_show_tickets() else mo.md("")

    # Calendar panel (slides from right when visible)
    calendar_panel_content = (
        calendar_panel.render() if get_show_calendar() else mo.md("")
    )

    # Comms panel (slides from right when visible)
    comms_panel_content = comms_panel.render() if get_show_comms() else mo.md("")

    # File Explorer panel (slides from right when visible)
    file_explorer_content = (
        file_explorer_panel.render() if get_show_file_explorer() else mo.md("")
    )

    # Deploy panel (House a Digital Native?) - modal overlay
    deploy_panel_content = deploy_panel.render() if get_show_deploy() else mo.md("")

    # Intent panel (C2P Intent Queue - slides from right when visible)
    intent_panel_content = intent_panel.render() if get_show_intents() else mo.md("")

    # Status bar
    root = get_root()
    selected = get_selected()
    status_bar = mo.md(f"**Root:** `{root}` | **Selected:** `{selected or 'None'}`")

    app_shell = mo.vstack(
        [top_row, panels, void_content, attachment_bar, control_surface], gap=0.6
    ).style(
        {
            "width": "100%",
            "max-width": "1440px",
            "margin": "0 auto",
            "padding": "0.5rem 0.5rem 1.5rem",
        }
    )

    # JavaScript to listen for Code City events and bridge to Python
    # The Code City iframe sends postMessage for node clicks and edge actions.
    bridge_runtime_js = build_marimo_bridge_runtime_js()
    node_click_js = mo.Html(f"""
    <script>
    {bridge_runtime_js}
    (function() {{
        const resultBridgeId = '{connection_action_result_bridge._id}';
        const cameraBridgeId = '{camera_nav_bridge._id}';
        let lastResultRaw = null;
        const bridgeRuntime = window.__orchestr8Bridge;
        if (!bridgeRuntime) {{
            console.error("Bridge runtime unavailable");
            return;
        }}

        function broadcastToCodeCityIframes(message) {{
            const frames = document.querySelectorAll('iframe');
            frames.forEach((frame) => {{
                if (!frame || !frame.contentWindow) return;
                try {{
                    frame.contentWindow.postMessage(message, '*');
                }} catch (err) {{
                    console.debug('Unable to post to iframe:', err);
                }}
            }});
        }}

        function relayConnectionResult() {{
            const resultInput = bridgeRuntime.resolveBridgeInput(resultBridgeId);
            if (!resultInput) return;

            const raw = resultInput.value || '';
            if (!raw || raw === lastResultRaw) return;
            lastResultRaw = raw;

            try {{
                const payload = JSON.parse(raw);
                broadcastToCodeCityIframes({{
                    type: 'WOVEN_MAPS_CONNECTION_RESULT',
                    payload
                }});
            }} catch (err) {{
                console.warn('Invalid connection result payload:', err);
            }}
        }}

        const intervalKey = '__orchestr8_connection_result_interval__';
        if (window[intervalKey]) {{
            clearInterval(window[intervalKey]);
        }}
        window[intervalKey] = setInterval(relayConnectionResult, 300);

        // Listen for messages from Code City iframe
        window.addEventListener('message', function(event) {{
            if (event.data && event.data.type === 'WOVEN_MAPS_NODE_CLICK') {{
                console.log('Node clicked:', event.data.node);
                const bridgeId = '{node_click_bridge._id}';
                bridgeRuntime.writePayloadToBridge(bridgeId, event.data.node, 'Node click');
                return;
            }}

            if (event.data && event.data.type === 'WOVEN_MAPS_CONNECTION_ACTION') {{
                console.log('Connection action:', event.data.payload);
                const bridgeId = '{connection_action_bridge._id}';
                bridgeRuntime.writePayloadToBridge(bridgeId, event.data.payload, 'Connection action');
                return;
            }}

            if (event.data && event.data.type === 'WOVEN_MAPS_CAMERA_NAVIGATE') {{
                bridgeRuntime.writePayloadToBridge(cameraBridgeId, event.data, 'Camera navigation');
                return;
            }}

            if (event.data && event.data.type === 'WOVEN_MAPS_CAMERA_RETURN') {{
                bridgeRuntime.writePayloadToBridge(cameraBridgeId, event.data, 'Camera return');
            }}
        }});
    }})();
    </script>
    """)

    # JavaScript phreak sound effect (plays on Phreak> trigger tick updates)
    phreak_sfx_js = mo.Html(
        f"""
    <script>
    (function() {{
        const tick = {get_phreak_sfx_tick()};
        const key = "__orchestr8_phreak_tick__";
        const stateKey = "__orchestr8_phreak_audio_state__";
        const prev = window[key];
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        const state = window[stateKey] || (window[stateKey] = {{
            ctx: null,
            pending: false,
            unlockBound: false,
            unlockHandler: null,
        }});

        function playPhreakBeep() {{
            if (!state.ctx || state.ctx.state !== "running") return false;
            try {{
                const osc = state.ctx.createOscillator();
                const gain = state.ctx.createGain();
                osc.type = "triangle";
                osc.frequency.setValueAtTime(520, state.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(880, state.ctx.currentTime + 0.08);
                gain.gain.setValueAtTime(0.0001, state.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.08, state.ctx.currentTime + 0.01);
                gain.gain.exponentialRampToValueAtTime(0.0001, state.ctx.currentTime + 0.18);
                osc.connect(gain);
                gain.connect(state.ctx.destination);
                osc.start();
                osc.stop(state.ctx.currentTime + 0.2);
                return true;
            }} catch (error) {{
                console.debug("Phreak SFX unavailable:", error);
                return false;
            }}
        }}

        async function ensurePhreakAudioContext() {{
            if (!AudioCtx) return false;
            if (!state.ctx) state.ctx = new AudioCtx();
            if (state.ctx.state === "suspended") {{
                try {{
                    await state.ctx.resume();
                }} catch (resumeError) {{
                    console.debug("Phreak SFX resume blocked:", resumeError);
                }}
            }}
            return state.ctx.state === "running";
        }}

        function bindUnlockHandler() {{
            if (state.unlockBound) return;
            state.unlockBound = true;
            state.unlockHandler = async () => {{
                const running = await ensurePhreakAudioContext();
                if (running && state.pending) {{
                    state.pending = false;
                    playPhreakBeep();
                }}
                if (running && state.unlockHandler) {{
                    document.removeEventListener("pointerdown", state.unlockHandler);
                    document.removeEventListener("keydown", state.unlockHandler);
                    document.removeEventListener("touchstart", state.unlockHandler);
                    state.unlockBound = false;
                    state.unlockHandler = null;
                }}
            }};
            document.addEventListener("pointerdown", state.unlockHandler, {{ passive: true }});
            document.addEventListener("keydown", state.unlockHandler);
            document.addEventListener("touchstart", state.unlockHandler, {{ passive: true }});
        }}

        if (typeof prev === "number" && tick > prev) {{
            ensurePhreakAudioContext().then((running) => {{
                if (running) {{
                    playPhreakBeep();
                    return;
                }}
                state.pending = true;
                bindUnlockHandler();
            }});
        }}
        window[key] = tick;
    }})();
    </script>
    """
    )

    # Wrap bridge elements with visibility:hidden to keep them in DOM but invisible
    hidden_bridge = mo.Html(f"""
    <div style="display:none;">
        {node_click_bridge}
        {connection_action_bridge}
        {camera_nav_bridge}
        {connection_action_result_bridge}
    </div>
    """)

    return mo.vstack(
        [
            css_injection,
            node_click_js,
            phreak_sfx_js,
            hidden_bridge,  # Hidden bridge element for JS->Python communication
            app_shell,  # Canonical app surface
            status_bar,
            # Right-side sliding panels (mutually exclusive)
            ticket_panel_content,
            calendar_panel_content,
            comms_panel_content,
            file_explorer_content,
            # Deploy panel (modal overlay on top)
            deploy_panel_content,
            # Intent panel (C2P Intent Queue - slides from right)
            intent_panel_content,
        ]
    )
