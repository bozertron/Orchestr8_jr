# spell_manager.py Integration Guide

- Source: `one integration at a time/888/senses/spell_manager.py`
- Total lines: `696`
- SHA256: `c37e3b7729f56acdd70c51cc4a1a38c9b550b7e91e5cddb136ad851a18c072b1`
- Memory chunks: `6`
- Observation IDs: `336..341`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/888/senses/spell_manager.py:79` 'supported_panels': ['orchestr8', 'integr8', 'communic8', 'actu8', 'cre8', 'innov8']
- `one integration at a time/888/senses/spell_manager.py:193` errors.append('Spell ID must be a string with at least 3 characters')
- `one integration at a time/888/senses/spell_manager.py:201` errors.append(f'Spell name must be a string with max {self.validation_settings["max_spell_name_length"]} characters')
- `one integration at a time/888/senses/spell_manager.py:206` errors.append(f'Description must be a string with max {self.validation_settings["max_description_length"]} characters')
- `one integration at a time/888/senses/spell_manager.py:216` errors.append('Speech pattern must be at least 3 characters long')
- `one integration at a time/888/senses/spell_manager.py:236` errors.append(f'Confidence threshold must be between {min_threshold} and {max_threshold}')
- `one integration at a time/888/senses/spell_manager.py:257` current_panel = context.get('current_panel', 'orchestr8')

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
