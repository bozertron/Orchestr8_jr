"""
Tests for integr8 adapter functionality.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the adapter functions
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from adapter import (
    get_version, health_check, create_editor_session, open_file, save_file,
    get_file_content, set_file_content, list_open_files,
    _check_zed_availability, _detect_language, _get_default_editor_settings
)


class TestIntegr8Adapter:
    """Test suite for integr8 adapter functions."""
    
    def test_get_version(self):
        """Test version retrieval."""
        version = get_version()
        assert isinstance(version, str)
        assert version == "1.0.0"
    
    def test_health_check_success(self):
        """Test health check with successful Zed availability."""
        with patch('adapter._check_zed_availability', return_value=True):
            result = health_check()
            
            assert result['success'] is True
            assert result['status'] == 'healthy'
            assert result['zed_available'] is True
            assert 'checked_at' in result
    
    def test_health_check_degraded(self):
        """Test health check with Zed unavailable."""
        with patch('adapter._check_zed_availability', return_value=False):
            result = health_check()
            
            assert result['success'] is True
            assert result['status'] == 'degraded'
            assert result['zed_available'] is False
    
    def test_health_check_exception(self):
        """Test health check with exception."""
        with patch('adapter._check_zed_availability', side_effect=Exception("Test error")):
            result = health_check()
            
            assert result['success'] is False
            assert result['status'] == 'unhealthy'
            assert 'error' in result
    
    def test_create_editor_session(self):
        """Test editor session creation."""
        with patch('adapter._start_zed_process', return_value=True):
            result = create_editor_session()
            
            assert result['success'] is True
            assert 'session_id' in result
            assert result['session_id'].startswith('zed_session_')
            assert 'created_at' in result
    
    def test_create_editor_session_with_workspace(self):
        """Test editor session creation with workspace path."""
        workspace_path = "/test/workspace"
        with patch('adapter._start_zed_process', return_value=True):
            result = create_editor_session(workspace_path)
            
            assert result['success'] is True
            assert result['workspace_path'] == workspace_path
    
    def test_open_file_success(self):
        """Test successful file opening."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            f.write("print('Hello, World!')")
            temp_file = f.name
        
        try:
            # Create a session first
            with patch('adapter._start_zed_process', return_value=True):
                session_result = create_editor_session()
                session_id = session_result['session_id']
            
            # Open the file
            result = open_file(session_id, temp_file)
            
            assert result['success'] is True
            assert result['file_path'] == os.path.abspath(temp_file)
            assert result['language'] == 'python'
            assert result['content'] == "print('Hello, World!')"
            assert result['size'] == len("print('Hello, World!')")
            
        finally:
            os.unlink(temp_file)
    
    def test_open_file_not_found(self):
        """Test opening non-existent file."""
        with patch('adapter._start_zed_process', return_value=True):
            session_result = create_editor_session()
            session_id = session_result['session_id']
        
        result = open_file(session_id, "/nonexistent/file.txt")
        
        assert result['success'] is False
        assert 'File not found' in result['error']
    
    def test_open_file_invalid_session(self):
        """Test opening file with invalid session."""
        result = open_file("invalid_session", "/some/file.txt")
        
        assert result['success'] is False
        assert 'Session invalid_session not found' in result['error']
    
    def test_save_file_success(self):
        """Test successful file saving."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("original content")
            temp_file = f.name
        
        try:
            # Create session and open file
            with patch('adapter._start_zed_process', return_value=True):
                session_result = create_editor_session()
                session_id = session_result['session_id']
            
            open_file(session_id, temp_file)
            
            # Save with new content
            new_content = "updated content"
            result = save_file(session_id, temp_file, new_content)
            
            assert result['success'] is True
            assert result['file_path'] == os.path.abspath(temp_file)
            assert result['size'] == len(new_content)
            
            # Verify file was actually saved
            with open(temp_file, 'r') as f:
                saved_content = f.read()
            assert saved_content == new_content
            
        finally:
            os.unlink(temp_file)
    
    def test_get_file_content(self):
        """Test getting file content."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.js') as f:
            content = "console.log('test');"
            f.write(content)
            temp_file = f.name
        
        try:
            # Create session and open file
            with patch('adapter._start_zed_process', return_value=True):
                session_result = create_editor_session()
                session_id = session_result['session_id']
            
            open_file(session_id, temp_file)
            
            # Get content
            result = get_file_content(temp_file)
            
            assert result['success'] is True
            assert result['content'] == content
            assert result['language'] == 'javascript'
            assert result['modified'] is False
            
        finally:
            os.unlink(temp_file)
    
    def test_set_file_content(self):
        """Test setting file content."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.rs') as f:
            f.write("fn main() {}")
            temp_file = f.name
        
        try:
            # Create session and open file
            with patch('adapter._start_zed_process', return_value=True):
                session_result = create_editor_session()
                session_id = session_result['session_id']
            
            open_file(session_id, temp_file)
            
            # Set new content
            new_content = "fn main() { println!(\"Hello!\"); }"
            result = set_file_content(temp_file, new_content)
            
            assert result['success'] is True
            assert result['modified'] is True
            assert result['size'] == len(new_content)
            
            # Verify content was updated
            content_result = get_file_content(temp_file)
            assert content_result['content'] == new_content
            
        finally:
            os.unlink(temp_file)
    
    def test_list_open_files(self):
        """Test listing open files."""
        with patch('adapter._start_zed_process', return_value=True):
            session_result = create_editor_session()
            session_id = session_result['session_id']
        
        # Initially no files
        result = list_open_files(session_id)
        assert result['success'] is True
        assert result['files'] == []
        
        # Open some files
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f1:
            f1.write("# File 1")
            temp_file1 = f1.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.js') as f2:
            f2.write("// File 2")
            temp_file2 = f2.name
        
        try:
            open_file(session_id, temp_file1)
            open_file(session_id, temp_file2)
            
            result = list_open_files(session_id)
            
            assert result['success'] is True
            assert len(result['files']) == 2
            
            file_paths = [f['file_path'] for f in result['files']]
            assert os.path.abspath(temp_file1) in file_paths
            assert os.path.abspath(temp_file2) in file_paths
            
        finally:
            os.unlink(temp_file1)
            os.unlink(temp_file2)


class TestHelperFunctions:
    """Test suite for helper functions."""
    
    def test_detect_language(self):
        """Test language detection from file extensions."""
        test_cases = [
            ('/path/to/file.py', 'python'),
            ('/path/to/file.rs', 'rust'),
            ('/path/to/file.js', 'javascript'),
            ('/path/to/file.ts', 'typescript'),
            ('/path/to/file.html', 'html'),
            ('/path/to/file.css', 'css'),
            ('/path/to/file.json', 'json'),
            ('/path/to/file.md', 'markdown'),
            ('/path/to/file.txt', 'text'),
            ('/path/to/file.unknown', 'text'),
        ]
        
        for file_path, expected_language in test_cases:
            assert _detect_language(file_path) == expected_language
    
    def test_get_default_editor_settings(self):
        """Test default editor settings."""
        settings = _get_default_editor_settings()
        
        assert isinstance(settings, dict)
        assert 'theme' in settings
        assert 'font_size' in settings
        assert 'tab_size' in settings
        assert 'word_wrap' in settings
        assert 'line_numbers' in settings
        assert 'auto_save' in settings
        assert 'format_on_save' in settings
    
    @patch('subprocess.run')
    def test_check_zed_availability_success(self, mock_run):
        """Test Zed availability check success."""
        mock_run.return_value.returncode = 0
        assert _check_zed_availability() is True
    
    @patch('subprocess.run')
    def test_check_zed_availability_failure(self, mock_run):
        """Test Zed availability check failure."""
        mock_run.return_value.returncode = 1
        assert _check_zed_availability() is False
    
    @patch('subprocess.run')
    def test_check_zed_availability_exception(self, mock_run):
        """Test Zed availability check with exception."""
        mock_run.side_effect = FileNotFoundError()
        assert _check_zed_availability() is False


if __name__ == '__main__':
    pytest.main([__file__])
