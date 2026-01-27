"""
Fusion Learning Engine Module for Phase 7.2 ML Enhanced Recognition.

This module implements continuous learning and optimization for multimodal spell recognition
through usage analytics, pattern learning, and intelligent suggestions.

Key Features:
- SpellUsageAnalytics for usage pattern analysis
- UserPatternLearner for behavioral learning
- SensesDirectorBridge for cross-application intelligence
- MLOptimizer for performance optimization
- Predictive spell recommendations
"""

import json
import time
import numpy as np
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional, Tuple
import logging
from collections import defaultdict, deque

# ML dependencies (graceful fallback if not available)
try:
    import sklearn.cluster
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    sklearn = None

# Import existing components
from .multimodal_fusion import SpellIntent, SpellDefinition

logger = logging.getLogger(__name__)


@dataclass
class SpellUsageAnalytics:
    """Analytics for spell usage patterns and performance."""
    spell_usage_history: List[Dict[str, Any]]
    performance_metrics: Dict[str, float]
    context_correlations: Dict[str, Any]
    temporal_patterns: Dict[str, Any]
    user_feedback_data: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SpellUsageAnalytics':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class UserPatternLearner:
    """Learns user behavioral patterns for spell optimization."""
    gesture_patterns: Dict[str, Any]
    speech_patterns: Dict[str, Any]
    temporal_patterns: Dict[str, Any]
    context_patterns: Dict[str, Any]
    adaptation_rate: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPatternLearner':
        """Create from dictionary."""
        return cls(**data)


class SensesDirectorBridge:
    """Integration with Enhanced Director Intelligence for context awareness."""
    
    def __init__(self):
        self.workspace_context = {}
        self.application_states = {}
        self.user_activity_patterns = {}
        
    def get_current_context(self) -> Dict[str, Any]:
        """Get current workspace context from Enhanced Director."""
        # This would integrate with the actual Enhanced Director system
        # For now, return mock context
        return {
            'current_panel': 'orchestr8',
            'active_applications': ['newelle', 'zed'],
            'recent_activities': ['file_edit', 'conversation'],
            'time_of_day': 'afternoon',
            'work_session_duration': 120,  # minutes
            'focus_level': 'high'
        }
    
    def predict_next_action(self, current_spell: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict likely next actions based on context and patterns."""
        # Simplified prediction logic
        predictions = []
        
        current_panel = context.get('current_panel', 'orchestr8')
        
        # Common follow-up actions based on current spell
        if 'navigation' in current_spell.lower():
            predictions.append({
                'action': 'file_operation',
                'confidence': 0.7,
                'suggested_spells': ['open_file', 'save_file']
            })
        elif 'file' in current_spell.lower():
            predictions.append({
                'action': 'edit_operation',
                'confidence': 0.8,
                'suggested_spells': ['select_text', 'copy_paste']
            })
        
        return predictions
    
    def update_activity_context(self, spell_intent: SpellIntent, outcome: Dict[str, Any]):
        """Update activity context based on spell execution."""
        timestamp = int(time.time() * 1000)
        
        activity_record = {
            'timestamp': timestamp,
            'spell_id': spell_intent.spell_id,
            'gesture': spell_intent.gesture_component,
            'speech': spell_intent.speech_component,
            'outcome': outcome,
            'context': self.get_current_context()
        }
        
        # Store in recent activities (keep last 100)
        if 'recent_activities' not in self.user_activity_patterns:
            self.user_activity_patterns['recent_activities'] = deque(maxlen=100)
        
        self.user_activity_patterns['recent_activities'].append(activity_record)


class MLOptimizer:
    """Machine learning optimizer for spell recognition performance."""
    
    def __init__(self):
        self.optimization_history = []
        self.performance_baselines = {}
        self.optimization_strategies = {}
        
    def analyze_performance_trends(self, usage_analytics: SpellUsageAnalytics) -> Dict[str, Any]:
        """Analyze performance trends and identify optimization opportunities."""
        try:
            if not usage_analytics.spell_usage_history:
                return {
                    'success': False,
                    'error': 'No usage history available for analysis'
                }
            
            # Calculate performance metrics
            total_attempts = len(usage_analytics.spell_usage_history)
            successful_attempts = sum(1 for usage in usage_analytics.spell_usage_history 
                                    if usage.get('success', False))
            
            success_rate = successful_attempts / total_attempts if total_attempts > 0 else 0.0
            
            # Analyze confidence trends
            confidences = [usage.get('confidence', 0.0) for usage in usage_analytics.spell_usage_history]
            avg_confidence = np.mean(confidences) if confidences else 0.0
            confidence_std = np.std(confidences) if confidences else 0.0
            
            # Identify problematic spells
            spell_performance = defaultdict(list)
            for usage in usage_analytics.spell_usage_history:
                spell_id = usage.get('spell_id', 'unknown')
                success = usage.get('success', False)
                confidence = usage.get('confidence', 0.0)
                
                spell_performance[spell_id].append({
                    'success': success,
                    'confidence': confidence
                })
            
            # Find spells needing optimization
            optimization_candidates = []
            for spell_id, performances in spell_performance.items():
                spell_success_rate = sum(1 for p in performances if p['success']) / len(performances)
                avg_spell_confidence = np.mean([p['confidence'] for p in performances])
                
                if spell_success_rate < 0.7 or avg_spell_confidence < 0.6:
                    optimization_candidates.append({
                        'spell_id': spell_id,
                        'success_rate': spell_success_rate,
                        'avg_confidence': avg_spell_confidence,
                        'usage_count': len(performances)
                    })
            
            return {
                'success': True,
                'overall_success_rate': success_rate,
                'avg_confidence': avg_confidence,
                'confidence_stability': 1.0 - (confidence_std / avg_confidence) if avg_confidence > 0 else 0.0,
                'optimization_candidates': optimization_candidates,
                'total_spells_analyzed': len(spell_performance),
                'analysis_timestamp': int(time.time() * 1000)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing performance trends: {e}")
            return {
                'success': False,
                'error': f'Performance analysis failed: {str(e)}'
            }
    
    def suggest_optimizations(self, performance_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest specific optimizations based on performance analysis."""
        suggestions = []
        
        if not performance_analysis.get('success', False):
            return suggestions
        
        overall_success_rate = performance_analysis.get('overall_success_rate', 0.0)
        avg_confidence = performance_analysis.get('avg_confidence', 0.0)
        optimization_candidates = performance_analysis.get('optimization_candidates', [])
        
        # Global optimization suggestions
        if overall_success_rate < 0.8:
            suggestions.append({
                'type': 'global_threshold_adjustment',
                'priority': 'high',
                'description': 'Lower recognition thresholds to improve success rate',
                'expected_improvement': '10-15% success rate increase',
                'parameters': {
                    'confidence_threshold': max(0.4, avg_confidence - 0.1),
                    'gesture_threshold': 0.6,
                    'speech_threshold': 0.6
                }
            })
        
        if avg_confidence < 0.7:
            suggestions.append({
                'type': 'model_retraining',
                'priority': 'medium',
                'description': 'Retrain recognition models with recent user data',
                'expected_improvement': '5-10% confidence increase',
                'parameters': {
                    'training_samples_needed': 50,
                    'retraining_frequency': 'weekly'
                }
            })
        
        # Spell-specific optimization suggestions
        for candidate in optimization_candidates:
            if candidate['success_rate'] < 0.6:
                suggestions.append({
                    'type': 'spell_specific_optimization',
                    'priority': 'high',
                    'spell_id': candidate['spell_id'],
                    'description': f"Optimize {candidate['spell_id']} spell recognition",
                    'expected_improvement': '15-20% success rate increase',
                    'parameters': {
                        'personalized_training': True,
                        'gesture_sensitivity': 'increase',
                        'speech_alternatives': 'expand'
                    }
                })
        
        return suggestions


class FusionLearningEngine:
    """
    Main class for fusion learning and continuous optimization.
    
    Provides intelligent learning from user interactions, pattern recognition,
    and performance optimization for multimodal spell recognition.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.usage_analytics = SpellUsageAnalytics(
            spell_usage_history=[],
            performance_metrics={},
            context_correlations={},
            temporal_patterns={},
            user_feedback_data=[]
        )
        
        self.pattern_learner = UserPatternLearner(
            gesture_patterns={},
            speech_patterns={},
            temporal_patterns={},
            context_patterns={},
            adaptation_rate=0.1
        )
        
        self.director_integration = SensesDirectorBridge()
        self.ml_optimizer = MLOptimizer()
        
        # Load existing data
        self._load_analytics_data()
        self._load_pattern_data()
    
    def learn_user_patterns(self, spell_usage: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Learn user spell usage patterns for optimization and prediction.

        Args:
            spell_usage: Historical spell usage data with context

        Returns:
            Pattern learning results and optimization recommendations
        """
        try:
            if not spell_usage:
                return {
                    'success': False,
                    'error': 'No spell usage data provided'
                }
            
            # Update usage analytics
            self.usage_analytics.spell_usage_history.extend(spell_usage)
            
            # Keep only recent history (last 1000 entries)
            if len(self.usage_analytics.spell_usage_history) > 1000:
                self.usage_analytics.spell_usage_history = \
                    self.usage_analytics.spell_usage_history[-1000:]
            
            # Learn gesture patterns
            gesture_patterns = self._analyze_gesture_patterns(spell_usage)
            self.pattern_learner.gesture_patterns.update(gesture_patterns)
            
            # Learn speech patterns
            speech_patterns = self._analyze_speech_patterns(spell_usage)
            self.pattern_learner.speech_patterns.update(speech_patterns)
            
            # Learn temporal patterns
            temporal_patterns = self._analyze_temporal_patterns(spell_usage)
            self.pattern_learner.temporal_patterns.update(temporal_patterns)
            
            # Learn context patterns
            context_patterns = self._analyze_context_patterns(spell_usage)
            self.pattern_learner.context_patterns.update(context_patterns)
            
            # Update performance metrics
            self._update_performance_metrics()
            
            # Save learned patterns
            self._save_analytics_data()
            self._save_pattern_data()
            
            return {
                'success': True,
                'patterns_learned': {
                    'gesture_patterns': len(gesture_patterns),
                    'speech_patterns': len(speech_patterns),
                    'temporal_patterns': len(temporal_patterns),
                    'context_patterns': len(context_patterns)
                },
                'usage_entries_processed': len(spell_usage),
                'total_history_size': len(self.usage_analytics.spell_usage_history),
                'message': 'User patterns learned successfully'
            }
            
        except Exception as e:
            logger.error(f"Error learning user patterns: {e}")
            return {
                'success': False,
                'error': f'Pattern learning failed: {str(e)}'
            }

    def suggest_spell_improvements(self, spell_id: str) -> Dict[str, Any]:
        """
        Suggest improvements to existing spells based on usage analytics.

        Args:
            spell_id: ID of spell to analyze for improvements

        Returns:
            Improvement suggestions with confidence scores and rationale
        """
        try:
            # Find usage data for the specific spell
            spell_usage = [usage for usage in self.usage_analytics.spell_usage_history
                          if usage.get('spell_id') == spell_id]

            if not spell_usage:
                return {
                    'success': False,
                    'error': f'No usage data found for spell {spell_id}'
                }

            # Analyze spell performance
            total_attempts = len(spell_usage)
            successful_attempts = sum(1 for usage in spell_usage if usage.get('success', False))
            success_rate = successful_attempts / total_attempts

            # Analyze confidence scores
            confidences = [usage.get('confidence', 0.0) for usage in spell_usage]
            avg_confidence = np.mean(confidences)
            confidence_std = np.std(confidences)

            # Analyze failure patterns
            failures = [usage for usage in spell_usage if not usage.get('success', False)]
            failure_reasons = defaultdict(int)
            for failure in failures:
                reason = failure.get('failure_reason', 'unknown')
                failure_reasons[reason] += 1

            # Generate improvement suggestions
            suggestions = []

            # Success rate improvements
            if success_rate < 0.7:
                if failure_reasons.get('gesture_mismatch', 0) > failure_reasons.get('speech_mismatch', 0):
                    suggestions.append({
                        'type': 'gesture_sensitivity',
                        'priority': 'high',
                        'description': 'Increase gesture recognition sensitivity',
                        'confidence': 0.8,
                        'expected_improvement': '15-20% success rate increase'
                    })
                else:
                    suggestions.append({
                        'type': 'speech_alternatives',
                        'priority': 'high',
                        'description': 'Add alternative speech patterns',
                        'confidence': 0.7,
                        'expected_improvement': '10-15% success rate increase'
                    })

            # Confidence improvements
            if avg_confidence < 0.6:
                suggestions.append({
                    'type': 'threshold_adjustment',
                    'priority': 'medium',
                    'description': 'Lower confidence thresholds for this spell',
                    'confidence': 0.6,
                    'expected_improvement': '5-10% confidence increase'
                })

            # Consistency improvements
            if confidence_std > 0.2:
                suggestions.append({
                    'type': 'personalized_training',
                    'priority': 'medium',
                    'description': 'Add personalized training samples',
                    'confidence': 0.7,
                    'expected_improvement': 'More consistent recognition'
                })

            # Context-based improvements
            context_patterns = self._analyze_spell_context_patterns(spell_usage)
            if context_patterns:
                suggestions.append({
                    'type': 'context_optimization',
                    'priority': 'low',
                    'description': 'Optimize for common usage contexts',
                    'confidence': 0.5,
                    'expected_improvement': 'Better context-aware recognition',
                    'context_patterns': context_patterns
                })

            return {
                'success': True,
                'spell_id': spell_id,
                'current_performance': {
                    'success_rate': success_rate,
                    'avg_confidence': avg_confidence,
                    'total_attempts': total_attempts
                },
                'suggestions': suggestions,
                'failure_analysis': dict(failure_reasons),
                'analysis_timestamp': int(time.time() * 1000)
            }

        except Exception as e:
            logger.error(f"Error suggesting spell improvements: {e}")
            return {
                'success': False,
                'error': f'Spell improvement analysis failed: {str(e)}'
            }

    def predict_next_spell(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Predict likely next spells based on current context and patterns.

        Args:
            context: Current workspace and user context

        Returns:
            Ranked list of predicted spells with confidence scores
        """
        try:
            # Get current context from Director
            current_context = self.director_integration.get_current_context()
            enhanced_context = {**current_context, **context}

            # Analyze recent usage patterns
            recent_usage = self.usage_analytics.spell_usage_history[-50:]  # Last 50 spells

            # Find patterns in recent usage
            spell_sequences = self._extract_spell_sequences(recent_usage)

            # Get context-based predictions
            context_predictions = self._predict_from_context(enhanced_context)

            # Get temporal predictions
            temporal_predictions = self._predict_from_temporal_patterns(enhanced_context)

            # Combine and rank predictions
            all_predictions = {}

            # Add sequence-based predictions
            for sequence in spell_sequences:
                if len(sequence) >= 2:
                    last_spell = sequence[-1]
                    for next_spell in sequence[1:]:
                        if next_spell not in all_predictions:
                            all_predictions[next_spell] = {'confidence': 0.0, 'sources': []}
                        all_predictions[next_spell]['confidence'] += 0.3
                        all_predictions[next_spell]['sources'].append('sequence_pattern')

            # Add context-based predictions
            for prediction in context_predictions:
                spell_id = prediction['spell_id']
                if spell_id not in all_predictions:
                    all_predictions[spell_id] = {'confidence': 0.0, 'sources': []}
                all_predictions[spell_id]['confidence'] += prediction['confidence'] * 0.4
                all_predictions[spell_id]['sources'].append('context_pattern')

            # Add temporal predictions
            for prediction in temporal_predictions:
                spell_id = prediction['spell_id']
                if spell_id not in all_predictions:
                    all_predictions[spell_id] = {'confidence': 0.0, 'sources': []}
                all_predictions[spell_id]['confidence'] += prediction['confidence'] * 0.3
                all_predictions[spell_id]['sources'].append('temporal_pattern')

            # Normalize and rank predictions
            max_confidence = max([p['confidence'] for p in all_predictions.values()]) if all_predictions else 1.0

            ranked_predictions = []
            for spell_id, prediction_data in all_predictions.items():
                normalized_confidence = prediction_data['confidence'] / max_confidence
                ranked_predictions.append({
                    'spell_id': spell_id,
                    'confidence': min(1.0, normalized_confidence),
                    'prediction_sources': prediction_data['sources'],
                    'context_match': self._calculate_context_match(spell_id, enhanced_context)
                })

            # Sort by confidence
            ranked_predictions.sort(key=lambda x: x['confidence'], reverse=True)

            # Return top 5 predictions
            return ranked_predictions[:5]

        except Exception as e:
            logger.error(f"Error predicting next spell: {e}")
            return []

    def optimize_spell_parameters(self, spell_performance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize spell parameters based on performance data and ML analysis.

        Args:
            spell_performance: Performance metrics for spell optimization

        Returns:
            Optimized parameters and expected performance improvements
        """
        try:
            spell_id = spell_performance.get('spell_id')
            if not spell_id:
                return {
                    'success': False,
                    'error': 'No spell ID provided for optimization'
                }

            # Analyze current performance
            performance_analysis = self.ml_optimizer.analyze_performance_trends(self.usage_analytics)

            if not performance_analysis.get('success', False):
                return {
                    'success': False,
                    'error': 'Failed to analyze performance trends'
                }

            # Get optimization suggestions
            suggestions = self.ml_optimizer.suggest_optimizations(performance_analysis)

            # Find spell-specific suggestions
            spell_suggestions = [s for s in suggestions if s.get('spell_id') == spell_id]

            # Generate optimized parameters
            optimized_params = {}
            expected_improvements = []

            for suggestion in spell_suggestions:
                if suggestion['type'] == 'spell_specific_optimization':
                    params = suggestion.get('parameters', {})

                    if params.get('personalized_training'):
                        optimized_params['enable_personalized_training'] = True
                        expected_improvements.append('15-20% accuracy improvement')

                    if params.get('gesture_sensitivity') == 'increase':
                        optimized_params['gesture_confidence_threshold'] = 0.5
                        expected_improvements.append('Better gesture recognition')

                    if params.get('speech_alternatives') == 'expand':
                        optimized_params['enable_speech_alternatives'] = True
                        expected_improvements.append('More flexible speech patterns')

            # Add global optimizations if no spell-specific ones found
            if not spell_suggestions:
                global_suggestions = [s for s in suggestions if s['type'] == 'global_threshold_adjustment']
                for suggestion in global_suggestions:
                    params = suggestion.get('parameters', {})
                    optimized_params.update(params)
                    expected_improvements.append(suggestion.get('expected_improvement', 'Performance improvement'))

            # Apply learning rate adjustments
            if spell_id in self.pattern_learner.gesture_patterns:
                gesture_success_rate = self.pattern_learner.gesture_patterns[spell_id].get('success_rate', 0.5)
                if gesture_success_rate < 0.6:
                    optimized_params['gesture_learning_rate'] = min(0.3, self.pattern_learner.adaptation_rate * 1.5)

            if spell_id in self.pattern_learner.speech_patterns:
                speech_success_rate = self.pattern_learner.speech_patterns[spell_id].get('success_rate', 0.5)
                if speech_success_rate < 0.6:
                    optimized_params['speech_learning_rate'] = min(0.3, self.pattern_learner.adaptation_rate * 1.5)

            return {
                'success': True,
                'spell_id': spell_id,
                'optimized_parameters': optimized_params,
                'expected_improvements': expected_improvements,
                'optimization_confidence': 0.7,
                'suggestions_applied': len(spell_suggestions) + len([s for s in suggestions if s['type'] == 'global_threshold_adjustment']),
                'optimization_timestamp': int(time.time() * 1000)
            }

        except Exception as e:
            logger.error(f"Error optimizing spell parameters: {e}")
            return {
                'success': False,
                'error': f'Parameter optimization failed: {str(e)}'
            }

    def train_fusion_model(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train ML model for improved multimodal fusion."""
        try:
            if not SKLEARN_AVAILABLE:
                return {
                    'success': False,
                    'error': 'Scikit-learn not available for ML training'
                }

            if len(training_data) < 20:
                return {
                    'success': False,
                    'error': 'Insufficient training data (need at least 20 samples)'
                }

            # Extract features and labels from training data
            features = []
            labels = []

            for sample in training_data:
                # Extract multimodal features
                gesture_confidence = sample.get('gesture_confidence', 0.0)
                speech_confidence = sample.get('speech_confidence', 0.0)
                context_boost = sample.get('context_boost', 0.0)
                temporal_factor = sample.get('temporal_factor', 0.0)

                feature_vector = [gesture_confidence, speech_confidence, context_boost, temporal_factor]
                features.append(feature_vector)

                # Label is whether the spell was successfully recognized
                labels.append(1 if sample.get('success', False) else 0)

            # Train a simple classifier
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import accuracy_score

            X = np.array(features)
            y = np.array(labels)

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train model
            model = RandomForestClassifier(n_estimators=50, random_state=42)
            model.fit(X_train, y_train)

            # Evaluate
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)

            # Store model (in real implementation, would save to disk)
            self.ml_optimizer.optimization_strategies['fusion_model'] = {
                'model': model,
                'accuracy': accuracy,
                'training_samples': len(training_data),
                'trained_at': int(time.time() * 1000)
            }

            return {
                'success': True,
                'model_accuracy': accuracy,
                'training_samples': len(training_data),
                'test_samples': len(X_test),
                'model_type': 'RandomForestClassifier',
                'message': 'Fusion model trained successfully'
            }

        except Exception as e:
            logger.error(f"Error training fusion model: {e}")
            return {
                'success': False,
                'error': f'Model training failed: {str(e)}'
            }

    def evaluate_model_performance(self) -> Dict[str, Any]:
        """Evaluate current ML model performance and suggest improvements."""
        try:
            # Analyze recent performance
            performance_analysis = self.ml_optimizer.analyze_performance_trends(self.usage_analytics)

            if not performance_analysis.get('success', False):
                return {
                    'success': False,
                    'error': 'Failed to analyze performance'
                }

            # Get current model info
            fusion_model_info = self.ml_optimizer.optimization_strategies.get('fusion_model', {})

            # Calculate performance metrics
            overall_success_rate = performance_analysis.get('overall_success_rate', 0.0)
            avg_confidence = performance_analysis.get('avg_confidence', 0.0)
            confidence_stability = performance_analysis.get('confidence_stability', 0.0)

            # Determine model health
            model_health = 'good'
            if overall_success_rate < 0.7:
                model_health = 'poor'
            elif overall_success_rate < 0.8:
                model_health = 'fair'

            # Generate improvement suggestions
            improvement_suggestions = []

            if overall_success_rate < 0.8:
                improvement_suggestions.append({
                    'type': 'retrain_model',
                    'priority': 'high',
                    'description': 'Retrain model with recent user data'
                })

            if avg_confidence < 0.7:
                improvement_suggestions.append({
                    'type': 'confidence_calibration',
                    'priority': 'medium',
                    'description': 'Recalibrate confidence thresholds'
                })

            if confidence_stability < 0.6:
                improvement_suggestions.append({
                    'type': 'stability_improvement',
                    'priority': 'medium',
                    'description': 'Improve model consistency'
                })

            return {
                'success': True,
                'model_health': model_health,
                'performance_metrics': {
                    'success_rate': overall_success_rate,
                    'avg_confidence': avg_confidence,
                    'confidence_stability': confidence_stability
                },
                'model_info': fusion_model_info,
                'improvement_suggestions': improvement_suggestions,
                'evaluation_timestamp': int(time.time() * 1000)
            }

        except Exception as e:
            logger.error(f"Error evaluating model performance: {e}")
            return {
                'success': False,
                'error': f'Model evaluation failed: {str(e)}'
            }

    # Helper methods for pattern analysis
    def _analyze_gesture_patterns(self, spell_usage: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze gesture usage patterns."""
        gesture_patterns = defaultdict(lambda: {'count': 0, 'success_count': 0, 'confidences': []})

        for usage in spell_usage:
            gesture = usage.get('gesture_component', 'unknown')
            success = usage.get('success', False)
            confidence = usage.get('gesture_confidence', 0.0)

            gesture_patterns[gesture]['count'] += 1
            if success:
                gesture_patterns[gesture]['success_count'] += 1
            gesture_patterns[gesture]['confidences'].append(confidence)

        # Calculate success rates and average confidences
        result = {}
        for gesture, data in gesture_patterns.items():
            result[gesture] = {
                'usage_count': data['count'],
                'success_rate': data['success_count'] / data['count'] if data['count'] > 0 else 0.0,
                'avg_confidence': np.mean(data['confidences']) if data['confidences'] else 0.0
            }

        return result

    def _analyze_speech_patterns(self, spell_usage: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze speech usage patterns."""
        speech_patterns = defaultdict(lambda: {'count': 0, 'success_count': 0, 'confidences': []})

        for usage in spell_usage:
            speech = usage.get('speech_component', 'unknown').lower()
            success = usage.get('success', False)
            confidence = usage.get('speech_confidence', 0.0)

            speech_patterns[speech]['count'] += 1
            if success:
                speech_patterns[speech]['success_count'] += 1
            speech_patterns[speech]['confidences'].append(confidence)

        # Calculate success rates and average confidences
        result = {}
        for speech, data in speech_patterns.items():
            result[speech] = {
                'usage_count': data['count'],
                'success_rate': data['success_count'] / data['count'] if data['count'] > 0 else 0.0,
                'avg_confidence': np.mean(data['confidences']) if data['confidences'] else 0.0
            }

        return result

    def _analyze_temporal_patterns(self, spell_usage: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze temporal usage patterns."""
        temporal_patterns = {}

        # Group by hour of day
        hourly_usage = defaultdict(int)
        for usage in spell_usage:
            timestamp = usage.get('timestamp', 0)
            if timestamp > 0:
                hour = time.localtime(timestamp / 1000).tm_hour
                hourly_usage[hour] += 1

        temporal_patterns['hourly_distribution'] = dict(hourly_usage)

        # Find peak usage hours
        if hourly_usage:
            peak_hour = max(hourly_usage.items(), key=lambda x: x[1])
            temporal_patterns['peak_hour'] = peak_hour[0]
            temporal_patterns['peak_usage_count'] = peak_hour[1]

        return temporal_patterns

    def _analyze_context_patterns(self, spell_usage: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze context usage patterns."""
        context_patterns = defaultdict(lambda: {'count': 0, 'success_count': 0})

        for usage in spell_usage:
            context = usage.get('context', {})
            panel = context.get('current_panel', 'unknown')
            success = usage.get('success', False)

            context_patterns[panel]['count'] += 1
            if success:
                context_patterns[panel]['success_count'] += 1

        # Calculate success rates
        result = {}
        for panel, data in context_patterns.items():
            result[panel] = {
                'usage_count': data['count'],
                'success_rate': data['success_count'] / data['count'] if data['count'] > 0 else 0.0
            }

        return result

    def _update_performance_metrics(self):
        """Update overall performance metrics."""
        if not self.usage_analytics.spell_usage_history:
            return

        total_attempts = len(self.usage_analytics.spell_usage_history)
        successful_attempts = sum(1 for usage in self.usage_analytics.spell_usage_history
                                if usage.get('success', False))

        self.usage_analytics.performance_metrics.update({
            'total_attempts': total_attempts,
            'successful_attempts': successful_attempts,
            'overall_success_rate': successful_attempts / total_attempts if total_attempts > 0 else 0.0,
            'last_updated': int(time.time() * 1000)
        })

    def _extract_spell_sequences(self, usage_history: List[Dict[str, Any]]) -> List[List[str]]:
        """Extract spell usage sequences for pattern recognition."""
        sequences = []
        current_sequence = []

        for usage in usage_history:
            spell_id = usage.get('spell_id', 'unknown')
            timestamp = usage.get('timestamp', 0)

            # Start new sequence if gap is too large (> 5 minutes)
            if current_sequence and len(current_sequence) > 0:
                last_timestamp = usage_history[usage_history.index(usage) - 1].get('timestamp', 0)
                if timestamp - last_timestamp > 300000:  # 5 minutes
                    if len(current_sequence) >= 2:
                        sequences.append(current_sequence)
                    current_sequence = []

            current_sequence.append(spell_id)

        # Add final sequence
        if len(current_sequence) >= 2:
            sequences.append(current_sequence)

        return sequences

    def _predict_from_context(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict spells based on current context."""
        predictions = []

        current_panel = context.get('current_panel', 'orchestr8')

        # Simple context-based predictions
        if current_panel == 'orchestr8':
            predictions.extend([
                {'spell_id': 'library_navigation', 'confidence': 0.6},
                {'spell_id': 'conversation_start', 'confidence': 0.5}
            ])
        elif current_panel == 'integr8':
            predictions.extend([
                {'spell_id': 'file_open', 'confidence': 0.7},
                {'spell_id': 'code_navigation', 'confidence': 0.6}
            ])

        return predictions

    def _predict_from_temporal_patterns(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict spells based on temporal patterns."""
        predictions = []

        current_hour = time.localtime().tm_hour

        # Simple temporal predictions
        if 9 <= current_hour <= 17:  # Work hours
            predictions.extend([
                {'spell_id': 'productivity_spell', 'confidence': 0.4},
                {'spell_id': 'focus_mode', 'confidence': 0.3}
            ])
        else:  # Off hours
            predictions.extend([
                {'spell_id': 'casual_navigation', 'confidence': 0.3},
                {'spell_id': 'exploration_mode', 'confidence': 0.2}
            ])

        return predictions

    def _calculate_context_match(self, spell_id: str, context: Dict[str, Any]) -> float:
        """Calculate how well a spell matches the current context."""
        # Simplified context matching
        current_panel = context.get('current_panel', 'orchestr8')

        # Panel-specific spell matching
        panel_spell_affinity = {
            'orchestr8': ['library_navigation', 'conversation_start', 'ai_assistance'],
            'integr8': ['file_open', 'code_navigation', 'editor_commands'],
            'communic8': ['message_send', 'contact_search', 'communication'],
            'actu8': ['task_create', 'productivity', 'scheduling'],
            'cre8': ['design_tools', 'creative_mode', 'art_commands'],
            'innov8': ['experiment', 'prototype', 'innovation']
        }

        if spell_id in panel_spell_affinity.get(current_panel, []):
            return 0.8

        return 0.3  # Default low match

    def _analyze_spell_context_patterns(self, spell_usage: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze context patterns for a specific spell."""
        context_analysis = defaultdict(int)

        for usage in spell_usage:
            context = usage.get('context', {})
            panel = context.get('current_panel', 'unknown')
            context_analysis[panel] += 1

        return dict(context_analysis)

    def _save_analytics_data(self):
        """Save analytics data to disk."""
        try:
            analytics_path = self.data_dir / "fusion_analytics.json"
            with open(analytics_path, 'w') as f:
                json.dump(self.usage_analytics.to_dict(), f, indent=2)
        except Exception as e:
            logger.error(f"Error saving analytics data: {e}")

    def _load_analytics_data(self):
        """Load analytics data from disk."""
        try:
            analytics_path = self.data_dir / "fusion_analytics.json"
            if analytics_path.exists():
                with open(analytics_path, 'r') as f:
                    data = json.load(f)
                    self.usage_analytics = SpellUsageAnalytics.from_dict(data)
        except Exception as e:
            logger.error(f"Error loading analytics data: {e}")

    def _save_pattern_data(self):
        """Save pattern data to disk."""
        try:
            pattern_path = self.data_dir / "fusion_patterns.json"
            with open(pattern_path, 'w') as f:
                json.dump(self.pattern_learner.to_dict(), f, indent=2)
        except Exception as e:
            logger.error(f"Error saving pattern data: {e}")

    def _load_pattern_data(self):
        """Load pattern data from disk."""
        try:
            pattern_path = self.data_dir / "fusion_patterns.json"
            if pattern_path.exists():
                with open(pattern_path, 'r') as f:
                    data = json.load(f)
                    self.pattern_learner = UserPatternLearner.from_dict(data)
        except Exception as e:
            logger.error(f"Error loading pattern data: {e}")


# Module-level functions for integration with existing senses system
def create_fusion_learning_engine(data_dir: str = "data") -> Dict[str, Any]:
    """Create a new fusion learning engine instance."""
    try:
        engine = FusionLearningEngine(data_dir=data_dir)
        return {
            'success': True,
            'engine': engine,
            'sklearn_available': SKLEARN_AVAILABLE,
            'message': 'Fusion learning engine created successfully'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to create fusion learning engine: {str(e)}'
        }
