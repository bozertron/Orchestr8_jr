use serde::{Deserialize, Serialize};
use std::time::Duration;

/// WebRTC configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WebRtcConfig {
    // ICE configuration
    pub ice_servers: Vec<IceServer>,
    pub ice_gathering_timeout: Duration,
    pub ice_connection_timeout: Duration,
    pub ice_restart_timeout: Duration,

    // Data channel configuration
    pub max_data_channels: usize,
    pub data_channel_buffer_size: usize,
    pub ordered_delivery: bool,
    pub max_retransmits: Option<u16>,
    pub max_packet_lifetime: Option<Duration>,

    // Connection configuration
    pub connection_timeout: Duration,
    pub keep_alive_interval: Duration,
    pub max_message_size: usize,

    // Security configuration
    pub dtls_fingerprint_algorithm: String,
    pub enable_dtls_srtp: bool,

    // Performance configuration
    pub bandwidth_limit: Option<u64>,
    pub cpu_adaptation: bool,
    pub network_adaptation: bool,
}

/// ICE server configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IceServer {
    pub urls: Vec<String>,
    pub username: Option<String>,
    pub credential: Option<String>,
    pub credential_type: IceCredentialType,
}

/// ICE credential types
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum IceCredentialType {
    Password,
    OAuth,
}

impl Default for WebRtcConfig {
    fn default() -> Self {
        let mut config = Self::default_ice_config();
        config.apply_data_channel_defaults();
        config.apply_connection_defaults();
        config.apply_security_defaults();
        config.apply_performance_defaults();
        config
    }
}

impl WebRtcConfig {
    /// Create default ICE configuration
    fn default_ice_config() -> Self {
        Self {
            ice_servers: vec![IceServer {
                urls: vec!["stun:stun.l.google.com:19302".to_string()],
                username: None,
                credential: None,
                credential_type: IceCredentialType::Password,
            }],
            ice_gathering_timeout: Duration::from_secs(10),
            ice_connection_timeout: Duration::from_secs(30),
            ice_restart_timeout: Duration::from_secs(5),

            // Initialize other fields with temporary values
            max_data_channels: 0,
            data_channel_buffer_size: 0,
            ordered_delivery: false,
            max_retransmits: None,
            max_packet_lifetime: None,
            connection_timeout: Duration::from_secs(0),
            keep_alive_interval: Duration::from_secs(0),
            max_message_size: 0,
            dtls_fingerprint_algorithm: String::new(),
            enable_dtls_srtp: false,
            bandwidth_limit: None,
            cpu_adaptation: false,
            network_adaptation: false,
        }
    }

    /// Apply data channel defaults
    fn apply_data_channel_defaults(&mut self) {
        self.max_data_channels = 16;
        self.data_channel_buffer_size = 64 * 1024; // 64KB
        self.ordered_delivery = true;
        self.max_retransmits = Some(3);
        self.max_packet_lifetime = Some(Duration::from_secs(3));
    }

    /// Apply connection defaults
    fn apply_connection_defaults(&mut self) {
        self.connection_timeout = Duration::from_secs(30);
        self.keep_alive_interval = Duration::from_secs(25);
        self.max_message_size = 1024 * 1024; // 1MB
    }

    /// Apply security defaults
    fn apply_security_defaults(&mut self) {
        self.dtls_fingerprint_algorithm = "sha-256".to_string();
        self.enable_dtls_srtp = true;
    }

    /// Apply performance defaults
    fn apply_performance_defaults(&mut self) {
        self.bandwidth_limit = None;
        self.cpu_adaptation = true;
        self.network_adaptation = true;
    }

    /// Create development configuration
    pub fn development() -> Self {
        let mut config = Self::default();
        config.ice_gathering_timeout = Duration::from_secs(5);
        config.ice_connection_timeout = Duration::from_secs(15);
        config.connection_timeout = Duration::from_secs(15);
        config
    }

    /// Create production configuration
    pub fn production() -> Self {
        let mut config = Self::default();
        config.ice_gathering_timeout = Duration::from_secs(15);
        config.ice_connection_timeout = Duration::from_secs(45);
        config.connection_timeout = Duration::from_secs(45);
        config.bandwidth_limit = Some(1_000_000); // 1Mbps
        config
    }

    /// Add STUN server
    pub fn add_stun_server(&mut self, url: String) {
        self.ice_servers.push(IceServer {
            urls: vec![url],
            username: None,
            credential: None,
            credential_type: IceCredentialType::Password,
        });
    }

    /// Add TURN server
    pub fn add_turn_server(&mut self, url: String, username: String, credential: String) {
        self.ice_servers.push(IceServer {
            urls: vec![url],
            username: Some(username),
            credential: Some(credential),
            credential_type: IceCredentialType::Password,
        });
    }

    /// Validate configuration
    pub fn validate(&self) -> Result<(), String> {
        if self.ice_servers.is_empty() {
            return Err("At least one ICE server must be configured".to_string());
        }

        if self.max_data_channels == 0 {
            return Err("Max data channels must be greater than 0".to_string());
        }

        if self.data_channel_buffer_size == 0 {
            return Err("Data channel buffer size must be greater than 0".to_string());
        }

        if self.max_message_size == 0 {
            return Err("Max message size must be greater than 0".to_string());
        }

        Ok(())
    }
}
