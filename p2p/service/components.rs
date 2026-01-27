use crate::p2p::{
    config::NetworkConfig, discovery::Discovery, manager::PeerManager, message::MessageService,
    transport::P2PTransport, webrtc::WebRtcService,
};
use anyhow::Result;
use libp2p::identity::Keypair;
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};
use tracing::debug;

/// Component management operations for P2P service
pub struct ComponentManager;

impl ComponentManager {
    /// Start transport layer
    pub async fn start_transport(transport: Arc<RwLock<P2PTransport>>) -> Result<()> {
        debug!("Starting transport layer");
        transport
            .write()
            .await
            .start()
            .await
            .map_err(|e| anyhow::anyhow!("Transport layer start failed: {}", e))?;
        Ok(())
    }

    /// Start discovery service
    pub async fn start_discovery(discovery: Arc<RwLock<Discovery>>) -> Result<()> {
        debug!("Starting discovery service");
        discovery
            .write()
            .await
            .start()
            .await
            .map_err(|e| anyhow::anyhow!("Discovery service start failed: {}", e))?;
        Ok(())
    }

    /// Start peer manager
    pub async fn start_peer_manager(peer_manager: Arc<RwLock<PeerManager>>) -> Result<()> {
        debug!("Starting peer manager");
        peer_manager
            .write()
            .await
            .start()
            .await
            .map_err(|e| anyhow::anyhow!("Peer manager start failed: {}", e))?;
        Ok(())
    }

    /// Start WebRTC service
    pub async fn start_webrtc(
        config: &NetworkConfig,
        webrtc: Arc<RwLock<Option<WebRtcService>>>,
    ) -> Result<()> {
        debug!("Starting WebRTC service");

        let webrtc_config = config.to_webrtc_config();
        let (mut service, _receiver) = WebRtcService::new(webrtc_config)
            .await
            .map_err(|e| anyhow::anyhow!("Failed to create WebRTC service: {}", e))?;

        service
            .start()
            .await
            .map_err(|e| anyhow::anyhow!("Failed to start WebRTC service: {}", e))?;

        *webrtc.write().await = Some(service);
        Ok(())
    }

    /// Initialize message service
    pub async fn initialize_message_service(
        message_service: Arc<RwLock<Option<MessageService>>>,
    ) -> Result<()> {
        debug!("Initializing message service");

        let keypair = Arc::new(Keypair::generate_ed25519());
        let config = crate::p2p::message::MessageConfig::default();

        // Create separate channel for MessageEvent
        let (message_event_sender, _message_event_receiver) = mpsc::unbounded_channel();

        let service = MessageService::new(config, keypair, message_event_sender)
            .await
            .map_err(|e| anyhow::anyhow!("Failed to create message service: {}", e))?;

        *message_service.write().await = Some(service);
        Ok(())
    }
}
