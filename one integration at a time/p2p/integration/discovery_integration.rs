use crate::p2p::{
    discovery::Discovery,
    events::{EventBus, P2PEventType},
    P2PEvent,
};
use anyhow::{Context, Result};
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};
use tracing::{debug, info};

/// Wire discovery service to event bus
pub async fn wire_discovery_service(
    _discovery: Arc<RwLock<Discovery>>,
    event_bus: Arc<EventBus>,
    mut p2p_event_receiver: mpsc::UnboundedReceiver<P2PEvent>,
) -> Result<()> {
    info!("Wiring discovery service to event bus");

    // Spawn task to forward discovery events to event bus
    tokio::spawn(async move {
        while let Some(event) = p2p_event_receiver.recv().await {
            if let Err(e) = handle_discovery_event(event, &event_bus).await {
                debug!("Error handling discovery event: {}", e);
            }
        }
    });

    info!("Discovery service wired to event bus");
    Ok(())
}

/// Handle discovery event
async fn handle_discovery_event(event: P2PEvent, event_bus: &EventBus) -> Result<()> {
    match event {
        P2PEvent::PeerDiscovered { peer_id, .. } => {
            handle_peer_discovered(peer_id, event_bus).await?;
        }
        P2PEvent::PeerDisconnected { peer_id } => {
            handle_peer_lost(peer_id, event_bus).await?;
        }
        _ => {
            debug!("Ignoring non-discovery event");
        }
    }

    Ok(())
}

/// Handle peer discovered event
async fn handle_peer_discovered(peer_id: libp2p::PeerId, event_bus: &EventBus) -> Result<()> {
    debug!("Peer discovered: {}", peer_id);

    event_bus
        .publish(P2PEventType::PeerDiscovered { peer_id })
        .await
        .context("Failed to publish peer discovered event")?;

    Ok(())
}

/// Handle peer lost event
async fn handle_peer_lost(peer_id: libp2p::PeerId, event_bus: &EventBus) -> Result<()> {
    debug!("Peer lost: {}", peer_id);

    event_bus
        .publish(P2PEventType::PeerLost { peer_id })
        .await
        .context("Failed to publish peer lost event")?;

    Ok(())
}

/// Configure discovery event handlers
pub async fn configure_discovery_events(
    _discovery: Arc<RwLock<Discovery>>,
    event_bus: Arc<EventBus>,
) -> Result<()> {
    debug!("Configuring discovery event handlers");

    // Subscribe to event bus for discovery-related events
    let mut receiver = event_bus.subscribe().await;

    // Spawn task to handle events
    tokio::spawn(async move {
        while let Ok(event) = receiver.recv().await {
            match event {
                P2PEventType::PeerDiscovered { peer_id } => {
                    debug!("Discovery handler received peer discovered: {}", peer_id);
                    // Additional discovery-specific handling can go here
                }
                P2PEventType::PeerLost { peer_id } => {
                    debug!("Discovery handler received peer lost: {}", peer_id);
                    // Additional discovery-specific handling can go here
                }
                _ => {}
            }
        }
    });

    debug!("Discovery event handlers configured");
    Ok(())
}
