"""
06_maestro Plugin - The Void
Orchestr8 v3.0 - Central Command Interface

The heart of Orchestr8 - a unified command center inspired by MaestroView.
Implements the spatial UI pattern with:
- Top navigation bar (orchestr8 | Collabor8 | JFDI | Gener8)
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
--bg-primary: #0A0A0B (The Void)
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


def get_model_config() -> dict:
    """Get model configuration from orchestr8_settings.toml."""
    try:
        import toml

        settings_file = Path("orchestr8_settings.toml")
        if settings_file.exists():
            settings = toml.load(settings_file)
            # Get director agent config (maestro uses this for chat)
            director = settings.get("agents", {}).get("director", {})
            doctor = settings.get("agents", {}).get("doctor", {})
            return {
                "model": doctor.get("model", "claude-sonnet-4-20250514"),
                "max_tokens": doctor.get("max_tokens", 8192),
            }
    except Exception:
        pass

    # Fallback defaults
    return {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 8192,
    }


PLUGIN_NAME = "The Void"
PLUGIN_ORDER = 6

# ============================================================================
# COLOR CONSTANTS - EXACT, NO EXCEPTIONS
# ============================================================================
BLUE_DOMINANT = "#1fbdea"
GOLD_METALLIC = "#D4AF37"
GOLD_DARK = "#B8860B"
GOLD_SAFFRON = "#F4C430"
BG_PRIMARY = "#0A0A0B"
BG_ELEVATED = "#121214"
PURPLE_COMBAT = "#9D4EDD"  # Combat state - General deployed and active

# ============================================================================
# CSS STYLES - Injected for void aesthetics
# ============================================================================
MAESTRO_CSS = f"""
<style>
/* =========================================================
   EMERGENCE ANIMATIONS - Things EMERGE, they don't breathe
   ========================================================= */

@keyframes emergence {{
    0% {{
        opacity: 0;
        transform: translateY(12px);
    }}
    100% {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes emergence-fade {{
    0% {{ opacity: 0; }}
    100% {{ opacity: 1; }}
}}

@keyframes emergence-scale {{
    0% {{
        opacity: 0;
        transform: scale(0.95);
    }}
    100% {{
        opacity: 1;
        transform: scale(1);
    }}
}}

/* Apply emergence to key elements with staggered delays */
.maestro-container {{
    min-height: 70vh;
    display: flex;
    flex-direction: column;
    animation: emergence-fade 0.3s ease-out forwards;
}}

.maestro-top-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid rgba(31, 189, 234, 0.2);
    animation: emergence 0.4s ease-out 0.1s both;
}}

.orchestr8-brand {{
    font-family: monospace;
    font-size: 14px;
    letter-spacing: 0.08em;
}}

.orchestr8-prefix {{
    color: {BLUE_DOMINANT};
}}

.orchestr8-suffix {{
    color: {GOLD_METALLIC};
}}

.void-center {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 40px 20px;
    min-height: 300px;
    animation: emergence-scale 0.5s ease-out 0.2s both;
}}

.emerged-message {{
    padding: 16px 20px;
    background: rgba(18, 18, 20, 0.9);
    border: 1px solid rgba(184, 134, 11, 0.3);
    border-radius: 8px;
    margin-bottom: 16px;
    max-width: 700px;
    width: 100%;
    animation: emergence 0.4s ease-out both;
}}

.emerged-message:nth-child(1) {{ animation-delay: 0.1s; }}
.emerged-message:nth-child(2) {{ animation-delay: 0.2s; }}
.emerged-message:nth-child(3) {{ animation-delay: 0.3s; }}

.emerged-message .content {{
    color: #e8e8e8;
    font-size: 14px;
    line-height: 1.6;
    white-space: pre-wrap;
}}

.emerged-message .meta {{
    text-align: right;
    margin-top: 8px;
    font-family: monospace;
    font-size: 10px;
    color: {GOLD_DARK};
}}

.control-surface {{
    border-top: 1px solid rgba(31, 189, 234, 0.2);
    padding: 12px 0;
    animation: emergence 0.4s ease-out 0.3s both;
}}

.maestro-btn {{
    padding: 6px 12px;
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.3);
    border-radius: 4px;
    color: {BLUE_DOMINANT};
    font-family: monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    cursor: pointer;
    transition: all 150ms ease-out;
}}

.maestro-btn:hover {{
    color: {GOLD_METALLIC};
    border-color: {GOLD_METALLIC};
    background: rgba(212, 175, 55, 0.1);
}}

.maestro-btn.active {{
    color: {GOLD_METALLIC};
    border-color: {GOLD_METALLIC};
}}

.maestro-center-btn {{
    padding: 10px 32px;
    background: none;
    border: 1px solid rgba(184, 134, 11, 0.3);
    border-radius: 4px;
    color: {GOLD_DARK};
    font-family: monospace;
    font-size: 14px;
    letter-spacing: 0.1em;
    cursor: pointer;
}}

.maestro-center-btn:hover {{
    color: {GOLD_SAFFRON};
    border-color: rgba(244, 196, 48, 0.4);
    background: rgba(184, 134, 11, 0.1);
}}

.panel-overlay {{
    background: rgba(18, 18, 20, 0.95);
    border: 1px solid rgba(31, 189, 234, 0.3);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
    animation: emergence-scale 0.35s ease-out both;
}}

.panel-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(31, 189, 234, 0.2);
}}

.panel-title {{
    color: {GOLD_METALLIC};
    font-family: monospace;
    font-size: 12px;
    letter-spacing: 0.1em;
}}

.void-placeholder {{
    color: rgba(255, 255, 255, 0.3);
    font-style: italic;
    text-align: center;
    animation: emergence-fade 0.8s ease-out 0.4s both;
}}

/* Button emergence with subtle scale */
.maestro-btn, .maestro-center-btn {{
    animation: emergence 0.3s ease-out both;
}}
</style>
"""


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
    get_health, set_health = STATE_MANAGERS.get("health", mo.state({}))

    # Get available models from settings
    def get_available_models() -> list:
        """Load available models from orchestr8_settings.toml."""
        try:
            import toml

            settings_file = Path("orchestr8_settings.toml")
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
    get_show_tasks, set_show_tasks = mo.state(False)
    get_show_terminal, set_show_terminal = mo.state(False)
    get_show_summon, set_show_summon = mo.state(False)

    # Local state - Conversation
    get_messages, set_messages = mo.state([])
    get_user_input, set_user_input = mo.state("")

    # Local state - Attachments
    get_attached_files, set_attached_files = mo.state([])

    # Local state - View mode (city vs chat)
    get_view_mode, set_view_mode = mo.state("city")  # "city" | "chat"

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

    carl = CarlContextualizer(str(project_root_path))

    def on_health_change(results: dict) -> None:
        """Callback when health check completes - updates health state."""
        set_health(results)
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

    # ========================================================================
    # EVENT HANDLERS (Transliterated from MaestroView.vue)
    # ========================================================================

    def log_action(action: str) -> None:
        """Log action to system logs."""
        logs = get_logs()
        timestamp = datetime.now().strftime("%H:%M:%S")
        set_logs(logs + [f"[{timestamp}] [Maestro] {action}"])

    def toggle_tickets() -> None:
        """Toggle ticket panel (slides from right)."""
        current = get_show_tickets()
        set_show_tickets(not current)
        ticket_panel.set_visible(not current)

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

    def handle_node_click(node_data: dict) -> None:
        """
        Handle click on Code City building node.
        If broken (blue), show the deploy panel to "House a Digital Native?"
        """
        if not node_data:
            return

        status = node_data.get("status", "working")
        file_path = node_data.get("path", "")

        log_action(f"Building clicked: {file_path} ({status})")

        if status == "broken":
            # Show deploy panel for broken buildings
            set_clicked_node(node_data)
            deploy_panel.show(
                file_path=file_path,
                status=status,
                errors=node_data.get("errors", []),
            )
            set_show_deploy(True)
            log_action(f"Deploy panel opened for {file_path}")
        elif status == "combat":
            # Already in combat - show status
            log_action(f"{file_path} is already in COMBAT - general deployed")
        else:
            # Working file - just select it
            set_selected(file_path)
            log_action(f"Selected: {file_path}")

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
        """Toggle agents panel - mutual exclusion with tasks."""
        current = get_show_agents()
        set_show_agents(not current)
        if not current:  # Opening agents
            set_show_tasks(False)
            log_action("Collabor8 panel opened")
        else:
            log_action("Collabor8 panel closed")

    def toggle_jfdi() -> None:
        """Toggle tasks panel - mutual exclusion with agents."""
        current = get_show_tasks()
        set_show_tasks(not current)
        if not current:  # Opening tasks
            set_show_agents(False)
            log_action("JFDI panel opened")
        else:
            log_action("JFDI panel closed")

    def handle_terminal() -> None:
        """Toggle terminal panel and spawn actu8 if opening."""
        current = get_show_terminal()
        set_show_terminal(not current)

        if not current:  # Opening terminal
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
        set_show_tasks(False)
        set_show_terminal(False)
        set_show_summon(False)
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
        """Open Linux app store (gnome-software)."""
        try:
            import subprocess

            # Try gnome-software first (Ubuntu/Fedora), fall back to others
            for app_store in [
                "gnome-software",
                "snap-store",
                "discover",
                "pamac-manager",
            ]:
                try:
                    subprocess.Popen([app_store])
                    log_action(f"Opened {app_store}")
                    return
                except FileNotFoundError:
                    continue
            log_action("No app store found - install gnome-software")
        except Exception as e:
            log_action(f"Failed to open app store: {e}")

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
            set_show_tasks(False)
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

        messages = get_messages()

        # Add user message
        user_msg = {
            "id": str(uuid.uuid4()),
            "role": "user",
            "content": text,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        }
        messages.append(user_msg)

        # LLM API Integration
        if not HAS_ANTHROPIC:
            # Anthropic not installed - graceful fallback
            assistant_msg = {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": "[INFO] Chat requires the anthropic SDK.\n\nInstall with: `pip install anthropic`\n\nCode City visualization still works!",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
            }
            messages.append(assistant_msg)
            set_messages(messages)
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

            # Create assistant message
            assistant_msg = {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": response_content,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
            }
            messages.append(assistant_msg)

        except Exception as e:
            error_name = type(e).__name__
            if "AuthenticationError" in error_name:
                log_action(f"LLM Authentication Error: {str(e)}")
                assistant_msg = {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": f"[WARNING] Authentication Error: Invalid ANTHROPIC_API_KEY\n\nPlease check your API key in environment variables.",
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                }
                messages.append(assistant_msg)
            elif "APIError" in error_name:
                log_action(f"LLM API Error: {str(e)}")
                assistant_msg = {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": f"[WARNING] LLM API Error: {str(e)}\n\nPlease check your ANTHROPIC_API_KEY environment variable and network connection.",
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                }
                messages.append(assistant_msg)
            else:
                log_action(f"Unexpected Error: {str(e)}")
                assistant_msg = {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": f"[WARNING] Unexpected Error: {str(e)}",
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                }
                messages.append(assistant_msg)

        set_messages(messages)
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

    def trigger_carl_search(query: str) -> None:
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
            context = carl.gather_context("IP")

            results = []
            context_dict = {
                "fiefdom": context.fiefdom,
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

            if query_lower in context.fiefdom.lower():
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
    # UI BUILDERS
    # ========================================================================

    def build_top_row() -> Any:
        """Build the top navigation row."""
        # Brand
        brand = mo.Html(f"""
        <div class="orchestr8-brand">
            <span class="orchestr8-prefix">orchestr</span><span class="orchestr8-suffix">8</span>
        </div>
        """)

        # Model picker dropdown
        model_picker = mo.ui.dropdown(
            options=available_models,
            value=get_selected_model(),
            label="General",
            on_change=set_selected_model,
        )

        # Navigation buttons
        nav_buttons = mo.hstack(
            [
                mo.ui.button(label="Collabor8", on_change=lambda _: toggle_collabor8()),
                mo.ui.button(label="JFDI", on_change=lambda _: toggle_jfdi()),
                mo.ui.button(
                    label="Gener8",
                    on_change=lambda _: log_action("Switch to Generator tab"),
                ),
            ],
            gap="0.5rem",
        )

        # Ticket panel toggle (slides from right)
        ticket_btn = mo.ui.button(
            label="Tickets",
            on_change=lambda _: toggle_tickets(),
        )

        return mo.hstack(
            [
                mo.ui.button(label="Home", on_change=lambda _: handle_home_click()),
                brand,
                model_picker,
                nav_buttons,
                ticket_btn,
            ],
            justify="space-between",
            align="center",
        )

    def build_code_city() -> Any:
        """
        Build the Woven Maps Code City visualization.
        Shows codebase as abstract cityscape with Gold/Blue/Purple status.
        """
        root = get_root()

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

        try:
            # Create the Code City visualization
            result = create_code_city(root, width=850, height=500)
            # Log health check status
            health_data = get_health()
            if health_data:
                log_action(f"Health data: {len(health_data)} results")
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
        """
        Render search results as emergent cards.
        Things EMERGE from the void - no breathing animations.
        """
        query = get_summon_query()
        results = get_summon_results()
        loading = get_summon_loading()

        if not query or len(query) < 2:
            return mo.Html("""
            <div class="void-placeholder">
                Type at least 2 characters to search the codebase...
            </div>
            """)

        if loading:
            return mo.Html("""
            <div class="void-placeholder" style="color: #D4AF37;">
                Scanning the Void...
            </div>
            """)

        if not results:
            return mo.Html(f"""
            <div class="void-placeholder">
                No results found for "{query}"
            </div>
            """)

        cards_html = ""
        for result in results[:10]:
            fiefdom = result.get("fiefdom", "Unknown")
            health = result.get("health", {})
            status = health.get("status", "working")

            status_color = "#D4AF37" if status == "working" else "#1fbdea"

            error_count = len(health.get("errors", []))
            warning_count = len(health.get("warnings", []))

            cards_html += f"""
            <div class="emerged-message" style="border-left: 3px solid {status_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: {status_color}; font-family: monospace; font-weight: 600;">
                        {fiefdom}
                    </span>
                    <span style="color: #666; font-size: 10px;">
                        {status.upper()}
                    </span>
                </div>
                <div style="margin-top: 8px; font-size: 12px; color: #888;">
                    {error_count} errors, {warning_count} warnings
                </div>
            </div>
            """

        return mo.Html(f"""
        <div style="width: 100%; max-width: 700px;">
            {cards_html}
        </div>
        """)

    def build_void_messages() -> Any:
        """
        Build the void emergence display.
        Only shows last 3 assistant messages - the emergence pattern.
        """
        messages = get_messages()
        assistant_msgs = [m for m in messages if m["role"] == "assistant"][-3:]

        if not assistant_msgs:
            return mo.Html("""
            <div class="void-center">
                <div class="void-placeholder">
                    The void awaits your command...
                </div>
            </div>
            """)

        message_html = ""
        for msg in assistant_msgs:
            message_html += f"""
            <div class="emerged-message">
                <div class="content">{msg["content"]}</div>
                <div class="meta">{msg["timestamp"]}</div>
            </div>
            """

        return mo.Html(f"""
        <div class="void-center">
            <div style="width: 100%; max-width: 700px;">
                {message_html}
            </div>
        </div>
        """)

    def build_void_content() -> Any:
        """
        Build the main void content based on current view mode.
        - City mode: Shows Woven Maps Code City visualization
        - Chat mode: Shows conversation messages
        """
        mode = get_view_mode()

        # View mode toggle
        toggle_label = "View Chat" if mode == "city" else "View City"
        toggle_btn = mo.ui.button(
            label=toggle_label,
            on_change=lambda _: set_view_mode("chat" if mode == "city" else "city"),
        )

        # Mode indicator
        mode_indicator = mo.Html(f"""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            margin-bottom: 8px;
            border-bottom: 1px solid rgba(31, 189, 234, 0.1);
        ">
            <span style="
                font-family: monospace;
                font-size: 10px;
                letter-spacing: 0.1em;
                color: {"#D4AF37" if mode == "city" else "#1fbdea"};
            ">
                {"CODE CITY" if mode == "city" else "CHAT"}
            </span>
        </div>
        """)

        # Content based on mode
        if mode == "city":
            content = build_code_city()
        else:
            content = build_void_messages()

        return mo.vstack(
            [
                mo.hstack(
                    [mode_indicator, toggle_btn],
                    justify="space-between",
                    align="center",
                ),
                content,
            ]
        )

    def build_panels() -> Any:
        """Build conditional overlay panels."""
        panels = []

        # Collabor8 (Agents) Panel
        if get_show_agents():
            agents_panel = mo.Html(f"""
            <div class="panel-overlay">
                <div class="panel-header">
                    <span class="panel-title">COLLABOR8 - Domain Agents</span>
                </div>
                <div style="color: #999; font-size: 12px;">
                    Agent management interface coming soon.
                    <br><br>
                    This panel will display available domain agents:
                    <ul style="margin-top: 8px; color: #666;">
                        <li>Scout - Codebase exploration</li>
                        <li>Builder - Code generation</li>
                        <li>Reviewer - Code review</li>
                        <li>Documenter - Documentation</li>
                    </ul>
                </div>
            </div>
            """)
            panels.append(agents_panel)

        # JFDI (Tasks) Panel
        if get_show_tasks():
            tasks_panel = mo.Html(f"""
            <div class="panel-overlay">
                <div class="panel-header">
                    <span class="panel-title">JFDI - Task Management</span>
                </div>
                <div style="color: #999; font-size: 12px;">
                    Task management interface coming soon.
                    <br><br>
                    This panel will display:
                    <ul style="margin-top: 8px; color: #666;">
                        <li>Active tasks</li>
                        <li>Task queue</li>
                        <li>Completed tasks</li>
                        <li>Task focus overlay</li>
                    </ul>
                </div>
            </div>
            """)
            panels.append(tasks_panel)

        # Summon (Search) Panel - with Carl integration + Search
        if get_show_summon():

            def _on_summon_change(q: str) -> None:
                set_summon_query(q)
                trigger_carl_search(q)

            summon_input = mo.ui.text(
                value=get_summon_query(),
                placeholder="Search codebase, tasks, agents...",
                on_change=_on_summon_change,
                full_width=True,
            )

            results_display = build_summon_results()

            selected_fiefdom = get_selected() or "IP"
            try:
                context_json = carl.gather_context_json(selected_fiefdom)
                context_footer = f"""<details style="margin-top: 16px;">
                    <summary style="color: #666; font-size: 11px; cursor: pointer;">
                        View Raw Context JSON
                    </summary>
                    <pre style='color:#888;font-size:9px;white-space:pre-wrap;max-height:200px;overflow:auto;background:#0A0A0B;padding:8px;border-radius:4px;margin-top:8px;'>{context_json}</pre>
                </details>"""
            except Exception as e:
                context_footer = f"<span style='color:#1fbdea;font-size:10px;'>Context error: {e}</span>"

            summon_panel = mo.Html(f"""
            <div class="panel-overlay" style="animation: emergence-scale 0.4s ease-out both;">
                <div class="panel-header">
                    <span class="panel-title">SUMMON - Neighborhood Search</span>
                </div>
                <div style="margin-bottom: 12px;">
                    <span style="color:#666;font-size:11px;">Selected: </span>
                    <span style="color:#D4AF37;font-family:monospace;">{selected_fiefdom}</span>
                </div>
            </div>
            """)
            panels.append(summon_panel)
            panels.append(summon_input)
            panels.append(results_display)
            panels.append(mo.Html(context_footer))

        if panels:
            return mo.vstack(panels)
        return mo.md("")

    def build_attachment_bar() -> Any:
        """Build attachment chips if files are attached."""
        attached = get_attached_files()
        if not attached:
            return mo.md("")

        chips_html = ""
        for f in attached:
            filename = f.split("/")[-1] if "/" in f else f
            chips_html += f"""
            <span style="
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 4px 8px;
                background: rgba(212, 175, 55, 0.1);
                border: 1px solid rgba(212, 175, 55, 0.3);
                border-radius: 4px;
                font-family: monospace;
                font-size: 10px;
                color: {GOLD_METALLIC};
                margin-right: 8px;
            ">
                {filename}
            </span>
            """

        return mo.Html(f"""
        <div style="
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 8px 0;
            margin-bottom: 8px;
        ">
            {chips_html}
        </div>
        """)

    def build_control_surface() -> Any:
        """Build the bottom control surface - the Overton anchor."""
        # Chat input
        chat_input = mo.ui.text_area(
            value=get_user_input(),
            placeholder="What would you like to accomplish?",
            on_change=set_user_input,
            full_width=True,
        )

        # Left group - Apps | Matrix | Calendar | Comms | Files
        left_buttons = mo.hstack(
            [
                mo.ui.button(
                    label="Apps",
                    on_change=lambda _: handle_apps(),  # Opens Linux app store
                ),
                mo.ui.button(
                    label="Matrix",
                    on_change=lambda _: handle_matrix(),  # Code editor + LLMs + Contacts
                ),
                mo.ui.button(
                    label="Calendar",
                    on_change=lambda _: toggle_calendar(),  # Calendar panel
                ),
                mo.ui.button(
                    label="Comms",
                    on_change=lambda _: toggle_comms(),  # P2P Comms panel
                ),
                mo.ui.button(
                    label="Files",
                    on_change=lambda _: toggle_file_explorer(),  # Inline file explorer
                ),
            ],
            gap="0.25rem",
        )

        # Center - maestro (summon)
        center_btn = mo.ui.button(label="maestro", on_change=lambda _: handle_summon())

        # Right group - Search | Record | Playback | Phreak> | Send | Attach | Settings
        right_buttons = mo.hstack(
            [
                mo.ui.button(label="Search", on_change=lambda _: handle_summon()),
                mo.ui.button(
                    label="Record",
                    on_change=lambda _: toggle_recording(),
                ),
                mo.ui.button(
                    label="Playback",
                    on_change=lambda _: handle_playback(),
                    disabled=not has_audio_recording(),
                ),
                mo.ui.button(
                    label="Phreak>",  # Opens terminal
                    on_change=lambda _: handle_terminal(),
                ),
                mo.ui.button(label="Send", on_change=lambda _: handle_send()),
                mo.ui.button(label="Attach", on_change=lambda _: handle_attach()),
                mo.ui.button(
                    label="~~~",  # Wave icon for Settings
                    on_change=lambda _: log_action("Open Settings tab"),
                ),
            ],
            gap="0.25rem",
        )

        return mo.vstack(
            [
                chat_input,
                mo.hstack(
                    [left_buttons, center_btn, right_buttons],
                    justify="space-between",
                    align="center",
                ),
            ]
        )

    # ========================================================================
    # MAIN LAYOUT
    # ========================================================================

    # Inject CSS
    css_injection = mo.Html(MAESTRO_CSS)

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

    # Status bar
    root = get_root()
    selected = get_selected()
    status_bar = mo.md(f"**Root:** `{root}` | **Selected:** `{selected or 'None'}`")

    # JavaScript to listen for Code City node clicks
    # The Code City iframe sends postMessage when a building is clicked
    node_click_js = mo.Html("""
    <script>
    (function() {
        // Listen for messages from Code City iframe
        window.addEventListener('message', function(event) {
            if (event.data && event.data.type === 'WOVEN_MAPS_NODE_CLICK') {
                console.log('Node clicked:', event.data.node);
                // Store in a global for Marimo to pick up
                window.__clicked_node__ = event.data.node;
                // Dispatch custom event for Marimo reactivity
                window.dispatchEvent(new CustomEvent('node-clicked', {
                    detail: event.data.node
                }));
            }
        });
    })();
    </script>
    """)

    return mo.vstack(
        [
            css_injection,
            node_click_js,
            mo.md("## The Void"),
            mo.md("*maestro overlooks the abyss*"),
            mo.md("---"),
            top_row,
            mo.md("---"),
            panels,
            void_content,  # Code City or Chat based on view mode
            mo.md("---"),
            attachment_bar,
            control_surface,
            mo.md("---"),
            status_bar,
            # Right-side sliding panels (mutually exclusive)
            ticket_panel_content,
            calendar_panel_content,
            comms_panel_content,
            file_explorer_content,
            # Deploy panel (modal overlay on top)
            deploy_panel_content,
        ]
    )
