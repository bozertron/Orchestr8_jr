"""
Director adapter for PyO3 integration.

This module provides the Python interface for the AI Director that will be
called from Rust via PyO3. It implements the OODA loop functionality and
returns Python primitives (following Option B enforcement).
"""

from typing import Dict, List, Optional, Any, Union
import json
import time
from .user_context import UserContext
from .ooda_engine import OODAEngine, Suggestion


# Global state for the Director
_director_engine: Optional[OODAEngine] = None
_current_context: Optional[UserContext] = None


def _get_engine() -> OODAEngine:
    """Get or create the global OODA engine instance."""
    global _director_engine
    if _director_engine is None:
        _director_engine = OODAEngine()
    return _director_engine


def _get_context() -> UserContext:
    """Get or create the global user context instance."""
    global _current_context
    if _current_context is None:
        _current_context = UserContext()
    return _current_context


def update_context(telemetry_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Update the Director's context with new telemetry events.
    
    Args:
        telemetry_events: List of telemetry event dictionaries
        
    Returns:
        Dictionary containing updated context summary
    """
    try:
        engine = _get_engine()
        
        # Observe: Process telemetry events
        context = engine.observe(telemetry_events)
        
        # Orient: Update context with pattern analysis
        updated_context = engine.orient(context)
        
        # Update global context
        global _current_context
        _current_context = updated_context
        
        # Return context summary
        return {
            'success': True,
            'context_summary': updated_context.get_context_summary(),
            'updated_at': int(time.time() * 1000)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'context_summary': {},
            'updated_at': int(time.time() * 1000)
        }


def get_suggestion() -> Dict[str, Any]:
    """
    Get a contextual suggestion from the Director.
    
    Returns:
        Dictionary containing suggestion data or None if no suggestion
    """
    try:
        engine = _get_engine()
        context = _get_context()
        
        # Decide: Generate suggestion based on current context
        suggestion = engine.decide(context)
        
        if suggestion is None:
            return {
                'success': True,
                'has_suggestion': False,
                'suggestion': None,
                'reason': 'No suggestion needed at this time'
            }
        
        # Act: Format suggestion for UI
        formatted_suggestion = engine.act(suggestion)
        
        # Update context with suggestion
        context.suggestion_history.append({
            'id': suggestion.id,
            'type': suggestion.type,
            'title': suggestion.title,
            'created_at': suggestion.created_at,
            'shown': True
        })
        context.last_suggestion_time = int(time.time() * 1000)
        
        return {
            'success': True,
            'has_suggestion': True,
            'suggestion': formatted_suggestion,
            'context_summary': context.get_context_summary()
        }
        
    except Exception as e:
        return {
            'success': False,
            'has_suggestion': False,
            'suggestion': None,
            'error': str(e)
        }


def record_feedback(suggestion_id: str, rating: int) -> Dict[str, Any]:
    """
    Record user feedback for a suggestion.
    
    Args:
        suggestion_id: Unique identifier for the suggestion
        rating: User rating (-1 = negative, 0 = neutral, 1 = positive)
        
    Returns:
        Dictionary indicating success/failure
    """
    try:
        context = _get_context()
        context.record_suggestion_feedback(suggestion_id, rating)
        
        return {
            'success': True,
            'suggestion_id': suggestion_id,
            'rating': rating,
            'recorded_at': int(time.time() * 1000)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'suggestion_id': suggestion_id
        }


def get_analytics() -> Dict[str, Any]:
    """
    Get comprehensive behavioral analytics and insights from the Enhanced Director.

    Returns:
        Dictionary containing enhanced analytics data
    """
    try:
        context = _get_context()
        engine = _get_engine()

        # Get basic analytics
        total_suggestions = len(context.suggestion_history)
        feedback_ratings = list(context.user_feedback.values())
        avg_rating = sum(feedback_ratings) / len(feedback_ratings) if feedback_ratings else 0.0

        # Zone analytics
        zone_time_spent = {}
        for transition in context.zone_transitions:
            zone = transition['to_zone']
            duration = transition.get('duration_ms', 0)
            zone_time_spent[zone] = zone_time_spent.get(zone, 0) + duration

        # Tool analytics
        top_tools = sorted(context.tool_usage_patterns.items(),
                          key=lambda x: x[1], reverse=True)[:10]

        # Productivity trend
        productivity_trend = context.productivity_metrics.get('productivity_trend', [])
        if isinstance(productivity_trend, list):
            recent_productivity = [p['score'] for p in productivity_trend[-10:] if isinstance(p, dict) and 'score' in p]
            avg_productivity = sum(recent_productivity) / len(recent_productivity) if recent_productivity else 0.5
        else:
            recent_productivity = []
            avg_productivity = 0.5

        # Get enhanced analytics from intelligence components
        enhanced_analytics = engine.get_enhanced_analytics()

        return {
            'success': True,
            'analytics': {
                'suggestions': {
                    'total_shown': total_suggestions,
                    'average_rating': avg_rating,
                    'feedback_count': len(context.user_feedback),
                    'recent_suggestions': context.suggestion_history[-5:]  # Last 5
                },
                'productivity': {
                    'current_score': context.get_productivity_score(),
                    'average_score': avg_productivity,
                    'trend': recent_productivity,
                    'session_duration': int(time.time() * 1000) - context.session_start_time
                },
                'zones': {
                    'current_zone': context.current_zone,
                    'time_spent': zone_time_spent,
                    'switches_per_hour': context.productivity_metrics.get('zone_switches_per_hour', 0),
                    'most_common_transition': context.productivity_metrics.get('most_common_transition', 'none')
                },
                'tools': {
                    'top_tools': top_tools,
                    'diversity_score': context.productivity_metrics.get('tool_diversity', 0.0),
                    'most_used': context.productivity_metrics.get('most_used_tool', 'none')
                },
                'context': {
                    'idle_duration': context.idle_duration,
                    'recent_files_count': len(context.recent_files),
                    'active_tools_count': len(context.active_tools)
                },
                # Enhanced intelligence analytics
                'enhanced_intelligence': enhanced_analytics
            },
            'generated_at': int(time.time() * 1000)
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'analytics': {},
            'generated_at': int(time.time() * 1000)
        }


def get_context_summary() -> Dict[str, Any]:
    """
    Get a summary of the current user context.
    
    Returns:
        Dictionary containing context summary
    """
    try:
        context = _get_context()
        return {
            'success': True,
            'context': context.get_context_summary()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'context': {}
        }


def reset_context() -> Dict[str, Any]:
    """
    Reset the Director's context (useful for testing or new sessions).
    
    Returns:
        Dictionary indicating success/failure
    """
    try:
        global _current_context, _director_engine
        _current_context = UserContext()
        _director_engine = OODAEngine()
        
        return {
            'success': True,
            'message': 'Director context reset successfully',
            'reset_at': int(time.time() * 1000)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'reset_at': int(time.time() * 1000)
        }


# Utility functions for testing and debugging
def get_version() -> str:
    """Get the Director version."""
    return "1.0.0"


def get_workflow_optimization_analysis() -> Dict[str, Any]:
    """
    Get workflow optimization analysis from the Enhanced Director.

    Returns:
        Dictionary containing workflow optimization recommendations
    """
    try:
        context = _get_context()

        # Get advanced pattern analysis from context
        pattern_analysis = context.productivity_metrics.get('advanced_patterns', {})
        optimization_analysis = context.productivity_metrics.get('optimization_analysis', {})

        return {
            'success': True,
            'workflow_patterns': pattern_analysis.get('workflow_patterns', []),
            'behavioral_insights': pattern_analysis.get('behavioral_insights', []),
            'optimization_recommendations': optimization_analysis.get('optimization_recommendations', []),
            'efficiency_analysis': optimization_analysis.get('efficiency_analysis', {}),
            'generated_at': int(time.time() * 1000)
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'workflow_patterns': [],
            'behavioral_insights': [],
            'optimization_recommendations': [],
            'efficiency_analysis': {},
            'generated_at': int(time.time() * 1000)
        }


def get_predictive_suggestions() -> Dict[str, Any]:
    """
    Get predictive suggestions from the Enhanced Director.

    Returns:
        Dictionary containing predictive suggestions and context
    """
    try:
        engine = _get_engine()
        context = _get_context()

        # Get pattern analysis
        pattern_analysis = context.productivity_metrics.get('advanced_patterns', {})

        if pattern_analysis:
            workflow_patterns = [engine._dict_to_workflow_pattern(p) for p in pattern_analysis.get('workflow_patterns', [])]
            behavioral_insights = [engine._dict_to_behavioral_insight(i) for i in pattern_analysis.get('behavioral_insights', [])]

            # Generate predictive suggestions
            predictive_suggestions = engine.predictive_engine.generate_predictive_suggestions(
                context, workflow_patterns, behavioral_insights
            )

            # Convert to serializable format
            suggestions_data = []
            for pred_suggestion in predictive_suggestions:
                suggestion_data = {
                    'base_suggestion': {
                        'id': pred_suggestion.base_suggestion.id,
                        'type': pred_suggestion.base_suggestion.type,
                        'title': pred_suggestion.base_suggestion.title,
                        'description': pred_suggestion.base_suggestion.description,
                        'confidence': pred_suggestion.base_suggestion.confidence,
                        'priority': pred_suggestion.base_suggestion.priority
                    },
                    'context_factors': pred_suggestion.context_factors,
                    'predicted_outcome': pred_suggestion.predicted_outcome,
                    'alternative_actions': pred_suggestion.alternative_actions,
                    'learning_opportunity': pred_suggestion.learning_opportunity
                }
                suggestions_data.append(suggestion_data)

            return {
                'success': True,
                'predictive_suggestions': suggestions_data,
                'context_summary': context.get_context_summary(),
                'generated_at': int(time.time() * 1000)
            }
        else:
            return {
                'success': True,
                'predictive_suggestions': [],
                'context_summary': context.get_context_summary(),
                'reason': 'Insufficient pattern data for predictions',
                'generated_at': int(time.time() * 1000)
            }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'predictive_suggestions': [],
            'generated_at': int(time.time() * 1000)
        }


def get_automation_status() -> Dict[str, Any]:
    """
    Get automation status and analytics from the Enhanced Director.

    Returns:
        Dictionary containing automation performance and status
    """
    try:
        engine = _get_engine()

        # Get automation analytics
        automation_analytics = engine.automation_engine.get_automation_analytics()

        return {
            'success': True,
            'automation_analytics': automation_analytics,
            'active_rules': automation_analytics.get('active_rules', 0),
            'total_triggers': automation_analytics.get('total_triggers', 0),
            'success_rate': automation_analytics.get('success_rate', 0.0),
            'generated_at': int(time.time() * 1000)
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'automation_analytics': {},
            'generated_at': int(time.time() * 1000)
        }


def health_check() -> Dict[str, Any]:
    """Perform a comprehensive health check of the Enhanced Director system."""
    try:
        engine = _get_engine()
        context = _get_context()

        # Check intelligence components
        components_status = {
            'pattern_recognition': hasattr(engine, 'pattern_recognition') and engine.pattern_recognition is not None,
            'predictive_engine': hasattr(engine, 'predictive_engine') and engine.predictive_engine is not None,
            'workflow_optimizer': hasattr(engine, 'workflow_optimizer') and engine.workflow_optimizer is not None,
            'automation_engine': hasattr(engine, 'automation_engine') and engine.automation_engine is not None
        }

        return {
            'success': True,
            'status': 'healthy',
            'engine_initialized': engine is not None,
            'context_initialized': context is not None,
            'intelligence_components': components_status,
            'context_events_processed': len(context.zone_transitions) + len(context.suggestion_history),
            'enhanced_features_active': all(components_status.values()),
            'checked_at': int(time.time() * 1000)
        }

    except Exception as e:
        return {
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'checked_at': int(time.time() * 1000)
        }
