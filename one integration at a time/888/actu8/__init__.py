"""
actu8 module for LibreOffice productivity suite integration.

This module implements the LibreOffice wrapper following the orchestr8 (Newelle) pattern,
providing complete productivity functionality within the Maestro workspace.
"""

from .adapter import *

__all__ = ['get_version', 'health_check', 'create_session', 'create_document', 
           'open_document', 'save_document', 'get_document_content', 'set_document_content',
           'export_document', 'get_document_info', 'close_document', 'list_open_documents',
           'insert_text', 'format_text', 'create_spreadsheet', 'create_presentation']
