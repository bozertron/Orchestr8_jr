pub mod builder;
pub mod connection;

pub use builder::TransportBuilder;
pub use connection::{ConnectionInfo, TransportStats};

use crate::p2p::NetworkConfig;
use libp2p::{core::upgrade, identity::Keypair, noise, tcp, websocket, yamux, PeerId, Transport};

/// P2P transport layer
pub struct P2PTransport {
    pub(crate) keypair: Keypair,
    pub(crate) peer_id: PeerId,
    pub(crate) config: NetworkConfig,
}

impl P2PTransport {
    /// Create new transport
    pub async fn new(config: &NetworkConfig) -> Result<Self, String> {
        let keypair = Keypair::generate_ed25519();
        let peer_id = PeerId::from(keypair.public());

        Ok(Self {
            keypair,
            peer_id,
            config: config.clone(),
        })
    }

    /// Start transport
    pub async fn start(&mut self) -> Result<(), String> {
        // Transport will be started by the swarm
        Ok(())
    }

    /// Stop transport
    pub async fn stop(&mut self) -> Result<(), String> {
        // Transport will be stopped by the swarm
        Ok(())
    }

    /// Get peer ID
    pub fn peer_id(&self) -> PeerId {
        self.peer_id
    }

    /// Get keypair
    pub fn keypair(&self) -> &Keypair {
        &self.keypair
    }

    /// Build transport stack
    pub fn build_transport(
        &self,
    ) -> Result<
        libp2p::core::transport::Boxed<(PeerId, libp2p::core::muxing::StreamMuxerBox)>,
        String,
    > {
        // Create TCP transport
        let tcp_transport = tcp::tokio::Transport::new(tcp::Config::default().nodelay(true));

        // Create WebSocket transport - create a new TCP transport for WebSocket
        let tcp_for_ws = tcp::tokio::Transport::new(tcp::Config::default().nodelay(true));
        let ws_transport = websocket::WsConfig::new(tcp_for_ws);

        // Combine transports
        let transport = tcp_transport
            .or_transport(ws_transport)
            .upgrade(upgrade::Version::V1)
            .authenticate(self.create_noise_config()?)
            .multiplex(self.create_yamux_config())
            .timeout(self.config.connection_timeout)
            .boxed();

        Ok(transport)
    }

    /// Create Noise authentication config
    fn create_noise_config(&self) -> Result<noise::Config, String> {
        let noise_config = noise::Config::new(&self.keypair).map_err(|e| {
            format!(
                "Transport: {}",
                format!("Failed to create noise config: {}", e)
            )
        })?;

        Ok(noise_config)
    }

    /// Create Yamux multiplexing config
    fn create_yamux_config(&self) -> yamux::Config {
        yamux::Config::default()
    }

    /// Validate transport configuration
    pub fn validate_config(&self) -> Result<(), String> {
        if self.config.connection_timeout.as_secs() == 0 {
            return Err("Connection timeout must be greater than 0".to_string());
        }

        if self.config.buffer_size == 0 {
            return Err("Buffer size must be greater than 0".to_string());
        }

        if self.config.max_concurrent_connections == 0 {
            return Err("Max concurrent connections must be greater than 0".to_string());
        }

        Ok(())
    }

    /// Get transport statistics
    pub async fn transport_stats(&self) -> TransportStats {
        TransportStats {
            peer_id: self.peer_id,
            active_connections: 0,  // Would be tracked by swarm
            pending_connections: 0, // Would be tracked by swarm
            bytes_sent: 0,          // Would be tracked by swarm
            bytes_received: 0,      // Would be tracked by swarm
        }
    }

    /// Check if transport is connected
    pub fn is_connected(&self) -> bool {
        // Transport is considered connected if it's been initialized
        // In real implementation, would check swarm connection status
        true
    }

    /// Create transport for testing
    pub fn new_for_testing() -> Self {
        let keypair = Keypair::generate_ed25519();
        let peer_id = PeerId::from(keypair.public());
        Self {
            keypair,
            peer_id,
            config: NetworkConfig::default(),
        }
    }
}
