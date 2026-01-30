use super::super::webrtc::WebRtcConfig;
use serde::{Deserialize, Serialize};
use std::time::Duration;

/// Network configuration for P2P networking
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NetworkConfig {
    // Connection settings
    pub max_peers: usize,
    pub connection_timeout: Duration,
    pub ping_interval: Duration,
    pub reconnect_interval: Duration,

    // Discovery settings
    pub enable_mdns: bool,
    pub enable_dht: bool,
    pub bootstrap_peers: Vec<String>,
    pub mdns_query_interval: Duration,
    pub dht_replication_factor: usize,

    // Relay settings
    pub relay_url: Option<String>,
    pub use_relay_fallback: bool,
    pub relay_timeout: Duration,

    // NAT traversal
    pub stun_servers: Vec<String>,
    pub turn_servers: Vec<TurnServer>,
    pub ice_timeout: Duration,

    // Security
    pub require_encryption: bool,
    pub allowed_protocols: Vec<String>,
    pub max_message_size: usize,

    // Performance
    pub buffer_size: usize,
    pub max_concurrent_connections: usize,
    pub connection_pool_size: usize,

    // WebRTC settings
    pub enable_webrtc: bool,
    pub webrtc_data_channels: usize,
    pub webrtc_ordered_delivery: bool,
    pub webrtc_max_retransmits: Option<u16>,
}

/// TURN server configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TurnServer {
    pub url: String,
    pub username: String,
    pub credential: String,
}

impl Default for NetworkConfig {
    fn default() -> Self {
        let mut config = Self::default_connection_settings();
        config.apply_discovery_settings();
        config.apply_relay_settings();
        config.apply_nat_settings();
        config.apply_security_settings();
        config.apply_performance_settings();
        config
    }
}

impl NetworkConfig {
    /// Default bootstrap peers
    fn default_bootstrap_peers() -> Vec<String> {
        super::defaults::bootstrap_peers()
    }

    /// Default STUN servers
    fn default_stun_servers() -> Vec<String> {
        super::defaults::stun_servers()
    }

    /// Default protocols
    fn default_protocols() -> Vec<String> {
        super::defaults::protocols()
    }

    /// Create config with default connection settings
    fn default_connection_settings() -> Self {
        Self {
            max_peers: 50,
            connection_timeout: Duration::from_secs(30),
            ping_interval: Duration::from_secs(30),
            reconnect_interval: Duration::from_secs(60),
            enable_mdns: false,
            enable_dht: false,
            bootstrap_peers: vec![],
            mdns_query_interval: Duration::from_secs(5),
            dht_replication_factor: 20,
            relay_url: None,
            use_relay_fallback: false,
            relay_timeout: Duration::from_secs(10),
            stun_servers: vec![],
            turn_servers: vec![],
            ice_timeout: Duration::from_secs(30),
            require_encryption: true,
            allowed_protocols: vec![],
            max_message_size: 1024 * 1024,
            buffer_size: 64 * 1024,
            max_concurrent_connections: 100,
            connection_pool_size: 10,
            enable_webrtc: true,
            webrtc_data_channels: 16,
            webrtc_ordered_delivery: true,
            webrtc_max_retransmits: Some(3),
        }
    }

    /// Apply discovery settings
    fn apply_discovery_settings(&mut self) {
        self.enable_mdns = true;
        self.enable_dht = true;
        self.bootstrap_peers = Self::default_bootstrap_peers();
    }

    /// Apply relay settings
    fn apply_relay_settings(&mut self) {
        self.relay_url = Some("ws://localhost:8080".to_string());
        self.use_relay_fallback = true;
    }

    /// Apply NAT traversal settings
    fn apply_nat_settings(&mut self) {
        self.stun_servers = Self::default_stun_servers();
    }

    /// Apply security settings
    fn apply_security_settings(&mut self) {
        self.allowed_protocols = Self::default_protocols();
    }

    /// Apply performance settings
    fn apply_performance_settings(&mut self) {
        // Performance settings already set in default_connection_settings
    }
    /// Create development configuration
    pub fn development() -> Self {
        let mut config = Self::default();
        config.max_peers = 10;
        config.bootstrap_peers = vec![];
        config.relay_url = Some("ws://localhost:8080".to_string());
        config
    }

    /// Create production configuration
    pub fn production() -> Self {
        let mut config = Self::default();
        config.relay_url = Some("wss://relay.jfdi.app".to_string());
        config.turn_servers = vec![TurnServer {
            url: "turn:turn.jfdi.app:3478".to_string(),
            username: "jfdi".to_string(),
            credential: "production-secret".to_string(),
        }];
        config
    }

    /// Validate configuration
    pub fn validate(&self) -> Result<(), String> {
        super::validation::validate_network_config(self)
    }

    /// Get effective bootstrap peers
    pub fn effective_bootstrap_peers(&self) -> Vec<String> {
        super::helpers::effective_bootstrap_peers(self)
    }

    /// Convert to WebRTC configuration
    pub fn to_webrtc_config(&self) -> WebRtcConfig {
        super::webrtc::create_webrtc_config_from_network(self)
    }
}
