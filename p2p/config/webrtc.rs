use super::super::webrtc::{
    config::{IceCredentialType, IceServer},
    WebRtcConfig,
};
use super::network::{NetworkConfig, TurnServer};
use std::time::Duration;

/// Create WebRTC configuration from NetworkConfig
pub fn create_webrtc_config_from_network(config: &NetworkConfig) -> WebRtcConfig {
    let ice_servers = create_ice_servers_from_network(config);

    WebRtcConfig {
        ice_servers,
        ice_gathering_timeout: Duration::from_secs(10),
        ice_connection_timeout: config.ice_timeout,
        ice_restart_timeout: Duration::from_secs(5),
        max_data_channels: config.webrtc_data_channels,
        data_channel_buffer_size: config.buffer_size,
        ordered_delivery: config.webrtc_ordered_delivery,
        max_retransmits: config.webrtc_max_retransmits,
        max_packet_lifetime: Some(Duration::from_secs(3)),
        connection_timeout: config.connection_timeout,
        keep_alive_interval: Duration::from_secs(25),
        max_message_size: config.max_message_size,
        dtls_fingerprint_algorithm: "sha-256".to_string(),
        enable_dtls_srtp: true,
        bandwidth_limit: None,
        cpu_adaptation: true,
        network_adaptation: true,
    }
}

/// Create ICE servers from STUN/TURN configuration
fn create_ice_servers_from_network(config: &NetworkConfig) -> Vec<IceServer> {
    let mut ice_servers = Vec::new();

    // Add STUN servers
    for stun_url in &config.stun_servers {
        ice_servers.push(IceServer {
            urls: vec![stun_url.clone()],
            username: None,
            credential: None,
            credential_type: IceCredentialType::Password,
        });
    }

    // Add TURN servers
    for turn_server in &config.turn_servers {
        ice_servers.push(create_ice_server_from_turn(turn_server));
    }

    // Add default STUN server if none configured
    if ice_servers.is_empty() {
        ice_servers.push(create_default_stun_server());
    }

    ice_servers
}

/// Create ICE server from TURN server configuration
fn create_ice_server_from_turn(turn_server: &TurnServer) -> IceServer {
    IceServer {
        urls: vec![turn_server.url.clone()],
        username: Some(turn_server.username.clone()),
        credential: Some(turn_server.credential.clone()),
        credential_type: IceCredentialType::Password,
    }
}

/// Create default STUN server
fn create_default_stun_server() -> IceServer {
    IceServer {
        urls: vec!["stun:stun.l.google.com:19302".to_string()],
        username: None,
        credential: None,
        credential_type: IceCredentialType::Password,
    }
}
