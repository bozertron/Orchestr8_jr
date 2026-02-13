# VISION REPORT: woven_maps.py

**File:** IP/woven_maps.py  
**Lines:** 1,982  
**Tokens:** 13,678  
**Survey Date:** 2026-02-12  

---

## Purpose

Code City visualization engine. Transforms codebase into a spatial city where files are buildings, imports are connections, and health status is color. The heart of the ∅明nos vision.

## Vision Alignment

### ∅明nos Vision Fit

**THE CENTERPIECE** - This is the realization of the spatial environment vision. Every file becomes a building. Every import becomes infrastructure. The Founder and agents co-inhabit this space.

### Current Status: FULLY IMPLEMENTED (with integration gaps)

| Aspect | Status | Notes |
|--------|--------|-------|
| Code scanning | ✅ Working | scan_codebase() finds all files |
| Layout calculation | ✅ Working | calculate_layout() positions buildings |
| Graph data building | ✅ Working | build_graph_data() creates edges |
| Emergence animation | ✅ Working | Particle coalescence effect |
| Audio reactivity | ✅ Working | Microphone input visualization |
| Keyframe system | ✅ Working | 4 slots, morph between states |
| **Health color integration** | ❌ **MISSING** | Doesn't accept health data |
| **Real-time updates** | ❌ **MISSING** | No Socket.io integration |

## Critical Finding

**Health data not integrated** - The create_code_city() function does not accept health_checker results. All buildings currently use default colors instead of Gold/Teal/Purple based on health.

This directly impacts **Requirement HLTH-02**.

## To Make It "Done"

1. **Accept health_data parameter:**
   ```python
   def create_code_city(health_data: Optional[Dict] = None, ...)
   ```

2. **Map health to colors:**
   ```python
   if health_data and file_path in health_data:
       if health_data[file_path].error_count > 0:
           color = TEAL  # Broken
       elif combat_tracker.is_in_combat(file_path):
           color = PURPLE  # Combat
       else:
           color = GOLD  # Working
   ```

3. **Add refresh mechanism** for re-checking health

## Decision Required

**Question:** Building height represents?
- **Option A:** File size (current)
- **Option B:** Complexity score
- **Option C:** Centrality in import graph
- **Option D:** Combination

**Default recommendation:** Option D - size + complexity + centrality weighted formula.

**Your decision:** _______________

---

**Status:** AWAITING VISION CONFIRMATION
