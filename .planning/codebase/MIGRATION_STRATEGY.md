# Migration Strategy Research for Orchestr8 Architecture

**Research Date:** 2026-02-16  
**Focus:** Architecture Migration Patterns and Rollback Strategies  
**Agent:** R-4 (Research Agent)

---

## Executive Summary

This research examines migration strategies applicable to Orchestr8's architecture transition from its current marimo-based implementation to a more modular structure. The analysis covers feature flag patterns, proxy-based backward compatibility, rollback mechanisms, and case studies from similar projects. Recommendations are provided for implementing gradual migrations without breaking existing functionality.

---

## 1. Feature Flag Patterns for Gradual Migration

### 1.1 Environment Variable-Based Feature Flags

**Current State in Orchestr8:**

The project already employs environment variables for configuration management. The following patterns are currently in use:

```python
# Example from IP/plugins/06_maestro.py
max_payload_raw = os.getenv("ORCHESTR8_CODE_CITY_MAX_BYTES", "9000000").strip()

# Example from IP/features/code_city/render.py
stream_bps_raw = os.getenv("ORCHESTR8_CODE_CITY_STREAM_BPS", "5000000").strip()
inline_building_data = os.getenv("ORCHESTR8_CODE_CITY_INLINE_BUILDING_DATA", "").strip()
```

**Pattern Recommendation for Migration:**

Implement feature flags using a consistent namespace convention:

```python
# Migration feature flag pattern
def is_feature_enabled(feature_name: str, default: bool = False) -> bool:
    """Check if a migration feature is enabled."""
    flag_name = f"ORCHESTR8_MIGRATE_{feature_name.upper()}"
    value = os.getenv(flag_name, str(default)).strip().lower()
    return value in {"1", "true", "yes", "enabled"}
```

**Key Implementation Locations:**

| Feature Flag Area | Current Config | Recommended Migration Flag |
|-------------------|----------------|---------------------------|
| Code City Rendering | `ORCHESTR8_CODE_CITY_MAX_BYTES` | `ORCHESTR8_MIGRATE_CODE_CITY_V2` |
| Panel System | N/A | `ORCHESTR8_MIGRATE_NEW_PANELS` |
| Connection Verifier | `ORCHESTR8_PATCHBAY_APPLY` | `ORCHESTR8_MIGRATE_PATCHBAY_V2` |
| Health System | N/A | `ORCHESTR8_MIGRATE_HEALTH_V2` |

### 1.2 Configuration File-Based Feature Flags

**Marimo Configuration Support:**

Marimo supports configuration through multiple layers with clear precedence:

```
Script metadata (PEP 723) > pyproject.toml > User config (.marimo.toml)
```

**Implementation for Orchestr8:**

```toml
# pyproject.toml
[tool.orchestr8.migration]
# Enable gradual migration features
enable_new_panel_system = false
enable_connection_v2 = false
enable_health_v2 = false

[tool.orchestr8.migration.code_city]
# Code City migration stages
stage = "legacy"  # legacy, hybrid, v2
fallback_on_error = true
```

```python
# Migration config loader
from dataclasses import dataclass
from pathlib import Path
import toml

@dataclass
class MigrationConfig:
    enable_new_panel_system: bool = False
    enable_connection_v2: bool = False
    enable_health_v2: bool = False
    code_city_stage: str = "legacy"
    fallback_on_error: bool = True

def load_migration_config() -> MigrationConfig:
    """Load migration configuration from pyproject.toml."""
    config_path = Path("pyproject.toml")
    if config_path.exists():
        config = toml.load(config_path)
        migration = config.get("tool", {}).get("orchestr8", {}).get("migration", {})
        return MigrationConfig(
            enable_new_panel_system=migration.get("enable_new_panel_system", False),
            enable_connection_v2=migration.get("enable_connection_v2", False),
            enable_health_v2=migration.get("enable_health_v2", False),
            code_city_stage=migration.get("code_city", {}).get("stage", "legacy"),
            fallback_on_error=migration.get("code_city", {}).get("fallback_on_error", True),
        )
    return MigrationConfig()
```

### 1.3 Gradual Rollout Pattern

**Stage-Based Migration:**

```python
class MigrationStage:
    """Represents a stage in the migration rollout."""
    
    STAGE_LEGACY = "legacy"      # Original implementation
    STAGE_HYBRID = "hybrid"       # Both systems running, feature-flagged
    STAGE_V2 = "v2"              # New implementation primary
    STAGE_COMPLETE = "complete"  # Legacy removed

def get_migration_stage(feature: str) -> str:
    """Get current migration stage for a feature."""
    config = load_migration_config()
    stage_map = {
        "code_city": config.code_city_stage,
        "panels": "legacy" if not config.enable_new_panel_system else "v2",
        "connection": "legacy" if not config.enable_connection_v2 else "v2",
        "health": "legacy" if not config.enable_health_v2 else "v2",
    }
    return stage_map.get(feature, MigrationStage.STAGE_LEGACY)
```

---

## 2. Proxy Pattern for Backward Compatibility

### 2.1 Proxy Architecture Overview

The proxy pattern allows intercepting and redirecting calls between old and new implementations without breaking existing consumers.

**Current Implementation in Orchestr8:**

```python
# orchestr8.py - Uses dynamic import as a form of proxy
spec = importlib.util.spec_from_file_location("maestro_direct", plugin_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
result = module.render(STATE_MANAGERS)
```

### 2.2 Migration Proxy Pattern

**Implementation for Subsystem Migration:**

```python
# IP/migration/proxies.py

from typing import TypeVar, Generic, Callable, Any
from functools import wraps
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')

class MigrationProxy(Generic[T]):
    """
    Proxy that routes calls between legacy and new implementations
    based on migration configuration.
    """
    
    def __init__(
        self,
        legacy_impl: Callable[..., T],
        new_impl: Callable[..., T],
        feature_name: str,
        fallback: Callable[..., T] = None
    ):
        self.legacy_impl = legacy_impl
        self.new_impl = new_impl
        self.feature_name = feature_name
        self.fallback = fallback or legacy_impl
        
    def __call__(self, *args, **kwargs) -> T:
        """Route to appropriate implementation based on migration stage."""
        from IP.migration.config import get_migration_stage, MigrationStage
        
        stage = get_migration_stage(self.feature_name)
        
        try:
            if stage == MigrationStage.STAGE_LEGACY:
                logger.debug(f"[{self.feature_name}] Using legacy implementation")
                return self.legacy_impl(*args, **kwargs)
            
            elif stage == MigrationStage.STAGE_HYBRID:
                # Try new implementation first, fallback on error
                try:
                    logger.debug(f"[{self.feature_name}] Trying new implementation (hybrid)")
                    return self.new_impl(*args, **kwargs)
                except Exception as e:
                    logger.warning(
                        f"[{self.feature_name}] New implementation failed, "
                        f"falling back to legacy: {e}"
                    )
                    return self.legacy_impl(*args, **kwargs)
            
            elif stage == MigrationStage.STAGE_V2:
                logger.debug(f"[{self.feature_name}] Using new implementation")
                return self.new_impl(*args, **kwargs)
            
            else:
                return self.fallback(*args, **kwargs)
                
        except Exception as e:
            logger.error(
                f"[{self.feature_name}] All implementations failed: {e}"
            )
            raise

def create_proxy(
    feature_name: str,
    legacy_impl: Callable[..., T],
    new_impl: Callable[..., T]
) -> MigrationProxy[T]:
    """Factory function to create a migration proxy."""
    return MigrationProxy(legacy_impl, new_impl, feature_name)
```

### 2.3 Example: Panel System Migration Proxy

```python
# IP/migration/panel_proxy.py

from IP.panels.legacy.deploy_panel import render_deploy_panel as legacy_deploy
from IP.panels.v2.deploy_panel import render_deploy_panel as new_deploy

# Create proxy with automatic fallback
deploy_panel_proxy = create_proxy(
    feature_name="panels",
    legacy_impl=legacy_deploy,
    new_impl=new_deploy
)

# Usage in 06_maestro.py or shell.py
def render_deploy_panel(building_data, state):
    return deploy_panel_proxy(building_data, state)
```

### 2.4 Adapter Pattern for Interface Differences

When legacy and new implementations have different interfaces:

```python
class PanelAdapter:
    """Adapter to normalize legacy panel interface to new interface."""
    
    def __init__(self, legacy_panel):
        self.legacy_panel = legacy_panel
        
    def to_v2_format(self, legacy_data: dict) -> dict:
        """Convert legacy data format to v2 format."""
        return {
            "node_id": legacy_data.get("file_path"),
            "building_type": legacy_data.get("type", "file"),
            "status": legacy_data.get("health_status", "unknown"),
            "metadata": legacy_data.get("context", {}),
        }
        
    def from_v2_format(self, v2_data: dict) -> dict:
        """Convert v2 data format to legacy format for backward compat."""
        return {
            "file_path": v2_data.get("node_id"),
            "type": v2_data.get("building_type", "file"),
            "health_status": v2_data.get("status", "unknown"),
            "context": v2_data.get("metadata", {}),
        }
```

---

## 3. Rollback Strategies for Large Migrations

### 3.1 Automatic Rollback Mechanisms

**Environment-Based Rollback:**

```python
# IP/migration/rollback.py

import os
import logging
from enum import Enum
from typing import Optional, Callable, Any
from functools import wraps

logger = logging.getLogger(__name__)

class RollbackStrategy(Enum):
    """Strategies for automatic rollback."""
    IMMEDIATE = "immediate"      # Rollback on first error
    RETRY = "retry"              # Retry N times before rollback
    GRACEFUL = "graceful"        # Log error but continue with legacy

class RollbackConfig:
    """Configuration for rollback behavior."""
    
    def __init__(self, feature: str):
        self.feature = feature
        self.strategy = RollbackStrategy(
            os.getenv(f"ORCHESTR8_ROLLBACK_{feature.upper()}", "immediate")
        )
        self.max_retries = int(
            os.getenv(f"ORCHESTR8_RETRY_{feature.upper()}", "3")
        )
        self.fallback_timeout = int(
            os.getenv(f"ORCHESTR8_TIMEOUT_{feature.upper()}", "5000")
        )

def with_rollback(
    feature: str,
    legacy_func: Callable[..., Any],
    migration_stage_check: Callable[[], bool]
) -> Callable[..., Any]:
    """
    Decorator that provides automatic rollback capability.
    
    Usage:
        @with_rollback("code_city", legacy_render_code_city, is_v2_enabled)
        def render_code_city(building_data):
            return render_code_city_v2(building_data)
    """
    config = RollbackConfig(feature)
    
    @wraps(legacy_func)
    def wrapper(*args, **kwargs):
        # Check if we should use legacy directly
        if not migration_stage_check():
            logger.info(f"[{feature}] Using legacy implementation (migration disabled)")
            return legacy_func(*args, **kwargs)
            
        if config.strategy == RollbackStrategy.IMMEDIATE:
            return _immediate_rollback(
                feature, legacy_func, args, kwargs, config
            )
        elif config.strategy == RollbackStrategy.RETRY:
            return _retry_with_rollback(
                feature, legacy_func, args, kwargs, config
            )
        else:
            return _graceful_rollback(
                feature, legacy_func, args, kwargs, config
            )
    
    return wrapper

def _immediate_rollback(feature, legacy_func, args, kwargs, config):
    """Rollback immediately on any error."""
    try:
        from IP.migration.new_impls import get_v2_implementation
        v2_func = get_v2_implementation(feature)
        return v2_func(*args, **kwargs)
    except Exception as e:
        logger.error(f"[{feature}] V2 failed, rolling back: {e}")
        return legacy_func(*args, **kwargs)

def _retry_with_rollback(feature, legacy_func, args, kwargs, config):
    """Retry V2 implementation N times before rolling back."""
    last_error = None
    for attempt in range(config.max_retries):
        try:
            from IP.migration.new_impls import get_v2_implementation
            v2_func = get_v2_implementation(feature)
            return v2_func(*args, **kwargs)
        except Exception as e:
            last_error = e
            logger.warning(
                f"[{feature}] Attempt {attempt + 1}/{config.max_retries} failed: {e}"
            )
    
    logger.error(
        f"[{feature}] All {config.max_retries} attempts failed, rolling back"
    )
    return legacy_func(*args, **kwargs)

def _graceful_rollback(feature, legacy_func, args, kwargs, config):
    """Log error but continue with legacy, don't raise."""
    try:
        from IP.migration.new_impls import get_v2_implementation
        v2_func = get_v2_implementation(feature)
        return v2_func(*args, **kwargs)
    except Exception as e:
        logger.error(f"[{feature}] V2 error (continuing with legacy): {e}")
        return legacy_func(*args, **kwargs)
```

### 3.2 Manual Rollback Procedures

**Configuration-Based Rollback:**

```bash
# Quick rollback commands
export ORCHESTR8_MIGRATE_CODE_CITY_V2=0          # Disable Code City v2
export ORCHESTR8_MIGRATE_NEW_PANELS=0           # Disable new panels
export ORCHESTR8_ROLLBACK_CODE_CITY=immediate   # Enable immediate rollback
```

**UI-Based Rollback Control:**

```python
# IP/plugins/07_settings.py - Migration controls

def render_migration_controls():
    """Render UI controls for migration management."""
    import marimo as mo
    
    current_stage = load_migration_config()
    
    return mo.vstack([
        mo.md("## Migration Controls"),
        mo.ui.dropdown(
            label="Code City Version",
            options=["legacy", "hybrid", "v2"],
            value=current_stage.code_city_stage,
            on_change=lambda v: update_migration_stage("code_city", v)
        ),
        mo.ui.switch(
            label="Enable Automatic Rollback",
            value=True,
            on_change=lambda v: set_rollback_enabled(v)
        ),
        mo.ui.button(
            label="Rollback All",
            on_click=rollback_all_migrations
        ),
    ])
```

### 3.3 State Preservation for Rollback

```python
# IP/migration/state_manager.py

import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional

class MigrationStateManager:
    """Manages migration state for rollback capability."""
    
    STATE_FILE = ".orchestr8/migration_state.json"
    
    def __init__(self):
        self.state_file = Path(self.STATE_FILE)
        self.state = self._load_state()
        
    def _load_state(self) -> Dict[str, Any]:
        """Load migration state from disk."""
        if self.state_file.exists():
            with open(self.state_file) as f:
                return json.load(f)
        return {"migrations": {}, "last_rollback": None}
    
    def save_state(self):
        """Persist migration state to disk."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def record_migration(self, feature: str, stage: str, version: str):
        """Record a migration event."""
        self.state["migrations"][feature] = {
            "stage": stage,
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "can_rollback": True,
        }
        self.save_state()
    
    def record_rollback(self, feature: str, reason: str = ""):
        """Record a rollback event."""
        self.state["last_rollback"] = {
            "feature": feature,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        }
        if feature in self.state["migrations"]:
            self.state["migrations"][feature]["stage"] = "legacy"
            self.state["migrations"][feature]["can_rollback"] = False
        self.save_state()
    
    def can_rollback(self, feature: str) -> bool:
        """Check if a feature can be rolled back."""
        return self.state.get("migrations", {}).get(feature, {}).get(
            "can_rollback", False
        )
```

---

## 4. How Other Projects Have Done Similar Migrations

### 4.1 Marimo's Own Migration Patterns

**Migration from Jupyter:**

Marimo provides clear migration paths from Jupyter notebooks. Key patterns observed:

1. **Incremental Adoption:** Users can run marimo alongside Jupyter
2. **Compatibility Mode:** `marimo convert` provides automatic conversion
3. **Gradual Cell Migration:** Notebooks can mix marimo and traditional Python

**Configuration Precedence:**

```toml
# marimo's layered configuration (reference pattern)
[tool.marimo.runtime]
auto_instantiate = false    # Legacy: default behavior
on_cell_change = "lazy"    # Migration: lazy by default
pythonpath = ["src/"]       # New: explicit path management
```

### 4.2 Django's Migration Framework

**Applicable Patterns:**

1. **Migration Files:** Sequential numbered migrations
2. **Dependencies:** Explicit migration dependencies
3. **Rollback:** `manage.py migrate <previous>` for rollback
4. **Fake Migrations:** Mark migrations as applied without running

**Orchestr8 Adaptation:**

```python
# Example: Migration file structure for Orchestr8
migrations/
├── 001_initial_code_city/
│   ├── 001_migration.py       # Initial Code City setup
│   ├── 002_add_health.py      # Health integration
│   └── dependencies.json     # {"001": [], "002": ["001"]}
├── 002_panels_v2/
│   ├── 001_create_panels.py
│   └── 002_proxy_setup.py
└── migration_manager.py
```

### 4.3 React's Feature Flag Migration

**Patterns Used:**

1. **React's Concurrent Mode:** Flag-gated new rendering engine
2. **Gradual Adoption:** `useEffect` cleanup timing changes
3. **Warning System:** Deprecation warnings before breaking changes

**Key Insight:** React provides escape hatches and compatibility layers.

```javascript
// React pattern: escape hatch
// If new behavior causes issues, can opt-out
<React.unstable_ConcurrentMode>
  <App />
</React.unstable_ConcurrentMode>
```

**Orchestr8 Adaptation:**

```python
# Escape hatch pattern for migration
def render_with_escape_hatch(app_type, config):
    """Allow opting out of new behavior if needed."""
    if os.getenv("ORCHESTR8_DISABLE_MIGRATION"):
        return render_legacy(app_type)
    
    try:
        return render_new(app_type, config)
    except Exception as e:
        logger.warning(f"New render failed: {e}, using legacy")
        return render_legacy(app_type)
```

### 4.4 Stripe's API Versioning

**Pattern: Header-Based API Versioning:**

Stripe uses date-based API versions with backward compatibility:

```
Stripe-Version: 2024-12-18.acacia
```

**Orchestr8 Adaptation:**

```python
# Header-based feature versioning
class FeatureVersion:
    """Version header for migration features."""
    
    HEADER = "X-Orchestr8-Version"
    DEFAULT = "2026-01-26"
    
    @classmethod
    def get_current(cls) -> str:
        return os.getenv(cls.HEADER, cls.DEFAULT)
    
    @classmethod
    def is_compatible(cls, required: str) -> bool:
        """Check if current version is compatible with required."""
        current = cls.get_current()
        return current >= required
```

---

## 5. Recommendations for Orchestr8

### 5.1 Immediate Actions (Phase 1: Foundation)

**Implement Migration Configuration System:**

1. Create `IP/migration/` directory with:
   - `config.py` - Configuration loader
   - `proxies.py` - Proxy pattern implementations
   - `rollback.py` - Rollback mechanisms
   - `state_manager.py` - State persistence

2. Add migration configuration to `pyproject_orchestr8_settings.toml`:

```toml
[migration]
# Global migration controls
enabled = true
default_stage = "legacy"
auto_rollback = true

[migration.code_city]
stage = "legacy"
fallback_on_error = true

[migration.panels]
stage = "legacy"
fallback_on_error = true
```

3. Create migration state file:

```bash
mkdir -p .orchestr8
touch .orchestr8/migration_state.json
```

### 5.2 Short-Term Actions (Phase 2: Proxy Implementation)

**Implement Proxy for Key Subsystems:**

1. **Code City Proxy:**
   ```python
   # IP/migration/code_city_proxy.py
   from IP.features.code_city.graph_builder import (
       build_graph as legacy_build_graph
   )
   from IP.features.code_city.v2.graph_builder import (
       build_graph as v2_build_graph
   )
   
   build_graph_proxy = create_proxy("code_city", legacy_build_graph, v2_build_graph)
   ```

2. **Panel System Proxy:**
   ```python
   # IP/migration/panel_proxy.py
   from IP.plugins.components.deploy_panel import render as legacy_deploy
   from IP.plugins.components.v2.deploy_panel import render as v2_deploy
   
   deploy_panel_proxy = create_proxy("panels", legacy_deploy, v2_deploy)
   ```

### 5.3 Medium-Term Actions (Phase 3: Testing Infrastructure)

**Implement Test Gates for Migration:**

```python
# tests/migration/test_migration_rollback.py

def test_code_city_proxy_fallback():
    """Verify proxy falls back to legacy on V2 failure."""
    # Set migration stage to hybrid
    os.environ["ORCHESTR8_MIGRATE_CODE_CITY_V2"] = "1"
    
    # Patch V2 to fail
    with patch("IP.features.code_city.v2.graph_builder.build_graph") as mock:
        mock.side_effect = Exception("Simulated V2 failure")
        
        result = build_graph_proxy(root_path)
        
        # Should have called legacy
        assert legacy_build_graph.called
        assert result is not None

def test_rollback_state_persistence():
    """Verify rollback state is saved."""
    manager = MigrationStateManager()
    manager.record_rollback("code_city", "Test rollback")
    
    assert manager.can_rollback("code_city") == False
```

### 5.4 Testing Strategy for Each Migration Step

**Recommended Test Hierarchy:**

| Test Type | Purpose | When to Run |
|-----------|---------|-------------|
| Unit Tests | Test proxy routing logic | Every commit |
| Integration Tests | Test legacy → V2 flow | Every PR |
| Rollback Tests | Verify rollback works | Before each stage promotion |
| Smoke Tests | Quick sanity check | Before deployment |
| Full Regression | Complete feature test | Before release |

**Example Test Commands:**

```bash
# Run migration-specific tests
pytest tests/migration/ -v

# Run with specific rollback strategy
ORCHESTR8_ROLLBACK_CODE_CITY=retry pytest tests/migration/ -v

# Run smoke test before deployment
pytest tests/migration/test_smoke.py -v --tb=short

# Full regression with rollback
ORCHESTR8_MIGRATE_CODE_CITY_V2=1 pytest tests/reliability/ -v
```

### 5.5 Rollback Quick Reference

**Quick Rollback Commands:**

```bash
# Emergency rollback all migrations
export ORCHESTR8_DISABLE_MIGRATION=1
marimo run orchestr8.py

# Rollback specific feature
export ORCHESTR8_MIGRATE_CODE_CITY_V2=0

# Enable aggressive rollback (immediate on any error)
export ORCHESTR8_ROLLBACK_CODE_CITY=immediate
export ORCHESTR8_ROLLBACK_PANELS=immediate

# Check migration status
cat .orchestr8/migration_state.json
```

---

## 6. Architecture Decision Records

### ADR-001: Use Environment Variables for Feature Flags

**Status:** Adopted (already in use)  
**Decision:** Continue using `ORCHESTR8_*` environment variables for feature flags  
**Rationale:** Already implemented, consistent with project patterns, easy to modify at runtime

### ADR-002: Use Proxy Pattern for Backward Compatibility

**Status:** Proposed  
**Decision:** Implement `MigrationProxy` class for all subsystem migrations  
**Rationale:** Provides clean separation between old/new, enables automatic fallback

### ADR-003: Implement Stage-Based Migration

**Status:** Proposed  
**Decision:** Use 4-stage model: legacy → hybrid → v2 → complete  
**Rationale:** Allows gradual rollout with safety net at each stage

### ADR-004: Persist Migration State for Rollback

**Status:** Proposed  
**Decision:** Use `.orchestr8/migration_state.json` for state tracking  
**Rationale:** Enables debugging, audit trail, and manual rollback verification

---

## 7. Appendix: Complete Migration Config Schema

```toml
# Complete migration configuration schema for pyproject_orchestr8_settings.toml

[migration]
# Global migration settings
enabled = true                          # Master switch for all migrations
default_stage = "legacy"               # Default: legacy, hybrid, v2, complete
auto_rollback = true                   # Enable automatic rollback on errors
max_retries = 3                        # Retry count before rollback (for retry strategy)

[migration.logging]
level = "INFO"                         # DEBUG, INFO, WARNING, ERROR
log_file = ".orchestr8/logs/migration.log"

[migration.code_city]
stage = "legacy"                       # Current migration stage
fallback_on_error = true               # Use legacy on V2 errors
timeout_ms = 5000                     # Timeout before fallback
require_manual_approval = false       # Require manual approval for promotion

[migration.panels]
stage = "legacy"
fallback_on_error = true
timeout_ms = 3000

[migration.connection]
stage = "legacy"
fallback_on_error = true
timeout_ms = 10000

[migration.health]
stage = "legacy"
fallback_on_error = true
timeout_ms = 5000
```

---

## Summary

This migration strategy provides Orchestr8 with a robust framework for evolving its architecture without breaking existing functionality. The key recommendations are:

1. **Feature Flags:** Use consistent `ORCHESTR8_MIGRATE_*` environment variables with a configuration file backup
2. **Proxy Pattern:** Implement `MigrationProxy` class for all subsystem migrations with automatic fallback
3. **Rollback:** Use state persistence with automatic and manual rollback options
4. **Testing:** Build test gates at each migration stage
5. **Staging:** Adopt 4-stage model (legacy → hybrid → v2 → complete) for gradual rollout

The existing wave-based integration strategy in `INTEGRATION_EXECUTION_STRATEGY.md` can be enhanced by adding these migration patterns at each wave boundary.

---

*Research completed by R-4 (Research Agent)*
*Analysis Date: 2026-02-16*
