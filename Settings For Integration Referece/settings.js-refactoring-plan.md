# settings.js Refactoring Plan

**File**: `/home/bozertron/EPO - JFDI - Maestro/src-tauri/html/scripts/settings.js`  
**Current Size**: 256 lines  
**Target Size**: 2 files, each ≤190 lines  
**Status**: MODERATE VIOLATION - 28% over 200-line limit (56 lines over)

---

## 1. CURRENT STATE ANALYSIS

### 1.1 Complete Function Inventory

**Total Functions**: 16 functions across 256 lines

#### Configuration Loading (Lines 5-67, 1 function)
1. `loadSettings()` - Lines 6-67 (62 lines) ❌ **VIOLATION: Exceeds 30 lines**

#### Configuration Saving (Lines 69-132, 1 function)
2. `saveSettings()` - Lines 70-132 (63 lines) ❌ **VIOLATION: Exceeds 30 lines**

#### Action Functions (Lines 134-172, 4 functions)
3. `resetToDefaults()` - Lines 135-139 (5 lines)
4. `restoreBackup()` - Lines 142-146 (5 lines)
5. `exportConfig()` - Lines 149-158 (10 lines)
6. `importConfig(event)` - Lines 161-172 (12 lines)

#### Validation Functions (Lines 174-199, 3 functions)
7. `validateNetworkSettings()` - Lines 175-181 (7 lines)
8. `validateSecuritySettings()` - Lines 184-190 (7 lines)
9. `validateUISettings()` - Lines 193-199 (7 lines)

#### UI Functions (Lines 201-216, 3 functions)
10. `applyThemePreview()` - Lines 202-205 (4 lines)
11. `showSuccessMessage(msg)` - Lines 208-212 (5 lines)
12. `showErrorMessage(msg)` - Lines 213-216 (4 lines)

#### Helper Functions (Lines 218-227, 8 functions)
13. `$(id)` - Line 219 (1 line)
14. `setToggle(id, v)` - Line 220 (1 line)
15. `getToggle(id)` - Line 221 (1 line)
16. `setSlider(id, v)` - Line 222 (1 line)
17. `getSlider(id)` - Line 223 (1 line)
18. `setValue(id, v)` - Line 224 (1 line)
19. `getValue(id)` - Line 225 (1 line)
20. `getNumber(id)` - Line 226 (1 line)
21. `setColor(id, v)` - Line 227 (1 line)

#### Initialization (Lines 229-255, 1 function)
22. DOMContentLoaded listener - Lines 230-255 (26 lines)

### 1.2 Dependency Map

**Function Call Graph**:

```
DOMContentLoaded
├── loadSettings()
│   ├── setToggle()
│   ├── setSlider()
│   ├── setValue()
│   └── setColor()
└── setupEventListeners()
    ├── saveSettings()
    │   ├── validateNetworkSettings()
    │   ├── validateSecuritySettings()
    │   ├── validateUISettings()
    │   ├── getToggle()
    │   ├── getSlider()
    │   ├── getValue()
    │   └── getNumber()
    ├── resetToDefaults()
    ├── restoreBackup()
    ├── exportConfig()
    ├── importConfig()
    └── applyThemePreview()
```

### 1.3 State Usage Audit

**✅ NO VIOLATIONS FOUND**

- No JavaScript state variables
- All configuration queried from Rust via `invoke('config_get')`
- All configuration saved to Rust via `invoke('config_update_*')`
- Pattern Bible compliant

### 1.4 Rust Integration Points

**Tauri Commands** (window.__TAURI__.invoke):
1. `config_get` - Line 8
2. `config_get_path` - Line 9
3. `config_update_network` - Line 74
4. `config_update_security` - Line 91
5. `config_update_ui` - Line 111
6. `config_reset_to_defaults` - Line 137
7. `config_restore_backup` - Line 144
8. `config_get` (for export) - Line 151
9. `config_update_network` (for import) - Line 166
10. `config_update_security` (for import) - Line 167
11. `config_update_ui` (for import) - Line 168

**All commands exist and are properly used** ✅

### 1.5 Line Count Verification

**Current**: 256 lines  
**Target**: ≤190 lines per file (2 files)  
**Overage**: 56 lines (28% over limit)

---

## 2. VIOLATION FIXES (PHASE 0)

### 2.1 State Management Violations

**✅ NONE FOUND** - File is Pattern Bible compliant for state management

### 2.2 Business Logic Violations

**✅ NONE FOUND** - All business logic is in Rust backend

### 2.3 DOM Creation Violations

**✅ NONE FOUND** - No inline styles, uses CSS classes

### 2.4 Long Function Violations

**Priority**: HIGH - 2 functions exceed 30 lines significantly

#### Violation 1: loadSettings() (Lines 6-67, 62 lines)

**Current**: Loads 50+ settings in one function

**Fix Plan**: Extract helper functions for each section

**After (≤30 lines)**:
```javascript
async function loadSettings() {
  try {
    const c = await invoke('config_get');
    document.getElementById('config-path').textContent = await invoke('config_get_path');

    loadNetworkSettings(c.network);
    loadSecuritySettings(c.security);
    loadUISettings(c.ui);
  } catch (e) {
    showErrorMessage('Failed to load settings: ' + e);
  }
}

// Helper functions (in settings_helpers.js)
function loadNetworkSettings(network) {
  // P2P settings (9 settings)
  setToggle('p2p-enabled', network.p2p.enabled);
  setSlider('max-peers', network.p2p.max_peers);
  setValue('discovery-interval', network.p2p.discovery_interval_secs);
  // ... etc
}

function loadSecuritySettings(security) {
  // Encryption, auth, keys, signing (15 settings)
  setToggle('encryption-enabled', security.encryption.enabled);
  setValue('session-timeout', security.auth.session_timeout_days);
  // ... etc
}

function loadUISettings(ui) {
  // Theme, language, notifications, layout, behavior (11 settings)
  setValue('theme-mode', ui.theme.mode);
  setColor('accent-color', ui.theme.accent_color);
  // ... etc
}
```

**Estimated Effort**: 30 minutes

---

#### Violation 2: saveSettings() (Lines 70-132, 63 lines)

**Current**: Builds and saves 3 config objects in one function

**Fix Plan**: Extract helper functions for building config objects

**After (≤30 lines)**:
```javascript
async function saveSettings() {
  try {
    if (!validateNetworkSettings() || !validateSecuritySettings() || !validateUISettings()) return;

    await invoke('config_update_network', { network: buildNetworkConfig() });
    await invoke('config_update_security', { security: buildSecurityConfig() });
    await invoke('config_update_ui', { ui: buildUIConfig() });

    showSuccessMessage('Settings saved successfully');
  } catch (e) {
    showErrorMessage('Failed to save settings: ' + e);
  }
}

// Helper functions (in settings_helpers.js)
function buildNetworkConfig() {
  return {
    p2p: {
      enabled: getToggle('p2p-enabled'),
      listen_port: 0,
      max_peers: getSlider('max-peers'),
      // ... etc
    },
    relay: { /* ... */ },
    webrtc: { /* ... */ },
    transport: { /* ... */ }
  };
}

function buildSecurityConfig() {
  return {
    encryption: { /* ... */ },
    authentication: { /* ... */ },
    keys: { /* ... */ },
    signing: { /* ... */ }
  };
}

function buildUIConfig() {
  return {
    theme: { /* ... */ },
    language: { /* ... */ },
    notifications: { /* ... */ },
    layout: { /* ... */ },
    behavior: { /* ... */ }
  };
}
```

**Estimated Effort**: 30 minutes

---

### 2.5 Phase 0 Summary

**Total Violations**: 2 long functions  
**Total Fixes Required**: Extract 6 helper functions  
**Estimated Effort**: 1 hour

**After Phase 0**:
- File size: 256 lines (unchanged, but functions ≤30 lines)
- Long functions: 0 (down from 2)
- Ready for file split

---

## 3. EXTRACTION PLAN (POST-PHASE 0)

### 3.1 Target File Structure

**2 Files, Both ≤190 Lines**:

1. **settings.js** (≤190 lines) - Core load/save/action logic
2. **settings_helpers.js** (≤190 lines) - Build/load/validation helpers

**Total**: ~250 lines (reduced from 256 lines after helper extraction)

---

### 3.2 Line-by-Line Allocation

#### File 1: settings.js (Core Logic, ≤190 lines)

**Purpose**: Configuration loading, saving, actions, initialization

**Lines to Include**:
- Lines 1-3: Imports and Tauri API
- Lines 6-67: `loadSettings()` function (refactored to ≤30 lines)
- Lines 70-132: `saveSettings()` function (refactored to ≤30 lines)
- Lines 135-172: Action functions (4 functions, 38 lines)
- Lines 175-199: Validation functions (3 functions, 25 lines)
- Lines 202-216: UI functions (3 functions, 15 lines)
- Lines 219-227: Helper functions (9 functions, 9 lines)
- Lines 230-255: DOMContentLoaded listener (26 lines)

**Functions** (22 functions):
1. `loadSettings()` - Refactored
2. `saveSettings()` - Refactored
3. `resetToDefaults()`
4. `restoreBackup()`
5. `exportConfig()`
6. `importConfig()`
7. `validateNetworkSettings()`
8. `validateSecuritySettings()`
9. `validateUISettings()`
10. `applyThemePreview()`
11. `showSuccessMessage()`
12. `showErrorMessage()`
13-21. Helper functions (9 functions)
22. DOMContentLoaded listener

**Estimated Lines**: ~180 lines (10-line buffer)

---

#### File 2: settings_helpers.js (Helper Functions, ≤190 lines)

**Purpose**: Config building and loading helpers

**Lines to Include**:
- Lines 1-3: Imports (if needed)
- New helper functions (~70 lines):
  - `loadNetworkSettings(network)` (~20 lines)
  - `loadSecuritySettings(security)` (~25 lines)
  - `loadUISettings(ui)` (~15 lines)
  - `buildNetworkConfig()` (~20 lines)
  - `buildSecurityConfig()` (~20 lines)
  - `buildUIConfig()` (~15 lines)

**Functions** (6 functions):
1. `loadNetworkSettings()`
2. `loadSecuritySettings()`
3. `loadUISettings()`
4. `buildNetworkConfig()`
5. `buildSecurityConfig()`
6. `buildUIConfig()`

**Estimated Lines**: ~75 lines (115-line buffer)

---

### 3.3 Function-by-Function Assignment

**Summary Table**:

| File | Functions | Lines | Status |
|------|-----------|-------|--------|
| settings.js | 22 | ~180 | ✅ Under 190 |
| settings_helpers.js | 6 | ~75 | ✅ Under 190 |
| **TOTAL** | **28** | **~255** | ✅ All compliant |

---

### 3.4 Helper File Structure

**Same directory as parent**: `/home/bozertron/EPO - JFDI - Maestro/src-tauri/html/scripts/`

```
html/scripts/
├── settings.js (≤190 lines)
└── settings_helpers.js (≤190 lines)
```

---

### 3.5 Import/Export Declarations

**Script Loading Order** (in settings.html):
```html
<!-- Load helpers first -->
<script src="../scripts/settings_helpers.js"></script>

<!-- Load main last -->
<script src="../scripts/settings.js"></script>
```

---

## 4. REFACTORING STEPS

### 4.1 Phase 0: Fix Long Functions (1 hour)

#### Step 1: Extract Load Helpers (30 minutes)

**Actions**:
1. Create git commit: "Pre-Phase 0: Before function refactoring"
2. Extract 3 helper functions for loading:
   - `loadNetworkSettings()`
   - `loadSecuritySettings()`
   - `loadUISettings()`
3. Update `loadSettings()` to call helpers
4. Verify function ≤30 lines
5. Test loading functionality

**Validation Checkpoint**:
- ✅ `loadSettings()` ≤30 lines
- ✅ All settings load correctly
- ✅ 0 errors in browser console

**Rollback Plan**: Git revert to "Pre-Phase 0" commit

---

#### Step 2: Extract Build Helpers (30 minutes)

**Actions**:
1. Extract 3 helper functions for building:
   - `buildNetworkConfig()`
   - `buildSecurityConfig()`
   - `buildUIConfig()`
2. Update `saveSettings()` to call helpers
3. Verify function ≤30 lines
4. Test saving functionality

**Validation Checkpoint**:
- ✅ `saveSettings()` ≤30 lines
- ✅ All settings save correctly
- ✅ 0 errors in browser console

**Rollback Plan**: Git revert to "Pre-Phase 0" commit

---

### 4.2 Phase 1: Split File (1 hour)

#### Step 1: Create Helper File (15 minutes)

**Actions**:
1. Create git commit: "Pre-Phase 1: Before file split"
2. Create `settings_helpers.js`
3. Copy 6 helper functions to new file
4. Verify file ≤190 lines

**Validation Checkpoint**:
- ✅ Helper file created
- ✅ Helper file ≤190 lines
- ✅ No duplicate functions

**Rollback Plan**: Delete helper file, git revert

---

#### Step 2: Update Script Loading (5 minutes)

**Actions**:
1. Update settings.html to load helper file first
2. Verify script loading order

**Validation Checkpoint**:
- ✅ Scripts load in correct order
- ✅ No "function not defined" errors

**Rollback Plan**: Revert HTML changes

---

#### Step 3: Remove Extracted Code (10 minutes)

**Actions**:
1. Remove helper functions from settings.js
2. Verify main file ≤190 lines
3. Verify no duplicate functions

**Validation Checkpoint**:
- ✅ Main file ≤190 lines
- ✅ No duplicate functions
- ✅ All functions still accessible

**Rollback Plan**: Git revert to "Pre-Phase 1" commit

---

#### Step 4: Test All Functionality (30 minutes)

**Actions**:
1. Load settings.html
2. Test all 3 configuration sections:
   - Network (P2P, relay, WebRTC, transport)
   - Security (encryption, auth, keys, signing)
   - UI (theme, language, notifications, layout, behavior)
3. Test save functionality
4. Test validation (invalid inputs)
5. Test reset to defaults
6. Test restore from backup
7. Test export configuration
8. Test import configuration
9. Test theme preview
10. Check browser console for errors

**Validation Checkpoint**:
- ✅ All settings load correctly
- ✅ All settings save correctly
- ✅ All toggles work
- ✅ All sliders work
- ✅ All inputs validate
- ✅ Reset works
- ✅ Restore works
- ✅ Export works
- ✅ Import works
- ✅ Theme preview works
- ✅ 0 errors in browser console
- ✅ 0 warnings in browser console

**Rollback Plan**: Git revert to "Pre-Phase 1" commit

---

## 5. TESTING PLAN

### 5.1 Functionality to Test

**After Phase 0** (Function Refactoring):
1. ✅ All settings load from Rust backend
2. ✅ All settings display correctly in UI
3. ✅ All settings save to Rust backend
4. ✅ Validation works for invalid inputs

**After Phase 1** (File Split):
1. ✅ All Phase 0 tests pass
2. ✅ Scripts load in correct order
3. ✅ No "function not defined" errors
4. ✅ Helper functions accessible from main file

### 5.2 Expected Behavior

**Configuration Loading**:
- All settings load from Rust
- All fields populate with current values
- All toggles reflect current state
- All sliders show current values
- No errors in console

**Configuration Saving**:
- Validation runs before save
- Invalid inputs show error message
- Valid inputs save to Rust
- Success message displays after save
- No errors in console

**Validation**:
- Max peers: 1-1000
- Discovery interval: >0
- Relay URL: ws:// or wss://
- Session timeout: >0
- Max devices: >0
- Pairing code length: ≥4
- Font size: 8-32
- Accent color: valid hex color
- Theme mode: 'dark' or 'light'

### 5.3 Browser Console Validation

**Required**: 0 errors, 0 warnings

**Check for**:
- ❌ "Uncaught ReferenceError: function is not defined"
- ❌ "Failed to invoke Tauri command"
- ❌ Any console.error() output

**Acceptable**:
- ✅ console.log() debug messages

---

## 6. COMPLETION CRITERIA

### Phase 0 Complete When:
- ✅ All functions ≤30 lines
- ✅ 6 helper functions extracted
- ✅ 100% functionality preserved
- ✅ 0 errors in browser console

### Phase 1 Complete When:
- ✅ 2 files created, both ≤190 lines
- ✅ Scripts load in correct order
- ✅ 100% functionality preserved
- ✅ 0 errors in browser console
- ✅ 0 warnings in browser console
- ✅ All tests pass (section 5)
- ✅ Git commits created for each step

---

## 7. RISK ASSESSMENT

### Low Risk Items:
1. **Function Refactoring** - Simple extraction, low risk
   - Mitigation: Test after each extraction
   - Fallback: Git revert

2. **File Split** - Straightforward, low risk
   - Mitigation: Verify file sizes before removing code
   - Fallback: Git revert

---

## 8. ESTIMATED TOTAL EFFORT

**Phase 0**: 1 hour  
**Phase 1**: 1 hour  
**Total**: 2 hours

---

## 9. SUCCESS METRICS

**Quantitative**:
- File count: 1 → 2 files
- Average file size: 256 lines → ~190 lines per file
- Long functions: 2 → 0

**Qualitative**:
- ✅ 100% Pattern Bible compliance
- ✅ 100% functionality preserved
- ✅ 0 errors in browser console
- ✅ Improved maintainability

---

**END OF PLAN**

**Status**: ✅ READY FOR EXECUTION  
**Next Step**: Await user approval to proceed with Phase 0

