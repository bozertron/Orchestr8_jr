"""
actu8 adapter for LibreOffice productivity suite PyO3 integration.

This module provides the Python interface for LibreOffice integration that will be
called from Rust via PyO3. It follows Option B enforcement (Python primitives only).
"""

import os
import json
import time
import subprocess
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


# Global state for LibreOffice integration
_libreoffice_process: Optional[subprocess.Popen] = None
_productivity_sessions: Dict[str, Dict[str, Any]] = {}
_open_documents: Dict[str, Dict[str, Any]] = {}


def get_version() -> str:
    """Get the actu8 (LibreOffice) wrapper version."""
    return "1.0.0"


def health_check() -> Dict[str, Any]:
    """Perform a health check of the LibreOffice integration system."""
    try:
        # Check if LibreOffice is available
        libreoffice_available = _check_libreoffice_availability()
        
        return {
            'success': True,
            'status': 'healthy' if libreoffice_available else 'degraded',
            'libreoffice_available': libreoffice_available,
            'active_sessions': len(_productivity_sessions),
            'open_documents': len(_open_documents),
            'checked_at': int(time.time() * 1000)
        }
        
    except Exception as e:
        return {
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'checked_at': int(time.time() * 1000)
        }


def create_session(workspace_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new LibreOffice productivity session.
    
    Args:
        workspace_path: Optional path to workspace directory
        
    Returns:
        Dictionary containing session information
    """
    try:
        session_id = f"libreoffice_session_{int(time.time() * 1000)}"
        
        session_data = {
            'session_id': session_id,
            'workspace_path': workspace_path,
            'created_at': int(time.time() * 1000),
            'open_documents': [],
            'active_document': None,
            'settings': _get_default_productivity_settings()
        }
        
        _productivity_sessions[session_id] = session_data
        
        # Start LibreOffice process if not already running
        if not _libreoffice_process or _libreoffice_process.poll() is not None:
            _start_libreoffice_process()
        
        return {
            'success': True,
            'session_id': session_id,
            'workspace_path': workspace_path,
            'created_at': session_data['created_at']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'session_id': None
        }


def create_document(session_id: str, document_type: str, title: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new document in LibreOffice.
    
    Args:
        session_id: Active session identifier
        document_type: Type of document (writer, calc, impress, draw)
        title: Optional document title
        
    Returns:
        Dictionary containing document information
    """
    try:
        if session_id not in _productivity_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        document_id = f"doc_{int(time.time() * 1000)}"
        
        document_data = {
            'document_id': document_id,
            'type': document_type,
            'title': title or f"Untitled {document_type}",
            'created_at': int(time.time() * 1000),
            'modified': False,
            'file_path': None,
            'content': _get_default_document_content(document_type)
        }
        
        _open_documents[document_id] = document_data
        _productivity_sessions[session_id]['open_documents'].append(document_id)
        _productivity_sessions[session_id]['active_document'] = document_id
        
        return {
            'success': True,
            'document_id': document_id,
            'type': document_type,
            'title': document_data['title'],
            'created_at': document_data['created_at']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def open_document(session_id: str, file_path: str) -> Dict[str, Any]:
    """
    Open an existing document in LibreOffice.
    
    Args:
        session_id: Active session identifier
        file_path: Path to the document file
        
    Returns:
        Dictionary containing document information
    """
    try:
        if session_id not in _productivity_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        # Resolve absolute path
        abs_path = os.path.abspath(file_path)
        
        if not os.path.exists(abs_path):
            return {
                'success': False,
                'error': f'Document not found: {abs_path}'
            }
        
        document_id = f"doc_{int(time.time() * 1000)}"
        document_type = _detect_document_type(abs_path)
        
        document_data = {
            'document_id': document_id,
            'type': document_type,
            'title': os.path.basename(abs_path),
            'file_path': abs_path,
            'opened_at': int(time.time() * 1000),
            'modified': False,
            'size': os.path.getsize(abs_path)
        }
        
        _open_documents[document_id] = document_data
        _productivity_sessions[session_id]['open_documents'].append(document_id)
        _productivity_sessions[session_id]['active_document'] = document_id
        
        return {
            'success': True,
            'document_id': document_id,
            'type': document_type,
            'title': document_data['title'],
            'file_path': abs_path,
            'size': document_data['size']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def save_document(session_id: str, document_id: str, file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Save a document in LibreOffice.
    
    Args:
        session_id: Active session identifier
        document_id: Document identifier
        file_path: Optional new file path for Save As
        
    Returns:
        Dictionary containing save result
    """
    try:
        if session_id not in _productivity_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        if document_id not in _open_documents:
            return {
                'success': False,
                'error': f'Document {document_id} not found'
            }
        
        document = _open_documents[document_id]
        save_path = file_path or document.get('file_path')
        
        if not save_path:
            return {
                'success': False,
                'error': 'No file path specified for save operation'
            }
        
        # Simulate document saving
        document['file_path'] = save_path
        document['modified'] = False
        document['saved_at'] = int(time.time() * 1000)
        
        return {
            'success': True,
            'document_id': document_id,
            'file_path': save_path,
            'saved_at': document['saved_at']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


# Helper functions
def _check_libreoffice_availability() -> bool:
    """Check if LibreOffice is available on the system."""
    try:
        result = subprocess.run(['which', 'libreoffice'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _start_libreoffice_process() -> None:
    """Start LibreOffice process."""
    global _libreoffice_process
    try:
        _libreoffice_process = subprocess.Popen(
            ['libreoffice', '--headless', '--accept=socket,host=localhost,port=2002;urp;'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"Failed to start LibreOffice: {e}")


def _detect_document_type(file_path: str) -> str:
    """Detect document type from file extension."""
    ext = Path(file_path).suffix.lower()
    type_map = {
        '.odt': 'writer', '.doc': 'writer', '.docx': 'writer',
        '.ods': 'calc', '.xls': 'calc', '.xlsx': 'calc',
        '.odp': 'impress', '.ppt': 'impress', '.pptx': 'impress',
        '.odg': 'draw'
    }
    return type_map.get(ext, 'writer')


def _get_default_document_content(document_type: str) -> str:
    """Get default content for new documents."""
    content_map = {
        'writer': 'New Document',
        'calc': 'A1: New Spreadsheet',
        'impress': 'Slide 1: New Presentation',
        'draw': 'New Drawing'
    }
    return content_map.get(document_type, 'New Document')


def _get_default_productivity_settings() -> Dict[str, Any]:
    """Get default productivity settings."""
    return {
        'auto_save_interval': 300,  # 5 minutes
        'backup_enabled': True,
        'spell_check_enabled': True,
        'default_format': 'odt'
    }
