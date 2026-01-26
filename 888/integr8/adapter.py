"""
integr8 adapter for Zed code editor PyO3 integration.

This module provides the Python interface for Zed integration that will be
called from Rust via PyO3. It follows Option B enforcement (Python primitives only).
"""

import os
import json
import time
import subprocess
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


# Global state for Zed integration
_zed_process: Optional[subprocess.Popen] = None
_editor_sessions: Dict[str, Dict[str, Any]] = {}
_open_files: Dict[str, Dict[str, Any]] = {}


def get_version() -> str:
    """Get the integr8 (Zed) wrapper version."""
    return "1.0.0"


def health_check() -> Dict[str, Any]:
    """Perform a health check of the Zed integration system."""
    try:
        # Check if Zed is available
        zed_available = _check_zed_availability()
        
        return {
            'success': True,
            'status': 'healthy' if zed_available else 'degraded',
            'zed_available': zed_available,
            'active_sessions': len(_editor_sessions),
            'open_files': len(_open_files),
            'checked_at': int(time.time() * 1000)
        }
        
    except Exception as e:
        return {
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'checked_at': int(time.time() * 1000)
        }


def create_editor_session(workspace_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new Zed editor session.
    
    Args:
        workspace_path: Optional path to workspace directory
        
    Returns:
        Dictionary containing session information
    """
    try:
        session_id = f"zed_session_{int(time.time() * 1000)}"
        
        session_data = {
            'session_id': session_id,
            'workspace_path': workspace_path,
            'created_at': int(time.time() * 1000),
            'open_files': [],
            'active_file': None,
            'settings': _get_default_editor_settings()
        }
        
        _editor_sessions[session_id] = session_data
        
        # Start Zed process if not already running
        if not _zed_process or _zed_process.poll() is not None:
            _start_zed_process(workspace_path)
        
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


def open_file(session_id: str, file_path: str) -> Dict[str, Any]:
    """
    Open a file in the specified editor session.
    
    Args:
        session_id: Editor session identifier
        file_path: Path to file to open
        
    Returns:
        Dictionary containing file information
    """
    try:
        if session_id not in _editor_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        # Resolve absolute path
        abs_path = os.path.abspath(file_path)
        
        if not os.path.exists(abs_path):
            return {
                'success': False,
                'error': f'File not found: {abs_path}'
            }
        
        # Read file content
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_info = {
            'file_path': abs_path,
            'content': content,
            'language': _detect_language(abs_path),
            'size': len(content),
            'modified': False,
            'opened_at': int(time.time() * 1000)
        }
        
        _open_files[abs_path] = file_info
        _editor_sessions[session_id]['open_files'].append(abs_path)
        _editor_sessions[session_id]['active_file'] = abs_path
        
        return {
            'success': True,
            'file_path': abs_path,
            'language': file_info['language'],
            'size': file_info['size'],
            'content': content
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'file_path': file_path
        }


def save_file(session_id: str, file_path: str, content: Optional[str] = None) -> Dict[str, Any]:
    """
    Save a file in the specified editor session.
    
    Args:
        session_id: Editor session identifier
        file_path: Path to file to save
        content: Optional new content (if None, saves current content)
        
    Returns:
        Dictionary indicating success/failure
    """
    try:
        if session_id not in _editor_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        abs_path = os.path.abspath(file_path)
        
        # Use provided content or current content
        if content is not None:
            save_content = content
        elif abs_path in _open_files:
            save_content = _open_files[abs_path]['content']
        else:
            return {
                'success': False,
                'error': f'File not open: {abs_path}'
            }
        
        # Write file
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(save_content)
        
        # Update file info
        if abs_path in _open_files:
            _open_files[abs_path]['content'] = save_content
            _open_files[abs_path]['modified'] = False
            _open_files[abs_path]['saved_at'] = int(time.time() * 1000)
        
        return {
            'success': True,
            'file_path': abs_path,
            'saved_at': int(time.time() * 1000),
            'size': len(save_content)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'file_path': file_path
        }


def get_file_content(file_path: str) -> Dict[str, Any]:
    """Get the current content of an open file."""
    try:
        abs_path = os.path.abspath(file_path)
        
        if abs_path in _open_files:
            file_info = _open_files[abs_path]
            return {
                'success': True,
                'file_path': abs_path,
                'content': file_info['content'],
                'language': file_info['language'],
                'modified': file_info['modified']
            }
        else:
            return {
                'success': False,
                'error': f'File not open: {abs_path}'
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'file_path': file_path
        }


def set_file_content(file_path: str, content: str) -> Dict[str, Any]:
    """Set the content of an open file."""
    try:
        abs_path = os.path.abspath(file_path)
        
        if abs_path in _open_files:
            _open_files[abs_path]['content'] = content
            _open_files[abs_path]['modified'] = True
            _open_files[abs_path]['modified_at'] = int(time.time() * 1000)
            
            return {
                'success': True,
                'file_path': abs_path,
                'modified': True,
                'size': len(content)
            }
        else:
            return {
                'success': False,
                'error': f'File not open: {abs_path}'
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'file_path': file_path
        }


def list_open_files(session_id: str) -> Dict[str, Any]:
    """List all open files in the specified session."""
    try:
        if session_id not in _editor_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        session = _editor_sessions[session_id]
        files = []
        
        for file_path in session['open_files']:
            if file_path in _open_files:
                file_info = _open_files[file_path]
                files.append({
                    'file_path': file_path,
                    'language': file_info['language'],
                    'modified': file_info['modified'],
                    'size': file_info['size']
                })
        
        return {
            'success': True,
            'session_id': session_id,
            'files': files,
            'active_file': session.get('active_file')
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'session_id': session_id
        }


# Helper functions
def _check_zed_availability() -> bool:
    """Check if Zed editor is available on the system."""
    try:
        result = subprocess.run(['zed', '--version'],
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _start_zed_process(workspace_path: Optional[str] = None) -> bool:
    """Start Zed editor process."""
    global _zed_process
    try:
        cmd = ['zed']
        if workspace_path:
            cmd.append(workspace_path)

        _zed_process = subprocess.Popen(cmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        return True
    except Exception:
        return False


def _detect_language(file_path: str) -> str:
    """Detect programming language from file extension."""
    ext = Path(file_path).suffix.lower()
    language_map = {
        '.py': 'python',
        '.rs': 'rust',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.html': 'html',
        '.css': 'css',
        '.json': 'json',
        '.md': 'markdown',
        '.txt': 'text',
        '.yml': 'yaml',
        '.yaml': 'yaml',
        '.toml': 'toml',
        '.xml': 'xml',
        '.sh': 'bash',
        '.go': 'go',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.h': 'c'
    }
    return language_map.get(ext, 'text')


def _get_default_editor_settings() -> Dict[str, Any]:
    """Get default editor settings."""
    return {
        'theme': 'default',
        'font_size': 14,
        'tab_size': 4,
        'word_wrap': True,
        'line_numbers': True,
        'auto_save': True,
        'format_on_save': False
    }
