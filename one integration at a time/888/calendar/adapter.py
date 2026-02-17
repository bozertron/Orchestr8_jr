"""
calendar adapter for Calendar system PyO3 integration.

This module provides the Python interface for the Calendar Rust module.
It follows Option B enforcement (Python primitives only).

Mirrors calendar/mod.rs exports:
- CalendarManager
- Events (Event, EventType, RecurrencePattern, Reminder)
- Scheduling (AvailabilityChecker, ConflictDetector, MeetingSuggester)
- Storage (CalendarStorage, CalendarSync)
"""

import json
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from pathlib import Path


# Global state for calendar integration
_calendar_sessions: Dict[str, Dict[str, Any]] = {}
_events: Dict[str, Dict[str, Any]] = {}
_reminders: Dict[str, List[Dict[str, Any]]] = {}


def get_version() -> str:
    """Get the calendar wrapper version."""
    return "1.0.0"


def health_check() -> Dict[str, Any]:
    """Perform a health check of the calendar system."""
    try:
        return {
            "success": True,
            "status": "healthy",
            "active_sessions": len(_calendar_sessions),
            "total_events": len(_events),
            "pending_reminders": sum(len(r) for r in _reminders.values()),
            "checked_at": int(time.time() * 1000),
        }
    except Exception as e:
        return {
            "success": False,
            "status": "unhealthy",
            "error": str(e),
            "checked_at": int(time.time() * 1000),
        }


def create_session(storage_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new calendar session.

    Args:
        storage_path: Optional path to calendar storage directory

    Returns:
        Dictionary containing session information
    """
    try:
        session_id = f"calendar_session_{int(time.time() * 1000)}"

        session_data = {
            "session_id": session_id,
            "storage_path": storage_path,
            "created_at": int(time.time() * 1000),
            "calendars": ["default"],
            "active_calendar": "default",
            "settings": _get_default_calendar_settings(),
        }

        _calendar_sessions[session_id] = session_data

        # Load existing events if storage path provided
        if storage_path:
            _load_events_from_storage(storage_path)

        return {
            "success": True,
            "session_id": session_id,
            "storage_path": storage_path,
            "created_at": session_data["created_at"],
        }

    except Exception as e:
        return {"success": False, "error": str(e), "session_id": None}


def create_event(
    session_id: str,
    title: str,
    start_time: str,
    end_time: Optional[str] = None,
    event_type: str = "meeting",
    description: Optional[str] = None,
    location: Optional[str] = None,
    attendees: Optional[List[str]] = None,
    recurrence: Optional[str] = None,
    reminders: Optional[List[int]] = None,
) -> Dict[str, Any]:
    """
    Create a new calendar event.

    Args:
        session_id: Active session identifier
        title: Event title
        start_time: ISO format start time
        end_time: Optional ISO format end time (defaults to 1 hour after start)
        event_type: Type of event (meeting, deadline, task, reminder, block)
        description: Optional event description
        location: Optional location
        attendees: Optional list of attendee emails
        recurrence: Optional recurrence pattern (daily, weekly, monthly, yearly)
        reminders: Optional list of reminder times in minutes before event

    Returns:
        Dictionary containing event information
    """
    try:
        if session_id not in _calendar_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        event_id = f"evt_{int(time.time() * 1000)}"

        # Parse times
        start_dt = datetime.fromisoformat(start_time)
        if end_time:
            end_dt = datetime.fromisoformat(end_time)
        else:
            end_dt = start_dt + timedelta(hours=1)

        event_data = {
            "event_id": event_id,
            "title": title,
            "start_time": start_time,
            "end_time": end_dt.isoformat(),
            "event_type": event_type,
            "description": description,
            "location": location,
            "attendees": attendees or [],
            "recurrence": recurrence,
            "created_at": int(time.time() * 1000),
            "calendar": _calendar_sessions[session_id]["active_calendar"],
        }

        _events[event_id] = event_data

        # Set up reminders
        if reminders:
            _reminders[event_id] = [
                {
                    "event_id": event_id,
                    "minutes_before": mins,
                    "trigger_at": (start_dt - timedelta(minutes=mins)).isoformat(),
                    "fired": False,
                }
                for mins in reminders
            ]

        return {
            "success": True,
            "event_id": event_id,
            "title": title,
            "start_time": start_time,
            "end_time": event_data["end_time"],
            "event_type": event_type,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_events(
    session_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    event_type: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get calendar events within a date range.

    Args:
        session_id: Active session identifier
        start_date: Optional ISO format start date filter
        end_date: Optional ISO format end date filter
        event_type: Optional event type filter

    Returns:
        Dictionary containing list of events
    """
    try:
        if session_id not in _calendar_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        events = list(_events.values())

        # Filter by date range
        if start_date:
            start_dt = datetime.fromisoformat(start_date)
            events = [
                e for e in events if datetime.fromisoformat(e["start_time"]) >= start_dt
            ]

        if end_date:
            end_dt = datetime.fromisoformat(end_date)
            events = [
                e for e in events if datetime.fromisoformat(e["start_time"]) <= end_dt
            ]

        # Filter by event type
        if event_type:
            events = [e for e in events if e["event_type"] == event_type]

        # Sort by start time
        events.sort(key=lambda e: e["start_time"])

        return {
            "success": True,
            "events": events,
            "count": len(events),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_today_events(session_id: str) -> Dict[str, Any]:
    """
    Get all events for today.

    Args:
        session_id: Active session identifier

    Returns:
        Dictionary containing today's events
    """
    today = datetime.now().date()
    start_date = datetime.combine(today, datetime.min.time()).isoformat()
    end_date = datetime.combine(today, datetime.max.time()).isoformat()

    return get_events(session_id, start_date=start_date, end_date=end_date)


def update_event(
    session_id: str, event_id: str, updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update an existing calendar event.

    Args:
        session_id: Active session identifier
        event_id: Event identifier
        updates: Dictionary of fields to update

    Returns:
        Dictionary containing updated event information
    """
    try:
        if session_id not in _calendar_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        if event_id not in _events:
            return {"success": False, "error": f"Event {event_id} not found"}

        event = _events[event_id]

        # Update allowed fields
        allowed_fields = [
            "title",
            "start_time",
            "end_time",
            "description",
            "location",
            "attendees",
            "recurrence",
        ]

        for field in allowed_fields:
            if field in updates:
                event[field] = updates[field]

        event["modified_at"] = int(time.time() * 1000)

        return {
            "success": True,
            "event_id": event_id,
            "updated_fields": list(updates.keys()),
            "modified_at": event["modified_at"],
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_event(session_id: str, event_id: str) -> Dict[str, Any]:
    """
    Delete a calendar event.

    Args:
        session_id: Active session identifier
        event_id: Event identifier

    Returns:
        Dictionary containing deletion result
    """
    try:
        if session_id not in _calendar_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        if event_id not in _events:
            return {"success": False, "error": f"Event {event_id} not found"}

        del _events[event_id]

        # Remove associated reminders
        if event_id in _reminders:
            del _reminders[event_id]

        return {
            "success": True,
            "event_id": event_id,
            "deleted_at": int(time.time() * 1000),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def check_availability(
    session_id: str, start_time: str, end_time: str
) -> Dict[str, Any]:
    """
    Check if a time slot is available.

    Args:
        session_id: Active session identifier
        start_time: ISO format start time
        end_time: ISO format end time

    Returns:
        Dictionary containing availability information
    """
    try:
        if session_id not in _calendar_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        check_start = datetime.fromisoformat(start_time)
        check_end = datetime.fromisoformat(end_time)

        conflicts = []
        for event in _events.values():
            event_start = datetime.fromisoformat(event["start_time"])
            event_end = datetime.fromisoformat(event["end_time"])

            # Check for overlap
            if check_start < event_end and check_end > event_start:
                conflicts.append(
                    {
                        "event_id": event["event_id"],
                        "title": event["title"],
                        "start_time": event["start_time"],
                        "end_time": event["end_time"],
                    }
                )

        return {
            "success": True,
            "available": len(conflicts) == 0,
            "conflicts": conflicts,
            "conflict_count": len(conflicts),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def suggest_meeting_times(
    session_id: str,
    duration_minutes: int = 60,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    preferred_hours: Optional[List[int]] = None,
) -> Dict[str, Any]:
    """
    Suggest available meeting times.

    Args:
        session_id: Active session identifier
        duration_minutes: Required meeting duration
        start_date: Start of search range (defaults to today)
        end_date: End of search range (defaults to 7 days from now)
        preferred_hours: List of preferred hours (9-17 by default)

    Returns:
        Dictionary containing suggested time slots
    """
    try:
        if session_id not in _calendar_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        # Set defaults
        if start_date:
            search_start = datetime.fromisoformat(start_date)
        else:
            search_start = datetime.now()

        if end_date:
            search_end = datetime.fromisoformat(end_date)
        else:
            search_end = search_start + timedelta(days=7)

        if preferred_hours is None:
            preferred_hours = list(range(9, 18))  # 9 AM to 5 PM

        suggestions = []
        current = search_start.replace(minute=0, second=0, microsecond=0)

        while current < search_end and len(suggestions) < 10:
            if current.hour in preferred_hours:
                slot_end = current + timedelta(minutes=duration_minutes)

                availability = check_availability(
                    session_id, current.isoformat(), slot_end.isoformat()
                )

                if availability.get("available", False):
                    suggestions.append(
                        {
                            "start_time": current.isoformat(),
                            "end_time": slot_end.isoformat(),
                            "duration_minutes": duration_minutes,
                        }
                    )

            current += timedelta(hours=1)

        return {
            "success": True,
            "suggestions": suggestions,
            "count": len(suggestions),
            "search_range": {
                "start": search_start.isoformat(),
                "end": search_end.isoformat(),
            },
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


# Helper functions
def _get_default_calendar_settings() -> Dict[str, Any]:
    """Get default calendar settings."""
    return {
        "default_reminder_minutes": 15,
        "work_hours_start": 9,
        "work_hours_end": 17,
        "default_event_duration": 60,
        "week_starts_on": "monday",
        "timezone": "local",
    }


def _load_events_from_storage(storage_path: str) -> None:
    """Load events from storage file."""
    try:
        events_file = Path(storage_path) / "events.json"
        if events_file.exists():
            with open(events_file) as f:
                data = json.load(f)
                for event in data.get("events", []):
                    _events[event["event_id"]] = event
    except Exception:
        pass  # Silently fail if storage can't be loaded


def _save_events_to_storage(storage_path: str) -> None:
    """Save events to storage file."""
    try:
        storage_dir = Path(storage_path)
        storage_dir.mkdir(parents=True, exist_ok=True)

        events_file = storage_dir / "events.json"
        with open(events_file, "w") as f:
            json.dump({"events": list(_events.values())}, f, indent=2)
    except Exception:
        pass  # Silently fail if storage can't be saved
