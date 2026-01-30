"""
888 Professor Agent - Main PyO3 Adapter Interface

The Professor agent provides breakthrough analysis, learning pattern recognition,
and contextual insights for software development workflows.

This adapter follows the established 888 agent pattern with PyO3 integration
and returns only Python primitives for compatibility.
"""

import subprocess
import time
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import json
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from professor.breakthrough_engine import BreakthroughEngine
from professor.learning_analyzer import LearningAnalyzer
from professor.insight_generator import InsightGenerator

# Global state management (following 888 adapter pattern)
_professor_process: Optional[subprocess.Popen] = None
_analysis_sessions: Dict[str, Dict[str, Any]] = {}
_learning_contexts: Dict[str, Dict[str, Any]] = {}
_breakthrough_patterns: Dict[str, Dict[str, Any]] = {}
_insight_cache: Dict[str, Dict[str, Any]] = {}

# Initialize core components
_breakthrough_engine = BreakthroughEngine()
_learning_analyzer = LearningAnalyzer()
_insight_generator = InsightGenerator()

# Configuration
PROFESSOR_CONFIG = {
    "version": "1.0.0",
    "analysis_timeout": 300,  # 5 minutes
    "max_patterns": 100,
    "cache_expiry": 3600,  # 1 hour
    "insight_depth": "comprehensive",
}


def get_version() -> str:
    """Return Professor agent version."""
    return PROFESSOR_CONFIG["version"]


def health_check() -> Dict[str, Any]:
    """Perform comprehensive health check of Professor agent."""
    try:
        current_time = time.time()

        # Check core components
        engine_status = _breakthrough_engine.get_status()
        analyzer_status = _learning_analyzer.get_status()
        generator_status = _insight_generator.get_status()

        # Count active sessions and patterns
        active_sessions = len(
            [s for s in _analysis_sessions.values() if s.get("status") == "active"]
        )
        cached_patterns = len(_breakthrough_patterns)
        cached_insights = len(_insight_cache)

        # Clean expired cache entries
        expired_insights = [
            k
            for k, v in _insight_cache.items()
            if current_time - v.get("timestamp", 0) > PROFESSOR_CONFIG["cache_expiry"]
        ]
        for insight_id in expired_insights:
            del _insight_cache[insight_id]

        return {
            "status": "healthy",
            "agent": "professor",
            "version": PROFESSOR_CONFIG["version"],
            "timestamp": datetime.now().isoformat(),
            "active_sessions": active_sessions,
            "total_sessions": len(_analysis_sessions),
            "cached_patterns": cached_patterns,
            "cached_insights": cached_insights,
            "expired_insights_cleaned": len(expired_insights),
            "components": {
                "breakthrough_engine": engine_status,
                "learning_analyzer": analyzer_status,
                "insight_generator": generator_status,
            },
            "capabilities": [
                "breakthrough_analysis",
                "learning_pattern_recognition",
                "contextual_insights",
                "workflow_optimization",
                "bottleneck_detection",
            ],
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "agent": "professor",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def create_session(
    project_path: str, analysis_type: str = "comprehensive"
) -> Dict[str, Any]:
    """Create a new Professor analysis session."""
    try:
        session_id = f"professor_{uuid.uuid4().hex[:8]}"
        current_time = datetime.now().isoformat()

        # Initialize session
        session = {
            "session_id": session_id,
            "project_path": os.path.abspath(project_path),
            "analysis_type": analysis_type,
            "status": "created",
            "created_at": current_time,
            "last_activity": current_time,
            "analysis_results": {},
            "patterns_found": [],
            "insights_generated": [],
            "recommendations": [],
            "metrics": {
                "files_analyzed": 0,
                "patterns_detected": 0,
                "insights_created": 0,
                "breakthroughs_identified": 0,
            },
        }

        _analysis_sessions[session_id] = session

        return {
            "success": True,
            "session_id": session_id,
            "status": session["status"],
            "created_at": current_time,
            "analysis_type": analysis_type,
            "project_path": session["project_path"],
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def close_session(session_id: str) -> Dict[str, Any]:
    """Close a Professor analysis session."""
    try:
        if session_id not in _analysis_sessions:
            return {
                "success": False,
                "error": f"Session {session_id} not found",
                "timestamp": datetime.now().isoformat(),
            }

        session = _analysis_sessions[session_id]
        session["status"] = "closed"
        session["closed_at"] = datetime.now().isoformat()

        # Calculate session summary
        metrics = session.get("metrics", {})

        return {
            "success": True,
            "session_id": session_id,
            "status": "closed",
            "summary": {
                "duration": session.get("closed_at"),
                "files_analyzed": metrics.get("files_analyzed", 0),
                "patterns_detected": metrics.get("patterns_detected", 0),
                "insights_created": metrics.get("insights_created", 0),
                "breakthroughs_identified": metrics.get("breakthroughs_identified", 0),
            },
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def list_sessions() -> Dict[str, Any]:
    """List all Professor analysis sessions."""
    try:
        sessions = []
        for session_id, session in _analysis_sessions.items():
            sessions.append(
                {
                    "session_id": session_id,
                    "project_path": session.get("project_path"),
                    "status": session.get("status"),
                    "created_at": session.get("created_at"),
                    "analysis_type": session.get("analysis_type"),
                    "last_activity": session.get("last_activity"),
                }
            )

        return {
            "success": True,
            "sessions": sessions,
            "total_count": len(sessions),
            "active_count": len([s for s in sessions if s["status"] == "active"]),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def get_session_status(session_id: str) -> Dict[str, Any]:
    """Get detailed status of a specific session."""
    try:
        if session_id not in _analysis_sessions:
            return {
                "success": False,
                "error": f"Session {session_id} not found",
                "timestamp": datetime.now().isoformat(),
            }

        session = _analysis_sessions[session_id]

        return {
            "success": True,
            "session_id": session_id,
            "status": session.get("status"),
            "project_path": session.get("project_path"),
            "analysis_type": session.get("analysis_type"),
            "created_at": session.get("created_at"),
            "last_activity": session.get("last_activity"),
            "metrics": session.get("metrics", {}),
            "patterns_found_count": len(session.get("patterns_found", [])),
            "insights_generated_count": len(session.get("insights_generated", [])),
            "recommendations_count": len(session.get("recommendations", [])),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def start_analysis(session_id: str, analysis_scope: str = "full") -> Dict[str, Any]:
    """Start breakthrough analysis for a session."""
    try:
        if session_id not in _analysis_sessions:
            return {
                "success": False,
                "error": f"Session {session_id} not found",
                "timestamp": datetime.now().isoformat(),
            }

        session = _analysis_sessions[session_id]
        session["status"] = "analyzing"
        session["last_activity"] = datetime.now().isoformat()

        # Initialize breakthrough analysis
        analysis_result = _breakthrough_engine.start_analysis(
            session["project_path"], analysis_scope, session_id
        )

        session["analysis_results"] = analysis_result
        session["metrics"]["files_analyzed"] = analysis_result.get("files_scanned", 0)

        return {
            "success": True,
            "session_id": session_id,
            "analysis_id": analysis_result.get("analysis_id"),
            "scope": analysis_scope,
            "files_to_analyze": analysis_result.get("files_scanned", 0),
            "started_at": session["last_activity"],
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def stop_analysis(session_id: str) -> Dict[str, Any]:
    """Stop ongoing analysis for a session."""
    try:
        if session_id not in _analysis_sessions:
            return {
                "success": False,
                "error": f"Session {session_id} not found",
                "timestamp": datetime.now().isoformat(),
            }

        session = _analysis_sessions[session_id]
        session["status"] = "stopped"
        session["last_activity"] = datetime.now().isoformat()

        # Stop breakthrough analysis
        stop_result = _breakthrough_engine.stop_analysis(session_id)

        return {
            "success": True,
            "session_id": session_id,
            "stopped_at": session["last_activity"],
            "analysis_summary": stop_result,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def get_analysis_results(session_id: str) -> Dict[str, Any]:
    """Get detailed analysis results for a session."""
    try:
        if session_id not in _analysis_sessions:
            return {
                "success": False,
                "error": f"Session {session_id} not found",
                "timestamp": datetime.now().isoformat(),
            }

        session = _analysis_sessions[session_id]

        # Get fresh results from breakthrough engine
        fresh_results = _breakthrough_engine.get_results(session_id)

        # Update session with latest results
        session["analysis_results"] = fresh_results
        session["metrics"]["patterns_detected"] = len(fresh_results.get("patterns", []))

        return {
            "success": True,
            "session_id": session_id,
            "analysis_results": fresh_results,
            "metrics": session.get("metrics", {}),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def get_patterns(session_id: str, pattern_type: str = "all") -> Dict[str, Any]:
    """Get breakthrough patterns for a session."""
    try:
        if session_id not in _analysis_sessions:
            return {
                "success": False,
                "error": f"Session {session_id} not found",
                "timestamp": datetime.now().isoformat(),
            }

        # Get patterns from breakthrough engine
        patterns_result = _breakthrough_engine.get_patterns(session_id, pattern_type)

        # Update session patterns
        session = _analysis_sessions[session_id]
        session["patterns_found"] = patterns_result.get("patterns", [])

        return {
            "success": True,
            "session_id": session_id,
            "pattern_type": pattern_type,
            "patterns": patterns_result.get("patterns", []),
            "total_count": len(patterns_result.get("patterns", [])),
            "breakthrough_count": len(
                [
                    p
                    for p in patterns_result.get("patterns", [])
                    if p.get("type") == "breakthrough"
                ]
            ),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def get_insights(session_id: str, insight_type: str = "all") -> Dict[str, Any]:
    """Get contextual insights for a session."""
    try:
        if session_id not in _analysis_sessions:
            return {
                "success": False,
                "error": f"Session {session_id} not found",
                "timestamp": datetime.now().isoformat(),
            }

        session = _analysis_sessions[session_id]

        # Generate or get cached insights
        insight_cache_key = f"{session_id}_{insight_type}"
        current_time = time.time()

        if (
            insight_cache_key in _insight_cache
            and current_time - _insight_cache[insight_cache_key]["timestamp"]
            < PROFESSOR_CONFIG["cache_expiry"]
        ):
            insights_result = _insight_cache[insight_cache_key]["data"]
        else:
            # Generate fresh insights
            insights_result = _insight_generator.generate_insights(
                session["analysis_results"], session["patterns_found"], insight_type
            )

            # Cache the insights
            _insight_cache[insight_cache_key] = {
                "data": insights_result,
                "timestamp": current_time,
            }

        # Update session insights
        session["insights_generated"] = insights_result.get("insights", [])
        session["metrics"]["insights_created"] = len(
            insights_result.get("insights", [])
        )

        return {
            "success": True,
            "session_id": session_id,
            "insight_type": insight_type,
            "insights": insights_result.get("insights", []),
            "total_count": len(insights_result.get("insights", [])),
            "actionable_count": len(
                [
                    i
                    for i in insights_result.get("insights", [])
                    if i.get("actionable", False)
                ]
            ),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def get_recommendations(session_id: str) -> Dict[str, Any]:
    """Get breakthrough recommendations for a session."""
    try:
        if session_id not in _analysis_sessions:
            return {
                "success": False,
                "error": f"Session {session_id} not found",
                "timestamp": datetime.now().isoformat(),
            }

        session = _analysis_sessions[session_id]

        # Generate recommendations based on insights and patterns
        recommendations_result = _insight_generator.generate_recommendations(
            session["patterns_found"],
            session["insights_generated"],
            session["analysis_results"],
        )

        # Update session recommendations
        session["recommendations"] = recommendations_result.get("recommendations", [])

        return {
            "success": True,
            "session_id": session_id,
            "recommendations": recommendations_result.get("recommendations", []),
            "total_count": len(recommendations_result.get("recommendations", [])),
            "high_priority_count": len(
                [
                    r
                    for r in recommendations_result.get("recommendations", [])
                    if r.get("priority") == "high"
                ]
            ),
            "breakthrough_opportunities": recommendations_result.get(
                "breakthrough_opportunities", []
            ),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def analyze_breakthrough(
    project_path: str, context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Analyze project for breakthrough opportunities."""
    try:
        if context is None:
            context = {}

        # Create temporary session for analysis
        session_result = create_session(project_path, "breakthrough_analysis")
        if not session_result.get("success"):
            return session_result

        session_id = session_result["session_id"]

        # Start comprehensive analysis
        start_result = start_analysis(session_id, "breakthrough_focused")
        if not start_result.get("success"):
            close_session(session_id)
            return start_result

        # Get analysis results
        analysis_result = get_analysis_results(session_id)

        # Get breakthrough patterns
        patterns_result = get_patterns(session_id, "breakthrough")

        # Generate insights
        insights_result = get_insights(session_id, "breakthrough")

        # Get recommendations
        recommendations_result = get_recommendations(session_id)

        # Compile breakthrough analysis
        breakthrough_analysis = {
            "success": True,
            "session_id": session_id,
            "project_path": os.path.abspath(project_path),
            "analysis_summary": {
                "files_analyzed": analysis_result.get("analysis_results", {}).get(
                    "files_scanned", 0
                ),
                "breakthrough_patterns": patterns_result.get("breakthrough_count", 0),
                "actionable_insights": insights_result.get("actionable_count", 0),
                "high_priority_recommendations": recommendations_result.get(
                    "high_priority_count", 0
                ),
            },
            "breakthrough_opportunities": recommendations_result.get(
                "breakthrough_opportunities", []
            ),
            "patterns": patterns_result.get("patterns", []),
            "insights": insights_result.get("insights", []),
            "recommendations": recommendations_result.get("recommendations", []),
            "context": context,
            "timestamp": datetime.now().isoformat(),
        }

        # Close session
        close_session(session_id)

        return breakthrough_analysis

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def get_learning_context(session_id: str) -> Dict[str, Any]:
    """Get learning context and patterns for a session."""
    try:
        if session_id not in _analysis_sessions:
            return {
                "success": False,
                "error": f"Session {session_id} not found",
                "timestamp": datetime.now().isoformat(),
            }

        session = _analysis_sessions[session_id]

        # Generate learning context
        learning_result = _learning_analyzer.analyze_learning_context(
            session["project_path"],
            session["analysis_results"],
            session["patterns_found"],
        )

        # Cache learning context
        _learning_contexts[session_id] = learning_result

        return {
            "success": True,
            "session_id": session_id,
            "learning_context": learning_result,
            "learning_patterns": learning_result.get("learning_patterns", []),
            "skill_gaps": learning_result.get("skill_gaps", []),
            "growth_opportunities": learning_result.get("growth_opportunities", []),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def generate_insights(
    session_id: str, insight_types: List[str] = None
) -> Dict[str, Any]:
    """Generate comprehensive insights for a session."""
    try:
        if insight_types is None:
            insight_types = ["breakthrough", "learning", "workflow", "optimization"]

        if session_id not in _analysis_sessions:
            return {
                "success": False,
                "error": f"Session {session_id} not found",
                "timestamp": datetime.now().isoformat(),
            }

        all_insights = []

        for insight_type in insight_types:
            insight_result = get_insights(session_id, insight_type)
            if insight_result.get("success"):
                all_insights.extend(insight_result.get("insights", []))

        return {
            "success": True,
            "session_id": session_id,
            "insights": all_insights,
            "total_count": len(all_insights),
            "insight_types": insight_types,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }
