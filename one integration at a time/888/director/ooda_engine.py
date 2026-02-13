"""
OODA Loop Engine for AI Director behavioral analysis and suggestion generation.

This module implements the Observe-Orient-Decide-Act loop for cross-application
intelligence and contextual suggestion generation.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import time
import uuid
from .user_context import UserContext


@dataclass
class Suggestion:
    """
    Represents a contextual suggestion from the AI Director.
    """
    id: str
    type: str  # "workflow", "tool", "productivity", "learning"
    title: str
    description: str
    action_data: Dict[str, Any]
    confidence: float  # 0.0 to 1.0
    priority: int  # 1 (low) to 5 (high)
    created_at: int
    expires_at: Optional[int] = None
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = int(time.time() * 1000)


class OODAEngine:
    """
    OODA Loop Engine for cross-application behavioral analysis.
    
    Implements the Observe-Orient-Decide-Act cycle:
    - Observe: Process telemetry events into unified context
    - Orient: Update context with pattern analysis
    - Decide: Analyze patterns and determine appropriate suggestions
    - Act: Format suggestions for UI display
    """
    
    def __init__(self):
        # Local imports avoid circular dependency with predictive_engine:
        # predictive_engine imports Suggestion from this module.
        from .pattern_recognition import AdvancedPatternRecognition
        from .predictive_engine import PredictiveEngine
        from .workflow_optimizer import WorkflowOptimizer
        from .automation_engine import ContextAwareAutomation

        self.context_history: List[UserContext] = []
        self.suggestion_templates = self._initialize_suggestion_templates()
        self.pattern_thresholds = {
            'idle_threshold': 120000,  # 2 minutes
            'productivity_low_threshold': 0.3,
            'zone_switch_frequency_high': 10,  # switches per hour
            'tool_repetition_threshold': 5,  # same tool used 5+ times
        }

        # Initialize enhanced intelligence components
        self.pattern_recognition = AdvancedPatternRecognition()
        self.predictive_engine = PredictiveEngine()
        self.workflow_optimizer = WorkflowOptimizer()
        self.automation_engine = ContextAwareAutomation()
    
    def observe(self, telemetry_events: List[Dict[str, Any]]) -> UserContext:
        """
        Process telemetry events into unified context.
        
        Args:
            telemetry_events: List of telemetry event dictionaries
            
        Returns:
            Updated UserContext with processed events
        """
        # Get the most recent context or create new one
        if self.context_history:
            context = self.context_history[-1]
        else:
            context = UserContext()
        
        # Process new telemetry events
        context.update_from_telemetry_events(telemetry_events)
        
        return context
    
    def orient(self, context: UserContext) -> UserContext:
        """
        Update context with advanced pattern analysis and behavioral insights.

        Args:
            context: Current UserContext

        Returns:
            UserContext updated with comprehensive pattern analysis
        """
        # Original pattern analysis
        self._analyze_productivity_patterns(context)
        self._analyze_zone_patterns(context)
        self._analyze_tool_patterns(context)

        # Enhanced pattern recognition
        pattern_analysis = self.pattern_recognition.analyze_patterns(context, self.context_history)

        # Store pattern analysis results in context
        context.productivity_metrics['advanced_patterns'] = pattern_analysis

        # Workflow optimization analysis
        if pattern_analysis.get('workflow_patterns'):
            workflow_patterns = [self._dict_to_workflow_pattern(p) for p in pattern_analysis['workflow_patterns']]
            optimization_analysis = self.workflow_optimizer.analyze_workflow_efficiency(
                workflow_patterns, context, self.context_history
            )
            context.productivity_metrics['optimization_analysis'] = optimization_analysis

        # Store context in history
        self.context_history.append(context)

        # Keep only recent context history (last 100 entries)
        if len(self.context_history) > 100:
            self.context_history = self.context_history[-100:]

        return context
    
    def decide(self, context: UserContext) -> Optional[Suggestion]:
        """
        Analyze patterns and determine appropriate suggestions using enhanced intelligence.

        Args:
            context: Current UserContext with comprehensive pattern analysis

        Returns:
            Best suggestion object if one should be made, None otherwise
        """
        if not context.should_show_suggestion():
            return None

        # Generate basic suggestions
        basic_suggestions = []

        # Check for idle time suggestions
        idle_suggestion = self._check_idle_patterns(context)
        if idle_suggestion:
            basic_suggestions.append(idle_suggestion)

        # Check for productivity suggestions
        productivity_suggestion = self._check_productivity_patterns(context)
        if productivity_suggestion:
            basic_suggestions.append(productivity_suggestion)

        # Check for workflow suggestions
        workflow_suggestion = self._check_workflow_patterns(context)
        if workflow_suggestion:
            basic_suggestions.append(workflow_suggestion)

        # Check for learning suggestions
        learning_suggestion = self._check_learning_patterns(context)
        if learning_suggestion:
            basic_suggestions.append(learning_suggestion)

        # Generate enhanced predictive suggestions
        enhanced_suggestions = []
        pattern_analysis = context.productivity_metrics.get('advanced_patterns', {})

        if pattern_analysis:
            workflow_patterns = [self._dict_to_workflow_pattern(p) for p in pattern_analysis.get('workflow_patterns', [])]
            behavioral_insights = [self._dict_to_behavioral_insight(i) for i in pattern_analysis.get('behavioral_insights', [])]

            # Generate predictive suggestions
            predictive_suggestions = self.predictive_engine.generate_predictive_suggestions(
                context, workflow_patterns, behavioral_insights
            )

            # Convert predictive suggestions to basic suggestions
            for pred_suggestion in predictive_suggestions:
                enhanced_suggestions.append(pred_suggestion.base_suggestion)

            # Process automation opportunities
            automation_results = self.automation_engine.process_context_for_automation(
                context, workflow_patterns, behavioral_insights
            )

            # Convert automation results to suggestions
            for automation in automation_results:
                if automation['action_type'] == 'suggestion_show':
                    auto_suggestion = Suggestion(
                        id="",
                        type=automation['parameters'].get('suggestion_type', 'automation'),
                        title=f"Auto: {automation['rule_name']}",
                        description=f"Automated suggestion: {automation['rule_name']}",
                        action_data=automation['parameters'],
                        confidence=automation['confidence'],
                        priority=automation['priority'],
                        created_at=0
                    )
                    enhanced_suggestions.append(auto_suggestion)

        # Combine all suggestions
        all_suggestions = basic_suggestions + enhanced_suggestions

        # Select the highest priority suggestion
        if all_suggestions:
            best_suggestion = max(all_suggestions, key=lambda s: (s.priority, s.confidence))
            return best_suggestion

        return None
    
    def act(self, suggestion: Suggestion) -> Dict[str, Any]:
        """
        Format suggestion for UI display.
        
        Args:
            suggestion: Suggestion object to format
            
        Returns:
            Dictionary formatted for UI consumption
        """
        return {
            'id': suggestion.id,
            'type': suggestion.type,
            'title': suggestion.title,
            'description': suggestion.description,
            'action_data': suggestion.action_data,
            'confidence': suggestion.confidence,
            'priority': suggestion.priority,
            'created_at': suggestion.created_at,
            'expires_at': suggestion.expires_at,
            'ui_config': {
                'show_duration': 10000,  # Show for 10 seconds
                'allow_dismiss': True,
                'require_feedback': suggestion.priority >= 4,
                'style': self._get_suggestion_style(suggestion.type)
            }
        }
    
    def _analyze_productivity_patterns(self, context: UserContext) -> None:
        """Analyze productivity patterns and update context metrics."""
        productivity_score = context.get_productivity_score()

        # Update productivity trend
        if 'productivity_trend' not in context.productivity_metrics:
            context.productivity_metrics['productivity_trend'] = []

        # Get the trend list (ensure it's a list)
        trend = context.productivity_metrics.get('productivity_trend', [])
        if not isinstance(trend, list):
            trend = []

        trend.append({
            'score': productivity_score,
            'timestamp': int(time.time() * 1000)
        })

        # Keep only recent trend data (last 20 points)
        if len(trend) > 20:
            trend = trend[-20:]

        context.productivity_metrics['productivity_trend'] = trend
    
    def _analyze_zone_patterns(self, context: UserContext) -> None:
        """Analyze zone transition patterns."""
        if len(context.zone_transitions) < 2:
            return
        
        # Calculate zone switching frequency
        recent_transitions = [t for t in context.zone_transitions 
                            if t['timestamp'] > (int(time.time() * 1000) - 3600000)]  # Last hour
        
        context.productivity_metrics['zone_switches_per_hour'] = len(recent_transitions)
        
        # Identify most common zone transitions
        transition_pairs = {}
        for i in range(1, len(context.zone_transitions)):
            prev_zone = context.zone_transitions[i-1]['to_zone']
            curr_zone = context.zone_transitions[i]['to_zone']
            pair = f"{prev_zone}->{curr_zone}"
            transition_pairs[pair] = transition_pairs.get(pair, 0) + 1
        
        if transition_pairs:
            most_common = max(transition_pairs.items(), key=lambda x: x[1])
            context.productivity_metrics['most_common_transition'] = most_common[0]
            context.productivity_metrics['most_common_transition_count'] = most_common[1]
    
    def _analyze_tool_patterns(self, context: UserContext) -> None:
        """Analyze tool usage patterns."""
        if not context.tool_usage_patterns:
            return
        
        # Find most used tool
        most_used = max(context.tool_usage_patterns.items(), key=lambda x: x[1])
        context.productivity_metrics['most_used_tool'] = most_used[0]
        context.productivity_metrics['most_used_tool_count'] = most_used[1]
        
        # Calculate tool diversity
        unique_tools = len(context.tool_usage_patterns)
        total_usage = sum(context.tool_usage_patterns.values())
        context.productivity_metrics['tool_diversity'] = unique_tools / max(1, total_usage)
    
    def _check_idle_patterns(self, context: UserContext) -> Optional[Suggestion]:
        """Check for idle time patterns and generate suggestions."""
        # Only suggest if idle duration is above threshold but not too high (user might be away)
        if (context.idle_duration > self.pattern_thresholds['idle_threshold'] and
            context.idle_duration < 300000):  # Less than 5 minutes idle
            return Suggestion(
                id="",
                type="productivity",
                title="Take a Break or Switch Tasks?",
                description=f"You've been idle for {context.idle_duration // 60000} minutes. Consider taking a break or switching to a different task.",
                action_data={
                    'suggested_actions': ['take_break', 'switch_zone', 'review_recent_files'],
                    'idle_duration': context.idle_duration
                },
                confidence=0.8,
                priority=3,
                created_at=0,
                expires_at=int(time.time() * 1000) + 300000  # Expires in 5 minutes
            )
        return None
    
    def _check_productivity_patterns(self, context: UserContext) -> Optional[Suggestion]:
        """Check for productivity patterns and generate suggestions."""
        productivity_score = context.get_productivity_score()
        
        if productivity_score < self.pattern_thresholds['productivity_low_threshold']:
            return Suggestion(
                id="",
                type="productivity",
                title="Boost Your Productivity",
                description="Your activity patterns suggest you might benefit from focusing on a single task or taking a short break.",
                action_data={
                    'suggested_actions': ['focus_mode', 'task_prioritization', 'break_reminder'],
                    'productivity_score': productivity_score
                },
                confidence=0.7,
                priority=2,
                created_at=0
            )
        return None
    
    def _check_workflow_patterns(self, context: UserContext) -> Optional[Suggestion]:
        """Check for workflow patterns and generate suggestions."""
        # Check for frequent zone switching
        zone_switches = context.productivity_metrics.get('zone_switches_per_hour', 0)
        
        if zone_switches > self.pattern_thresholds['zone_switch_frequency_high']:
            return Suggestion(
                id="",
                type="workflow",
                title="Optimize Your Workflow",
                description=f"You've switched between applications {zone_switches} times this hour. Consider batching similar tasks.",
                action_data={
                    'suggested_actions': ['batch_tasks', 'workflow_optimization', 'focus_timer'],
                    'switch_count': zone_switches
                },
                confidence=0.6,
                priority=2,
                created_at=0
            )
        
        # Check for repetitive tool usage
        most_used_tool_count = context.productivity_metrics.get('most_used_tool_count', 0)
        if most_used_tool_count > self.pattern_thresholds['tool_repetition_threshold']:
            most_used_tool = context.productivity_metrics.get('most_used_tool', '')
            return Suggestion(
                id="",
                type="workflow",
                title="Explore Alternative Tools",
                description=f"You've used {most_used_tool} {most_used_tool_count} times. Consider exploring alternative approaches.",
                action_data={
                    'suggested_actions': ['tool_alternatives', 'workflow_review', 'efficiency_tips'],
                    'tool_name': most_used_tool,
                    'usage_count': most_used_tool_count
                },
                confidence=0.5,
                priority=1,
                created_at=0
            )
        
        return None
    
    def _check_learning_patterns(self, context: UserContext) -> Optional[Suggestion]:
        """Check for learning opportunities and generate suggestions."""
        # Check for new zone exploration
        recent_zones = set(t['to_zone'] for t in context.zone_transitions[-10:])
        
        if len(recent_zones) == 1 and context.current_zone == 'orchestr8':
            return Suggestion(
                id="",
                type="learning",
                title="Explore More Features",
                description="You've been focused on the AI assistant. Consider exploring other tools and features available.",
                action_data={
                    'suggested_actions': ['feature_tour', 'explore_integr8', 'workflow_templates'],
                    'current_zone': context.current_zone
                },
                confidence=0.4,
                priority=1,
                created_at=0
            )
        
        return None
    
    def _get_suggestion_style(self, suggestion_type: str) -> Dict[str, str]:
        """Get UI style configuration for suggestion type."""
        styles = {
            'productivity': {'color': '#4CAF50', 'icon': 'trending_up'},
            'workflow': {'color': '#2196F3', 'icon': 'settings'},
            'learning': {'color': '#FF9800', 'icon': 'school'},
            'tool': {'color': '#9C27B0', 'icon': 'build'}
        }
        return styles.get(suggestion_type, {'color': '#757575', 'icon': 'info'})
    
    def _initialize_suggestion_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize suggestion templates for different scenarios."""
        return {
            'idle_break': {
                'title': 'Take a Break',
                'description': 'You\'ve been idle for a while. Consider taking a short break.',
                'type': 'productivity'
            },
            'zone_switch': {
                'title': 'Switch Context',
                'description': 'Try switching to a different application or task.',
                'type': 'workflow'
            },
            'tool_exploration': {
                'title': 'Explore New Tools',
                'description': 'Discover new features and tools available in your current application.',
                'type': 'learning'
            }
        }

    def _dict_to_workflow_pattern(self, pattern_dict: Dict[str, Any]):
        """Convert dictionary to WorkflowPattern object."""
        from .pattern_recognition import WorkflowPattern
        return WorkflowPattern(
            id=pattern_dict['id'],
            name=pattern_dict['name'],
            description=pattern_dict['description'],
            steps=pattern_dict['steps'],
            frequency=pattern_dict['frequency'],
            confidence=pattern_dict['confidence'],
            efficiency_score=pattern_dict['efficiency_score'],
            last_seen=pattern_dict['last_seen'],
            optimization_suggestions=pattern_dict.get('optimization_suggestions', [])
        )

    def _dict_to_behavioral_insight(self, insight_dict: Dict[str, Any]):
        """Convert dictionary to BehavioralInsight object."""
        from .pattern_recognition import BehavioralInsight
        return BehavioralInsight(
            type=insight_dict['type'],
            title=insight_dict['title'],
            description=insight_dict['description'],
            evidence=insight_dict['evidence'],
            confidence=insight_dict['confidence'],
            impact_score=insight_dict['impact_score'],
            actionable_suggestions=insight_dict.get('actionable_suggestions', [])
        )

    def get_enhanced_analytics(self) -> Dict[str, Any]:
        """Get comprehensive analytics from all intelligence components."""
        analytics = {
            'pattern_recognition': {},
            'workflow_optimization': {},
            'automation_performance': {},
            'predictive_accuracy': {},
            'overall_intelligence_score': 0.0
        }

        try:
            # Get pattern recognition analytics
            if hasattr(self.pattern_recognition, 'pattern_history'):
                pattern_count = len(self.pattern_recognition.pattern_history)
                analytics['pattern_recognition'] = {
                    'patterns_analyzed': pattern_count,
                    'detection_accuracy': 0.8,  # Placeholder - would be calculated from feedback
                    'insights_generated': pattern_count * 2  # Estimate
                }

            # Get workflow optimization analytics
            optimization_summary = self.workflow_optimizer.get_optimization_summary()
            analytics['workflow_optimization'] = optimization_summary

            # Get automation analytics
            automation_analytics = self.automation_engine.get_automation_analytics()
            analytics['automation_performance'] = automation_analytics

            # Calculate overall intelligence score
            scores = []
            if analytics['pattern_recognition']:
                scores.append(analytics['pattern_recognition'].get('detection_accuracy', 0.0))
            if analytics['workflow_optimization']:
                scores.append(analytics['workflow_optimization'].get('average_efficiency', 0.0))
            if analytics['automation_performance']:
                scores.append(analytics['automation_performance'].get('success_rate', 0.0))

            if scores:
                analytics['overall_intelligence_score'] = sum(scores) / len(scores)

        except Exception as e:
            analytics['error'] = str(e)

        return analytics
