"""Maestro shell view builders for panels and controls."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

# VISUAL TOKEN LOCK - EXACT VALUES (HERD 2)
BG_OBSIDIAN = "#050505"  # Panel background
GOLD_DARK = "#C5A028"  # Borders
GOLD_LIGHT = "#F4C430"  # Lock icon (locked)
TEXT_GREY = "#CCC"  # Body text
TEXT_DIM = "rgba(255,255,255,0.4)"  # Unlocked state
STATE_WORKING = "#D4AF37"  # Header
FONT_DATA = "'VT323', monospace"  # Data text


def _build_lock_indicator(is_locked: bool, lock_reason: Optional[str] = None) -> str:
    """Build Louis lock indicator with proper colors."""
    if is_locked:
        color = GOLD_LIGHT
        icon = "&#128274;"  # Lock emoji
        tooltip = f"LOCKED: {lock_reason or 'Louis Lock'}"
    else:
        color = TEXT_DIM
        icon = "&#128275;"  # Unlock emoji
        tooltip = "Unlocked"

    return (
        f'<span style="color:{color};font-size:12px;" title="{tooltip}">{icon}</span>'
    )


def _build_node_info_panel(building_panel: dict, room_entry: Optional[dict]) -> str:
    """Build the working node info panel with real data."""
    path = building_panel.get("path", "unknown")
    status = building_panel.get("status", "working")
    loc = building_panel.get("loc", 0)
    export_count = building_panel.get("export_count", 0)
    centrality = building_panel.get("centrality", 0.0)
    in_cycle = building_panel.get("in_cycle", False)
    locked = building_panel.get("locked", False)
    lock_state = building_panel.get("lock_state")

    # Get imports/exports
    imports = building_panel.get("imports", [])[:5]  # Limit display
    exports = building_panel.get("exports", [])[:5]
    rooms = building_panel.get("rooms", [])[:4]  # Limit rooms

    # Health errors
    health_errors = building_panel.get("health_errors", [])[:3]

    # Status color
    if status == "broken":
        status_color = "#1fbdea"  # Blue for broken
        status_label = "BROKEN"
    elif status == "combat":
        status_color = "#9D4EDD"  # Purple for combat
        status_label = "COMBAT"
    else:
        status_color = STATE_WORKING  # Gold for working
        status_label = "WORKING"

    # Build imports section
    imports_html = ""
    if imports:
        imports_html = "<div style='margin-top:8px;'><span style='color:#666;font-size:10px;'>IMPORTS:</span>"
        for imp in imports:
            imports_html += f"<div style='color:var(--text-secondary);font-size:10px;font-family:{FONT_DATA};margin-left:4px;'>- {imp.split('/')[-1]}</div>"
        imports_html += "</div>"

    # Build exports section
    exports_html = ""
    if exports:
        exports_html = "<div style='margin-top:8px;'><span style='color:#666;font-size:10px;'>EXPORTS:</span>"
        for exp in exports:
            exports_html += f"<div style='color:var(--text-secondary);font-size:10px;font-family:{FONT_DATA};margin-left:4px;'>+ {exp}</div>"
        exports_html += "</div>"

    # Build rooms section
    rooms_html = ""
    if rooms:
        rooms_html = "<div style='margin-top:8px;'><span style='color:#666;font-size:10px;'>ROOMS:</span>"
        for room in rooms:
            room_status_color = (
                STATE_WORKING if room.get("status") == "working" else "#1fbdea"
            )
            rooms_html += f"<div style='color:{room_status_color};font-size:10px;font-family:{FONT_DATA};margin-left:4px;'>• {room.get('name', 'unknown')} ({room.get('room_type', 'func')})</div>"
        rooms_html += "</div>"

    # Build errors section
    errors_html = ""
    if health_errors:
        errors_html = "<div style='margin-top:8px;padding:6px;background:rgba(31,189,234,0.1);border-radius:4px;'>"
        errors_html += "<span style='color:#1fbdea;font-size:10px;'>ERRORS:</span>"
        for err in health_errors:
            errors_html += f"<div style='color:#1fbdea;font-size:10px;font-family:{FONT_DATA};margin-left:4px;'>! {err[:60]}</div>"
        errors_html += "</div>"

    # Lock indicator
    lock_indicator = _build_lock_indicator(locked, lock_state)

    # Centrality and cycle info
    meta_info = f"centrality: {centrality:.2f}" + (", in cycle" if in_cycle else "")

    return f"""
    <div style='background:{BG_OBSIDIAN};border:1px solid {GOLD_DARK};border-radius:8px;padding:16px;margin-bottom:12px;'>
        <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;'>
            <span style='color:{STATE_WORKING};font-family:{FONT_DATA};font-size:14px;letter-spacing:1px;'>
                NODE INFO {lock_indicator}
            </span>
            <span style='color:{status_color};font-family:{FONT_DATA};font-size:11px;padding:2px 8px;border:1px solid {status_color};border-radius:3px;'>
                {status_label}
            </span>
        </div>
        
        <div style='color:{TEXT_GREY};font-family:{FONT_DATA};font-size:12px;margin-bottom:4px;word-break:break-all;'>
            {path}
        </div>
        
        <div style='display:flex;gap:16px;margin-top:8px;color:#666;font-size:10px;font-family:{FONT_DATA};'>
            <span>loc: {loc}</span>
            <span>exports: {export_count}</span>
            <span>{meta_info}</span>
        </div>
        
        {errors_html}
        {imports_html}
        {exports_html}
        {rooms_html}
    </div>
    """


def _build_room_info_panel(room_entry: dict, building_panel: dict) -> str:
    """Build room-level info panel when a room is selected."""
    if not room_entry:
        return ""

    name = room_entry.get("name", "unknown")
    room_type = room_entry.get("room_type", "function")
    line_start = room_entry.get("line_start", 0)
    line_end = room_entry.get("line_end", 0)
    status = room_entry.get("status", "working")
    errors = room_entry.get("errors", [])

    # Status color
    if status == "broken":
        status_color = "#1fbdea"
        status_label = "BROKEN"
    elif status == "combat":
        status_color = "#9D4EDD"
        status_label = "COMBAT"
    else:
        status_color = STATE_WORKING
        status_label = "WORKING"

    # Errors display
    errors_html = ""
    if errors:
        errors_html = "<div style='margin-top:8px;padding:6px;background:rgba(31,189,234,0.1);border-radius:4px;'>"
        for err in errors[:2]:
            errors_html += f"<div style='color:#1fbdea;font-size:10px;font-family:{FONT_DATA};'>! {err[:80]}</div>"
        errors_html += "</div>"

    return f"""
    <div style='background:{BG_OBSIDIAN};border:1px solid {GOLD_DARK};border-radius:8px;padding:12px;margin-top:8px;'>
        <div style='display:flex;justify-content:space-between;align-items:center;'>
            <span style='color:{GOLD_LIGHT};font-family:{FONT_DATA};font-size:12px;'>
                {name}
            </span>
            <span style='color:{status_color};font-size:10px;font-family:{FONT_DATA};'>
                {status_label} · {room_type}
            </span>
        </div>
        <div style='color:#666;font-size:10px;font-family:{FONT_DATA};margin-top:4px;'>
            lines {line_start}-{line_end}
        </div>
        {errors_html}
    </div>
    """


def build_panels_view(
    mo: Any,
    *,
    get_show_agents: Callable[[], bool],
    get_agent_group: Callable[[], str],
    settlement_agent_groups: Dict[str, List[dict]],
    get_agent_id: Callable[[], str],
    set_collabor8_group: Callable[[str], None],
    set_agent_id: Callable[[str], None],
    deploy_selected_agent: Callable[[], None],
    get_show_settings: Callable[[], bool],
    gold_color: str,
    available_models: List[str],
    get_selected_model: Callable[[], str],
    set_selected_model: Callable[[str], None],
    get_show_summon: Callable[[], bool],
    get_summon_query: Callable[[], str],
    set_summon_query: Callable[[str], None],
    trigger_carl_search: Callable[[str], None],
    build_summon_results: Callable[[], Any],
    get_selected: Callable[[], Optional[str]],
    get_code_city_context: Callable[[], Optional[dict]],
    carl: Any,
    bg_primary: str,
    blue_color: str,
) -> Any:
    """Build conditional overlay panels."""
    panels: List[Any] = []
    code_city_context = get_code_city_context() or {}
    building_panel = (
        code_city_context.get("building_panel", {})
        if isinstance(code_city_context, dict)
        else {}
    )
    room_entry = (
        code_city_context.get("room_entry", {})
        if isinstance(code_city_context, dict)
        else {}
    )
    context_path = (
        building_panel.get("path") if isinstance(building_panel, dict) else None
    )

    if get_show_agents():
        selected_group = get_agent_group()
        group_agents = settlement_agent_groups.get(selected_group, [])
        group_options = list(settlement_agent_groups.keys())
        current_agent_id = get_agent_id()
        if (
            current_agent_id not in {agent["id"] for agent in group_agents}
            and group_agents
        ):
            current_agent_id = group_agents[0]["id"]

        selected_agent = next(
            (agent for agent in group_agents if agent["id"] == current_agent_id),
            None,
        )
        agent_options = {
            agent["id"]: f"T{agent['tier']} · {agent['name']}" for agent in group_agents
        }

        header = mo.Html(
            """
            <div class="panel-overlay">
                <div class="panel-header">
                    <span class="panel-title">COLLABOR8 - Settlement Agents</span>
                </div>
                <div style="color:var(--text-secondary);font-size:11px;margin-bottom:8px;">
                    Explore / Plan / Execute / Monitor / Strategic
                </div>
            </div>
            """
        )

        # Define agent selectors (before using them)
        group_picker = mo.ui.dropdown(
            options=group_options,
            value=selected_group,
            label="Agent Group",
            on_change=lambda value: set_collabor8_group(value),
        )
        agent_picker = mo.ui.dropdown(
            options=agent_options,
            value=current_agent_id,
            label="Agent",
            on_change=set_agent_id,
        )

        if selected_agent:
            brief = mo.Html(
                f"""
                <div class="panel-overlay" style="margin-top:8px;">
                    <div style="color:{gold_color};font-family:monospace;font-size:11px;">
                        {selected_agent["name"]} · Tier {selected_agent["tier"]}
                    </div>
                    <div style="color:var(--text-secondary);font-size:11px;margin-top:6px;line-height:1.5;">
                        {selected_agent["brief"]}
                    </div>
                </div>
                """
            )
        else:
            brief = mo.md("")

        deploy_btn = mo.ui.button(
            label="Deploy Agent",
            on_click=lambda _: deploy_selected_agent(),
            disabled=selected_agent is None,
        )

        # Use new node info panel with locked visual tokens
        if context_path:
            context_card = mo.Html(_build_node_info_panel(building_panel, room_entry))

            # Add room info panel if a room is selected
            if room_entry:
                room_info = mo.Html(_build_room_info_panel(room_entry, building_panel))
                panels.extend(
                    [
                        header,
                        context_card,
                        room_info,
                        group_picker,
                        agent_picker,
                        brief,
                        deploy_btn,
                    ]
                )
            else:
                panels.extend(
                    [
                        header,
                        context_card,
                        group_picker,
                        agent_picker,
                        brief,
                        deploy_btn,
                    ]
                )
        else:
            context_card = mo.md("")
            panels.extend(
                [header, context_card, group_picker, agent_picker, brief, deploy_btn]
            )

    if get_show_settings():
        setting_rows = "".join(
            f"<div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.04);'>"
            f"<span style='color:var(--text-secondary);'>parameter_{idx:03d}</span><span style='color:{gold_color};'>active</span></div>"
            for idx in range(1, 161)
        )
        settings_panel = mo.Html(
            f"""
            <div class="panel-overlay">
                <div class="panel-header">
                    <span class="panel-title">SETTINGS - Infinite Scroll</span>
                </div>
                <div style="color:var(--text-secondary);font-size:11px;margin-bottom:8px;">
                    Model and behavior configuration surface (150+ parameters).
                </div>
                <div style="max-height:280px;overflow-y:auto;padding-right:6px;">
                    {setting_rows}
                </div>
            </div>
            """
        )
        settings_model_picker = mo.ui.dropdown(
            options=available_models,
            value=get_selected_model(),
            label="Default Model",
            on_change=set_selected_model,
        )
        panels.extend([settings_panel, settings_model_picker])

    if get_show_summon():

        def on_summon_change(query: str) -> None:
            set_summon_query(query)
            trigger_carl_search(query)

        summon_input = mo.ui.text(
            value=get_summon_query(),
            placeholder="Search codebase, tasks, agents...",
            on_change=on_summon_change,
            full_width=True,
        )
        results_display = build_summon_results()

        selected_fiefdom = (
            get_selected() or code_city_context.get("context_scope") or "IP"
        )
        try:
            context_json = carl.gather_context_json(selected_fiefdom)
            context_footer = f"""<details style="margin-top: 16px;">
                <summary style="color: var(--text-muted); font-size: 11px; cursor: pointer;">
                    View Raw Context JSON
                </summary>
                <pre style='color:var(--text-secondary);font-size:9px;white-space:pre-wrap;max-height:200px;overflow:auto;background:{bg_primary};padding:8px;border-radius:4px;margin-top:8px;'>{context_json}</pre>
            </details>"""
        except Exception as error:
            context_footer = (
                f"<span style='color:{blue_color};font-size:10px;'>"
                f"Context error: {error}</span>"
            )

        summon_panel = mo.Html(
            f"""
            <div class="panel-overlay" style="animation: emergence-scale 0.4s ease-out both;">
                <div class="panel-header">
                    <span class="panel-title">SUMMON - Neighborhood Search</span>
                </div>
                <div style="margin-bottom: 12px;">
                    <span style="color:var(--text-muted);font-size:11px;">Selected: </span>
                    <span style="color:{gold_color};font-family:monospace;">{selected_fiefdom}</span>
                </div>
            </div>
            """
        )
        if context_path:
            # Use new node info panel with locked visual tokens for summon view
            context_summary = mo.Html(
                _build_node_info_panel(building_panel, room_entry)
            )
        else:
            context_summary = mo.md("")
        panels.extend(
            [
                summon_panel,
                context_summary,
                summon_input,
                results_display,
                mo.Html(context_footer),
            ]
        )

    if panels:
        return mo.vstack(panels)
    return mo.md("")


def build_control_surface_view(
    mo: Any,
    *,
    user_input: str,
    set_user_input: Callable[[str], None],
    flagship_agent: str,
    cycle_maestro_state: Callable[[], None],
    get_maestro_state: Callable[[], str],
    handle_apps: Callable[[], None],
    toggle_calendar: Callable[[], None],
    toggle_comms: Callable[[], None],
    toggle_file_explorer: Callable[[], None],
    handle_summon: Callable[[], None],
    toggle_recording: Callable[[], None],
    handle_playback: Callable[[], None],
    has_audio_recording: Callable[[], bool],
    handle_terminal: Callable[[], None],
    handle_send: Callable[[], None],
    handle_attach: Callable[[], None],
) -> Any:
    """Build the bottom control surface with 5-1-6 button rhythm."""
    chat_input = mo.ui.text_area(
        value=user_input,
        placeholder="What would you like to accomplish?",
        on_change=set_user_input,
        full_width=True,
        rows=3,
        debounce=False,
    )

    left_buttons = mo.hstack(
        [
            mo.ui.button(label="Apps", on_click=lambda _: handle_apps()),
            mo.ui.button(
                label="Matrix",
                on_click=lambda _: handle_apps(),
            ),
            mo.ui.button(label="Calendar*", on_click=lambda _: toggle_calendar()),
            mo.ui.button(label="Comms*", on_click=lambda _: toggle_comms()),
            mo.ui.button(label="Files", on_click=lambda _: toggle_file_explorer()),
        ],
        gap=0.5,
        justify="start",
        align="center",
        wrap=True,
    )

    center_btn = mo.ui.button(
        label=flagship_agent,
        on_click=lambda _: cycle_maestro_state(),
    )
    state_indicator = mo.Html(
        f'<span class="maestro-state-indicator">@{flagship_agent} {get_maestro_state().lower()}</span>'
    )
    center_group = mo.hstack(
        [center_btn, state_indicator],
        gap=0.35,
        justify="center",
        align="center",
        wrap=True,
    )

    right_buttons = mo.hstack(
        [
            mo.ui.button(label="Search", on_click=lambda _: handle_summon()),
            mo.ui.button(label="Record", on_click=lambda _: toggle_recording()),
            mo.ui.button(
                label="Playback",
                on_click=lambda _: handle_playback(),
                disabled=not has_audio_recording(),
            ),
            mo.ui.button(label="Phreak>", on_click=lambda _: handle_terminal()),
            mo.ui.button(label="Send", on_click=lambda _: handle_send()),
            mo.ui.button(label="Attach", on_click=lambda _: handle_attach()),
        ],
        gap=0.5,
        justify="end",
        align="center",
        wrap=True,
    )

    control_row = mo.hstack(
        [left_buttons, center_group, right_buttons],
        justify="space-between",
        align="center",
        wrap=True,
        gap=1.0,
    )

    return mo.vstack([chat_input, control_row], gap=0.4).style(
        {
            "width": "100%",
            "max-width": "1280px",
            "margin": "0 auto",
            "padding": "0.5rem 0 0",
            "border-top": "1px solid rgba(31, 189, 234, 0.2)",
        }
    )
