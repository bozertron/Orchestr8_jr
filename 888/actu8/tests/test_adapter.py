"""
Tests for actu8 (LibreOffice) adapter.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import the adapter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapter import get_version, health_check, create_session, create_document, open_document, save_document


class TestActu8Adapter:
    """Test suite for actu8 adapter functions."""
    
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
    
    def test_create_document(self):
        """Test document creation."""
        # First create a session
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for document test")
        
        session_id = session_result['session_id']
        
        # Test creating different document types
        for doc_type in ['writer', 'calc', 'impress', 'draw']:
            result = create_document(
                session_id=session_id,
                document_type=doc_type,
                title=f"Test {doc_type} Document"
            )
            
            assert isinstance(result, dict)
            assert 'success' in result
            
            if result['success']:
                assert 'document_id' in result
                assert 'type' in result
                assert 'title' in result
                assert 'created_at' in result
                assert result['type'] == doc_type
                assert isinstance(result['document_id'], str)
                assert isinstance(result['created_at'], int)
    
    def test_create_document_without_title(self):
        """Test document creation without title."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for document test")
        
        session_id = session_result['session_id']
        
        result = create_document(
            session_id=session_id,
            document_type='writer'
        )
        
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'title' in result
            assert 'writer' in result['title']  # Should contain document type
    
    def test_open_document(self):
        """Test document opening."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for document test")
        
        session_id = session_result['session_id']
        
        # Test with non-existent file
        result = open_document(
            session_id=session_id,
            file_path="/nonexistent/file.odt"
        )
        
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result
    
    def test_save_document(self):
        """Test document saving."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for document test")
        
        session_id = session_result['session_id']
        
        # First create a document
        doc_result = create_document(
            session_id=session_id,
            document_type='writer',
            title="Test Document"
        )
        
        if not doc_result['success']:
            pytest.skip("Cannot create document for save test")
        
        document_id = doc_result['document_id']
        
        # Test saving with file path
        result = save_document(
            session_id=session_id,
            document_id=document_id,
            file_path="/tmp/test_document.odt"
        )
        
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'document_id' in result
            assert 'file_path' in result
            assert 'saved_at' in result
            assert result['document_id'] == document_id
            assert isinstance(result['saved_at'], int)
    
    def test_save_document_without_path(self):
        """Test document saving without file path."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for document test")
        
        session_id = session_result['session_id']
        
        # First create a document
        doc_result = create_document(
            session_id=session_id,
            document_type='writer'
        )
        
        if not doc_result['success']:
            pytest.skip("Cannot create document for save test")
        
        document_id = doc_result['document_id']
        
        # Test saving without file path (should fail)
        result = save_document(
            session_id=session_id,
            document_id=document_id
        )
        
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result
    
    def test_invalid_session_id(self):
        """Test operations with invalid session ID."""
        invalid_session_id = "invalid_session_123"
        
        # Test create_document with invalid session
        result = create_document(
            session_id=invalid_session_id,
            document_type='writer'
        )
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result
    
    def test_invalid_document_id(self):
        """Test operations with invalid document ID."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for document test")
        
        session_id = session_result['session_id']
        invalid_document_id = "invalid_document_123"
        
        # Test save_document with invalid document ID
        result = save_document(
            session_id=session_id,
            document_id=invalid_document_id,
            file_path="/tmp/test.odt"
        )
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result


if __name__ == "__main__":
    pytest.main([__file__])
