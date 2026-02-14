# settings-advanced.js Refactoring Plan

**File**: `/home/bozertron/EPO - JFDI - Maestro/src-tauri/html/scripts/settings-advanced.js`  
**Current Size**: 382 lines  
**Target Size**: 2 files, each ≤190 lines  
**Status**: MAJOR VIOLATION - 91% over 200-line limit (182 lines over)

---

## 1. CURRENT STATE ANALYSIS

### 1.1 Complete Function Inventory

**Total Functions**: 17 functions across 382 lines

#### Message Display (Lines 6-12, 1 function)
1. `showMessage(text, type)` - Lines 7-12 (6 lines)

#### Configuration Loading (Lines 14-157, 5 functions)
2. `loadConfig()` - Lines 15-40 (26 lines)
3. `loadMessageProtocolConfig(config)` - Lines 43-66 (24 lines)
4. `loadChatConfig(config)` - Lines 69-95 (27 lines)
5. `loadDatabaseConfig(config)` - Lines 98-130 (33 lines) ❌ **VIOLATION: Exceeds 30 lines**
6. `loadDevelopmentConfig(config)` - Lines 133-157 (25 lines)

#### Configuration Saving (Lines 159-181, 1 function)
7. `saveConfig()` - Lines 160-181 (22 lines)

#### Configuration Building (Lines 183-310, 4 functions)
8. `buildMessageProtocolConfig()` - Lines 184-210 (27 lines)
9. `buildChatConfig()` - Lines 213-242 (30 lines)
10. `buildDatabaseConfig()` - Lines 245-280 (36 lines) ❌ **VIOLATION: Exceeds 30 lines**
11. `buildDevelopmentConfig()` - Lines 283-310 (28 lines)

#### Helper Functions (Lines 312-337, 4 functions)
12. `getFieldValue(id)` - Lines 313-316 (4 lines)
13. `setFieldValue(id, value)` - Lines 319-322 (4 lines)
14. `getToggle(id)` - Lines 325-328 (4 lines)
15. `setToggle(id, active)` - Lines 331-337 (7 lines)

#### Action Functions (Lines 339-363, 2 functions)
16. `resetToDefaults()` - Lines 340-350 (11 lines)
17. `restoreFromBackup()` - Lines 353-363 (11 lines)

#### Initialization (Lines 365-381, 1 function)
18. DOMContentLoaded listener - Lines 366-381 (16 lines)

### 1.2 Dependency Map

**Function Call Graph**:

```
DOMContentLoaded
├── loadConfig()
│   ├── loadMessageProtocolConfig()
│   ├── loadChatConfig()
│   ├── loadDatabaseConfig()
│   └── loadDevelopmentConfig()
└── setupEventListeners()
    ├── saveConfig()
    │   ├── buildMessageProtocolConfig()
    │   ├── buildChatConfig()
    │   ├── buildDatabaseConfig()
    │   └── buildDevelopmentConfig()
    ├── resetToDefaults()
    └── restoreFromBackup()

All load/build functions use:
├── getFieldValue()
├── setFieldValue()
├── getToggle()
└── setToggle()
```

### 1.3 State Usage Audit

**✅ NO VIOLATIONS FOUND**

- No JavaScript state variables
- All configuration queried from Rust via `invoke('config_get_*')`
- All configuration saved to Rust via `invoke('config_update_*')`
- Pattern Bible compliant

### 1.4 Rust Integration Points

**Tauri Commands** (window.__TAURI__.invoke):
1. `config_get_message_protocol` - Line 18
2. `config_get_chat` - Line 19
3. `config_get_database` - Line 20
4. `config_get_development` - Line 21
5. `config_update_message_protocol` - Line 170
6. `config_update_chat` - Line 171
7. `config_update_database` - Line 172
8. `config_update_development` - Line 173
9. `config_reset_to_defaults` - Line 344
10. `config_restore_backup` - Line 357

**All commands exist and are properly used** ✅

### 1.5 Line Count Verification

**Current**: 382 lines  
**Target**: ≤190 lines per file (2 files)  
**Overage**: 182 lines (91% over limit)

---

## 2. VIOLATION FIXES (PHASE 0)

### 2.1 State Management Violations

**✅ NONE FOUND** - File is Pattern Bible compliant for state management

### 2.2 Business Logic Violations

**✅ NONE FOUND** - All business logic is in Rust backend

### 2.3 DOM Creation Violations

**✅ NONE FOUND** - No inline styles, uses CSS classes

### 2.4 Long Function Violations

**Priority**: MEDIUM - 2 functions exceed 30 lines

#### Violation 1: loadDatabaseConfig() (Lines 98-130, 33 lines)

**Current**:
```javascript
function loadDatabaseConfig(config) {
  // SQLite (5 settings)
  setFieldValue('db-path', config.sqlite.database_path);
  setFieldValue('db-journal-mode', config.sqlite.journal_mode);
  setFieldValue('db-synchronous', config.sqlite.synchronous);
  setFieldValue('db-cache-size', config.sqlite.cache_size_kb);
  setFieldValue('db-page-size', config.sqlite.page_size);

  // FTS (4 settings)
  setToggle('db-fts-enabled', config.fts.enabled);
  setFieldValue('db-fts-tokenizer', config.fts.tokenizer);
  setFieldValue('db-fts-rank', config.fts.fts_rank_function);
  setToggle('db-fts-rebuild', config.fts.rebuild_on_startup);

  // Connection Pool (4 settings)
  setFieldValue('db-max-connections', config.connection_pool.max_connections);
  setFieldValue('db-min-connections', config.connection_pool.min_connections);
  setFieldValue('db-connection-timeout', config.connection_pool.connection_timeout_secs);
  setFieldValue('db-idle-timeout', config.connection_pool.idle_timeout_secs);

  // Maintenance (4 settings)
  setToggle('db-auto-vacuum', config.maintenance.auto_vacuum);
  setFieldValue('db-vacuum-interval', config.maintenance.vacuum_interval_days);
  setToggle('db-analyze-startup', config.maintenance.analyze_on_startup);
  setToggle('db-optimize-startup', config.maintenance.optimize_on_startup);

  // Backups (5 settings)
  setToggle('db-backup-enabled', config.backups.enabled);
  setFieldValue('db-backup-interval', config.backups.interval_hours);
  setFieldValue('db-max-backups', config.backups.max_backups);
  setFieldValue('db-backup-path', config.backups.backup_path);
  setToggle('db-compress-backups', config.backups.compress_backups);
}
```

**Fix Plan**: Extract helper functions for each section

**After (≤30 lines)**:
```javascript
function loadDatabaseConfig(config) {
  loadDatabaseSQLiteConfig(config.sqlite);
  loadDatabaseFTSConfig(config.fts);
  loadDatabaseConnectionPoolConfig(config.connection_pool);
  loadDatabaseMaintenanceConfig(config.maintenance);
  loadDatabaseBackupsConfig(config.backups);
}

// Helper functions (in settings_advanced_helpers.js)
function loadDatabaseSQLiteConfig(sqlite) {
  setFieldValue('db-path', sqlite.database_path);
  setFieldValue('db-journal-mode', sqlite.journal_mode);
  setFieldValue('db-synchronous', sqlite.synchronous);
  setFieldValue('db-cache-size', sqlite.cache_size_kb);
  setFieldValue('db-page-size', sqlite.page_size);
}

function loadDatabaseFTSConfig(fts) {
  setToggle('db-fts-enabled', fts.enabled);
  setFieldValue('db-fts-tokenizer', fts.tokenizer);
  setFieldValue('db-fts-rank', fts.fts_rank_function);
  setToggle('db-fts-rebuild', fts.rebuild_on_startup);
}

// ... similar for other sections
```

**Estimated Effort**: 30 minutes

---

#### Violation 2: buildDatabaseConfig() (Lines 245-280, 36 lines)

**Current**:
```javascript
function buildDatabaseConfig() {
  return {
    sqlite: {
      database_path: getFieldValue('db-path'),
      journal_mode: getFieldValue('db-journal-mode'),
      synchronous: getFieldValue('db-synchronous'),
      cache_size_kb: parseInt(getFieldValue('db-cache-size')),
      page_size: parseInt(getFieldValue('db-page-size'))
    },
    fts: {
      enabled: getToggle('db-fts-enabled'),
      tokenizer: getFieldValue('db-fts-tokenizer'),
      rebuild_on_startup: getToggle('db-fts-rebuild'),
      fts_rank_function: getFieldValue('db-fts-rank')
    },
    connection_pool: {
      max_connections: parseInt(getFieldValue('db-max-connections')),
      min_connections: parseInt(getFieldValue('db-min-connections')),
      connection_timeout_secs: parseInt(getFieldValue('db-connection-timeout')),
      idle_timeout_secs: parseInt(getFieldValue('db-idle-timeout'))
    },
    maintenance: {
      auto_vacuum: getToggle('db-auto-vacuum'),
      vacuum_interval_days: parseInt(getFieldValue('db-vacuum-interval')),
      analyze_on_startup: getToggle('db-analyze-startup'),
      optimize_on_startup: getToggle('db-optimize-startup')
    },
    backups: {
      enabled: getToggle('db-backup-enabled'),
      interval_hours: parseInt(getFieldValue('db-backup-interval')),
      max_backups: parseInt(getFieldValue('db-max-backups')),
      backup_path: getFieldValue('db-backup-path'),
      compress_backups: getToggle('db-compress-backups')
    }
  };
}
```

**Fix Plan**: Extract helper functions for each section

**After (≤30 lines)**:
```javascript
function buildDatabaseConfig() {
  return {
    sqlite: buildDatabaseSQLiteConfig(),
    fts: buildDatabaseFTSConfig(),
    connection_pool: buildDatabaseConnectionPoolConfig(),
    maintenance: buildDatabaseMaintenanceConfig(),
    backups: buildDatabaseBackupsConfig()
  };
}

// Helper functions (in settings_advanced_helpers.js)
function buildDatabaseSQLiteConfig() {
  return {
    database_path: getFieldValue('db-path'),
    journal_mode: getFieldValue('db-journal-mode'),
    synchronous: getFieldValue('db-synchronous'),
    cache_size_kb: parseInt(getFieldValue('db-cache-size')),
    page_size: parseInt(getFieldValue('db-page-size'))
  };
}

// ... similar for other sections
```

**Estimated Effort**: 30 minutes

---

### 2.5 Phase 0 Summary

**Total Violations**: 2 long functions  
**Total Fixes Required**: Extract 10 helper functions  
**Estimated Effort**: 1 hour

**After Phase 0**:
- File size: 382 lines (unchanged, but functions ≤30 lines)
- Long functions: 0 (down from 2)
- Ready for file split

---

## 3. EXTRACTION PLAN (POST-PHASE 0)

### 3.1 Target File Structure

**2 Files, Both ≤190 Lines**:

1. **settings-advanced.js** (≤190 lines) - Core load/save/reset logic
2. **settings_advanced_helpers.js** (≤190 lines) - Build/load helper functions

**Total**: ~380 lines (reduced from 382 lines after helper extraction)

---

### 3.2 Line-by-Line Allocation

#### File 1: settings-advanced.js (Core Logic, ≤190 lines)

**Purpose**: Configuration loading, saving, resetting

**Lines to Include**:
- Lines 1-4: Imports and Tauri API
- Lines 6-12: `showMessage()` function
- Lines 14-40: `loadConfig()` function
- Lines 43-66: `loadMessageProtocolConfig()` function
- Lines 69-95: `loadChatConfig()` function
- Lines 98-130: `loadDatabaseConfig()` function (refactored to ≤30 lines)
- Lines 133-157: `loadDevelopmentConfig()` function
- Lines 159-181: `saveConfig()` function
- Lines 183-210: `buildMessageProtocolConfig()` function
- Lines 213-242: `buildChatConfig()` function
- Lines 245-280: `buildDatabaseConfig()` function (refactored to ≤30 lines)
- Lines 283-310: `buildDevelopmentConfig()` function
- Lines 339-363: `resetToDefaults()`, `restoreFromBackup()` functions
- Lines 365-381: DOMContentLoaded listener

**Functions** (17 functions):
1. `showMessage()`
2. `loadConfig()`
3. `loadMessageProtocolConfig()`
4. `loadChatConfig()`
5. `loadDatabaseConfig()` - Refactored
6. `loadDevelopmentConfig()`
7. `saveConfig()`
8. `buildMessageProtocolConfig()`
9. `buildChatConfig()`
10. `buildDatabaseConfig()` - Refactored
11. `buildDevelopmentConfig()`
12. `resetToDefaults()`
13. `restoreFromBackup()`
14. DOMContentLoaded listener

**Estimated Lines**: ~185 lines (5-line buffer)

---

#### File 2: settings_advanced_helpers.js (Helper Functions, ≤190 lines)

**Purpose**: Field get/set helpers, database config helpers

**Lines to Include**:
- Lines 1-4: Imports (if needed)
- Lines 312-337: Field helper functions (4 functions, 26 lines)
- New helper functions for database config (10 functions, ~100 lines):
  - `loadDatabaseSQLiteConfig()`
  - `loadDatabaseFTSConfig()`
  - `loadDatabaseConnectionPoolConfig()`
  - `loadDatabaseMaintenanceConfig()`
  - `loadDatabaseBackupsConfig()`
  - `buildDatabaseSQLiteConfig()`
  - `buildDatabaseFTSConfig()`
  - `buildDatabaseConnectionPoolConfig()`
  - `buildDatabaseMaintenanceConfig()`
  - `buildDatabaseBackupsConfig()`

**Functions** (14 functions):
1. `getFieldValue()`
2. `setFieldValue()`
3. `getToggle()`
4. `setToggle()`
5-14. Database config helpers (10 functions)

**Estimated Lines**: ~130 lines (60-line buffer)

---

### 3.3 Function-by-Function Assignment

**Summary Table**:

| File | Functions | Lines | Status |
|------|-----------|-------|--------|
| settings-advanced.js | 14 | ~185 | ✅ Under 190 |
| settings_advanced_helpers.js | 14 | ~130 | ✅ Under 190 |
| **TOTAL** | **28** | **~315** | ✅ All compliant |

---

### 3.4 Helper File Structure

**Same directory as parent**: `/home/bozertron/EPO - JFDI - Maestro/src-tauri/html/scripts/`

```
html/scripts/
├── settings-advanced.js (≤190 lines)
└── settings_advanced_helpers.js (≤190 lines)
```

---

### 3.5 Import/Export Declarations

**Script Loading Order** (in settings-advanced.html):
```html
<!-- Load helpers first -->
<script src="../scripts/settings_advanced_helpers.js"></script>

<!-- Load main last -->
<script src="../scripts/settings-advanced.js"></script>
```

---

## 4. REFACTORING STEPS

### 4.1 Phase 0: Fix Long Functions (30 minutes)

#### Step 1: Extract Database Config Helpers (15 minutes)

**Actions**:
1. Create git commit: "Pre-Phase 0: Before function refactoring"
2. Extract 10 helper functions for database config
3. Update `loadDatabaseConfig()` to call helpers
4. Update `buildDatabaseConfig()` to call helpers
5. Verify functions ≤30 lines

**Validation Checkpoint**:
- ✅ All functions ≤30 lines
- ✅ Functionality preserved
- ✅ 0 errors in browser console

**Rollback Plan**: Git revert to "Pre-Phase 0" commit

---

#### Step 2: Test Functionality (15 minutes)

**Actions**:
1. Load settings-advanced.html
2. Verify all settings load correctly
3. Modify settings and save
4. Verify settings save correctly
5. Test reset to defaults
6. Test restore from backup

**Validation Checkpoint**:
- ✅ All settings load correctly
- ✅ All settings save correctly
- ✅ Reset works
- ✅ Restore works
- ✅ 0 errors in browser console

**Rollback Plan**: Git revert to "Pre-Phase 0" commit

---

### 4.2 Phase 1: Split File (1 hour)

#### Step 1: Create Helper File (15 minutes)

**Actions**:
1. Create git commit: "Pre-Phase 1: Before file split"
2. Create `settings_advanced_helpers.js`
3. Copy helper functions to new file
4. Verify file ≤190 lines

**Validation Checkpoint**:
- ✅ Helper file created
- ✅ Helper file ≤190 lines
- ✅ No duplicate functions

**Rollback Plan**: Delete helper file, git revert

---

#### Step 2: Update Script Loading (5 minutes)

**Actions**:
1. Update settings-advanced.html to load helper file first
2. Verify script loading order

**Validation Checkpoint**:
- ✅ Scripts load in correct order
- ✅ No "function not defined" errors

**Rollback Plan**: Revert HTML changes

---

#### Step 3: Remove Extracted Code (10 minutes)

**Actions**:
1. Remove helper functions from settings-advanced.js
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
1. Load settings-advanced.html
2. Test all 4 configuration sections:
   - Message Protocol (routing, persistence, delivery, events)
   - Chat (messages, storage, maestro, features)
   - Database (SQLite, FTS, connection pool, maintenance, backups)
   - Development (logging, relay server, MCP server, debug)
3. Test save functionality
4. Test reset to defaults
5. Test restore from backup
6. Check browser console for errors

**Validation Checkpoint**:
- ✅ All settings load correctly
- ✅ All settings save correctly
- ✅ All toggles work
- ✅ All inputs validate
- ✅ Reset works
- ✅ Restore works
- ✅ 0 errors in browser console
- ✅ 0 warnings in browser console

**Rollback Plan**: Git revert to "Pre-Phase 1" commit

---

## 5. TESTING PLAN

### 5.1 Functionality to Test

**After Phase 0** (Function Refactoring):
1. ✅ All settings load from Rust backend
2. ✅ All settings display correctly in UI
3. ✅ All toggles work
4. ✅ All inputs accept valid values
5. ✅ Save button saves all settings
6. ✅ Reset button resets to defaults
7. ✅ Restore button restores from backup

**After Phase 1** (File Split):
1. ✅ All Phase 0 tests pass
2. ✅ Scripts load in correct order
3. ✅ No "function not defined" errors
4. ✅ Helper functions accessible from main file

### 5.2 Expected Behavior

**Configuration Loading**:
- All 4 sections load simultaneously (Promise.all)
- All fields populate with current values from Rust
- All toggles reflect current state
- No errors in console

**Configuration Saving**:
- All 4 sections save simultaneously (Promise.all)
- Success message displays after save
- No errors in console

**Reset to Defaults**:
- Confirmation dialog appears
- All settings reset to default values
- Settings reload from Rust
- Success message displays

**Restore from Backup**:
- Confirmation dialog appears
- Settings restore from backup
- Settings reload from Rust
- Success message displays

### 5.3 Browser Console Validation

**Required**: 0 errors, 0 warnings

**Check for**:
- ❌ "Uncaught ReferenceError: function is not defined"
- ❌ "Failed to invoke Tauri command"
- ❌ Any console.error() output

**Acceptable**:
- ✅ console.log() debug messages

### 5.4 Tauri Command Verification

**Test Each Command**:
1. `config_get_message_protocol` - Verify data structure
2. `config_get_chat` - Verify data structure
3. `config_get_database` - Verify data structure
4. `config_get_development` - Verify data structure
5. `config_update_message_protocol` - Verify save works
6. `config_update_chat` - Verify save works
7. `config_update_database` - Verify save works
8. `config_update_development` - Verify save works
9. `config_reset_to_defaults` - Verify reset works
10. `config_restore_backup` - Verify restore works

---

## 6. COMPLETION CRITERIA

### Phase 0 Complete When:
- ✅ All functions ≤30 lines
- ✅ 10 helper functions extracted
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

**Phase 0**: 30 minutes  
**Phase 1**: 1 hour  
**Total**: 1.5 hours

---

## 9. SUCCESS METRICS

**Quantitative**:
- File count: 1 → 2 files
- Average file size: 382 lines → ~190 lines per file
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

