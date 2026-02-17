# FEEDBACK ON ARCHITECTURE_SYNTHESIS.md
**Generated:** 2026-02-16

---

## STRENGTHS

1. **Comprehensive analysis** - 5 parallel agent swarms provides good coverage
2. **Layer violation identification** - Critical L1→L3 issues well documented
3. **Canonical structure** - Clear L1-L5 separation makes sense
4. **Evidence-based** - File paths and line numbers cited

---

## GAPS & CONCERNS

### 1. Missing: Marimo-Specific Considerations

The synthesis mentions "Standard Python package structure works perfectly" but doesn't address:
- **Cell execution order** - Not determined by file location, but by variable references
- **Global state** - Must use `mo.state()` which requires module-level initialization
- **UI element globals** - All `mo.ui.*` elements must be global variables

**Recommendation:** Add section on Marimo-specific patterns

### 2. Missing: Visual Token Integration

The canonical structure has `schemas/tokens/` but doesn't address:
- How VISUAL_TOKEN_LOCK.md flows into the structure
- The exact CSS/typography/dimension tokens
- The Three.js integration with color tokens

**Recommendation:** Add visual token layer to L1 (presentation)

### 3. Missing: The 2D/3D Files

The structure places `woven_maps.py` in L4 but doesn't address:
- `woven_maps_3d.js` - Where does this go?
- `woven_maps_template.html` - Static assets location
- Font files - Where do Marcellus SC, Poiret One, VT323 live?

**Recommendation:** Add `static/` layer or `presentation/assets/`

### 4. Concern: Migration Complexity

The 4-phase migration (sys.path → L1→L3 → singletons → woven_maps) is:
- Ambitious but risky
- No rollback plan if phase fails
- No parallelization possible (phases are sequential)

**Recommendation:** Add rollback criteria for each phase

### 5. Missing: Integration Testing Strategy

No mention of:
- How to test migrations don't break existing functionality
- Mock strategies for external dependencies
- End-to-end test requirements

---

## IDEAS FOR SUCCESSFUL INTEGRATION

### Idea 1: Layer Contract Testing

Add explicit contract tests between layers:

```python
# tests/contracts/test_l1_l2.py
def test_l1_does_not_import_l3():
    """L1 (presentation) should not import L3 (services) directly."""
    # Import audit
    pass
```

### Idea 2: Visual Token Gate

Add automated visual token verification:

```python
# tests/visual/test_tokens.py
def test_css_tokens_match_lock():
    """Verify orchestr8.css tokens match VISUAL_TOKEN_LOCK.md"""
    lock = load_visual_token_lock()
    css = load_css_variables()
    assert css['--bg-obsidian'] == lock['--bg-obsidian']
```

### Idea 3: Feature Flags for Migration

Instead of big-bang migration, use feature flags:

```python
# orchestr8_next/config.py
class FeatureFlags:
    USE_NEW_STRUCTURE = os.getenv('ORCHESTR8_USE_NEW', 'false') == 'true'
```

### Idea 4: Incremental Migration with Proxy Pattern

Instead of moving files, create proxy interfaces:

```python
# orchestr8_next/compat.py
# Old import: from IP import health_checker
# New: from orchestr8_next.services.health import HealthChecker

class HealthCheckerProxy:
    """Proxy that routes to old or new implementation based on flag."""
    pass
```

---

## SPECIFIC RECOMMENDATIONS

| Area | Recommendation |
|------|----------------|
| **Structure** | Add `static/` directory for JS/CSS/fonts |
| **Testing** | Add layer contract tests |
| **Migration** | Add feature flags for rollback |
| **Visual** | Add visual token gate to CI |
| **Docs** | Document Marimo-specific patterns |
| **Migration** | Add checkpoint criteria for each phase |

---

## QUESTIONS FOR THE TEAM

1. How do we handle the 37 artifact files - should they be in `.planning/artifacts/` or deleted?

2. Is the 4-phase migration realistic, or should we break it into smaller increments?

3. Should we keep backward compatibility with old imports (IP/ style) or force new imports?

4. How do we verify visual tokens haven't drifted during migration?

---

## SUMMARY

The architecture synthesis is **strong foundation** but needs:
1. Visual token integration layer
2. Static asset handling (JS/fonts)
3. Marimo-specific patterns documented
4. Migration rollback strategy
5. Contract testing between layers

**Overall: Ready for refinement, not yet ready for execution.**