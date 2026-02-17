#[path = "transport_integration_helpers.rs"]
mod transport_integration_helpers;

use crate::p2p::{
    events::{EventBus, P2PEventType},
    transport::P2PTransport,
    P2PEvent,
};
use anyhow::{Context, Result};
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};
use tracing::{debug, info};
use transport_integration_helpers::handle_connection_event;

/// Wire transport layer to event bus
pub async fn wire_transport_layer(
    transport: Arc<RwLock<P2PTransport>>,
    event_bus: Arc<EventBus>,
    mut p2p_event_receiver: mpsc::UnboundedReceiver<P2PEvent>,
) -> Result<()> {
    info!("Wiring transport layer to event bus");

    // Spawn task to forward transport events to event bus
    tokio::spawn(async move {
        while let Some(event) = p2p_event_receiver.recv().await {
            if let Err(e) = handle_transport_event(event, &event_bus, &transport).await {
                debug!("Error handling transport event: {}", e);
            }
        }
    });

    info!("Transport layer wired to event bus");
    Ok(())
}

/// Handle transport event
async fn handle_transport_event(
    event: P2PEvent,
    event_bus: &EventBus,
    transport: &Arc<RwLock<P2PTransport>>,
) -> Result<()> {
    match event {
        P2PEvent::PeerConnected { peer_id } => {
            handle_connection_established(peer_id, event_bus, transport).await?;
        }
        P2PEvent::PeerDisconnected { peer_id } => {
            handle_connection_lost(peer_id, event_bus, transport).await?;
        }
        P2PEvent::ConnectionFailed { peer_id, error } => {
            handle_connection_failed(peer_id, error, event_bus, transport).await?;
        }
        _ => {
            debug!("Ignoring non-transport event");
        }
    }

    Ok(())
}

/// Handle connection established event
async fn handle_connection_established(
    peer_id: libp2p::PeerId,
    event_bus: &EventBus,
    transport: &Arc<RwLock<P2PTransport>>,
) -> Result<()> {
    debug!("Connection established: {}", peer_id);

    // Update transport layer with new connection
    if let Ok(_t) = transport.try_write() {
        debug!("Updating transport layer with new peer: {}", peer_id);
        // TODO: Implement connection state update
        // In a full implementation, this would update connection state
    }

    event_bus
        .publish(P2PEventType::ConnectionEstablished { peer_id })
        .await
        .context("Failed to publish connection established event")?;

    Ok(())
}

/// Handle connection lost event
async fn handle_connection_lost(
    peer_id: libp2p::PeerId,
    event_bus: &EventBus,
    _transport: &Arc<RwLock<P2PTransport>>,
) -> Result<()> {
    debug!("Connection lost: {}", peer_id);

    event_bus
        .publish(P2PEventType::ConnectionLost { peer_id })
        .await
        .context("Failed to publish connection lost event")?;

    Ok(())
}

/// Handle connection failed event
async fn handle_connection_failed(
    peer_id: libp2p::PeerId,
    error: String,
    event_bus: &EventBus,
    _transport: &Arc<RwLock<P2PTransport>>,
) -> Result<()> {
    debug!("Connection failed: {} - {}", peer_id, error);

    event_bus
        .publish(P2PEventType::ComponentFailed {
            component: format!("transport:{}", peer_id),
        })
        .await
        .context("Failed to publish connection failed event")?;

    Ok(())
}

/// Configure transport event handlers
pub async fn configure_transport_events(
    transport: Arc<RwLock<P2PTransport>>,
    event_bus: Arc<EventBus>,
) -> Result<()> {
    debug!("Configuring transport event handlers");

    let mut receiver = event_bus.subscribe().await;

    tokio::spawn(async move {
        while let Ok(event) = receiver.recv().await {
            handle_connection_event(&event, &transport).await;
        }
    });

    debug!("Transport event handlers configured");
    Ok(())
}
