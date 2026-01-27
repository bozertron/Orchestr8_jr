"""
comms - Python adapter for P2P Communication Rust module.
Provides peer-to-peer messaging, WebRTC, and contact management.
"""

from .adapter import (
    get_version,
    health_check,
    create_session,
    get_network_stats,
    list_contacts,
    add_contact,
    remove_contact,
    send_message,
    get_messages,
    get_conversation,
    start_webrtc_call,
    end_webrtc_call,
    get_active_calls,
)

__all__ = [
    "get_version",
    "health_check",
    "create_session",
    "get_network_stats",
    "list_contacts",
    "add_contact",
    "remove_contact",
    "send_message",
    "get_messages",
    "get_conversation",
    "start_webrtc_call",
    "end_webrtc_call",
    "get_active_calls",
]
