//! Peer Manager Core - Coordination and API
//! Handles peer manager initialization, start/stop, and core API

use super::{connection::PeerConnection, stats::PeerManagerStats};
use crate::p2p::{NetworkConfig, P2PEvent};
use libp2p::PeerId;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};

/// Peer connection manager core
pub struct PeerManager {
    peers: Arc<RwLock<HashMap<PeerId, PeerConnection>>>,
    config: NetworkConfig,
    event_sender: mpsc::UnboundedSender<P2PEvent>,
    stats: Arc<RwLock<PeerManagerStats>>,
}

impl PeerManager {
    /// Create new peer manager
    pub async fn new(
        config: &NetworkConfig,
        event_sender: mpsc::UnboundedSender<P2PEvent>,
    ) -> Result<Self, String> {
        Ok(Self {
            peers: Arc::new(RwLock::new(HashMap::new())),
            config: config.clone(),
            event_sender,
            stats: Arc::new(RwLock::new(PeerManagerStats::default())),
        })
    }

    /// Start peer manager
    pub async fn start(&mut self) -> Result<(), String> {
        // Start connection maintenance task
        super::maintenance::start_maintenance_task(
            self.peers.clone(),
            self.config.clone(),
            self.event_sender.clone(),
        )
        .await;
        Ok(())
    }

    /// Stop peer manager
    pub async fn stop(&mut self) -> Result<(), String> {
        let peers_guard = self.peers.read().await;
        for (peer_id, _connection) in peers_guard.iter() {
            // In real implementation, would disconnect properly
            let _ = self
                .send_event(P2PEvent::PeerDisconnected { peer_id: *peer_id })
                .await;
        }
        // Clear peers
        self.peers.write().await.clear();
        Ok(())
    }

    /// Get manager statistics
    pub async fn get_stats(&self) -> PeerManagerStats {
        self.stats.read().await.clone()
    }

    /// Send event (helper method)
    async fn send_event(&self, event: P2PEvent) -> Result<(), String> {
        self.event_sender
            .send(event)
            .map_err(|_| format!("Connection: {}", "Failed to send event".to_string()))?;
        Ok(())
    }

    /// Get peers map for operations (accessor for trait implementations)
    pub(crate) fn peers(&self) -> &Arc<RwLock<HashMap<PeerId, PeerConnection>>> {
        &self.peers
    }

    /// Get stats for operations (accessor for trait implementations)
    pub(crate) fn stats(&self) -> &Arc<RwLock<PeerManagerStats>> {
        &self.stats
    }

    /// Get config (accessor for trait implementations)
    pub(crate) fn config(&self) -> &NetworkConfig {
        &self.config
    }

    /// Get event sender for operations (accessor for trait implementations)
    pub(crate) fn event_sender(&self) -> &mpsc::UnboundedSender<P2PEvent> {
        &self.event_sender
    }

    /// Validate peer against configuration
    pub async fn validate_peer_config(&self, peer_id: &PeerId) -> bool {
        let _config = self.config();
        // Check if peer is in allowed list (if configured)
        // For now, return true - can be enhanced with actual validation
        tracing::debug!("Validating peer {} against config", peer_id);
        true
    }

    /// Get maximum peers from config
    pub fn get_max_peers(&self) -> usize {
        let config = self.config();
        config.max_peers
    }

    /// Get current peer count
    pub async fn peer_count(&self) -> usize {
        let peers = self.peers.read().await;
        peers.len()
    }

    /// Check if specific peer is connected
    pub async fn is_peer_connected(&self, peer_id: &PeerId) -> bool {
        let peers = self.peers.read().await;
        peers.contains_key(peer_id)
    }

    /// Create peer manager for testing
    pub fn new_for_testing() -> Self {
        let (event_sender, _) = mpsc::unbounded_channel();
        Self {
            peers: Arc::new(RwLock::new(HashMap::new())),
            config: NetworkConfig::default(),
            event_sender,
            stats: Arc::new(RwLock::new(PeerManagerStats::default())),
        }
    }
}
