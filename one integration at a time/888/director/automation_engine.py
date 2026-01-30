"""
Context-Aware Automation Engine for Director Intelligence.

This module implements automatic workflow trigger detection and context-aware
automation based on user activity patterns and behavioral analysis.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
import time
import statistics
from collections import defaultdict, Counter
from .user_context import UserContext
from .pattern_recognition import WorkflowPattern, BehavioralInsight


@dataclass
class AutomationTrigger:
    """Represents an automation trigger condition."""
    id: str
    name: str
    description: str
    trigger_type: str  # "time_based", "context_based", "pattern_based", "event_based"
    conditions: Dict[str, Any]
    confidence: float
    enabled: bool = True
    last_triggered: Optional[int] = None
    trigger_count: int = 0


@dataclass
class AutomationAction:
    """Represents an automated action."""
    id: str
    name: str
    description: str
    action_type: str  # "workflow_start", "suggestion_show", "context_switch", "notification"
    parameters: Dict[str, Any]
    success_rate: float = 1.0
    execution_count: int = 0


@dataclass
class AutomationRule:
    """Represents a complete automation rule."""
    id: str
    name: str
    description: str
    trigger: AutomationTrigger
    action: AutomationAction
    priority: int
    created_at: int
    last_executed: Optional[int] = None
    success_count: int = 0
    failure_count: int = 0


class ContextAwareAutomation:
    """
    Context-aware automation engine for intelligent workflow automation.
    
    This engine monitors user behavior patterns and automatically triggers
    workflows, suggestions, and optimizations based on contextual cues.
    """
    
    def __init__(self):
        self.automation_rules: Dict[str, AutomationRule] = {}
        self.trigger_history: List[Dict[str, Any]] = []
        self.context_patterns: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.learning_data: Dict[str, Any] = {}
        
        # Initialize default automation rules
        self._initialize_default_rules()
        
        # Automation thresholds
        self.thresholds = {
            'min_trigger_confidence': 0.7,
            'pattern_frequency_threshold': 3,
            'context_similarity_threshold': 0.8,
            'automation_cooldown_ms': 300000,  # 5 minutes
            'max_automations_per_hour': 10,
        }
    
    def process_context_for_automation(self, context: UserContext,
                                     patterns: List[WorkflowPattern],
                                     insights: List[BehavioralInsight]) -> List[Dict[str, Any]]:
        """
        Process current context to identify and trigger automation opportunities.
        
        Args:
            context: Current user context
            patterns: Detected workflow patterns
            insights: Behavioral insights
            
        Returns:
            List of triggered automations
        """
        triggered_automations = []
        current_time = int(time.time() * 1000)
        
        try:
            # Check if we're within automation limits
            if not self._within_automation_limits(current_time):
                return triggered_automations
            
            # Evaluate each automation rule
            for rule_id, rule in self.automation_rules.items():
                if not rule.trigger.enabled:
                    continue
                
                # Check if rule should be triggered
                should_trigger, trigger_confidence = self._evaluate_trigger(rule.trigger, context, patterns, insights)
                
                if should_trigger and trigger_confidence >= self.thresholds['min_trigger_confidence']:
                    # Check cooldown period
                    if self._is_within_cooldown(rule, current_time):
                        continue
                    
                    # Execute automation
                    automation_result = self._execute_automation(rule, context, current_time)
                    if automation_result:
                        triggered_automations.append(automation_result)
            
            # Learn from context patterns
            self._learn_from_context(context, patterns, insights)
            
            # Generate new automation rules based on patterns
            new_rules = self._generate_dynamic_rules(context, patterns, insights)
            for rule in new_rules:
                self.automation_rules[rule.id] = rule
            
            # Update trigger history
            self._update_trigger_history(triggered_automations, context)
            
        except Exception as e:
            print(f"Error in automation processing: {e}")
        
        return triggered_automations
    
    def _initialize_default_rules(self) -> None:
        """Initialize default automation rules."""
        current_time = int(time.time() * 1000)
        
        # Rule 1: Auto-suggest workflow completion
        workflow_completion_trigger = AutomationTrigger(
            id="workflow_completion_trigger",
            name="Workflow Completion Detection",
            description="Trigger when user is likely to complete a workflow",
            trigger_type="pattern_based",
            conditions={
                'workflow_progress_threshold': 0.7,
                'idle_time_max': 60000,  # 1 minute
                'confidence_min': 0.6
            },
            confidence=0.8
        )
        
        workflow_completion_action = AutomationAction(
            id="suggest_workflow_completion",
            name="Suggest Workflow Completion",
            description="Show suggestion to complete current workflow",
            action_type="suggestion_show",
            parameters={
                'suggestion_type': 'workflow_completion',
                'priority': 4,
                'auto_dismiss_ms': 15000
            }
        )
        
        self.automation_rules["workflow_completion"] = AutomationRule(
            id="workflow_completion",
            name="Auto-suggest Workflow Completion",
            description="Automatically suggest workflow completion when appropriate",
            trigger=workflow_completion_trigger,
            action=workflow_completion_action,
            priority=4,
            created_at=current_time
        )
        
        # Rule 2: Context switch optimization
        context_switch_trigger = AutomationTrigger(
            id="excessive_switching_trigger",
            name="Excessive Context Switching Detection",
            description="Trigger when user switches contexts too frequently",
            trigger_type="context_based",
            conditions={
                'switches_per_hour_threshold': 15,
                'efficiency_drop_threshold': 0.2
            },
            confidence=0.9
        )
        
        context_switch_action = AutomationAction(
            id="suggest_focus_mode",
            name="Suggest Focus Mode",
            description="Suggest enabling focus mode to reduce distractions",
            action_type="suggestion_show",
            parameters={
                'suggestion_type': 'focus_optimization',
                'priority': 3,
                'focus_duration_minutes': 25  # Pomodoro-style
            }
        )
        
        self.automation_rules["context_switch_optimization"] = AutomationRule(
            id="context_switch_optimization",
            name="Auto-suggest Focus Mode",
            description="Automatically suggest focus mode when context switching is excessive",
            trigger=context_switch_trigger,
            action=context_switch_action,
            priority=3,
            created_at=current_time
        )
        
        # Rule 3: Productivity break reminder
        break_reminder_trigger = AutomationTrigger(
            id="productivity_break_trigger",
            name="Productivity Break Detection",
            description="Trigger break reminder based on work patterns",
            trigger_type="time_based",
            conditions={
                'continuous_work_minutes': 90,
                'productivity_decline_threshold': 0.3
            },
            confidence=0.7
        )
        
        break_reminder_action = AutomationAction(
            id="suggest_break",
            name="Suggest Taking a Break",
            description="Suggest taking a productivity break",
            action_type="suggestion_show",
            parameters={
                'suggestion_type': 'productivity_break',
                'priority': 2,
                'break_duration_minutes': 10
            }
        )
        
        self.automation_rules["productivity_break"] = AutomationRule(
            id="productivity_break",
            name="Auto-suggest Productivity Breaks",
            description="Automatically suggest breaks based on work patterns",
            trigger=break_reminder_trigger,
            action=break_reminder_action,
            priority=2,
            created_at=current_time
        )
    
    def _evaluate_trigger(self, trigger: AutomationTrigger, context: UserContext,
                         patterns: List[WorkflowPattern], insights: List[BehavioralInsight]) -> Tuple[bool, float]:
        """Evaluate if a trigger should fire based on current context."""
        if trigger.trigger_type == "pattern_based":
            return self._evaluate_pattern_trigger(trigger, context, patterns)
        elif trigger.trigger_type == "context_based":
            return self._evaluate_context_trigger(trigger, context)
        elif trigger.trigger_type == "time_based":
            return self._evaluate_time_trigger(trigger, context)
        elif trigger.trigger_type == "event_based":
            return self._evaluate_event_trigger(trigger, context, insights)
        
        return False, 0.0
    
    def _evaluate_pattern_trigger(self, trigger: AutomationTrigger, context: UserContext,
                                patterns: List[WorkflowPattern]) -> Tuple[bool, float]:
        """Evaluate pattern-based triggers."""
        conditions = trigger.conditions
        
        if trigger.id == "workflow_completion_trigger":
            # Check if user is in middle of a workflow
            for pattern in patterns:
                if pattern.confidence > conditions.get('confidence_min', 0.6):
                    # Estimate workflow progress (simplified)
                    current_zone = context.current_zone
                    pattern_zones = [step.get('zone') for step in pattern.steps if step.get('zone')]
                    
                    if current_zone in pattern_zones:
                        zone_index = pattern_zones.index(current_zone)
                        progress = (zone_index + 1) / len(pattern_zones)
                        
                        if (progress > conditions.get('workflow_progress_threshold', 0.7) and
                            context.idle_duration < conditions.get('idle_time_max', 60000)):
                            return True, pattern.confidence
        
        return False, 0.0
    
    def _evaluate_context_trigger(self, trigger: AutomationTrigger, context: UserContext) -> Tuple[bool, float]:
        """Evaluate context-based triggers."""
        conditions = trigger.conditions
        
        if trigger.id == "excessive_switching_trigger":
            switches_per_hour = context.productivity_metrics.get('zone_switches_per_hour', 0)
            current_efficiency = context.get_productivity_score()
            
            # Check if switching is excessive and efficiency is dropping
            if (switches_per_hour > conditions.get('switches_per_hour_threshold', 15) and
                current_efficiency < (1.0 - conditions.get('efficiency_drop_threshold', 0.2))):
                confidence = min(1.0, switches_per_hour / 20.0)  # Normalize to 20 switches
                return True, confidence
        
        return False, 0.0

    def _within_automation_limits(self, current_time: int) -> bool:
        """Check if we're within automation rate limits."""
        # Count automations in the last hour
        hour_ago = current_time - 3600000  # 1 hour in milliseconds
        recent_automations = [
            entry for entry in self.trigger_history
            if entry['timestamp'] > hour_ago
        ]

        return len(recent_automations) < self.thresholds['max_automations_per_hour']

    def _is_within_cooldown(self, rule: AutomationRule, current_time: int) -> bool:
        """Check if automation rule is within cooldown period."""
        if rule.last_executed is None:
            return False

        cooldown_period = self.thresholds['automation_cooldown_ms']
        return (current_time - rule.last_executed) < cooldown_period

    def _execute_automation(self, rule: AutomationRule, context: UserContext, current_time: int) -> Optional[Dict[str, Any]]:
        """Execute an automation rule."""
        try:
            # Update rule execution tracking
            rule.last_executed = current_time
            rule.trigger.last_triggered = current_time
            rule.trigger.trigger_count += 1
            rule.action.execution_count += 1

            # Create automation result
            automation_result = {
                'rule_id': rule.id,
                'rule_name': rule.name,
                'trigger_type': rule.trigger.trigger_type,
                'action_type': rule.action.action_type,
                'parameters': rule.action.parameters.copy(),
                'confidence': rule.trigger.confidence,
                'priority': rule.priority,
                'executed_at': current_time,
                'context_zone': context.current_zone,
                'context_productivity': context.get_productivity_score()
            }

            # Add context-specific parameters
            if rule.action.action_type == "suggestion_show":
                automation_result['parameters']['context_factors'] = [
                    f"Current zone: {context.current_zone}",
                    f"Productivity score: {context.get_productivity_score():.2f}",
                    f"Idle duration: {context.idle_duration}ms"
                ]

            rule.success_count += 1
            return automation_result

        except Exception as e:
            rule.failure_count += 1
            print(f"Error executing automation {rule.id}: {e}")
            return None

    def _learn_from_context(self, context: UserContext, patterns: List[WorkflowPattern], insights: List[BehavioralInsight]) -> None:
        """Learn from current context to improve automation."""
        # Store context patterns for learning
        context_key = f"{context.current_zone}_{int(context.get_productivity_score() * 10)}"

        context_data = {
            'timestamp': int(time.time() * 1000),
            'zone': context.current_zone,
            'productivity': context.get_productivity_score(),
            'idle_duration': context.idle_duration,
            'patterns_detected': len(patterns),
            'insights_generated': len(insights)
        }

        self.context_patterns[context_key].append(context_data)

        # Keep only recent patterns (last 50 per context type)
        if len(self.context_patterns[context_key]) > 50:
            self.context_patterns[context_key] = self.context_patterns[context_key][-50:]

    def _generate_dynamic_rules(self, context: UserContext, patterns: List[WorkflowPattern], insights: List[BehavioralInsight]) -> List[AutomationRule]:
        """Generate new automation rules based on detected patterns."""
        new_rules = []
        current_time = int(time.time() * 1000)

        # Generate rules for frequently detected patterns
        for pattern in patterns:
            if pattern.frequency > 5 and pattern.confidence > 0.8:
                rule_id = f"dynamic_pattern_{pattern.id}"

                # Don't create duplicate rules
                if rule_id in self.automation_rules:
                    continue

                trigger = AutomationTrigger(
                    id=f"trigger_{pattern.id}",
                    name=f"Pattern {pattern.name} Detection",
                    description=f"Auto-trigger for pattern {pattern.name}",
                    trigger_type="pattern_based",
                    conditions={
                        'pattern_id': pattern.id,
                        'confidence_threshold': 0.7,
                        'frequency_threshold': 3
                    },
                    confidence=pattern.confidence
                )

                action = AutomationAction(
                    id=f"action_{pattern.id}",
                    name=f"Suggest {pattern.name}",
                    description=f"Suggest continuing with {pattern.name}",
                    action_type="workflow_start",
                    parameters={
                        'workflow_pattern_id': pattern.id,
                        'suggestion_type': 'pattern_continuation'
                    }
                )

                rule = AutomationRule(
                    id=rule_id,
                    name=f"Auto-suggest {pattern.name}",
                    description=f"Automatically suggest {pattern.name} when conditions are met",
                    trigger=trigger,
                    action=action,
                    priority=2,
                    created_at=current_time
                )

                new_rules.append(rule)

        return new_rules

    def _update_trigger_history(self, triggered_automations: List[Dict[str, Any]], context: UserContext) -> None:
        """Update trigger history with current automations."""
        for automation in triggered_automations:
            history_entry = {
                'timestamp': automation['executed_at'],
                'rule_id': automation['rule_id'],
                'trigger_type': automation['trigger_type'],
                'action_type': automation['action_type'],
                'confidence': automation['confidence'],
                'context_zone': automation['context_zone'],
                'context_productivity': automation['context_productivity']
            }

            self.trigger_history.append(history_entry)

        # Keep only recent history (last 200 entries)
        if len(self.trigger_history) > 200:
            self.trigger_history = self.trigger_history[-200:]

    def get_automation_analytics(self) -> Dict[str, Any]:
        """Get analytics about automation performance."""
        analytics = {
            'total_rules': len(self.automation_rules),
            'active_rules': sum(1 for rule in self.automation_rules.values() if rule.trigger.enabled),
            'total_triggers': len(self.trigger_history),
            'success_rate': 0.0,
            'most_triggered_rules': [],
            'automation_frequency': {},
            'effectiveness_metrics': {}
        }

        if self.automation_rules:
            # Calculate success rate
            total_successes = sum(rule.success_count for rule in self.automation_rules.values())
            total_attempts = sum(rule.success_count + rule.failure_count for rule in self.automation_rules.values())

            if total_attempts > 0:
                analytics['success_rate'] = total_successes / total_attempts

            # Find most triggered rules
            rule_triggers = [(rule.id, rule.trigger.trigger_count) for rule in self.automation_rules.values()]
            analytics['most_triggered_rules'] = sorted(rule_triggers, key=lambda x: x[1], reverse=True)[:5]

            # Analyze automation frequency by type
            trigger_types = [rule.trigger.trigger_type for rule in self.automation_rules.values()]
            analytics['automation_frequency'] = dict(Counter(trigger_types))

        return analytics
    
    def _evaluate_time_trigger(self, trigger: AutomationTrigger, context: UserContext) -> Tuple[bool, float]:
        """Evaluate time-based triggers."""
        conditions = trigger.conditions
        
        if trigger.id == "productivity_break_trigger":
            # Estimate continuous work time (simplified)
            session_duration = int(time.time() * 1000) - context.session_start_time
            continuous_work_minutes = session_duration / 60000
            
            # Check productivity decline
            current_productivity = context.get_productivity_score()
            productivity_decline = current_productivity < (1.0 - conditions.get('productivity_decline_threshold', 0.3))
            
            if (continuous_work_minutes > conditions.get('continuous_work_minutes', 90) and
                productivity_decline):
                confidence = min(1.0, continuous_work_minutes / 120.0)  # Normalize to 2 hours
                return True, confidence
        
        return False, 0.0
    
    def _evaluate_event_trigger(self, trigger: AutomationTrigger, context: UserContext,
                              insights: List[BehavioralInsight]) -> Tuple[bool, float]:
        """Evaluate event-based triggers."""
        # Check if any insights match trigger conditions
        for insight in insights:
            if insight.type in trigger.conditions.get('insight_types', []):
                if insight.confidence > trigger.conditions.get('min_insight_confidence', 0.7):
                    return True, insight.confidence
        
        return False, 0.0
