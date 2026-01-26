from typing import Dict, Any, Optional
import json
import time
from .gesture_recognition import create_gesture_session, process_gesture_frame, health_check as gesture_health
from .speech_recognition import create_speech_session, health_check as speech_health
from .multimodal_fusion import create_fusion_session, health_check as fusion_health

# Global session management
_gesture_session = None
_speech_session = None
_fusion_session = None
_senses_enabled = False

def get_version() -> str:
    return "1.0.0"

def health_check() -> Dict[str, Any]:
    """Comprehensive health check for all senses components."""
    gesture_status = gesture_health()
    speech_status = speech_health()
    fusion_status = fusion_health()

    overall_healthy = (gesture_status['success'] and
                      speech_status['success'] and
                      fusion_status['success'])

    return {
        'success': overall_healthy,
        'status': 'healthy' if overall_healthy else 'degraded',
        'components': {
            'gesture_recognition': gesture_status,
            'speech_recognition': speech_status,
            'multimodal_fusion': fusion_status
        },
        'senses_enabled': _senses_enabled,
        'checked_at': int(time.time() * 1000)
    }

def enable_senses(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Enable multimodal senses with optional configuration."""
    global _gesture_session, _speech_session, _fusion_session, _senses_enabled

    try:
        if _senses_enabled:
            return {'success': False, 'error': 'Senses already enabled'}

        # Create sessions
        gesture_result = create_gesture_session(config.get('gesture', {}) if config else None)
        if not gesture_result['success']:
            return {'success': False, 'error': f"Gesture session failed: {gesture_result['error']}"}

        speech_result = create_speech_session(config.get('speech', {}) if config else None)
        if not speech_result['success']:
            return {'success': False, 'error': f"Speech session failed: {speech_result['error']}"}

        fusion_result = create_fusion_session(config.get('fusion', {}) if config else None)
        if not fusion_result['success']:
            return {'success': False, 'error': f"Fusion session failed: {fusion_result['error']}"}

        _gesture_session = gesture_result
        _speech_session = speech_result
        _fusion_session = fusion_result
        _senses_enabled = True

        return {
            'success': True,
            'message': 'Multimodal senses enabled successfully',
            'sessions': {
                'gesture': gesture_result['session_id'],
                'speech': speech_result['session_id'],
                'fusion': fusion_result['session_id']
            },
            'enabled_at': int(time.time() * 1000)
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def disable_senses() -> Dict[str, Any]:
    """Disable multimodal senses."""
    global _gesture_session, _speech_session, _fusion_session, _senses_enabled

    try:
        if not _senses_enabled:
            return {'success': False, 'error': 'Senses not currently enabled'}

        # Clean up sessions
        if _speech_session and 'engine' in _speech_session:
            _speech_session['engine'].cleanup()

        _gesture_session = None
        _speech_session = None
        _fusion_session = None
        _senses_enabled = False

        return {
            'success': True,
            'message': 'Multimodal senses disabled successfully',
            'disabled_at': int(time.time() * 1000)
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def process_multimodal_frame(frame_data: bytes, audio_enabled: bool = True) -> Dict[str, Any]:
    """Process a frame for multimodal input recognition."""
    if not _senses_enabled:
        return {'success': False, 'error': 'Senses not enabled'}

    try:
        # Process gesture
        gesture_result = process_gesture_frame(_gesture_session['session_id'], frame_data)

        # Get current speech transcription
        speech_result = {'success': True, 'transcription': '', 'confidence': 0.0}
        if audio_enabled and _speech_session and 'engine' in _speech_session:
            speech_result = _speech_session['engine'].get_current_transcription()

        # Attempt multimodal fusion
        spell_intent = None
        if (gesture_result['success'] and gesture_result.get('gesture_detected') and
            speech_result['success'] and speech_result.get('transcription')):

            # Create data objects for fusion
            from .gesture_recognition import GestureData
            from .speech_recognition import SpeechData

            if gesture_result['gesture_detected']:
                gesture_data = GestureData(
                    gesture_type=gesture_result['gesture_type'],
                    confidence=gesture_result['confidence'],
                    hand_landmarks=[],  # Simplified for adapter
                    timestamp=gesture_result['timestamp'],
                    bounding_box=gesture_result.get('bounding_box', {})
                )
            else:
                gesture_data = None

            if speech_result.get('transcription'):
                speech_data = SpeechData(
                    transcription=speech_result['transcription'],
                    confidence=speech_result.get('confidence', 0.8),
                    language='en',
                    timestamp=speech_result['timestamp'],
                    duration_ms=1000,  # Placeholder
                    audio_level=0.5
                )
            else:
                speech_data = None

            # Process through fusion engine
            if _fusion_session and 'engine' in _fusion_session:
                spell_intent = _fusion_session['engine'].process_multimodal_input(gesture_data, speech_data)

        return {
            'success': True,
            'gesture': gesture_result,
            'speech': speech_result,
            'spell_intent': {
                'detected': spell_intent is not None,
                'spell_id': spell_intent.spell_id if spell_intent else None,
                'confidence': spell_intent.confidence if spell_intent else 0.0,
                'target_action': spell_intent.target_action if spell_intent else None,
                'target_panel': spell_intent.target_panel if spell_intent else None,
                'parameters': spell_intent.parameters if spell_intent else {}
            } if spell_intent else {'detected': False},
            'processed_at': int(time.time() * 1000)
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_senses_analytics() -> Dict[str, Any]:
    """Get comprehensive analytics from all senses components."""
    if not _senses_enabled:
        return {'success': False, 'error': 'Senses not enabled'}

    try:
        analytics = {
            'success': True,
            'senses_enabled': True,
            'gesture_analytics': {},
            'speech_analytics': {},
            'fusion_analytics': {}
        }

        # Get gesture analytics
        if _gesture_session and 'engine' in _gesture_session:
            analytics['gesture_analytics'] = _gesture_session['engine'].get_gesture_analytics()

        # Get speech analytics
        if _speech_session and 'engine' in _speech_session:
            analytics['speech_analytics'] = _speech_session['engine'].get_speech_analytics()

        # Get fusion analytics
        if _fusion_session and 'engine' in _fusion_session:
            analytics['fusion_analytics'] = _fusion_session['engine'].get_fusion_analytics()

        return analytics
    except Exception as e:
        return {'success': False, 'error': str(e)}
