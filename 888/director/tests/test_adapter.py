"""
Tests for Director adapter PyO3 integration.
"""

import unittest
import json
from wrappers.director import adapter


class TestDirectorAdapter(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        # Reset the Director context for each test
        adapter.reset_context()
    
    def test_adapter_initialization(self):
        """Test adapter initialization and health check."""
        health = adapter.health_check()
        
        self.assertIsInstance(health, dict)
        self.assertTrue(health['success'])
        self.assertEqual(health['status'], 'healthy')
        self.assertTrue(health['engine_initialized'])
        self.assertTrue(health['context_initialized'])
    
    def test_get_version(self):
        """Test version retrieval."""
        version = adapter.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, "1.0.0")
    
    def test_update_context(self):
        """Test context update with telemetry events."""
        telemetry_events = [
            {
                'event_type': {
                    'type': 'UIInteraction',
                    'data': {
                        'component': 'send_button',
                        'action': 'clicked',
                        'target': None,
                        'app_context': 'orchestr8'
                    }
                }
            },
            {
                'event_type': {
                    'type': 'ZoneChange',
                    'data': {
                        'from_zone': 'orchestr8',
                        'to_zone': 'integr8',
                        'duration_ms': 5000,
                        'app_context': 'maestro'
                    }
                }
            }
        ]
        
        result = adapter.update_context(telemetry_events)
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        self.assertIn('context_summary', result)
        self.assertIn('updated_at', result)
        
        # Check context summary content
        summary = result['context_summary']
        self.assertIn('current_zone', summary)
        self.assertIn('productivity_score', summary)
        self.assertEqual(summary['current_zone'], 'integr8')
    
    def test_get_suggestion_no_suggestion(self):
        """Test getting suggestion when none should be provided."""
        # Fresh context should not provide suggestions immediately
        result = adapter.get_suggestion()
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        self.assertFalse(result['has_suggestion'])
        self.assertIsNone(result['suggestion'])
        self.assertIn('reason', result)
    
    def test_get_suggestion_with_idle_pattern(self):
        """Test getting suggestion for idle patterns."""
        # First, update context to set up idle conditions
        # Note: This test may not always produce a suggestion due to timing constraints
        telemetry_events = [
            {
                'event_type': {
                    'type': 'IdleTime',
                    'data': {
                        'duration_ms': 150000,  # 2.5 minutes
                        'last_activity_type': 'ui_interaction',
                        'last_app_context': 'orchestr8'
                    }
                }
            }
        ]
        
        # Update context
        adapter.update_context(telemetry_events)
        
        # Manually adjust timing for testing
        context = adapter._get_context()
        context.last_suggestion_time = context.last_suggestion_time - 31000  # 31 seconds ago
        context.idle_duration = 150000  # 2.5 minutes
        
        result = adapter.get_suggestion()
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        # May or may not have suggestion depending on other conditions
        if result['has_suggestion']:
            self.assertIsInstance(result['suggestion'], dict)
            self.assertIn('id', result['suggestion'])
            self.assertIn('type', result['suggestion'])
            self.assertIn('title', result['suggestion'])
    
    def test_record_feedback(self):
        """Test recording user feedback for suggestions."""
        suggestion_id = "test-suggestion-123"
        rating = 1
        
        result = adapter.record_feedback(suggestion_id, rating)
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        self.assertEqual(result['suggestion_id'], suggestion_id)
        self.assertEqual(result['rating'], rating)
        self.assertIn('recorded_at', result)
        
        # Verify feedback was recorded in context
        context = adapter._get_context()
        self.assertEqual(context.user_feedback[suggestion_id], rating)
    
    def test_record_feedback_invalid_rating(self):
        """Test recording feedback with invalid rating (should be clamped)."""
        suggestion_id = "test-suggestion-456"
        
        # Test high rating (should be clamped to 1)
        result = adapter.record_feedback(suggestion_id, 5)
        self.assertTrue(result['success'])
        
        context = adapter._get_context()
        self.assertEqual(context.user_feedback[suggestion_id], 1)
        
        # Test low rating (should be clamped to -1)
        result = adapter.record_feedback(suggestion_id, -5)
        self.assertTrue(result['success'])
        
        context = adapter._get_context()
        self.assertEqual(context.user_feedback[suggestion_id], -1)
    
    def test_get_analytics(self):
        """Test getting behavioral analytics."""
        # Add some test data first
        telemetry_events = [
            {
                'event_type': {
                    'type': 'ToolActivation',
                    'data': {
                        'tool_name': 'chat_interface',
                        'context': 'user_interaction',
                        'activation_method': 'click',
                        'app_context': 'orchestr8'
                    }
                }
            },
            {
                'event_type': {
                    'type': 'ZoneChange',
                    'data': {
                        'from_zone': 'orchestr8',
                        'to_zone': 'integr8',
                        'duration_ms': 10000,
                        'app_context': 'maestro'
                    }
                }
            }
        ]
        
        adapter.update_context(telemetry_events)
        
        # Record some feedback
        adapter.record_feedback("test-suggestion", 1)
        
        result = adapter.get_analytics()
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        self.assertIn('analytics', result)
        self.assertIn('generated_at', result)
        
        analytics = result['analytics']
        self.assertIn('suggestions', analytics)
        self.assertIn('productivity', analytics)
        self.assertIn('zones', analytics)
        self.assertIn('tools', analytics)
        self.assertIn('context', analytics)
        
        # Check specific analytics content
        self.assertIn('feedback_count', analytics['suggestions'])
        self.assertIn('current_score', analytics['productivity'])
        self.assertIn('current_zone', analytics['zones'])
        self.assertEqual(analytics['zones']['current_zone'], 'integr8')
    
    def test_get_context_summary(self):
        """Test getting context summary."""
        # Add some test data
        telemetry_events = [
            {
                'event_type': {
                    'type': 'FileAccess',
                    'data': {
                        'file_path': '/test/file.py',
                        'access_type': 'open',
                        'file_size': 1024,
                        'app_context': 'integr8'
                    }
                }
            }
        ]
        
        adapter.update_context(telemetry_events)
        
        result = adapter.get_context_summary()
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        self.assertIn('context', result)
        
        context = result['context']
        self.assertIn('current_zone', context)
        self.assertIn('recent_files', context)
        self.assertIn('productivity_score', context)
        self.assertIn('/test/file.py', context['recent_files'])
    
    def test_reset_context(self):
        """Test context reset functionality."""
        # Add some data first
        telemetry_events = [
            {
                'event_type': {
                    'type': 'UIInteraction',
                    'data': {
                        'component': 'test_button',
                        'action': 'clicked',
                        'target': None,
                        'app_context': 'orchestr8'
                    }
                }
            }
        ]
        
        adapter.update_context(telemetry_events)
        adapter.record_feedback("test-suggestion", 1)
        
        # Verify data exists
        context_before = adapter._get_context()
        self.assertGreater(len(context_before.productivity_metrics), 0)
        self.assertGreater(len(context_before.user_feedback), 0)
        
        # Reset context
        result = adapter.reset_context()
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        self.assertIn('message', result)
        self.assertIn('reset_at', result)
        
        # Verify context was reset
        context_after = adapter._get_context()
        self.assertEqual(len(context_after.user_feedback), 0)
        self.assertEqual(context_after.current_zone, "orchestr8")  # Default value
    
    def test_error_handling(self):
        """Test error handling in adapter functions."""
        # Test with invalid telemetry events
        invalid_events = [
            {
                'invalid_structure': 'this should cause an error'
            }
        ]
        
        # Should handle errors gracefully
        result = adapter.update_context(invalid_events)
        
        # The adapter should handle this gracefully and not crash
        self.assertIsInstance(result, dict)
        # May succeed or fail depending on error handling, but should not crash
    
    def test_multiple_context_updates(self):
        """Test multiple context updates and state persistence."""
        # First update
        events1 = [
            {
                'event_type': {
                    'type': 'ZoneChange',
                    'data': {
                        'from_zone': 'orchestr8',
                        'to_zone': 'integr8',
                        'duration_ms': 5000,
                        'app_context': 'maestro'
                    }
                }
            }
        ]
        
        result1 = adapter.update_context(events1)
        self.assertTrue(result1['success'])
        self.assertEqual(result1['context_summary']['current_zone'], 'integr8')
        
        # Second update
        events2 = [
            {
                'event_type': {
                    'type': 'ToolActivation',
                    'data': {
                        'tool_name': 'editor',
                        'context': 'file_editing',
                        'activation_method': 'click',
                        'app_context': 'integr8'
                    }
                }
            }
        ]
        
        result2 = adapter.update_context(events2)
        self.assertTrue(result2['success'])
        
        # Verify state persistence
        context = adapter._get_context()
        self.assertEqual(context.current_zone, 'integr8')  # From first update
        self.assertIn('integr8:editor', context.tool_usage_patterns)  # From second update
    
    def test_suggestion_history_tracking(self):
        """Test that suggestion history is properly tracked."""
        # Manually create a suggestion scenario
        context = adapter._get_context()
        context.last_suggestion_time = context.last_suggestion_time - 31000  # 31 seconds ago
        context.idle_duration = 10000  # 10 seconds (good timing)
        
        # Try to get a suggestion
        result = adapter.get_suggestion()
        
        if result['has_suggestion']:
            # Verify suggestion was added to history
            context_after = adapter._get_context()
            self.assertGreater(len(context_after.suggestion_history), 0)
            
            last_suggestion = context_after.suggestion_history[-1]
            self.assertEqual(last_suggestion['id'], result['suggestion']['id'])
            self.assertTrue(last_suggestion['shown'])


if __name__ == '__main__':
    unittest.main()
