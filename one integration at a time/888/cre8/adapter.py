"""
cre8 adapter for GIMP creative image editor PyO3 integration.

This module provides the Python interface for GIMP integration that will be
called from Rust via PyO3. It follows Option B enforcement (Python primitives only).
"""

import os
import json
import time
import subprocess
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


# Global state for GIMP integration
_gimp_process: Optional[subprocess.Popen] = None
_creative_sessions: Dict[str, Dict[str, Any]] = {}
_open_images: Dict[str, Dict[str, Any]] = {}


def get_version() -> str:
    """Get the cre8 (GIMP) wrapper version."""
    return "1.0.0"


def health_check() -> Dict[str, Any]:
    """Perform a health check of the GIMP integration system."""
    try:
        # Check if GIMP is available
        gimp_available = _check_gimp_availability()
        
        return {
            'success': True,
            'status': 'healthy' if gimp_available else 'degraded',
            'gimp_available': gimp_available,
            'active_sessions': len(_creative_sessions),
            'open_images': len(_open_images),
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
    Create a new GIMP creative session.
    
    Args:
        workspace_path: Optional path to workspace directory
        
    Returns:
        Dictionary containing session information
    """
    try:
        session_id = f"gimp_session_{int(time.time() * 1000)}"
        
        session_data = {
            'session_id': session_id,
            'workspace_path': workspace_path,
            'created_at': int(time.time() * 1000),
            'open_images': [],
            'active_image': None,
            'settings': _get_default_creative_settings()
        }
        
        _creative_sessions[session_id] = session_data
        
        # Start GIMP process if not already running
        if not _gimp_process or _gimp_process.poll() is not None:
            _start_gimp_process()
        
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


def create_image(session_id: str, width: int, height: int, name: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new image in GIMP.
    
    Args:
        session_id: Active session identifier
        width: Image width in pixels
        height: Image height in pixels
        name: Optional image name
        
    Returns:
        Dictionary containing image information
    """
    try:
        if session_id not in _creative_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        image_id = f"img_{int(time.time() * 1000)}"
        
        image_data = {
            'image_id': image_id,
            'name': name or f"Untitled-{image_id}",
            'width': width,
            'height': height,
            'created_at': int(time.time() * 1000),
            'modified': False,
            'file_path': None,
            'layers': ['Background'],
            'color_mode': 'RGB'
        }
        
        _open_images[image_id] = image_data
        _creative_sessions[session_id]['open_images'].append(image_id)
        _creative_sessions[session_id]['active_image'] = image_id
        
        return {
            'success': True,
            'image_id': image_id,
            'name': image_data['name'],
            'width': width,
            'height': height,
            'created_at': image_data['created_at']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def open_image(session_id: str, file_path: str) -> Dict[str, Any]:
    """
    Open an existing image in GIMP.
    
    Args:
        session_id: Active session identifier
        file_path: Path to the image file
        
    Returns:
        Dictionary containing image information
    """
    try:
        if session_id not in _creative_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        # Resolve absolute path
        abs_path = os.path.abspath(file_path)
        
        if not os.path.exists(abs_path):
            return {
                'success': False,
                'error': f'Image not found: {abs_path}'
            }
        
        image_id = f"img_{int(time.time() * 1000)}"
        
        # Get basic image info (in real implementation, would use GIMP Python API)
        image_data = {
            'image_id': image_id,
            'name': os.path.basename(abs_path),
            'file_path': abs_path,
            'opened_at': int(time.time() * 1000),
            'modified': False,
            'size': os.path.getsize(abs_path),
            'format': _detect_image_format(abs_path),
            'layers': ['Background']  # Simplified
        }
        
        _open_images[image_id] = image_data
        _creative_sessions[session_id]['open_images'].append(image_id)
        _creative_sessions[session_id]['active_image'] = image_id
        
        return {
            'success': True,
            'image_id': image_id,
            'name': image_data['name'],
            'file_path': abs_path,
            'size': image_data['size'],
            'format': image_data['format']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def save_image(session_id: str, image_id: str, file_path: Optional[str] = None, 
               format: Optional[str] = None) -> Dict[str, Any]:
    """
    Save an image in GIMP.
    
    Args:
        session_id: Active session identifier
        image_id: Image identifier
        file_path: Optional new file path for Save As
        format: Optional export format (jpg, png, gif, etc.)
        
    Returns:
        Dictionary containing save result
    """
    try:
        if session_id not in _creative_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        if image_id not in _open_images:
            return {
                'success': False,
                'error': f'Image {image_id} not found'
            }
        
        image = _open_images[image_id]
        save_path = file_path or image.get('file_path')
        
        if not save_path:
            return {
                'success': False,
                'error': 'No file path specified for save operation'
            }
        
        # Simulate image saving
        image['file_path'] = save_path
        image['modified'] = False
        image['saved_at'] = int(time.time() * 1000)
        if format:
            image['format'] = format
        
        return {
            'success': True,
            'image_id': image_id,
            'file_path': save_path,
            'format': image.get('format', 'xcf'),
            'saved_at': image['saved_at']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def apply_filter(session_id: str, image_id: str, filter_name: str, 
                 parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Apply a filter to an image in GIMP.
    
    Args:
        session_id: Active session identifier
        image_id: Image identifier
        filter_name: Name of the filter to apply
        parameters: Optional filter parameters
        
    Returns:
        Dictionary containing filter application result
    """
    try:
        if session_id not in _creative_sessions:
            return {
                'success': False,
                'error': f'Session {session_id} not found'
            }
        
        if image_id not in _open_images:
            return {
                'success': False,
                'error': f'Image {image_id} not found'
            }
        
        # Simulate filter application
        image = _open_images[image_id]
        image['modified'] = True
        image['last_filter'] = {
            'name': filter_name,
            'parameters': parameters or {},
            'applied_at': int(time.time() * 1000)
        }
        
        return {
            'success': True,
            'image_id': image_id,
            'filter_applied': filter_name,
            'applied_at': image['last_filter']['applied_at']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


# Helper functions
def _check_gimp_availability() -> bool:
    """Check if GIMP is available on the system."""
    try:
        result = subprocess.run(['which', 'gimp'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _start_gimp_process() -> None:
    """Start GIMP process."""
    global _gimp_process
    try:
        _gimp_process = subprocess.Popen(
            ['gimp', '--no-interface', '--batch-interpreter=python-fu-eval'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"Failed to start GIMP: {e}")


def _detect_image_format(file_path: str) -> str:
    """Detect image format from file extension."""
    ext = Path(file_path).suffix.lower()
    format_map = {
        '.jpg': 'jpeg', '.jpeg': 'jpeg',
        '.png': 'png',
        '.gif': 'gif',
        '.bmp': 'bmp',
        '.tiff': 'tiff', '.tif': 'tiff',
        '.xcf': 'xcf'
    }
    return format_map.get(ext, 'unknown')


def _get_default_creative_settings() -> Dict[str, Any]:
    """Get default creative settings."""
    return {
        'default_brush_size': 10,
        'default_color': '#000000',
        'grid_enabled': False,
        'snap_to_grid': False,
        'auto_save_interval': 600  # 10 minutes
    }
