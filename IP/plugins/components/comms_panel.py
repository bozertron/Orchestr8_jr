# IP/plugins/components/comms_panel.py
"""
Comms panel for Marimo.
Provides P2P messaging and contacts within maestro.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
import importlib.util
from pathlib import Path
import marimo as mo

# Import comms adapter using importlib to handle path resolution
comms_adapter = None
try:
    _adapter_path = Path(__file__).parent.parent.parent.parent / "888" / "comms" / "adapter.py"
    if _adapter_path.exists():
        spec = importlib.util.spec_from_file_location("comms_adapter", _adapter_path)
        if spec and spec.loader:
            comms_adapter = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(comms_adapter)
except Exception:
    comms_adapter = None

# Import Maestro colors for consistency
BLUE_DOMINANT = "#1fbdea"
GOLD_METALLIC = "#D4AF37"
GOLD_DARK = "#B8860B"
GOLD_SAFFRON = "#F4C430"
BG_ELEVATED = "#121214"
PURPLE_COMBAT = "#9D4EDD"

# Comms Panel CSS
COMMS_PANEL_CSS = f"""
<style>
.comms-panel-overlay {{
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

.comms-panel-header {{
    padding: 16px;
    border-bottom: 1px solid rgba(31, 189, 234, 0.2);
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.comms-panel-title {{
    color: {GOLD_METALLIC};
    font-family: monospace;
    font-size: 12px;
    letter-spacing: 0.1em;
}}

.comms-panel-close {{
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.3);
    color: {BLUE_DOMINANT};
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
    font-family: monospace;
    font-size: 10px;
}}

.comms-panel-close:hover {{
    color: {GOLD_METALLIC};
    border-color: {GOLD_METALLIC};
}}

.comms-tabs {{
    display: flex;
    border-bottom: 1px solid rgba(31, 189, 234, 0.1);
}}

.comms-tab {{
    flex: 1;
    padding: 10px;
    background: transparent;
    border: none;
    color: #666;
    font-family: monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    cursor: pointer;
    transition: all 150ms ease-out;
}}

.comms-tab:hover {{
    color: {BLUE_DOMINANT};
}}

.comms-tab.active {{
    color: {GOLD_METALLIC};
    border-bottom: 2px solid {GOLD_METALLIC};
}}

.comms-body {{
    flex: 1;
    overflow-y: auto;
    padding: 16px;
}}

.contact-list {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.contact-item {{
    display: flex;
    align-items: center;
    padding: 12px;
    background: rgba(18, 18, 20, 0.9);
    border: 1px solid rgba(31, 189, 234, 0.2);
    border-radius: 6px;
    cursor: pointer;
    transition: all 150ms ease-out;
}}

.contact-item:hover {{
    border-color: rgba(212, 175, 55, 0.3);
    background: rgba(212, 175, 55, 0.05);
}}

.contact-avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(31, 189, 234, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: monospace;
    font-size: 14px;
    color: {BLUE_DOMINANT};
    margin-right: 12px;
}}

.contact-info {{
    flex: 1;
}}

.contact-name {{
    color: #e8e8e8;
    font-size: 12px;
    font-weight: 500;
}}

.contact-status {{
    font-family: monospace;
    font-size: 9px;
    color: #666;
    margin-top: 2px;
}}

.contact-status.online {{
    color: #22c55e;
}}

.contact-status.offline {{
    color: #666;
}}

.status-dot {{
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    margin-right: 4px;
}}

.status-dot.online {{
    background: #22c55e;
}}

.status-dot.offline {{
    background: #666;
}}

.message-list {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.message-item {{
    padding: 12px;
    background: rgba(18, 18, 20, 0.9);
    border: 1px solid rgba(31, 189, 234, 0.2);
    border-radius: 6px;
}}

.message-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}}

.message-sender {{
    color: {GOLD_METALLIC};
    font-family: monospace;
    font-size: 10px;
}}

.message-time {{
    color: #666;
    font-family: monospace;
    font-size: 9px;
}}

.message-content {{
    color: #e8e8e8;
    font-size: 11px;
    line-height: 1.4;
}}

.network-stats {{
    padding: 16px;
    background: rgba(18, 18, 20, 0.9);
    border: 1px solid rgba(31, 189, 234, 0.2);
    border-radius: 6px;
}}

.stat-row {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}}

.stat-label {{
    color: {GOLD_DARK};
    font-family: monospace;
    font-size: 10px;
}}

.stat-value {{
    color: #e8e8e8;
    font-family: monospace;
    font-size: 10px;
}}

.comms-footer {{
    padding: 12px 16px;
    border-top: 1px solid rgba(31, 189, 234, 0.2);
}}

.compose-area {{
    display: flex;
    gap: 8px;
}}

.compose-input {{
    flex: 1;
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.3);
    color: #e8e8e8;
    padding: 8px 12px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 11px;
}}

.compose-input:focus {{
    border-color: {GOLD_METALLIC};
    outline: none;
}}

.send-btn {{
    background: rgba(212, 175, 55, 0.1);
    border: 1px solid {GOLD_METALLIC};
    color: {GOLD_METALLIC};
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-family: monospace;
    font-size: 10px;
    transition: all 150ms ease-out;
}}

.send-btn:hover {{
    background: rgba(212, 175, 55, 0.2);
}}

.empty-state {{
    text-align: center;
    padding: 40px;
    color: #666;
    font-style: italic;
}}
</style>
"""


class CommsPanel:
    """Comms panel for Marimo - P2P messaging and contacts."""

    def __init__(self, project_root: str):
        self.project_root = project_root
        self._is_visible = False
        self._active_tab = "contacts"  # contacts, messages, network
        self._session_id: Optional[str] = None
        self._selected_contact: Optional[str] = None

        # Initialize session if adapter available
        if comms_adapter:
            result = comms_adapter.create_session()
            if result.get("success"):
                self._session_id = result["session_id"]

    def toggle_visibility(self) -> None:
        """Toggle panel visibility."""
        self._is_visible = not self._is_visible

    def set_visible(self, visible: bool) -> None:
        """Set panel visibility."""
        self._is_visible = visible

    def is_visible(self) -> bool:
        """Check if panel is visible."""
        return self._is_visible

    def set_tab(self, tab: str) -> None:
        """Set active tab."""
        if tab in ["contacts", "messages", "network"]:
            self._active_tab = tab

    def select_contact(self, contact_id: str) -> None:
        """Select a contact for messaging."""
        self._selected_contact = contact_id

    def get_contacts(self) -> List[Dict[str, Any]]:
        """Get list of contacts."""
        if not comms_adapter or not self._session_id:
            return self._get_mock_contacts()

        result = comms_adapter.list_contacts(self._session_id)
        if result.get("success"):
            return result.get("contacts", [])
        return []

    def get_messages(self) -> List[Dict[str, Any]]:
        """Get recent messages."""
        if not comms_adapter or not self._session_id:
            return self._get_mock_messages()

        result = comms_adapter.get_messages(self._session_id, limit=20)
        if result.get("success"):
            return result.get("messages", [])
        return []

    def get_network_stats(self) -> Dict[str, Any]:
        """Get network statistics."""
        if not comms_adapter or not self._session_id:
            return self._get_mock_stats()

        result = comms_adapter.get_network_stats(self._session_id)
        if result.get("success"):
            return result
        return self._get_mock_stats()

    def _get_mock_contacts(self) -> List[Dict[str, Any]]:
        """Return mock contacts for display."""
        return [
            {
                "contact_id": "c1",
                "name": "Alice Developer",
                "peer_id": "peer_alice",
                "status": "online",
            },
            {
                "contact_id": "c2",
                "name": "Bob Engineer",
                "peer_id": "peer_bob",
                "status": "offline",
            },
            {
                "contact_id": "c3",
                "name": "Carol Designer",
                "peer_id": "peer_carol",
                "status": "online",
            },
        ]

    def _get_mock_messages(self) -> List[Dict[str, Any]]:
        """Return mock messages for display."""
        now = datetime.now()
        return [
            {
                "message_id": "m1",
                "sender": "Alice",
                "content": "Just pushed the calendar component. Ready for review!",
                "sent_at": int((now.timestamp() - 3600) * 1000),
            },
            {
                "message_id": "m2",
                "sender": "Bob",
                "content": "Great work on the P2P integration.",
                "sent_at": int((now.timestamp() - 1800) * 1000),
            },
            {
                "message_id": "m3",
                "sender": "You",
                "content": "Thanks! Still wiring up the maestro buttons.",
                "sent_at": int((now.timestamp() - 600) * 1000),
            },
        ]

    def _get_mock_stats(self) -> Dict[str, Any]:
        """Return mock network stats."""
        return {
            "connected_peers": 2,
            "discovered_peers": 5,
            "bytes_sent": 12500,
            "bytes_received": 8700,
            "messages_sent": 15,
            "messages_received": 12,
        }

    def render(self) -> Any:
        """Render the comms panel."""
        if not self._is_visible:
            return mo.md("")

        panel_html = f"""
        <div class="comms-panel-overlay">
            <div class="comms-panel-header">
                <span class="comms-panel-title">COMMS</span>
                <button class="comms-panel-close" onclick="window.location.reload()">X</button>
            </div>
            {self._build_tabs()}
            <div class="comms-body">
                {self._build_content()}
            </div>
            {self._build_footer()}
        </div>
        """

        return mo.Html(COMMS_PANEL_CSS + panel_html)

    def _build_tabs(self) -> str:
        """Build tab bar."""
        tabs = [
            ("contacts", "CONTACTS"),
            ("messages", "MESSAGES"),
            ("network", "NETWORK"),
        ]

        tab_html = ""
        for tab_id, label in tabs:
            active = "active" if self._active_tab == tab_id else ""
            tab_html += f'<button class="comms-tab {active}" data-tab="{tab_id}">{label}</button>'

        return f'<div class="comms-tabs">{tab_html}</div>'

    def _build_content(self) -> str:
        """Build content based on active tab."""
        if self._active_tab == "contacts":
            return self._build_contacts()
        elif self._active_tab == "messages":
            return self._build_messages()
        elif self._active_tab == "network":
            return self._build_network_stats()
        return ""

    def _build_contacts(self) -> str:
        """Build contacts list."""
        contacts = self.get_contacts()

        if not contacts:
            return '<div class="empty-state">No contacts yet</div>'

        items = ""
        for contact in contacts:
            initials = "".join(w[0].upper() for w in contact["name"].split()[:2])
            status = contact.get("status", "offline")

            items += f"""
            <div class="contact-item" data-contact="{contact['contact_id']}">
                <div class="contact-avatar">{initials}</div>
                <div class="contact-info">
                    <div class="contact-name">{contact['name']}</div>
                    <div class="contact-status {status}">
                        <span class="status-dot {status}"></span>
                        {status.upper()}
                    </div>
                </div>
            </div>
            """

        return f'<div class="contact-list">{items}</div>'

    def _build_messages(self) -> str:
        """Build messages list."""
        messages = self.get_messages()

        if not messages:
            return '<div class="empty-state">No messages yet</div>'

        items = ""
        for msg in messages:
            time_ms = msg.get("sent_at", 0)
            time_str = datetime.fromtimestamp(time_ms / 1000).strftime("%H:%M")
            sender = msg.get("sender", "Unknown")

            items += f"""
            <div class="message-item">
                <div class="message-header">
                    <span class="message-sender">{sender}</span>
                    <span class="message-time">{time_str}</span>
                </div>
                <div class="message-content">{msg.get('content', '')}</div>
            </div>
            """

        return f'<div class="message-list">{items}</div>'

    def _build_network_stats(self) -> str:
        """Build network statistics view."""
        stats = self.get_network_stats()

        def format_bytes(b: int) -> str:
            if b < 1024:
                return f"{b} B"
            elif b < 1024 * 1024:
                return f"{b / 1024:.1f} KB"
            else:
                return f"{b / (1024 * 1024):.1f} MB"

        return f"""
        <div class="network-stats">
            <div class="stat-row">
                <span class="stat-label">CONNECTED PEERS</span>
                <span class="stat-value">{stats.get('connected_peers', 0)}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">DISCOVERED PEERS</span>
                <span class="stat-value">{stats.get('discovered_peers', 0)}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">BYTES SENT</span>
                <span class="stat-value">{format_bytes(stats.get('bytes_sent', 0))}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">BYTES RECEIVED</span>
                <span class="stat-value">{format_bytes(stats.get('bytes_received', 0))}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">MESSAGES SENT</span>
                <span class="stat-value">{stats.get('messages_sent', 0)}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">MESSAGES RECEIVED</span>
                <span class="stat-value">{stats.get('messages_received', 0)}</span>
            </div>
        </div>
        """

    def _build_footer(self) -> str:
        """Build footer with compose area."""
        if self._active_tab != "messages":
            return ""

        return """
        <div class="comms-footer">
            <div class="compose-area">
                <input type="text" class="compose-input" placeholder="Type a message...">
                <button class="send-btn">SEND</button>
            </div>
        </div>
        """
