"""
Advanced Pattern Recognition Engine for Director Intelligence.

This module implements sophisticated pattern recognition algorithms to identify
complex multi-panel usage patterns, workflow opportunities, and behavioral insights.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
import time
import statistics
from collections import defaultdict, Counter
from .user_context import UserContext


@dataclass
class WorkflowPattern:
    """Represents a detected workflow pattern."""
    id: str
    name: str
    description: str
    steps: List[Dict[str, Any]]
    frequency: int
    confidence: float
    efficiency_score: float
    last_seen: int
    optimization_suggestions: List[str] = field(default_factory=list)


@dataclass
class BehavioralInsight:
    """Represents a behavioral insight derived from pattern analysis."""
    type: str  # "efficiency", "habit", "bottleneck", "opportunity"
    title: str
    description: str
    evidence: List[str]
    confidence: float
    impact_score: float  # Potential impact on productivity
    actionable_suggestions: List[str] = field(default_factory=list)


class AdvancedPatternRecognition:
    """
    Advanced pattern recognition engine for identifying complex behavioral patterns.
    
    This class analyzes user behavior across multiple panels to identify:
    - Multi-panel workflow patterns
    - Efficiency bottlenecks
    - Optimization opportunities
    - Behavioral habits and trends
    """
    
    def __init__(self):
        self.detected_patterns: Dict[str, WorkflowPattern] = {}
        self.behavioral_insights: List[BehavioralInsight] = []
        self.pattern_history: List[Dict[str, Any]] = []
        self.efficiency_baselines: Dict[str, float] = {}
        
        # Pattern detection thresholds
        self.thresholds = {
            'min_pattern_frequency': 3,
            'min_confidence_score': 0.6,
            'workflow_time_window': 1800000,  # 30 minutes
            'efficiency_improvement_threshold': 0.15,  # 15% improvement potential
            'bottleneck_detection_threshold': 2.0,  # 2x longer than average
        }
    
    def analyze_patterns(self, context: UserContext, context_history: List[UserContext]) -> Dict[str, Any]:
        """
        Perform comprehensive pattern analysis on user context and history.
        
        Args:
            context: Current user context
            context_history: Historical context data
            
        Returns:
            Dictionary containing detected patterns and insights
        """
        results = {
            'workflow_patterns': [],
            'behavioral_insights': [],
            'efficiency_analysis': {},
            'optimization_opportunities': [],
            'pattern_confidence': 0.0
        }
        
        try:
            # Detect multi-panel workflow patterns
            workflow_patterns = self._detect_workflow_patterns(context, context_history)
            results['workflow_patterns'] = [self._pattern_to_dict(p) for p in workflow_patterns]
            
            # Analyze behavioral insights
            insights = self._analyze_behavioral_insights(context, context_history)
            results['behavioral_insights'] = [self._insight_to_dict(i) for i in insights]
            
            # Perform efficiency analysis
            efficiency_analysis = self._analyze_efficiency_patterns(context, context_history)
            results['efficiency_analysis'] = efficiency_analysis
            
            # Identify optimization opportunities
            opportunities = self._identify_optimization_opportunities(context, workflow_patterns, insights)
            results['optimization_opportunities'] = opportunities
            
            # Calculate overall pattern confidence
            if workflow_patterns:
                avg_confidence = statistics.mean([p.confidence for p in workflow_patterns])
                results['pattern_confidence'] = avg_confidence
            
            # Update pattern history
            self._update_pattern_history(results)
            
        except Exception as e:
            results['error'] = str(e)
            results['pattern_confidence'] = 0.0
        
        return results
    
    def _detect_workflow_patterns(self, context: UserContext, history: List[UserContext]) -> List[WorkflowPattern]:
        """Detect multi-panel workflow patterns from user behavior."""
        patterns = []
        
        # Analyze zone transition sequences
        zone_sequences = self._extract_zone_sequences(context, history)
        common_sequences = self._find_common_sequences(zone_sequences)
        
        for sequence, frequency in common_sequences.items():
            if frequency >= self.thresholds['min_pattern_frequency']:
                pattern = self._create_workflow_pattern_from_sequence(sequence, frequency)
                if pattern.confidence >= self.thresholds['min_confidence_score']:
                    patterns.append(pattern)
        
        # Analyze tool usage patterns within workflows
        tool_patterns = self._analyze_tool_workflow_patterns(context, history)
        patterns.extend(tool_patterns)
        
        # Analyze file access patterns
        file_patterns = self._analyze_file_workflow_patterns(context, history)
        patterns.extend(file_patterns)
        
        return patterns
    
    def _analyze_behavioral_insights(self, context: UserContext, history: List[UserContext]) -> List[BehavioralInsight]:
        """Analyze behavioral patterns to generate insights."""
        insights = []
        
        # Analyze productivity trends
        productivity_insights = self._analyze_productivity_trends(context, history)
        insights.extend(productivity_insights)
        
        # Analyze efficiency bottlenecks
        bottleneck_insights = self._analyze_efficiency_bottlenecks(context, history)
        insights.extend(bottleneck_insights)
        
        # Analyze habit formation
        habit_insights = self._analyze_habit_patterns(context, history)
        insights.extend(habit_insights)
        
        # Analyze collaboration patterns
        collaboration_insights = self._analyze_collaboration_patterns(context, history)
        insights.extend(collaboration_insights)
        
        return insights
    
    def _analyze_efficiency_patterns(self, context: UserContext, history: List[UserContext]) -> Dict[str, Any]:
        """Analyze efficiency patterns and calculate metrics."""
        efficiency_data = {
            'current_efficiency': context.get_productivity_score(),
            'efficiency_trend': [],
            'zone_efficiency': {},
            'tool_efficiency': {},
            'time_distribution': {},
            'bottlenecks': []
        }
        
        # Calculate efficiency trend
        if history:
            efficiency_scores = [ctx.get_productivity_score() for ctx in history[-20:]]
            efficiency_data['efficiency_trend'] = efficiency_scores
        
        # Analyze zone efficiency
        zone_times = defaultdict(list)
        zone_productivity = defaultdict(list)
        
        for ctx in history[-10:]:  # Last 10 contexts
            for transition in ctx.zone_transitions:
                zone = transition['to_zone']
                duration = transition.get('duration_ms', 0)
                if duration > 0:
                    zone_times[zone].append(duration)
                    zone_productivity[zone].append(ctx.get_productivity_score())
        
        for zone in zone_times:
            if zone_times[zone] and zone_productivity[zone]:
                avg_time = statistics.mean(zone_times[zone])
                avg_productivity = statistics.mean(zone_productivity[zone])
                efficiency_data['zone_efficiency'][zone] = {
                    'average_time_ms': avg_time,
                    'average_productivity': avg_productivity,
                    'efficiency_ratio': avg_productivity / (avg_time / 60000)  # productivity per minute
                }
        
        # Analyze tool efficiency
        for tool, usage_count in context.tool_usage_patterns.items():
            if usage_count > 0:
                # Estimate efficiency based on usage frequency and context
                base_efficiency = min(1.0, usage_count / 10.0)  # Normalize to 10 uses
                efficiency_data['tool_efficiency'][tool] = base_efficiency
        
        return efficiency_data
    
    def _identify_optimization_opportunities(self, context: UserContext, 
                                          patterns: List[WorkflowPattern], 
                                          insights: List[BehavioralInsight]) -> List[Dict[str, Any]]:
        """Identify specific optimization opportunities."""
        opportunities = []
        
        # Workflow optimization opportunities
        for pattern in patterns:
            if pattern.efficiency_score < 0.7:  # Below 70% efficiency
                opportunities.append({
                    'type': 'workflow_optimization',
                    'title': f'Optimize {pattern.name} Workflow',
                    'description': f'This workflow could be {(1 - pattern.efficiency_score) * 100:.0f}% more efficient',
                    'potential_impact': 'high',
                    'suggestions': pattern.optimization_suggestions,
                    'confidence': pattern.confidence
                })
        
        # Tool usage optimization
        tool_usage = context.tool_usage_patterns
        if tool_usage:
            most_used_tool = max(tool_usage.items(), key=lambda x: x[1])
            if most_used_tool[1] > 20:  # Used more than 20 times
                opportunities.append({
                    'type': 'tool_optimization',
                    'title': 'Optimize Frequent Tool Usage',
                    'description': f'Consider creating shortcuts or automation for {most_used_tool[0]}',
                    'potential_impact': 'medium',
                    'suggestions': [
                        'Create keyboard shortcuts',
                        'Set up automation workflows',
                        'Use templates or presets'
                    ],
                    'confidence': 0.8
                })
        
        # Zone switching optimization
        zone_switches = context.productivity_metrics.get('zone_switches_per_hour', 0)
        if zone_switches > 15:  # More than 15 switches per hour
            opportunities.append({
                'type': 'focus_optimization',
                'title': 'Reduce Context Switching',
                'description': f'You switch between applications {zone_switches} times per hour',
                'potential_impact': 'high',
                'suggestions': [
                    'Batch similar tasks together',
                    'Use focus mode or time blocking',
                    'Set up dedicated workspaces'
                ],
                'confidence': 0.9
            })
        
        return opportunities
    
    def _extract_zone_sequences(self, context: UserContext, history: List[UserContext]) -> List[List[str]]:
        """Extract zone transition sequences from context history."""
        sequences = []
        
        # Combine current context with history
        all_contexts = history + [context]
        
        for ctx in all_contexts:
            if len(ctx.zone_transitions) >= 2:
                sequence = [t['to_zone'] for t in ctx.zone_transitions[-10:]]  # Last 10 transitions
                if len(sequence) >= 3:  # Minimum sequence length
                    sequences.append(sequence)
        
        return sequences
    
    def _find_common_sequences(self, sequences: List[List[str]]) -> Dict[str, int]:
        """Find common subsequences in zone transitions."""
        sequence_counts = Counter()
        
        for sequence in sequences:
            # Generate all subsequences of length 3-5
            for length in range(3, min(6, len(sequence) + 1)):
                for i in range(len(sequence) - length + 1):
                    subseq = tuple(sequence[i:i + length])
                    sequence_counts[subseq] += 1
        
        # Convert tuples back to strings for easier handling
        return {' -> '.join(seq): count for seq, count in sequence_counts.items()}
    
    def _create_workflow_pattern_from_sequence(self, sequence: str, frequency: int) -> WorkflowPattern:
        """Create a workflow pattern from a zone sequence."""
        zones = sequence.split(' -> ')
        
        # Calculate confidence based on frequency and sequence length
        confidence = min(1.0, (frequency / 10.0) * (len(zones) / 5.0))
        
        # Estimate efficiency score (placeholder - would be more sophisticated in practice)
        efficiency_score = max(0.3, 1.0 - (len(zones) * 0.1))  # Longer sequences are less efficient
        
        # Generate optimization suggestions
        suggestions = []
        if len(zones) > 4:
            suggestions.append("Consider batching tasks to reduce context switching")
        if frequency > 5:
            suggestions.append("Create a workflow template for this common pattern")
        
        return WorkflowPattern(
            id=f"workflow_{hash(sequence)}",
            name=f"Multi-Panel Workflow: {' → '.join(zones[:3])}{'...' if len(zones) > 3 else ''}",
            description=f"Common workflow pattern involving {len(zones)} applications",
            steps=[{'zone': zone, 'order': i} for i, zone in enumerate(zones)],
            frequency=frequency,
            confidence=confidence,
            efficiency_score=efficiency_score,
            last_seen=int(time.time() * 1000),
            optimization_suggestions=suggestions
        )
    
    def _analyze_tool_workflow_patterns(self, context: UserContext, history: List[UserContext]) -> List[WorkflowPattern]:
        """Analyze tool usage patterns within workflows."""
        patterns = []
        
        # Analyze tool sequences within zones
        tool_sequences = defaultdict(list)
        
        for ctx in history + [context]:
            current_zone = ctx.current_zone
            zone_tools = [tool for zone_tool, count in ctx.tool_usage_patterns.items() 
                         if zone_tool.startswith(current_zone + ':') and count > 0]
            
            if len(zone_tools) >= 2:
                tool_sequences[current_zone].append(zone_tools)
        
        # Find common tool patterns within each zone
        for zone, sequences in tool_sequences.items():
            if len(sequences) >= 3:  # At least 3 occurrences
                # This is a simplified pattern detection - in practice would be more sophisticated
                common_tools = set.intersection(*[set(seq) for seq in sequences])
                if len(common_tools) >= 2:
                    pattern = WorkflowPattern(
                        id=f"tool_pattern_{zone}_{hash(frozenset(common_tools))}",
                        name=f"Tool Pattern in {zone}",
                        description=f"Common tool usage pattern in {zone}",
                        steps=[{'tool': tool, 'zone': zone} for tool in common_tools],
                        frequency=len(sequences),
                        confidence=0.7,
                        efficiency_score=0.8,
                        last_seen=int(time.time() * 1000),
                        optimization_suggestions=["Consider creating tool shortcuts or macros"]
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def _analyze_file_workflow_patterns(self, context: UserContext, history: List[UserContext]) -> List[WorkflowPattern]:
        """Analyze file access patterns within workflows."""
        patterns = []
        
        # Analyze file access sequences
        file_sequences = []
        for ctx in history + [context]:
            if len(ctx.recent_files) >= 2:
                file_sequences.append(ctx.recent_files[:5])  # Top 5 recent files
        
        if len(file_sequences) >= 3:
            # Find common file patterns (simplified)
            all_files = [file for seq in file_sequences for file in seq]
            file_counts = Counter(all_files)
            common_files = [file for file, count in file_counts.items() if count >= 3]
            
            if len(common_files) >= 2:
                pattern = WorkflowPattern(
                    id=f"file_pattern_{hash(frozenset(common_files))}",
                    name="File Access Pattern",
                    description="Common file access pattern detected",
                    steps=[{'file': file, 'type': 'file_access'} for file in common_files],
                    frequency=min([file_counts[file] for file in common_files]),
                    confidence=0.6,
                    efficiency_score=0.7,
                    last_seen=int(time.time() * 1000),
                    optimization_suggestions=["Consider organizing frequently accessed files in a dedicated workspace"]
                )
                patterns.append(pattern)
        
        return patterns

    def _analyze_productivity_trends(self, context: UserContext, history: List[UserContext]) -> List[BehavioralInsight]:
        """Analyze productivity trends and patterns."""
        insights = []

        if len(history) < 5:
            return insights

        # Get productivity scores from history
        productivity_scores = [ctx.get_productivity_score() for ctx in history[-10:]]

        if len(productivity_scores) >= 5:
            # Calculate trend
            recent_avg = statistics.mean(productivity_scores[-3:])
            earlier_avg = statistics.mean(productivity_scores[:3])
            trend_change = recent_avg - earlier_avg

            if abs(trend_change) > 0.2:  # Significant change
                trend_type = "improving" if trend_change > 0 else "declining"
                insights.append(BehavioralInsight(
                    type="efficiency",
                    title=f"Productivity Trend: {trend_type.title()}",
                    description=f"Your productivity has been {trend_type} by {abs(trend_change)*100:.1f}% recently",
                    evidence=[f"Recent average: {recent_avg:.2f}", f"Earlier average: {earlier_avg:.2f}"],
                    confidence=0.8,
                    impact_score=abs(trend_change),
                    actionable_suggestions=[
                        "Continue current practices" if trend_change > 0 else "Review recent changes in workflow",
                        "Identify factors contributing to the trend",
                        "Set productivity goals and tracking"
                    ]
                ))

        return insights

    def _analyze_efficiency_bottlenecks(self, context: UserContext, history: List[UserContext]) -> List[BehavioralInsight]:
        """Analyze efficiency bottlenecks in user behavior."""
        insights = []

        # Analyze zone switching patterns
        zone_switches = context.productivity_metrics.get('zone_switches_per_hour', 0)
        if zone_switches > 20:  # High switching frequency
            insights.append(BehavioralInsight(
                type="bottleneck",
                title="High Context Switching Detected",
                description=f"You're switching between applications {zone_switches} times per hour",
                evidence=[f"Zone switches per hour: {zone_switches}", "Frequent switching reduces focus"],
                confidence=0.9,
                impact_score=0.7,
                actionable_suggestions=[
                    "Use time blocking to batch similar tasks",
                    "Set up dedicated workspaces for different types of work",
                    "Use focus mode or do-not-disturb settings"
                ]
            ))

        # Analyze idle time patterns
        if context.idle_duration > 300000:  # More than 5 minutes idle
            insights.append(BehavioralInsight(
                type="bottleneck",
                title="Extended Idle Time Detected",
                description=f"You've been idle for {context.idle_duration // 60000} minutes",
                evidence=[f"Current idle duration: {context.idle_duration}ms"],
                confidence=0.7,
                impact_score=0.5,
                actionable_suggestions=[
                    "Take regular breaks to maintain focus",
                    "Set reminders for task transitions",
                    "Review if current task needs different approach"
                ]
            ))

        return insights

    def _analyze_habit_patterns(self, context: UserContext, history: List[UserContext]) -> List[BehavioralInsight]:
        """Analyze habit formation and behavioral patterns."""
        insights = []

        # Analyze tool usage habits
        if context.tool_usage_patterns:
            most_used_tool = max(context.tool_usage_patterns.items(), key=lambda x: x[1])
            total_usage = sum(context.tool_usage_patterns.values())

            if most_used_tool[1] / total_usage > 0.6:  # More than 60% of usage
                insights.append(BehavioralInsight(
                    type="habit",
                    title="Strong Tool Preference Detected",
                    description=f"You use {most_used_tool[0]} for {(most_used_tool[1]/total_usage)*100:.0f}% of your tool interactions",
                    evidence=[f"Tool usage: {most_used_tool[1]} out of {total_usage} total"],
                    confidence=0.8,
                    impact_score=0.4,
                    actionable_suggestions=[
                        "Explore alternative tools for variety",
                        "Consider if this tool is optimal for all use cases",
                        "Learn advanced features of your preferred tool"
                    ]
                ))

        # Analyze zone preferences
        zone_transitions = context.zone_transitions
        if len(zone_transitions) > 10:
            zone_counts = Counter([t['to_zone'] for t in zone_transitions])
            most_used_zone = zone_counts.most_common(1)[0]

            if most_used_zone[1] / len(zone_transitions) > 0.7:  # More than 70% in one zone
                insights.append(BehavioralInsight(
                    type="habit",
                    title="Zone Preference Pattern",
                    description=f"You spend {(most_used_zone[1]/len(zone_transitions))*100:.0f}% of your time in {most_used_zone[0]}",
                    evidence=[f"Zone usage: {most_used_zone[1]} out of {len(zone_transitions)} transitions"],
                    confidence=0.7,
                    impact_score=0.3,
                    actionable_suggestions=[
                        "Explore other available applications",
                        "Consider if other tools might enhance your workflow",
                        "Set goals to try new features regularly"
                    ]
                ))

        return insights

    def _analyze_collaboration_patterns(self, context: UserContext, history: List[UserContext]) -> List[BehavioralInsight]:
        """Analyze collaboration and communication patterns."""
        insights = []

        # Check for communication tool usage
        comm_tools = [tool for tool in context.tool_usage_patterns.keys() if 'communic8' in tool]

        if comm_tools:
            total_comm_usage = sum([context.tool_usage_patterns[tool] for tool in comm_tools])
            total_usage = sum(context.tool_usage_patterns.values())

            comm_ratio = total_comm_usage / total_usage if total_usage > 0 else 0

            if comm_ratio > 0.3:  # More than 30% communication
                insights.append(BehavioralInsight(
                    type="opportunity",
                    title="High Communication Activity",
                    description=f"Communication tools account for {comm_ratio*100:.0f}% of your activity",
                    evidence=[f"Communication usage: {total_comm_usage} out of {total_usage}"],
                    confidence=0.6,
                    impact_score=0.4,
                    actionable_suggestions=[
                        "Consider batching communication tasks",
                        "Set specific times for checking messages",
                        "Use templates for common responses"
                    ]
                ))

        return insights

    def _pattern_to_dict(self, pattern: WorkflowPattern) -> Dict[str, Any]:
        """Convert WorkflowPattern to dictionary."""
        return {
            'id': pattern.id,
            'name': pattern.name,
            'description': pattern.description,
            'steps': pattern.steps,
            'frequency': pattern.frequency,
            'confidence': pattern.confidence,
            'efficiency_score': pattern.efficiency_score,
            'last_seen': pattern.last_seen,
            'optimization_suggestions': pattern.optimization_suggestions
        }

    def _insight_to_dict(self, insight: BehavioralInsight) -> Dict[str, Any]:
        """Convert BehavioralInsight to dictionary."""
        return {
            'type': insight.type,
            'title': insight.title,
            'description': insight.description,
            'evidence': insight.evidence,
            'confidence': insight.confidence,
            'impact_score': insight.impact_score,
            'actionable_suggestions': insight.actionable_suggestions
        }

    def _update_pattern_history(self, results: Dict[str, Any]) -> None:
        """Update pattern history with current results."""
        history_entry = {
            'timestamp': int(time.time() * 1000),
            'patterns_detected': len(results.get('workflow_patterns', [])),
            'insights_generated': len(results.get('behavioral_insights', [])),
            'confidence': results.get('pattern_confidence', 0.0)
        }

        self.pattern_history.append(history_entry)

        # Keep only recent history (last 100 entries)
        if len(self.pattern_history) > 100:
            self.pattern_history = self.pattern_history[-100:]
