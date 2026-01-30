use super::core::LifecycleState;
use crate::p2p::{manager::PeerManager, webrtc::WebRtcService};
use std::sync::Arc;
use tokio::sync::RwLock;

/// Health status of the P2P service
#[derive(Debug, Clone)]
pub struct HealthStatus {
    pub lifecycle_state: LifecycleState,
    pub discovery_active: bool,
    pub transport_connected: bool,
    pub webrtc_ready: bool,
    pub peer_count: usize,
}

/// Health monitoring operations for P2P service
pub struct HealthMonitor;

impl HealthMonitor {
    /// Check if discovery is active
    pub async fn is_discovery_active(lifecycle_state: Arc<RwLock<LifecycleState>>) -> bool {
        matches!(
            *lifecycle_state.read().await,
            LifecycleState::Running | LifecycleState::Degraded
        )
    }

    /// Check if transport is connected
    pub async fn is_transport_connected(lifecycle_state: Arc<RwLock<LifecycleState>>) -> bool {
        matches!(
            *lifecycle_state.read().await,
            LifecycleState::Running | LifecycleState::Degraded
        )
    }

    /// Check if WebRTC is ready
    pub async fn is_webrtc_ready(webrtc: Arc<RwLock<Option<WebRtcService>>>) -> bool {
        webrtc.read().await.is_some()
    }

    /// Get peer count
    pub async fn peer_count(peer_manager: Arc<RwLock<PeerManager>>) -> usize {
        peer_manager.read().await.peer_count().await
    }

    /// Get comprehensive health status
    pub async fn get_health_status(
        lifecycle_state: Arc<RwLock<LifecycleState>>,
        webrtc: Arc<RwLock<Option<WebRtcService>>>,
        peer_manager: Arc<RwLock<PeerManager>>,
    ) -> HealthStatus {
        let state = lifecycle_state.read().await.clone();

        HealthStatus {
            lifecycle_state: state,
            discovery_active: Self::is_discovery_active(Arc::clone(&lifecycle_state)).await,
            transport_connected: Self::is_transport_connected(Arc::clone(&lifecycle_state)).await,
            webrtc_ready: Self::is_webrtc_ready(Arc::clone(&webrtc)).await,
            peer_count: Self::peer_count(Arc::clone(&peer_manager)).await,
        }
    }
}
