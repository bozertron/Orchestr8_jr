pub mod maintenance;
pub mod operations;
pub mod stats;

pub use stats::ManagerStats;

use super::config::WebRtcConfig;
use super::connection::{ConnectionState, WebRtcConnection};
use libp2p::PeerId;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};

/// WebRTC connection manager
pub struct WebRtcManager {
    connections: Arc<RwLock<HashMap<PeerId, WebRtcConnection>>>,
    config: WebRtcConfig,
    event_sender: mpsc::UnboundedSender<super::WebRtcEvent>,
    stats: Arc<RwLock<ManagerStats>>,
}

impl WebRtcManager {
    /// Create new WebRTC manager
    pub async fn new(
        config: &WebRtcConfig,
        event_sender: mpsc::UnboundedSender<super::WebRtcEvent>,
    ) -> Result<Self, String> {
        // Validate configuration
        config.validate().map_err(|e| format!("Config: {}", e))?;

        Ok(Self {
            connections: Arc::new(RwLock::new(HashMap::new())),
            config: config.clone(),
            event_sender,
            stats: Arc::new(RwLock::new(ManagerStats::default())),
        })
    }

    /// Start manager
    pub async fn start(&mut self) -> Result<(), String> {
        // Start background tasks for connection maintenance
        maintenance::start_maintenance_task(
            self.connections.clone(),
            self.event_sender.clone(),
            self.config.keep_alive_interval,
        )
        .await;
        Ok(())
    }

    /// Stop manager
    pub async fn stop(&mut self) -> Result<(), String> {
        // Close all connections
        let mut connections = self.connections.write().await;
        for (peer_id, connection) in connections.iter() {
            if let Err(e) = connection.close().await {
                eprintln!("Failed to close connection to {}: {}", peer_id, e);
            }
        }
        connections.clear();
        Ok(())
    }

    /// Create connection to peer (as offerer)
    pub async fn create_connection(&mut self, peer_id: PeerId) -> Result<(), String> {
        operations::create_connection(
            peer_id,
            &self.connections,
            &self.config,
            &self.event_sender,
            &self.stats,
        )
        .await
    }

    /// Accept connection from peer (as answerer)
    pub async fn accept_connection(
        &mut self,
        peer_id: PeerId,
        offer: String,
    ) -> Result<String, String> {
        operations::accept_connection(
            peer_id,
            offer,
            &self.connections,
            &self.config,
            &self.event_sender,
            &self.stats,
        )
        .await
    }

    /// Set answer for existing connection
    pub async fn set_answer(&mut self, peer_id: PeerId, answer: String) -> Result<(), String> {
        operations::set_answer(peer_id, answer, &self.connections).await
    }

    /// Send data through data channel
    pub async fn send_data(
        &mut self,
        peer_id: PeerId,
        channel_id: String,
        data: Vec<u8>,
    ) -> Result<(), String> {
        operations::send_data(peer_id, channel_id, data, &self.connections).await
    }

    /// Create data channel for existing connection
    pub async fn create_data_channel(
        &mut self,
        peer_id: PeerId,
        channel_id: String,
    ) -> Result<(), String> {
        operations::create_data_channel(peer_id, channel_id, &self.connections).await
    }

    /// Remove connection
    pub async fn remove_connection(&mut self, peer_id: PeerId) -> Result<(), String> {
        operations::remove_connection(peer_id, &self.connections).await
    }

    /// Get active connections
    pub async fn active_connections(&self) -> HashMap<PeerId, ConnectionState> {
        let connections = self.connections.read().await;
        let mut result = HashMap::new();

        for (peer_id, connection) in connections.iter() {
            result.insert(*peer_id, connection.state().await);
        }

        result
    }

    /// Get connection count
    pub async fn connection_count(&self) -> usize {
        self.connections.read().await.len()
    }

    /// Get WebRTC statistics
    pub async fn webrtc_stats(&self) -> super::WebRtcStats {
        let stats = self.stats.read().await;
        let active_connections = self.connection_count().await;

        super::WebRtcStats {
            active_connections,
            data_channels_open: 0, // Would need to aggregate from connections
            bytes_sent: stats.bytes_sent,
            bytes_received: stats.bytes_received,
            ice_candidates_gathered: stats.ice_candidates_gathered,
            connection_failures: stats.failed_connections,
        }
    }
}
