"""
06_maestro Plugin - The Void
Orchestr8 v3.0 - Central Command Interface

The heart of Orchestr8 - a unified command center inspired by stereOS MaestroView.
Implements the spatial UI pattern with:
- Top navigation bar (stereOS | Collabor8 | JFDI | Gener8)
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

from datetime import datetime
from typing import Any, Optional
import uuid

# Import new modules
from IP.mermaid_generator import Fiefdom, FiefdomStatus, generate_empire_mermaid
from IP.terminal_spawner import TerminalSpawner
from IP.health_checker import HealthChecker
from IP.briefing_generator import BriefingGenerator
from IP.combat_tracker import CombatTracker
import anthropic

# Import Woven Maps Code City visualization
from IP.woven_maps import create_code_city, build_graph_data

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

.stereos-brand {{
    font-family: monospace;
    font-size: 14px;
    letter-spacing: 0.08em;
}}

.stereos-prefix {{
    color: {BLUE_DOMINANT};
}}

.stereos-suffix {{
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

    # Initialize services
    project_root_path = get_root()
    combat_tracker = CombatTracker(project_root_path)
    briefing_generator = BriefingGenerator(project_root_path)
    terminal_spawner = TerminalSpawner(project_root_path)

    # ========================================================================
    # EVENT HANDLERS (Transliterated from MaestroView.vue)
    # ========================================================================

    def log_action(action: str) -> None:
        """Log action to system logs."""
        logs = get_logs()
        timestamp = datetime.now().strftime("%H:%M:%S")
        set_logs(logs + [f"[{timestamp}] [Maestro] {action}"])

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

    def handle_home_click() -> None:
        """Reset to home state - clear panels and messages."""
        set_messages([])
        set_show_agents(False)
        set_show_tasks(False)
        set_show_terminal(False)
        set_show_summon(False)
        log_action("Reset to home state")

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

            # Call Claude API
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8192,
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
                    model="claude-sonnet-4",
                )

            # Create assistant message
            assistant_msg = {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": response_content,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
            }
            messages.append(assistant_msg)

        except anthropic.AuthenticationError as e:
            log_action(f"LLM Authentication Error: {str(e)}")
            assistant_msg = {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": f"⚠️ Authentication Error: Invalid ANTHROPIC_API_KEY\n\nPlease check your API key in environment variables.",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
            }
            messages.append(assistant_msg)
        except anthropic.APIError as e:
            log_action(f"LLM API Error: {str(e)}")

            # Fallback response
            assistant_msg = {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": f"⚠️ LLM API Error: {str(e)}\n\nPlease check your ANTHROPIC_API_KEY environment variable and network connection.",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
            }
            messages.append(assistant_msg)
        except Exception as e:
            log_action(f"Unexpected Error: {str(e)}")

            assistant_msg = {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": f"⚠️ Unexpected Error: {str(e)}",
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

    # ========================================================================
    # UI BUILDERS
    # ========================================================================

    def build_top_row() -> Any:
        """Build the top navigation row."""
        # Brand
        brand = mo.Html(f"""
        <div class="stereos-brand">
            <span class="stereos-prefix">stere</span><span class="stereos-suffix">OS</span>
        </div>
        """)

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

        return mo.hstack(
            [
                mo.ui.button(label="Home", on_change=lambda _: handle_home_click()),
                brand,
                nav_buttons,
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
            return create_code_city(root, width=850, height=500)
        except Exception as e:
            log_action(f"Code City error: {str(e)}")
            return mo.Html(f"""
            <div class="void-center">
                <div class="void-placeholder" style="color: {BLUE_DOMINANT};">
                    Error rendering Code City: {str(e)}
                </div>
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

        # Summon (Search) Panel
        if get_show_summon():
            summon_panel = mo.Html(f"""
            <div class="panel-overlay">
                <div class="panel-header">
                    <span class="panel-title">SUMMON - Global Search</span>
                </div>
                <div style="color: #999; font-size: 12px;">
                    Search across codebase, tasks, and agents.
                    <br><br>
                    <em>Integration with Carl contextualizer pending.</em>
                </div>
            </div>
            """)
            panels.append(summon_panel)

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

        # Left group
        left_buttons = mo.hstack(
            [
                mo.ui.button(
                    label="Apps", on_change=lambda _: log_action("Apps grid toggled")
                ),
                mo.ui.button(
                    label="Matrix",
                    on_change=lambda _: log_action("Matrix diagnostics opened"),
                ),
                mo.ui.button(
                    label="Files",
                    on_change=lambda _: log_action("Switch to Explorer tab"),
                ),
            ],
            gap="0.25rem",
        )

        # Center - maestro
        center_btn = mo.ui.button(label="maestro", on_change=lambda _: handle_summon())

        # Right group
        right_buttons = mo.hstack(
            [
                mo.ui.button(label="Search", on_change=lambda _: handle_summon()),
                mo.ui.button(
                    label="Phreak>",  # Opens actu8 terminal
                    on_change=lambda _: set_show_terminal(not get_show_terminal()),
                ),
                mo.ui.button(label="Send", on_change=lambda _: handle_send()),
                mo.ui.button(label="Attach", on_change=lambda _: handle_attach()),
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

    # Status bar
    root = get_root()
    selected = get_selected()
    status_bar = mo.md(f"**Root:** `{root}` | **Selected:** `{selected or 'None'}`")

    return mo.vstack(
        [
            css_injection,
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
        ]
    )
