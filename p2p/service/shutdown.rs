use crate::p2p::{
    discovery::Discovery, manager::PeerManager, transport::P2PTransport, webrtc::WebRtcService,
};
use anyhow::Result;
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::info;

/// Shutdown coordinator for P2P service
pub struct ShutdownCoordinator;

impl ShutdownCoordinator {
    /// Execute graceful shutdown sequence
    pub async fn execute_shutdown(
        webrtc: Arc<RwLock<Option<WebRtcService>>>,
        peer_manager: Arc<RwLock<PeerManager>>,
        discovery: Arc<RwLock<Discovery>>,
        transport: Arc<RwLock<P2PTransport>>,
    ) -> Result<()> {
        info!("Executing P2P service shutdown sequence");

        // Stop WebRTC connections
        Self::stop_webrtc(webrtc).await?;

        // Stop peer manager
        Self::stop_peer_manager(peer_manager).await?;

        // Stop discovery
        Self::stop_discovery(discovery).await?;

        // Stop transport
        Self::stop_transport(transport).await?;

        info!("P2P service shutdown sequence complete");
        Ok(())
    }

    /// Stop WebRTC service
    async fn stop_webrtc(webrtc: Arc<RwLock<Option<WebRtcService>>>) -> Result<()> {
        if let Some(webrtc_service) = webrtc.write().await.as_mut() {
            webrtc_service
                .stop()
                .await
                .map_err(|e| anyhow::anyhow!("Failed to stop WebRTC service: {}", e))?;
        }
        Ok(())
    }

    /// Stop peer manager
    async fn stop_peer_manager(peer_manager: Arc<RwLock<PeerManager>>) -> Result<()> {
        peer_manager
            .write()
            .await
            .stop()
            .await
            .map_err(|e| anyhow::anyhow!("Failed to stop peer manager: {}", e))?;
        Ok(())
    }

    /// Stop discovery service
    async fn stop_discovery(discovery: Arc<RwLock<Discovery>>) -> Result<()> {
        discovery
            .write()
            .await
            .stop()
            .await
            .map_err(|e| anyhow::anyhow!("Failed to stop discovery service: {}", e))?;
        Ok(())
    }

    /// Stop transport layer
    async fn stop_transport(transport: Arc<RwLock<P2PTransport>>) -> Result<()> {
        transport
            .write()
            .await
            .stop()
            .await
            .map_err(|e| anyhow::anyhow!("Failed to stop transport layer: {}", e))?;
        Ok(())
    }
}
