"""
Tests for communic8 (Thunderbird) adapter.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import the adapter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapter import get_version, health_check, create_session, send_email, get_inbox


class TestCommunic8Adapter:
    """Test suite for communic8 adapter functions."""
    
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
    
    def test_create_session_with_profile(self):
        """Test session creation with profile path."""
        profile_path = "/tmp/test_profile"
        result = create_session(profile_path=profile_path)
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'profile_path' in result
            assert result['profile_path'] == profile_path
    
    def test_send_email(self):
        """Test email sending functionality."""
        # First create a session
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for email test")
        
        session_id = session_result['session_id']
        
        # Test sending email
        result = send_email(
            session_id=session_id,
            to_address="test@example.com",
            subject="Test Email",
            body="This is a test email."
        )
        
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'email_id' in result
            assert 'sent_at' in result
            assert isinstance(result['email_id'], str)
            assert isinstance(result['sent_at'], int)
    
    def test_send_email_with_cc_bcc(self):
        """Test email sending with CC and BCC."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for email test")
        
        session_id = session_result['session_id']
        
        result = send_email(
            session_id=session_id,
            to_address="test@example.com",
            subject="Test Email with CC/BCC",
            body="This is a test email with CC and BCC.",
            cc="cc@example.com",
            bcc="bcc@example.com"
        )
        
        assert isinstance(result, dict)
        assert 'success' in result
    
    def test_get_inbox(self):
        """Test inbox retrieval."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for inbox test")
        
        session_id = session_result['session_id']
        
        result = get_inbox(session_id=session_id)
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert 'emails' in result
            assert 'total_count' in result
            assert 'folder' in result
            assert isinstance(result['emails'], list)
            assert isinstance(result['total_count'], int)
            assert result['folder'] == 'INBOX'
    
    def test_get_inbox_with_limit(self):
        """Test inbox retrieval with limit."""
        session_result = create_session()
        if not session_result['success']:
            pytest.skip("Cannot create session for inbox test")
        
        session_id = session_result['session_id']
        
        result = get_inbox(session_id=session_id, limit=5)
        assert isinstance(result, dict)
        assert 'success' in result
        
        if result['success']:
            assert len(result['emails']) <= 5
    
    def test_invalid_session_id(self):
        """Test operations with invalid session ID."""
        invalid_session_id = "invalid_session_123"
        
        # Test send_email with invalid session
        result = send_email(
            session_id=invalid_session_id,
            to_address="test@example.com",
            subject="Test",
            body="Test"
        )
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result
        
        # Test get_inbox with invalid session
        result = get_inbox(session_id=invalid_session_id)
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result


if __name__ == "__main__":
    pytest.main([__file__])
