"""
Tests for cre8 (GIMP) adapter.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import the adapter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapter import get_version, health_check, create_session, create_image, open_image, save_image, apply_filter


class TestCre8Adapter:
    """Test suite for cre8 adapter functions."""
    
    def test_get_version(self):
        """Test version retrieval."""
        version = get_version()
        assert isinstance(version, str)
        assert version == "1.0.0"
    
    def test_health_check(self):
        """Test health check functionality."""
        result = health_check()
        assert isinstance(result, dict)
        assert 'success' in result
        assert 'status' in result
        assert 'checked_at' in result
        assert isinstance(result['success'], bool)
        assert isinstance(result['checked_at'], int)
    
    def test_create_session(self):
        """Test session creation."""
        result = create_session()
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'session_id' in result
            assert 'created_at' in result
            assert isinstance(result['session_id'], str)
            assert isinstance(result['created_at'], int)
    
    def test_create_session_with_workspace(self):
        """Test session creation with workspace path."""
        workspace_path = "/tmp/test_workspace"
        result = create_session(workspace_path=workspace_path)
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'workspace_path' in result
            assert result['workspace_path'] == workspace_path
    
    def test_create_image(self):
        """Test image creation."""
        # First create a session
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for image test")
        
        session_id = session_result['session_id']
        
        # Test creating image
        result = create_image(
            session_id=session_id,
            width=800,
            height=600,
            name="Test Image"
        )
        
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'image_id' in result
            assert 'name' in result
            assert 'width' in result
            assert 'height' in result
            assert 'created_at' in result
            assert result['width'] == 800
            assert result['height'] == 600
            assert result['name'] == "Test Image"
            assert isinstance(result['image_id'], str)
            assert isinstance(result['created_at'], int)
    
    def test_create_image_without_name(self):
        """Test image creation without name."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for image test")
        
        session_id = session_result['session_id']
        
        result = create_image(
            session_id=session_id,
            width=400,
            height=300
        )
        
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'name' in result
            assert 'Untitled' in result['name']  # Should contain default name
    
    def test_open_image(self):
        """Test image opening."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for image test")
        
        session_id = session_result['session_id']
        
        # Test with non-existent file
        result = open_image(
            session_id=session_id,
            file_path="/nonexistent/image.png"
        )
        
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result
    
    def test_save_image(self):
        """Test image saving."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for image test")
        
        session_id = session_result['session_id']
        
        # First create an image
        img_result = create_image(
            session_id=session_id,
            width=200,
            height=200,
            name="Test Save Image"
        )
        
        if not img_result['success']:
            pytest.skip("Cannot create image for save test")
        
        image_id = img_result['image_id']
        
        # Test saving with file path
        result = save_image(
            session_id=session_id,
            image_id=image_id,
            file_path="/tmp/test_image.png",
            format="png"
        )
        
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'image_id' in result
            assert 'file_path' in result
            assert 'format' in result
            assert 'saved_at' in result
            assert result['image_id'] == image_id
            assert result['format'] == "png"
            assert isinstance(result['saved_at'], int)
    
    def test_apply_filter(self):
        """Test filter application."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for filter test")
        
        session_id = session_result['session_id']
        
        # First create an image
        img_result = create_image(
            session_id=session_id,
            width=100,
            height=100
        )
        
        if not img_result['success']:
            pytest.skip("Cannot create image for filter test")
        
        image_id = img_result['image_id']
        
        # Test applying filter
        result = apply_filter(
            session_id=session_id,
            image_id=image_id,
            filter_name="blur",
            parameters={"radius": 5}
        )
        
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'image_id' in result
            assert 'filter_applied' in result
            assert 'applied_at' in result
            assert result['image_id'] == image_id
            assert result['filter_applied'] == "blur"
            assert isinstance(result['applied_at'], int)
    
    def test_invalid_session_id(self):
        """Test operations with invalid session ID."""
        invalid_session_id = "invalid_session_123"
        
        # Test create_image with invalid session
        result = create_image(
            session_id=invalid_session_id,
            width=100,
            height=100
        )
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result
    
    def test_invalid_image_id(self):
        """Test operations with invalid image ID."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for image test")
        
        session_id = session_result['session_id']
        invalid_image_id = "invalid_image_123"
        
        # Test save_image with invalid image ID
        result = save_image(
            session_id=session_id,
            image_id=invalid_image_id,
            file_path="/tmp/test.png"
        )
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result


if __name__ == "__main__":
    pytest.main([__file__])
