"""
integr8 module for Zed code editor integration.

This module implements the Zed wrapper following the orchestr8 (Newelle) pattern,
providing complete code editor functionality within the Maestro workspace.
"""

from .adapter import *

__all__ = ['get_version', 'health_check', 'create_editor_session', 'open_file', 
           'save_file', 'get_file_content', 'set_file_content', 'list_open_files',
           'close_file', 'find_in_files', 'replace_in_files', 'get_editor_settings',
           'set_editor_settings', 'get_language_servers', 'start_language_server',
           'stop_language_server', 'get_diagnostics', 'apply_code_action']
