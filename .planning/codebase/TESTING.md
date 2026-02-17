# Testing Patterns

**Analysis Date:** 2026-01-30

## Test Framework

**Runner:**
- `unittest` - Primary test framework for core modules
- `pytest` - Secondary framework for integration tests
- No explicit test configuration files (pytest.ini, setup.cfg) detected

**Location:** `one integration at a time/888/*/tests/test_*.py`

**Key Test Files:**
- `one integration at a time/888/director/tests/test_adapter.py`
- `one integration at a time/888/director/tests/test_ooda_engine.py`
- `one integration at a time/888/director/tests/test_user_context.py`
- `one integration at a time/888/panel_foundation/tests/test_panel_registry.py`
- `IP/test_styles.py` - Marimo notebook style component testing

**Run Commands:**
```bash
python -m unittest discover -s one integration at a time/888 -p "test_*.py"
python -m pytest one integration at a time/888/*/tests/
```

## Test File Organization

**Location:**
- Integration tests in `one integration at a time/888/[module]/tests/test_[component].py`
- UI/style tests in `IP/test_styles.py` (Marimo notebook format)
- Tests are separate from source, not co-located

**Naming:**
- Test files: `test_*.py` prefix pattern
- Test classes: `Test[ComponentName]` PascalCase (e.g., `TestDirectorAdapter`)
- Test methods: `test_[functionality]` snake_case (e.g., `test_adapter_initialization()`)

**Directory Structure:**
```
one integration at a time/888/
├── director/
│   ├── tests/
│   │   ├── test_adapter.py
│   │   ├── test_ooda_engine.py
│   │   └── test_user_context.py
│   └── [source files]
├── panel_foundation/
│   ├── tests/
│   │   └── test_panel_registry.py
│   └── [source files]
└── [other modules]
```

## Test Structure

**Suite Organization - unittest Pattern:**
```python
# From test_adapter.py
class TestDirectorAdapter(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        adapter.reset_context()

    def test_adapter_initialization(self):
        """Test adapter initialization and health check."""
        health = adapter.health_check()
        self.assertIsInstance(health, dict)
        self.assertTrue(health['success'])
```

**Suite Organization - pytest Pattern:**
```python
# From test_panel_registry.py (uses pytest)
class MockPanel(BasePanel):
    """Mock panel implementation for testing."""
    def __init__(self, panel_name: str, capabilities: PanelCapabilities):
        super().__init__(panel_name, capabilities)
        self.initialized = False
```

**Patterns:**
- Setup: Use `setUp()` method in unittest classes to reset/initialize state
- Teardown: Not heavily used; cleanup happens via setUp reset
- Assertions: Use `self.assert*` methods (assertTrue, assertEqual, assertIsInstance, assertIn)

## Mocking

**Framework:** No explicit mocking library imports detected (no unittest.mock usage)

**Patterns:**
- Manual mock objects created as test helper classes (e.g., `MockPanel` in `test_panel_registry.py`)
- Mock objects implement required interface methods
- Direct state manipulation for testing (example from `test_adapter.py` line 106):
```python
# Manually adjust timing for testing
context = adapter._get_context()
context.last_suggestion_time = context.last_suggestion_time - 31000
context.idle_duration = 150000
```

**What to Mock:**
- External adapters and integrations (PyO3 bindings, subprocess calls)
- Panel implementations for registry testing
- State objects that need controlled initialization

**What NOT to Mock:**
- Core business logic in OODA engine
- Context state transitions
- Validation functions
- Analytics generation functions

## Fixtures and Factories

**Test Data - Fixed Fixtures:**
```python
# From test_adapter.py
telemetry_events = [
    {
        'event_type': {
            'type': 'UIInteraction',
            'data': {
                'component': 'send_button',
                'action': 'clicked',
                'target': None,
                'app_context': 'orchestr8'
            }
        }
    },
    # ... more events
]
```

**Test Data - Multiple Scenarios:**
Tests use multiple hardcoded telemetry event structures for different test cases:
- UIInteraction events (test_adapter.py lines 36-45)
- ZoneChange events (test_adapter.py lines 49-57)
- IdleTime events (test_adapter.py lines 88-97)
- FileAccess events (test_adapter.py lines 212-220)

**Location:**
- Inline test data defined in test methods
- No separate fixtures directory or shared test data files
- Helper factory methods used in some cases (e.g., `MockPanel()` constructor)

## Coverage

**Requirements:** No explicit coverage requirements enforced

**View Coverage:**
```bash
# Manual coverage tracking not found in config files
# Would use: python -m coverage run -m unittest
# Then: python -m coverage report
```

## Test Types

**Unit Tests:**
- Scope: Individual adapter/component methods
- Approach: Direct method calls with assertions
- Example: `test_adapter_initialization()` in test_adapter.py
- Typical assertions: Type checks, state values, dictionary contents

**Integration Tests:**
- Scope: Component interactions through adapters
- Approach: Call adapter methods in sequence, verify state persistence
- Example: `test_multiple_context_updates()` in test_adapter.py lines 293-335
- Verification: Check that state persists across multiple function calls

**E2E Tests:**
- Framework: Not used
- Style/UI testing: `IP/test_styles.py` is a Marimo notebook-based visual test

## Common Patterns

**Async Testing:**
Not used in detected test files. All test code is synchronous.

**Error Testing:**
```python
# From test_adapter.py - Testing error conditions
def test_error_handling(self):
    """Test error handling in adapter functions."""
    invalid_events = [
        {'invalid_structure': 'this should cause an error'}
    ]
    result = adapter.update_context(invalid_events)

    # Adapter should handle gracefully
    self.assertIsInstance(result, dict)
```

**State Verification Testing:**
```python
# From test_adapter.py - Verifying state after operations
def test_record_feedback(self):
    """Test recording user feedback for suggestions."""
    suggestion_id = "test-suggestion-123"
    rating = 1

    result = adapter.record_feedback(suggestion_id, rating)

    self.assertIsInstance(result, dict)
    self.assertTrue(result['success'])
    self.assertEqual(result['suggestion_id'], suggestion_id)

    # Verify in context
    context = adapter._get_context()
    self.assertEqual(context.user_feedback[suggestion_id], rating)
```

**Conditional Assertions:**
Tests use conditional logic for behavior that may or may not occur:
```python
# From test_adapter.py lines 346-354
if result['has_suggestion']:
    context_after = adapter._get_context()
    self.assertGreater(len(context_after.suggestion_history), 0)

    last_suggestion = context_after.suggestion_history[-1]
    self.assertEqual(last_suggestion['id'], result['suggestion']['id'])
```

## Test Coverage Gaps

**Untested Areas:**

**1. Marimo Plugin System:**
- Plugin rendering: Not tested (plugins designed for interactive UI)
- Plugin loader dynamic import: Not tested
- STATE_MANAGERS injection: Not tested
- File path: `orchestr8.py` (lines 78-156) - plugin_loader function

**2. File I/O Operations:**
- Directory scanning: Not tested
- File reading/preview: Not tested
- Permission handling: Partially tested, only error paths
- File path: `IP/plugins/02_explorer.py` (lines 65-108)

**3. UI Component Rendering:**
- Marimo component composition: Not tested
- Style injection: Only tested visually via `IP/test_styles.py`
- Component state updates: Not tested
- File path: `IP/test_styles.py`

**4. Carl Context Integration:**
- TypeScript subprocess execution: Not tested
- Output file parsing: Not tested
- Timeout behavior: Not tested
- File path: `IP/carl_core.py` (lines 40-91)

**5. Louis File Protection:**
- Permission bit changes: Not tested
- Git hook installation: Not tested
- Lock/unlock logic: Not tested
- File path: `IP/louis_core.py` (not examined in detail)

**Risk Assessment:**
- **High Risk:** Plugin loader - uses dynamic import, could fail silently
- **High Risk:** File I/O - permission errors, path issues could break explorer
- **Medium Risk:** UI components - style changes could break appearance without detection
- **Low Risk:** Director adapter - well-tested with multiple scenarios

## Test Execution

**Example - Running Director Tests:**
```bash
cd one integration at a time/888/director
python -m unittest tests.test_adapter.TestDirectorAdapter
python -m unittest tests.test_adapter.TestDirectorAdapter.test_adapter_initialization
```

**Example - Running All Tests:**
```bash
cd one integration at a time/888
python -m unittest discover -p "test_*.py" -v
```

## Mocking Advanced Patterns

**State Context Manipulation:**
```python
# From test_adapter.py - Direct context access for setup
context = adapter._get_context()
context.last_suggestion_time = context.last_suggestion_time - 31000
context.idle_duration = 150000
```

**Reset Pattern:**
Tests reset adapter state between test methods:
```python
def setUp(self):
    """Set up test fixtures."""
    adapter.reset_context()
```

This ensures test isolation without using complex mocking frameworks.

---

*Testing analysis: 2026-01-30*
