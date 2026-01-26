"""
Adaptive Gesture Recognition Module for Phase 7.2 ML Enhanced Recognition.

This module implements user-specific gesture calibration and learning to improve
recognition accuracy through personalized adaptation and machine learning.

Key Features:
- UserGestureProfile for personalized calibration data
- CalibrationDataManager for training data management  
- GestureLearningEngine for ML model training
- TensorFlowModelAdapter for model integration
- Real-time personalized confidence scoring
"""

import json
import time
import numpy as np
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional, Tuple
import logging

# ML dependencies (graceful fallback if not available)
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    tf = None

try:
    import sklearn.metrics
    from sklearn.model_selection import train_test_split
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# Import existing gesture recognition components
from .gesture_recognition import GestureData, GestureRecognitionEngine

logger = logging.getLogger(__name__)


@dataclass
class UserGestureProfile:
    """User-specific gesture profile for personalized recognition."""
    user_id: str
    gesture_preferences: Dict[str, float]  # Gesture -> preference weight
    hand_characteristics: Dict[str, Any]   # Hand size, dominant hand, etc.
    calibration_data: Dict[str, Any]       # Personalized calibration parameters
    adaptation_history: List[Dict[str, Any]]  # Historical adaptation data
    created_at: int
    last_updated: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserGestureProfile':
        """Create profile from dictionary."""
        return cls(**data)


@dataclass
class CalibrationDataManager:
    """Manages calibration sessions and training data."""
    calibration_sessions: List[Dict[str, Any]]
    accuracy_metrics: Dict[str, float]
    threshold_adjustments: Dict[str, float]
    performance_trends: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CalibrationDataManager':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class GestureCalibrationSample:
    """Individual gesture sample for calibration."""
    gesture_type: str
    landmarks: List[List[float]]  # MediaPipe landmarks
    confidence: float
    timestamp: int
    user_feedback: bool  # True if user confirmed correct recognition
    hand_characteristics: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GestureCalibrationSample':
        """Create from dictionary."""
        return cls(**data)


class GestureLearningEngine:
    """Machine learning engine for gesture adaptation."""
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.feature_scaler = None
        self.gesture_classes = ['open_palm', 'fist', 'point', 'peace', 'thumbs_up']
        
    def extract_features(self, landmarks: List[List[float]]) -> np.ndarray:
        """Extract features from MediaPipe landmarks for ML training."""
        if not landmarks:
            return np.zeros(42)  # 21 landmarks * 2 coordinates
            
        # Flatten landmarks to feature vector
        features = []
        for landmark in landmarks:
            features.extend(landmark[:2])  # x, y coordinates only
            
        # Pad or truncate to fixed size
        features = features[:42]  # Ensure max 21 landmarks * 2
        while len(features) < 42:
            features.append(0.0)
            
        return np.array(features)
    
    def train_personalized_model(self, calibration_samples: List[GestureCalibrationSample]) -> Dict[str, Any]:
        """Train personalized gesture recognition model."""
        if not TENSORFLOW_AVAILABLE:
            return {
                'success': False,
                'error': 'TensorFlow not available - using fallback recognition'
            }
            
        try:
            # Prepare training data
            X = []
            y = []
            
            for sample in calibration_samples:
                if sample.user_feedback:  # Only use confirmed samples
                    features = self.extract_features(sample.landmarks)
                    X.append(features)
                    y.append(self.gesture_classes.index(sample.gesture_type))
            
            if len(X) < 10:  # Need minimum samples
                return {
                    'success': False,
                    'error': 'Insufficient training samples (need at least 10)'
                }
            
            X = np.array(X)
            y = np.array(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Create simple neural network
            self.model = tf.keras.Sequential([
                tf.keras.layers.Dense(64, activation='relu', input_shape=(42,)),
                tf.keras.layers.Dropout(0.3),
                tf.keras.layers.Dense(32, activation='relu'),
                tf.keras.layers.Dropout(0.3),
                tf.keras.layers.Dense(len(self.gesture_classes), activation='softmax')
            ])
            
            self.model.compile(
                optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
            )
            
            # Train model
            history = self.model.fit(
                X_train, y_train,
                epochs=50,
                batch_size=8,
                validation_data=(X_test, y_test),
                verbose=0
            )
            
            # Evaluate
            test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
            
            self.is_trained = True
            
            return {
                'success': True,
                'test_accuracy': float(test_accuracy),
                'training_samples': len(X),
                'epochs_trained': 50,
                'model_summary': str(self.model.summary())
            }
            
        except Exception as e:
            logger.error(f"Error training personalized model: {e}")
            return {
                'success': False,
                'error': f'Training failed: {str(e)}'
            }
    
    def predict_gesture(self, landmarks: List[List[float]]) -> Tuple[str, float]:
        """Predict gesture using personalized model."""
        if not self.is_trained or not TENSORFLOW_AVAILABLE:
            return "unknown", 0.0
            
        try:
            features = self.extract_features(landmarks)
            features = features.reshape(1, -1)
            
            predictions = self.model.predict(features, verbose=0)
            predicted_class = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class])
            
            gesture_type = self.gesture_classes[predicted_class]
            return gesture_type, confidence
            
        except Exception as e:
            logger.error(f"Error predicting gesture: {e}")
            return "unknown", 0.0


class TensorFlowModelAdapter:
    """Adapter for TensorFlow model integration."""
    
    def __init__(self):
        self.models = {}
        self.model_metadata = {}
        
    def save_model(self, user_id: str, model: tf.keras.Model, metadata: Dict[str, Any]) -> bool:
        """Save trained model for user."""
        if not TENSORFLOW_AVAILABLE:
            return False
            
        try:
            model_path = Path(f"data/models/gesture_{user_id}.h5")
            model_path.parent.mkdir(parents=True, exist_ok=True)
            
            model.save(str(model_path))
            
            # Save metadata
            metadata_path = Path(f"data/models/gesture_{user_id}_metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                
            return True
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False
    
    def load_model(self, user_id: str) -> Tuple[Optional[tf.keras.Model], Dict[str, Any]]:
        """Load trained model for user."""
        if not TENSORFLOW_AVAILABLE:
            return None, {}
            
        try:
            model_path = Path(f"data/models/gesture_{user_id}.h5")
            metadata_path = Path(f"data/models/gesture_{user_id}_metadata.json")
            
            if not model_path.exists():
                return None, {}
                
            model = tf.keras.models.load_model(str(model_path))
            
            metadata = {}
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    
            return model, metadata
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return None, {}


class AdaptiveGestureRecognition:
    """
    Main class for adaptive gesture recognition with user-specific calibration.

    Provides personalized gesture recognition through machine learning adaptation,
    user profile management, and continuous learning from user feedback.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # Initialize components
        self.user_profile = None
        self.calibration_data = CalibrationDataManager(
            calibration_sessions=[],
            accuracy_metrics={},
            threshold_adjustments={},
            performance_trends=[]
        )
        self.learning_engine = GestureLearningEngine()
        self.model_adapter = TensorFlowModelAdapter()

        # Base gesture recognition engine
        self.base_engine = GestureRecognitionEngine()

        # Calibration state
        self.calibration_samples = []
        self.is_calibrating = False

    def calibrate_user_gestures(self, gesture_samples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calibrate gesture recognition for specific user through sample collection.

        Args:
            gesture_samples: List of labeled gesture samples for training

        Returns:
            Calibration results with accuracy metrics and personalized thresholds
        """
        try:
            # Convert samples to calibration format
            calibration_samples = []
            for sample_data in gesture_samples:
                sample = GestureCalibrationSample(
                    gesture_type=sample_data.get('gesture_type', 'unknown'),
                    landmarks=sample_data.get('landmarks', []),
                    confidence=sample_data.get('confidence', 0.0),
                    timestamp=sample_data.get('timestamp', int(time.time() * 1000)),
                    user_feedback=sample_data.get('user_feedback', True),
                    hand_characteristics=sample_data.get('hand_characteristics', {})
                )
                calibration_samples.append(sample)

            # Train personalized model
            training_result = self.learning_engine.train_personalized_model(calibration_samples)

            if training_result['success']:
                # Update calibration data
                session_data = {
                    'timestamp': int(time.time() * 1000),
                    'samples_count': len(calibration_samples),
                    'accuracy': training_result.get('test_accuracy', 0.0),
                    'training_result': training_result
                }
                self.calibration_data.calibration_sessions.append(session_data)

                # Update accuracy metrics
                self.calibration_data.accuracy_metrics['latest_accuracy'] = training_result.get('test_accuracy', 0.0)
                self.calibration_data.accuracy_metrics['total_sessions'] = len(self.calibration_data.calibration_sessions)

                # Save calibration data
                self._save_calibration_data()

                return {
                    'success': True,
                    'accuracy': training_result.get('test_accuracy', 0.0),
                    'samples_used': len(calibration_samples),
                    'model_trained': True,
                    'message': 'User gesture calibration completed successfully'
                }
            else:
                return {
                    'success': False,
                    'error': training_result.get('error', 'Unknown training error'),
                    'samples_provided': len(calibration_samples)
                }

        except Exception as e:
            logger.error(f"Error in user gesture calibration: {e}")
            return {
                'success': False,
                'error': f'Calibration failed: {str(e)}'
            }

    def adapt_recognition_thresholds(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Continuously adapt recognition thresholds based on user performance.

        Args:
            performance_data: User performance metrics and feedback data

        Returns:
            Updated threshold configuration and adaptation results
        """
        try:
            # Extract performance metrics
            accuracy = performance_data.get('accuracy', 0.0)
            false_positives = performance_data.get('false_positives', 0)
            false_negatives = performance_data.get('false_negatives', 0)
            user_satisfaction = performance_data.get('user_satisfaction', 0.5)

            # Calculate threshold adjustments
            adjustments = {}

            # If accuracy is low, lower thresholds to be more sensitive
            if accuracy < 0.7:
                adjustments['confidence_threshold'] = max(0.3, accuracy - 0.1)
                adjustments['gesture_threshold'] = max(0.4, accuracy - 0.05)

            # If too many false positives, raise thresholds
            elif false_positives > 5:
                adjustments['confidence_threshold'] = min(0.9, accuracy + 0.1)
                adjustments['gesture_threshold'] = min(0.8, accuracy + 0.05)

            # If user satisfaction is low, be more conservative
            elif user_satisfaction < 0.3:
                adjustments['confidence_threshold'] = min(0.85, accuracy + 0.05)
                adjustments['gesture_threshold'] = min(0.75, accuracy + 0.03)

            # Update calibration data
            self.calibration_data.threshold_adjustments.update(adjustments)

            # Record performance trend
            trend_data = {
                'timestamp': int(time.time() * 1000),
                'accuracy': accuracy,
                'false_positives': false_positives,
                'false_negatives': false_negatives,
                'user_satisfaction': user_satisfaction,
                'adjustments': adjustments
            }
            self.calibration_data.performance_trends.append(trend_data)

            # Keep only recent trends (last 100)
            if len(self.calibration_data.performance_trends) > 100:
                self.calibration_data.performance_trends = self.calibration_data.performance_trends[-100:]

            # Save updated data
            self._save_calibration_data()

            return {
                'success': True,
                'adjustments': adjustments,
                'current_accuracy': accuracy,
                'trend_recorded': True,
                'message': 'Recognition thresholds adapted successfully'
            }

        except Exception as e:
            logger.error(f"Error adapting recognition thresholds: {e}")
            return {
                'success': False,
                'error': f'Threshold adaptation failed: {str(e)}'
            }

    def learn_gesture_variations(self, gesture_data: Dict[str, Any], feedback: bool) -> Dict[str, Any]:
        """
        Learn from user feedback to improve recognition accuracy.

        Args:
            gesture_data: Raw gesture data from MediaPipe
            feedback: User feedback on recognition accuracy

        Returns:
            Learning results and model update status
        """
        try:
            # Create calibration sample from feedback
            sample = GestureCalibrationSample(
                gesture_type=gesture_data.get('gesture_type', 'unknown'),
                landmarks=gesture_data.get('landmarks', []),
                confidence=gesture_data.get('confidence', 0.0),
                timestamp=int(time.time() * 1000),
                user_feedback=feedback,
                hand_characteristics=gesture_data.get('hand_characteristics', {})
            )

            # Add to calibration samples
            self.calibration_samples.append(sample)

            # If we have enough samples, retrain
            positive_samples = [s for s in self.calibration_samples if s.user_feedback]
            if len(positive_samples) >= 20:  # Retrain every 20 positive samples
                training_result = self.learning_engine.train_personalized_model(self.calibration_samples)

                if training_result['success']:
                    # Clear old samples to prevent memory growth
                    self.calibration_samples = self.calibration_samples[-50:]  # Keep last 50

                    return {
                        'success': True,
                        'model_updated': True,
                        'new_accuracy': training_result.get('test_accuracy', 0.0),
                        'samples_used': len(positive_samples),
                        'message': 'Model retrained with new gesture variations'
                    }

            return {
                'success': True,
                'model_updated': False,
                'samples_collected': len(self.calibration_samples),
                'positive_samples': len(positive_samples),
                'message': 'Gesture variation learned, collecting more samples'
            }

        except Exception as e:
            logger.error(f"Error learning gesture variations: {e}")
            return {
                'success': False,
                'error': f'Learning failed: {str(e)}'
            }

    def get_personalized_confidence(self, gesture_data: Dict[str, Any]) -> float:
        """
        Calculate personalized confidence score based on user profile.

        Args:
            gesture_data: Current gesture data for evaluation

        Returns:
            Personalized confidence score (0.0-1.0)
        """
        try:
            # Extract gesture information
            gesture_type = gesture_data.get('gesture_type', 'unknown')
            base_confidence = gesture_data.get('confidence', 0.0)
            landmarks = gesture_data.get('landmarks', [])

            # Start with base confidence
            personalized_confidence = base_confidence

            # Apply user profile adjustments if available
            if self.user_profile and gesture_type in self.user_profile.gesture_preferences:
                preference_weight = self.user_profile.gesture_preferences[gesture_type]
                personalized_confidence *= preference_weight

            # Apply threshold adjustments
            threshold_adjustment = self.calibration_data.threshold_adjustments.get('confidence_threshold', 1.0)
            personalized_confidence *= threshold_adjustment

            # Use personalized model if available
            if self.learning_engine.is_trained and landmarks:
                ml_gesture, ml_confidence = self.learning_engine.predict_gesture(landmarks)
                if ml_gesture == gesture_type:
                    # Blend ML confidence with base confidence
                    personalized_confidence = (personalized_confidence * 0.6) + (ml_confidence * 0.4)

            # Ensure confidence is within bounds
            personalized_confidence = max(0.0, min(1.0, personalized_confidence))

            return personalized_confidence

        except Exception as e:
            logger.error(f"Error calculating personalized confidence: {e}")
            return gesture_data.get('confidence', 0.0)  # Fallback to base confidence

    def export_user_profile(self) -> Dict[str, Any]:
        """Export user gesture profile for backup or sharing."""
        try:
            profile_data = {}

            if self.user_profile:
                profile_data['user_profile'] = self.user_profile.to_dict()

            profile_data['calibration_data'] = self.calibration_data.to_dict()
            profile_data['calibration_samples'] = [sample.to_dict() for sample in self.calibration_samples]
            profile_data['export_timestamp'] = int(time.time() * 1000)

            return {
                'success': True,
                'profile_data': profile_data,
                'message': 'User profile exported successfully'
            }

        except Exception as e:
            logger.error(f"Error exporting user profile: {e}")
            return {
                'success': False,
                'error': f'Export failed: {str(e)}'
            }

    def import_user_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Import user gesture profile with validation."""
        try:
            # Validate profile data structure
            if 'profile_data' not in profile_data:
                return {
                    'success': False,
                    'error': 'Invalid profile data format'
                }

            data = profile_data['profile_data']

            # Import user profile if present
            if 'user_profile' in data:
                self.user_profile = UserGestureProfile.from_dict(data['user_profile'])

            # Import calibration data
            if 'calibration_data' in data:
                self.calibration_data = CalibrationDataManager.from_dict(data['calibration_data'])

            # Import calibration samples
            if 'calibration_samples' in data:
                self.calibration_samples = [
                    GestureCalibrationSample.from_dict(sample_data)
                    for sample_data in data['calibration_samples']
                ]

            # Retrain model if we have samples
            if self.calibration_samples:
                training_result = self.learning_engine.train_personalized_model(self.calibration_samples)
                model_trained = training_result.get('success', False)
            else:
                model_trained = False

            # Save imported data
            self._save_calibration_data()
            if self.user_profile:
                self._save_user_profile()

            return {
                'success': True,
                'model_trained': model_trained,
                'samples_imported': len(self.calibration_samples),
                'message': 'User profile imported successfully'
            }

        except Exception as e:
            logger.error(f"Error importing user profile: {e}")
            return {
                'success': False,
                'error': f'Import failed: {str(e)}'
            }

    def _save_calibration_data(self):
        """Save calibration data to disk."""
        try:
            calibration_path = self.data_dir / "gesture_calibration.json"
            with open(calibration_path, 'w') as f:
                json.dump(self.calibration_data.to_dict(), f, indent=2)
        except Exception as e:
            logger.error(f"Error saving calibration data: {e}")

    def _load_calibration_data(self):
        """Load calibration data from disk."""
        try:
            calibration_path = self.data_dir / "gesture_calibration.json"
            if calibration_path.exists():
                with open(calibration_path, 'r') as f:
                    data = json.load(f)
                    self.calibration_data = CalibrationDataManager.from_dict(data)
        except Exception as e:
            logger.error(f"Error loading calibration data: {e}")

    def _save_user_profile(self):
        """Save user profile to disk."""
        try:
            if self.user_profile:
                profile_path = self.data_dir / f"gesture_profile_{self.user_profile.user_id}.json"
                with open(profile_path, 'w') as f:
                    json.dump(self.user_profile.to_dict(), f, indent=2)
        except Exception as e:
            logger.error(f"Error saving user profile: {e}")

    def _load_user_profile(self, user_id: str):
        """Load user profile from disk."""
        try:
            profile_path = self.data_dir / f"gesture_profile_{user_id}.json"
            if profile_path.exists():
                with open(profile_path, 'r') as f:
                    data = json.load(f)
                    self.user_profile = UserGestureProfile.from_dict(data)
        except Exception as e:
            logger.error(f"Error loading user profile: {e}")


# Module-level functions for integration with existing senses system
def create_adaptive_gesture_recognition(data_dir: str = "data") -> Dict[str, Any]:
    """Create a new adaptive gesture recognition instance."""
    try:
        recognition = AdaptiveGestureRecognition(data_dir=data_dir)
        return {
            'success': True,
            'recognition': recognition,
            'tensorflow_available': TENSORFLOW_AVAILABLE,
            'message': 'Adaptive gesture recognition created successfully'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to create adaptive gesture recognition: {str(e)}'
        }
