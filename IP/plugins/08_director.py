"""
IP/plugins/08_director.py - Director Agent Integration
Orchestr8 v4.0 - AI Director for LLM management

Integrates the Director agent that monitors all deployed Generals (Claude, Big Pickle, etc.),
detects when an LLM is stuck, reallocates work, and escalates to Doctor.
"""

from typing import Any, Dict, List, Optional
import threading
import time
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

PLUGIN_NAME = "Director"
PLUGIN_ORDER = 8

# ============================================================================
# DIRECTOR INTEGRATION CSS
# ============================================================================
DIRECTOR_CSS = """
<style>
.director-panel {
    background: linear-gradient(135deg, #0A0A0B 0%, #121214 100%);
    border-radius: 8px;
    padding: 20px;
    font-family: var(--font-body, 'Orchestr8 CalSans', 'Segoe UI', sans-serif);
}

.director-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(31, 189, 234, 0.2);
}

.director-title {
    color: #D4AF37;
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.05em;
    display: flex;
    align-items: center;
    gap: 12px;
}

.director-status {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    animation: pulse 2s ease-in-out infinite;
}

.director-status.active { background: #22c55e; }
.director-status.idle { background: #f59e0b; }
.director-status.error { background: #ef4444; }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.director-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 16px;
}

.general-card {
    background: rgba(18, 18, 20, 0.9);
    border: 1px solid rgba(31, 189, 234, 0.2);
    border-radius: 8px;
    padding: 16px;
    transition: all 150ms ease-out;
}

.general-card:hover {
    border-color: rgba(212, 175, 55, 0.3);
    background: rgba(212, 175, 55, 0.05);
}

.general-name {
    color: #e8e8e8;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.general-status {
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.general-status.working { background: rgba(34, 197, 94, 0.2); color: #22c55e; }
.general-status.stuck { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
.general-status.idle { background: rgba(107, 114, 128, 0.2); color: #6b7280; }

.general-metrics {
    margin-top: 12px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    color: #999;
    font-size: 11px;
}

.metric-value {
    color: #e8e8e8;
    font-weight: 500;
}

.alert-section {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
}

.alert-header {
    color: #ef4444;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 8px;
}

.alert-item {
    color: #e8e8e8;
    font-size: 11px;
    padding: 4px 0;
    border-bottom: 1px solid rgba(239, 68, 68, 0.1);
}

.alert-item:last-child {
    border-bottom: none;
}

.action-buttons {
    display: flex;
    gap: 8px;
    margin-top: 16px;
    flex-wrap: wrap;
}

.director-btn {
    background: rgba(31, 189, 234, 0.2);
    border: 1px solid rgba(31, 189, 234, 0.3);
    border-radius: 4px;
    color: #1fbdea;
    padding: 8px 16px;
    font-family: inherit;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    cursor: pointer;
    transition: all 150ms ease-out;
}

.director-btn:hover {
    background: rgba(31, 189, 234, 0.3);
    border-color: #D4AF37;
    color: #D4AF37;
}

.director-btn.danger {
    background: rgba(239, 68, 68, 0.2);
    border-color: rgba(239, 68, 68, 0.3);
    color: #ef4444;
}

.director-btn.danger:hover {
    background: rgba(239, 68, 68, 0.3);
    border-color: #ef4444;
}
</style>
"""


class DirectorIntegration:
    """Integration layer for Director agent in Orchestr8"""

    @staticmethod
    def _discover_888_paths(root_hint: Optional[str] = None) -> List[Path]:
        """Discover candidate 888 roots that may host director sources."""
        candidates: List[Path] = []

        # Explicit override wins.
        env_path = os.getenv("ORCHESTR8_888_PATH", "").strip()
        if env_path:
            candidates.append(Path(env_path))

        plugin_file = Path(__file__).resolve()
        repo_root = plugin_file.parents[2]  # .../Orchestr8_jr
        cwd = Path.cwd()

        candidates.extend(
            [
                repo_root / "888",
                cwd / "888",
                repo_root / "one integration at a time" / "888",
                cwd / "one integration at a time" / "888",
            ]
        )

        if root_hint:
            root_path = Path(root_hint).resolve()
            candidates.extend(
                [
                    root_path / "888",
                    root_path.parent / "888",
                    root_path.parent / "one integration at a time" / "888",
                ]
            )

        deduped: List[Path] = []
        seen: set[str] = set()
        for path in candidates:
            key = str(path)
            if key not in seen:
                deduped.append(path)
                seen.add(key)
        return deduped

    @staticmethod
    def _resolve_director_root(root_hint: Optional[str] = None) -> Optional[Path]:
        """Return first 888 root containing director/adapter.py."""
        for root in DirectorIntegration._discover_888_paths(root_hint):
            adapter_py = root / "director" / "adapter.py"
            if adapter_py.is_file():
                return root
        return None

    def __init__(self, root_hint: Optional[str] = None):
        self.director_engine = None
        self.director_adapter = None
        self.import_error = None
        self.director_root = None
        self.monitoring = False
        self.generals = {}
        self.last_check = None
        self.alerts = []

        # Try to import Director from discovered 888 roots.
        try:
            director_root = self._resolve_director_root(root_hint)
            if director_root is None:
                searched = ", ".join(
                    str(p) for p in self._discover_888_paths(root_hint)
                )
                raise ImportError(
                    f"director.adapter source not found. searched: {searched}"
                )

            self.director_root = str(director_root)
            sys.path.insert(0, str(director_root))
            import director.adapter as director_adapter

            self.director_adapter = director_adapter
            get_engine = getattr(director_adapter, "_get_engine", None)
            self.director_engine = (
                get_engine() if callable(get_engine) else director_adapter
            )

            # Backward compatibility:
            # old API expected get_active_generals/detect_stuck_patterns.
            # New adapter exposes health/analytics/context APIs.
            get_generals = getattr(director_adapter, "get_active_generals", None)
            detect_stuck = getattr(director_adapter, "detect_stuck_patterns", None)
            self.get_generals = (
                get_generals if callable(get_generals) else self._adapter_get_generals
            )
            self.detect_stuck = (
                detect_stuck
                if callable(detect_stuck)
                else self._adapter_detect_stuck_patterns
            )

        except ImportError as e:
            self.import_error = str(e)
            self.director_engine = None

    def _adapter_get_generals(self) -> Dict[str, Dict[str, Any]]:
        """Compatibility shim for newer director.adapter API."""
        now = datetime.now().isoformat()
        health: Dict[str, Any] = {}
        analytics: Dict[str, Any] = {}

        if self.director_adapter and hasattr(self.director_adapter, "health_check"):
            try:
                health = self.director_adapter.health_check() or {}
            except Exception:
                health = {}

        if self.director_adapter and hasattr(self.director_adapter, "get_analytics"):
            try:
                analytics = self.director_adapter.get_analytics() or {}
            except Exception:
                analytics = {}

        status = "working"
        if health and not health.get("success", True):
            status = "stuck"
        elif health.get("status") == "unhealthy":
            status = "stuck"

        context_events = health.get("context_events_processed", 0)
        productivity_score = (
            analytics.get("analytics", {})
            .get("productivity", {})
            .get("current_score", 0.0)
        )

        return {
            "director-core": {
                "status": status,
                "last_activity": now,
                "stuck_count": 0,
                "context_events_processed": context_events,
                "productivity_score": productivity_score,
            }
        }

    def _adapter_detect_stuck_patterns(
        self, current_generals: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """Compatibility shim that derives stuck signals from health/analytics."""
        stuck: Dict[str, Dict[str, Any]] = {}
        core = current_generals.get("director-core", {})
        suggestions: List[str] = []

        if core.get("status") == "stuck":
            suggestions.append("Run director.health_check and review adapter errors.")

        productivity_score = core.get("productivity_score", 0.0)
        if isinstance(productivity_score, (int, float)) and productivity_score < 0.25:
            suggestions.append("Low productivity trend detected; suggest context reset.")

        if suggestions:
            stuck["director-core"] = {"suggestions": suggestions}
        return stuck

    def start_monitoring(self):
        """Start background monitoring of generals"""
        if not self.director_engine:
            return False

        self.monitoring = True
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()
        return True

    def stop_monitoring(self):
        """Stop background monitoring"""
        self.monitoring = False

    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring:
            try:
                self._check_generals()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"Director monitoring error: {e}")
                time.sleep(5)

    def _check_generals(self):
        """Check status of all deployed generals"""
        if not self.get_generals:
            return

        try:
            current_generals = self.get_generals()
            stuck_generals = self.detect_stuck(current_generals)

            # Update general status
            for general_id, general_info in current_generals.items():
                if general_id not in self.generals:
                    self.generals[general_id] = {
                        "first_seen": datetime.now().isoformat(),
                        "last_activity": datetime.now().isoformat(),
                        "stuck_count": 0,
                    }

                # Update activity
                self.generals[general_id]["last_activity"] = general_info.get(
                    "last_activity", datetime.now().isoformat()
                )

                # Check if stuck
                if general_id in stuck_generals:
                    self.generals[general_id]["stuck_count"] += 1
                    self.alerts.append(
                        {
                            "timestamp": datetime.now().isoformat(),
                            "general_id": general_id,
                            "type": "stuck",
                            "message": f"General {general_id} appears to be stuck",
                            "suggestions": stuck_generals[general_id].get(
                                "suggestions", []
                            ),
                        }
                    )

            self.last_check = datetime.now().isoformat()

        except Exception as e:
            print(f"Error checking generals: {e}")

    def get_system_status(self) -> Dict:
        """Get overall Director system status"""
        return {
            "director_active": self.monitoring,
            "generals_count": len(self.generals),
            "stuck_generals": len(
                [g for g in self.generals.values() if g.get("stuck_count", 0) > 0]
            ),
            "alerts_count": len(self.alerts),
            "last_check": self.last_check,
        }

    def escalate_to_doctor(self, general_id: str, reason: str) -> bool:
        """Escalate a stuck general to the Doctor"""
        if not self.director_engine:
            return False

        try:
            # Create escalation ticket
            from IP.ticket_manager import TicketManager

            ticket_mgr = TicketManager(".")

            ticket_id = ticket_mgr.create_ticket(
                fiefdom=f"general/{general_id}",
                title=f"ESCALATION: {general_id} Stuck",
                description=f"General {general_id} stuck and requires Doctor intervention.\n\nReason: {reason}",
                errors=[f"General {general_id} stuck: {reason}"],
                warnings=[],
                context={"escalated_from": "director", "priority": "high"},
            )

            # Add note about escalation
            ticket_mgr.add_note(ticket_id, "Director", f"Escalated due to: {reason}")

            # Record escalation
            self.alerts.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "general_id": general_id,
                    "type": "escalation",
                    "message": f"Escalated {general_id} to Doctor",
                    "ticket_id": ticket_id,
                }
            )

            return True

        except Exception as e:
            print(f"Escalation failed: {e}")
            return False

    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Get recent alerts"""
        return sorted(self.alerts, key=lambda x: x["timestamp"], reverse=True)[:limit]


def render(STATE_MANAGERS: Dict) -> Any:
    """
    Render Director Agent panel

    Shows status of all deployed generals, stuck detection, and escalation controls.
    """
    import marimo as mo

    # Get global state
    get_root, _ = STATE_MANAGERS["root"]

    # Initialize Director integration
    director = DirectorIntegration(root_hint=get_root())

    # Local state
    get_monitoring, set_monitoring = mo.state(False)
    get_show_alerts, set_show_alerts = mo.state(False)

    def start_director():
        """Start Director monitoring"""
        if director.start_monitoring():
            set_monitoring(True)
            return mo.md("Director monitoring started")
        else:
            return mo.md("Failed to start Director")

    def stop_director():
        """Stop Director monitoring"""
        director.stop_monitoring()
        set_monitoring(False)
        return mo.md("Director monitoring stopped")

    def render_general_card(general_id: str, general_info: Dict):
        """Render card for a single general"""
        status = general_info.get("status", "idle")
        stuck_count = general_info.get("stuck_count", 0)
        last_activity = general_info.get("last_activity", "Unknown")

        # Determine status class
        if status == "stuck" or stuck_count > 0:
            status_class = "stuck"
            status_text = "STUCK"
        elif status == "working":
            status_class = "working"
            status_text = "WORKING"
        else:
            status_class = "idle"
            status_text = "IDLE"

        return mo.Html(f"""
        <div class="general-card">
            <div class="general-name">
                <span>{general_id}</span>
                <span class="general-status {status_class}">{status_text}</span>
            </div>
            <div class="general-metrics">
                <div class="metric-row">
                    <span>Last Activity:</span>
                    <span class="metric-value">{last_activity[:16]}</span>
                </div>
                <div class="metric-row">
                    <span>Stuck Count:</span>
                    <span class="metric-value">{stuck_count}</span>
                </div>
                <div class="metric-row">
                    <span>Status:</span>
                    <span class="metric-value">{status.upper()}</span>
                </div>
            </div>
        </div>
        """)

    def render_alerts():
        """Render recent alerts"""
        alerts = director.get_recent_alerts(5)

        if not alerts:
            return mo.md("No recent alerts - all systems operating normally")

        alert_html = ""
        for alert in alerts:
            alert_html += f"""
            <div class="alert-item">
                <strong>{alert["timestamp"][:19]}</strong> - {alert["message"]}
            </div>
            """

        return mo.Html(f"""
        <div class="alert-section">
            <div class="alert-header">Recent Alerts</div>
            {alert_html}
        </div>
        """)

    def render_content():
        """Render main content"""
        if director.import_error:
            return mo.vstack(
                [
                    mo.md("### Director Agent"),
                    mo.md(
                        "Director integration is unavailable in this environment."
                    ),
                    mo.md(
                        f"`{director.import_error}`"
                    ),
                    mo.md(
                        "Install/configure the `888/director` package to enable monitoring."
                    ),
                ]
            )

        if not get_monitoring():
            return mo.vstack(
                [
                    mo.md("### Director Agent"),
                    mo.md(
                        "The Director monitors all deployed Generals and detects when they get stuck."
                    ),
                    mo.md("---"),
                    mo.hstack(
                        [
                            mo.ui.button(
                                label="Start Monitoring",
                                on_change=lambda _: start_director(),
                                kind="success",  # Use kind instead of style
                            ),
                            mo.md("*Monitors all active Generals for stuck patterns*"),
                        ],
                        gap="1rem",
                    ),
                ]
            )

        # Get system status
        system_status = director.get_system_status()
        generals_list = director.generals

        return mo.vstack(
            [
                mo.Html(f"""
            <div class="director-panel">
                <div class="director-header">
                    <div class="director-title">
                        <div class="director-status active"></div>
                        <span>Director Agent - Active</span>
                    </div>
                    <div>
                        <div style="color: #999; font-size: 11px;">Generals: {system_status["generals_count"]}</div>
                        <div style="color: #ef4444; font-size: 11px;">Stuck: {system_status["stuck_generals"]}</div>
                    </div>
                </div>
            </div>
            """),
                # General cards
                mo.md("### Deployed Generals"),
                mo.hstack(
                    [
                        render_general_card(gid, info)
                        for gid, info in generals_list.items()
                    ],
                    gap="1rem",
                )
                if generals_list
                else mo.md("*No generals currently deployed*"),
                mo.md("---"),
                # Alerts section
                render_alerts() if get_show_alerts() else mo.md(""),
                # Control buttons
                mo.Html("""
            <div class="action-buttons">
                <button class="director-btn" onclick="window.location.reload()">Refresh Status</button>
                <button class="director-btn" onclick="window.open('/settings', '_blank')">Settings</button>
                <button class="director-btn danger" onclick="window.open('/tickets', '_blank')">Create Ticket</button>
            </div>
            """),
            ]
        )

    return mo.vstack(
        [
            mo.Html(DIRECTOR_CSS),
            mo.md("## Director Agent"),
            mo.md("*Monitors all deployed Generals and detects stuck patterns*"),
            mo.md("---"),
            render_content(),
        ]
    )
