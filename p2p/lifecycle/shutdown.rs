use crate::p2p::{
    discovery::Discovery, manager::PeerManager, message::MessageService, transport::P2PTransport,
    webrtc::WebRtcService,
};
use anyhow::Result;
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::{debug, info};

/// Coordinator for P2P service shutdown sequence
pub struct ShutdownCoordinator {
    discovery: Arc<RwLock<Discovery>>,
    transport: Arc<RwLock<P2PTransport>>,
    webrtc: Arc<RwLock<Option<WebRtcService>>>,
    peer_manager: Arc<RwLock<PeerManager>>,
    message_service: Arc<RwLock<Option<MessageService>>>,
}

impl ShutdownCoordinator {
    /// Create new shutdown coordinator
    pub fn new(
        discovery: Arc<RwLock<Discovery>>,
        transport: Arc<RwLock<P2PTransport>>,
        webrtc: Arc<RwLock<Option<WebRtcService>>>,
        peer_manager: Arc<RwLock<PeerManager>>,
        message_service: Arc<RwLock<Option<MessageService>>>,
    ) -> Self {
        Self {
            discovery,
            transport,
            webrtc,
            peer_manager,
            message_service,
        }
    }

    /// Execute complete shutdown sequence
    pub async fn execute_shutdown_sequence(&self) -> Result<()> {
        info!("Starting P2P service shutdown");

        // Step 1: Close all WebRTC connections
        self.close_webrtc_connections().await.map_err(|e| {
            anyhow::anyhow!("Failed to close WebRTC connections during shutdown: {}", e)
        })?;

        // Step 2: Stop peer manager
        self.stop_peer_manager()
            .await
            .map_err(|e| anyhow::anyhow!("Failed to stop peer manager during shutdown: {}", e))?;

        // Step 3: Stop discovery service
        self.shutdown_discovery()
            .await
            .map_err(|e| anyhow::anyhow!("Failed to shutdown discovery service: {}", e))?;

        // Step 4: Stop transport layer
        self.stop_transport().await.map_err(|e| {
            anyhow::anyhow!("Failed to stop transport layer during shutdown: {}", e)
        })?;

        // Step 5: Flush persistence layer
        self.flush_persistence().await.map_err(|e| {
            anyhow::anyhow!("Failed to flush persistence layer during shutdown: {}", e)
        })?;

        info!("P2P service shutdown complete");
        Ok(())
    }

    /// Close all WebRTC connections
    async fn close_webrtc_connections(&self) -> Result<()> {
        debug!("Closing WebRTC connections");

        if let Some(webrtc) = self.webrtc.write().await.as_mut() {
            webrtc
                .stop()
                .await
                .map_err(|e| anyhow::anyhow!("Failed to stop WebRTC service: {}", e))?;
        }

        debug!("WebRTC connections closed");
        Ok(())
    }

    /// Stop peer manager
    async fn stop_peer_manager(&self) -> Result<()> {
        debug!("Stopping peer manager");

        self.peer_manager
            .write()
            .await
            .stop()
            .await
            .map_err(|e| anyhow::anyhow!("Failed to stop peer manager: {}", e))?;

        debug!("Peer manager stopped");
        Ok(())
    }

    /// Shutdown discovery service
    async fn shutdown_discovery(&self) -> Result<()> {
        debug!("Shutting down discovery service");

        self.discovery
            .write()
            .await
            .stop()
            .await
            .map_err(|e| anyhow::anyhow!("Failed to stop discovery service: {}", e))?;

        debug!("Discovery service shutdown");
        Ok(())
    }

    /// Stop transport layer
    async fn stop_transport(&self) -> Result<()> {
        debug!("Stopping transport layer");

        self.transport
            .write()
            .await
            .stop()
            .await
            .map_err(|e| anyhow::anyhow!("Failed to stop transport layer: {}", e))?;

        debug!("Transport layer stopped");
        Ok(())
    }

    /// Flush persistence layer
    async fn flush_persistence(&self) -> Result<()> {
        debug!("Flushing persistence layer");

        // Use message_service field to flush any pending operations
        if let Some(service) = self.message_service.write().await.as_mut() {
            service
                .flush_pending_messages()
                .await
                .map_err(|e| anyhow::anyhow!("Failed to flush pending messages: {}", e))?;
        }

        debug!("Persistence layer flushed");
        Ok(())
    }
}
