import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import time

@dataclass
class GestureData:
    gesture_type: str  # "open_palm", "fist", "point", "peace", "thumbs_up"
    confidence: float
    hand_landmarks: List[Dict[str, float]]
    timestamp: int
    bounding_box: Dict[str, float]

class GestureRecognitionEngine:
    """
    Advanced gesture recognition using MediaPipe for real-time hand tracking.
    
    Integrates with Enhanced Director Intelligence for context-aware gesture interpretation.
    """
    
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Gesture recognition thresholds
        self.gesture_thresholds = {
            'open_palm_confidence': 0.8,
            'fist_confidence': 0.8,
            'point_confidence': 0.7,
            'gesture_hold_duration': 1000,  # ms
        }
        
        # Gesture state tracking
        self.current_gesture: Optional[GestureData] = None
        self.gesture_start_time: Optional[int] = None
        self.gesture_history: List[GestureData] = []
    
    def process_frame(self, frame: np.ndarray) -> Optional[GestureData]:
        """
        Process a single video frame for gesture recognition.
        
        Args:
            frame: OpenCV image frame
            
        Returns:
            GestureData if gesture detected, None otherwise
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extract landmark coordinates
                landmarks = self._extract_landmarks(hand_landmarks)
                
                # Recognize gesture
                gesture_type, confidence = self._recognize_gesture(landmarks)
                
                if confidence > self.gesture_thresholds.get(f'{gesture_type}_confidence', 0.7):
                    gesture_data = GestureData(
                        gesture_type=gesture_type,
                        confidence=confidence,
                        hand_landmarks=landmarks,
                        timestamp=int(time.time() * 1000),
                        bounding_box=self._calculate_bounding_box(landmarks)
                    )
                    
                    # Update gesture state
                    self._update_gesture_state(gesture_data)
                    
                    return gesture_data
        
        # No gesture detected
        self._reset_gesture_state()
        return None
    
    def _extract_landmarks(self, hand_landmarks) -> List[Dict[str, float]]:
        """Extract normalized landmark coordinates."""
        landmarks = []
        for landmark in hand_landmarks.landmark:
            landmarks.append({
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z
            })
        return landmarks
    
    def _recognize_gesture(self, landmarks: List[Dict[str, float]]) -> tuple[str, float]:
        """
        Recognize gesture type from hand landmarks.
        
        Returns:
            Tuple of (gesture_type, confidence)
        """
        # Get key landmark positions
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Get MCP (base) positions for comparison
        index_mcp = landmarks[5]
        middle_mcp = landmarks[9]
        ring_mcp = landmarks[13]
        pinky_mcp = landmarks[17]
        
        # Open Palm Detection
        if (self._is_finger_extended(index_tip, index_mcp) and
            self._is_finger_extended(middle_tip, middle_mcp) and
            self._is_finger_extended(ring_tip, ring_mcp) and
            self._is_finger_extended(pinky_tip, pinky_mcp)):
            return "open_palm", 0.9
        
        # Fist Detection
        if (not self._is_finger_extended(index_tip, index_mcp) and
            not self._is_finger_extended(middle_tip, middle_mcp) and
            not self._is_finger_extended(ring_tip, ring_mcp) and
            not self._is_finger_extended(pinky_tip, pinky_mcp)):
            return "fist", 0.9
        
        # Point Detection (index finger extended, others closed)
        if (self._is_finger_extended(index_tip, index_mcp) and
            not self._is_finger_extended(middle_tip, middle_mcp) and
            not self._is_finger_extended(ring_tip, ring_mcp) and
            not self._is_finger_extended(pinky_tip, pinky_mcp)):
            return "point", 0.8
        
        # Peace Sign Detection (index and middle extended)
        if (self._is_finger_extended(index_tip, index_mcp) and
            self._is_finger_extended(middle_tip, middle_mcp) and
            not self._is_finger_extended(ring_tip, ring_mcp) and
            not self._is_finger_extended(pinky_tip, pinky_mcp)):
            return "peace", 0.8
        
        # Thumbs Up Detection
        if (thumb_tip['y'] < landmarks[3]['y'] and  # Thumb extended upward
            not self._is_finger_extended(index_tip, index_mcp) and
            not self._is_finger_extended(middle_tip, middle_mcp)):
            return "thumbs_up", 0.7
        
        return "unknown", 0.0
    
    def _is_finger_extended(self, tip: Dict[str, float], mcp: Dict[str, float]) -> bool:
        """Check if finger is extended based on tip vs MCP position."""
        return tip['y'] < mcp['y']  # Tip is above MCP (extended)
    
    def _calculate_bounding_box(self, landmarks: List[Dict[str, float]]) -> Dict[str, float]:
        """Calculate bounding box for hand landmarks."""
        x_coords = [lm['x'] for lm in landmarks]
        y_coords = [lm['y'] for lm in landmarks]
        
        return {
            'x_min': min(x_coords),
            'x_max': max(x_coords),
            'y_min': min(y_coords),
            'y_max': max(y_coords)
        }

    def _update_gesture_state(self, gesture_data: GestureData) -> None:
        """Update current gesture state and history."""
        current_time = int(time.time() * 1000)

        if (self.current_gesture is None or
            self.current_gesture.gesture_type != gesture_data.gesture_type):
            # New gesture detected
            self.current_gesture = gesture_data
            self.gesture_start_time = current_time
        else:
            # Same gesture continuing
            self.current_gesture = gesture_data

        # Add to history
        self.gesture_history.append(gesture_data)

        # Keep only recent history (last 100 gestures)
        if len(self.gesture_history) > 100:
            self.gesture_history = self.gesture_history[-100:]

    def _reset_gesture_state(self) -> None:
        """Reset gesture state when no gesture detected."""
        self.current_gesture = None
        self.gesture_start_time = None

    def get_stable_gesture(self) -> Optional[GestureData]:
        """
        Get current gesture if it has been stable for minimum duration.

        Returns:
            GestureData if gesture is stable, None otherwise
        """
        if (self.current_gesture and self.gesture_start_time):
            current_time = int(time.time() * 1000)
            hold_duration = current_time - self.gesture_start_time

            if hold_duration >= self.gesture_thresholds['gesture_hold_duration']:
                return self.current_gesture

        return None

    def get_gesture_analytics(self) -> Dict[str, Any]:
        """Get analytics about gesture recognition performance."""
        if not self.gesture_history:
            return {
                'total_gestures': 0,
                'gesture_types': {},
                'average_confidence': 0.0,
                'recognition_rate': 0.0
            }

        gesture_types = {}
        total_confidence = 0.0

        for gesture in self.gesture_history:
            gesture_types[gesture.gesture_type] = gesture_types.get(gesture.gesture_type, 0) + 1
            total_confidence += gesture.confidence

        return {
            'total_gestures': len(self.gesture_history),
            'gesture_types': gesture_types,
            'average_confidence': total_confidence / len(self.gesture_history),
            'recognition_rate': len([g for g in self.gesture_history if g.confidence > 0.7]) / len(self.gesture_history)
        }

def get_version() -> str:
    """Get gesture recognition engine version."""
    return "1.0.0"

def health_check() -> Dict[str, Any]:
    """Perform health check of gesture recognition system."""
    try:
        # Test MediaPipe initialization
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()
        hands.close()

        return {
            'success': True,
            'status': 'healthy',
            'mediapipe_available': True,
            'opencv_available': True,
            'checked_at': int(time.time() * 1000)
        }
    except Exception as e:
        return {
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'checked_at': int(time.time() * 1000)
        }

def create_gesture_session(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create a new gesture recognition session."""
    try:
        engine = GestureRecognitionEngine()

        # Apply configuration if provided
        if config:
            if 'gesture_thresholds' in config:
                engine.gesture_thresholds.update(config['gesture_thresholds'])

        session_id = f"gesture_session_{int(time.time() * 1000)}"

        return {
            'success': True,
            'session_id': session_id,
            'engine': engine,  # In practice, this would be stored in a session manager
            'config': engine.gesture_thresholds,
            'created_at': int(time.time() * 1000)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'created_at': int(time.time() * 1000)
        }

def process_gesture_frame(session_id: str, frame_data: bytes) -> Dict[str, Any]:
    """Process a video frame for gesture recognition."""
    try:
        # Convert frame data to OpenCV format
        nparr = np.frombuffer(frame_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Get session engine (in practice, from session manager)
        engine = GestureRecognitionEngine()  # Placeholder

        # Process frame
        gesture_data = engine.process_frame(frame)

        if gesture_data:
            return {
                'success': True,
                'gesture_detected': True,
                'gesture_type': gesture_data.gesture_type,
                'confidence': gesture_data.confidence,
                'timestamp': gesture_data.timestamp,
                'bounding_box': gesture_data.bounding_box
            }
        else:
            return {
                'success': True,
                'gesture_detected': False,
                'timestamp': int(time.time() * 1000)
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': int(time.time() * 1000)
        }
