pub mod config;
pub mod connection;
pub mod data_channel;
pub mod manager;

pub use config::WebRtcConfig;
pub use connection::{ConnectionState, WebRtcConnection};
pub use data_channel::{DataChannel, DataChannelEvent};
pub use manager::WebRtcManager;

use libp2p::PeerId;
use std::collections::HashMap;
use tokio::sync::mpsc;

/// WebRTC-specific events
#[derive(Debug, Clone)]
pub enum WebRtcEvent {
    ConnectionEstablished {
        peer_id: PeerId,
    },
    ConnectionFailed {
        peer_id: PeerId,
        error: String,
    },
    ConnectionClosed {
        peer_id: PeerId,
    },
    DataChannelOpened {
        peer_id: PeerId,
        channel_id: String,
    },
    DataChannelClosed {
        peer_id: PeerId,
        channel_id: String,
    },
    MessageReceived {
        peer_id: PeerId,
        channel_id: String,
        data: Vec<u8>,
    },
    IceCandidateReceived {
        peer_id: PeerId,
        candidate: String,
    },
}

/// WebRTC service for real-time peer communication
pub struct WebRtcService {
    manager: WebRtcManager,
    config: WebRtcConfig,
    event_sender: mpsc::UnboundedSender<WebRtcEvent>,
}

impl WebRtcService {
    /// Create new WebRTC service
    pub async fn new(
        config: WebRtcConfig,
    ) -> Result<(Self, mpsc::UnboundedReceiver<WebRtcEvent>), String> {
        let (event_sender, event_receiver) = mpsc::unbounded_channel();
        let manager = WebRtcManager::new(&config, event_sender.clone()).await?;

        Ok((
            Self {
                manager,
                config,
                event_sender,
            },
            event_receiver,
        ))
    }

    /// Start WebRTC service
    pub async fn start(&mut self) -> Result<(), String> {
        self.manager.start().await
    }

    /// Stop WebRTC service
    pub async fn stop(&mut self) -> Result<(), String> {
        self.manager.stop().await
    }

    /// Create connection to peer
    pub async fn create_connection(&mut self, peer_id: PeerId) -> Result<(), String> {
        self.manager.create_connection(peer_id).await
    }

    /// Accept connection from peer
    pub async fn accept_connection(
        &mut self,
        peer_id: PeerId,
        offer: String,
    ) -> Result<String, String> {
        self.manager.accept_connection(peer_id, offer).await
    }

    /// Send data through data channel
    pub async fn send_data(
        &mut self,
        peer_id: PeerId,
        channel_id: String,
        data: Vec<u8>,
    ) -> Result<(), String> {
        self.manager.send_data(peer_id, channel_id, data).await
    }

    /// Get active connections
    pub async fn active_connections(&self) -> HashMap<PeerId, ConnectionState> {
        self.manager.active_connections().await
    }

    /// Get WebRTC statistics
    pub async fn webrtc_stats(&self) -> WebRtcStats {
        self.manager.webrtc_stats().await
    }

    /// Get service configuration reference
    pub fn service_config(&self) -> &WebRtcConfig {
        &self.config
    }

    /// Subscribe to WebRTC events (push-based architecture)
    pub fn subscribe_events(&self) -> mpsc::UnboundedReceiver<WebRtcEvent> {
        // For this implementation, return a channel that never receives events
        // Real implementation would use a broadcast or subscription model
        let (_tx, rx) = mpsc::unbounded_channel();
        rx
    }

    /// Forward event to external listeners (lifecycle events)
    pub fn emit_service_started(&self) -> Result<(), String> {
        self.event_sender
            .send(WebRtcEvent::ConnectionEstablished {
                peer_id: PeerId::random(), // Service-wide event
            })
            .map_err(|_| format!("Connection: {}", "Channel closed".to_string()))
    }

    /// Emit service lifecycle events
    pub fn emit_service_stopped(&self) -> Result<(), String> {
        self.event_sender
            .send(WebRtcEvent::ConnectionClosed {
                peer_id: PeerId::random(), // Service-wide event
            })
            .map_err(|_| format!("Connection: {}", "Channel closed".to_string()))
    }
}

/// WebRTC statistics
#[derive(Debug, Clone)]
pub struct WebRtcStats {
    pub active_connections: usize,
    pub data_channels_open: usize,
    pub bytes_sent: u64,
    pub bytes_received: u64,
    pub ice_candidates_gathered: u64,
    pub connection_failures: u64,
}
