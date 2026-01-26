import time
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from .gesture_recognition import GestureData
from .speech_recognition import SpeechData

@dataclass
class SpellIntent:
    spell_id: str
    gesture_component: str
    speech_component: str
    confidence: float
    timestamp: int
    parameters: Dict[str, Any]
    target_action: str
    target_panel: Optional[str] = None

@dataclass
class SpellDefinition:
    spell_id: str
    name: str
    description: str
    required_gesture: str
    required_speech_pattern: str
    target_action: str
    target_panel: Optional[str]
    confidence_threshold: float
    enabled: bool = True

class MultimodalFusionEngine:
    """
    Fuses gesture and speech inputs into actionable spell intents.

    Integrates with Enhanced Director Intelligence for intelligent spell interpretation
    and context-aware command execution.
    """

    def __init__(self, spell_manager=None):
        # Spell definitions
        self.spell_definitions: Dict[str, SpellDefinition] = {}
        self._initialize_default_spells()

        # Spell manager for custom spells
        self.spell_manager = spell_manager
        self.custom_spells_enabled = True

        # Load custom spells if manager is available
        if self.spell_manager:
            self.load_custom_spells()

        # Fusion settings
        self.fusion_settings = {
            'gesture_speech_sync_window': 2000,  # ms
            'min_spell_confidence': 0.7,
            'gesture_weight': 0.4,
            'speech_weight': 0.6,
            'context_boost': 0.1,
            'custom_spell_priority': 0.1,  # Boost for custom spells
        }

        # State tracking
        self.recent_gestures: List[GestureData] = []
        self.recent_speech: List[SpeechData] = []
        self.recognized_spells: List[SpellIntent] = []

        # Spell priority system
        self.spell_priorities: Dict[str, float] = {}
        self._initialize_spell_priorities()

        # Performance metrics
        self.fusion_metrics = {
            'total_attempts': 0,
            'successful_fusions': 0,
            'spell_recognitions': 0,
            'false_positives': 0,
            'custom_spell_usage': 0,
            'default_spell_usage': 0,
        }

        # User adaptation data
        self.user_patterns: Dict[str, Any] = {
            'gesture_preferences': {},
            'speech_patterns': {},
            'spell_usage_frequency': {},
            'context_associations': {}
        }

    def _initialize_default_spells(self):
        """Initialize default spell definitions."""
        # Demo spell: OpenPalm + "Take me to the Library"
        self.spell_definitions["library_navigation"] = SpellDefinition(
            spell_id="library_navigation",
            name="Library Navigation",
            description="Navigate to the Library zone",
            required_gesture="open_palm",
            required_speech_pattern="take me to the library",
            target_action="zone_change",
            target_panel="orchestr8",
            confidence_threshold=0.7
        )

        # Additional demo spells
        self.spell_definitions["code_editor"] = SpellDefinition(
            spell_id="code_editor",
            name="Code Editor",
            description="Open code editor",
            required_gesture="point",
            required_speech_pattern="open code editor",
            target_action="open_panel",
            target_panel="integr8",
            confidence_threshold=0.7
        )

        self.spell_definitions["new_conversation"] = SpellDefinition(
            spell_id="new_conversation",
            name="New Conversation",
            description="Start new AI conversation",
            required_gesture="fist",
            required_speech_pattern="new conversation",
            target_action="new_session",
            target_panel="orchestr8",
            confidence_threshold=0.7
        )

        self.spell_definitions["save_workspace"] = SpellDefinition(
            spell_id="save_workspace",
            name="Save Workspace",
            description="Save current workspace state",
            required_gesture="thumbs_up",
            required_speech_pattern="save workspace",
            target_action="save_session",
            target_panel=None,  # Global action
            confidence_threshold=0.8
        )

    def process_multimodal_input(self, gesture_data: Optional[GestureData],
                                speech_data: Optional[SpeechData]) -> Optional[SpellIntent]:
        """
        Process gesture and speech inputs to recognize spell intents.

        Args:
            gesture_data: Current gesture data
            speech_data: Current speech data

        Returns:
            SpellIntent if recognized, None otherwise
        """
        self.fusion_metrics['total_attempts'] += 1

        # Update recent inputs
        if gesture_data:
            self.recent_gestures.append(gesture_data)
            # Keep only recent gestures (last 10 seconds)
            cutoff_time = int(time.time() * 1000) - 10000
            self.recent_gestures = [g for g in self.recent_gestures if g.timestamp > cutoff_time]

        if speech_data:
            self.recent_speech.append(speech_data)
            # Keep only recent speech (last 10 seconds)
            cutoff_time = int(time.time() * 1000) - 10000
            self.recent_speech = [s for s in self.recent_speech if s.timestamp > cutoff_time]

        # Attempt spell recognition
        spell_intent = self._recognize_spell_intent()

        if spell_intent:
            self.fusion_metrics['successful_fusions'] += 1
            self.fusion_metrics['spell_recognitions'] += 1
            self.recognized_spells.append(spell_intent)

            # Keep only recent spells
            if len(self.recognized_spells) > 100:
                self.recognized_spells = self.recognized_spells[-100:]

        return spell_intent

    def _recognize_spell_intent(self) -> Optional[SpellIntent]:
        """Recognize spell intent from recent gesture and speech inputs."""
        current_time = int(time.time() * 1000)
        sync_window = self.fusion_settings['gesture_speech_sync_window']

        # Find synchronized gesture-speech pairs
        for gesture in self.recent_gestures:
            for speech in self.recent_speech:
                # Check if gesture and speech are within sync window
                time_diff = abs(gesture.timestamp - speech.timestamp)
                if time_diff <= sync_window:
                    # Try to match against spell definitions
                    spell_intent = self._match_spell_definition(gesture, speech)
                    if spell_intent:
                        return spell_intent

        return None

    def _match_spell_definition(self, gesture: GestureData, speech: SpeechData) -> Optional[SpellIntent]:
        """Match gesture-speech pair against spell definitions."""
        for spell_def in self.spell_definitions.values():
            if not spell_def.enabled:
                continue

            # Check gesture match
            gesture_match = self._match_gesture(gesture, spell_def.required_gesture)

            # Check speech match
            speech_match = self._match_speech(speech, spell_def.required_speech_pattern)

            if gesture_match and speech_match:
                # Calculate combined confidence
                gesture_weight = self.fusion_settings['gesture_weight']
                speech_weight = self.fusion_settings['speech_weight']

                combined_confidence = (
                    gesture.confidence * gesture_weight +
                    speech.confidence * speech_weight
                )

                # Apply context boost if applicable
                context_boost = self._calculate_context_boost(spell_def)
                combined_confidence += context_boost
                combined_confidence = min(1.0, combined_confidence)

                if combined_confidence >= spell_def.confidence_threshold:
                    return SpellIntent(
                        spell_id=spell_def.spell_id,
                        gesture_component=gesture.gesture_type,
                        speech_component=speech.transcription,
                        confidence=combined_confidence,
                        timestamp=max(gesture.timestamp, speech.timestamp),
                        parameters=self._extract_spell_parameters(spell_def, gesture, speech),
                        target_action=spell_def.target_action,
                        target_panel=spell_def.target_panel
                    )

        return None

    def _match_gesture(self, gesture: GestureData, required_gesture: str) -> bool:
        """Check if gesture matches required gesture type."""
        return gesture.gesture_type.lower() == required_gesture.lower()

    def _match_speech(self, speech: SpeechData, required_pattern: str) -> bool:
        """Check if speech matches required pattern."""
        # Simple substring matching (could be enhanced with NLP)
        speech_text = speech.transcription.lower().strip()
        pattern = required_pattern.lower().strip()

        # Exact match
        if speech_text == pattern:
            return True

        # Fuzzy matching - check if all pattern words are in speech
        pattern_words = pattern.split()
        speech_words = speech_text.split()

        matches = 0
        for pattern_word in pattern_words:
            for speech_word in speech_words:
                if pattern_word in speech_word or speech_word in pattern_word:
                    matches += 1
                    break

        # Require at least 80% of pattern words to match
        return matches >= len(pattern_words) * 0.8

    def _calculate_context_boost(self, spell_def: SpellDefinition) -> float:
        """Calculate context-based confidence boost."""
        # This would integrate with Enhanced Director Intelligence
        # to provide context-aware boosting based on current workspace state

        # Placeholder implementation
        context_boost = self.fusion_settings['context_boost']

        # Example: boost library navigation if user is currently in orchestr8
        if spell_def.spell_id == "library_navigation":
            # Would check current panel from Enhanced Director
            return context_boost

        return 0.0

    def _extract_spell_parameters(self, spell_def: SpellDefinition,
                                gesture: GestureData, speech: SpeechData) -> Dict[str, Any]:
        """Extract parameters from gesture and speech for spell execution."""
        parameters = {
            'gesture_confidence': gesture.confidence,
            'speech_confidence': speech.confidence,
            'gesture_timestamp': gesture.timestamp,
            'speech_timestamp': speech.timestamp,
            'speech_text': speech.transcription,
            'gesture_type': gesture.gesture_type
        }

        # Extract specific parameters based on spell type
        if spell_def.target_action == "zone_change":
            parameters['zone'] = spell_def.target_panel
        elif spell_def.target_action == "open_panel":
            parameters['panel_type'] = spell_def.target_panel

        return parameters

    def add_spell_definition(self, spell_def: SpellDefinition) -> Dict[str, Any]:
        """Add a new spell definition."""
        try:
            self.spell_definitions[spell_def.spell_id] = spell_def
            return {
                'success': True,
                'spell_id': spell_def.spell_id,
                'message': 'Spell definition added successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def remove_spell_definition(self, spell_id: str) -> Dict[str, Any]:
        """Remove a spell definition."""
        if spell_id in self.spell_definitions:
            del self.spell_definitions[spell_id]
            return {
                'success': True,
                'message': f'Spell {spell_id} removed successfully'
            }
        else:
            return {
                'success': False,
                'error': f'Spell {spell_id} not found'
            }

    def get_spell_definitions(self) -> Dict[str, Any]:
        """Get all spell definitions."""
        spells = {}
        for spell_id, spell_def in self.spell_definitions.items():
            spells[spell_id] = {
                'spell_id': spell_def.spell_id,
                'name': spell_def.name,
                'description': spell_def.description,
                'required_gesture': spell_def.required_gesture,
                'required_speech_pattern': spell_def.required_speech_pattern,
                'target_action': spell_def.target_action,
                'target_panel': spell_def.target_panel,
                'confidence_threshold': spell_def.confidence_threshold,
                'enabled': spell_def.enabled
            }

        return {
            'success': True,
            'spells': spells,
            'total_spells': len(spells)
        }

    def get_fusion_analytics(self) -> Dict[str, Any]:
        """Get analytics about multimodal fusion performance."""
        success_rate = 0.0
        if self.fusion_metrics['total_attempts'] > 0:
            success_rate = self.fusion_metrics['successful_fusions'] / self.fusion_metrics['total_attempts']

        return {
            'success': True,
            'metrics': self.fusion_metrics,
            'success_rate': success_rate,
            'recent_gestures': len(self.recent_gestures),
            'recent_speech': len(self.recent_speech),
            'recognized_spells': len(self.recognized_spells)
        }

def get_version() -> str:
    """Get multimodal fusion engine version."""
    return "1.0.0"

def health_check() -> Dict[str, Any]:
    """Perform health check of multimodal fusion system."""
    try:
        engine = MultimodalFusionEngine()

        return {
            'success': True,
            'status': 'healthy',
            'spell_definitions': len(engine.spell_definitions),
            'fusion_engine_ready': True,
            'checked_at': int(time.time() * 1000)
        }
    except Exception as e:
        return {
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'checked_at': int(time.time() * 1000)
        }

    def load_custom_spells(self) -> Dict[str, Any]:
        """Load user-created custom spells from spell manager."""
        if not self.spell_manager:
            return {'success': False, 'error': 'No spell manager available'}

        try:
            custom_spells_data = self.spell_manager.get_custom_spells()
            loaded_count = 0

            for spell_id, spell_data in custom_spells_data['spells'].items():
                spell_definition = spell_data['definition']

                # Create SpellDefinition object
                custom_spell = SpellDefinition(
                    spell_id=spell_definition['spell_id'],
                    name=spell_definition['name'],
                    description=spell_definition['description'],
                    required_gesture=spell_definition['required_gesture'],
                    required_speech_pattern=spell_definition['required_speech_pattern'],
                    target_action=spell_definition['target_action'],
                    target_panel=spell_definition.get('target_panel'),
                    confidence_threshold=spell_definition.get('confidence_threshold', 0.7),
                    enabled=spell_definition.get('enabled', True)
                )

                # Add to spell definitions with custom priority
                self.spell_definitions[spell_id] = custom_spell
                self.spell_priorities[spell_id] = 1.0 + self.fusion_settings['custom_spell_priority']
                loaded_count += 1

            return {
                'success': True,
                'loaded_count': loaded_count,
                'message': f'Loaded {loaded_count} custom spells'
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to load custom spells: {str(e)}'
            }

    def resolve_spell_conflicts(self, spells: List[SpellDefinition]) -> List[SpellDefinition]:
        """Resolve conflicts between default and custom spells using priority system."""
        # Group spells by gesture-speech pattern combination
        pattern_groups: Dict[str, List[SpellDefinition]] = {}

        for spell in spells:
            pattern_key = f"{spell.required_gesture}:{spell.required_speech_pattern.lower()}"
            if pattern_key not in pattern_groups:
                pattern_groups[pattern_key] = []
            pattern_groups[pattern_key].append(spell)

        resolved_spells = []

        for pattern_key, conflicting_spells in pattern_groups.items():
            if len(conflicting_spells) == 1:
                # No conflict
                resolved_spells.append(conflicting_spells[0])
            else:
                # Resolve conflict using priority system
                best_spell = max(conflicting_spells,
                               key=lambda s: self.spell_priorities.get(s.spell_id, 0.5))
                resolved_spells.append(best_spell)

                # Log conflict resolution
                print(f"Spell conflict resolved for pattern '{pattern_key}': "
                      f"Selected '{best_spell.name}' over {len(conflicting_spells)-1} alternatives")

        return resolved_spells

    def adapt_spell_thresholds(self, user_performance: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt spell recognition thresholds based on user performance."""
        adaptations = {}

        for spell_id, performance_data in user_performance.items():
            if spell_id not in self.spell_definitions:
                continue

            spell_def = self.spell_definitions[spell_id]
            current_threshold = spell_def.confidence_threshold

            success_rate = performance_data.get('success_rate', 0.5)
            false_positive_rate = performance_data.get('false_positive_rate', 0.1)
            usage_count = performance_data.get('usage_count', 0)

            # Only adapt if we have sufficient data
            if usage_count < 5:
                continue

            # Calculate new threshold
            new_threshold = current_threshold

            if success_rate < 0.6:
                # Lower threshold to improve recognition
                new_threshold = max(0.1, current_threshold - 0.1)
                adaptations[spell_id] = {
                    'old_threshold': current_threshold,
                    'new_threshold': new_threshold,
                    'reason': 'Low success rate - lowering threshold'
                }
            elif false_positive_rate > 0.3:
                # Raise threshold to reduce false positives
                new_threshold = min(0.9, current_threshold + 0.1)
                adaptations[spell_id] = {
                    'old_threshold': current_threshold,
                    'new_threshold': new_threshold,
                    'reason': 'High false positive rate - raising threshold'
                }
            elif success_rate > 0.9 and false_positive_rate < 0.05:
                # Optimal performance - slight threshold optimization
                new_threshold = current_threshold * 0.95  # Slight reduction for better UX
                adaptations[spell_id] = {
                    'old_threshold': current_threshold,
                    'new_threshold': new_threshold,
                    'reason': 'Optimal performance - fine-tuning threshold'
                }

            # Apply the adaptation
            spell_def.confidence_threshold = new_threshold

        return {
            'success': True,
            'adaptations': adaptations,
            'adapted_count': len(adaptations)
        }

    def learn_user_patterns(self, spell_intent: SpellIntent, context: Dict[str, Any]) -> Dict[str, Any]:
        """Learn from user spell usage patterns for future optimization."""
        spell_id = spell_intent.spell_id

        # Update gesture preferences
        gesture = spell_intent.gesture_component
        if gesture not in self.user_patterns['gesture_preferences']:
            self.user_patterns['gesture_preferences'][gesture] = 0
        self.user_patterns['gesture_preferences'][gesture] += 1

        # Update speech patterns
        speech = spell_intent.speech_component.lower()
        if speech not in self.user_patterns['speech_patterns']:
            self.user_patterns['speech_patterns'][speech] = 0
        self.user_patterns['speech_patterns'][speech] += 1

        # Update spell usage frequency
        if spell_id not in self.user_patterns['spell_usage_frequency']:
            self.user_patterns['spell_usage_frequency'][spell_id] = 0
        self.user_patterns['spell_usage_frequency'][spell_id] += 1

        # Update context associations
        current_panel = context.get('current_panel', 'unknown')
        context_key = f"{spell_id}:{current_panel}"
        if context_key not in self.user_patterns['context_associations']:
            self.user_patterns['context_associations'][context_key] = 0
        self.user_patterns['context_associations'][context_key] += 1

        # Update spell manager analytics if available
        if self.spell_manager:
            usage_data = {
                'confidence': spell_intent.confidence,
                'success': True,  # Assume success if spell was executed
                'context': context
            }
            self.spell_manager.update_spell_analytics(spell_id, usage_data)

        return {
            'success': True,
            'patterns_updated': ['gesture_preferences', 'speech_patterns',
                               'spell_usage_frequency', 'context_associations']
        }

    def _initialize_spell_priorities(self):
        """Initialize priority values for default spells."""
        # Default spells have base priority of 0.5
        for spell_id in self.spell_definitions.keys():
            self.spell_priorities[spell_id] = 0.5

        # Demo spell gets slightly higher priority
        if 'library_navigation' in self.spell_priorities:
            self.spell_priorities['library_navigation'] = 0.6

def create_fusion_session(config: Optional[Dict[str, Any]] = None, spell_manager=None) -> Dict[str, Any]:
    """Create a new multimodal fusion session with optional spell manager."""
    try:
        engine = MultimodalFusionEngine(spell_manager=spell_manager)

        # Apply configuration if provided
        if config:
            if 'fusion_settings' in config:
                engine.fusion_settings.update(config['fusion_settings'])
            if 'custom_spells' in config:
                for spell_data in config['custom_spells']:
                    spell_def = SpellDefinition(**spell_data)
                    engine.add_spell_definition(spell_def)

        session_id = f"fusion_session_{int(time.time() * 1000)}"

        return {
            'success': True,
            'session_id': session_id,
            'engine': engine,  # In practice, stored in session manager
            'spell_count': len(engine.spell_definitions),
            'created_at': int(time.time() * 1000)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'created_at': int(time.time() * 1000)
        }
