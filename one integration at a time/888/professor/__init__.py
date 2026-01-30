"""
888 Professor Agent - Breakthrough Analysis Engine

The Professor agent specializes in breakthrough analysis, learning pattern recognition,
and generating contextual insights for software development workflows.

Author: BIG PICKLE SYSTEMS
Version: 1.0.0
"""

from .adapter import (
    get_version,
    health_check,
    analyze_breakthrough,
    get_learning_context,
    generate_insights,
    create_session,
    close_session,
    list_sessions,
    get_session_status,
    start_analysis,
    stop_analysis,
    get_analysis_results,
    get_patterns,
    get_insights,
    get_recommendations,
)

__all__ = [
    "get_version",
    "health_check",
    "analyze_breakthrough",
    "get_learning_context",
    "generate_insights",
    "create_session",
    "close_session",
    "list_sessions",
    "get_session_status",
    "start_analysis",
    "stop_analysis",
    "get_analysis_results",
    "get_patterns",
    "get_insights",
    "get_recommendations",
]
