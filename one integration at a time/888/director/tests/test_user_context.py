"""
Tests for UserContext model and telemetry event processing.
"""

import unittest
import time
from wrappers.director.user_context import UserContext


class TestUserContext(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.context = UserContext()
    
    def test_initial_state(self):
        """Test initial UserContext state."""
        self.assertEqual(self.context.current_zone, "orchestr8")
        self.assertEqual(len(self.context.active_tools), 0)
        self.assertEqual(len(self.context.recent_files), 0)
        self.assertIsNone(self.context.conversation_context)
        self.assertEqual(self.context.idle_duration, 0)
    
    def test_zone_change_handling(self):
        """Test zone change event processing."""
        event = {
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
        
        self.context.update_from_telemetry_events([event])
        
        self.assertEqual(self.context.current_zone, 'integr8')
        self.assertEqual(len(self.context.zone_transitions), 1)
        self.assertEqual(self.context.zone_transitions[0]['from_zone'], 'orchestr8')
        self.assertEqual(self.context.zone_transitions[0]['to_zone'], 'integr8')
    
    def test_tool_activation_handling(self):
        """Test tool activation event processing."""
        event = {
            'event_type': {
                'type': 'ToolActivation',
                'data': {
                    'tool_name': 'chat_interface',
                    'context': 'user_interaction',
                    'activation_method': 'click',
                    'app_context': 'orchestr8'
                }
            }
        }
        
        self.context.update_from_telemetry_events([event])
        
        self.assertEqual(self.context.active_tools['orchestr8'], 'chat_interface')
        self.assertEqual(self.context.tool_usage_patterns['orchestr8:chat_interface'], 1)
    
    def test_file_access_handling(self):
        """Test file access event processing."""
        event = {
            'event_type': {
                'type': 'FileAccess',
                'data': {
                    'file_path': '/path/to/test.py',
                    'access_type': 'open',
                    'file_size': 1024,
                    'app_context': 'integr8'
                }
            }
        }
        
        self.context.update_from_telemetry_events([event])
        
        self.assertIn('/path/to/test.py', self.context.recent_files)
        self.assertEqual(self.context.recent_files[0], '/path/to/test.py')
    
    def test_idle_time_handling(self):
        """Test idle time event processing."""
        event = {
            'event_type': {
                'type': 'IdleTime',
                'data': {
                    'duration_ms': 120000,
                    'last_activity_type': 'ui_interaction',
                    'last_app_context': 'orchestr8'
                }
            }
        }
        
        self.context.update_from_telemetry_events([event])
        
        self.assertEqual(self.context.idle_duration, 120000)
    
    def test_ui_interaction_handling(self):
        """Test UI interaction event processing."""
        event = {
            'event_type': {
                'type': 'UIInteraction',
                'data': {
                    'component': 'send_button',
                    'action': 'clicked',
                    'target': None,
                    'app_context': 'orchestr8'
                }
            }
        }
        
        self.context.update_from_telemetry_events([event])
        
        self.assertEqual(self.context.idle_duration, 0)  # Reset on interaction
        self.assertEqual(self.context.productivity_metrics['send_button:clicked'], 1.0)
    
    def test_productivity_score_calculation(self):
        """Test productivity score calculation."""
        # Add some activity
        events = [
            {
                'event_type': {
                    'type': 'UIInteraction',
                    'data': {
                        'component': 'input_field',
                        'action': 'typed',
                        'target': None,
                        'app_context': 'orchestr8'
                    }
                }
            },
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
            }
        ]
        
        self.context.update_from_telemetry_events(events)
        score = self.context.get_productivity_score()
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_context_summary(self):
        """Test context summary generation."""
        # Add some test data
        events = [
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
            },
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
        
        self.context.update_from_telemetry_events(events)
        summary = self.context.get_context_summary()
        
        self.assertIn('current_zone', summary)
        self.assertIn('active_tools', summary)
        self.assertIn('recent_files', summary)
        self.assertIn('productivity_score', summary)
        self.assertEqual(summary['current_zone'], 'integr8')
        self.assertIn('/test/file.py', summary['recent_files'])
    
    def test_suggestion_feedback(self):
        """Test suggestion feedback recording."""
        suggestion_id = "test-suggestion-123"
        
        self.context.record_suggestion_feedback(suggestion_id, 1)
        self.assertEqual(self.context.user_feedback[suggestion_id], 1)
        
        self.context.record_suggestion_feedback(suggestion_id, -1)
        self.assertEqual(self.context.user_feedback[suggestion_id], -1)
        
        # Test rating bounds
        self.context.record_suggestion_feedback(suggestion_id, 5)  # Should be clamped to 1
        self.assertEqual(self.context.user_feedback[suggestion_id], 1)
        
        self.context.record_suggestion_feedback(suggestion_id, -5)  # Should be clamped to -1
        self.assertEqual(self.context.user_feedback[suggestion_id], -1)
    
    def test_should_show_suggestion(self):
        """Test suggestion display logic."""
        # Initially should not show (too recent)
        self.assertFalse(self.context.should_show_suggestion())
        
        # Set last suggestion time to 31 seconds ago
        self.context.last_suggestion_time = int(time.time() * 1000) - 31000

        # Set idle duration to a good timing (5 seconds)
        self.context.idle_duration = 5000

        # Should show now (enough time has passed and good timing)
        self.assertTrue(self.context.should_show_suggestion())
        
        # Set idle duration to 6 minutes (above our 5-minute threshold)
        self.context.idle_duration = 360000

        # Should not show (too idle)
        self.assertFalse(self.context.should_show_suggestion())
        
        # Set idle duration to 1 second (very active)
        self.context.idle_duration = 1000
        
        # Should not show (too active)
        self.assertFalse(self.context.should_show_suggestion())
        
        # Set idle duration to 10 seconds (good timing)
        self.context.idle_duration = 10000
        
        # Should show now
        self.assertTrue(self.context.should_show_suggestion())
    
    def test_recent_files_limit(self):
        """Test that recent files list is properly limited."""
        # Add 25 files (more than the limit of 20)
        for i in range(25):
            event = {
                'event_type': {
                    'type': 'FileAccess',
                    'data': {
                        'file_path': f'/test/file{i}.py',
                        'access_type': 'open',
                        'file_size': 1024,
                        'app_context': 'integr8'
                    }
                }
            }
            self.context.update_from_telemetry_events([event])
        
        # Should only keep the most recent 20
        self.assertEqual(len(self.context.recent_files), 20)
        self.assertEqual(self.context.recent_files[0], '/test/file24.py')  # Most recent
        self.assertEqual(self.context.recent_files[-1], '/test/file5.py')  # Oldest kept
    
    def test_zone_transitions_limit(self):
        """Test that zone transitions list is properly limited."""
        # Add 60 zone transitions (more than the limit of 50)
        for i in range(60):
            event = {
                'event_type': {
                    'type': 'ZoneChange',
                    'data': {
                        'from_zone': f'zone{i}',
                        'to_zone': f'zone{i+1}',
                        'duration_ms': 1000,
                        'app_context': 'maestro'
                    }
                }
            }
            self.context.update_from_telemetry_events([event])
        
        # Should only keep the most recent 50
        self.assertEqual(len(self.context.zone_transitions), 50)
        self.assertEqual(self.context.zone_transitions[-1]['to_zone'], 'zone60')  # Most recent
        self.assertEqual(self.context.zone_transitions[0]['to_zone'], 'zone11')  # Oldest kept


if __name__ == '__main__':
    unittest.main()
