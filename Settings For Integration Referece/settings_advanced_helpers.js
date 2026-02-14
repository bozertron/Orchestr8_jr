/**
 * Settings Advanced Helper Functions
 * Pattern Bible: Helper functions for loading/building advanced configuration sections
 */

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function getFieldValue(id) {
  const el = document.getElementById(id);
  return el ? el.value : '';
}

function setFieldValue(id, value) {
  const el = document.getElementById(id);
  if (el) el.value = value;
}

function getToggle(id) {
  const el = document.getElementById(id);
  return el ? el.classList.contains('active') : false;
}

function setToggle(id, active) {
  const el = document.getElementById(id);
  if (el) {
    if (active) el.classList.add('active');
    else el.classList.remove('active');
  }
}

// ============================================================================
// LOAD DATABASE CONFIG HELPERS
// ============================================================================

function loadDatabaseSQLiteSettings(sqlite) {
  setFieldValue('db-path', sqlite.database_path);
  setFieldValue('db-journal-mode', sqlite.journal_mode);
  setFieldValue('db-synchronous', sqlite.synchronous);
  setFieldValue('db-cache-size', sqlite.cache_size_kb);
  setFieldValue('db-page-size', sqlite.page_size);
}

function loadDatabaseFTSSettings(fts) {
  setToggle('db-fts-enabled', fts.enabled);
  setFieldValue('db-fts-tokenizer', fts.tokenizer);
  setFieldValue('db-fts-rank', fts.fts_rank_function);
  setToggle('db-fts-rebuild', fts.rebuild_on_startup);
}

function loadDatabaseConnectionPoolSettings(pool) {
  setFieldValue('db-max-connections', pool.max_connections);
  setFieldValue('db-min-connections', pool.min_connections);
  setFieldValue('db-connection-timeout', pool.connection_timeout_secs);
  setFieldValue('db-idle-timeout', pool.idle_timeout_secs);
}

function loadDatabaseMaintenanceSettings(maintenance) {
  setToggle('db-auto-vacuum', maintenance.auto_vacuum);
  setFieldValue('db-vacuum-interval', maintenance.vacuum_interval_days);
  setToggle('db-analyze-startup', maintenance.analyze_on_startup);
  setToggle('db-optimize-startup', maintenance.optimize_on_startup);
}

function loadDatabaseBackupSettings(backups) {
  setToggle('db-backup-enabled', backups.enabled);
  setFieldValue('db-backup-interval', backups.interval_hours);
  setFieldValue('db-max-backups', backups.max_backups);
  setFieldValue('db-backup-path', backups.backup_path);
  setToggle('db-compress-backups', backups.compress_backups);
}

// ============================================================================
// BUILD DATABASE CONFIG HELPERS
// ============================================================================

function buildDatabaseSQLiteConfig() {
  return {
    database_path: getFieldValue('db-path'),
    journal_mode: getFieldValue('db-journal-mode'),
    synchronous: getFieldValue('db-synchronous'),
    cache_size_kb: parseInt(getFieldValue('db-cache-size')),
    page_size: parseInt(getFieldValue('db-page-size'))
  };
}

function buildDatabaseFTSConfig() {
  return {
    enabled: getToggle('db-fts-enabled'),
    tokenizer: getFieldValue('db-fts-tokenizer'),
    rebuild_on_startup: getToggle('db-fts-rebuild'),
    fts_rank_function: getFieldValue('db-fts-rank')
  };
}

function buildDatabaseConnectionPoolConfig() {
  return {
    max_connections: parseInt(getFieldValue('db-max-connections')),
    min_connections: parseInt(getFieldValue('db-min-connections')),
    connection_timeout_secs: parseInt(getFieldValue('db-connection-timeout')),
    idle_timeout_secs: parseInt(getFieldValue('db-idle-timeout'))
  };
}

function buildDatabaseMaintenanceConfig() {
  return {
    auto_vacuum: getToggle('db-auto-vacuum'),
    vacuum_interval_days: parseInt(getFieldValue('db-vacuum-interval')),
    analyze_on_startup: getToggle('db-analyze-startup'),
    optimize_on_startup: getToggle('db-optimize-startup')
  };
}

function buildDatabaseBackupConfig() {
  return {
    enabled: getToggle('db-backup-enabled'),
    interval_hours: parseInt(getFieldValue('db-backup-interval')),
    max_backups: parseInt(getFieldValue('db-max-backups')),
    backup_path: getFieldValue('db-backup-path'),
    compress_backups: getToggle('db-compress-backups')
  };
}

// Note: Load/build config functions moved to settings_advanced_helpers_config.js

