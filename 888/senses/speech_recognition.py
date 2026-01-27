import whisper
import numpy as np
import pyaudio
import wave
import threading
import queue
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class SpeechData:
    transcription: str
    confidence: float
    language: str
    timestamp: int
    duration_ms: int
    audio_level: float

class SpeechRecognitionEngine:
    """
    Real-time speech recognition using Whisper for multimodal spell commands.

    Integrates with Enhanced Director Intelligence for context-aware speech interpretation.
    """

    def __init__(self, model_size: str = "base"):
        # Load Whisper model
        self.model = whisper.load_model(model_size)

        # Audio configuration
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16

        # Recognition settings
        self.recognition_settings = {
            'min_confidence': 0.7,
            'min_speech_duration': 500,  # ms
            'max_silence_duration': 2000,  # ms
            'voice_activity_threshold': 0.01,
        }

        # State tracking
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.speech_history: List[SpeechData] = []
        self.current_transcription = ""

        # Audio processing
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.processing_thread = None

    def start_listening(self) -> Dict[str, Any]:
        """Start continuous speech recognition."""
        try:
            if self.is_listening:
                return {'success': False, 'error': 'Already listening'}

            # Open audio stream
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback
            )

            # Start processing thread
            self.processing_thread = threading.Thread(target=self._process_audio_loop)
            self.processing_thread.daemon = True
            self.processing_thread.start()

            self.is_listening = True
            self.stream.start_stream()

            return {
                'success': True,
                'status': 'listening',
                'started_at': int(time.time() * 1000)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def stop_listening(self) -> Dict[str, Any]:
        """Stop speech recognition."""
        try:
            if not self.is_listening:
                return {'success': False, 'error': 'Not currently listening'}

            self.is_listening = False

            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None

            return {
                'success': True,
                'status': 'stopped',
                'stopped_at': int(time.time() * 1000)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Audio stream callback for continuous capture."""
        if self.is_listening:
            # Calculate audio level
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            audio_level = np.sqrt(np.mean(audio_data**2)) / 32768.0

            # Add to processing queue if above threshold
            if audio_level > self.recognition_settings['voice_activity_threshold']:
                self.audio_queue.put((in_data, audio_level, time.time()))

        return (in_data, pyaudio.paContinue)

    def _process_audio_loop(self):
        """Main audio processing loop."""
        audio_buffer = []
        last_speech_time = time.time()

        while self.is_listening:
            try:
                # Get audio data with timeout
                try:
                    audio_data, audio_level, timestamp = self.audio_queue.get(timeout=0.1)
                    audio_buffer.append(audio_data)
                    last_speech_time = timestamp
                except queue.Empty:
                    # Check for silence timeout
                    if (time.time() - last_speech_time >
                        self.recognition_settings['max_silence_duration'] / 1000.0):
                        if audio_buffer:
                            # Process accumulated audio
                            self._process_audio_buffer(audio_buffer)
                            audio_buffer = []
                    continue

                # Process buffer if it gets too large
                if len(audio_buffer) > 50:  # ~5 seconds at 10 chunks/sec
                    self._process_audio_buffer(audio_buffer)
                    audio_buffer = []

            except Exception as e:
                print(f"Error in audio processing loop: {e}")

    def _process_audio_buffer(self, audio_buffer: List[bytes]):
        """Process accumulated audio buffer for speech recognition."""
        if not audio_buffer:
            return

        try:
            # Combine audio chunks
            combined_audio = b''.join(audio_buffer)

            # Convert to numpy array
            audio_data = np.frombuffer(combined_audio, dtype=np.int16).astype(np.float32) / 32768.0

            # Skip if too short
            duration_ms = len(audio_data) / self.sample_rate * 1000
            if duration_ms < self.recognition_settings['min_speech_duration']:
                return

            # Transcribe with Whisper
            result = self.model.transcribe(
                audio_data,
                language='en',  # Can be made configurable
                task='transcribe'
            )

            transcription = result['text'].strip()

            if transcription and len(transcription) > 1:
                # Calculate confidence (Whisper doesn't provide direct confidence)
                # Use segment-level confidence if available
                confidence = 0.8  # Default confidence
                if 'segments' in result and result['segments']:
                    segment_confidences = []
                    for segment in result['segments']:
                        if 'avg_logprob' in segment:
                            # Convert log probability to confidence estimate
                            segment_conf = min(1.0, max(0.0, (segment['avg_logprob'] + 1.0)))
                            segment_confidences.append(segment_conf)
                    if segment_confidences:
                        confidence = sum(segment_confidences) / len(segment_confidences)

                # Create speech data
                speech_data = SpeechData(
                    transcription=transcription,
                    confidence=confidence,
                    language=result.get('language', 'en'),
                    timestamp=int(time.time() * 1000),
                    duration_ms=int(duration_ms),
                    audio_level=0.5  # Placeholder
                )

                # Update current transcription and history
                self.current_transcription = transcription
                self.speech_history.append(speech_data)

                # Keep only recent history
                if len(self.speech_history) > 50:
                    self.speech_history = self.speech_history[-50:]

        except Exception as e:
            print(f"Error processing audio buffer: {e}")

    def get_current_transcription(self) -> Dict[str, Any]:
        """Get the most recent transcription."""
        return {
            'success': True,
            'transcription': self.current_transcription,
            'is_listening': self.is_listening,
            'timestamp': int(time.time() * 1000)
        }

    def get_speech_analytics(self) -> Dict[str, Any]:
        """Get analytics about speech recognition performance."""
        if not self.speech_history:
            return {
                'total_transcriptions': 0,
                'average_confidence': 0.0,
                'average_duration': 0.0,
                'languages_detected': {}
            }

        languages = {}
        total_confidence = 0.0
        total_duration = 0.0

        for speech in self.speech_history:
            languages[speech.language] = languages.get(speech.language, 0) + 1
            total_confidence += speech.confidence
            total_duration += speech.duration_ms

        return {
            'total_transcriptions': len(self.speech_history),
            'average_confidence': total_confidence / len(self.speech_history),
            'average_duration': total_duration / len(self.speech_history),
            'languages_detected': languages
        }

    def cleanup(self):
        """Clean up resources."""
        self.stop_listening()
        if self.audio:
            self.audio.terminate()

def get_version() -> str:
    """Get speech recognition engine version."""
    return "1.0.0"

def health_check() -> Dict[str, Any]:
    """Perform health check of speech recognition system."""
    try:
        # Test Whisper model loading
        model = whisper.load_model("tiny")  # Use tiny model for quick test

        # Test PyAudio
        audio = pyaudio.PyAudio()
        audio.terminate()

        return {
            'success': True,
            'status': 'healthy',
            'whisper_available': True,
            'pyaudio_available': True,
            'checked_at': int(time.time() * 1000)
        }
    except Exception as e:
        return {
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'checked_at': int(time.time() * 1000)
        }

def create_speech_session(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create a new speech recognition session."""
    try:
        model_size = "base"
        if config and 'model_size' in config:
            model_size = config['model_size']

        engine = SpeechRecognitionEngine(model_size=model_size)

        # Apply configuration if provided
        if config:
            if 'recognition_settings' in config:
                engine.recognition_settings.update(config['recognition_settings'])

        session_id = f"speech_session_{int(time.time() * 1000)}"

        return {
            'success': True,
            'session_id': session_id,
            'engine': engine,  # In practice, stored in session manager
            'config': engine.recognition_settings,
            'created_at': int(time.time() * 1000)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'created_at': int(time.time() * 1000)
        }
