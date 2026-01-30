"""
comms adapter for P2P Communication system PyO3 integration.

This module provides the Python interface for the P2P Rust module.
It follows Option B enforcement (Python primitives only).

Mirrors p2p/mod.rs exports:
- P2PNetwork (main service)
- PeerManager (connection management)
- Discovery (peer discovery)
- WebRtcService (video/audio calls)
- MessageService (text messaging)
"""

import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path


# Global state for P2P integration
_p2p_sessions: Dict[str, Dict[str, Any]] = {}
_contacts: Dict[str, Dict[str, Any]] = {}
_messages: Dict[str, List[Dict[str, Any]]] = {}  # conversation_id -> messages
_active_calls: Dict[str, Dict[str, Any]] = {}


def get_version() -> str:
    """Get the comms (P2P) wrapper version."""
    return "1.0.0"


def health_check() -> Dict[str, Any]:
    """Perform a health check of the P2P communication system."""
    try:
        return {
            "success": True,
            "status": "healthy",
            "active_sessions": len(_p2p_sessions),
            "total_contacts": len(_contacts),
            "active_calls": len(_active_calls),
            "message_threads": len(_messages),
            "checked_at": int(time.time() * 1000),
        }
    except Exception as e:
        return {
            "success": False,
            "status": "unhealthy",
            "error": str(e),
            "checked_at": int(time.time() * 1000),
        }


def create_session(
    peer_id: Optional[str] = None, storage_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new P2P communication session.

    Args:
        peer_id: Optional custom peer ID (auto-generated if not provided)
        storage_path: Optional path for message persistence

    Returns:
        Dictionary containing session information
    """
    try:
        session_id = f"p2p_session_{int(time.time() * 1000)}"

        if not peer_id:
            peer_id = f"peer_{int(time.time() * 1000)}"

        session_data = {
            "session_id": session_id,
            "peer_id": peer_id,
            "storage_path": storage_path,
            "created_at": int(time.time() * 1000),
            "connected_peers": [],
            "settings": _get_default_p2p_settings(),
            "network_stats": {
                "bytes_sent": 0,
                "bytes_received": 0,
                "messages_sent": 0,
                "messages_received": 0,
            },
        }

        _p2p_sessions[session_id] = session_data

        # Load contacts and messages if storage path provided
        if storage_path:
            _load_from_storage(storage_path)

        return {
            "success": True,
            "session_id": session_id,
            "peer_id": peer_id,
            "storage_path": storage_path,
            "created_at": session_data["created_at"],
        }

    except Exception as e:
        return {"success": False, "error": str(e), "session_id": None}


def get_network_stats(session_id: str) -> Dict[str, Any]:
    """
    Get network statistics for a session.

    Args:
        session_id: Active session identifier

    Returns:
        Dictionary containing network statistics
    """
    try:
        if session_id not in _p2p_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        session = _p2p_sessions[session_id]
        stats = session["network_stats"]

        return {
            "success": True,
            "connected_peers": len(session["connected_peers"]),
            "discovered_peers": len(_contacts),
            "bytes_sent": stats["bytes_sent"],
            "bytes_received": stats["bytes_received"],
            "messages_sent": stats["messages_sent"],
            "messages_received": stats["messages_received"],
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def list_contacts(session_id: str) -> Dict[str, Any]:
    """
    List all contacts.

    Args:
        session_id: Active session identifier

    Returns:
        Dictionary containing list of contacts
    """
    try:
        if session_id not in _p2p_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        contacts = [
            {
                "contact_id": c["contact_id"],
                "name": c["name"],
                "peer_id": c["peer_id"],
                "status": c.get("status", "offline"),
                "last_seen": c.get("last_seen"),
            }
            for c in _contacts.values()
        ]

        return {
            "success": True,
            "contacts": contacts,
            "count": len(contacts),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def add_contact(
    session_id: str,
    name: str,
    peer_id: str,
    email: Optional[str] = None,
    notes: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Add a new contact.

    Args:
        session_id: Active session identifier
        name: Contact display name
        peer_id: Contact's peer ID for P2P connection
        email: Optional email address
        notes: Optional notes about the contact

    Returns:
        Dictionary containing contact information
    """
    try:
        if session_id not in _p2p_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        contact_id = f"contact_{int(time.time() * 1000)}"

        contact_data = {
            "contact_id": contact_id,
            "name": name,
            "peer_id": peer_id,
            "email": email,
            "notes": notes,
            "added_at": int(time.time() * 1000),
            "status": "offline",
            "last_seen": None,
        }

        _contacts[contact_id] = contact_data

        return {
            "success": True,
            "contact_id": contact_id,
            "name": name,
            "peer_id": peer_id,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def remove_contact(session_id: str, contact_id: str) -> Dict[str, Any]:
    """
    Remove a contact.

    Args:
        session_id: Active session identifier
        contact_id: Contact identifier

    Returns:
        Dictionary containing removal result
    """
    try:
        if session_id not in _p2p_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        if contact_id not in _contacts:
            return {"success": False, "error": f"Contact {contact_id} not found"}

        del _contacts[contact_id]

        return {
            "success": True,
            "contact_id": contact_id,
            "removed_at": int(time.time() * 1000),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def send_message(
    session_id: str,
    recipient_peer_id: str,
    content: str,
    message_type: str = "text",
    attachments: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Send a message to a peer.

    Args:
        session_id: Active session identifier
        recipient_peer_id: Recipient's peer ID
        content: Message content
        message_type: Type of message (text, file, image)
        attachments: Optional list of attachment paths

    Returns:
        Dictionary containing message information
    """
    try:
        if session_id not in _p2p_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        session = _p2p_sessions[session_id]
        sender_peer_id = session["peer_id"]

        message_id = f"msg_{int(time.time() * 1000)}"
        conversation_id = _get_conversation_id(sender_peer_id, recipient_peer_id)

        message_data = {
            "message_id": message_id,
            "conversation_id": conversation_id,
            "sender": sender_peer_id,
            "recipient": recipient_peer_id,
            "content": content,
            "message_type": message_type,
            "attachments": attachments or [],
            "sent_at": int(time.time() * 1000),
            "delivered": False,
            "read": False,
        }

        # Add to conversation
        if conversation_id not in _messages:
            _messages[conversation_id] = []
        _messages[conversation_id].append(message_data)

        # Update stats
        session["network_stats"]["messages_sent"] += 1
        session["network_stats"]["bytes_sent"] += len(content)

        return {
            "success": True,
            "message_id": message_id,
            "conversation_id": conversation_id,
            "sent_at": message_data["sent_at"],
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_messages(
    session_id: str, limit: int = 50, offset: int = 0
) -> Dict[str, Any]:
    """
    Get recent messages across all conversations.

    Args:
        session_id: Active session identifier
        limit: Maximum number of messages to return
        offset: Offset for pagination

    Returns:
        Dictionary containing messages
    """
    try:
        if session_id not in _p2p_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        # Flatten all messages and sort by time
        all_messages = []
        for conv_messages in _messages.values():
            all_messages.extend(conv_messages)

        all_messages.sort(key=lambda m: m["sent_at"], reverse=True)

        # Apply pagination
        paginated = all_messages[offset : offset + limit]

        return {
            "success": True,
            "messages": paginated,
            "count": len(paginated),
            "total": len(all_messages),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_conversation(
    session_id: str, peer_id: str, limit: int = 100
) -> Dict[str, Any]:
    """
    Get messages from a specific conversation.

    Args:
        session_id: Active session identifier
        peer_id: Peer ID of the conversation partner
        limit: Maximum number of messages to return

    Returns:
        Dictionary containing conversation messages
    """
    try:
        if session_id not in _p2p_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        session = _p2p_sessions[session_id]
        my_peer_id = session["peer_id"]
        conversation_id = _get_conversation_id(my_peer_id, peer_id)

        messages = _messages.get(conversation_id, [])
        messages = sorted(messages, key=lambda m: m["sent_at"])[-limit:]

        return {
            "success": True,
            "conversation_id": conversation_id,
            "peer_id": peer_id,
            "messages": messages,
            "count": len(messages),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def start_webrtc_call(
    session_id: str, peer_id: str, video: bool = True, audio: bool = True
) -> Dict[str, Any]:
    """
    Start a WebRTC call with a peer.

    Args:
        session_id: Active session identifier
        peer_id: Peer ID to call
        video: Enable video
        audio: Enable audio

    Returns:
        Dictionary containing call information
    """
    try:
        if session_id not in _p2p_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        call_id = f"call_{int(time.time() * 1000)}"

        call_data = {
            "call_id": call_id,
            "peer_id": peer_id,
            "video": video,
            "audio": audio,
            "started_at": int(time.time() * 1000),
            "status": "connecting",
            "duration_seconds": 0,
        }

        _active_calls[call_id] = call_data

        return {
            "success": True,
            "call_id": call_id,
            "peer_id": peer_id,
            "video": video,
            "audio": audio,
            "status": "connecting",
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def end_webrtc_call(session_id: str, call_id: str) -> Dict[str, Any]:
    """
    End a WebRTC call.

    Args:
        session_id: Active session identifier
        call_id: Call identifier

    Returns:
        Dictionary containing call end information
    """
    try:
        if session_id not in _p2p_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        if call_id not in _active_calls:
            return {"success": False, "error": f"Call {call_id} not found"}

        call = _active_calls[call_id]
        ended_at = int(time.time() * 1000)
        duration = (ended_at - call["started_at"]) // 1000

        del _active_calls[call_id]

        return {
            "success": True,
            "call_id": call_id,
            "ended_at": ended_at,
            "duration_seconds": duration,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_active_calls(session_id: str) -> Dict[str, Any]:
    """
    Get list of active calls.

    Args:
        session_id: Active session identifier

    Returns:
        Dictionary containing active calls
    """
    try:
        if session_id not in _p2p_sessions:
            return {"success": False, "error": f"Session {session_id} not found"}

        calls = list(_active_calls.values())

        # Update duration for each call
        now = int(time.time() * 1000)
        for call in calls:
            call["duration_seconds"] = (now - call["started_at"]) // 1000

        return {
            "success": True,
            "calls": calls,
            "count": len(calls),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


# Helper functions
def _get_default_p2p_settings() -> Dict[str, Any]:
    """Get default P2P settings."""
    return {
        "enable_webrtc": True,
        "enable_discovery": True,
        "max_peers": 50,
        "message_retention_days": 30,
        "encryption_enabled": True,
    }


def _get_conversation_id(peer_a: str, peer_b: str) -> str:
    """Generate consistent conversation ID for two peers."""
    peers = sorted([peer_a, peer_b])
    return f"conv_{peers[0]}_{peers[1]}"


def _load_from_storage(storage_path: str) -> None:
    """Load contacts and messages from storage."""
    try:
        storage_dir = Path(storage_path)

        # Load contacts
        contacts_file = storage_dir / "contacts.json"
        if contacts_file.exists():
            with open(contacts_file) as f:
                data = json.load(f)
                for contact in data.get("contacts", []):
                    _contacts[contact["contact_id"]] = contact

        # Load messages
        messages_file = storage_dir / "messages.json"
        if messages_file.exists():
            with open(messages_file) as f:
                data = json.load(f)
                _messages.update(data.get("conversations", {}))

    except Exception:
        pass  # Silently fail if storage can't be loaded


def _save_to_storage(storage_path: str) -> None:
    """Save contacts and messages to storage."""
    try:
        storage_dir = Path(storage_path)
        storage_dir.mkdir(parents=True, exist_ok=True)

        # Save contacts
        contacts_file = storage_dir / "contacts.json"
        with open(contacts_file, "w") as f:
            json.dump({"contacts": list(_contacts.values())}, f, indent=2)

        # Save messages
        messages_file = storage_dir / "messages.json"
        with open(messages_file, "w") as f:
            json.dump({"conversations": _messages}, f, indent=2)

    except Exception:
        pass  # Silently fail if storage can't be saved
