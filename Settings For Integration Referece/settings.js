// Settings Page JavaScript - Task 4.6
// Pattern Bible: No JavaScript state storage, all state in Rust
const { invoke } = window.__TAURI__;

// Load configuration from Rust backend
async function loadSettings() {
  try {
    const c = await invoke('config_get');
    document.getElementById('config-path').textContent = await invoke('config_get_path');

    loadNetworkSettings(c);
    loadSecuritySettings(c);
    loadUISettings(c);
  } catch (e) {
    showSettingsError('Failed to load settings: ' + e);
  }
}

// Save configuration changes
async function saveSettings() {
  try {
    if (!validateNetworkSettings() || !validateSecuritySettings() || !validateUISettings()) return;

    await invoke('config_update_network', { network: buildNetworkConfig() });
    await invoke('config_update_security', { security: buildSecurityConfig() });
    await invoke('config_update_ui', { ui: buildUIConfig() });

    showSettingsSuccess('Settings saved successfully');
  } catch (e) {
    showSettingsError('Failed to save settings: ' + e);
  }
}

// Reset configuration to defaults
async function resetBasicToDefaults() {
  if (!confirm('Reset all settings to defaults? This cannot be undone.')) return;
  try { await invoke('config_reset_to_defaults'); await loadSettings(); showSettingsSuccess('Settings reset to defaults'); }
  catch (e) { showSettingsError('Failed to reset settings: ' + e); }
}

// Restore configuration from backup
async function restoreBackup() {
  if (!confirm('Restore settings from backup? Current settings will be overwritten.')) return;
  try { await invoke('config_restore_backup'); await loadSettings(); showSettingsSuccess('Settings restored from backup'); }
  catch (e) { showSettingsError('Failed to restore backup: ' + e); }
}

// Export configuration as JSON
async function exportConfig() {
  try {
    const json = JSON.stringify(await invoke('config_get'), null, 2);
    const url = URL.createObjectURL(new Blob([json], { type: 'application/json' }));
    const a = document.createElement('a');
    a.href = url; a.download = `jfdi-config-export-${Date.now()}.json`; a.click();
    URL.revokeObjectURL(url);
    showSettingsSuccess('Configuration exported');
  } catch (e) { showSettingsError('Failed to export configuration: ' + e); }
}

// Import configuration from JSON file
async function importConfig(event) {
  const file = event.target.files[0];
  if (!file) return;
  try {
    const c = JSON.parse(await file.text());
    await invoke('config_update_network', { network: c.network });
    await invoke('config_update_security', { security: c.security });
    await invoke('config_update_ui', { ui: c.ui });
    await loadSettings();
    showSettingsSuccess('Configuration imported successfully');
  } catch (e) { showSettingsError('Failed to import configuration: ' + e); }
}

// Validate network settings
function validateNetworkSettings() {
  const mp = getSlider('max-peers'), di = getNumber('discovery-interval'), url = getValue('relay-url');
  if (mp < 1 || mp > 1000) { showSettingsError('Max peers must be between 1 and 1000'); return false; }
  if (di <= 0) { showSettingsError('Discovery interval must be greater than 0'); return false; }
  if (url && !url.match(/^wss?:\/\/.+/)) { showSettingsError('Relay URL must start with ws:// or wss://'); return false; }
  return true;
}

// Validate security settings
function validateSecuritySettings() {
  const st = getNumber('session-timeout'), md = getNumber('max-devices'), pl = getNumber('pairing-code-length');
  if (st <= 0) { showSettingsError('Session timeout must be greater than 0'); return false; }
  if (md <= 0) { showSettingsError('Max devices must be greater than 0'); return false; }
  if (pl < 4) { showSettingsError('Pairing code length must be at least 4'); return false; }
  return true;
}

// Validate UI settings
function validateUISettings() {
  const fs = getSlider('font-size'), ac = getValue('accent-color'), tm = getValue('theme-mode');
  if (fs < 8 || fs > 32) { showSettingsError('Font size must be between 8 and 32'); return false; }
  if (!ac.match(/^#[0-9a-fA-F]{6}$/)) { showSettingsError('Accent color must be a valid hex color'); return false; }
  if (tm !== 'dark' && tm !== 'light') { showSettingsError('Theme mode must be dark or light'); return false; }
  return true;
}

// Apply theme preview
function applyThemePreview() {
  document.documentElement.style.setProperty('--vio', getValue('accent-color'));
  document.body.style.fontSize = getSlider('font-size') + 'px';
}

// Show success/error messages
/**
 * Show success message (settings page specific)
 * Pattern Bible: Renamed for clarity and consistency
 */
function showSettingsSuccess(msg) {
  const el = document.getElementById('message');
  el.textContent = msg; el.className = 'message success show';
  setTimeout(() => el.classList.remove('show'), 3000);
}

/**
 * Show error message (settings page specific)
 * Pattern Bible: Renamed to avoid collision with global showError()
 */
function showSettingsError(msg) {
  const el = document.getElementById('message');
  el.textContent = msg; el.className = 'message error show';
}

// Helper functions
const $ = id => document.getElementById(id);
const setToggle = (id, v) => $(id).classList.toggle('active', v);
const getToggle = id => $(id).classList.contains('active');
const setSlider = (id, v) => { $(id).value = v; $(id + '-value').textContent = v + (id === 'font-size' ? 'pt' : ''); };
const getSlider = id => parseInt($(id).value);
const setValue = (id, v) => $(id).value = v;
const getValue = id => $(id).value;
const getNumber = id => parseInt(getValue(id));
const setColor = (id, v) => { setValue(id, v); $('accent-preview').style.background = v; $('accent-picker').value = v; };

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
  loadSettings();
  $('save-btn').addEventListener('click', saveSettings);
  $('reset-btn').addEventListener('click', resetToDefaults);
  $('restore-btn').addEventListener('click', restoreBackup);
  $('export-btn').addEventListener('click', exportConfig);
  $('import-file').addEventListener('change', importConfig);

  document.querySelectorAll('.toggle').forEach(el => el.addEventListener('click', () => el.classList.toggle('active')));
  document.querySelectorAll('input[type="range"]').forEach(el => el.addEventListener('input', () => {
    $(el.id + '-value').textContent = el.value + (el.id === 'font-size' ? 'pt' : '');
    if (el.id === 'font-size') applyThemePreview();
  }));

  $('accent-color').addEventListener('input', e => {
    $('accent-preview').style.background = e.target.value;
    $('accent-picker').value = e.target.value;
    applyThemePreview();
  });
  $('accent-picker').addEventListener('input', e => {
    $('accent-color').value = e.target.value;
    $('accent-preview').style.background = e.target.value;
    applyThemePreview();
  });
  $('accent-preview').addEventListener('click', () => $('accent-picker').click());
});

