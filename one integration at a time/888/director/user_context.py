"""
UserContext model for cross-application state management.

This module defines the UserContext dataclass that aggregates telemetry data
across all wrapped applications (orchestr8, integr8, etc.) for behavioral analysis.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import time


@dataclass
class UserContext:
    """
    Unified context model for cross-application behavioral analysis.
    
    This class aggregates telemetry data from all wrapped applications
    and maintains behavioral patterns for the AI Director's OODA loop.
    """
    
    # Cross-application state
    current_zone: str = "orchestr8"  # Current active application zone
    active_tools: Dict[str, Any] = field(default_factory=dict)  # Currently active tools per app
    recent_files: List[str] = field(default_factory=list)  # Recently accessed files
    conversation_context: Optional[str] = None  # Current conversation/chat context
    idle_duration: int = 0  # Current idle time in milliseconds
    
    # Behavioral patterns
    zone_transitions: List[Dict[str, Any]] = field(default_factory=list)  # App switching patterns
    tool_usage_patterns: Dict[str, int] = field(default_factory=dict)  # Tool usage frequency
    productivity_metrics: Dict[str, float] = field(default_factory=dict)  # Productivity indicators
    
    # Suggestion state
    last_suggestion_time: int = field(default_factory=lambda: int(time.time() * 1000))
    suggestion_history: List[Dict[str, Any]] = field(default_factory=list)  # Past suggestions
    user_feedback: Dict[str, int] = field(default_factory=dict)  # suggestion_id -> rating
    
    # Session tracking
    session_start_time: int = field(default_factory=lambda: int(time.time() * 1000))
    total_session_duration: int = 0  # Total active time in current session
    
    def update_from_telemetry_events(self, events: List[Dict[str, Any]]) -> None:
        """
        Update context from a list of telemetry events.
        
        Args:
            events: List of telemetry event dictionaries
        """
        for event in events:
            self._process_telemetry_event(event)
    
    def _process_telemetry_event(self, event: Dict[str, Any]) -> None:
        """Process a single telemetry event to update context."""
        event_type = event.get('event_type', {})
        event_data = event_type.get('data', {}) if isinstance(event_type, dict) else {}
        
        # Handle different event types
        if isinstance(event_type, dict):
            type_name = event_type.get('type')
        else:
            type_name = str(event_type)
            
        if type_name == 'ZoneChange':
            self._handle_zone_change(event_data)
        elif type_name == 'ToolActivation':
            self._handle_tool_activation(event_data)
        elif type_name == 'FileAccess':
            self._handle_file_access(event_data)
        elif type_name == 'IdleTime':
            self._handle_idle_time(event_data)
        elif type_name == 'UIInteraction':
            self._handle_ui_interaction(event_data)
        elif type_name == 'TabSwitch':
            self._handle_tab_switch(event_data)
        elif type_name == 'AppSwitch':
            self._handle_app_switch(event_data)
        elif type_name == 'SessionEvent':
            self._handle_session_event(event_data)
    
    def _handle_zone_change(self, data: Dict[str, Any]) -> None:
        """Handle zone change events."""
        from_zone = data.get('from_zone', self.current_zone)
        to_zone = data.get('to_zone', self.current_zone)
        duration_ms = data.get('duration_ms', 0)
        
        # Update current zone
        self.current_zone = to_zone
        
        # Track zone transition patterns
        transition = {
            'from_zone': from_zone,
            'to_zone': to_zone,
            'duration_ms': duration_ms,
            'timestamp': int(time.time() * 1000)
        }
        self.zone_transitions.append(transition)
        
        # Keep only recent transitions (last 50)
        if len(self.zone_transitions) > 50:
            self.zone_transitions = self.zone_transitions[-50:]
    
    def _handle_tool_activation(self, data: Dict[str, Any]) -> None:
        """Handle tool activation events."""
        tool_name = data.get('tool_name', '')
        app_context = data.get('app_context', self.current_zone)
        
        # Update active tools
        self.active_tools[app_context] = tool_name
        
        # Track tool usage patterns
        tool_key = f"{app_context}:{tool_name}"
        self.tool_usage_patterns[tool_key] = self.tool_usage_patterns.get(tool_key, 0) + 1
    
    def _handle_file_access(self, data: Dict[str, Any]) -> None:
        """Handle file access events."""
        file_path = data.get('file_path', '')
        access_type = data.get('access_type', 'unknown')
        
        if file_path and access_type in ['open', 'edit']:
            # Add to recent files (avoid duplicates)
            if file_path in self.recent_files:
                self.recent_files.remove(file_path)
            self.recent_files.insert(0, file_path)
            
            # Keep only recent files (last 20)
            if len(self.recent_files) > 20:
                self.recent_files = self.recent_files[:20]
    
    def _handle_idle_time(self, data: Dict[str, Any]) -> None:
        """Handle idle time events."""
        self.idle_duration = data.get('duration_ms', 0)
    
    def _handle_ui_interaction(self, data: Dict[str, Any]) -> None:
        """Handle UI interaction events."""
        # Reset idle time on interaction
        self.idle_duration = 0
        
        # Update productivity metrics based on interaction patterns
        component = data.get('component', '')
        action = data.get('action', '')
        
        if component and action:
            interaction_key = f"{component}:{action}"
            current_count = self.productivity_metrics.get(interaction_key, 0.0)
            self.productivity_metrics[interaction_key] = current_count + 1.0
    
    def _handle_tab_switch(self, data: Dict[str, Any]) -> None:
        """Handle tab switch events."""
        # Track tab switching patterns for productivity analysis
        tab_type = data.get('tab_type', 'unknown')
        app_context = data.get('app_context', self.current_zone)
        
        tab_key = f"{app_context}:tab_switches"
        current_count = self.productivity_metrics.get(tab_key, 0.0)
        self.productivity_metrics[tab_key] = current_count + 1.0
    
    def _handle_app_switch(self, data: Dict[str, Any]) -> None:
        """Handle app switch events."""
        from_app = data.get('from_app')
        to_app = data.get('to_app', self.current_zone)
        switch_reason = data.get('switch_reason', 'unknown')
        
        # Update current zone
        self.current_zone = to_app
        
        # Track app switching patterns
        if from_app:
            switch_key = f"{from_app}->{to_app}"
            current_count = self.productivity_metrics.get(switch_key, 0.0)
            self.productivity_metrics[switch_key] = current_count + 1.0
    
    def _handle_session_event(self, data: Dict[str, Any]) -> None:
        """Handle session events."""
        event = data.get('event', '')
        session_duration_ms = data.get('session_duration_ms', 0)
        
        if event == 'start':
            self.session_start_time = int(time.time() * 1000)
        elif event in ['end', 'pause'] and session_duration_ms:
            self.total_session_duration += session_duration_ms
    
    def get_productivity_score(self) -> float:
        """
        Calculate a productivity score based on behavioral patterns.
        
        Returns:
            Float between 0.0 and 1.0 representing productivity level
        """
        if not self.productivity_metrics:
            return 0.5  # Neutral score with no data
        
        # Simple productivity scoring based on activity patterns
        # Only sum numeric values, skip lists and other non-numeric values
        numeric_values = [v for v in self.productivity_metrics.values() if isinstance(v, (int, float))]
        total_interactions = sum(numeric_values) if numeric_values else 0
        if total_interactions == 0:
            return 0.5  # Return neutral score instead of 0
        
        # Factor in idle time (lower idle = higher productivity)
        idle_factor = max(0.0, 1.0 - (self.idle_duration / 300000))  # 5 minutes max
        
        # Factor in tool usage diversity
        unique_tools = len(self.tool_usage_patterns)
        diversity_factor = min(1.0, unique_tools / 10.0)  # Normalize to 10 tools
        
        # Factor in zone transitions (moderate switching is good)
        recent_transitions = len([t for t in self.zone_transitions 
                                if t['timestamp'] > (int(time.time() * 1000) - 3600000)])  # Last hour
        transition_factor = min(1.0, recent_transitions / 5.0)  # Normalize to 5 transitions/hour
        
        # Weighted average
        score = (idle_factor * 0.4 + diversity_factor * 0.3 + transition_factor * 0.3)
        return max(0.0, min(1.0, score))
    
    def get_context_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current context for suggestion generation.
        
        Returns:
            Dictionary containing key context information
        """
        return {
            'current_zone': self.current_zone,
            'active_tools': self.active_tools,
            'recent_files': self.recent_files[:5],  # Top 5 recent files
            'idle_duration': self.idle_duration,
            'productivity_score': self.get_productivity_score(),
            'session_duration': int(time.time() * 1000) - self.session_start_time,
            'recent_zones': [t['to_zone'] for t in self.zone_transitions[-5:]],  # Last 5 zones
            'top_tools': sorted(self.tool_usage_patterns.items(), 
                              key=lambda x: x[1], reverse=True)[:5]  # Top 5 tools
        }
    
    def record_suggestion_feedback(self, suggestion_id: str, rating: int) -> None:
        """
        Record user feedback for a suggestion.
        
        Args:
            suggestion_id: Unique identifier for the suggestion
            rating: User rating (-1 = negative, 0 = neutral, 1 = positive)
        """
        self.user_feedback[suggestion_id] = max(-1, min(1, rating))
    
    def should_show_suggestion(self) -> bool:
        """
        Determine if it's appropriate to show a suggestion based on context.

        Returns:
            True if a suggestion should be shown, False otherwise
        """
        current_time = int(time.time() * 1000)

        # Don't show suggestions too frequently (minimum 30 seconds apart)
        if current_time - self.last_suggestion_time < 30000:
            return False

        # Don't show suggestions during very long idle periods (more than 5 minutes)
        if self.idle_duration > 300000:  # 5 minutes idle
            return False

        # Don't show suggestions if user is very actively working (less than 2 seconds since last interaction)
        if self.idle_duration < 2000:  # Less than 2 seconds since last interaction
            return False

        return True
