/**
 * Settings Helper Functions
 * Pattern Bible: Helper functions for loading/saving configuration sections
 */

// ============================================================================
// LOAD SETTINGS HELPERS
// ============================================================================

function loadNetworkSettings(c) {
  setToggle('p2p-enabled', c.network.p2p.enabled);
  setSlider('max-peers', c.network.p2p.max_peers);
  setValue('discovery-interval', c.network.p2p.discovery_interval_secs);
  setValue('connection-timeout', c.network.p2p.connection_timeout_secs);
  setValue('relay-url', c.network.relay.server_url);
  setValue('stun-servers', c.network.webrtc.stun_servers.join('\n'));
  
  // Network expansion
  setToggle('mdns-enabled', c.network.p2p.mdns_enabled);
  setToggle('kad-enabled', c.network.p2p.kad_enabled);
  setValue('max-idle-time', c.network.p2p.max_idle_time_secs);
  setValue('keep-alive-interval', c.network.p2p.keep_alive_interval_secs);
  setValue('transport-protocol', c.network.transport.protocol);
  setValue('buffer-size', c.network.transport.buffer_size_kb);
  setValue('max-frame-size', c.network.transport.max_frame_size_kb);
  setToggle('compression-enabled', c.network.transport.compression_enabled);
  setToggle('tcp-nodelay', c.network.transport.tcp_nodelay);
}

function loadSecuritySettings(c) {
  setToggle('encryption-enabled', c.security.encryption.enabled);
  setValue('session-timeout', c.security.auth.session_timeout_days);
  setValue('max-devices', c.security.auth.max_devices_per_user);
  setValue('pairing-code-length', c.security.auth.pairing_code_length);
  setValue('pairing-expiry', c.security.auth.pairing_code_expiry_mins);
  setToggle('use-keyring', c.security.keys.use_platform_keyring);
  
  // Security expansion
  setToggle('per-message-encryption', c.security.encryption.per_message_encryption);
  setValue('group-key-rotation', c.security.encryption.group_key_rotation_days);
  setValue('key-storage-path', c.security.encryption.key_storage_path);
  setValue('device-name', c.security.authentication.device_name);
  setToggle('auto-pair-trusted', c.security.authentication.auto_pair_trusted_devices);
  setToggle('session-persistence', c.security.authentication.session_persistence);
  setToggle('signing-enabled', c.security.signing.enabled);
  setToggle('verify-all-messages', c.security.signing.verify_all_messages);
  setValue('signature-algorithm', c.security.signing.signature_algorithm);
  setToggle('trust-on-first-use', c.security.signing.trust_on_first_use);
}

function loadUISettings(c) {
  setValue('theme-mode', c.ui.theme.mode);
  setColor('accent-color', c.ui.theme.accent_color);
  setSlider('font-size', c.ui.theme.font_size);
  setValue('language', c.ui.language.locale);
  setValue('time-format', c.ui.language.time_format);
  setToggle('notifications-enabled', c.ui.notifications.enabled);
  setToggle('notification-sound', c.ui.notifications.sound_enabled);
  setToggle('show-previews', c.ui.notifications.show_previews);
  
  // UI expansion
  setValue('sidebar-width', c.ui.layout.sidebar_width);
  setValue('message-density', c.ui.layout.message_density);
  setToggle('show-timestamps', c.ui.layout.show_timestamps);
  setToggle('show-avatars', c.ui.layout.show_avatars);
  setToggle('auto-scroll', c.ui.behavior.auto_scroll_on_new_message);
  setToggle('focus-input-on-send', c.ui.behavior.focus_input_on_send);
}

// ============================================================================
// SAVE SETTINGS HELPERS
// ============================================================================

function buildP2PConfig() {
  return {
    enabled: getToggle('p2p-enabled'),
    listen_port: 0,
    max_peers: getSlider('max-peers'),
    discovery_interval_secs: getNumber('discovery-interval'),
    connection_timeout_secs: getNumber('connection-timeout'),
    mdns_enabled: getToggle('mdns-enabled'),
    kad_enabled: getToggle('kad-enabled'),
    discovery_methods: [],
    bootstrap_peers: [],
    max_idle_time_secs: getNumber('max-idle-time'),
    keep_alive_interval_secs: getNumber('keep-alive-interval')
  };
}

function buildRelayConfig() {
  return {
    enabled: true,
    server_url: getValue('relay-url'),
    fallback_urls: [],
    reconnect_interval_secs: 5
  };
}

function buildWebRTCConfig() {
  return {
    enabled: true,
    stun_servers: getValue('stun-servers').split('\n').filter(s => s.trim()),
    turn_servers: [],
    ice_timeout_secs: 30
  };
}

function buildTransportConfig() {
  return {
    protocol: getValue('transport-protocol'),
    buffer_size_kb: getNumber('buffer-size'),
    max_frame_size_kb: getNumber('max-frame-size'),
    compression_enabled: getToggle('compression-enabled'),
    tcp_nodelay: getToggle('tcp-nodelay')
  };
}

function buildNetworkConfig() {
  return {
    p2p: buildP2PConfig(),
    relay: buildRelayConfig(),
    webrtc: buildWebRTCConfig(),
    transport: buildTransportConfig()
  };
}

function buildEncryptionConfig() {
  return {
    enabled: getToggle('encryption-enabled'),
    algorithm: 'ChaCha20-Poly1305',
    key_rotation_days: 90,
    per_message_encryption: getToggle('per-message-encryption'),
    group_key_rotation_days: getNumber('group-key-rotation'),
    key_storage_path: getValue('key-storage-path')
  };
}

function buildAuthenticationConfig() {
  return {
    session_timeout_days: getNumber('session-timeout'),
    max_devices_per_user: getNumber('max-devices'),
    pairing_code_length: getNumber('pairing-code-length'),
    pairing_code_expiry_mins: getNumber('pairing-expiry'),
    device_name: getValue('device-name'),
    auto_pair_trusted_devices: getToggle('auto-pair-trusted'),
    session_persistence: getToggle('session-persistence')
  };
}

function buildSecurityConfig() {
  return {
    encryption: buildEncryptionConfig(),
    authentication: buildAuthenticationConfig(),
    keys: {
      use_platform_keyring: getToggle('use-keyring'),
      key_derivation_iterations: 100000
    },
    signing: {
      enabled: getToggle('signing-enabled'),
      verify_all_messages: getToggle('verify-all-messages'),
      signature_algorithm: getValue('signature-algorithm'),
      trust_on_first_use: getToggle('trust-on-first-use')
    }
  };
}

// Note: buildNotificationsConfig() and buildUIConfig() moved to settings_helpers_ui.js

