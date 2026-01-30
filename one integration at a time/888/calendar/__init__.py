"""
calendar - Python adapter for Calendar Rust module.
Provides scheduling, events, and calendar integration.
"""

from .adapter import (
    get_version,
    health_check,
    create_session,
    create_event,
    get_events,
    get_today_events,
    update_event,
    delete_event,
    check_availability,
    suggest_meeting_times,
)

__all__ = [
    "get_version",
    "health_check",
    "create_session",
    "create_event",
    "get_events",
    "get_today_events",
    "update_event",
    "delete_event",
    "check_availability",
    "suggest_meeting_times",
]
