"""
communic8 module for Thunderbird email/communication integration.

This module implements the Thunderbird wrapper following the orchestr8 (Newelle) pattern,
providing complete communication functionality within the Maestro workspace.
"""

from .adapter import *

__all__ = ['get_version', 'health_check', 'create_session', 'send_email', 
           'get_inbox', 'get_folders', 'search_emails', 'get_email_content',
           'mark_as_read', 'mark_as_unread', 'delete_email', 'get_contacts',
           'add_contact', 'get_calendar_events', 'create_calendar_event']
