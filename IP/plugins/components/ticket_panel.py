# IP/plugins/components/ticket_panel.py
from datetime import datetime
from typing import Any, List, Optional
import marimo as mo

from IP.ticket_manager import TicketManager, Ticket

# Import Maestro colors for consistency
BLUE_DOMINANT = "#1fbdea"
GOLD_METALLIC = "#D4AF37"
GOLD_DARK = "#B8860B"
GOLD_SAFFRON = "#F4C430"
BG_ELEVATED = "#121214"

# Ticket panel CSS - slides from RIGHT
TICKET_PANEL_CSS = f"""
<style>
.ticket-panel-overlay {{
    position: fixed;
    top: 0;
    right: 0;
    width: 400px;
    height: 100vh;
    background: {BG_ELEVATED};
    border-left: 1px solid rgba(31, 189, 234, 0.3);
    z-index: 1000;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.ticket-panel-header {{
    padding: 16px;
    border-bottom: 1px solid rgba(31, 189, 234, 0.2);
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.ticket-panel-title {{
    color: {GOLD_METALLIC};
    font-family: monospace;
    font-size: 12px;
    letter-spacing: 0.1em;
}}

.ticket-panel-close {{
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.3);
    color: {BLUE_DOMINANT};
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
    font-family: monospace;
    font-size: 10px;
}}

.ticket-panel-close:hover {{
    color: {GOLD_METALLIC};
    border-color: {GOLD_METALLIC};
}}

.ticket-panel-body {{
    flex: 1;
    overflow-y: auto;
    padding: 16px;
}}

.ticket-filter-bar {{
    margin-bottom: 16px;
    display: flex;
    gap: 8px;
    align-items: center;
}}

.ticket-filter-select {{
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.3);
    color: {BLUE_DOMINANT};
    padding: 4px 8px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 10px;
}}

.ticket-search-input {{
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.3);
    color: #e8e8e8;
    padding: 4px 8px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 10px;
    flex: 1;
}}

.ticket-list {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.ticket-item {{
    background: rgba(18, 18, 20, 0.9);
    border: 1px solid rgba(31, 189, 234, 0.2);
    border-radius: 6px;
    padding: 12px;
    cursor: pointer;
    transition: all 150ms ease-out;
}}

.ticket-item:hover {{
    border-color: rgba(212, 175, 55, 0.3);
    background: rgba(212, 175, 55, 0.05);
}}

.ticket-item.selected {{
    border-color: {GOLD_METALLIC};
    background: rgba(212, 175, 55, 0.1);
}}

.ticket-item-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}}

.ticket-item-id {{
    color: {GOLD_METALLIC};
    font-family: monospace;
    font-size: 10px;
}}

.ticket-item-status {{
    padding: 2px 6px;
    border-radius: 3px;
    font-family: monospace;
    font-size: 8px;
    text-transform: uppercase;
}}

.ticket-item-status.open {{
    background: rgba(31, 189, 234, 0.2);
    color: {BLUE_DOMINANT};
}}

.ticket-item-status.in_progress {{
    background: rgba(244, 196, 48, 0.2);
    color: {GOLD_SAFFRON};
}}

.ticket-item-status.resolved {{
    background: rgba(34, 197, 94, 0.2);
    color: #22c55e;
}}

.ticket-item-status.archived {{
    background: rgba(107, 114, 128, 0.2);
    color: #6b7280;
}}

.ticket-item-title {{
    color: #e8e8e8;
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 4px;
}}

.ticket-item-fiefdom {{
    color: #999;
    font-family: monospace;
    font-size: 9px;
    margin-bottom: 4px;
}}

.ticket-item-meta {{
    display: flex;
    justify-content: space-between;
    color: #666;
    font-family: monospace;
    font-size: 8px;
}}

.ticket-detail-panel {{
    background: rgba(18, 18, 20, 0.9);
    border: 1px solid rgba(31, 189, 234, 0.2);
    border-radius: 6px;
    padding: 16px;
    margin-top: 16px;
}}

.ticket-detail-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(31, 189, 234, 0.2);
}}

.ticket-detail-title {{
    color: {GOLD_METALLIC};
    font-size: 14px;
    font-weight: 500;
}}

.ticket-detail-section {{
    margin-bottom: 16px;
}}

.ticket-detail-label {{
    color: {GOLD_METALLIC};
    font-family: monospace;
    font-size: 10px;
    text-transform: uppercase;
    margin-bottom: 4px;
}}

.ticket-detail-content {{
    color: #e8e8e8;
    font-size: 11px;
    line-height: 1.4;
    white-space: pre-wrap;
}}

.ticket-detail-errors {{
    color: #ef4444;
    font-family: monospace;
    font-size: 9px;
    margin-top: 4px;
}}

.ticket-detail-warnings {{
    color: #f59e0b;
    font-family: monospace;
    font-size: 9px;
    margin-top: 4px;
}}

.ticket-notes-section {{
    margin-top: 16px;
}}

.ticket-note-item {{
    background: rgba(31, 189, 234, 0.05);
    border-left: 2px solid {BLUE_DOMINANT};
    padding: 8px;
    margin-bottom: 8px;
}}

.ticket-note-time {{
    color: {GOLD_DARK};
    font-family: monospace;
    font-size: 8px;
}}

.ticket-note-author {{
    color: {BLUE_DOMINANT};
    font-family: monospace;
    font-size: 9px;
    margin-left: 8px;
}}

.ticket-note-text {{
    color: #e8e8e8;
    font-size: 10px;
    margin-top: 4px;
}}

.ticket-add-note-form {{
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid rgba(31, 189, 234, 0.2);
}}

.ticket-note-input {{
    width: 100%;
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.3);
    color: #e8e8e8;
    padding: 6px 8px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 10px;
    resize: vertical;
    min-height: 40px;
}}

.ticket-actions {{
    display: flex;
    gap: 8px;
    margin-top: 12px;
}}

.ticket-action-btn {{
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.3);
    color: {BLUE_DOMINANT};
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
    font-family: monospace;
    font-size: 9px;
    transition: all 150ms ease-out;
}}

.ticket-action-btn:hover {{
    color: {GOLD_METALLIC};
    border-color: {GOLD_METALLIC};
}}
</style>
"""


class TicketPanel:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.ticket_manager = TicketManager(project_root)

        # State
        self._is_visible = False
        self._selected_ticket_id = None
        self._status_filter = None
        self._search_query = ""

    def toggle_visibility(self) -> None:
        """Toggle panel visibility."""
        self._is_visible = not self._is_visible

    def set_visible(self, visible: bool) -> None:
        """Set panel visibility."""
        self._is_visible = visible

    def is_visible(self) -> bool:
        """Check if panel is visible."""
        return self._is_visible

    def select_ticket(self, ticket_id: str) -> None:
        """Select a ticket for detail view."""
        self._selected_ticket_id = ticket_id

    def set_status_filter(self, status_filter: Optional[str]) -> None:
        """Set status filter."""
        self._status_filter = status_filter

    def set_search_query(self, query: str) -> None:
        """Set search query."""
        self._search_query = query.lower()

    def get_filtered_tickets(self) -> List[Ticket]:
        """Get tickets filtered by current filters."""
        tickets = self.ticket_manager.list_tickets(self._status_filter)

        # Apply search filter
        if self._search_query:
            tickets = [
                t
                for t in tickets
                if (
                    self._search_query in t.title.lower()
                    or self._search_query in t.description.lower()
                    or self._search_query in t.fiefdom.lower()
                    or self._search_query in t.id.lower()
                )
            ]

        return tickets

    def add_note_to_selected(self, author: str, text: str) -> bool:
        """Add note to selected ticket."""
        if not self._selected_ticket_id:
            return False

        return self.ticket_manager.add_note(self._selected_ticket_id, author, text)

    def update_selected_status(self, status: str) -> bool:
        """Update selected ticket status."""
        if not self._selected_ticket_id:
            return False

        return self.ticket_manager.update_ticket_status(
            self._selected_ticket_id, status
        )

    def render(self) -> Any:
        """Render the ticket panel."""
        if not self._is_visible:
            return mo.md("")

        # Get filtered tickets
        tickets = self.get_filtered_tickets()
        selected_ticket = None
        if self._selected_ticket_id:
            selected_ticket = self.ticket_manager.get_ticket(self._selected_ticket_id)

        # Build HTML
        panel_html = f"""
        <div class="ticket-panel-overlay">
            <div class="ticket-panel-header">
                <span class="ticket-panel-title">TICKET PANEL</span>
                <button class="ticket-panel-close" onclick="window.location.reload()">✕</button>
            </div>
            <div class="ticket-panel-body">
                {self._build_filter_bar()}
                {self._build_ticket_list(tickets)}
                {self._build_ticket_detail(selected_ticket) if selected_ticket else ""}
            </div>
        </div>
        """

        return mo.Html(TICKET_PANEL_CSS + panel_html)

    def _build_filter_bar(self) -> str:
        """Build filter and search bar."""
        return f"""
        <div class="ticket-filter-bar">
            <select class="ticket-filter-select">
                <option value="">All Status</option>
                <option value="open" {"selected" if self._status_filter == "open" else ""}>Open</option>
                <option value="in_progress" {"selected" if self._status_filter == "in_progress" else ""}>In Progress</option>
                <option value="resolved" {"selected" if self._status_filter == "resolved" else ""}>Resolved</option>
                <option value="archived" {"selected" if self._status_filter == "archived" else ""}>Archived</option>
            </select>
            <input type="text" class="ticket-search-input" placeholder="Search tickets..." value="{self._search_query}">
        </div>
        """

    def _build_ticket_list(self, tickets: List[Ticket]) -> str:
        """Build ticket list."""
        if not tickets:
            return '<div style="color: #666; text-align: center; padding: 20px;">No tickets found</div>'

        tickets_html = ""
        for ticket in tickets:
            is_selected = ticket.id == self._selected_ticket_id
            tickets_html += self._build_ticket_item(ticket, is_selected)

        return f'<div class="ticket-list">{tickets_html}</div>'

    def _build_ticket_item(self, ticket: Ticket, is_selected: bool) -> str:
        """Build single ticket item."""
        created_date = datetime.fromisoformat(ticket.created_at).strftime("%m/%d")
        error_count = len(ticket.errors)
        warning_count = len(ticket.warnings)

        return f"""
        <div class="ticket-item {"selected" if is_selected else ""}" onclick="select_ticket('{ticket.id}')">
            <div class="ticket-item-header">
                <span class="ticket-item-id">#{ticket.id}</span>
                <span class="ticket-item-status {ticket.status}">{ticket.status.replace("_", " ")}</span>
            </div>
            <div class="ticket-item-title">{ticket.title}</div>
            <div class="ticket-item-fiefdom">{ticket.fiefdom}</div>
            <div class="ticket-item-meta">
                <span>{created_date}</span>
                <span>{error_count}E {warning_count}W</span>
            </div>
        </div>
        """

    def _build_ticket_detail(self, ticket: Ticket) -> str:
        """Build ticket detail panel."""
        if not ticket:
            return ""

        # Format errors and warnings
        errors_html = ""
        if ticket.errors:
            errors_html = (
                '<div class="ticket-detail-errors">'
                + "\n".join(ticket.errors)
                + "</div>"
            )

        warnings_html = ""
        if ticket.warnings:
            warnings_html = (
                '<div class="ticket-detail-warnings">'
                + "\n".join(ticket.warnings)
                + "</div>"
            )

        # Format notes
        notes_html = ""
        if ticket.notes:
            notes_items = ""
            for note in ticket.notes:
                notes_items += f"""
                <div class="ticket-note-item">
                    <span class="ticket-note-time">{note["time"]}</span>
                    <span class="ticket-note-author">{note["author"]}</span>
                    <div class="ticket-note-text">{note["text"]}</div>
                </div>
                """
            notes_html = f'<div class="ticket-notes-section">{notes_items}</div>'

        return f"""
        <div class="ticket-detail-panel">
            <div class="ticket-detail-header">
                <span class="ticket-detail-title">#{ticket.id}: {ticket.title}</span>
                <span class="ticket-item-status {ticket.status}">{ticket.status.replace("_", " ")}</span>
            </div>
            
            <div class="ticket-detail-section">
                <div class="ticket-detail-label">Fiefdom</div>
                <div class="ticket-detail-content">{ticket.fiefdom}</div>
            </div>
            
            <div class="ticket-detail-section">
                <div class="ticket-detail-label">Description</div>
                <div class="ticket-detail-content">{ticket.description}</div>
            </div>
            
            <div class="ticket-detail-section">
                <div class="ticket-detail-label">Issues</div>
                {errors_html}
                {warnings_html}
            </div>
            
            {notes_html}
            
            <div class="ticket-add-note-form">
                <div class="ticket-detail-label">Add Note</div>
                <textarea class="ticket-note-input" placeholder="Enter note..."></textarea>
                <div class="ticket-actions">
                    <button class="ticket-action-btn">Add Note</button>
                    <button class="ticket-action-btn">Update Status</button>
                </div>
            </div>
        </div>
        """
