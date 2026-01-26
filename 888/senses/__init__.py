"""
Senses module for multimodal input (gesture + speech) recognition.

This module implements the Maestro "Senses" system that provides:
- Gesture recognition using MediaPipe
- Speech recognition using Whisper
- Multimodal fusion for spell-based commands
- Integration with Enhanced Director Intelligence

The system follows the established PyO3→Bridge→Tauri→UI architecture pattern.
"""

from .adapter import *

__all__ = [
    'get_version', 
    'health_check', 
    'enable_senses', 
    'disable_senses',
    'process_multimodal_frame',
    'get_senses_analytics'
]
