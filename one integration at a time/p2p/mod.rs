pub mod config;
pub mod discovery;
pub mod errors;
pub mod events;
pub mod integration;
pub mod lifecycle;
pub mod manager;
pub mod message;
pub mod service;
pub mod transport;
pub mod webrtc;

pub use config::NetworkConfig;
pub use discovery::{Discovery, DiscoveryEvent};
pub use manager::{PeerConnection, PeerManager};
pub use message::{MessageConfig, MessageEvent, MessageService, P2PMessage};
pub use service::{HealthStatus, LifecycleState, P2PService};
pub use transport::P2PTransport;
pub use webrtc::{WebRtcConfig, WebRtcEvent, WebRtcService};

// Import PeerOperations trait for trait methods to be available on PeerManager
use crate::p2p::manager::peer_ops::PeerOperations;

use libp2p::{Multiaddr, PeerId};
use std::collections::HashMap;
use tokio::sync::mpsc;

/// Main P2P network service
pub struct P2PNetwork {
    peer_manager: PeerManager,
    discovery: Discovery,
    transport: P2PTransport,
    webrtc_service: Option<webrtc::WebRtcService>,
    config: NetworkConfig,
    event_sender: mpsc::UnboundedSender<P2PEvent>,
}

/// P2P network events
#[derive(Debug, Clone)]
pub enum P2PEvent {
    PeerDiscovered { peer_id: PeerId, addr: Multiaddr },
    PeerConnected { peer_id: PeerId },
    PeerDisconnected { peer_id: PeerId },
    MessageReceived { from: PeerId, data: Vec<u8> },
    ConnectionFailed { peer_id: PeerId, error: String },
    MaintenanceSummary(String),
}

impl P2PNetwork {
    /// Create new P2P network instance
    pub async fn new(
        config: NetworkConfig,
    ) -> Result<(Self, mpsc::UnboundedReceiver<P2PEvent>), String> {
        let (event_sender, event_receiver) = mpsc::unbounded_channel();

        let transport = P2PTransport::new(&config).await?;
        let discovery = Discovery::new(&config, event_sender.clone()).await?;
        let peer_manager = PeerManager::new(&config, event_sender.clone()).await?;

        // Initialize WebRTC service if enabled
        let webrtc_service = if config.enable_webrtc {
            let webrtc_config = config.to_webrtc_config();
            let (service, _webrtc_receiver) = webrtc::WebRtcService::new(webrtc_config).await?;
            Some(service)
        } else {
            None
        };

        Ok((
            Self {
                peer_manager,
                discovery,
                transport,
                webrtc_service,
                config,
                event_sender,
            },
            event_receiver,
        ))
    }

    /// Start the P2P network
    pub async fn start(&mut self) -> Result<(), String> {
        self.transport.start().await?;
        self.discovery.start().await?;
        self.peer_manager.start().await?;

        // Start WebRTC service if enabled
        if let Some(ref mut webrtc_service) = self.webrtc_service {
            webrtc_service.start().await?;
        }

        Ok(())
    }

    /// Stop the P2P network
    pub async fn stop(&mut self) -> Result<(), String> {
        self.peer_manager.stop().await?;
        self.discovery.stop().await?;
        self.transport.stop().await?;
        Ok(())
    }

    /// Connect to a specific peer
    pub async fn connect_peer(&mut self, peer_id: PeerId, addr: Multiaddr) -> Result<(), String> {
        self.peer_manager.connect_peer(peer_id, addr).await
    }

    /// Send message to peer
    pub async fn send_message(&mut self, peer_id: PeerId, data: Vec<u8>) -> Result<(), String> {
        self.peer_manager.send_message(peer_id, data).await
    }

    /// Get connected peers
    pub async fn connected_peers(&self) -> HashMap<PeerId, PeerConnection> {
        self.peer_manager.connected_peers().await
    }

    /// Get network statistics
    pub async fn network_stats(&self) -> NetworkStats {
        NetworkStats {
            connected_peers: self.peer_manager.peer_count().await,
            discovered_peers: self.discovery.discovered_count().await,
            bytes_sent: self.peer_manager.bytes_sent().await,
            bytes_received: self.peer_manager.bytes_received().await,
        }
    }

    /// Create WebRTC connection to peer
    pub async fn create_webrtc_connection(&mut self, peer_id: PeerId) -> Result<(), String> {
        if let Some(ref mut webrtc_service) = self.webrtc_service {
            webrtc_service.create_connection(peer_id).await
        } else {
            Err(format!("Config: {}", "WebRTC not enabled".to_string()))
        }
    }

    /// Send data via WebRTC
    pub async fn send_webrtc_data(
        &mut self,
        peer_id: PeerId,
        channel_id: String,
        data: Vec<u8>,
    ) -> Result<(), String> {
        if let Some(ref mut webrtc_service) = self.webrtc_service {
            webrtc_service.send_data(peer_id, channel_id, data).await
        } else {
            Err(format!("Config: {}", "WebRTC not enabled".to_string()))
        }
    }

    /// Get WebRTC service reference
    pub fn webrtc_service(&self) -> Option<&webrtc::WebRtcService> {
        self.webrtc_service.as_ref()
    }

    /// Get network configuration reference
    pub fn network_config(&self) -> &NetworkConfig {
        &self.config
    }

    /// Forward event to external listeners (push architecture)
    pub fn forward_event(&self, event: P2PEvent) -> Result<(), String> {
        self.event_sender
            .send(event)
            .map_err(|_| format!("Connection: {}", "Channel closed".to_string()))
    }

    /// Send network startup event (lifecycle event emission)
    pub fn emit_startup_event(&self) -> Result<(), String> {
        self.forward_event(P2PEvent::MaintenanceSummary(
            "P2P Network started successfully".to_string(),
        ))
    }

    /// Send network shutdown event (lifecycle event emission)
    pub fn emit_shutdown_event(&self) -> Result<(), String> {
        self.forward_event(P2PEvent::MaintenanceSummary(
            "P2P Network stopped".to_string(),
        ))
    }
}

/// Network statistics
#[derive(Debug, Clone)]
pub struct NetworkStats {
    pub connected_peers: usize,
    pub discovered_peers: usize,
    pub bytes_sent: u64,
    pub bytes_received: u64,
}

// Re-export error types from errors module
pub use errors::P2PError;
