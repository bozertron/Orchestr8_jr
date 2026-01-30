import json
import os
import time
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from .multimodal_fusion import SpellDefinition, SpellIntent


@dataclass
class SpellAnalytics:
    """Analytics data for spell performance tracking."""
    spell_id: str
    usage_count: int
    success_rate: float
    average_confidence: float
    last_used: int
    creation_date: int
    user_feedback_score: float = 0.0
    optimization_suggestions: List[str] = None

    def __post_init__(self):
        if self.optimization_suggestions is None:
            self.optimization_suggestions = []


@dataclass
class CustomSpellData:
    """Complete custom spell data including definition and analytics."""
    definition: SpellDefinition
    analytics: SpellAnalytics
    created_by: str = "user"
    version: str = "1.0"
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class SpellManager:
    """
    Manages custom spell creation, validation, persistence, and analytics.
    
    Provides comprehensive spell management capabilities including:
    - Custom spell creation and validation
    - Conflict detection and resolution
    - Import/export functionality for spell sharing
    - Performance analytics and optimization suggestions
    - Integration with Enhanced Director Intelligence
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.custom_spells_path = self.data_dir / "custom_spells.json"
        self.spell_analytics_path = self.data_dir / "spell_analytics.json"
        self.spell_templates_path = self.data_dir / "spell_templates.json"
        
        # In-memory storage
        self.custom_spells: Dict[str, CustomSpellData] = {}
        self.spell_analytics: Dict[str, SpellAnalytics] = {}
        self.spell_templates: Dict[str, Dict[str, Any]] = {}
        
        # Load existing data
        self._load_custom_spells()
        self._load_spell_analytics()
        self._load_spell_templates()
        
        # Validation settings
        self.validation_settings = {
            'max_spell_name_length': 50,
            'max_description_length': 200,
            'min_confidence_threshold': 0.1,
            'max_confidence_threshold': 1.0,
            'supported_gestures': ['open_palm', 'fist', 'point', 'peace', 'thumbs_up'],
            'supported_actions': ['zone_change', 'open_panel', 'new_session', 'save_session', 'custom_command'],
            'supported_panels': ['orchestr8', 'integr8', 'communic8', 'actu8', 'cre8', 'innov8']
        }

    def create_custom_spell(self, spell_definition: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create and validate a new custom spell.
        
        Args:
            spell_definition: Dictionary containing spell definition data
            
        Returns:
            Dictionary with success status and spell data or error information
        """
        try:
            # Validate spell definition
            validation_result = self.validate_spell(spell_definition)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'error': 'Validation failed',
                    'validation_errors': validation_result['errors']
                }
            
            # Create SpellDefinition object
            spell_def = SpellDefinition(
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
            
            # Create analytics object
            current_time = int(time.time() * 1000)
            analytics = SpellAnalytics(
                spell_id=spell_def.spell_id,
                usage_count=0,
                success_rate=0.0,
                average_confidence=0.0,
                last_used=0,
                creation_date=current_time
            )
            
            # Create custom spell data
            custom_spell = CustomSpellData(
                definition=spell_def,
                analytics=analytics,
                created_by=spell_definition.get('created_by', 'user'),
                version=spell_definition.get('version', '1.0'),
                tags=spell_definition.get('tags', [])
            )
            
            # Check for conflicts
            conflict_result = self._check_spell_conflicts(spell_def)
            if conflict_result['has_conflicts']:
                return {
                    'success': False,
                    'error': 'Spell conflicts detected',
                    'conflicts': conflict_result['conflicts'],
                    'suggestions': conflict_result['suggestions']
                }
            
            # Store the spell
            self.custom_spells[spell_def.spell_id] = custom_spell
            self.spell_analytics[spell_def.spell_id] = analytics
            
            # Persist to disk
            self._save_custom_spells()
            self._save_spell_analytics()
            
            return {
                'success': True,
                'spell_id': spell_def.spell_id,
                'spell_data': self._serialize_custom_spell(custom_spell),
                'message': f'Custom spell "{spell_def.name}" created successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to create custom spell: {str(e)}'
            }

    def validate_spell(self, spell_def: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate spell definition for correctness and feasibility.
        
        Args:
            spell_def: Dictionary containing spell definition
            
        Returns:
            Dictionary with validation results
        """
        errors = []
        warnings = []
        
        # Required fields validation
        required_fields = ['spell_id', 'name', 'description', 'required_gesture', 
                          'required_speech_pattern', 'target_action']
        
        for field in required_fields:
            if field not in spell_def or not spell_def[field]:
                errors.append(f'Missing required field: {field}')
        
        if errors:
            return {'valid': False, 'errors': errors, 'warnings': warnings}
        
        # Spell ID validation
        spell_id = spell_def['spell_id']
        if not isinstance(spell_id, str) or len(spell_id) < 3:
            errors.append('Spell ID must be a string with at least 3 characters')
        
        if spell_id in self.custom_spells:
            errors.append(f'Spell ID "{spell_id}" already exists')
        
        # Name validation
        name = spell_def['name']
        if not isinstance(name, str) or len(name) > self.validation_settings['max_spell_name_length']:
            errors.append(f'Spell name must be a string with max {self.validation_settings["max_spell_name_length"]} characters')
        
        # Description validation
        description = spell_def['description']
        if not isinstance(description, str) or len(description) > self.validation_settings['max_description_length']:
            errors.append(f'Description must be a string with max {self.validation_settings["max_description_length"]} characters')
        
        # Gesture validation
        gesture = spell_def['required_gesture']
        if gesture not in self.validation_settings['supported_gestures']:
            errors.append(f'Unsupported gesture: {gesture}. Supported: {self.validation_settings["supported_gestures"]}')
        
        # Speech pattern validation
        speech_pattern = spell_def['required_speech_pattern']
        if not isinstance(speech_pattern, str) or len(speech_pattern.strip()) < 3:
            errors.append('Speech pattern must be at least 3 characters long')
        
        # Action validation
        action = spell_def['target_action']
        if action not in self.validation_settings['supported_actions']:
            errors.append(f'Unsupported action: {action}. Supported: {self.validation_settings["supported_actions"]}')
        
        # Panel validation (if specified)
        if 'target_panel' in spell_def and spell_def['target_panel']:
            panel = spell_def['target_panel']
            if panel not in self.validation_settings['supported_panels']:
                warnings.append(f'Panel "{panel}" may not be available. Supported: {self.validation_settings["supported_panels"]}')
        
        # Confidence threshold validation
        if 'confidence_threshold' in spell_def:
            threshold = spell_def['confidence_threshold']
            min_threshold = self.validation_settings['min_confidence_threshold']
            max_threshold = self.validation_settings['max_confidence_threshold']
            
            if not isinstance(threshold, (int, float)) or threshold < min_threshold or threshold > max_threshold:
                errors.append(f'Confidence threshold must be between {min_threshold} and {max_threshold}')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def get_spell_suggestions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get intelligent spell creation suggestions based on context.

        Args:
            context: Current workspace context and user behavior data

        Returns:
            List of suggested spell definitions
        """
        suggestions = []

        # Analyze current workspace state
        current_panel = context.get('current_panel', 'orchestr8')
        recent_actions = context.get('recent_actions', [])
        user_patterns = context.get('user_patterns', {})

        # Common workflow suggestions
        if current_panel == 'integr8' and 'file_operations' in user_patterns:
            suggestions.append({
                'spell_id': 'quick_save_file',
                'name': 'Quick Save File',
                'description': 'Quickly save current file in editor',
                'required_gesture': 'thumbs_up',
                'required_speech_pattern': 'save file',
                'target_action': 'custom_command',
                'target_panel': 'integr8',
                'confidence_threshold': 0.7,
                'suggestion_reason': 'Based on frequent file operations in code editor'
            })

        # Panel navigation suggestions
        if len(recent_actions) > 0:
            most_common_action = max(set(recent_actions), key=recent_actions.count)
            if most_common_action == 'panel_switch':
                suggestions.append({
                    'spell_id': 'quick_panel_switch',
                    'name': 'Quick Panel Switch',
                    'description': 'Switch between panels quickly',
                    'required_gesture': 'point',
                    'required_speech_pattern': 'switch panel',
                    'target_action': 'zone_change',
                    'target_panel': None,
                    'confidence_threshold': 0.6,
                    'suggestion_reason': 'Based on frequent panel switching behavior'
                })

        # Time-based suggestions
        current_hour = time.localtime().tm_hour
        if 9 <= current_hour <= 17:  # Work hours
            suggestions.append({
                'spell_id': 'focus_mode',
                'name': 'Focus Mode',
                'description': 'Enter focused work mode',
                'required_gesture': 'fist',
                'required_speech_pattern': 'focus mode',
                'target_action': 'custom_command',
                'target_panel': None,
                'confidence_threshold': 0.8,
                'suggestion_reason': 'Productivity suggestion for work hours'
            })

        return suggestions

    def export_spells(self, spell_ids: List[str]) -> Dict[str, Any]:
        """
        Export spells for sharing with other users.

        Args:
            spell_ids: List of spell IDs to export

        Returns:
            Dictionary containing exported spell data
        """
        try:
            exported_spells = {}
            export_metadata = {
                'export_date': int(time.time() * 1000),
                'export_version': '1.0',
                'total_spells': 0
            }

            for spell_id in spell_ids:
                if spell_id in self.custom_spells:
                    custom_spell = self.custom_spells[spell_id]
                    exported_spells[spell_id] = self._serialize_custom_spell(custom_spell)
                    export_metadata['total_spells'] += 1

            if export_metadata['total_spells'] == 0:
                return {
                    'success': False,
                    'error': 'No valid spells found to export'
                }

            export_data = {
                'metadata': export_metadata,
                'spells': exported_spells
            }

            return {
                'success': True,
                'export_data': export_data,
                'message': f'Successfully exported {export_metadata["total_spells"]} spells'
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to export spells: {str(e)}'
            }

    def import_spells(self, spell_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Import shared spells with conflict resolution.

        Args:
            spell_data: Dictionary containing exported spell data

        Returns:
            Dictionary with import results and conflict information
        """
        try:
            if 'spells' not in spell_data:
                return {
                    'success': False,
                    'error': 'Invalid spell data format'
                }

            imported_spells = []
            conflicts = []
            errors = []

            for spell_id, spell_info in spell_data['spells'].items():
                try:
                    # Check for existing spell
                    if spell_id in self.custom_spells:
                        conflicts.append({
                            'spell_id': spell_id,
                            'existing_spell': self._serialize_custom_spell(self.custom_spells[spell_id]),
                            'imported_spell': spell_info,
                            'resolution_options': ['skip', 'overwrite', 'rename']
                        })
                        continue

                    # Validate imported spell
                    spell_definition = spell_info['definition']
                    validation_result = self.validate_spell(spell_definition)

                    if not validation_result['valid']:
                        errors.append({
                            'spell_id': spell_id,
                            'error': 'Validation failed',
                            'details': validation_result['errors']
                        })
                        continue

                    # Create spell objects
                    spell_def = SpellDefinition(**spell_definition)

                    # Import analytics if available
                    if 'analytics' in spell_info:
                        analytics_data = spell_info['analytics']
                        analytics = SpellAnalytics(**analytics_data)
                    else:
                        current_time = int(time.time() * 1000)
                        analytics = SpellAnalytics(
                            spell_id=spell_id,
                            usage_count=0,
                            success_rate=0.0,
                            average_confidence=0.0,
                            last_used=0,
                            creation_date=current_time
                        )

                    # Create custom spell data
                    custom_spell = CustomSpellData(
                        definition=spell_def,
                        analytics=analytics,
                        created_by=spell_info.get('created_by', 'imported'),
                        version=spell_info.get('version', '1.0'),
                        tags=spell_info.get('tags', [])
                    )

                    # Store the spell
                    self.custom_spells[spell_id] = custom_spell
                    self.spell_analytics[spell_id] = analytics
                    imported_spells.append(spell_id)

                except Exception as e:
                    errors.append({
                        'spell_id': spell_id,
                        'error': f'Import failed: {str(e)}'
                    })

            # Save if any spells were imported
            if imported_spells:
                self._save_custom_spells()
                self._save_spell_analytics()

            return {
                'success': True,
                'imported_spells': imported_spells,
                'conflicts': conflicts,
                'errors': errors,
                'message': f'Successfully imported {len(imported_spells)} spells'
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to import spells: {str(e)}'
            }

    def get_custom_spells(self) -> Dict[str, Any]:
        """Get all custom spells with their analytics."""
        return {
            'spells': {spell_id: self._serialize_custom_spell(spell_data)
                      for spell_id, spell_data in self.custom_spells.items()},
            'total_count': len(self.custom_spells)
        }

    def update_spell_analytics(self, spell_id: str, usage_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update spell analytics based on usage data."""
        if spell_id not in self.spell_analytics:
            return {'success': False, 'error': 'Spell not found'}

        analytics = self.spell_analytics[spell_id]

        # Update usage count
        analytics.usage_count += 1
        analytics.last_used = int(time.time() * 1000)

        # Update confidence tracking
        if 'confidence' in usage_data:
            confidence = usage_data['confidence']
            if analytics.usage_count == 1:
                analytics.average_confidence = confidence
            else:
                # Running average
                analytics.average_confidence = (
                    (analytics.average_confidence * (analytics.usage_count - 1) + confidence) /
                    analytics.usage_count
                )

        # Update success rate
        if 'success' in usage_data:
            success = usage_data['success']
            if analytics.usage_count == 1:
                analytics.success_rate = 1.0 if success else 0.0
            else:
                # Running average
                current_successes = analytics.success_rate * (analytics.usage_count - 1)
                if success:
                    current_successes += 1
                analytics.success_rate = current_successes / analytics.usage_count

        # Generate optimization suggestions
        analytics.optimization_suggestions = self._generate_optimization_suggestions(analytics)

        self._save_spell_analytics()

        return {'success': True, 'analytics': asdict(analytics)}

    def _check_spell_conflicts(self, spell_def: SpellDefinition) -> Dict[str, Any]:
        """Check for conflicts with existing spells."""
        conflicts = []
        suggestions = []

        # Check gesture-speech pattern conflicts
        for existing_id, existing_spell in self.custom_spells.items():
            existing_def = existing_spell.definition

            # Exact match conflict
            if (existing_def.required_gesture == spell_def.required_gesture and
                existing_def.required_speech_pattern.lower() == spell_def.required_speech_pattern.lower()):
                conflicts.append({
                    'type': 'exact_match',
                    'conflicting_spell_id': existing_id,
                    'conflicting_spell_name': existing_def.name,
                    'description': 'Identical gesture and speech pattern'
                })

            # Similar speech pattern conflict (fuzzy matching)
            elif (existing_def.required_gesture == spell_def.required_gesture and
                  self._calculate_speech_similarity(existing_def.required_speech_pattern,
                                                  spell_def.required_speech_pattern) > 0.8):
                conflicts.append({
                    'type': 'similar_pattern',
                    'conflicting_spell_id': existing_id,
                    'conflicting_spell_name': existing_def.name,
                    'description': 'Very similar gesture and speech pattern'
                })

                suggestions.append(f'Consider using a different gesture or more distinct speech pattern')

        return {
            'has_conflicts': len(conflicts) > 0,
            'conflicts': conflicts,
            'suggestions': suggestions
        }

    def _calculate_speech_similarity(self, pattern1: str, pattern2: str) -> float:
        """Calculate similarity between two speech patterns."""
        words1 = set(pattern1.lower().split())
        words2 = set(pattern2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0.0

    def _generate_optimization_suggestions(self, analytics: SpellAnalytics) -> List[str]:
        """Generate optimization suggestions based on analytics."""
        suggestions = []

        if analytics.usage_count > 10:
            if analytics.success_rate < 0.7:
                suggestions.append('Consider adjusting confidence threshold - low success rate detected')

            if analytics.average_confidence < 0.6:
                suggestions.append('Speech pattern may be too complex - consider simplifying')

            if analytics.usage_count > 50 and analytics.success_rate > 0.9:
                suggestions.append('High-performing spell - consider creating similar variations')

        return suggestions

    def _serialize_custom_spell(self, custom_spell: CustomSpellData) -> Dict[str, Any]:
        """Serialize custom spell data for storage/export."""
        return {
            'definition': asdict(custom_spell.definition),
            'analytics': asdict(custom_spell.analytics),
            'created_by': custom_spell.created_by,
            'version': custom_spell.version,
            'tags': custom_spell.tags
        }

    def _load_custom_spells(self):
        """Load custom spells from disk."""
        if self.custom_spells_path.exists():
            try:
                with open(self.custom_spells_path, 'r') as f:
                    data = json.load(f)

                for spell_id, spell_data in data.items():
                    spell_def = SpellDefinition(**spell_data['definition'])
                    analytics = SpellAnalytics(**spell_data['analytics'])

                    custom_spell = CustomSpellData(
                        definition=spell_def,
                        analytics=analytics,
                        created_by=spell_data.get('created_by', 'user'),
                        version=spell_data.get('version', '1.0'),
                        tags=spell_data.get('tags', [])
                    )

                    self.custom_spells[spell_id] = custom_spell

            except Exception as e:
                print(f"Error loading custom spells: {e}")

    def _save_custom_spells(self):
        """Save custom spells to disk."""
        try:
            data = {spell_id: self._serialize_custom_spell(spell_data)
                   for spell_id, spell_data in self.custom_spells.items()}

            with open(self.custom_spells_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving custom spells: {e}")

    def _load_spell_analytics(self):
        """Load spell analytics from disk."""
        if self.spell_analytics_path.exists():
            try:
                with open(self.spell_analytics_path, 'r') as f:
                    data = json.load(f)

                for spell_id, analytics_data in data.items():
                    self.spell_analytics[spell_id] = SpellAnalytics(**analytics_data)

            except Exception as e:
                print(f"Error loading spell analytics: {e}")

    def _save_spell_analytics(self):
        """Save spell analytics to disk."""
        try:
            data = {spell_id: asdict(analytics)
                   for spell_id, analytics in self.spell_analytics.items()}

            with open(self.spell_analytics_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving spell analytics: {e}")

    def _load_spell_templates(self):
        """Load spell templates from disk."""
        if self.spell_templates_path.exists():
            try:
                with open(self.spell_templates_path, 'r') as f:
                    self.spell_templates = json.load(f)
            except Exception as e:
                print(f"Error loading spell templates: {e}")
        else:
            # Initialize with default templates
            self.spell_templates = {
                'navigation': {
                    'name': 'Navigation Template',
                    'description': 'Template for panel navigation spells',
                    'required_gesture': 'point',
                    'target_action': 'zone_change',
                    'confidence_threshold': 0.7
                },
                'action': {
                    'name': 'Action Template',
                    'description': 'Template for action-based spells',
                    'required_gesture': 'fist',
                    'target_action': 'custom_command',
                    'confidence_threshold': 0.8
                }
            }
            self._save_spell_templates()

    def _save_spell_templates(self):
        """Save spell templates to disk."""
        try:
            with open(self.spell_templates_path, 'w') as f:
                json.dump(self.spell_templates, f, indent=2)
        except Exception as e:
            print(f"Error saving spell templates: {e}")


# Module-level functions for integration with existing senses system
def create_spell_manager(data_dir: str = "data") -> Dict[str, Any]:
    """Create a new spell manager instance."""
    try:
        manager = SpellManager(data_dir=data_dir)
        return {
            'success': True,
            'manager': manager,
            'message': 'Spell manager created successfully'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to create spell manager: {str(e)}'
        }
