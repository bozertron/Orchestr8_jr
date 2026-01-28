"""
Director module for cross-application OODA loop functionality.

This module implements the AI Director that provides contextual suggestions
based on behavioral analysis across all wrapped applications using telemetry data.
"""

from .user_context import UserContext
from .ooda_engine import OODAEngine
from .models import Suggestion

__all__ = ['UserContext', 'OODAEngine', 'Suggestion']
