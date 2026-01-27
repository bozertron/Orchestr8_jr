# IP/plugins/components/calendar_panel.py
"""
Calendar panel for Marimo.
Provides calendar view and event management within maestro.
"""
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import marimo as mo

# Import calendar adapter using importlib to avoid conflict with built-in calendar
import importlib.util
from pathlib import Path

calendar_adapter = None
try:
    _adapter_path = Path(__file__).parent.parent.parent.parent / "888" / "calendar" / "adapter.py"
    if _adapter_path.exists():
        spec = importlib.util.spec_from_file_location("calendar_adapter", _adapter_path)
        if spec and spec.loader:
            calendar_adapter = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(calendar_adapter)
except Exception:
    calendar_adapter = None

# Import Maestro colors for consistency
BLUE_DOMINANT = "#1fbdea"
GOLD_METALLIC = "#D4AF37"
GOLD_DARK = "#B8860B"
GOLD_SAFFRON = "#F4C430"
BG_ELEVATED = "#121214"
PURPLE_COMBAT = "#9D4EDD"

# Calendar Panel CSS
CALENDAR_PANEL_CSS = f"""
<style>
.calendar-panel-overlay {{
    position: fixed;
    top: 0;
    right: 0;
    width: 450px;
    height: 100vh;
    background: {BG_ELEVATED};
    border-left: 1px solid rgba(31, 189, 234, 0.3);
    z-index: 1000;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.calendar-panel-header {{
    padding: 16px;
    border-bottom: 1px solid rgba(31, 189, 234, 0.2);
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.calendar-panel-title {{
    color: {GOLD_METALLIC};
    font-family: monospace;
    font-size: 12px;
    letter-spacing: 0.1em;
}}

.calendar-panel-close {{
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.3);
    color: {BLUE_DOMINANT};
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
    font-family: monospace;
    font-size: 10px;
}}

.calendar-panel-close:hover {{
    color: {GOLD_METALLIC};
    border-color: {GOLD_METALLIC};
}}

.calendar-nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(31, 189, 234, 0.1);
}}

.calendar-month {{
    color: {GOLD_METALLIC};
    font-family: monospace;
    font-size: 14px;
    letter-spacing: 0.05em;
}}

.calendar-nav-btn {{
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.2);
    color: {BLUE_DOMINANT};
    padding: 4px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-family: monospace;
    font-size: 12px;
}}

.calendar-nav-btn:hover {{
    color: {GOLD_METALLIC};
    border-color: {GOLD_METALLIC};
}}

.calendar-grid {{
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 1px;
    padding: 8px 16px;
    background: rgba(31, 189, 234, 0.05);
}}

.calendar-day-header {{
    text-align: center;
    padding: 8px 0;
    font-family: monospace;
    font-size: 9px;
    color: {GOLD_DARK};
    letter-spacing: 0.1em;
}}

.calendar-day {{
    aspect-ratio: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding: 4px;
    background: rgba(18, 18, 20, 0.8);
    cursor: pointer;
    transition: all 150ms ease-out;
}}

.calendar-day:hover {{
    background: rgba(212, 175, 55, 0.1);
}}

.calendar-day.today {{
    border: 1px solid {GOLD_METALLIC};
}}

.calendar-day.selected {{
    background: rgba(212, 175, 55, 0.2);
}}

.calendar-day.other-month {{
    opacity: 0.3;
}}

.calendar-day-number {{
    font-family: monospace;
    font-size: 11px;
    color: #e8e8e8;
}}

.calendar-day.today .calendar-day-number {{
    color: {GOLD_METALLIC};
    font-weight: bold;
}}

.calendar-day-events {{
    display: flex;
    gap: 2px;
    margin-top: 2px;
}}

.event-dot {{
    width: 4px;
    height: 4px;
    border-radius: 50%;
}}

.event-dot.meeting {{
    background: {BLUE_DOMINANT};
}}

.event-dot.deadline {{
    background: #ef4444;
}}

.event-dot.task {{
    background: {GOLD_SAFFRON};
}}

.event-dot.block {{
    background: {PURPLE_COMBAT};
}}

.calendar-body {{
    flex: 1;
    overflow-y: auto;
    padding: 16px;
}}

.today-section {{
    margin-bottom: 24px;
}}

.section-title {{
    color: {GOLD_METALLIC};
    font-family: monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    margin-bottom: 12px;
    text-transform: uppercase;
}}

.event-list {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.event-item {{
    background: rgba(18, 18, 20, 0.9);
    border: 1px solid rgba(31, 189, 234, 0.2);
    border-radius: 6px;
    padding: 12px;
    cursor: pointer;
    transition: all 150ms ease-out;
}}

.event-item:hover {{
    border-color: rgba(212, 175, 55, 0.3);
    background: rgba(212, 175, 55, 0.05);
}}

.event-item-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
}}

.event-time {{
    font-family: monospace;
    font-size: 10px;
    color: {GOLD_DARK};
}}

.event-type {{
    padding: 2px 6px;
    border-radius: 3px;
    font-family: monospace;
    font-size: 8px;
    text-transform: uppercase;
}}

.event-type.meeting {{
    background: rgba(31, 189, 234, 0.2);
    color: {BLUE_DOMINANT};
}}

.event-type.deadline {{
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
}}

.event-type.task {{
    background: rgba(244, 196, 48, 0.2);
    color: {GOLD_SAFFRON};
}}

.event-type.block {{
    background: rgba(157, 78, 221, 0.2);
    color: {PURPLE_COMBAT};
}}

.event-title {{
    color: #e8e8e8;
    font-size: 12px;
    font-weight: 500;
}}

.event-location {{
    color: #666;
    font-size: 10px;
    margin-top: 4px;
}}

.no-events {{
    color: #666;
    font-style: italic;
    text-align: center;
    padding: 20px;
}}

.calendar-footer {{
    padding: 12px 16px;
    border-top: 1px solid rgba(31, 189, 234, 0.2);
    display: flex;
    justify-content: center;
}}

.add-event-btn {{
    background: rgba(212, 175, 55, 0.1);
    border: 1px solid {GOLD_METALLIC};
    color: {GOLD_METALLIC};
    padding: 8px 24px;
    border-radius: 4px;
    cursor: pointer;
    font-family: monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    transition: all 150ms ease-out;
}}

.add-event-btn:hover {{
    background: rgba(212, 175, 55, 0.2);
}}
</style>
"""


class CalendarPanel:
    """Calendar panel for Marimo."""

    def __init__(self, project_root: str):
        self.project_root = project_root
        self._is_visible = False
        self._selected_date = datetime.now().date()
        self._current_month = datetime.now().replace(day=1)
        self._session_id: Optional[str] = None

        # Initialize session if adapter available
        if calendar_adapter:
            result = calendar_adapter.create_session()
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

    def select_date(self, date: datetime) -> None:
        """Select a date."""
        self._selected_date = date.date()

    def navigate_month(self, offset: int) -> None:
        """Navigate months (offset: -1 for prev, +1 for next)."""
        year = self._current_month.year
        month = self._current_month.month + offset

        if month < 1:
            month = 12
            year -= 1
        elif month > 12:
            month = 1
            year += 1

        self._current_month = datetime(year, month, 1)

    def get_today_events(self) -> List[Dict[str, Any]]:
        """Get events for today."""
        if not calendar_adapter or not self._session_id:
            return self._get_mock_events()

        result = calendar_adapter.get_today_events(self._session_id)
        if result.get("success"):
            return result.get("events", [])
        return []

    def get_month_events(self) -> Dict[int, List[Dict[str, Any]]]:
        """Get events for current month, grouped by day."""
        if not calendar_adapter or not self._session_id:
            return self._get_mock_month_events()

        start = self._current_month
        if self._current_month.month == 12:
            end = datetime(self._current_month.year + 1, 1, 1)
        else:
            end = datetime(self._current_month.year, self._current_month.month + 1, 1)

        result = calendar_adapter.get_events(
            self._session_id,
            start_date=start.isoformat(),
            end_date=end.isoformat(),
        )

        events_by_day: Dict[int, List[Dict[str, Any]]] = {}
        if result.get("success"):
            for event in result.get("events", []):
                event_date = datetime.fromisoformat(event["start_time"])
                day = event_date.day
                if day not in events_by_day:
                    events_by_day[day] = []
                events_by_day[day].append(event)

        return events_by_day

    def _get_mock_events(self) -> List[Dict[str, Any]]:
        """Return mock events for display."""
        now = datetime.now()
        return [
            {
                "event_id": "mock_1",
                "title": "Daily Standup",
                "start_time": now.replace(hour=9, minute=0).isoformat(),
                "end_time": now.replace(hour=9, minute=30).isoformat(),
                "event_type": "meeting",
            },
            {
                "event_id": "mock_2",
                "title": "Code Review",
                "start_time": now.replace(hour=14, minute=0).isoformat(),
                "end_time": now.replace(hour=15, minute=0).isoformat(),
                "event_type": "task",
            },
            {
                "event_id": "mock_3",
                "title": "Sprint Deadline",
                "start_time": now.replace(hour=17, minute=0).isoformat(),
                "end_time": now.replace(hour=17, minute=0).isoformat(),
                "event_type": "deadline",
            },
        ]

    def _get_mock_month_events(self) -> Dict[int, List[Dict[str, Any]]]:
        """Return mock month events for display."""
        today = datetime.now().day
        return {
            today: [{"event_type": "meeting"}],
            today + 2: [{"event_type": "deadline"}],
            today + 5: [{"event_type": "task"}, {"event_type": "meeting"}],
        }

    def render(self) -> Any:
        """Render the calendar panel."""
        if not self._is_visible:
            return mo.md("")

        today_events = self.get_today_events()
        month_events = self.get_month_events()

        panel_html = f"""
        <div class="calendar-panel-overlay">
            <div class="calendar-panel-header">
                <span class="calendar-panel-title">CALENDAR</span>
                <button class="calendar-panel-close" onclick="window.location.reload()">X</button>
            </div>
            {self._build_calendar_nav()}
            {self._build_calendar_grid(month_events)}
            <div class="calendar-body">
                {self._build_today_section(today_events)}
            </div>
            <div class="calendar-footer">
                <button class="add-event-btn">+ ADD EVENT</button>
            </div>
        </div>
        """

        return mo.Html(CALENDAR_PANEL_CSS + panel_html)

    def _build_calendar_nav(self) -> str:
        """Build month navigation."""
        month_name = self._current_month.strftime("%B %Y").upper()
        return f"""
        <div class="calendar-nav">
            <button class="calendar-nav-btn">&lt;</button>
            <span class="calendar-month">{month_name}</span>
            <button class="calendar-nav-btn">&gt;</button>
        </div>
        """

    def _build_calendar_grid(self, month_events: Dict[int, List[Dict[str, Any]]]) -> str:
        """Build calendar grid."""
        today = datetime.now().date()

        # Day headers
        days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        headers = "".join(
            f'<div class="calendar-day-header">{d}</div>' for d in days
        )

        # Calculate grid
        first_day = self._current_month
        start_weekday = first_day.weekday()  # Monday = 0
        # Adjust for Sunday start
        start_weekday = (start_weekday + 1) % 7

        # Get days in month
        if self._current_month.month == 12:
            next_month = datetime(self._current_month.year + 1, 1, 1)
        else:
            next_month = datetime(self._current_month.year, self._current_month.month + 1, 1)
        days_in_month = (next_month - first_day).days

        # Build day cells
        cells = ""

        # Previous month padding
        for _ in range(start_weekday):
            cells += '<div class="calendar-day other-month"><span class="calendar-day-number"></span></div>'

        # Current month days
        for day in range(1, days_in_month + 1):
            current_date = datetime(self._current_month.year, self._current_month.month, day).date()
            is_today = current_date == today
            is_selected = current_date == self._selected_date

            classes = ["calendar-day"]
            if is_today:
                classes.append("today")
            if is_selected:
                classes.append("selected")

            # Event dots
            dots = ""
            if day in month_events:
                for event in month_events[day][:3]:  # Max 3 dots
                    event_type = event.get("event_type", "meeting")
                    dots += f'<span class="event-dot {event_type}"></span>'

            cells += f"""
            <div class="{' '.join(classes)}" data-date="{current_date}">
                <span class="calendar-day-number">{day}</span>
                <div class="calendar-day-events">{dots}</div>
            </div>
            """

        return f"""
        <div class="calendar-grid">
            {headers}
            {cells}
        </div>
        """

    def _build_today_section(self, events: List[Dict[str, Any]]) -> str:
        """Build today's events section."""
        if not events:
            return """
            <div class="today-section">
                <div class="section-title">TODAY</div>
                <div class="no-events">No events scheduled</div>
            </div>
            """

        event_items = ""
        for event in events:
            start_time = datetime.fromisoformat(event["start_time"])
            time_str = start_time.strftime("%H:%M")
            event_type = event.get("event_type", "meeting")
            location = event.get("location", "")

            event_items += f"""
            <div class="event-item">
                <div class="event-item-header">
                    <span class="event-time">{time_str}</span>
                    <span class="event-type {event_type}">{event_type}</span>
                </div>
                <div class="event-title">{event['title']}</div>
                {"<div class='event-location'>" + location + "</div>" if location else ""}
            </div>
            """

        return f"""
        <div class="today-section">
            <div class="section-title">TODAY</div>
            <div class="event-list">{event_items}</div>
        </div>
        """
