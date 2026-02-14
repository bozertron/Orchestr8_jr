/**
 * Settings Advanced Helper Functions - Config Load/Build
 * Pattern Bible: Extracted from settings_advanced_helpers.js for hyper-modular architecture
 * Purpose: Load and build configuration objects for settings-advanced.js
 */

// ============================================================================
// LOAD CONFIG FUNCTIONS
// ============================================================================

function loadMessageProtocolConfig(config) {
  setFieldValue('mp-max-retries', config.routing.max_retries);
  setFieldValue('mp-retry-backoff', config.routing.retry_backoff_ms);
  setFieldValue('mp-delivery-timeout', config.routing.delivery_timeout_secs);
  setToggle('mp-prefer-direct', config.routing.prefer_direct_connection);
  setToggle('mp-persistence-enabled', config.persistence.enabled);
  setFieldValue('mp-retention-days', config.persistence.retention_days);
  setFieldValue('mp-max-storage', config.persistence.max_storage_mb);
  setToggle('mp-auto-cleanup', config.persistence.auto_cleanup);
  setToggle('mp-compress-old', config.persistence.compress_old_messages);
  setToggle('mp-require-ack', config.delivery.require_acknowledgment);
  setToggle('mp-offline-queue', config.delivery.offline_queue_enabled);
  setFieldValue('mp-max-queue-size', config.delivery.max_queue_size);
  setToggle('mp-resend-reconnect', config.delivery.resend_on_reconnect);
  setToggle('mp-event-logging', config.events.event_logging_enabled);
  setFieldValue('mp-event-retention', config.events.event_retention_days);
}

function loadChatConfig(config) {
  setFieldValue('chat-max-length', config.messages.max_message_length);
  setFieldValue('chat-history-retention', config.messages.history_retention_days);
  setToggle('chat-enable-editing', config.messages.enable_editing);
  setFieldValue('chat-edit-time-limit', config.messages.edit_time_limit_mins);
  setToggle('chat-enable-deletion', config.messages.enable_deletion);
  setFieldValue('chat-database-path', config.storage.database_path);
  setToggle('chat-fts-enabled', config.storage.fts_enabled);
  setFieldValue('chat-auto-archive', config.storage.auto_archive_days);
  setFieldValue('chat-search-history', config.storage.search_history_days);
  setToggle('maestro-enabled', config.maestro.enabled);
  setFieldValue('maestro-mode', config.maestro.default_mode);
  setFieldValue('maestro-model', config.maestro.ollama_model);
  setFieldValue('maestro-temperature', config.maestro.temperature);
  setFieldValue('maestro-max-tokens', config.maestro.max_tokens);
  setToggle('chat-typing-indicators', config.features.typing_indicators);
  setToggle('chat-read-receipts', config.features.read_receipts);
  setToggle('chat-reactions', config.features.reactions_enabled);
  setToggle('chat-threads', config.features.threads_enabled);
}

function loadDatabaseConfig(config) {
  loadDatabaseSQLiteSettings(config.sqlite);
  loadDatabaseFTSSettings(config.fts);
  loadDatabaseConnectionPoolSettings(config.connection_pool);
  loadDatabaseMaintenanceSettings(config.maintenance);
  loadDatabaseBackupSettings(config.backups);
}

function loadDevelopmentConfig(config) {
  setFieldValue('dev-log-level', config.logging.level);
  setToggle('dev-log-to-file', config.logging.log_to_file);
  setFieldValue('dev-log-path', config.logging.log_path);
  setFieldValue('dev-max-log-size', config.logging.max_log_size_mb);
  setToggle('dev-hot-reload', config.hot_reload.enabled);
  setFieldValue('dev-reload-delay', config.hot_reload.delay_ms);
  setToggle('dev-mock-p2p', config.testing.mock_p2p_connections);
  setToggle('dev-mock-llm', config.testing.mock_llm_responses);
  setToggle('dev-debug-ui', config.testing.debug_ui_events);
  setToggle('dev-verbose-errors', config.testing.verbose_error_messages);
}

// ============================================================================
// BUILD CONFIG FUNCTIONS
// ============================================================================

function buildMessageProtocolConfig() {
  return {
    routing: {
      max_retries: parseInt(getFieldValue('mp-max-retries')),
      retry_backoff_ms: parseInt(getFieldValue('mp-retry-backoff')),
      delivery_timeout_secs: parseInt(getFieldValue('mp-delivery-timeout')),
      prefer_direct_connection: getToggle('mp-prefer-direct')
    },
    persistence: {
      enabled: getToggle('mp-persistence-enabled'),
      retention_days: parseInt(getFieldValue('mp-retention-days')),
      max_storage_mb: parseInt(getFieldValue('mp-max-storage')),
      auto_cleanup: getToggle('mp-auto-cleanup'),
      compress_old_messages: getToggle('mp-compress-old')
    },
    delivery: {
      require_acknowledgment: getToggle('mp-require-ack'),
      offline_queue_enabled: getToggle('mp-offline-queue'),
      max_queue_size: parseInt(getFieldValue('mp-max-queue-size')),
      resend_on_reconnect: getToggle('mp-resend-reconnect')
    },
    events: {
      event_logging_enabled: getToggle('mp-event-logging'),
      event_retention_days: parseInt(getFieldValue('mp-event-retention'))
    }
  };
}

function buildChatConfig() {
  return {
    messages: {
      max_message_length: parseInt(getFieldValue('chat-max-length')),
      history_retention_days: parseInt(getFieldValue('chat-history-retention')),
      enable_editing: getToggle('chat-enable-editing'),
      edit_time_limit_mins: parseInt(getFieldValue('chat-edit-time-limit')),
      enable_deletion: getToggle('chat-enable-deletion')
    },
    storage: {
      database_path: getFieldValue('chat-database-path'),
      fts_enabled: getToggle('chat-fts-enabled'),
      auto_archive_days: parseInt(getFieldValue('chat-auto-archive')),
      search_history_days: parseInt(getFieldValue('chat-search-history'))
    },
    maestro: {
      enabled: getToggle('maestro-enabled'),
      default_mode: getFieldValue('maestro-mode'),
      ollama_model: getFieldValue('maestro-model'),
      temperature: parseFloat(getFieldValue('maestro-temperature')),
      max_tokens: parseInt(getFieldValue('maestro-max-tokens'))
    },
    features: {
      typing_indicators: getToggle('chat-typing-indicators'),
      read_receipts: getToggle('chat-read-receipts'),
      reactions_enabled: getToggle('chat-reactions'),
      threads_enabled: getToggle('chat-threads')
    }
  };
}

function buildDatabaseConfig() {
  return {
    sqlite: buildDatabaseSQLiteConfig(),
    fts: buildDatabaseFTSConfig(),
    connection_pool: buildDatabaseConnectionPoolConfig(),
    maintenance: buildDatabaseMaintenanceConfig(),
    backups: buildDatabaseBackupConfig()
  };
}

function buildDevelopmentConfig() {
  return {
    logging: {
      level: getFieldValue('dev-log-level'),
      log_to_file: getToggle('dev-log-to-file'),
      log_path: getFieldValue('dev-log-path'),
      max_log_size_mb: parseInt(getFieldValue('dev-max-log-size'))
    },
    hot_reload: {
      enabled: getToggle('dev-hot-reload'),
      delay_ms: parseInt(getFieldValue('dev-reload-delay'))
    },
    testing: {
      mock_p2p_connections: getToggle('dev-mock-p2p'),
      mock_llm_responses: getToggle('dev-mock-llm'),
      debug_ui_events: getToggle('dev-debug-ui'),
      verbose_error_messages: getToggle('dev-verbose-errors')
    }
  };
}

