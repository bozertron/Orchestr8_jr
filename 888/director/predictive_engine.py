"""
Predictive Suggestions Engine for Director Intelligence.

This module implements intelligent next-action suggestions based on workspace context,
user behavior patterns, and predictive modeling of user needs.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
import time
import statistics
from collections import defaultdict, Counter
from .user_context import UserContext
from .pattern_recognition import WorkflowPattern, BehavioralInsight
from .models import Suggestion


@dataclass
class PredictiveModel:
    """Represents a predictive model for user behavior."""
    model_type: str  # "next_action", "workflow_completion", "tool_suggestion"
    confidence: float
    accuracy_history: List[float] = field(default_factory=list)
    last_updated: int = field(default_factory=lambda: int(time.time() * 1000))
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextualSuggestion:
    """Enhanced suggestion with contextual information."""
    base_suggestion: Suggestion
    context_factors: List[str]
    predicted_outcome: Dict[str, Any]
    alternative_actions: List[Dict[str, Any]] = field(default_factory=list)
    learning_opportunity: Optional[str] = None


class PredictiveEngine:
    """
    Predictive suggestions engine for intelligent next-action recommendations.
    
    This engine uses machine learning-inspired techniques to predict user needs
    and suggest optimal next actions based on context and behavioral patterns.
    """
    
    def __init__(self):
        self.predictive_models: Dict[str, PredictiveModel] = {}
        self.suggestion_history: List[Dict[str, Any]] = []
        self.context_patterns: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.workflow_predictions: Dict[str, float] = {}
        
        # Initialize predictive models
        self._initialize_models()
        
        # Prediction thresholds
        self.thresholds = {
            'min_prediction_confidence': 0.7,
            'context_similarity_threshold': 0.8,
            'workflow_completion_threshold': 0.6,
            'learning_opportunity_threshold': 0.5,
        }
    
    def generate_predictive_suggestions(self, context: UserContext, 
                                      patterns: List[WorkflowPattern],
                                      insights: List[BehavioralInsight]) -> List[ContextualSuggestion]:
        """
        Generate intelligent predictive suggestions based on current context.
        
        Args:
            context: Current user context
            patterns: Detected workflow patterns
            insights: Behavioral insights
            
        Returns:
            List of contextual suggestions with predictions
        """
        suggestions = []
        
        try:
            # Generate next-action predictions
            next_action_suggestions = self._predict_next_actions(context, patterns)
            suggestions.extend(next_action_suggestions)
            
            # Generate workflow completion suggestions
            workflow_suggestions = self._predict_workflow_completions(context, patterns)
            suggestions.extend(workflow_suggestions)
            
            # Generate tool optimization suggestions
            tool_suggestions = self._predict_tool_optimizations(context, insights)
            suggestions.extend(tool_suggestions)
            
            # Generate learning opportunity suggestions
            learning_suggestions = self._predict_learning_opportunities(context, patterns, insights)
            suggestions.extend(learning_suggestions)
            
            # Generate context-aware automation suggestions
            automation_suggestions = self._predict_automation_opportunities(context, patterns)
            suggestions.extend(automation_suggestions)
            
            # Rank suggestions by predicted value
            suggestions = self._rank_suggestions_by_value(suggestions, context)
            
            # Update models based on context
            self._update_predictive_models(context, suggestions)
            
        except Exception as e:
            # Return empty list on error, but log for debugging
            print(f"Error in predictive suggestions: {e}")
            suggestions = []
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def _predict_next_actions(self, context: UserContext, patterns: List[WorkflowPattern]) -> List[ContextualSuggestion]:
        """Predict likely next actions based on current context."""
        suggestions = []
        
        # Analyze current context for next action prediction
        current_zone = context.current_zone
        recent_zones = [t['to_zone'] for t in context.zone_transitions[-5:]]
        
        # Find patterns that match current context
        matching_patterns = [p for p in patterns if any(step.get('zone') == current_zone for step in p.steps)]
        
        for pattern in matching_patterns:
            if pattern.confidence > self.thresholds['min_prediction_confidence']:
                # Predict next step in workflow
                current_step_index = self._find_current_step_in_pattern(pattern, context)
                if current_step_index is not None and current_step_index < len(pattern.steps) - 1:
                    next_step = pattern.steps[current_step_index + 1]
                    
                    base_suggestion = Suggestion(
                        id="",
                        type="workflow",
                        title=f"Continue {pattern.name}",
                        description=f"Based on your pattern, consider moving to {next_step.get('zone', 'next step')}",
                        action_data={
                            'suggested_zone': next_step.get('zone'),
                            'pattern_id': pattern.id,
                            'confidence': pattern.confidence
                        },
                        confidence=pattern.confidence,
                        priority=4,
                        created_at=0
                    )
                    
                    contextual_suggestion = ContextualSuggestion(
                        base_suggestion=base_suggestion,
                        context_factors=[
                            f"Current zone: {current_zone}",
                            f"Pattern frequency: {pattern.frequency}",
                            f"Efficiency score: {pattern.efficiency_score:.2f}"
                        ],
                        predicted_outcome={
                            'efficiency_gain': pattern.efficiency_score * 0.2,
                            'time_saved_minutes': 5 * pattern.efficiency_score,
                            'workflow_completion_probability': 0.8
                        },
                        alternative_actions=[
                            {'action': 'skip_step', 'description': 'Skip this step and continue'},
                            {'action': 'modify_workflow', 'description': 'Customize the workflow'}
                        ]
                    )
                    
                    suggestions.append(contextual_suggestion)
        
        # Predict zone transitions based on time patterns
        if len(context.zone_transitions) >= 5:
            time_based_prediction = self._predict_time_based_transitions(context)
            if time_based_prediction:
                suggestions.append(time_based_prediction)
        
        return suggestions
    
    def _predict_workflow_completions(self, context: UserContext, patterns: List[WorkflowPattern]) -> List[ContextualSuggestion]:
        """Predict workflow completion opportunities."""
        suggestions = []
        
        # Find incomplete workflows
        for pattern in patterns:
            completion_probability = self._calculate_workflow_completion_probability(pattern, context)
            
            if completion_probability > self.thresholds['workflow_completion_threshold']:
                base_suggestion = Suggestion(
                    id="",
                    type="workflow",
                    title=f"Complete {pattern.name}",
                    description=f"You're {completion_probability*100:.0f}% through this workflow",
                    action_data={
                        'pattern_id': pattern.id,
                        'completion_probability': completion_probability,
                        'remaining_steps': self._get_remaining_steps(pattern, context)
                    },
                    confidence=completion_probability,
                    priority=3,
                    created_at=0
                )
                
                contextual_suggestion = ContextualSuggestion(
                    base_suggestion=base_suggestion,
                    context_factors=[
                        f"Workflow progress: {completion_probability*100:.0f}%",
                        f"Estimated time to complete: {self._estimate_completion_time(pattern)} minutes"
                    ],
                    predicted_outcome={
                        'productivity_boost': 0.3,
                        'satisfaction_score': 0.8,
                        'workflow_mastery_gain': 0.1
                    }
                )
                
                suggestions.append(contextual_suggestion)
        
        return suggestions
    
    def _predict_tool_optimizations(self, context: UserContext, insights: List[BehavioralInsight]) -> List[ContextualSuggestion]:
        """Predict tool optimization opportunities."""
        suggestions = []
        
        # Analyze tool usage patterns for optimization
        if context.tool_usage_patterns:
            most_used_tools = sorted(context.tool_usage_patterns.items(), key=lambda x: x[1], reverse=True)[:3]
            
            for tool, usage_count in most_used_tools:
                if usage_count > 10:  # Frequently used tool
                    optimization_potential = self._calculate_tool_optimization_potential(tool, usage_count, context)
                    
                    if optimization_potential > 0.5:
                        base_suggestion = Suggestion(
                            id="",
                            type="tool",
                            title=f"Optimize {tool} Usage",
                            description=f"Learn advanced features to boost efficiency with {tool}",
                            action_data={
                                'tool_name': tool,
                                'usage_count': usage_count,
                                'optimization_potential': optimization_potential
                            },
                            confidence=0.7,
                            priority=2,
                            created_at=0
                        )
                        
                        contextual_suggestion = ContextualSuggestion(
                            base_suggestion=base_suggestion,
                            context_factors=[
                                f"Tool usage: {usage_count} times",
                                f"Optimization potential: {optimization_potential*100:.0f}%"
                            ],
                            predicted_outcome={
                                'efficiency_gain': optimization_potential * 0.4,
                                'time_saved_per_use': 30,  # seconds
                                'skill_improvement': 0.2
                            },
                            learning_opportunity=f"Advanced {tool} techniques and shortcuts"
                        )
                        
                        suggestions.append(contextual_suggestion)
        
        return suggestions
    
    def _predict_learning_opportunities(self, context: UserContext, 
                                      patterns: List[WorkflowPattern],
                                      insights: List[BehavioralInsight]) -> List[ContextualSuggestion]:
        """Predict learning opportunities based on usage patterns."""
        suggestions = []
        
        # Identify underutilized zones/tools
        all_zones = ['orchestr8', 'integr8', 'communic8', 'actu8', 'cre8', 'innov8']
        used_zones = set([t['to_zone'] for t in context.zone_transitions])
        unused_zones = set(all_zones) - used_zones
        
        for zone in unused_zones:
            if len(unused_zones) <= 3:  # Don't overwhelm with too many suggestions
                base_suggestion = Suggestion(
                    id="",
                    type="learning",
                    title=f"Explore {zone}",
                    description=f"Discover new capabilities in {zone} to enhance your workflow",
                    action_data={
                        'zone': zone,
                        'exploration_type': 'guided_tour'
                    },
                    confidence=0.6,
                    priority=1,
                    created_at=0
                )
                
                contextual_suggestion = ContextualSuggestion(
                    base_suggestion=base_suggestion,
                    context_factors=[
                        f"Zone not yet explored: {zone}",
                        f"Potential workflow enhancement"
                    ],
                    predicted_outcome={
                        'skill_expansion': 0.3,
                        'workflow_diversity': 0.4,
                        'productivity_potential': 0.2
                    },
                    learning_opportunity=f"Introduction to {zone} features and capabilities"
                )
                
                suggestions.append(contextual_suggestion)
        
        return suggestions

    def _initialize_models(self) -> None:
        """Initialize predictive models."""
        self.predictive_models = {
            'next_action': PredictiveModel(
                model_type='next_action',
                confidence=0.5,
                parameters={'lookback_window': 5, 'weight_recent': 0.7}
            ),
            'workflow_completion': PredictiveModel(
                model_type='workflow_completion',
                confidence=0.6,
                parameters={'completion_threshold': 0.6, 'time_decay': 0.9}
            ),
            'tool_optimization': PredictiveModel(
                model_type='tool_optimization',
                confidence=0.7,
                parameters={'usage_threshold': 10, 'optimization_factor': 0.3}
            )
        }

    def _find_current_step_in_pattern(self, pattern: WorkflowPattern, context: UserContext) -> Optional[int]:
        """Find the current step index in a workflow pattern."""
        current_zone = context.current_zone

        for i, step in enumerate(pattern.steps):
            if step.get('zone') == current_zone:
                return i

        return None

    def _predict_time_based_transitions(self, context: UserContext) -> Optional[ContextualSuggestion]:
        """Predict zone transitions based on time patterns."""
        # Analyze time-based patterns in zone transitions
        current_hour = time.localtime().tm_hour

        # Simple time-based prediction (could be more sophisticated)
        if 9 <= current_hour <= 11:  # Morning
            suggested_zone = 'integr8'  # Code/development work
            description = "Morning is typically good for focused development work"
        elif 14 <= current_hour <= 16:  # Afternoon
            suggested_zone = 'communic8'  # Communication
            description = "Afternoon is good for communication and collaboration"
        else:
            return None

        base_suggestion = Suggestion(
            id="",
            type="productivity",
            title=f"Consider switching to {suggested_zone}",
            description=description,
            action_data={
                'suggested_zone': suggested_zone,
                'time_based': True,
                'current_hour': current_hour
            },
            confidence=0.6,
            priority=2,
            created_at=0
        )

        return ContextualSuggestion(
            base_suggestion=base_suggestion,
            context_factors=[f"Current time: {current_hour}:00", "Time-based productivity pattern"],
            predicted_outcome={
                'productivity_alignment': 0.3,
                'energy_optimization': 0.4
            }
        )

    def _calculate_workflow_completion_probability(self, pattern: WorkflowPattern, context: UserContext) -> float:
        """Calculate the probability of workflow completion."""
        current_step = self._find_current_step_in_pattern(pattern, context)

        if current_step is None:
            return 0.0

        # Simple completion probability based on current progress
        progress = (current_step + 1) / len(pattern.steps)

        # Factor in pattern confidence and frequency
        completion_prob = progress * pattern.confidence * min(1.0, pattern.frequency / 10.0)

        return min(1.0, completion_prob)

    def _get_remaining_steps(self, pattern: WorkflowPattern, context: UserContext) -> List[Dict[str, Any]]:
        """Get remaining steps in a workflow pattern."""
        current_step = self._find_current_step_in_pattern(pattern, context)

        if current_step is None:
            return pattern.steps

        return pattern.steps[current_step + 1:]

    def _estimate_completion_time(self, pattern: WorkflowPattern) -> int:
        """Estimate time to complete workflow in minutes."""
        # Simple estimation based on number of steps
        return len(pattern.steps) * 3  # 3 minutes per step average

    def _calculate_tool_optimization_potential(self, tool: str, usage_count: int, context: UserContext) -> float:
        """Calculate optimization potential for a tool."""
        # Base potential on usage frequency
        frequency_factor = min(1.0, usage_count / 50.0)  # Normalize to 50 uses

        # Factor in current productivity score
        productivity_factor = 1.0 - context.get_productivity_score()

        # Combine factors
        optimization_potential = (frequency_factor * 0.6) + (productivity_factor * 0.4)

        return min(1.0, optimization_potential)

    def _calculate_automation_potential(self, pattern: WorkflowPattern, context: UserContext) -> float:
        """Calculate automation potential for a workflow pattern."""
        # Base on frequency and inefficiency
        frequency_factor = min(1.0, pattern.frequency / 10.0)
        inefficiency_factor = 1.0 - pattern.efficiency_score

        # Combine factors
        automation_potential = (frequency_factor * 0.7) + (inefficiency_factor * 0.3)

        return min(1.0, automation_potential)

    def _rank_suggestions_by_value(self, suggestions: List[ContextualSuggestion], context: UserContext) -> List[ContextualSuggestion]:
        """Rank suggestions by predicted value to user."""
        def calculate_value_score(suggestion: ContextualSuggestion) -> float:
            base_score = suggestion.base_suggestion.confidence * suggestion.base_suggestion.priority

            # Factor in predicted outcomes
            outcome_score = 0.0
            if 'efficiency_gain' in suggestion.predicted_outcome:
                outcome_score += suggestion.predicted_outcome['efficiency_gain'] * 2
            if 'time_saved_minutes' in suggestion.predicted_outcome:
                outcome_score += suggestion.predicted_outcome['time_saved_minutes'] * 0.1
            if 'productivity_boost' in suggestion.predicted_outcome:
                outcome_score += suggestion.predicted_outcome['productivity_boost'] * 1.5

            return base_score + outcome_score

        return sorted(suggestions, key=calculate_value_score, reverse=True)

    def _update_predictive_models(self, context: UserContext, suggestions: List[ContextualSuggestion]) -> None:
        """Update predictive models based on current context and suggestions."""
        current_time = int(time.time() * 1000)

        # Update model confidence based on context patterns
        for model_name, model in self.predictive_models.items():
            # Simple confidence adjustment based on productivity score
            productivity_score = context.get_productivity_score()

            if productivity_score > 0.7:  # High productivity
                model.confidence = min(1.0, model.confidence + 0.05)
            elif productivity_score < 0.3:  # Low productivity
                model.confidence = max(0.1, model.confidence - 0.02)

            model.last_updated = current_time

        # Record suggestions for learning
        suggestion_record = {
            'timestamp': current_time,
            'context_zone': context.current_zone,
            'productivity_score': context.get_productivity_score(),
            'suggestions_count': len(suggestions),
            'suggestion_types': [s.base_suggestion.type for s in suggestions]
        }

        self.suggestion_history.append(suggestion_record)

        # Keep only recent history
        if len(self.suggestion_history) > 100:
            self.suggestion_history = self.suggestion_history[-100:]
    
    def _predict_automation_opportunities(self, context: UserContext, patterns: List[WorkflowPattern]) -> List[ContextualSuggestion]:
        """Predict automation opportunities based on repetitive patterns."""
        suggestions = []
        
        # Find highly repetitive patterns
        for pattern in patterns:
            if pattern.frequency > 5 and pattern.efficiency_score < 0.8:  # Frequent but inefficient
                automation_potential = self._calculate_automation_potential(pattern, context)
                
                if automation_potential > 0.6:
                    base_suggestion = Suggestion(
                        id="",
                        type="workflow",
                        title=f"Automate {pattern.name}",
                        description=f"This repetitive workflow could be automated to save time",
                        action_data={
                            'pattern_id': pattern.id,
                            'automation_type': 'workflow_template',
                            'potential_time_saved': pattern.frequency * 5  # minutes per week
                        },
                        confidence=automation_potential,
                        priority=4,
                        created_at=0
                    )
                    
                    contextual_suggestion = ContextualSuggestion(
                        base_suggestion=base_suggestion,
                        context_factors=[
                            f"Pattern frequency: {pattern.frequency}",
                            f"Current efficiency: {pattern.efficiency_score*100:.0f}%",
                            f"Automation potential: {automation_potential*100:.0f}%"
                        ],
                        predicted_outcome={
                            'time_saved_per_week': pattern.frequency * 5,
                            'efficiency_improvement': 0.4,
                            'cognitive_load_reduction': 0.3
                        }
                    )
                    
                    suggestions.append(contextual_suggestion)
        
        return suggestions
