"""
communic8 adapter for Thunderbird email/communication PyO3 integration.

This module provides the Python interface for Thunderbird integration that will be
called from Rust via PyO3. It follows Option B enforcement (Python primitives only).
"""

import os
import json
import time
import subprocess
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


# Global state for Thunderbird integration
_thunderbird_process: Optional[subprocess.Popen] = None
_communication_sessions: Dict[str, Dict[str, Any]] = {}
_email_cache: Dict[str, Dict[str, Any]] = {}


def get_version() -> str:
    """Get the communic8 (Thunderbird) wrapper version."""
    return "1.0.0"


def health_check() -> Dict[str, Any]:
    """Perform a health check of the Thunderbird integration system."""
    try:
        # Check if Thunderbird is available
        thunderbird_available = _check_thunderbird_availability()
        
        return {
            'success': True,
            'status': 'healthy' if thunderbird_available else 'degraded',
            'thunderbird_available': thunderbird_available,
            'active_sessions': len(_communication_sessions),
            'cached_emails': len(_email_cache),
            'checked_at': int(time.time() * 1000)
        }
        
    except Exception as e:
        return {
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'checked_at': int(time.time() * 1000)
        }


def create_session(profile_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new Thunderbird communication session.
    
    Args:
        profile_path: Optional path to Thunderbird profile directory
        
    Returns:
        Dictionary containing session information
    """
    try:
        session_id = f"thunderbird_session_{int(time.time() * 1000)}"
        
        session_data = {
            'session_id': session_id,
            'profile_path': profile_path,
            'created_at': int(time.time() * 1000),
            'active_folders': [],
            'current_folder': 'INBOX',
            'settings': _get_default_communication_settings()
        }
        
        _communication_sessions[session_id] = session_data
        
        # Start Thunderbird process if not already running
        if not _thunderbird_process or _thunderbird_process.poll() is not None:
            _start_thunderbird_process(profile_path)
        
        return {
            'success': True,
            'session_id': session_id,
            'profile_path': profile_path,
            'created_at': session_data['created_at']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'session_id': None
        }


def send_email(session_id: str, to_address: str, subject: str, body: str, 
               cc: Optional[str] = None, bcc: Optional[str] = None) -> Dict[str, Any]:
    """
    Send an email through Thunderbird.
    
    Args:
        session_id: Active session identifier
        to_address: Recipient email address
        subject: Email subject
        body: Email body content
        cc: Optional CC recipients
        bcc: Optional BCC recipients
        
    Returns:
        Dictionary containing send result
    """
    try:
        if session_id not in _communication_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        # Simulate email sending (in real implementation, would use Thunderbird automation)
        email_id = f"email_{int(time.time() * 1000)}"
        
        email_data = {
            'email_id': email_id,
            'to': to_address,
            'cc': cc,
            'bcc': bcc,
            'subject': subject,
            'body': body,
            'sent_at': int(time.time() * 1000),
            'status': 'sent'
        }
        
        return {
            'success': True,
            'email_id': email_id,
            'sent_at': email_data['sent_at']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_inbox(session_id: str, limit: int = 50) -> Dict[str, Any]:
    """
    Get inbox emails from Thunderbird.
    
    Args:
        session_id: Active session identifier
        limit: Maximum number of emails to retrieve
        
    Returns:
        Dictionary containing inbox emails
    """
    try:
        if session_id not in _communication_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        # Simulate inbox retrieval
        emails = []
        for i in range(min(limit, 10)):  # Mock data
            emails.append({
                'id': f"email_{i}",
                'from': f"sender{i}@example.com",
                'subject': f"Test Email {i}",
                'date': int(time.time() * 1000) - (i * 3600000),  # Hours ago
                'read': i % 3 == 0,
                'size': 1024 + (i * 100)
            })
        
        return {
            'success': True,
            'emails': emails,
            'total_count': len(emails),
            'folder': 'INBOX'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


# Helper functions
def _check_thunderbird_availability() -> bool:
    """Check if Thunderbird is available on the system."""
    try:
        result = subprocess.run(['which', 'thunderbird'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _start_thunderbird_process(profile_path: Optional[str] = None) -> None:
    """Start Thunderbird process."""
    global _thunderbird_process
    try:
        cmd = ['thunderbird']
        if profile_path:
            cmd.extend(['-profile', profile_path])
        
        _thunderbird_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"Failed to start Thunderbird: {e}")


def _get_default_communication_settings() -> Dict[str, Any]:
    """Get default communication settings."""
    return {
        'auto_check_interval': 300,  # 5 minutes
        'show_notifications': True,
        'mark_as_read_delay': 2,  # seconds
        'default_folder': 'INBOX'
    }
