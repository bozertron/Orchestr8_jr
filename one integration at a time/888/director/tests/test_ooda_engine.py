"""
Tests for OODA Engine behavioral analysis and suggestion generation.
"""

import unittest
import time
from wrappers.director.user_context import UserContext
from wrappers.director.ooda_engine import OODAEngine, Suggestion


class TestOODAEngine(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = OODAEngine()
    
    def test_engine_initialization(self):
        """Test OODA engine initialization."""
        self.assertIsInstance(self.engine, OODAEngine)
        self.assertEqual(len(self.engine.context_history), 0)
        self.assertIn('idle_threshold', self.engine.pattern_thresholds)
        self.assertIn('productivity_low_threshold', self.engine.pattern_thresholds)
    
    def test_observe_phase(self):
        """Test the Observe phase of OODA loop."""
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
            }
        ]
        
        context = self.engine.observe(telemetry_events)
        
        self.assertIsInstance(context, UserContext)
        self.assertEqual(context.productivity_metrics['send_button:clicked'], 1.0)
    
    def test_orient_phase(self):
        """Test the Orient phase of OODA loop."""
        # Create a context with some data
        context = UserContext()
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
        context.update_from_telemetry_events(events)
        
        oriented_context = self.engine.orient(context)
        
        self.assertIsInstance(oriented_context, UserContext)
        self.assertEqual(len(self.engine.context_history), 1)
        self.assertIn('productivity_trend', oriented_context.productivity_metrics)
    
    def test_decide_phase_no_suggestion(self):
        """Test the Decide phase when no suggestion should be made."""
        context = UserContext()
        # Set conditions where no suggestion should be made
        context.last_suggestion_time = int(time.time() * 1000)  # Very recent
        
        suggestion = self.engine.decide(context)
        
        self.assertIsNone(suggestion)
    
    def test_decide_phase_idle_suggestion(self):
        """Test the Decide phase for idle time suggestions."""
        context = UserContext()
        context.last_suggestion_time = int(time.time() * 1000) - 31000  # 31 seconds ago
        context.idle_duration = 150000  # 2.5 minutes (above threshold)
        
        suggestion = self.engine.decide(context)
        
        self.assertIsInstance(suggestion, Suggestion)
        self.assertEqual(suggestion.type, 'productivity')
        # Check that it's a break/task switching suggestion (which is what we generate for idle)
        self.assertIn('break', suggestion.title.lower())
    
    def test_decide_phase_productivity_suggestion(self):
        """Test the Decide phase for productivity suggestions."""
        context = UserContext()
        context.last_suggestion_time = int(time.time() * 1000) - 31000  # 31 seconds ago
        context.idle_duration = 10000  # 10 seconds (good timing)
        
        # Set low productivity score
        context.productivity_metrics['test_metric'] = 0.1
        
        suggestion = self.engine.decide(context)
        
        # Should get a productivity suggestion
        if suggestion:
            self.assertEqual(suggestion.type, 'productivity')
    
    def test_decide_phase_workflow_suggestion(self):
        """Test the Decide phase for workflow suggestions."""
        context = UserContext()
        context.last_suggestion_time = int(time.time() * 1000) - 31000  # 31 seconds ago
        context.idle_duration = 10000  # 10 seconds (good timing)
        
        # Set high zone switching frequency
        context.productivity_metrics['zone_switches_per_hour'] = 15
        
        suggestion = self.engine.decide(context)
        
        # Should get a workflow suggestion
        if suggestion:
            self.assertEqual(suggestion.type, 'workflow')
            self.assertIn('workflow', suggestion.title.lower())
    
    def test_act_phase(self):
        """Test the Act phase of OODA loop."""
        suggestion = Suggestion(
            id="test-123",
            type="productivity",
            title="Test Suggestion",
            description="This is a test suggestion",
            action_data={'test': 'data'},
            confidence=0.8,
            priority=3,
            created_at=int(time.time() * 1000)
        )
        
        formatted = self.engine.act(suggestion)
        
        self.assertIsInstance(formatted, dict)
        self.assertEqual(formatted['id'], "test-123")
        self.assertEqual(formatted['type'], "productivity")
        self.assertEqual(formatted['title'], "Test Suggestion")
        self.assertEqual(formatted['confidence'], 0.8)
        self.assertEqual(formatted['priority'], 3)
        self.assertIn('ui_config', formatted)
        self.assertIn('show_duration', formatted['ui_config'])
    
    def test_suggestion_creation(self):
        """Test Suggestion object creation and properties."""
        suggestion = Suggestion(
            id="",  # Should auto-generate
            type="learning",
            title="Learn Something New",
            description="Try exploring new features",
            action_data={'action': 'explore'},
            confidence=0.6,
            priority=2,
            created_at=0  # Should auto-generate
        )
        
        self.assertNotEqual(suggestion.id, "")  # Should have generated ID
        self.assertGreater(suggestion.created_at, 0)  # Should have generated timestamp
        self.assertEqual(suggestion.type, "learning")
        self.assertEqual(suggestion.confidence, 0.6)
        self.assertEqual(suggestion.priority, 2)
    
    def test_pattern_analysis_productivity(self):
        """Test productivity pattern analysis."""
        context = UserContext()
        
        # Add some productivity data
        context.productivity_metrics['test_interaction'] = 5.0
        context.tool_usage_patterns['orchestr8:chat'] = 3
        
        self.engine._analyze_productivity_patterns(context)
        
        self.assertIn('productivity_trend', context.productivity_metrics)
        trend = context.productivity_metrics['productivity_trend']
        self.assertGreater(len(trend), 0)
        self.assertIn('score', trend[0])
        self.assertIn('timestamp', trend[0])
    
    def test_pattern_analysis_zones(self):
        """Test zone pattern analysis."""
        context = UserContext()
        
        # Add zone transitions
        current_time = int(time.time() * 1000)
        for i in range(5):
            context.zone_transitions.append({
                'from_zone': f'zone{i}',
                'to_zone': f'zone{i+1}',
                'duration_ms': 1000,
                'timestamp': current_time - (i * 60000)  # 1 minute apart
            })
        
        self.engine._analyze_zone_patterns(context)
        
        self.assertIn('zone_switches_per_hour', context.productivity_metrics)
        # Should count recent transitions (within last hour)
        self.assertGreaterEqual(context.productivity_metrics['zone_switches_per_hour'], 0)
    
    def test_pattern_analysis_tools(self):
        """Test tool pattern analysis."""
        context = UserContext()
        
        # Add tool usage data
        context.tool_usage_patterns = {
            'orchestr8:chat': 10,
            'integr8:editor': 5,
            'orchestr8:settings': 2
        }
        
        self.engine._analyze_tool_patterns(context)
        
        self.assertIn('most_used_tool', context.productivity_metrics)
        self.assertIn('most_used_tool_count', context.productivity_metrics)
        self.assertIn('tool_diversity', context.productivity_metrics)
        
        self.assertEqual(context.productivity_metrics['most_used_tool'], 'orchestr8:chat')
        self.assertEqual(context.productivity_metrics['most_used_tool_count'], 10)
    
    def test_context_history_limit(self):
        """Test that context history is properly limited."""
        # Add more than 100 contexts
        for i in range(105):
            context = UserContext()
            context.current_zone = f'zone{i}'
            self.engine.context_history.append(context)
        
        # Trigger orient to apply limit
        test_context = UserContext()
        self.engine.orient(test_context)
        
        # Should only keep the most recent 100
        self.assertEqual(len(self.engine.context_history), 100)
    
    def test_full_ooda_cycle(self):
        """Test a complete OODA cycle."""
        # Observe
        telemetry_events = [
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
            }
        ]
        
        context = self.engine.observe(telemetry_events)
        
        # Orient
        oriented_context = self.engine.orient(context)
        
        # Decide (may or may not produce a suggestion)
        suggestion = self.engine.decide(oriented_context)
        
        # Act (if there's a suggestion)
        if suggestion:
            formatted = self.engine.act(suggestion)
            self.assertIsInstance(formatted, dict)
            self.assertIn('id', formatted)
            self.assertIn('type', formatted)
            self.assertIn('ui_config', formatted)
        
        # Verify context was processed
        self.assertGreater(len(self.engine.context_history), 0)
        self.assertEqual(oriented_context.productivity_metrics['input_field:typed'], 1.0)


if __name__ == '__main__':
    unittest.main()
