"""
Enhanced Speech Recognition Module for Phase 7.2 ML Enhanced Recognition.

This module implements user-specific voice profiles and context-aware speech recognition
to improve transcription accuracy through personalized adaptation and environmental optimization.

Key Features:
- UserVoiceProfile for personalized voice characteristics
- SpeechContextEngine for context-aware processing
- VocabularyAdapter for domain-specific vocabulary expansion
- WhisperModelAdapter for enhanced Whisper integration
- Environmental adaptation and noise handling
"""

import json
import time
import numpy as np
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional, Tuple
import logging

# ML and audio dependencies (graceful fallback if not available)
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    whisper = None

try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    librosa = None

try:
    import scipy.signal
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    scipy = None

# Import existing speech recognition components
from .speech_recognition import SpeechData, SpeechRecognitionEngine

logger = logging.getLogger(__name__)


@dataclass
class UserVoiceProfile:
    """User-specific voice profile for personalized recognition."""
    user_id: str
    voice_characteristics: Dict[str, Any]  # Pitch, tone, accent, etc.
    pronunciation_patterns: Dict[str, List[str]]  # Word -> pronunciation variants
    vocabulary_preferences: Dict[str, float]  # Domain-specific vocabulary weights
    adaptation_data: Dict[str, Any]  # Personalized adaptation parameters
    created_at: int
    last_updated: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserVoiceProfile':
        """Create profile from dictionary."""
        return cls(**data)


@dataclass
class SpeechContextEngine:
    """Context engine for domain-aware speech processing."""
    domain_vocabularies: Dict[str, List[str]]  # Domain -> vocabulary list
    context_weights: Dict[str, float]  # Context type -> weight
    temporal_patterns: Dict[str, Any]  # Time-based speech patterns
    workspace_integration: Dict[str, Any]  # Integration with workspace context
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SpeechContextEngine':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class VoiceSample:
    """Individual voice sample for profile creation."""
    audio_data: bytes
    transcription: str
    duration_ms: int
    sample_rate: int
    timestamp: int
    quality_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (excluding audio data for size)."""
        return {
            'transcription': self.transcription,
            'duration_ms': self.duration_ms,
            'sample_rate': self.sample_rate,
            'timestamp': self.timestamp,
            'quality_score': self.quality_score
        }


class VocabularyAdapter:
    """Adapter for domain-specific vocabulary expansion."""
    
    def __init__(self):
        self.domain_vocabularies = {
            'coding': [
                'function', 'variable', 'class', 'method', 'array', 'object',
                'string', 'integer', 'boolean', 'null', 'undefined', 'async',
                'await', 'promise', 'callback', 'closure', 'prototype', 'scope'
            ],
            'writing': [
                'paragraph', 'sentence', 'chapter', 'section', 'heading',
                'bullet', 'list', 'format', 'style', 'font', 'bold', 'italic'
            ],
            'design': [
                'color', 'palette', 'gradient', 'shadow', 'border', 'margin',
                'padding', 'layout', 'grid', 'flex', 'responsive', 'mobile'
            ],
            'general': [
                'open', 'close', 'save', 'delete', 'copy', 'paste', 'cut',
                'undo', 'redo', 'search', 'find', 'replace', 'navigate'
            ]
        }
        
        self.context_weights = {
            'coding': 1.2,
            'writing': 1.1,
            'design': 1.1,
            'general': 1.0
        }
    
    def get_domain_vocabulary(self, domain: str) -> List[str]:
        """Get vocabulary for specific domain."""
        return self.domain_vocabularies.get(domain, self.domain_vocabularies['general'])
    
    def expand_vocabulary(self, domain: str, new_words: List[str]) -> Dict[str, Any]:
        """Expand vocabulary for specific domain."""
        try:
            if domain not in self.domain_vocabularies:
                self.domain_vocabularies[domain] = []
            
            # Add new words (avoid duplicates)
            added_words = []
            for word in new_words:
                if word.lower() not in [w.lower() for w in self.domain_vocabularies[domain]]:
                    self.domain_vocabularies[domain].append(word.lower())
                    added_words.append(word.lower())
            
            return {
                'success': True,
                'domain': domain,
                'added_words': added_words,
                'total_vocabulary_size': len(self.domain_vocabularies[domain])
            }
            
        except Exception as e:
            logger.error(f"Error expanding vocabulary: {e}")
            return {
                'success': False,
                'error': f'Vocabulary expansion failed: {str(e)}'
            }
    
    def get_context_boost(self, word: str, domain: str) -> float:
        """Get context boost for word in specific domain."""
        domain_vocab = self.get_domain_vocabulary(domain)
        if word.lower() in [w.lower() for w in domain_vocab]:
            return self.context_weights.get(domain, 1.0)
        return 1.0


class WhisperModelAdapter:
    """Enhanced adapter for Whisper model integration."""
    
    def __init__(self):
        self.model = None
        self.model_size = "base"
        self.is_loaded = False
        
    def load_model(self, model_size: str = "base") -> Dict[str, Any]:
        """Load Whisper model with specified size."""
        if not WHISPER_AVAILABLE:
            return {
                'success': False,
                'error': 'Whisper not available - install openai-whisper'
            }
        
        try:
            self.model = whisper.load_model(model_size)
            self.model_size = model_size
            self.is_loaded = True
            
            return {
                'success': True,
                'model_size': model_size,
                'message': f'Whisper {model_size} model loaded successfully'
            }
            
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            return {
                'success': False,
                'error': f'Model loading failed: {str(e)}'
            }
    
    def transcribe_with_context(self, audio_data: bytes, context: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced transcription with context awareness."""
        if not self.is_loaded or not WHISPER_AVAILABLE:
            return {
                'success': False,
                'error': 'Whisper model not loaded'
            }
        
        try:
            # Convert audio data to format Whisper expects
            # This is a simplified implementation - real implementation would handle audio conversion
            
            # Get domain context for vocabulary boosting
            domain = context.get('domain', 'general')
            
            # Perform transcription
            result = self.model.transcribe(audio_data)
            
            # Apply context-aware post-processing
            transcription = result['text']
            confidence = result.get('confidence', 0.0)
            
            # Apply domain-specific corrections (simplified)
            if domain == 'coding':
                transcription = self._apply_coding_corrections(transcription)
            elif domain == 'writing':
                transcription = self._apply_writing_corrections(transcription)
            
            return {
                'success': True,
                'transcription': transcription,
                'confidence': confidence,
                'language': result.get('language', 'en'),
                'domain': domain
            }
            
        except Exception as e:
            logger.error(f"Error in context-aware transcription: {e}")
            return {
                'success': False,
                'error': f'Transcription failed: {str(e)}'
            }
    
    def _apply_coding_corrections(self, text: str) -> str:
        """Apply coding-specific corrections to transcription."""
        # Common coding transcription corrections
        corrections = {
            'def': 'def',
            'death': 'def',
            'class': 'class',
            'glass': 'class',
            'function': 'function',
            'return': 'return',
            'if': 'if',
            'else': 'else',
            'for': 'for',
            'while': 'while'
        }
        
        words = text.split()
        corrected_words = []
        
        for word in words:
            corrected_word = corrections.get(word.lower(), word)
            corrected_words.append(corrected_word)
        
        return ' '.join(corrected_words)
    
    def _apply_writing_corrections(self, text: str) -> str:
        """Apply writing-specific corrections to transcription."""
        # Common writing transcription corrections
        corrections = {
            'period': '.',
            'comma': ',',
            'question mark': '?',
            'exclamation point': '!',
            'new paragraph': '\n\n',
            'new line': '\n'
        }
        
        corrected_text = text
        for phrase, replacement in corrections.items():
            corrected_text = corrected_text.replace(phrase, replacement)
        
        return corrected_text


class EnhancedSpeechRecognition:
    """
    Main class for enhanced speech recognition with voice profiles and context awareness.

    Provides personalized speech recognition through voice profile adaptation,
    environmental optimization, and domain-specific vocabulary enhancement.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # Initialize components
        self.voice_profile = None
        self.context_engine = SpeechContextEngine(
            domain_vocabularies={},
            context_weights={},
            temporal_patterns={},
            workspace_integration={}
        )
        self.vocabulary_adapter = VocabularyAdapter()
        self.whisper_adapter = WhisperModelAdapter()

        # Base speech recognition engine
        self.base_engine = SpeechRecognitionEngine()

        # Voice samples for profile creation
        self.voice_samples = []

        # Load existing data
        self._load_context_engine()

    def create_voice_profile(self, voice_samples: List[bytes]) -> Dict[str, Any]:
        """
        Create personalized voice profile for improved recognition accuracy.

        Args:
            voice_samples: List of audio samples for voice profiling

        Returns:
            Voice profile creation results with accuracy improvements
        """
        try:
            if not voice_samples:
                return {
                    'success': False,
                    'error': 'No voice samples provided'
                }

            # Analyze voice characteristics from samples
            voice_characteristics = self._analyze_voice_characteristics(voice_samples)

            # Extract pronunciation patterns
            pronunciation_patterns = self._extract_pronunciation_patterns(voice_samples)

            # Create voice profile
            self.voice_profile = UserVoiceProfile(
                user_id="default_user",  # Would be parameterized in real implementation
                voice_characteristics=voice_characteristics,
                pronunciation_patterns=pronunciation_patterns,
                vocabulary_preferences={},
                adaptation_data={},
                created_at=int(time.time() * 1000),
                last_updated=int(time.time() * 1000)
            )

            # Save profile
            self._save_voice_profile()

            return {
                'success': True,
                'profile_created': True,
                'voice_characteristics': voice_characteristics,
                'pronunciation_patterns_count': len(pronunciation_patterns),
                'samples_analyzed': len(voice_samples),
                'message': 'Voice profile created successfully'
            }

        except Exception as e:
            logger.error(f"Error creating voice profile: {e}")
            return {
                'success': False,
                'error': f'Voice profile creation failed: {str(e)}'
            }

    def adapt_to_environment(self, audio_characteristics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt speech recognition to current audio environment.

        Args:
            audio_characteristics: Current audio environment data (noise, echo, etc.)

        Returns:
            Environment adaptation results and configuration updates
        """
        try:
            # Extract environment characteristics
            noise_level = audio_characteristics.get('noise_level', 0.0)
            echo_level = audio_characteristics.get('echo_level', 0.0)
            background_type = audio_characteristics.get('background_type', 'quiet')

            # Calculate adaptation parameters
            adaptations = {}

            # Adjust for noise level
            if noise_level > 0.7:
                adaptations['noise_reduction'] = True
                adaptations['sensitivity_threshold'] = min(0.9, 0.6 + noise_level * 0.3)
            elif noise_level < 0.3:
                adaptations['noise_reduction'] = False
                adaptations['sensitivity_threshold'] = max(0.4, 0.6 - noise_level * 0.2)

            # Adjust for echo
            if echo_level > 0.5:
                adaptations['echo_cancellation'] = True
                adaptations['processing_delay'] = min(200, 100 + echo_level * 100)

            # Adjust for background type
            if background_type == 'music':
                adaptations['frequency_filtering'] = 'high_pass'
                adaptations['voice_isolation'] = True
            elif background_type == 'conversation':
                adaptations['speaker_separation'] = True
                adaptations['voice_isolation'] = True

            # Update context engine with environment data
            self.context_engine.workspace_integration['environment'] = {
                'noise_level': noise_level,
                'echo_level': echo_level,
                'background_type': background_type,
                'adaptations': adaptations,
                'timestamp': int(time.time() * 1000)
            }

            # Save updated context
            self._save_context_engine()

            return {
                'success': True,
                'adaptations': adaptations,
                'environment_analyzed': True,
                'noise_level': noise_level,
                'echo_level': echo_level,
                'message': 'Environment adaptation completed'
            }

        except Exception as e:
            logger.error(f"Error adapting to environment: {e}")
            return {
                'success': False,
                'error': f'Environment adaptation failed: {str(e)}'
            }

    def expand_vocabulary(self, domain_context: str) -> Dict[str, Any]:
        """
        Expand recognition vocabulary based on current work domain.

        Args:
            domain_context: Current work domain ("coding", "writing", "design", etc.)

        Returns:
            Vocabulary expansion results and recognition improvements
        """
        try:
            # Get domain-specific vocabulary
            domain_vocab = self.vocabulary_adapter.get_domain_vocabulary(domain_context)

            # Update context engine with domain vocabulary
            self.context_engine.domain_vocabularies[domain_context] = domain_vocab

            # Set context weights
            context_weight = self.vocabulary_adapter.context_weights.get(domain_context, 1.0)
            self.context_engine.context_weights[domain_context] = context_weight

            # Update temporal patterns for domain switching
            current_time = int(time.time() * 1000)
            if 'domain_switches' not in self.context_engine.temporal_patterns:
                self.context_engine.temporal_patterns['domain_switches'] = []

            self.context_engine.temporal_patterns['domain_switches'].append({
                'domain': domain_context,
                'timestamp': current_time,
                'vocabulary_size': len(domain_vocab)
            })

            # Keep only recent domain switches (last 50)
            if len(self.context_engine.temporal_patterns['domain_switches']) > 50:
                self.context_engine.temporal_patterns['domain_switches'] = \
                    self.context_engine.temporal_patterns['domain_switches'][-50:]

            # Save updated context
            self._save_context_engine()

            return {
                'success': True,
                'domain': domain_context,
                'vocabulary_size': len(domain_vocab),
                'context_weight': context_weight,
                'domain_switches_recorded': len(self.context_engine.temporal_patterns['domain_switches']),
                'message': f'Vocabulary expanded for {domain_context} domain'
            }

        except Exception as e:
            logger.error(f"Error expanding vocabulary: {e}")
            return {
                'success': False,
                'error': f'Vocabulary expansion failed: {str(e)}'
            }

    def get_contextual_transcription(self, audio_data: bytes, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhanced transcription with context awareness and voice profile.

        Args:
            audio_data: Raw audio data for transcription
            context: Current workspace context for improved accuracy

        Returns:
            Enhanced transcription with confidence scores and alternatives
        """
        try:
            # Load Whisper model if not already loaded
            if not self.whisper_adapter.is_loaded:
                load_result = self.whisper_adapter.load_model("base")
                if not load_result['success']:
                    # Fallback to base engine
                    return self._fallback_transcription(audio_data, context)

            # Enhance context with voice profile and domain information
            enhanced_context = context.copy()

            # Add domain context
            domain = context.get('domain', 'general')
            enhanced_context['domain_vocabulary'] = self.vocabulary_adapter.get_domain_vocabulary(domain)
            enhanced_context['context_weight'] = self.vocabulary_adapter.get_context_boost("", domain)

            # Add voice profile information
            if self.voice_profile:
                enhanced_context['voice_characteristics'] = self.voice_profile.voice_characteristics
                enhanced_context['pronunciation_patterns'] = self.voice_profile.pronunciation_patterns

            # Add environment adaptations
            if 'environment' in self.context_engine.workspace_integration:
                enhanced_context['environment'] = self.context_engine.workspace_integration['environment']

            # Perform enhanced transcription
            transcription_result = self.whisper_adapter.transcribe_with_context(audio_data, enhanced_context)

            if transcription_result['success']:
                # Apply voice profile corrections if available
                transcription = transcription_result['transcription']
                if self.voice_profile:
                    transcription = self._apply_voice_profile_corrections(transcription)

                # Apply domain-specific post-processing
                transcription = self._apply_domain_corrections(transcription, domain)

                return {
                    'success': True,
                    'transcription': transcription,
                    'confidence': transcription_result.get('confidence', 0.0),
                    'language': transcription_result.get('language', 'en'),
                    'domain': domain,
                    'voice_profile_applied': self.voice_profile is not None,
                    'context_enhanced': True
                }
            else:
                return self._fallback_transcription(audio_data, context)

        except Exception as e:
            logger.error(f"Error in contextual transcription: {e}")
            return {
                'success': False,
                'error': f'Contextual transcription failed: {str(e)}'
            }

    def learn_speech_patterns(self, transcription_data: Dict[str, Any], feedback: bool) -> Dict[str, Any]:
        """Learn from user corrections to improve future transcriptions."""
        try:
            if not feedback:
                return {
                    'success': True,
                    'learning_applied': False,
                    'message': 'Negative feedback received, no learning applied'
                }

            # Extract learning data
            original_transcription = transcription_data.get('original_transcription', '')
            corrected_transcription = transcription_data.get('corrected_transcription', '')
            domain = transcription_data.get('domain', 'general')

            if not corrected_transcription or original_transcription == corrected_transcription:
                return {
                    'success': True,
                    'learning_applied': False,
                    'message': 'No corrections to learn from'
                }

            # Learn pronunciation patterns
            if self.voice_profile:
                self._learn_pronunciation_corrections(original_transcription, corrected_transcription)

            # Learn domain-specific vocabulary
            corrected_words = corrected_transcription.split()
            new_vocab = [word for word in corrected_words if len(word) > 2]  # Filter short words

            if new_vocab:
                vocab_result = self.vocabulary_adapter.expand_vocabulary(domain, new_vocab)
                vocab_added = vocab_result.get('added_words', [])
            else:
                vocab_added = []

            # Update voice profile
            if self.voice_profile:
                self.voice_profile.last_updated = int(time.time() * 1000)
                self._save_voice_profile()

            # Save updated context
            self._save_context_engine()

            return {
                'success': True,
                'learning_applied': True,
                'pronunciation_patterns_updated': self.voice_profile is not None,
                'vocabulary_added': vocab_added,
                'domain': domain,
                'message': 'Speech patterns learned successfully'
            }

        except Exception as e:
            logger.error(f"Error learning speech patterns: {e}")
            return {
                'success': False,
                'error': f'Speech pattern learning failed: {str(e)}'
            }

    def get_pronunciation_variants(self, word: str) -> List[str]:
        """Get pronunciation variants for improved recognition."""
        try:
            variants = [word.lower()]

            # Add voice profile variants if available
            if self.voice_profile and word.lower() in self.voice_profile.pronunciation_patterns:
                profile_variants = self.voice_profile.pronunciation_patterns[word.lower()]
                variants.extend(profile_variants)

            # Add common pronunciation variants
            common_variants = self._get_common_variants(word.lower())
            variants.extend(common_variants)

            # Remove duplicates and return
            return list(set(variants))

        except Exception as e:
            logger.error(f"Error getting pronunciation variants: {e}")
            return [word.lower()]

    def _analyze_voice_characteristics(self, voice_samples: List[bytes]) -> Dict[str, Any]:
        """Analyze voice characteristics from audio samples."""
        # Simplified implementation - real implementation would use audio analysis
        return {
            'pitch_range': {'min': 80.0, 'max': 300.0, 'average': 150.0},
            'speaking_rate': 'medium',  # words per minute analysis
            'accent_markers': [],
            'voice_quality': 'clear',
            'samples_analyzed': len(voice_samples)
        }

    def _extract_pronunciation_patterns(self, voice_samples: List[bytes]) -> Dict[str, List[str]]:
        """Extract pronunciation patterns from voice samples."""
        # Simplified implementation - real implementation would analyze audio
        return {
            'common_words': ['the', 'and', 'or', 'but'],
            'technical_terms': ['function', 'variable', 'class']
        }

    def _apply_voice_profile_corrections(self, transcription: str) -> str:
        """Apply voice profile-specific corrections."""
        if not self.voice_profile:
            return transcription

        corrected = transcription
        for word, variants in self.voice_profile.pronunciation_patterns.items():
            for variant in variants:
                corrected = corrected.replace(variant, word)

        return corrected

    def _apply_domain_corrections(self, transcription: str, domain: str) -> str:
        """Apply domain-specific corrections to transcription."""
        if domain == 'coding':
            return self.whisper_adapter._apply_coding_corrections(transcription)
        elif domain == 'writing':
            return self.whisper_adapter._apply_writing_corrections(transcription)
        return transcription

    def _learn_pronunciation_corrections(self, original: str, corrected: str):
        """Learn from pronunciation corrections."""
        if not self.voice_profile:
            return

        original_words = original.split()
        corrected_words = corrected.split()

        # Simple word-by-word learning (real implementation would be more sophisticated)
        for i, (orig_word, corr_word) in enumerate(zip(original_words, corrected_words)):
            if orig_word.lower() != corr_word.lower():
                if corr_word.lower() not in self.voice_profile.pronunciation_patterns:
                    self.voice_profile.pronunciation_patterns[corr_word.lower()] = []

                if orig_word.lower() not in self.voice_profile.pronunciation_patterns[corr_word.lower()]:
                    self.voice_profile.pronunciation_patterns[corr_word.lower()].append(orig_word.lower())

    def _get_common_variants(self, word: str) -> List[str]:
        """Get common pronunciation variants for a word."""
        # Simplified common variants - real implementation would use phonetic analysis
        common_variants = {
            'the': ['da', 'thee'],
            'and': ['an', 'nd'],
            'function': ['funk-shun', 'func-tion'],
            'variable': ['var-ee-able', 'vari-able']
        }
        return common_variants.get(word, [])

    def _fallback_transcription(self, audio_data: bytes, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback transcription using base engine."""
        try:
            # Use base speech recognition engine
            result = self.base_engine.transcribe_audio(audio_data)
            return {
                'success': True,
                'transcription': result.get('text', ''),
                'confidence': result.get('confidence', 0.0),
                'fallback_used': True,
                'message': 'Used fallback transcription engine'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Fallback transcription failed: {str(e)}'
            }

    def _save_voice_profile(self):
        """Save voice profile to disk."""
        try:
            if self.voice_profile:
                profile_path = self.data_dir / f"voice_profile_{self.voice_profile.user_id}.json"
                with open(profile_path, 'w') as f:
                    json.dump(self.voice_profile.to_dict(), f, indent=2)
        except Exception as e:
            logger.error(f"Error saving voice profile: {e}")

    def _load_voice_profile(self, user_id: str):
        """Load voice profile from disk."""
        try:
            profile_path = self.data_dir / f"voice_profile_{user_id}.json"
            if profile_path.exists():
                with open(profile_path, 'r') as f:
                    data = json.load(f)
                    self.voice_profile = UserVoiceProfile.from_dict(data)
        except Exception as e:
            logger.error(f"Error loading voice profile: {e}")

    def _save_context_engine(self):
        """Save context engine to disk."""
        try:
            context_path = self.data_dir / "speech_context.json"
            with open(context_path, 'w') as f:
                json.dump(self.context_engine.to_dict(), f, indent=2)
        except Exception as e:
            logger.error(f"Error saving context engine: {e}")

    def _load_context_engine(self):
        """Load context engine from disk."""
        try:
            context_path = self.data_dir / "speech_context.json"
            if context_path.exists():
                with open(context_path, 'r') as f:
                    data = json.load(f)
                    self.context_engine = SpeechContextEngine.from_dict(data)
        except Exception as e:
            logger.error(f"Error loading context engine: {e}")


# Module-level functions for integration with existing senses system
def create_enhanced_speech_recognition(data_dir: str = "data") -> Dict[str, Any]:
    """Create a new enhanced speech recognition instance."""
    try:
        recognition = EnhancedSpeechRecognition(data_dir=data_dir)
        return {
            'success': True,
            'recognition': recognition,
            'whisper_available': WHISPER_AVAILABLE,
            'librosa_available': LIBROSA_AVAILABLE,
            'message': 'Enhanced speech recognition created successfully'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to create enhanced speech recognition: {str(e)}'
        }
