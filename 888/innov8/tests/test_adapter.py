"""
Tests for innov8 (Jupyter) adapter.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import the adapter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapter import get_version, health_check, create_session, create_notebook, open_notebook, execute_cell, add_cell


class TestInnov8Adapter:
    """Test suite for innov8 adapter functions."""
    
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
    
    def test_create_notebook(self):
        """Test notebook creation."""
        # First create a session
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for notebook test")
        
        session_id = session_result['session_id']
        
        # Test creating notebook
        result = create_notebook(
            session_id=session_id,
            name="Test Notebook",
            kernel_type="python3"
        )
        
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'notebook_id' in result
            assert 'name' in result
            assert 'kernel_type' in result
            assert 'created_at' in result
            assert result['name'] == "Test Notebook"
            assert result['kernel_type'] == "python3"
            assert isinstance(result['notebook_id'], str)
            assert isinstance(result['created_at'], int)
    
    def test_create_notebook_without_name(self):
        """Test notebook creation without name."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for notebook test")
        
        session_id = session_result['session_id']
        
        result = create_notebook(session_id=session_id)
        
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'name' in result
            assert 'Untitled' in result['name']  # Should contain default name
            assert result['kernel_type'] == "python3"  # Default kernel
    
    def test_open_notebook(self):
        """Test notebook opening."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for notebook test")
        
        session_id = session_result['session_id']
        
        # Test with non-existent file
        result = open_notebook(
            session_id=session_id,
            file_path="/nonexistent/notebook.ipynb"
        )
        
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result
    
    def test_execute_cell(self):
        """Test cell execution."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for cell test")
        
        session_id = session_result['session_id']
        
        # First create a notebook
        nb_result = create_notebook(
            session_id=session_id,
            name="Test Execution Notebook"
        )
        
        if not nb_result['success']:
            pytest.skip("Cannot create notebook for cell test")
        
        notebook_id = nb_result['notebook_id']
        
        # Test executing the default cell (cell_0)
        result = execute_cell(
            session_id=session_id,
            notebook_id=notebook_id,
            cell_id="cell_0"
        )
        
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'notebook_id' in result
            assert 'cell_id' in result
            assert 'execution_count' in result
            assert 'output' in result
            assert result['notebook_id'] == notebook_id
            assert result['cell_id'] == "cell_0"
            assert isinstance(result['execution_count'], int)
            assert isinstance(result['output'], dict)
    
    def test_add_cell(self):
        """Test cell addition."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for cell test")
        
        session_id = session_result['session_id']
        
        # First create a notebook
        nb_result = create_notebook(session_id=session_id)
        
        if not nb_result['success']:
            pytest.skip("Cannot create notebook for cell test")
        
        notebook_id = nb_result['notebook_id']
        
        # Test adding different cell types
        for cell_type in ['code', 'markdown', 'raw']:
            result = add_cell(
                session_id=session_id,
                notebook_id=notebook_id,
                cell_type=cell_type
            )
            
            assert isinstance(result, dict)
            assert 'success' in result
            
            if result['success']:
                assert 'notebook_id' in result
                assert 'cell_id' in result
                assert 'cell_type' in result
                assert 'index' in result
                assert result['notebook_id'] == notebook_id
                assert result['cell_type'] == cell_type
                assert isinstance(result['cell_id'], str)
                assert isinstance(result['index'], int)
    
    def test_add_cell_at_index(self):
        """Test cell addition at specific index."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for cell test")
        
        session_id = session_result['session_id']
        
        # First create a notebook
        nb_result = create_notebook(session_id=session_id)
        
        if not nb_result['success']:
            pytest.skip("Cannot create notebook for cell test")
        
        notebook_id = nb_result['notebook_id']
        
        # Test adding cell at index 0
        result = add_cell(
            session_id=session_id,
            notebook_id=notebook_id,
            cell_type='markdown',
            index=0
        )
        
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert result['index'] == 0
    
    def test_invalid_session_id(self):
        """Test operations with invalid session ID."""
        invalid_session_id = "invalid_session_123"
        
        # Test create_notebook with invalid session
        result = create_notebook(
            session_id=invalid_session_id,
            name="Test Notebook"
        )
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result
    
    def test_invalid_notebook_id(self):
        """Test operations with invalid notebook ID."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for notebook test")
        
        session_id = session_result['session_id']
        invalid_notebook_id = "invalid_notebook_123"
        
        # Test execute_cell with invalid notebook ID
        result = execute_cell(
            session_id=session_id,
            notebook_id=invalid_notebook_id,
            cell_id="cell_0"
        )
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result
    
    def test_invalid_cell_id(self):
        """Test operations with invalid cell ID."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for notebook test")
        
        session_id = session_result['session_id']
        
        # First create a notebook
        nb_result = create_notebook(session_id=session_id)
        
        if not nb_result['success']:
            pytest.skip("Cannot create notebook for cell test")
        
        notebook_id = nb_result['notebook_id']
        
        # Test execute_cell with invalid cell ID
        result = execute_cell(
            session_id=session_id,
            notebook_id=notebook_id,
            cell_id="invalid_cell_123"
        )
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result


if __name__ == "__main__":
    pytest.main([__file__])
