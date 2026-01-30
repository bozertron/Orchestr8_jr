"""
Workflow Optimization Analyzer for Director Intelligence.

This module analyzes user workflows to identify efficiency improvements,
bottlenecks, and optimization opportunities for common workflow patterns.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
import time
import statistics
from collections import defaultdict, Counter
from .user_context import UserContext
from .pattern_recognition import WorkflowPattern, BehavioralInsight


@dataclass
class OptimizationRecommendation:
    """Represents a workflow optimization recommendation."""
    id: str
    workflow_id: str
    type: str  # "eliminate_step", "reorder_steps", "batch_operations", "automate", "tool_switch"
    title: str
    description: str
    current_efficiency: float
    projected_efficiency: float
    implementation_effort: str  # "low", "medium", "high"
    time_savings_per_execution: int  # seconds
    confidence: float
    evidence: List[str] = field(default_factory=list)
    implementation_steps: List[str] = field(default_factory=list)


@dataclass
class WorkflowMetrics:
    """Metrics for workflow analysis."""
    total_execution_time: int  # milliseconds
    step_durations: List[int]
    context_switches: int
    idle_time: int
    tool_changes: int
    efficiency_score: float
    bottleneck_steps: List[int] = field(default_factory=list)


class WorkflowOptimizer:
    """
    Workflow optimization analyzer for identifying efficiency improvements.
    
    This class analyzes workflow patterns to identify bottlenecks, inefficiencies,
    and opportunities for optimization across multi-panel workflows.
    """
    
    def __init__(self):
        self.optimization_history: List[Dict[str, Any]] = []
        self.workflow_metrics: Dict[str, WorkflowMetrics] = {}
        self.baseline_metrics: Dict[str, float] = {}
        
        # Optimization thresholds
        self.thresholds = {
            'min_efficiency_improvement': 0.15,  # 15% improvement
            'bottleneck_threshold': 2.0,  # 2x average step time
            'context_switch_penalty': 0.1,  # 10% efficiency penalty per switch
            'idle_time_threshold': 30000,  # 30 seconds
            'min_execution_count': 3,  # Minimum executions to analyze
        }
    
    def analyze_workflow_efficiency(self, patterns: List[WorkflowPattern], 
                                  context: UserContext,
                                  context_history: List[UserContext]) -> Dict[str, Any]:
        """
        Analyze workflow efficiency and generate optimization recommendations.
        
        Args:
            patterns: Detected workflow patterns
            context: Current user context
            context_history: Historical context data
            
        Returns:
            Dictionary containing efficiency analysis and recommendations
        """
        analysis_results = {
            'workflow_metrics': {},
            'optimization_recommendations': [],
            'efficiency_trends': {},
            'bottleneck_analysis': {},
            'overall_efficiency_score': 0.0
        }
        
        try:
            # Calculate metrics for each workflow pattern
            for pattern in patterns:
                if pattern.frequency >= self.thresholds['min_execution_count']:
                    metrics = self._calculate_workflow_metrics(pattern, context, context_history)
                    analysis_results['workflow_metrics'][pattern.id] = self._metrics_to_dict(metrics)
                    
                    # Generate optimization recommendations
                    recommendations = self._generate_optimization_recommendations(pattern, metrics, context)
                    analysis_results['optimization_recommendations'].extend(
                        [self._recommendation_to_dict(rec) for rec in recommendations]
                    )
            
            # Analyze efficiency trends
            efficiency_trends = self._analyze_efficiency_trends(patterns, context_history)
            analysis_results['efficiency_trends'] = efficiency_trends
            
            # Perform bottleneck analysis
            bottleneck_analysis = self._analyze_workflow_bottlenecks(patterns, context)
            analysis_results['bottleneck_analysis'] = bottleneck_analysis
            
            # Calculate overall efficiency score
            if patterns:
                overall_score = statistics.mean([p.efficiency_score for p in patterns])
                analysis_results['overall_efficiency_score'] = overall_score
            
            # Update optimization history
            self._update_optimization_history(analysis_results)
            
        except Exception as e:
            analysis_results['error'] = str(e)
            analysis_results['overall_efficiency_score'] = 0.0
        
        return analysis_results
    
    def _calculate_workflow_metrics(self, pattern: WorkflowPattern, 
                                  context: UserContext,
                                  history: List[UserContext]) -> WorkflowMetrics:
        """Calculate detailed metrics for a workflow pattern."""
        # Estimate execution time based on pattern complexity
        estimated_time = len(pattern.steps) * 60000  # 1 minute per step base
        
        # Calculate step durations (estimated)
        step_durations = []
        for i, step in enumerate(pattern.steps):
            # Base duration with variation based on step type
            base_duration = 60000  # 1 minute
            
            if step.get('zone') == 'orchestr8':  # AI assistant - variable time
                duration = base_duration * 1.5
            elif step.get('zone') == 'integr8':  # Code editor - longer tasks
                duration = base_duration * 2.0
            elif step.get('zone') == 'communic8':  # Communication - quick
                duration = base_duration * 0.5
            else:
                duration = base_duration
            
            step_durations.append(int(duration))
        
        # Count context switches
        context_switches = max(0, len(pattern.steps) - 1)
        
        # Estimate idle time based on context switches
        idle_time = context_switches * 5000  # 5 seconds per switch
        
        # Count tool changes (simplified)
        tool_changes = len(set(step.get('tool', '') for step in pattern.steps if step.get('tool')))
        
        # Calculate efficiency score
        total_time = sum(step_durations) + idle_time
        productive_time = sum(step_durations)
        efficiency_score = productive_time / total_time if total_time > 0 else 0.0
        
        # Identify bottleneck steps
        if step_durations:
            avg_duration = statistics.mean(step_durations)
            bottleneck_steps = [
                i for i, duration in enumerate(step_durations)
                if duration > avg_duration * self.thresholds['bottleneck_threshold']
            ]
        else:
            bottleneck_steps = []
        
        return WorkflowMetrics(
            total_execution_time=total_time,
            step_durations=step_durations,
            context_switches=context_switches,
            idle_time=idle_time,
            tool_changes=tool_changes,
            efficiency_score=efficiency_score,
            bottleneck_steps=bottleneck_steps
        )
    
    def _generate_optimization_recommendations(self, pattern: WorkflowPattern,
                                             metrics: WorkflowMetrics,
                                             context: UserContext) -> List[OptimizationRecommendation]:
        """Generate optimization recommendations for a workflow."""
        recommendations = []
        
        # Recommend eliminating unnecessary steps
        if len(pattern.steps) > 5:  # Long workflow
            recommendations.append(OptimizationRecommendation(
                id=f"eliminate_{pattern.id}",
                workflow_id=pattern.id,
                type="eliminate_step",
                title="Eliminate Unnecessary Steps",
                description=f"Consider combining or eliminating steps in {pattern.name}",
                current_efficiency=pattern.efficiency_score,
                projected_efficiency=min(1.0, pattern.efficiency_score + 0.2),
                implementation_effort="medium",
                time_savings_per_execution=60,  # 1 minute saved
                confidence=0.7,
                evidence=[f"Workflow has {len(pattern.steps)} steps", "Long workflows often have redundancy"],
                implementation_steps=[
                    "Review each step for necessity",
                    "Combine similar operations",
                    "Remove duplicate actions"
                ]
            ))
        
        # Recommend reducing context switches
        if metrics.context_switches > 3:
            recommendations.append(OptimizationRecommendation(
                id=f"reduce_switches_{pattern.id}",
                workflow_id=pattern.id,
                type="batch_operations",
                title="Batch Similar Operations",
                description=f"Reduce context switching by batching similar tasks",
                current_efficiency=pattern.efficiency_score,
                projected_efficiency=min(1.0, pattern.efficiency_score + 0.15),
                implementation_effort="low",
                time_savings_per_execution=metrics.context_switches * 5,  # 5 seconds per switch saved
                confidence=0.8,
                evidence=[f"{metrics.context_switches} context switches detected", "Context switching reduces efficiency"],
                implementation_steps=[
                    "Group similar tasks together",
                    "Complete all tasks in one application before switching",
                    "Use workspace organization features"
                ]
            ))
        
        # Recommend automation for highly repetitive workflows
        if pattern.frequency > 8:  # Very frequent pattern
            recommendations.append(OptimizationRecommendation(
                id=f"automate_{pattern.id}",
                workflow_id=pattern.id,
                type="automate",
                title="Automate Repetitive Workflow",
                description=f"Create automation for this frequently used workflow",
                current_efficiency=pattern.efficiency_score,
                projected_efficiency=min(1.0, pattern.efficiency_score + 0.3),
                implementation_effort="high",
                time_savings_per_execution=int(metrics.total_execution_time * 0.5 / 1000),  # 50% time savings
                confidence=0.6,
                evidence=[f"Executed {pattern.frequency} times", "High repetition indicates automation potential"],
                implementation_steps=[
                    "Create workflow template",
                    "Set up keyboard shortcuts",
                    "Use automation tools where available"
                ]
            ))
        
        # Recommend tool optimization for bottleneck steps
        if metrics.bottleneck_steps:
            recommendations.append(OptimizationRecommendation(
                id=f"optimize_tools_{pattern.id}",
                workflow_id=pattern.id,
                type="tool_switch",
                title="Optimize Bottleneck Steps",
                description=f"Optimize tools used in slow steps of {pattern.name}",
                current_efficiency=pattern.efficiency_score,
                projected_efficiency=min(1.0, pattern.efficiency_score + 0.25),
                implementation_effort="medium",
                time_savings_per_execution=120,  # 2 minutes saved
                confidence=0.7,
                evidence=[f"{len(metrics.bottleneck_steps)} bottleneck steps identified"],
                implementation_steps=[
                    "Identify alternative tools for slow steps",
                    "Learn advanced features of current tools",
                    "Consider workflow reordering"
                ]
            ))
        
        return recommendations
    
    def _analyze_efficiency_trends(self, patterns: List[WorkflowPattern], 
                                 history: List[UserContext]) -> Dict[str, Any]:
        """Analyze efficiency trends over time."""
        trends = {
            'overall_trend': 'stable',
            'trend_direction': 0.0,
            'efficiency_variance': 0.0,
            'improvement_opportunities': []
        }
        
        if len(history) < 5:
            return trends
        
        # Calculate efficiency scores over time
        efficiency_scores = []
        for ctx in history[-10:]:  # Last 10 contexts
            score = ctx.get_productivity_score()
            efficiency_scores.append(score)
        
        if len(efficiency_scores) >= 5:
            # Calculate trend
            recent_avg = statistics.mean(efficiency_scores[-3:])
            earlier_avg = statistics.mean(efficiency_scores[:3])
            trend_direction = recent_avg - earlier_avg
            
            if trend_direction > 0.1:
                trends['overall_trend'] = 'improving'
            elif trend_direction < -0.1:
                trends['overall_trend'] = 'declining'
            
            trends['trend_direction'] = trend_direction
            trends['efficiency_variance'] = statistics.stdev(efficiency_scores) if len(efficiency_scores) > 1 else 0.0
            
            # Identify improvement opportunities
            if trends['overall_trend'] == 'declining':
                trends['improvement_opportunities'].append("Review recent workflow changes")
                trends['improvement_opportunities'].append("Identify factors causing efficiency decline")
            elif trends['efficiency_variance'] > 0.2:
                trends['improvement_opportunities'].append("Standardize workflow processes")
                trends['improvement_opportunities'].append("Reduce variability in execution")
        
        return trends
    
    def _analyze_workflow_bottlenecks(self, patterns: List[WorkflowPattern], 
                                    context: UserContext) -> Dict[str, Any]:
        """Analyze bottlenecks across all workflows."""
        bottlenecks = {
            'common_bottleneck_zones': [],
            'common_bottleneck_tools': [],
            'bottleneck_patterns': [],
            'optimization_priority': []
        }
        
        # Analyze zone-based bottlenecks
        zone_times = defaultdict(list)
        for pattern in patterns:
            for step in pattern.steps:
                zone = step.get('zone')
                if zone:
                    # Estimate time for this zone (simplified)
                    estimated_time = 60  # seconds
                    zone_times[zone].append(estimated_time)
        
        # Find zones with consistently high times
        for zone, times in zone_times.items():
            if len(times) >= 3 and statistics.mean(times) > 90:  # More than 1.5 minutes average
                bottlenecks['common_bottleneck_zones'].append({
                    'zone': zone,
                    'average_time': statistics.mean(times),
                    'frequency': len(times)
                })
        
        # Analyze tool-based bottlenecks
        tool_usage = context.tool_usage_patterns
        if tool_usage:
            # Find overused tools that might be bottlenecks
            total_usage = sum(tool_usage.values())
            for tool, usage in tool_usage.items():
                if usage / total_usage > 0.4:  # More than 40% of usage
                    bottlenecks['common_bottleneck_tools'].append({
                        'tool': tool,
                        'usage_percentage': (usage / total_usage) * 100,
                        'usage_count': usage
                    })
        
        # Prioritize optimization efforts
        if bottlenecks['common_bottleneck_zones']:
            bottlenecks['optimization_priority'].append("Focus on optimizing high-time zones")
        if bottlenecks['common_bottleneck_tools']:
            bottlenecks['optimization_priority'].append("Diversify tool usage or optimize frequent tools")
        
        return bottlenecks

    def _metrics_to_dict(self, metrics: WorkflowMetrics) -> Dict[str, Any]:
        """Convert WorkflowMetrics to dictionary."""
        return {
            'total_execution_time': metrics.total_execution_time,
            'step_durations': metrics.step_durations,
            'context_switches': metrics.context_switches,
            'idle_time': metrics.idle_time,
            'tool_changes': metrics.tool_changes,
            'efficiency_score': metrics.efficiency_score,
            'bottleneck_steps': metrics.bottleneck_steps
        }

    def _recommendation_to_dict(self, rec: OptimizationRecommendation) -> Dict[str, Any]:
        """Convert OptimizationRecommendation to dictionary."""
        return {
            'id': rec.id,
            'workflow_id': rec.workflow_id,
            'type': rec.type,
            'title': rec.title,
            'description': rec.description,
            'current_efficiency': rec.current_efficiency,
            'projected_efficiency': rec.projected_efficiency,
            'implementation_effort': rec.implementation_effort,
            'time_savings_per_execution': rec.time_savings_per_execution,
            'confidence': rec.confidence,
            'evidence': rec.evidence,
            'implementation_steps': rec.implementation_steps
        }

    def _update_optimization_history(self, results: Dict[str, Any]) -> None:
        """Update optimization analysis history."""
        history_entry = {
            'timestamp': int(time.time() * 1000),
            'workflows_analyzed': len(results.get('workflow_metrics', {})),
            'recommendations_generated': len(results.get('optimization_recommendations', [])),
            'overall_efficiency': results.get('overall_efficiency_score', 0.0)
        }

        self.optimization_history.append(history_entry)

        # Keep only recent history (last 50 entries)
        if len(self.optimization_history) > 50:
            self.optimization_history = self.optimization_history[-50:]

    def get_optimization_summary(self) -> Dict[str, Any]:
        """Get a summary of optimization analysis history."""
        if not self.optimization_history:
            return {
                'total_analyses': 0,
                'average_efficiency': 0.0,
                'total_recommendations': 0,
                'efficiency_trend': 'no_data'
            }

        total_analyses = len(self.optimization_history)
        efficiency_scores = [entry['overall_efficiency'] for entry in self.optimization_history]
        average_efficiency = statistics.mean(efficiency_scores) if efficiency_scores else 0.0
        total_recommendations = sum(entry['recommendations_generated'] for entry in self.optimization_history)

        # Calculate efficiency trend
        if len(efficiency_scores) >= 5:
            recent_avg = statistics.mean(efficiency_scores[-3:])
            earlier_avg = statistics.mean(efficiency_scores[:3])
            trend_change = recent_avg - earlier_avg

            if trend_change > 0.05:
                efficiency_trend = 'improving'
            elif trend_change < -0.05:
                efficiency_trend = 'declining'
            else:
                efficiency_trend = 'stable'
        else:
            efficiency_trend = 'insufficient_data'

        return {
            'total_analyses': total_analyses,
            'average_efficiency': average_efficiency,
            'total_recommendations': total_recommendations,
            'efficiency_trend': efficiency_trend,
            'recent_efficiency': efficiency_scores[-1] if efficiency_scores else 0.0
        }
