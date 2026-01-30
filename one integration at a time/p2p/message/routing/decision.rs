mod cache;

use super::errors::RoutingError;
use super::TransportMethod;
use crate::p2p::manager::peer_ops::PeerOperations;
use crate::p2p::PeerManager;
use cache::{ConnectionCache, ConnectionStatus};
use libp2p::PeerId;
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::{debug, warn};

/// Routing decision engine for transport selection (Task 3.4 Priority 1)
pub struct RoutingDecisionEngine {
    peer_manager: Option<Arc<RwLock<PeerManager>>>,
    connection_cache: Arc<RwLock<ConnectionCache>>,
}

impl RoutingDecisionEngine {
    /// Create new routing decision engine
    pub fn new(peer_manager: Option<Arc<RwLock<PeerManager>>>) -> Self {
        Self {
            peer_manager,
            connection_cache: Arc::new(RwLock::new(ConnectionCache::new())),
        }
    }

    /// Select best transport for peer based on connection status
    pub async fn select_best_transport(&self, peer_id: &PeerId) -> Result<TransportMethod, String> {
        debug!("Selecting best transport for peer: {}", peer_id);

        // Check WebRTC connection (Priority 1: lowest latency)
        match self.check_webrtc_connection(peer_id).await {
            Ok(true) => {
                debug!("Selected WebRTC transport for {}", peer_id);
                return Ok(TransportMethod::WebRTC(format!("channel_{}", peer_id)));
            }
            Err(e) => {
                warn!("WebRTC check failed for {}: {}", peer_id, e);
            }
            _ => {}
        }

        // Check libp2p connection (Priority 2: reliable fallback)
        match self.check_libp2p_connection(peer_id).await {
            Ok(true) => {
                debug!("Selected libp2p transport for {}", peer_id);
                return Ok(TransportMethod::LibP2P);
            }
            Err(e) => {
                warn!("libp2p check failed for {}: {}", peer_id, e);
            }
            _ => {}
        }

        // Fallback to relay (Priority 3: NAT traversal)
        warn!("No direct connection to {}, using relay", peer_id);

        // Check if relay is available
        if self.is_relay_available().await {
            Ok(TransportMethod::Relay("relay.jfdi.local".to_string()))
        } else {
            Err(format!(
                "{}",
                RoutingError::NoTransportAvailable(peer_id.to_string())
            ))
        }
    }

    /// Check WebRTC connection status
    async fn check_webrtc_connection(&self, peer_id: &PeerId) -> Result<bool, String> {
        // Check cache first
        if let Some(status) = self.get_cached_webrtc_status(peer_id).await {
            return Ok(status.is_connected);
        }

        // TODO: Implement actual WebRTC connection check
        // For now, return false (will be implemented when WebRTC service is integrated)
        let is_connected = false;

        // Update cache
        self.update_webrtc_cache(peer_id, is_connected, None).await;

        Ok(is_connected)
    }

    /// Check libp2p connection status
    async fn check_libp2p_connection(&self, peer_id: &PeerId) -> Result<bool, String> {
        // Check cache first
        if let Some(status) = self.get_cached_libp2p_status(peer_id).await {
            return Ok(status.is_connected);
        }

        // Check actual connection via PeerManager
        let is_connected = if let Some(ref pm) = self.peer_manager {
            let mgr = pm.read().await;
            // Check if peer is in connected peers list
            let connected_peers = mgr.connected_peers().await;
            connected_peers.contains_key(peer_id)
        } else {
            false
        };

        // Update cache
        self.update_libp2p_cache(peer_id, is_connected, None).await;

        Ok(is_connected)
    }

    /// Check if relay server is available
    async fn is_relay_available(&self) -> bool {
        // For now, assume relay is always available
        // In a full implementation, this would ping the relay server
        true
    }

    /// Get cached WebRTC status
    async fn get_cached_webrtc_status(&self, peer_id: &PeerId) -> Option<ConnectionStatus> {
        let cache = self.connection_cache.read().await;
        cache.get_webrtc_status(peer_id)
    }

    /// Get cached libp2p status
    async fn get_cached_libp2p_status(&self, peer_id: &PeerId) -> Option<ConnectionStatus> {
        let cache = self.connection_cache.read().await;
        cache.get_libp2p_status(peer_id)
    }

    /// Update WebRTC cache
    async fn update_webrtc_cache(
        &self,
        peer_id: &PeerId,
        is_connected: bool,
        latency_ms: Option<u64>,
    ) {
        let mut cache = self.connection_cache.write().await;
        cache.update_webrtc_status(*peer_id, is_connected, latency_ms);
    }

    /// Update libp2p cache
    async fn update_libp2p_cache(
        &self,
        peer_id: &PeerId,
        is_connected: bool,
        latency_ms: Option<u64>,
    ) {
        let mut cache = self.connection_cache.write().await;
        cache.update_libp2p_status(*peer_id, is_connected, latency_ms);
    }

    /// Clear cache for peer (call when connection status changes)
    pub async fn invalidate_cache(&self, peer_id: &PeerId) {
        let mut cache = self.connection_cache.write().await;
        cache.invalidate_peer(peer_id);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_routing_decision_engine_creation() {
        let engine = RoutingDecisionEngine::new(None);
        // Engine created successfully
    }

    #[tokio::test]
    async fn test_select_best_transport_no_connections() {
        let engine = RoutingDecisionEngine::new(None);
        let peer_id = PeerId::random();

        let result = engine.select_best_transport(&peer_id).await;
        assert!(result.is_ok());

        // Should fallback to relay when no connections available
        match result.unwrap() {
            TransportMethod::Relay(_) => {} // Expected
            _ => panic!("Expected Relay transport"),
        }
    }
}
