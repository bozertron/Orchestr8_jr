use super::health::HealthStatus;
use crate::p2p::{
    config::NetworkConfig, discovery::Discovery, manager::PeerManager, message::MessageService,
    transport::P2PTransport, webrtc::WebRtcService, P2PEvent,
};
use anyhow::Result;
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};
use tracing::info;

/// Lifecycle state of the P2P service
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum LifecycleState {
    /// Service not yet initialized
    Uninitialized,
    /// Service is starting up
    Starting,
    /// Service is running normally
    Running,
    /// Service is running but degraded (some components failed)
    Degraded,
    /// Service is shutting down
    Stopping,
    /// Service has stopped
    Stopped,
    /// Service has failed
    Failed(String),
}

/// P2P Service coordinator for lifecycle management
pub struct P2PService {
    config: NetworkConfig,
    discovery: Arc<RwLock<Discovery>>,
    transport: Arc<RwLock<P2PTransport>>,
    webrtc: Arc<RwLock<Option<WebRtcService>>>,
    peer_manager: Arc<RwLock<PeerManager>>,
    message_service: Arc<RwLock<Option<MessageService>>>,
    lifecycle_state: Arc<RwLock<LifecycleState>>,
    #[allow(dead_code)] // Used for event broadcasting in future
    event_sender: mpsc::UnboundedSender<P2PEvent>,
    event_receiver: Arc<RwLock<Option<mpsc::UnboundedReceiver<P2PEvent>>>>,
}

impl P2PService {
    /// Create new P2P service
    pub async fn new(config: NetworkConfig) -> Result<Self> {
        info!("Creating P2P service");
        let (event_sender, event_receiver) = mpsc::unbounded_channel();

        let transport = P2PTransport::new(&config)
            .await
            .map_err(|e| anyhow::anyhow!("Failed to create P2P transport layer: {}", e))?;
        let discovery = Discovery::new(&config, event_sender.clone())
            .await
            .map_err(|e| anyhow::anyhow!("Failed to create discovery service: {}", e))?;
        let peer_manager = PeerManager::new(&config, event_sender.clone())
            .await
            .map_err(|e| anyhow::anyhow!("Failed to create peer manager: {}", e))?;

        let webrtc = None;
        let message_service = None;
        info!("P2P service created successfully");

        Ok(Self {
            config,
            discovery: Arc::new(RwLock::new(discovery)),
            transport: Arc::new(RwLock::new(transport)),
            webrtc: Arc::new(RwLock::new(webrtc)),
            peer_manager: Arc::new(RwLock::new(peer_manager)),
            message_service: Arc::new(RwLock::new(message_service)),
            lifecycle_state: Arc::new(RwLock::new(LifecycleState::Uninitialized)),
            event_sender,
            event_receiver: Arc::new(RwLock::new(Some(event_receiver))),
        })
    }

    /// Start the P2P service
    pub async fn start(&self) -> Result<()> {
        info!("Starting P2P service");
        *self.lifecycle_state.write().await = LifecycleState::Starting;

        super::components::ComponentManager::start_transport(Arc::clone(&self.transport))
            .await
            .map_err(|e| anyhow::anyhow!("Failed to start transport layer: {}", e))?;
        super::components::ComponentManager::start_discovery(Arc::clone(&self.discovery))
            .await
            .map_err(|e| anyhow::anyhow!("Failed to start discovery service: {}", e))?;
        super::components::ComponentManager::start_peer_manager(Arc::clone(&self.peer_manager))
            .await
            .map_err(|e| anyhow::anyhow!("Failed to start peer manager: {}", e))?;

        if self.config.enable_webrtc {
            super::components::ComponentManager::start_webrtc(
                &self.config,
                Arc::clone(&self.webrtc),
            )
            .await
            .map_err(|e| anyhow::anyhow!("Failed to start WebRTC service: {}", e))?;
        }

        super::components::ComponentManager::initialize_message_service(Arc::clone(
            &self.message_service,
        ))
        .await
        .map_err(|e| anyhow::anyhow!("Failed to initialize message service: {}", e))?;

        *self.lifecycle_state.write().await = LifecycleState::Running;
        info!("P2P service started successfully");
        Ok(())
    }

    /// Shutdown the P2P service
    pub async fn shutdown(&self) -> Result<()> {
        info!("Shutting down P2P service");
        *self.lifecycle_state.write().await = LifecycleState::Stopping;

        super::shutdown::ShutdownCoordinator::execute_shutdown(
            Arc::clone(&self.webrtc),
            Arc::clone(&self.peer_manager),
            Arc::clone(&self.discovery),
            Arc::clone(&self.transport),
        )
        .await?;

        *self.lifecycle_state.write().await = LifecycleState::Stopped;
        info!("P2P service shutdown complete");
        Ok(())
    }

    /// Get current lifecycle state
    pub async fn lifecycle_state(&self) -> LifecycleState {
        self.lifecycle_state.read().await.clone()
    }

    /// Get health status of the service
    pub async fn health_status(&self) -> HealthStatus {
        super::health::HealthMonitor::get_health_status(
            Arc::clone(&self.lifecycle_state),
            Arc::clone(&self.webrtc),
            Arc::clone(&self.peer_manager),
        )
        .await
    }

    /// Send message through P2P service
    pub async fn send_message(
        &self,
        peer_id: libp2p::PeerId,
        text: String,
    ) -> Result<crate::p2p::message::MessageId> {
        super::operations::ServiceOperations::send_message(
            Arc::clone(&self.message_service),
            peer_id,
            text,
        )
        .await
    }

    /// Get MessageService for direct access (Task 3.3 integration)
    pub async fn message_service(&self) -> Result<Arc<RwLock<Option<MessageService>>>> {
        Ok(Arc::clone(&self.message_service))
    }

    /// Check if peer is connected
    pub async fn is_peer_connected(&self, peer_id: &libp2p::PeerId) -> Result<bool> {
        // Use event_sender to query peer connection status
        let peer_manager = self.peer_manager.read().await;
        Ok(peer_manager.is_peer_connected(peer_id).await)
    }

    /// Get current peer count
    pub async fn get_peer_count(&self) -> usize {
        let peer_manager = self.peer_manager.read().await;
        peer_manager.peer_count().await
    }

    /// Get event receiver for external event handling
    pub async fn take_event_receiver(&self) -> Option<mpsc::UnboundedReceiver<P2PEvent>> {
        self.event_receiver.write().await.take()
    }

    /// Create P2P service for testing
    pub fn new_for_testing() -> Self {
        let config = NetworkConfig::default();
        let (event_sender, event_receiver) = mpsc::unbounded_channel();

        Self {
            config,
            discovery: Arc::new(RwLock::new(Discovery::new_for_testing())),
            transport: Arc::new(RwLock::new(P2PTransport::new_for_testing())),
            webrtc: Arc::new(RwLock::new(None)),
            peer_manager: Arc::new(RwLock::new(PeerManager::new_for_testing())),
            message_service: Arc::new(RwLock::new(None)),
            lifecycle_state: Arc::new(RwLock::new(LifecycleState::Uninitialized)),
            event_sender,
            event_receiver: Arc::new(RwLock::new(Some(event_receiver))),
        }
    }
}
