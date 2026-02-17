"""Reusable Maestro view builders with explicit inputs."""

from __future__ import annotations

from typing import Any, Callable, List


def build_summon_results_view(
    mo: Any,
    *,
    query: str,
    results: List[dict],
    loading: bool,
    gold_color: str,
    blue_color: str,
    purple_color: str,
    dismiss_button: Any = None,
) -> Any:
    """Render search results as emergent cards with Void Design patterns."""
    # Build dismiss button HTML - diamond (rotated square), NOT X
    dismiss_html = ""
    if dismiss_button:
        dismiss_html = f"""
        <div class="summon-header">
            <span class="summon-title">Summon</span>
            <div class="diamond-dismiss" onclick="{dismiss_button._js_event_name}" title="Dismiss"></div>
        </div>
        """
    else:
        dismiss_html = """
        <div class="summon-header">
            <span class="summon-title">Summon</span>
        </div>
        """

    if not query or len(query) < 2:
        return mo.Html(
            f"""
            <div class="summon-container">
                {dismiss_html}
                <div class="void-placeholder" style="color: var(--text-muted);">
                    Type at least 2 characters to search the codebase...
                </div>
            </div>
            """
        )

    if loading:
        return mo.Html(
            f"""
            <div class="summon-container">
                {dismiss_html}
                <div class="void-placeholder" style="color: {gold_color};">
                    Scanning the Void...
                </div>
            </div>
            """
        )

    if not results:
        return mo.Html(
            f"""
            <div class="summon-container">
                {dismiss_html}
                <div class="void-placeholder">
                    No results found for "{query}"
                </div>
            </div>
            """
        )

    cards_html = ""
    for idx, result in enumerate(results[:10]):
        fiefdom = result.get("fiefdom", "Unknown")
        health = result.get("health", {})
        status = health.get("status", "working")

        status_color = {
            "working": gold_color,
            "broken": blue_color,
            "combat": purple_color,
        }.get(status, gold_color)

        error_count = len(health.get("errors", []))
        warning_count = len(health.get("warnings", []))

        # Use summon-item with emergence animation (staggered delay)
        cards_html += f"""
        <div class="summon-item" style="border-left-color: {status_color}; animation-delay: {idx * 50}ms;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: {status_color}; font-family: monospace; font-weight: 600;">
                    {fiefdom}
                </span>
                <span style="color: var(--text-muted); font-size: 10px;">
                    {status.upper()}
                </span>
            </div>
            <div style="margin-top: 8px; font-size: 12px; color: var(--text-secondary);">
                {error_count} errors, {warning_count} warnings
            </div>
        </div>
        """

    # Return with summon-container for emergence animation
    return mo.Html(
        f"""
        <div class="summon-container">
            {dismiss_html}
            <div class="summon-results">
                {cards_html}
            </div>
        </div>
        """
    )


def build_void_messages_view(mo: Any, *, messages: List[dict]) -> Any:
    """Build the void emergence display from the last assistant messages."""
    assistant_msgs = [m for m in messages if m["role"] == "assistant"][-3:]

    if not assistant_msgs:
        return mo.Html(
            """
            <div class="void-center">
                <div class="void-placeholder">
                    The void awaits your command...
                </div>
            </div>
            """
        )

    message_html = ""
    for msg in assistant_msgs:
        msg_class = (
            "emerged-message optimistic-message"
            if msg.get("optimistic")
            else "emerged-message"
        )
        message_html += f"""
        <div class="{msg_class}">
            <div class="content">{msg["content"]}</div>
            <div class="meta">{msg["timestamp"]}</div>
        </div>
        """

    return mo.Html(
        f"""
        <div class="void-center">
            <div style="width: 100%; max-width: 700px;">
                {message_html}
            </div>
        </div>
        """
    )


def build_app_matrix_view(
    mo: Any,
    *,
    toggle_calendar: Callable[[], None],
    toggle_comms: Callable[[], None],
    toggle_file_explorer: Callable[[], None],
    handle_jfdi: Callable[[], None],
    set_view_mode: Callable[[str], None],
    gold_color: str,
) -> Any:
    """Render App Matrix launcher view in THE VOID."""
    matrix_header = mo.Html(
        f"""
        <div class="void-center" style="padding-bottom: 12px;">
            <div style="width: 100%; max-width: 820px;">
                <div style="color:{gold_color};font-size:12px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">
                    App Matrix
                </div>
                <div style="color:var(--text-secondary);font-size:11px;line-height:1.5;">
                    Launch command interfaces without leaving THE VOID.
                </div>
            </div>
        </div>
        """
    )
    launchers = mo.hstack(
        [
            mo.ui.button(label="Calendar*", on_click=lambda _: toggle_calendar()),
            mo.ui.button(label="Comms*", on_click=lambda _: toggle_comms()),
            mo.ui.button(label="Files", on_click=lambda _: toggle_file_explorer()),
            mo.ui.button(label="JFDI", on_click=lambda _: handle_jfdi()),
            mo.ui.button(label="Chat", on_click=lambda _: set_view_mode("chat")),
            mo.ui.button(label="Code City", on_click=lambda _: set_view_mode("city")),
        ],
        gap=0.5,
        justify="start",
        align="center",
        wrap=True,
    )
    return mo.vstack([matrix_header, launchers])


def build_attachment_bar_view(
    mo: Any, *, attached_files: List[str], gold_color: str
) -> Any:
    """Build attachment chips if files are attached."""
    if not attached_files:
        return mo.md("")

    chips_html = ""
    for file_path in attached_files:
        filename = file_path.split("/")[-1] if "/" in file_path else file_path
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
            color: {gold_color};
            margin-right: 8px;
        ">
            {filename}
        </span>
        """

    return mo.Html(
        f"""
        <div style="
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 8px 0;
            margin-bottom: 8px;
        ">
            {chips_html}
        </div>
        """
    )
