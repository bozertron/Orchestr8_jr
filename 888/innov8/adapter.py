"""
innov8 adapter for Jupyter experimental/innovation platform PyO3 integration.

This module provides the Python interface for Jupyter integration that will be
called from Rust via PyO3. It follows Option B enforcement (Python primitives only).
"""

import os
import json
import time
import subprocess
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


# Global state for Jupyter integration
_jupyter_process: Optional[subprocess.Popen] = None
_innovation_sessions: Dict[str, Dict[str, Any]] = {}
_open_notebooks: Dict[str, Dict[str, Any]] = {}


def get_version() -> str:
    """Get the innov8 (Jupyter) wrapper version."""
    return "1.0.0"


def health_check() -> Dict[str, Any]:
    """Perform a health check of the Jupyter integration system."""
    try:
        # Check if Jupyter is available
        jupyter_available = _check_jupyter_availability()
        
        return {
            'success': True,
            'status': 'healthy' if jupyter_available else 'degraded',
            'jupyter_available': jupyter_available,
            'active_sessions': len(_innovation_sessions),
            'open_notebooks': len(_open_notebooks),
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
    Create a new Jupyter innovation session.
    
    Args:
        workspace_path: Optional path to workspace directory
        
    Returns:
        Dictionary containing session information
    """
    try:
        session_id = f"jupyter_session_{int(time.time() * 1000)}"
        
        session_data = {
            'session_id': session_id,
            'workspace_path': workspace_path,
            'created_at': int(time.time() * 1000),
            'open_notebooks': [],
            'active_notebook': None,
            'kernels': {},
            'settings': _get_default_innovation_settings()
        }
        
        _innovation_sessions[session_id] = session_data
        
        # Start Jupyter process if not already running
        if not _jupyter_process or _jupyter_process.poll() is not None:
            _start_jupyter_process(workspace_path)
        
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


def create_notebook(session_id: str, name: Optional[str] = None, kernel_type: str = 'python3') -> Dict[str, Any]:
    """
    Create a new Jupyter notebook.
    
    Args:
        session_id: Active session identifier
        name: Optional notebook name
        kernel_type: Kernel type (python3, r, julia, etc.)
        
    Returns:
        Dictionary containing notebook information
    """
    try:
        if session_id not in _innovation_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        notebook_id = f"nb_{int(time.time() * 1000)}"
        
        notebook_data = {
            'notebook_id': notebook_id,
            'name': name or f"Untitled-{notebook_id}.ipynb",
            'kernel_type': kernel_type,
            'created_at': int(time.time() * 1000),
            'modified': False,
            'file_path': None,
            'cells': [
                {
                    'cell_id': 'cell_0',
                    'cell_type': 'code',
                    'source': '',
                    'execution_count': None,
                    'outputs': []
                }
            ]
        }
        
        _open_notebooks[notebook_id] = notebook_data
        _innovation_sessions[session_id]['open_notebooks'].append(notebook_id)
        _innovation_sessions[session_id]['active_notebook'] = notebook_id
        
        return {
            'success': True,
            'notebook_id': notebook_id,
            'name': notebook_data['name'],
            'kernel_type': kernel_type,
            'created_at': notebook_data['created_at']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def open_notebook(session_id: str, file_path: str) -> Dict[str, Any]:
    """
    Open an existing Jupyter notebook.
    
    Args:
        session_id: Active session identifier
        file_path: Path to the notebook file
        
    Returns:
        Dictionary containing notebook information
    """
    try:
        if session_id not in _innovation_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        # Resolve absolute path
        abs_path = os.path.abspath(file_path)
        
        if not os.path.exists(abs_path):
            return {
                'success': False,
                'error': f'Notebook not found: {abs_path}'
            }
        
        notebook_id = f"nb_{int(time.time() * 1000)}"
        
        # Load notebook content (simplified)
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                notebook_content = json.load(f)
        except json.JSONDecodeError:
            return {
                'success': False,
                'error': f'Invalid notebook format: {abs_path}'
            }
        
        notebook_data = {
            'notebook_id': notebook_id,
            'name': os.path.basename(abs_path),
            'file_path': abs_path,
            'opened_at': int(time.time() * 1000),
            'modified': False,
            'size': os.path.getsize(abs_path),
            'kernel_type': notebook_content.get('metadata', {}).get('kernelspec', {}).get('name', 'python3'),
            'cells': notebook_content.get('cells', [])
        }
        
        _open_notebooks[notebook_id] = notebook_data
        _innovation_sessions[session_id]['open_notebooks'].append(notebook_id)
        _innovation_sessions[session_id]['active_notebook'] = notebook_id
        
        return {
            'success': True,
            'notebook_id': notebook_id,
            'name': notebook_data['name'],
            'file_path': abs_path,
            'size': notebook_data['size'],
            'kernel_type': notebook_data['kernel_type'],
            'cell_count': len(notebook_data['cells'])
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def execute_cell(session_id: str, notebook_id: str, cell_id: str) -> Dict[str, Any]:
    """
    Execute a cell in a Jupyter notebook.
    
    Args:
        session_id: Active session identifier
        notebook_id: Notebook identifier
        cell_id: Cell identifier
        
    Returns:
        Dictionary containing execution result
    """
    try:
        if session_id not in _innovation_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        if notebook_id not in _open_notebooks:
            return {
                'success': False,
                'error': f'Notebook {notebook_id} not found'
            }
        
        notebook = _open_notebooks[notebook_id]
        cell = None
        
        for c in notebook['cells']:
            if c.get('cell_id') == cell_id:
                cell = c
                break
        
        if not cell:
            return {
                'success': False,
                'error': f'Cell {cell_id} not found'
            }
        
        # Simulate cell execution
        execution_count = int(time.time() % 1000)
        output = {
            'output_type': 'execute_result',
            'execution_count': execution_count,
            'data': {
                'text/plain': f"Executed: {cell.get('source', '')[:50]}..."
            }
        }
        
        cell['execution_count'] = execution_count
        cell['outputs'] = [output]
        notebook['modified'] = True
        
        return {
            'success': True,
            'notebook_id': notebook_id,
            'cell_id': cell_id,
            'execution_count': execution_count,
            'output': output
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def add_cell(session_id: str, notebook_id: str, cell_type: str = 'code', 
             index: Optional[int] = None) -> Dict[str, Any]:
    """
    Add a new cell to a Jupyter notebook.
    
    Args:
        session_id: Active session identifier
        notebook_id: Notebook identifier
        cell_type: Type of cell (code, markdown, raw)
        index: Optional position to insert cell
        
    Returns:
        Dictionary containing new cell information
    """
    try:
        if session_id not in _innovation_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        if notebook_id not in _open_notebooks:
            return {
                'success': False,
                'error': f'Notebook {notebook_id} not found'
            }
        
        notebook = _open_notebooks[notebook_id]
        cell_id = f"cell_{int(time.time() * 1000)}"
        
        new_cell = {
            'cell_id': cell_id,
            'cell_type': cell_type,
            'source': '',
            'execution_count': None,
            'outputs': []
        }
        
        if index is None:
            notebook['cells'].append(new_cell)
            index = len(notebook['cells']) - 1
        else:
            notebook['cells'].insert(index, new_cell)
        
        notebook['modified'] = True
        
        return {
            'success': True,
            'notebook_id': notebook_id,
            'cell_id': cell_id,
            'cell_type': cell_type,
            'index': index
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


# Helper functions
def _check_jupyter_availability() -> bool:
    """Check if Jupyter is available on the system."""
    try:
        result = subprocess.run(['which', 'jupyter'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _start_jupyter_process(workspace_path: Optional[str] = None) -> None:
    """Start Jupyter process."""
    global _jupyter_process
    try:
        cmd = ['jupyter', 'lab', '--no-browser', '--port=8888']
        if workspace_path:
            cmd.extend(['--notebook-dir', workspace_path])
        
        _jupyter_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"Failed to start Jupyter: {e}")


def _get_default_innovation_settings() -> Dict[str, Any]:
    """Get default innovation settings."""
    return {
        'auto_save_interval': 120,  # 2 minutes
        'kernel_timeout': 60,  # 1 minute
        'max_output_lines': 1000,
        'default_kernel': 'python3'
    }
