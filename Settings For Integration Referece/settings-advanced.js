// Advanced Settings JavaScript (Task 4.6)
// Pattern Bible Compliance: No JavaScript state storage, all state in Rust

const { invoke } = window.__TAURI__.tauri;

// Show message helper
function showMessage(text, type = 'success') {
  const messageEl = document.getElementById('message');
  messageEl.textContent = text;
  messageEl.className = `message ${type} show`;
  setTimeout(() => messageEl.classList.remove('show'), 5000);
}

// Load configuration from Rust
async function loadConfig() {
  try {
    const [messageProtocol, chat, database, development] = await Promise.all([
      invoke('config_get_message_protocol'),
      invoke('config_get_chat'),
      invoke('config_get_database'),
      invoke('config_get_development')
    ]);

    // Load Message Protocol settings
    loadMessageProtocolConfig(messageProtocol);
    
    // Load Chat settings
    loadChatConfig(chat);
    
    // Load Database settings
    loadDatabaseConfig(database);
    
    // Load Development settings
    loadDevelopmentConfig(development);

  } catch (error) {
    showMessage(`Failed to load configuration: ${error}`, 'error');
    console.error('Load config error:', error);
  }
}

// Note: Load/build config functions are in settings_advanced_helpers.js

// Save configuration to Rust
async function saveConfig() {
  try {
    // Build configuration objects
    const messageProtocol = buildMessageProtocolConfig();
    const chat = buildChatConfig();
    const database = buildDatabaseConfig();
    const development = buildDevelopmentConfig();

    // Save all configurations
    await Promise.all([
      invoke('config_update_message_protocol', { messageProtocol }),
      invoke('config_update_chat', { chat }),
      invoke('config_update_database', { database }),
      invoke('config_update_development', { development })
    ]);

    showMessage('Advanced settings saved successfully!', 'success');
  } catch (error) {
    showMessage(`Failed to save settings: ${error}`, 'error');
    console.error('Save config error:', error);
  }
}

// Note: Build config and utility functions are in settings_advanced_helpers.js

/**
 * Reset advanced settings to defaults
 * Pattern Bible: Renamed to avoid collision with resetBasicToDefaults() in settings.js
 */
async function resetAdvancedToDefaults() {
  if (!confirm('Reset all advanced settings to defaults? This cannot be undone.')) return;

  try {
    await invoke('config_reset_to_defaults');
    await loadConfig();
    showMessage('Settings reset to defaults', 'success');
  } catch (error) {
    showMessage(`Failed to reset: ${error}`, 'error');
  }
}

// Restore from backup
async function restoreFromBackup() {
  if (!confirm('Restore configuration from backup? Current settings will be lost.')) return;
  
  try {
    await invoke('config_restore_backup');
    await loadConfig();
    showMessage('Configuration restored from backup', 'success');
  } catch (error) {
    showMessage(`Failed to restore: ${error}`, 'error');
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  // Load configuration
  loadConfig();

  // Setup toggle click handlers
  document.querySelectorAll('.toggle').forEach(toggle => {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('active');
    });
  });

  // Setup button handlers
  document.getElementById('save-btn').addEventListener('click', saveConfig);
  document.getElementById('reset-btn').addEventListener('click', resetToDefaults);
  document.getElementById('restore-btn').addEventListener('click', restoreFromBackup);
});

