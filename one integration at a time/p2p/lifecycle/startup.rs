use crate::p2p::{
    config::NetworkConfig, discovery::Discovery, manager::PeerManager, message::MessageService,
    transport::P2PTransport, webrtc::WebRtcService,
};
use anyhow::Result;
use libp2p::identity::Keypair;
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};
use tracing::{debug, info};

/// Coordinator for P2P service startup sequence
pub struct StartupCoordinator {
    config: NetworkConfig,
    discovery: Arc<RwLock<Discovery>>,
    transport: Arc<RwLock<P2PTransport>>,
    webrtc: Arc<RwLock<Option<WebRtcService>>>,
    peer_manager: Arc<RwLock<PeerManager>>,
    message_service: Arc<RwLock<Option<MessageService>>>,
}

impl StartupCoordinator {
    /// Create new startup coordinator
    pub fn new(
        config: NetworkConfig,
        discovery: Arc<RwLock<Discovery>>,
        transport: Arc<RwLock<P2PTransport>>,
        webrtc: Arc<RwLock<Option<WebRtcService>>>,
        peer_manager: Arc<RwLock<PeerManager>>,
        message_service: Arc<RwLock<Option<MessageService>>>,
    ) -> Self {
        Self {
            config,
            discovery,
            transport,
            webrtc,
            peer_manager,
            message_service,
        }
    }

    /// Execute complete startup sequence
    pub async fn execute_startup_sequence(&self) -> Result<()> {
        info!("Starting P2P service initialization");

        // Step 1: Initialize discovery (mDNS + Kademlia)
        self.initialize_discovery().await.map_err(|e| {
            anyhow::anyhow!(
                "Failed to initialize discovery service during startup: {}",
                e
            )
        })?;

        // Step 2: Start transport layer (TCP + WebSocket)
        self.initialize_transport().await.map_err(|e| {
            anyhow::anyhow!("Failed to initialize transport layer during startup: {}", e)
        })?;

        // Step 3: Start peer manager
        self.initialize_peer_manager().await.map_err(|e| {
            anyhow::anyhow!("Failed to initialize peer manager during startup: {}", e)
        })?;

        // Step 4: Enable WebRTC data channels (if configured)
        if self.config.enable_webrtc {
            self.initialize_webrtc().await.map_err(|e| {
                anyhow::anyhow!("Failed to initialize WebRTC during startup: {}", e)
            })?;
        }

        // Step 5: Wire message routing
        self.initialize_messaging().await.map_err(|e| {
            anyhow::anyhow!(
                "Failed to initialize messaging system during startup: {}",
                e
            )
        })?;

        // Step 6: Connect to relay server (fallback)
        if self.config.use_relay_fallback {
            self.connect_relay().await.map_err(|e| {
                anyhow::anyhow!("Failed to connect to relay server during startup: {}", e)
            })?;
        }

        info!("P2P service initialization complete");
        Ok(())
    }

    /// Initialize discovery service
    async fn initialize_discovery(&self) -> Result<()> {
        debug!("Initializing discovery service");

        self.discovery
            .write()
            .await
            .start()
            .await
            .map_err(|e| anyhow::anyhow!("Discovery service start failed: {}", e))?;

        debug!("Discovery service initialized");
        Ok(())
    }

    /// Initialize transport layer
    async fn initialize_transport(&self) -> Result<()> {
        debug!("Initializing transport layer");

        self.transport
            .write()
            .await
            .start()
            .await
            .map_err(|e| anyhow::anyhow!("Transport layer start failed: {}", e))?;

        debug!("Transport layer initialized");
        Ok(())
    }

    /// Initialize peer manager
    async fn initialize_peer_manager(&self) -> Result<()> {
        debug!("Initializing peer manager");

        self.peer_manager
            .write()
            .await
            .start()
            .await
            .map_err(|e| anyhow::anyhow!("Peer manager start failed: {}", e))?;

        debug!("Peer manager initialized");
        Ok(())
    }

    /// Initialize WebRTC service
    async fn initialize_webrtc(&self) -> Result<()> {
        debug!("Initializing WebRTC service");

        let webrtc_config = self.config.to_webrtc_config();
        let (mut service, _receiver) = WebRtcService::new(webrtc_config)
            .await
            .map_err(|e| anyhow::anyhow!("Failed to create WebRTC service: {}", e))?;

        service
            .start()
            .await
            .map_err(|e| anyhow::anyhow!("Failed to start WebRTC service: {}", e))?;

        *self.webrtc.write().await = Some(service);

        debug!("WebRTC service initialized");
        Ok(())
    }

    /// Initialize messaging system
    async fn initialize_messaging(&self) -> Result<()> {
        debug!("Initializing messaging system");

        let keypair = Arc::new(Keypair::generate_ed25519());
        let config = crate::p2p::message::MessageConfig::default();

        // Create separate channel for MessageEvent
        let (message_event_sender, _message_event_receiver) = mpsc::unbounded_channel();

        let service = MessageService::new(config, keypair, message_event_sender)
            .await
            .map_err(|e| anyhow::anyhow!("Failed to create message service: {}", e))?;

        *self.message_service.write().await = Some(service);

        debug!("Messaging system initialized");
        Ok(())
    }

    /// Connect to relay server
    async fn connect_relay(&self) -> Result<()> {
        debug!("Connecting to relay server");

        if let Some(relay_url) = &self.config.relay_url {
            info!("Relay URL configured: {}", relay_url);
            // TODO: Implement actual relay connection
            // For now, just log that relay is configured
        } else {
            debug!("No relay URL configured, skipping relay connection");
        }

        debug!("Relay connection complete");
        Ok(())
    }
}
