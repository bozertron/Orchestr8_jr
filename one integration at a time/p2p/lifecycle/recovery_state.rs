// Recovery State Restoration
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines
// Solves: State restoration logic separated from core recovery coordinator

use crate::p2p::{
    config::NetworkConfig, discovery::Discovery, manager::PeerManager, message::MessageService,
    transport::P2PTransport, webrtc::WebRtcService,
};
use anyhow::Result;
use libp2p::identity::Keypair;
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};
use tracing::{debug, info};

/// Recover discovery service
pub async fn recover_discovery(discovery: &Arc<RwLock<Discovery>>) -> Result<()> {
    debug!("Recovering discovery service");

    let mut discovery_guard = discovery.write().await;

    // Stop existing discovery
    let _ = discovery_guard.stop().await;

    // Restart discovery
    discovery_guard
        .start()
        .await
        .map_err(|e| anyhow::anyhow!("Failed to restart discovery service: {}", e))?;

    info!("Discovery service recovered");
    Ok(())
}

/// Recover transport layer
pub async fn recover_transport(transport: &Arc<RwLock<P2PTransport>>) -> Result<()> {
    debug!("Recovering transport layer");

    let mut transport_guard = transport.write().await;

    // Stop existing transport
    let _ = transport_guard.stop().await;

    // Restart transport
    transport_guard
        .start()
        .await
        .map_err(|e| anyhow::anyhow!("Failed to restart transport layer: {}", e))?;

    info!("Transport layer recovered");
    Ok(())
}

/// Recover WebRTC service
pub async fn recover_webrtc(
    webrtc: &Arc<RwLock<Option<WebRtcService>>>,
    config: &NetworkConfig,
) -> Result<()> {
    debug!("Recovering WebRTC service");

    let mut webrtc_guard = webrtc.write().await;

    // Stop existing WebRTC
    if let Some(webrtc_service) = webrtc_guard.as_mut() {
        let _ = webrtc_service.stop().await;
    }

    // Create new WebRTC service
    let webrtc_config = config.to_webrtc_config();
    let (mut service, _receiver) = WebRtcService::new(webrtc_config)
        .await
        .map_err(|e| anyhow::anyhow!("Failed to create WebRTC service during recovery: {}", e))?;

    service
        .start()
        .await
        .map_err(|e| anyhow::anyhow!("Failed to start WebRTC service during recovery: {}", e))?;

    *webrtc_guard = Some(service);

    info!("WebRTC service recovered");
    Ok(())
}

/// Recover peer manager
pub async fn recover_peer_manager(peer_manager: &Arc<RwLock<PeerManager>>) -> Result<()> {
    debug!("Recovering peer manager");

    let mut peer_manager_guard = peer_manager.write().await;

    // Stop existing peer manager
    let _ = peer_manager_guard.stop().await;

    // Restart peer manager
    peer_manager_guard
        .start()
        .await
        .map_err(|e| anyhow::anyhow!("Failed to restart peer manager during recovery: {}", e))?;

    info!("Peer manager recovered");
    Ok(())
}

/// Recover message service
pub async fn recover_message_service(
    message_service: &Arc<RwLock<Option<MessageService>>>,
) -> Result<()> {
    debug!("Recovering message service");

    let keypair = Arc::new(Keypair::generate_ed25519());
    let config = crate::p2p::message::MessageConfig::default();

    // Create separate channel for MessageEvent
    let (message_event_sender, _message_event_receiver) = mpsc::unbounded_channel();

    let service = MessageService::new(config, keypair, message_event_sender)
        .await
        .map_err(|e| anyhow::anyhow!("Failed to create message service during recovery: {}", e))?;

    *message_service.write().await = Some(service);

    info!("Message service recovered");
    Ok(())
}
